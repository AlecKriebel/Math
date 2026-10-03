# Five substantive approaches and their outcomes

This is a record of mathematical approaches, not five claims of a solution. The final quantitative theorem and its limitations are in `PROOF.md`. No approach resolves the qualitative naturalness requirement by definition or by assertion.

## 1. Reconstruct the published fractional gadget

**Target.** Check the existing constant-size evidence before searching for a large separation.

Potechin–Zhang [PROOF reference 2, Appendix A] use three variables `x_1,x_2,x_3` and three selector variables. For every full selector indicator `delta_y`, include `x_i delta_y=0` for `i=1,2,3`. Also include `x_1x_2x_3=0` and `bar(x_1)bar(x_2)=bar(x_1)bar(x_3)=bar(x_2)bar(x_3)=0`.

Their identity is

\[
1=\tfrac12\bar x_1\bar x_2+\tfrac12\bar x_1\bar x_3
 +\tfrac12 x_1\bar x_2\bar x_3
 -\tfrac12 x_1x_2x_3
 +\tfrac12(x_1+x_2+x_3)\sum_y\delta_y.
\]

Its mass is `2+3*8/2=14`. On the three weight-two `x` assignments for any fixed selector, at least two of the three `x_i delta_y` axiom groups are needed. At the all-zero `x` assignment, at least one low-weight axiom group is needed. Hence every proof has support at least `2*8+1=17`; integer mass is also at least 17.

The elementary integer identity

\[
1=\sum_y\delta_y(x_1+\bar x_1x_2)+\bar x_1\bar x_2
\]

has mass 17. Approach 2 supplies a matching real dual of mass 14. Thus the exact values for this fixed example are `C_R=14`, `C_Z=17`. The original 14-versus-17 separation is published prior work, not a new resolution.

**Outcome.** The distinction is real, but this one finite example does not establish growing savings.

## 2. Increase the selector replication

**Target.** Test whether simply enlarging the published gadget amplifies its ratio.

Use `k>=1` selector bits and put `B=2^k`, with the same three `x` variables and the same four ungated axioms. The two identities above give

\[
C_R\le 3B/2+2,\qquad C_Z\le 2B+1.
\]

The same support argument yields `S_R>=2B+1`, hence `C_Z=2B+1`.

Here is an exact dual proving the fractional optimum. For every selector assignment `y`, assign a signed point weight depending only on `t=x_1+x_2+x_3`:

\[
D(x,y)=\begin{cases}
0&t=0,\\
1/B&t=1,\\
1/2&t=2,\\
-1/B&t=3.
\end{cases}
\]

For a weakening of a gated `x_i delta_y`, the selector is fixed. Sums over unrestricted or fixed remaining `x` coordinates are among `0, 1/B, 1/2, -1/B, 1/2+1/B, 1/2-1/B, 1`; all have absolute value at most one for `B>=2`. For a weakening of a low-weight pair axiom, at most `B` selector values and at most one positive point of weight `1/B` remain. For the triple axiom the sum lies between `-1` and zero. Therefore every weakening has dual value of absolute value at most one. Summing all point weights gives `3B/2+2`.

Weak duality follows directly by applying `D` to a refutation. Thus

\[
C_R=3B/2+2,\qquad C_Z=S_R=2B+1.
\]

**Outcome.** Exact guarded replication fails to create an unbounded ratio: it tends to `4/3`. This rules out a tempting amplification of the published example, rather than just reporting unsuccessful numerics.

## 3. Tensor-product amplification

**Target.** Try multiplicative growth instead of selector replication.

For unsatisfiable monomial systems `F` and `G` on disjoint variable blocks, define the product system to contain every product `AB`, where `A` is an axiom of `F` and `B` is an axiom of `G`. Its weakenings are precisely products of weakenings in the two blocks. Multiplying real certificates gives

\[
C_R(F\otimes G)\le C_R(F)C_R(G).
\]

The finite linear-program dual is the maximum of `D(1)` over linear functionals satisfying `|D(W)|<=1` for every weakening. Optimal duals exist: primal feasibility follows from unsatisfiability and full-assignment indicators, and mass is bounded below and attained in a finite-dimensional linear program. Tensor two optimal duals. They obey the product constraints because `|D_F(W_F)D_G(W_G)|<=1`; their objective is the product. Hence

\[
C_R(F\otimes G)=C_R(F)C_R(G).
\]

For the six-variable published example, the `t`-fold product consequently has real optimum exactly `14^t`.

**Obstruction.** The argument gives no integer lower bound `17^t`. Integer optima do not have this real linear dual characterization, and a minimum-support lower bound does not automatically tensorize. One would have to prove an additional covering or arithmetic statement for the product weakening family. No such general statement was proved here. The product also introduces `28^t` original axioms, so an exponential-in-`t` statement is not an exponential-in-input-size lower bound.

**Outcome.** Exact fractional tensorization established; claimed integer amplification withheld. Small numerical integer programs were used only to explore an auxiliary triangle-incidence analogy. Those solver outputs are not relied upon or published as certified tensor lower bounds.

## 4. Hamming-slice hitting sets with full-assignment padding

**Target.** Replace the three-point cover by a set system with a growing covering gap.

Let `m` be even, `r=m/2`, and introduce `m` input bits `x` and `m` selector bits `y`, with `B=2^m`. Include these normalized monomial axioms:

- `x_i delta_y=0` for every input index and every full selector assignment;
- `delta_z(x)=0` for every full input assignment `z` whose weight is not `r`.

The system is unsatisfiable. The exact identity

\[
1=\frac1r\sum_{i,y}x_i\delta_y
 +\sum_{z:|z|\ne r}(1-|z|/r)\delta_z(x)
\]

gives fractional mass at most `mB/r+2^m=3B`, since `|1-|z|/r|<=1`.

For each fixed selector assignment, every `r`-element input subset survives all second-type axioms. The input indices of used first-type axiom groups must hit every such subset. At least `m-r+1` groups are needed per selector; groups for distinct selectors cannot coincide. Therefore every proof has support, and every integer proof has mass, at least `B(m-r+1)`. The mass ratio is at least `(m/2+1)/3`.

**Outcome.** This is a valid unbounded explicit ratio, but it uses exponentially many input axioms in `m` and an artificial full-assignment selector expansion. Its improvement is only logarithmic in formula size and does not convincingly meet the source's intended naturalness. It motivates a succinct cardinality encoding rather than being promoted as a complete answer.

## 5. Replace the padding by a balanced binary-adder CNF

**Target.** Retain the Hamming-slice lower bound while giving the arithmetic counting identity a succinct normalized proof.

Remove every selector. Encode `sum_i x_i=m/2` by a balanced tree of ripple additions, each local gate expressed by all forbidden Boolean tuples, and keep the zero-input unit axioms. This is the exact linear-size, width-five `F_d` defined in `PROOF.md`.

Three independently checkable facts drive the result:

1. On each four- or five-variable gate, the affine arithmetic residual expands in its forbidden-tuple axioms with mass 18 or 36.
2. Positional weights telescope over carries and over the addition tree; after dividing by `m/2`, the explicit total certificate mass is `72d-102+106/m`.
3. For every weight-`m/2` input there is a valid gate/root extension. Any proof using at most `m/2` input unit groups vanishes on an extension avoiding those groups, a contradiction.

Thus the final family has logarithmic fractional mass and linear support/integer mass, with linearly many input variables and clauses. The entire proof is algebraic and combinatorial; computation checks local identities, actual generated certificates, exact size counts and the lower-bound witnesses. No numerical LP optimum is required.

**Outcome.** The theorem is a rigorous quantitative answer for a familiar encoding of an elementary cardinality contradiction. A complete solution of the original qualitative open-ended request is deliberately not asserted. The unresolved issue is the intended strength/naturalness of the example, not a missing step in the displayed separation theorem. Neither a novel-discovery claim nor a superpolynomial separation follows.
