# Exact labeled-tree height control and two diagonal permuton limits

## Theorem

For each n, let Pi_n be exactly uniform among permutations of size n avoiding 2431, or exactly uniform among those avoiding 3241. Its square-spread permuton converges weakly in probability to Law(U,U), where U is uniform on [0,1]. More precisely, for every epsilon>0 there are constants c_epsilon>0, C_epsilon<infinity and N_epsilon such that, for n>=N_epsilon,

P(d_BL(mu_{Pi_n},Law(U,U))>epsilon) <= C_epsilon exp(−c_epsilon n).

Here d_BL is the bounded-Lipschitz metric for the Euclidean square. Equivalently, uniform 1342-avoiders have the anti-diagonal limit Law(U,1−U), with the same form of fixed-deviation bound. These are the two cases alpha=132 and alpha=213 of avoidance of alpha skew-sum 1. The assertion for every fixed nonempty alpha is not proved here.

The proof uses Bóna’s established permutation–tree bijection and counting series, then derives an exact-label weighted tree-height estimate. No priority claim is made.

## 1. Credited combinatorial input and conventions

Miklós Bóna, *Exact enumeration of 1342-avoiding permutations: a close link with labeled trees and planar maps*, J. Combin. Theory Ser. A 80 (1997), 257–272; primary preprint https://arxiv.org/abs/math/9702223, especially Definition 1, Lemma 2, Theorem 1, Corollary 2 and equation (4).

A beta(0,1) tree here is a rooted ordered tree with nonnegative integer labels: leaves have label zero; the root has the sum of its children's labels; each nonroot internal vertex has label at most one plus the sum of its children's labels. The one-vertex tree is allowed. Its size is its vertex count and height is its maximum edge-depth.

Bóna's bijection sends skew-indecomposable 1342-avoiders of size n to these labeled trees on n vertices. His term “indecomposable” is explicitly skew-indecomposable. On erasing labels, the underlying ordered tree corresponds to the unique 132-avoider with the same positions and values of left-to-right minima. That 132-avoider is read in postorder, recursively assigning successive child subtrees decreasing value intervals and assigning the maximum to the root. The bijection extends componentwise from all 1342-avoiders to ordered forests of beta trees; components are combined by skew sum. Uniform permutations therefore correspond exactly to uniform labeled forests of total size n, not to uniform unlabeled forests.

Write T(z)=sum t_n z^n for the beta-tree counting series. Bóna's equation (4) gives

T(z) = [8z^2+12z−1+(1−8z)^(3/2)]/(32z)
     = z+z^2+3z^3+12z^4+56z^5+288z^6+... .                 (1)

Bibliographic caution: the preprint's displayed closed formula for t_n is shifted relative to its vertex convention; its displayed denominator for the full-avoidance series also contains a separate typographical inconsistency. We use equation (4), not those conflicting displays. Expanding (1) gives t_1=1 and, for n>=2,

t_n=3*2^(n−2)*(2n−2)!/[(n+1)!(n−1)!].                     (2)

Consequently, with rho=1/8,

t_n ~ [3/(16 sqrt(pi))] rho^(−n) n^(−5/2).               (3)

The forest series is A(z)=1/(1−T(z)), and T(rho)=5/32<1. No claim that a uniform forest has a particular largest-component law is needed below.

## 2. Relaxed-root labeled trees and a catalytic generating function

Let B be the class of rooted ordered trees with zero-labeled leaves, and with EVERY internal vertex, including the root, permitted a label in {0,...,1+sum(child labels)}. Let

B(z,u)=sum_{Q in B} z^|Q| u^label(root(Q)),

as a formal series in z with polynomial coefficients in u. The combinatorial specification immediately gives

T(z)=z/(1−B(z,1)),                                      (4)

because the root label of a beta tree is uniquely determined by its sequence of B children. Let C(z)=B(z,1)/(1−B(z,1)). Separating the singleton tree from a nonempty sequence of children and summing the allowed root labels gives

B(z,u)=z+z/(1−u)*[ C(z)−u^2 B(z,u)/(1−B(z,u)) ].          (5)

The right side at u=1 is interpreted by continuity. For u≠1, multiplying out yields

(1−u)(B−z)(1−B)−z C(z)(1−B)+z u^2 B=0.                 (6)

All counts in this construction are exact counts of labeled trees. There is no independence assumption on the unlabeled shape or labels.

For real 0<z<rho, set s=sqrt(1−8z), so 0<s<1. Equations (1) and (4) give

T(z)=(1−s)(s^2+10s+5)/[32(s+1)],
B(z,1)=(1−s)(3s+1)/(s^2+10s+5),
C(z)=(1−s)(3s+1)/[4(s+1)^2].                            (7)

Fix u=3/2, and denote b(z)=B(z,3/2). Solving (6) with b(0)=0 gives

b(z)=[s^3+3s^2+2s+2−s^(3/2)*sqrt(s^3+6s^2+33s+24)]
     /[8(s+1)].                                        (8)

This formula is valid for the generating series throughout 0<=z<rho. Here are the analytic details needed to avoid assuming its convergence: the formal series is the root of (6) with constant term zero. At z=0 and B=0 the derivative of the left side of (6) with respect to B is 1−u=−1/2, so the analytic implicit function theorem gives a positive radius of convergence. Near z=0 this selects (8). The formula is real analytic at every point of (0,rho), its discriminant there is positive, and its denominators are nonzero. Since its Taylor coefficients count nonnegative objects, if its radius of convergence were less than rho, Pringsheim's theorem would force a singularity on that positive real radius. Formula (8) supplies analytic continuation across each such point, a contradiction.

In particular b(z)<1/4 for z<rho, b(rho)=1/4 by monotone convergence, and expansion at s=0 gives

b(z)=1/4−(sqrt(6)/4) s^(3/2)+O(s^2).                    (9)

Strict b(z)<1/4 also follows from its strictly positive coefficients and its finite limit.

## 3. A marked-depth bound for the exact labeled law

For h>=0 define

W_h(z,u)=sum_{Q in B} z^|Q| u^label(root(Q))
                      * #{vertices of Q at depth h}.

Thus W_0=B. At u=3/2 and 0<z<rho, every W_h is finite: its coefficients are bounded by those of z*partial_z B(z,3/2), because a size-n tree has at most n depth-h vertices. The latter derivative series converges for z<rho. For u>1 and an internal vertex whose child labels total S,

sum_{k=0}^{S+1}u^k = (u^(S+2)−1)/(u−1) <= u^(S+2)/(u−1).

To distinguish a vertex at depth h+1, distinguish the child containing it, then choose an arbitrary ordered sequence of children to its left and to its right. Weighting the distinguished subtree by W_h and the other subtrees by B proves, whenever the series converge,

W_{h+1}(z,u) <= [z u^2 / ((u−1)(1−B(z,u))^2)] W_h(z,u).

Therefore, at u=3/2,

W_h(z,3/2) <= b(z) M(z)^h,
M(z)= (9z/2)/(1−b(z))^2.                               (10)

Every beta tree is a relaxed-root tree with the same labels, since equality to the sum is among the relaxed allowed labels. Thus the NUMBER of beta trees having height at least h, weighted by z^size, is at most W_h(z,3/2): each such tree has a depth-h vertex, and u^rootlabel>=1. This is an upper bound only; no claim that the labeled laws coincide is made.

Using (9), z=(1−s^2)/8, and 1−b(rho)=3/4 gives

M(z)=1−(2 sqrt(6)/3) s^(3/2)+O(s^2)
    =1−(2 sqrt(6)/3)(1−8z)^(3/4)+O(1−8z).               (11)

In particular M(z)<1 for all z sufficiently close to rho from below. In fact M(z)<1 for every 0<z<rho follows from z<rho and b(z)<1/4, but the fractional-power expansion is essential in the next step.

For any fixed epsilon>0, choose z<rho sufficiently close to rho that

log(rho/z)+epsilon log M(z)<0.                          (12)

Such z exists: putting delta=1−8z, the first term equals delta+O(delta^2), whereas the second equals −epsilon*(2 sqrt(6)/3) delta^(3/4)+O(delta). The negative delta^(3/4) term dominates.

Let Q_n be uniform among the t_n beta trees on n vertices. Taking h=ceil(epsilon n), nonnegativity, (10), and (3) give

P(height(Q_n)>=h)
 <= z^(−n)b(z)M(z)^h/t_n
 <= C_z n^(5/2) [(rho/z)M(z)^epsilon]^n.                 (13)

For all sufficiently large n this is exponentially small in n by (12). This proves height(Q_n)/n→0 in probability under the exact UNIFORM LABELED-tree law.

## 4. Exact forest extension without a component-size assumption

Let H(F) be the maximum component height of a forest. A forest with H(F)>=h has a distinguished depth-h vertex in some component. Components before and after it have generating series A(z). Hence the total generating series of such forests, counting with multiplicity if needed, is at most

A(z)^2 W_h(z,3/2) <= A(z)^2 b(z)M(z)^h.                 (14)

This uses the beta-to-relaxed-root injection only for the marked component; the unmarked components remain actual beta trees. For the exact uniform forest F_n of total size n, its denominator a_n=[z^n]A(z) is at least t_n. Thus

P(H(F_n)>=ceil(epsilon n))
 <= C_z A(z)^2 n^(5/2) [(rho/z)M(z)^epsilon]^n→0.        (15)

Indeed the tail is exponentially small for each fixed epsilon>0. This is a whole-forest estimate under the correct uniform measure, not a statement deduced from uniform Catalan tree height.

## 5. Deterministic one-sided geometry and weak convergence

For completeness the needed shape lemma is stated and proved. For a rooted ordered tree T on k vertices, construct its associated 132-avoiding skew-indecomposable permutation q recursively: assign the largest value k to the root; allocate child subtrees value intervals in decreasing order from left to right; read nodes in postorder. If a leaf v appears in postorder position i and has edge-depth d, its assigned value is

q_i=k+1−i−d.                                           (16)

Proof by induction: if v lies in child j of size k_j, let L be the total size of preceding children and R that of following children. Its local postorder position is i'=i−L, local depth d'=d−1, and local value k_j+1−i'−d'. Its global value is R plus that quantity. Since k=1+L+k_j+R, this equals k+1−i−d.

Leaves are precisely the left-to-right minima of q, because each subtree receives lower values than its preceding siblings and each internal vertex follows its children with a larger value. By Bóna's preservation property, the associated labeled-tree permutation p has those same minima in the same positions and with the same values. If j<=i is the position of the preceding minimum, p_i>=p_j; therefore

i+p_i >= j+p_j >= k+1−height(T).                       (17)

For a forest of total size n, combine component permutations by SKEW sum. A component of size k following a total of a earlier entries is shifted horizontally by a and vertically by n−a−k. Equation (17) therefore gives, for every point of the full permutation p,

i+p_i >= n+1−H(F).                                    (18)

All-singleton forests yield the decreasing permutation, consistent with (18). This bound is ONE-SIDED: an isolated point at (n,n), for example, is entirely compatible with it.

For the square-spread permuton mu_p used in the frozen contract, (18) implies

x+y >= 1−(H(F)+1)/n  almost surely under mu_p.           (19)

If (X,Y) has law mu_p, its uniform marginals give E(X+Y−1)=0. Consequently

E|X+Y−1|=2 E(1−X−Y)_+ <=2(H(F)+1)/n.                   (20)

Couple mu_p with the anti-diagonal permuton through (X,Y) and (X,1−X). Their Euclidean distance is |X+Y−1|, and therefore

d_BL(mu_p,Law(U,1−U)) <=2(H(F)+1)/n.                    (21)

Combining (15) and (21), the uniform 1342-avoiding permutation converges weakly in probability to the anti-diagonal permuton. For each fixed positive d_BL deviation, its probability is exponentially small in n after a polynomial prefactor, which can be absorbed by weakening the exponential rate.

Reverse positions, an exact bijection between Av_n(1342) and Av_n(2431), to obtain the diagonal limit for 2431=132 skew-sum 1. Inversion preserves the anti-diagonal and maps 1342 to 1423; then reversing positions maps 1423 to 3241=213 skew-sum 1, again giving the diagonal limit. Thus this argument supplies the two target cases alpha=132 and alpha=213.

## 6. Scope and historical boundary

The proof does not handle alpha=312, whose pattern 4231 reverses to 1324, and it does not establish the universal alpha statement. A claimed proof for that statement must go beyond these cases.

Hohmeier–Slivken arXiv:2502.19541v3 (24 February 2026), Section 6, calls the 1342 anti-diagonal limit conjectural. The July 2023 conference abstract had announced that limit; both historical statements are retained, and no reason for their difference is asserted here. The height estimate (13)–(15) above concerns the exact labeled-tree law; it does not substitute a uniform-unlabeled-tree height theorem.

A separate recent primary source, Henning Arnór Skeggi Úlfarsson, arXiv:2609.15642v2 (1 October 2026; first submitted 14 September 2026), gives polynomial-time exact counting and sampling for I_d direct-sum 231. It does not provide a permuton limit in the inspected statements and is not used in this proof.
