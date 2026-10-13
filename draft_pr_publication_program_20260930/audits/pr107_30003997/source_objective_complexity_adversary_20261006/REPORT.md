# Source, objective, and complexity adversarial audit

**Verdict: mathematical and literal-source gate passes for the frozen complete candidate.** No substantive proof correction is required. Historical priority remains unestablished and is a separate gate. This report does not promote the result, modify the original attempt, or make a novelty claim.

Target: PR107, canonical upstream ID30003997, supplied head `cc2ae01897135b35bee135917819e782a220f2c1`. Audited frozen `original_attempt/PROOF.md`: 8,009 bytes, SHA256 `2c219bf80ad4bbba75f8c70169b26b7e9b11b6f5e1742543f25d9cb0d0c5ebe8`. Scope: independent source interpretation, formal construction audit, finite objective checks, numerical complexity, and related-source identity only. Original complete candidate is turn1/5; this audit consumes zero new proof-search turns.

## 1. Independent source pin and exact target

Before opening the candidate or any review, I inspected both images of the full Kaibel contribution, printed3014-3015 / PDF46-47, and independently extracted its text. `INITIAL_SOURCE_COMPARISON.md` and `INITIAL_SOURCE_PIN.json` record that sequence and hashes. No old or other-family review was consulted in deriving the interpretation or verdict.

Literal Problem2 supplies D=(V,A), one fixed root r, and a vector c^v in R^A for each nonroot destination v. Its objective is

C(T) = sum_{v != r} sum_{a in P_T^v} c^v_a.

The stated directed r-v path exists for every nonroot v. This makes the feasible tree a spanning out-arborescence: paths run from the supplied root to each destination, all vertices are included, and they share one common tree. The source does not optimize the root or permit a separate tree/path structure for each destination. The vector belongs to the destination, not to the head of each traversed arc. These conventions agree with candidate section1.

Adjacent Problem1 has a different domain and objective: one undirected spanning tree is assessed using every possible root's full rooted orientation. Its Martin motivation is distinct from Problem2's Wong motivation. Neither adjacency nor the common word arborescence establishes equivalence. The candidate correctly confines its theorem to Problem2 and does not claim a translation proving Problem1.

The source wording `(Why)` requests a hardness explanation. It is not a hardness proof, proof of an unresolved historical status, or novelty certificate. The motivation explicitly concerns **integer** optimization over an extended formulation. A continuous linear relaxation's tractability cannot establish polynomial integer optimization. The candidate proves the literal graph statement directly and appropriately does not rely on an unverified polyhedral translation.

## 2. Decision, exact zero, and arbitrary real scopes

The original source permits arbitrary real entries. The candidate defines a separate finitely encoded decision problem: rational coefficients and rational threshold K in binary; ask whether some feasible arborescence has C(T) <= K. It claims NP membership for this existential decision problem. That claim is correct: a certificate lists |V|-1 arcs; rooted spanning structure and all paths can be checked in polynomial time; paths have length at most |V|-1; there are at most |V|(|V|-1) rational summands; exact addition/comparison uses polynomially many bits in the total rational input encoding. Feasibility failure is a no instance.

The theorem's phrase 'has value zero' is explicitly within the restriction c^v_a in {0,1}. In this subclass every feasible C(T) is nonnegative, so OPT=0 is equivalent to existence of a tree with C(T)<=0. The NP certificate therefore proves the theorem's zero claim. The proof does **not** claim NP membership for exact OPT=0 on unrestricted signed rational inputs, nor for arbitrary unencoded reals. With signed costs a zero-cost tree alone would be insufficient: `guard_results.json` checks a three-vertex instance having tree values0 and-1. This guard is a distinction in scope, not a counterexample to the candidate.

The integer subclass is included in the source's real coefficient domain. NP-hardness of this bounded integer subclass supplies a valid hardness explanation for the literal optimization task under any computational model supporting ordinary encoded integer inputs. It does not transform an unencoded real input task into an NP language.

## 3. Formal construction audit

The prerequisite theorem was independently checked on the primary Karp scan: printed94 gives the main completeness theorem; printed95 item11 is satisfiability with **at most** three literals per clause. Unit and binary clauses are allowed. Text extraction of those scan pages returned only form-feed characters; this limitation is retained in `karp_extraction_failure.txt`, and both pages were visually inspected.

After tautology and repeated-literal removal, the nontrivial formula has n variables and m nonempty clauses, each with distinct variables and one sign per variable. The construction has N=1+3n+m vertices, M=4n+sum_j |C_j| <=4n+3m arcs, and a dense coefficient table of (N-1)M entries. Its size is polynomial even in the dense input convention. Literal names can be relabeled compactly; n need not depend on the numerical magnitude of an input variable label.

All arcs go to the next of four layers. No loop or parallel arc occurs after preprocessing. Root arcs force both t_i and f_i into the tree, the variable vertex v_i has exactly one of its two incoming parents, and each clause vertex has exactly one selected variable parent. Thus every tree gives one globally consistent assignment. Conversely every such collection of parent choices gives exactly N-1 arcs and, by the layer order, an acyclic reachable spanning out-arborescence. Root, branch, variable, and clause indegrees are respectively0,1,2, and at most3. Every clause is reachable because it is nonempty.

A clause path uses the same variable parent as all other destinations passing through that variable. A positive literal is charged on r->f_i and a negative literal on r->t_i. Therefore the clause's path cost is1 precisely when its selected literal is false. Costs for all other destinations vanish. Candidate equation6 follows without charging forced unused root branches or any other clause's vector.

A satisfying assignment chooses a true literal for every clause and gives zero cost. A zero-cost tree gives a globally consistent satisfying assignment. For a fixed assignment, clause-parent choices are independent: satisfied clauses can select a true literal; an unsatisfied clause cannot. Consequently equation7, OPT equals the minimum number of unsatisfied clauses, is valid. No circularity, extra search oracle, unsupported equivalence, or change of objective is used.

## 4. Strong NP-hardness and strictly positive costs

The primary reduction's only numeric coefficients are0 and1, and K=0. They remain constant under unary encoding. The nonnumerical graph construction is polynomial and contains the SAT difficulty. Thus the bounded-integer decision subclass is NP-complete and strongly NP-hard in the conventional bounded-numeric-data sense; the optimization task is strongly NP-hard. This conclusion is not based merely on short binary encodings of large values.

In the positive variant, every coefficient is increased by1, including those for non-clause destinations. Each path in the constructed graph has its destination's layer depth. There are2n depth1 vertices, n depth2 vertices, and m depth3 vertices. The exact increase is2n+2n+3m=4n+3m for **every** tree. Entries become1 or2, and the threshold satisfies

K'=4n+3m <=3(N-1).

This gives polynomially bounded numerical data and preserves satisfiability exactly. The offset relies on the fixed depths of this reduction; the candidate correctly limits that assertion to 'this layered graph'. It does not assert that adding1 preserves optima on arbitrary directed graphs.

## 5. Boundary and reinterpretation challenges

The main hard family can be taken to have n>=1 and m>=1, so all four layers are nonempty. Unit/binary clauses, unused variables, either literal sign, repeated literals, tautologies, empty conjunctions, and explicit unsatisfiable clauses were considered. No-clause graphs have an empty last layer but do not weaken hardness on the nontrivial family. An empty clause must use the stated trivial-input branch rather than become an unreachable z_j. The candidate already reserves fixed yes/no instances; its existing gadget on formula (x) has OPT0, and on (x) AND (not x) has OPT1, both with nonempty four layers and all promised graph restrictions. Making the empty-clause early branch explicit would improve the prose, but is not a substantive gap in the hardness proof.

The obvious polynomial replacements fail exact objective checks:

- Separate per-destination shortest paths: for (x) AND (not x), each clause individually has a cost0 root path, but these paths require conflicting parents of the shared variable vertex. A common arborescence has OPT1.
- Sum all destination vectors into a single ordinary arc-cost vector: for (x), (not x), and (x OR y), the literal source costs of feasible trees take values1 and2; every tree's ordinary arc sum after that aggregation is4. The aggregation changes the objective and loses the coupling.
- Treat a destination's coefficient as a charge only when an arc enters that destination: the construction places all nonzero coefficients on early root arcs, so this reading discards the clause charges and contradicts the printed path sum.
- Continuous LP optimization: the source says integer optimization. The candidate makes no claim of an integral relaxation or relies on one.

`independent_scope_checks.py` imports no candidate verifier or review. It constructs full dense tables, enumerates incoming-parent choices, reconstructs literal directed root paths, computes destination-vector costs, and compares every optimum with exhaustive assignments. It checked396 formula cases and64,400 trees, including the eight full three-variable clauses, all normalized clauses over up to3 variables in formulas of at most2 clauses, and fixed yes/no gadgets. Every tested restriction, equation6, equation7, positive offset, and numerical bound passed. `signed_and_scalar_guard_checks.py` checks the additional signed-language and aggregation examples. Finite tests support the audited deductions; the arbitrary-size proof is the formal argument above.

## 6. Related-record identity and priority separation

Primary payloads were selected read-only from `unsolved_math_prioritization/cache/catalog.sqlite`, metadata revision `37e53eabe540fb458758e198be61634bd02ee008`, using only numeric IDs30003996 and30003998. Their reports are empty objects. The primary30003998 payload exactly equals frozen `duplicate_record.json`. It repeats literal source Problem2 and is not a separate mathematical target or a fresh proof budget. Primary30003996 is literal source Problem1, the distinct all-roots undirected-tree objective. These facts are source comparisons, not audits of any other PR.

The related-target file contains no group entry for these IDs. Its absence is not evidence of conceptual independence. The candidate already explicitly credits the shared assignment/literal-selection mechanism and distinguishes model equivalence from common ideas. The frozen source30003997's background assessment incorrectly uses a Problem1 description, while its original/displayed statement agrees with Problem2. Candidate `SOURCES.md` already records this metadata discrepancy; the primary contribution controls the mathematical scope.

Neither the dated dataset 'open' labels, the parenthesized `(Why)`, nor an unsuccessful bounded search establishes novelty or a prior solution. This audit does not conduct a comprehensive priority investigation. Its strongest verified result is the complete literal Problem2 hardness proof with all stated restrictions, including the strictly positive extension. A historical-priority finding is unresolved separately and must not be inferred from this mathematical pass.

## 7. Corrections and unresolved items

Required proof/source corrections: **none**.

Nonblocking wording improvement: explicitly route an input containing an empty clause to the trivial unsatisfiable branch before asserting all remaining clauses are nonempty; optionally state the fixed yes/no examples already generated by the existing construction. This uses the candidate's stated branch and is clarification, not additional proof-search.

Unresolved outside this audit: historical priority; explicit equivalence to a particular Wong formulation (not needed by the literal graph theorem and not claimed as a proved result); any theorem for distinct Problem1. No publication, native/editor, Git, queue mutation, outreach, or GitHub review action was performed. All new artifacts stay in the assigned audit folder.
