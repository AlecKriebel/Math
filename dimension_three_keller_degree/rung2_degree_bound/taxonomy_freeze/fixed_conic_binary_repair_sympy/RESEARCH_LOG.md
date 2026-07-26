# Research log: binary fixed-conic E7/E6 repair

## 2026-07-26T09:54:52Z — kickoff

- Scope is restricted to the binary fixed-conic normals \(h=pq\) and
  \(h=p^2\).
- The retained audit was read.  Its exact fail-closed gap is confirmed:
  the old degree-six regressions use \(V=0\), one selected \(H_2\), and
  zero linear part instead of eliminating the full degree-seven fibre.
- The repair will begin with all 12 coefficients of the binary cubic
  \(V\), all 18 coefficients of \(H_2\), all six degree-eight tangent
  parameters, and all nine coefficients of the linear part.
- Existing unrelated untracked files in the worktree will not be touched.
- Best-guess completion: 10%.

## 2026-07-26T10:09:44Z — exact E7/E6 repair completed

- For \(h=pq\), the E7 matrix in the 18 quadratic coefficients has
  constant rank 7.  The reduced compatibility locus is
  \(e=f=b=c=0\),
  \((3a-d)v_8=(a-3d)v_3=0\), and the complete \(H_2\) fibre is affine
  11-space with constant pivots.
- For \(h=p^2\), the same matrix rank is 7.  The reduced compatibility
  locus is \(e=f=b=0\) together with
  \((a-4d)v_2+6(2d-a)v_7-6cv_3=0\) and
  \((a-2d)v_3=0\); the complete \(H_2\) fibre is again affine 11-space.
- Substitution of the full fibres, with arbitrary free \(H_2\), arbitrary
  \(V\), and arbitrary \(L\), gives exactly equations (7) and (8).
- Polynomial sections prove that the raw tangent-elimination ideals are
  \(\langle(a-d)^2(a+d)\rangle\) and
  \(d\langle c,d-a\rangle^2\), respectively.
- Their reduced components give exactly the tangent representatives
  claimed in equation (9).  All E7 rank jumps and the zero intersections
  were retained explicitly.
- The strict checker passes under exact SymPy 1.14.0 in about six seconds
  including its dependency check, using well under 100 MB RSS for the
  main calculation.
- No counterexample to equations (7)--(9) or the tangent list was found.
- Best-guess completion of the assigned binary E7/E6 repair: 95%;
  independent review and final worktree-scope checks remain.

## 2026-07-26T10:13:51Z — audit boundary hardened

- The strict runner now executes the checker under `python -O`.
- All mathematical checks use explicit fail-closed `require` calls; no
  Python `assert` can disappear under optimization.
- The exact ranks, compatibility ideals, elimination ideals, radicals,
  orbit list, and rank jumps are retained in `NOTE.md` and `REPORT.md`.
- The composition boundary is explicit: the repair transports the full
  E7 fibres onto every E6 tangent orbit, but it does not rederive the
  later legacy families from those full fibres.  Those later endgames
  remain unclaimed by this artifact.
- Best-guess completion of the assigned binary E7/E6 repair: 100%.
