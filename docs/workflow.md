# Branching and PR workflow

## Branch policy

- `prd` is the production branch.
- `dev` is the development baseline.
- New work branches should start from `dev`.
- PRs should target `dev` unless a user explicitly requests a different target.
- `dev` is synced from `prd` daily so new work begins from the production baseline.

## Local workspace policy

All Darth-managed GitHub checkouts should be under:

```text
/opt/shared/repos/
```

Existing checkouts:

```text
/opt/shared/repos/redsalt
/opt/shared/repos/redsalt-master
/opt/shared/repos/redsalt-minion
```

## PR review policy

Every Darth-created PR should request at least one reviewer. If the user does not specify a reviewer, choose from repository contributors and collaborators with review permission. `jlang-rdt` is a valid reviewer for the RDT repos even if absent from GitHub's contributor graph.

## Merge policy

Approved Darth-authored PRs may be squash-merged automatically when all gates pass:

- repo is allowlisted;
- PR author is `rdt-ai-ops`;
- PR is open and not draft;
- branch is mergeable;
- at least one non-author approval exists;
- no latest `CHANGES_REQUESTED` review exists;
- no failing or pending checks exist;
- zero check runs/status contexts is treated as no CI configured.

The automerge job deletes same-repo source branches after successful merge.
