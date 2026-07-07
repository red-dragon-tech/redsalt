# Repository map

## red-dragon-tech/redsalt

Documentation hub. This repo should contain cross-repo runbooks, architecture notes, and workflow policy. It should not contain secrets, minion private keys, or generated operational state.

Local checkout:

```text
/opt/shared/repos/redsalt
```

## red-dragon-tech/redsalt-master

Salt master state and pillar repository. It includes:

- `states/top.sls` role targeting by pillar booleans.
- `pillar/top.sls` and minion-specific pillar examples.
- `states/common`, `states/users`, `states/docker`, `states/nvidia`, `states/models`, and `states/vllm`.
- Validation tooling under `scripts/validate.py`.

Local checkout:

```text
/opt/shared/repos/redsalt-master
```

## red-dragon-tech/redsalt-minion

Minion bootstrap/configuration repository. It includes:

- `scripts/bootstrap-minion.sh` for Ubuntu minion setup.
- `scripts/render-pillar.py` for generating compatible master-side pillar.
- Example minion config and grains under `configs/`.
- Validation tooling under `scripts/validate.py`.

Local checkout:

```text
/opt/shared/repos/redsalt-minion
```

## Local workspace policy

All local GitHub workspaces/checkouts used by Darth should live under:

```text
/opt/shared/repos/
```

The directory is readable by all local users. Git safe-directory entries are configured for the existing shared checkouts.
