# Mathematical audit of Steinberg quotient problem 30006265

Audit date: 2026-10-11 UTC.

This is an AI-assisted mathematical audit and exposition, independently rechecked in a separate computational pass. It is not external human peer review or formal proof-assistant certification. Acceptance below is limited to the explicit theorem and the stated source-level interpretation.

## Verdict

**Accept the explicit counterexample and the good-characteristic literature interpretation, with the qualifications below.** The mathematics of the frozen counterexample passes. It does not justify a claim that the entire original all-characteristic geometric question has been independently solved.

The complete checked exposition is `EXPLICIT_PROOF.md`. The original candidate remains untouched: 4,668 bytes; SHA-256 `7da140525a0d0fb00c3642e2221fa235d8af30fc8147740366c1c3d69afbf302`.

## Findings on the frozen proof

1. **Symmetric-power convention: correct conclusion, qualify the explanation.** Sym⁴E is the induced module ∇(4), not automatically its linear dual. E ≅ E* does not make the symmetric and divided-power functors interchangeable in degree four. Replace the candidate's ambiguous “harmless dual convention” parenthesis with the precise convention and projective-line argument in the proof.
2. **Self-duality: correct.** The invariant form on V has Gram matrix with entries B(a,c)=B(c,a)=B(b,b)=1 in characteristic 3. The induced form on W is explicitly nondegenerate. The relevant symmetrizer has degree two, whose factorial is invertible.
3. **Filtration: correct.** Multiplication is surjective, its kernel is the invariant line k(ac−b²), and its quotient is ∇(4). Linear duality and W≅W* give the Δ-filtration. No assumption of Sym⁴E self-duality enters.
4. **Invariants/functionals: correct.** Wᴳ=k(ac−b²), and every invariant functional vanishes on this line. Coefficient comparison is for the entire algebraic root subgroup, not just its three F₃-points.
5. **Indecomposability: correct.** The candidate's argument uses the standard direct-summand closure and classification of tilting modules; the highest-weight-4 summand has dimension at least dim Δ(4)=5. The revised proof instead supplies an elementary orbit argument: a² generates a submodule containing five independent vectors, including q, and a one-dimensional complementary module would have to equal the already-contained invariant line. This removes the closure theorem as a proof dependency.
6. **Character quotient: correct.** The identity is computed in ℤ[z,z⁻¹]; the coefficient 2 of the zero weight is a dimension, not a coefficient reduced modulo 3.
7. **Non-module obstruction: correct for all finite-dimensional rational SL₂(k)-modules.** Root operators shift exact torus weights by ±2, so both vanish on a hypothetical module with only weights ±2. Their bracket contradicts the nonzero differential of weight 2. Differential weights modulo 3 are not substituted for algebraic torus weights.
8. **Scope: important.** The quotient is nevertheless a torus character and a virtual G-character. Only an ordinary rational G-module realization is excluded. The example lies in good characteristic for type A₁ and establishes no bad-prime extension or novelty claim.

## Primary-source match

The [OWR contribution](https://ems.press/content/serial-article-files/51851), printed pp. 1275–1277, formulates Question 1 on p. 1275 and announces a geometric answer as Theorem 1 on p. 1276. It describes work in progress. The corpus adds the universal finite-dimensional-module subquestion. Replace “immediately after its question” by “later in the same contribution”; other questions intervene.

[Achar–Sobaje v1](https://arxiv.org/pdf/2606.21697v1), Theorems 1.2 (p. 2) and 7.6 (p. 41), gives

\[
t(\lambda)=\sum_{\mu\in X^+,\,i\in\mathbb Z}
\operatorname{rank}H^i(\mathcal E^{\varpi,\mathrm{sph}}_\lambda|_{\mathrm{Gr}^{\varpi}_\mu})
\sum_{\nu\in W\mu}e^\nu.
\]

The character uses unsigned stalk ranks and specialization v=1, as in Lemma 6.6(1), p. 34. The parity extension has orbit-closure support and the orbit-dimension normalization. Setup: algebraically closed k of characteristic p; connected reductive G admitting ς with all simple-coroot pairings 1 (2.1, p. 4); auxiliary algebraically closed F of characteristic ℓ>0, ℓ≠p (§4.1, p. 16). For semisimple simply connected G, ς=ρ. Main results require p good; §4.6 already requires p non-torsion for the dual. Sections 4.9–4.11 (pp. 22–24) use L⁺ₚǦ(R)=Ǧ(R[[zᵖ]]) and Grϖμ=Grμ∩Grϖ. Theorem 7.5 (p. 39) imposes Gₘ-equivariance and pς-twisted rotation on the spherical Smith side; this twist preserves the ϖ-fixed locus. The introduction explicitly rejects universal G-module realization. Remark 7.10 (p. 43) says the quotient theorem needs only the Grothendieck-group diagram. Public status checked: v1 preprint, submitted 19 June 2026.

## Dependency and acceptance boundaries

- The explicit proof is independent of Smith–Treumann localization, geometric Satake, a general tilting-character formula, and the long geometric proof.
- Its standard structural inputs are the SL₂ induced-module identification and uniqueness of an indecomposable tilting module with prescribed highest weight. Root-subgroup generation, diagonal-torus weight decomposition and differentiation of a rational action are the elementary algebraic-group background.
- [Doty–Henke, Lemma 1.1](https://arxiv.org/pdf/math/0205186v1#page=3), supplies a separate established-character cross-check: T(4) has Weyl character χ(4)+χ(0) when p=3. [Martin, §1.1](https://arxiv.org/pdf/1705.06980v3#page=2), independently pins the induced/Weyl conventions; its pp. 3–4 also use closure under direct summands and decomposition into indecomposable tiltings.
- Inspection of the geometric source verifies statement, setup, theorem references, and the target match. It is not an independent audit of its 56-page proof or all its prerequisites. No conclusion that all bad-characteristic cases are solved, false, or open follows from this audit.
- Therefore the corpus assessment that ordinary G-module realization is merely unestablished requires correction: the universal positive assertion is false. The broader geometric question must retain the exact hypotheses of the cited result.

## Reproducibility and custody

A local verification script, excluded from this public packet, checks 22 identities/conditions, including invariant forms, multiplication equivariance, invariant spaces, the five-dimensional orbit span, and a two-dimensional endomorphism algebra with a nonzero square-zero generator. It compares polynomial coefficients over F₃, rather than sampling only F₃-rational group elements. All checks passed in normal, -O and -OO modes, producing byte-identical results. Computation supplements, and does not replace, the written proof.

`SOURCE_PINS.json` records exact PDF hashes, byte counts, public URLs and inspected locations; source files themselves are excluded. Inherited source PDFs were rehashed; the source web pages were independently opened. Two additional primary papers were downloaded into this audit directory. Formula-bearing pages 2 and 41 of Achar–Sobaje and printed p. 1276 of OWR were also rendered locally and visually inspected after the arXiv web-screenshot route returned a cache-miss error.

The underlying audit performed no external publication and did not modify its frozen candidate. This packet was subsequently prepared locally for public review; packet preparation performs no publication. Third-party PDFs, extracted source text and rendered source pages are excluded from this public mathematical audit artifact.
