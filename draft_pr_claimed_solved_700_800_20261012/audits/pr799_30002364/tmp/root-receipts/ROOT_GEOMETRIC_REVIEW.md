# Root mathematical verification of the completed CM candidate

2026-10-16, after the authenticated intake and an independent target-only
position. Original substantive proof budget: 5/5; new proof-search turns: 0.
This document verifies the saved construction. It does not establish priority,
human peer review, formal proof verification, or publication readiness.

## Exact claim and success criteria

The first question printed on OWR 32/2013 p.1890 is universal in the CM variety
and the reduction prime. A single actual CM variety with the characteristic-zero
all-powers property and a reduction failing the property suffices to refute it.
The second question asks for a class of characteristic-zero varieties. The
already classical CM elliptic class answers its literal existential wording;
a theorem about selected variety/prime pairs alone would not do that. The OWR
contribution itself explicitly credits products of elliptic curves as examples.

The proposed variety is an eightfold over Qbar. Its reduction is over Fbar_5,
with a model over some F_(5^m); no model over F_5 is asserted. Tate classes
mean invariants after a finite extension, exactly as in the source definition.
The claimed failure concerns cohomological divisor generation. It does not
assert nonalgebraicity, a counterexample to either cycle conjecture, or any
identification with numerical equivalence.

## Field, type and geometric existence

For a^2=3+sqrt(6), b^2=3-sqrt(6), a,b positive, ab=sqrt(3). The quartic is
Eisenstein at 3. If sqrt(3) lay in Q(a), then Q(a)=Q(sqrt(6),sqrt(3)). Writing
a=u+v sqrt(3) over Q(sqrt(6)) gives uv=0. The two possible square equations
have rational norms 3 and 1/3, neither a rational square. Thus the real
splitting field L has degree 8. Its signed root substitutions generate D4.
Adjoining i, which is outside a totally real field, gives a degree-16 CM Galois
field E with group D4 times the central complex-conjugation group C2.

Every choice of one embedding from each conjugate pair is an actual CM type.
For example, choose a purely imaginary element with the prescribed signs by
weak approximation in L. Its trace alternating form gives a rational positive
Riemann form; clearing denominators on the O_E lattice makes it integral.
Milne CM pp.26,29–30, Example2.11/Proposition3.12 verify this construction.
Proposition7.9 p.54 supplies descent to Qbar, including the endomorphisms;
finite presentation places the data over a number field. Proposition7.12 p.55
permits potential good reduction at the selected place after finite extension.

For the displayed type f=(-1,-1,-1,1,-1,1,1,-1), its conjugate centered
cocharacters span all eight anti-invariant directions: det(M)=256. A rational
CM subtorus containing the Hodge cocharacter must contain its Galois
translates. Adding the weight direction therefore gives the full nine
dimensional torus defined by x_h*x_ch being independent of h. No rank-to-
geometry assertion is assumed without this minimum-rational-subtorus step.

On every A^n, split E in a characteristic-zero coefficient field. An exterior
monomial is Hodge-invariant exactly when M times its vector of conjugate-pair
multiplicity differences vanishes. Invertibility forces balance in every
pair. Pair the factors, across copies when necessary, to express that monomial
as a product of degree-two invariant monomials. Invariant spaces and the
images of multiplication maps commute with coefficient extension. Surjectivity
therefore descends to Q, where degree-two Hodge classes are divisors by the
Lefschetz (1,1) theorem. This proves the all-powers statement, not only a
finite collection of checks on A itself.

The sixteen torus characters on H1 are distinct, so the rational Hodge
commutant is E. The fully faithful Hodge description of homomorphisms of
complex abelian varieties yields End0(A)=E. An isogeny decomposition would
supply a nontrivial idempotent, impossible in a field. Thus A is simple;
primitiveness is a conclusion rather than an extra unsupported hypothesis.

## Actual prime and normalized specialization

The quartic discriminant is 2^10*3^3. At 5 its factors are
(X^2-4)(X^2-2), with the latter irreducible. At the chosen place a and i
reduce to 2 and sqrt(6) to 1, while b is in F25 and b^5=-b. Thus the actual
decomposition group is {1,s}, where s fixes a,i and negates b. The degree-two
local field is unramified. All E-endomorphisms can be defined before taking
good reduction, and the maximal-order action is available from the chosen
lattice. The hypotheses of Milne CM Theorem8.1 are satisfied.

Let P be this place. Embeddings sigma with sigma^(-1)P=h^(-1)tP form the
left coset D*t^(-1)*h. Counting the type in this actual fiber, divided by |D|,
is the normalized valuation of h(pi) at tP. This is the formula in Milne2001
AppendixA.8 (***) p.22 and Milne CM Corollary8.3 p.68; Conrad Theorem2.1 /
Remark2.2 p.3 independently verifies its finite-extension invariance. There
is no ordinarity hypothesis. The candidate's left/right convention agrees
with this fiber calculation. Replacing the model by a finite extension raises
both pi and q to the same power and leaves all these normalized data unchanged.

The resulting eight-by-eight centered matrix N has four repeated rows and
a top-left four-by-four determinant 80, hence rank4. Its sixteen signed
columns are distinct and nonzero. At P the slopes have multiplicities
0^6,(1/2)^4,1^6. This is neither ordinary nor supersingular. Local degree2
times each slope is integral, consistent with a field endomorphism algebra.
The last observation is a consistency check; existence was supplied by the
CM abelian scheme, not inferred solely from a putative Weil polynomial.

## Geometric endomorphisms and the obstruction

Frobenius commutes with the rank-one E action on H1, so it is an element of
E, integral by the usual endomorphism integrality. The Weil property gives
pi*c(pi)=q. If two conjugates of a positive power of pi coincided, their
quotient before powering would be a root of unity. All its finite valuations
would vanish. The distinct signed valuation columns rule this out for every
pair of different embeddings. Consequently Q(pi^m)=E for every positive m.
Its linear commutant is E tensor Q_l. Tate's finite-field endomorphism theorem
over each finite extension, and descent of every geometric endomorphism to
one such extension, yield End0(A0)=E. This proves geometric simplicity and
prevents an invalid comparison with an obsolete characteristic-zero
Lefschetz group after new reduction endomorphisms appeared.

The candidate relation e=(0,1,0,1,0,-1,0,-1) lies in ker(N). The corresponding
ratio r(pi)*r^3(pi)/((rs)(pi)*(r^3s)(pi)) has zero valuations at every place
over5. It is a unit away from5 because each Frobenius eigenvalue is, and every
archimedean absolute value is1 because total weight is0. Kronecker's theorem
therefore makes it a root of unity, not necessarily1 over the initial model.
The wedge with labels r,r^3,c*rs,c*r^3s in H4(2) is Tate after a finite
extension killing that root of unity.

A degree-two Tate wedge requires two signed columns summing to0. The only
such pairs are the eight conjugate pairs. Tate's divisor theorem makes these
exactly the split divisor space. Products of two of them are supported only
on exterior-basis monomials with two conjugate pairs. The exhibited four
distinct labels have no conjugate pair, so their wedge is outside that image.
The subspace of Tate classes stabilizes after one common finite extension:
there are finitely many eigenvalues in each cohomological degree. Both that
subspace and the divisor-product image are Q_l spaces, and scalar extension
commutes with each. Strict containment over a splitting field therefore
descends to Q_l for every l!=5; no individual eigenline is asserted to possess
a Q_l generator. Exact enumeration gives dimensions32 and28, corroborating
the explicit single-wedge proof.

## Source conflict and remaining scope

The inspected Angle ranks v3 pp.4–6 has absolute simplicity and exclusion of
supersingularity, which this example satisfies. Remark3.5's unqualified
lift-equivalence reading is contradicted by this construction. Its averaging
formula agrees with the calculation; averaging need not preserve orbit rank.
Centered dimensions are8 and4, and including weight gives9 and5, so a weight
convention cannot repair that discrepancy. The publisher HTML currently
contains the same assertion. Section3.6 p.13 separately discusses a lift
associated to a hyperplane arrangement. A paper must acknowledge that
context and frame precisely the assertion about arbitrary CM lifts under
challenge. No author agreement, published erratum, or broader invalidation
of the paper's theorems is established.

The elliptic converse class is classical and already appears in the OWR
discussion. Sugiyama's complete-splitting theorem concerns specified pairs;
the OWR reflex-field and arXiv Galois-closure hypotheses must stay distinct.
The latter file has a17January2013 arXiv v1 header and internal20June2018
date, which must not be flattened into an invented revision history.

Core mathematical verification is consistent so far. Final independent
family reports/replays and a separate extensive priority audit remain
required before promotion. The finite programs are not formal proofs of
the geometric inputs. No outside individual has been contacted.
