# Independent primary-source audit of the pivotal upstream FPRAS

Audit completed 2026-10-07 UTC. Pin: `adc7f1241b42e322a6451854ab7e4b4c146bf78a`.

**Verdict: no substantive upstream mathematical gap identified.** The pinned manuscript supplies a coherent argument for a uniform unweighted FPRAS on finite simple undirected graphs, including certain-zero behavior and a polynomial bit-time bound on every execution. Its deletion self-reduction also supplies an approximate uniform sampler with guaranteed feasibility on every execution. This is an independently reconstructed source-level verdict, not an independently reproduced Lean kernel certificate or an execution of the full, extremely large FPRAS.

No candidate manuscript, package, or prior favorable audit file was read or edited. While inspecting available concurrency slots, the collaboration tool automatically exposed previous completed agents' final summaries, including a favorable upstream verdict and finite-test counts. These summaries were not used as proof and no previous check implementation was imported. This incidental exposure means that this audit should not be described as fully blinded. The proofs and both check scripts below were derived directly from the original source. The separate Lean-scope child likewise received the shared context but read no prior audit file.

## 1. Exact source and scope

The source audited is

`/Users/alec/Documents/Math/openai_followon_weighted_hafnian/sources/preprints/A-Fully-Polynomial-Randomized-Approximation-Scheme-for-Perfect-Matchings-in-General-Graphs-September-23-2026/build/main.tex`.

Its SHA-256 is `dcf28553d442dfc53a9f90f7c52bd48c9e2e7e5e27b197aa7ca4be1c8daed703`. The original clone file and its exact pinned Git blob have the same hash and bytes. The original clone HEAD is also the pin. A read-only `git ls-remote origin refs/heads/main` during this audit returned the same pin; this checks that ref, not unmerged corrections or other branches.

Below, `T:L` denotes line L of that exact manuscript. The theorem at **T:132–143** quantifies a single uniform classical algorithm over finite simple undirected graphs and rational `0<epsilon<1`, `0<delta<1/2`. It returns a nonnegative rational approximation, returns zero certainly for zero count, and has worst-case bit time polynomial in full input length, `epsilon^-1`, and `log(delta^-1)`. The nonempty branch has at least one perfect matching; empty input returns one (**T:2538–2542**). The input representation guard covers succinct vertex counts with uncovered vertices (**T:2853–2859**).

This theorem does **not** itself accept binary rational edge weights or compressed multiplicities. The intermediate weighted/colored matching spaces are explicitly represented, while the main theorem retains simple unweighted inputs (**T:335–356**). A weighted-hafnian consequence therefore needs a separately proved compact exact reduction; it cannot be inferred merely from the weighted notation in the upstream proof. Extending the permitted confidence interval to `0<delta<1` is harmless by calling the base algorithm at `min(delta,1/4)`.

The supplied manuscript citation names OpenAI; original preprint README **lines 3–16** specifies the author, date and BibTeX block. The source repository README **lines 3–9, 46–50** describes AI production and differing verification stages. Neither provenance nor directory presence was treated as mathematical evidence.

## 2. Inflation bridge reconstructed

The four-hole inequality follows from a weight-preserving alternating-path injection with a specified endpoint, with an explicit inverse (**T:497–524**). The strong-path relocation argument normalizes by the current row maximum; this is what makes relocation errors additive rather than multiplicative along a long strong path (**T:536–637**). In particular, each step can be inverted after removing its specified inserted edge. The stops at the first fixed hole handle two-hole and four-hole sets uniformly.

The deformation `mu(t)=lambda+tB/D0` uses the original fixed bottleneck similarity B. Its log partition derivative and two-hole derivatives are finite polynomial identities (**T:640–661**). On a provisional row-range interval, relocation bounds the derivative summands. Integration puts all rows strictly inside that interval; continuity prevents a first exit (**T:663–690**). This establishes inflation below two without assuming the conclusion. Inserting a pairing of an arbitrary even hole set using distinguished added edges is injective and yields the logical all-hole bound (**T:696–706**).

For the subdivision, intact paths have the two required tilings, with odd/even weight ratio `lambda_e` (**T:752–810**). Deleting internal vertices either consumes a terminal or creates a neutral pair. The explicit accounting factors and forbidden broken logical edges yield an exact bijection, not merely an inequality (**T:977–1092**).

The maximum bottleneck pairing capacity has the simultaneous threshold-class floor-count formula (**T:1103–1139**). Removing neutral pairs and mapping consumed holes gives the threshold charge. Away-from-home and cross-center cases use `max(1,lambda_e)` in the integrated threshold charge, with the correct inequality direction when `lambda_e<1` (**T:1141–1234**). This is a potential boundary trap; the stated factors cover it. Each virtual edge label has height at most the endpoints' bottleneck similarity. Summing the lifted-hole estimate over colored partial matchings gives the convergent geometric series `1+2/99<2` (**T:1236–1257**). No guide-mixing assertion is used in this inflation proof.

## 3. Cycle identity, repairs, congestion and rare guides

The label walk lives in a tree because a vertex has at most two adjacent memberships (**T:1272–1282**). The recursive quadrangulation preserves the original full-cycle label sets. Its two cases, depending on whether the exterior arc is good, provide both an opposite good pair and the stronger condition needed when the other opposite pair has two long sides (**T:1393–1521**). The strengthened condition is necessary for error-demand guides and is actually proved.

Long arc conversions are not asserted to be single chain transitions. The signed cell identity uses conversions as exact function identities. Complementary occurrences of one diagonal contribute one whole-cycle difference; they do not cancel to zero. Since there is one more cell than diagonal, the global identity has exactly one copy of the whole-cycle difference (**T:1683–1706, 1776–1847**). The examples and the algebra agree.

The repair construction removes one incident edge at every corner. For a long good arc, removing both boundary edges uncovers two distinct leaves and the repair rematches those leaves, including the length-three boundary case (**T:1875–1886**). Every encoding changes at most four added and four dropped edge occurrences in the multiset union. Comparability of those edges gives the weight factor `A0^4`; the reconstruction tag restores the original union and determines the active cycle and its alternating layers (**T:1888–1955**). Coincident colored edges are tracked as occurrences, avoiding an injectivity failure caused by losing multiplicity.

For each error arc X, **both** encoded guides contain its closed pattern `C_X` (**T:1899–1917**). The conditional demand-mass estimate retains the event mass `p_X` (**T:1977–1997**). Jensen contributes `1/p_X`, and the two factors cancel exactly (**T:2004–2043**). Thus even a very rare closed-pattern event does not cause an unsupported inverse-probability bound. The through and closed patterns perfectly match the same vertices, so their union is an entire isolated discrepancy component, and the fresh-pair swap sum has only polynomial multiplicity (**T:2045–2073**).

Safe-switch, color-change and cycle-swap proposal probabilities provide explicit capacities (**T:1648–1679**). Reindexing previously toggled demand cycles is an involution preserving product weight. Combining this with the global identity and the encoding loads proves the additive two-coordinate energy theorem (**T:2077–2136**). No canonical-path congestion theorem or assumption of single-coordinate rapid mixing is silently substituted.

## 4. Global gap for arbitrary functions

The additive pair inequality alone would not establish a global gap. The replica proof provides the missing step explicitly (**T:2137–2152**).

Adjacent tier densities are within a factor two (**T:2248–2272**), so Metropolis capacities transfer the pair inequality to unequal tiers (**T:2304–2317**). Order upper tiers before lower tiers. A martingale increment at upper slot x is estimated by each lower guide y, plus a two-coordinate residual. Product conditional expectation decreases pair energy, giving the displayed one-pair estimate (**T:2325–2363**).

In the ANOVA expansion, a residual `r_xy` consists precisely of centered components S containing x,y whose other coordinates precede x. Since y follows x, y is last and x is penultimate in S. These two positions determine the pair uniquely, even for pairs sharing a slot. Therefore the residual squared norms sum to at most the total variance (**T:2370–2393**). Averaging over `q=32L` guides makes the residual coefficient 1/4, which is absorbed. Base refreshes control base martingale increments exactly. The resulting inequality `Var <= (8M/3)E` is a global Poincare inequality for **arbitrary** functions on the augmented product space (**T:2397–2418**).

This argument does not assume irreducibility to prove the gap; full-support stationary weights, the finite reversible kernel and the proved Poincare inequality supply that conclusion. Laziness and the explicit minimum-mass bound then yield the claimed total-variation mixing estimate (**T:2449–2482**).

## 5. Uniform counting, bounded-bit histories, and sampling

The unit-tier dynamic program uses vertex-to-bag assignments and clique pairings. Disjoint interfaces make the polynomial convolution recurrence valid; it counts rather than enumerates all assignments. Its counts have `O(N log(N+1))` bits, and its sampling procedures use only polynomially many sequential choices (**T:2166–2244**).

The annealing estimator uses marked exact-event identities with one batch exposing both partition and two-hole ratios (**T:2592–2637**). Scaling preserves the normalized matching law. The one-pass scaling constraints remain feasible, and a tight constraint in every row persists because a later update cannot decrease its tight neighbor (**T:2667–2687**). On accurate empirical histories this restores balance (**T:2713–2771**). Fresh-run errors and concentration are accumulated conditionally on each preceding successful stage; no independent-history assumption is needed (**T:2785–2800**).

The completed logical graph has final bias at most `epsilon/32` times the target because the unweighted nonzero target is at least one; the exact zero test occurs first (**T:2802–2842**). The powers used for the schedule and confidence are computed by rational comparisons, avoiding real-arithmetic assumptions (**T:2862–2886**).

Crucially, failed histories remain defined. Clipped estimates and scale update bounds keep positive scales and unconditional `lambda_e<=4^K` (**T:2573–2588, 2664–2711**). A maximizer dependency in a scale update strictly decreases its update index, so the expression has at most n factors; successive stages add, rather than exponentially multiply, bit lengths (**T:2904–2949**). Matching product weights and unequal-tier acceptance ratios have polynomially many rational bits. The unknown partition functions cancel (**T:2951–2965**).

The fixed-grid categorical method never selects a zero-probability outcome. Its error is accumulated over a deterministic draw bound and a deterministic number of chain steps. All bit choices, DP choices and marking choices are budgeted (**T:2967–3031**). The final time envelope has fixed polynomial degree and holds on unsuccessful tapes as well (**T:3033–3079**). Very large constants and the degree 100 are serious practical limitations, not a uniformity or polynomial-time gap.

The separate deletion sampler has exactly the needed unweighted scope: explicit finite simple graphs, certain infeasibility, feasible output on every tape, TV error at most tau, and every-execution bit time polynomial in full length and `tau^-1` (**T:3203–3211**). Both child branches are checked exactly for feasibility; even count-estimation failures and a zero estimate sum choose a feasible branch (**T:3226–3249**). Count-relative-error, failed-call and dyadic errors are accumulated over at most the original number of edges (**T:3251–3289**). This justifies an applicable base sampler; an FPRAS name alone was not used to infer one.

## 6. Independently reproduced finite checks

`cycle_checks.py` imports no prior project or audit code. It transcribes the manuscript's recursive split and matching constructions. Exhaustive closed label walks of lengths 4,6,8,10 on the three-node path and four-node star produced:

- 34,868 walks;
- 133,698 cells;
- 24,569 two-long-side error demands.

Every case passed admissibility, the two good-side conditions, edge-label diameter at most six, legal repaired matchings, at most four multiset changes in each direction, both guide containments, isolation of the swap component, and the **symbolic global cell identity for arbitrary function values**. Chord and repair colors use a fixed minimum common label. This is exhaustive for those walks and choices, not all trees, cycle sizes or permissible color choices.

Script SHA-256: `60781ae85b749da55cdf86b1ba81ba353afebb6e2d79d231ddc66549f91d7282`.

`hole_checks.py` builds a four-terminal complete logical graph with activities `(4,1/7,2,3,1/3,1)` and p=4, giving a 100-vertex real graph. A generic exact weighted graph recursion supplies the deleted partition functions independently of the source deletion formula. For 1,767 deterministic/random hole sets, including selected same-leg and cross-center patterns, 516 feasible and 1,251 infeasible cases passed. The feasible cases also passed the **exact rational** threshold-capacity charge `F Phi_B'(U) <= Phi_B(R)`. The source-formula side and the generic graph-count side therefore agreed exactly. The test intentionally includes activities below one and unequal strong bottlenecks.

The same script enumerates all subsets of nine slots (three tiers, three replicas). Each of the 189 eligible ANOVA components was assigned to a unique allowed pair, verifying the finite set-theoretic charging mechanism.

Script SHA-256: `4342f9367a95a4526c6bb5eeb859d5a95138ebf64f06e2e24af1965d0cc805ee`.

These checks can be rerun with Python 3 standard library only. They support the specific constructions and can expose small counterexamples; they do not prove the full upstream FPRAS or certify arbitrary untested instances.

## 7. Actual Lean scope and verification limit

The actual source theorem is `OAI.MatchingFPRAS.thm_main` at

`/Users/alec/Desktop/math/lean/OAI/Combinatorics/MatchingCount/Main.lean:21–30`.

Its `MainStatement` at `Model.lean:94–100` places one finite-alphabet machine and fixed polynomial constants **before** all graph/accuracy/confidence inputs. Its graph input contains no weights (`Model.lean:8–11`); its exact count is the integer cardinality of perfect matchings (`Model.lean:14–23`). Input encoding and physical tick semantics are explicit (`Model.lean:38–64, 74–82`). The top source proof invokes supplied time, output, zero, and fair-tape success declarations, not a hypothesis containing the desired conclusion. I inspected these top definitions directly.

The independent child inspected the entire actual local import closure and concrete global-gap declarations. `Machines/TreePairProposal.lean:389–394` states the concrete ladder Poincare inequality; its section hypotheses include acyclic label graph, same-vertex labels adjacent, positive label heights comparable across adjacent labels, `D>=1`, bag edge activity bounds, an existing perfect matching, and `|V|>=2` (lines 369–387). The local pair-Poincare requirement is discharged in the concrete proof (lines 406–421), rather than left as an oracle assumption. `Graphs/Evolve.lean:172–180` states the corresponding concrete ladder mixing inequality and invokes that gap at lines 206–224. Its detailed source report and receipts are in `lean_scope/`.

The comparator `MatchingFPRAS.lean:105–106` has a `sorry` template; it is not imported by the actual proof. The child's lexical scan of the 415 actual local source files (3,091,883 bytes) found no `sorry`, `admit`, `axiom`, `unsafe`, `opaque`, `implemented_by`, `native_decide`, or `cheat`. All 423 upstream files read by the child matched their exact pinned Git blobs. A lexical scan is not a kernel-generated axiom audit.

Lean 4.34.1 is installed, but this pinned checkout has no `.lake` directory and no compiled local or Mathlib dependencies. A direct import probe failed at missing `Main.olean`. No build, successful import, kernel axiom list, executable FPRAS run, or formal verification of the follow-on weighted theorem is claimed. Absence of the build is a verification limitation; it does not alone falsify the complete manuscript proof. The source-level theorem statement does agree with the unweighted bounded-bit claim needed by the follow-on reduction.

## Final disposition

There is no identified substantive upstream obstruction requiring withdrawal of an unconditional consequence **on the strength of the independently checked manuscript proof**. A package must still accurately disclose upstream attribution, source-level versus kernel-checked status, the exact-reduction dependency for binary weights, and the limited role of finite tests. Priority, the candidate compact gadget, and candidate packaging were outside this audit's assigned scope.

Completion estimates: upstream mathematical audit 100%; this audit report/receipts 100%. These are completion estimates, not a proof of correctness or a global publication-completion claim.
