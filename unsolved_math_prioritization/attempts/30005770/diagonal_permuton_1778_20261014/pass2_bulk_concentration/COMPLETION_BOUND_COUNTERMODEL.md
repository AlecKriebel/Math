# An abstract tree obstruction surviving the full completion bound

**Status and scope.** This is an obstruction to a specified collection of numerical generating-tree arguments, not a counterexample to the permutation conjecture. The tree below is not the minimum-insertion tree of Av(alpha skew-sum 1) for any fixed alpha. It shows that the all-size completion upper bound proved in pass 1 does not, even together with the other numerical hypotheses listed below, force the proposed macroscopic descendant-weighted frontier estimate. This is a substantive negative result about that proof route. No novelty claim is made.

## 1. Exact claim

There is a rooted tree with a positive integer label L at each vertex, level counts a_n, and depth-t descendant counts D_t(v), such that all the following hold.

1. The root label is 1. Every label-L vertex has exactly L children, with labels at most L+1. Sorted child labels b_1 <= ... <= b_L satisfy b_j >= j+1. In particular the Catalan comparison tree embeds below every vertex.
2. With a_0=1, the level counts are supermultiplicative: a_(p+q) >= a_p a_q. They have a finite exponential growth rate lambda=9/2; also a_n <= n!.
3. For every vertex v, every t >= 0, and L=L(v),

B(L,t) <= D_t(v) <= binomial(L+t-1,t) a_t,

where B(L,t)=L/(L+2t) binomial(L+2t,t). Both inequalities hold for every size, not merely on an enumerated range.
4. If V_n is uniform among level-n vertices and V_(n,j) is its ancestor at level j, then for every epsilon in (0,1/2),

liminf_(n->infinity) (1/n) sum_(j=0)^(n-1)
    P( L(V_(n,j)) >= epsilon n ) >= 1/2-epsilon > 0.               (1)

The probabilities in (1) have exactly the descendant-weighted form

P(V_(n,j)=v) = D_(n-j)(v)/a_n.

Thus the sufficient weighted-frontier condition in the pass-1 bulk bottleneck fails despite hypotheses 1--3. No claim is made that these exhaust all constraints of actual permutation avoidance. In particular, the exact pattern-dependent state geometry remains available to a genuine proof.

## 2. Tree construction

There are three preliminary types P_0, P_1, P_2, of respective labels 1,2,3, and then types A_L for L>=4 and B_L for L>=2. Repeatedly named children are distinct vertices with identical future rules.

- The root P_0 has one P_1 child.
- Each P_1 vertex has two P_2 children.
- Each P_2 vertex has three A_4 children.
- A_L has three A_(L+1) children and one B_j child for every j=2,...,L-2.
- B_L has one B_j child for every j=2,...,L+1.

There are six A_4 vertices at level 3. An A-path may stay in A for many steps, then enter B permanently. An A_L has (L-3)+3=L children. Its sorted labels are 2,3,...,L-2,L+1,L+1,L+1, which dominate 2,3,...,L+1. Preliminary and B vertices have the same required domination, and all child labels are at most their parent's label plus one. Starting from label 1, the label at depth n is at most n+1, so a_(n+1) <= (n+1)a_n and a_n <= n!.

This is a finite initial modification of the simpler A_1 model considered in the independent audit. That original model failed the actual avoidance upper completion bound: D_3(A_3)=51 exceeded binomial(5,3)a_3=50. The present construction replaces its initial levels. Earlier accepted files describing the original model are unchanged.

## 3. Exact generating functions

Let C=C(z) be the Catalan generating series, C=1+zC^2, and write w=zC. For B_L, the depth generating series is C^L, as follows directly from the Catalan child rule.

For an A_L starting vertex, let F_L(z) be the depth generating series, including the starting vertex at depth zero. A path makes r>=0 consecutive A-to-A steps, with 3^r choices, then either stops in A or enters a B subtree. At its endpoint A_(L+r), the stop/exit series is

1 + z sum_(j=2)^(L+r-2) C^j = C^(L+r-3).

The equality is the finite geometric identity C^h=1+z sum_(j=2)^(h+1) C^j. Therefore

F_L(z) = sum_(r>=0) (3z)^r C^(L+r-3)
       = C^(L-3)/(1-3zC),  L>=4.                                (2)

Set

F(z)=F_4(z)=C/(1-3zC)=sum_(t>=0) d_t z^t.

The full tree's level series is

A(z)=sum_(n>=0) a_n z^n = 1+z+2z^2+6z^3 F(z).                    (3)

In particular a_0=1, a_1=1, a_2=2 and a_n=6d_(n-3) for n>=3. The first values are

1, 1, 2, 6, 24, 102, 444, 1956, 8676, 38646, 172620.

At rho=2/9, w(rho)=1/3 and C(rho)=3/2. The denominator of F has a simple zero there, whereas C is analytic for |z|<1/4. The equation 3zC(z)=1 has no other solution in that disk: the identity z=w(1-w) forces z=2/9. Moreover

F(z) = (3/4)/(1-z/rho) + a function analytic in |z|<1/4.

Consequently, for any fixed R with rho<R<1/4,

d_t=(3/4)(9/2)^t+O(R^(-t)),
a_n=(4/81)(9/2)^n+O(R^(-n)).                                   (4)

This proves the finite growth claim and will also control the marked law below.

## 4. Supermultiplicativity, with an all-size proof

We first show that d_t is log-convex. Let J be the bounded self-adjoint operator on the nonnegative integer half-line with diagonal entries 4,2,2,2,... and off-diagonal entries 1. For finitely supported real vectors x,

<x,Jx> = sum_(i>=0) (x_i+x_(i+1))^2 + 3x_0^2 >= 0.

Thus J is positive. Its tail return generating function T(z), obtained by deleting the initial row and column, satisfies

T=1/(1-2z-z^2 T)=C^2.

This can be read as a first-return decomposition of weighted walks or as the usual resolvent Schur complement. The unique formal solution has constant term 1. At the initial vertex the return series is

sum_(t>=0) <e_0,J^t e_0> z^t = 1/(1-4z-z^2 C^2).

Since 1/C=1-zC and zC=z+z^2 C^2,

C/(1-3zC)=1/(1/C-3z)=1/(1-4z-z^2 C^2)=F(z).

Hence d_t=<e_0,J^t e_0>. The spectral theorem for a bounded positive operator gives d_t=integral x^t dnu(x) for a positive finite measure supported on a bounded subset of [0,infinity). Cauchy--Schwarz therefore gives

d_t^2 <= d_(t-1)d_(t+1), t>=1.

All coefficients are positive, so the successive d-ratios are nondecreasing. The successive a-ratios start with 1,2,3,4 and thereafter equal successive d-ratios starting after d_1/d_0=4. Thus a_n is also log-convex. With a_0=1,

a_(p+q)/a_p = product_(i=1)^q [a_(p+i)/a_(p+i-1)]
           >= product_(i=1)^q [a_i/a_(i-1)] = a_q.

This proves supermultiplicativity for every p,q. It is not inferred from finite enumeration.

## 5. All-size completion upper bound

The Catalan lower bound B(L,t) follows from the sorted child-label domination by the same recursive embedding as in pass 1. In particular a_t is at least the t-th Catalan number c_t.

### 5.1 B vertices

Expand C^L by weak compositions t=t_1+...+t_L. Each coefficient product satisfies

product_i c_(t_i) <= product_i a_(t_i) <= a_t

by Catalan domination and supermultiplicativity. There are binomial(L+t-1,t) weak compositions. Thus

D_t(B_L) <= binomial(L+t-1,t) a_t.                               (5)

### 5.2 The starting A_4 vertex

At relative depth s below A_4, every vertex has label at most 4+s. Therefore, for t>=3, the final three generations give

d_t <= (t+1)(t+2)(t+3)d_(t-3)
    = binomial(t+3,t) a_t.                                      (6)

Here the identity uses a_t=6d_(t-3). At t=0,1,2 the values d_t=1,4,17 are bounded respectively by 1,4,20, so (6) holds at every t>=0.

### 5.3 All A_L vertices

For L=4 this is (6). For L>4, put r=L-4 and use F_L=C^r F. Equations (5)--(6), coefficient convolution and supermultiplicativity give

D_t(A_L)
 <= sum_(u=0)^t binomial(r+u-1,u)a_u
                    binomial(t-u+3,t-u)a_(t-u)
 <= a_t sum_(u=0)^t binomial(r+u-1,u)binomial(t-u+3,t-u)
  = a_t binomial(L+t-1,t).                                      (7)

The last identity is the coefficient identity for (1-z)^(-r)(1-z)^(-4). Thus the upper bound holds for all labels and all depths in A.

### 5.4 Preliminary vertices

For P_1 (label 2), D_0=1, D_1=2 and D_t=6d_(t-2) for t>=2. For t>=3 the one-generation degree bound gives

d_(t-2) <= (t+1)d_(t-3),

so D_t(P_1) <= (t+1)a_t = binomial(t+1,t)a_t. At t=2 both sides equal 6, and t=0,1 are immediate.

For P_2 (label 3), D_0=1 and D_t=3d_(t-1) for t>=1. For t>=3 the last two generations give

d_(t-1) <= (t+1)(t+2)d_(t-3),

so D_t(P_2) <= binomial(t+2,t)a_t. At t=1,2 both sides equal 3,12 respectively, and t=0 is immediate. At the root the upper bound is equality D_t=a_t. This completes the all-size proof of hypothesis 3.

## 6. Uniform leaves have a macroscopic A-spine

For a leaf at relative depth t below A_4, let S be the number of initial A-to-A edges before first entering B, or all those edges if the leaf remains in A. Marking each such edge by u modifies (2) to

F(z,u)=C(z)/(1-3u z C(z)).                                      (8)

For all u in a sufficiently small complex neighborhood of 1, its unique pole inside a fixed circle |z|=R<1/4 is

rho(u)=(3u-1)/(9u^2).

The pole coefficient is analytic and nonzero there:

K(u)=3u(3u-2)/(3u-1)^2.

After subtracting K(u)/(1-z/rho(u)), the remainder is jointly analytic on a slightly larger closed z-disk than the pole radius, uniformly for u near 1. Cauchy's coefficient formula therefore gives the uniform expansion

[z^t]F(z,u)=K(u)rho(u)^(-t)+O(R^(-t)).                            (9)

All level-n leaves, for n>=3, choose one of the six A_4 vertices and a uniform relative-depth-(n-3) descendant. Thus their probability generating function for S is the ratio of the coefficients in (9), with t=n-3. Differentiating the corresponding logarithmic moment generating function at u=e^s near s=0 is justified by the uniform analytic error. Direct differentiation yields

E S = t/2+O(1),     Var S = 3t/4+O(1).

For example, -[u d/du log rho(u)]_(u=1)=1/2, and the next cumulant coefficient is 3/4. Chebyshev gives

S/n -> 1/2 in probability.                                    (10)

Whenever an ancestor at level j>=3 is still of type A, its label is exactly j+1. Fix epsilon in (0,1/2) and eta>0 with epsilon<1/2-eta. With probability tending to one, S >= (1/2-eta)n. On this event all ancestor levels from ceil(epsilon n) through floor((1/2-eta)n) are in A, up to harmless bounded endpoint shifts, and all their labels are at least epsilon n. Hence the average in (1) has liminf at least 1/2-eta-epsilon. Letting eta decrease to zero proves (1).

Every probability used here is the exact uniform leaf law, with actual completion weights. The high-label ancestors are not sampled uniformly from their levels.

## 7. Interpretation and explicit non-permutation boundary

This model excludes the proposed implication from exactly these inputs:

- degree equals frontier label;
- child labels at most parent label plus one;
- sorted Catalan domination;
- finite exponential growth and supermultiplicative level counts;
- the all-size lower Catalan and upper binomial completion bounds.

Those numerical inputs are all compatible with macroscopic descendant-weighted labels. The earlier isolated failure 51>50 is therefore not evidence that the binomial completion bound, by itself, repairs the proof route.

The model is not an avoidance-class counterexample. Indeed its counts agree with n! through n=4 but give a_5=102. For a principal class avoiding a single fixed pattern, either the first forbidden length is at most 4 (contradicting the earlier counts), equals 5 (giving 5!-1=119), or exceeds 5 (giving 5!=120). Thus no principal pattern-avoidance class has these counts. Also the literal B_2 labels are not first-alpha-hit labels when |alpha|>=3. The model imposes neither arbitrary pattern-restriction closure nor the full alpha-dependent transition geometry.

The universal diagonal-permuton conjecture remains unresolved by this lane. Any successful completion of the descendant approach must use additional actual permutation structure, not just the numerical bounds listed above. Finite verification of this note is supplementary; sections 2--6 supply the all-size arguments.
