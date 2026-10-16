# Independent adversarial audit: global action and topology

Audit date: 7 October 2026.

## Verdict and pinned object

**Accept the mathematical argument in the pinned candidate. No fatal gap, counterexample, or required correction was found.** The argument proves the stated stronger theorem: a finite-dimensional complex unimodular Lie algebra admitting a transverse pair of homomorphisms into a complex semisimple Lie algebra of the same dimension is semisimple. The post-Lie reduction then proves the specified perfect-source, semisimple-target nonexistence statement.

This is an audit of the argument, not a historical novelty claim, a claim of exhaustive literature review, or a statement of external peer acceptance. I independently recalculated the group-action identities and checked the global topology. I did not consult another reviewer's report.

Pinned candidate:

- `PROOF.md`, SHA-256 `2ac96492f1791f7fa2d5e988a7a44f60040395f6f2994649441755559c01f7f1`.
- `SOURCES.md`, SHA-256 `46b03c8ce7a98b555b37e29137d75eb2e2cbcfb249e9e889f36545e2bb75d25b`.

The files were not edited during this audit. The verdict applies to these bytes.

## 1. The exact mathematical target

The original Oberwolfach report, printed p.2689, distinguishes three matters: a semisimple-source rigidity theorem, nilpotent-target conjectures, and the conjectured extension of the displayed `sl_3(C)` target proposition to every semisimple target. The candidate addresses that last statement, with source perfect and nonsemisimple. It does not reverse the brackets or claim to settle the adjacent nilpotent-target questions. The subsequent paper's Section 3 expressly works over the complex numbers. [Original report](https://ems.press/content/serial-article-files/48175), [author's 2024 paper](https://homepage.univie.ac.at/dietrich.burde/papers/burde_78_perfect.pdf).

The theorem actually audited assumes only source unimodularity. Neither solvability of the source, nilpotence of its radical, algebraicity of either homomorphism, nor a supplied global form of either group is used.

## 2. Integration and conventions

Let `D = j_1 - j_2`. Because `D` is an isomorphism, the source and target complex dimensions agree. Choose simply connected integrations `G` and `N`. Both homomorphisms integrate on the same `G`; the target may also be chosen simply connected. Integration requires no faithfulness or closedness of the images.

The proposed formula really is a left action:

`A_h(A_k(p)) = J_1(hk) p J_2(hk)^{-1}`.

For a matrix calculation, the fundamental tangent vector at `p` is `j_1(x)p - p j_2(x)`. Left translation by `p^{-1}` sends it to

`B_p(x) = Ad_(p^{-1}) j_1(x) - j_2(x)`.

This calculation fixes the signs and the use of left rather than right trivialization. It remains valid intrinsically. A possible convention in which fundamental vector fields form an antihomomorphism is irrelevant: the argument uses the actual derivative of this explicitly defined action and its equivariance, not an asserted bracket convention for those vector fields.

At the identity, the orbit differential is `D`. The complex inverse function theorem therefore supplies a genuine nonempty open subset of `N` in the orbit. Translating that neighborhood by the action shows the whole orbit is open.

## 3. Determinant identity checked independently

For `h in G`, write `q = A_h(p)`. Homomorphism equivariance yields

`j_i(Ad_(h^{-1}) x) = Ad_(J_i(h)^{-1}) j_i(x)`.

Consequently,

`Ad_(J_2(h)) B_p(Ad_(h^{-1}) x)`

`= Ad_(J_2(h) p^{-1} J_1(h)^{-1}) j_1(x) - j_2(x)`

`= B_q(x)`.

Thus the candidate's equation (1), including its inverse and its placement of `J_2`, is correct.

Choose fixed complex bases once. The determinant of `B_p` is a single-valued global holomorphic scalar function: the left trivialization of a Lie group's tangent bundle is global, and `p -> Ad_(p^{-1})` is holomorphic. No local volume chart, logarithm, or determinant-line trivialization must be patched.

For any connected complex group `Q`, the character `det Ad: Q -> C^*` has differential `x -> tr(ad x)`. If this is zero, the character is locally constant and hence identically one. This is the complex determinant itself, not merely its absolute value. Source unimodularity gives this for `G`; target semisimplicity gives it for `N`. Taking determinants in the identity above therefore gives exact invariance of `f(p) = det B_p`.

On the initial orbit, `f` has the nonzero constant value `f(e)`. The several-complex-variable identity theorem on the connected manifold `N` applies to `f - f(e)`. Thus `B_p` is invertible everywhere. Every orbit contains a neighborhood of each of its points, so every orbit is open. If there were two orbits, one orbit and the union of all the others would disconnect `N`.

There is no hidden density, algebraic-group, or closed-image assumption in this step.

### Independent robustness check: analytic continuation is unnecessary

One can check this conclusion without the identity theorem. Let `U` be the initial orbit. Continuity gives `f(p) = f(e) != 0` for every `p` in the closure of `U`. Each such point has an open orbit. That orbit intersects `U`, because it is a neighborhood of a point in the closure of `U`; hence it is `U`. Therefore `U` is also closed. Connectedness gives `U = N`.

This alternative validates the potentially surprising completeness step by a separate elementary argument. It also shows that the obstacle in a direct real-form proof is later topology, not analytic continuation.

## 4. The orbit map really is a covering

The stabilizer `H = {h: A_h(e) = e}` is closed by continuity. Its Lie algebra is the kernel of `B_e`, so it has dimension zero and is discrete.

After transitivity has been proved, the induced map `G/H -> N` is a bijection. Its differential is invertible at every point, by translation of the orbit differential, so it is a local holomorphic isomorphism and hence a global holomorphic isomorphism.

Here `G/H` means right cosets, as appropriate for a left action. A closed discrete subgroup acts properly discontinuously on `G` by right translations. Explicitly, choose a neighborhood `W` of the identity with `W^{-1} W intersect H = {e}`. Its distinct right translates are disjoint, and their projections provide evenly covered neighborhoods. Thus `G -> G/H` is a covering, not merely a surjective local diffeomorphism.

The total space is connected and the base `N` is simply connected, so the covering has one sheet. The fiber over the identity is exactly `H`, whence `H` is trivial. The candidate correctly concludes a manifold isomorphism, without mistaking the orbit map for a homomorphism of groups.

## 5. Topology of the source and the degree comparison

Take a Levi decomposition `g = s semidirect r`. Integrate the action of `s` on `r` using simply connected groups `S` and `R`. The resulting semidirect product is simply connected, has Lie algebra `g`, and is therefore the chosen `G` by uniqueness of simply connected integration. Its underlying manifold is `S x R`.

This construction avoids the dangerous claim that a radical or Levi subgroup in an arbitrary connected global form must already have the desired topology. The argument constructs the simply connected product first. No torus or discrete quotient survives in its radical factor.

The candidate's induction proving contractibility of `R` is valid. A nonzero solvable algebra has a nonzero functional killing its derived algebra. Its kernel is a codimension-one ideal. A vector outside the kernel spans a complementary one-dimensional subalgebra, so the algebra splits as a semidirect product by the additive complex line. Iteration gives an underlying manifold `C^q`. The argument does not claim the exponential map is a diffeomorphism for all solvable groups; that false stronger assertion is unnecessary.

Let `d = dim_C n = dim_C g` and `s = dim_C s`. A compact real form of `N` has real dimension `d`, because its Lie algebra complexifies to `n`. A compact real form of `S` has real dimension `s`. Compact connected Lie groups are orientable, so the top integral homology in these degrees is `Z`. Ordinary singular homology, rather than compactly supported homology, is being used. Hence

- `H_d(N; Z) = Z`;
- `G` is homotopy equivalent to an `s`-dimensional compact manifold;
- if the radical is nonzero, `s < d` and `H_d(G; Z) = 0`.

This contradicts the manifold isomorphism. In particular, the candidate does not confuse the real manifold dimension `2d` of `N` with the real dimension `d` of its compact deformation retract. The zero-dimensional case is harmless.

### Classical-source scope verified

Etingof's MIT notes state integration over both `R` and `C` in Theorems 9.12–9.13 and Corollary 9.14, printed p.55. Theorem 49.1, p.265, covers simply connected solvable groups. Corollary 49.6, p.266, explicitly covers arbitrary simply connected complex Lie groups and their Levi-factor compact homotopy type. Corollary 43.5 ensures compactness of simply connected compact semisimple forms; Theorem 43.7, Corollary 43.8, and the following covering discussion, p.233, supply polar decomposition. These inputs have the scope required here. [MIT notes](https://ocw.mit.edu/courses/18-755-lie-groups-and-lie-algebras-ii-spring-2024/mit18_755_s24_lec_full.pdf).

## 6. The post-Lie reduction

For a post-Lie product, the derivation identity places `L(x)` in `Der(n)`. Semisimplicity makes `ad: n -> Der(n)` an isomorphism, so `R = ad^{-1} L` exists linearly and uniquely. The representation identity gives

`R([x,y]) = {R(x), R(y)}`.

The skew-product identity gives

`[x,y] = {R(x),y} + {x,R(y)} + {x,y}`.

Adding these formulas verifies that `R + I` is a Lie homomorphism. Thus `j_1 = R + I`, `j_2 = R` are exactly the required transverse pair. Finally, `tr(ad [x,y]) = tr([ad x, ad y]) = 0`, so perfectness makes the source unimodular. Every implication uses the correct bracket.

## 7. Counterexample and scope stress tests

### Nonunimodular source: the determinant really can vanish

Take `n = sl_2(C)` with basis `(H,E,F)` and `[H,E] = 2E`. Let the source be the direct sum of the upper Borel `span(H,E)` and the one-dimensional abelian algebra `C F`. Set `j_1(H)=H`, `j_1(E)=E`, `j_1(F)=0`, and `j_2(F)=F`, with `j_2(H)=j_2(E)=0`. The difference is invertible, but the source has `tr(ad H)=2`.

For `p = [[a,b],[c,d]]` in `SL_2(C)`, direct calculation in the basis `(H,E,F)` gives

`B_p = [[ad+bc, cd, 0], [2bd, d^2, 0], [-2ac, -c^2, -1]]`,

and therefore `det B_p = -d^2(ad-bc) = -d^2`.

It is nonzero at the identity and zero on the locus `d=0`. Thus there is an open cell but no transitivity. The formula was also checked symbolically. This reproduces the mechanism behind the familiar Borel/triangular examples and verifies that unimodularity is doing essential work, rather than being superfluous rhetoric. The published triangular examples and solvable-unimodular obstruction agree with this test. [Burde–Dekimpe, Sections 2–3](https://arxiv.org/pdf/1108.5950).

### Reductive target: actual examples do not contradict the theorem

The 2024 paper's Example 3.13 has source `sl_2(C) semidirect C^2` and target `sl_2(C) direct-sum C^2`. The target has a two-dimensional center. Its compact homotopy dimension is three, not its total complex dimension five, and its derivations need not be inner. Both target-specific mechanisms in this proof are therefore unavailable. [Example 3.13](https://homepage.univie.ac.at/dietrich.burde/papers/burde_78_perfect.pdf).

### Real forms: topology differs, but complexification recovers the theorem

For real semisimple groups, compact homotopy dimension is not their real Lie algebra dimension. The simply connected integration of `sl_2(R)` is contractible, as follows by lifting the `SO(2) x R^2` decomposition of `SL_2(R)`. Thus a direct real version of the top-degree contradiction would be invalid.

This does not supply a counterexample to the algebraic statement. A real transverse pair can be complexified. Real unimodularity becomes complex unimodularity, a real semisimple target has semisimple complexification, and invertibility survives scalar extension. Applying the audited complex theorem gives semisimplicity of the complexified source, hence of the original source. The candidate only says its direct dimension argument is not asserted for arbitrary real forms, which is correct. No change to the stated complex theorem is needed.

## 8. Disposition

All essential steps pass: integration, determinant equivariance, global transitivity, discrete-stabilizer covering, simply connected Levi topology, compact-form dimension, and the post-Lie reduction. The proof's conclusion does not rely on the finite example or a literature search. No additional substantive assumption was found necessary.

Nonblocking editorial options are to add the closure-of-orbit proof of transitivity and to mention the complexification consequence if real scope is discussed. Neither is a repair of a mathematical gap. No claim of historical priority or external acceptance is justified by this audit.
