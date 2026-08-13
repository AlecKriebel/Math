# Research log: diffuse support variational obstruction

## 2026-08-13 — negative `K_Rhyb` with positive `T_Rhyb`

- Worked proof-first; no graph search, kernel scan, literature search, or
  external communication was used.
- Attacked the stronger ground-energy route
  `K_Rhyb>=0` from the exact support decomposition.
- Reused the structural positive symmetric three-type singular family, but
  derived its `K_r` limit for the first time.  The vanishing `A` extinction
  atom and diverging `B` temperature were retained exactly.
- For `gamma=1/14`, `theta=1/50`, proved

  ```text
  K_lim(r) = -13 Q(r)/(87500000 r^3),
  Q(r)>0 on [3/2,151/100].
  ```

  Therefore `K_lim(R_hyb)<0`, and sufficiently small finite positive
  kernels have negative ground energy.
- The full support deficit remains
  `T_lim(r)=13(r-1)/(700r)>0`.  Thus this is not a counterexample to the
  desired diffuse support inequality.  It proves that the manifest square
  in the exact decomposition is essential and stops the scalar
  `K>=0`/Jensen/Picone strengthening.
- Added an exact symbolic replay for the limit formula and all sign claims.
- Best-guess program estimate after this obstruction: the structural route
  to the exact value is roughly `70--75%` isolated, while a complete proof
  of `R_sim=R_hyb` is roughly `45--50%` complete.  This checkpoint removes
  a tempting shortcut but leaves the essential combined `T/DA` inequality
  and the response-scale cutoff aggregate open.

No commit was made pending report to the primary agent, as requested.
