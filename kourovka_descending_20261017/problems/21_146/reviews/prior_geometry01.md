# Independent audit: ascending-torus and geometric finiteness

Audit checkpoint: **2026-10-17T20:45:36Z**. Completion estimate: **100% of the assigned first-pass geometric audit** (this is not a probability that the entire manuscript is correct, and is not an estimate of completion of the research problem). Reviewer: independent subagent `p21146_claim_geometry`. No other reviewer verdict was read before this report. No external individual was contacted. No Git operation or publication was performed.

## Source and precise scope

Prior claim: OpenAI, *A universal group of type F-infinity*, manuscript dated September 23, 2026. Audited version is Git commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a`:

<https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/A-universal-group-of-type-F-infinity-September-23-2026/paper.pdf>

The cached PDF and a fresh read of the pinned raw PDF both have SHA-256 `67e7907dc8afc00512ff80ba196072860e0d237e5703d9f013af4dbfde835733`. Its printed and PDF page numbers agree. I read the text of Sections 5-8 and the construction interface in Sections 3-4; I also visually inspected complete PDF pages 14-17 to verify the sensitive coefficient and cellular formulas.

The exact target of this audit is the implication asserted by Theorem 5.1 (p. 8): an injective endomorphism `f: U -> U` factoring through a finitely presented group, together with the two specified finite orthogonal-idempotent homomorphism diagrams, produces an embedding into an ascending HNN group of type F-infinity. I tested the finite-presentation lemma, the controlled-chain input, the product-module argument, the ascending-HNN sequence, the geometric passage, and the formal application to the universal finitely presented group. I do not independently certify Higman's theorem, the existence/enumeration construction in Lemma 2.2, or every finite-idempotent relation in Lemma 3.1; those are separate inputs.

## Verdict within this scope

**No fatal gap or counterexample found in Theorem 5.1's geometric/ascending-torus argument.** The passage from Proposition 6.2 to a classifying space with finite skeleta survives the attempted objections below. I also reconstructed the control mechanism in Lemma 6.1 and Proposition 6.2 rather than treating the uniformity assertion as an unsupported black box. Conditional on the finite-diagram additivity Lemma 3.1, that mechanism closes its induction with the quantifiers needed in Section 7.

This is a scoped favorable audit, not a claim of independent discovery and not by itself a determination that Kourovka 21.146 is already solved. To promote the entire prior claim, the independent audits of the universal-group and finite-diagram construction must also pass, and the relevant literature/status must be assessed separately.

## Reconstruction of the implication

### 1. Finite presentation (Lemma 5.2, pp. 8-9)

Write `f=ba`, with `a:U->P`, `b:P->U`, and `P` finitely presented; put `g=ab`. The two claimed maps are legitimate:

\[
\Phi:T(U,f)\to T(P,g),\quad u\mapsto a(u),\quad t\mapsto s,
\]
\[
\Psi:T(P,g)\to T(U,f),\quad p\mapsto t b(p)t^{-1},\quad s\mapsto t.
\]

The relation in the first target follows from `af=ga`. For the second, conjugating `t b(p)t^{-1}` by `t^{-1}` gives `b(p)`, while the image of `g(p)` is `t f(b(p))t^{-1}=b(p)`. Their composites are the identity using the defining relations, without assuming `g` injective. Thus `T(U,f)` is isomorphic to the group presented by the finite presentation of `P` plus one stable letter and finitely many generator conjugation relations. There is no hidden assumption that `U` is already finitely presented in this lemma.

One additional use of this factorization occurs in Proposition 6.2's degree-zero base case: the finitely generated group `b(P)` contains `f(U)`. This supplies paths from `1` to every `f(u)` using one finite edge-difference set. The paths can have unbounded length, which is permissible.

### 2. The exact uniformity needed (Proposition 6.2, pp. 12-13)

The required statement is

\[
\forall n\ge0\ \forall A\text{ finite bound}\ \exists k,B\ 
\forall z\in Z_n(C_*^A(U))\ \exists y\in C_{n+1}^B(U):
\quad\partial y=(f^k)_*z,
\]

with reduced cycles in degree zero. In particular `k` and `B` precede `z`. A claim allowing `k` or `B` to depend on an individual coordinate cycle would not suffice for the product-module step.

Here the induction does obtain the displayed order. In extending the controlled partial homotopy through a fixed degree `q<n`, the prospective boundaries `F(a)-H_{q-1}(partial a)` for **all** normalized basis simplices share one finite bound. The lower-degree assertion supplies a common iterate and output bound for this entire family. Postcomposing all previous homotopies by that iterate preserves their equations because every group homomorphism fixes `1`. A filling can then be chosen separately for every basis simplex and extended linearly. The construction does not need a finite basis as an abelian group, an equivariant choice, or a uniform filling length.

The missing degree-`n` homotopy is replaced by the idempotent diagrams. Lemma 6.1 gives additivity in one bounded homology group for the finite collection of all orthogonal relations; its common full-identity value is the class of `(f^(k+1))_*z`. Lemma 3.1 then kills that class by both `2` and `3`, hence integrally. There is no change of coefficient ring in this last inference.

### 3. Controlled additivity (Lemma 6.1, pp. 10-12)

I checked the points at which ordinary, non-equivariant chain homotopies could have lost control:

- Truncating `H` by `H_n=0` makes `F'=F-partial H-H partial` a chain map with `F'_0=c_0` and `F'_q=0` for `0<q<n`; on an `n`-cycle, `F'z=Fz`.
- The Alexander-Whitney and shuffle maps use only input vertices in each coordinate. The recursive homotopy from the diagonal to their composite fills inside the full tuple complex on `V x V`, where `V` is the finite vertex set of the input simplex. Its control is therefore in relative differences, independent of the locations of `V`.
- For the tensor homotopy, the factor `(-1)^deg(a)` in `K(a tensor b)=H(a) tensor F(b)+(-1)^deg(a) F'(a) tensor H(b)` gives `partial K+K partial=F tensor F-F' tensor F'`. There is no missing sign at that point.
- Only the `(0,n)` and `(n,0)` Alexander-Whitney terms survive after applying `F' tensor F'` to a cycle. The constant vertex is `1`, so the resulting two terms are precisely the two summand maps, without uncontrolled translations.
- Elementwise commuting images make `(u,v) -> h_1(u)h_2(v)` a group homomorphism. If coordinate-difference bounds are `B_1,B_2`, its output differences lie in the finite set `h_1(B_1)h_2(B_2)`. Thus it is legitimate to apply it to the non-equivariant homotopy.

These checks include `n=1`, when the interval of mixed positive bidegrees is empty. No use of a nonexistent uniform bound on vertex positions or chain lengths was detected.

### 4. The ascending HNN group and sign (Section 7.2, pp. 14-16)

For injective `f`, the direct limit `L=colim(U --f--> U --f--> ...)` contains every stage. The automorphism shifting the stage index makes `T(U,f)` isomorphic to `L rtimes Z`, with `t^{-1}ut=f(u)`. This establishes the base-group injection independently of any word-problem assumption.

The coset tree has vertices and oriented edges `jU`, with edge `jU -> jtU`; well-definedness uses `ut=tf(u)`. Every vertex has one outgoing edge and a height increasing by one. The representation `j=t^p u t^{-q}` shows every forward ray meets the standard ray, hence connectedness; a least-height vertex in a simple undirected cycle would have two outgoing edges, hence no cycle. Both orbit stabilizers are `U`.

On the induced resolution, the terminal map is

\[
E(j\otimes c)=jt\otimes f_*c.
\]

Balancing works because `jut=jtf(u)`. The cone of `1-E` resolves `Z`: the homology of the induced complex is the vertex permutation module, and the residual complex is the tree's exact augmented cellular complex. Tensoring gives the stated exact sequence with

\[
F(m\otimes c)=mt\otimes f_*c.
\]

The multiplier really is `t`, and there is no unacknowledged reversal of the HNN convention.

### 5. Product modules (Section 7.3, pp. 16-17)

For a finite bound `A`, the module `C_q^A(U)` has a finite set `S_q(A)` of free `ZU` basis types, obtained by translating the first vertex to `1`. Consequently

\[
(ZJ)^I\otimes_{ZU} C_q^A(U)
\cong\bigoplus_{s\in S_q(A)}(ZJ)^I
\cong\prod_{\alpha\in I}\bigoplus_{s\in S_q(A)}ZJ.
\]

Only a **finite** direct sum is interchanged with the product. This is the crucial valid restriction. Degreewise inclusions for nested bounds are split free-basis inclusions, so tensoring does not introduce an injectivity problem even though a product of group rings need not be flat.

A tensor cycle has one common finite simplex-type bound. In a fixed coordinate it is a finite ordinary chain and splits into finitely many left-`U`-coset cycles. Proposition 6.2 supplies the same `k,B` for all these cycles in all coordinates. Under `F^k`, a tuple's origin becomes `jt^k`, and the relative vertices are mapped by `f^k`. Filling separately in each coset and coordinate gives coordinatewise finite chains of the common bound `B`, hence a genuine tensor chain by the preceding identification. Two input cosets may merge after right multiplication by `t^k`; adding their finitely many fillings causes no problem.

Thus every individual positive-degree homology class is killed by some `F^k`. The proof needs local nilpotence, not a single global nilpotence exponent on the whole homology group. The finite geometric series makes `1-F` invertible. In degrees `n>=2` both adjacent terms of the long exact sequence have positive degree, yielding `H_n(J,(ZJ)^I)=0`. No assertion about degree zero is being smuggled in.

### 6. Geometric finiteness (Lemma 7.1, pp. 13-14)

This step proves more than an unqualified assertion of homological finiteness. Begin with a finite presentation complex `X_2`. If `X_n` is finite and its universal cover `Z` is `(n-1)`-connected, extend `Z` by unrestricted higher cell orbits to a contractible free `J`-complex `Y`. The chain modules in degrees at most `n` stay finite-rank free over `R=ZJ`.

Let the index set `I` consist of all cellular `n`-cycles of `Z`. Since the chain module in degree `n` has finite rank, the family containing **every cycle as its own coordinate** defines a tensor cycle in `R^I tensor_R C_n(Y)`. Its vanishing homology class gives one tensor boundary; any such tensor involves only finitely many basis elements of `C_(n+1)(Y)`. Taking coordinates shows their cellular boundaries generate the entire `n`-cycle module over `R`.

Since `Z` is simply connected and `(n-1)`-connected with `n>=2`, the Hurewicz isomorphism supplies sphere representatives of those finitely many module generators. Naturality and canonical basepoint changes give the needed deck-transformation module compatibility. Attaching their orbits kills `pi_n`, leaves lower homotopy groups unchanged, and adds finitely many cells downstairs. The union over `n` has finitely many cells in each dimension; cellular approximation places any sphere in the corresponding finite-dimensional stage, where it is killed at the next stage, and Whitehead's theorem then makes the universal cover contractible.

No geometric-dimension bound, torsion-freeness, asphericity of the finite presentation complex, or finiteness of the auxiliary resolution was assumed. In particular, torsion in a universal group is not an objection to F-infinity: the final classifying space can be infinite-dimensional.

## Construction interface and the actual quantifiers

Corollary 4.2 (p. 7) and Section 8 (p. 17) formally meet both hypotheses of Theorem 5.1 if their earlier construction inputs are valid:

1. The one chosen `U` is finitely presented and universal for finitely presented groups.
2. Proposition 4.1's finite envelope embeds back into this same `U` by universality. Postcomposition carries all identities to endomorphisms of `U`, and preserves injectivity of the common distinguished map.
3. The factorization hypothesis is satisfied with `P=U`, `a=id`, `b=f`. There is no demand for the envelope itself to have F-infinity or for its faithful algebra model to be finitely presented.
4. The resulting target `H=T(U,f)` is chosen once. Only the final map `G->U` varies with a finitely presented input `G`. Thus the asserted result is a single universal target, not merely separate targets for individual inputs.
5. For every finite integer `n>=3`, a group of type `F_(n-1)` is finitely presented, so this prior claim, **if fully verified**, supplies an F-infinity target and hence an F_n target for the official Kourovka quantifiers. This deduction does not need a word-problem restriction.

The geometric theorem does not make universality circular: finite presentation is established before the homology argument, and universality is used to construct endomorphisms before applying the geometric theorem.

## External dependencies checked

The geometric proof is sufficiently explicit that it does not need an unverified appeal to the full Bieri-Eckmann/Brown finiteness criterion. I reconstructed the relevant product-module argument directly above; the papers cited as [1] and [2] were not independently re-read for this audit and are not being used as substitutes for that reconstruction.

I checked the author's primary online text of Allen Hatcher, *Algebraic Topology*, at <https://pi.math.cornell.edu/~hatcher/AT/AT.pdf>: the natural absolute Hurewicz map and its isomorphism statement (printed pp. 370-371, Theorem 4.37, PDF pp. 378-379), cellular approximation (printed p. 349, Theorem 4.8, PDF p. 357), and Whitehead's theorem (printed p. 346, Theorem 4.5, PDF p. 354). These supply precisely the topological facts used in the cellular construction. The simple-connectivity condition needed for Hurewicz holds upstairs.

The manuscript gives explicit Alexander-Whitney, shuffle, and controlled diagonal-homotopy constructions (pp. 10-11), which I checked locally. I did not retrieve the 1953 Eilenberg-Zilber paper; no additional support-control conclusion is being assumed from that citation. The companion manuscript [9] is not necessary for any step reconstructed in this report and was not used.

## Strongest verified result and exact remaining gap

The strongest result certified by this review is: **assuming the finite-idempotent additivity Lemma 3.1, the stated hypotheses of Theorem 5.1 imply that `T(U,f)` contains `U` and has a single K(pi,1) with finite skeleta in every degree**. The proof's exponent/bound quantifiers and the ordinary-chain-to-product-module conversion are adequate. The formal Section 8 application also has the correct quantifiers, conditional on the independent construction inputs.

No unresolved central difficulty was found in this geometric route. The remaining gap in this review's coverage is outside the assigned geometric scope: independently certifying the finite operator systems/additivity and faithful finite envelope, and the universal finitely presented group input. A lack of a word-problem algorithm or explicit computable sphere list is not such a gap, since the claim is existential.

## Checkpoint log

- **2026-10-17T20:44:58Z; 90% audit completion:** finite presentation, HNN sign, product-coordinate finiteness, and cellular induction reconstructed; cached PDF hash confirmed. No fatal issue identified.
- **2026-10-17T20:45:36Z; 100% assigned first-pass audit completion:** pinned source hash matched, controlled-chain uniformity and universal-construction interface checked, relevant primary Hatcher results verified, and this independent scoped report recorded. No conclusion about publication status or a new solution is authorized by this checkpoint.
