# Independent v2 audit

## Disposition

**PASS.** The asserted four-dimensional fixed-support family, its positive
cone, both rate specializations, geometric coprimality statement, clean-rate
integer optimality, both radical decompositions, and the transverse-stability
classification all replay exactly.

This audit makes no publication or priority claim.  It uses no web search and
does not modify the v1 construction.  Its only implementation is the
standalone script in this directory:

```text
.venv/bin/python weakly_reversible_continuum_no_common_factor/audit_v2/verify_v2_independent.py
```

Machine-readable output is available with `--json` and is frozen in
`audit_results.json`.

## Independence of the replay

The asserted data were read, but the original implementations were not
imported or called.  The audit uses four deliberately separate mechanisms:

1. It eliminates (z) by direct substitution and divides univariately in
   (y) to reconstruct the rate-family matrix.  It does not use the asserted
   multivariate normal-form implementation.
2. It enumerates integer rates with integer numerators, divisibility tests,
   and a verified dependency partition.  It does not call an optimizer or the
   existing enumeration routine.
3. It derives each residual steady component by saturation and then
   recomputes the ideal intersection with an auxiliary variable.  It does not
   use the asserted Gröbner-factor/product certificate.
4. It constructs and evaluates the signed Sturm remainder sequence directly.
   It does not call the existing real-root-count convenience method.

No floating-point value is used in a conclusion.

## 1. Four-dimensional family and rank certificate

For a unit rate on a directed reaction, the audit first substitutes

\[
z=x+y-1
\]

and then divides the resulting polynomial by the monic plane equation

\[
\frac{Q}{7}
=y^2-\frac27xy+x^2-\frac{16}{7}(x+y)+\frac{16}{7}
\]

as a polynomial in (y) over (mathbb Q(x)).  Every remainder lies in the
seven-dimensional span

\[
1,x,y,x^2,xy,x^3,x^2y.
\]

Stacking the three coordinate remainders reconstructs

\[
M\in\mathbb Q^{21\times20}.
\]

The asserted submatrix on zero-based rows

```text
0,1,2,4,5,6,7,8,9,12,13,14,15,16,18,19
```

and columns

```text
0,1,2,3,4,5,6,7,8,9,10,11,13,14,16,18
```

has exact determinant

\[
\frac{7255941120}{823543}
=\frac{2^{13}3^{11}5}{7^7}\ne0.
\]

Thus (operatorname{rank}M\ge16).  Substitution of the twenty asserted
formulas gives (Mk=0) identically in (a,b,c,d), and rows
(12,15,17,19) of their coefficient matrix form the (4\times4) identity.
The four kernel directions are independent, so

\[
\operatorname{rank}M=16,
\qquad
\dim\ker M=4.
\]

Because those four rows are exactly (a,b,c,d), the formulas describe every
kernel vector, not merely a four-dimensional subfamily.

## 2. Exact positive cone

Necessity is witnessed by six rates:

- (k_{12}=a, k_{15}=b, k_{17}=c, k_{19}=d);
- (k_3=(c-b)/3);
- (k_{10}=(154d-192a-221c)/64).

Hence positivity requires

\[
a,b,c,d>0,qquad b<c,qquad192a+221c<154d.
\]

For sufficiency, set (h=c-b) and
(s=154d-192a-221c).  The audit forms one exact (20\times4) coefficient
matrix taking ((a,b,h,s)) to all rates.  All eighty entries are
nonnegative and every row has a positive entry (sixty entries are strictly
positive).  The parameter transformation has determinant (1/154), so it is
a rational bijection.  This proves that the six displayed inequalities are
both necessary and sufficient and that the cone has full relative dimension
four.

The two verified interior points are

\[
\begin{array}{c|c|c}
& (a,b,c,d)&(a,b,h,s)\\ \hline
\text{original}&(3920,3920,15680,658560)&
(3920,3920,11760,97200320)\\
\text{clean}&(653,1,70,915)&(653,1,69,64).
\end{array}
\]

Direct evaluation of the family formulas reproduces all twenty frozen rates
in each case.  Both vectors are positive and primitive.  The reconstructed
fields equal the two displayed fields coefficientwise, vanish modulo
((L,Q)), and have Jacobian rank two at
((3/2,1/2,1)).

## 3. Rational and geometric gcd audit

For both rate vectors, exact multivariate calculations over
(mathbb Q[x,y,z]) give

\[
\gcd(F_1,F_2,F_3)=1
\]

and all three pairwise gcds have degree zero.  Homogenizing each primitive
coordinate to degree three also gives homogeneous gcd one.

The geometric implication uses the following lemma.

**Scalar-extension lemma.** If polynomials with rational coefficients have
gcd one over (mathbb Q), they have gcd one after extension to
(mathbb R) or (mathbb C).

To prove it, suppose a normalized irreducible common factor exists over
(mathbb C).  The equations expressing a simultaneous factorization are a
finite polynomial system over (overline{mathbb Q}); a complex solution
therefore yields one over the algebraically closed field
(overline{mathbb Q}).  Every Galois conjugate of this factor divides every
rational coordinate.  The product of its distinct conjugates, with their
common multiplicity, is a nonconstant rational polynomial dividing every
coordinate, contradicting the rational gcd.

The generic-family assertion is also sound.  For common-factor degree
(e=1,2,3), multiplication defines a morphism from the projective space of
degree-(e) factors times the projective space of triples of degree-(3-e)
cofactors.  Its image is closed because the source is projective.  Adding the
origin gives a closed affine cone.  The finite union of these cones pulls back
to a Zariski-closed subset of the four-dimensional rate space.  Any affine
common factor gives a homogeneous common factor after degree-three
homogenization; harmless degree-drop points may enlarge, but cannot shrink,
the closed bad locus.  The verified original and clean specializations lie
outside it.  Therefore geometrically coprime fields contain a nonempty
Zariski-open subset of the family, and this open set meets the positive cone.

**Audit result: PASS.** No rational-versus-geometric gap remains.

## 4. Exact fixed-support integer optimality

The audit enumerates every positive integral family point needed for the two
objectives.  Completeness follows as follows.

Since

\[
k_2=\frac{16d}{15},\qquad k_7=\frac{5c}{14},
\]

integrality forces (15\mid d) and (14\mid c).  Once (c,d) are fixed,
the rate indices split exactly into

```text
fixed: 0,1,2,4,5,6,7,11,13,14,16,17,18,19
a-only: 8,10,12
b-only: 3,9,15
```

with no cross-dependence.  Positivity gives

\[
1\le a<\frac{154d-221c}{192},qquad1\le b<c.
\]

The verifier loops over every allowed integer in these finite ranges and
tests every remaining numerator for positivity and divisibility by its exact
denominator.  For fixed (c,d), minimization separates:

\[
\min_{a,b}\max(F,A(a),B(b))
=\max(F,\min_a A(a),\min_b B(b)),
\]

and the rate sum is additively separable.  Thus no Cartesian-product candidate
is omitted.

For the maximum objective, any competitor strictly below (10296) satisfies

\[
k_{14}=\frac{88d}{15}<10296,
\]

so (d\le1754).  The exact census scans 5006 candidate ((c,d)) pairs; five
pass the fixed integrality tests, with 2775 admissible (a)-values and 675
admissible (b)-values.  Its minimum possible maximum is exactly (10296).

For the sum objective,

\[
k_{14}+k_{16}+k_{18}+k_{19}=\frac{58d}{3}.
\]

A sum below (52464) therefore forces (d\le2713).  This census scans 12070
((c,d)) pairs; sixteen pass the fixed tests, with 12373 admissible
(a)-values and 3553 admissible (b)-values.  Its minimum sum is exactly
(52464).

The clean tuple ((a,b,c,d)=(653,1,70,915)) realizes both values and yields
the asserted primitive vector.  The census includes nonprimitive competitors,
so the conclusion is at least as strong as primitive-normalized optimality.

**Audit result: PASS.** This proves fixed-support positive-integral
max/sum optimality only; it makes no claim of global network minimality.

## 5. Exact steady ideals

The audit repeats the following computation separately for the original and
clean fields.  Let (K=(F_1,F_2,F_3)), let
(mathfrak p=(L,Q)), and derive the eliminated conic equation (D) from
(L,Q).  The residual ideal is discovered by the saturation

\[
\mathfrak q=K:D^\infty
=\bigl(K+(1-uD)\bigr)\cap\mathbb Q[x,y,z].
\]

Its reduced lexicographic basis has the independently checked triangular
shape

\[
x+r_x(z),\qquad y+r_y(z),\qquad R(z),
\]

where (R) is irreducible of degree fifteen and
(gcd(R,R')=1).  Hence (mathfrak q) is maximal of degree fifteen over
(mathbb Q), and becomes fifteen reduced points over an algebraic closure.

The audit then recomputes, rather than assumes, the intersection via

\[
\mathfrak p\cap\mathfrak q
=\bigl(v\mathfrak p+(1-v)\mathfrak q\bigr)
  \cap\mathbb Q[x,y,z].
\]

Its unique reduced basis agrees term-for-term with the basis of (K).
Moreover a direct sum-ideal calculation gives
(mathfrak p+mathfrak q=(1)).  The conic is absolutely prime because its
projective symmetric matrix has determinant (-256).  Therefore, in both
specializations,

\[
K=\mathfrak p\cap\mathfrak q=\sqrt K,
\]

the components are disjoint, and the steady ideal has dimension one.

**Audit result: PASS for both original and clean rates.**

## 6. Exact transverse stability and Sturm audit

The original field is differentiated and then restricted to the exact
rational parametrization.  The verifier checks that the Jacobian annihilates
the parametrized tangent.  It derives the trace and the sum of principal
(2\times2) minors directly, obtaining

\[
\lambda_1+\lambda_2=-\frac{8T(t)}{d(t)^2},
\qquad
\lambda_1\lambda_2=-\frac{6272N(t)}{d(t)^4},
\]

and verifies

\[
(\lambda_1-\lambda_2)^2=\frac{64E(t)}{d(t)^4}.
\]

The signed polynomial-remainder Sturm sequences have degree patterns

```text
T: 4,3,2,1,0
E: 8,7,6,5,4,3,2,1,0
N: 8,7,6,5,4,3,2,1,0
```

and exact real-root counts

\[
\#Z_\mathbb R(T)=0,qquad
\#Z_\mathbb R(E)=0,qquad
\#Z_\mathbb R(N)=2.
\]

Since (T(0),E(0)>0), both (T) and (E) are positive everywhere.  Thus
the transverse trace is strictly negative and the two transverse eigenvalues
are always real and distinct.  For (N), the exact interval counts are

| interval | root count |
|:---|---:|
| ((-infty,-4)) | 0 |
| ((-4,-3)) | 1 |
| ((-3,9/10)) | 0 |
| ((9/10,1)) | 1 |
| ((1,infty)) | 0 |

The signs are (N(-4)>0,N(-3)<0,N(9/10)<0,N(1)>0).  Writing the two roots
as (alpha\in(-4,-3)) and (eta\in(9/10,1)), it follows that the product
of transverse eigenvalues is positive on ((\alpha,\beta)) and negative
outside.  Together with negative trace this gives:

- normally attracting for (alpha<t<eta);
- saddle-type for (t<alpha) or (t>eta);
- one zero transverse eigenvalue at (t=alpha,eta).

The missing parametrization point is exactly
((1/2,3/2,1)).  Leading coefficients give a negative transverse product
there, so it is saddle-type.  On the original theorem interval ((-1,1)),
the classification is attracting on ((-1,eta)), nonhyperbolic at
(eta), and saddle-type on ((eta,1)).

**Audit result: PASS.** The root counts and all sign transitions are exact.

## Final gap assessment

No mathematical gap was found in the audited v2 assertions.  The following
scope limits are important and are preserved here:

- the max/sum theorem is for positive integral rates on this fixed directed
  support;
- generic coprimality means a nonempty Zariski-open subset, not every positive
  parameter;
- stability is transverse to the equilibrium ellipse for the original rate
  vector, not a global nonlinear basin-of-attraction theorem.
