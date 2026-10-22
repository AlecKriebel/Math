# Strong pre-involutions: a scoped reciprocal-log bound

## 1. Exact problem and disposition

This note concerns 30001860 / OWR-11129-006. For a classical matrix group G on a natural module V of dimension N over a field of odd characteristic, put

Q(G) = {g in G : ord(g) is even, N/3 <= dim ker(g^(ord(g)/2)-I) < 2N/3}.

All interval endpoints here are intentional. Write p(G)=|Q(G)|/|G|. The original OWR problem session, printed p. 2154, asks for its asymptotic value and also prints p(G)=O(log N). The latter is true for every such group, uniformly: 0<=p(G)<=1<=log(N)/log(2) for N>=2. It does not answer the asymptotic-value question. LNP, p. 3 of the author-hosted version, explicitly discusses experimental evidence for O(1/log(rank)), with fixed q in {3,5,9,13} and dimensions at most 1000. That is a separately sourced research version, not a silent alteration of OWR.

Theorem A below establishes an order-of-magnitude upper bound on specified matrix families, conditional only on the published maximal-torus counting identity identified in Section 3. Together with the published lower bound it establishes a reciprocal-log order of magnitude for those families. It does not establish an asymptotic equivalent, a limiting coefficient, or the full range of all interpretations of Class(N,q). No novelty claim is made.

Throughout log means natural logarithm; v2(m) is the exponent of 2 in a positive integer m. U_N(q) means the full unitary ISOMETRY group on an N-dimensional space over F_(q^2). It is the group denoted GU_N(q) in LNP's Frobenius definition in Section 3.1; no group of unitary similitudes is included merely by notation.

### Theorem A (uniform upper bounds)

For every odd prime power q:

* For N>=2, p(GL_N(q)) and p(U_N(q)) are at most min(1,512/log N).
* For r>=2, p(Sp_(2r)(q)) and p(SO_(2r+1)(q)) are at most min(1,512/log r).
* For r>=2 and either sign, p(SO^+_(2r)(q)) and p(SO^-_(2r)(q)) are at most min(1,1024/log r).

The constants are deliberately loose. The bounds are uniform in q and dimension, so q may also vary with dimension. For the same families with Lie rank at least two, LNP Theorem 1.1 supplies the lower bound 1/(5000 log_2(rank)). Thus these families have p(G)=Theta(1/log(rank)), with constants independent of odd q. For GL/U use rank=N-1. Dimension and rank are not identified literally.

For SL_N(q)<=H<=GL_N(q), the same natural-module predicate gives p(H)<=[GL_N(q):H] p(GL_N(q)) <= (q-1)512/log N. For SU_N(q)<=H<=U_N(q) replace q-1 by q+1. Combined with LNP, this proves Theta_q(1/log N) for these intermediate groups at fixed q, uniformly over H for that q. This argument does NOT prove a q-uniform upper bound for SL or SU.

## 2. Algebraic and centralizer reductions

### Lemma 2.1 (semisimple dependence and maximum valuation)

In odd characteristic write the multiplicative Jordan decomposition as g=su=us. Since ord(u) is a power of the odd characteristic and ord(s) is prime to it, ord(g)=ord(s)ord(u). If ord(g) is even then

g^(ord(g)/2)=s^(ord(s)/2).

Indeed u is killed by the exponent, while s^(ord(s)/2) is an involution and its odd power ord(u) is itself. If ord(g) is odd there is no involution. Consequently Q is conjugacy invariant and depends only on s.

Let 2^j be the largest 2-part of the orders of the eigenvalues of s over an algebraic closure. If j=0, g has odd order. Otherwise s^(ord(s)/2) acts as -1 precisely on the sum of eigenspaces whose eigenvalues have order with 2-part 2^j, and as +1 on all the other eigenspaces. To see this, write ord(s)=2^j m with m odd. An eigenvalue of order with smaller 2-part is killed by 2^(j-1)m. An eigenvalue with maximal 2-part has half of its even order dividing this exponent with odd quotient, and hence yields -1. Multiplicities are retained. Thus the minus-space dimension is the total multiplicity at the maximal nonzero valuation.

### Lemma 2.2 (exact involution fibers)

For any finite group and any conjugacy-closed set I of involutions, let F_t={g:ord(g) even and g^(ord(g)/2)=t}. Then

|PreInv(G,I)|/|G| = sum over G-class representatives t in I of |F_t|/|C_G(t)|.

Proof: each g has exactly one cyclic involution, so the fibers are disjoint. An element of F_t commutes with its power t. Conjugation transports fibers, and the class of t has |G|/|C_G(t)| elements. Sum and divide by |G|.

For GL_N(q), let A_(m,j) be the proportion of a in GL_m(q) such that the 2-part of ord(a) is 2^j and a^(ord(a)/2)=-I, and let B_(k,j-1) be the proportion in GL_k(q) having 2-part order at most 2^(j-1). Then the exact identity is

p(GL_N(q)) = sum_{N/3<=k<2N/3} sum_{j>=1} A_(N-k,j) B_(k,j-1).

Here the outer sum is over integer k. Proof: each involution with plus-space dimension k is conjugate to diag(I_k,-I_(N-k)); its centralizer is GL_k x GL_(N-k). Its fiber consists exactly of pairs with smaller 2-part order in the first factor and scalar powered involution -I in the second factor at their maximal valuation. Lemma 2.2 cancels the centralizer orders. This identity alone supplies no asymptotic estimates for its factors.

## 3. Published transfer input and exact colored models

We use the following published theorem, not a numerical assumption: LNP Lemma 2.3 (author version p. 6), with its Lemma 2.1 counting proof, says that for a conjugacy-closed semisimple-dependent set Q in a connected finite reductive group, its proportion is

sum_C (|C|/|W|) (|Q intersect T_C|/|T_C|),

where C ranges over Frobenius-conjugacy classes in its Weyl group, and T_C is the associated rational maximal torus. The application is justified by Lemma 2.1 above. The input depends on standard rational-torus and unipotent-centralizer counting theorems; those results are credited, not claimed proved afresh here.

LNP Sections 3.1-3.4 and 5(i),(vi) give the tori and their actions used below. For GL_N(q), choose a uniform permutation of N labels. Each cycle of length d contributes an independent uniform element of the cyclic group of order q^d-1; the cycle accounts for d natural eigenvalue positions. For U_N(q), replace its order by q^d-(-1)^d. In either case assign to a cycle the color j equal to the v2 of the order of that cyclic element. Its powered involution is -1 on the entire block exactly when its color is the positive maximum among all cycles. The proportion p is exactly the probability that this maximal-color mass M satisfies N/3<M<=2N/3.

For Sp_(2r)(q) and SO_(2r+1)(q), choose a uniform permutation on r labels and give each cycle an independent equiprobable sign. A positive cycle of length d contributes a cyclic group of order q^d-1; a negative cycle contributes order q^d+1. Its natural block dimension is 2d. In SO_(2r+1) the additional natural eigenvalue is 1. Thus the target implies M>r/3; for Sp it is precisely r/3<M<=2r/3. These are equality models for the original predicates before the indicated relaxation.

For SO^+_(2r) condition the signed-permutation model on an even number of negative cycles; for SO^-_(2r), on an odd number. These are LNP's type D and twisted type D descriptions. Each conditioning event has probability 1/2 for r>=1: every permutation has at least one cycle and its independent signs have unbiased product. Conditional probabilities of any event are therefore at most twice its unconditional probability. Possible splitting of Weyl conjugacy classes does not change the sum over all their elements in the counting identity.

For a cyclic group with order of v2 equal to t, the color probabilities are

w_0(t)=2^(-t), and w_j(t)=2^(j-1-t) for 1<=j<=t, with w_j(t)=0 otherwise.

The probability of color at most j is b_j(t)=min(1,2^(j-t)). These formulas follow by counting the elements of each order in its cyclic Sylow 2-subgroup. All independent choices in this section are exact finite uniform distributions, not heuristic random-matrix approximations.

### Exact coefficient version for the control program

For the unsigned models let w_j(d) be the cycle-color probabilities and b_(j-1)(d) their cumulative probabilities below j. For the signed model use the averages over the two signs. Define

A_j(z)=exp(sum_{d>=1} w_j(d) z^d/d),
B_(j-1)(z)=exp(sum_{d>=1} b_(j-1)(d) z^d/d).

The probability that the positive maximal color is j and its mass is exactly m is

[z^m]A_j(z) * [z^(n-m)]B_(j-1)(z), for m>=1.

Proof: split the permutation into the labels in color-j cycles and all remaining labels. For a chosen m-label subset, cycle-count enumeration gives the two displayed normalized coefficients; the binomial choice of the subset cancels the factor m!(n-m)!/n!. Requiring all remaining colors below j makes the maximal color exactly j. Summing over n/3<m<=2n/3 and over j gives the exact GL, U, and Sp predicates. This is the formula implemented in verify.py; it is not used as a numerical substitute for the upper-bound proof.

## 4. Permutation estimates with complete proofs

Take a uniform permutation of n labels and independently color each cycle of length d according to any given distribution w_j(d). Let E_j mean that every color is at most j. Set B_j(n)=Pr(E_j), B_j(0)=1, and let M_j be the sum of lengths of color-j cycles.

### Lemma 4.1 (cycle pointing)

E[M_j 1_(E_j)] = sum_{d=1}^n w_j(d) B_j(n-d).

Proof: the expected number of d-cycles satisfying a specified cycle property and a remainder property is (1/d) times the cycle-property probability times the probability of the remainder property in a uniform permutation on n-d labels. Explicitly, choose its d labels, order them in (d-1)! cyclic ways, and choose the remaining permutation in (n-d)! ways; division by n! gives 1/d. Multiply by the mass d and sum. Color-j itself satisfies the cutoff E_j.

In particular, if p_j is the target probability with maximal color j and M_j>n/3, then

p_j <= (3/n) sum_{d=1}^n w_j(d) B_j(n-d).       (4.1)

Also p_j<=B_j(n). The target's upper endpoint is not needed for this upper bound.

### Lemma 4.2 (fractional cycle avoidance)

Suppose cycles whose length is divisible by L are independently accepted with probability 1-rho, and all other cycles are accepted. Write U_(L,rho)(m) for the probability that all cycles are accepted. For 0<rho<1,

U_(L,rho)(m) = product_{i=1}^{floor(m/L)} (1-rho/(Li))
             <= (floor(m/L)+1)^(-rho/L).             (4.2)

Proof: the cycle-index exponential formula follows directly by summing cycle counts c_d with weight product 1/(d^(c_d)c_d!): its generating function is exp(sum a_d z^d/d), where a_d are the acceptance probabilities. It is (1-z)^(-1)(1-z^L)^(rho/L). The coefficient at z^m is the sum of the first floor(m/L)+1 coefficients of (1-x)^(rho/L), namely product_{i=1}^k(1-rho/(Li)); this finite binomial identity follows by induction on k. Finally log(1-x)<=-x and sum_{i=1}^k1/i>=log(k+1), giving (4.2). No complex-analytic transfer theorem is involved.

If the actual acceptance probabilities b_j(d) are bounded above by these model acceptance probabilities, then B_j(m)<=U_(L,rho)(m): couple the independent acceptance test on each cycle using one uniform random number. In particular, if b_j(d)<=t<1 for all d then

B_j(m) <= product_{i=1}^m(1-(1-t)/i) <= (m+1)^(-(1-t)).       (4.3)

### Lemma 4.3 (dyadic sum)

For c>0 and n>1, summing over powers of two h with 2<=h<=n gives

sum h^(-1) exp(-log(n/h)/(c h)) <= 8c/log n + 2/sqrt(n).      (4.4)

Proof: the tail h>sqrt(n) is less than 2/sqrt(n). On the rest log(n/h)>=log(n)/2. Put L=log(n)/(2c). For each h,

h^(-1)exp(-L/h) <= 4 integral_h^(2h) x^(-2)exp(-L/x) dx,

since on that interval x^(-2)>=1/(4h^2) and exp(-L/x)>=exp(-L/h). The dyadic intervals are disjoint up to endpoints. The integral over (0,infinity) equals 1/L by y=L/x. This proves the remaining bound 4/L.

### Lemma 4.4 (one high layer)

Suppose w_j(d)=0 unless h divides d, w_j(d)<=w, and b_j(d)<=1-rho whenever 2h divides d. If h is a power of two with 2<=h<=n and alpha=rho/(2h)<=1/2, then

p_j <= (24w/h)(n/h)^(-alpha).                  (4.5)

Proof: (4.1)-(4.2) give a sum over d=hj. Write n=hN+r_0, 0<=r_0<h. Then floor((n-hj)/(2h))=floor((N-j)/2). Consequently

sum_{j=1}^N (floor((N-j)/2)+1)^(-alpha)
 <= 2 sum_{i=1}^{ceil(N/2)}i^(-alpha)
 <= 4 N^(1-alpha),

using sum_{i=1}^K i^(-alpha)<=K^(1-alpha)/(1-alpha) and alpha<=1/2. Hence p_j<=12w N^(1-alpha)/n <=12w N^(-alpha)/h. Since N>=n/(2h) and 2^alpha<=2, (4.5) follows.

## 5. Linear and unitary upper bounds

Set a=v2(q-1), b=v2(q+1), so min(a,b)=1. For GL the v2 of a cycle factor's order is

t_d=a for odd d;  t_d=a+b+v2(d)-1 for even d.       (5.1)

For U the same formula holds after swapping a and b. Formula (5.1) follows from q^(2m)-1=(q^m-1)(q^m+1): squaring successively adds exactly one factor of two after the first squaring, while an odd exponent leaves v2(q-1) unchanged. We prove the result for either ordered pair (a,b) of positive integers with min(a,b)=1.

Low layers first:

* For 1<=j<a, w_j(d)<=delta_j=2^(j-1-a), b_j(d)<=2^(j-a)<=1/2, and sum_{j<a}delta_j<1/2. Equations (4.1),(4.3) and sum_{r=1}^n r^(-1/2)<=2 sqrt(n) bound their combined contribution by 3 n^(-1/2).
* For j=a, odd cycles are accepted and even cycles have b_j(d)<=1/2. Thus p_a<=U_(2,1/2)(n)<=2^(1/4)n^(-1/4).
* For a<j<a+b, marking is possible only on even cycles, w_j(d)<=delta_j=2^(j-a-b-1), and sum delta_j<1/2. Again even cycles have b_j(d)<=1/2. With B_j(r)<=2^(1/4)(r+1)^(-1/4), (4.1) and sum_{r=1}^n r^(-1/4)<=(4/3)n^(3/4) give at most 2*2^(1/4)n^(-1/4).

Empty layer ranges contribute zero. Since 2^(1/4)<4/3, all low layers together contribute at most 7 n^(-1/4).

For each high layer j>=a+b, put h=2^(j-a-b+1). Its possible cycle lengths are precisely multiples of h. For d=hk with t_d>=j,

w_j(d)=1/(2*2^(v2(k)))<=1/2.

For 2h|d, b_j(d)<=1/2. Lemma 4.4 with w=1/2, rho=1/2 bounds this layer by

(12/h) exp(-log(n/h)/(4h)).

When h>n the layer is impossible. Apply Lemma 4.3 with c=4. The total upper bound is

7 n^(-1/4) + 384/log n + 24/sqrt(n).

For n>1, log n <= n^delta/delta for any delta>0 (integrate x^(delta-1)>=1/x from 1 to n and weaken). Therefore n^(-1/4)<=4/log n and n^(-1/2)<=2/log n. The preceding bound is at most 460/log n, hence at most 512/log n. The transfer in Section 3 proves Theorem A for GL and U.

## 6. Signed-cycle upper bounds

Put a=v2(q-1), b=v2(q+1), c=max(a,b)>=2. A positive cycle has the t_d from (5.1); a negative cycle has v2(q^d+1)=b for odd d and 1 for even d. Average both color distributions with weight 1/2, as required by independent cycle signs.

For j=1, at every length at least one of the two signs has factor-order valuation at least two. Thus b_1(d)<=3/4, and p_1<=n^(-1/4).

For 2<=j<c, at each length one sign has factor-order valuation 1 and the other at least c. Thus b_j(d)<=3/4 and w_j(d)<=delta_j=2^(j-c-2). The sum of these delta_j is less than 1/4. Equation (4.1) with (4.3) gives combined contribution at most n^(-1/4).

For j=c, at every even length the positive factor has valuation at least c+1 and the negative factor has valuation 1. Hence b_c(d)<=3/4 on even d. Consequently p_c<=U_(2,1/4)(n)<=2^(1/8)n^(-1/8). All low layers together are at most 4n^(-1/8).

For j>=c+1 put h=2^(j-c). Marking occurs only on positive cycles whose lengths are multiples of h. Averaging the signs gives w_j(d)<=1/4, and whenever 2h divides d the acceptance probability is at most 3/4. Lemma 4.4 with w=1/4, rho=1/4 gives

p_j <= (6/h) exp(-log(n/h)/(8h)).

Summing by Lemma 4.3 with c=8 gives total at most

4n^(-1/8)+384/log n+12/sqrt(n) <=440/log n<=512/log n.

Use n=r in the Weyl model. For Sp_(2r) the target requires M>r/3. For SO_(2r+1) it requires 2M>(2r+1)/3, which again implies M>r/3. Conditioning the signed model by the appropriate sign-product parity proves the factor-two upper bound for each even orthogonal type. This finishes Theorem A.

The finite-index assertion in Section 1 follows simply because Q(H)=Q(G) intersect H for a subgroup in the SAME natural representation, and |Q(H)|<=|Q(G)|. No analogous argument from a subgroup to a larger group, or to a central quotient, has been used.

## 7. Exact rank-two and quotient controls

For every odd q put a=v2(q-1). Then

p(GL_2(q))=(1-4^(-a))/3, while p(SL_2(q))=0.       (7.1)

Proof: the qualifying involutions in GL_2 form the class of diag(1,-1), whose centralizer is the product of two copies of F_q^*. In the corresponding fiber one eigenvalue has color j>=1 and the other smaller color. Lemma 2.2 gives sum_{j=1}^a 2^(j-1-a)*2^(j-1-a)=sum_{j=1}^a4^(j-1-a)=(1-4^(-a))/3. In SL_2 every involution in odd characteristic is -I (diagonalizability and determinant one); its fixed-space dimension is zero, which is outside the target interval.

Thus fixing N=2 and letting q tend to infinity does not give a common limit for GL_2: q=3^(2k+1) has a=1 and p=1/4; q=3^(2^k), k>=1, has a=k+2 and p tends to 1/3. Both are sequences of odd prime powers tending to infinity. This does not contradict any rank-growth assertion.

For GL_3(3), t=diag(1,-1,-1) belongs to Q because its plus-space dimension is 1. Its scalar multiple -t has plus-space dimension 2 and is excluded by the strict upper endpoint. They have the same image in PGL_3(3). Hence the literal Q predicate is not constant on central cosets and cannot be imposed on a projective element by choosing an arbitrary lift. LNP's projective lower-bound corollary instead specifies an image set of involutions; its exact predicate must be used in a separate argument.

## 8. Precisely what remains

No asymptotic equivalent p(G)~C/log(rank), no existence or value of lim log(rank)*p(G), and no uniform description of any possible oscillation is proved here, even for GL. The bounded finite computations are checks of identities and implementation, not evidence replacing those missing estimates.

The q-uniform reciprocal-log upper bound has NOT been proved here for determinant-constrained SL/SU intermediates, conformal/similitude extensions, all disconnected orthogonal groups, Spin/half-spin forms, or central/projective quotient predicates. The fixed-q finite-index result stated above is only for subgroups of GL and U. No conclusions about those other families are inferred from their similar names.

Thus the broad asymptotic-value request remains unresolved in this work. The retained positive result is an explicit, proved order-of-magnitude bound for the listed natural matrix families and a fixed-q extension to SL/SU intermediates, together with exact reductions and counterexamples to parameter/quotient conflations.

## References used

[LNP] F. Lübeck, A. C. Niemeyer, C. E. Praeger, Finding involutions in finite Lie type groups of odd characteristic, Journal of Algebra 321 (2009), 3397-3417, DOI 10.1016/j.jalgebra.2008.05.009. Author-hosted version: https://www.math.rwth-aachen.de/~Frank.Luebeck/preprints/powerinvReprint.pdf . Specifically Theorem 1.1/Table 1, discussion p. 3, Lemmas 2.1-2.3, Sections 3 and 5.

[OWR] Computational Group Theory, Oberwolfach Reports 8 (2011), 2113-2161, DOI 10.4171/OWR/2011/37, problem session p. 2154. https://ems.press/journals/owr/articles/11129 .
