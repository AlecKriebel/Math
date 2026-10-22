# Independent adversarial audit: rank 593 / problem 2807 / KP-3.9

Date: 2026-10-04 UTC. Audit target: the frozen eight-file public package whose SHA256SUMS has SHA-256 `697ef5b8667cba0b0bc6bc259fde7e6146275f693ce7d9125da00d720d572c64`.

## Verdict

**Pass as an explicitly unsolved, five-pass partial research attempt, with minor precision corrections recorded separately.** No fatal error was found in its self-contained mathematical conclusions. Theorem 4 holds for arbitrary finitely generated groups, including groups not assumed residually finite. Lemma 6 correctly transports trace characters over an algebraic closure of a finite field and detects positive dimension. The trefoil splice and closed-summand controls have exactly the limited consequences claimed.

This is **not** approval of a solution of KP-3.9, a new theorem priority claim, or an independent certification of the census examples. Keep `unsolved`, 5/5, and `full_candidate_saved: false`. The subjective 5% estimate is not a mathematical certificate.

All original public files were left unchanged. No remote write, queue write, contact with authors, or source-PDF redistribution occurred. No helpers were used.

## Integrity and replay

- Verified the supplied manifest hash and all seven hashes listed in it.
- Re-executed the frozen `controls.py`; `audit/controls-replay.json` is byte-for-byte identical to the frozen expected output.
- Independently checked the original four double-cover profiles using the sign-isotypic rational cellular/Fox complex rather than the author's lifted two-vertex chain complex.
- Independently re-enumerated the finite SL2 matrices and trace triples at 2, 3, and 5.
- Independently certified the quartic's irreducibility modulo 7 by exhaustive division by every monic degree-one and degree-two polynomial, a different certificate from the original Frobenius-power test.
- Computed the octic discriminant with an exact rational determinant of its Sylvester matrix: `242352128 = 2^17 * 43^2`.
- Checked the printed presentation's abelianization and an explicit trefoil-splice abelianization matrix.
- Verified all three locally held source PDF hashes and the selected upstream record hash against the frozen provenance. PDFs remain outside this audit's deliverables.

Run `python3 public/controls.py > audit/controls-replay.json` and then `python3 audit/independent_checks.py`. The second script uses only the Python standard library and imports none of the author's control code. Its saved output is `audit/independent-results.json`.

## Statement and source identity

The selected upstream record and the K3 author PDF agree on problem number KP-3.9 and the Haken/profinite target; the authoritative printed location is page 138. Problem 3.8 is the adjacent hyperbolic rigidity problem. The package expressly works in the intended compact, orientable, irreducible setting and restricts its surface proofs to the closed case. It does not exploit an omitted catalogue hypothesis or replace Haken by virtually Haken.

The key residual closed hyperbolic rational-homology-sphere case remains beyond the package. The reduction to that case is attributed to literature rather than newly proved here. The full hypothetical problem does not follow merely from having positive Betti number in a finite cover.

Primary references rechecked:

- [K3 author version](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf), printed page 138.
- [Cheetham-West–Lê, v1](https://arxiv.org/abs/2603.22543v1), Theorem 1.3, Lemmas 4.11–4.15, Example 5.4, and Section 6.
- [Garden–Tillmann, v2](https://arxiv.org/html/2411.06859v2), the trace-character construction, Theorem 24, Proposition 26, and Section 6.3.

The live arXiv submission history for Cheetham-West–Lê showed only v1. Additional targeted searches located no full resolution. This is a dated search finding, not proof that no later or unindexed result exists.

## Mathematical checks

### Lemmas 1 and 2: abelianization and finite-index profiles

The p-power Hom-count formula is correct. Its eventual first difference recovers the free rank, and successive differences recover the multiplicity of each p-primary cyclic factor. Finite generation is essential to the stated reconstruction and is present.

The finite-index correspondence and completion identification are valid without residual finiteness. There is one literal notation issue: for such arbitrary groups, a group need not embed in its completion. Thus “intersection” in Lemma 2 must mean inverse image under the canonical completion map. With i_G:G→Ghat, the exact operations are L↦closure(i_G(L)) and U↦i_G^(-1)(U). The normal-core argument in the proof supplies the full induced profinite topology. This correction does not alter the conclusion or require a residual-finiteness hypothesis.

### Lemma 3: a homology-dual incompressible surface

The regular level set represents a nonzero integral Poincaré dual. Compression preserves its homology class. A nonseparating compression reduces total genus; an essential separating compression splits a genus g component into strictly smaller positive genera and reduces the sum of their squares. The proposed lexicographic complexity therefore terminates. Irreducibility makes discarded spheres homologically zero, so a nonspherical component remains. The Loop Theorem gives injectivity. Closedness and orientability supply the required boundary and two-sidedness conditions.

### Theorem 4: dihedral quotient iff an index-two Betti jump

The proof survives all relevant extension issues:

1. An index-two subgroup H is normal. Conjugation by t∉H gives an involution on Hom(H,Q), because t²∈H acts by an inner automorphism.
2. Restriction Hom(G,Q)→Hom(H,Q) identifies its image with the +1 eigenspace. The extension value ψ(t²)/2 is legitimate over Q, including for nonsplit extensions.
3. A nonzero −1 eigenvector has finitely generated rational image because H is finitely generated by Schreier's theorem. Scaling produces a surjection φ:H→Z.
4. Anti-invariance forces φ(t²)=0. Thus mapping H by translations and t to a reflection respects both the conjugation and square relations. No assumption that t is an involution in G is needed.
5. Conversely, the preimage of the translation subgroup under an epimorphism to D∞ has index two, and its translation exponent is a nonzero anti-invariant class.
6. Lemmas 1 and 2 preserve the strict Betti jump, so the quotient property is profinite in the stated finitely generated category.

The finite controls agree: Z² has no jump; F2 has three jumps; D∞ has cover Betti numbers 0,0,1; the Klein-bottle group has cover Betti numbers 1,1,2. These controls supplement but do not replace the universal proof.

### Corollary 5 and the exact trefoil-splice control

The pulled-back dihedral action on a subdivided line has no fixed vertex and no inversion. Garden–Tillmann Proposition 26 supplies the topological input; irreducibility excludes sphere components. This proves sufficiency, not necessity.

For the control, choose oriented trefoil exteriors E_i and glue μ_1 to λ_2 and λ_1 to μ_2. The induced boundary matrix is a swap with determinant −1, so it is an orientation-reversing gluing and gives a closed orientable manifold. Both exteriors have incompressible boundary and are irreducible. The standard gluing lemma gives irreducibility; amalgam normal form gives injectivity of the gluing torus. Hence the torus is a two-sided essential surface.

On H1 the meridians generate and preferred longitudes vanish. The Mayer–Vietoris map is diag(1,−1), and the following H0 map is injective. Consequently H1(M;Z)=0; closed orientability then gives the full integral homology-sphere conclusion by duality.

As a separate exact algebraic cross-check, use trefoil group generators a,b with a²=b³, peripheral μ=ab^(-1), and λ=a²μ^(-6). In ordered generators a_1,b_1,a_2,b_2, the two trefoil relators and the two gluing relators have exponent matrix

    [ 2 -3  0  0 ]
    [ 0  0  2 -3 ]
    [ 1 -1  4 -6 ]
    [-4  6 -1  1 ]

Its determinant is 1. The topology argument, rather than this determinant alone, proves that the presentation describes the asserted Haken control. A perfect group cannot surject onto D∞ because its abelianization would then surject onto C2×C2. The essential torus rules out hyperbolicity. This is a counterexample only to necessity of the dihedral criterion, not a counterexample to KP-3.9.

### Lemma 6: trace-character transport and dimension

Each representation of a finitely generated group into SL2(F̄p) lands in one finite matrix group. Precomposition of its extension with a fixed profinite isomorphism is invertible. If two representations have equal trace functions on the original group, their extensions have equal trace functions on the completion: both functions take values in a common finite field and agree on a dense set. The converse follows from inverse transport. Thus the map descends to an actual bijection on characters, not just representations or conjugacy classes.

For precision, interpret the variety as the affine **variety of trace characters** in Garden–Tillmann's sense. Its points are exactly the characters just transported. Finite type over an algebraically closed field makes zero dimension equivalent to finitely many points; the trivial character ensures nonemptiness. Positive dimension yields a curve and an ideal point, to which Theorem 24 applies. No algebraic isomorphism, equality of full dimensions, or preservation of individual components is claimed.

Finite presentation is stronger than needed here but causes no problem. The algebraic-closure-of-finite-field restriction is essential for the finite-image argument: diag(t,t^(-1)) over an algebraic closure of Fp(t) has infinite order. Transfer to other algebraically closed characteristic-p fields must use scalar extension of the algebraic character construction, not finite-image transport in that larger field. The frozen text correctly separates these steps.

### Lemma 7 and the arithmetic control

If A∈SL2(K) fixes a lattice homothety class, AL=cL and determinant valuation gives 2v(c)=0. Hence c is a valuation unit and AL=L. In a lattice basis the matrix and trace are integral. A negative trace valuation therefore excludes a fixed vertex. A subdivision can remove any inversion concern before applying the topological theorem; the usual SL2 action already preserves types.

The quartic is primitive and retains degree four modulo 7. The independent lack of degree-one/two factors proves irreducibility modulo 7 and hence over Q. Its monic rational minimal polynomial is f/2 and has coefficient −17/2, so no root is an algebraic integer. A nonintegral square forces a nonintegral trace. Neither this calculation nor the replay identifies the trace in a particular manifold. The package correctly disclaims that further certification and correctly rejects direct extension of an unbounded representation to a compact profinite group.

### Lemma 8: failure of the general subgroup-pullback inference

The graph of multiplication by α is closed and its first-coordinate projection is an isomorphism with Zhat. The complement {0}×Zhat makes it a direct summand. For an integer point (m,n) in the graph, the 2-adic coordinate forces n=0, and any odd-adic coordinate then forces m=0. The displayed triangular matrix with diagonal 1 is a continuous automorphism with inverse obtained by negating α. Thus the example really is an automorphic image of the closure of Z×{0}.

No finite CRT sample proves the infinite intersection statement; the written coordinate argument does. The example does not satisfy the extra hyperbolic homology regularity that could constrain a geometric profinite isomorphism. It refutes only an unrestricted density/intersection argument. Section 6's discrete freeness question remains an unproved extra input, not a consequence of the example.

## Source-specific cautions

Cheetham-West–Lê Theorem 1.3 imposes extra hypotheses; Section 6 still discusses the general obstruction. Its positive-characteristic finite-image sentence is too broad as written. The frozen Lemma 6 repairs the relevant argument for trace characters. Condition (5) of Theorem 1.3 explicitly uses finitely many **conjugacy classes** and an algebraic representation with nonintegral trace. Preserve that exact hypothesis when summarizing the external result; finite characters alone should not silently replace it. This audit has not re-proved all external theorems cited in that preprint.

Garden–Tillmann Section 6.3's displayed relators were rechecked in the actual PDF image and text, as well as the HTML. Their exponent rows are (6,2) and (10,−5), giving C50. That conflicts with the following page's C40. The octic has discriminant 2^17·43², and modulo 43 it factors as

    2(s²+1)²(s²+19)(s²+17).

Thus there are six distinct roots over F̄43, two of them double, rather than eight. For every other odd prime the octic is squarefree. These exact defects do not create a curve and do not refute the source's qualitative dimension conclusion. No decision was made about which presentation/manifold identification should be repaired. The named census example remains quarantined.

## Publication gate and remaining gap

Publish or archive only as an unsolved partial attempt, with this audit and the precision notes retained. No promotion to `claimed_solved` or `already_solved` is justified. The frozen files can remain historical; apply any editorial changes to a new version rather than rewriting the freeze.

The missing step remains a valid transfer of a general separating incompressible surface in a closed hyperbolic rational homology sphere, beyond the special mechanisms, or a certified counterexample pair. This audit did not open a sixth search pass for that step.
