# Substantive turn 4: a full-conjugator obstruction to translation commutators

**Unreviewed partial, 4/5 substantive author turns. Original generalized-tame membership remains unresolved.** Date: 2026-10-01.

This turn tests a construction using factors that can move x: write gamma as a translation and a polynomial conjugate of its inverse. Such a commutator would be a product of two allowed polynomial LND exponentials even if the conjugating automorphism were not already known to be generalized tame. The construction fails for this target for a precise degree reason. The conjugator in the obstruction is completely arbitrary, not restricted to the localized two-flow group of Turn 3.

## 1. The affine flag subgroup

Retain R=C[x,y,z] and ring composition (sigma tau)(f)=sigma(tau(f)). Let B be the affine subgroup consisting of maps

    d(x)=a*x+b,
    d(z)=e*z+q(x),
    d(y)=c*y+h*z+r(x),                              (1)

where a,c,e are nonzero complex constants, b,h are complex constants, and q,r have degree at most one. It preserves the flag C[x] subset C[x,z] subset R. In particular B contains **every translation of C^3**, including translations moving x. No determinant-one condition is needed for the following obstruction, although translations and the determinant-one members are allowed tame factors.

For a polynomial automorphism F, write deg_(y,z) F(y) for its total degree in y,z over K=C(x), when F fixes x. Denote the usual maximum total coordinate degree over C by deg F.

## 2. Uniform form of every flag-affine conjugate

Put

    X=a*x+b,   Z=e*z+q(x),   Y=c*y+h*z+r(x),
    D=X^2*Y+Z^2.

Direct substitution in the exact source map gives F=d gamma d^(-1) as

    F(x)=x,
    F(z)=z+(X/e)*D,
    F(y)=y-(2*X/c)*Y*Z-D^2/c+6*Z^2*D/c
              +6*X*Z*D^2/c+2*X^2*D^3/c-(h*X/(c*e))*D.        (2)

The x-dependence of q,r is included; it cancels from the affine part in (2). These are polynomial maps with coefficients in C, not merely rational maps. Division is only by the nonzero constants c,e.

Two leading-term facts will be used. First,

    deg_(y,z) F(y)=6,  with leading term (2*X^2*e^6/c)*z^6,
    deg_(y,z) F(z)=2,  with leading term (X*e)*z^2.             (3)

The coefficients are nonzero in K, even though X has a zero on some particular fiber.

Second, suppose polynomials U,V in K[y,z] have degrees p,q satisfying p>2q and q>=1. Substituting (y,z)=(U,V) in (2), the leading term of D is X^2*c times the leading term of U. The cubic D term in F(y) has degree3p; every other displayed term has smaller degree. Consequently

    deg F(y)(U,V)=3p,
    leading coefficient multiplier on U^3 = 2*X^8*c^2,
    deg F(z)(U,V)=p,
    leading coefficient multiplier on U = X^3*c/e.           (4)

Both multipliers are nonzero. This calculation does not require the parameters of successive conjugates to agree.

## 3. Exact degree growth for twisted products

Fix d in B and define

    F_j=d^j gamma d^(-j),
    P_n=F_0 F_1 ... F_(n-1),       n>=1.                      (5)

Each d^j is again in B with nonzero diagonal coefficients, so each F_j has the form (2). Starting from (3), induction using (4) proves

    deg_(y,z) P_n(y)=2*3^n,
    deg_(y,z) P_n(z)=2*3^(n-1).                              (6)

Indeed the degree ratio after the first factor is3, hence the strict inequality required in (4) persists. With ring composition, appending F_j replaces its arguments by the coordinate images under the preceding product, exactly as in (4). The proof treats x as a transcendental coefficient. It does not select a favorable specialization, and it is valid for every d in B.

## 4. No single commutator, with arbitrary polynomial conjugator

**Theorem.** There is no polynomial automorphism H of R and no d in B such that

    gamma = H d H^(-1) d^(-1).                              (7)

Proof. If (7) held, multiplying its successive d-conjugates would telescope:

    P_n = H d^n H^(-1) d^(-n).                              (8)

Both d^n and d^(-n) are affine. Therefore the right side has total degree at most deg H * deg H^(-1), independently of n. But (6) gives deg P_n >= 2*3^n, a contradiction. No requirement that H preserve x or any other coordinate was used. QED.

For a translation d=exp(D_v), where D_v is any constant vector field, its polynomial conjugate is exp(H D_v H^(-1)), a genuine polynomial LND exponential. Thus (7) is a bona fide two-allowed-factor construction moving x whenever the chosen translation does. The theorem excludes that entire construction family, with arbitrary polynomial H and arbitrary translation direction.

It does not exclude all commutators of polynomial automorphisms or all products of two LND exponentials. In particular, a general LND need not be a polynomial conjugate of a constant vector field, and the second factor of a potential factorization need not be a translation.

## 5. Stronger single-exponential and linearization consequence

From (5),

    (gamma d)^n=P_n d^n.                                    (9)

Composing on either side with an invertible affine map preserves maximum total polynomial degree. Consequently (6) implies that the iterate degrees of gamma d are unbounded for every d in B.

Every polynomial LND exponential exp(D) has bounded iterate degrees, since its n-th iterate is exp(nD) and each coordinate has only finitely many nonzero D-iterates. Similarly, an automorphism polynomially conjugate to a linear map has bounded iterate degrees. Thus no flag-affine perturbation gamma d can be a single polynomial LND exponential or be polynomially linearized.

More generally, for d_1,d_2 in B, the map d_1 gamma d_2 is conjugate by d_1 to gamma d_2 d_1. Since B is a group, its iterate degrees are also unbounded. In particular there is no factorization

    gamma=d_1 exp(D) d_2,       d_1,d_2 in B,                 (10)

with an arbitrary polynomial LND D. This allows D to move all coordinates. It excludes one arbitrary nonlinear exponential padded by these affine factors, but places no restriction on a word with two or more general nonlinear exponential factors or with affine factors outside B.

## 6. Why this does not furnish a global subgroup invariant

A concrete countercheck prevents overinterpreting the commutator obstruction. Define two elementary exponentials fixing x,

    E=exp(y*partial_z),       Q=exp(z^3*partial_y),
    h=Q E:   h(y)=y+z^3,     h(z)=z+y+z^3.

Then h is in the allowed subgroup U. Conjugating it by a translation with y,z shifts b,c gives

    h_j(y)=y+(z+c)^3,
    h_j(z)=z+y+b+(z+c)^3.

Every product of n such translation-conjugates has both fiber coordinate degrees3^n: after the first factor the cubic of the preceding z-image strictly dominates every linear term. Therefore h, too, cannot be a single commutator [H,d] with a translation, by the same telescoping argument. This shows explicitly that failure of the translation-commutator construction is compatible with membership in U.

Also h E^(-1)=Q is a single allowed exponential. The affine map E^(-1) does not preserve C[x,z], illustrating why one must not discard the flag restriction in the perturbation theorem.

## 7. Checkpoint

This is an exact obstruction to a natural moving-coordinate factorization mechanism. The proof is global in the polynomial conjugator H, but restricted in the affine map d. It goes beyond the localized group calculation of Turn 3 without claiming an invariant of all finite polynomial-LND words.

The accompanying checker verifies the general conjugation formula, both relevant leading-term tests, exact telescoping as a formal word, and finite examples of the permitted two-exponential countercheck. The all-n conclusions follow from the degree induction above.

No finite factorization of gamma, or valid obstruction to every such factorization, has been obtained. The exact source target remains unresolved after4/5 substantive turns. The 2012 stabilization theorem and the finite-jet/transitivity literature still do not supply the missing three-variable finite word; their credited scopes remain as recorded in earlier turns.
