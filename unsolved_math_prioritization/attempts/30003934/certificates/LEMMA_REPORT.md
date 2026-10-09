# Rational certificates and the rank one uniqueness obstruction

## Scope and conclusion

This report concerns finite two-player games with explicitly encoded rational payoff matrices A and B of size m by n. An equilibrium is a pair of mixed strategies, not merely a pair of payoffs. Degenerate games and positive-dimensional equilibrium sets are allowed.

The proved complexity preliminary is:

**NONUNIQUENESS is in NP for every rational bimatrix game. Consequently UNIQUENESS restricted to games with rank(A+B)=1 is in coNP.**

The proof supplies two polynomial-size rational equilibrium witnesses even if the original witnesses are irrational points in positive-dimensional components. Rank exactly one is itself checkable in polynomial time. These statements establish membership only. They neither prove coNP-hardness nor give a polynomial-time algorithm for global rank-one uniqueness.

An explicit rank-one 2 by 2 example below shows why testing one equilibrium's support cell or parameter fiber is insufficient. At fixed parameter, the full equilibrium fiber is one LP-described polytope; across parameters, the essential multiplicative condition returns.

## 1 Compact support polytopes

Write Delta_m and Delta_n for the probability simplices. For each pair of nonempty index sets I contained in {1,...,m} and J contained in {1,...,n}, choose i0 in I and j0 in J. Define

X(I,J) = {x in Delta_m:
  x_i=0 for i outside I;
  x^T(B_.j-B_.j0) <= 0 for every j;
  x^T(B_.j-B_.j0) = 0 for j in J}.

Y(I,J) = {y in Delta_n:
  y_j=0 for j outside J;
  (A_i.-A_i0.)y <= 0 for every i;
  (A_i.-A_i0.)y = 0 for i in I}.

The dot denotes the indicated whole row or column. Both sets are compact rational polytopes, possibly empty. Their definitions use weak inequalities throughout; no positive lower bound on a supported probability is needed.

**Lemma 1.** Every pair in X(I,J) times Y(I,J) is a Nash equilibrium, and the full equilibrium set E is the union of these products over nonempty I,J.

**Proof.** In a product member, x uses only I, while every row in I is a maximizing response to y. Similarly y uses only J, and every column in J maximizes against x. This is exactly the equilibrium condition. Conversely, for an equilibrium take I and J to be its actual supports. All their actions are maximizing responses, so the equilibrium lies in the corresponding product. Taking closed cells with possibly smaller supports adds no nonequilibria. QED.

This is an exact finite union, not a claim that the union is convex or that the number of cells is polynomial. There are at most (2^m-1)(2^n-1) indicated cells.

## 2 Explicit rational bit bounds

Let L be the total binary input length, including the signed integer numerators and positive denominators of all payoff entries and the dimensions. Let D be the product of all denominators appearing in A and B. Multiplying both matrices by D produces integer matrices whose entries have absolute value at most 2^L. Consequently every comparison coefficient in the preceding polytopes has absolute value at most

H = 2^(L+1).

The remaining coefficients and all right-hand sides are 0, 1, or -1. Forming D and the integer matrices is polynomial-time exact arithmetic: D has at most L+1 bits. Cancellation or least common denominators are optional.

At a vertex of one of the polytopes in ambient dimension d, the active constraint normals span R^d, even when the polytope is lower-dimensional. Otherwise a nonzero direction annihilating every active constraint could be followed a sufficiently small distance in both signs while keeping all inactive inequalities feasible, contradicting extremality. Therefore choose d linearly independent active equations Mz=c.

M is an integer nonsingular d by d matrix, |M_ij|<=H, and |c_i|<=1. Cramer's rule and Hadamard's determinant bound give, for every coordinate of z,

z_k = det(M_k)/det(M),
|det(M)|, |det(M_k)| <= d^(d/2) H^d.

The same bound applies to M_k since its substituted column has entries bounded by H. After reduction, each coordinate's numerator and denominator can therefore be encoded using at most

h(d,L) = ceil(d(L+1) + (d/2) log_2(d)) + 2

bits each, allowing a sign. Use d=m for X(I,J) and d=n for Y(I,J). A vertex pair has total length O(m h(m,L)+n h(n,L)), hence polynomial in the explicitly encoded input. This bound is deliberately coarse and requires no nondegeneracy promise.

**Lemma 2.** If E contains more than one pair, it contains two distinct rational equilibrium pairs satisfying these vertex bounds.

**Proof.** Every nonempty cell X(I,J) times Y(I,J) is a compact polytope and is the convex hull of its vertices; its vertices are precisely products of vertices of the two factors. Let V be the union of the vertex sets of all nonempty cells. If V contained just one point p, every nonempty cell would equal {p}, so E would also equal {p}. Thus nonuniqueness implies that V contains two distinct points. The preceding bound applies to both. QED.

This proof does not try to preserve the supports or component membership of two initially supplied equilibria. That is unnecessary. If a component has positive dimension, some contributing cell is nonsingleton and already supplies two distinct vertices, possibly on its boundary.

## 3 Verification and the precise complexity statements

A NONUNIQUENESS certificate consists of two rational pairs (x,y) and (x',y'). The verifier checks, using exact rational arithmetic:

1. Every vector is nonnegative and its coordinates sum to one.
2. For each pair, every row payoff (Ay)_i is at most x^T A y, and every column payoff (B^T x)_j is at most x^T B y.
3. The two pairs differ in at least one coordinate.

These are necessary and sufficient equilibrium conditions and are polynomial-time checks on the stated bit bounds. Lemma 2 proves completeness of the certificates, including infinite equilibrium sets. Finite games have at least one equilibrium, so the complement of NONUNIQUENESS is precisely uniqueness, rather than “at most one” with a possible empty case.

For rank-restricted input, form C=A+B. If C=0 its rank is zero, not one. Otherwise select a nonzero pivot C_i0,j0. Then

rank(C)=1 iff C_ij C_i0,j0 = C_i,j0 C_i0,j for every i,j.

This is a polynomial number of exact rational operations. In the affirmative case the factorization

a_i=C_i,j0,   b_j=C_i0,j/C_i0,j0

has polynomial encoding length and gives C=ab^T. Gaussian elimination is an alternative.

Thus the ordinary language {rational games: rank(A+B)=1 and E is nonsingleton} belongs to NP. The language {rational games: rank(A+B)=1 and E is a singleton} belongs to coNP: its complement is the union of the polynomial-time rank-invalid case and the two-equilibrium certificate case. The corresponding promise problem has the same membership statement. The statements remain true with rank at most one.

If a rational equilibrium e0 is additionally supplied, existence of an equilibrium other than e0 is also in NP. Whenever E is nonsingleton, at least one of the polynomial-size vertex equilibria differs from e0. The input length then includes the encoding of e0.

For clarity, degeneracy recognition is not required anywhere above. One can also prove the weaker auxiliary fact that DEGENERACY has polynomial rational witnesses: choose a mixed strategy supported within a set I of size k and impose that at least k+1 specified opponent actions tie for best response. These conditions define a compact rational polytope. A vertex witness may have smaller support, which only strengthens “more best responses than support size.” Apply the same argument to either player. No hardness claim about recognizing degeneracy, with or without a rank restriction, is made here.

## 4 Rank zero and equilibrium pair versus payoff uniqueness

When A+B=0, let v be the value of the zero-sum game. Its equilibrium set is exactly the Cartesian product

X* = {x in Delta_m: A^T x >= v 1},
Y* = {y in Delta_n: A y <= v 1}.

Compute v by LP. Then maximize and minimize each coordinate over X* and Y*. The pair is unique exactly when every range has width zero. This needs polynomially many polynomial-size LPs. If an equilibrium is supplied, its payoff gives v directly. Positive-dimensional zero-sum equilibrium sets pose no difficulty.

Rank exactly one also contains easy constant-sum and strategically zero-sum subclasses. In the factorization A+B=ab^T, if a is constant then a^T x is constant on the entire simplex; if b is constant then b^T y is constant. The equilibrium gap in the next section is then linear globally. Therefore zero-sum tractability does not, by itself, extend to unrestricted rank one, and rank one must not be confused with “genuinely non-zero-sum strategic behavior” in every instance.

Uniqueness of an equilibrium pair is different from uniqueness of equilibrium payoffs. For example, let A be the all-zero 2 by 2 matrix and B the all-one matrix. Then rank(A+B)=1, every strategy pair is an equilibrium, and all have payoff pair (0,1). Unique strategies imply unique payoffs, but the converse fails.

For completeness, distinct equilibrium payoffs also have polynomial rational witnesses. On each support cell, u=(A_i0.)y and v=x^T(B_.j0), so the payoff map is affine on that cell. If all cell vertices had the same payoff pair, every cell and their union would have that pair. The proof of Lemma 2 therefore adapts to payoff nonuniqueness, but that is a different decision problem.

## 5 What can be tested given one rank one equilibrium

Assume A+B=ab^T. Introduce u,v and the best-response inequalities

x in Delta_m, y in Delta_n, Ay<=u 1, B^T x<=v 1.

For every feasible point,

g(x,y,u,v) = u+v-(a^T x)(b^T y) >= 0.

Indeed g is the sum of the nonnegative row and column best-response gaps. Equality holds exactly at equilibria and then forces u=x^T A y and v=x^T B y.

For a fixed rational lambda, add

a^T x=lambda,   u+v=lambda b^T y.

Everything is now linear. The resulting feasible set is a compact rational polytope (or empty), and its projection to (x,y) is exactly all original-game equilibria with a^T x=lambda. Compactness follows because equality forces u and v to equal the actual, bounded equilibrium payoffs.

**Lemma 3.** Given an equilibrium e0=(x0,y0), uniqueness among all equilibria with a^T x=a^T x0 can be decided by at most 2(m+n) coordinate LP optimizations over this fiber. Any nonzero coordinate range produces another equilibrium. No support restriction or nondegeneracy is needed.

Testing the support cell X(supp x0,supp y0) times Y(supp x0,supp y0) is also polynomial by coordinate LPs. That is an even narrower test and does not certify global uniqueness.

The obstruction to a global LP is exact: with lambda free, the equality u+v=lambda b^T y is bilinear, even after imposing the linear equation lambda=a^T x. The set of equilibria is generally nonconvex. Replacing that equality by an unsupported linear relaxation loses the equilibrium condition. Excluding e0 by maximizing or minimizing coordinates is valid only if the optimization is genuinely over the whole equilibrium set, which is the unresolved part of the approach.

Equivalently, for fixed lambda consider the auxiliary zero-sum matrix M_lambda=A-1 lambda b^T. If X_lambda and Y_lambda are its optimal-strategy polytopes, then the original game's equilibrium fiber is

(X_lambda intersect {x: a^T x=lambda}) times Y_lambda.

This is the rank-one specialization of Adsul et al., Theorem 7. An LP checks whether lambda is between min and max of a^T x over X_lambda. However, as lambda varies the optimal faces change, and monotonicity of the path's parameter does not mean that a^T x-lambda is monotone. The known binary search proves existence of one intersection using a sign bracket; it does not prove absence of further intersections once one is found.

## 6 An exact two by two obstruction

Take

A = [[1,6],[0,9]],
B = [[1,0],[6,9]],
a = (1,3)^T, b = (2,6)^T.

Then A+B=ab^T. Against y=(t,1-t), the row payoff difference between rows 1 and 2 is 4t-3. By symmetry the corresponding column difference against x=(s,1-s) is 4s-3. Consequently the exact equilibrium set is

(e1,e1), (e2,e2), and ((3/4,1/4),(3/4,1/4)).

To see exhaustion, if one player mixes with both actions, the opponent's first probability must equal 3/4, hence that opponent also mixes and forces the same value for the first player. If neither mixes, only the two diagonal pure profiles satisfy both best responses. A profile with exactly one mixing player is impossible by the same indifference equation. The game is nondegenerate: each pure opponent strategy has a unique best response, and any two-action mixed strategy has at most two best responses.

The three parameter values lambda=a^T x are 1, 3, and 3/2, respectively. Every fiber containing an equilibrium is a singleton, and every equilibrium's exact-support cell is a singleton. Hence neither LP test finds the other equilibria. The midpoint of the two pure equilibria is the uniform pair, where the row payoffs are 7/2 and 9/2; thus E is explicitly nonconvex.

The auxiliary zero-sum game's optimal row strategy has first probability

s(lambda) = 1                       if lambda<=5/4,
            9/4-lambda             if 5/4<=lambda<=9/4,
            0                     if lambda>=9/4.

This follows by maximizing over 0<=s<=1 the minimum of the two column payoffs s-2 lambda and 9-3s-6 lambda. They intersect at s=9/4-lambda; clipping that point to [0,1] gives the unique maximizer, including the boundary cases.

Thus the residual r(lambda)=a^T x(lambda)-lambda is

1-lambda     if lambda<=5/4,
lambda-3/2   if 5/4<=lambda<=9/4,
3-lambda     if lambda>=9/4.

It changes slope from -1 to +1 and back to -1 and has the three zeros 1,3/2,3, all in the feasible original-game parameter interval [1,3]. In particular r(5/4)=-1/4 and r(9/4)=3/4. No monotone-residual uniqueness criterion follows from the monotone parameterization.

This example is the n=2, p=3 instance of Adsul et al., Theorem 21, with both payoff matrices divided by nine. The arithmetic and exhaustion proof above are independent checks. Exponentially many equilibria in larger instances obstruct naive complete enumeration but do not, alone, prove hardness of deciding whether a second equilibrium exists.

## Sources and limits

1. Bharat Adsul, Jugal Garg, Ruta Mehta, Milind Sohoni, and Bernhard von Stengel, *Fast Algorithms for Rank-1 Bimatrix Games*, arXiv:1812.04611v4, revised 22 December 2019; published in Operations Research 69(2), 613-631 (2021). Public URL: https://arxiv.org/abs/1812.04611. Relevant statements: Lemma 3 (gap formulation), Theorem 7 (rank reduction), Theorem 19 (polynomial-time one-equilibrium algorithm), Section 6 and Theorem 20 (degenerate Nash subsets), Theorem 21 (exponential family). The abstract and bibliographic metadata were checked online on 9 October 2026. The detailed sections were inspected in the supplied local extraction.
2. Bernhard von Stengel, *Algorithms for Rank-1 Bimatrix Games*, Oberwolfach Reports 38/2018, p. 2332, in *New Directions in Stochastic Optimisation*. The supplied text explicitly states the coNP-hardness claim as a conjecture. That source establishes the historical question, not a proof or a current exhaustive literature status.

The support-polytope certificate proof, explicit bit bound, fixed-fiber LP test, and the detailed arithmetic in Section 6 are proved in this report. They do not rely on a hardness citation. No reduction, publication action, or queue update is supplied.
