# Adversarial mathematical review — Zenodo 23414025

**Verdict: PASS within the stated hypotheses. No substantive mathematical defect or unresolved central gap was identified.**

This is an AI-assisted mathematical review, not independent human peer review, formal proof certification or novelty certification. Reviewed version 1.0.0, published 16 October 2026. The complete four-page PDF, complete current `note.tex`, full authored `source/authored/PROOF.md`, and authored finite checker were read. No sibling or historical reviewer-opinion files were consulted. The paper's general AI-audit disclosure and the authored proof's candidate-status language were encountered, but no prior verdict was used as evidence.

## Exact claim

The source and target are finite-dimensional **complex** Lie algebras of equal dimension. The source is unimodular; the target is semisimple. Two Lie homomorphisms from source to target have invertible vector-space difference. The conclusion is that the source is semisimple. The post-Lie corollary uses precisely the three displayed identities and the same complex finite-dimensional setting. Perfectness implies source unimodularity, so a perfect nonsemisimple source cannot occur with a semisimple target.

This does not assert an isomorphism of the two Lie algebras merely from a manifold identification. It does not cover a general real form, positive characteristic, infinite dimension or a merely reductive target. Zero dimension is explicitly harmless.

## Independent proof reconstruction and attacks

1. **Integration and global action.** Simply connected complex integrations exist, and both homomorphisms integrate uniquely. Their left-right formula satisfies the action law because the inverse of the second homomorphism reverses order exactly as needed. The action is globally defined from the outset. It requires neither closed images nor injectivity of either map, and it is not a locally defined action whose completeness is being assumed.

2. **Infinitesimal signs.** Left trivialization gives `B_p = Ad(p⁻¹) j₁ − j₂`. The proof's covariance is `B_(A_h p) = Ad(J₂(h)) B_p Ad(h⁻¹)`. Directly substituting `q⁻¹ = J₂(h)p⁻¹J₁(h)⁻¹` and intertwining each homomorphism verifies both terms. The second adjoint factor involves J₂, not J₁. This sign/factor is tested independently below.

3. **Determinant and transitivity.** The determinant is a single globally holomorphic function after fixing bases; there is no patching or volume-form ambiguity. Its value at the identity is nonzero. Connectedness turns zero differential of the determinant character into the constant character 1; this applies to the unimodular source and to the perfect semisimple target. Covariance therefore makes the determinant constant on the identity orbit. The inverse function theorem supplies an open neighborhood in that orbit, so the holomorphic identity theorem forces the same nonzero constant on the entire connected target. Each orbit is then open, and connectedness leaves exactly one orbit. This establishes transitivity rather than assuming it from initial transversality.

4. **Stabilizer and covering.** The stabilizer is an actual closed subgroup, being the inverse image of the identity under the orbit map. Its Lie algebra is the kernel of the invertible difference, hence zero. The resulting discrete closed subgroup yields a covering of the homogeneous-space quotient. The source is connected and the target simply connected, so the cover has one sheet. The proof does not rely on the false general statement that every surjective local diffeomorphism is a covering. The resulting map is a manifold diffeomorphism; it need not be a homomorphism.

5. **Levi splitting and contractibility.** A Levi semidirect decomposition can be integrated using simply connected factors and uniqueness, giving the source manifold as `R × S`. This avoids assuming that a previously selected immersed Levi subgroup has closed image. The solvable induction uses a codimension-one ideal and a one-dimensional complementary subalgebra; the corresponding automorphism action integrates on the simply connected smaller group. Thus its manifold is a product with C at each step. No bijective exponential map is asserted for an arbitrary solvable group.

6. **Homological obstruction.** The compact real form of a complex semisimple group has real dimension equal to the group's complex dimension, not twice it. Polar decomposition and the covering discussion apply to the simply connected integrations used here. A compact connected Lie group is orientable by a left-invariant frame and has nonzero top integral homology. Contractibility of the source radical reduces its homology to the compact real form of the Levi factor. If the radical were nonzero, this compact manifold would have strictly smaller dimension; its homology in the target compact form's top degree would vanish. This contradicts the diffeomorphism. Ordinary singular homology is sufficient; compact-support homology of the noncompact groups is not being confused with it.

7. **Post-Lie reduction.** The third identity makes left multiplication a target derivation, and the second makes it a representation of the source. The target has zero center and nondegenerate Killing form. The displayed trace identity proves derivation innerness with the correct sign: cyclicity turns the derivation commutator into `tr(D[ad u,ad v])`, and Killing invariance identifies it with an inner derivation. Hence R is linear and uniquely defined. The second post-Lie identity gives the homomorphism property of R; the first gives `[x,y] = {Rx,y}+{x,Ry}+{x,y}`. Expansion proves that R+I is also a homomorphism, with difference I. Finally the adjoint-trace functional vanishes on source brackets and therefore on a perfect source.

No central statement was reduced to an unsupported equivalent conjecture. The primary classical imports match their required complex/global/topological hypotheses; exact locations and receipts are in `primary-sources/FINDINGS.md`.

## Fresh exact controls

`fresh_controls.py` imports no supplied implementation. It uses rational matrices and a nine-dimensional three-factor chain, rather than relying on the package's six-dimensional example. With source and target `sl₂³`, take J₁ as identity and J₂ as the shifted homomorphism `(h₁,h₂,h₃) ↦ (1,h₁,h₂)`. Its differential difference is invertible and yields a nontrivial nilpotent R of length three after transporting the source bracket.

The fresh controls verify 324 pair identities, 2,187 triple identities, 60 full group covariance/determinant instances, and 81 inner-derivation equations. Exact rank calculations find the entire three-dimensional derivation space of sl₂ equal to the inner span. A deliberately wrong covariance factor fails in all 60 trials.

Excluded-hypothesis checks are substantive controls:

- The non-unimodular affine-plus-central source has two homomorphisms with invertible difference but determinant zeros away from the identity. Its 18 pair checks pass, while its nonzero adjoint trace and failure of global transversality show why unimodularity is indispensable.
- A perfect unimodular source with a two-dimensional abelian radical admits a post-Lie structure with the merely reductive target `sl₂ ⊕ C²`. The 250 checked identities and derived-rank calculation confirm that this lies outside the theorem rather than contradicting it.
- Zero homomorphisms from an abelian source show that the invertible-difference condition cannot be discarded.

All fresh controls pass. They do not test or certify universal integration, holomorphic continuation, covering theory or homology; those steps were reviewed in the proof and original references.

## Published replay and source binding

The authored checker reports 2,896 exact finite conditions and passes in both normal and `-O` modes. These are repeated runs of the same finite cases. The complete portable replay also passes: 242 archive members authenticated, original root execution retained, two positive runs, two semantic invalid-product rejections, two explicit failure rejections and two corrupt-preexecution rejections. Source and archive bytes remain unchanged. The mathematical PDF and ZIP SHA-256 values are bound in `verdict.json`; every extracted member matches the archive.

The portable harness authenticates/replays archival computations; its archived verdict language is not mathematical evidence. No source-to-PDF rebuild, full novelty audit or check of the inaccessible Onishchik body was undertaken. The affine predecessor and other historical credit are not used as substitutes for the paper's global proof. No website, Git, spreadsheet, Zenodo, deployment or outreach action was performed.
