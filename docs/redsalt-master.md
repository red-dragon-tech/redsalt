# redsalt-master

`redsalt-master` is the Salt master repository for desired state and pillar data. For the code-backed cross-repository catalogue and known limitations, see the [current feature inventory](https://github.com/red-dragon-tech/redsalt/blob/dev/docs/features.md).

## Role model

Hosts opt into roles through authoritative pillar booleans:

```yaml
roles:
  base: true
  docker: true
  nvidia: true
  llm_vllm: true
```

`states/top.sls` matches these pillar values and includes role composition states from `states/roles/`. The current master defines seven roles: `base`, `docker`, `nvidia`, `llm_vllm`, `salt_master`, `kali_workstation`, and `restic_backup`. The minion-side pillar renderer currently supports only the first four; see the feature inventory.

## Current roles

| Role | Purpose |
| --- | --- |
| `base` | Common packages, timezone, managed directories, managed users, firewall, and pillar-configured package-update capability. |
| `docker` | Docker Engine and Docker Compose plugin. |
| `nvidia` | NVIDIA Container Toolkit and optional driver package policy. |
| `llm_vllm` | Model storage and vLLM OpenAI-compatible service using Docker Compose/systemd; includes optional Caddy state. |
| `salt_master` | Production sync/apply, recurring highstate convergence, and package-update runner. Current sync/convergence coordination has a known issue: [#30](https://github.com/red-dragon-tech/redsalt-master/issues/30). |
| `kali_workstation` | Configurable shared workspace/repository permissions and shell helpers. |
| `restic_backup` | Optional scheduled restic backup scaffold; disabled by default until each host's root-only secrets are provisioned out of band. |

Role composition states live in `states/roles/` and keep `states/top.sls` small. Firewall dynamic SSH source refresh is an additional optional master-side capability associated with the firewall state. Package-update behavior is pillar-configured; safe defaults keep automatic updates disabled. See the [package update policy](https://github.com/red-dragon-tech/redsalt-master/blob/dev/docs/package-updates.md) before changing host policy.

## Managed SSH access

The base role includes `states/users/init.sls`, which reads `managed_users` from pillar. The default pillar manages a `darthai` user with key-only SSH access via a public key. Public SSH keys are non-secret access policy; do not commit private keys or password hashes.

## Firewall baseline

The base role includes `states/firewall/init.sls`, which manages UFW policy from pillar. Defaults set incoming traffic to deny and outgoing to allow, scope SSH to configured sources, and restrict Salt ports to configured source CIDRs. Optional master-side dynamic source refresh updates generated pillar and reapplies the firewall state when the source changes.

## Salt master roots

The example master roots config is `salt-master.d/redsalt-roots.conf.example`. It maps `file_roots` to the `states/` tree and `pillar_roots` to the `pillar/` tree.

## Validation

From the master checkout:

```bash
python3 scripts/validate.py
python3 -m pytest tests -q
```

The validator checks required files, YAML parseability, Jinja syntax, role/top-file consistency, and obvious secret patterns. Repository validation does not require a running Salt master.

## Highstate workflow

Preview a target before any approved live apply:

```bash
salt '<minion-id>' test.ping
salt '<minion-id>' state.show_highstate
salt '<minion-id>' state.apply test=True
```

Run `state.apply` only after reviewing the preview and obtaining the relevant operational approval. A passing static test or test-mode preview does not establish that live convergence completed.
