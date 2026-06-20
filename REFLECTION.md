# REFLECTION

## What does each stage of the pipeline protect against?

The **lint stage** (`black --check` and `flake8`) protects against inconsistent
code formatting and style violations — it ensures all code follows the same
standards before anything else runs, catching obvious issues like unused imports
or inconsistent spacing that would otherwise clutter code reviews.
The **test stage** (`pytest`) protects against functional regressions — it
verifies that every endpoint behaves correctly and that new changes haven't
broken existing functionality. The **deploy stage** protects the production
environment by ensuring that only code which has already passed both lint and
tests actually reaches users; it acts as the final gate before anything goes live.

## Why does the order matter?

The order matters critically: if `deploy` ran before `test`, broken or
untested code could reach production and cause real failures for users before
anyone noticed the problem. The entire value of a CI/CD pipeline is that errors
are caught as early and cheaply as possible — fixing a bug in development costs
minutes, but fixing one in production can cost hours of downtime, data issues,
or lost user trust. By gating `deploy` on `test` with `needs: test`, we
guarantee that deployment only happens when we have confidence the code works.

## What would I add to make this closer to a real production setup?

I would add a **test coverage threshold** (e.g. `pytest --cov=main --cov-fail-under=80`)
so the pipeline fails if coverage drops below 80%, ensuring new features are
always tested. I would also replace the simulated deploy step with a real
deployment to a platform like Render or Railway using an API key stored as a
GitHub Secret, and add a **notification step** (Slack or email) that alerts the
team whenever a deployment succeeds or the pipeline fails.
