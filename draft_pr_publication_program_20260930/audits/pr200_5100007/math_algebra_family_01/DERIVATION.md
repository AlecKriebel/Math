# Independent physical-coordinate derivation and proof audit

Authored independently after freezing the test design and then reading only
the submitted PROOF.md and verify.py. This is validation, not a novelty claim.
Write A=a², B=b², C=A−B>0 and 0<λ<B.

## Euclidean billiard recurrence and caustic invariant

Use normalized point p=(x,y), x²+y²=1, and normalized ray direction d=(u,v),
so the physical point and direction are (a x,b y) and (a u,b v).
The second outer-ellipse intersection is

    t = −2(xu+yv)/(u²+v²),       p_next=p+t d.

The physical Euclidean normal is n=(x/a,y/b). Reflection gives, in these
normalized coordinates,

    f = 2(xu+yv)/(x²/A+y²/B),
    d_next = (u−f x/A, v−f y/B).

This is not a reflection in the normalized unit circle. Using circle
reflection would silently change the billiard and is a useful wrong-model
challenge. The ray's physical line normal is (b v,−a u). Its tangency to
the confocal ellipse is equivalent to

    λ(Au²+Bv²) = AB(xu+yv)².                         (D1)

To derive (D1), impose line tangency via its support quadratic
(A−λ)ℓ_x²+(B−λ)ℓ_y²=(ℓ·P)² and use x²+y²=1.
Equivalently λ=AB(n·d_phys_unit)². Euclidean reflection reverses the normal
component of a unit ray and preserves its length, so it preserves λ.
Thus the recurrence, straight-line caustic tangency, and reflection are
independent checks of the same geometric trajectory.

The numerical implementation constructs only the first tangent by affinely
mapping the caustic to the unit circle. For p_c=(P_x/√(A−λ),P_y/√(B−λ)),
R=p_c·p_c>1, its two contact points in that circle are

    T_c = (p_c ± √(R−1) J p_c)/R.

Choose the inward ray with positive angular advance, intersect the outer
ellipse, and then use Euclidean reflection for every subsequent ray.
Resonant λ is found by shooting until the lifted total angle is 2πτ,
not by evaluating a Jacobi period formula.

## Tangent intersections and their locus

For outer points with eccentric angles θ,φ, put h=(θ+φ)/2 and
d=(φ−θ)/2. Their chord has equation

    X cos(h)/a + Y sin(h)/b = cos(d),

while the intersection of their two outer tangents is

    Q=(a cos(h)/cos(d), b sin(h)/cos(d)).

Chord tangency to the inner ellipse means

    cos²(d)=1−λ(cos²(h)/A+sin²(h)/B)>0.

It follows directly, without the submitted addition-formula calculation,
that all tangent intersections lie on

    (A−λ)Q_x²/A² + (B−λ)Q_y²/B² = 1.                (D2)

The two positive squared semiaxes of this locus are

    U=A²/(A−λ),       V=B²/(B−λ).

The labels U,V need not be in decreasing order. Their difference is

    U−V = C[AB−λ(A+B)]/[(A−λ)(B−λ)].

At λ=AB/(A+B), the locus is a circle of squared radius A+B. No adjacent
chord of a strictly nested nondegenerate elliptic caustic is a diameter,
so the consecutive tangent intersections are finite. Axis phases present
no singularity in the direct linear solve.

## Paired focal-distance polynomial, in physical variables

For Q_x²=US and Q_y²=V(1−S), its paired squared distance is

    H = (|Q−f_+| |Q−f_-|)²
      = [V+C+(U−V)S]²−4CU S
      = (1−CS/(A−λ))
        ×[(V+C)²−(A−λ)(U−V)²S/C].                  (D3)

The last identity is a rational-function identity in A,B,λ,S;
exact_certificates.py clears and checks it identically. It independently
recovers the essential factorization in the submission after changing
variables to its canonical Jacobi parameter. It also exposes the degree
drop U=V in the four-period case without numerical cancellation.

## Universal exact four-period certificate

At λ=AB/(A+B), write r=√(A²y²+B²x²)>0. The map

    (x,y) → (−Ay/r, Bx/r)                            (D4)

has second iterate (−x,−y), preserves (D1), and selects the next
counterclockwise tangent ray. Reflection preservation of λ establishes
that this is the billiard map. Its four vertices are distinct for real
x²+y²=1 because A,B,r are positive. Let D=Bx²+Ay²>0. Two consecutive
normalized tangent intersections are

    q_0=((Bx−ry)/D, (rx+Ay)/D),
    q_1=((−Bx−ry)/D, (rx−Ay)/D).

The others are −q_0,−q_1. Substituting r²=A²y²+B²x² and x²+y²=1 gives

    A q_0x²+B q_0y²=A+B,
    [A−C q_0x²][A−C q_1x²]=B².

Since H(q)=4A[A−C q_x²] on this circle, the ordinary one-focus product
has square 16A²B², and its positive value is 4AB=4a²b². The script checks
the cleared polynomial identities by exact successive remainders modulo
r²−A²y²−B²x² and x²+y²−1. This is an all-phase N4 calculation.

## Exact primitive eight-period certificate

Take A=8, B=3, λ=24/35. At the axis phase, the normalized vertices are

    (1,0),(4/5,3/5),(0,1),(−4/5,3/5),
    (−1,0),(−4/5,−3/5),(0,−1),(4/5,−3/5).

Their normalized tangent intersections have coordinate types
(±1,±1/3) and (±1/2,±1). For these two types the paired H values are
160/9 and 60, respectively. The ordinary product is therefore

    (160/9) × 60 = 3200/3.

To avoid an axis-only check, start instead at normalized (3/5,4/5) with
normalized inward direction

    (−1, (84−5√193)/97).

All arithmetic in the recurrence is then in QQ(√193). The exact program
verifies eight distinct vertices, closure, every chord's tangency, every
tangent equation and locus equation, antipodal pairing, and the exact
product square 10,240,000/9. Positivity gives the same ordinary value
3200/3. The full vertices are in exact_certificates.json. The N4 generic
certificate similarly uses QQ(√10), with A=9,B=4 and product 144.

## Exact wrong-parity and repeated-cover counterexample

For A=9,B=1,λ=9/16, the exact geometric recurrence has primitive period
six. At normalized starting point (1,0), use direction (−1,√7); its
ordinary one-focus product is 20736/343. At starting point (0,1), use
direction (−1,−√15/5); the product is 6912/125. Exact closure,
primitivity, tangency, tangent intersections and the squared products are
checked in QQ(√7) and QQ(√15), respectively. The two positive rational
products are unequal. Their twofold repeated traversals have twelve
factors, with unequal products (20736/343)² and (6912/125)². This proves
that a hypothesis phrased only as a traversal length divisible by four
would be false; the submitted least-period requirement is substantive.

## Independent recovery of the canonical translation

The canonical parametrization need not be accepted merely because it was
cited in the submission. Set κ=C/(A−λ) in (0,1), and choose the unique
v in (0,K) with sn²(v)=λ/B. Write h=sn(v), C_v=cn(v), D_v=dn(v).
Then

    (A−λ)D_v²/A = C_v² = (B−λ)/B.

For P(u)=(-a sn(u),b cn(u)), the addition identities give the chord through
P(u−v),P(u+v) explicitly as

    −D_v sn(u) X/a + cn(u) Y/b = C_v.                (D5)

Its inner-ellipse support quadratic equals
(A−λ)D_v² sn²(u)/A+(B−λ)cn²(u)/B=C_v², so it is tangent
to that fixed caustic. The normalized cross determinant of its endpoints
is 2h C_v dn(u)/(1−κ sn²(u)h²)>0. Therefore the chord follows the
counterclockwise non-diameter branch. Equation (D1) shows that Euclidean
reflection exchanges the two confocal tangent rays at an outer point;
its outgoing branch is precisely the next such chord. Consequently the
billiard is the translation u→u+2v. As sn/cn traverse the ellipse exactly
once in real period 4K, primitivity is exactly the usual coprime rotation
condition. The endpoint, determinant and coefficient algebra in this
paragraph is checked independently in exact_certificates.py. This recovers
the needed canonical input using standard addition identities; it is not
a new attribution or priority claim about that classical parametrization.

For the branch assertion: reflection preserves (D1) and sends an incoming
ray to an inward ray. It cannot simply reverse the incoming ray, since
normal incidence would give λ=AB|n|²=Bx²+Ay²≥B. Thus it is the other of
the two inward caustic-tangent rays. The two rays have opposite circulation
around the origin because the inner ellipse contains the origin. This
fixes the forward branch used in (D5).

## Audit of the general submitted divisor mechanism

With this canonical input independently recovered, the argument has no
identified algebraic or divisor gap:

* The real point parameter has period 4K. The squared paired function has
  lattice 2K Z+2iK′ Z. Keeping these periods distinct is necessary.
* On that latter torus, sn² has one double pole at p=iK′ and dn² has its
  double zero at p+K. For cn(δ)≠0, the second factor's two simple zeros
  are p+K±δ. Distinctness and absence of accidental pole cancellation
  follow from 0<δ<2K and δ≠K.
* For primitive N=4n, τ is odd, translation δ has exact order m=N/2,
  and nδ=K modulo 2K. Each zero orbit is the same orbit as the poles,
  with the stated multiplicities. Hence the finite cyclic product has
  zero divisor and is constant on the compact torus.
* At δ=K, primitivity forces N=4. The second factor is constant and
  both pole and zero multiplicities drop to two; the separate argument
  in the submission handles this correctly.
* Half the real orbit is antipodal. Pairing converts the positive
  ordinary one-focus product squared to the cyclic product, so the two
  foci have the same value and there is no square-root branch ambiguity.

The period/pole/zero and quarter-shift claims were checked directly against
[NIST DLMF 22.4](https://dlmf.nist.gov/22.4), Tables 22.4.1–22.4.3, read
2026-10-16 UTC. The standard addition identities were also checked at
[NIST DLMF 22.8](https://dlmf.nist.gov/22.8). These support the stated
lattice, shifts, and addition identities;
no source PDF was downloaded or included. This mathematical assessment
does not establish historical priority, and finite computation does not
replace the stated analytic argument.
