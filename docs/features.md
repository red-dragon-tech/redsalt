# Current feature inventory

This page records behavior found in the `dev` checkouts of `redsalt-master` and `redsalt-minion` on 2026-10-27. It is an implementation inventory, not a roadmap, deployment attestation, or guarantee that each feature is enabled or healthy on a live host. For live state, inspect the relevant minion pillar and Salt results.

## How the pieces fit together

- `redsalt-minion` bootstraps a host's Salt minion and provides example configuration plus a helper for generating master-side pillar.
- `redsalt-master` owns the Salt state and pillar trees. Its `states/top.sls` selects roles using authoritative pillar booleans.
- Minion grains written by `redsalt-minion` are inventory metadata only. They do not authorize access or select highstate roles.
- `redsalt` is the documentation and operations hub.

## `redsalt-master`

### Pillar-selected roles

The seven role states below are registered in `states/top.sls`; each composes one or more capability states. A role is applied only when the matching pillar boolean selects it.

| Role | Composed states | Implemented purpose |
| --- | --- | --- |
| `base` | `common`, `firewall`, `package_updates`, `users` | Common host setup, UFW firewall policy, configurable package update policy, and pillar-managed local users/SSH authorized keys. |
| `docker` | `docker` | Docker Engine and Compose plugin setup. |
| `nvidia` | `nvidia` | NVIDIA Container Toolkit configuration and optional driver package policy. |
| `llm_vllm` | `models`, `vllm`, `caddy` | Model/cache directories, vLLM service via Docker Compose/systemd, and optional pillar-enabled Caddy configuration. |
| `salt_master` | `redsalt_master_sync`, `redsalt_highstate_convergence`, `redsalt_package_updates` | Production-branch repository sync/apply, recurring master-orchestrated highstate convergence, and master-side scheduled package-update runner. |
| `kali_workstation` | `kali_workstation` | Configurable shared workspace/repository permissions and shell helpers for the configured Kali workstation. |
| `restic_backup` | `restic_backup` | Optional scheduled restic backup scaffold, retention/prune, and repository checks. Disabled by default pending manual per-host secret provisioning. |

Role/state mappings: `states/top.sls`, `states/roles/*.sls`.

### Additional capabilities and operating notes

- **Firewall and dynamic SSH source refresh:** the base firewall state manages UFW policy from pillar. An optional Salt-master timer refreshes the generated SSH source pillar and reapplies the firewall state when the configured source changes. Source: `states/firewall/`.
- **Package updates:** `states/package_updates/` provides a pillar-configured update policy with Salt-managed and optional native OS updater paths. The scheduled runner is separately configured; defaults leave update automation disabled, and package application is gated by explicit approved preview data and policy. Automatic reboot defaults off. Host scope and current policy are in pillar; consult the runbook and open Kali policy issue [#23](https://github.com/red-dragon-tech/redsalt-master/issues/23) before describing a specific live rollout.
- **vLLM service support:** state manages Compose, environment/config files, model and cache directories, systemd service, and bundled Qwen2.5-Coder tool-parser/template assets. It includes Triton cache cleanup support. Caddy configuration is composed in the role but is enabled only when its pillar `enabled` value is true. Actual model, arguments, Caddy enablement, and ports depend on pillar. Source: `states/vllm/`, `states/models/`, `states/caddy/`.
- **Production sync:** the master sync script tracks `origin/prd`; when the desired commit differs from its last-applied marker, it validates the checkout, updates the fileserver/pillar, applies highstate, then records the applied SHA on success. Source: `states/redsalt_master_sync/`.
- **Recurring convergence:** a separate systemd timer runs highstate on a schedule and records per-minion outcomes. Source: `states/redsalt_highstate_convergence/`.
- **Known sync/convergence caveat:** the current convergence unit declares `Conflicts=redsalt-master-sync.service`, while sync runs every minute. Open issue [redsalt-master #30](https://github.com/red-dragon-tech/redsalt-master/issues/30) documents that this can cause systemd to terminate an in-progress convergence. The two paths should not be described as safely serialized until that issue is resolved and verified.
- **Restic is not turnkey enabled backup:** the role is opt-in (`enabled: false` by default). Per-host repository credentials and a unique repository password are provisioned out of band in root-only files; they are not supplied by Salt pillar. Source: `pillar/restic_backup/defaults.sls`, `states/restic_backup/`.

### Static validation

From the master checkout, run `python3 scripts/validate.py` and `python3 -m pytest tests -q` (or the repository's documented `make validate` / `make test` targets when present). Static validation does not require a running Salt master; only a reviewed live preview/apply can confirm rendered or converged behavior on a target.

## `redsalt-minion`

### Bootstrap and host configuration

`scripts/bootstrap-minion.sh` supports installing Salt Minion via configured apt repositories, the Salt bootstrap script, or no installation (`apt`, `bootstrap`, `none`). It accepts a master address, stable minion ID, inventory-role list, Salt/pillar environment names, and optional verified master fingerprint. `--no-start` suppresses enabling/restarting the service. By default the script writes `/etc/salt/minion.d/99-redsalt.conf` and `/etc/salt/grains`, then enables/restarts `salt-minion` when systemd is available.

After bootstrap, key verification/acceptance and pillar registration are separate operator steps on the master; bootstrap does not itself accept a key or deploy highstate.

Source: `scripts/bootstrap-minion.sh`, `configs/minion.d/99-redsalt.conf.example`, `configs/grains.example`.

### Pillar rendering helper

`scripts/render-pillar.py` emits a master-side pillar file and optionally prints the corresponding `pillar/top.sls` entry. It currently accepts only `base`, `docker`, `nvidia`, and `llm_vllm`; it automatically includes `base`. For NVIDIA/vLLM roles it also renders example model/NVIDIA defaults, and for `llm_vllm` it includes example service defaults. Review generated pillar for the host before use.

**Known coverage gap:** the master currently also defines `salt_master`, `kali_workstation`, and `restic_backup`, but this helper cannot render those roles. Do not interpret the helper's role list as the complete master role list. Source: `scripts/render-pillar.py` in `redsalt-minion`; `states/top.sls` and `scripts/validate.py` in `redsalt-master`.

### Supporting tooling

The minion repo includes example minion/grains configuration, `scripts/validate.py`, and `tests/test_repo_static.py`. These check repository artifacts and examples; they do not prove that a live minion enrolled successfully or that its master applied highstate.

## Validation and live-state boundary

Both repositories provide static validation and tests. A passing repo check establishes only what those checks exercise. It does not prove a live Salt master is using that revision, a minion has accepted keys/pillar, or a live highstate has completed successfully. Use the operational guides for preview/apply and host-specific health checks.
