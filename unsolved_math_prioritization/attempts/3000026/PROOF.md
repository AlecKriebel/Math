# Complete round-robin 3–1–0 recognition: partial result

Target: 3000026 / AMR-029-0026. Public prose edition of the complete mathematical report and correction note.

This AI-assisted manuscript is unrefereed. Acceptance refers to an internal AI mathematical audit, not external human peer review, journal acceptance, or formal proof-assistant certification. This is not a computational reproduction package. Novelty and priority are unestablished; no exhaustive current-openness claim is made.
Date: 2026-10-11. Status: **partial; the unrestricted complexity question is not solved**.

## 1. Exact target and separation from prior results

Input is an integer vector s=(s_1,...,s_n), n>=1. Every unordered pair of distinct teams plays exactly once. Its two scores must be (3,0), (0,3), or (1,1). Decide whether the full vector can occur. There are no prescribed results or arbitrary host graph. Sorting only relabels teams.

A full positive answer requires an algorithm polynomial in the input length for every vector. No such algorithm is established here. A complexity lower bound would have to preserve this complete-host restriction; even NP-completeness would imply absence of a polynomial algorithm only under P!=NP. The alternatives P and NP-complete are not logically exhaustive without additional assumptions.

Prior sources:
- The original [Egres statement](https://lemon.cs.elte.hu/egres/open/Deciding_the_validity_of_the_score_sequence_of_a_soccer_tournament) is revision 594, dated 10 November 2009. It distinguishes the original problem from prescribed-result and elimination variants.
- Iványi–Schoenfield, [Deciding football sequences](https://arxiv.org/abs/1207.6384), arXiv v1 (2012), provides rejection filters and exponential exact algorithms. The inspected pp. 164–169 already show that a draw degree sequence does not determine a usable draw graph. This phenomenon is not new here.
- Pálvölgyi, [Deciding Soccer Scores and Partial Orientations of Graphs](https://domotorp.web.elte.hu/cikkek/soccer.pdf), inspected author manuscript pp. 1–2, defines its hard score-vector problem using a prescribed graph of matches. Its hardness is not a proof for the complete-host target.
- Pirzada–Samee–Naikoo, [Tournaments, oriented graphs and football sequences](https://emis.de/ft/40409), Acta Univ. Sapientiae Mathematica 9(1) (2017), 213–223, DOI 10.1515/ausm-2017-0014, uses the oriented-graph score identity below. The correction note included below corrects the direction of its printed Theorem 9.

The authored work here is a self-contained derivation of a bounded-decisive-match kernel, an exact parameterized search, and explicit route obstructions. Novelty is unestablished: bounded searches found no matching kernel result or published correction, which does not certify priority. The unrestricted problem's current worldwide status is also not certified by this search.

## 2. Draw graphs: an exact criterion and its unresolved choice

Write N=n(n-1)/2, S=sum_i s_i, k=3N-S and m=S-2N. In any realization k is exactly the number of drawn matches, m the number of decisive matches, and k+m=N. Reject out-of-range scores or k,m outside [0,N].

Fix a simple graph D on the teams and declare its edges to be precisely the draws. Put d_i=deg_D(i), H=K_n-D, and w_i=(s_i-d_i)/3.

**Fixed-draw criterion.** D extends to a realization if and only if:
1. Each w_i is an integer with 0<=w_i<=n-1-d_i.
2. sum_i w_i=|E(H)|.
3. For every vertex subset U, sum_{i in U}w_i >= |E(H[U])|.

Proof. Orient each decisive match from its winner to its loser. Internal edges of U account for |E(H[U])| wins within U, proving necessity. For sufficiency, make one unit-demand node per decisive edge, with its two endpoints as the allowed recipients. Team i has w_i recipient slots. Any collection A of edge nodes has endpoints in a set U; hence |A|<=|E(H[U])|<=sum_{i in U}w_i. The usual augmenting-path matching argument therefore assigns each edge to a slot at one endpoint. Equivalently, source-to-edge, edge-to-endpoint, and endpoint-to-sink arcs give an integral maximum flow. Total capacity equals the number of edges, so every team receives exactly its prescribed number of wins. Add the draws. This is precisely the desired score vector. QED.

The condition has a polynomial-time test and a reconstructible match certificate; it does not require enumerating all subsets. With e_D(U) internal draw edges and c_D(U) draw edges crossing its boundary, condition 3 is equivalently

s(U)+e_D(U)-c_D(U) >= 3*binom(|U|,2).

Searching all k-edge draw graphs gives an exact algorithm with at most binom(N,k) polynomial-time flow tests, hence an XP algorithm in the draw count k. This is not fixed-parameter tractability in k, and it is not a polynomial-time solution when k varies.

**Known obstruction to discarding the draw graph.** For s=(1,1,7,7), all draw degrees are 1. Draws {12,34} work, whereas draws {14,23} do not: teams 1 and 2 would then have to play a decisive game even though neither has any wins. This example is explicitly present in the 2012 paper, p. 167. Graphical draw degrees, local quotas, and their total are insufficient to replace the flow test.

## 3. A kernel parameterized by the number of decisive matches

Set delta_i=s_i-(n-1). In the oriented graph of decisive matches,

 delta_i = 2 w_i - l_i,

where w_i and l_i count wins and losses. Summing shows that the number of arcs is m=sum_i delta_i. This identity is standard and also appears in the 2017 source; it is not claimed as a new fact.

For a nonzero integer t, let

 h(t) = -t if t<0;
 h(t) = ceil(t/2)+(t mod 2) if t>0.

It is the smallest possible w+l with w,l>=0 integers and 2w-l=t. Indeed l=2w-t and w+l=3w-t, minimized at w=max(0,ceil(t/2)). A vertex with delta=0 that is incident to any decisive match satisfies l=2w and w>=1, so it has degree at least 3.

Let Q={i:delta_i!=0}, q=|Q|, z=n-q, and B=sum_{i in Q}h(delta_i). If B>2m, reject. If m=0, accept exactly when all delta_i=0, since every match must be a draw.

For m>=1 and B<=2m, put

 a = min(z, floor((2m-B)/3)).

Keep every vertex in Q and any a of the zero-delta vertices. Delete the other r=n-q-a zero-delta vertices, subtract r from each retained score, and call the resulting vector s'. Reject if it has a score outside [0,3(|s'|-1)].

**Kernel theorem.** The original vector is realizable if and only if s' is realizable. The retained vector has at most 2m entries and preserves m.

Proof, forward. In a realizing decisive graph the total degree is 2m. Nonzero-delta vertices consume at least B, and each active zero-delta vertex consumes at least 3. At most a zero-delta vertices can therefore be active. All zero-delta teams have the same prescribed original score n-1. Permuting their labels preserves the input vector, so move every active zero-delta vertex into the chosen retained set. The deleted vertices are now isolated in the decisive graph and drew every game. Removing them subtracts exactly r points from each retained team, giving a realization of s'.

Proof, reverse. Add the r deleted teams, declaring every new match a draw. Every retained score increases by r. Each new team gets n-1 points, its required original score. This reconstructs the input.

Size and parameter. Every h(t) for t!=0 is at least 1. Thus q+a<=B+3a<=2m. The new deviations are unchanged because s_i-r-(n-r-1)=delta_i. Deleted deviations were zero, so m is preserved. Valid reduced scores are at most 3(2m-1), yielding O(m log(m+1)) bits for the reduced vector. QED.

For a simpler bound one may merely retain enough zero-delta teams to bring the total to 2m. The sharper incidence-budget reduction above explains when zero-delta teams really must be retained. It is unsound to delete all of them: (2,3,5,5) is realizable, but deleting its 3-point team and shifting the other scores gives the impossible vector (1,4,4).

**Exact FPT algorithm.** After the reduction, let r'<=2m be the number of retained teams. Enumerate every m-edge subgraph of K_{r'}, then all 2^m orientations. Test the resulting deviations. The search has at most

 binom(binom(2m,2),m) * 2^m <= (4 e m)^m

candidates for m>=1, with a polynomial factor for evaluating each. Thus recognition is in time 2^{O(m log(m+1))} times a polynomial in the original input length, with an explicitly reconstructible tournament when accepted. The m=0 case is handled separately. If m exceeds binom(r',2), no search candidate exists and the instance is rejected.

The support bound 2m is sharp for deletion of only all-draw teams while preserving all nonzero deviations: m disjoint decisive games have deviations consisting of m copies of 2 and m copies of -1, all on distinct active teams. Additional all-draw teams may be padded arbitrarily.

**Small-m corollary.** Ignoring zero entries and ordering, the possible deviation vectors are:
- m=0: the empty list.
- m=1: (-1,2).
- m=2: (-1,-1,2,2), (-1,-1,4), (-2,2,2), or (-1,1,2).

These follow from the four possible forms/orientations of two distinct decisive edges: disjoint, common winner, common loser, or a directed path. Conversely each listed pattern is realized by that graph, with zero-delta teams added as all-draw teams. This is a restricted classification, not a replacement target.

## 4. Convexity obstruction

For every n>=2 the integer vector

 (n,n-1,...,n-1)

is impossible: it has m=1 but lacks the mandatory deviations (2,-1). Yet it is a convex combination of feasible vectors. Have all games drawn except game 12. Let x be the score vector when team 1 wins, and y when team 2 wins. Then (2x+y)/3 equals the displayed impossible vector.

Therefore the feasible integer vectors have holes in their convex hull. No system of linear inequalities solely in the score coordinates can characterize the feasible integer score vectors by membership: such a system would contain this convex combination. This also blocks exact recognition by merely testing the continuous projection of a linear extended formulation. It does not preclude integer auxiliary variables, nonlinear tests, or a polynomial combinatorial algorithm. This obstruction concerns labeled score coordinates and pure continuous linear feasibility/projection. Sorting or other nonlinear preprocessing, and arbitrary Boolean combinations of inequalities, are outside this claim.

## 5. Validation and precise remaining gap

The authored programs never execute scholarly-source code. Independent direct enumeration of every match outcome for n<=5 is compared with the draw-graph/flow recognizer on all 6,998 sorted score vectors in range, including 6,593 impossible vectors. Counts of feasible sorted vectors are 1,2,7,40,355; these counts are prior known values, reproduced as regressions. The kernel's equivalence is checked against those exact oracles, with direct kernel-search witness checks for n<=4 and all n=5 vectors with m<=2. Additional label-permutation checks, every fixed-host orientation quota within degree bounds for n<=4, and semantic negative controls are recorded separately. All tests run under ordinary Python, -O, and -OO, using explicit failure guards rather than assertions.

The mathematical proofs above establish the partial claims; finite computations do not establish unrestricted correctness or novelty on their own. At the time the original report was sealed, no independent audit had yet accepted it. The subsequent internal AI mathematical audit in AUDIT.md accepts the scoped partial results and correction. External human peer review has not been claimed.

The remaining obstruction is substantive: the unknown draw graph must be selected in a way compatible with all orientation constraints. Enumerating it is exponential in general; the alternative decisive-graph kernel is useful only when m is small and may leave Theta(n) teams in the dense regime. No complete-host hardness reduction or input-polynomial recognition mechanism has been found. The original target must remain **partial/unsolved by this attempt**, not candidate full resolution.

# Counterexample to the printed sufficiency direction in Theorem 9

Source: S. Pirzada, U. Samee and T. A. Naikoo, [Tournaments, oriented graphs and football sequences](https://emis.de/ft/40409), Acta Universitatis Sapientiae, Mathematica 9(1) (2017), 213–223, DOI [10.1515/ausm-2017-0014](https://doi.org/10.1515/ausm-2017-0014). This note concerns the displayed Theorem 9 on p. 220 and its proof on pp. 220–221, not the paper as a whole.

## Exact scope

In the paper's Section 2, an oriented edge records a win and its absence a draw. The score is f_i=n-1+2w_i-l_i. Page 219 defines a transmitter as a vertex of indegree zero, equivalently a team with no losses.

Theorem 9 is stated for a vertex in an oriented graph. Its printed direction says that a team is a transmitter if n and its score have different parity and the score is congruent to both n-1 and 3(n-1) modulo 2. These conditions are redundant: all say f_i congruent to n-1 modulo 2. They are necessary, but not sufficient, for zero losses. The proof begins by assuming the vertex is a transmitter, so establishes the opposite implication.

This is not an assertion that a given scalar score can be achieved undefeated in some unspecified tournament. That different scalar-existence question is true precisely for the scores n-1,n+1,...,3(n-1). The counterexample below also rules out an undefeated realization of an entire fixed score vector, a stronger interpretation than needed to refute the printed statement about a given graph.

## Explicit four-team counterexample

Teams are A, B, C, D. A beats B, loses to C and D, and the other three games are draws:

- A–B: (3,0)
- A–C: (0,3)
- A–D: (0,3)
- B–C: (1,1)
- B–D: (1,1)
- C–D: (1,1)

The labeled score vector is (3,2,5,5), or (2,3,5,5) when sorted. Team A has n=4 and f_A=3, so the parities differ, 3 is congruent to n-1=3 modulo 2, and 3 is congruent to 3(n-1)=9 modulo 2. Nevertheless A has two losses and is not a transmitter.

Indeed the 3-point team cannot be a transmitter in *any* realization of this full score vector. If unbeaten, its three games would all be draws: the unbeaten score formula is 3+2w, and score 3 forces w=0. Deleting it would leave scores (1,4,4) on three teams. Their sum is 9, which forces all three remaining games to be decisive. Each score would then be a multiple of 3, a contradiction. Thus the counterexample is not explained away by changing the realization while preserving the full score vector.

## Correct replacement

For any team,

 f_i-(n-1)=2w_i-l_i,
 so l_i is congruent to n-1-f_i modulo 2.

Consequently:
- If f_i and n have the same parity, the team has an odd, hence positive, number of losses. This agrees with the paper's Lemma 2.
- If f_i and n have different parity, the number of losses is even. It may be zero or positive.
- A transmitter necessarily has f_i in {n-1,n+1,...,3(n-1)}. For a transmitter the exact counts are w_i=(f_i-(n-1))/2 and d_i=(3(n-1)-f_i)/2. These are nonnegative, not necessarily positive, integers.

The minimal textual repair to the theorem's implication is to replace its sufficiency claim by necessity. The parity identity above gives the precise stronger statement. No parity-only sufficiency statement for the vertex of a prescribed tournament or prescribed full score vector survives.

## Verification and limits

The article was inspected as a published journal contribution in a 272-page issue retained from the Hungarian Academy repository, and its page 220 was visually rendered. An independently opened EMIS article PDF has 11 pages and the same printed statement. Complete issue retrieval does not mean the whole issue was read; the decisive inspection covers the article's title/definitions and pp. 218–221.

The independent finite verifier enumerates all 729 labeled four-team tournaments, validates the six listed match outcomes, and confirms there is exactly one labeled realization of (3,2,5,5); its A team loses twice. It also checks the corrected balance and parity identities on every team of those 729 tournaments. The handwritten argument, rather than exhaustive computation, proves that no undefeated realization exists.

Bounded searches for the title with correction/erratum and for the theorem and transmitter did not locate a prior correction. Novelty and priority are unestablished. This narrow correction does not answer the general polynomial-time recognition question.
