# PR108: independent all-spanning-tree threshold adversarial audit

The submitted mathematical proof passes this audit. It establishes strong NP-completeness of the explicit nonnegative-integer decision problem, and therefore the NP-hardness requested by literal Problem 1 in Volker Kaibel's contribution. No substantive mathematical repair is required. The audit establishes validity of the reduction, not priority or novelty.

## Scope, source and independence

Audited target: problem 30003996 / OWR-16633-013, original head label `3526d46bf143b08e5055ffa7728c6278e9f958ea`. `INPUT_MANIFEST.json` pins exact bytes and SHA256 values of the supplied original-attempt source record, source manifest, candidate proof, candidate prose research log, and local primary-source inputs. Commit authentication itself belongs to the parent's source-custody procedure; this audit verifies unchanged pinned artifact bytes.

I read the entire Kaibel contribution, printed pp. 3014-3015 / PDF pp. 46-47 of [Oberwolfach Report 50/2018](https://ems.press/content/serial-article-files/46772). Problem 1 assigns a cost vector to each vertex on both directed copies of every undirected edge and sums costs of the root-induced orientation of the whole spanning tree over all roots. Problem 2 uses destination-specific path costs in one fixed-root directed tree, and is a distinct problem. The source's Martin/Wong formulation motivations are not assumptions used in this reduction. The candidate matches Problem 1 literally. Source orientation convention is neutralized by reversing every arc entry if inward arborescences are intended.

The independent universal reconstruction was frozen at 2026-10-06T04:47:44.820905Z, before reading any author checker, old review, or other audit. None was read subsequently. `INDEPENDENT_RECONSTRUCTION.md` and `FREEZE_RECEIPT.json` preserve that reconstruction and its checksum. The finite checker was written from the graph and cost definitions, with direct traversals from every root. The only imported complexity theorem is NP-completeness of at-most-three-literals-per-clause SAT: the local Karp primary scan was inspected at printed pp. 92-96 and 98, including the Main Theorem, list item 11, and its explicit SAT reduction. [Karp's source](https://doi.org/10.1007/978-1-4684-2001-2_9) is a dependency; no present-day literature or priority search was conducted.

## Decisive universal argument

For the original construction, B=n+1, K=Bm+n, N=n+m+2. In an arbitrary spanning tree, h is the indicator of tf, p counts hub-variable edges, and q counts clause-variable edges. The clauses have degree at least 1 and every incidence edge touches just one clause, so q>=m. Counting all N-1 tree edges gives p+q+h=n+m+1. Since the t-root vector is symmetric, its actual contribution is p+Bq regardless of the t-induced orientation. Therefore

    p+Bq = K+(1-h)+n(q-m).

All other root costs are nonnegative. With n>=1, a tree of cost at most K must have h=1 and q=m. Thus all clause vertices are leaves. Removing the leaves preserves a connected acyclic core containing tf. A variable needs at least one hub attachment for connectivity and cannot have both, because tf plus the two hub edges is a triangle. Every variable consequently has exactly one hub edge. This proof covers every spanning tree, including trees missing tf, using a variable to bridge the hubs, using multiply attached clauses, or using longer hub-to-hub routes. Those structures cannot escape the threshold. No normalization to assignment trees is assumed.

In such a structured tree, root q_j enters the core through its uniquely selected variable v_s. The edge v_s-h_s points from the variable to its hub. Every other variable-hub edge points from its hub to the variable, even if several clause leaves share one variable. This can be verified by removing each variable-hub edge: q_j lies on the variable side exactly for v_s. Each clause-root vector charges only the variable-to-hub copies of its occurring variables. Thus only the selected variable can incur a cost, equal to 1 exactly for a false selected literal. Hub-to-variable reverses, tf, clause edges, absent variables, the f root and every variable root contribute zero. Consequently only for these structured trees,

    F(T) = K + number of false selected literals.

A satisfying assignment supplies a structured tree with all selected literals true and cost K. Every arbitrary tree of cost at most K is structured and supplies a satisfying assignment. The two directions are exact for all n,m in the nontrivial source class. This is the decisive all-size proof, independently reconstructed; enumeration is supporting evidence.

## Boundaries and encoding

Repeated literals may be removed; a clause containing a variable in both signs may be deleted. An empty clause yields a fixed no-instance, while an empty remaining formula yields a fixed yes-instance. Explicit examples use a connected simple two-vertex graph with one edge and threshold 0: all entries 0 for yes, or both arc copies at one root equal 1 for no. No negative threshold or disconnected gadget is needed. With a remaining nonempty clause, at least one variable exists. Unit clauses and two-literal clauses are covered. Unused variables may remain if listed explicitly or may be removed.

Sparse numeric variable IDs do not require a number of vertices equal to the largest ID. Relabel the distinct occurring symbols to 1,...,n. The candidate's symbol-indexed construction supports this elementary normalization; it is an implementation detail, not a missing mathematical mechanism. The checker tests labels as large as 10^60 and relabels them by occurrence. There is no substantive repair request.

All 2N|E| root/arc entries are explicitly given, including zeros, with |E|<=1+2n+3m. Maximum original entry n+1 is O(N), and K=nm+m+n is O(N^2). Even a dense table with unary numerical entries has polynomial size. A tree certificate is checked by connectivity/acyclicity and a traversal from every root; all sums have polynomial bit length. The exact explicit integer decision problem is therefore strongly NP-complete. The same argument also applies to finitely encoded rational tables for ordinary NP membership, although that generalization is not needed. Arbitrary real vectors without a specified finite encoding do not justify an NP-membership claim; the integer subclass already establishes the source's optimization hardness.

Adding 1 to every arc entry at every root contributes exactly N(N-1) to every spanning-tree objective: N roots times N-1 chosen arcs. Adding N(N-1) to K preserves the decision answer. Strict positivity is therefore valid. Inward orientation together with the table replacement c_r(u,v) <- c_r(v,u) preserves every objective exactly.

## Independent finite support and negative controls

`independent_checks.py` ran successfully with `python3 independent_checks.py` and `python3 -O independent_checks.py`. Both runs have identical mathematical results. All checks use explicit exceptions, and an intentional failure under -O returned exit code 1 with the expected RuntimeError; `CHECKER_EXECUTION_RECEIPTS.json` and its stdout/stderr files record that control.

The suite includes all multisets of 1-3 nonempty normalized clauses for n=1,2; all multisets of 1-2 clauses for n=3; extra three-literal, unsatisfiable, repeated-clause and unused-variable cases; preprocessing boundaries; and the negative controls below. It tests the original B=n+1 and, separately after the freeze, B=2. Totals are 1,103 formula/parameter cases and 198,775 tree/parameter cases, including 117,629 trees missing tf, 125,646 with multiply attached clauses, 86,093 with a variable attached to both hubs, and 30,086 structured trees. Categories overlap. Each full run evaluated 1,395,584 actual root orientations for each of three configurations: original outward costs, inward orientation with reversed tables, and the positive shift. Every tree checked the exact threshold identity. Every structured tree checked its actual individual clause-root contributions and absence of unintended costs. Brute-force truth assignments independently verified satisfiability and the optimum among structured trees. Full finite data are in the normal and optimized results files.

After the independent freeze, the parent requested a parameter robustness check. The same edge count gives, for K=Bm+n,

    p+Bq = K+(1-h)+(B-1)(q-m).

Thus any integer B>=2 still enforces the same structure; B=2 bounds the costs by {0,1,2}. This is an elementary extracted consequence of the submitted mechanism, not a new approach, originality claim, or alteration of the original receipt. B=1 fails: for (x OR y) AND (y) AND (NOT y), take tf, t-v_x, q1-v_x, q1-v_y, q2-v_y, q3-v_y. This is a tree with p=1, q=4, h=1, and K=5. It has cost 5: the bridge clause is free at its root via x, and each unit-clause root charges no arc because the only variable with a hub edge is x, absent from those clauses. The formula is unsatisfiable. The checker verifies the witness and all root contributions. This is a counterexample to the unclaimed B=1 extension, not to the submitted B=n+1 construction.

The candidate correctly does not claim that the unrestricted optimum is K+minimum-unsatisfied-clauses. A control shows why that distinction matters. For n=2, B=3 and formula (x OR y) with three copies of (y) and three copies of (NOT y), m=7, K=23. The minimum unsatisfied count is 3, so the best structured cost is 26. A tree with only the hub attachment t-v_x, the bridge q1-v_x-v_y, and all six unit-clause leaves at v_y costs 25. Full enumeration of all 24 spanning trees confirms unrestricted OPT=25. Therefore the stronger global identity is false on this valid gadget; the threshold equivalence remains true and rejects all trees at K=23.

## Verdict, effort ledger and remaining gap

The original decision reduction and its strong NP-completeness, positive-cost and orientation conclusions are valid as written. No mathematical blocker or unsupported central lemma was found. No original file was edited. The strongest decisive evidence is the independently reconstructed universal proof; the finite results confirm implementation and illuminate unclaimed boundaries. Completion of this mathematical audit is 100%.

The original claim `claimed_solved 2/5` is preserved exactly. Its evidence is the original prose RESEARCH_LOG.md listing two substantive approaches; no author status.json or turns.json is inferred or fabricated. Additional proof-search approaches charged by this audit: 0. The parameter and negative controls are adversarial validation of the existing mechanism.

Priority and novelty remain unassessed. This report supports mathematical validity only; it does not independently assert an earlier-literature absence, human peer review, publication readiness, Martin-formulation equivalence, approximation guarantees, planar or bounded-degree restrictions, a fixed number of roots, or any result for adjacent Problem 2. No outreach, Git/index/service/editor mutation, or external publication was performed. Temporary third-party page images were deleted; no third-party PDF, image, or long extraction is included among public audit outputs.
