# Atlassian REST API Reference

All project tracking, documentation, and IP lives in Atlassian.

| Tool | URL | Purpose |
|------|-----|---------|
| Jira | `https://contoso.atlassian.net/jira/for-you` | Work tracking, epics, stories, sprints |
| Confluence | `https://contoso.atlassian.net/wiki/home` | Collaboration docs, specs, design docs, IP |

## Authentication

API calls require basic auth with an Atlassian API token:

- **User:** `$ATLASSIAN_USER` (your email address)
- **Token:** `$ATLASSIAN_TOKEN` (personal API token from <https://id.atlassian.com/manage-profile/security/api-tokens>)

Store these as environment variables. Never hardcode credentials.

> **IMPORTANT:** `curl -u "$ATLASSIAN_USER:$ATLASSIAN_TOKEN"` does NOT work
> because the API token contains characters that break curl's credential parser.
> Always construct the Basic auth header manually using Python:

```bash
# Set auth header (run once per shell session)
AUTH_HEADER=$(python3 -c "import base64, os; u=os.environ['ATLASSIAN_USER']; t=os.environ['ATLASSIAN_TOKEN']; print(base64.b64encode(f'{u}:{t}'.encode()).decode())")
```

## Jira REST API

Base URL: `https://contoso.atlassian.net/rest/api/3`

```bash
# Get an issue (epic, story, etc.)
curl -s -H "Authorization: Basic $AUTH_HEADER" -H "Accept: application/json" \
  "https://contoso.atlassian.net/rest/api/3/issue/PROJ-123" | jq .

# Search issues (JQL)
curl -s -H "Authorization: Basic $AUTH_HEADER" -H "Accept: application/json" \
  --data-urlencode "jql=project = PROJ AND type = Epic AND status != Done" \
  "https://contoso.atlassian.net/rest/api/3/search" | jq .

# Get all stories under an epic
curl -s -H "Authorization: Basic $AUTH_HEADER" -H "Accept: application/json" \
  --data-urlencode "jql='Epic Link' = PROJ-123" \
  "https://contoso.atlassian.net/rest/api/3/search" | jq .

# Add a comment to an issue
curl -s -H "Authorization: Basic $AUTH_HEADER" -H "Accept: application/json" \
  -X POST -H "Content-Type: application/json" \
  -d '{"body":{"type":"doc","version":1,"content":[{"type":"paragraph","content":[{"type":"text","text":"Comment text here"}]}]}}' \
  "https://contoso.atlassian.net/rest/api/3/issue/PROJ-123/comment"
```

## Confluence REST API

Base URL: `https://contoso.atlassian.net/wiki/rest/api`

```bash
# Search for a page by title
curl -s -H "Authorization: Basic $AUTH_HEADER" -H "Accept: application/json" \
  --data-urlencode "cql=title = 'Page Title' AND type = page" \
  "https://contoso.atlassian.net/wiki/rest/api/content/search" | jq .

# Get page content (expand body.storage for HTML)
curl -s -H "Authorization: Basic $AUTH_HEADER" -H "Accept: application/json" \
  "https://contoso.atlassian.net/wiki/rest/api/content/PAGE_ID?expand=body.storage" | jq .

# Search across all spaces
curl -s -H "Authorization: Basic $AUTH_HEADER" -H "Accept: application/json" \
  --data-urlencode "cql=text ~ 'search term' AND type = page" \
  "https://contoso.atlassian.net/wiki/rest/api/content/search" | jq .
```
