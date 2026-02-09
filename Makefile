.PHONY: lint-md check-structure

lint-md:
	@echo "markdown lint placeholder (wire to markdownlint/prettier if desired)"

check-structure:
	@test -d skills
	@test -d learnings/daily
	@test -d learnings/weekly
	@test -d docs/playbooks
	@test -d docs/adr
	@echo "Repository structure looks good."
