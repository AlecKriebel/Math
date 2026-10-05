# Spread bounds for the random triangle removal process

## Conclusion

Problem 30005114, OWR-10252930-024, is not resolved by this investigation. The original problem asks for a conditional C/n inclusion bound for every prescribed triangle family, with one constant and one high-probability conditioning event. Dense families with quadratically many triangles remain outside the sharp bound proved here.

The proved scoped results are:

1. One high-probability event gives an O(n^(-0.98))-spread bound for all families and all k.
2. On the same event, the bound (4/n)^k holds whenever the graph formed by the prescribed triangles has maximum degree at most n p_m^2/10. In particular it holds for every family with k <= n p_m^2/20, and for some much larger sparse families.
3. An exact dense-family example shows why the particular potential used for result 2 cannot simply be extended to all families. It is not a counterexample to the problem.

All asymptotic assertions concern sufficiently large n. The quasirandomness input is an explicitly cited existing theorem; its full proof is not re-proved here. The remaining arguments are supplied below. No novelty or priority claim is made. Computational checks supplement these arguments and do not replace them.

## 1 The target and its normalization

Start with the graph G_0=K_n. At each step choose uniformly from its current triangles and delete the three edges of the selected triangle. Write T_m for the set of selected triples after

    m = floor(n^2/6 - n^(199/100))

steps. If the process ends before m, keep its final output as a failure convention. The event used below excludes that outcome. The floor is an explicit integer convention for the source's real-valued stopping expression. Indeed, this expression becomes positive only for extraordinarily large n; all small-n computations below are separate process checks, not simulations at this stopping time.

For a deterministic family F of k distinct triples, the target is the existence of C independent of n,k,F and events E_n independent of F such that P(E_n)=1-o(1) and

    P(F subset T_m | E_n) <= (C/n)^k.

The source is Mehtaab Sawhney's Problem 6, printed page 1226 of [OWR]. It explicitly allows k growing as far as order n^2 and notes an easier small-k range. The imported clean statement has the correct mathematical target. The imported original extraction mixes neighboring questions; the primary page controls. In particular the polynomial Hales-Jewett remark belongs to the preceding problem, not this one.

Triangles in F may share vertices. If two share an edge, the event has probability zero. Thus the only nontrivial families are edge-disjoint triangle packings. Their edge-shadow U(F) is the simple graph consisting of all 3k covered edges; write Delta(F) for its maximum degree. Necessarily k<=m for a positive event probability. The case k=0 is exactly 1.

This is spread on the ground set of unordered triangles, not graph edges. Conditioning can be on a global trajectory event. It must not be chosen separately for each F, and a proof only for fixed k would not settle the problem.

For any permutation-invariant event E on which exactly m triangles are selected, symmetry and summing indicator variables give, for every fixed triangle T,

    P(T in T_m | E) = m / binom(n,3).

Thus the normalization is asymptotically 1/n. Even without permutation invariance, the average marginal is m/binom(n,3); any uniform proposed constant must be at least 1 asymptotically.

## 2 The common trajectory event

For 0<=i<=m put

    p_i = 1 - 6i/n^2,       Q_i = number of triangles of G_i,
    Y_uv(i) = |N_Gi(u) intersect N_Gi(v)|.

Here p_i is the standard trajectory parameter, not the exact graph edge-density: the exact edge count is (n^2 p_i-n)/2. Set E_n to be the event that the process reaches m and, for every 0<=i<=m,

    Y_uv(i) >= (99/100) n p_i^2 for every pair u,v,
    (99/100) n^3 p_i^3/6 <= Q_i <= (101/100) n^3 p_i^3/6.

This event does not depend on F or k, and is invariant under vertex permutations. Its probability tends to 1 by the codegree and triangle-count estimates of Bohman, Frieze and Lubetzky [BFL], Theorems 2.1 and 2.2 and their combined consequence at the end of Section 2. Take their fixed parameter M=3. Their trajectory range includes p>=n^(-1/6), while

    p_m = 6 n^(-1/100) + O(n^(-2)),

which is larger for sufficiently large n. Their relative errors tend to zero uniformly in our range. The positive lower bound for Q ensures the process remains active. This is the sole probabilistic concentration input to the partial results.

For every sufficiently large n, P(E_n)>=1/2. All probability calculations below are performed for the original, unconditioned Markov chain killed at its first violation of the trajectory bounds. The division by P(E_n) is made only at the end. In particular, no invalid claim is made that the next triangle stays uniform after conditioning on a future event.

## 3 An all family bound from triangle counts

### Proposition 1

With E_n as above, uniformly over all distinct families F of size k>=1,

    P(F subset T_m | E_n)
      <= [ (100/(99n)) (p_m^(-2)-1) ]^k
      = O(n^(-0.98))^k,

where the O constant is absolute and independent of k.

### Proof

Let q_i=(99/100)n^3p_i^3/6. Assign distinct selection times in {0,...,m-1} to the labeled triangles of F. At any assigned time, conditional on a history not yet killed, the probability of selecting its specified triangle is either zero or 1/Q_i<=1/q_i. Recursion over the assigned times, killing whenever a bound first fails, gives a product upper bound. This is a statement about the joint event of the assignments and E_n, not a conditional transition law given E_n.

Sum over all injections from F to the time set. With a_i=1/q_i this yields

    P(F subset T_m, E_n) <= k! e_k(a_0,...,a_(m-1))
                           <= (sum_(i=0)^(m-1) a_i)^k.

The last inequality includes repeated time assignments as additional nonnegative terms. If k>m there are no injections and the left side is zero. Since the function (1-6x/n^2)^(-3) is increasing,

    sum_(i=0)^(m-1) p_i^(-3)
       <= integral_0^m (1-6x/n^2)^(-3) dx
       = (n^2/12)(p_m^(-2)-1).

Therefore the joint bound is [50(p_m^(-2)-1)/(99n)]^k. Divide by P(E_n)>=1/2 and use 2<=2^k. Finally p_m is asymptotic to 6n^(-0.01), so the base has order n^(-0.98). This proves the claimed uniform all-k bound. It is weaker than C/n by a polynomial factor and does not resolve the problem.

## 4 Protected edges and the sharp sparse family bound

Suppose F is edge-disjoint and its inclusion has not yet become impossible. At a given time let R be its r still unselected triangles and let U be their edge-shadow. All edges of U are present. A current triangle is called bad if it is not in R but shares an edge with U. Selecting it makes the desired event impossible. Let b be the number of bad triangles, d a lower bound on current codegrees of protected edges, and Delta an upper bound on the maximum degree of U.

### Lemma 2 The two hazard estimates

    b >= r(d-1),                 b >= 3r(d-Delta).

For a bad triangle S, let a(S) count its protected edges. Then 1<=a(S)<=3. Summing codegrees over the 3r protected edges and subtracting the three contributions of each target gives

    sum_bad a(S) >= 3r(d-1).

Since a(S)<=3, the first inequality follows. For the second, use

    b >= sum_bad [a(S)-binom(a(S),2)].

Indeed the bracket equals 1,1,0 for a=1,2,3. Each pair of protected edges of a triangle is a wedge in U, whence

    sum_bad binom(a(S),2)
       <= sum_v binom(deg_U(v),2)
       <= (Delta-1)|E(U)| = 3r(Delta-1).

Subtracting proves b>=3r(d-Delta). Both estimates are deterministic and make no independence assumption.

A useful second proof of a weaker all-family result now follows. Put d_*=(99/100)n p_m^2. Let s_i count selected targets. Give a live, unspoiled trajectory weight d_*^(s_i), and give a killed or spoiled trajectory weight zero. Its expected multiplier is at most

    1 + [r(d_*-1)-b]/Q_i <= 1.

Completion has weight d_*^k, so P(F subset T_m,E_n)<=d_*^(-k). Dividing by P(E_n) gives (2/d_*)^k. This again has base O(n^(-0.98)), now without needing a lower bound on Q.

### Theorem 3 The bounded shadow degree estimate

For every sufficiently large n and every distinct family F of k triangles with

    Delta(F) <= n p_m^2/10,

one has

    P(F subset T_m | E_n) <= (4/n)^k.

The same E_n works for all such families simultaneously, in the sense that every one of their conditional probabilities satisfies this inequality. There is no union bound over families and no restriction that k be fixed.

### Proof

The edge-overlapping case is zero, so assume F is edge-disjoint. Set

    w_i = 2/(n p_i^2).

On a trajectory that is neither killed nor spoiled, with r_i remaining targets, define Z_i=w_i^(r_i); otherwise define Z_i=0. If all targets have been selected and E_n occurs, Z_m=1. We prove Z_i is a nonnegative supermartingale. At a live history with r=r_i>=1 let Q=Q_i, b be as in Lemma 2, w'=w_(i+1), and a=w_i/w'=(p_(i+1)/p_i)^2. Ignoring a possible further killing can only increase the next weight. Exactly r next selections succeed in removing one target, b spoil the event, and all others preserve r. Hence

    E[Z_(i+1) | history]
       <= (w')^r [1-r(1+b/r-1/w')/Q].                  (1)

The remaining shadow is a subgraph of U(F). Since p_i>=p_m, Lemma 2 gives

    b/r >= 3[(99/100)n p_i^2 - n p_m^2/10]
           >= (267/100)n p_i^2.

Also 1/w'=n p_(i+1)^2/2 <= n p_i^2/2. Thus

    1+b/r-1/w' >= 1+(217/100)n p_i^2.                (2)

Writing h=6/n^2, the trajectory upper bound yields

    Q(1-a)
      <= (101/100)(n^3 p_i^3/6)[2h/p_i-(h/p_i)^2]
      <= (202/100)n p_i^2.                          (3)

Equations (2) and (3) imply (1+b/r-1/w')/Q >= 1-a. Substitution into (1), followed by Bernoulli's inequality a^r>=(1-r(1-a)) for 0<a<=1, proves

    E[Z_(i+1) | history] <= (w')^r[1-r(1-a)]
                         <= (w')^r a^r = Z_i.

For r=0 the weight is 1 until it is possibly killed, so the same conclusion holds. A killed or spoiled trajectory stays at zero. Consequently

    P(F subset T_m,E_n) <= E[Z_m] <= Z_0=(2/n)^k.

Divide by P(E_n)>=1/2 and absorb the factor 2 as 2^k for k>=1. The k=0 case is immediate.

### Scope of Theorem 3

Always Delta(F)<=2k. Therefore it proves the requested C/n estimate for every family in the growing range k<=n p_m^2/20, which is of order n^0.98. It also permits much larger families: a union of disjoint complete graphs of order proportional to n^0.98, each triangle-decomposed, can have order n^1.98 targets while respecting the degree restriction. This observation is about the theorem's scope and is not a novelty comparison with the literature.

The full problem includes families with Delta(F) of order n and k of order n^2. Those are not covered. The loss in Proposition 1 is not removed for those families.

## 5 Two tests of tempting extensions

### Negative dependence is not available automatically

For the process on K_5 run to its natural end, exactly two triangles are selected. There are 15 edge-disjoint unordered pairs, each with probability 1/15: the first triangle is uniform among 10, and it leaves exactly three choices for the second. A fixed triangle has marginal 1/5. For F={012,034}, the joint probability is 1/15, strictly exceeding 1/25, the product of the marginals. Thus universal negative correlation of triangle inclusion indicators is false for this process. This small-n terminal example does not refute the asymptotic conditioned assertion.

### The sparse family potential fails for dense families

Take n=2s where s is admissible for a Steiner triple system, and prescribe a triangle decomposition F of a clique on s vertices. Then

    r=s(s-1)/6,
    b=binom(s,3)+binom(s,2)(n-s)-r = r(3n-2s-3).

These are exact initial-state counts. For the potential in Theorem 3, before trajectory killing, the ratio of its expected weight after one step to its initial weight is

    R_n=(1-6/n^2)^(-2r)
         [1-(r+b)/binom(n,3) + r/(binom(n,3) w_1)].

Along n=2s with s tending to infinity,

    R_n -> exp(1/2) * 5/8 > 1.

For a completely elementary strict lower bound, exp(1/2)>1+1/2+1/8=13/8, so the limiting expression exceeds 65/64. Thus the required supermartingale property fails. For sufficiently large n, neither the initial state nor any state after its first triangle deletion is excluded by the 1% trajectory bounds, so killing does not repair this first-step failure. The chosen F has k asymptotic to n^2/24, and eventually k<m; it is within the legitimate large-k regime.

The verifier constructs a Bose Steiner triple system on s=201 vertices, embeds it in K_402, checks every pair is covered exactly once, and verifies R_402>1 by exact rational comparison. The displayed decimal 1.028397528... is diagnostic only. This finite witness checks the potential formula; n=402 is not an instance of the original positive stopping time. The asymptotic argument above is the applicable failure of this proof route. No assertion is made that the true inclusion probability violates a C/n bound.

## 6 Five investigated approaches and the remaining gap

1. **Symmetry and negative dependence.** Symmetry fixes the one-point scale exactly. The proposed extension by negative dependence fails on K_5; arbitrary high-order inclusion probabilities do not follow from marginals.
2. **Uniform trajectory denominators.** Summing marked selection times gives Proposition 1 uniformly over every k. It loses p_m^(-2), leaving n^(-0.98) instead of n^(-1).
3. **Protected edge supermartingales.** Multiplicity counting reproves an all-k weaker bound; wedge counting and a time-varying potential prove Theorem 3. Its maximum-degree hypothesis is essential to the argument provided.
4. **Switchings and comparison with known spread measures.** A particular ordered valid sequence (S_1,...,S_m) has probability product_(i=0)^(m-1) 1/Q(G_i). Switching triangle packings changes intermediate Q(G_i), so counting switchings without controlling these weights is insufficient. The later constructions in [JP] supply C/n-spread measures on full Steiner triple systems, but no bounded-density comparison between those constructed measures and the conditioned ordinary triangle-removal output was obtained here. Existence of another spread distribution does not identify this one.
5. **Dense subsystem stress test.** The preceding clique decomposition makes the sparse potential's initial drift positive. It isolates a concrete large-k obstruction to that method, rather than a counterexample to the problem.

The unresolved requirement is a uniform exponential inclusion bound for the remaining high-degree prescribed families under one high-probability event. In particular, neither fixed-k asymptotics, standard quasirandomness of the residual graph, existence of another spread design measure, nor finite experiments establish it. No full proof or counterexample was found in the bounded research pass.

## 7 Literature and provenance boundaries

The original page was visually inspected in the complete official OWR PDF. The numeric problem landing page was inaccessible through the web reader and returned HTTP 403 to a direct read. Complete local copies of both public dataset files were hashed and matched the repository's pinned manifest; the selected clean statement hash matches the catalog. No exact selected record or code was found in the separate research-results corpus. Repository searches by ID and topic, branch and commit searches, and the attempts directory found no actual earlier attempt artifact. These checks do not establish the absence of unpublished, deleted, or unindexed work.

The current search located relevant later threshold work and an adjacent Latin-rectangle inclusion result. None of the inspected statements identifies its distribution with the stopped K_n process in this problem. This is a bounded literature assessment, not evidence that no later or unindexed resolution exists.

- [OWR] Combinatorics, Probability and Computing, Oberwolfach Report 22/2022, DOI 10.4171/OWR/2022/22. Workshop April 24-30, 2022; printed p. 1226, Problem 6. https://publications.mfo.de/bitstream/handle/mfo/3964/OWR_2022_22.pdf?isAllowed=y&sequence=4
- [BFL] Tom Bohman, Alan Frieze and Eyal Lubetzky, Random triangle removal. Inspected arXiv:1203.4223v3, June 8, 2012, especially Theorems 2.1-2.2 and the end of Section 2. Publication DOI 10.1016/j.aim.2015.04.015. https://arxiv.org/abs/1203.4223
- [SSS] Ashwin Sah, Mehtaab Sawhney and Michael Simkin, Threshold for Steiner triple systems. Inspected author-hosted arXiv v1, April 8, 2022, introduction and Section 1.2. The current abstract lists v2, May 3, 2022, with unchanged results; its full PDF was not inspected. This work uses a modified construction and iterative absorption. https://www.mit.edu/~asah/papers/2204.03964.pdf
- [JP] Vishesh Jain and Huy Tuan Pham, Optimal thresholds for Latin squares, Steiner Triple Systems, and edge colorings. Inspected arXiv:2212.06109v2, December 19, 2022, introduction and Theorems 2-3. Its constructions give optimal-order spread distributions; they are not the ordinary triangle-removal law. https://arxiv.org/abs/2212.06109
- [DKKS] Alexander Divoux, Tom Kelly, Camille Kennedy and Jasdeep Sidhu, Subsquares in random Latin squares and rectangles. Current arXiv abstract and the journal search result were checked. This concerns uniform Latin rectangles and a sparse prescribed pattern, not the K_n process; full proof not used. https://arxiv.org/abs/2311.04152

Hashes, inspected locations, versions, query scope and limitations are recorded in SOURCE_VERIFICATION.json. Public metadata is included; source PDFs, extracted text, source images, raw dataset contents and private coordination files are excluded from this package.

## 8 Reproduction

Run from this directory with Python 3:

    python code/verify_triangle_removal.py --output results/replayed.json

The standard-library-only script uses exact rational arithmetic and integer comparisons for its claims. It enumerates terminal distributions for n=3,...,7, checks both hazard inequalities over all 1,024 labeled graphs on five vertices and their 1,520 nonempty available edge-disjoint target families, checks the rational constant margin, and verifies the dense subsystem witness. It does not simulate the asymptotic stopping time or independently prove the imported concentration theorem. Independent mathematical review of this report is still required before publication as a certified result.
