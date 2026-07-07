# redsalt-master

`redsalt-master` is the Salt master repository for desired state and pillar data.

## Role model

Hosts opt into roles through pillar booleans:

```yaml
roles:
  base: true
  docker: true
  nvidia: true
  llm_vllm: true
```

`states/top.sls` matches these pillar values and includes role composition states from `states/roles/`.

## Current roles

| Role | Purpose |
| --- | --- |
| `base` | Common packages, timezone, managed directories, and managed users. |
| `docker` | Docker Engine and Docker Compose plugin. |
| `nvidia` | NVIDIA Container Toolkit and optional driver package policy. |
| `llm_vllm` | vLLM OpenAI-compatible service using Docker Compose and systemd. |

## Managed SSH access

The base role includes the `users` state. The default pillar manages a `darthai` user with Darth's Ed25519 public SSH key. Public keys are non-secret access policy; private keys must never be committed.

## Salt master roots

The master repo includes an example roots config:

```text
salt-master.d/redsalt-roots.conf.example
```

It maps:

```yaml
file_roots:
  base:
    - /srv/redsalt-master/states

pillar_roots:
  base:
    - /srv/redsalt-master/pillar
```

## Validation

Run from the master repo checkout:

```bash
make validate
make test
```

The validator checks required files, YAML parseability, Jinja syntax, role consistency, managed SSH user policy, and obvious secret patterns.

## Highstate workflow

```bash
salt '<minion-id>' test.ping
salt '<minion-id>' pillar.items
salt '<minion-id>' state.show_highstate
salt '<minion-id>' state.apply test=True
salt '<minion-id>' state.apply
```
