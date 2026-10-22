# Independent topology and set-theory falsification assessment

Phase boundary: this document was completed on 2026-10-16 before the contents of either original audit, ACCEPTANCE.md, or the package metadata were read. The completion UTC and SHA-256 are recorded separately in PHASE_BOUNDARY.json. This is a direct falsification audit: I read the submitted candidate REPORT.md and was not blind to its proposed proof. I did not consult another new review family. I independently checked each deduction below rather than treating the candidate or its labels as true.

## Exact scope and evidence

Submitted HEAD: b356dec5cb01e5f536b9cfeece56ad08844c03cb. The externally supplied ORIGINAL_FILE_RECORDS.json SHA-256 610351fbb778f78ce53cda03ea715f38615abb5710690987c214f8093bda13ae was verified. All 26 originals, totaling 147731 bytes, matched their recorded SHA-256, exact Git blobs/HEAD contents, Git modes and disk modes. The candidate REPORT.md SHA-256 is ddde58f03f320c881b78e59b60a40f315e1811c7c88aaa25ce620c427afbb6ca. The starting authentication is AUTHENTICATION_BEFORE.json.

Primary question: Khukhro–Mazurov, Kourovka Notebook, arXiv 1401.0300v48, printed/PDF page 193, problem 21.107, https://arxiv.org/pdf/1401.0300v48. I read the web extraction, downloaded the pinned PDF and rendered/visually inspected that page. The PDF is 1476795 bytes, SHA-256 a646018b69344a06729ba0cfda50d3850e99fd6c04e798f58b6e82aef8c33462. Download and source bodies/images are private and excluded from public sealing. I then read NEUTRAL_PROBLEM_BRIEF.md and RESEARCH_CHARTER.md, then the candidate. The actual problem statement adds no first-countability, metric, uniform block-size or covering requirement. I do not infer any priority/current-status claim from this local observation or from the queue label.

Formal target, under the meaningful nonempty-open convention: does a countable topological group with a partition into countably many dense sets necessarily have pairwise disjoint finite sets F_n such that

    for every nonempty open O, there exists m such that every n > m has F_n intersect O nonempty?

A negative answer requires one group satisfying the antecedent and, for every such block sequence, one nonempty open O with arbitrarily late missed blocks. The neighborhood O may depend on the whole sequence but must remain fixed for infinitely many indices. I use the stronger hypotheses of a countably infinite Hausdorff nondiscrete group and countably infinitely many nonempty dense pieces. I do not use the empty open set or a finite-group convention as a loophole.

## Reconstructed proof, with the possible failure points exposed

### 1. The only set-theoretic ingredient is a free ultrafilter available in ZFC

Let N denote the nonnegative integers. Order by inclusion all proper filters containing the cofinite filter. A chain has a union which is a proper filter: any two chosen members already belong together to one filter in the chain; no filter in the chain contains the empty set. Zorn supplies a maximal proper filter U. If C is not in U and adjoining C generated a proper filter, maximality would fail. Consequently some B in U has B intersect C empty, so N minus C is in U by upward closure. A proper filter cannot contain both C and its complement. Thus U decides every subset. It contains no finite set, because its cofinite complement already belongs to U.

Only closure under finitely many intersections, exclusion of the empty set, inclusion of cofinite sets, and the complement decision are used later. No intersection over infinitely many U-members is taken. No pseudointersection, selector, Ramsey homogeneous set, rate-of-growth restriction or countable completeness is assumed. An arbitrary such U suffices. This is a nonconstructive ZFC existence proof, not a finite computation and not an assertion in ZF alone.

### 2. A Hausdorff joint group topology

Let G be the set of all finite subsets of N; add by symmetric difference. The empty support is 0, each element is its own inverse, and Boolean group laws are immediate from parity of membership of every coordinate. The group is infinite because its singleton supports are distinct; it is countable because it is the union over r of the finite powersets of {0,...,r}, together with the empty support if desired.

For A in U let H_A be the finite subsets of A. This is a subgroup. H_A intersect H_B equals H_(A intersect B), and A intersect B is in U. Define a base to consist of all x + H_A. Every point belongs to such a set. If x belongs to both s + H_A and t + H_B, these cosets respectively equal x + H_A and x + H_B. Their intersection is x + H_(A intersect B). This proves the base axiom, including arbitrary different centers.

For joint continuity of addition, a basic neighborhood of s+t can be written (s+t)+H_A. The product neighborhood (s+H_A) times (t+H_A) maps into it, since H_A+H_A=H_A. This checks the two-variable product topology, not just separate translation continuity. Inversion is the identity map. Translations carry basic cosets to basic cosets and their inverses do the same.

For distinct s,t choose k in s+t. The cofinite A=N minus {k} is in U. If (s+H_A) and (t+H_A) intersected, s+t would be in H_A, contradicting k in s+t. These are disjoint open neighborhoods, proving Hausdorffness. Each A in U is infinite; H_A contains infinitely many singletons. Every basic coset is therefore infinite. An open singleton would contain a basic coset, impossible. The group is nondiscrete. Each coset is also closed since its complement is a union of other cosets of the same subgroup.

### 3. Exactly countably infinitely many dense pieces

For j in N put D_j={s in G : v_2(|s|+1)=j}. Because |s|+1 is a positive integer with exactly one finite 2-adic valuation, these are disjoint and cover G; 0 is in D_0. Fix j, s in G, A in U. The integers

    q = 2^j(2r+1)-1, r in N,

are nonnegative, unbounded, and have v_2(q+1)=j. Choose q at least |s|. Since A minus s is infinite, it has a finite subset t of the prescribed nonnegative size q-|s|, including t empty when that size is 0. Then t is in H_A, s and t are disjoint, and s+t=s union t has size q. Thus (s+H_A) intersects D_j.

This proves density in every basic coset, not just in identity neighborhoods, and hence density in every nonempty open set. It also proves every D_j is nonempty (apply the argument to G itself). The partition has exactly countably infinitely many pieces. Neither closure of D_j under the group operation nor any compatibility of the coloring with homomorphisms is required by the question. The countably many distinct j are all realized, even if s contains coordinates outside A: those coordinates are preserved by adding t inside A.

### 4. The finite-fiber obstruction and its quantifiers

Take an arbitrary sequence (F_n) of pairwise disjoint finite subsets of G. If infinitely many blocks are empty, G is a fixed nonempty open set missing those blocks, so the sequence fails the desired property.

Otherwise, only finitely many blocks are empty; remove a finite initial segment beyond all their indices. Because the blocks are disjoint, 0 belongs to at most one block. Remove another finite initial segment beyond its index if it exists. The remaining index set is a full infinite tail, and every member of every remaining block is a nonempty support. This removal neither assumes a uniform block-size bound nor changes the fact that infinitely many later indices would refute eventual intersection for the original sequence.

Define M_n={max(s):s in F_n} on this tail. Each M_n is finite and nonempty. For each k there are exactly 2^k nonempty supports with maximum k, obtained by adjoining k to an arbitrary subset of {0,...,k-1}. Since a support appears in at most one block, k belongs to M_n for at most 2^k different indices. Different elements in the same block can have the same maximum; treating M_n as a set simply removes duplicate values and does not invalidate this upper bound. Different blocks can also repeat a maximum; this is why the argument needs point-finiteness, not a false claim of initial disjointness of the M_n.

Here is the thinning lemma with its full proof. An infinite sequence of nonempty finite sets (M_n), each coordinate belonging to only finitely many M_n, has an infinite subsequence of pairwise disjoint sets with increasing indices. Suppose n_0<...<n_(r-1) have been selected. Their union V is finite. For each k in V only finitely many indices n have k in M_n, and the union of these finitely many finite forbidden index sets is finite. There are infinitely many later indices, so choose one outside this finite forbidden set. Its M_n avoids V. Starting with any first index and taking the least eligible later index each time yields an infinite sequence without any additional choice principle. All chosen n_i are strictly increasing and therefore unbounded.

Let C_0 be the union of M_(n_i) over even i and C_1 the analogous odd union. They are disjoint (and both infinite, though infinitude is not needed for the filter contradiction). They need not cover N, and the proof does not pretend that they do. A proper filter cannot contain both because their intersection is empty. Choose e in {0,1} for which C_e is not in U; there may be two such choices. By the ultrafilter decision, A=N minus C_e belongs to U. This is a single A chosen after the entire block sequence and the thinning have been fixed.

For every i of parity e and every s in F_(n_i), max(s) is in C_e. Thus s is not a subset of A. Equivalently, s is not in H_A. Therefore the fixed nonempty open neighborhood H_A misses every F_(n_i) of this parity. That is an infinite unbounded set of original indices. In symbols the proof gives

    for every block sequence F, there exists A in U such that for every m,
    there exists n>m with F_n intersect H_A empty.

It does not merely give a different neighborhood for each missed block. The finite-tail removals preserve this displayed conclusion. This negates exactly the target eventual-intersection conclusion. The construction is therefore a valid counterexample under the stated ZFC and nonempty-open conventions.

## Direct line-by-line assessment of the submitted REPORT.md

Line references refer to the authenticated 105-line candidate, not to a later edited rendering.

| Candidate lines | Independent test and disposition |
|---|---|
| 1–5 | Mathematical title and ZFC target agree with the theorem above. Authorship/independent-development claims are historical assertions, not established by this proof audit. One topology mechanism is correctly distinguished from finite tests. |
| 7–11 | Scope matches primary 21.107. Nonempty opens is the substantive intended reading. The stronger infinite partition avoids ambiguity of countably many. No metric/first-countability hypothesis appears in the printed problem. |
| 13 | Printed location and absence of a solution annotation at 21.107 are directly visible in v48. Predecessor and repository/history observations remain bounded bibliographic claims, not needed for the deduction; defer checking them to the post-boundary source intake. No current-open or priority inference is accepted here. |
| 15–23 | Zorn/filter argument is valid and uses no special ultrafilter property. See reconstructed proof 1 for the generated-filter step expanded. No hidden countable-intersection assumption. |
| 25–37 | G is countably infinite, each H_A is a subgroup, and arbitrary intersecting cosets have the claimed intersection. All base axioms pass. |
| 39 | Addition is jointly continuous by the displayed product neighborhood; inversion is the identity. No semitopological-only gap. |
| 41 | Cofinite coordinate exclusion gives disjoint neighborhoods. Infinitude of all basic cosets proves nondiscreteness. The closed-coset observation also holds. |
| 43–59 | Every color has unbounded available support sizes; additions in A minus s realize them in every coset. Identity color and q=|s| cause no exception. Exactly infinitely many nonempty dense pieces are proved. |
| 61–65 | Arbitrary finite blocks, potentially non-covering and of unbounded sizes, are covered. Infinitely empty blocks give a fixed open G; otherwise finite initial-segment removal is legitimate. Identity occurs in at most one block. |
| 67–71 | Maxima exist after that removal. The finite fiber has size exactly 2^k, including k=0 with one support {0}. Point-finiteness follows; pairwise disjointness of maxima before thinning is neither asserted nor needed. |
| 73 | Greedy finite-exclusion proof works for every point-finite sequence of finite nonempty sets. Strictly later indices remain. No Ramsey/selective thinning enters. |
| 75–83 | Disjoint C_0,C_1 cannot both be filter members. They are not assumed complementary. For a nonmember its complement is in U; this is the exact ultrafilter use. |
| 84–90 | Every support in each chosen parity block has an excluded coordinate. One fixed H_A misses infinitely unbounded original indices. This is the needed negation, including all tail issues. |
| 92–96 | The computation limitation is correct. ZFC ultrafilter existence is nonconstructive; finite principal-ultrafilter computations cannot certify it. Lineage naming is a separate attribution claim to check after this independent document is saved. |
| 98–105 | Approach count and publication disclaimers do not add mathematical premises. Bibliographic existence/priority is not certified by the proof. |

No required mathematical correction was found in lines 15–90. The strongest verified result is the complete stated counterexample in ZFC, including Hausdorffness and the infinite dense partition. This is a mathematical validity conclusion, not acceptance, publication, priority, or independent human confirmation.

## Boundary falsification and limiting cases

1. **An arbitrary free filter is not enough for the obstruction.** Use the cofinite filter instead of U. The same coset topology is Hausdorff and nondiscrete, and the same D_j are dense, but it has an explicit expansive sequence: L_n={s in G:max(s)=n}. These blocks are finite (2^n elements), nonempty, pairwise disjoint and cover G except 0. Given a cofinite A and a coset s+H_A, choose n larger than every member of s and every member of N minus A. Then s+{n} belongs to that coset and to L_n, for every such n. Thus L_n eventually hits the coset. This detects the exact failure of the parity step for a general free filter: neither complement of the two infinite parity unions need be cofinite. I do not claim that an ultrafilter is a necessary condition for every conceivable obstruction, only that replacing U by the cofinite filter falsifies this construction's conclusion.

2. **A principal ultrafilter does not model this example.** At k its smallest permitted A is {k}, so H_{ {k} }={0,{k}} is a two-point open neighborhood. The resulting topology cannot separate 0 from {k}. Moreover, infinitely many disjoint dense pieces cannot each meet that two-point open set. Freeness is therefore needed for the intended hypothesis and separation, and a finite principal simulation is not evidence for the free case.

3. **Dropping all incidence restrictions makes the obstruction impossible.** Enumerate G as g_0,g_1,... and take E_n={g_0,...,g_n}. For any topology and any nonempty open O, choose g_k in O; every E_n for n at least k meets O. These are finite blocks which deliberately repeat points. Thus the theorem does not say that arbitrary finite selections fail; disjointness or the stronger proved incidence condition below is substantive.

4. **No hidden uniform bound or cover.** Each original F_n need only be finite individually. Their union need not equal G. The proof uses a finite union of selected finite M_n at each step and the finite fibers of max, never a bound shared across n or an enumeration exhausted by the blocks.

5. **Finite countability and empty-open ambiguities are bypassed.** A countably infinite Hausdorff example with infinitely many nonempty dense pieces satisfies the strongest natural reading of the antecedent. Its failing open H_A contains 0 and infinitely many other points. The argument has no dependence on those wording ambiguities.

6. **The nonmetrizable scope is real.** The additional consequence below implies the example is not first countable. A metric restriction would materially change the problem; it cannot be imported into primary 21.107.

## Stronger deductions, scoped and completely proved

These are deductions of the same mechanism for checking robustness, not a novelty claim or an extra mechanism.

**Point-finite block strengthening.** In the group above, the same obstruction holds for every sequence of finite sets E_n such that each g in G belongs to only finitely many E_n; the E_n need not be pairwise disjoint. Proof: infinitely empty blocks are handled as above. Otherwise remove a finite initial segment beyond all empty indices and all occurrences of 0, which are finite by assumption. For each k the max-fiber has only 2^k supports; each such support appears at finitely many indices, so the union of their occurrence sets is finite. Thus the maxima sets are point-finite. The thinning, parity split and one fixed H_A apply without alteration. No uniform bound on point multiplicities is needed.

**No non-eventually-constant convergent sequences.** If a sequence converges to x in this Hausdorff group, translate it by x. Every fixed nonzero g occurs only finitely often: choose a neighborhood of 0 missing g, using Hausdorffness. If infinitely many terms were nonzero, infinitely many distinct nonzero terms could be selected in increasing order; otherwise a finite union of finite occurrence sets would contain all those infinitely many indices. The singleton blocks of such an injective subsequence are pairwise disjoint. The main obstruction supplies an open neighborhood of 0 missed by infinitely many of them, contradicting convergence. Hence the translated sequence is eventually 0, and the original is eventually x.

**Not first countable and hence not metrizable.** Suppose there were a countable neighborhood base at 0. Replace it by the nested finite intersections B_n of its first n members. Each B_n is an open neighborhood and is infinite, by the topology already checked. Choose x_n in B_n avoiding 0 and all previously chosen x_i. The resulting distinct sequence converges to 0 because every neighborhood contains some B_m and every x_n for n at least m lies in B_m. This contradicts the preceding deduction. Thus no countable local base exists. Any metric has the balls of radius 1/n as a local base, so a metric is impossible.

## Mechanism/status/exact-gap ledger at this phase boundary

| Family / attack | Mechanism and evidence | Status | Exact remaining gap |
|---|---|---|---|
| Free-ultrafilter existence | Zorn extension of cofinite filter, explicit decision proof | Complete in ZFC | No claim in ZF; no constructive ultrafilter produced |
| Joint group topology / separation | Subgroup intersections, product neighborhoods, cofinite coordinate exclusion | Complete | None for stated topology |
| Infinite dense partition | Unbounded support-size fibers, finite additions avoiding original support | Complete | None; no subgroup-color requirement imposed |
| Universal obstruction | Finite max fibers, point-finite greedy subsequence, two disjoint unions, U complement | Complete | None for pairwise disjoint finite blocks |
| Hidden special ultrafilter properties | Every infinite step reduced to a finite exclusion; only ordinary complement decision used | Attack did not falsify | No selective/Ramsey/rapid/P-point assumption found |
| Cofinite-filter replacement | Explicit expansive max layers | Falsified as a stronger replacement claim | Cannot reopen that replacement without a new mechanism |
| All finite-block sequences without point-finiteness | Exhausting initial segments of enumeration | Falsified as an overextension | No obstruction possible in that generality |
| Point-finite strengthening | Finite union of finite occurrence sets per max fiber | Complete scoped strengthening | No priority claim |
| Prior lineage / exact earlier solutions | Not a mathematical premise; source identity only established for question | Deferred | Requires post-boundary primary reading and separate priority audit |
| Original old-audit qualifications | Their contents intentionally unread at this phase | Deferred | Must independently adjudicate after this document is saved |

No route is being called successful merely by transferring the main claim to an unsupported equivalent lemma. The finite-thinning lemma and filter argument are proved in full. No finite test is being used to establish a universal quantifier.
