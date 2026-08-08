# Research log: chi-square channel route at dB fitness two

## 2026-08-02 -- initialization

- Objective: prove or refute the stationary target-information inequality
  `I_2(V;B) <= 2` for the exact random-target geometric-union dual at `r=2`.
- Required route: derive identities from the generator/channel and use
  entropy, collision, or resolvent structure; avoid the already explored
  pairwise-crossing and linear-potential arguments.
- The posterior identity is immediate: under the stationary one-step
  experiment, `Pr(V=v | B)=f_v(B)/n`; hence `I_2=n E sum_v Pr(V=v|B)^2`.
- Initial computational objective: search both arbitrary directed kernels and
  reversible kernels induced by symmetric weights before investing in a
  universal contraction proof.

## 2026-08-02 -- midpoint resolvent and failed separations

- Derived the exact fair-geometric resolvent `Q_v=A_v(2I-A_v)^(-1)` and its
  stationary submeasure form `2 nu_v=(sigma_v+nu_v)A_v`.
- Derived the exact posterior decomposition
  `Pr(effective|B)=|B|/n` and
  `Pr(V=v|B,effective)=e_v(B)/|B|`.
- Exhaustive directed tests whose rows are uniform on a nonempty neighbor
  subset through `n=4` (1,606 strongly connected order-four kernels), plus
  random and continuous optimization through `n=6`, found no violation of
  `I2<=2`.  These are diagnostics only; equality was seen only at the
  uniform complete kernel.
- Exactly falsified fixed-reference Hilbert contraction on the unweighted
  three-path: `||nu A||^2=19/9 > 13/9=||nu||^2`, while `I2=17/9<2`.
- Exactly falsified the stronger route obtained by revealing the
  effective/null flag on the triangle with weights `(7,1,1)`.  Therefore
  cancellation between the two history types is essential.

## 2026-08-02 -- Shannon reflection and exact path reversal

- Rewrote the proposed Shannon gap as
  `H(V|B)-H(V|A,J)`, where `J=1_{V in A}`.  Hence it compares the output
  experiment with the stationary membership experiment.
- Identified a common likelihood-ratio formulation: the membership channel
  has `E L0^2=2` and `E L0 log L0=M`; the output channel has
  `E L1^2=I2` and `E L1 log L1=I(V;B)`.
- Built the exact normalized Cayley reverse step and proved by telescoping
  that it reverses every labelled geometric sample path with identical
  probability.  The natural path-space entropy production is therefore
  exactly zero, not the conjectured gap.
- Exactly falsified Blackwell dominance on the unweighted three-path:
  target-row total variation expands from `7/9` to `5/6`.
- Exactly falsified aggregate likelihood convex order on the triangle with
  weights `(7,1,1)`: at stop-loss threshold `3/2`, the membership-minus-output
  gap is `-8/327`.
- Exhaustive directed uniform-subset kernels through order four and random
  or optimized positive kernels through order six found no negative Shannon
  gap.  This remains diagnostic evidence only.
