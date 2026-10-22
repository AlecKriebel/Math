# Independent adversarial audit: 30001887

Date: 2026-10-05 UTC. Target: rank 708, OWR-11136-013, planar multiple-cover decomposition thresholds.

## Verdict

**PASS, with the packet's stated scope limits. Five of five substantive approaches are accepted. The investigation remains UNSOLVED.**

No substantive mathematical error, invalid retained theorem, fabricated full resolution, novelty claim, or global-openness claim was found. No correction to the frozen packet is required. The audit certifies the retained conditional results, special cases, counter-inferences, and the appropriately limited outcome. It does not certify a solution to the original problem or present-day global openness.

The strongest retained statement is valid: each finite hypergraph can be encoded at finitely many witness points using translates of an open planar set P whose every whole-plane cover splits into k covers for every fixed finite k. Thus m_k(P)=1 under the minimum-positive-threshold convention. This statement remains valid for arbitrary indexed covers, including uncountable families and repeated translates.

## Exact binding and preservation

The input consists of exactly 11 files. The 1,778-byte MANIFEST.json has SHA-256:

ff6abddb8c4dc94bd3ef7da776d88e42bfe41501e5f6de8bf9a5206b72f8fa64

All ten manifest entries match their recorded byte lengths and hashes. No extra input files are present. The full eleven-file binding is in exact_binding.json. PROOF.md is 17,261 bytes with SHA-256 9972fb6d317b11ef877f5e7f6d2d1abad0799cb18dd6943ce96322def9f9d2a8. The original files were read without modification and rechecked after the audit.

The binding is to this frozen packet and the recovered primary-source question. It is not a certification of an inaccessible website's exact wording or of an unavailable raw AI record. The numeric rank and catalog identifier are supplied target metadata, not separate mathematical facts proven by the sources.

## Primary-source scope

Fresh downloads of all five cited PDFs succeeded with HTTP 200. Each fresh file exactly matches the packet's recorded SHA-256 and byte count. source_checks.json records those independent retrieval results; no PDF, extract, image, or raw record is included in this audit.

1. **Original OWR contribution.** The definitions on printed pp. 2512-2513 and questions on p. 2514 use one fixed planar set and its translates covering the whole plane. No boundedness, convexity, openness, point-finiteness, or local-finiteness assumption is imposed in those definitions. The discussion of non-locally-finite covers confirms that local finiteness is not a standing hypothesis. The two questions are linear growth with a shape-dependent constant and the weaker implication from finite m_2 to finite m_3. The footnote qualifies Theorem C(iv) by the earlier wedge criterion; the packet properly avoids upgrading it to an unrestricted polygon assertion. The catalog suffix 013 is not treated as the later problem-session number. Printed pp. 2512-2514 were independently read and visually inspected from the fresh PDF. [Primary OWR PDF](https://ems.press/content/serial-article-files/46358?nt=1).

2. **2013 survey.** Definitions 1.1, 1.6 and 2.3, Section 2.3, and Problem 6.6 distinguish whole-plane from arbitrary-target decomposability. The distant-half-plane example and finite-type bound are genuinely present, so neither is misrepresented as new. Definition 1.6 supplies the positive-threshold convention used for m_k(P)=1. Its older open-question list does not establish present-day openness. [Survey on Decomposition of Multiple Coverings](https://real.mtak.hu/15290/1/surveyfinal.pdf).

3. **2025 survey v1.** The definitions and Conjectures 2.1, 9.1 and 9.2 retain hereditary-family finiteness and linear-growth conjectures. Sections 2.3 and 2.3.2 explicitly focus the geometric parameters on finite subconfigurations and explain the avoidance of infinite-hypergraph issues. This supports the packet's warning against identifying these parameters with arbitrary whole-plane covers. Submission date 10 December 2025 was checked on arXiv. [Coloring Geometric Hypergraphs: A Survey](https://arxiv.org/abs/2512.09509v1).

4. **2024 note.** Theorem 3 states the finite hereditary example m_2=3, m_3=6. This refutes a proposed sharp bound, not finiteness of m_3, and supplies no whole-plane fixed-shape counterexample. The statement and surrounding definitions were inspected; its source edge list was not independently recomputed and is not copied here. [Published note](https://d-nb.info/1357048173/34).

5. **2026 note v1.** Theorem 2 and Lemma 3 on pp. 1-3 concern finite (2h-1)-uniform hypergraphs with h-heavy restricted subhypergraphs two-colorable. Varying h does not hold the two-color threshold fixed. No geometric realization with the required global quantifiers follows. The complement lemma's case distinction was checked, but the later probabilistic construction and finite appendix certificates were not audited. arXiv's public author-checked/AI-drafted description and submission date 27 April 2026 were verified; the manuscript's internal title-page date is 28 April. No journal-acceptance claim is made. [Public preprint](https://arxiv.org/abs/2604.24412v1).

The exact unsolvedmath page again returned HTTP 403 in a fresh fetch; the web reader also failed. No raw AI record was inspected. A bounded current search did not identify a verified full resolution. None of these negative searches is a proof of absence.

## Adversarial reconstruction of the coding theorem

Let n>=1, q>=1, Q=n+1, t_i=(i,0), and x_e=(Q(e+1),0). Put an open radius-1/4 disk at x_e-t_i for every desired incidence, and append the open half-plane with first coordinate greater than R=Q(q+1)+n.

### Exact finite incidences

For any two pairs (e,i), (f,j), equality of their candidate centers implies Q(e-f)=i-j. Since |i-j|<=n-1<Q, both differences vanish. The candidate coordinates are distinct integers, separated by at least one. A witness preimage is in a disk exactly when that disk was selected for its own incidence. Radius 1/4 creates no accidental incidence and places no witness on a disk boundary.

All witness preimages have horizontal coordinate at most Qq<R. The appended half-plane cannot change any witness incidence. Its separation from the disks is also strict. Empty edges, repeated edges, isolated vertices, and the all-empty incidence system cause no exception. If no disks are selected, P is just the open right half-plane. The finite realization does not itself cover the plane.

### Whole-plane coverage and uncountable families

P lies inside the open half-plane u>0 and contains u>R. Consider any indexed whole-plane cover (P+(a_i,b_i)) over any set I. If all a_i were bounded below by L, every member would lie in u>L, leaving points to the left uncovered. Therefore the horizontal coordinates, not merely the norms of the translation vectors, are unbounded below.

Recursively select indices i_j with

a_(i_j) < min(-j, a_(i_(j-1))-1).

The first choice can be made below -1. These coordinates are strictly decreasing and tend to minus infinity; distinctness of the indices is automatic. This is a countable extraction from I, not an assumption that I is countable. Even if equal translates are disallowed, the selected sets are distinct: the infimum of the horizontal projection of P is finite, and translation shifts that infimum by a_i.

For fixed finite k, color i_j by j modulo k. Each residue class remains cofinal towards minus infinity. For any point (x,y) and color c, choose a sufficiently late j of that residue so a_(i_j)<x-R. Then (x,y) is in the translated open half-plane u>R+a_(i_j), independently of b_(i_j). The strict inequality removes the boundary concern. Assign every unselected index, however many, to one fixed color. Coverage is preserved, and every original index belongs to exactly one color.

This gives a partition of each whole-plane cover into k covers. The claim is nonvacuous: translations with a_j=-j(R+1) form a whole-plane cover. Thus the positive threshold is exactly one. The same argument puts infinitely many members through each point, so no point-finite whole-plane cover of this P exists.

### Failed substitutions that were rejected

- A finite prefix of the extracted sequence cannot cover the entire plane.
- Strict decrease alone does not suffice: a sequence decreasing to a finite limit is not cofinal towards minus infinity.
- Unbounded vertical translations or unbounded parameter norm do not force horizontal coverage.
- Finite deep incidence failure is not a global obstruction: extending by cofinal half-planes supplies each missing color at every witness.
- The constructed shape depends on the finite hypergraph. No single bad fixed P with all-threshold global witnesses is obtained.
- The unbounded, generally disconnected shape proves nothing for a separately imposed bounded or convex subclass.
- General openness does not make these covers point-finite. The OWR local-finiteness reduction discussed for open polygons must not be transferred to this unbounded construction.

The countable extraction and compactness arguments are understood in the usual classical set-theoretic setting.

## Review of the other retained arguments

### 1. Hereditary balancing: accepted

The recursive real lower bound after j levels is (|e|-(2^j-1)D)/2^j. At q=2^ceil(log_2 k) leaves, the asserted threshold q+(q-1)D gives at least one vertex of every finite edge per leaf. Merging leaf labels preserves coverage, and the bound is linear in k for fixed D. Finite edges and a uniform hereditary discrepancy hypothesis are essential and stated.

A merely successful two-cover split has no promised depth balance. The one-versus-many split illustrates this logical gap without claiming that a better split does not exist. No discrepancy bound or infinite-depth invariant is derived from whole-plane m_2(P). This route therefore remains conditional.

Nonblocking precision note: the verifier's one-below-threshold zero is a failure of a deliberately conservative floor lower bound. Actual integer child bounds can be stronger. For D=1, q=2, the displayed M is 3, yet a balanced split of size 2 has both children of size 1. The packet does not claim threshold optimality; neither does this audit.

### 2. Shallow subcovers and intervals: accepted

Removing s-shallow subcovers k-1 times leaves depth at least one from initial depth 1+s(k-1). Finite loss also preserves infinite point degree. The hypothesis applies at every removal because the current family remains a subfamily covering the same target.

A finite inclusion-minimal closed-interval subcover has depth at most two: among three intervals through one point, the two extreme endpoints identify at most two intervals containing the third. Removing that third interval contradicts minimality. Degenerate intervals, ties, duplicate copies, an infinite target, and an empty target present no defect. The resulting 2k-1 bound is sufficient, not an asserted optimal interval bound.

For congruent closed strips, point-finiteness makes the endpoint multiset locally finite. Whole-line coverage forces endpoints unbounded in both directions; hence they have a Z-order, including finite ties. Every point sees a consecutive finite block, so cyclic coloring works. The lattice/shifted-lattice example gives the lower bound k for the restricted threshold. The missing extension to arbitrary P is a uniform shallow-subcover theorem, not supplied here.

### 3. Random coloring: accepted

The union bound is strict and counts at most Nk missing-color events. Choosing M finite witnesses in each of finitely many infinite edges legitimately reduces that case to a finite hypergraph. The complete s-uniform hypergraph on 2s-1 vertices blocks any attempt to remove the constraint count for arbitrary hypergraphs. Neither a uniform N nor a suitable dependency bound is derived from the original hypothesis.

### 4. Extremal obstructions and geometric coding: accepted

The hub construction is two-colorable, but a polychromatic three-coloring would induce a two-coloring of every s-subset of 2s-1 old vertices, which is impossible. Deleting the hub gives the offending non-two-colorable trace, so the examples are explicitly nonhereditary. The coding theorem was reconstructed above. These two controls show why finite obstruction data do not meet the required fixed-shape global quantifiers.

### 5. Finite types and compactness: accepted

If depth exceeds r(k-1), some covering type at each point has at least k copies. Distributing k copies of each sufficiently frequent type across all colors covers every point. Infinite multiplicity is harmless. Replacing r by a uniform pointwise type bound t is valid.

For a point-finite cover, each all-colors incidence condition depends on finitely many coordinates and is closed in the compact product of finite color sets. Finitely many point conditions involve a finite union of their complete incidence edges. The finite-family heavy-point premise yields their simultaneous coloring, giving the finite intersection property. It is stronger than a premise only about whole-plane covers. Infinite-edge constraints can fail to be closed; the red-prefix/alternating-tail sequence converges to the all-red coloring. This is a failure of that compactness proof, not a noncolorability example.

The five routes have different operative hypotheses and different barriers: quantitative discrepancy, shallow subcovers, constraint counts, extremal/global realization, and finite-type/compactness transfer. Counting them as five substantive approaches is justified.

## Independent computation and deliberate negatives

The frozen verifier was executed from an unrelated empty temporary directory. Its stdout was byte-identical to verification_results.json: 2,198 bytes, SHA-256 91315b5fc5bfdc64db6b5d10aef37db2412bd2f5919dc8f0a44d8459536abdf6. This is a replay, not the independent test.

independent_controls.py was written separately and neither imports nor reads the frozen verifier or its outputs. It uses exact integers, bit masks, and rational arithmetic. Its independent checks include:

- 48 balancing formulas, plus 488 feasible integer child-bound cases
- 30,648 base interval-cover/target cases, using reversed removal order
- 1,368 additional degenerate/duplicate interval cases, checking every minimal subcover
- 4,149 matching cyclic cases plus 1,383 right-closed cases; 56,940 point/boundary queries
- 157,888 multiplicity/incidence cases, testing an explicit coloring on all 999 qualifying heavy patterns, and 15 one-less pigeonhole controls
- Exhaustive hub colorings for s=2,3,4, with two-color counts 8,32,128 and zero three-color counts
- 352 hub incidence pairs, plus 5,050 arbitrary incidence systems and 56,770 witness pairs
- All-empty, repeated, full, and isolated-vertex incidence cases, and strict disk/half-plane boundaries
- The four strict rational union-bound thresholds M=2,9,21,39
- 2,727 explicit residue-class half-plane witnesses

Deliberate negatives detect all-equal coloring, union-bound equality, colliding spacing, oversized disks, a prematurely placed half-plane, finite-prefix global coverage, bounded decreasing horizontal parameters, and vertical-only escape. The infinite-tail closure warning and the non-sharp balancing-bound interpretation are also independently checked. Full results and negative witnesses appear in independent_results.json and deliberate_negatives.json.

These enumerations are finite controls. They are not extrapolated into a universal geometric proof; the written arguments support the accepted universal claims.

## Prior-work check and exclusions

Independent read-only GitHub queries for both exact identifiers among all PR states, an exact-ID branch query, and default-branch code search returned no matches. The branch query returned no continuation. These repeat a narrower subset of the packet's repository checks and do not certify every branch's contents or unindexed work. The earlier broad branch/tree search history remains an explicitly bounded author record.

No input packet, repository, branch, commit, PR, or remote service was modified. This audit contains only the audit text, verification code, metadata, numeric finite-control results, and a manifest. Source PDFs, source extracts, source images, raw AI/catalog records, and private coordination files are excluded.

## Disposition

Accept the five approaches and retained results as a correctly scoped unsuccessful investigation. Retain outcome=unsolved, complete_proof=false, complete_counterexample=false, verified_prior_resolution=false, novelty_claim=false, and global_openness_claim=false. Keep the exact-website/raw-record limitations visible. No dependent mathematical work is blocked by a required correction.
