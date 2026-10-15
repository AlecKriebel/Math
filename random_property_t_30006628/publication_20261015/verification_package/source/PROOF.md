# Candidate proof: property (T) above one-third density in free products

Problem 30006628 / OWR-14299911-031. Author freeze prepared 2026-10-06.

**Status:** a complete candidate argument awaiting independent mathematical audit. This document is not formal verification, human certification, or a claim of journal acceptance. The attached checker tests exact finite identities and negative controls; it does not certify this asymptotic proof.

## 1. Claim and scope

Fix n >= 3 nontrivial finitely generated groups G_i, finite generating sets for them, a fixed ball radius m >= 1, and a density d with 1/3 < d < 1. Let B_i be the nonidentity elements in the radius-m word ball, with the usual symmetric word metric. Form the disjoint alphabet B = union_i B_i, and let S_ell consist of the syllable sequences of length ell whose successive factors, including the last and first factors, differ. Choose N_ell = floor(|S_ell|^d) independent uniform elements of S_ell, with replacement. Let G_ell be the quotient of the free product by their normal closure.

**Theorem claimed.** As ell tends to infinity through all positive integers, the probability that G_ell has Kazhdan's property (T) tends to one.

The hypotheses fix the factors, their generating sets, m and d before ell varies. No uniformity over these parameters is asserted. Factors may contain torsion or be infinite or not finitely presented. The argument applies more generally to any fixed finite, nonempty, inverse-closed generating subset in each factor. It makes no assertion at density 1/3, for two factors, or when these alphabets change with ell.

The model is Definition 1.1 of Einstein--Krishna--Montee--Ng--Steenbock, arXiv:2502.08630v2. The question remains explicit in that revision as Question 1.9. The OWR problem imposes at least three factors. The known collapse theorem above density 1/2 is consistent with, but is not used in, the argument below.

## 2. Alphabet matrix and counting

Put k = |B| and let c(a) denote the factor of a letter a. Inversion a -> a^{-1} is an involution preserving c. Define the symmetric k by k matrix

    A[a,b] = 1 if c(a) != c(b), and 0 otherwise.

It is the adjacency matrix of a complete n-partite graph with all parts nonempty. It is connected and contains a triangle, so it is primitive. Let lambda be its Perron eigenvalue, and let r be its strictly positive Perron vector normalized by sum_a r_a^2 = 1. Since there are at least three parts, lambda >= 2. Letters in one part have identical coordinates in r; in particular r_{a^{-1}} = r_a.

Every eigenvalue of A except lambda is nonpositive. Indeed, for a real vector z,

    z' A z = (sum_a z_a)^2 - sum_i (sum_{a in B_i} z_a)^2.

This is nonpositive on the codimension-one subspace sum_a z_a = 0, so A has at most one positive eigenvalue. Perron--Frobenius supplies that positive eigenvalue and gives |mu| < lambda for every other eigenvalue mu. Consequently

    P[a,b] = A[a,b] r_b / (lambda r_a)

is a reversible stochastic matrix whose spectrum consists of 1 and numbers in (-1,0]. Write rho = -min spectrum(P), so 0 <= rho < 1.

Let W_t be the reduced syllable words of length t over B, and write f(w), l(w) for first and last letters. Normal-form uniqueness in a free product makes these actual distinct elements. The exact number with endpoints a,b is (A^{t-1})[a,b]. Also

    Z_ell := |S_ell| = trace(A^ell) = lambda^ell (1+o(1)).

All asymptotic estimates here and below are for fixed A. Diagonalization of the real symmetric matrix A gives, uniformly over its finitely many indices,

    (A^t)[a,b] = lambda^t r_a r_b + O(lambda^t theta^t)

for a fixed theta < 1 (enlarging theta within (0,1) if needed). The elementary Perron facts and this finite-dimensional diagonalization are the only counting inputs.

### 2.1 Removing words equal to their inverses

Set V_t = {w in W_t : w != w^{-1}}. This set is inverse closed and has no fixed points under inversion. A reduced word of even length cannot equal its inverse: its middle two syllables would then be inverse and hence in the same factor. For t = 2s+1, such a word is determined by its first s syllables and a middle self-inverse letter. Thus the total number removed is O(lambda^s), using |W_s| = O(lambda^s). For large t, uniformly over a,b,

    v_t(a,b) := |{w in V_t : f(w)=a, l(w)=b}|
               = lambda^{t-1} r_a r_b (1+o(1)).                 (2.1)

In particular every endpoint class is nonempty for sufficiently large t. All errors in (2.1) decay exponentially with t; the constants may depend on B.

Define the exact completion count

    T_h(p,q) = sum_{w in V_h} A[p,f(w)] A[l(w),q].

The same sum over W_h is (A^{h+1})[p,q]. The deletion bound therefore gives

    T_h(p,q) = lambda^{h+1} r_p r_q (1+o(1)),                 (2.2)

again uniformly with exponential error. The matrix T_h is symmetric, since reversal followed by inversion is a bijection of V_h and A depends only on factors. In fact its values depend only on the factors of p,q. No independence of endpoint letters is assumed; equations (2.1)-(2.2) establish the needed asymptotic factorization.

## 3. A triangular presentation, for every length residue

Write ell = 3L + e, 0 <= e <= 2. Cut each sampled relator at fixed positions into three blocks of lengths

    e=0: (L,L,L)
    e=1: (L,L,L+1)
    e=2: (L,L+1,L+1).

Let I be the one or two distinct block lengths. Our vertex alphabet is the disjoint union V = union_{t in I} V_t, with inverse pairs identified only to choose one formal generator per pair. Distinct lengths cannot represent the same free-product element. The formal generator associated to w^{-1} means the inverse of the generator associated to w.

Retain a sampled relator only when all its three blocks belong to their corresponding V_t. For a retained relator uvw introduce the corresponding length-three relation in the formal generators. Discarded samples contribute no relation. Denote this finitely presented triangular group by Gamma_ell. Repeated sampled relators are retained with multiplicity when constructing its link; multiplicity does not change its group.

The three-block relation is cyclically reduced in these formal generators. Cancellation of adjacent formal block letters would mean adjacent blocks are inverse free-product normal forms; their two meeting syllables would then lie in the same factor, contrary to membership of the original word in S_ell. This includes the last/first boundary.

Use the link convention with three undirected edges

    {u^{-1},v}, {v^{-1},w}, {w^{-1},u}.

This is globally inverse-isomorphic to the link convention in Kotowski--Kotowski, Definition 2.12. There are no loops, because a loop would be an adjacent block cancellation. Multiple edges are allowed. Each retained sample contributes exactly three edges, independently of the contributions of the other samples. The three edges from one sample are not claimed to be independent.

### 3.1 Finite-index image, independent of probability

Map each formal block generator to that block's image in G_ell. Every imposed relation maps to a sampled relation and hence to the identity. Thus Gamma_ell surjects onto the subgroup H_ell of G_ell generated by all V_t, t in I.

We prove that already the subgroup H_0 generated by V_L in the original free product has index at most two for all L >= 4. For arbitrary letters a,b in B choose a common reduced suffix v of length L-1 such that av and b^{-1}v belong to V_L. Then

    (av)(b^{-1}v)^{-1} = ab,

so H_0 contains every product of two letters.

Here are the promised suffix choices, including the torsion issue. Pick a factor C different from the factors of a and b, possible because n >= 3. If L is even, any reduced suffix of length L-1 beginning in C works, since no even-length reduced word equals its inverse. If L is odd, then L >= 5. Choose a suffix of even length L-1 whose first and last syllables lie in C. It exists: at length four use factor sequence C,D,E,C with three distinct factors, and insert two-step backtracks to increase the length by two as needed. Now both av and b^{-1}v have first and last syllables in different factors, so they cannot equal their inverses. These choices use only nonempty factor alphabets.

For completeness, the subgroup K generated by all products ab is normal: for a letter c,

    c(ab)c^{-1} = (ca)(bc^{-1}) belongs to K.

In the quotient by K all letters have the same image, of order at most two. Thus K has index at most two; H_0 contains K, and its image H_ell also has index at most two in G_ell. No model-preserving replacement of arbitrary factors by free groups is required.

Property (T) passes to quotients and from a finite-index subgroup to the whole group. Therefore it remains to prove that Gamma_ell has property (T) with probability tending to one.

## 4. Exact expected-link matrix

Let E denote the adjacency matrix of the random link, counting edge multiplicities, and let bar E = E[E]. Define c_{tu} as the number of oriented edge incidences between block-length types t,u in one three-block cyclic pattern. For equal lengths c_{LL}=6. In increasing type order the unequal cases are

    e=1: C = [[2,2],[2,0]],       e=2: C = [[0,2],[2,2]].

Let h_t = sum_u c_{tu}. For vertices x in V_t and y in V_u with c_{tu} nonzero, put a=f(x), b=l(x), c=f(y), f=l(y), and h=ell-t-u. Then the exact identity is

    bar E[x,y] = (N_ell / Z_ell) c_{tu} A[a,c] T_h(b,f).     (4.1)

If c_{tu}=0 the entry is zero.

To check (4.1), consider an oriented corner with first block x^{-1} and second block y. Their common boundary is legal exactly when A[a,c]=1. The remaining block must belong to V_h, start in a factor different from l(y), and end in a factor different from f(x^{-1}), which is the factor of b. Its number of choices is T_h(f,b)=T_h(b,f). Each completion determines exactly one cyclic syllable word with the fixed cut positions. Uniform sampling supplies 1/Z_ell, and the number of corner occurrences of the prescribed two types is c_{tu}. Reversed corner orientations obey the same count; cyclic rotation and inversion preserve uniform counting. This argument explicitly enforces all three reduced-word boundaries. Rejection of inverse-fixed blocks is present in T_h and in the vertex set; no further conditioning of the random samples is used.

Summing (4.1) over destination endpoint classes and using (2.1)-(2.2), the expected degree of x is

    bar d_x = (N_ell / Z_ell) lambda^{ell-t+1} r_a r_b h_t (1+o(1)).    (4.2)

Indeed the summand of type u has endpoint sum proportional to

    sum_{c,f} A[a,c] r_c r_f^2 = lambda r_a.

Consequently all expected degrees are positive eventually, and for some fixed constants c_0,C_0>0,

    delta_ell := min_x bar d_x >= c_0 lambda^{d ell - ceil(ell/3)},
    M_ell := |V| <= C_0 lambda^{ceil(ell/3)}.                 (4.3)

Rounding N_ell changes none of these bounds. Since d>1/3, delta_ell grows exponentially while log M_ell is O(ell).

## 5. Spectral gap of the mean link

The mean walk bar P[x,y] = bar E[x,y]/bar d_x has rows that depend on x only through its type and two endpoints. It maps every function to a function constant on each endpoint class. Hence its nonzero eigenvalues equal those of the finite compressed stochastic matrix on labels (t,a,b), with entries

    hat P[(t,a,b),(u,c,f)]
        = v_u(c,f) bar E[x,y] / bar d_x.

This compression is exact and reversible: its stationary weights are endpoint-class size times the common expected degree. There are at most 2k^2 classes, independent of ell. All other eigenvalues of the full walk are zero. For sufficiently large L every class exists, by (2.1).

Equations (2.1), (2.2), (4.1), (4.2) give entrywise convergence of this fixed-size matrix to

    Q[t,u] P[a,c] r_f^2,         Q[t,u] = c_{tu}/h_t.        (5.1)

The limit is the tensor product of Q, P and the rank-one stochastic matrix R[b,f]=r_f^2. The spectra of the type matrices are explicit:

    e=0: Q=[1], spectrum {1};
    e=1: Q=[[1/2,1/2],[1,0]], spectrum {1,-1/2};
    e=2: Q=[[0,1],[1/2,1/2]], spectrum {1,-1/2}.

R has eigenvalues 1 and zero. P has simple eigenvalue 1 and remaining eigenvalues in [-rho,0], where rho<1. Therefore the eigenvalue 1 of the limit in (5.1) is simple, and all other eigenvalues are at most rho/2 < 1/2. For e=0 the sharper upper bound is zero. These conclusions follow from the tensor-product spectrum; in the unequal cases positive nonprincipal eigenvalues can occur as (-1/2) times a negative eigenvalue of P, and they must not be discarded.

Eigenvalues vary continuously for these fixed-size characteristic polynomials. The finite compressed walks have real spectra by reversibility. Thus, simultaneously for the three length residues, the smallest positive eigenvalue of the mean normalized Laplacian is eventually at least

    gamma := 1/2 + (1-rho)/4 > 1/2.                        (5.2)

More explicitly, the full mean walk has exactly one eigenvalue 1 and its second-largest eigenvalue is at most 1-gamma eventually; the extra zero eigenvalues cause no problem. This also proves eventual connectivity of the mean graph. This is a statement about the mean graph only; the next section supplies the random control.

## 6. Uniform random-link control without edge independence

Write the unnormalized random Laplacian as L = sum_{j=1}^{N_ell} L_j, where a discarded sample has L_j=0 and a retained one supplies its three-edge Laplacian. Each L_j is positive semidefinite, has row sums zero, and has operator norm at most six. One way to see the norm bound is to write it as a sum of three rank-one edge Laplacians, each of norm two. These matrices are independent across samples, which is precisely the independence used here.

Let bar D = diag(bar d_x) and z=bar D^{1/2} 1. Define X_j=bar D^{-1/2}L_j bar D^{-1/2}. Then X_j is positive semidefinite, kills z, and has norm at most 6/delta_ell. On the deterministic subspace z-perpendicular, the sum of its expectations is the mean normalized Laplacian, whose smallest eigenvalue is at least gamma by (5.2).

For any fixed epsilon in (0,1), the lower-tail matrix Chernoff inequality (Tropp, Corollary 5.2 and Remark 5.3), applied on that subspace, gives

    Pr[sum_j X_j is not >= (1-epsilon)gamma I on z-perp]
        <= M_ell exp(-epsilon^2 gamma delta_ell / 12).      (6.1)

Here the actual smallest eigenvalue of the expectation may exceed gamma; using the smaller threshold and the displayed weaker bound is valid.

The degree contribution of one sample at a fixed vertex is between zero and three. The scalar Chernoff upper tail, equivalently the one-dimensional case of the same theorem after dividing by three, and a union bound imply

    Pr[some d_x > (1+epsilon) bar d_x]
        <= M_ell exp(-epsilon^2 delta_ell / 9)             (6.2)

for 0<epsilon<1, using (1+epsilon)log(1+epsilon)-epsilon >= epsilon^2/3. No independence of degrees at different vertices is needed. Both bounds tend to zero by (4.3).

On the complementary high-probability event, for every real f with f'bar D 1=0,

    f' L f >= (1-epsilon)gamma f'bar D f,
    f' D f <= (1+epsilon) f'bar D f.

The first inequality also forces the kernel of L to consist only of constants, so the actual graph is connected and all actual degrees are positive. By the generalized Courant--Fischer variational principle, taking the codimension-one subspace f'bar D1=0, its actual normalized Laplacian gap is at least

    (1-epsilon)gamma/(1+epsilon).

It is not necessary to confuse orthogonality for D with orthogonality for bar D: Courant--Fischer maximizes over all codimension-one subspaces, and the one chosen above is legitimate. Choose once and for all

    0 < epsilon < (2gamma-1)/(2gamma+1).

The resulting lower bound is strictly greater than 1/2. Thus the actual triangular link is connected with normalized Laplacian gap >1/2 with probability tending to one, for every residue of ell modulo three.

## 7. Conclusion and audit boundaries

The triangular-presentation spectral criterion (Kotowski--Kotowski Theorem 2.13, citing Zuk's Proposition 6) now gives property (T) for Gamma_ell with probability tending to one. The criterion permits the multigraph link used here. Its inverse-isomorphic edge convention has the same spectrum. Section 3.1 gives an epimorphism onto an index-at-most-two subgroup of G_ell. Property (T) passes along the epimorphism and across that finite extension, establishing the claimed theorem.

The argument uses the published spectral criterion and matrix Chernoff theorem, plus standard Perron--Frobenius, min--max, and free-product normal-form facts. It does not independently reprove those established results. It does prove the model-specific kernel, the endpoint compression, torsion deletion, finite-index transfer, degree growth, and all three length-residue calculations.

There is no numerical simulation in the proof. The attached exact checker independently enumerates small cyclic relator spaces, compares the kernel against actual corner counts, tests the limiting gap by rational positive-definiteness, and checks finite-index suffix witnesses. It also rejects four deliberate errors in normal and optimized Python. Those finite tests cannot prove the asymptotic statements or property (T) itself.

An independent audit should particularly examine (4.1), the tensor-product limit (5.1) when the two lengths occur with different multiplicities, the inverse-fixed-word deletion estimates, the common-nullspace Chernoff application, and the finite-index transfer. A failure at one of these steps would invalidate the full-scope conclusion until corrected.

## References and current literature scope

1. Median Geometry and Applications, Oberwolfach Reports 23 (2026), report 8, pp. 487-540; Problem 16 on pp. 535-536. DOI: https://doi.org/10.4171/owr/2026/8 . Primary PDF: https://ems.press/content/serial-article-files/53603 .
2. Eduard Einstein, Suraj Krishna M S, MurphyKate Montee, Thomas Ng, Markus Steenbock, Random Quotients of Free Products, arXiv:2502.08630v2, submitted September 28, 2026; PDF internally dated September 29. The public arXiv record says 'To appear in Trans. AMS.' Definition 1.1, Theorem 1.2, Question 1.9. https://arxiv.org/abs/2502.08630v2 .
3. Marcin Kotowski, Michal Kotowski, Random groups and property (T): Zuk's theorem revisited, arXiv:1106.2242v2; Journal of the London Mathematical Society 88 (2013), 396-416. Definitions 2.12, Theorem 2.13, Remarks 2.10-2.11. https://arxiv.org/abs/1106.2242v2 ; https://doi.org/10.1112/jlms/jdt024 .
4. Joel A. Tropp, User-friendly tail bounds for sums of random matrices, arXiv:1004.4389v7; Foundations of Computational Mathematics 12 (2012), 389-434. Corollary 5.2 and Remark 5.3. https://arxiv.org/abs/1004.4389v7 ; https://doi.org/10.1007/s10208-011-9099-z .
5. Calum J. Ashcroft, Property (T) in random quotients of hyperbolic groups at densities above 1/3, arXiv:2202.12318v2. Theorems A-B concern random elements from word-metric annuli in a non-elementary hyperbolic group. These are not assumed to be identical to the present syllable model. https://arxiv.org/abs/2202.12318v2 .
6. Izhar Oppenheim, Property (T) for random groups in the density model with d>1/4, arXiv:2609.21255v1, September 18, 2026. Theorem 1.2 concerns the Gromov model along lengths divisible by four, rather than this free-product syllable model. This recent preprint was inspected to avoid repeating the outdated blanket claim that the Gromov upper threshold is still 1/3. It is not used in this proof. https://arxiv.org/abs/2609.21255v1 .

The current target webpage returned an access error (and HTTP 403 in the direct fetch). Its live contents were not verified. The exact-ID inherited record and the actual primary OWR problem were verified instead. Literature searches and inspection of the above current primary sources found no prior solution of this exact free-product question; that search result is not an exhaustive novelty guarantee.
