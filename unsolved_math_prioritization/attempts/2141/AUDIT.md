# Independent mathematical audit of the EP486 counterexample

## Outcome

**ACCEPTED AT THE PROSE PROOF LEVEL.** The complete ten-page manuscript by Shouqiao Wang, *A Proposed Solution to Erdős Problem 486*, supplies a valid fixed arbitrary-residue congruence system whose survivor logarithmic averages have lower limit at most 177/200 and upper limit at least 49/50. The mathematical dependencies, quantifiers, activation restrictions, conditional probability argument, and constants were independently checked. No unresolved mathematical gap was found in the proof of Theorem 1.1.

The original inclusive-activation question in Erdős's 1961 Problem I.26 receives the same negative answer. There are two valid bridges. The manuscript's general primitive-set bridge is correct. More strongly, the particular constructed system uses no zero residue, so its strict and inclusive survivors agree exactly. A proof of this latter observation is given below.

This is acceptance of the identified manuscript after a mathematical audit, not a claim of journal acceptance, a current problem-site status, or a local formal verification. No Lean compiler, build, imported executable, author script, or third-party verification script was run. The retained Lean statement was read; another group's replay remains an explicitly external claim at a different commit. Nothing here settles singleton-residue EP25.

## Sources and versions

- Primary manuscript: [Wang, A Proposed Solution to Erdős Problem 486](https://multiscalar.ai/results/erdos-486/paper.pdf), ten pages, 350612 bytes, SHA-256 `01ce6f1d22b0c9208cc45ecaa15039f0ee13ea75c334908ca65f371c365b9048`. The source was retrieved on 2026-10-10 at 22:38:54 UTC and was byte-identical to the previously retained copy. All ten pages were text-read during this audit, together with the full retained TeX source; manuscript pages 6 and 9 were also visually inspected.
- Original problem: [Erdős, Some unsolved problems, 1961](https://users.renyi.hu/~p_erdos/1961-22.pdf), printed pp. 235–236, I.26. The full PDF is 5669229 bytes, SHA-256 `60860c80588580d509a7af5ca6a771a700455508359816fb861e415bbf4f5a67`. Both relevant printed pages were text-read and visually inspected. The preceding I.25 on printed p. 235 also explicitly records Behrend's logarithmic-density-zero theorem for primitive integer sequences.
- Author's retained source tree: [commit d28713ac8245ca86a686b8c67370a8d19d81b242](https://github.com/ShouqiaoW/erdos/tree/d28713ac8245ca86a686b8c67370a8d19d81b242/486). The manuscript TeX has SHA-256 `fe03985bf3e7cf15adb5ed848a2cbc4b6a8b22dd31b3f418e2323c318b26949b`. Source hashes and Git blob matches were checked without executing the source.
- External replay report: [Millennium Research, Independent verification of Erdős Problem 486](https://github.com/ibrahimmian36/Pilus/blob/main/reports/erdos-486.md), retained report SHA-256 `0487372003ab4bbd46946b27220d8acdaa771c3a899f0582320c154a1f560fce`. It reports a replay of author commit `61325b10bbdc29f4fb5e0618b414b9f2189333ad`. That is not the same commit as the retained current tree, and byte identity between those trees was not established here.

## The exact question being answered

Take an infinite set A of positive integer moduli. For each n in A, let X_n be an arbitrary subset of Z/nZ. Define

    B_> = {m >= 1 : for every n in A with n < m, m mod n is not in X_n}.
    L_B(x) = (1/log x) sum_{1 <= m < x, m in B} 1/m,  x > 1.

The manuscript constructs one fixed pair (A,X), independent of x, with

    liminf L_B(x) <= 177/200 < 49/50 <= limsup L_B(x).

Erdős's original condition activates a modulus at m >= n. It permits finitely many arbitrary residues at each modulus, with no uniform cardinality bound, coprimality condition, or summability assumption. The constructed A is an infinite subset of positive integers and therefore has the required increasing enumeration. Every X_n is automatically finite. The survivor set is infinite, since its logarithmic sums are unbounded along the recovery cutoffs. The original cutoff is m < x and the normalization is log x, exactly as above.

The proof does not remove the activation threshold. It repeatedly uses that future moduli are inactive below previous recovery cutoffs. It does not use the zero modulus, negative survivors, a cutoff-dependent family, or one independently chosen system for each x.

## 1 Finite periodic recovery

For a finite family F of positive moduli and residue sets, form the completed union U_F of the corresponding periodic cylinders. Let L be the least common multiple of its moduli. Above the largest modulus, every constraint is active, so the delayed survivor differs only finitely from the periodic complement of U_F.

For each occupied residue class a modulo L, represented by 1 <= a <= L,

    sum_{ell >= 0, a+ell L < x} 1/(a+ell L) = (1/L) log x + O_L(1).

This follows by upper and lower integral comparison for the decreasing function 1/(a+Lt). Summing over the finitely many occupied classes, and adding the finite initial discrepancy, gives

    sum_{m < x, m in B_F} 1/m = (1 - mu(U_F)) log x + O_F(1).

The empty family gives the ordinary harmonic sum. The error constant need not be uniform across epochs: each later epoch is chosen after its finite past is fixed. Thus there is no illicit exchange of a finite-family limit with the eventual infinite system.

## 2 Arithmetic skeleton

At scale Q=2^j set k=2 floor(sqrt(j)/8), and retain subsets S of {1,...,k} with ||S|-k/2| <= sqrt(k). For sufficiently large j, k is a positive even integer tending to infinity.

Bertrand's postulate provides a prime p_i strictly between 4^(k+i) and 2*4^(k+i). These intervals are pairwise disjoint. Put P=product p_i. The exponent sum is exactly

    sum_{i=1}^k (2(k+i)+1) = 3k^2+2k.

Therefore P < 2^(3k^2+2k). Since k <= sqrt(j)/4,

    P^2/Q <= 2^(6k^2+4k-j) <= 2^(-5j/8+sqrt(j)) -> 0.

For each central S put d_S=product_{i in S} p_i. Choose R_S in 1+P Z nearest to Q/d_S and set q_S=d_S R_S. Then

    |q_S-Q| <= d_S P/2 <= P^2/2.

Also Q/d_S >= Q/P > P eventually, so R_S > P/2 > 0. It follows that 19Q/20 <= q_S <= 21Q/20 for every S simultaneously once j is large enough. Because R_S is 1 modulo every p_i,

    p_i divides q_S if and only if i is in S.

Distinct S give distinct q_S by their divisibility patterns. No additional distribution theorem for primes is used.

Let J=[11Q/10,19Q/10] intersect Z. Then q_S < every member of J, every member of J is at most 2q_S, and diam(J) <= 4Q/5 < q_S. Hence any residue class modulo q_S has at most one representative in J. The strict inequality q_S<m, needed for actual deletion, is already built into the geometry.

## 3 Endpoint abundance and finite randomness

Choose independent fair labels epsilon_i(b), one for each pair (i,b) with b modulo p_i. This is a finite product probability space. Put K(m)={i:epsilon_i(m mod p_i)=1}, and let E comprise the m in J for which K(m) is central. Assign such an endpoint the modulus q_{K(m)}.

For each fixed m, |K(m)| has binomial distribution Bin(k,1/2). Chebyshev gives a failure probability at most 1/4 for the central window, so E[|E|/|J|] >= 3/4. No independence between different endpoints is asserted or needed.

Changing a single label affects at most |J|/p_i+1 endpoint indicators. Since p_i <= P=o(sqrt(Q)) and |J| is asymptotic to 4Q/5, the change in Z=|E|/|J| is at most 2/p_i eventually. There are p_i coordinates with first index i. Their squared Lipschitz bounds total at most

    4 sum_i 1/p_i < k/4^k.

The strict inequality follows from p_i>4^(k+1). The lower-tail bounded-differences inequality with deviation 1/4 consequently gives

    P(Z<1/2) <= exp(-4^k/(8k)).

The hypotheses and the direction of this bound are correct. This strong concentration is more than the existence argument needs: Markov applied to 1-Z also yields P(Z<1/2) <= 1/2, which can be combined with a sufficiently small footprint-failure probability. This optional simplification does not change the manuscript's valid estimate.

## 4 The footprint and conditional fresh bits

Write U=union_{m in E} [m]_{q_{K(m)}}. For a fixed profinite point omega and a central S, let a_S(omega) be its residue representative in {1,...,q_S}; set m_S(omega)=q_S+a_S(omega). The skeleton geometry gives the exact equivalence

    omega in U iff some central S has m_S(omega) in J and K(m_S(omega))=S.

This equivalence is two-sided. A contributing endpoint lies in (q_S,2q_S], so it is precisely that representative; conversely a candidate satisfying the displayed conditions is an endpoint assigned q_S.

For i outside S let C_{S,i} be the event, in the Haar variable omega, that m_S(omega) and omega agree modulo p_i. Here gcd(q_S,p_i)=1. Conditional on a residue modulo q_S, the candidate m_S is fixed; CRT makes omega modulo p_i uniform. Thus mu(C_{S,i})=1/p_i exactly. The union C over all such S,i is determined by the skeleton alone, independently of every label, and

    mu(C) <= 2^k sum_i 1/p_i <= k/2^(k+2).

Now fix omega outside C before conditioning on the labels. Expose the k anchor labels epsilon_i(omega mod p_i), and denote their 1-set by T. A contributing S must be contained in T, because p_i divides q_S for i in S and hence its candidate queries the anchor at that index.

For every i outside a fixed S, the candidate's queried coordinate differs from the anchor at the same i by noncollision. It differs from every other anchor by its first coordinate. The k-|S| off-S queries also have different first coordinates from one another. Consequently they are independent fair bits even after all anchors have been exposed. The conditional contribution probability is therefore zero when S is not contained in T, and otherwise is at most 2^(-(k-|S|)). The deterministic condition m_S in J can only reduce it.

The proof neither asserts nor needs independence among candidates for different S. Those candidates may share queried labels. The next step is a union bound, not a product of probabilities. This distinction discharges the main potential dependency objection.

## 5 Entropy and numerical margins

The anchor count is Bin(k,1/2), so Hoeffding gives P(|T|>3k/5) <= exp(-k/50). When |T| <= 3k/5, each central S contained in T has

    |T minus S| <= k/10+sqrt(k).

The complement map is injective. Padding T to N_k=floor(3k/5) elements therefore bounds the number of candidates by sum_{ell=0}^{M_k} binom(N_k,ell), where M_k=floor(k/10+sqrt(k)). Eventually 0<M_k/N_k<1/2.

For 0<rho<=1/2 and ell<=rho N, the binomial probability weight rho^ell(1-rho)^(N-ell) is at least exp(-N H(rho)). Comparison with the full binomial expansion gives the claimed entropy bound. The direction is correct because rho/(1-rho)<=1. With rho=M_k/N_k, the exponent divided by k tends to

    (3/5) H(1/6) = (1/10)log 6 + (1/2)log(6/5) < 7/25.

Here log(6/5)<1/5, and the first seven positive terms of exp(9/5) already exceed 6. Continuity then gives the manuscript's exponent 0.29k for all sufficiently large k. Floors do not cause a problem; their normalized errors vanish.

Every central S has k-|S| >= k/2-sqrt(k) >= 0.49k eventually. The positive series for log 2 gives log 2>56/81, and (49/100)(56/81)>33/100. Thus each contribution is at most exp(-0.33k). The conditional union bound for a typical anchor configuration is at most exp(-0.04k).

Integrating over omega and averaging over anchors is legitimate: all random coordinates are finite in number and the relevant sets are finite cylinder unions. Tonelli, or a finite-period counting argument, gives

    E mu(U) <= k/2^(k+2) + exp(-k/50) + exp(-0.04k)
            <= 3 exp(-k/50)

eventually. Markov at threshold exp(-k/100) gives a failure probability at most 3 exp(-k/100). All exponent signs and factors are consistent.

## 6 The finite block and summable footprints

The sum of endpoint and footprint failure probabilities tends to zero. A single labeling therefore satisfies both |E|>=|J|/2 and mu(U)<=exp(-k/100). This is simultaneous existence, not an invalid combination of separate witnesses.

Since |J|>=4Q/5-1, half this count is at least 3Q/8 for Q>=20. Hence at every sufficiently large scale there is a finite block with at least 3Q/8 endpoints, moduli between 19Q/20 and 21Q/20, strict activation at each endpoint, and footprint at most eta_j=exp(-k_j/100).

The floor inequality k_j>=sqrt(j)/4-2 gives eta_j<=exp(1/50) exp(-sqrt(j)/400). Grouping r^2<=j<(r+1)^2 bounds the group by a fixed multiple of (2r+1) exp(-r/400). The resulting series converges. Accordingly its tail can be made smaller than any fixed positive error budget.

Choose and fix one valid block for every sufficiently large j before forming the epochs. All each-scale choices are among finite labelings. Existence is sufficient; no computationally feasible enumeration of the enormous moduli is claimed.

## 7 Epochs and one fixed system

Take epsilon=1/100 and j_0 sufficiently large that all block claims hold, sum_{j>=j_0} eta_j<epsilon, and 1/((2j_0+1)log 2)<epsilon. Recursively choose a_t>=j_0 with a_t>2a_{t-1}+3 and install all scales I_t={a_t,...,2a_t}.

At stage t, the previous epochs form a finite congruence family. Its completed footprint is the finite union of the corresponding U_j and has measure less than epsilon, by disjointness of the scale-index intervals and the tail bound. Periodic recovery gives a limiting survivor logarithmic average greater than 1-epsilon. Thus a_t can be taken sufficiently large that the finite-past average at x_t=2^(a_t-1) is at least 1-2epsilon=49/50. Restricting to dyadic cutoffs is harmless because the recovery estimate holds at every sufficiently large real cutoff.

Define A to consist of all moduli in the installed blocks, and define X_q by grouping all endpoint residues assigned to q. Adjacent modulus ranges are disjoint because 21*2^j/20 < 19*2^(j+1)/20. Thus a later scale cannot add residues to an old modulus. Each installed scale supplies at least one modulus, so A is infinite. These definitions produce one system fixed independently of the eventual averaging cutoff.

At x_t, every modulus from epoch t or later is at least 19*2^(a_t)/20 > x_t. None is active below x_t. Consequently the final survivor agrees there exactly with the finite-past survivor, including all individual initial integers. This proves L_B(x_t)>=49/50 along an unbounded sequence, hence the required limsup bound.

## 8 Deletion cutoffs

Set y_t=2^(2a_t+1). Every endpoint from a scale j in I_t lies below y_t and is removed by its assigned strictly smaller modulus. Endpoint intervals at different scales are disjoint because 19*2^j/10 < 11*2^(j+1)/10. Therefore their harmonic contributions may be added without double-counting.

At each scale,

    sum_{m in E_j} 1/m >= (3*2^j/8)/(19*2^j/10) = 15/76.

There are a_t+1 scales in I_t. Subtracting these known removed terms from the complete harmonic sum yields

    L_B(y_t) <= H_{y_t-1}/log y_t
                - (15/76)(a_t+1)/((2a_t+1)log 2).

The first term is less than 1+1/100. The ratio (a_t+1)/(2a_t+1) exceeds 1/2. Since log 2<3/4, the deletion term exceeds 15/(152 log 2)>5/38>1/8. Thus

    L_B(y_t) < 1+1/100-1/8 = 177/200.

This supplies the liminf bound. The gap between the asserted upper and lower subsequence bounds is 19/200. For completeness, all averages are nonnegative and are at most H_{ceil(x)-1}/log x=1+o(1), so the real liminf and limsup are finite. The separated subsequences exclude convergence.

## 9 Strict and inclusive activation

### General bridge in the manuscript

Let D=B_> minus B_>= for the same A and X. Membership in D is possible only at a modulus m in A with 0 in X_m. If d<e lie in D and d divides e, the already active modulus d removes e from B_>, a contradiction. Thus D is primitive. If 1 belongs to D, primitivity forces D={1}; otherwise D is a primitive subset of integers greater than 1.

Behrend's theorem says the reciprocal sum of a primitive set below x is o(log x). This is the exact assertion recorded in the visually inspected original Erdős source, printed p.235, I.25.2 and its following attribution. Finite primitive sets also satisfy it immediately. Consequently L_{B_>}(x)-L_{B_>=}(x) tends to zero. This preserves existence and value of density, and also both liminf and limsup. The general bridge is valid with precisely the required normalization.

### Exact bridge for the constructed example

In this construction every assigned pair satisfies

    q < m <= 19*2^j/10 <= 2q.

Equality m=2q could hold only if m=19*2^j/10. That number is not an integer: its denominator retains a factor 5, since no power of 2 is divisible by 5. Hence in fact q<m<2q, so m modulo q is nonzero.

Every residue in every X_q is generated by such an endpoint. Therefore 0 is absent from every X_q. Switching a constraint from n<m to n<=m changes only its test at m=n, where the residue is 0 and the test is automatically satisfied. The two survivor sets are thus exactly equal for every integer m. The theorem applies to the original Erdős formulation without any appeal to primitive-set theory. This is an authored strengthening of the audit's source bridge, not a change to the construction or a repair of a fatal gap.

## 10 Scope and formal evidence

The three complete files Statement.lean, Survivors.lean, and Main.lean were read. The formal statement explicitly excludes 0 from A, requires positive survivors, quantifies residue sets over moduli in A, uses strict activation, and defines the logarithmic average with a real cutoff and strict m<x. Its quantitative assertion includes A infinite, nonconvergence, and the two advertised bounds. Main names the two corresponding theorems.

Selected interface and coloring source was additionally inspected. The formal implementation uses a four-color biased finite construction, whereas the manuscript audited above uses fair bits and a central-subset window. Thus statement readback is not a claim of a line-for-line formalization of this particular prose construction. No full formal dependency audit or local axiom computation was performed.

The external report claims a kernel replay with standard axioms at its own pinned author commit and explicitly says the strict/inclusive bridge was not formalized there. Those claims have not been reproduced by this audit. Our acceptance rests on the prose argument verified above and its independently proved activation bridge, not on that report's headline. The lack of a local replay is a limitation of formal verification evidence, not an unresolved mathematical step in this prose proof.

Singleton EP25 is excluded. Each block can assign many distinct residues to the same modulus. Indeed the residue-to-endpoint map at a fixed modulus is injective by the diameter bound, and each installed scale has total sum |X_q|/q at least 5/14. There are infinitely many installed scales, so that sum diverges. Small measure of the overlapping union is entirely consistent with this divergent sum. Neither replacing each X_q by one residue nor duplicating moduli would preserve the argument or the original distinct-modulus requirement.

## Reproducibility and limitations

Historical independently authored arithmetic checks used exact rational arithmetic and proved power-series remainder bounds. They checked 29 conditions, including entropy and exponent margins, performed 112132 finite interval sanity checks, and rejected three deliberately false conditions. Their output was identical under ordinary Python, -O, and -OO. These are recorded verification results, not new publication-stage runs. Code and raw computational certificates are excluded from this edition. Finite checks support the written proof audit but do not establish infinite statements or constitute proof-assistant verification.

Input byte counts and SHA-256 hashes were independently recomputed during the audit. Copied manuscripts, source code, original source extracts, and third-party reports remain outside this public authored edition. SOURCES.json contains titles, public URLs, version identifiers, hashes, byte counts, and accurately limited historical inspection claims.

No remote mutation was made as part of this audit. No community-wide resolution status is asserted. The exact outcome is acceptance of Wang's specified prior-result prose proof, with the stated formal-verification limitation and with no claimed solution of EP25.
