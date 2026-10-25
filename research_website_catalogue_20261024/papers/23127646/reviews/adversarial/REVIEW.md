# Independent adversarial review — Zenodo 23127646

**Verdict: PASS for the stated mathematical claims. No substantive defect found.** The universal rational-boundary formula and its deduction of non-symmetry survive independent reconstruction and attempts to break the finite-graph, positivity, grouping, and blow-up assumptions. This is an AI mathematical review, not external human peer review or a certification of historical priority.

Paper: *Non-symmetry of biconstrained two-step reachability*, version 1.0, October 3, 2026, DOI https://doi.org/10.5281/zenodo.23127646. Inventory row 49. Review completed 2026-10-25 UTC.

## Exact publication binding and coverage

The four-page main PDF has SHA-256 `35ddcd2a64bf0906fadcf762b913dfd9369941784ca0da87d97a3e9080ea80e4`, MD5 `82911cd471138ea4c5c40d2ba0747634`, and 67359 bytes. The verification ZIP has SHA-256 `5415f48f702ab2e234376b73c4853043b1b7601316392ff4750123eb66339d81`, MD5 `75a0dfae581142f858d6c2455e14dbf1`, and 198015 bytes. Both fresh assets were independently rehashed; `source_pins.json` preserves the acquisition receipt.

Read all four PDF pages, rendered and visually inspected all four, and read the full corresponding TeX. Read all three original mathematical proof records (`TURN_1.md`, `TURN_2.md`, `TURN_3.md`), the six mathematical programs executed by the portable package, the launcher, and the usage README. Hashes and exact paths of these twelve reviewed support files are in `reviewed_mathematical_sources.json`. The full main proof is self-contained; no unseen mathematical theorem is delegated to a historical report.

Dedicated historical audits, review verdicts, priority reports, disposition files, and status logs were kept opaque. Their bytes were read by the package's hash verifier, but their opinions were not read or used by this reviewer. Necessary proof records and the README contain incidental author progress assertions and statements about past AI reviews; these were treated as claims. The single historical `reference/review/check_independent.py` file was read as an executable mathematical checker required by the portable replay, not as a verdict. No sibling review findings or code were consulted.

## Independence and falsification sequence

Before reading supplied mathematical helpers, I reconstructed both main proofs from the actual paper and wrote a fresh ordinary-vertex graph checker. The independent provisional no-defect conclusion was saved as `independent_preliminary_conclusion.json` before helper and historical proof-record inspection. Primary source paths were supplied by the scope agent without conclusions; the cited definitions, question, and figure were inspected independently.

The fresh control uses bitset neighborhoods on actual individual vertices, rather than importing the submitted incidence/weight checker. It exhausts complete finite classes of small graphs and reconstructs the two explicit graphs, so it tests path existence and distinct reached vertices directly. The zero-middle-weight control deliberately violates an assumption to demonstrate that the proof's positivity condition has real content.

## Claims and precise domain

For nonempty finite stable parts A,B,C, with only adjacent-part edges, an (x,y)-biconstrained graph has **all four** minimum-degree conditions: A→B and B→A at relative threshold x, B→C and C→B at threshold y. The function is

`psi(x,y) = inf_G max_{c in C} |{a in A : N_B(a) intersects N_B(c)}|/|A|`.

The infimum is over all eligible finite graphs and all positive part sizes. It counts distinct reached A vertices, not paths. Equivalently, it is the greatest lower bound guaranteed for at least one C vertex in every graph. Attainment is not assumed.

Theorem 2, pages 2–3, asserts for every **rational** theta in (0,1):

`psi(1-theta,theta) = 1-theta/d(theta)`,

with finite attainment. The integer d(theta) is the minimum maximum **unweighted row degree** of a binary incidence matrix with distinct columns, positive rational probability vectors b,q, and `Mq=theta*1`, `M^T b=theta*1`. Rows may repeat. It is not a minimum weighted row sum: those weighted row sums are already fixed at theta.

Theorem 1, page 1 and deduction on page 3, asserts

`|psi(13/27,14/27)-psi(14/27,13/27)| >= 1/108`.

The paper does not evaluate d(13/27), d(14/27), either exact psi value, or their ordering. It does not infer asymmetry merely from two unequal upper-bound examples. It does not transfer the known symmetry of the one-direction function phi to psi.

## Universal lower bound: adversarial reconstruction

Fix any finite boundary graph and write `F=max_c reach(c)/|A|`. The F=1 case already satisfies the claimed lower bound. If F<1, each c misses at least one a. Their middle neighborhoods are disjoint; their respective minimum sizes theta|B| and (1−theta)|B| add to |B|. Therefore both bounds are equalities and the neighborhoods partition B.

This argument applies to **every** c, because F<1 is a maximum condition. Hence each C vertex has exactly theta|B| neighbors. Counting B–C edges and using every B vertex's lower bound theta|C| then forces exact regularity in the reverse direction too. In particular, if theta|B| or theta|C| cannot be an integer, no nonfull case exists; the argument does not round equality claims.

Group C vertices by their distinct neighborhoods T_i. Uniform positive weights on B and positive class proportions on C give an eligible incidence template. Duplicate actual C vertices are grouped before the unweighted degree Delta is counted. The A vertices missed by any member of class i are exactly those with neighborhood B\T_i: a proper subset of that complement would violate their minimum degree. The classes A_i are nonempty and pairwise disjoint.

Let `p_i=|A_i|/|A|` and `t=min_i p_i`. Then F=1−t. At a middle vertex v, all A_i with v in T_i are nonneighbors, so `sum_{i:v in T_i}p_i<=theta`. Taking a row of maximum distinct-column degree gives `t*Delta<=theta`. Since `Delta>=d(theta)`,

`F >= 1-theta/Delta >= 1-theta/d(theta)`.

Additional A vertices outside all these classes are not removed or renormalized: they may add nonneighbors, which only strengthens the row budget. There is no minimizer assumption or exchange of a minimum with an infimum in this step.

## Integer minimum and finite upper construction

For theta=p/r in lowest terms, 0<p<r, the r cyclic intervals of length p give a finite regular template with uniform positive rational weights, distinct columns and Delta=p. Thus the set of admissible integer degrees is nonempty and contained in positive integers; its least member is actually represented by one of its defining finite templates. This well-ordering argument does not require compactness of the space of all graphs.

For a minimizing template with n columns and degree d, every support T_i has b-weight theta. Strictly positive b and distinct columns force pairwise incomparability. Set `t=theta/d`, `delta=1-n*t`. Summing support weights yields `n*theta=sum_v b_v deg(v)<=d`, so delta≥0.

Assign each A type a_i weight t and neighborhood B\T_i; add a universal A type of weight delta precisely when delta>0. Retain B weights b and C weights q. A→B is at least 1−theta; B→A is `1-t*deg(v)>=1-theta`; both B–C directions are exactly theta. For c_i, only a_i is missed: for j≠i, a middle vertex in T_i\T_j is a surviving path to a_j. The universal type is reached because theta>0. Every C type therefore reaches exactly weight 1−t.

Every retained type has positive rational weight. Taking a common denominator **within each part** yields positive integer copies of each type and complete or empty type-pair adjacency. Unequal denominators across parts cause no difficulty: relative degrees are normalized within the relevant neighbor part. Each middle type survives, so Boolean path existence is preserved exactly. The graph is simple, finite, and has nonempty parts; zero residual mass is omitted rather than represented by a fictitious vertex. This proves attainment and the upper bound.

The endpoints theta=0,1 are excluded and are not silently handled by this construction. The source proof record's additional irrational-boundary observation is consistent: F<1 would require the irrational theta times the nonzero integer |B| to be an integer, so every finite graph has F=1. That observation is not needed for either main theorem.

## Non-symmetry and source construction

The displayed 7×7 matrix has row degrees (4,4,3,3,3,3,3), positive weights b=(5,5,3,3,3,4,4)/27 and q=(4,4,3,3,3,5,5)/27, and weighted row and column sums 13/27. Its complement has degrees (3,3,4,4,4,4,4), weighted sums 14/27 and distinct columns. Thus both integer minima lie in {1,2,3,4}. The upper construction can use these templates even without knowing whether either minimizes d.

The boundary formula places the two universal values in the respective finite sets `1-13/(27d)` and `1-14/(27e)`. Equality requires 13e=14d, impossible in the stated integer range. All sixteen exact gaps have minimum 1/108, occurring only at d=e=4 among those candidate pairs. Excluding additional impossible integer values could only strengthen this argument; no such exclusion is needed.

The ordinary first example has part sizes (108,27,27), four relative minimum degrees (14/27,14/27,13/27,13/27), and every C vertex reaches exactly 95 A vertices. The complement example has the same part sizes, relative minima (13/27,13/27,14/27,14/27), and every C vertex reaches exactly 94 A vertices. These establish upper bounds 95/108 and 47/54, not exact values. The manuscript makes this distinction explicitly.

## Fresh exact controls

`fresh_graph_controls.py` and `fresh_graph_results.json` record **893** exact checks with no submitted code imported:

- Literal construction of both 162-vertex graphs and all four degree directions; reachability computed by intersection of actual middle-vertex neighborhoods.
- A rational split of one middle type into two repeated rows with unequal positive weights, giving part sizes (108,81,27) and the same reach fraction; this tests independent part denominators and repeated rows.
- Every reduced rational cyclic template p/r with 2≤r≤9, verifying regularity, distinct/incomparable columns, zero residual mass and the resulting graph fractions.
- All sixteen possible integer gap values, with exact minimum 1/108.
- Exhaustion of **25,527** admissible labeled graphs across six part-size triples and theta∈{1/3,1/2,2/3}. The **88** F<1 cases satisfy the exact-degree rigidity, complementary missing classes, disjointness, row budget and integer-degree lower bound. **12** cases have A vertices outside the missing classes, so the extra-mass test is nonvacuous.
- A deliberately invalid zero-middle-weight template still satisfying the weighted regularity equations. Distinct nested supports become indistinguishable after zero-weight deletion; the literal reach fraction is 1/2 instead of the invalid prediction 3/4. This confirms why the published strict positivity assumption cannot be discarded.

Finite graph tests corroborate the universal proof; they do not enumerate psi or determine d. The initial reviewer implementation used the minimal A denominator 54 for the complementary example; it was then doubled to reproduce the paper's explicitly chosen 108 A copies. An initial small-size census had no extra-A cases; adding (3,2,2) made that control nonvacuous. These were reviewer-control adjustments, not defects or repairs to published sources.

## Published replay and supplementary mathematical claims

The portable package was copied unchanged into an ignored private replay directory and run with Python 3.14, normal assertion mode and bytecode disabled. It returned 0, empty stderr, reproduced the entire expected stdout of all six programs, checked the public inventory and 135 nested manifest instances, and reported no writes. The six arithmetic/bookkeeping counts sum to **169,232**. Full stdout and a fresh receipt are retained. These counts are not independent proofs.

The three original proof records were checked as mathematics:

1. The rational cofinal reduction uses a near-optimal finite graph's actual rational minimum degrees and monotonicity, not continuity. The sampling lemma conditions on endpoints, controls four degree and two reach families, and uses a valid union bound `6n exp(-2n epsilon²)<1`; sampled paths are a subset of original reachability. Its finite-table sandwich retains the stated degree slack.
2. The fixed-pattern LP factorization correctly retains the coupled middle feasibility polytope. Positive-support infima follow by mixing with a strictly positive feasible point. The displayed dual inequalities have the correct direction; the family has different fixed-pattern forward/reverse optima but equal universal psi values. The records explicitly avoid turning that into a symmetry counterexample.
3. The boundary proof agrees with the main manuscript. Positive real regular solutions can be rationalized on the same support because the defining affine systems have rational coefficients and strict positivity is relatively open. The optional irrational-boundary observation and the two concrete graph counts are consistent.

Dedicated repository-oriented audit verifiers requiring private evidence were not run, and their historical judgments were not adopted. The portable verification claims are limited to the files and checks it actually executes. There is no need to assume inaccessible audit artifacts for the main universal proof.

## Primary-source comparison

Fresh raw primary sources were supplied by the scope reviewer without findings, then rehashed and independently read; identities are in `primary_source_pins.json`.

- Seymour, Oberwolfach Report 1/2019, printed pages 46–47, explicitly adds the two reverse degree conditions and asks whether psi is symmetric. The model and question match. Official PDF: https://ems.press/content/serial-article-files/46780 .
- Chudnovsky–Hompe–Scott–Seymour–Spirkl, *Concatenating Bipartite Graphs*, EJC 29(2) (2022), #P2.47: definitions on pages 5–6 match; Theorem 2.3 and the subsequent remark concern phi symmetry and an unresolved psi analogue; Theorem 12.2 on page 72 concerns only the minimal-value regime `psi(x,y)=x`. It does not establish general symmetry. Figure 1 on page 6 was visually traced: its upper bipartite block and weights match the credited matrix. The regular example discussion is on page 71. Official article: https://www.combinatorics.org/ojs/index.php/eljc/article/view/v29i2p47 ; official PDF: https://www.combinatorics.org/ojs/index.php/eljc/article/download/v29i2p47/pdf/ .

The published proof does not depend on a disputed optimizer theorem or imported large computational classification. Earlier weighted-graph and matrix constructions are credited. I did not independently exhaust later literature, the inaccessible senior thesis, or every possible antecedent, so historical originality remains outside this mathematical PASS.

## Strongest verified conclusion and exact remaining limitations

Theorem 2 is justified for every rational theta∈(0,1), including the asserted finite attainment, and the given templates imply Theorem 1's universal absolute gap ≥1/108 under the original biconstrained definition. No remaining mathematical gap was identified in these stated claims or their necessary support.

The invariant minima, exact values, sign of the asymmetry, and global novelty are not determined. No claim that the examples themselves are extremizers is licensed. No source edits, repairs, website or spreadsheet changes, Git actions, publication actions, or external outreach were performed. Review completion is 100% for the assigned bounded mathematical validation, not a statement that AI review replaces human peer review.
