# Turn 2: try reconstruction from all cyclic branched-cover residues

**Result:** the full unweighted root-grid residue sequence is noninjective
on the symmetric Laurent-polynomial target, even after normalization at
(1,1). This is the second substantive attempt; the invariant itself remains
unconstructed by this route.

Garoufalidis–Kricker, Corollary 1.2 and Section 5.3, express a
signature-corrected Casson–Walker invariant by a root-of-unity residue of
the rational two-loop function. Their residue carries a normalization
factor depending on the cover degree. Multiplying each entry by a nonzero
known factor does not affect injectivity. We therefore work with the
unambiguous normalized linear operator

A_n(f)=1/n^2 sum_{xi^n=eta^n=1} f(xi,eta), n>=1,

on Laurent polynomials f(x,y), with z=(xy)^-1. No roots-of-unity
denominators occur in the polynomial case examined first.

## 1. Complete coefficient description of the transform

Write f=sum c_ab x^a y^b with finite support. Orthogonality of characters
of the cyclic group gives

A_n(f)=sum_{n divides a and n divides b} c_ab.

This is an identity for every n, not a finite numerical sample. Define

B_0=c_00,
B_d=sum_{gcd(|a|,|b|)=d} c_ab for d>=1.

Then

A_n(f)=B_0+sum_{k>=1} B_(kn).

Only finitely many B_d are nonzero. Therefore B_0 is the eventual constant
value of A_n, and Möbius inversion gives

B_d=sum_{k>=1} mu(k)[A_(dk)-B_0].

The series on the right is finite because A_(dk)=B_0 for large k.
Consequently the entire residue sequence determines exactly these gcd
shell totals. It does not recover the distribution of coefficients within
a shell.

## 2. A theta-symmetric kernel element

For integers a,b, let O_(a,b) be the sum of the **distinct** monomials in
the orbit of x^a y^b under S3 and simultaneous inversion. Operationally,
start from the exponent triple (a,b,0), permute it to (p,q,r), then use
(p-r,q-r) and its negative. Repeated exponents contribute only once.

The action on Z^2 is by unimodular integral matrices. It preserves the gcd
of the two exponents. In particular all exponents in both O_(1,0) and
O_(2,1) are primitive, and both orbits contain six monomials:

O_(1,0)=x+y+(xy)^-1+x^-1+y^-1+xy,

O_(2,1)=x^2 y+x y^2+x/y+y/x+x^-2 y^-1+x^-1 y^-2.

Set F=O_(1,0)-O_(2,1). It is nonzero: the coefficient of x^2 y is -1.
It is G-invariant and F(1,1)=0. Every nonconstant exponent has gcd 1, so

A_1(F)=6-6=0, and A_n(F)=0 for every n>=2.

Thus even *all* cover degrees, together with the normalization at 1 and
theta symmetry, cannot identify an arbitrary polynomial in the target.

There are infinitely many distinct primitive orbits. Differences of their
orbit averages give an infinite-dimensional kernel. Indeed orbit supports
are disjoint; after fixing one reference orbit, the other differences are
linearly independent.

## 3. Denominators and topology are not to be skipped

For a fixed Alexander polynomial Delta, the actual input to the residue
operation is a rational function with denominator
Delta(x)Delta(y)Delta((xy)^-1). Only cover degrees at which that denominator
does not vanish are directly admissible in the rational-homology-sphere
formula. These restrictions cannot produce more observations than the
full root-grid transform.

However, the particular polynomial F above is **not asserted to be the
difference of invariants of two actual knots**. Algebraic noninjectivity
on the ambient target does not prove that the topological residue data
fails to distinguish every possible knot-value pair. A realization theorem
or a theorem restricting the image could change that question. The result
does prove that a formal inversion of the residue transform, without any
further topological information, is invalid.

## 4. Next test

The kernel in this turn need not lie in the kernel from Turn 1. Perhaps
combining all residues with the reduced invariant could remove the
ambiguity. That stronger possibility is the next substantive test.

**Remaining full-target gap:** either identify an actual-image injectivity
theorem or construct topological data beyond unweighted cyclic-cover
residues. No comparison theorem for a candidate invariant has been proved.
