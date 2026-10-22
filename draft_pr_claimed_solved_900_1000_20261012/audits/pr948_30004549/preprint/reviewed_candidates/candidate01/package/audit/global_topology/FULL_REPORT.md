# Independent global, topological, and cohomological audit

Problem 30004549; PR 948; immutable submitted head
`be4313efafa1af5962394e07d8a4debff2e94d92`.
This review concerns the submitted construction, not priority or novelty.

## Result and limits

**PASS for the assigned global/smooth/topological/cohomological scope.**
The candidate's compact manifold, holomorphic forms, local ratio chart,
global exact perturbations, positive-plane realization, collar gluing, and
three independent anti-invariant classes all survive the independent
checks below. No topological, de Rham, zero-set, elliptic, or unique-continuation
obstruction was found. The submitted core also has a directly checkable
nonzero Nijenhuis component, recorded below for consistency.

Strongest verified statement in this scope: on the smooth compact
boundaryless connected four-manifold C x E specified below, every sufficiently
small nonzero real epsilon gives a smooth almost-complex structure J_epsilon,
equal to the product J_0 outside one coordinate ball and converging to J_0
in C-infinity, with three fixed independent de Rham classes represented by
closed J_epsilon-anti-invariant real two-forms. The core structure is
nonintegrable.

This statement assumes the ordinary smooth category and allows the
compatible metric to depend on J. No exact value of h_J^-, compatibility
with a prescribed symplectic form or metric, analytic continuation statement,
priority, current openness, or novelty is certified here. The source-scope
and prior-theorem families remain separate parent audits. Verification adds
zero author proof responses; the supplied declared count is 4/5, and native
earlier author history remains unknown to this reviewer.

## Authentication and independence

Before mathematical intake I read ELIGIBILITY_GATE.json,
ORIGINAL_SNAPSHOT.json, ORIGINAL_FILE_RECORDS.json,
TARGET_IDENTITY_PREFLIGHT.json, and RESEARCH_CHARTER.md. All 24 original
files were independently checked for exact SHA-256, byte count, regular-file
status, and disk mode 0644 against both manifests. The head identities agree.
The gate says current claimed_solved and eligible; the supplied preflight
says present, no holds, related groups {}.

The complete selected private source record was available. Its problem
statement hashes to
`a5ce90b9c2087f20cd09cb33d9d92ca40039c19a08de3b1c098d10bf75b9179b`;
its declared review hash agrees with
`b667ba93b244f20bf9dd6b244af355c1b933340bb194c5a18a0d7c27d5ed9bb4`.
The entire private record hashes to
`5df3868e802d9da72bced3f4606c3ccd9b6610208bcc2a086bf25e082239b34f`.
Raw source bodies are excluded from this review's public allowlist.

I read the original author's R3_counterexample_candidate.md and reconstructed
the arguments below before reading any earlier audit judgment. Earlier
audit_a/audit_b judgments were not needed and remain unread in this family.
Input authentication is separately machine-readable in
INPUT_AUTHENTICATION.json. The parent authenticated the status-only immutable
head gate before distributing this task; I do not substitute a new mutable
head for that submitted object.

## 1. Compact smooth curve, connectedness, and genus

Use the affine chart
  y^2 = z^6 - 1.
It is smooth: simultaneous vanishing of partial derivatives would require
y = z = 0, which is not on the curve.

On the overlap z != 0 set s = 1/z and q = y/z^3. The equation becomes
  q^2 = 1 - s^6.
At s = 0 this has exactly two smooth points q = +1 and q = -1, each with
s as a coordinate. Glue this chart to the affine chart using the indicated
transition maps. This is the smooth compact completion, rather than the
possibly singular naive plane-projective closure.

The projection to the z-sphere is a double cover. It is proper/compact:
over bounded finite base charts the polynomial equation bounds y, and near
infinity the q chart bounds q. More formally it is a finite map to the
compact Riemann sphere with the two explicit infinity charts. There are six
simple branch points at the sixth roots of unity, and no branching at the
two infinity points.

Connectedness does not have to be assumed. A loop around any simple finite
root exchanges the two local sheets of the unbranched cover away from the
six branch values. Hence that covering, and then its branched completion,
is connected. Equivalently z^6-1 is not a square in C(z), since its simple
zeros have odd valuation.

The branched-cover Euler characteristic is
  chi(C) = 2 chi(S^2) - 6 = 4 - 6 = -2.
For the resulting connected closed oriented surface,
  2 - 2g = -2,
so g = 2. The complex charts give an orientation, and the construction has
no boundary.

## 2. Global one-forms and their zero sets

At a finite unbranched point, dz/y is holomorphic in the z coordinate.
At a branch point r, y is a valid coordinate because r != 0 and
the derivative with respect to z is nonzero. Differentiating the equation:
  2y dy = 6 z^5 dz,
so exactly
  dz/y = dy/(3 z^5).
This extends holomorphically and is nonzero there. Multiplication by z
preserves holomorphicity.

At infinity the two q branches are holomorphic and nonzero:
  eta_0 = dz/y = -(s/q) ds,
  eta_1 = z dz/y = -(1/q) ds.
Thus eta_0 has one simple zero at each infinity point and no poles;
eta_1 is nonzero at both infinity points. The two eta_1 zeros occur over
z = 0. These divisor counts agree with degree 2g-2 = 2 and furnish an
additional check.

If A eta_0 + B eta_1 is zero, then (A+Bz) eta_0 is zero on an affine
unbranched open set. Since z varies there and eta_0 is nonzero, A=B=0.
This proves complex linear independence without a dimension count.

Let E = mathbb C/(mathbb Z+i mathbb Z); this use of mathbb C must be
distinguished from the named genus-two curve C. Its globally defined
one-form theta=dw has no zeros. The product M=C x E is a smooth connected
compact boundaryless real four-manifold with product integrable J_0.

Omega_j=eta_j wedge theta are global holomorphic (2,0)-forms and are
complex linearly independent. They are closed directly: eta_j and theta
are holomorphic one-forms on complex curves and therefore closed, and
d respects the product wedge. Their real and imaginary parts are
J_0-anti-invariant by the (2,0)+(0,2) type identity.

## 3. Independent cohomology classes, without an elliptic assumption

Set alpha=Re Omega_0, beta=Im Omega_0, gamma=Re Omega_1.
Suppose a alpha+b beta+c gamma is exact for real a,b,c. Put
  Omega=(a-i b)Omega_0+c Omega_1.
Then that exact real form is F=Re Omega. In complex dimension two,
Omega wedge Omega = 0 and its conjugate square is zero, hence
  F wedge F = (1/2) Omega wedge conjugate(Omega).
In positively oriented holomorphic coordinates, if
Omega=h d zeta wedge d xi, then
  Omega wedge conjugate(Omega)=4 |h|^2
          du wedge dv wedge dx wedge dt.
Consequently F wedge F is nonnegative everywhere and positive wherever
Omega is nonzero.

Since F=d lambda and dF=0, compactness and absence of boundary give
  integral_M F wedge F = integral_M d(lambda wedge F) = 0.
It follows that Omega vanishes identically. On the affine region its
coefficient is (a-i b)+cz. The variable z is nonconstant, so c=0 and
a-i b=0, hence a=b=c=0. Thus [alpha],[beta],[gamma] are real linearly
independent in H^2_dR(M).

The same positivity/Stokes argument explains the identification of closed
anti-invariant forms with their de Rham classes on any compact oriented
four-manifold without boundary: choose a J-compatible metric. Every real
J-anti-invariant two-form kappa is self-dual, so
  kappa wedge kappa = |kappa|^2 vol_g.
An exact closed such form has integral square zero and is therefore zero.
Thus the natural map from closed anti-invariant forms to H^2 is injective.
In this example the stronger independent-class statement is already proved
directly, so ambiguity between dimensions of forms and classes cannot
invalidate the lower bound three.

This argument would require modification on a noncompact manifold or in
the presence of boundary. Those categories are not used.

## 4. Exact simultaneous local ratio chart

At the chosen curve point z=0,y=i, y is a nonzero holomorphic branch.
Choose a genuine local coordinate w near the zero point of E. On the
product set
  zeta=z,  xi=w/y(z).
The inverse is z=zeta, w=y(zeta)xi, so this is a holomorphic coordinate
system after shrinking. Its Jacobian is 1/y(z), nonzero. Moreover
  d zeta wedge d xi = dz wedge dw/y(z) = Omega_0,
because the other derivative term is proportional to dz and disappears
under the wedge. Also Omega_1=zeta Omega_0.

Writing zeta=u+i v and xi=x+i t gives
  alpha=du wedge dx-dv wedge dt,
  beta=du wedge dt+dv wedge dx,
  gamma=u alpha-v beta.
The coordinate orientation is precisely
  vol=du wedge dv wedge dx wedge dt.
Only this local chart is used for the meromorphic ratio z; no global
coordinate zeta, v, or x is required.

Choose a ball B whose closure lies in this chart, and explicitly interpret
the submitted cutoff as rho in C_c^infinity(B), equal to one near the
origin. This is a conventional cutoff choice already required by the
candidate, not a new proof mechanism.

## 5. Compact-support zero extension and exactness

Fix f=rho x^2/2 and R=epsilon f. Since the support K of rho is compactly
contained in B, there is an open collar of the boundary of B on which
rho and all of its derivatives vanish. Both R dv and Rv dv are smooth
one-forms supported in K, and extension by zero gives genuine global
smooth one-forms. All their jets match zero across the chart boundary.

Define the submitted global forms
  alpha_epsilon=alpha,
  beta_epsilon=beta+d(R dv),
  gamma_epsilon=gamma-d(Rv dv).
They are globally closed and their cohomology classes are exactly the
original ones, with no continuity or smallness requirement for this fact.

The exact local identity survives every cutoff derivative:
  d(Rv dv)=d(Rv) wedge dv
          =(v dR+R dv) wedge dv
          =v dR wedge dv
          =v d(R dv).
Therefore on all of B, including the transition annulus,
  gamma_epsilon=u alpha-v beta_epsilon.
This calculation uses no condition that rho be constant and contains no
omitted d rho term. All cutoff derivatives remain in the common dR wedge dv
factor.

## 6. Positive plane and its smooth almost-complex realization

The fully perturbed form, including all cutoff derivatives, is
  beta_epsilon=du wedge dt+(1-R_x)dv wedge dx
               -R_t dv wedge dt+R_u du wedge dv.
Direct wedge multiplication gives
  alpha^2=2vol,
  alpha wedge beta_epsilon=R_t vol,
  beta_epsilon^2=2(1-R_x)vol.
The R_v term vanishes identically in dR wedge dv; the R_u term is
present but cancels from these three wedge products.

Let s=R_t/2 and D=1-R_x-R_t^2/4. A single positive epsilon bound works
on the entire chart. For example put
  A=max(1, sup_B |f_x|),  T=max(1, sup_B |f_t|),
  epsilon_0=min(1/(4A),1/T).
For |epsilon|<=epsilon_0, |R_x|<=1/4 and |R_t|<=1, hence D>=1/2.
Both suprema are finite because f has compact support. This handles the
transition region, not merely the core where rho=1.

Now
  B_epsilon=(beta_epsilon-s alpha)/sqrt(D),
  Psi_epsilon=alpha+i B_epsilon
satisfy
  alpha wedge B_epsilon=0,
  B_epsilon^2=alpha^2,
  Psi_epsilon^2=0,
  Psi_epsilon wedge conjugate(Psi_epsilon)=4vol>0.
In particular alpha and beta_epsilon span a genuine positive rank-two
plane everywhere in B.

For clarity, the passage from Psi to J has no global topological
extension assumption. On each real tangent space, the nonzero complex
two-form Psi with Psi^2=0 has complex rank two and is decomposable.
Its contraction kernel K has complex dimension two. The nonzero wedge
Psi wedge conjugate(Psi) means K and conjugate(K) are complementary.
Declare the complexification of J to act by -i on K and +i on
conjugate(K). The two actions are exchanged by conjugation, so they define
a real endomorphism J with J^2=-Id. This convention makes Psi a (2,0)-form.

The constant rank kernel is a smooth subbundle because Psi is smooth and
has constant rank. Complementarity supplies a smooth real J. At epsilon=0,
Psi=Omega_0, so the same convention gives exactly J_0, not -J_0.
This also fixes the potential sign ambiguity in selecting a complex
structure from an unoriented real plane.

On the collar where R and all derivatives vanish, s=0,D=1 and
Psi=alpha+i beta=Omega_0. Thus the locally constructed J equals J_0 on
an open collar. Defining it to be J_0 outside B is a smooth global gluing,
with all derivatives matching.

## 7. Global anti-invariance, zero sets, and convergence

On B the forms alpha and B_epsilon are the real and imaginary parts of
a (2,0)-form. They are J_epsilon-anti-invariant. The linear expression
  beta_epsilon=s alpha+sqrt(D) B_epsilon
gives anti-invariance of beta_epsilon; the retained exact relation then
gives anti-invariance of gamma_epsilon. Outside B the three forms equal
their original J_0-anti-invariant forms, and J_epsilon=J_0. Thus they
are anti-invariant everywhere. Their three independent unchanged classes
give h^-_{J_epsilon}>=3.

Omega_0 vanishes on the two infinity fibers {p_+,p_-} x E, well away
from the chosen ball. Nothing in the construction uses its positive plane
there: J is already J_0. The original anti-invariance type argument
remains valid even for a zero form. The third form is nonzero on those
fibers. A proof need not extend the locally chosen rank-two span across
the zeros.

At zeta=0, gamma_epsilon vanishes. These are codimension-two zero sets,
not open subsets, so they create no unique-continuation conflict.

For convergence, R=epsilon f with one fixed compactly supported smooth f.
For every finite m, its derivatives up to order m are O_m(|epsilon|).
The uniform bound D>=1/2 controls the denominators in every derivative
of sqrt(D), 1/sqrt(D), and therefore Psi_epsilon-Psi_0. The algebraic
map from the complementary kernel planes to J is smooth near J_0;
using the compact closure of the ball gives
  ||J_epsilon-J_0||_{C^m} <= C_m |epsilon|
for each finite m, after possibly shrinking a common fixed positive
epsilon interval. Outside B the difference is exactly zero. This is
C-infinity convergence. No bound uniform in m is needed for this
topology, and no analyticity of the cutoff is claimed.

## 8. Local nonintegrability cross-check

On the core rho=1, put k=1-epsilon x. The chosen epsilon bound gives k>0
there, and the submitted form factors as
  Psi=(du+i sqrt(k)dv) wedge (dx+i k^(-1/2)dt).
Consequently
  J partial_u=k^(-1/2)partial_v,
  J partial_v=-sqrt(k)partial_u,
  J partial_x=sqrt(k)partial_t,
  J partial_t=-k^(-1/2)partial_x.

For the convention
  N(X,Y)=[JX,JY]-J[JX,Y]-J[X,JY]-[X,Y],
let a=k^(-1/2). Then
  [J partial_u, partial_x]=-a' partial_v,
while the other three bracket contributions for X=partial_u,
Y=partial_x vanish. Hence
  N(partial_u,partial_x)=-a' sqrt(k) partial_u
                       =k'/(2k) partial_u.
At the origin k=1 and k'=-epsilon, so this is
  -epsilon/2 partial_u,
nonzero for every nonzero epsilon. This agrees with the candidate's
claimed convention and exhibits a local obstruction, sufficient for the
global J to be nonintegrable. No global continuation theorem makes
integrability on the exterior force integrability through a smooth bump.

## 9. Attempted falsifiers and boundary cases

- **Infinity singularity or missing branch:** explicit (s,q) charts show
  two smooth unbranched points; all six finite roots are simple.
- **Disconnected cover:** one simple-root monodromy exchanges the sheets.
- **Poles or dependent global differentials:** exact branch/infinity
  expansions and the nonconstant ratio z exclude them.
- **Exact-class or harmonic-collapse problem:** direct positive-square
  Stokes argument excludes any nonzero exact linear combination.
- **Cutoff derivatives destroy the third relation:** all derivatives
  enter dR wedge dv, and d(Rv dv)=v d(R dv) identically.
- **Only core positivity checked:** the explicit epsilon bound controls
  f_x and f_t on the full compact support, including the transition.
- **No real J or wrong sign:** complementary conjugate kernels give a real
  J with J^2=-Id; equality to J_0 at epsilon=0 fixes the sign.
- **Boundary/collar mismatch:** compact support provides an open equality
  collar and matching jets, not only pointwise equality at the boundary.
- **Zeros outside B obstruct the plane:** the plane is used only on B;
  the untouched J_0 supplies the structure everywhere else.
- **Unique continuation forces the perturbation to vanish:** a difference
  such as beta_epsilon-beta is exact and supported in B, but beta need
  not be J_epsilon-anti-invariant there. The difference is not a closed
  anti-invariant form for one fixed J; harmonic unique continuation
  therefore does not apply. None of the three nonzero retained forms
  vanishes on an open set.
- **Topological positive-dimension bound:** by Kunneth,
  b_2(C x E)=1+1+(4)(2)=10. Its intersection form has signature (5,5):
  the two factor H^2 classes form one hyperbolic plane, and the tensor
  H^1(C) x H^1(E) portion has signature (4,4). Thus a positive
  three-dimensional cohomology subspace is topologically allowed.
- **Limit epsilon=0:** all corrections vanish, J=J_0, and the Nijenhuis
  component vanishes as expected. Only epsilon!=0 is claimed to refute
  an integrability implication.
- **Noncompact, boundary, fixed-metric, symplectic, analytic categories:**
  none is silently inferred. Compactness/no boundary are explicitly used
  in the cohomological injection argument; the example satisfies them.

No unproved equivalent claim replaces the central global construction.
The direct reconstruction supplies proofs rather than relying on finite
local scripts or on earlier acceptance judgments. No external individual,
other shard, branch, index, head, original file, or source catalog was
changed by this review.
