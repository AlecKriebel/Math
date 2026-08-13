# Research log: complete-ray fixed-colour PAPT route

## 2026-08-13 13:08 PDT -- unsigned coloured-forest reduction

- Replaced the smaller cancellation-based dB clearing by the full positive
  clearing
  `Gamma_v=prod_{empty != S subset V-v}(2d_v-w_v(S))`.
- Proved the first-appearance-order formula
  `g_v(J)=sum_pi prod_r w_v,pi_r/(2d_v-w_v(S_r))`.  It makes every cleared
  dB off-diagonal entry coefficientwise nonnegative; the full-set factor
  `d_v` is essential for this unsigned representation.
- Derived the corrected paired-tree degree
  `q_n=n(2^n-2)+n(2^(n-1)-1)(2^n-3)`.
- Polarized the cleared PAPT numerator along
  `W_alpha=(1-alpha)K+alpha W`.  Its colour-`j` coefficient is exactly a
  positive normalization times
  `N_b N_d-D_b D_d E[R_L R_D]` under a coupled two-tree law with exactly
  `j` actual-coloured microscopic slots.
- Proved the zero- and one-colour coefficients vanish by complete-graph
  equality, vertex symmetry, and Euler homogeneity; equivalently the
  cleared numerator lies in the square of the complete-diagonal ideal.
- Proved every fixed-colour coefficient for `n=3` is nonnegative: the
  24-atom triangle certificate contributes `alpha^2` times products of
  positive linear interpolants, including the full clearing multiplier
  `72(d_0d_1d_2)^7 delta^4`.
- Performed one, and only one, order-four exact audit.  The quadratic PAPT
  gap has two positive invariant orbit coefficients:
  `4/9555` on adjacent-edge differences and
  `431881/53402895` on disjoint-edge differences.  This refutes the earlier
  one-wedge-orbit completion and supplies the `j=2` invariant base.
- Exact remaining sign: under fixed total colour count `j`, prove
  `E[R_L R_D] <= b_n d_n`.  Sampling-without-replacement exchangeability
  alone does not prove it because actual conductance evaluation reweights
  the tree packet and the split of colours between replicas.
- Rewrote the missing statement sharply under the complete decorated
  packet law `nu_0` as
  `Cov(R_L R_D,e_j(ell_1(W)/ell_1(K),...,ell_q(W)/ell_q(K))) <= 0`.
  Conditional negative association of the fixed-size colour set cannot
  imply it: after conditioning on the forest packet, the root product is
  constant and that conditional covariance is exactly zero.  The missing
  mechanism is across-packet negative regression.
- One targeted exact audit on the already frozen hostile K4 ray
  `(0,1000,2,1,1000,10)` found every canonical coefficient `C_j` positive
  for `2<=j<=12`, with the tilted mean root product strictly decreasing.
  This is evidence only; no graph or architecture scan was performed.
- Completion estimate: **100%** for the positive clearing and exact
  fixed-colour reduction; **100%** for all fixed-colour levels at `n=3`;
  **30%** for an all-order coefficient proof.  The root/slot correlation
  inequality remains open.
