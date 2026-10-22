# Independent audit: KOU-21.100 / catalogue 2609 / queue rank 469

Audit date: 3 October 2026 UTC.

## Verdict

**PASS for the exact original universal counting assertion.** The frozen packet gives a valid, credited reconstruction of an existing counterexample of Eric Hou. Its hand proof establishes strict failure without relying on the supplemental exact count. An independent direct enumeration also reproduces the exact number 1728. No mathematical repair to the frozen packet is required.

Recommended mathematical disposition: `already_solved`, meaning that this audit verifies an existing attributed negative answer. This is **not** a claim of journal publication, peer review, acceptance by the Kourovka editors, formal proof-assistant verification, first priority, or discovery by the packet author or auditor. The remote/publication gate remains a separate decision; this audit performed no remote writes.

The original substantive proof-attempt count stays 0/5: this work verifies and audits a source result and does not claim an original proof attempt.

## 1. Frozen input and reproducibility

The frozen author input comprised twelve files including its manifest. `AUTHOR_MANIFEST.json` records the original file identities; `PUBLICATION_PROJECTION.json` identifies the presentation-only changes in this public copy.

- Manifest SHA-256 independently checked: `f5f61a011e63525e9fd76ad5e18657c1e43c0d644d9753adcfbe0fa7d1d0c2d8`.
- All eleven manifest-listed file sizes and SHA-256 hashes pass.
- The actual file set matches the manifest plus `MANIFEST.json`.
- `python3 verify_packet.py --replay` passes and reproduces both stored JSON results byte for byte.
- The author C++ checker additionally passes an undefined-behavior-sanitized compilation and execution (`-fsanitize=undefined -fno-sanitize-recover=all`), with output matching the stored result.
- All three source PDF hashes match the separate frozen source record. No author file was modified.

Source PDF SHA-256 values:

- Kourovka October revision: `31baec1b36ec3a956e787355eccfffa2e89df5b1fe31b22a3123377d8103baab`.
- Hou v1: `6387024113f7e69aee2b292efd8b23dcf669b475316fdbbe391bcf0d393563f8`.
- Navarro 2023: `1a8dead112bdd91d8f70c0af96e9de18e265e40e02beffe77160f28cd033aabc`.

## 2. Exact target, source identity, and status

The October Kourovka PDF, printed page 192, asks whether the number of A-invariant irreducible complex characters of G that are nonzero at every element of C_G(A) equals the order of the abelianization of C_G(A), for every coprime finite action. The next sentence offers the stronger proposed characterization through linearity of the Glauberman–Isaacs correspondent. The packet correctly distinguishes these two statements. It disproves the counting assertion itself.

The source statement and attribution to G. Navarro were checked against the local PDF and its text, and the page was independently rendered during this audit. Navarro's *Problems on characters: solvable groups*, Publ. Mat. 67 (2023), 173–198, DOI 10.5565/PUBLMAT6712304, printed page 189, Problem 6.3, is indeed the earlier stronger correspondent question. Page 190 states the known implication when A is a p-group. An operator group of order 21 does not refute that restricted implication.

Hou's [versioned arXiv record](https://arxiv.org/abs/2609.16227v1), [current record](https://arxiv.org/abs/2609.16227), and [primary HTML](https://arxiv.org/html/2609.16227v1) were freshly opened. The local PDF agrees on author, title, construction, and theorem statements. Section 2 supplies the character-theoretic dependencies; Section 4, Theorem 4.1, supplies the short strict inequality; Sections 5–7 supply the stronger exact count. Printed page 12 was independently rendered and reviewed.

Important provenance detail: both arXiv records and the PDF display **30 July 2026**, despite the `2609` identifier prefix. Preserve the literal identifier and displayed date; do not replace the displayed date with an inferred September date. The packet already does this correctly. Only v1 and no journal reference were visible in the inspected records. This is a preprint-status observation, not proof that no acceptance exists elsewhere.

The [October update notice](https://kourovkanotebookorg.wordpress.com/2026/09/30/october-2026-update-for-the-21st-edition/) and the [editors' repository](https://kourovkanotebookorg.wordpress.com/repository/) were also freshly opened. The frozen October PDF has no solution marker at 21.100, and the repository search returned no 21.100 entry. These facts must remain separate from the mathematical audit. The catalogue's supplied local record matches the primary problem, but its current public-page status is not independently established by this audit.

## 3. Group and automorphism: PASS

Let V = F4² ⊕ F8, and let T multiply the two F4 coordinates by r and the F8 coordinate by s. The polynomials r²+r+1 and s³+s+1 are irreducible over F2. Their residue classes are neither zero nor one, and their multiplicative orders are respectively 3 and 7 because the corresponding nonzero groups have prime orders. Thus T has order 21, is F2-linear, and has fixed space zero.

B is the additive group of all functions V → F2. Translations are linear automorphisms of B and satisfy τ_t τ_u = τ_(t+u). Consequently the displayed multiplication defines the semidirect product B ⋊ V, with identity (0,0), inverses supplied by the semidirect-product formula, and order 2^(128+7) = 2^135.

The action (f,t) ↦ (f composed with T inverse, Tt) is multiplicative because it intertwines τ_t with τ_(Tt). It has order 21, and is faithful already on the quotient G/B = V. Since G is a 2-group, its order is coprime to 21. No illicit infinite group, nonautomorphic map, or failure of coprimality is present.

One terminology caution applies to descriptions outside the packet: V^A = 0 means no vector is fixed by every operator. It does not mean every nonidentity element of A acts without nonzero fixed vectors. In fact the size-3 and size-7 orbits exhibit such stabilizers. The certificate uses the needed common-fixed-space condition correctly.

## 4. Fixed subgroup: PASS

If (f,t) is fixed by A then t is fixed by T, so t = 0. Conversely, (f,0) is fixed exactly when f is constant on every A-orbit. Thus C_G(A) = B^A, with its inherited elementary abelian group law; no translation component survives.

There are five F4-lines in F4². Their nonzero parts each have three points and partition its fifteen nonzero vectors. The twelve A-orbits on V have sizes

1, 3, 3, 3, 3, 3, 7, 21, 21, 21, 21, 21.

For a mixed orbit, the order-3 and order-7 scalar exponents vary independently by the Chinese remainder theorem. These sizes sum to 128. Therefore C is elementary abelian of rank 12, C' is trivial, and |C/C'| = 4096.

## 5. Explicit invariant irreducible character and zero: PASS

For λ(f) = (-1)^(f(0)), the 128 translation conjugates are the 128 evaluation characters. They are distinct because a function supported at one point separates any two evaluations. Therefore the inertia group of λ in G is exactly B. Mackey's formula gives inner product 1 for Ind_B^G λ, hence an irreducible character χ of degree 128. This is a character-theoretic proof, not an inference from numerical traces alone.

T fixes the zero vector, so it fixes λ and therefore fixes χ. On B the induced character is the sum of its evaluation weights:

χ(c) = sum over t in V of (-1)^(c(t)) = 128 - 2 times the support size of c.

Take c to indicate the union of the zero orbit and any three mixed size-21 orbits. This union is A-stable and has size 64. Thus c belongs to C, and χ(c) = 0. All hypotheses on the character and its zero are independently established.

An alternative irreducibility perspective confirms the same point: the B-action has 128 distinct one-dimensional weight spaces in the induced representation, and V acts transitively on them. Any nonzero G-invariant subspace, after decomposing into B-weight spaces, must contain all of them.

## 6. Exhaustive character parametrization and invariant count: PASS

For u in B, the perfect F2 pairing with B defines λ_u. Its inertia group is I_u = B ⋊ V_u, where V_u is the translation stabilizer of u. I_u is normal because it is the inverse image of a subgroup of the abelian quotient V. The formula θ_(u,μ)(f,t) = λ_u(f) μ(t) is a genuine linear character: translation invariance of u is exactly the condition needed for multiplicativity.

For each translation orbit of u and each linear character μ of V_u, induction produces an irreducible character. In Mackey's formula every coset outside I_u changes the restriction to B and contributes zero; the identity coset gives the Kronecker delta for μ. Distinct translation orbits have disjoint B-weight sets. Completeness follows because the sum of squared degrees is

sum over translation orbits O of |V_u| [V:V_u]² = sum over O of |V| |O| = |V| |B| = |G|.

The invariant-parameter step has no missing cohomology or uniqueness assumption. For an A-stable translation orbit, V_u is A-stable and the translation offsets form a 1-cocycle in V/V_u. Summing that cocycle over the odd-order group A makes it a coboundary, producing an A-fixed representative. Maschke's theorem gives an A-stable complement to V_u; since V^A = 0, the quotient has no fixed vectors. Hence the representative is unique.

For this fixed u, the extension with μ = 1 is A-invariant. The full parametrization is equivariant, so its induced character is invariant exactly when μ is invariant. Semisimplicity and V_u^A = 0 show that V_u has no trivial quotient, equivalently that its dual has no nonzero invariant functional. Thus μ = 1 is the only possibility. Therefore B^A parametrizes all and only the invariant irreducibles, and there are exactly 4096.

The separate appeal to Glauberman is also legitimate: A is solvable and acts coprimely, so the classical correspondence gives a bijection to Irr(C), which has 4096 elements. No identification of the particular correspondent of χ, or unproved assertion about its zeros, is needed. The elementary argument removes reliance on this theorem for the count.

Combining the exhaustive total 4096 with the explicit vanishing character gives at most 4095 nowhere-zero invariant characters. Because C is abelian, 4096 is exactly the conjectured count. This is a strict counterexample to the original assertion, not merely to its proposed sufficient criterion.

## 7. Code audit and independent complete enumeration: PASS

The author Python witness program correctly models the fields and operator, checks order and common fixed vectors, checks all vector-pair linearity identities, constructs the orbit partition and 64-point support, and checks its trace. Its claimed scope is appropriately limited: it does not purport to enumerate the group of order 2^135 or computationally prove irreducibility.

The author C++ checker correctly encodes the parity of the translated pairings as a histogram of 12-bit linear functionals on C. Its integer Walsh transform gives all unnormalized sums; its separately computed stabilizer divides those sums to give actual character values. Divisibility and five fully direct rows are checked. Array indices, shifts, signed arithmetic, and counts are within their relevant bounds. No numerical approximation or source-code execution from the paper's archive is needed.

The new audit program `independent_direct.cpp` does not use the author program's polynomial-multiplication routines, signature histograms, or Walsh transform. It encodes points differently, builds the five-line spread directly, applies binary companion matrices to verify those proposed orbits, constructs literal 128-bit supports for every invariant function, and evaluates characters by direct parity of intersections with translated supports. It computes stabilizers from literal translated-support equality. For every u, t, and orbit-indicator basis element, it verifies that the pairing agrees with the representative for t's operator orbit, justifying a 12-term weighted direct sum. It then exhausts all 4096² character/element pairs.

Independent results:

- Nowhere-zero characters: 1728.
- Characters with a zero: 2368.
- Zero-count histogram per character: 1728 with zero zeros, 2048 with 20 zeros, and 320 with 128 zeros.
- Total zero pairs: 81,920 out of 16,777,216.
- Degree histogram: 2 of degree 1, 10 of degree 4, 2 of degree 8, 52 of degree 16, 50 of degree 32, and 3980 of degree 128.
- All vanishing characters have degree 128; exactly 1612 degree-128 characters are nowhere zero.
- Exactly twenty invariant subsets of V have size 64.

The audit also checks Hou's optional analytic zero criterion against every independently computed row. It gives 2048 characters from the first criterion, 320 from the second, and 1728 from neither. The relevant radial-correlation derivation, solvability conditions, and final count in Sections 5–7 were inspected; the extra computation agrees with them. The frozen certificate does not need that derivation for its strict inequality.

Reproduce the independent check with a GNU or Clang C++ compiler (128-bit integer extension used):

    c++ -O2 -std=c++17 -Wall -Wextra independent_direct.cpp -o /tmp/audit_2609
    /tmp/audit_2609

Expected output is `independent_direct_results.json`.

## 8. Required repairs, advisory notes, and exact scope

Required mathematical repairs: **none**.

Required packet repairs: **none**. Any downstream description should preserve the packet's exact provenance and status qualifications, particularly the displayed July date rather than inferring September from the identifier.

Verified conclusions: the actual finite group and faithful coprime order-21 action; its elementary abelian fixed subgroup of order 4096; the exhaustive invariant-character parametrization; the explicit degree-128 character and fixed-subgroup zero; strict failure of the precise original counting assertion; and the supplemental exact count 1728.

Not certified by this audit: minimality among constructions, all infinite-family claims, Carter-subgroup/head-character extensions, other surrounding open problems, the p-group-operator case, earliest historical priority, peer review, editor acceptance, or the live catalogue classification. Reading adjacent claims for scope is not an audit pass for their proofs. The mathematical disposition should remain credited to Eric Hou and should not be presented as a new discovery.
