# Second independent geometry audit: tangent-Seshadri candidate 30004324

Date: 2026-10-05.

## Verdict

**PASS, as an independently checked mathematical candidate.** I found no essential mathematical gap in the frozen argument. In particular, its passage from positivity at one arbitrary point to Picard number one and then to the Fano case survives this audit in arbitrary characteristic.

This is a review of an argument, not a refereed resolution, formal verification, or priority determination. The shortness of the argument compared with the stated literature status warrants review by a specialist before any announcement that the conjecture has been settled. Finite tests are not evidence for the geometric assertions.

**First essential gap:** none found. Some compressed standard steps deserve the explicit justifications given below, especially projectivity of the evaluation fiber. None requires an additional hypothesis on X, the point, or the characteristic.

The mathematical assessment was formed by reconstructing the frozen candidate from its hypotheses and checking its primary sources, rather than treating any earlier verdict as mathematical evidence.

## Object reviewed

- Candidate: `candidate_proof.md`, 10,612 bytes, SHA-256 `eb96aab30ab17aca553ef83102145c5dd51b2c36895be2b2a028f5090b9aedc1`.
- Author archive: `TANGENT_SESHADRI_30004324_AUTHOR_SAFE_FREEZE.zip`, 19,163 bytes, SHA-256 `6483242536c534a84072815ae4c3aa9de57fd2769386eb2e5e1ad85041cc6a01`.
- Author manifest SHA-256: `4869e62250a25e64fc6e4096ea56842a7b23400789f3ba00c14ba81c2c8cd8f7`.
- The candidate in the archive was compared byte-for-byte with the candidate inspected. They agree. The author files were not edited.

The assertion reviewed is: if X is a smooth integral projective n-fold, n at least one, over an algebraically closed field of any characteristic and epsilon(T_X;x)>0 for one closed point x, then X is isomorphic to projective n-space. The proof does not replace x by a general point.

## 1. Source and hypothesis checks

The OWR contribution, printed p. 3289, matches the intended one-point characterization. FM21 Conjecture 4.9 supplies the precise smooth-projective, algebraically closed formulation. The final-numbering FM21 manuscript was inspected directly, including the relevant page images.

The exact FM21 dependencies checked were Example 3.20 and Corollary 3.21 for the normalized-curve formula; Corollary 4.6 for a rational curve through the specified point; and Proposition 4.8(1) for the Fano conclusion in arbitrary characteristic. The restriction to characteristic zero and to a general point belongs to the separate clause 4.8(2). The final invocation of clause (1) is consequently noncircular.

AO Theorem 2.8 and Section 2.5 were inspected directly. They provide the proper Artin stack of stable maps of fixed embedding degree and a projective coarse scheme over the field in question. Using an Artin stack here is important: inseparable stable maps can have nonreduced stabilizers. The proof need not claim that the entire moduli stack is Deligne–Mumford.

Public primary sources:

- Fulger–Murayama, [Seshadri constants for vector bundles](https://par.nsf.gov/servlets/purl/10198624).
- Fulger's contribution to [Mini-Workshop: Seshadri Constants](https://publications.mfo.de/bitstream/handle/mfo/3816/OWR_2019_53.pdf?isAllowed=y&sequence=1).
- Abramovich–Oort, [Stable maps and Hurwitz schemes in mixed characteristic](https://arxiv.org/pdf/math/9808074).

The proof can cite the established FM21 proposition directly. I did not independently re-prove Mori's classification or inspect the full text of Kollár V.3.2: the public publisher access located for the book was limited. This is a dependency boundary, not a substitution of a stronger general-point theorem for the proposition actually used.

## 2. Curve positivity and existence

For the normalization f:P1 -> C -> X of an integral rational curve containing x, write f^*T_X as the direct sum of O(a_i). Its asymptotic normalized minimum slope is min(a_i). In positive characteristic, every Frobenius pullback multiplies the splitting degrees by the corresponding power of the characteristic, which is canceled by the normalization in that slope invariant.

The normalized-curve formula therefore yields

    min(a_i) >= mult_x(C) epsilon(T_X;x) > 0.

Every a_i is an integer, so all a_i are at least one. Thus every rational normalization through this very same x is very free. This is stronger than the existence of some very free curve through x, and that distinction is decisive later.

The anticanonical intersection on C is the degree of f^*T_X and is positive. The optional stronger estimate n+1 is also justified: f is birational onto its image, hence generically an isomorphism to an open subset of C. Over the perfect base field C is generically smooth. The differential T_P1 -> f^*T_X is consequently generically injective; it is a nonzero map from O(2). One splitting degree is at least two.

This differential argument is not valid for a purely inseparable multiple cover, but the candidate expressly applies it to normalizations, where that problem does not arise.

Existence is furnished by the cited one-point corollary, whose proof explicitly produces a rational curve through x. No assertion that every positive-characteristic rationally connected variety is separably rationally connected is inserted here. The candidate's alternate specialization argument from a proper compactification of a covering family would also give a rational component through x, but the alternate route is unnecessary.

## 3. Why the pointed minimum excludes all boundaries

Choose very ample A. The set of A-degrees of rational images containing x is a nonempty set of positive integers, so its minimum d exists and is attained.

For a genus-zero stable map of A-degree d with its sole marked point mapping to x, the domain has rational components and a tree as dual graph. Starting at the marked component, any components encountered before the first nonconstant component are contracted to x. The first nonconstant component therefore has image C_v containing x. That image is rational: a nonconstant image of P1 has rational function field by Lüroth's theorem, also in positive characteristic.

The total degree is the sum of positive integers e_w(A.C_w), where e_w is the full function-field degree, including inseparable degree. Thus

    d >= e_v(A.C_v) >= A.C_v >= d.

Equality forces e_v=1 and leaves no positive degree for any other nonconstant component. This rules out reducible positive-degree limits and multiple covers at once.

There is a minor quantifier worth making explicit. The minimum was initially taken over curves over k, whereas properness is checked at all geometric points, including extension fields. A rational image of smaller degree over an algebraically closed extension would give a point of a finite-type Hom scheme over k, with the marked evaluation constrained to x. Nonemptiness of that scheme implies a k-point because k is algebraically closed. The k-map's rational image would have degree at most that smaller map degree, contradicting the definition of d. Hence the minimum remains a lower bound at the required geometric points. This uses neither uncountability nor a very-general-point choice.

Once there is only one nonconstant component, any connected contracted subtree has exactly one attaching edge to it. For t contracted vertices and m markings in that subtree, its total special-point count is

    2(t-1) + 1 + m <= 2t,

because the entire curve has only one mark. Stability would require at least 3t. No nonempty such subtree exists. Hence the complete domain is a smooth P1 and the map is birational onto its image.

The mark can initially lie on a ghost: the path argument accounts for this before the counting argument eliminates it. The proof does not assume that the mark initially lies on a nonconstant component.

## 4. Stabilizers, the actual scheme, and the actual universal curve

### 4.1 Full stabilizer group scheme

For a birational normalization f:P1 -> X, an automorphism preserving f is the identity on the dense open set where f is an isomorphism to its image. Thus the only geometric automorphism is the identity.

That statement alone would not remove nonreduced stabilizers in positive characteristic. The tangent space at the identity of the automorphism group is a space of vector fields v on P1, vanishing at the mark, with df(v)=0. Since df is generically injective and T_P1 is torsion-free, such a field vanishes. The finite stabilizer group scheme has one geometric point and zero tangent space, hence is the reduced identity group scheme. This is a full group-scheme argument, not just a count of automorphisms.

The inertia morphism for the proper stable-map stack is finite. On the evaluation fiber all its geometric fibers are the identity. The identity section then gives an isomorphism: locally, its augmentation ideal is a finite module with zero residue fibers, so Nakayama applies. The evaluation fiber is therefore an algebraic space. See [Stacks Project, Proposition 94.13.3, Tag 04SZ](https://stacks.math.columbia.edu/tag/04SZ).

### 4.2 Projectivity without assuming arbitrary coarse base change

This is the most useful expansion of the candidate's compressed wording.

Let M be the full proper one-marked stable-map stack and Q its projective coarse scheme. Let F=M_x be the evaluation fiber, now known to be an algebraic space. The restricted morphism

    F -> Q

is proper, because F is proper over k and Q is separated. It is quasi-finite: the coarse map identifies geometric points with isomorphism classes, so every geometric fiber has at most one point. Consequently F is a scheme and F -> Q is finite. Since a finite morphism is projective and Q is projective over k, F is projective. The selected reduced irreducible component H is therefore a projective integral scheme.

The scheme assertion follows from [Stacks Project, Proposition 67.50.2, Tag 03XX](https://stacks.math.columbia.edu/tag/03XX), and finiteness from [Lemma 37.44.1, Tag 02LS](https://stacks.math.columbia.edu/tag/02LS), after that assertion. This argument avoids relying on unrestricted formation of coarse moduli spaces under closed base change in wild characteristic. It is enough for everything in the candidate, even without a claim that F equals the scheme-theoretic evaluation fiber of Q.

### 4.3 Universal family and projectivity of its total space

There is a universal curve over the stable-map stack by the definition of its objects. Restricting to H gives a genuine family pi:U -> H, not merely a family on the coarse space whose descent is unproved. All its geometric fibers are smooth P1 by Section 3. The family is flat and finitely presented, so it is smooth, as well as proper. The marked section sigma is an actual section and e sigma is the constant map to x.

For completeness, U is projective too. The section of a smooth relative curve is an effective Cartier divisor. The line bundle O_U(sigma) has degree one on every fiber; its pushforward has rank two and its fiberwise evaluation gives the usual presentation of U as a projective-line bundle. Alternatively the relative anticanonical bundle supplies a relative ample line bundle. Thus the later use of complete curves in U is legitimate.

## 5. Dominance comes from deformation smoothness, not generic smoothness

Let f be the chosen normalization, with f(0)=x and infinity distinct from 0. Put E=f^*T_X. Since each a_i is at least one,

    H^1(P1,E(-0)) = 0,
    H^1(P1,E(-0-infinity)) = 0.

The first vanishing makes the Hom scheme fixing the value at 0 smooth at f. The second gives smoothness at f of its evaluation at infinity.

One can check the latter directly: for a square-zero extension, lift a map into the smooth target locally on an affine cover of P1, imposing the specified values at 0 and infinity. Differences of lifts form a Cech cocycle in E(-0-infinity) tensored with the extension ideal. Its H^1 vanishes, so the local lifts can be corrected and glued. Finite presentation then gives smoothness. This works over any field characteristic. Equivalently, the tangent evaluation is surjective by the cohomology sequence, with the same vanishing controlling obstructions.

The quotient group Aut(P1,0) is smooth. The parametrized Hom scheme presents the moduli of smooth pointed domains locally as its quotient by this group. At f the pointed moduli fiber is consequently smooth and has a unique local irreducible component. It is the component selected in the candidate. One may shrink to a neighborhood whose maps lie in that component.

The evaluation of the corresponding local family at infinity factors through e:U -> X. Smooth morphisms are open, so e(U) contains a nonempty open subset of X. On the other hand U is proper, so e(U) is closed. Since X is integral, the nonempty open subset is dense, and e is surjective.

None of this says that the fixed point x is general. None uses characteristic-zero generic smoothness. A mere dominance argument for an inseparable evaluation map would be inadequate; the explicit H^1 argument is what avoids that issue.

## 6. Descent and numerical generation

Let D be any Cartier divisor on X. The number b=deg(f_h^*O_X(D)) is constant on connected H: the Euler characteristic of an invertible sheaf on a proper flat family of curves is locally constant, and the genus is zero. Every f_h is birational onto its image, so this degree equals D.C_h. Similarly A.C_h=d.

For L=O_X(dD) tensor A^(-b), the restriction of e^*L to every geometric fiber of pi has degree zero. On P1 a degree-zero line bundle is trivial; this implication would fail on a positive-genus fiber, but those do not occur here.

Cohomology and base change gives B=pi_*e^*L locally free of rank one, with the evaluation pi^*B -> e^*L an isomorphism. A direct supporting reference is [Stacks Project, Lemma 37.33.2, Tag 0EX7](https://stacks.math.columbia.edu/tag/0EX7); its properness, flatness, reduced-base and structure-sheaf base-change assumptions hold. The stronger cohomology statement also follows from [Tag 0B91](https://stacks.math.columbia.edu/tag/0B91) and the fiber cohomology of O_P1.

Pullback along the genuine section gives

    B = sigma^*e^*L = (e sigma)^*L = L_x tensor O_H.

The last line bundle is trivial. A canonical choice of its trivialization is unnecessary. Hence e^*L is trivial on U.

To deduce numerical triviality downstairs, no separable multisection theorem is needed. For any integral curve Gamma in X, take its generic point eta. Because e is surjective, U_eta is nonempty. Choose a closed point of this finite-type k(Gamma)-scheme. Its residue field is a finite extension of k(Gamma). Its closure Gamma' in U, with the reduced structure, is an integral proper curve dominating Gamma with finite generic degree q>0. This is an especially economical substitute for cutting by general hyperplanes.

The projection formula yields

    0 = deg(e^*L | Gamma') = q deg(L | Gamma).

Here q includes any inseparable degree. It is a positive integer in an equality of integer intersection numbers, not a scalar in k that might vanish modulo the characteristic. Thus deg(L | Gamma)=0 for every Gamma.

It follows that d[D]=b[A] in N^1(X). Since D was arbitrary and A is ample on a positive-dimensional variety, rho(X)=1. Notice that this argument tests *all* integral curves Gamma on X, including curves avoiding x and curves of positive genus. It does not silently assume that rational curves generate all numerical curve classes.

## 7. Fano reduction

Apply Section 6 to D=-K_X. Section 2 gives b=-K_X.C>0. Thus d(-K_X) is numerically equivalent to bA, which is ample. Numerical invariance of ampleness and invariance under positive tensor powers show that -K_X is ample. This proves the required Fano hypothesis rather than assuming it.

FM21 Proposition 4.8(1) now applies with the original point x. This concludes the proposed characterization in every characteristic. For n=1 the argument is compatible with the direct degree calculation for the tangent bundle of a smooth projective curve.

## 8. Attempts to break the argument

1. **Purely inseparable covers:** their full degree contributes to e_v, so they cannot appear at the pointed minimum. They do not spoil the stabilizer argument.
2. **A contracted component containing the mark:** following the contracted tree still reaches a rational image through x. The one-mark stability count then removes the entire contracted tree.
3. **Two-marked ghosts:** they really do exist. One contracted component with two markings and one node has three special points. This does not contradict Section 3, which concerns the one-marked moduli space. The actual universal curve has unmarked points that may coincide with the existing marked point; no claim that every associated two-marked stable domain is irreducible is used.
4. **Only one very free rational curve through x:** insufficient. It can degenerate to a smaller non-very-free curve through x. The candidate assumes positivity along every rational normalization through x, so the minimum still has the required freeness.
5. **Product P1 times a positive-dimensional smooth variety:** tangent restriction along a ruling fiber has a trivial quotient, so the positivity premise fails. The fixed-point family of ruling fibers does not cover the product.
6. **Blowing up Pn at a point:** away from the exceptional divisor, the strict transform of the line joining the point to the center lies in a ruling fiber of the projection to P^(n-1). The tangent restriction has a trivial quotient when n>1, so this familiar source of quasi-lines does not satisfy the premise. Very free curves elsewhere cannot replace the minimum through x.
7. **A complete unpointed family:** does not suffice for the descent argument. The contracted section supplies the essential trivialization on the base, and is genuinely present here.
8. **A general-point theorem transplanted to a special point:** absent. The numerical argument is reconstructed directly for this point, and the final theorem used is the fixed-point Fano clause.
9. **Closed coarse base change in wild characteristic:** the finite-map construction in Section 4.2 removes the potential hidden assumption.
10. **The characteristic dividing q or d:** harmless. Numerical equivalence and intersection degrees are taken over integers or real numbers, not in the field k.

## 9. Comparison with standard family theory and literature status

The numerical-generation conclusion is consistent with the standard theory of unsplit rational-curve families. For example, Novelli–Occhetta's [Rational curves and bounds on the Picard number of Fano manifolds](https://iris.unito.it/bitstream/2318/1852269/2/0905.4388-NO2-RCBound.pdf), Lemma 2.12 and Corollary 2.13, record generation for the locus swept out from a point by an appropriate proper family. The latter corollary is stated at a general point because it starts only with generic local unsplitness. It does not forbid the candidate's conclusion, where properness at the particular x has already been proved. This source is a consistency check, not an imported positive-characteristic theorem.

Occhetta–Paterno's [Rationally cubic connected manifolds I](https://arxiv.org/pdf/1003.4936), in the inspected preprint's Proposition 4.3, similarly connects a proper pointed connecting family with projective space in its complex setting. Again, its additional setting is not used as a substitute for the candidate's proof.

Chang's [2025 revision on toric tangent sheaves](https://arxiv.org/pdf/2211.17172v2), pp. 1–2, states the unrestricted assertion as a conjecture and proves the smooth projective toric case. Its singular counterexample reinforces the necessity of smoothness. These observations justify caution about declaring a new solution; they do not identify a false inference in the present proof. Bounded searching is not a historical novelty certificate.

## 10. Recommended exposition, without changing the theorem

Before a specialist-facing revision, I recommend inserting four short details:

- Explain persistence of the minimal degree over algebraically closed extension fields.
- Replace the abbreviated projective-coarse-fiber sentence with the proper quasi-finite map to the full coarse scheme in Section 4.2.
- Note that the marking provides O_U(sigma) of relative degree one, so the universal total space is projective.
- Use the closure of a closed point in the generic evaluation fiber for the numerical pullback argument, avoiding unnecessary Bertini language.

These are explicit justifications of available standard steps, not repairs requiring a new geometric hypothesis. The frozen argument remains untouched. This report includes original mathematical analysis and public bibliographic references; no source PDFs, extracted source text, or source page images are included.
