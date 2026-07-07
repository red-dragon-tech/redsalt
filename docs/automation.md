# Operational automation

This page documents the Hermes-side automation currently supporting the redsalt repos.

## Approved PR automerge

Script:

```text
/root/.hermes/scripts/github_approved_pr_automerge.py
```

Cron job:

```text
name: GitHub approved PR automerge
schedule: every 60m
deliver: slack:C0B6Z9GP1ML
```

Current allowlist:

- `red-dragon-tech/redsalt`
- `red-dragon-tech/redsalt-master`
- `red-dragon-tech/redsalt-minion`

The script is silent when there are no eligible PRs and prints Slack-friendly output on merges, new blockers, or errors.

## Daily dev sync from prd

Script:

```text
/root/.hermes/scripts/sync_dev_with_prd.py
```

Cron job:

```text
name: Daily GitHub dev sync from prd
schedule: 0 2 * * *
deliver: slack:C0B6Z9GP1ML
```

Current allowlist:

- `red-dragon-tech/redsalt`
- `red-dragon-tech/redsalt-master`
- `red-dragon-tech/redsalt-minion`

The script makes `dev` match the exact `prd` SHA and is silent when already synced.

## AgentMail GitHub notification monitor

Script:

```text
/root/.hermes/scripts/monitor_agentmail_github_notifications.py
```

The monitor classifies GitHub notification emails, labels them in AgentMail, and alerts Slack for actionable events. It does not merge PRs; merge decisions come from live GitHub state in the automerge job.
