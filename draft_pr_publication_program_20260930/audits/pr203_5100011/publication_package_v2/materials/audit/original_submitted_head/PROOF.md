# The arbitrary-point pedal-area product, k203,a

**5100011 / AMR-050-0011. Full candidate, author turn 2; independent review pending.**

## 1. Exact statement and conventions

Let E be x²/a²+y²/b²=1, a>b>0, and let C be its strictly nested
nondegenerate confocal elliptical caustic, with semiaxes alpha>beta>0.
Write lambda=a²−alpha²=b²−beta², so 0<lambda<b². Fix a billiard
family with **least period N divisible by four**. For each fixed real point
M, project M orthogonally onto the successive side **lines** of its ordered
billiard polygon P. Let Q_M be the resulting ordered pedal polygon.
All areas are signed shoelace areas, A(W)=1/2 Σ det(W_i,W_(i+1)). Then

    A(P) A(Q_M) is independent of the orbit's starting point.        (1)

The constant may depend on E,C,N, the turning number, and M. We also prove
that for each fixed M there is a phase-independent real number c_M with

    A(Q_M)=c_M A(P''),                                               (2)

where P'' is the ordered caustic-contact polygon. The coefficient can be
zero or negative; no division by a pedal area is used.

This is k203,a in **Table 3 of both** arXiv:2004.12497v11, p.6, and the
published *Fifty New Invariants*, Arnold Math. J. 7 (2021), p.346. These
agree on A A_M, N=0 modulo4, and arbitrary M. It is the pedal of P, not
of its outer tangent polygon and not an antipedal. The source's confocal
pair is two ellipses and its area convention is signed. Primitive star
orbits are included. Multiple traversals do not change the primitive
parity hypothesis; no claim about hyperbolic or degenerate caustics is made.

## 2. A radial-area lemma for centrally symmetric polygons

Let an ordered polygon have even length N=2m and opposite side lines paired
by central inversion. Choose a unit tangent t_i on line i, let q_i be the
projection of O to that line, and put T_i=t_i t_i^t. Its pedal vertex is

    q_i+T_i M.

Opposite lines have q_(i+m)=−q_i and T_(i+m)=T_i. Expanding signed
shoelace area, all terms linear in M cancel in pairs. For
M=rho(cos phi,sin phi), t_i=(cos alpha_i,sin alpha_i), and
Delta_i=alpha_(i+1)−alpha_i, the quadratic summand before the shoelace
factor 1/2 is

    det(T_i M,T_(i+1) M)
      =rho² cos(phi−alpha_i) cos(phi−alpha_(i+1)) sin Delta_i
      =rho²/4 [sin(2Delta_i)
          +sin(2phi−2alpha_i)−sin(2phi−2alpha_(i+1))].

The last two terms telescope. Therefore

    A(Q_M)=A(Q_0)+|M|²/8 Σ sin(2Delta_i).                            (3)

Only the ordered shoelace identity was used: convexity and simplicity are
unnecessary. In particular A(Q_M)=A(Q_(−M))=A(Q_(JM)) for
J=diag(1,−1). This equality compares M for the *same* polygon; it does not
yet assert that either coefficient in (3) is an orbit invariant.

## 3. Canonical parameters and a universal area formula

Use Stachel's published Theorem 4.3/(4.9), with modulus
k=sqrt(alpha²−beta²)/alpha in (0,1), complementary modulus
k'=beta/alpha, and complete integrals K,K'. Jacobi functions below use
modulus k. There is v=2K tau/N in (0,K), gcd(tau,N)=1, such that

    delta=2v,  P(w)=(-a sn w,b cn w),
    a=alpha dn v/cn v,   b=beta/cn v.

The orbit is P(w+j delta), and its side-contact sequence is

    B(w+v+j delta),   B(u)=(-alpha sn u,beta cn u).                    (4)

These contact points follow also from the addition formulas and their
caustic tangent equations. Put N=4n and m=N/2=2n. Then tau is odd,

    m delta=2K tau,    n delta=K tau≡K (mod 2K).                     (5)

The real polygon and its lines are centrally symmetric, so (3) applies.
Define the meromorphic cyclic sum

    S(u)=Σ_(j=0)^(N−1) dn(u+j delta).                                (6)

For any constants A,B, the signed area of the ordered points
(-A sn(u+j delta),B cn(u+j delta)) is

    A B sn(v)cn(v)/dn(v) · S(u).                                    (7)

To verify (7), center an edge at x=u+(j+1/2)delta. Addition formulas give
its determinant as 2AB sn(v)cn(v)dn(x)/D(x), where
D(x)=1−k²sn²(x)sn²(v). Also

    dn(x−v)+dn(x+v)=2dn(x)dn(v)/D(x).

Summing the half-determinants over edges proves (7), since every vertex
term occurs twice. In particular

    A(P'')=alpha beta sn(v)cn(v)/dn(v) · S(w+v).                     (8)

The scalar in (8) and S on the real line are positive. Equation (7) is an
ordered signed-area computation valid for stars.

## 4. Meromorphic pedal vertices

The caustic tangent at B(u) has equation n(u)^t X=1, where

    n(u)=(-sn(u)/alpha,cn(u)/beta),
    n(u)^t n(u)=dn²(u)/beta².

Its perpendicular projection of a real point M is

    q_M(u)=q_0(u)+[I−n(u)n(u)^t/(n(u)^t n(u))]M,
    q_0(u)=(-alpha k'^2 sn(u),beta cn(u))/dn²(u).                     (9)

These real formulas define meromorphic functions of complex u using the
**bilinear transpose**, not complex conjugation. Set

    T_M(u)=1/2 Σ_(j=0)^(N−1)
                   det(q_M(u+j delta),q_M(u+(j+1)delta)).           (10)

Thus the required pedal area is T_M(w+v).

The only possible poles of q_M are at the zeros of dn, namely
r=K+iK' modulo 2K and 2iK', each of order at most two. At a pole of
sn,cn,dn all three have simple poles: in q_0 the denominator has order two
and the numerator order one, while n n^t/(n^t n) is regular. Thus the
apparent singularities at iK' are removable, and there are no other poles.

Moreover **q_M is even about every possible pole**. At r this follows
from the standard quarter-period formulas

    sn(r+z)=dn(z)/(k cn(z)),
    cn(r+z)=−i k'/(k cn(z)),
    dn(r+z)=i k' sn(z)/cn(z).

The first two are even and the last is odd in z. Formula (9) is therefore
even. Real and imaginary period shifts of (9) give the same conclusion
at the other poles. The identities and pole orders are the standard
DLMF 22.4 facts, not an assumption inferred from numerical experiments.

## 5. Cancellation of the double poles in the cyclic area

Consider a phase where q_M(u+j delta) has a pole. Its two neighbors are
regular: delta is real and not a multiple of 2K, by primitive N>=4.
The two summands containing this singular vertex combine as

    1/2 det(q_M(u+j delta),
            q_M(u+(j+1)delta)−q_M(u+(j−1)delta)).                    (11)

Writing the singular argument as r+epsilon, the first factor has an even
Laurent expansion with order at most two. The difference in (11) is an
odd holomorphic function of epsilon and vanishes at zero, because q_M is
even about r. The combined expression has a pole of order at most one.

This remains valid if multiple nonadjacent vertices are singular at the
same phase. Adjacent vertices cannot be singular simultaneously. Group
each singular vertex with its two incident edge terms; no edge then
belongs to two such groups. Hence every pole of T_M is at most simple.
This also covers N=4; no separate generic pole-order assumption is used.

## 6. Two-pole uniqueness with the correct symmetries

Under Jacobi period shifts, (9) gives

    q_M(u+2K)=−q_(−M)(u),
    q_M(u+2iK')=J q_(JM)(u),   J=diag(1,−1).                        (12)

For real u, the radial lemma (3) implies T_(−M)(u)=T_(JM)(u)=T_M(u).
All are meromorphic functions, so these equalities extend to complex u
by the identity theorem. Taking determinants in (12), with det J=−1,
therefore gives

    T_M(u+2K)=T_M(u),   T_M(u+2iK')=−T_M(u).                        (13)

Cyclic reindexing also gives T_M(u+delta)=T_M(u). Since
2K=m h and delta=tau h for h=2K/m, and gcd(tau,m)=1, Bezout's identity
shows that h is a real period. On the compact torus

    X=C/(h Z+4iK' Z),                                           (14)

T_M has at most two simple poles, at r and r+2iK'. All translated real
pole locations collapse to these two classes. They remain distinct
because K'>0 and the other generator h is real.

The comparison function F(u)=S(u+K) is also h-periodic and changes sign
under 2iK'. It has **exactly** those two simple poles. Indeed, dn has a
simple pole at iK', and in the N-term sum every residue at the reduced
real pole occurs twice with the same sign: dn has real period 2K, and
the m distinct translates exhaust one orbit. Thus its residue is nonzero.
The imaginary translate has the opposite residue by anti-periodicity.

Choose c so that T_M−cF has zero residue at r. Anti-periodicity cancels
the other residue as well. Both possible poles are simple; thus the
difference is holomorphic on the compact torus (14), and so is constant.
Its anti-periodicity under 2iK' forces that constant to be zero. We obtain

    T_M(u)=c(M)S(u+K).                                          (15)

This argument permits c(M)=0. Since the real pedal area and real positive
S have real values, c(M) is real. No numerical pole cancellation or
unjustified square-root branch is involved.

By (5), K is a cyclic translate modulo 2K, so S(u+K)=S(u). Combining
(8), (10), and (15) proves the phase-independent proportionality (2).
In particular it proves both previously outstanding coefficients from
turn 1, not merely the central-pedal special case.

## 7. Credited even-period area product completes the proof

Chavez-Caliz, *More About Areas and Centers of Poncelet Polygons*, Arnold
Math. J. 7 (2021), 91–106, Theorems 3 and 6 (proof p.104), proves that
A(P)A(P') is constant for even-period Poncelet families between concentric
ellipses in complex-projective general position. The areas are algebraic
areas. For our confocal ellipses, with c²=a²−b²>0, their common complex
points satisfy x²=a²alpha²/c² and y²=−b²beta²/c². These are four distinct
finite transverse intersections: both coordinates are nonzero and the
coefficient determinant is

    1/(a²beta²)−1/(b²alpha²)
       =lambda c²/(a²b²alpha²beta²)>0.

There are no common points at infinity, and the gradient determinant at
each affine common point is 4xy times this nonzero number. Thus the
published theorem's general-position hypothesis is verified.

For completeness the contact polygon is a fixed linear image of P'. If
R_i is the intersection of the outer tangents at P_i,P_(i+1), its polar
line with respect to E is the chord P_i P_(i+1), hence the tangent to C
at the contact B_i. With D_E=diag(a^(-2),b^(-2)) and
D_C=diag(alpha^(-2),beta^(-2)), their normalized equations give

    D_C B_i=D_E R_i,
    B_i=diag(alpha²/a²,beta²/b²) R_i.

No R_i is infinite: an antipodal chord would pass through O and could
not touch the strictly nested elliptical caustic. Taking determinants
in the shoelace sum yields

    A(P'')=alpha²beta²/(a²b²) A(P').                              (16)

Therefore A(P)A(P'') is constant. Multiplying by the fixed c_M in (2)
proves (1), including zero or negative pedal area and arbitrary fixed M.

## 8. Attribution, bounds, and verification

- The radial lemma and arbitrary-M extension were developed in this target's
  two author turns. The central-pedal evenness/simple-pole mechanism and
  two-pole uniqueness were shared author input from the parallel k203,b
  target (5100012), whose turn-1 checkpoint is identified in SOURCES.md.
  That contributor is **not** an independent reviewer of this proof.
- Stachel's canonical parametrization, DLMF Jacobi facts, and Chavez-Caliz's
  area-product theorem are credited inputs. The contact/outer polarity
  reduction was also used in the campaign k110 package; it is reproduced
  here and not presented as a new discovery. The complex pole-cancellation
  method is classical, also used by Akopyan–Schwartz–Tabachnikov.
- The source's strict a>b excludes the circle. If considered separately,
  circular primitive even orbits rotate rigidly and (3) immediately gives
  the same arbitrary-M invariance; no degenerate modulus is inserted into
  the complex proof.
- Reversing traversal changes both signed areas' signs, preserving their
  product. Cyclic relabeling changes neither. Multiple traversals of an
  already admissible primitive orbit multiply both areas by their number
  of repetitions; they do not extend the primitive parity hypothesis.
- The written all-period argument is the proof. Exact algebra and finite
  geometric controls, plus separately labeled high-precision diagnostics,
  are reproducibility aids, not a replacement for that argument.
- A bounded source/literature check did not locate a prior proof of this
  exact arbitrary-M general-period target. This is not a novelty guarantee.
  Full separate review by an uninvolved reviewer is required before a PR.

### Primary references

1. Reznik–Garcia–Koiller, source Table 3 and Sections 1–3:
   https://arxiv.org/pdf/2004.12497v11 and
   https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf
2. Stachel, published Theorem 4.3/(4.9), p.1614:
   https://doi.org/10.1007/s40879-021-00524-2
3. NIST DLMF: https://dlmf.nist.gov/22.4 and https://dlmf.nist.gov/22.8
4. Chavez-Caliz, Theorems 3/6 and signed-area/general-position definitions:
   https://armj.math.stonybrook.edu/pdf-Springer-final/020-0154.pdf
5. Akopyan–Schwartz–Tabachnikov, classical pole cancellation:
   https://arxiv.org/abs/2001.02934
