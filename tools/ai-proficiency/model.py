"""Fixed, regularized probability model; developer-grouped nested calibration."""
import numpy as np
import pandas as pd
from scipy.optimize import minimize_scalar
from scipy.special import softmax
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, f1_score, log_loss
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from prepare import AI

LEVELS = np.arange(1, 5)


class InsufficientEvidence(ValueError):
    pass


def features(frame):
    # Fixed whitelist excludes identifiers, survey fields, role, spend and productivity.
    return np.log1p(frame[AI].astype(float)).to_numpy()


def pipeline():
    return make_pipeline(SimpleImputer(strategy='median', add_indicator=True, keep_empty_features=True),
                         StandardScaler(), LogisticRegression(C=0.3, max_iter=2000))


def splits(y, groups, n=3, seed=42):
    counts = pd.DataFrame({'y': y, 'g': groups}).drop_duplicates().groupby('y').size()
    if set(counts.index) != set(LEVELS) or counts.min() < n:
        raise InsufficientEvidence('Every class needs developers in each fold')
    cv = list(StratifiedGroupKFold(n_splits=n, shuffle=True, random_state=seed).split(np.zeros(len(y)), y, groups))
    for train, test in cv:
        if set(np.asarray(groups)[train]) & set(np.asarray(groups)[test]):
            raise AssertionError('Developer leakage')
        if set(np.asarray(y)[train]) != set(LEVELS) or set(np.asarray(y)[test]) != set(LEVELS):
            raise InsufficientEvidence('A grouped fold lacks a class')
    return cv


def temperature_scale(p, temperature):
    return softmax(np.log(np.clip(p, 1e-12, 1)) / temperature, axis=1)


class CalibratedModel:
    def fit(self, frame):
        y = frame.label.to_numpy(dtype=int)
        x = features(frame)
        if len(frame) < 80 or frame.groupby('label').username.nunique().min() < 12:
            raise InsufficientEvidence('Need 80 labeled rows and 12 developers per class in model-fitting data')
        oof = np.full((len(y), 4), np.nan)
        for train, test in splits(y, frame.username.to_numpy()):
            estimator = pipeline().fit(x[train], y[train])
            oof[test] = estimator.predict_proba(x[test])
        fit = minimize_scalar(lambda t: log_loss(y, temperature_scale(oof, t), labels=LEVELS),
                              bounds=(0.5, 5), method='bounded')
        if not fit.success:
            raise InsufficientEvidence('Temperature optimization failed')
        self.temperature = float(fit.x)
        self.estimator = pipeline().fit(x, y)
        self.prior = (np.bincount(y, minlength=5)[1:] + 1) / (len(y) + 4)
        self.minimum = frame[AI].min()
        self.maximum = frame[AI].max()
        self.missing_pattern = frame[AI].isna().all()
        self.training_users = set(frame.username)
        return self

    def predict(self, frame):
        return temperature_scale(self.estimator.predict_proba(features(frame)), self.temperature)

    def out_of_support(self, frame):
        raw = frame[AI]
        beyond = raw.lt(self.minimum) | raw.gt(self.maximum)
        # A new missing or newly present metric also changes the feature regime.
        novel_missing = raw.isna() & self.minimum.notna()
        novel_present = raw.notna() & self.missing_pattern
        return (beyond | novel_missing | novel_present).any(axis=1).to_numpy()


def brier_rows(y, p):
    return ((p - np.eye(4)[np.asarray(y, dtype=int) - 1]) ** 2).sum(axis=1)


def metrics(y, p, weights=None):
    y = np.asarray(y, dtype=int)
    pred = LEVELS[p.argmax(axis=1)]
    truth_cdf = np.cumsum(np.eye(4)[y - 1], axis=1)[:, :-1]
    rps = ((np.cumsum(p, axis=1)[:, :-1] - truth_cdf) ** 2).mean(axis=1)
    return {'n': len(y), 'log_loss': float(log_loss(y, p, labels=LEVELS, sample_weight=weights)),
            'brier': float(np.average(brier_rows(y, p), weights=weights)),
            'ranked_probability_score': float(np.average(rps, weights=weights)),
            'accuracy': float(np.average(pred == y, weights=weights)),
            'mae': float(np.average(np.abs(pred - y), weights=weights)),
            'macro_f1': float(f1_score(y, pred, labels=LEVELS, average='macro', zero_division=0, sample_weight=weights)),
            'confusion_matrix': confusion_matrix(y, pred, labels=LEVELS, sample_weight=weights).tolist()}


def reliability(y, p):
    y = np.asarray(y, dtype=int)
    rows = []
    for level in LEVELS:
        prob = p[:, level - 1]
        bins = np.minimum((prob * 5).astype(int), 4)
        for b in range(5):
            mask = bins == b
            if mask.any():
                rows.append({'level': int(level), 'bin': b, 'n': int(mask.sum()),
                             'mean_probability': float(prob[mask].mean()),
                             'observed_frequency': float((y[mask] == level).mean())})
    table = pd.DataFrame(rows)
    table['gap'] = abs(table.mean_probability - table.observed_frequency)
    ece = table.groupby('level').apply(lambda t: float(np.average(t.gap, weights=t.n)), include_groups=False)
    return table, {str(k): float(v) for k, v in ece.items()}


def paired_brier_interval(y, p, baseline, groups, repeats=500, seed=42):
    """Cluster bootstrap of fixed held-out errors; excludes refit and selection uncertainty."""
    differences = brier_rows(y, p) - brier_rows(y, baseline)
    rng = np.random.default_rng(seed)
    groups = np.asarray(groups)
    unique = np.unique(groups)
    positions = {g: np.flatnonzero(groups == g) for g in unique}
    samples = [differences[np.concatenate([positions[g] for g in rng.choice(unique, len(unique), replace=True)])].mean()
               for _ in range(repeats)]
    return {'mean': float(differences.mean()), 'lower': float(np.quantile(samples, .025)),
            'upper': float(np.quantile(samples, .975)), 'repeats': repeats}


def nested_oof(frame):
    y = frame.label.to_numpy(dtype=int)
    p = np.full((len(frame), 4), np.nan)
    prior = p.copy()
    folds = np.zeros(len(frame), dtype=int)
    for fold, (train, test) in enumerate(splits(y, frame.username.to_numpy())):
        fitted = CalibratedModel().fit(frame.iloc[train])
        p[test] = fitted.predict(frame.iloc[test])
        prior[test] = fitted.prior
        folds[test] = fold
    return p, prior, folds


def release_gate(y, p, baseline, groups):
    table, ece = reliability(y, p)
    interval = paired_brier_interval(y, p, baseline, groups)
    counts = np.bincount(np.asarray(y, dtype=int), minlength=5)[1:]
    matrix = confusion_matrix(y, LEVELS[p.argmax(axis=1)], labels=LEVELS)
    recall = np.divide(np.diag(matrix), matrix.sum(axis=1), out=np.zeros(4), where=matrix.sum(axis=1) > 0)
    reasons = []
    if len(y) < 80 or counts.min() < 10:
        reasons.append('insufficient_temporal_validation_support')
    if interval['upper'] >= 0:
        reasons.append('no_clear_brier_improvement_over_prior')
    if max(ece.values()) > .10:
        reasons.append('classwise_calibration_gap_above_0.10')
    if recall.min() < .35:
        reasons.append('class_recall_below_0.35')
    return {'passed': not reasons, 'reasons': reasons, 'paired_brier_95_interval': interval,
            'classwise_ece': ece, 'class_recall': recall.tolist()}, table
