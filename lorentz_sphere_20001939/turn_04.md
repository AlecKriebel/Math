# Attempt 4 of 5: torus symmetry with cross terms and nondegenerate principal orbits

## Target and verdict

The cached diagonal Hopf ansatz fails before projective equivalence is imposed, but Lorentz Berger metrics show that angular cross terms are essential and legitimate. This attempt keeps those cross terms and proves a wider restricted nonexistence result. The outstanding hypothesis is that every principal torus orbit is nondegenerate for one metric.

## Theorem

Let g be a smooth Lorentzian metric on S³ invariant under the standard T² action

(z1,z2)↦(e^(iφ)z1,e^(iψ)z2).

Assume the induced metric on each principal torus 0<r<π/2 is nondegenerate, where |z1|=sin r and |z2|=cos r. Then every indefinite metric globally projectively equivalent to g is proportional to g.

Proof. Suppose a nonproportional partner gbar exists. Attempt 3 makes gbar T²-invariant. Write a general invariant metric on the principal interval as

g = a0(r) dr² + 2 b(r)^T dr dθ + dθ^T G(r)dθ,

where θ=(φ,ψ). By hypothesis G is invertible throughout the interval. An r-dependent translation of θ, with derivative -G^(-1)b, eliminates the radial-orbit terms of g. This does not change the Killing fields K1=∂φ,K2=∂ψ or the orbit matrix G. The result is

g=a(r)dr²+dθ^T G(r)dθ,

with a nowhere zero. Smooth invariant polar-coordinate expansions at each singular circle show that this gauge can be taken smooth there: the collapsing-angle radial coefficient is O(r³), the surviving-angle radial coefficient is O(r), and G has one eigenvalue of order r² and one with nonzero limit. Thus the required gauge derivatives are O(r). Alternatively, all calculations below can be performed on the open interval, with endpoint limits interpreted through the invariant Killing fields and the smooth horizontal normal direction.

### Step 1: the partner has no radial-orbit terms in this gauge

The projective connection difference is δ^i_j φ_k+δ^i_k φ_j. Invariance makes φ=p(r)dr. Write the partner's radial-orbit coefficients as bar b_a. The metric compatibility identity is

∇_k gbar_ij = 2φ_k gbar_ij + φ_i gbar_kj + φ_j gbar_ik.

For angular k=a,i=b,j=c, the Christoffel symbols of g give

G'_(ab) bar b_c + G'_(ac) bar b_b = 0.

A nonzero row w of G' therefore satisfies w⊗bar b+bar b⊗w=0, which forces bar b=0. Such a row exists at some r: the collapsing angular coefficient tends to zero at an endpoint but is positive close to it.

The (k,i,j)=(r,r,a) equations give a homogeneous linear ODE for bar b:

bar b' = [(a'/2a+3p)I+(1/2)Q^T]bar b,  Q=G^(-1)G'.

Its coefficients are smooth on the entire principal interval. Since bar b vanishes at one point, it vanishes throughout. Thus both metrics, and hence their compatibility tensor, are block diagonal:

L=diag(l(r),A(r)).

### Step 2: the angular block of L is constant

Put τ=tr L. The radial-radial component of the compatibility equation yields l'=τ'. The angular-radial and radial-angular components yield respectively

(lI-A)Q=τ'I,   Q(lI-A)=τ'I.

Thus [A,Q]=0. The radial derivative of the angular block satisfies

A'+(1/2)[Q,A]=0,

and therefore A'=0. This argument remains valid when l is an eigenvalue of A; no inverse of lI-A was taken.

### Step 3: smooth collapse diagonalizes this constant block

At r=0, K1 vanishes while K2 does not. The identity L K1=A11 K1+A21 K2 and smoothness force A21=0. At r=π/2, K2 vanishes while K1 does not, forcing A12=0. Therefore A=diag(c1,c2) with real constants.

If c1≠c2, g-self-adjointness of A gives (c1-c2)G12=0. Thus G12=0. The radial coefficient a is positive near both endpoints because each collapsing normal two-disk has a rotation-invariant definite metric, and in signature (-,+,+) that two-disk must be positive definite. Hence a>0 everywhere. At the first endpoint the collapsing φ direction is positive and the surviving ψ direction negative; at the second, ψ is positive and φ negative. A diagonal nondegenerate G on the connected interval cannot change either diagonal sign. Contradiction.

If c1=c2=c, put u=l-c. The equations become uQ=u'I. Their trace yields the scalar linear ODE

u'=(1/2)tr(Q)u.

If u vanishes anywhere, uniqueness forces u≡0, so L=cI and the pair is proportional. Otherwise u never vanishes and G'=u'G/u, whence G(r)=u(r)C for a constant nonsingular matrix C. Smoothness bounds l and gives an endpoint limit for u. But G has a finite nonzero rank-one limit at either singular circle. A scalar multiple of a fixed nonsingular two-by-two matrix cannot have such a limit: a nonzero limiting scalar gives rank two, while a zero limiting scalar gives the zero matrix. Contradiction. ∎

## Scope and failed extension

The theorem allows general angular cross terms and, initially, radial-orbit terms. It requires nondegenerate principal torus orbits for g, not for gbar. It excludes, for example, the usual Lorentz Berger metrics as possible first metrics without assuming the partner is invariant.

If det G vanishes at a principal orbit, the horizontal gauge and Q=G^(-1)G' need not extend. The proof gives no justification for crossing such a torus. Those degeneracies can occur in perfectly smooth Lorentz metrics on S³, as the next attempt checks explicitly. The unrestricted problem is still open in this work.

## Credit and novelty

The argument uses the published mobility-two theorem through Attempt 3; all displayed one-variable equations follow directly from metric and projective compatibility. No priority claim is made for this restricted theorem.
