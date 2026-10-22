# EP486: independent audit of the finite deletion lemma and activation convention

## Verdict and scope

**PASS for the finite deletion lemma and the strict/inclusive activation bridge of the pinned manuscript.** No defect was found in the skeleton, the conditional fresh-bit calculation, the entropy count, the first-moment footprint estimate, or the simultaneous choice of endpoints and small footprint. This is a focused mathematical audit, not a claim of a Lean replay or independent verification of every step of the global theorem.

For the actual construction, the activation bridge is stronger than the general bridge stated in the manuscript: **every installed residue is nonzero, so the strict and inclusive survivor sets are exactly equal.** No appeal to Behrend is necessary for this particular counterexample.

The argument audited is Shouqiao Wang, *A Proposed Solution to Erdős Problem 486*, ten-page PDF, SHA-256 `01ce6f1d22b0c9208cc45ecaa15039f0ee13ea75c334908ca65f371c365b9048`, 350612 bytes, and its source at author commit `d28713ac8245ca86a686b8c67370a8d19d81b242`. The mathematical derivation below is independently written. Source documents and third-party programs are not included in this authored directory, and no such program was executed.

- [Primary manuscript](https://multiscalar.ai/results/erdos-486/paper.pdf), Section 3, pp. 3–7; Remark 1.2, pp. 1–2.
- [Pinned author source](https://github.com/ShouqiaoW/erdos/blob/d28713ac8245ca86a686b8c67370a8d19d81b242/486/paper.tex), lines 222–586, with residue installation at 650–676.
- [Erdős, Some unsolved problems (1961)](https://users.renyi.hu/~p_erdos/1961-22.pdf), printed pp. 235–236, especially I.25.2 and I.26.1–2.

## 1. Deterministic arithmetic and the quantifier order

Fix a sufficiently large integer j; let Q=2^j and k=2 floor(sqrt(j)/8). All choices in this paragraph precede every random label. Bertrand's postulate supplies distinct primes p_i in (4^(k+i), 2·4^(k+i)), for 1≤i≤k. If P is their product, then

    log_2 P < 3k²+2k,
    P²/Q ≤ 2^(6k²+4k−j) ≤ 2^(−5j/8+sqrt(j)) → 0.

For each central subset S, meaning ||S|−k/2|≤sqrt(k), put d_S=product_{i in S} p_i. Choose R_S≡1 (mod P) nearest to Q/d_S and set q_S=d_S R_S. The progression has spacing P, so |R_S−Q/d_S|≤P/2. Since Q/P²→∞, eventually R_S>0, uniformly over S. Moreover,

    |q_S−Q|≤d_S P/2≤P²/2,
    19Q/20≤q_S≤21Q/20,
    p_i divides q_S if and only if i belongs to S.

The last equivalence holds because R_S≡1 modulo every p_i. It also makes q_S distinct for distinct S. None of these moduli depends on random labels or on the later variable ω.

Let J=[11Q/10,19Q/10]∩Z. Then every q_S is below every point of J; J is contained in (q_S,2q_S], and diam(J)≤4Q/5<q_S. Thus a residue modulo q_S has at most one representative in J.

There is one common sufficiently-large-j threshold for these assertions: all estimates above are uniform in S. Since k tends to infinity with j, every later sufficiently-large-k condition can be added to this threshold. There is no exchange of a pointwise-in-ω threshold with a uniform conclusion.

## 2. Endpoint abundance and simultaneous selection

Give every pair (i,b), b modulo p_i, an independent fair bit ε_i(b). Define K(m)={i:ε_i(m modulo p_i)=1}, E={m in J:K(m) is central}, and q_m=q_{K(m)} for m in E.

For a fixed m, |K(m)| has mean k/2 and variance k/4. Chebyshev therefore gives P(m not in E)≤1/4, and consequently E[|E|/|J|]≥3/4. No independence between distinct endpoints is asserted or needed for this expectation.

The manuscript's stronger concentration calculation is correct: changing one label changes Z=|E|/|J| by at most 1/p_i+1/|J|≤2/p_i, because |J|≥p_i eventually. There are p_i such labels for coordinate i. Thus the sum of squared change bounds is at most 4 sum_i 1/p_i<k/4^k. The bounded-differences inequality gives the stated failure bound exp(−4^k/(8k)).

For finite-block existence, even that concentration theorem is unnecessary. From 0≤Z≤1 and E Z≥3/4,

    P(Z<1/2)=P(1−Z>1/2)≤2 E(1−Z)≤1/2.

Once the footprint failure probability below is less than 1/2, the probability that both requirements hold is positive. This simpler first-moment check independently confirms the simultaneous-selection step; it is not a claimed strengthening of the manuscript's concentration lemma.

## 3. Candidate identity and collision geometry

For fixed ω in the profinite integers, let a_S(ω) be its residue modulo q_S represented in {1,…,q_S}, and put m_S(ω)=q_S+a_S(ω). This is the unique integer in (q_S,2q_S] congruent to ω modulo q_S. The geometry of J gives the exact identity

    ω belongs to U=union_{m in E} [m]_(q_m)
    if and only if some central S satisfies m_S(ω) in J and K(m_S(ω))=S.

This equivalence does not assume that different S give different candidates. Repeated candidates cause no problem for a union bound.

For i outside S, define C_(S,i) by m_S(ω)≡ω (mod p_i). Because p_i does not divide q_S and p_i is prime, gcd(q_S,p_i)=1. Once ω modulo q_S is fixed, m_S(ω) is fixed, and exactly one of the p_i equally likely residues of ω modulo p_i causes the equality. Hence the Chinese remainder theorem gives μ(C_(S,i))=1/p_i. No coprimality between different q_S is required.

Let C be the union of these collision sets over central S and i outside S. It depends solely on the deterministic skeleton. Therefore

    μ(C)≤2^k sum_i 1/p_i≤k/2^(k+2).

One may do the whole calculation in a finite uniform cyclic space: take L divisible by every q_S and every p_i. All candidate functions, collision events, and cylinder indicators depend only on ω modulo L. Thus the measure identities and the later interchange of averages are finite counting identities; there is no measurability difficulty.

## 4. Conditional fresh bits: what is and is not independent

Fix ω outside C, and condition on all k anchor bits ε_i(ω modulo p_i). Write T for the indices whose anchor bit is one.

For a fixed central S, the bits at indices i in S are anchors, since p_i divides q_S and m_S(ω)≡ω modulo p_i. Thus K(m_S(ω))=S is impossible unless S is a subset of T.

For each i outside S, the queried variable is ε_i(m_S(ω) modulo p_i). The exclusion of C guarantees that this variable differs from the anchor variable at the same index i. It differs from every other anchor and from every other off-S query because those have a different first coordinate. The off-S queries are therefore mutually independent fair bits, even after the complete anchor realization has been specified.

Accordingly, for fixed S, the exact conditional probability is

    1_{S subset T} · 1_{m_S(ω) in J} · 2^(−(k−|S|)).

There is no random choice of S or of a queried residue inside this conditional assertion: S and ω have already been fixed. Distinct candidates S and S' may share queried bits and be strongly dependent. The argument uses only their individual conditional probabilities and a union bound, so that dependence is harmless.

Removing C is essential. Conditioning merely on anchors without removing the skeleton collisions would not justify the displayed formula.

## 5. Entropy count and constants

The anchor vector is a vector of k independent fair bits for every fixed ω. Its law does not change when ω is restricted to the deterministic complement of C. The fair-binomial upper tail satisfies

    P(|T|>3k/5)≤exp(−k/50).

For completeness, this particular tail bound follows from a short exponential-moment calculation. For a fair bit X, E exp(t(X−1/2))=cosh(t/2)≤exp(t²/8), because tanh u≤u for u≥0. Multiplication over k independent bits and Markov with t=2/5 give exp(−tk/10+kt²/8)=exp(−k/50).

Now suppose |T|≤3k/5. Every central S contained in T has |T\S|≤k/10+sqrt(k). Padding T to size N_k=floor(3k/5) gives an injection of all such S into the subsets of an N_k-element set of sizes at most M_k=floor(k/10+sqrt(k)). The number of candidates is at most sum_{ell=0}^{M_k} binom(N_k,ell).

If 0<ρ≤1/2 and M=floor(ρN), then each weight ρ^ell(1−ρ)^(N−ell), for ell≤M, is at least exp(−NH(ρ)), where H(ρ)=−ρ logρ−(1−ρ)log(1−ρ). Comparing the partial weighted sum with the full binomial expansion gives

    sum_{ell=0}^M binom(N,ell)≤exp(NH(ρ)).

Here M_k/N_k→1/6 and N_k/k→3/5. The limiting exponent is

    (3/5)H(1/6)=(1/10)log6+(1/2)log(6/5)<7/25=0.28.

The logarithm bounds are rigorous: log(6/5)<1/5; the sum of the first seven terms of exp(9/5) is 7542629/1250000>6, so log6<9/5. Continuity of H gives the uniform candidate count ≤exp(0.29k) eventually. Floors do not change these limits.

Eventually sqrt(k)≤k/100, so k−|S|≥0.49k. The first two terms of the positive atanh series give log2>56/81. In exact rational arithmetic,

    (49/100)(56/81)−33/100=71/8100>0.

Each conditional candidate probability is therefore at most exp(−0.33k). A conditional union bound gives exp(0.29k)exp(−0.33k)=exp(−0.04k), uniformly over ω outside C and anchor realizations with |T|≤3k/5.

## 6. First moment, small footprint, and summability

Average the preceding estimate over anchors, then over ω. On C bound the probability by one. Finite Fubini, or Tonelli, gives

    E μ(U)≤k/2^(k+2)+exp(−k/50)+exp(−k/25)≤3exp(−k/50)

for all sufficiently large k. The collision term is eventually at most exp(−k/50) since its logarithm is log k−(k+2)log2. The third term is already no larger than exp(−k/50).

Markov with threshold η=exp(−k/100) yields

    P(μ(U)>η)≤3exp(−k/100).

Combining with Section 2 gives positive probability of both |E|≥|J|/2 and μ(U)≤η once k is sufficiently large. Correlation between endpoint abundance and footprint size is irrelevant: only the sum of the failure probabilities is used. Fix one successful labeling at each scale.

Since |J|≥4Q/5−1, |J|/2≥3Q/8 whenever Q≥20. Thus the chosen finite block has the advertised endpoint count, active moduli, and footprint. Finally k_j≥sqrt(j)/4−2 implies

    η_j≤exp(1/50)exp(−sqrt(j)/400).

Grouping r²≤j<(r+1)² bounds its total by exp(1/50) sum_r (2r+1)exp(−r/400), a convergent series. The footprint bound is compatible with selecting all blocks at once: each scale is a separate finite existence statement, and a successful labeling can be fixed deterministically. No independence between scales is needed.

The footprint is the measure of a union, not the sum of its constituent cylinder measures. Endpoints sharing q give distinct residues because their pairwise distances are below q. Thus a large local deletion count and a small union footprint are not contradictory; overlaps between cylinders associated to different q are allowed and are essential.

## 7. Exact activation bridge for the installed system

For every endpoint m and its modulus q at scale Q=2^j,

    q<m≤19Q/10≤2q.

If m=2q, both weak inequalities in the latter chain are equalities, so m=19·2^j/10. That rational number is not an integer: divisibility by 10 would force 5 to divide 2^j. Hence m<2q, and

    m modulo q=m−q belongs to {1,…,q−1}.

Every installed residue is of this form. Grouping endpoints into residue sets preserves the exclusion of zero, and different scales have disjoint modulus ranges. Therefore 0 is absent from every installed X_q.

At an arbitrary positive integer n, the strict rule checks q<n and the inclusive rule additionally checks q=n, if present. That extra check tests n modulo n=0, which is not in X_n. The two rules hence have exactly the same outcome at every n. This proves equality of survivor sets and therefore equality of every finite logarithmic average, not merely of limiting densities.

For comparison, the manuscript's general bridge is also logically correct: if D=B_strict\B_inclusive, then each d in D has d in A and 0 in X_d. If d<e are in D with d dividing e, the active modulus d would exclude e from B_strict, a contradiction. Thus D is primitive, and the standard Behrend conclusion gives logarithmic density zero. Erdős's 1961 printed p.235, I.25.2, explicitly records that theorem for primitive integer sequences; the finite-set case is immediate. Printed p.236, I.26.1, explicitly uses inclusive activation. These two pages were visually inspected in the pinned primary-source render. The exact bridge above makes the external primitive-set theorem unnecessary here.

## 8. Independent finite checks and limits of the audit

Historical independently authored finite-mechanism checks verified candidate equivalence, conditional fresh-bit identities, exact CRT collision measures, conditional union bounds, finite Fubini, and rational logarithmic margins. Their results were byte-identical under normal Python, -O, and -OO. Negative controls detected the failure of fresh-bit reasoning at a collision, actual dependence between distinct candidates, and failure of the collision formula when off-S coprimality was removed.

This publication edition omits the finite illustrative toy parameters, numerical computational witnesses, raw certificates, and checker code. Sections 1–7 retain the complete general analytical argument. This omission is editorial only and changes no theorem or mathematical acceptance. These historical checks were not rerun during publication preparation.

These checks exercise logical mechanisms; small examples cannot prove the asymptotic block lemma. That conclusion rests on Sections 1–7. No Lean build, axiom replay, third-party executable, remote write, or full-global-theorem certification is claimed by this focused audit.
