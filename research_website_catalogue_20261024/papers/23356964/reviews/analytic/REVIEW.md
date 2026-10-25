# Independent analytic review — Zenodo 23356964

**Verdict: PASS for the exact current mathematical statements. Completion: 100%.** No substantive defect or unresolved central interface was identified. This is an AI-assisted analytic review, not external human peer review, a formal proof-assistant certificate, or a priority determination. Root publication disposition remains separate.

## Source identity

*Generic Cantor actions of Z wr Z are hyperfinite*, Alec Kriebel, version 1.0.0, five pages. The manuscript and Zenodo publication-date field say 13 October 2026; the record-created timestamp is 2026-10-14T04:32:49.677542+00:00. These are distinct recorded fields, not a claim about earlier public availability. Record: https://zenodo.org/records/23356964; version-specific DOI: 10.5281/zenodo.23356964.

| Asset | SHA-256 |
|---|---|
| generic-wreath-hyperfiniteness-note.pdf | a164240679a1ed733c4eebce1817c239a423a9cd7952d93d9902e0885160ae4e |
| generic-wreath-hyperfiniteness-verification.zip | 3d73bb07b994c619df8a7e27ed2e43c99dd4e30c9fc1e5406454ee0671d1ebdd |
| record.json | f4096d4c3f6357b761902cc97f30454d12e3dbbfe78e8ff4f2ec5201bb0eb827 |

The public assets independently match their API sizes, MD5 values and SHA-256 receipts. All 121 outer ZIP members and 51 members in three nested archival ZIPs match their extracted counterparts. Those 172 archive entries include repeated archived views, not 172 distinct on-disk files. All 126 files under sources remain byte-identical to the start-of-review inventory. The only embedded reader PDF is identical to the five-page public main PDF. Custody hashing of historical assessments did not involve reading or adopting their bodies.

## Exact claims and strongest verified result

The group is the **countable discrete restricted** wreath product
\[
W=(\bigoplus_{i\in\mathbb Z}\mathbb Z)\rtimes\mathbb Z,\qquad ta_it^{-1}=a_{i+1},
\]
with the shift character \(\chi:W\to\mathbb Z\).

1. **Theorem 1, p.1:** a dense \(G_\delta\) subset of the full Polish space of continuous \(W\)-actions on Cantor space consists of actions whose orbit equivalence relation is hyperfinite on **the entire Cantor space**.
2. **Lemma 2, p.2:** a dense \(G_\delta\) of those actions admits a continuous equivariant map to the profinite integers, with the group acting there by addition through \(\chi\). The map is surjective in this compact continuous setting. No measurable choice of the map as the action varies is required.
3. **Theorem 3, pp.3–4:** every Borel \(W\)-action on a standard Borel space which admits the specified Borel equivariant profinite-height map has a hyperfinite orbit relation on its entire domain. This conditional result allows stabilizers and does not assume freeness, minimality, an invariant probability measure, or surjectivity of the height map.
4. **Lemma 4, p.3:** each finite-width cut slab has finite Borel asymptotic dimension. The bound may depend on its width. The graph itself need not have finite connected components.

Here “generic” concerns the **space of actions** with the product compact-open homeomorphism topology. Hyperfiniteness means an increasing union of finite Borel equivalence relations on the **phase space**. The proof does not substitute a conull or comeager subset of that phase space, measured hyperfiniteness, finite-order actions, or a comeager conjugacy class.

**Exact remaining mathematical gap:** none found in these stated conclusions. The manuscript does not prove hyperfiniteness for every Borel \(W\)-action without the factor hypothesis. No such extension is adopted here.

## Independent reconstruction

The complete argument is recorded in INDEPENDENT_DERIVATION.md. The load-bearing points checked were:

- The action space is a closed Polish homomorphism space. Finite residue-map obligations are clopen, and there are countably many possible continuous residue maps. The relative fiber-product construction gives an exact action and an atomwise Cantor homeomorphism. Refining the old fibers, a small partition and inverse images of that partition controls every prescribed group element and its inverse. Countable open dense obligations support the factorial-compatible recursion.
- Slab normalization is a genuine Borel bijection even with lamp stabilizers. The conjugated lamp index is \(-r\); the excluded wrap edge is essential. The graph metric is Borel and proper in the imported finite-ball sense.
- The finite-color Borel asymptotic dimension argument uses a color count fixed for each width, with radius-dependent component bounds. Threshold chains project using only their endpoints; their connecting paths need not be monochromatic. No dimension bound uniform over widths is used.
- Divisible widths give nested graphs and decreasing old distances. This supplies the exact compatibility assumption in CJMST Theorem 7.3, rather than an unrestricted increasing-union principle for hyperfinite relations.
- The persistent factorial cut is located at profinite height −1. The proof separates the **whole invariant preimage of the embedded integers**, not just that one fiber. The preimage can be uncountable.
- On that exceptional preimage, normalization reduces orbit equivalence to the lamp action. The explicit height cutoff in the pullback of finite relations makes classes finite; omitting it would be invalid. Each specified normalized point and integer height has exactly one preimage. The two invariant pieces are then joined stage by stage.
- The prior locally finite-asymptotic-dimension theorem does not cover this finitely generated group: finite-rank lamp subgroups have the displayed undistorted \(\mathbb Z^d\) word-length bounds for arbitrarily large \(d\).

These are deductions under explicit mathematical definitions and cited established results. There are no empirical/model-fitting assumptions. The finite diagnostics supply corroborating local checks, not a substitute for the infinite argument.

## Primary bodies and interfaces

The exact fresh raw PDF versions, URLs and hashes are recorded in read-coverage.json. No scope conclusions or sibling review bodies were read.

- **CJMST, author manuscript polycyclic_v13:** read the proper extended-metric definitions; Lemma 2.2; full Lemma 3.1 proof and Definition 3.2; the Borel finite-move characterization; the polynomial-growth argument through Corollary 5.5; complete Theorem 7.3 and proof; and Corollary 7.5 with its preceding explanation. Corollary 5.5 applies to arbitrary, not only free, actions of each fixed \(\mathbb Z^m\). Theorem 7.3 permits varying finite dimensions. Corollary 7.5 applies to arbitrary Borel actions of the countable locally polynomial-growth lamp group. [Exact author-hosted body](https://math.berkeley.edu/~marks/papers/polycyclic_v13.pdf).
- **Iyer, joint with Shinko, OWR 2/2025:** read the complete contribution, printed pp.114–115, including the action-space topology, whole-space versus measured distinction, and Question 3. It is the exact historical question addressed. [Published report](https://publications.mfo.de/bitstream/handle/mfo/4296/OWR_2025_02.pdf).
- **Iyer–Shinko 2409.03078v1:** read all seven pages, including Theorems 3,18,19 and the definitions of generic actions and locally finite asymptotic dimension. [Pinned preprint](https://arxiv.org/abs/2409.03078v1).
- **Akin–Glasner–Weiss:** read Theorem 3.3 and its proof, including the conditional-compatible-lift equation (3.7), in the pinned 22 March 2006 arXiv version. This supports the credited lifting predecessor. A publisher-final 2008 body was **not** acquired; the failed author-host attempt is retained in the raw receipt, and this review does not claim publisher-byte identity. The current paper gives its own lifting proof, which was checked directly. [Inspected preprint](https://arxiv.org/abs/math/0603538v1).
- **Doucha 2211.08145v3:** read Proposition 2.12 with its proof and surrounding factor/partition conventions, especially part (3)'s all-group extension perturbation. [Pinned version](https://arxiv.org/abs/2211.08145v3).
- **Doucha–Melleray–Tsankov 2507.05474v1 and v2:** inspected the Boolean/subshift coding, Proposition 3.2 and proof, the relevant Appendix A definitions and Proposition A.7 with proof in both versions. The credited generic existential-extension realization concerns the full action coding, not solely a restricted minimal-action subspace. The direct specialization is also independently checked here. [v1](https://arxiv.org/abs/2507.05474v1), [v2](https://arxiv.org/abs/2507.05474v2).

Only these relevant portions of the longer primary works were read; no full-book/full-article coverage is implied for the other references. The OWR web-tool open failed, but its freshly acquired full PDF and hash receipt were available and inspected. Priority searches and historical firstness are not part of this analytic verdict.

## Fresh controls, then unchanged replay

Before submitted helper inspection, fresh_height_controls.py independently implemented:

- exact prefix-code homeomorphisms for compatible finite extensions of Cantor actions, preserving a prescribed initial-bit partition;
- an infinite-integer-height, nonfree action with a finite lamp quotient, including widths larger than the lamp period;
- slab coordinate inverses, conjugation signs, inactive lamps and short-path projection;
- nested divisor cuts, a noninteger compatible factorial height and 201 translated-edge admission checks;
- finite exceptional-band relations and exact class sizes;
- negative controls for the wrong conjugation sign, an uncut wrap, and nondivisible widths.

There are 36 lift cases, 80 slab cases and 26 assertion families. The run's 372,046 repeated assertions include many routine fiber-compatibility checks and are not presented as independent theorem tests. The script, results and their pre-helper completion timestamp are retained.

After reading all four submitted mathematical programs, replay_selected.py ran their **unchanged** code in a byte-authenticated copy using isolated, nonoptimized Python. Each complete numerical JSON output exactly matched its corresponding published numerical file:

| Program | Counted finite conditions |
|---|---:|
| source/author/checks.py | 97,924 |
| source/audit_bundle/audit/independent_checks.py | 20,525 |
| source/independent_review_2/independent_diagnostics.py | 53,857 |
| audits/slab/boundary_diagnostics.py | 12,349 |

The outer and inner inventory-only wrappers also passed, including the nested archive bindings. The wrappers' **--full modes were not run**: inspection showed that one explicitly parses historical ACCEPTANCE.json files and checks acceptance strings. Those assessment bodies remain unread and unadopted. The historical integrity-mutation suites were not rerun. The report therefore claims the four targeted mathematical replays and inventory checks, not the package's full historical-review pipeline. This is sufficient for the numerical corroboration used here; the theorem is independently reconstructed.

## Coverage and independence

All five actual published pages were read in text and visually, along with all 296 lines of the matching main TeX and the complete 159-line original mathematical proof. Read both current inventory/replay entry scripts and all four selected mathematical diagnostics in full. All archive inventories and byte bindings were checked. Nested archive assessment bodies, dedicated historical audit/priority/review bodies and sibling opinions remained opaque.

The main paper and necessary original proof contain prior status, review and bounded-search statements. The inspected replay wrapper contains literal historical acceptance strings. This incidental exposure is disclosed; neither those strings nor any past acceptance claim was used to reach the verdict. Numerical certificate files were machine-compared only after fresh reasoning and controls.

The programme objective was read at the start and, after the interruptions, from the active attached goal-objective.md before resuming. The completed fresh run had already exited successfully; it was preserved rather than restarted. Review ownership remained within reviews/analytic. Sources and prior sealed tasks were unchanged; no repair, publication, website, Sheet, Git, UI or outreach action occurred. No follow-up question is recommended by this analytic review.
