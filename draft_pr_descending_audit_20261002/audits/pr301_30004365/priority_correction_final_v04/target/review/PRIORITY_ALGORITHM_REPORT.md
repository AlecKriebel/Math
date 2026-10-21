# PR301 / problem30004365 — independent direct-algorithm priority audit

Audit date: 2026-10-05. Family: direct gentle-algebra numerical algorithms, workshop citation network and later implementations. Completion estimate: 95% (full accessible evidence gathered; unavailable thesis and exact PL-route priority remain unresolved).

## Verdict

**The original blanket framing as a new resolution in 2026 of the still-open numerical-computation problem is not defensible.** Before this PR, explicit constructive homology and numerical-invariant methods were public in QPA source and in Jan Geuenich's String Applet. Exact archived March 2025 applet code computes the missing genus-one gcd, genus-two parity/Arf data and all puncture end data. Its numerical step uses finite tree/cotree operations and finite quadratic-form elimination. This is substantially more than an existential classification theorem.

This verdict is about priority framing, not acceptance of a public release. It does **not** assert that every line of either prior software is correct on every gentle input. QPA contains comparison defects and possible input-construction defects; the applet has an isolated-vertex convention defect. Neither was formally certified here. The precise candidate contribution—an exhaustive rational PL search with explicit geometric certificate predicates and a halting proof—may be distinct. **Novelty of that particular route is UNKNOWN**, and no claim of earliest explicit correct certification is cleared by this audit.

The reviewed input was the exact corrected proof SHA256 `d92a870709f5ce62440fa8a83313dd13790773f247e01cfb63c43c5ae8ea272a`, together with the original TURN_1 and SOURCE_GATE from head `125d90fa3f5a4f90b813fec7a7c0f1918914d885`. No other priority family report was read before preserving independent obligations, derivations and checkpoints. The mathematical acceptance of the current proof was supplied by ROOT; this priority audit does not replace that correctness review.

## What the workshop actually requested

Plamondon's contribution in the 19–25 January 2020 workshop, printed pp.161–164 (PDF pp.19–22), asks in Problem3.4 on printed p.163 for an algorithm from the bound quiver to all numerical data of Theorem3.3. AG already supplies end/mark data, and genus is easy. The stated missing step is algorithmic gcd/parity/Arf data via handle curves. There is no efficiency, complexity or practical implementation requirement. The abbreviated workshop theorem should be read together with the complete paper's end-winding data. [Original workshop report](https://ems.press/content/serial-article-files/46842).

APS's final paper was published online 14 March 2023. Remark7.6, PDF p.27, says that their methods do not construct quiver walks for a geometric symplectic basis. This is a limitation of that paper, not a statement that no later algorithm exists. Its introduction p.5 states the same limitation. A 2021 Amiot HDR, pp.78–79, identifies QPA and Geuenich's applet as possible homes for such an algorithm and mentions a project with Francis Lazarus. The HDR predates the later implementations; its date is authenticated by the author's homepage and manuscript, not the search engine's age label. [APS](https://doi.org/10.1007/s00029-022-00822-x), [Amiot HDR](http://www-fourier.ujf-grenoble.fr/~amiot/HDR.pdf).

## Earlier papers: classification versus effectivity

LP v5, dated 27 August 2019, Theorem1.2.4 and full proof pp.8–9 classify line-field orbits by every boundary winding, genus-one gcd and genus-at-least-two parity/conditional Arf. Remark3.2.6 p.19 (journal Remark3.15) gives a local combinatorial winding recipe for cycles of its ribbon graph and says these windings suffice for every invariant. Section3.3 pp.19–20 explains passage from finite-dimensional degree-zero gentle algebras to their homologically smooth graded Koszul duals. The inspected bodies therefore remove the supposed finite-global-dimension barrier to using the graph recipe. LP alone is not being claimed here as a fully spelled-out input-to-output geometric-basis algorithm: that composition requires a constructive basis step. Lemma3.1.8 p.15 already includes zero-marked forbidden-cycle ends, with multiplicity. [LP v5](https://arxiv.org/abs/1801.06370v5).

Jin–Schroll–Wang v2, 20 March 2025, Proposition4.3 p.12 changes to a depicted standard dissection; §4.2 pp.12–15 gives numerical formulas in that form. The proposition's complete proof is geometric existence, without a finite input conversion routine. Theorem7.1 p.23 and its proofs pp.23–25 give a broader complete classification for homologically smooth graded gentle algebras. These are stronger classification results, and useful formula sources, but this audit does not silently promote the existential standard-form argument to an implemented algorithm. [JSW v2](https://arxiv.org/abs/2303.17474v2).

Opper v2, 6 February 2026, TheoremC p.3 and Theorem12.17 with full proof p.37 cover graded gentle algebras which are homologically smooth **or** proper and broader Fukaya categories. The introduction explicitly describes the LP numerical invariants as yielding an effective classification. This is important later evidence against assuming the 2023 limitation persists in 2026; the paper's full relevant bodies were read. Its contribution is broader categorical/geometric classification, rather than a new step-by-step numerical implementation. [Opper v2](https://arxiv.org/abs/2510.11543v2).

The graph-theoretic work arXiv2407.04817 was checked at its relevant numerical-invariant discussion and Corollary4.34 pp.23–24; it supplies useful derived invariants, without furnishing the complete missing invariant in that corollary. Bodin's thesis defended 15 January 2026, printed introduction p.7, cites LP/APS/Opper/JSW for complete classification; full-text search did not locate a direct algorithm or Winspeare thesis body. Neither source is used as a decisive priority theorem. [Graph model](https://arxiv.org/abs/2407.04817), [Bodin thesis](https://plamondon.pages.math.cnrs.fr/plamondon/bodin_phd.pdf).

## QPA: dated public source, constructive methods, defects

The official QPA manual §12.3 explicitly documents a marked combinatorial map, local winding computation, a nonseparating curve, handle cutting/joining, a symplectic handle basis, and `AreDerivedEquivalent(A,B)` returning a true/false answer for gentle algebras over the same field. The complete relevant method bodies were read, not just function names. [Official manual](https://gap-packages.github.io/qpa/doc/chap12.html).

Primary Git history pins addition to commit `1d22164f49a0d0b7e4376f2820da78243510e835`, 13 June 2024; a syntax bugfix pointed out by Joseph Winspeare is commit `87aee76da6cec5e29ceea4c9c8fa6bfd64d9c0b7`, 18 June 2024. These are repository history dates. The official release API and CHANGES establish inclusion in QPA1.36 released **28 May 2025**, which is an independently checkable public-release date. [Addition](https://github.com/gap-packages/qpa/commit/1d22164f49a0d0b7e4376f2820da78243510e835), [bugfix](https://github.com/gap-packages/qpa/commit/87aee76da6cec5e29ceea4c9c8fa6bfd64d9c0b7), [release1.36](https://github.com/gap-packages/qpa/releases/tag/v1.36).

Pinned current source blob is `9dc9387574b4f10824c082446867f830529fca7f`, under repository tree `6bb8746c564ccb3c4c7837659218ca417291f001`. The decoded blob's Git SHA1 was independently verified. Relevant current line locations are:

| Constructive body | Source lines | What is explicit |
|---|---:|---|
| Gentle marked map | 245–301 | Finite maximal-path/ribbon permutation construction |
| Marked boundaries | 313–338 | Visits **all** faces, including zero-marked ones |
| WindingNumber | 349–395 | Finite local cyclic-order computation |
| Boundary curves | 411–467 | All-face cycles, finite backtracking removal |
| Graph searches / nonseparating curve | 480–672 | Tree/cotree search, finite tree paths |
| Cut / join / cut-join | 687–867 | Explicit handle operations |
| Homology basis | 880–930 | Repeats a handle cut to genus zero, returns handle pairs |
| Derived comparison | 941–1105 | End winding/mark tuples, gcd, parity and Arf |

[Complete current body](https://github.com/gap-packages/qpa/blob/6bb8746c564ccb3c4c7837659218ca417291f001/lib/combinatorialmap.gi), [complete June2024 corrected body](https://github.com/gap-packages/qpa/blob/87aee76da6cec5e29ceea4c9c8fa6bfd64d9c0b7/lib/combinatorialmap.gi).

**Adversarial qualification:** current and June2024 code use `IsSubset` for boundary tuples, losing multiplicity; the B-handle parity loop instead repeats A and updates `oddA`; parity mismatch is not separately rejected before the mod4 branch. The genus formula assumes connectedness. ROOT independently raised a square-zero-loop constructor concern, not executed in this family. A native GAP runtime was unavailable here, so QPA was not replayed. Consequently its documentation is a decision-procedure claim, not a correctness certificate. The code nevertheless publishes the substantive constructive handle/homology mechanism and all numerical steps. Fixing a faulty comparator does not create that earlier mechanism for the first time.

The author-hosted applet bibliography cites Joseph Winspeare, *Algorithme de calcul d’un invariant dérivé pour les algèbres aimables*, Grenoble master's thesis, 2024. This is a primary bibliographic lead, **not a read theorem**: no complete public body was located after exact-title/author searches and the supervisor's homepage. The institutional award notice confirms spring2024 QPA contributions, and the GAP page confirms a 2025 award. Neither proves the unavailable thesis's full mathematical scope. [Bibliography](https://www.math.uni-bielefeld.de/~jgeuenich/string-applet/refs.html), [institutional notice](https://www-fourier.univ-grenoble-alpes.fr/fr/node/27723), [GAP award](https://www.gap-system.org/award/).

## String Applet: exact historical implementation and successful replay

The live author-hosted applet labels its displayed values a complete derived invariant. More decisively, the exact **21 March 2025, 11:18:07 UTC** archived main/vendor bytes contain the finite `surfaceHomologyBasis`, winding, intersection, gcd, parity and Arf bodies. Memento and original Last-Modified headers are retained. The current main was last modified 21 June 2025, but the archived methods already exist in March. The author's 2017–2020 appointment and ©2020 footer do not date this feature. The 2022 capture lacks these methods; this is evidence of absence in that snapshot, not proof of their earliest creation date. [Applet](https://www.math.uni-bielefeld.de/~jgeuenich/string-applet/), [raw archived main](https://web.archive.org/web/20250321111807id_/https://www.math.uni-bielefeld.de/~jgeuenich/string-applet/main.bundle.js), [raw archived vendor](https://web.archive.org/web/20250321111807id_/https://www.math.uni-bielefeld.de/~jgeuenich/string-applet/vendors.bundle.js).

Archived decoded-main SHA256: `99a8209e6f54b3f24ad68b463e0a5ae83fc4487af8481b76a38271dff83644ba`. `APPLET_METHOD_INDEX.json` pins complete method bodies and their UTF8 byte ranges. Notable ranges (end exclusive): all-end AG 123586–124057; gcd124229–124393; parity124394–124611; Arf124612–125778; end windings125779–125895; basis126194–126539; dual graph126865–127354.

The algorithm deletes the dual spanning-tree edges, takes a primal spanning tree, and uses the remaining edge/tree-path cycles as a basis of capped first homology. It computes local signed windings and intersections, then forms the F2 quadratic matrix and eliminates symplectic pairs. All zero-marked forbidden cycles are inserted in AG before alternating-thread ends. `DERIVATION_DIRECT_METHOD.md` separately proves why this conditional numerical mechanism is finite and sufficient; it does not assume mere theorem existence solves a basis problem.

Canonical offline replays used pinned bytes, blocked every network request, and changed only wrappers to expose classes, skip UI, set public path and stub MathJax. Numerical method bodies were untouched. The successful historical replay computes fifteen original gentle examples, followed by four adversarial edge fixtures:

| Historical fixture | Output relevant to the missing algorithm |
|---|---|
| APS Examples1/2, genus1 | gcd0 / gcd2 |
| APS Examples3/4, genus1 with puncture | AG includes (0,3); gcd1 / gcd1 |
| APS Surface Cut0/1/2, genus2 | Arf1 / Arf0 / Arf0 |
| Win24 Example2, genus2 | odd handle data; parity1 |
| k[a]/(a²) | Annulus data (0,1),(1,0), end windings -1,1 |
| A(3,5) | (0,3),(0,5),(7,1), end windings -3,-5,6 |
| A(4,4) | (0,4),(0,4),(7,1), end windings -4,-4,6 |

The A(m,n) fixtures are exactly the candidate's puncture-deficiency witness, independently entered as two full-relation cycles and an unrelated bridge. Thus that distinction is already produced by the historical implementation. However, isolated k returned genus0 and empty AG/end lists, omitting its disk boundary. This is an actual software edge defect. These replays are bounded evidence, not universal executable certification; the successful main numerical mechanism is separate from that caveat.

Full historical outputs are `APPLET_HISTORICAL_REPLAY_RESULTS.json` and `APPLET_HISTORICAL_EDGE_RESULTS.json`. Native cell PIDs were50076 and50947; requests, start/end UTC, exit0 and untruncated stdout/stderr are retained. Early failures are also retained: missing MathJax, then an audit-harness conversion mistake causing caught invalid-relation errors. The corrected harness creates actual Quiver objects before the unchanged Algebra constructor.

## Puncture correction and legitimate contribution

APS Remark6.2, final PDF p.21, already explicitly gives every end pair (n_j,n_j-w(c_j)), j=1..b+p, as the AG invariant. LP Lemma3.1.8 gives the corresponding all-combinatorial-boundary statement. The final APS Theorem7.4(2), PDF p.24, nevertheless restricts the winding equality to j<=b. The current publisher HTML retains this defect; the inspected searches did not find a separate published erratum. [APS current text](https://link.springer.com/article/10.1007/s00029-022-00822-x).

Therefore the all-end numerical data and their importance are **not a new invariant**. An explicit counterexample to the printed index range, and a careful compact-core deduction repairing that range, could be a legitimate explanatory/corrective result. Priority for that particular counterexample or explicit erratum argument is **UNKNOWN**; absence of a located erratum is not proof of first discovery.

Legitimate framing would be: an explicit certificate-based effectivity proof for computing the known complete gentle derived invariant, with a correction of a puncture index range and independently checkable finite constructions. It must cite LP/APS and the existing direct numerical methods/implementations, identify whether its geometric certificates or proof organization offer a benefit, and distinguish proven termination from an implemented full search. It should not say the invariant itself is new, that its theoretical search is a new practical implementation, or that the 2020 problem remained unaddressed through2026. A title such as **“A certificate-based effectivity proof for the complete derived invariant of gentle algebras”** makes the verified contribution reviewable without asserting first resolution.

## Strongest verified result and exact gaps

Verified: correct pinned input; actual workshop scope; complete relevant prior theorem/method bodies; dated public numerical implementations; exact historical replay of every difficult numerical case plus puncture witness; conditional constructive sufficiency derivation; software caveats preserved.

Unresolved: full Win24 thesis body/date/scope; formal universal verification of prior complete software (known defects make an unconditional assertion false); earliest introduction of applet features; priority of the specific exhaustive PL certificate route; priority of the explicit puncture-range counterexample/correction. None of these gaps supports restoring blanket first-algorithm novelty.

No Git, index, branch, PR, publication service, sheet or external-contact mutation was made. All artifacts were written only within this family's assigned folder. Complete fetch/decode/replay evidence, source pins and failed attempts are retained; ordinary light reads/search tools did not supply native PIDs and are identified accordingly. Final hashes and byte-cap check are in `EVIDENCE_MANIFEST.json` / the verification output.
