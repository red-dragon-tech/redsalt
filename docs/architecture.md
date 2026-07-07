# Architecture overview

## System model

`redsalt` manages Linux hosts with SaltStack using a clear split between master-side desired state and minion-side enrollment.

```text
+----------------------+        Salt ZeroMQ         +----------------------+
| Salt master          | <------------------------> | Salt minions         |
| redsalt-master repo  |   TCP/4505 + TCP/4506      | redsalt-minion setup |
| states/ + pillar/    |                            | salt-minion service  |
+----------------------+                            +----------------------+
          ^                                                   |
          | docs/runbooks                                      | local services
+----------------------+                                      v
| redsalt docs repo    |                            Docker / NVIDIA / vLLM
+----------------------+
```

## Design principles

1. **Pillar is authoritative policy**
   - `redsalt-master` selects highstate using pillar role booleans.
   - Minion grains are inventory hints only and must not be treated as authorization.

2. **Roles are composable**
   - Current roles are `base`, `docker`, `nvidia`, and `llm_vllm`.
   - `base` owns common packages, directories, and managed SSH access.

3. **Minion bootstrap is repeatable**
   - `redsalt-minion` writes deterministic Salt minion config and inventory grains.
   - Master-side pillar is generated or reviewed separately before highstate.

4. **Automation is gated by GitHub live state**
   - Approval emails are useful signals, but merge decisions come from live PR state.
   - Repos with no configured checks have zero check runs/statuses; that is treated as no CI, not as pending work.

## Data flow

1. Operator bootstraps a host using `redsalt-minion/scripts/bootstrap-minion.sh`.
2. Salt master receives a pending minion key.
3. Operator verifies and accepts the minion key.
4. Operator adds or generates `redsalt-master/pillar/minions/<id>.sls`.
5. Salt highstate applies role-driven configuration.
6. Validation and service health checks confirm convergence.
