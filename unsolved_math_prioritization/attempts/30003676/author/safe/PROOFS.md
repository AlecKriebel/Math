# Retained proofs and rigorously delimited obstructions

All statements here concern the exact stochastic process, except the abstract negative control explicitly identified in §5. These are self-contained retained results, not claims of mathematical novelty.

## 0. Generator and finite-state preliminaries

Let V be finite, |V|=n, w_uv=w_vu≥0 with w_vv=0, and μ_v>0. An infected set A⊆V has generator

    Lf(A) = Σ_{v∈A} μ_v[f(A\{v})−f(A)]
          + Σ_{v∉A}(ε+θΣ_{u∈A}w_vu)[f(A∪{v})−f(A)].             (0.1)

Here θ≥0 and ε>0. Every subset can reach every other through positive-rate births and deaths, so the finite chain is irreducible. For completeness, the all-infected state is reached with positive probability from any state by a prescribed finite sequence of external births; prescribed recoveries then give any target state. A finite irreducible continuous-time chain has a unique invariant probability π and converges to it: one can see convergence by uniformizing at a rate strictly exceeding all exit rates, obtaining an irreducible aperiodic finite stochastic matrix. Its positive sufficiently high power gives a strict total-variation contraction by a common-minorization coupling. Iteration yields convergence and uniqueness.

The stationary equations πQ=0, Σπ=1 form a nonsingular system after replacing one dependent equation by normalization. Its coefficients are affine in θ,ε,μ,w. Cramer's rule therefore makes π rational and analytic wherever irreducibility is retained. Thus no finite-n, ε>0 singular phase transition is being asserted. With ε=0 the empty state is the only closed class when μ_v>0: from every nonempty state, a sequence of deaths before births reaches it with positive probability. Hence its unique stationary law is δ_∅. Taking ε→0 at fixed n also gives δ_∅, by compactness and continuity of the invariant equations. Joint n,ε limits are essential.

## 1. Approach 1: coupling and subcritical certificates

### 1.1 Monotonicity

Use independent Poisson recovery marks of rate μ_v at each v, external birth marks of rate ε, and directed arrows u→v of rate θw_uv for each orientation of each undirected edge. An arrow infects its target only when its source is infected. For two processes with ordered initial sets, the same marks preserve inclusion: a common death deletes a vertex from both when present, and a birth or arrow cannot create an infection only in the smaller process. Larger θ, larger ε, or larger edge weights are obtained by adding arrows/births; smaller recovery by deleting recovery marks. These changes preserve the stochastic order. Pass to stationary laws using finite-state convergence. This proves stationary monotonicity without factorizing any correlations.

### 1.2 Positive-vector drift

Let a_v>0, H(A)=Σ_{v∈A}a_v, a_min=min_v a_v, and suppose

    μ_u a_u − θΣ_v w_uv a_v ≥ c a_u  for every u, with c>0.        (1.1)

By (0.1), dropping susceptible restrictions only increases births, giving

    LH(A) ≤ εΣ_v a_v − cH(A).

Stationarity implies 0=E[LH] and hence

    E[X]/n ≤ ε Σ_v a_v / (c n a_min).                            (1.2)

If the right side tends to zero along a graph sequence, Markov's inequality proves X/n→0 in probability. In particular, if μ_v≥μ_0, every weighted degree is at most d, and θd<μ_0, use a_v=1 and c=μ_0−θd.

For a resolvent form, put D=diag(μ_v), W=(w_uv), and p_v=P(v infected). Exact first moments give

    μ_v p_v = ε(1−p_v)+θΣ_u w_vu E[1_{v susceptible}1_{u infected}]
             ≤ ε+θ(Wp)_v.

Let B=θD^{-1}W. If ρ(B)<1, iterating p≤εD^{-1}1+Bp and using B^m→0 yields

    p ≤ εΣ_{j≥0}B^j D^{-1}1 = ε(D−θW)^{-1}1.                   (1.3)

The inverse is entrywise nonnegative. This is a **sufficient extinction bound**, not an equivalence: the exact moments contain correlations, and the linear upper bound is not a lower bound. Approach 3 exhibits a macroscopic failure of the reverse implication even under the conjecture's endpoint premise.

## 2. Approach 2: complete-graph stationary asymptotics

Consider N vertices, μ_v=μ>0, and w_uv=a/N for u≠v, with a>0 fixed. Write β=θa and R=β/μ. The number K infected is itself Markov because its rates depend only on k:

    b_k=(N−k)(ε+βk/N),  d_k=μk.                                (2.1)

Define r_0=1 and r_{k+1}=r_k b_k/d_{k+1}. Detailed balance between consecutive states proves

    P(K=k)=r_k/Z,  Z=Σ_{j=0}^N r_j.                             (2.2)

For β>0 and k≥1, direct telescoping gives

    r_k = (Nε/(μk)) R^{k−1}
          ∏_{j=1}^{k−1}(1−j/N)
          ∏_{j=1}^{k−1}(1+Nε/(βj)).                            (2.3)

The empty products at k=1 equal one. No approximation occurs in (2.1)–(2.3).

### Theorem 2.1

If ε_N→0 and log(1/ε_N)=o(N), then

    K/N → x_R := max(0,1−1/R) in probability,

with x_R=0 when β=0. In particular the exact stochastic threshold for this family is θ=μ/a, with the critical normalized prevalence also tending to zero.

**Proof.** For β>0 define, continuously at x=1,

    F_R(x)=x log R − x − (1−x)log(1−x),  0≤x≤1.

We first prove uniform convergence

    max_{0≤k≤N} |N^{-1}log r_k − F_R(k/N)| →0.                  (2.4)

At k=0 it is exact. The first factor of (2.3) contributes at most
(|log ε_N|+log N+|log μ|)/N in absolute value, hence o(1). Replacing (k−1)log R/N by k log R/N has error |log R|/N. The partial Riemann sums of log(1−t) converge uniformly to their integrals: for g(t)=−log(1−t), monotonicity traps the sum by upper/lower integrals through the penultimate subinterval, with discrepancy at most (log N)/N, and the last integral is (log N+1)/N. These bounds also cover all partial sums. The integral of log(1−t) from 0 to x is −x−(1−x)log(1−x).

Finally set q=ε_N/β. The last sum in (2.3) is nonnegative, and, by the integral bound for a decreasing nonnegative function,

    N^{-1}Σ_{j=1}^{N−1}log(1+Nq/j)
    ≤ ∫_0^1 log(1+q/t)dt
    = log(1+q)+q log(1+1/q) →0.

This proves (2.4). Now F'_R(x)=log(R(1−x)) for x<1 and F''_R(x)=−1/(1−x)<0. Thus F has the unique maximum x_R: it is decreasing if R<1; at R=1 it strictly decreases for x>0; and for R>1 its maximum is at 1−1/R. For any fixed distance η>0 the maximum of F outside the η-neighborhood of x_R is separated by some γ>0 from F(x_R), by compactness and uniqueness. Choose a grid point approaching x_R. Equation (2.4) and (2.2) bound the total probability outside that neighborhood by (N+1)exp(−Nγ/2) for all sufficiently large N. This tends to zero. When β=0, coordinates are independent with infection probability ε/(μ+ε), so Markov's inequality proves the result. ∎

This gives a concrete sufficient meaning of slow immigration for this family, not a universal one for the problem. For example, every ε_N≥exp(−√N) with ε_N→0 satisfies the theorem.

### 2.2 Why the slow condition cannot simply be deleted

For every fixed β,μ>0 take ε_N=exp(−N²). From (2.1), for k≥1 and ε_N≤1,

    r_k ≤ (Nε_N/μ)[N(1+β)/μ]^{k−1}.

Consequently Σ_{k≥1}r_k ≤ N(Nε_N/μ) max(1,[N(1+β)/μ]^{N−1})→0, since its logarithm is −N²+O(Nlog N). Hence P(K=0)→1, even for β>μ. This is a counterexample to an extension requiring supercritical persistence for **every** ε_N↓0. It is not a counterexample to the stated sufficiently-slow version.

## 3. Approach 3: a connected spectral-shortcut obstruction

### 3.1 Exact dimer

For two vertices, unit recovery, unit edge weight, immigration h>0 and transmission multiplier θ, the count chain has b_0=2h, b_1=h+θ, d_1=1, d_2=2. Its unnormalized stationary probabilities are

    (1, 2h, h(h+θ)).

Thus either vertex has infection probability

    p(h,θ)=h(1+h+θ)/[(1+h)²+hθ].                               (3.1)

For each fixed θ this tends to zero as h→0, regardless of whether θ is above the linearized threshold 1.

### Theorem 3.2

There is a sequence of connected undirected weighted graphs with μ_v=1 and n→∞ for which:

- 1/ρ(W_n)→1;
- for every fixed 0≤θ≤2, X^(n)_{θ,ε_n}/n→0;
- for every fixed θ>2, X^(n)_{θ,ε_n}/n→(1/2)(1−2/θ)>0;

where ε_n→0 and log(1/ε_n)=o(n). Thus it satisfies the primary endpoint premise, for example with θ_*=1/2 and θ^*=4, and its sharp onset is 2 rather than the inverse spectral limit 1.

**Construction and proof.** First take n=4m. On 2m vertices place a clique with every edge weight 1/n. Partition the other 2m vertices into m disjoint dimers of edge weight 1. Regard the clique and these m dimers as m+1 blocks in a path, and join consecutive blocks by a single edge of weight η_n=n^{-2}. Endpoints can be chosen so that each vertex has at most two such weak incident edges. This graph is connected and all its weights are positive on its declared edges.

For any block, deleting cross-block arrows gives a smaller process with immigration ε_n. For an upper process, replace all incoming weak arrows by external birth marks, independently of their sources. At any vertex the total incoming weak-arrow rate is at most 2θη_n. Add extra external marks if necessary to obtain the same immigration

    h_n=ε_n+2θη_n

at each vertex of the independent upper blocks. The graphical coupling in §1 sandwiches the original block processes between these lower/upper block chains, including their stationary laws.

The total upper expected infections in all dimers, divided by n, is at most p(h_n,θ)/2→0 by (3.1). Markov's inequality makes the total dimer contribution negligible. On the clique, N=2m=n/2 and the internal weights are 1/n=(1/2)/N. Hence β=θ/2, μ=1. Both immigration sequences ε_n and h_n meet Theorem 2.1: h_n→0, h_n≥ε_n, and eventually h_n<1, so log(1/h_n)≤log(1/ε_n)=o(n)=o(N). The lower and upper clique fractions both converge to (1−2/θ)_+. Squeezing and N/n=1/2 prove the claimed full-graph limit, including θ=2.

Let W_n^0 be the disconnected block matrix. Each dimer has top eigenvalue 1; the clique top eigenvalue is (2m−1)/n<1/2. Thus ρ(W_n^0)=1. The weak-edge matrix E_n=W_n−W_n^0 is symmetric, nonnegative, with row sums≤2η_n. Its spectral norm is≤2η_n (for example, |x^TE_nx|≤Σ_{ij}E_ij(x_i²+x_j²)/2≤2η_n||x||²). Rayleigh's principle applied to a dimer's positive eigenvector yields ρ(W_n)≥1, and the same principle with the norm bound yields ρ(W_n)≤1+2η_n. Therefore 1/ρ(W_n)→1.

If an index at every integer n is desired, use the 4⌊n/4⌋-vertex construction and attach the at most three remaining unit-recovery vertices in a weak-edge path. The clique fraction still tends to 1/2, weak degrees can still be bounded by two, and the O(1) extra count is negligible; the same arguments apply. ∎

The exact stochastic model therefore cannot be replaced by the first-order closure p'_v=−μ_vp_v+(1−p_v)θΣ_uw_vup_u and its disease-free Jacobian. A block with large spectral radius can consist entirely of bounded-size pieces whose stationary prevalence vanishes with immigration. This observation does not obstruct a deterministic separating threshold; the construction has one.

## 4. Approach 4: dual ancestry and stationary susceptibility

Run the Poisson graphical construction backwards from a target set A at time 0. Its ancestral set evolves, in backwards elapsed time, as the same contact process **without immigration**: a recovery mark removes a current ancestor and an incoming arrow adds its source. Symmetry of W makes the reversed directed-arrow rates the same as the forward rates; vertex-dependent recovery causes no problem. Write ξ_t^A for this zero-immigration dual and

    T_A=∫_0^∞ |ξ_t^A|dt.

With μ_v>0 on a fixed finite graph, the dual is absorbed at ∅ almost surely, with finite expected extinction time. A uniform positive probability of a no-arrow interval with all current vertices recovering gives an exponential tail in units of that interval, so T_A is finite almost surely and has finite mean.

### Theorem 4.1

For every A⊆V,

    π_{θ,ε}(all vertices of A susceptible)=E_A[exp(−εT_A)].      (4.1)

**Proof.** Start a forward process empty at time −t. A target in A is infected at time 0 exactly when a backwards ancestral path reaches an external birth mark in [−t,0]. Conditional on the recovery/arrow structure, external marks are independent Poisson processes, and the total space-time measure of the explored ancestor set is ∫_0^t|ξ_s^A|ds. The probability of no external mark in it is the exponential of minus ε times that measure. Take t→∞. On the forward side use finite-state convergence to π; on the backwards side use bounded convergence. This proves (4.1). ∎

In particular,

    E[X]=Σ_v (1−E_v[e^{−εT_{\{v\}}}])
        ≤ ε Σ_v E_v[T_{\{v\}}].                               (4.2)

This is an exact susceptibility route to subcritical estimates, using 1−e^{−z}≤z. It says nothing alone about a uniform supercritical lower tail of X.

Let Q^0 be the full dual generator at ε=0. The values h(A)=E_A[e^{−εT_A}] solve

    h(∅)=1,
    (Q^0h)(A)=ε|A|h(A), A≠∅.                                 (4.3)

Indeed conditioning on the first holding time (with total jump rate q_A) gives
(q_A+ε|A|)h(A)=Σ_{B≠A}q_ABh(B), which is (4.3). This linear system has a unique solution: its killed generator is the transient generator of a process with additional killing rate ε|A|, and a maximum-principle argument also works. If a homogeneous solution has positive maximum at a nonempty A, the left form (q_A+ε|A|)h(A)=Σq_ABh(B) is impossible; apply the same argument to its negative.

There is also a precise pair-correlation identity. Put H(A)=E_A[e^{−εT_A}]. Inclusion-exclusion gives

    Cov(1_{u infected},1_{v infected})=H({u,v})−H({u})H({v}).    (4.4)

Thus single-vertex estimates do not determine Var(X); they leave all joint-ancestry terms. The verifier checks (4.1), (4.3), and (4.4) exactly for every subset in its finite weighted examples. No claimed bound on (4.4) closes the arbitrary-network gap here.

## 5. Approach 5: testing the abstract monotonicity shortcut

Let U be uniform on [0,1], and g(θ)=0 for θ≤1, g(θ)=θ−1 for 1<θ<2, and g(θ)=1 for θ≥2. Define, for every n and every ε,

    Y^(n)_{θ,ε}=1_{U≤g(θ)}.

This family is coupled monotonically in θ and is independent of ε. At θ_*=1/2 it is identically zero and at θ^*=5/2 it is identically one. Nevertheless there are no θ_n∈[1/2,5/2] with Y_{θ_n−δ}→0 in probability and Y_{θ_n+δ} bounded away from zero in probability for every sufficiently small fixed δ>0.

**Proof.** Pass to a convergent subsequence θ_n→t in the compact interval. Since these variables are Bernoulli, the lower conclusion at a fixed δ means g(θ_n−δ)→0. The upper conclusion means g(θ_n+δ)→1: for every 0<a<1 its probability of being at most a is 1−g(θ_n+δ), so the bounded-away definition is exactly convergence of this probability to zero. Continuity gives g(t−δ)=0 and g(t+δ)=1. Taking δ↓0 forces g(t)=0 and g(t)=1 simultaneously, a contradiction. Parameters can be kept positive by restricting δ<1/4. ∎

This is **not** a contact-process construction. It is a logical negative control: no proof can derive the desired conclusion from endpoint conditions and abstract attractiveness alone. One must use extra structure of the contact process (or justified graph assumptions). Positive mean is likewise insufficient: at θ=3/2 the mean is 1/2 but the variable has probability 1/2 of being zero.

## 6. What has and has not been established

The finite chains, subcritical inequalities, complete-graph limit including criticality, connected spectral obstruction, dual equations, and abstract counterexample have full proofs above. They establish no unrestricted choice of θ_n, no graph-uniform sufficiently-slow scale, and no counterexample satisfying all of Aldous's stated SIS conditions. A finite exact replay is a check on these formulas, not a proof by experiments of the remaining asymptotic conjecture.
