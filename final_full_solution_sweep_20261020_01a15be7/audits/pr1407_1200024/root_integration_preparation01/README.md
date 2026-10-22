# Inert PR1407 integration plan

Read REPORT.md and INTEGRATION_PLAN.json. The selected PUBLICATION.md is supplied
as an ordinary readable file; all other exact selected bodies are hash-addressed
gzip payloads under private/. The full41path vector includes Git modes and
blob hashes. Only those paths are proposed.

Authenticate the complete closed manifest and both verifier sources before
executing trusted checked bytes. Scientific input seals and root adoption pins
are part of the closure verification. Preparation is not publication authority.

Local read-only payload/queue check:

    python3 -I -S -B verify_git_candidate_readonly.py 21b568e58c635f49951bfcc47179cd81d9d4427084cc4cf92e6d7700f6109eb0 --offline

Root's later exact candidate check, after separately authorized construction:

    python3 -I -S -B verify_git_candidate_readonly.py EXPECTED_PLAN_SHA256 CANDIDATE_COMMIT_SHA

The candidate checker uses GitHub GET only and writes only stdout. Capture any
later outputs in root's NEW execution namespace, never into this closed packet.
Its source hash is recorded in REPORT.md and the outer manifest. No candidate
commit was created or checked during preparation.

Before constructing anything, refresh live PR head/ref/state/draft, current main,
the target queue row, scientific/source hashes and all duplicate/account/register
gates. If main differs from6a8c636bad94d39caf468a645aff342febb945f8, rebuild a
new dated plan on the latest root tree and latest QUEUE.md, preserving all other
queue bytes. If another actor created this project or changed its target row,
reconcile rather than overwrite. Do not mutate this frozen packet to rebase it.

Root's later construction should retain parents[originalhead,currentmain], exact
selected modes, Git blob hashes and prospective tree hashes. A complete readback
must establish every unselected Merkle sibling and all40project leaf identities.
Fresh gates are required again before non-force branch advance and merge. A
known or ambiguous effect is reconciled by GET, never blindly repeated.

prepare_readonly.py is retained as a one-shot historical GET collector and pure
plan generator. Its output already exists; do not rerun it inside this closed
folder. It is not a branch/commit/upload/merge driver. Private raw observations
and duplicate payloads are excluded from ordinary public checkpoints by the
private/.gitignore rule.
