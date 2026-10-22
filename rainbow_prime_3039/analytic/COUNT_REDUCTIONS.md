# Rainbow 4AP: exact counts, a pairwise-data obstruction, and a uniformity criterion

Authored 2026-10-20. This is partial analysis, not a resolution or novelty claim. All progressions below are ordered (a,d), and p>3 is prime.

## 1. Exact inclusion-exclusion

Put N=p(p−1), n_i=|A_i|, and D=Σ_i n_i(n_i−1). For each of the six position pairs r<s in {0,1,2,3}, (a,d)↦(a+rd,a+sd) bijects the nonzero-d progression parameters with ordered distinct points. Thus the count of progressions whose r,s colors agree is D.

Let R,S,U,V,W count exact color-multiplicity types 1111,211,22,31,4, respectively. Counting equal-color position pairs gives

N=R+S+U+V+W,
6D=S+2U+3V+6W,
R=N−6D+U+2V+5W.

Equivalently, let P be the sum over the three pair partitions of the count satisfying both equalities (the two pair colors need not differ), and let T be the sum over the four position triples of the monochromatic-triple count. Then P=U+3W and T=V+4W, so

R=N−6D+P+2T−6W.

This is also partition-lattice inclusion-exclusion: coefficients for block types 2,22,3,4 are −1,+1,+2,−6. For balanced class sizes write p=4q+r, r∈{1,3}. Then

D=(p²+3)/4−p,
6D−N=(p²−10p+9)/2.

Hence R>0 is equivalent to U+2V+5W>(p²−10p+9)/2. This equivalence by itself is not new control of the unknown higher-order counts.

## 2. Exact pairwise information alone does not imply a rainbow

Here is a rigorous obstruction to any proof that uses only the single/pair color marginals and abstract probability inequalities. It does NOT construct an actual coloring of Z_p.

For every prime p≥10000 and any almost-balanced vector (n_1,...,n_4), there is an exchangeable random color vector (C_0,C_1,C_2,C_3), never rainbow, such that for every r≠s,

Pr(C_r=i,C_s=j)=Q_ij:=n_i(n_j−1_{i=j})/[p(p−1)].

These are exactly all the pair-color marginals forced by an actual almost-balanced coloring along a uniformly sampled nondegenerate 4AP.

Proof. For a non-rainbow count vector k=(k_1,...,k_4) of nonnegative integers summing to four, let the law uniformly permute a multiset with these counts. Its pair matrix M(k) has diagonal entries k_i(k_i−1)/12 and off-diagonal entries k_i k_j/12.

First choose multiplicity types 211,22,31,4 with respective probabilities 59/100,35/100,5/100,1/100, and within each type choose the count vector uniformly. There are respectively 12,6,12,4 such count vectors. The resulting law is color-symmetric. Its probability of equal colors at a fixed pair is

(59/100)/6+(35/100)/3+(5/100)/2+1/100=1/4.

Consequently its pair matrix is Q^0_ij=1/16 for all i,j. Every count vector has positive mass; in particular each 31 vector has mass 1/240 and each 4 vector has mass 1/400.

Let Δ=Q−Q^0. For each i<j add weight 4Δ_ij to the count vector 3e_i+e_j. Add weight

a_i=Δ_ii−2Σ_{j>i}Δ_ij

to 4e_i. Leave all other weights unchanged. The matrix of 3e_i+e_j has off-diagonal entries (i,j),(j,i) equal to 1/4 and diagonal i equal to 1/2. The proposed changes therefore alter the pair matrix by exactly Δ. Their total weight is

Σ_i a_i+4Σ_{i<j}Δ_ij=Σ_iΔ_ii+2Σ_{i<j}Δ_ij=0,

since both pair matrices have total sum one.

Write n_i=p/4+e_i, |e_i|≤3/4. Direct expansion gives |Δ_ij|≤1/p for p≥6: off-diagonal numerators are p[(e_i+e_j)/4+1/16]+e_i e_j; diagonal numerators are p(e_i/2−3/16)+e_i²−e_i; all are divided by p(p−1). Thus every changed 31 weight stays positive when 4/p<1/240, and every changed 4 weight stays positive when 7/p<1/400. Both hold for p≥10000. The modified weights are a probability law, supported on non-rainbow count vectors, with the required pair matrix. Its one-coordinate marginal is the row sum of Q, namely n_i/p. QED.

Interpretation: even the exact finite-p pair marginals leave room for zero rainbow mass. A successful proof must exploit consistency between different arithmetic progressions, higher-order information, or another property not encoded in those marginals. This is not an impossibility theorem for analytic methods in general.

## 3. Walsh identity (four colors identified with F_2²)

Let χ range over the three nontrivial characters of F_2², and define s_χ(x)=χ(c(x)). Set H_χ=Σ_{a,d≠0}Π_{j=0}^3 s_χ(a+jd). The number X of progressions whose four color labels have xor zero satisfies

X=(N+Σ_χ H_χ)/4.

The xor-zero patterns are exactly 1111,22,4, so X=R+U+W. Therefore

R=(N+Σ_χ H_χ)/4−P+2W.

This identity does not give a sign for H_χ. Almost-balancedness gives |Σ_x s_χ(x)|=1, not a bound on these four-point correlations.

## 4. A sufficient U³-uniformity condition

Use normalized averages on Z_p and let f_i=1_{A_i}−α_i, α_i=n_i/p, δ=max_i ||f_i||_{U³}. The normalized U³ norm is the eighth root of the cube average Π_{ω∈{0,1}³} C^{|ω|}f(x+ω·h).

Then the actual rainbow count obeys

R/p² ≥ 24α_1α_2α_3α_4−30δ.

Proof. Write Λ(g_0,g_1,g_2,g_3)=E_{a,d} Π_j g_j(a+jd), now INCLUDING d=0. The standard generalized von Neumann inequality for four-term APs over Z_p (p>3) bounds |Λ| by the U³ norm of any one argument when all arguments are 1-bounded. For a fixed permutation (i,j,k,l) of the colors, telescoping and pairwise independence over all (a,d) give exactly

Λ(1_{A_i},1_{A_j},1_{A_k},1_{A_l})−α_iα_jα_kα_l
=Λ(f_i,1_{A_j},1_{A_k},1_{A_l})+α_iΛ(1,f_j,1_{A_k},1_{A_l}).

The omitted last two telescoping terms vanish because the relevant centered factor has zero mean and any two distinct AP positions are independent under the full (a,d) average. Each displayed term is bounded in modulus by δ and α_iδ. Summing over the 24 permutations gives total error at most 24δ+6(Σ_iα_i)δ=30δ. The sum of the left-hand counts is R/p², because d=0 can never have four distinct colors. QED.

In particular δ<(4/5)Π_iα_i suffices. For asymptotically balanced colorings the threshold tends to 1/320. Equivalently, any rainbow-free almost-balanced coloring must have a centered color-class indicator with U³ norm at least (4/5)Π_iα_i=1/320+O(1/p).

This is a conditional result, not a solution: balancedness alone does not imply U³-uniformity. The generalized von Neumann input is standard, not claimed as original. Primary-source reference: Terence Tao, “254B, Notes 3: Linear patterns,” 23 April 2010, Exercise 23, with the four-term-AP system of Cauchy–Schwarz complexity two. https://terrytao.wordpress.com/2010/04/23/254b-notes-3-linear-patterns/ . This source was inspected on 2026-10-20. The inequality also follows directly by three Cauchy–Schwarz steps for this AP system.

## Scope conclusion

No unconditional lower bound for R, asymptotic counterexample, or resolution of the prime-modulus question is established here. The concrete outputs are verified count identities, an exact pair-marginal relaxation obstruction, and a standard-uniformity conditional criterion with an explicit constant.
