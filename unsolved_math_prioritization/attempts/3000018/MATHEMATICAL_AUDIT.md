# Independent adversarial audit: simple directed chip-firing halting

## Decision and immutable scope

**ACCEPTED COMPLETE PROOF**, for the exact main theorem and, separately, the oriented-graph strengthening. No unresolved mathematical gap was found. This public edition preserves the complete accepted arguments and binds these distributed files:

- Main report: [MATHEMATICAL_REPORT.md](MATHEMATICAL_REPORT.md), 13,502 bytes; SHA-256 `ca97098b22a3841876d3a9f6d66460312b5820cea1f0cacd381e3d16e6abe4c7`.
- Oriented appendix: [ORIENTED_APPENDIX.md](ORIENTED_APPENDIX.md), 2,692 bytes; SHA-256 `4550676ad4a0af003ba6ce068c2c63f1c4dabba4840af48b2087adbac6921a73`.

Editorial changes update titles, reconcile completed acceptance, use public file names, and distinguish recorded supporting evidence from edition preparation. No mathematical proof correction was required. This audit is AI-assisted and unrefereed; its acceptance is not external human peer review, journal acceptance, or formal proof-assistant certification.

The accepted result answers problem 3000018 / AMR-029-0018 affirmatively: deciding stabilization of a nonnegative integer configuration on a finite loopless simple strongly connected directed graph is NP-complete under polynomial-time many-one reductions. In the main proof antiparallel arcs are allowed. The independently checked appendix removes antiparallel arcs as well. Hardness persists when deleting one specified vertex leaves an acyclic graph with no directed path of two arcs, and when all initial counts, including the total, are polynomially bounded in the SAT input length.

This is mathematical acceptance of an authored proof, not a claim of first-in-literature priority or external peer review. It is separate from the multigraph reachability result for problem 3000016. The independent audit performed no publication or queue edit; this edition likewise changes no queue entry.

## 1. Bank identity: signs, constants, and endpoints

Fix a modulus q and a nonempty allowed set A. With h the periodic indicator of A, the proposed multiplicities are

    c_a = 1 + h(-a-1) - h(-a),       0 <= a < q.

Every multiplicity is 0, 1, or 2. Summing the two translated indicator sums shows that there are exactly q counters, including when some offsets are absent and others are duplicated. Duplicates denote different vertices.

The storage difference is particularly sensitive to the minus signs. On the transition k to k+1, every counter gains one and the counters at offset a=-k-1 wrap, losing q. Therefore

    S(k+1)-S(k) = q - q c_(-k-1)
                = q [h(k+1)-h(k)].

Thus S(k)-q h(k) is constant. Averaging q consecutive positions gives q(q-1)/2-|A|, since each of the q counters has mean (q-1)/2, and the average of q h is |A|. Hence the exact identity, including its constant term, is valid. Nonemptiness guarantees that the displayed maximum is attained. For A equal to the full residue set the storage is constant and all positions attain the displayed maximum, as required. For q=2 the constant itself can be negative, but the storage and maximum remain nonnegative; the proof does not confuse the constant with a chip count. The actual reduction uses q>=3 and nonempty proper sets.

Integer k may be negative in the identity; it is only a periodic residue parameter. The firing interpretation uses k>=0. All these edge cases were checked separately in the finite verifier.

## 2. Boolean/CRT semantics and preprocessing

Distinct primes at least 3 distinguish the residues 0 and 1 from all other residues. The variable banks enforce exactly a Boolean assignment. A normalized non-tautological clause on t distinct variables, 1<=t<=3, has exactly 2^t-1 satisfying local assignments. CRT maps those assignments injectively into residues modulo the product of the corresponding distinct primes. No non-Boolean residue is admitted by the clause predicate.

In one direction, all successful variable banks identify b_i=k mod p_i in {0,1}, and each successful clause bank forces the corresponding clause true. In the other direction, CRT gives a single nonnegative representative for any satisfying complete assignment. Reduction correctness does not require finding that representative or knowing the assignment.

Repeated literals may be deleted without changing truth. Clauses containing both signs of a variable may be deleted. An empty remaining clause is unsatisfiable; no remaining clauses is satisfiable. The fixed directed two-cycles in the main proof correctly represent those cases and satisfy its graph restriction. In the appendix these are correctly replaced by directed three-cycles. Deleting the distinguished vertex from the three-cycle leaves a single arc, so the stronger depth condition also holds in preprocessing cases.

As usual, n means the number of actual variables in the encoded formula; names can be relabeled consecutively and unused declared variables discarded. Thus n<=L. No large numerical variable identifier or binary declaration of unused variables needs to be expanded. This is the standard SAT encoding convention underlying Section 6, not an additional mathematical assumption about satisfiability.

## 3. Graph audit and shared returns

The main construction has disjoint vertex types: root, counters, and return vertices. A root-to-counter arc, counter-to-root arc, counter-to-return arc, and return-to-root arc cannot coincide. Each listed ordered pair occurs once. Distinct copies of an offset remain distinct source/target vertices. There are no loops, sinks, or parallel arcs. The root/counter antiparallel pairs fit the explicitly stated language.

A largest-modulus bank contains exactly P counters even if some of its offsets have multiplicity zero. Any one of these counters reaches every return vertex. The root therefore reaches all vertices, while each counter and return vertex reaches the root. This proves strong connectivity, including the highest-index return vertex.

Sharing return vertices among banks does not feed chips into any counter. It only accumulates chips at degree-one vertices whose unique outgoing arc returns them to the root. A return vertex holding b chips can legally fire b times and becomes empty. This works for arbitrarily large b and does not rely on simultaneous firing. Deleting the root leaves counter-to-return arcs only, and in particular no two-arc directed path.

The counts Q+P vertices and Q+sum(q_b^2)+P-1 arcs are exact. Every modulus-q bank has q counters of outdegree q, rather than one counter of multiplicity q. The output is a genuine simple graph.

## 4. Nonnegative input and conservative legal dynamics

Every counter starts below its positive outdegree, and every return vertex starts empty. Since S(0)<=B, the root starts with Q+B-1-S(0)>=Q-1>=0. Conservation gives total C=Q+B-1.

The root can be held inactive while legal counter and return firings are processed; legal asynchronous firing does not require firing every currently active vertex immediately. After one root firing, a previously stabilized counter gains exactly one chip. It has no other incoming arc, so it fires at most once before the next root firing. All counter firings can be completed before any return firings. The return phase is finite and returns all emitted chips. No vertex outside the root can be activated again until another root firing.

At checkpoint k, the counters are therefore exactly (a+k) mod q_b, all returns are empty, and the root has C-S(k). These are legal states reached by a legal sequence, not a fictitious system with a dissipative sink. The root may already be legal during the non-root phase; delaying it is permissible.

The root is stable precisely when C-S(k)<Q, or S(k)>B-1. Since S(k)<=B and storage is integral, this is equivalent to S(k)=B. Each bank is at most its own B_b and misses it by exactly q_b if false. Deficits are nonnegative, so there is no cancellation: equality of the total to B is equivalent to success of every predicate.

If SAT holds, the canonical sequence either stops earlier or reaches the first successful nonnegative CRT position and stops there. Its possibly exponential length is not an operation of the polynomial reduction. If SAT fails, every checkpoint permits another root firing and finite non-root phase, producing an infinite legal word.

For the converse required by halting, suppose a stabilizing vector f is realized by a legal terminating word. In any other legal word, at the first proposed firing that would exceed f_v, the current firing count at v is f_v and all other firing counts are at most their f coordinates. Nonnegative arc multiplicities imply that the current chips at v are at most the terminal chips at v under f, strictly less than its outdegree. The proposed firing is therefore illegal. This proves the needed least-action bound. Consequently an infinite legal word and a terminating legal word cannot coexist. No fairness hypothesis is needed.

## 5. Polynomial construction and chip bound

With H=O(L) banks and primes bounded by U=O(n log(n+1)), every expanded modulus is at most U^3. P<=U^3, Q<=HP, N=Q+P, and E=Q+sum(q_b^2)+P-1 are polynomial in L. Writing an adjacency matrix is polynomial as well.

The construction enumerates individual moduli only. A clause's allowed set is obtained from at most eight local assignments with polynomial-bit CRT arithmetic. It then enumerates q_b offsets. The global product of all n primes is not expanded as vertices, arcs, multiplicity, or a simulation length in the reduction. Its bit length is in any case polynomial; the mathematical existence of its CRT representative costs the reduction no simulation.

The count C is at most Q+sum(q_b(q_b+1)/2), hence polynomial in L, and every initial coordinate lies between 0 and C. Consequently the same construction establishes hardness with unary chip encoding. Our tests use complete periods only for bounded small instances; that testing choice is not part of the reduction algorithm.

As a consistency check independent of satisfiability, the nontrivial constructed inputs fit below the maximal stable capacity:

    (E-N)-C = sum_b [q_b(q_b-3)/2 + |A_b|] >= 0.

Here all q_b>=3. Thus the reduction does not inadvertently encode all instances as immediate NO cases by exceeding total stable capacity. The appendix increases both E and N by one, preserving this check.

## 6. NP certificate and bit-length bound

The report's self-contained membership specialization is valid. A certificate f>=0 has stable nonnegative z=x-Delta f, and can be checked by binary arithmetic in polynomial time. It need not be supplied as an exponentially long firing word. Least action against this stabilizing vector bounds every legal word and proves termination.

For an actually halting input, let f be its terminating odometer and let pi be the primitive positive integer kernel vector. The tree formula and choice of one outgoing arc at each non-root tree vertex give pi_v<=(N-1)^(N-1). If f>=pi coordinatewise, then f-pi is a nonnegative stabilizing vector with the same z, contradicting least action against the actual terminating word. Therefore some w satisfies f_w<pi_w.

For an arc u->v, the chip balance reads

    sum_(a->v) f_a = d_v f_v + z_v - x_v.

All firing counts and initial chips are nonnegative and z_v<=d_v-1. Dropping other incoming terms yields

    f_u <= d_v(f_v+1)-1,
    f_u+1 <= d_v(f_v+1).

The additive slack is essential and is retained by the report. A simple directed path from u to w has length at most N-1; iterating along it gives

    f_u+1 <= (N-1)^(N-1) (f_w+1)
           <= (N-1)^(N-1) pi_w
           <= (N-1)^(2N-2).

Each coordinate has O(N log N) bits. For N=2 the unique strongly connected loopless simple graph is the directed two-cycle; a nonnegative halting configuration is zero and its odometer is zero, agreeing with the bound. The argument does not assume polynomial stabilization time.

## 7. Separate oriented-graph strengthening

The appendix preserves the same bank moduli, outdegrees, chip counts, and checkpoint equations. It removes counter-to-root arcs and replaces the outgoing neighborhood of each modulus-q counter by q distinct return vertices. All arcs then follow the cyclic three-part order root -> counters -> returns -> root, forbidding antiparallel pairs as well as loops and parallel arcs.

A modulus-P counter reaches all P returns. Every counter reaches the root through a return vertex, proving strong connectivity. A counter firing still ultimately returns exactly q chips, so all legal checkpoint arguments remain valid. There is one extra vertex and one extra arc, and deleting the root still leaves only counter-to-return arcs. The directed three-cycle preprocessing in the appendix respects every strengthened restriction. NP membership applies to this subclass. Accordingly the strengthening is accepted independently rather than silently retrofitted into the main construction.

## 8. Recorded supporting checks and negative controls

The independent audit records a separately implemented verification that imported neither the construction checks nor their outputs. For clauses it scanned residues and evaluated literal truth, rather than using the construction's local CRT formula. It constructed explicit adjacency lists, performed each individual legal firing, and compared outcomes with exhaustive Boolean truth evaluation. Programs and raw generated outputs are not distributed; the written analytic proof depends on no omitted executable.

The audit records byte-identical final normal and optimized Python outputs. Both recorded executions passed:

- 8,177 nonempty bank sets for every modulus 2 through 12, including full sets; 270,105 positions spanning negative, zero, and positive representatives.
- 592 explicit graph cases, half main and half oriented; 256 satisfiable and 336 unsatisfiable; 1,542,295 individual legal firings. Coverage includes every subset of the eight normalized one- and two-literal clauses on two variables, unique-solution three-variable formulas, the full unsatisfiable three-variable clause set, mixed-length formulas, repeated literals, tautologies, empty clauses, and no-clause cases.
- 30 additional schedules using lowest-index, highest-index, and pseudorandom currently legal vertices, including interleavings outside the canonical order; 20,220 individual firings. A repeated state gives a concrete nonempty legal lasso for nontermination; terminal vectors are independently checked for stabilization.
- Exhaustive legal-successor exploration for 256 configurations across all 19 strongly connected loopless simple graphs on two or three vertices, examining 1,092 reachable states and 113 halting configurations. This checks the halting dichotomy, stable uniqueness, least-action count bounds, tree/kernel orientation, and the explicit certificate bound in a family independent of the reduction graph shape.
- Five deliberately damaged variants detected: reversed bank-difference sign; an extra total chip causing a SAT false negative; three deleted chips causing an UNSAT false positive; a parallel root arc; and an invalid firing-vector certificate.

Finite tests support the audit but are not the general proof. The symbolic arguments in Sections 1-7 are what establish acceptance. The aggregate results are retained as supporting metadata in [ACCEPTANCE.json](ACCEPTANCE.json). Edition preparation did not rerun these mathematical checks.

## 9. Primary-source inspection and bounded literature check

Farrell and Levine, *CoEulerian graphs*, arXiv:1502.04690v3, supplies the nonnegative strongly connected halting language on PDF page 2 and prior NP membership in Section 3 on page 10. Section 3.1 and Table 1 on page 13 explicitly leave the simple directed case open. The graph convention there permits ordered-pair multiplicities in {0,1}; the optional appendix removes any possible ambiguity about antiparallel arcs. The source's maximal-stable-capacity observation on page 2 is prior work. [Versioned primary source](https://arxiv.org/pdf/1502.04690v3)

The corresponding Egres problem page asks exactly the NP-completeness question for simple digraphs and attributes it to Farrell and Levine. During the recorded audit inspection it labeled the entry an open problem, with a displayed modification date of 5 December 2016; that is historical evidence, not a certification of the whole 2026 literature. [Original problem page](https://oldlemon.cs.elte.hu/egres/open/Complexity_of_the_halting_problem_for_simple_digraphs)

The audit records a bounded web search on 10 October 2026 that found no competing exact resolution. The acceptance decision does not depend on that negative search and makes no novelty or exhaustive-search claim. [SOURCE_METADATA.json](SOURCE_METADATA.json) records version, URLs, PDF hash and size, inspected pages, and the distinction between reused source bytes and fresh web inspection during the audit. Edition preparation performed no new scholarly-source retrieval, source-file rehash, source inspection, or literature search. No third-party source text or PDF is included in these authored audit deliverables.
