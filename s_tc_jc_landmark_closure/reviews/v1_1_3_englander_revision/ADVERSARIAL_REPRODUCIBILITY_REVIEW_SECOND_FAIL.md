# Second adversarial reproducibility review — preserved failure

Date: 2026-08-17
Status: **FAIL — superseded only after a third clean review**

The second clean-room referee confirmed that the first four defects were
substantively repaired, including literal archive-local PDF replay and full
tag-tree byte/mode binding.  It then found four adjacent inconsistencies:

1. `STATUS.md` still called all three capsules portal uploads, and the common
   capsule called itself a portal attachment, despite the journal-specific
   repository routing.
2. The capsule told archive users to run Git-dependent full/regeneration
   commands even though the deterministic `git archive` has no `.git`
   history.  A plain extraction failed as predicted.
3. The preserved v1.1.2 package regression was being described as though it
   parsed the current v1.1.3 manifests, even though its exact file sets
   correctly predated all three new capsules.
4. One active-verifier comment still named a stale fixed archive size.

The repair changed all active wording to submission-support and
journal-specific routing, split clone commands from the archive-only active
verifier, assigned current exact manifest checking and capsule-omission
mutation rejection to the v1.1.3 source-replay gate, explicitly retained the
v1.1.2 parser as version-specific history, and removed fixed-size wording.

FAIL
