# A countermodel to coarse completion-weighted tree assumptions

Date: 14 October 2026. This is a stress test of a proposed proof bridge, not a counterexample to the diagonal-permuton conjecture. The objects here are abstract tree vertices, not permutations. No claim is made that this tree is the minimum-insertion tree of any avoidance class, or that it satisfies every avoidance-specific completion estimate.

## Statement and scope

There is a rooted tree with positive integer labels L satisfying all of the following:

1. Every vertex has exactly L children.
2. Every child has label at most L+1.
3. When the L child labels are sorted as b_1<=...<=b_L, they satisfy b_j>=j+1.
4. The level counts a_n have finite exponential growth, lim a_n^(1/n)=9/2, and are supermultiplicative: a_(p+q)>=a_p a_q.

Nevertheless, if V_n is a uniform level-n vertex and L_j is the label of its ancestor at level j, then for every fixed 0<epsilon<1/2,

    liminf (1/n) sum_(j=0)^(n-1) P(L_j>=epsilon n) >= 1/2-epsilon > 0.

Thus these four coarse hypotheses do not imply the completion-weighted tail condition in the accepted bottleneck appendix. This does not invalidate that appendix or its sufficient condition. Additional avoidance-specific structure could still establish the required condition.

## 1. Construction

Vertices have type A or B as well as label L. The root has type A and label 1. All children are distinct vertices, including children of the same type and label.

- A B-vertex of label L has one B-child of each label 2,3,...,L+1.
- An A-vertex of label L=1 or L=2 has one A-child of label L+1, and one B-child of each label 2,...,L (an empty range when L=1).
- An A-vertex of label L>=3 has three A-children of label L+1, and one B-child of each label 2,...,L-2 (an empty range when L=3).

Every vertex has L children and all labels are at most L+1. In the last case the first L-3 sorted labels are 2,...,L-2; the final three labels are all L+1, which meet b_j>=j+1. The first two cases meet the same condition directly. Hence properties 1-3 hold at every vertex.

## 2. Exact counting series

Let C(z) be the Catalan series defined by C=1+z C^2, and put

    w(z)=z C(z)=(1-sqrt(1-4z))/2,
    z=w(1-w).

A B-vertex of label L has depth generating function C(z)^L, by the accepted Catalan succession recurrence.

Let R(v) be the last level occupied by an A-vertex on the path from the root to v. If v itself has type A at level n, define R(v)=n. Once a path enters type B, it never returns to type A. Define

    G(z,u)=sum_v z^(level(v)) u^(R(v)).

The A-only part has one vertex at levels 0 and 1, and 3^(n-2) vertices at level n>=2. Its contribution is

    1+u z+u^2 z^2/(1-3u z).

There is one early B-exit, from the A-vertex at level 1 to a B-vertex of label 2. Its contribution is u z^2 C^2.

All later exits occur from A-level r>=3. At level r there are 3^(r-2) A-vertices, each with B-child labels 2,...,r-1. Setting h=r-3 and summing their continuations yields

    sum_(h>=0) 3^(h+1) u^(h+3) z^(h+4) sum_(j=2)^(h+2) C^j
      = 3u^3 z^4 C^2 / ((1-3u z)(1-3u z C)).

Consequently

    G(z,u)=1+u z+u^2 z^2/(1-3u z)+u z^2 C^2
           +3u^3 z^4 C^2/((1-3u z)(1-3u z C)).                 (1)

At u=1 this simplifies, using z=w(1-w), to

    A(z):=sum_(n>=0) a_n z^n = 1+w+z^2/(1-3w).                 (2)

The cancellation in (2) is harmless at the dominant pole: 1-3z is nonzero at z=2/9. The coefficients begin 1,1,2,5,17.

## 3. Finite growth and supermultiplicativity

The series w is analytic in |z|<1/4. The denominator 1-3w vanishes at exactly

    rho=2/9

inside that disk. Its derivative there is -9, since w'(rho)=3. Equation (2) therefore has a unique simple dominant pole, with principal part

    (2/81)/(1-z/rho).

For any fixed radius between rho and 1/4, after subtracting that principal part the remainder is analytic on a slightly larger disk than rho. Hence

    a_n ~ (2/81)(9/2)^n,

which proves finite exponential growth 9/2.

Supermultiplicativity is a separate assertion; it does not follow just from this asymptotic formula. Set I(z)=1-1/A(z). Algebra in the variable w gives

    I(z)=w+w^4(3-w)/D(w),
    D(w)=1-2w-2w^2-2w^3+w^4.                                  (3)

The coefficients d_n of 1/D(w) start 1,2,6,18 and satisfy, for n>=4,

    d_n=2d_(n-1)+2d_(n-2)+2d_(n-3)-d_(n-4).

Induction shows they are positive and increasing: once preceding terms are increasing, 2d_(n-3)-d_(n-4)>0 and the remaining summands give d_n>d_(n-1). Thus the coefficients 3d_n-d_(n-1) of (3-w)/D(w), with d_(-1)=0, are positive. As w(z) has nonnegative integer coefficients and zero constant term, (3) shows that I(z) has nonnegative integer coefficients and zero constant term.

Therefore A(z)=1/(1-I(z)) counts finite words of positive-size atoms, with exactly [z^r]I(z) possible atoms of size r. Concatenating a size-p word and a size-q word gives a size-(p+q) word injectively: because atom sizes are positive, the split at cumulative size p is unique. This proves a_(p+q)>=a_p a_q for all p,q, establishing property 4. This auxiliary word interpretation asserts only a property of the level-count sequence; it does not identify the tree with a permutation class.

## 4. A macroscopic A-spine under the exact uniform leaf law

For u in a sufficiently small neighborhood of 1, the first singularity of (1) is the simple pole defined by

    3u z C(z)=1.

Solving with w=z C(z) gives

    rho(u)=(3u-1)/(9u^2).

The other denominator 1-3u z and the Catalan branch point stay a positive distance farther away. Choose a circle of radius strictly between rho(1)=2/9 and 1/4, and then a sufficiently small complex neighborhood of u=1. Within that circle the pole rho(u) is unique and simple; its residue coefficient K(u) is analytic and nonzero, with K(1)=2/81. Subtracting K(u)/(1-z/rho(u)) leaves a function analytic inside that fixed circle, uniformly on a smaller u-neighborhood. Cauchy's coefficient estimate and differentiation in u therefore give

    [z^n]G(z,u)=K(u)rho(u)^(-n)+O(R_0^(-n)),
    E[R(V_n)]=-n rho'(1)/rho(1)+O(1)=n/2+O(1).                 (4)

The expectation is exactly uniform on all level-n vertices because its numerator is [z^n] partial_u G(z,1) and its denominator is a_n. No law on selected spines or exits is substituted.

Along every A-spine, the label at level j is exactly j+1. Thus the number of levels j in {0,...,n-1} with L_j>=epsilon n is at least R(V_n)-epsilon n-1, whether the terminal vertex is A or B. Taking expectations, dividing by n and applying (4) proves the displayed lower bound 1/2-epsilon.

## 5. What the countermodel does and does not rule out

It rules out a deduction of completion-weighted macroscopic label concentration from properties 1-4 alone. In particular, terminal-level frontier concentration and finite growth do not automatically control the uniform-leaf ancestor law.

It does not provide a permutation, a forbidden pattern, an avoidance-class counterexample, or a competing permuton limit. The sharper avoidance-specific upper bound actually fails in this abstract tree: D_3(A3)=3 D_2(A4)=3(3 times 5+2)=51, while binom(3+3-1,3)a_3=10 times 5=50. Thus this example cannot refute an argument that genuinely uses that upper bound. Any argument using it or finer information about the standardized alpha-containing prefix must be judged separately.
