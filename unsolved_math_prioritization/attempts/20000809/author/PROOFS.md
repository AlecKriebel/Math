# Proofs and exact scope

Throughout, k is algebraically closed of characteristic zero unless explicitly indicated otherwise. Rational means that the reduced irreducible support has purely transcendental function field over k. Smooth at a point means smooth on the **whole** Hilbert scheme. It does not mean merely smooth on one reduced component, nor smoothness of the subscheme parametrized by the point.

## 1. The finite-length case has a classical affirmative answer

### Lemma 1: distraction smooths every finite-colength monomial ideal

Let R=k[x_1,...,x_n] and let I be a monomial ideal with finite colength d. Let B be the finite set of exponent vectors of standard monomials, so |B|=d. Choose, for each i, sufficiently many distinct elements a_(i,0),a_(i,1),... of k. For each minimal generator x^alpha of I set

D_alpha(t,x) = product over i of product over 0 <= j < alpha_i of (x_i-t a_(i,j)),

and let K be the ideal these polynomials generate in k[t,x_1,...,x_n].

**Claim.** k[t,x]/K is free of rank d over k[t], specializes to R/I at t=0, and has d distinct reduced points at every t != 0.

**Proof.** Each D_alpha is monic with leading x-monomial x^alpha for a degree-compatible order; its other x-monomials have smaller total degree. Repeated reduction therefore expresses every residue class as a k[t]-linear combination of x^beta with beta in B. Thus these d classes span.

Over k(t), for each beta in B consider the point p_beta=(t a_(1,beta_1),...,t a_(n,beta_n)). These d points are distinct. For every generator alpha and standard beta, alpha is not coordinatewise <= beta; choose i with alpha_i>beta_i. Then the factor with j=beta_i vanishes, so D_alpha(p_beta)=0. Consequently the generic quotient has dimension at least d, while the spanning argument gives dimension at most d. Its standard monomials are therefore a basis. The kernel of the spanning surjection k[t]^d -> k[t,x]/K becomes zero after tensoring with k(t). A submodule of the torsion-free k[t]-module k[t]^d with zero generic fiber is zero. The surjection is an isomorphism.

At t=0 the defining generators are exactly the minimal monomial generators of I. At any nonzero t the same d-point argument, now over k, shows that the fiber ideal is precisely the radical ideal of the d displayed points. This proves the claim and smoothability. The proof works over any infinite field with enough distinct chosen scalars; algebraically closed fields of every characteristic suffice. This is the classical distraction argument, explicitly proved in Cartwright--Erman--Velasco--Viray, *Hilbert schemes of 8 points*, published Proposition 4.15. Their preprint has different numbering. QED.

### Lemma 2: the smoothable component has an affine-space chart

Let H=Hilb^d(A^n), with n,d>=1. Consider the open locus U on which 1,x_1,...,x_1^(d-1) is a basis of the universal quotient. Giving an ideal in this locus is equivalent, functorially over any k-algebra, to choosing a monic polynomial

f(X)=X^d+c_(d-1)X^(d-1)+...+c_0

and, for each j=2,...,n, a polynomial g_j(X) of degree <d. The ideal is

(f(x_1), x_2-g_2(x_1),...,x_n-g_n(x_1)).

Indeed multiplication by x_1 determines its unique monic degree-d relation, and each x_j has a unique expression in the chosen basis. Conversely the displayed quotient is free with exactly this basis. These constructions are mutually inverse and polynomial in the coefficients. Thus U is isomorphic to A^(nd).

The condition that f have d distinct roots defines a nonempty open subset of U (the nonvanishing discriminant); its points correspond to d distinct points with pairwise distinct first coordinates. The locus of all d distinct points is irreducible, open, and smooth of dimension nd: it is the quotient of the ordered distinct-point configuration space by a free permutation action. Its closure C_sm is an irreducible component, because near every distinct-point configuration the Hilbert scheme is smooth of dimension nd. The nonempty chart U lies in C_sm: its reduced-distinct-point subset is dense in U, and C_sm is closed. Since U is open in H and C_sm has dimension nd, it is a dense affine-space chart of C_sm. Hence C_sm is rational. No invariant-field rationality conjecture is needed.

The same rationality holds for the smoothable component of Hilb^d(P^n), since the subschemes contained in a fixed affine chart form an open locus, and it contains a dense set of distinct-point configurations. QED.

### Theorem 3: finite-length smooth monomial points lie on a rational component

If [I] is a smooth point of Hilb^d(A^n) and I is monomial, then its unique irreducible component is C_sm and is rational.

**Proof.** Lemma 1 places [I] in C_sm. A smooth local ring is regular, hence a domain; only one irreducible component passes through [I]. Lemma 2 applies. QED.

For the projective characteristic-zero version, let J be a saturated strongly stable ideal in S=k[x_0,...,x_n], ordered x_0>...>x_n, with constant Hilbert polynomial d. No minimal generator is divisible by x_n: if m x_n is in J, strong stability puts m x_i in J for every i, and saturation then puts m in J. Thus J is extended from a monomial ideal I in the first n variables. Its quotient's Hilbert function in degree q is the number of standard monomials of I of total degree <=q. Constancy for large q forces this standard set to be finite of size d. The support is in the affine chart x_n !=0, which identifies a neighbourhood in the projective Hilbert scheme with Hilb^d(A^n). Therefore a smooth Borel-fixed projective point with constant polynomial also has rational unique component. The argument does not assert the same for arbitrary positive-degree Hilbert polynomials.

**Consequence for attempted counterexamples.** Any nonrational component of a Hilbert scheme of points must be singular in the whole Hilbert scheme at every monomial point it contains. Otherwise Theorem 3 would identify it with C_sm. Existing irrational components of Hilbert schemes of points therefore do not contradict this theorem or supply a counterexample with the required smooth Borel point.

## 2. A credited family disproves universal tangent attraction

Fix m>=3 and set

I_m=(x^2,xy^m,y^(m+1)) in R=k[x,y],
J_m=I_m k[x,y,z].

This family is the odd-length family in Cioffi--Lella--Marinari--Roggero, Proposition 3.16. The m=3 case is their Example 3.15(1), credited there to Conca--Sidman. We rederive the relevant geometry and tangent calculation.

### 2.1 Length, saturation and Borel fixation

A basis of A=R/I_m is

1,y,...,y^m, x,xy,...,xy^(m-1),

so d=2m+1. Replacing any factor y in a generator by x yields an element of I_m. Since z occurs in no generator, replacing a z in a multiple by x or y preserves ideal membership as well. Hence J_m is strongly stable for x>y>z and is Borel-fixed in characteristic zero. Multiplication by z on S/J_m is injective; if a polynomial is in the saturation, some power of z annihilates its residue, so the polynomial was in J_m. Thus J_m is saturated. The scheme it defines is supported at [0:0:1] and has constant Hilbert polynomial d.

### 2.2 Complete affine tangent calculation and smoothness

The two adjacent syzygies of the ordered generators (x^2,xy^m,y^(m+1)) are

y^m e_1 - x e_2,
y e_2 - x e_3.

They generate all syzygies: the remaining pair's least-common-multiple syzygy is y times the first plus x times the second, and the pair syzygies generate the syzygies of any monomial ideal. Thus a tangent vector in Hom_R(I_m,A) is exactly a triple (a,b,c) in A^3 satisfying

y^m a = x b,     y b = x c.

Write each element in the basis from 2.1. The first equality imposes precisely m+1 independent linear equations: the coefficient of 1 in a is zero, and the coefficients of 1,y,...,y^(m-1) in b are zero. After imposing these, the second equality imposes exactly m further independent equations: the coefficient of 1 in c is zero, and for 1<=j<=m-1 the coefficient of y^j in c equals the coefficient of xy^(j-1) in b. No other coefficients are constrained. Hence

dim_k Hom_R(I_m,A)=3(2m+1)-(2m+1)=4m+2=2d.

By Lemma 1 the point lies on the smoothable component of dimension 2d. The local dimension is at least 2d and never exceeds the Zariski tangent dimension, which is 2d. The local ring therefore has Krull dimension equal to embedding dimension, so is regular. Over algebraically closed characteristic-zero k this is a smooth point of the whole Hilbert scheme. The same is true projectively because support stays in the open chart z!=0 near the point. The component is rational by Theorem 3.

### 2.3 Two opposite characters

Define R-linear maps on the three generators by

phi: (x^2,xy^m,y^(m+1)) -> (xy^2,0,0),
psi: (x^2,xy^m,y^(m+1)) -> (0,0,xy^(m-1)).

Both images are nonzero standard monomials for m>=3. Both maps kill the displayed syzygies: y^m xy^2=0 in A, and x xy^(m-1)=0 in A. For the action on polynomial ideals induced by x->s x, y->t y, a monomial arrow x^alpha->x^beta has character beta-alpha. Therefore phi has character (-1,2) and psi has character (1,-2).

The full effective diagonal torus of P^2 is (G_m^3)/G_m. The affine coordinates x/z,y/z identify its character lattice with pairs (a,b), lifted to (a,b,-a-b). Thus the projective characters are

chi=(-1,2,-1),    -chi=(1,-2,1).

For every cocharacter lambda, their pairings sum to zero. They cannot both be strictly positive or both strictly negative. This is an exact nonnegative-relation certificate (coefficients 1,1) obstructing a full-dimensional source or sink at this point for **every** diagonal one-parameter subgroup of the full torus. Passing from a small subtorus to the full torus cannot remove this obstruction.

The point is smooth and its component rational. Hence smoothness plus Borel fixation does **not** imply tangent attraction, and failure of attraction does **not** imply irrationality. This refutes the auxiliary conjecture proposed in the prior report, not the original general rationality question.

### 2.4 The m=3 nonsegment certificate

In degree r>=4 let u=x^2 z^(r-2), v=y^4 z^(r-4), w=xy^2 z^(r-3). Then u,v belong to J_3, w does not, and uv=w^2. If J_(3,r) were a segment for any multiplicative term order, both u>w and v>w would imply uv>w^2, a contradiction. In particular r=7, the Gotzmann number for seven points, is excluded. This is the standard equal-product obstruction from the cited source.

## 3. Correct tangent spaces: a concrete 12-versus-14 discrepancy

The tangent space of the projective Hilbert scheme at a closed subscheme Z is

Hom_(O_Pn)(I_Z,O_Z),

not unconditionally Hom_S(J,S/J)_0 for the untruncated saturated ideal J. For a sufficiently large regularity/Gotzmann truncation the usual homogeneous Hom computation does give the projective Hilbert tangent space. For the present finite-support example one can instead work on z!=0, obtaining the affine Hom calculation above.

At m=3, set A=k[x,y]/(x^2,xy^3,y^4). The full tangent triples (a,b,c) have 21 potential coefficients and seven independent relations, hence dimension 14. For Hom_S(J_3,S/J_3)_0, the degree-two generator x^2 must have degree-two homogeneous image. After z=1 its allowed image has only the five basis monomials of affine total degree <=2. The two other generators have degree four and allow all seven basis monomials. There are only 19 potential coefficients, with the same seven independent relations. Thus the untruncated homogeneous Hom space has dimension 12.

Precisely the directions x^2->xy^2 and x^2->y^3 are excluded. The former is one member of the opposite-character pair. The naive 12-dimensional weight set even admits a strict separating cocharacter: in affine coordinates take lambda=(3,2). The retained weights are (-2,1),(-2,2),(-1,0),(-1,1),(0,-3),(0,-2),(0,-1),(1,-4),(1,-3),(1,-2), each pairing strictly negatively with (3,2). The omitted (-1,2) has positive pairing and the other omitted weight (-2,3) has zero pairing. Thus an untruncated implementation would falsely report a contracting direction for the actual Hilbert point.

For example phi on the degree-r truncation sends x^2 z^(r-2) to xy^2 z^(r-3), and psi sends y^4 z^(r-4) to xy^2 z^(r-3). These are degree-preserving arrows with the two stated opposite characters. They are shorthand for the maps induced from the full affine/sheaf morphisms on all truncated generators; specifying only one arrow would not define the entire morphism. The exact code reconstructs the whole kernel using every pair syzygy, at r=4 and r=7, and obtains all 14 directions with their multiplicities.

## 4. The valid sufficient criterion remains useful, but does not settle AIM

Let X be a projective finite-type k-scheme with a torus action, let p be a torus-fixed smooth point, and let C be its unique irreducible component. Suppose some cocharacter has all tangent weights strictly positive (with the convention that positive weights attract as t->0).

The smooth locus X_sm is invariant. Every point attracted to p lies in X_sm: otherwise its punctured orbit is contained in the closed invariant nonsmooth locus and so is its limit p, a contradiction. On X_sm, the smooth Bialynicki--Birula theorem gives the attracting fiber over the isolated fixed point p as affine space of dimension equal to the positive tangent dimension. The zero tangent space of the fixed locus is zero, so p is an isolated component of the fixed locus. The affine fiber has dimension dim T_pX=dim C, is locally closed and irreducible, and contains p. Its closure is C; being locally closed and dense, it is open in C. Therefore C is rational. A convenient modern reference for exactly the smooth affine-fiber conclusion is Jelisiejew--Sienkiewicz, arXiv:1805.11558v3, Theorem 1.5.

For a finite integral set of characters chi_i, strict half-space feasibility is equivalent to the nonexistence of a nonzero nonnegative rational relation sum_i a_i chi_i=0. One elementary proof is to separate the origin strictly from the compact convex hull of the characters when it does not belong to that hull. If it belongs, a convex relation exists; solving a minimal-support rational linear system yields rational coefficients. If the strict separating functional is real, openness and rational density yield a rational one, and clearing denominators yields an integral cocharacter. Pairing with a nonnegative relation proves mutual exclusivity. This is the standard Gordan alternative.

This criterion requires **the actual** tangent representation, and it is only sufficient. Section 2 shows why smooth Borel fixation cannot be used to supply its missing half-space hypothesis.

## 5. Why the double-generic theorem does not automatically close the gap

Bertone--Cioffi--Roggero, arXiv:1503.03768v2, Theorem 6.10, prove rationality for an isolated irreducible component whose double-generic initial point is smooth on that component. Their Corollary 6.11 covers components containing an arithmetically Cohen--Macaulay codimension-two subscheme. These are credited prior results.

One cannot simply replace that distinguished point by any smooth Borel point. For J_3, the quadratic Hilbert function is 5. For a general set of seven points of P^2 it is 6: six suitable points impose independent conditions on quadrics (e.g. the affine points (0,0),(1,0),(2,0),(0,1),(0,2),(1,1)); adding a seventh cannot decrease the rank. The nonzero minor condition is open, so the same holds generally. Ordinary initial and generic initial ideals preserve the homogeneous Hilbert function. It follows that J_3 is not the saturated generic initial ideal of a general point of this component under any order whose initial ideal is saturated. More generally it cannot be the high-degree double-generic limit for any order: a double-generic source is the limit of a dense stratum and would satisfy the tangent-source property when smooth; Section 2 rules this out. The latter conclusion uses the dense Groebner-stratum/positive-grading argument, not an invalid claim that saturation always preserves low-degree Hilbert functions.

Thus the given smooth Borel point need not be the one used by the double-generic theorem. There is no proof here that a different double-generic point of an arbitrary component is smooth. Smoothness can be lost in a flat degeneration. Neither the existence of a smooth affine local chart nor unirationality alone establishes rationality.

## 6. Remaining general question

For positive-dimensional subschemes of projective space, beyond the cited segment, globally smooth, smooth-double-generic, and ACM codimension-two cases, this packet proves neither that every component containing a smooth Borel point is rational nor that some such component is nonrational. The full source target must therefore remain unresolved under that general interpretation. The finite-length theorem and the failure of a proposed sufficient method are distinct conclusions, and neither should be reported as a new complete solution of the general AIM question.
