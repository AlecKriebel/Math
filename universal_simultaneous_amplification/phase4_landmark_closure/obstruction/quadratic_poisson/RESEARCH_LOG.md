# Research log: quadratic Poisson route

All timestamps use America/Los_Angeles.

## 2026-08-02

- 02:37 -- [NUMERICALLY OBSERVED] Formulated the exact monomial drifts for
  the `r=2` geometric-union dB dual.  A full quadratic certificate for the
  half-density target `2|A|-n` passed every connected unweighted graph
  through five vertices and thousands of random weighted graphs through ten
  vertices.  The stronger common-linear-plus-support-edge ansatz also passed
  all 995 connected unweighted isomorphism classes through seven vertices in
  a floating-point atlas screen.  This is evidence only.
- 03:01 -- [NUMERICALLY OBSERVED] Reduced the support-edge coefficients in
  broad random screens to the vertex-potential form
  `q_ij=a_i P_ij+a_j P_ji` with unrestricted `a_i`.  Nonnegativity of the
  vertex potentials is false on an extreme eight-vertex weighted example;
  no universal reduction is claimed.
- 03:12 -- [EXACTLY COMPUTED / PROOF ARCHITECTURE REFUTED] For the stronger
  complete-graph target, found an exact dihedrally invariant pseudo-law on
  `C_5` that annihilates all degree-two generator balances but has mean
  `40/17 > 32/15`.  Therefore no quadratic Poisson certificate can prove the
  `K_5` mean ceiling on `C_5`.  The actual stationary mean is exactly
  `80/39 < 32/15`, so this is not a fixation counterexample.
- 03:22 -- [PROVED BY EXACT CERTIFICATE] Found and independently verified a
  symmetric cubic on `C_5` whose drift dominates `|A|-32/15` on every
  nonempty state.  Atlas discovery counts show that degree three is again
  insufficient on 11 connected six-vertex isomorphism classes, while degree
  four passes all 112 on proper states.  The exact universal `r=2` mean
  ceiling and the half-density quadratic existence theorem remain OPEN.
- 03:31 -- [PROVED] Established an exact degree barrier on the complete
  graph.  For `F_d(k)=binom(k,d)`, the `r=2` complete-graph dual generator
  raises polynomial degree from `d` to `d+1`, with nonzero leading
  coefficient `-2/((d-1)!(n-1+d))`.  Stationary equality then forces every
  pointwise certificate for the exact complete mean to have Boolean degree
  at least `n-2`; the centered Poisson equation and interpolation show this
  degree is attained.  Therefore no bounded-degree exact-baseline Poisson
  architecture can prove the desired universal maximization theorem, even
  on the baseline itself.
