# Independent audit of KOU 21.114

## Decision

**Mathematical and computational checks pass. One provenance correction is required before a separately frozen v2 can be accepted.** The outcome remains **unresolved after five approaches**, with no solution, no absolute derived-length bound, no counterexample family of unbounded derived length, and no claim of novelty.

The immutable author archive is `KOUROVKA_2623_AUTHOR_SAFE_FREEZE.zip`, 21,815 bytes, SHA-256 `d1f66407e8a7ff1c7aceaf7531b959085877de50c4198558d5d69dc33983f0f4`. All nine extracted members match the supplied author directory byte for byte. The author manifest and exact checker replay successfully. The archive, receipt, and author files were not modified by this audit.

The mandatory correction concerns the earliest identified source. The equivalent question is already present in Lisi–Sabatini's **22 March 2022** preprint, *Weakly-top groups*, arXiv:2203.12021v1, Section 3.3, page 5. Its Section 1 definition is the same subgroup-abelianization inequality. The 2024 article and Question A attribution remain correct, but 2024 is no longer the earliest source identified. This is a documented earlier occurrence, not a claim of absolute priority. [Verified v1 PDF](https://arxiv.org/pdf/2203.12021v1)

A secondary editorial recommendation changes “right coset” to “left coset xH” in the enumeration explanation and its code docstring. The enumeration itself is correct. Exact files, locators, old/new strings, and required metadata are supplied in `CORRECTIONS.json`.

**Release gate:** this audit does not accept an as-yet uncreated v2. Preserve the original freeze, create a separately named corrected v2 with a full delta and new manifest, and obtain explicit independent delta acceptance before publication. No remote mutation was performed.

## Scope and independence

The audit reviewed every argument in `PROOFS.md`, all five approach outcomes, the stated limitations, source identities and relevant primary passages, the original checker after constructing a fresh implementation, and the archive/manifest boundary.

The independent checker was implemented before reading the author checker. It constructs groups from faithful permutation generators rather than the author's coordinate multiplication formulas. It enumerates subgroups by **normal extensions of index p**, rather than arbitrary one-element adjunction with coset pruning. It neither imports nor executes the author checker to obtain its independent results. The author results were used as the comparison target only. A later author replay is recorded separately.

All 11 group constructions independently reproduce their structural invariants. The nine full subgroup lattices contain 578 subgroups in total. Every one of the 21,347,492 associativity triples across the 11 group tables was checked. All **114** compared invariant, histogram, and witness fields agree. Table hashes are intentionally not compared across different group labelings; this audit records its own permutation-element hashes.

The audit establishes correctness of the stated partial results, subject to the explicitly cited nilpotency theorem. It does not independently re-prove every theorem imported by that published result, audit the full probabilistic proof in the 2025 paper, perform a complete database census of p-groups, or formalize the mathematics in a proof assistant.

## Problem identity and mathematical boundary

For a finite group X, put a(X)=|X/X'|. Weak ab-maximality means a(H)≤a(X) for every H≤X. The requested bound must be independent of group order, abelianization size, and prime. A bound depending on those parameters is not a solution. Nilpotency class and derived length must remain distinct.

The October 2026 editor-hosted Notebook was independently downloaded. Its bytes and hash reproduce the author's values. Printed page 194 is PDF page 194 and was visually inspected: 21.114 is attributed to L. Sabatini, has the stated weak inequality and finite-group scope, carries the p-group reduction annotation, and has neither a solved marker nor an unverified-AI marker. This is a current primary-source status check; it does not prove absence of unindexed work. [October update](https://kourovkanotebookorg.wordpress.com/2026/09/30/october-2026-update-for-the-21st-edition/)

## Proof review

### Quotients

**Pass.** For N normal in G and N≤H≤G, the abelianization of H/N has order a(H)/|N:N∩H'|. Since H'≤G', the denominator for H is at least the denominator for G. Combining this with a(H)≤a(G) gives the required quotient inequality. The argument includes N not contained in G'; that restriction is unnecessary. Quotient closure does not imply subgroup closure.

### Direct products and reduction to p groups

**Pass, with an external theorem clearly identified.** For H≤A×B, take K=H∩(A×1) and L its projection to B. Projection sends H' onto L', so the kernel on abelianizations is exactly the image of K. Thus a(H)≤a(K)a(L). This proves sufficiency for a direct product; necessity follows by taking factor quotients.

The imported Lisi–Sabatini Theorem 1.2 supplies finite nilpotency. Its statement and the complete relevant proof in Section 3 were checked in arXiv v4. It is correctly applicable to the weak, rather than strict, abelianization condition. The proof's imported foundations remain external. Once nilpotency is available, Sylow factors and coordinatewise derived series give the claimed reduction to finite p-groups. [Lisi–Sabatini v4](https://arxiv.org/abs/2203.12021v4)

### Minimal quotient obstruction

**Pass.** Fix d≥1 and choose a minimum-order weakly ab-maximal p-group P of derived length greater than d, if one exists. Quotient closure and minimality imply P^(d)≤N for every nontrivial normal subgroup N. Therefore all such N contain the same nontrivial subgroup; a minimal one is unique. The p-group class equation supplies a nontrivial central element in that minimal normal subgroup, forcing it to have order p. Hence P^(d) is exactly this subgroup and P^(d+1)=1.

Every order-p subgroup of Z(P) is normal, so Z(P) has a unique order-p subgroup. Finite abelian p-group structure then makes Z(P) cyclic. There is no illicit assumption that all subgroups of P inherit the defining condition. These are necessary conditions on hypothetical minimal counterexamples, not a contradiction or an existence assertion.

### Parameter dependent order and derived length bounds

**Pass.** For a finite p-group P, choose an inclusion-maximal abelian normal subgroup A. The centralizer C_P(A) is normal. If it strictly contains A, its image in P/A meets the center nontrivially. An order-p subgroup of that intersection lifts to a strictly larger abelian normal subgroup, contradicting maximality. Thus C_P(A)=A and P/A embeds into Aut(A).

Writing |A|=p^b, A has at most b generators, so its automorphism group has at most p^(b²) elements. Weak ab-maximality gives b≤a when |P/P'|=p^a. Consequently |P|≤p^(a(a+1)). The lower central series strictly descends while nontrivial; if |P|=p^N, its class is at most N. The standard inclusion P^(j)≤γ_(2^j)(P) yields the stated ceiling bound from 2^j>N. The off-by-one at N+1 is correct.

The statement uses P in the p-group setting established by the surrounding section. Explicitly writing “finite p-group” in its opening sentence would improve readability but is not needed to repair the argument. Even under a more literal finite-group reading, the imported nilpotency theorem and p-power abelianization force all non-p Sylow factors to be trivial. The parameter a is unbounded, so this conclusion has no uniform-bound consequence.

### Cyclic holomorphs

**Pass for every prime, including p=2.** The units congruent to 1 modulo p form an abelian group K of order p^(n−1). For p=2 this is the full unit group, which need not be cyclic. With N cyclic of order p^n, the commutator subgroup of N⋊K is pN because every u−1 is divisible by p and u=1+p achieves valuation one. Successive commutation produces p^(i−1)N, so class n and derived length two follow exactly for n≥2.

For an arbitrary subgroup H, let A=H∩N have order p^s and let R be the projected subgroup of K. If R is trivial, H is contained in N. Otherwise the minimum nonidentity valuation t of u−1 exists with 1≤t<n. The commutators of A with lifts of R generate p^t A; changing the conjugation convention only multiplies u−1 by a unit and does not change this subgroup. Hence a(H)≤|R|p^min(s,t). All R elements lie among the p^(n−t) units congruent to 1 modulo p^t, proving a(H)≤p^n.

This argument does not assume a complement in H, does not need K to be cyclic, and covers A trivial, R trivial, and s≤t. It is a complete direct reconstruction of the known family, not a finite-sample inference.

### Failure of subgroup inheritance

**Pass.** The affine action of C8⋊Aut(C8) contains the inversion subgroup D16, which contains C8. The three abelianization orders are 8, 4, and 8. Thus the middle subgroup fails the condition despite lying in a group that satisfies it. The independent verifier checks the inclusion as an explicit homomorphism of permutation tables, not just through coincident invariants.

### Regular wreath products

**Pass for the exact stated scope.** For nontrivial finite p-groups A and B and regular top action, abelianizing the base kills coordinate commutators and identifies the coordinate images transitively. Together with the top projection this gives W_ab≅A_ab×B_ab. The base has a(A)^|B| as its abelianization order. Therefore a(A)^(|B|−1)≤a(B)≤|B| is necessary.

Because a(A)≥2 and 2^(m−1)>m for every integer m≥3, |B| must be two. Then p=2 and a(A)=2. The proof that a finite p-group with cyclic abelianization is cyclic is valid: a maximal subgroup containing a putative proper cyclic generating lift would also contain the commutator subgroup, a contradiction. It follows that A=B=C2. The converse uses D8 and its proper subgroup order bound correctly.

The recursive wreath formulas a(W_r)=p^r and a(base)=p^(p(r−1)) are consistent. The first bad 2-wreath example has derived series orders 128,16,2,1, while its base has a=16 and the whole group a=8. It reaches derived length three but fails weak ab-maximality. No conclusion is drawn about general semidirect products or nonregular actions.

### Full unitriangular groups

**Pass for all prime powers q and n≥4.** Projection onto the first superdiagonal gives an abelian quotient of order q^(n−1). The elementary commutators generate all entries of larger superdiagonal distance, so the displayed kernel is exactly the commutator subgroup, in every characteristic.

The top-right rectangular block with k=floor(n/2) has zero product with itself. It therefore gives an abelian subgroup of order q^(k(n−k)). The even and odd n inequalities are correct beginning at n=4 and n=5 respectively. The obstruction applies to full UT_n(F_q); it does not pass automatically to their arbitrary subgroups or sections. The verifier explicitly constructs the order-16 rectangular subgroup of UT4(2).

### Direct product padding and the stated central products

**Pass under the displayed hypotheses.** The direct-product implication already rules out ordinary padding. In the central product Q=(G×E)/Δ, the assumption Δ≤G'×E' makes Q'=(G'×E')/Δ. The same cancellation applies to the image of H×E only because the hypotheses also put Δ inside H'×E'. Thus the violating abelianization ratio survives exactly. No assertion about arbitrary central extensions follows.

For the order-128 wreath example, the diagonal copy of the center of D8 lies in the derived subgroup of its base. The independent table reconstruction confirms that the entire wreath center has order two and is contained in that base derived subgroup. Amalgamation with an extraspecial group along its derived center consequently meets the stated hypotheses. This closes the claimed construction route and no larger class of extensions.

## Independent finite computation

The nine exhaustive counts, in the same order as the author examples, are:

| Group | Order | Subgroups | Largest subgroup abelianization | Whole abelianization |
|---|---:|---:|---:|---:|
| C4 holomorph p part | 8 | 10 | 4 | 4 |
| C8 holomorph p part | 32 | 58 | 8 | 8 |
| C16 holomorph p part | 128 | 196 | 16 | 16 |
| C9 holomorph p part | 27 | 10 | 9 | 9 |
| C27 holomorph p part | 243 | 36 | 27 | 27 |
| C25 holomorph p part | 125 | 14 | 25 | 25 |
| C8 inversion subgroup | 16 | 19 | 8 | 4 |
| C2 wr C2 | 8 | 10 | 4 | 4 |
| UT4(2) | 64 | 225 | 16 | 8 |

For the two nonexhaustive cases, the exact disqualifying subgroups are the order-64 base of the order-128 iterated wreath group and the order-27 elementary abelian base of C3 wr C3. Their abelianization orders exceed those of their ambient groups by factors two and three respectively. The verifier reports no lattice completeness claim for these two cases.

### Why the independent lattice search is complete

For a proper subgroup H of a finite p-group K, let H act on K/H. The number of fixed cosets is |N_K(H):H| and is congruent to [K:H] modulo p. Since the identity coset is fixed and p divides [K:H], there are at least p fixed cosets. Thus H<N_K(H), and N_K(H)/H has an order-p subgroup. Its inverse image is a subgroup extending H normally with index p.

Starting at the identity and repeatedly taking such extensions therefore reaches every subgroup K by induction on its order. The implementation tries every x outside each H, verifies x^p∈H and normalization of H, and forms the p cosets. Every emitted subgroup is separately checked for identity, inverses, multiplication closure, and equality with the subgroup regenerated from its recorded generators. Full element sets identify duplicates.

The permutation constructions are faithful affine actions for holomorphs, imprimitive block actions for wreath products, and the natural action on F2^4 for UT4(2). Adjacent transvections generate the latter full group. Derived and lower-central series are generated from all pairwise commutators in the relevant terms. Normality of each computed derived subgroup is checked directly. These algorithms use exact integers and finite sets only.

The verifier's 55 wreath sanity tests and 97 rectangular-exponent sanity tests are explicitly bounded checks. They are not the proofs of the corresponding infinite statements. The author's 55 wreath tests exercise iterated-wreath exponents, whereas the independent 55 tests exercise the necessary regular-wreath inequality; matching the sample count is not a claim that these are the same test vectors.

## Literature audit and source proof caveats

The 2022 preprint, 2024 arXiv version, 2025 arXiv version, and October 2026 Notebook were all freshly downloaded as complete PDFs. The last three hashes match the author's source metadata exactly. `SOURCE_AUDIT.json` records byte counts, hashes, inspected locations, public version/status, successful retrievals, and access failures.

The v1 terminology “weakly-top” is equivalent here, since including H=G in a nonstrict inequality adds only an equality. The question on v1 page 5 explicitly considers whether a uniform derived-length bound exists. Its earlier title must be retained when citing that version; using the v4 title for v1 without qualification would obscure the version history.

The 2025 Eberhard–Sabatini paper answers Lisi–Sabatini Question C negatively through class-two constructions. It is not a resolution of Question A or 21.114. The theorem gives |G:G'|=p^n and |G'|=p^(n−3) for arbitrarily large n. The exponent of |G| in the abelianization size tends to one half, while derived length remains at most two. Published and peer-reviewed status was independently checked at Warwick's institutional repository; the inspected mathematical text is arXiv v2. [Publication record](https://wrap.warwick.ac.uk/id/eprint/191736/)

The proposer's current bibliography and the eight explicitly enumerated problems of the July 2026 *On Some Problems from the Kourovka Notebook* paper were checked. That paper's list does not include 21.114. These are bounded discovery checks, not an exhaustive survey of every manuscript or every proof in those papers. [July 2026 paper](https://arxiv.org/html/2607.17477v2)

The inspected v4 source contains small issues that must not be silently imported into a reconstruction:

- The cyclic index in the Lemma 3.6 proof is p^(i−1), whereas one printed equality has p^i. The end of its p=2 argument also has an indexing shift.
- The binomial-divisibility sentence in Lemma 3.7 is too strong: binomial(9,3)=84 is not divisible by 9. The intended odd-prime congruence is nevertheless obtainable by a correct valuation argument.
- The cyclic-complement description in Example 3.8 does not cover p=2, where the full unit group of Z/16Z is noncyclic.

Pages 8 and 9 were visually checked to distinguish these from extraction artifacts. The author proof uses the correct lower-central indexing, avoids the faulty divisibility shortcut, and explicitly allows the noncyclic 2-power unit group. Consequently none of these source caveats is a mathematical defect in the submitted reconstruction. They reinforce the need to keep the reconstructed argument and its exact scope rather than treating a citation alone as proof.

## Dataset and repository verification

The complete locally available public `problems.json` and `research_results.json` bytes were independently rehashed and compared with a freshly read manifest at commit `e6d8afc10086a94847764cdef165fffec3314c6b`. This is complete-byte verification, not a fresh dataset download. The byte counts are 68,931,837 and 80,334,822, with 15,458 problem records and 6,701 research entries. Both SHA-256 values match the pinned manifest. The selected target record and its statement hash match the author's selection. No dataset records or source text are included in this release.

The complete research-results corpus was searched by target key, problem number, and contemporary/historical defining terminology; no matching entry was identified. The pinned queue independently confirms rank 772, identifier 2623, KOU-21.114, and historical queued 0/5 state. This is not a statement that the completed local five approaches are still zero attempts.

The pinned attempts listing contains 62 entries and no 2623 entry. Bounded current code and PR searches for 2623 return no match. The independent recursive-tree read failed with a transport error, just as the author's tree access had failed. Thus no claim of exhaustive repository-history absence is made. No branch, commit, PR, comment, queue record, or other remote state was changed.

## Remaining gap and acceptance conditions

All five approaches are substantive but partial: structural descent; cyclic holomorph reconstruction; regular-wreath growth obstruction; full unitriangular obstruction; and center-enlargement obstruction. Their distinct stopping points are accurately stated. None controls derived length in every weakly ab-maximal p-group uniformly.

The next mathematical contribution would have to bound the necessary minimal-counterexample family or give a different construction with genuinely unbounded derived length and verified inequalities for every subgroup. This audit recommends neither a solved classification nor a novelty claim for the present partial results.

Before a corrected release is accepted:

1. Apply C1 exactly or supply an equivalent, independently checked correction with the same evidence and priority limitation.
2. Prefer also applying the harmless C2 terminology correction.
3. Preserve the original archive and receipt; create separate v2 artifacts and a complete old/new hash delta.
4. Replay both checkers. The mathematical results should remain byte-identical; any substantive change needs renewed review.
5. Record independent acceptance of the actual v2 delta and final safe manifest. Do not infer acceptance from this conditional report.

The safe audit package contains only authored analysis, correction instructions, public verification metadata, independent code/results, and integrity metadata. Source PDFs, extracted source text, raw datasets, service responses, and private coordination are excluded.
