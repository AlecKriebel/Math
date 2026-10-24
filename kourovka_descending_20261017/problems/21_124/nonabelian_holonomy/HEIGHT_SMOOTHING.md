# Height convolution and a rational-function positivity criterion

UTC: 2026-10-24T22:52:00Z. **Proposed supporting mechanism, not independently audited.** This is a general construction criterion for finite projected-multiset couplings. It does not prove that CAT(0) Gram compatibility implies such couplings. Full21.124 discovery estimate remains **4%**.

## An exact polynomial encoding

Fix any finite collection of integer pairs (pi,qi). A finite integer multiset of triples (a,b,t) with nonnegative multiplicities is encoded by a Laurent polynomial

    P(X,Y,Z)=sum m_(a,b,t) X^a Y^b Z^t,  m_(a,b,t)>=0.

Its paired projected multisets agree precisely when

    P(Z^pi,1,Z)=P(1,Z^qi,Z)                         (1)

as Laurent polynomials in Z, for every i. A nonzero horizontal component is present if some term with a nonzero has positive multiplicity. Repeated triples are incorporated in their integer coefficients.

Multiplication by any Laurent polynomial H(Z) preserves (1). If H has nonnegative coefficients, it is simply common convolution of the height coordinate by a finite measure. Crucially, a signed H can also be useful when its final product has nonnegative coefficients.

## Positivity-by-smoothing lemma

**Lemma.** Let Q(X,Y,Z)=sum_(a,b) q_(a,b)(Z) X^aY^b be a Laurent polynomial with rational coefficients, having finitely many horizontal slices. Suppose every nonzero slice satisfies

    q_(a,b)(z)>0 for every real z>0.                 (2)

Then there is an integer N>=0 for which every coefficient of (1+Z)^N Q is nonnegative. A common shift Z^K and multiplication by a positive integer make the result a polynomial in Z with nonnegative integer Laurent-polynomial coefficients in X,Y. Horizontal support is preserved; no horizontal shift is used.

**Proof.** Treat one nonzero Laurent slice q. After factoring its lowest power of Z it is a polynomial f(z)=sum_(j=0)^d c_j z^j with c0 and cd nonzero. Positivity on z>0 implies c0>0 and cd>0. Its degree-d homogenization

    F(x,y)=sum c_j x^j y^(d-j)

is strictly positive on the compact simplex x,y>=0, x+y=1. At the endpoints this follows from c0,cd>0; in its interior it follows from f>0. Let its minimum be epsilon>0.

Set M=N+d. The coefficient of x^k y^(M-k) in (x+y)^N F, divided by binomial(M,k), is

    sum_j c_j (k)_j (M-k)_(d-j) / (M)_d,            (3)

where (r)_j is the falling factorial. The convention (r)_j=0 for integers 0<=r<j automatically handles all boundary coefficients. For fixed d, (3) converges uniformly over 0<=k<=M to F(k/M,1-k/M) as M→infinity: divide numerator and denominator by M^d, and use that every finite product of factors k/M-l/M or 1-k/M-l/M differs uniformly by O_d(1/M) from its repeated-factor limit. The denominator tends to one. Thus every normalized coefficient is positive for all sufficiently large N. This proves the assertion for one slice. There are finitely many slices, so choose the maximum required N. Increasing N further preserves nonnegative coefficients. Restoring the factored powers, applying a common height shift, and clearing rational denominators proves the lemma. QED.

This is the elementary two-variable homogeneous positivity argument often called Pólya positivity, proved here rather than invoked with unstated endpoint hypotheses.

## Equivalent rational-function criterion

A finite positive multiset satisfying (1) with a nonzero a exists **if and only if** there is a finite horizontal support S⊂Z² containing an a≠0 and rational functions w_(a,b)(Z)∈Q(Z), one for each (a,b)∈S, such that:

1. each w_(a,b) is defined and strictly positive on all real Z>0;
2. for every i,

       sum_(a,b) w_(a,b)(Z) [ Z^(pi a)-Z^(qi b) ] = 0            (4)

   as an identity of rational functions.

For necessity, collect the height slices of a positive multiset. Each nonzero slice is a Laurent polynomial with positive coefficients and is strictly positive for every z>0, giving (4).

For sufficiency, write each rational function in reduced form. Its denominator has no positive real zero because the function has no pole there. Multiply all functions by the product D of all denominator squares, and by a common power of Z if needed. D is positive on z>0, and each resulting q_(a,b)=D w_(a,b) is a rational polynomial strictly positive there. Equation(4) survives multiplication by D. Apply the smoothing lemma and clear rational denominators. The resulting Laurent polynomial P with nonnegative integer coefficients has the desired equal projections and preserves every nonzero horizontal slice. This is a finite multiset construction.

For injectivity of two independent vertices, require both an a-nonzero slice and a b-nonzero slice; the construction preserves both. The criterion remains valid with negative a,b or negative initial height exponents. Strict positivity of every chosen nonzero slice is essential. Mere nonnegativity with a positive real zero is insufficient for the smoothing conclusion, because a nonzero polynomial with nonnegative coefficients cannot vanish at a positive argument.

## What this contributes to the broader positive question

This replaces an unbounded height-support search by a possible search for positive rational-function weights on a fixed finite horizontal support. It supplies a genuine exact construction mechanism: a proved positive rational kernel over Q(Z), followed by coefficient smoothing, produces a finite witness. It does **not** prove that such a rational kernel exists whenever a compatible positive-definite Gram matrix exists.

For the Pell pairs, the root's exact 517-type positive finite multiset already supplies such a kernel, so the negative candidate is defeated independently of this mechanism. Re-encoding that known certificate is not a new general theorem about other CAT(0) groups.

The precise new barrier is to construct finitely many (a,b) and a rational-function vector strictly positive on the whole interval (0,infinity) in the kernel of the columns

    (Z^(pi a)-Z^(qi b))_i.

Pointwise numerical feasibility at selected Z, formal Taylor matching near Z=1, or Gaussian covariance compatibility is insufficient. Such local or sampled evidence does not provide one rational kernel that stays positive for every Z>0. This route is therefore **blocked at that positivity-construction assertion** until a new mechanism or an explicit rational-function solution is supplied.

## Small exact falsifiable check

The family f_m(Z)=Z²-(2-1/m)Z+1, for integers m>=1, is strictly positive on Z>0 since f_m(Z)=(Z-1)²+Z/m. Its negative middle coefficient illustrates why the lemma is stronger than checking initially positive coefficients. Direct binomial arithmetic shows that (1+Z)^(4m-3) f_m has all coefficients nonnegative, while no smaller exponent does; for m=1 this is (1+Z)(Z²-Z+1)=1+Z³. Indeed, with M=N+2, the normalized coefficient at k is

    [M(M-1)-(4-1/m)k(M-k)] / [M(M-1)].

Its minimum is attained at k=floor(M/2). For even M its numerator is M(M-4m)/(4m); for odd M it is (M-1)(M-(4m-1))/(4m). Therefore the first nonnegative case is M=4m-1, namely N=4m-3. The standard-library checker verifies these claims for 1<=m<=30 by exact rational convolution. This bounded check tests the formula, while the preceding proof supplies the general smoothing lemma.
