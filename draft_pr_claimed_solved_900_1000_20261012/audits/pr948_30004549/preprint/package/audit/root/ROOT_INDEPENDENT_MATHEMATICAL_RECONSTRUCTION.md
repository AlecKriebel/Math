# Root reconstruction of the submitted PR948 construction

Recorded 2026-10-16, before consulting the submitted audit A/B verdicts.
This reconstructs the complete saved author candidate; it is verification,
not an additional author proof response. The controller authenticated the
current PR identity and exact `claimed_solved` row before source intake.
The original snapshot was authenticated before delegation; the later full
root reauthentication and native history receipt is timestamped separately.
Independent family results are not a substitute for the reasoning below.
This is a preliminary mathematical check, not a priority certificate.

## Global starting data

The affine curve y²=z⁶−1 is nonsingular: at y=0 a root r has
6r⁵≠0. Completing its degree-two map to CP¹ gives six simple finite branch
points. At infinity let s=1/z and Y=y/z³; then Y²=1−s⁶ and Y=±1 at s=0,
so there are two smooth unbranched points. The cover is connected because
z⁶−1 is not a rational square. Riemann–Hurwitz gives 2g−2=−4+6=2.
At a finite branch point a local square-root coordinate makes dz/y regular
and nonzero; at infinity dz/y=−s ds/Y and z dz/y=−ds/Y. Thus eta0=dz/y
and eta1=z dz/y are global independent holomorphic one-forms.

On M=C×E, E=C/(Z+iZ), Omega0=eta0∧dw and Omega1=eta1∧dw are global
closed holomorphic two-forms. Alpha=Re Omega0, beta=Im Omega0, and
gamma=Re Omega1 have independent real de Rham classes. Indeed, a real
combination is Re Omega, Omega=((a−ib)+cz)Omega0. If this real form were
exact, Stokes would give integral (Re Omega)²=0, whereas
(Re Omega)²=(Omega∧conjugate(Omega))/2 is nonnegative and positive on an
open set for every nonzero Omega. Therefore Omega=0; independence of
Omega0,Omega1 implies a=b=c=0. This verifies the candidate's harmonic
argument without needing a chosen metric. No exact value of h minus follows.

## Simultaneous coordinates and exact perturbation

Near z=0,y=i,w=0, set zeta=z and xi=w/y(z). The holomorphic Jacobian
is 1/y≠0. The term w d(1/y) disappears after wedging with dz, hence
Omega0=d zeta∧d xi and Omega1=zeta Omega0. With zeta=u+iv, xi=x+it,

    alpha=du∧dx−dv∧dt,
    beta=du∧dt+dv∧dx,
    gamma=u alpha−v beta.

Fix a relatively compact coordinate ball and a smooth rho supported
strictly inside it and equal to one near the origin. R=epsilon rho x²/2
has support strictly inside the chart. Both R dv and Rv dv extend by zero
as smooth global one-forms. Consequently beta_e=beta+d(R dv) and
gamma_e=gamma−d(Rv dv), together with alpha, are global closed forms in
the same independent cohomology classes. Since d(Rv dv)=v d(R dv),
gamma_e=u alpha−v beta_e holds exactly through the entire cutoff region.
This identity, rather than mere smallness, retains three forms in one plane.

## Positive plane and real almost-complex structure

For vol=du∧dv∧dx∧dt, the complete expression is

    beta_e=du∧dt+(1−R_x)dv∧dx−R_t dv∧dt+R_u du∧dv.

Direct wedging gives alpha²=2vol, alpha∧beta_e=R_t vol,
beta_e²=2(1−R_x)vol. With s=R_t/2 and D=1−R_x−R_t²/4, define
B=(beta_e−s alpha)/sqrt(D). Then alpha∧B=0 and B²=alpha².
The R_u term is present in beta_e even though it drops from these wedges.
Writing f=rho x²/2, bounded f_x,f_t on the fixed compact support give a
uniform nonzero epsilon interval with |epsilon f_x|≤1/4 and
|epsilon f_t|≤1, hence D≥1/2. At epsilon=0 the original plane is recovered.

Psi=alpha+iB satisfies Psi²=0 and Psi∧conjugate(Psi)=4vol. A nonzero
alternating two-form on a four-dimensional complex vector space with
square zero has rank two; equivalently it is decomposable. Its contraction
kernel K is two-dimensional. The nonzero wedge with its conjugate implies
K∩conjugate(K)=0. Declaring K=T^(0,1) therefore defines a real J with
J²=−Id, smoothly since the rank is constant. Psi has type (2,0), so its
real and imaginary parts span Lambda_J^- and alpha,beta_e,gamma_e are
anti-invariant. On a collar of the ball R and all its derivatives vanish,
so Psi=Omega0 and J=J0. Setting J=J0 outside the ball glues smoothly.
Zeros of Omega0 elsewhere never enter this construction. Uniform D≥1/2
and compact support show J_e→J0 in every finite derivative norm, hence
in the C-infinity topology. No fixed metric or symplectic form is asserted.

## Nonintegrability, conventions, and falsifiers

Where rho=1, k=1−epsilon x and

    Psi=(du+i sqrt(k)dv)∧(dx+i k^(-1/2)dt).

For phi1=du+i sqrt(k)dv, phi2=dx+i k^(-1/2)dt,
d phi1∧phi1∧phi2=(k'/(2k))vol. This is nonzero when epsilon≠0,
whereas an integrable J has no (0,2) component in d phi1.
Equivalently J du-vector=k^(-1/2)dv-vector,
J dv-vector=−sqrt(k)du-vector, J dx-vector=sqrt(k)dt-vector,
J dt-vector=−k^(-1/2)dx-vector. The convention
N(X,Y)=[JX,JY]−J[JX,Y]−J[X,JY]−[X,Y] gives
N(partial_u,partial_x)=k'/(2k)partial_u, equal to −epsilon/2 partial_u
at the origin. Other common tensor normalizations do not change nonvanishing.

The epsilon=0 limit is integrable as required. Wrong sign on the gamma
correction destroys its exact plane relation. Omitting derivatives of rho
invalidates the transition-region closedness argument. Closedness of Psi
is neither claimed nor needed: alpha and beta_e are closed, whereas the
pointwise normalization B need not be. This last distinction avoids a
false inference from the local decomposable form to integrability.

Strongest preliminary conclusion: the submitted construction supplies
smooth nonintegrable structures on the specified closed connected M with
at least three independent closed anti-invariant classes, assuming the
source scope is as stated. Computation-family completion, an independent
cross-cutting adversary, primary-source scope verification and priority
audit remain required before promotion. No claim of first priority or
continued openness is established here.
