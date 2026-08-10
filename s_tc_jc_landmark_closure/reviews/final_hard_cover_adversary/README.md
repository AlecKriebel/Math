# Independent final hard-cover adversary

This directory contains a clean-room, fail-closed audit of the primary
hard-cover artifacts.  It imports no primary graph, Fourier, canonicalization,
separator-selection, or sign-verification code.  Primary certificate files are
read-only inputs.

The decisive schema rule is:

> One state binds exactly one fixed-full root case and one exact rooted source
> and target graph.  Equality after standard semi-directed reduction does not
> permit these rooted provenances to merge.  Child sets are regenerated for
> every exact path.

`quarantined_schema2_failure.json` preserves the counterexample to the old
schema.  `audit_candidate_full.py` implements the stronger schema-3 replay.
The final scientific verdict is recorded in `REVIEW.md` after all jobs finish.
