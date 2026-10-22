# Independent adversarial audit: 10400167

Publication copy of the complete mathematical review. Operational publication-permission notes have been removed. This is independent AI review, not human peer review. The historical wording correction below is resolved by NARROW_REVIEW.md; the original problem remains unresolved.

Date: 2026-10-03 UTC. Reviewed frozen 15-file packet with tree SHA-256 `640b3c4babf475f7af81f14d49206987e4e39b7bd4a3001463e9ac61ecb25f2e`.

## Disposition

- **PASS, mathematical partial results:** all five surviving claims are valid within their expressly stated hypotheses. No error was found in the normalization, cyclic bar calculation, square-orbit argument, or naturality argument.
- **HOLD, publication wording:** make the one source-scope repair below before treating the packet as fully reviewed. This is a qualification of the cited preprint, not a failure of the packet's lemmas.
- **HOLD, original problem:** no proof of the ordinary-TQFT-to-center converse, no counterexample, and no full solution. Keep five attempts exhausted and the original question unresolved in this investigation.

The frozen packet was not edited. This audit is verification and source-scope checking, not a sixth proof-search attempt.

## Required repair

In `TURN_5.md`, the Luo–Tian summary says that their invariants match for every framed oriented link with at most two components. Insert **“in S^3”**. Main Theorem (A) has that explicit ambient-manifold restriction. The previous paragraphs of the packet discuss links in arbitrary closed manifolds, so leaving the ambient manifold unstated risks an actual scope expansion. Equality for vacuum-colored unlinks in arbitrary ambient manifolds would already force equality of their closed-manifold partition functions.

Suggested replacement sentence:

> The primary Luo–Tian preprint, arXiv:2609.33231v1, submitted 2026-09-27, reports inequivalent Dijkgraaf–Witten centers with matching invariants of every framed oriented link in S^3 with at most two components, under one common simple-label bijection, but also a closed oriented 3-manifold partition function separating the family.

Its Theorem 7.1 concerns surgery with coefficient +p on each component of a Borromean link. Thus it expressly distinguishes the ordinary theories. The packet correctly declines to use it as a counterexample. This audit verifies the preprint's statement and scope, not its entire proof. [Primary preprint, Main Theorem and §7](https://arxiv.org/html/2609.33231v1).

## Primary target and categorical scope

The source's Problem 9.3 concerns two fusion-rule algebras with 6j-symbols giving isomorphic TQFTs and asks for their relationship; the remark refers to Sato. The definition on printed p. 493 uses closed surfaces and compact 3-cobordisms. Its framing/p1 qualification does not insert circle objects into the domain. Section 8.5 and Problem 8.17 separately discuss circle-level data. The packet's ordinary-versus-once-extended distinction is correct. The surrounding 6j discussion includes unitarity and treats positivity when relating inputs to subfactors; identifying all conceivable spherical fusion inputs with the exact historical problem would require additional care. The packet avoids such an identification by declaring its unitary scope. [Ohtsuki, pp. 493, 504, 507, 510](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf).

Sato's author-written 1998 explanation describes a finite system containing the two even bimodule systems and two cross-bimodule types, closed under relative tensor product, contragredients and decomposition. This is the appropriate Morita-type reading, not trivalent basis change. The packet accurately discloses that it used this explanation rather than inspecting the complete 1997 IMRN paper. Do not upgrade that disclosure to a claim of full inspection. [Sato, pp. 42–44](https://www.kurims.kyoto-u.ac.jp/~kyodo/kokyuroku/contents/pdf/1024-5.pdf).

Turaev–Virelizier Theorem 11.2 compares the state-sum theory with the RT theory of the center; Corollary 11.5 supplies a sufficient direction. ENO Theorem 3.1 characterizes Morita equivalence by braided equivalence of centers. Neither quoted statement reconstructs a center from a given ordinary natural isomorphism. [Turaev–Virelizier](https://arxiv.org/pdf/1006.3501), [ENO](https://arxiv.org/pdf/0809.3031).

BDSPV Theorems 1–4 classify representations of bordism **2**-categories with closed 1-manifolds, surfaces with boundary and 3-bordisms with corners; Theorem 2 is the oriented form. Forgetting this structure and then applying that classification to an ordinary isomorphism is not justified. [BDSPV, introductory definitions and theorems](https://arxiv.org/pdf/1509.06811).

## Claim-by-claim mathematical audit

### 1. Torus basis and modular data: PASS in the declared unitary scope

The ordinary product is supplied by pair-of-pants × S^1, with unit and counit supplied by the appropriately parameterized solid tori. In the simple-core basis, the multiplication is fusion and the counit selects the vacuum. Hence the primitive-idempotent formula has counit S_0j^2. Symmetry and unitarity give S(p_j)=S_0j x_j; the complex conjugate in p_j is essential and is present.

Canonical positive dimensions make S_0j positive, so the stated positive-square-root normalization fixes signs and phases. A symmetric monoidal natural isomorphism preserves this entire construction, even without additionally assuming that its component maps are unitary. The same permutation transports S, T, fusion coefficients, vacuum, duality and dimensions. This establishes necessary based data, not categorical equivalence.

The credit is properly assigned: KSW Remark 2.6(2) states primitive-idempotent uniqueness, and Lemma 2.7 supports the counit normalization. Do not present this supporting fact as new. [KSW, Definition 2.5, Remark 2.6 and Lemma 2.7](https://arxiv.org/pdf/math/0208238).

### 2. Vec_G / Rep(G): PASS as a negative gauge control

The one-simple-object Vec module category over Vec_G yields representations as its module endofunctors. Depending on module-functor conventions one can obtain an opposite tensor category; Rep(G) is symmetric, so this changes no conclusion. The S_3 character computation and ranks six versus three are correct. This obstructs input gauge equivalence and confirms Morita equivalence. It does not obstruct the relation asked for in the original remark.

### 3. Untwisted finite abelian groups: PASS

For a connected closed manifold, groupoid cardinality is |Hom(pi_1(M),G)|/|G|. Counting conjugacy classes without their automorphism weights is wrong; the packet uses the correct convention. The connected flat-coloring argument has precisely |G|^(v−1) configurations per based homomorphism and |G|^(−v) vertex normalization.

The sphere determines |A|. Prime-power lens values determine |A[p^k]|, successive base-p logarithmic differences determine numbers of cyclic factors of length at least k, and their successive differences recover every elementary divisor. The endpoint r_p(E+1)=0 is valid for E=v_p(|A|). The trivial group case is also covered. C_4 versus C_2×C_2 is a correct exact negative control. This argument needs no information about arbitrary nonabelian multiplication and does not claim to recover it.

### 4. Prime-cyclic cocycles: PASS

The carry cocycle has the correct normalized pentagon identity. In the free normalized bar resolution, f_2=sum_j[j|1] satisfies d f_2=N[1], and f_3=sum_j[1|j|1] satisfies d f_3=(g−1)f_2. Terms with a zero entry are interpreted as zero. After passing to trivial coefficients, f_3 is a cycle. The standard oriented lens skeleton of the cyclic classifying space represents the corresponding homology generator.

Under 1↦x, the carry exponents telescope to u x^2. This remains valid at x=0, without treating multiplication by zero as a permutation. Every homomorphism has automorphism group C_p, producing the factor 1/p. Reversing the common orientation conjugates every value and cannot alter the equality criterion.

The polynomial argument is exact: the difference polynomial has degree at most p−1, so vanishing at zeta_p makes it a constant multiple of Phi_p; its value at 1 then makes it zero. The distributions distinguish zero and the two nonzero square cosets for odd primes, and distinguish 0 and 1 for p=2. Pullback by a group automorphism multiplies the cohomology parameter by its square. Equality of cohomology classes after relabeling produces precisely the tensorator coboundary required for tensor equivalence. No gap was found in this restricted reconstruction theorem.

### 5. All center-colored links: PASS in the declared unitary scope

Removing framed tubular neighborhoods gives an ordinary cobordism with torus boundary. Colored core states are vectors in its ordinary state spaces; the colors need not be additional objects of the source bordism category for the argument. Monoidality gives one tensor power of the already recovered label permutation, and naturality intertwines the undecorated complement functional. Unit compatibility fixes the empty-object scalar. Thus the result covers all numbers of components and arbitrary closed oriented ambient manifolds, with orientations and framings handled consistently.

For the centers here, sqrt(Dim Z(C))=Dim C, so Z(S^3)=1/Dim C. The stated conversion to the S^3 empty-link-equals-one convention is correct. There is no claim that merely matching these invariants constructs a natural isomorphism in the converse direction.

## Why no full converse follows

The argument has not constructed coherent maps on Hom(k,i⊗j), their reassociation operators, and their braiding maps. Linear identifications of closed-surface state spaces and equality of scalar link evaluations do not by themselves supply those constructions. A full theorem could potentially extract more from the ordinary theory, but no such reconstruction is proved here. The failure to prove it is a gap in completion, not a counterexample or a proof that completion is impossible. The packet states exactly this distinction.

## Exact verification and reproducibility

The following results record the original frozen audit. The publication includes its exact recorded output in `original_audit_verification.json`. To replay the unchanged mathematical controls against the corrected packet, run `python3 audit/independent_controls.py` from the attempt directory; it uses only the Python standard library and writes `audit/independent_verification.json`. The adapter changes only packet location, expected corrected digest and output filename; all mathematical control functions are unchanged.

- All 15 frozen file bytes match the stated tree digest; all 14 manifest entries match their byte counts and SHA-256 hashes.
- The four original verifier functions were rerun without invoking the function that writes inside the frozen packet; their results exactly reproduce `verification.json`.
- Independent free-bar checks passed for cyclic orders 2 through 31: 60 comparison identities and 30 trivial-coefficient cycles.
- Independent non-real Fourier S controls for the centers of Vec_(C_3) and Vec_(C_5) passed 17,060 exact coefficient checks. These include non-self-dual labels and test the conjugation issue that real toric-code controls cannot detect.
- Independent permutation-group calculations of S_3 centralizers and conjugacy orbits verify weighted lens values for n=1 through 12. For example, L(2,1) has weighted value 2/3 despite having two conjugacy orbits.
- Arbitrary deterministic normalized 2-cochain modifications passed 2,397 exact lens-exponent checks, independently testing coboundary invariance of the cyclic evaluation.

These tests corroborate the displayed calculations. They do not certify a general reconstruction theorem.

## Release checklist after the repair

1. Preserve the unresolved/exhausted disposition and the five-turn count.
2. Apply the ambient-S^3 qualification; optionally cite Theorem 7.1 explicitly.
3. If the packet is revised, update its review status, regenerate its manifest, and produce a new receipt. Do not reuse the frozen digest for changed bytes.
4. See the later narrow review and publication note for the final disposition. A partial-results PASS is not a full solution.
