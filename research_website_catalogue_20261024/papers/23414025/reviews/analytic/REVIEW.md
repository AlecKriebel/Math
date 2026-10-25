# Analytic review — Zenodo 23414025

**Verdict: no substantive mathematical defect identified.** The four-page note supports its transverse-pair theorem over the complex numbers and its post-Lie nonexistence corollary. The proof depends on standard global Lie theory and ordinary singular homology, whose exact interfaces were checked directly. The computational evidence is auxiliary, not a substitute for those global steps.

## Reviewed identity and independence

The published paper is *Post-Lie nonexistence with a semisimple target*, dated 16 October 2026, version 1.0.0. Its four-page PDF has SHA256 `849aaf7d065061f0fb69e7f3c507d1c5c70301ededa142a61af11cbaddbef74d`. The verification ZIP has SHA256 `7b0142907fd2f5d453c095ed24176cbc0aad456eb9c54b01e81c74ba646b01ff`; the main TeX source has SHA256 `07e4dc2b7af5acd42ecd2c59863a67bc1ed722dcf038b8c656683c9c01ed5315`.

All four actual PDF pages, the complete main TeX, the full authored `PROOF.md`, `SOURCES.md`, and `check_algebra.py` were read. No historical reviewer reports, decisions, root-disposition files, or sibling opinions were opened. The authored proof/source documents contain candidate/awaiting-review status text, and the paper itself states that separate AI audits occurred. These incidental statements were read as part of the mathematical material and were not used as validation. No prior review verdict was consulted.

A fresh source compilation succeeds. Every page's extracted text exactly matches the corresponding published page. The binary PDFs differ, so byte-for-byte reproducibility is not claimed. Source identities, the rebuilt hash and the four text comparisons are in `source_bindings.json`; the build log is preserved.

## Precise mathematical scope

Theorem 1 concerns two finite-dimensional **complex** Lie algebras of the same dimension. The source `g` is unimodular, meaning `tr(ad_g x)=0` for every source element. The target `n` is semisimple. Two complex Lie algebra homomorphisms `j1,j2:g→n` have an invertible linear difference. The conclusion is that `g` is semisimple.

Corollary 3 uses the specified post-Lie identities on two brackets on a common finite-dimensional complex vector space. It concludes that a unimodular source admitting a post-Lie product with a semisimple target must be semisimple. Perfectness implies unimodularity, so the requested perfect, nonsemisimple-source case is excluded.

These are deductive mathematical statements, with no empirical assumptions. They do not assert the result for arbitrary real forms, positive characteristic, infinite dimension or merely reductive targets. No algebraicity, closedness or injectivity of either homomorphism image is assumed. The source need not be solvable, perfect, reductive or initially semisimple. The zero-dimensional case is included explicitly. The proof infers a manifold diffeomorphism during the argument, not a Lie algebra isomorphism merely from that diffeomorphism.

## Reconstructed argument

### 1. Integration and the determinant — page 2

Choose connected simply connected complex integrations `G,N`. The two Lie algebra maps integrate uniquely to holomorphic group homomorphisms. Their formula

\[
A_h(p)=J_1(h)pJ_2(h)^{-1}
\]

defines a global action: the reversed order of inverses in the right factor is exactly what makes `A_(hh')=A_h A_h'`. Thus the argument does not start with a local action whose completeness is unproved.

Differentiating the orbit map and left-translating its tangent vector to the identity gives

\[
B_p=\operatorname{Ad}(p^{-1})j_1-j_2.
\]

Its domain and codomain both have dimension `d`. At the identity it is the assumed invertible difference, so the inverse function theorem gives an open identity orbit. In fixed bases, `f(p)=det B_p` is a single globally defined holomorphic function, rather than a determinant in incompatible local charts.

I expanded the covariance formula independently. For `q=J1(h)pJ2(h)^{-1}`, equivariance gives

\[
B_q=\operatorname{Ad}_N(J_2(h))B_p\operatorname{Ad}_G(h^{-1}).
\]

The first term uses `j1 Ad_G(h^{-1})=Ad_N(J1(h)^{-1})j1`; the second reduces to `-j2`. The sign and the choice of the **second** homomorphism in the left factor are correct.

For a connected complex Lie group, the differential of `det Ad` is the trace of the adjoint Lie algebra action. Zero differential makes this character locally constant and hence equal to one on the connected group. The source hypothesis supplies this property for `G`; semisimplicity gives perfectness and trace zero for `N`. Consequently `f` is invariant under the action and equal to the same nonzero value on the open identity orbit.

The holomorphic identity theorem on connected `N` then makes `f` that constant everywhere. No compactness of `N` or polynomial/algebraic nature of `f` is required. Every orbit is therefore open. A partition of a connected space into open orbits can contain only one orbit, since any chosen orbit and the union of all other orbits would otherwise disconnect it. This establishes transitivity, the essential global step.

### 2. From transitivity to a genuine diffeomorphism — pages 2–3

The stabilizer `H` of the identity is a closed subgroup, as the inverse image of a point under the orbit map. Its Lie algebra is `ker B_e=0`, so it is discrete. The transitive homogeneous-space theorem identifies `G/H` with `N`.

The paper also checks the covering issue explicitly. A sufficiently small identity neighborhood `U` has `U^{-1}U∩H={e}`. The right translates `Uh` are disjoint and give the sheets over the quotient image of `U`; translates give these neighborhoods everywhere. Normality of `H` is unnecessary. Since the covering's total space is connected and its base `N` is simply connected, it has one sheet. Hence the orbit map is a diffeomorphism and `H` is trivial. The reasoning does not mistake an arbitrary surjective local diffeomorphism for a covering.

### 3. Radical and compact-form homology — pages 2–3

The solvable-group lemma is established by an explicit induction. A nonzero solvable algebra has a codimension-one ideal containing its derived algebra; any complementary line is a subalgebra. Exponentiating its derivation gives a holomorphic action of the additive complex line on the simply connected integration of the ideal. The semidirect product is simply connected and integrates the algebra, so uniqueness gives its product manifold structure. Induction yields a manifold diffeomorphic to complex affine space. This uses no false assertion that the exponential map of every solvable group is bijective.

A Levi decomposition writes the source algebra as its solvable radical acted on by a semisimple Levi factor. Integrating both simply connected factors and the action gives a simply connected semidirect product with the source Lie algebra. Uniqueness identifies this with `G`. This avoids any assumption about the image or closedness of an arbitrarily chosen Levi subgroup inside a different global integration.

The radical factor is contractible, so `G` has the homotopy type of a compact real form of its Levi factor. The target `N` has the homotopy type of its own compact real form. If `dim_C n=d` and `dim_C s=s`, the compact real forms have **real dimensions** `d` and `s`. A compact connected Lie group is orientable by left translation of an identity basis. Its top integral singular homology is therefore nonzero, specifically `Z`.

If the radical is nonzero, then `s<d`, so `H_d(N;Z)=Z` while `H_d(G;Z)=0`. The latter is homology above the dimension of a compact `s`-manifold. This contradicts the proved manifold diffeomorphism. Ordinary homology, not compactly supported cohomology or Lie algebra homology, is used throughout. Therefore the radical vanishes.

### 4. Post-Lie reduction — pages 3–4

The third post-Lie identity makes each left multiplication a target derivation. The second makes their assignment a source Lie algebra homomorphism. For a complex semisimple target, its Killing form is nondegenerate and its center is zero. The included trace argument correctly proves that every derivation is inner: for the unique element representing the functional `u↦tr(D ad u)` under the Killing form, cyclicity of trace gives `κ(Du,v)=κ([a,u],v)`. Nondegeneracy then gives `D=ad a`.

Thus a unique linear `R` satisfies `x·y={Rx,y}`. Injectivity of the target adjoint representation gives `R[x,y]={Rx,Ry}`. The first post-Lie identity gives

\[
[x,y]=\{Rx,y\}+\{x,Ry\}+\{x,y\}.
\]

Expanding the bracket of `(R+I)x,(R+I)y` verifies that both `R+I` and `R` are source-to-target homomorphisms and that their difference is exactly the identity. This is the correct sign convention and uses semisimplicity of the target, not the source. Finally, the trace-of-adjoint functional annihilates every source bracket because the trace of a commutator is zero. A perfect source is therefore unimodular, and Theorem 1 applies.

## Primary references and hypothesis matching

Fresh primary-source acquisitions and hashes are in `reference_acquisition.json`.

* [Etingof's MIT notes](https://ocw.mit.edu/courses/18-755-lie-groups-and-lie-algebras-ii-spring-2024/mit18_755_s24_lec_full.pdf): Theorems 9.12–9.13 and Corollary 9.14 explicitly cover finite-dimensional complex integration and uniqueness; Proposition 4.12 and Corollary 4.16 cover the closed stabilizer and homogeneous-space fibration. Theorem 48.9 provides Levi decomposition. Theorem 49.1 and Corollaries 49.5–49.6 support the solvable induction and semidirect-product topology. Corollary 43.5, Theorem 43.7, Corollary 43.8 and the covering discussion justify the compact real forms and polar decomposition for the chosen simply connected groups. Theorem 16.19 supplies Killing-form nondegeneracy in characteristic zero. The source's distinction between a general solvable group and a nilpotent exponential map is respected.
* [Hatcher](https://pi.math.cornell.edu/~hatcher/AT/AT.pdf): Proposition 1.32 requires path-connected spaces and a covering; these are established. Theorem 3.26(a),(c) applies to the closed connected compact real-form manifolds and supplies top homology and vanishing above their dimensions. It is not applied directly to the noncompact complex groups.
* [Baues](https://arxiv.org/pdf/0809.0824v1), §5.4.1, equation (5.3), Theorem 5.19 and Corollary 5.20: the credited determinant-character method genuinely precedes this paper in the affine setting. The present argument proves its group-target continuation step directly and does not apply an affine-space completeness theorem outside its domain.
* [Burde–Dekimpe–Vercammen](https://arxiv.org/pdf/1109.0251), Proposition 2.16, and [Burde–Dekimpe–Monadjem](https://homepage.univie.ac.at/dietrich.burde/papers/burde_78_perfect.pdf), Proposition 2.6, support the credited transverse-pair reduction. The latter's Theorem 3.10 and Propositions 3.11–3.12 have the special-case scope described in the introduction. Those special cases are contextual, not necessary premises in this proof.
* [Burde–Dekimpe](https://homepage.univie.ac.at/dietrich.burde/papers/burde_44_postlie_der.pdf), Theorem 3.3, is the earlier solvable-unimodular-source obstruction. The original [2023 Oberwolfach report](https://ems.press/content/serial-article-files/48175), printed page 2689, does formulate the desired extension from the `sl3(C)` target case to arbitrary semisimple targets. These checked historical passages establish the problem match, not current openness or exhaustive priority.

## Executable and independent controls

The published exact checker was inspected and replayed in isolated Python normal, `-O`, and `-OO` modes. Each exits successfully and reports 2,896 diagnostic conditions; outputs are preserved in `published_replay.json`. Its finite algebra, determinant covariance and boundary examples do not establish integration, transitivity, coverings or homology. Repeated interpreter modes are robustness checks, not independent proof families.

`fresh_algebra_controls.py` imports no submitted code and takes two different algebraic routes:

1. It builds `sl2` and `sl3` from matrix commutators and solves the complete linear derivation equations by exact rational elimination. The derivation dimensions are respectively 3 and 8, equal to the dimensions of the inner-derivation spaces; the Killing forms have full rank and all adjoint traces vanish. It independently constructs `sl2 ⋉ Sym^4(C^2)`, an eight-dimensional perfect unimodular algebra with a five-dimensional abelian radical, and verifies its Jacobi identities, derived rank and adjoint traces. This checks a nonsemisimple source boundary without pretending to search all possible post-Lie products.
2. It works symbolically over `Z[a,b,c,d]` rather than sampling group points. For the paper's actual nonunimodular example it checks both homomorphisms on every basis pair and the invertibility of their difference. Conjugation by the adjugate of the generic two-by-two matrix has determinant `(ad-bc)^3` on `sl2`; the example's infinitesimal determinant is `-d^2(ad-bc)`, hence `-d^2` on `SL2`. It is nonzero at the identity but vanishes at the Weyl element. This is an exact all-parameter negative control showing why dropping source unimodularity invalidates the transitivity step.

All fresh controls pass. Their source hash and exact results are in `fresh_algebra_results.json`. No numerical tolerance or floating-point matrix exponential is used. These calculations validate concrete algebraic identities and boundary mechanisms, not the universal theorem by finite exhaustion.

## Strongest verified claim and exact remaining limits

The strongest supported claim is Theorem 1 in its full stated scope: a finite-dimensional complex unimodular source admitting two homomorphisms with invertible difference into an equal-dimensional semisimple complex target is itself semisimple. The post-Lie nonexistence corollary follows with the paper's explicit bracket conventions. No substantive mathematical gap was identified.

The review does not certify first-ever priority, current openness, journal acceptance, conventional human peer review or formal machine verification. The paper's stated inaccessible Onishchik comparison remains a historical-priority limitation; no matching competing result was inferred from it, and that work is not a proof dependency. Real-form, reductive-target, positive-characteristic and infinite-dimensional generalizations were not established. No repairs or source changes were made.

Completion: **100% of the assigned analytic review**, not a claim of absolute certainty. All work is confined to this review directory; no website, spreadsheet, Git, publication, Zenodo or outreach action was taken.
