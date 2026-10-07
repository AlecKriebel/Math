# Independent audit of unitary period multiplicities

Problem 30001738 / OWR-4804-006. Audit date: 2026-10-07 UTC.

## Verdict and disposition

**Accept the frozen author packet within its expressly stated scope. No mathematical correction patch is required.** The p-adic, smooth complex, irreducible-induction target with individually Galois-invariant essentially square-integrable factors follows from the credited Beuzart-Plessis theorem. The weaker catalogue assertion is false, including within the irreducible generic p-adic category.

Recommended disposition: **Prior-literature resolution of the precise p-adic irreducible source target; catalogue formulation corrected by a counterexample.** Do not shorten this to a claim that all literal local-field or reducible-induction interpretations have been proved. Credit the multiplicity theorem to Raphaël Beuzart-Plessis, extending Feigon–Lapid–Offen. No new theorem or novelty is claimed.

This is an independent AI-authored source, hypothesis, mathematical-reduction and packet-integrity audit. It is not human peer review or a formal proof-assistant certificate. The analytic theorem and the representation classification remain credited external dependencies.

## Frozen object

The full REPORT.md and every public companion were read. The original directory and archive were preserved.

- Author manifest SHA-256: 56c934a8949d90e0558849578e1421826b9e66520c0a9899a8745eebe7223ef2
- Author verifier SHA-256: ac53854fdf7f99f902da3461929d03dec1c31c2891afa9df96bfc56efe9153fb
- Author ZIP SHA-256: 02a24cc8994a462d65de1471ba73a7d2cca63b51e3f562278db9866d9012ee58
- ZIP size: 15,176 bytes; flat packet inventory: nine files
- REPORT.md SHA-256: 9e821d62ef0cace0bc3a09e33230c8aa267e36d2aee4ea27696e456926e5b51a

The ZIP inventory, CRCs and every uncompressed member agree with the public directory. Both public corpora were independently rehashed and counted. There is one exact target problem record and no target research entry, by either problem identifier or problem-number key. Dataset contents are excluded here.

## Primary source and scope audit

Fresh downloads of all three primary PDFs match the author's byte counts and SHA-256 fingerprints. The source checks record the URLs and inspection locations. The decisive formulas were also checked visually against the PDF pages.

The [workshop contribution](https://doi.org/10.4171/owr/2011/14), pp.727–736, was inspected in full. Its Conjecture 3 attaches Galois invariance to the individual factors. The abbreviated conjecture sentence does not by itself justify every hypothesis in the precise affirmative target. This distinction is correctly disclosed by the author.

The detailed [Feigon–Lapid–Offen paper](https://www.numdam.org/item/PMIHES_2012__115__185_0/) supplies the substantive reconciliation: Theorem 0.2 specifies irreducibility and p-adic fields; §13 has the same field restriction; §13.6 explicitly formulates the irreducible-induced problem. Its conventions distinguish the full dual from the smooth contragredient and use normalized induction. Thus the repaired scope is grounded in the original collaborators' detailed treatment. It is not evidence for all broader readings of the workshop sentence.

In [Beuzart-Plessis, arXiv version 2](https://arxiv.org/abs/2008.05036v2), the category conventions, symmetric-space definition and complete Chapter 5 were inspected, including the proof through §5.5. Equation (5.2.1) uses fixed indices, with repetitions; Theorem 5.2.2 applies to every irreducible generic representation in its stated p-adic category. It imposes no distinctness requirement. Its degree is a scheme-fiber length. Section 5.1 explicitly supplies the genericity and parabolic-permutation facts used in the reduction. No restriction to unramified extensions or odd residue characteristic enters the cited multiplicity theorem. The proof chain was checked for applicability, not independently rebuilt from its analytic prerequisites.

The [publisher record](https://www.sciencedirect.com/science/article/pii/S0022314X21001815) independently confirms Journal of Number Theory 230 (January 2022), pp.5–63, DOI 10.1016/j.jnt.2021.06.001. The publisher's search result was accessible; a direct page open returned an error. The full theorem inspection used the independently retrieved, version-pinned arXiv PDF.

## Mathematical reduction audit

### Action and dual conventions

For the right action x·g = τ(g)^t xg, the equality x·g = x·g′ implies g′ = hg with h in the stabilizer H_x. Consequently ℓ_x ◦ π(g) is independent of the representative g exactly when ℓ_x is H_x-invariant. This checks the order of multiplication in the author's inverse construction; no inverse or contragredient has been inadvertently inserted.

The correspondence T(v)(y) = α_y(v) then satisfies T(π(g)v)(y) = T(v)(y·g). A compact open subgroup fixing v makes T(v) invariant under that subgroup. Its orbits on each homogeneous component are open, so T(v) is locally constant. The two Hermitian-form orbits are open; equivalently their discriminants lie in the two open norm classes. Thus the full-dual equivariant-map space agrees with Hom_G(π,C^∞(X)) and with the sum of the two period spaces. No continuity restriction on an algebraic linear functional is silently imposed in the p-adic setting.

The two objects being counted are form orbits, not isomorphism classes of abstract stabilizer groups. In odd dimension the two stabilizers can both be quasi-split. The author's accounting handles this correctly.

### Induction and factor counting

Galois pullback preserves the standard parabolic and its modulus. Inducing the individual intertwining maps therefore gives π^τ ≅ π. Essentially square-integrable general-linear-group representations are generic; irreducibility of their normalized induction puts π in the generic irreducible category. The generic parabolic-permutation property identifies the given multiset with the Langlands inducing multiset. Reordering cannot change its number of occurrences.

All k occurrences are fixed, so d(π)=2^k and the total multiplicity is 2^k. Each form contributes 2^(k−1). Since k≥1, the ceiling and floor agree here. No step replaces k by the number of distinct isomorphism classes. These are valid corollary deductions relative to the cited theorem and classification facts.

### Singular fiber example

Eliminating p from s²−2p=2 and p²=1 gives s⁴−4s²=0. Conversely p=(s²−2)/2 satisfies both equations in that quotient, and p is invertible because p²=1. These two constructions give inverse algebra maps, so no extraneous component is introduced.

The quotient by the monic quartic has complex dimension four. Its pairwise coprime factors s+2, s² and s−2 give local lengths 1, 2 and 1, at three geometric points. This proves the claimed discrepancy between fiber length and point count without numerical approximation. For an unramified quadratic extension, the norm sends a common uniformizer to its square; the displayed squaring map is therefore the correct parameter model.

The normalized principal series 1×1 is irreducible: its character ratio is 1, not either reducibility character |·|_E or |·|_E^(−1). Thus it genuinely lies in the claimed generic category and realizes the repeated-factor case. No theorem about a nongeneric quotient is substituted.

### Paired character counterexample

Over F_3, the polynomial t²+1 has no root. Hence the residue algebra is F_9, and u=1+i has order eight because u⁴=−1 and u⁸=1. Reduction of units and the decomposition E×=3^Z O_E× define the stated finite-order character unambiguously.

The Galois automorphism fixes 3 and acts by the third power on the residue field. Its pullback therefore sends χ to χ³. The two characters are distinct; their ratio χ^(−2) is nontrivial on units. It is consequently neither an absolute-value reducibility character nor any integral absolute-value twist. The cited disjoint-induction criterion makes χ×χ^τ irreducible, and genericity follows. Permutation interchanges the two factors, proving invariance of their product.

There are zero fixed factor occurrences. The theorem gives total multiplicity one, divided as one on the quasi-split form and zero on the other. The catalogue prediction is four. This is a valid counterexample to the catalogue's weaker hypothesis and fails exactly the individual-invariance condition in the repaired source target.

The exponents 3, 7 and 5 distinguish arithmetic pullback, coefficient conjugation and conjugate-duality. The character example does not confuse these operations.

## Independent replay and corruption testing

The independent replay script first checks the external manifest, verifier and archive pins before execution. It then checks the closed inventory and archive equality. A separately captured, pinned verifier is run against the original directory, with optimization enabled, and against a relocated copy. All three runs reproduce the author's 3,044 checks and 494 synthetic multisets.

Eleven integrity mutations are rejected in both normal and optimized modes: changed payload, hidden extra file, missing file, extra directory, payload symlink, manifest symlink, wrong pin, modified manifest bytes, a false receipt with updated test hashes, duplicated inventory path, and traversal path. Eight semantic mutations are likewise rejected in both modes: counting distinct fixed factors, counting every factor, removing the stability test, swapping orbit multiplicities, replacing the residue-field relation, reversing the fiber-quartic sign, using coefficient conjugation for the arithmetic twist, and removing the scope guard. Total deliberate rejections: 38.

Rehashed test fixtures are deliberate checks of the verifier's internal behavior; they are not approved replacements for the frozen packet. No output was accepted merely because a program exited successfully. The original packet was rechecked for byte-for-byte preservation afterward.

The tests support reproducibility, finite arithmetic and the declared scope controls. They do not evaluate infinite-dimensional Hom spaces or establish the analytic theorem. The verifier is correctly described as an integrity checker under a trusted Python interpreter and operating system, not a hostile-code sandbox. Filesystem race resistance is outside that stated trust model.

## Limits and final acceptance

No affirmative statement for arbitrary reducible full inductions, their nongeneric quotients, Archimedean local fields, positive-characteristic fields or modular coefficients is accepted. No extension to a split quadratic algebra is inferred. These exclusions do not weaken the explicit counterexample to the literal catalogue question.

The 0/5 research-turn label is consistent with a prior-literature resolution found before new source-problem proof attempts. Elementary illustrations and the subsequent audit are not new attempts at the unresolved analytic theorem. The packet's chronological timestamps are author provenance; this audit does not independently reconstruct every earlier activity.

No substantive error requiring a correction patch was found. Acceptance is conditional only on the clearly disclosed external mathematical dependencies, not on an unresolved step in the authored corollary. The original source-free author packet may be retained unchanged, accompanied by this audit and its independently pinned test results.
