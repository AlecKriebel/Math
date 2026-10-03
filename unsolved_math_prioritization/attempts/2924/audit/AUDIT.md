# Independent audit: KP-4.48 / 2924

Date: 3 October 2026, UTC.

## Verdict

**Pass as an explicitly unresolved research report.** Five substantive approaches are present. No general proof or counterexample is established, and no such result is claimed. The first untreated homotopy group is already π₁ of the boundary-pointwise homeomorphism group. There are no blocking mathematical findings. Two minor precision advisories appear below.

This is an audit of the particular frozen packet, not a certification that the open problem has been solved, a formal verification of the cited theorems, or an exhaustive literature review.

The reviewed `SHA256SUMS` has SHA-256:

`b17e146dff9c3f63a2e3445d5fe1bac763ac3216029fca7dfbc23801e74c6e05`

The packet contains nine authored files, including that manifest. All eight manifest entries matched before and after this audit. The seven source PDFs also match every byte count and SHA-256 recorded in `SOURCE_HASHES.json`. The reviewed files were not changed. In particular, their historical `independent_review: pending` field was not rewritten; this separate report supplies the review result.

## 1. Exact target and source scope

The text and page images of K3, printed pp. 228–229, identify the target as contractibility of the compact-open group of homeomorphisms of a compact contractible topological 4-manifold that fix its boundary pointwise. The report does not substitute diffeomorphisms, boundary-setwise homeomorphisms, or dimension 5. The disk case and the recorded connectedness statement agree with the book. The actual problem book is correctly distinguished from the short workshop report. [K3 source](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf).

The following primary-source distinctions survive independent inspection:

- GRW's Theorem A concludes weak contractibility for dimensions at least 6. Its abstract uses shorter contractibility language. Theorem C's embedding-calculus proof separates the tower calculation from convergence. The former uses acyclicity; the latter uses a relative handle-dimension bound. Remark 1.2 already points to the dimension-5 extension. The smooth dimension-4 failures mentioned there do not disprove the topological target. The audit inspected Theorems A–C, §1.3 and the first proof in §2. [Accepted manuscript](https://api.repository.cam.ac.uk/server/api/core/bitstreams/f3e65116-e119-4947-b4fe-ae433c519841/content).
- KK's Theorem 6.18 extends those results to dimension 5. Theorems 6.1 and 6.3, the handle-trading inequality in Lemma 6.10, and the smoothing-comparison exclusion of dimension 4 were checked in the final institutional PDF. The complete relevant convergence proofs and the proof of Theorem 6.18 were inspected. Nothing in the cited extension supplies dimension-4 convergence. Formal smoothability alone does not remove that restriction. [Institutional publication record](https://publikationen.bibliothek.kit.edu/1000192734).
- Orson–Powell uses the compact-open, pointwise-relative homeomorphism group. Theorem A is a component classification. Its use of the pseudo-isotopy classification, Theorem 3.1, and the obstruction identification in Proposition 6.2 was checked, including §3.3 and §6.2. The topological proof uses a 6-dimensional surgery/h-cobordism argument; it does not establish a continuously chosen family of isotopies. [Author preprint v3](https://arxiv.org/pdf/2207.05986v3).
- GGHKP's 2026 Theorem 1.5 applies to compact simply connected topological 4-manifolds, including boundary. Its conclusion concerns isotoping an individual pseudo-isotopy relative to the bottom and side. Section 5 extends the boundary scope beyond Perron's original no-1-handles case; §6 bypasses Quinn's problematic replacement criterion through factorization and controlled cancellation. The report correctly uses this repaired theorem for connectedness without promoting it to an arbitrary-parameter straightening theorem. [Published article](https://www.cambridge.org/core/journals/forum-of-mathematics-pi/article/pseudoisotopies-of-simply-connected-4manifolds/76BC09B6D1CF91456A4189800D2B0494).
- The Alexander formula agrees with FNOP Lemma 4.4. Edwards–Kirby's Corollaries 1.2–1.4, the ambient-extension proof and its boundary-relative refinement, and §7 were inspected for the relative extension input. KK §5.4.2 explicitly identifies that input for codimension-zero topological embeddings. Neither an individual extension theorem in an arbitrary embedding space nor an unsupported global section is being used. [FNOP](https://nyjm.albany.edu/m/2025/6p.pdf), [Edwards–Kirby](https://doi.org/10.2307/1970753).

The repository-history statements were checked against the retained records, without making new remote repository requests. Their stated scope is appropriately bounded: a failed recursive tree request is disclosed, and the report does not turn successful directory/search checks into a proof that no differently labeled or unpublished attempt exists.

## 2. Mathematical checks

### Preliminary topology and the component calculation

Poincaré–Lefschetz duality gives the relative integral homology asserted in §1. The long exact sequence gives a connected integral homology 3-sphere boundary. Naturality of the boundary map from the relative orientation class shows that every boundary-pointwise homeomorphism preserves orientation. Contractibility annihilates the second Stiefel–Whitney class and the required homology/cohomology groups. Both the variation factor and the relative spin-difference factor of the Orson–Powell classification are therefore trivial. With the corrected pseudo-isotopy theorem, π₀G is indeed trivial. This does not calculate any positive homotopy group.

### Alexander contraction and factorization criterion

For positive time, the two radial formulas agree on their common sphere and are inverse to the corresponding construction applied to the inverse homeomorphism. At time zero the bound 2t is uniform in the homeomorphism. Consequently this is jointly continuous in the compact-open topology, not merely a separately specified collection of isotopies. Reversing time gives a strong contraction. Extension by the identity in one fixed embedded disk is continuous.

The finite-product sufficient condition is valid: multiply the continuously contracted factors, then normalize by the value at the chosen basepoint if necessary. The missing global continuous factorization of arbitrary spherical families is explicitly retained. The cone argument correctly rules out the proposed radial-coordinate shortcut when the boundary fundamental group is nontrivial; it does not provide a counterexample to contractibility of G.

### Relative mapping space

The collar makes the boundary inclusion a cofibration. Its mapping-space restriction has the homotopy-lifting property in the standard compactly generated/compact-open setting used here. Postcomposition with a fixed contraction contracts both the total and base mapping spaces. The homotopy fiber is therefore weakly contractible. Every absolute self-map of a contractible space is a homotopy equivalence, but neither observation forces injectivity. The report does not confuse extension through continuous maps with extension through homeomorphisms.

### Punctured manifold and the embedding restriction

Van Kampen and Mayer–Vietoris give π₁C = 0 and the homology equivalence from the inner S³ boundary. The homology Whitehead argument is applicable because these manifolds have CW homotopy type. Thus C is the stated one-sided h-cobordism.

For the fibration reduction, the relevant embedding space has the compact-open relative codimension-zero convention, with the outer boundary mapped to the outer boundary and the inner boundary in the interior. Restrict to the ambient-isotopy component of the inclusion. Relative parametrized isotopy extension gives the standard Serre/homotopy fibration there, which is sufficient for the asserted long exact sequence. Its fiber over the inclusion consists exactly of homeomorphisms supported in the missing disk, fixing the disk boundary pointwise. It is homeomorphic to the disk group by restriction and extension. Its contraction gives the claimed homotopy-group comparison.

The report does not need surjectivity onto an unrestricted embedding space, a continuous global choice of extension, or a statement about wild/nonproper embedding families. Its component restriction is important. The handle obstruction is also correct: adding only relative 0- and 1-handles cannot impose relations in the original boundary group. A nontrivial π₁Σ cannot thereby become the trivial π₁C. The dimension-4 relative bound d − 3 = 1 therefore cannot be supplied in that way. The newer KK argument still has the stated independent dimensional exclusions.

### Pseudo-isotopy evaluation

The group P fixes the bottom and side faces pointwise. The top face is preserved because it is the closure of the remaining boundary stratum; the restriction map is well-defined. Its identity fiber fixes the entire boundary of Δ × I.

The lifting formula in equation (9) has the correct order of composition. At the top face it gives

δ(z,s)h(z,0) = h(z,s).

At the bottom, δ(z,0) is the identity; on the side every δ fixes Σ. At s = 0 the lift is the supplied F. The displayed inverse is correct. Evaluation, inversion, composition and the compact-open exponential law justify continuity for arbitrary homotopy parameters. Thus the explicit lifting claim is sound. Connectedness of G supplies surjectivity.

Δ × I is a compact contractible topological 5-manifold after interpreting its corners topologically. The dimension-5 theorem supplies a weakly contractible identity fiber. The resulting weak equivalence P → G is a reduction, not a contraction of either space. The level-preserving subspace is the path space starting at the identity, which contracts by rescaling time. Passing from arbitrary pseudo-isotopies to that subspace in all parameter dimensions is exactly the missing assertion. An arbitrary deformation in the full product homeomorphism group need not preserve levels, and f × id generally moves boundary caps.

### Boundary restriction and clutching

The collar lift in §6 is continuous and invertible, agrees with the initial lift at time zero, and is the identity before reaching the inner collar seam. Its boundary value is the prescribed homotopy. The long exact sequence is correctly displayed for the inverse image of the boundary identity component.

The relative clutching criterion is valid over the two hemispheres: a nullhomotopy supplies compatible trivializations, while a relative trivialization supplies two disk-defined maps into G whose equatorial quotient is the clutching map. Basepoint normalization removes the difference between free and based nullhomotopy here. Boundary cork maps are not elements of G, and smooth nontriviality does not survive automatically in the topological group. No nontrivial higher clutching class has been produced.

## 3. Boundary and homotopy-type safeguards

The target uses identity on the boundary, not identity on a fixed collar. The explicit Alexander, pseudo-isotopy and boundary-extension constructions all respect that convention. The cited Orson–Powell definition matches it. The report does not replace G by a collar-fixing subgroup without a comparison theorem.

The compact-open topology is uniform convergence on the compact domain, and inversion is continuous within the homeomorphism group. The mapping spaces and compact parameter families used above admit the standard exponential-law arguments. For the embedding reduction, the ordinary Serre-fibration interpretation suffices; no stronger universal lifting statement is needed there.

No ANR or CW-type property of G is invoked. The report's refusal to silently deduce actual contractibility from the vanishing of homotopy groups is mathematically appropriate. This does not assert that such an upgrade is impossible or itself an open theorem; it only marks an extra justification that this packet has not supplied. In fact, the packet does not reach weak contractibility for arbitrary Δ in the first place.

## 4. Reproducibility and negative controls

Running the frozen verifier with ordinary Python reproduced `verification.json` byte-for-byte, including all **104,647 assertions**. The count equals the sum of the named counts.

The independent audit verifier uses a separate closed displacement formula, new rational grid values, three different shear parameters and different times. It checks inverses, cube preservation, support, special and general displacement bounds, agreement with dilation, and the two-time semigroup identity. It performs **82,017 additional exact checks**. Its negative controls reject a wrong inverse sign, missing scale amplitude, the incorrect time-zero endpoint, a product map falsely claimed to fix a boundary cap, and the dimension-4 strict inequality. Dimension 5 passes the same inequality.

These calculations concern explicit finite rational models. They do not test all compact contractible 4-manifolds, compute π₁G, prove embedding-calculus convergence, verify a surgery argument, or certify contractibility.

To replay from this audit directory with a sibling directory named `public`:

```sh
python3 audit_verify.py ../public > /tmp/kp448-audit.json
cmp audit_verification.json /tmp/kp448-audit.json
sha256sum -c SHA256SUMS
```

The audit script raises explicit exceptions for its own checks rather than relying on Python's optional assert statements. The frozen verifier is invoked under the ordinary interpreter, without optimization flags.

## 5. Nonblocking advisories

1. **Embedding-space precision, §4.** A future revision could spell out e⁻¹(Σ) = Σ, the compact-open topology and the Serre-fibration meaning directly beside equation (8), and define the base as the ambient-isotopy orbit of the inclusion. The existing relative-convention language and component restriction are adequate for the reduction, but those additions would make its scope harder to misread. They should not be replaced by an assertion that arbitrary pointwise locally flat families automatically have every required parametrized extension property.
2. **Cone-chart wording, §2.3.** The phrase “a punctured 4-ball V” should be “a chart 4-ball V containing v,” followed by taking V minus v. The surrounding inclusions and the displayed puncturing already make the intended argument clear. This is a local wording error, not a failure of the fundamental-group argument.

Neither advisory changes the unresolved conclusion or any numerical result. The frozen packet has been preserved, so these are recommendations rather than silently applied edits.

## 6. Publication scope

The authored packet and this audit contain explanations, source links and hashes, and small verification programs/results. The audit redistributes no source paper, scan, page image, extracted full text or catalogue dataset. No private absolute workspace paths, credentials, personal material or internal coordination records are included in these audit deliverables. No remote repository mutation was performed as part of this audit.

**Final disposition:** retain the outcome `unsolved`, the five-attempt count and the explicit higher-parametric gap. The review supports publication as a checked unsuccessful investigation, not as a solution.
