# redsalt

Documentation hub for Red Dragon Technology's SaltStack tooling. RedSalt is split across three repositories: Salt master desired state and pillar, minion enrollment tooling, and this documentation hub.

## Repositories

- [`redsalt-master`](https://github.com/red-dragon-tech/redsalt-master): Salt states, pillar, role composition, and master-side automation.
- [`redsalt-minion`](https://github.com/red-dragon-tech/redsalt-minion): minion bootstrap/configuration helpers and master-pillar renderer.
- `redsalt` (this repository): architecture, operations, security, and a cross-repository feature catalogue.

## Start here

- [Current feature inventory](docs/features.md) — what is implemented, where it lives, and known limitations.
- [Architecture overview](https://github.com/red-dragon-tech/redsalt-master/blob/dev/docs/architecture.md)
- [Master operations guide](https://github.com/red-dragon-tech/redsalt-master/blob/dev/docs/operations.md)
- [Minion operations guide](https://github.com/red-dragon-tech/redsalt-minion/blob/dev/docs/operations.md)
- [Security model](https://github.com/red-dragon-tech/redsalt-master/blob/dev/docs/security.md)

The feature inventory is a code-backed snapshot, not a claim that every role is enabled or healthy on a live host. Check the relevant pillar and runtime status before operational changes.

## Current feature inventory

See [docs/features.md](docs/features.md) for the code-backed list of what is currently implemented in `redsalt-master` and `redsalt-minion`, where it lives, and known limitations.

## Validate docs

Run the repository-local check for required inventory pages and local Markdown links:

```bash
python3 scripts/validate.py
```
