# A tensor-moment counterexample to fixed odd-power SOS convexity

**Author turn 2 of 5. Complete candidate for the general yes/no question; independent review pending.** This proves a counterexample in a finite, very large number of variables. It does not classify the small-dimensional cones or answer the ternary fixed-exponent case.

## 1. Exact target and result

For positive n, positive even m and odd q, put

C_(n,m,q) = {f in R[x1,...,xn]_m : f is nonnegative and f^q is a sum of squares}.

These are the source's Sigma_(n,m)(2k+1), with q=2k+1. The coefficient space is real, the forms are homogeneous, and all exponents here are fixed before taking a convex combination. The source asks whether these sets are closed convex cones. Closedness and nonnegative scalar closure hold; the general convexity assertion has a negative answer if the following candidate is correct.

**Theorem.** Let N=10^62 and n=3N. Partition n variables into N triples (xi,yi,zi), and set

p_i = xi^4 yi² + xi² yi^4 + zi^6 - xi² yi² zi².

Each p_i belongs to C_(n,6,3), but their average N^-1 sum_i p_i does not. Consequently C_(3*10^62,6,3) is not convex.

More generally, for every odd q>=3 there is a finite n(q) for which C_(n(q),6,q) is not convex. Nonconvexity persists on adding unused variables. The classical convex cases, including q=1 and the Hilbert equality cases, are unaffected. No claim that every remaining parameter triple is nonconvex is made.

The seed cube identity is credited to Reznick's report and Blekherman–Kozhasov–Reznick, published 2026, §6 after Theorem 6.3. Tensor products of positive moment matrices, elementary Schur complements and finite-dimensional separation are standard tools. No historical novelty claim is made.

## 2. Tensor amplification lemma

Let p be a real homogeneous polynomial of positive even degree m, and q a positive odd integer. Set d=qm/2. Suppose there is a linear functional L on real polynomials of total degree at most 2d in the variables of p satisfying

L(1)=1,   L(h²)>=0 for deg(h)<=d,   a1=L(p)<0.

Write aj=L(p^j), 0<=j<=q; thus a0=1. For each positive integer s take s disjoint copies of the variables and define the product functional L_s on monomials with degree at most 2d in each block by

L_s(product_i x_i^(alpha_i)) = product_i L(x^(alpha_i)).

This is a finite-dimensional functional for every finite s. If H is a polynomial of *total* degree at most d in all blocks, its monomials have degree at most d in each block. The matrix for L_s(H²) is a principal submatrix of the s-fold Kronecker product of the positive semidefinite moment matrix (L(x^(alpha+beta)))_(|alpha|,|beta|<=d). It is therefore positive semidefinite. Hence L_s is nonnegative on every SOS of total degree at most 2d. An SOS identity of that degree cannot involve higher-degree square summands, since their top homogeneous squares could not cancel. It is unnecessary to form or store this enormous tensor matrix.

Let S_s=sum_(i=1)^s p_i. Expanding by functions from the q labeled factors to the s blocks gives

L_s(S_s^q) = sum_(partitions pi of {1,...,q}) (s)_(|pi|) product_(B in pi) a_(|B|),

where (s)_r=s(s-1)...(s-r+1). This is a polynomial in s of degree q with leading coefficient a1^q<0: the unique q-block partition consists of singletons. Thus it is negative for every sufficiently large integer s. For such s, S_s^q cannot be SOS. This is an exact finite-degree argument, with no limit of measures, independence assumption about actual random variables, or uniform-integrability step.

If p^q is SOS, then every p_i is in the same ambient C_(s*n0,m,q), whereas their finite average is not. A convex set is closed under arbitrary finite convex combinations by induction on their number, so this disproves convexity. If a two-input formulation is desired, take the least j<=s for which S_j is outside that ambient cone. Then S_(j-1) and p_j are inside it and their sum is outside. This last argument proves existence of a violating pair; it does not assert that a particular untested prefix has an SOS power.

**General availability of L.** If p is not SOS, it is also not an SOS of polynomials of degree <=d. Higher-degree summands cannot cancel their highest homogeneous squares to give p of lower degree. The cone of SOS polynomials of degree <=2d is closed: for a convergent sequence v^T Q_j v, Q_j>=0, integration against a Gaussian bounds tr(Q_j G), where G is its positive-definite monomial Gram matrix, and hence bounds Q_j. A convergent subsequence gives a limiting Gram matrix. Finite-dimensional separation gives L(p)<0 and L nonnegative on that cone. Add a sufficiently small positive Gaussian functional to make its moment matrix positive definite while keeping L(p)<0, then divide by L(1)>0. This proves the amplification lemma applies whenever a non-SOS p has an SOS q-th power.

The following explicit construction avoids relying on a nonconstructive separation for the displayed dimension bound.

## 3. The credited seed and its cube

Let p=x^4y²+x²y^4+z^6-x²y²z². Weighted AM–GM proves p>=0. It is not itself SOS; this follows either from the usual half-Newton-polytope obstruction or from the negative positive-functional value constructed below.

Here is the published cube identity specialized to this seed. Let

h1=x^5y^4-x³y^4z²,
h2=x^4y^5-x^4y³z²,
h3=x^4y²z³-x²y²z^5,
h4=x²y^4z³-x²y²z^5,
h5=xy²z^6-x³y^4z²,
h6=x²yz^6-x^4y³z²,
h7=x²y^4z³-x^4y²z³,
h8=x^4y^5-x²yz^6,
h9=x^5y^4-xy²z^6.

Then

p³ = (3/2) sum_(j=1)^9 hj²
 + (z^9-2x²y²z^5)²
 + (xyz^7-2x³y³z³)²
 + (x³y^6-2x³y^4z²)²
 + (x³y^5z-2x³y³z³)²
 + (x^6y³-2x^4y³z²)²
 + (x^5y³z-2x³y³z³)²
 + 2(x³y³z³)².

All summands have degree 18, with positive real weights. The checker expands this equality exactly. In particular p_i³ is SOS in the common n-variable ring. For every odd q>=3, p^q=p³*(p^((q-3)/2))² is also SOS. The amplification lemma proves the general odd-q assertion.

## 4. Explicit rational moment functional through degree 18

For a multi-index alpha in N³ let g_alpha be the standard Gaussian moment:

- g_alpha=0 if any coordinate is odd;
- otherwise g_alpha=product_j (alpha_j-1)!!, with (-1)!!=1.

Define mu_alpha=L(x^alpha) for |alpha|<=18 as follows. Set all moments with an odd coordinate to zero. For the remaining moments:

- mu_0=1;
- mu_alpha=g_alpha/1024 for |alpha|=2 or 4;
- at degree 6, write alpha=2(a,b,c), a+b+c=3, and use

(a,b,c)          (3,0,0) (0,3,0) (2,1,0) (1,2,0) (0,0,3) (1,1,1) (1,0,2) (0,1,2) (2,0,1) (0,2,1)
mu_(2a,2b,2c)   2^24    2^24    1       1       1       4       32      32      4096    4096;

- for |alpha|=2r, 4<=r<=9, let mu_alpha=T_r g_alpha, with

r    4   5   6   7   8   9
T_r  10^16 10^34 10^53 10^73 10^94 10^116.

This specifies every entry of the order-nine moment matrix, a 220-by-220 rational matrix. Coordinate parity makes it block diagonal, with eight blocks of size at most 35.

### Exact positivity certificate

Let I_r be all multi-indices of total degree <=r. For r=3, split (mu_(alpha+beta))_(alpha,beta in I_3) by coordinate parity. The certificate records every leading principal minor of each block; all are positive rational numbers. Sylvester's criterion proves the order-three moment matrix is positive definite.

For r=4,...,9, in each nonempty parity block split the rows into old degrees <=r-1 and new degree exactly r. Its matrix has the form

[ A  B ; B^T  T_r G ],

where A is the preceding positive-definite block, B uses moments already specified, and G=(g_(alpha+beta)) over the new monomials. G is positive definite because it is the Gaussian Gram matrix of distinct monomials. Put C=B^T A^-1 B (or C=0 if no old rows). The certificate verifies, in exact rational arithmetic,

T_r > tr(G^-1 C)

for every block. All eigenvalues of G^-1/2 C G^-1/2 are nonnegative, and each is at most their trace. Therefore T_r G-C is positive definite. The Schur complement proves the enlarged block positive definite. Blocks with no new rows are unchanged. Induction proves the full order-nine moment matrix positive definite.

The finite certificate lists the initial rational minors and every exact trace bound. The checker rebuilds all matrices from the moment table, rather than trusting a numerical eigenvalue or a supplied positivity flag. These are rational inequalities between explicitly specified integers and fractions, not an SDP infeasibility claim.

## 5. Exact cubic sign and finite dimension

Direct expansion gives

L(p)=-1,
L(p²)=11292*10^53,
L(p³)=35039520*10^116.

The first is 1+1+1-4. The other two follow from the Gaussian moments at total degrees 12 and 18, respectively; the checker verifies their polynomial expansions.

For the N-block sum, the exact cubic partition formula is

L_N(S_N³)=N a3+3N(N-1)a2 a1+N(N-1)(N-2)a1³.

Here a1=-1, a2>=1, and therefore

L_N(S_N³) <= N [ a3 - (N²-1) ].

Take N=10^62. Then a3=35039520*10^116 < 10^124-1 = N²-1. The right-hand side is strictly negative. Section 2 proves L_N nonnegative on every square of total degree <=9, so S_N³ is not SOS. The same conclusion holds for (S_N/N)³ by positive scaling. Each p_i³ has the displayed SOS certificate, so their average is an actual finite convex combination of members of C_(3N,6,3) outside that set. This proves the theorem.

The functional is not a measure on real points. Its negative value on the pointwise nonnegative p is precisely the separating property; treating it as an ordinary expectation would be incorrect. Positivity is asserted for the required squares, which is sufficient for the non-SOS certificate.

## 6. Parameter and source limits

- The counterexample uses fixed exponent q=3, fixed degree m=6 and one finite ambient dimension n=3*10^62. Its size is not claimed optimal or practical for writing out every variable or tensor entry.
- The variable number is allowed by the original statement. No theorem here establishes nonconvexity for n=3, for every n, or at a prescribed small dimension.
- For all n>=3*10^62, the same cubic counterexample persists by ignoring the extra variables: an SOS in the larger ring would restrict to an SOS when those extra variables are zero.
- Closedness survives. The union over odd exponents remains convex by the published Blekherman–Kozhasov–Reznick theorem. The block sum can therefore acquire an SOS at a later odd exponent; it is not claimed stubborn.
- The proof uses disjoint variable blocks, beyond Turn 1's single fixed circuit subspace. It does not convert the earlier formal-preordering obstruction into a claim about arbitrary SOS certificates.
- The April 2026 published paper leaves fixed-exponent convexity open in §6. A bounded follow-up source search found no later primary resolution, but no worldwide priority claim is based on that search.

This completes substantive author turn 2. The candidate is frozen for an uninvolved full adversarial review before any status promotion or final PR. If a genuine gap is found, three substantive author turns remain.
