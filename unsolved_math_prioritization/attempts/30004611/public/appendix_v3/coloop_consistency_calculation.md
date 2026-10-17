# Coloop consistency calculation on the full arrangement functor

14 October 2026 UTC. Row 1775 / 30004611, shared substantive pass 3.

This is an independently derived mathematical calculation for the stated
consistency question, not an independent acceptance report. It does not use
acceptance of pass 2 as evidence for its new consequence. No novelty claim is made.

## 1. Result and precise source scope

Let K be any field and let A be the essential central arrangement in K^4 with
defining polynomial

    x y z (x+y+z) w.

Let P be its intersection lattice with the zero flat removed, ordered by
geometric inclusion. Let D be the covariant S-module functor

    X -> D(A_X),    S=K[x,y,z,w],

with the actual inclusions on arrows. Then

    H^n(P,D)=0 for every n>0,

but D(A) is not free. In fact, in coefficient grading it has the minimal
graded free resolution

    0 -> S(-3) -> S(-1)^2 direct-sum S(-2)^3 -> D(A) -> 0.       (1)

Both assertions below are proved over every field, without importing a
freeness criterion or an acyclicity lemma from the source under review.

These assertions contradict the unrestricted Corollary 1.6 as literally
printed in the retained arXiv:2008.13700v3, and the explicit local-cohomology
calculation in Section 7 also contradicts its stated Theorem 1.1 in this
example. This conclusion is restricted to that inspected arXiv version.
The version of record has not been inspected in this calculation, and no
claim about its corresponding statements or correctness is made.

The exact retained source is Paul Mücksch, *On Yuzvinsky's lattice sheaf
cohomology for hyperplane arrangements*, arXiv:2008.13700v3, revision
12 October 2021, https://arxiv.org/abs/2008.13700v3. The retained PDF has
254,251 bytes and SHA-256
`2a4309b567e5113b48124cc4f17feb1c051c4dbb8ffacebd23ed700fd587676b`.
The separate source-version check verifies the printed conventions and
keeps the published-version question separate.

## 2. Complete product lattice and all stalks

Put R=K[x,y,z], t=x+y+z, B={x=0,y=0,z=0,t=0} in K^3, and W=Kw.
Write H=K^3 direct-sum 0. Every flat of A is exactly one of

    a_Y=Y direct-sum 0,       b_Y=Y direct-sum W,

where Y runs through L(B). After removing the zero flat a_0, P consists of
all a_Y with Y nonzero and all b_Y, including b_0=W.

The arrows are exactly

    a_Y <= a_Z  iff Y<=Z;
    b_Y <= b_Z  iff Y<=Z;
    a_Y <= b_Z  iff Y<=Z;

and there are no arrows from a b-flat to an a-flat. Here and below <= means
geometric inclusion. The localization at a_Y consists of the lifted B_Y
hyperplanes and H. The localization at b_Y consists only of the lifted B_Y
hyperplanes.

All defining equations of B are w-independent. Expanding polynomial
coefficients in powers of w therefore gives, as actual submodules of
Der_K(S),

    D(a_Y) = (S tensor_R D(B_Y)) direct-sum w S partial_w,
    D(b_Y) = (S tensor_R D(B_Y)) direct-sum   S partial_w.       (2)

The first summands contain only partial_x,partial_y,partial_z components.
On every arrow they have the actual inclusion induced by
D(B_Y) subset D(B_Z). The second summand has the identity transition on
each layer and the inclusion wS -> S from the a-layer to the b-layer.
Thus (2) is a decomposition of the full functor, not just of its stalks.

Write E for the first summand and I for the coefficient module of the
second. Thus D=E direct-sum I partial_w. This splitting is homogeneous
and S-linear.

The lattice L(B) has twelve flats over every field: zero, six pairwise
intersection lines, four hyperplanes, and K^3. Indeed any three of
x,y,z,x+y+z are linearly independent, including in characteristic two.
Consequently P has 23 flats. Its strict chains with respectively 1,2,3,4
vertices number 23,88,114,48.

## 3. A self-contained cochain contraction lemma

For a finite poset P and a covariant module functor F, use normalized
cochains

    C^n(P,F) = product over x_0<...<x_n of F(x_n).

The differential on a chain x_0<...<x_(n+1) is the alternating sum of
the first n+1 omitted-vertex values, plus

    (-1)^(n+1) F(x_n<=x_(n+1)) f(x_0,...,x_n).

In particular (d s)(x<y)=s(y)-F(x<=y)s(x). This is the ordinary finite
Alexandrov-sheaf cochain model. All formulas below are module-linear.
For weakly increasing chains, extend a normalized cochain by zero whenever
two adjacent vertices coincide.

Suppose c:P->P is an increasing, idempotent map with x<=c(x), whose image
U has a minimum u. Suppose additionally that

    F(x)=F(c(x)), and F(x<=c(x)) is the identity,                 (3)

using fixed compatible identifications. Restriction j^*:C(P,F)->C(U,F)
and pullback c^*:C(U,F)->C(P,F) are then cochain maps, with j^*c^*=id.

For f of degree n>=1 define

    (K f)(x_0,...,x_(n-1))
      = sum_(i=0)^(n-1) (-1)^i
        f(x_0,...,x_i,c(x_i),c(x_(i+1)),...,c(x_(n-1))).          (4)

All displayed sequences are weakly increasing. Their final coefficient
module F(c(x_(n-1))) is F(x_(n-1)) by (3). The alternating-face
cancellation gives

    d K + K d = c^*j^* - id.                                   (5)

On U, define h by prepending its minimum:

    (h f)(y_0,...,y_(n-1)) = f(u,y_0,...,y_(n-1)).

The same face cancellation gives d h+h d=id-pi, where pi is zero
in positive degrees and in degree zero sends s to the section
y -> F(u<=y)s(u). Consequently

    H = c^*h j^* - K

satisfies dH+Hd=id-c^*pi j^*. In positive degrees it contracts the
complex. Hence

    H^n(P,F)=0 for n>0,       H^0(P,F)=F(u).                     (6)

This proof also works degree by degree for graded modules, since all
maps have degree zero. Equivalently, F is the exact direct image from a
principal open with minimum, but no source lemma about that direct image
is required here.

## 4. Apply the contraction to both summands

For E use the closure

    c_E(a_Y)=b_Y,       c_E(b_Y)=b_Y.

Its image is the principal open U_W={X:W subset X}, with minimum b_0=W.
Formula (2) gives E(X)=E(c_E(X)) with identity transition on X<=c_E(X).
Thus the lemma applies and gives

    H^0(P,E)=S tensor_R D(B),       H^n(P,E)=0 for n>0.

For I use the closure

    c_I(a_Y)=H=a_(K^3),       c_I(b_Y)=V=b_(K^3).

Its image is the principal open {H,V}, with minimum H. Its stalks are
wS and S, with the inclusion as transition. Again I(X)=I(c_I(X)) and
the transition to the closure is the identity. Therefore

    H^0(P,I)=wS,       H^n(P,I)=0 for n>0.

Since the entire functor splits as in (2), so does its full cochain
complex. This proves

    H^0(P,D)=(S tensor_R D(B)) direct-sum wS partial_w = D(A),
    H^n(P,D)=0 for every n>0.                                  (7)

The same proof works for any central essential arrangement with a coloop,
replacing B by its complementary essential factor. In particular, no
freeness assumption on the factor entered the contraction.

## 5. Elementary characteristic-free nonfreeness calculation

Let epsilon=x partial_x+y partial_y+z partial_z. For theta in D(B),
theta(z) is a multiple fz of z. Thus theta-f epsilon kills z, and

    D(B)=R epsilon direct-sum E_z,

where E_z consists of pairs (a,b), standing for a partial_x+b partial_y,
such that x divides a, y divides b, and t divides a+b.

The following three degree-two vectors generate E_z:

    g1=(xy,-xy),       g2=(xt,0),       g3=(0,yt).                (8)

To see generation, write a=xu and b=yv. Reducing xu+yv=0 modulo t
puts us in R/(t)=K[x,y]. Since x,y are relatively prime, there is f
such that u=yf modulo t and v=-xf modulo t. Lifting f to R gives
u=yf+tg and v=-xf+th, yielding fg1+gg2+hg3.

The entire relation module in (8) is generated by

    t g1-y g2+x g3=0.                                          (9)

Indeed a relation f g1+g g2+h g3=0 says
yf+tg=0 and -xf+th=0. Since t is relatively prime to x and y,
t divides f. Writing f=tk forces g=-yk and h=xk. No division by an
integer or characteristic restriction is involved.

Equations (8)-(9) prove the exact graded sequence

    0 -> R(-3) --(0,t,-y,x)--> R(-1) direct-sum R(-2)^3
      -> D(B) -> 0.

Tensoring with S and adding the free generator w partial_w proves (1),
whose injection is (0,0,t,-y,x) in the displayed five generators.
All entries lie in the homogeneous maximal ideal m=(x,y,z,w), so

    dim_K D(A)/mD(A)=5.

Its rank is four: D(A) is contained in Der(S) of rank four and contains
Q(A) Der(S). A free module of rank four over S_m would have a
four-dimensional quotient by m. Thus D(A)_m, and therefore D(A), is
not free. This proves nonfreeness without a factorization theorem,
Ziegler criterion, projective-dimension theorem, or prior example audit.

For orientation, (1) also gives projective dimension one. At the nonzero
flat W the stalk is (S tensor_R D(B)) direct-sum S partial_w and is
nonfree. Hence A is not locally free in the arrangement sense. The older
criterion requiring local freeness is not contradicted by this example.

## 6. Source conventions and possible escape routes checked

The retained v3 defines L_0 by removing the center, which is zero for
this essential arrangement. It uses geometric inclusion, the upper
Alexandrov topology, covariant S-module functors, and exactly
D(U_X)=D(A_X) with the inclusion maps. These are the conventions in
Sections 2-4. Its standing assumptions are central and essential over
an arbitrary field, with ambient dimension at least two. There is no
standing irreducibility or local-freeness hypothesis. The statement
introducing Corollary 1.6 expressly removes local freeness.

Here ambient dimension is four, so the stated test range is n=1,2;
(7) vanishes in both and also in every other positive degree. The
center of the full arrangement is zero, not W; W is retained in its
punctured lattice. Removing W as if it were the full arrangement's
center would change the problem and the functor.

All decompositions, contractions, and resolutions are graded. Assigning
degree -1 rather than 0 to the coordinate partial derivatives just
shifts every coefficient grading uniformly; it cannot change vanishing
of the full cohomology modules or module freeness. The S-module
definition in the source does not impose a different degree truncation.
Taking degree-zero global sections in a graded category likewise does
not restore the asserted unrestricted criterion for this example.

Thus no variance, endpoint, grading, essentiality, or characteristic
mismatch found in these checks removes the contradiction with the
literal v3 statements. The product is excluded by local freeness, but
that is precisely the hypothesis the printed corollary claims to omit.

## 7. A concrete failure in the v3 source proof

For a polynomial ring S=K[u_1,...,u_l] with l>=2, the top cohomology of its
punctured spectrum is the Cech quotient

    H^(l-1)(Spec S minus {m},O)
      = S_(u_1...u_l) / sum_i S_(product_(j != i) u_j).          (10)

The retained v3 Proposition 4.5 instead prints denominator S. This is
not the same S-module. For example in two variables, the true quotient
vanishes on localization at u_1, whereas
(S_(u_1u_2)/S)_(u_1)=S_(u_1u_2)/S_(u_1) is nonzero.
Equivalently, (10) is spanned by monomials with every exponent negative;
the printed quotient also retains monomials with only some negative
exponents. Separate source verification inspected the printed
formula and an official university-hosted copy of the Huneke notes
cited there; the notes give the Cech denominator, not the printed /S.

Write J=H_m^l(S), the module in (10). The class
1/(u_1...u_l) is nonzero and killed by all u_i. The top differential of
the Koszul complex on the u_i, tensored with J, therefore has nonzero
kernel and no incoming differential. In particular

    Tor_l^S(K,J) != 0.

For l>=2 this rules out flat dimension at most one. In contrast,
S_(u_1...u_l)/S is a quotient of two flat modules and does have flat
dimension at most one. The v3 proof of Proposition 5.3 uses precisely
that latter property to apply Lemma 2.9 and assert flat coboundaries.
Replacing only the display in Proposition 4.5 does not preserve that
proof. Proposition 5.4 also uses the same mistaken identification and
its Lemma 2.10 to remove a Tor_1 term for a torsion-free derivation
module. That removal fails concretely here.

For the arrangement A, change polynomial coordinates from x,y,z,w to
x,y,t,w. Let J=H_m^4(S), with the usual all-negative monomial basis.
Tensor the minimal resolution (1) with J. Its first Tor is

    Tor_1^S(D(A),J)
      = {v in J(-3): xv=yv=tv=0}
      = span_K {x^(-1)y^(-1)t^(-1)w^(-d):d>=1},                (11)

where the shift (-3) makes the displayed d-th vector have coefficient
degree -d. Thus, as a graded S-module, (11) is

    K[w,w^(-1)] / K[w],

with x,y,t acting by zero. It is nonzero even though D(A) is torsion-free.

Applying local cohomology to (1), using vanishing of H_m^i(S) for i<4,
gives the identical kernel description

    H_m^3(D(A)) = Tor_1^S(D(A),J).

Consequently for X=Spec S minus {m},

    H^2(X, D(A)-tilde restricted to X)
      = K[w,w^(-1)]/K[w] != 0,

whereas H^2(P,D)=0 by (7). This directly distinguishes the two groups
that retained v3 Theorem 1.1 identifies for n<l-1. It also identifies
the exact omitted contribution in this example, rather than treating
a typographical correction as a completed repair of the theorem.

## 8. Independent finite cochain controls

The accompanying `independent_cochains/check_product_cochains.py` was
written independently for this calculation. It does not use the
E-plus-I decomposition to compute its cohomology. It:

1. Enumerates intersections of all subsets of the defining normals and
   verifies the complete active-hyperplane sets for every tested field.
2. Builds each homogeneous D(A_X)_d as the kernel of polynomial
   divisibility constraints, reducing theta(alpha_H) modulo alpha_H.
3. Constructs every actual inclusion matrix and checks reconstruction
   in the common ambient polynomial-vector space.
4. Builds the normalized strict-chain differentials from these matrices
   and checks every consecutive composite is zero.
5. Computes ranks over the finite field and compares H^0 with the
   independently constructed whole-arrangement kernel and with (1).

All 20 controls pass. They cover both B in three variables and A in four
variables, degrees 0,1,2,3 over F_2 and degrees 0,1 over F_3,F_5,F_7.
For B in degree zero the cochain dimensions are (17,54,36) and ranks
are (17,36), giving cohomology dimensions (0,1,0). Thus the control
correctly detects a positive lattice-cohomology class before adding the
coloop. For A the results include:

| Degree | Cochain dimensions C^0,C^1,C^2,C^3 | Differential ranks | Cohomology dimensions |
| --- | --- | --- | --- |
| 0 | 46,262,408,192 | 46,216,192 | 0,0,0,0 |
| 1 | 228,1138,1680,768 | 226,912,768 | 2,0,0,0 |
| 2 | 639,2980,4272,1920 | 628,2352,1920 | 11,0,0,0 |
| 3 | 1371,6140,8640,3840 | 1340,4800,3840 | 31,0,0,0 |

Degrees 0 and 1 have these same dimensions/ranks in every tested
characteristic. The script is a bounded check, not the proof of the
all-field, all-degree assertion; Sections 2-5 supply that proof.

The JSON result is `independent_cochains/full_cochain_checks.json`.
Run the script from its containing directory with Python 3; it has no
third-party package requirements and rewrites the result JSON there.

## 9. Consequence for the original constructive work

The independently proved pass-1/pass-2 exact sheaf and complex
constructions need not be discarded: this calculation is consistent
with their coloop splitting and does not identify an error in those
constructions. Their use must remain independent of the unrestricted
v3 freeness/cohomology criterion. One can still discuss freeness under
a correctly stated locally-free criterion, subject to verifying the
applicable reference and hypotheses.

This is not a solution of the broad short-exact-sequence Problem 6.3,
does not rule out other constructions, does not certify a repair of
all source theorems, and does not establish what the version of record
states. It settles the specified concrete consistency test and gives
an explicit source-proof obstruction that explains why the unrestricted
inference cannot be imported from the inspected v3.
