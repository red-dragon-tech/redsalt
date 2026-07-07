# Security model

## Repository secrets boundary

Do not commit:

- SSH private keys;
- Salt minion private keys from `/etc/salt/pki/minion/`;
- password hashes unless intentionally reviewed;
- API tokens;
- registry credentials;
- TLS private keys.

SSH public keys, such as `authorized_keys` entries or master-side `managed_users` public keys, are not secrets and may be committed as access policy.

## Salt trust boundaries

- Pillar is authoritative for desired roles and access policy.
- Grains are minion-controlled and should be treated as inventory metadata only.
- Minion keys should be accepted only after verifying the minion ID and fingerprint.

## GitHub automation boundaries

Automerge is restricted by repository allowlist, PR author allowlist, non-author review approval, live mergeability, and check status. Approval emails alone are not sufficient to merge.

## Local shared checkouts

`/opt/shared/repos` is readable by local users. Do not store credentials or generated secrets inside these checkouts. Git transport credentials should remain in the Hermes profile environment or approved credential helpers, not in remote URLs.
