# redsalt

Documentation hub for the Red Dragon Technology `redsalt` SaltStack tooling.

`redsalt` is split into focused repositories:

| Repository | Purpose |
| --- | --- |
| [`red-dragon-tech/redsalt`](https://github.com/red-dragon-tech/redsalt) | Documentation, operations runbooks, and cross-repo workflow guidance. |
| [`red-dragon-tech/redsalt-master`](https://github.com/red-dragon-tech/redsalt-master) | Salt master state/pillar tree for Ubuntu hosts, Docker/NVIDIA/vLLM roles, and managed SSH access. |
| [`red-dragon-tech/redsalt-minion`](https://github.com/red-dragon-tech/redsalt-minion) | Minion-side bootstrap/configuration scripts and examples that prepare hosts to join the master. |

## Current conventions

- Development branches and PRs target `dev`.
- `dev` is synced from `prd` daily so new work starts from the production baseline.
- PRs created by Darth request at least one human reviewer/approver, with `jlang-rdt` eligible for RDT repos.
- Approved Darth-authored PRs in allowlisted repos are eligible for automated squash merge after live GitHub checks pass.
- Local shared checkouts live under `/opt/shared/repos/` and are readable by local users.

## Documentation index

- [Architecture overview](docs/architecture.md)
- [Repository map](docs/repositories.md)
- [Salt master documentation](docs/redsalt-master.md)
- [Salt minion documentation](docs/redsalt-minion.md)
- [Branching and PR workflow](docs/workflow.md)
- [Operational automation](docs/automation.md)
- [Security model](docs/security.md)

## Validate docs

```bash
make validate
```

The validator checks required documentation files and local Markdown links.
