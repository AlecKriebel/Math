# Independent mathematical acceptance: restricted soccer-score results

Date: 2026-10-11. Target: complete-host 3–1–0 full-vector recognition, problem 3000026 / AMR-029-0026.

This AI-assisted manuscript is unrefereed. Acceptance refers to an internal AI mathematical audit, not external human peer review, journal acceptance, or formal proof-assistant certification. This is not a computational reproduction package. Novelty and priority are unestablished; no exhaustive current-openness claim is made.

## Verdict and boundaries

**ACCEPTED as partial results:** the fixed-draw-graph criterion; the decisive-match parameter and incidence-budget kernel; the stated exact FPT algorithm; the small-parameter classifications; the labeled-coordinate convex-hull obstruction; and the narrow correction of the printed 2017 Theorem 9.

**NOT a solution of the original unrestricted recognition-complexity problem.** This audit establishes neither a polynomial-time algorithm for all complete-host instances nor a complete-host hardness reduction. It does not certify current worldwide openness, novelty, or priority. The general-host and elimination hardness results are not substitutions for the specified target.

The audited candidate is the immutable packet whose manifest SHA-256 is `8d645a11fbdb020381a54b89ea37bb9e8bf772d9876ba841510eb311b917742a`. Its mathematical report hash is `87b09f880bd5f42a87d43228b701589acf8705ebdbdeb54fbf57ceee5346c332`; its correction-note hash is `16c8d0f38f66ecf5aed02d648ee4fb78fe5448fda91848433501f4b1463fa848`. The candidate's historical statements that no independent audit had yet accepted it remain accurate descriptions of its pre-audit state; this separate document supplies the later acceptance without altering that sealed packet.

No candidate mathematical correction was required. One interpretation boundary is worth making explicit: the convexity claim concerns all labeled score vectors in a fixed coordinate space and pure continuous linear feasibility/projection. It does not claim that preprocessing by sorting or other nonlinear operations is itself a linear projection, or exclude arbitrary Boolean combinations of inequalities.

## 1. Exact model and global accounting

The problem includes one integer score per team, at least one team, and exactly one match between each unordered pair. Permitted ordered contributions are (3,0), (0,3), and (1,1). The relevant host is the complete graph. A certificate specifies one legal outcome per pair. Arbitrary-host partial-orientation problems and tournaments with preassigned match outcomes are distinct inputs.

For N=n(n−1)/2 games, if m are decisive and k are draws, then S=3m+2k and N=m+k. Solving gives m=S−n(n−1) and k=3N−S. Hence the report's total-score bounds are necessary. They are not sufficient: (1,4,4) has an allowed total and allowed individual scores but cannot occur.

The n=1 case has N=m=k=0 and the sole legal vector (0). Noninteger entries, negative entries, or entries above 3(n−1) are excluded before using the reduction. The candidate code also deliberately rejects Python Boolean values. No n=0 convention is claimed or needed.

## 2. Fixed draws and integral orientation

Fix a simple draw graph D and write H=K_n−D. The points obtained from draws at team i are d_i=deg_D(i); the remaining points must be 3w_i. Therefore each quota w_i=(s_i−d_i)/3 must be an integer between zero and deg_H(i), and the quota total must be |E(H)|.

The subset inequalities are necessary because every decisive edge with both ends in U chooses its winner in U. For sufficiency, replace team i by w_i slots. A decisive edge is a left-side matching object adjacent to every slot of its two endpoints. For an arbitrary set A of edge objects, let U be the union of their endpoints. Every member of A lies in H[U], so

|A| ≤ |E(H[U])| ≤ sum_{i in U} w_i.

The last quantity is exactly the number of neighboring slots, including the harmless case of endpoints with zero slots. This is Hall's condition for every edge-object set. A full matching exists. Since the slot total equals the edge count, every team's slots are filled exactly, giving its prescribed win quota. A standard integral unit-capacity flow implements the matching in polynomial time. The candidate's residual-capacity winner extraction correctly identifies the unique used endpoint for each edge node.

For the alternate inequality, sum_{i in U} d_i=2e_D(U)+c_D(U), while |E(H[U])|=binom(|U|,2)−e_D(U). Substitution gives precisely s(U)+e_D(U)−c_D(U)≥3binom(|U|,2), with the signs printed in the report.

The empty subset, the full subset, the empty decisive graph, zero-win teams, and saturated-win teams introduce no missing cases. The total condition is separately present. Enumerating binom(N,k) draw graphs followed by flow is XP in k, not the stated FPT result in m and not an input-polynomial solution.

The (1,1,7,7) example is correctly credited to Iványi–Schoenfield, printed p. 167. Draws 12 and 34 allow the two 7-point teams to defeat both 1-point teams; draws 14 and 23 leave a required decisive game between two teams with zero win quota. The latter passes the local degree, divisibility, and total tests but fails the subset constraint for teams 1 and 2. This is an actual obstruction, not a hypothetical failure of a particular implementation.

## 3. Kernel proof and reconstruction

Relative to the all-draw baseline, a decisive win changes a team's score by +2 and a loss by −1. Thus delta_i=s_i−(n−1)=2w_i−l_i and sum_i delta_i=m.

For fixed nonzero integer t, the nonnegative integer solutions satisfy l=2w−t and total incidence w+l=3w−t. The minimum occurs at w=max(0,ceil(t/2)). This yields −t for negative t, t/2 for positive even t, and (t+3)/2 for positive odd t. These are exactly the report's h(t). The formula is a lower bound even when a particular local choice would be disallowed by a small host; the later range/realizability tests handle those additional restrictions.

For t=0, any active vertex has w≥1 and l=2w, hence degree at least three. If Q is the set of nonzero deviations and B is the sum of their minimum incidences, total degree 2m permits at most floor((2m−B)/3) active zero-deviation teams. B>2m is therefore a safe rejection. If m=0, all games must be draws; the algorithm correctly accepts only the all-zero deviation vector rather than every vector summing to zero.

Let a be the smaller of the available zero-deviation count and the incidence bound. Keep all of Q and any a neutral labels. All neutral labels have the same required score n−1. Therefore a permutation among them preserves the labeled input score vector, and can move every active neutral team into the retained set. Every deleted team can then be made isolated in the decisive graph, which means it drew every match, including matches with other deleted teams.

Removing r such teams subtracts exactly r from each retained score. Conversely, add r teams and declare every new match a draw. A retained team gains r points, and each added team gets n−1 points. The reverse operation reconstructs the original vector exactly. Thus the reduction is an equivalence, not merely a necessary filter. Rejecting an out-of-range reduced score is justified by this equivalence.

Every nonzero h(t) is at least one. Consequently q+a≤B+3a≤2m. The reduced deviations equal the original retained deviations because both the score and baseline decrease by r; the removed deviations are zero. Hence m is preserved. For m≥1 there must be a nonzero deviation, so no erroneous empty-vector convention enters this branch. Retained individual scores are bounded by 3(2m−1), giving O(m log(m+1)) bits. Terminal yes/no answers may equivalently be represented by fixed constant-sized instances.

The ability to retain active neutral vertices matters. The vector (2,3,5,5) has a neutral 3-point team with one win and two losses in its realization. Deleting that team would produce (1,4,4), impossible by the all-decisive/multiple-of-three argument. The sharper budget retains it: m=3, B=3, and a=1. A mutation that deletes all neutral teams is detected by this concrete positive case. The score-shift mutation is separately detected by a padded one-decisive-game instance.

The support bound is sharp for reductions restricted to deleting all-draw teams while preserving nonzero deviations. m disjoint decisive games produce m deviations +2 and m deviations −1, all requiring distinct retained labels. This is the stated restricted sharpness, not a universal lower bound on every possible parameterized reduction.

## 4. FPT enumeration, small m, and convexity

After reduction there are r'≤2m vertices. Enumerating each m-edge simple subgraph and each orientation covers every possible decisive graph exactly within that support. It excludes loops and reciprocal pairs. Comparing all deviations is sufficient, and adding draws on absent edges returns a complete legal schedule. If m>binom(r',2), the search correctly has no candidate. The code's lifted certificate swaps endpoint scores when the retained-label order differs from the original labels; independent labeled tests validate this case.

With M=binom(2m,2)=m(2m−1), the candidate count is binom(M,m)2^m≤(eM/m)^m2^m≤(4em)^m for m≥1. A polynomial evaluation cost and polynomial-time reduction preserve 2^{O(m log(m+1))} times input-polynomial running time. Explicit output of the n-team schedule costs only O(n²), also polynomial in input length. The zero-parameter case is handled separately. Dense instances can have m=Theta(n²), so this theorem gives no general polynomial-time resolution.

For one decisive edge the nonzero deviations are (−1,2). For two distinct decisive edges the underlying graph is either a matching or two adjacent edges. The matching gives (−1,−1,2,2); the three orientation types for the adjacent edges give (−1,−1,4), (−2,2,2), and (−1,1,2). No active neutral vertex can occur with only two edges. The converse constructions and addition of all-draw teams prove the complete m≤2 list, subject to enough teams to contain its entries.

The impossible vector (n,n−1,...,n−1) has m=1 and deviation support (1), contradicting the one-edge pattern. Let x and y have all draws except opposite decisive outcomes on game 12. Their first two coordinates are respectively (n+1,n−2) and (n−2,n+1); all other coordinates are n−1. Their weighted average (2x+y)/3 is exactly the impossible integer vector. This remains valid at n=2. Any convex feasible set containing every labeled feasible vector must contain this hole, as must every continuous projection of a linear system. This does not rule out integer auxiliary variables, nonlinear preprocessing/tests, sorting followed by other algorithms, or polynomial combinatorial recognition.

## 5. Published Theorem 9: source and quantifiers

The source is S. Pirzada, U. Samee, and T. A. Naikoo, [Tournaments, oriented graphs and football sequences](https://emis.de/ft/40409), Acta Universitatis Sapientiae, Mathematica 9(1) (2017), 213–223, DOI [10.1515/ausm-2017-0014](https://doi.org/10.1515/ausm-2017-0014). The inspected contribution has a printed journal citation and DOI. It is not treated as an unpublished manuscript based on a PDF's later modification or crawler timestamp.

I independently opened the 11-page EMIS article, read the score and graph definitions, and inspected the statement and complete proof on printed pp. 220–221. I also read the corresponding retained journal-issue extraction and visually inspected printed pp. 219, 220, and 221. Page 219 defines transmitter through zero indegree, so it means a team with no losses, regardless of whether it draws. Page 220 uses a vertex in a given oriented graph; its sufficient hypothesis is redundant parity information. It does not quantify over an unspecified alternative graph realizing only the scalar score. Its proof assumes that the vertex is already a transmitter, and derives parity. Thus the direction mismatch is present in the actual published typesetting and is not an OCR inference.

The four-team schedule in the correction note yields A=3, B=2, C=D=5. A has one win and two losses, so it is not a transmitter, while n=4 and score 3 satisfy all the printed parity conditions. This alone refutes the literal sufficient implication.

The fixed-vector strengthening is also valid. An undefeated 3-point team among four teams has score 3+2w, so w=0 and all its games are draws. Removing it leaves (1,4,4). The remaining total 9 is the maximum for three games, requiring every game decisive. All scores must then be multiples of three, contradiction. The independently enumerated unique labeled realization is additional evidence; the short argument already proves the assertion.

The identity l_i≡n−1−f_i (mod 2) gives the correct statement: same parity of f_i and n forces an odd positive loss count; different parity permits an even loss count, including zero or two. A transmitter has f_i=n−1+2w_i and scalar score in {n−1,n+1,...,3(n−1)}. Conversely each scalar in that list is attainable by choosing that team's wins and draws and freely completing the other matches. This scalar-existence fact does not repair the printed claim for a prescribed graph or full vector. The counterexample even uses a scalar inside that attainable list.

The replacement's win/draw formulas use nonnegative integers, including the all-draw and all-win endpoints; the paper's proof uses a strictly positive description that is not valid at those endpoints. The correction remains narrow: it does not reject the paper as a whole, its earlier theorems, or its valid necessary parity direction. Neither paper-wide correctness nor other apparent typographical issues were audited.

## 6. Source scope, prior credit, and reproducible checks

The complete 272-page issue was previously retrieved from the [Hungarian Academy repository](https://real-j.mtak.hu/23015/1/Acta%20Mathematica%209_1_2017.pdf); its retained bytes independently rehash to `5441a2815f801eddd70b72ad19fe0163d1e46591717c7665444c05511193d749`, length 6,675,078. This audit does not claim to have read the whole issue or every proof in the 11-page contribution. Opening the separate EMIS article does not establish byte identity between hosts; only agreement of the inspected statement/definitions is asserted.

The source evidence was byte-authenticated before use; this does not constitute a full-reading claim. The original Egres statement and its complete-host versus prescribed-results distinction were read. In the 2012 Iványi–Schoenfield arXiv v1 journal-formatted paper, I read the title/abstract/model introduction and printed pp. 167–168 around the exact draw-pairing example; the full algorithm collection was not audited. The inspected Pálvölgyi author manuscript's abstract and pp. 1–2 explicitly supply the graph of played matches, validating the scope distinction without auditing its reduction.

The score identity, graph-orientation matching/flow argument, and specific (1,1,7,7) obstruction must not receive new-priority claims here. The kernel and correction are self-contained authored deductions with unestablished novelty. Independent bounded searches for the title with correction/erratum and relevant kernel/parameter terms located no matching correction or kernel result, but sparse search coverage and terminology variation prevent any absence or priority certificate.

Both authored candidate Python files and their integrity verifiers were read before execution. No scholarly-source program was executed. An independently written enumerator uses a different outcome ordering and direct score/loss accumulation, with its own complete-schedule checker and separately implemented incidence minimization. It reproduces the following in normal, -O, and -OO Python:

- 59,809 match assignments across n=1,...,5 and 298,249 individual team balance/parity checks.
- All 6,998 sorted in-range inputs through n=5: 405 positive, 6,593 negative; feasible counts 1, 2, 7, 40, 355.
- All 10,360 labeled in-range inputs through n=4, checked against both candidate recognizers, including negative labeled inputs.
- All 3,194 simple-host quota inputs through n=4, checked against independent orientation enumeration, subset inequalities, and candidate flow.
- All 4,091 six-team sparse decisive assignments with m≤3, yielding an oracle for 3,967 sorted in-range inputs in those parameter slices. The feasible-vector counts by m=0,1,2,3 are 1,1,4,14.
- 135 padded/permuted positive inputs, convex holes for every n=2,...,100, local-incidence minima for deviations −30,...,30, and support-sharpness fixtures m=1,...,6.
- The counterexample's unique labeled realization and two losses at its 3-point vertex.
- Nine actual semantic corruption controls: all-neutral deletion, omitted shift, parity sufficiency, local-quota-only acceptance, reciprocal decisive edges, total-and-range-only acceptance, and three malformed schedule types.

The candidate's own mathematical suite, closed-inventory verifier, and eleven actual corrupted-inventory controls were independently rerun under all three optimization modes. Explicit failure guards remain active under optimization. These finite checks support the reviewed proofs; they do not extrapolate finite enumeration into a proof of the unrestricted recognition problem.

## 7. Evidence integrity and distribution scope

The original closed audit inventory pins all 22 retained audit members and relevant inputs. A separate external seal pins the audit manifest. The creator's closed 27-member inventory is separately authenticated. Reverification and deliberately corrupted-copy controls were recorded outside those closed trees. VERIFICATION.json records their byte identities and separates historical mathematical checks from the checks made when preparing this edition.

The complete mathematical review and source-inspection qualifications above are retained. Only authored mathematical prose and eligible verification/source metadata are distributed here. Programs, raw scans, datasets, copied sources and source images are excluded. The six-game counterexample and the all-realizations contradiction are essential mathematical proof content, retained in PROOF.md. Neither a hash nor an internal acceptance report constitutes publication permission or external peer review.

This edition adds no mathematical computation, source-body inspection, or literature survey. The full unrestricted recognition question remains unresolved by this work.
