# Exact examples and negative controls

Row 1793 / ID 20000200, shared mathematical pass 1, 2026-10-16.

These are authored algebraic calculations for the frozen complex fixed-pair
problem. They independently check conventions, canonical-cover behavior,
reconstruction, positive genus, and strictness of the obstruction stages.
They are not finite experimental evidence for the general theorem.
The accompanying script runs **49 exact checks over Q(i)**, all passing.

## 1. Conventions checked from an arbitrary parametrization

Use isotropic coordinates z=x+iy, w=x-iy, so the Euclidean metric is dz dw.
For a local parameter t, write P=z', Q=w', and

    h=P'/P-Q'/Q.

On the open stratum hPQ != 0, the invariant formulas are

    u= -h^2/(4PQ),                 v= i u'/h.

Indeed, h dt=dlog(dz/dw)=2i kappa ds and ds^2=PQ dt^2, while
du=2 kappa v ds. Thus

    eta = i du/v = h dt,
    q = du^2/(4u v^2) = PQ dt^2.

These formulas give u=-1/(8t^3), v=-3i/(8t^3) for z=t,w=t^2,
and hence v=3iu. Swapping z,w preserves u but negates v: this is the
reflection check, and the fixed target pair does distinguish the two signs.

For the preferred-cover notation used in the proofs, put

    omega=(eta-dlog u)/2,
    rho=du/(2v),                   sigma=du/(2uv),
    dlog a=omega,
    alpha=a rho,                  beta=a^-1 sigma.

Then alpha beta=q and alpha/beta=u a^2. For an already parametrized
source one can take a=2iP/h, giving alpha=dz and beta=dw exactly.
All factors 2 and i in the examples below follow this convention.

## 2. A nonhomogeneous realizable cubic signature requiring a double cover

Take the irreducible degree-three source

    z=t,                         w=t^3+t.

Its metric is (3t^2+1)dt^2, generically nonzero, and its signature is

    u=-9t^2/(3t^2+1)^3,
    v=-3i(6t^2-1)/(3t^2+1)^3.

Set r=t^2. The signature field is exactly K=C(r), because

    r=iu/[3(2iu-v)].

The signature is the integral cubic whose equation is

    27u^3+27iu^2v+12u^2-9uv^2+12iuv-iv^3-3v^2=0.

One can take its image closure as the definition; substitution verifies
the displayed equation. The rational parametrization is birational, and
its homogeneous degree-three coordinate polynomials have no common zero,
so the image has degree three and this is its irreducible equation.

On K,

    eta=-3 dr/(3r+1)=dlog(1/(3r+1)),
    omega=3 dr/(3r+1)-dr/(2r).

Thus the tangent-ratio logarithmic derivative already has an ordinary
rational primitive, but the canonical omega-root requires a double cover:

    a^2=-(3r+1)^2/(9r),
    a=(3t^2+1)/(3it),             t^2=r.

The half-integral residue at r=0 proves that this root cannot be in K.
The extension L=C(t) is genuinely quadratic, and on it

    alpha=dt,
    beta=(3t^2+1)dt.

Its primitives are precisely z=t and w=t^3+t. They generate L, so the
reconstructed plane image has the prescribed normalization rather than
just an unexplained finite quotient of it.

The two descended rational ODE certificates are

    A=3ir/(3r+1),                 B=(r+1)(3r+1)/(3i),
    dA+omega A=rho,               dB-omega B=sigma.

They give z=aA and w=a^-1B. This example checks a nonhomogeneous input
and shows why working only with a logarithmic tangent ratio on K misses
the square-root step. The source has the order-two symmetry t -> -t.

## 3. A realizable signature whose own normalization has genus one

Let E be the smooth projective model of

    y^2=x^3-x,

and take source isotropic coordinates z=x,w=y. Its affine plane image is
the reduced integral degree-three curve w^2=z^3-z. Let

    f=x^3-x,                     f'=3x^2-1,
    H=3x^4-6x^2-1,
    J=15x^8-68x^6+10x^4+28x^2-1.

The metric is [f'/(2y)]dx^2, generically nonzero. Direct differentiation
in the function field C(x,y) gives

    h= -H/(2ff'),
    u= -y H^2/(8f^2(f')^3),
    v= -3iy J/(8f^2(f')^3).

These invariant functions generate all of C(x,y), not merely an unknown
subfield. In fact

    u^2=H^4/[64f^3(f')^6],       v/(iu)=3J/H^2.

The first rational function of x has degree 21, and the second has degree
8. Their respective numerator/denominator pairs are coprime, as verified
by exact polynomial gcds. If K0 is their joint subfield of C(x), then
[C(x):K0] divides both 21 and 8 by the tower formula. Consequently K0=C(x).
It follows that x belongs to C(u,v), and then

    y= -8u f^2(f')^3/H^2

belongs to C(u,v) too. Therefore C(u,v)=C(x,y), and the smooth projective
normalization of the signature has genus one.

For this input the preferred cover is trivial:

    a=2i/h= -4iff'/H is in K=C(u,v),
    omega=dlog a,
    alpha=dx,
    beta=dy=[f'/(2y)]dx.

The two primitives generate K. Thus this is a positive-genus successful
case, with neither a rational-signature restriction nor an additional
cover. It also checks that positive genus itself is not an obstruction.

## 4. A logarithmic-pass, zero-residue-pass conic that is not realizable

Consider the integral conic parametrized by

    u=(t-1)(t-2),                v=it(2t-3).

Its function field is K=C(t), since

    t=(-iv-2u+4)/3.

An implicit equation is

    -4u^2-4iuv+7u+v^2-iv+2=0.

Here

    eta=dt/t,
    omega=(dlog t-dlog[(t-1)(t-2)])/2.

Thus eta is already logarithmic on K. The minimal omega-root has degree
two, since its residues at 0,1,2,infinity are respectively
1/2,-1/2,-1/2,1/2. Write the canonical cover as

    y^2=t(t-1)(t-2),             a=t/y.

The squarefree cubic gives a smooth projective genus-one normalization,
with branch points 0,1,2,infinity. The canonical differentials become

    alpha=dt/(2iy),
    beta=dt/(2ity).

The differential alpha is a nonzero holomorphic differential on this
elliptic curve. It cannot be the differential of a meromorphic function:
the derivative of a function with a pole has a pole in characteristic
zero, while a holomorphic function on a projective connected curve is
constant.

Both alpha and beta nevertheless have zero residues everywhere. For
alpha this follows from holomorphy. The only pole of beta is the point
above t=0, where it has order two. In a parameter s with t=s^2,

    y=s sqrt((s^2-1)(s^2-2)),
    beta= [1/(i sqrt(2))] s^-2 (1+3s^2/4+...) ds.

There is no s^-1 term. At the other finite branch points dt/y is regular,
and beta has no additional pole; at infinity, t=s^-2 gives dt/(ty)=O(s^2)ds.

Hence this input defeats not only a torsion-logarithmic-only criterion
but also any criterion that replaces global exactness on the canonical
cover by vanishing residues. Further finite covers cannot help: the
pullback of alpha remains nonzero and holomorphic, so the same argument
rules out exactness there. This gives a direct geometric no-rescue check
independent of the general trace lemma.

## 5. A simpler logarithmic-pass, residue-fail polynomial graph

Take

    u=t,                        v=it(t-1).

Then eta=dlog((t-1)/t), and a^2=(t-1)/t^2 is a minimal quadratic
omega-root. Put b^2=t-1 and a=b/(b^2+1). The cover is rational and

    alpha= -i db/(b^2+1)^2,
    beta= -i db/[b^2(b^2+1)].

The residues of alpha at b=i,-i are -1/4,+1/4. The residues of beta
there are +1/2,-1/2; its residue at b=0 is zero. Thus this graph passes
the logarithmic test, but fails exactness already by residues.
Pulling back a nonzero residue along any finite ramification multiplies
it by a positive integer; it does not remove the obstruction.

## 6. Rational ODE certificates alone do not certify an algebraic root

For the cuspidal signature input

    u=t^2,                      v=t^3,

one has K=C(t) because t=v/u. Its data are

    eta=2i dt/t^2,
    omega=(i/t^2-1/t)dt,
    rho=dt/t^2,                 sigma=dt/t^4.

Both descended rational ODEs have solutions:

    A=-t-i,                     B=i/t^2-1/t,
    dA+omega A=rho,             dB-omega B=sigma.

But omega has a double pole. No nonzero integer multiple can be a
logarithmic derivative of a meromorphic function on K, or on any finite
cover. A formal analytic root is a=e^(-i/t)/t; its resulting primitives

    z=(-i/t-1)e^(-i/t),          w=(i/t-1)e^(i/t)

are transcendental. This explicitly separates the algebraic-root condition
from the two rational ODE conditions. The observation and trial formulas also appear in the differential-equations report; every identity here was independently verified by the accompanying exact script.

## 7. Finite-cover and source-normalization controls

The trace identity supplies a general exactness check: if a differential
alpha in a characteristic-zero one-variable function field L becomes
dG in a finite extension M/L of degree d, then

    alpha=d(Tr_(M/L)(G)/d).

Thus further finite covers cannot repair failed meromorphic exactness.
The holomorphic example in Section 4 and residue example in Section 5
verify two different concrete manifestations of this fact.

Redundant parametrization covers must not be mistaken for the source
normalization. On C(s), the functions z=s^2,w=s^4 satisfy the same Frenet
identities as the parabola z=t,w=t^2 under t=s^2. They give

    u=-1/(8s^6),                 v=-3i/(8s^6),

but C(z,w)=C(s^2) is strictly smaller than C(s). The image is still the
same parabola and its signature closure is still v=3iu. The unnecessary
cover cannot change the image or upgrade its normalization.

For the actual minimal omega-cover, an exact reconstruction has the
useful automatic equality mechanism: u,v can be recovered as rational
invariants of its image, so K is contained in C(z,w); then
a=2v dz/du belongs to C(z,w), and L=K(a) is contained in C(z,w).
The reverse inclusion is immediate. This uses the differential identities
and nondegeneracy, not an unverified assumption about a parametrization.

## Files and verification scope

- `check_examples.py`: reproducible exact symbolic checks.
- `CHECK_RECEIPT.json`: all 49 checks pass, with the SymPy version recorded.

The geometric assertions about genus, poles, holomorphic exactness, and
field degrees are proved above; the script checks the supporting rational
identities and coprimality statements. No numeric integration, finite
sampling, numerical period test, or source-text quotation is used.
