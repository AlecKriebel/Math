# Adversarial release review

Status: **PASS — no remaining implementation blocker found**

The release reviewer ran three successive falsification rounds.  The first
rejected a seal that trusted a prepared working-tree stage.  The second found
that ignored working-tree files could enter a nominally fresh reconstruction.
The third demonstrated a `PYTHONPATH/sitecustomize` startup-hook attack.  Each
defect was preserved before repair.

The final implementation passed the following independent checks:

- preparation and sealing require both Python isolated mode and disabled
  `site` startup (`python -I -S`);
- the detached committed builder is also launched with `-I -S` and a strict
  subprocess environment excluding Python and dynamic-loader startup hooks;
- the proof payload is reconstructed from `git archive` of the exact recorded
  commit rather than from ambient working-tree bytes;
- changed bytes, missing or extra paths, executable-mode changes, ignored-file
  injection, and startup-hook injection are rejected;
- duplicate active-manifest paths, altered payload commitments, and altered
  executable-mode bindings are rejected;
- the external envelope and archived manifest are cross-checked, and the
  repository-level verifier requires the recorded source commit to exist as a
  Git object;
- the focused stage/source regression and consolidated referee-repair gate
  both pass.

The reviewer found no mathematical consequence and no reason to weaken the
headline theorem.  The clean source commit and uninterrupted archive-local
quick, full, and regenerate-all transcripts remain mandatory final release
artifacts; their generation follows this review and does not alter the proof.

PASS
