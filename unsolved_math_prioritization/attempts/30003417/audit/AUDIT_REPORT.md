# Independent adversarial audit: problem 30003417

Audit date: 2026-10-05 UTC. Target: rank 735, OWR-15216-023.

## Verdict

**PASS, narrowly scoped to a sound exhausted/no-resolution packet.**

The exact requested universal equalities have not been proved, refuted, or shown independent. The retained supporting mathematics is correct in its stated regime. The five approach records identify the surviving gaps honestly, and the provenance and integrity claims independently checked below agree with the frozen packet. This is not a solved-problem verdict and does not certify worldwide openness.

**Mandatory corrections: none.** Two optional editorial clarifications appear below. The appropriate disposition remains **exhausted, 5/5 approaches, no resolution**, with known min–max formulas, exact elementary special cases, topological transfer, and the filter-union obstruction retained. A promotion to solved, already solved, independent, or a new universal theorem would fail this audit.

The frozen author artifact was preserved byte-for-byte:

- File: `MEAGER_30003417_SAFE_PACKET.zip`
- Bytes: 23,352
- SHA-256: `69a2cea3fb5fcc1568d0bd538f5738d53ff7208b3b1c021d25f6b642cbdfbd4e`
- All nine archive members agree with the adjacent safe directory.
- The freeze receipt and all nine adjacent files, eleven tracked files in total when including the ZIP, match the independent pre-audit baseline after testing.

## 1. Exact statement and interpretation

The primary contribution is Jörg Brendle's *Generalized cardinal invariants*, in the 2017 Oberwolfach Set Theory report, printed pages 561–563. The definitions on page 561 and conjecture on page 562 were read; the supplied page-562 rendering was also visually inspected. The primary PDF was independently hashed. The report's two equalities are indeed the conjecture, while the neighboring successor-cardinal suggestion is separate. [Primary report](https://publications.mfo.de/bitstream/handle/mfo/3575/OWR_2017_11.pdf?isAllowed=y&sequence=1)

The scope accepted by this audit is:

1. ZFC, with regular uncountable κ and 2^{<κ}=κ.
2. The bounded topology on 2^κ, with initial-segment cylinders of length below κ.
3. The ideal Mκ of unions of at most κ nowhere dense sets.
4. Ordinary inclusion for ideal cofinality.
5. Eventual domination modulo a bounded subset of κ for bκ and dκ.
6. The targets add(Mκ)=bκ and cof(Mκ)=dκ, universally in that regime.

No inaccessible, weakly compact, supercompact, successor, or minimal-continuum assumption is silently added. Regularity is essential to several proofs below; it is not just a convention. ZFC supplies the well-orderings, choices of avoidance extensions, partitions, witnesses, and transfinite recursions used in the exposition. The work does not claim a choice-free result.

The two missing inequalities are exactly bκ≤cov(Mκ) and non(Mκ)≤dκ, once the known min–max formulas are available. This is an equivalence, not a replacement by a weaker objective.

## 2. Proof-by-proof mathematical audit

Every proof in `RETAINED_PROOFS.md` was read in full. Each was checked directly at infinite regular κ. Finite regression output was not used as a substitute for these arguments.

### Lemma 1.1: generalized category and closure — PASS

The recursion avoiding δ<κ nowhere dense sets is valid because the union of fewer than κ stems of length below κ remains a stem. Taking a closure before avoidance is harmless. For the κ-stage recursion, only intermediate stages need be legal stems; the final union is a point of 2^κ. Requiring lengths at least the stage index ensures a total point. This proves properness rather than incorrectly trying to produce a stem of length below κ after κ steps.

A κ-indexed union of κ-indexed meager decompositions has only κ constituents, by κ·κ=κ. Thus the ideal is closed under unions of at most κ members, yielding κ^+≤add(Mκ). The proof never promotes this closure to larger families.

### Lemma 1.2: bκ, dκ and cofinal coding — PASS

For each α<κ, the diagonal supremum ranges over at most |α+1|<κ ordinals below κ, so it is below κ by regularity. The resulting function eventually strictly exceeds each member of a κ-sized family. This shows both failure of unboundedness and failure of domination for that family, with the two directions correctly distinguished.

A dominating family cannot have an eventual upper bound, since it would then fail to dominate that bound plus one. The identity |κ^κ|=2^κ follows from 2^κ≤κ^κ≤(2^κ)^κ=2^κ. For the category cofinality bound, the basis has size κ and hence there are at most 2^κ closed sets and (2^κ)^κ=2^κ many κ-sequences of them. Only closed nowhere dense sequences are needed for a cofinal family. No bound is claimed on the number of arbitrary meager subsets.

### Lemma 1.3: non(I)≤cof(I) — PASS

Properness permits choosing a point outside each member of a cofinal family. If the chosen set belonged to the ideal, cofinality would place it inside a member whose own chosen point lies outside. This is the required diagonal contradiction. The choice is an ordinary use of AC.

### Proposition 2.1: additivity envelope — PASS

The bounded-support group Q has size κ under the arithmetic assumption. Every cylinder contains κ distinct members of Q, by varying a fresh nonzero coordinate beyond its stem, so every tail of a bijective κ-enumeration is dense. Translating that enumeration preserves density. The open sets Uα are consequently dense and E(x,f) is κ-meager.

Closedness of F is needed to obtain a cylinder avoiding it from a point outside F; the proof first takes closed nowhere dense covers. Enlarging each B_i before choosing the common escape point ensures that x avoids every F_{i,j}⊕Q. This avoids a possible but absent closure error.

The number of avoidance functions is μ·κ<bκ: for infinite cardinals, this product is max(μ,κ), and κ<bκ. No regularity of bκ is needed for this particular estimate. An eventual bound makes each closed constituent lie in the appropriate complement of Uα. Thresholds may vary across constituents; the definition of E accommodates that.

The escape-point step still requires μ<cov(Mκ). Boundedness alone does not supply x. The explicit obstruction stated after the proposition is correct.

### Proposition 2.2: cofinal envelope — PASS

A nonmeager Z cannot be contained in the meager translate B⊕Q. After taking a closed cover, one may therefore choose x outside that translate. The κ avoidance functions have a common eventual bound; a member of D eventually dominates that bound. Transitivity of eventual domination yields B⊆E(x,f). The size of the resulting cofinal family is dκ·non(Mκ)=max(dκ,non(Mκ)).

The nonmeager parameter set is not removed or assumed to have size dκ. Removing it would assume the missing inequality.

### Lemma 3.1: the ordinal tree is closed nowhere dense — PASS

The codes 1 and 0⌢1^γ⌢0 are prefix-free for all ordinal γ<κ. Their use does not require a cardinal below κ large enough to enumerate all stems. Each successor child has ordinal length lh(s⌢σγ)+g(γ)+1<κ. All limit unions indexed by δ<κ remain below κ by regularity.

Induction supplies the front antichain property and unique earlier ancestors. Given a node in the downward closure, a front node extends it; appending the reserved symbol 1 is incompatible with every next-front descendant, all of which begin with 0. Later compatible front nodes must descend through that next front. Earlier compatible nodes are prefixes. Thus the omitted cylinder really misses the entire tree body, including nodes from other fronts. Closedness follows from the prefix characterization of a tree body.

### Lemma 3.2: escaping an arbitrary meager set — PASS

The increasing closed nowhere dense cover is legitimate: the closure of a union of fewer than κ nowhere dense sets is nowhere dense by Lemma 1.1. The functions f_s^A take values below κ and there are at most κ of them.

At stage α, g≰*f_{tα}^A gives a coordinate γ with g(γ)>lh(h_A(tα⌢σγ)). The prescribed child length exceeds that absolute ordinal length, since ordinal addition never reduces the right summand. It can therefore accommodate the avoidance extension. The extra +1 in the child length also ensures strict growth, including zero-value cases.

Lengths satisfy lh(tα)≥α by transfinite induction. Consequently the avoidance of A_{lh(tα⌢σγ)} implies avoidance of Aα. Coherent limits are permitted by the construction; the final κ-union has length κ, belongs to the body, and misses every Aα. This does not rely on finite-tree intuition.

### Proposition 3.3: reverse comparison — PASS

For a fixed A, the family of κ many f_s^A is eventually bounded by h. Choosing g from an unbounded family with g≰*h makes g≰*f_s^A for every s, since the contrary would imply g≤*h. Hence the union of the corresponding N_g cannot be meager.

For a proposed cofinal family C of size μ<dκ, collecting its function families gives at most μ·κ<dκ functions. A non-dominating family admits one g not eventually dominated by any member, the quantifier order used in Lemma 3.2. Thus C misses N_g. Neither inference accidentally replaces domination by mere boundedness.

Combining these results with Section 2 and elementary ideal inequalities proves the known min–max formulas in the exact target regime. It does not prove the target equalities.

### Unary-block homeomorphism and Lemma 4.1 — PASS

The complement of the set Y of points with unbounded 1-coordinates is a κ-union of closed nowhere dense eventual-zero sets. Y is dense. Concatenating fewer than κ unary blocks has length below κ by regularity; κ nonempty blocks have total length κ. An unbounded subset of regular κ has order type κ, so the inverse reads all blocks. Gaps at limit-indexed marker positions are handled by ordinal interval lengths.

Cylinders specified through a marker form a base in Y and correspond to successor-length cylinders in κ^κ, which form a base there. This is sufficient for both continuities; no assertion that every limit-length cylinder ends at a marker is necessary.

For dense Y, traces of ambient nowhere dense sets are nowhere dense in Y. Conversely, the ambient closure of a relatively nowhere dense subset of Y cannot contain a nonempty open set, since its trace would contradict relative nowhere density. This establishes the trace equivalence for the κ-meager ideals. Adding or removing the fixed meager complement preserves meagerness. The transfers for add, cov, non, and cof have the correct directions and use ordinary inclusion.

The proof establishes a homeomorphism with a dense comeager subspace, which is enough. It does not assert that all of 2^κ and κ^κ are homeomorphic for every κ.

### Bounding/covering inequalities and Corollary 4.2 — PASS

For a given g, every fixed-threshold eventual-bound set is closed nowhere dense: one fresh coordinate can exceed g there. Their κ-union contains every function eventually dominated by g. This proves bκ≤non(Mκ) and cov(Mκ)≤dκ after topological transfer, with no inaccessible hypothesis.

The exact equalities are equivalent to the two missing comparisons by min–max arithmetic. If bκ=κ^+, the bounds κ^+≤add(Mκ)≤bκ squeeze the first equality. If dκ=2^κ, the bounds dκ≤cof(Mκ)≤2^κ squeeze the second. With 2^κ=κ^+, both hold and all six invariants coincide.

The final comparison κ^{<κ}=κ⇔2^{<κ}=κ is valid here. Regularity bounds the range of every μ→κ function for μ<κ; the arithmetic assumption bounds each λ^μ by some 2^{ν·μ}≤κ. Taking κ many bounded ranges yields κ^μ≤κ. This argument would not justify silently dropping regularity.

### Proposition 5.1: increasing filter unions — PASS

A countable partition of κ into κ-sized pieces exists in ZFC. Each tail A_n has size κ; the stated filter consists precisely of supersets modulo <κ of that tail. A union of fewer than κ small exceptional sets is still small by regularity, proving <κ-completeness. Uniformity, properness, and inclusion of the co-small filter all hold.

The filters increase as their tails shrink. Their union remains a proper filter because any finite family is contained in one stage, but all A_n belong to the union and have empty countable intersection. Thus it is not countably complete. The example refutes only an unqualified filter-union inference. It neither refutes a carefully arranged preservation theorem nor constitutes a forcing countermodel to the target.

## 3. Literature-scope audit

The following are claim-location and scope checks, not complete independent audits of imported forcing constructions.

- Brendle's 2022 v2 Theorem 1 and Corollaries 2–3 support the general reverse comparisons and the two min–max formulas in the required arithmetic regime. The larger arithmetic case is explicitly different. The source's correction of an older equality claim outside the target regime gives an additional reason not to import an old formulation indiscriminately. The publisher confirms volume 46(2), pages 255–269. [arXiv](https://arxiv.org/abs/1907.03111), [publisher](https://program.math.tsukuba.ac.jp/publications/tsukuba-journal-of-mathematics/3943/?lang=en)
- BBFM Proposition 30 and Corollary 31 supply the known translation-envelope mechanism; Question 84 asks about the strict forms at strongly inaccessible or supercompact κ. The authored reconstruction does not claim novelty. [Institutional manuscript](https://eprints.whiterose.ac.uk/id/eprint/118463/1/cichon-large%28revised%29.pdf)
- The dissertation's Question 2.6.1(3)–(4) is specifically posed for **inaccessible κ**, and lists the two strict target failures and equivalent forms. This is dated evidence within that scope. It cannot alone certify openness at every regular successor. [Dissertation](https://ediss.sub.uni-hamburg.de/handle/ediss/10850)
- The 2025 survey distinguishes topological from combinatorial category at non-inaccessible κ in Question 2.3. Its horizontal result cov(Mκ)<dκ and discussion of the corrected iteration are not a separation cov(Mκ)<bκ. Questions 4.8 and 4.21 record actual preservation obstacles. The publicly mentioned prospective random construction is not presented there as a completed target countermodel. [Survey](https://arxiv.org/html/2503.04471v1)
- The revised compactness v2 Theorems 4.1–4.2 state special forcing models with the indicated common category/bounding values. The author packet accurately transcribes their ground-model hypotheses. The earlier author-hosted manuscript includes additional DSS conclusions, whereas v2 Remark 1.1 leaves the relevant uncountable DSS assertion unknown. This discrepancy is unrelated to establishing either universal equality. The journal page confirms publication on 16 May 2025, volume 64, pages 1077–1102. [Revised manuscript](https://arxiv.org/html/2308.13478v2), [publisher](https://link.springer.com/article/10.1007/s00153-025-00977-2)
- The June 2026 singular-product manuscript's introduction and overview concern changing the regularity and topology setting. They do not justify replacing this regular target by a singular-space result. The current arXiv history confirms v2 dated 10 June 2026. [Manuscript](https://arxiv.org/html/2605.09582v2)
- The similarly titled 2026 meager-ideal paper concerns complete metrizable spaces and κ^ω. That is a different exponent/topology. The publisher DOI request failed in this audit, but a university-hosted copy returned through search confirms the relevant κ^ω context. No full-paper audit of that work is asserted. [University-hosted paper](https://ninercommons.charlotte.edu/nanna/record/12840/files/briawil_carin_ir_2026.pdf?registerDownload=1&version=1&withMetadata=0&withWatermark=0)

Targeted fresh web searches did not establish a later solution. This remains a bounded search result. It does not prove worldwide openness, and no contact with authors or private research was attempted.

## 4. Independent data and repository checks

The two complete local corpus files were independently read and hashed against the manifest freshly fetched from the pinned repository commit 73300d9223ca6175983c78cb2370f99ffdd4b59c. The advertised dataset revision is 37e53eabe540fb458758e198be61634bd02ee008. No new corpus download is claimed.

- `problems.json`: 68,931,837 bytes; SHA-256 `04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf`.
- `research_results.json`: 80,334,822 bytes; SHA-256 `8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b`.
- There are 15,458 problem records and 6,701 report keys.
- Numeric ID and problem code match uniquely at index 12,201.
- The report dictionary has no target-code key, and its bytes have no numeric-ID occurrence.
- Statement SHA-256 independently matches `95510472b00f597ee20b5d3b689d5638f605d14ea868458f0e114d9cfbf98296`.
- Review SHA-256 independently matches `c4b6b81057cb7365d95fc908415f318373e18be6d655021fe9eeca8b14a1eb9e` using the exact queue-code convention, including the empty joined report.
- An available complete catalog copy has 21,735,099 bytes; SHA-256 `891938878f1e395de77f6829d5d5d13cb5d5393f85efaa7941fb14bd3e3d7566`; recomputed Git blob SHA-1 `bd5c23e4e6c7e1901717a7e596477a7f6dc72425`. The fresh repository metadata returns that same catalog Git blob SHA-1. Its unique target record exactly equals the supplied descriptor.

The fresh pinned attempts-directory listing has 62 entries and no 30003417 entry. Current exact-ID code, all-state PR, and branch searches returned no results. This independently corroborates a bounded no-prior-attempt finding. It does not certify absence from deleted branches, unindexed files, unrelated histories, or unpublished working trees. Not every historical topic/commit search reported by the author was repeated.

All eight supplied scholarly PDF byte counts and SHA-256 values match the author provenance metadata. This certifies file identity with the inspected input set; it is not a claim that every PDF was redownloaded or that every proof inside it was audited.

Only authored audit text, executable verification code, and public verification metadata appear in this audit output. No corpus records, source extracts, scholarly PDFs, screenshots, credentials, or private coordination material are included.

## 5. Tests, limitations and negative controls

The author's portable verifier was run without modifications and passed with its stated restricted scope. Its 371 finite admissible order assignments are regression tests, not realizable cardinal configurations.

The independent verifier imports none of the author's code. It checks the externally specified ZIP anchor, internal hashes, exact archive allowlist, duplicate names, symlink entries, directory equality, frozen baseline, complete semantic controls, full optional source bytes, identity joins, statement/review hashing, and catalog identity.

A separately implemented eight-label order test visits 1,086 admissible assignments. It records 336 abstract failures of each target and 126 simultaneous abstract failures while preserving the known order constraints and min–max formulas. Those counts only demonstrate that the displayed comparisons and formulas do not logically force the conjecture. They do not produce cardinal models.

Sixteen negative controls were all rejected, including deletion of regularity or the arithmetic hypothesis, an inaccessible-only scope substitution, countable instead of κ-unions, changed cofinality order, false solution/countermodel flags, substituting the min–max formula for the target, reversing a missing inequality, source-PDF inclusion, path traversal, duplicate ZIP members, symlinks, corrupt archive bytes, and a bad hash.

Normal Python and optimized Python both passed the independent verifier's portable checks. Its failures use explicit exceptions, so `python -O` cannot erase checks. Syntax compilation also passed. The complete source run is recorded separately from the portable run.

Neither verifier proves infinite-cardinal statements. No formal proof assistant was used. The mathematical PASS is the direct proof audit in Section 2; the executable PASS is the narrower result recorded in `INDEPENDENT_VERIFICATION.json`.

## 6. Optional clarifications and publication boundary

No change is necessary to retain the packet under its present no-resolution disposition. For a later editorial revision, the following would make the scope even clearer:

1. In the dissertation paragraph, explicitly add that Question 2.6.1 is posed for inaccessible κ. Its missing qualifier does not invalidate the current cautious, bounded-status conclusion, but specifying it prevents an overly broad reading.
2. State ZFC explicitly at the start of the proof file. Its conventional AC uses are valid and do not require mathematical repair.

Do not edit the frozen packet in place to replace its historical `pending` audit fields. This independent audit is a separate attestation to that exact artifact. Any newly packaged revision needs its own hashes and an explicit connection to the audited version.

There were no remote writes, publication, queue changes, or uploads during this audit. A later authorized publication should retain the no-resolution warning and must exclude the source inputs. This PASS supplies no authorization for publication or a claim that the universal conjecture has been settled.
