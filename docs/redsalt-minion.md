# redsalt-minion

`redsalt-minion` prepares Ubuntu hosts to join the `redsalt-master` Salt environment. For the code-backed cross-repository catalogue and known role coverage gap, see the [current feature inventory](https://github.com/red-dragon-tech/redsalt/blob/dev/docs/features.md).

## Bootstrap script

Run on a target Ubuntu host:

```bash
sudo ./scripts/bootstrap-minion.sh \
  --master salt.example.internal \
  --id example-vllm-node \
  --roles base,docker,nvidia,llm_vllm
```

The script supports Salt installation via configured apt repositories, the Salt bootstrap script, or no installation (`--install-method apt|bootstrap|none`). It writes `/etc/salt/minion.d/99-redsalt.conf` and `/etc/salt/grains`; optionally pins a verified master fingerprint with `--master-finger`. By default it enables/restarts `salt-minion` when systemd is available; `--no-start` suppresses that step.

Bootstrap does not accept a Salt key, register pillar on the master, or apply highstate. Verify and accept the minion key through the documented master-side process, then configure its pillar separately.

## Pillar rendering helper

Generate master-side pillar with `scripts/render-pillar.py`:

```bash
./scripts/render-pillar.py \
  --minion-id example-vllm-node \
  --roles base,docker,nvidia,llm_vllm \
  --output ../redsalt-master/pillar/minions/example-vllm-node.sls
```

Then add the matching minion entry to `redsalt-master/pillar/top.sls`. The helper supports only `base`, `docker`, `nvidia`, and `llm_vllm`; the master also has `salt_master`, `kali_workstation`, and `restic_backup` roles, which must be configured by other means. See the feature inventory for details.

## Grains vs pillar

`redsalt-minion` writes role names into grains for inventory visibility. `redsalt-master` uses pillar as authoritative role policy. Do not grant access or select highstate based on minion-controlled grains.

## Validation

Run from the minion repo checkout:

```bash
make validate
make test
```

These checks validate repository tooling and examples; they do not establish that a live host enrolled successfully or converged.
