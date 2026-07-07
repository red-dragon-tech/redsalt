# redsalt-minion

`redsalt-minion` prepares Ubuntu hosts to join the `redsalt-master` Salt environment.

## Bootstrap script

Run on a target Ubuntu host:

```bash
sudo ./scripts/bootstrap-minion.sh \
  --master salt.example.internal \
  --id example-vllm-node \
  --roles base,docker,nvidia,llm_vllm
```

The script writes:

- `/etc/salt/minion.d/99-redsalt.conf`
- `/etc/salt/grains`

It can install `salt-minion` through apt, Salt bootstrap, or skip installation with `--install-method none`.

## Pillar rendering helper

Generate master-side pillar:

```bash
./scripts/render-pillar.py \
  --minion-id example-vllm-node \
  --roles base,docker,nvidia,llm_vllm \
  --output ../redsalt-master/pillar/minions/example-vllm-node.sls
```

Then add the minion to `redsalt-master/pillar/top.sls`:

```yaml
base:
  'example-vllm-node':
    - minions.example-vllm-node
```

## Grains vs pillar

`redsalt-minion` writes role names into grains for inventory visibility. `redsalt-master` still uses pillar as authoritative role policy. Do not grant access or select highstate based on minion-controlled grains.

## Validation

Run from the minion repo checkout:

```bash
make validate
make test
```
