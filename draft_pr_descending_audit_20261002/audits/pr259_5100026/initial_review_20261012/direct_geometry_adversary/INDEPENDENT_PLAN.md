# Independent direct geometry freeze

Frozen 2026-10-12 11:39:06 UTC; audit completion estimate 10%.

Identity: PR259, original head 0524ed734ee8185681d030af98088259134a6af7,
target 5100026 / k407. Root assigned this direct Cartesian family.
Before this freeze I read only the supplied assignment, applicable AGENTS.md,
the input file inventory, and submitted SOURCE_GATE.md, SOURCES.md, metadata.json,
README.md. I have not read PROOF.md, submitted verification code, old review
verdicts, another new family's derivations, or the root research log.
The first overbroad file inventory printed many unrelated file *names*, no
contents; later searches were confined to this audit.

## Hypothesis and scope

E: x^2/a^2+y^2/b^2=1, a>b>0; original focus M=(sqrt(a^2-b^2),0).
Caustic x^2/(a^2-lambda)+y^2/(b^2-lambda)=1 with 0<lambda<b^2.
P_i form an actual specular billiard trajectory of primitive even least period
N>=4, allowing coprime star winding 1<=p<N/2. Tangents to E at P_i,P_{i+1}
intersect at R_i. At R_i construct the line perpendicular to R_i-M.
Consecutive such lines intersect at U_i; desired centroid is sum U_i/N.
Hypotheses to test: all real U_i are finite; centroid independent of phase,
on the focal axis, negative x for M positive when N>4; N=4 mean zero.
An even-length repeated list of an odd least-period orbit will be tested
separately because source wording may not explicitly impose primitiveness.
The circular and separatrix/degenerate limits will be distinguished from scope.

## Cartesian derivation before reading submitted proof

Write P(theta)=(a cos(theta),b sin(theta)),
g^2=a^2 sin(theta)^2+b^2 cos(theta)^2. The positively oriented unit tangent
is T=(-a sin(theta),b cos(theta))/g and unit outward normal is
H=(b cos(theta),a sin(theta))/g.
For a unit line direction d, unit line normal n=(-d_y,d_x) and line height
h=n dot P, confocal tangency is
lambda=a^2 n_x^2+b^2 n_y^2-h^2
=(a d_y sin(theta)+b d_x cos(theta))^2.
Hence the outgoing forward ray tangent to this caustic is
d=sqrt(1-lambda/g^2) T - sqrt(lambda)/g H.
Its second boundary intersection is Q=P+s d, where
s=-2(P_x d_x/a^2+P_y d_y/b^2)/(d_x^2/a^2+d_y^2/b^2).
The incoming ray must reflect by d_new=d-2(d dot H_Q)H_Q;
I will use physical reflection propagation independently of constant-caustic
step generation and compare them.

The actual ellipse tangent at P is (P_x/a^2,P_y/b^2) dot X=1.
Solve the two consecutive equations to obtain R.
The constructed normal line is (R-M) dot U=|R|^2-M dot R.
Solve consecutive equations for U. Determinants are explicit diagnostics;
no elliptic parametrization or imported verifier will be used initially.

## Exact four-period control

a=5,b=3,c=4, lambda=a^2 b^2/(a^2+b^2)=225/34.
P=(5,0),(0,3),(-5,0),(0,-3) obey specular reflection and have least period 4.
R=(5,3),(-5,3),(-5,-3),(5,-3).
U=(-4,6),(-6,0),(-4,-6),(14,0). Their arithmetic mean is (0,0).
All values are rational, and the line tangency identity certifies the same
strict nested elliptical caustic. This is a checkable control, not a proof
for every four-period orbit.

## Controls and falsification plan

Use mpmath high precision, bisection of physical ray-traced total boundary
angle after N steps to achieve p turns, and freeze caustic parameters before
varying phase. Test aspect ratios near the circle and elongated, many least
even periods, coprime stars, both focus signs and both orbit orientations.
Record boundary, reflection, caustic, closure, determinant, centroid-phase
and symmetry residuals. Recompute challenging cases at 120+ digits to detect
conditioning rather than treating float precision as proof.
Derive at least one exact odd triangle using a rational ellipse/focus if
possible, then repeat it twice and check the even-list extension.
After this freeze read every submitted proof step and relevant source definitions,
test all hidden assumptions, complete singularity/limiting-case audit, and
report strongest verified result plus exact remaining gap. Numerics alone
cannot certify universal phase invariance or finiteness.

## Reproducibility and restrictions

All scripts, outputs, receipts and reports stay in this dedicated family folder.
No contacts with individuals, no Git/index/refs or shared branch changes,
no provider writes. Root owns publication/review decisions. No priority or
novelty verdict is attempted here. Primary-source locators/hashes only in
public artifact selection; no copied full copyrighted sources.
