# Research log: full-list terminal completion layer

## 2026-07-28 16:05 PDT

- Fixed the C-157/C-168 notation for one rank-zero nonroot corridor:
  \(S=\{u,v,t\}\), predecessor \(\{v,t,q\}\), banned terminal
  \(E=\{v,t,r\}\), secondary color \(v\), and missed witness \(w_v\).
- Observed a necessary collision correction.  A common nonneighbor
  \(d\) of \(x,r\) can in principle equal \(w_v\).  Therefore domination
  of \(\{d,t,r\}\) proves \(d\in N_G[w_v]\), not automatically the open
  edge \(dw_v\).
- Proved the exact row-wise response statement: every completion
  \(d\in C_{xr}\) has at least one retained successor
  \(\{d,t,r\}\) or \(\{v,d,r\}\); a surviving first successor puts
  \(d\) in the closed neighborhood of \(w_v\), and its attack at \(x\)
  has the unique response \(t\to x\), returning to
  \(\{x,r,d\}\).  The symmetric statement holds for a second secondary
  color \(t\).
- With two secondary colors, the completion clique is covered by the
  two closed witness neighborhoods.  This is the strongest conclusion
  obtained without comparing unrelated restricted deletion ranks.
- Exact exploration of the accepted equality control
  `OYifur}UO]}iTij]tpo]v` found the reverse of the tempting rank
  descent: in two empty-color rows, the completion successor has source
  rank zero while the uniquely reached independent completion has
  source rank three.
- Constructed an 11-vertex one-vertex extension of MMV-001,
  `JEhbtj{rvu?`.  It has all three restricted kernels empty and a
  completion for every one of the three terminal pairs, but
  \(\gamma=2\).  This is a boundary control, not a counterexample.
- A separate exact 9-vertex gamma-two control `HF~mdfj` realizes a full
  terminal palette, both distinct witnesses, one completion, both
  completion successors, and both unique returns.
- Discovery SAT runs for the same named full-terminal geometry with
  \(\gamma\ge3\) returned `UNSAT` through order 12, but no proof logs or
  all-order argument exist; this is **OBSERVED only**.

Best-guess completion toward the assigned terminal-completion theorem
and exact-control package: **65%**.  The proof is stable; the remaining
work is a strict verifier, manifest, scope audit, and commit/push.

## 2026-07-28 16:37 PDT

- Finished the self-contained proof note with the collision-safe
  closed-neighborhood statement and the symmetric two-witness cover.
- Added a strict exact verifier for all three controls.  It independently
  decodes and re-encodes each graph6 record, recomputes
  \(\gamma,i,\alpha,\gamma^\infty,\theta\), greatest eternal families,
  restricted kernels and ranks, completion sets, retained attack moves,
  unique returns, and dominating pairs.
- Strict replay matches the frozen canonical expected result.
- Scope audit is explicit: the unlogged finite `UNSAT` observations are
  not promoted, and no safe color, complete \(k=3\), or universal result
  is claimed.

Best-guess completion toward the assigned terminal-completion theorem
and exact-control package: **100%** before independent hostile review.
