# Independent local differential geometry audit of PR948

Original target head: be4313efafa1af5962394e07d8a4debff2e94d92.  
Problem: 30004549 / OWR-2654829-012.  
Family: local exterior algebra, real endomorphism reconstruction, and coordinate
Nijenhuis calculation. Verdict: LOCAL_MECHANISM_VERIFIED.

This verdict is restricted to the submitted local deformation and its gluing.
It does not adjudicate the global compact curve or cohomological independence,
the exact historical source scope, priority, author history, publication
readiness, or the full target. No new construction or central repair is
supplied. This is verification, adding zero proof-search author responses.

## Provenance, actual order, and independence

The root's scope gate and byte-preserved snapshot preceded delegation. My
actual order was: complete source/charter/candidate reading first; preliminary
mental inspection second; own direct Git/disk authentication at
2026-10-16T06:46:40.518432Z third; independent executable reconstruction at
2026-10-16T06:49:45.253233Z fourth. Thus my own authentication did NOT precede
the initial mathematical reading. This procedural ordering exception is
recorded explicitly rather than being replaced by the root's earlier gate.

My read-only authentication independently checked all 24 original files:
each tree mode is 100644, each Git blob and byte count matches the root record,
and Git-object bytes equal preserved disk bytes with the declared SHA-256.
The selected statement SHA-256 is
a5ce90b9c2087f20cd09cb33d9d92ca40039c19a08de3b1c098d10bf75b9179b.
The selected private record carries review hash
b667ba93b244f20bf9dd6b244af355c1b933340bb194c5a18a0d7c27d5ed9bb4.
That carried review hash is not a fresh independent reconstruction of the
root's native-source review-hash algorithm. The root's source-identity gate
covers that separate concern. No original-content drift was found.

The submitted candidate has SHA-256
50a267656e6a5412a2e14208ada5aec203df4c5385be63b831029188cb1cf39e.
I did not read the original audit_a/audit_b judgments or scripts, nor the
author's verification script; reading their bytes for hashing supplied no
mathematical content. The executable check here was written independently.
The main independent algebraic mechanism is an explicit real 4-by-4 matrix
reconstruction of J, including the cutoff term R_u, followed by direct
differentiation of all six coordinate Nijenhuis pairs. Exterior forms and a
mixed-type annihilator bracket furnish cross-checks.

## Exact claim and local inputs

Assume the global product complex surface and its three closed real forms
exist as stated. In a holomorphic coordinate ball, write
zeta=u+iv, xi=x+it and take orientation

    V = du ∧ dv ∧ dx ∧ dt.

The local inputs are

    alpha = du ∧ dx - dv ∧ dt,
    beta  = du ∧ dt + dv ∧ dx,
    gamma = u alpha - v beta.

For a fixed smooth compactly supported real cutoff rho, equal to 1 near the
origin, set R=epsilon rho x^2/2 and define the submitted global exact changes

    beta_R = beta + d(R dv),
    gamma_R = gamma - d(R v dv).

The local success criterion is a smooth real almost-complex J_R, equal to the
product structure near the patch boundary, for which these three forms are
anti-invariant and which has nonzero Nijenhuis tensor for all sufficiently
small nonzero epsilon. The equations below prove this criterion for the
complete submitted formulas.

## Simultaneous holomorphic coordinates and orientation

At the specified curve point z=0,y=i, the curve equation has a holomorphic
solution y(z) with y(0) nonzero. The change

    zeta=z,  xi=w/y(z)

has complex Jacobian determinant 1/y(z), hence is locally invertible. Since

    dxi = dw/y - w y'(z) dz/y^2,

wedging with dz kills the second term. Thus

    dzeta ∧ dxi = (dz/y) ∧ dw,
    zeta dzeta ∧ dxi = z (dz/y) ∧ dw.

Both normal forms hold in the same coordinates. Their real and imaginary
parts give exactly the three displayed real forms, including the minus sign
in gamma=u alpha-v beta. A holomorphic invertible coordinate change preserves
real complex orientation: its real determinant is the positive number
|1/y|^2. Therefore V has the claimed complex orientation.

Directly,

    du ∧ alpha - dv ∧ beta = 0,

so d gamma=0. The relation uses neither an approximation nor the assumption
that R is independent of u,v,t.

## Exact cutoff calculation and preserved relation

Write a=R_u, b=R_x, c=R_t. With no specialization of R,

    d(R dv) = a du∧dv - b dv∧dx - c dv∧dt.

The R_v term vanishes because dv∧dv=0. For the actual cutoff,

    a = epsilon x^2 rho_u/2,
    b = epsilon (rho x + x^2 rho_x/2),
    c = epsilon x^2 rho_t/2.

These derivatives include the transition region. The product rule gives

    d(R v dv) = v dR∧dv + R dv∧dv = v d(R dv).

Consequently the exact pointwise relation is

    gamma_R = u alpha - v beta_R

everywhere in the ball. Both new forms are closed because their changes are
global exact forms. The one-forms being differentiated have compact support
inside the chart and extend smoothly by zero. Thus there is no hidden
boundary derivative. Their de Rham classes are unchanged. These statements
are conditional only on the original global forms, not on any global
independence argument.

Three globally independent forms or classes need not have three independent
values at a point. The retained relation places their values in a real plane;
this is consistent with three independent cohomology classes.

## Positivity, including the complete transition region

The perturbed form is

    beta_R = du∧dt + (1-b) dv∧dx - c dv∧dt + a du∧dv.

Direct wedge multiplication gives

    alpha^2 = 2V,
    alpha ∧ beta_R = cV,
    beta_R^2 = 2(1-b)V.

The absence of a in this Gram matrix does not permit dropping a from the form
or from J. For arbitrary real l,m,

    (l alpha + m beta_R)^2
      = 2[(l+cm/2)^2 + D m^2] V,
    D = 1-b-c^2/4.

Thus D>0 is precisely the required positive definiteness. Since rho is fixed
and compactly supported, b and c are uniformly O(epsilon) on the full patch.
The submitted sufficient conditions |b|<=1/4, |c|<=1 give D>=1/2. A common
nonzero epsilon interval satisfying these conditions exists because the
respective coefficient functions are bounded. This is a uniform proof, not
a numerical sample or an inference from assertion checks.

With h=sqrt(D)>0 define

    B = (beta_R - c alpha/2)/h,
    Psi = alpha + iB.

Then alpha∧B=0, B^2=alpha^2, and

    Psi^2=0,  Psi∧conjugate(Psi)=4V.

The boundary D=0 is excluded: there the Gram form degenerates and the square
root construction cannot be used. The chosen epsilon interval stays a fixed
positive distance from that boundary.

## Real almost-complex realization: explicit matrix and kernel proof

A nonzero complex two-form in complex dimension four with square zero has
skew rank two: the rank is even; rank four would have nonzero Pfaffian and
nonzero square. It is therefore decomposable. Its kernel K has complex
dimension two. If a vector lies in both K and conjugate(K), its contraction
with Psi∧conjugate(Psi) vanishes. Contraction into a nonzero top form is
injective, so that vector is zero. Hence K and conjugate(K) are complementary.

Declaring J=-i on K and J=+i on conjugate(K) defines a unique real J for this
chosen complex line Psi, with J^2=-Id. Complex conjugation exchanges the two
summands, so the endomorphism is real. The constant-rank kernel is smooth.
The ordered choice Psi=alpha+iB and the positive square root select the
structure agreeing with J_0; an unoriented real plane alone would leave a
J versus -J choice. The submitted construction contains the needed choice.

For an independent reconstruction, represent alpha and B by real skew
matrices A and Bmat in coordinate order (u,v,x,t), and set

    J = -A^{-1} Bmat
      = (1/h) [ c/2   b-1    0       0
                1    -c/2   0       0
                0    -a     c/2    -1
               -a     0     1-b    -c/2 ].

Here A^2=-Id. Direct matrix multiplication, before imposing h^2=D, gives

    J^2 = -(D/h^2) Id,
    J^T A = -Bmat,
    J^T Bmat = (D/h^2) A.

After h^2=D these imply both J^2=-Id and

    Psi(JX,Y)=i Psi(X,Y).

Thus the real matrix supplies exactly the kernel-defined J, and

    J^T A J = -A,  J^T Bmat J = -Bmat.

Alpha and B, and therefore beta_R, are anti-invariant. The exact third-form
relation proves anti-invariance of gamma_R. The matrix also makes the
smoothness, the a dependence, and the sign choice explicit. These are
expanded verifications of the submitted realization, not additional repairs.

## Gluing, zeros elsewhere, and the full smooth limit

Compact support of rho inside B gives a collar of the boundary where all
derivatives of R vanish. On that collar a=b=c=0, h=1, B=beta and Psi is the
original dzeta∧dxi. The constructed J is J_0 there, so defining J=J_0 outside
B glues smoothly. Away from B the three forms are the original
anti-invariant forms. Possible zeros of Omega_0 elsewhere do not enter the
local construction or its denominators; J there is simply J_0.

On the fixed closed chart region, (a,b,c) depend linearly on epsilon and
D>=1/2 holds on a common epsilon interval. The displayed real matrix is a
smooth function of these quantities and of the positive square root. Every
coordinate derivative therefore converges uniformly to its epsilon=0 value.
For each fixed derivative order the difference is O(|epsilon|), with an
order-dependent constant determined by the fixed cutoff. Outside the patch
the difference is zero. This proves J_epsilon -> J_0 in the full C-infinity
topology, with epsilon=0 giving J_0 exactly. It does not require a cutoff
whose derivatives are uniformly bounded over all possible choices of cutoff.

## Nonintegrability in three consistent calculations

Near the origin rho=1. Set k=1-epsilon x>0, so a=c=0, b=epsilon x.
The explicit matrix reduces to

    J partial_u = k^(-1/2) partial_v,
    J partial_v = -k^(1/2) partial_u,
    J partial_x = k^(1/2) partial_t,
    J partial_t = -k^(-1/2) partial_x.

Here the notation means the corresponding coordinate vector fields. In
particular, at x=0 the value of J is J_0, while its first derivative changes.

First, a coframe with pullback eigenvalue i is

    phi_1=du+i sqrt(k)dv,  phi_2=dx+i k^(-1/2)dt,

and its wedge equals the submitted Psi. Since k'=-epsilon,

    d phi_1 = i k'/(2 sqrt(k)) dx∧dv,
    d phi_1∧phi_1∧phi_2 = k'/(2k) V.

This last form is nonzero for nonzero epsilon. In holomorphic coordinates the
exterior derivative of any (1,0)-form has no (0,2) component. Wedging with a
(2,0)-form in complex dimension two would consequently vanish. This necessary
integrability condition fails.

Second, use the submitted convention

    N(X,Y)=[JX,JY]-J[JX,Y]-J[X,JY]-[X,Y].

The direct coordinate formula used in the independent executable check is

    N^i_jl = J^p_j partial_p J^i_l - J^p_l partial_p J^i_j
             - J^i_p partial_j J^p_l + J^i_p partial_l J^p_j.

It gives

    N(partial_u,partial_x) = -epsilon/(2k) partial_u,

hence at the origin -epsilon/2 partial_u, exactly as submitted. All six
coordinate pairs were computed; the nonzero remaining pairs are

    N(partial_u,partial_t) = epsilon/(2k^2) partial_v,
    N(partial_v,partial_x) = epsilon/(2k) partial_v,
    N(partial_v,partial_t) = epsilon/(2k) partial_u.

The (u,v) and (x,t) pairs vanish. All components vanish at epsilon=0.

Third, an annihilator basis is

    Zbar_1=partial_u+i k^(-1/2)partial_v,
    Zbar_2=partial_x+i sqrt(k)partial_t.

If Z_1 is the conjugate of Zbar_1, then

    [Zbar_1,Zbar_2] = k'/(4k) (Zbar_1-Z_1).

The nonzero Z_1 component shows that the kernel distribution is not
involutive for epsilon nonzero. This independently catches the possible
coframe/kernel conjugation convention error. All three tests agree.

## Adversarial controls, exact remaining gap, and evidence limits

The exact program checks 33 identities and controls with explicit exceptions,
in ordinary Python and optimized Python, using SymPy 1.14.0. Checks are not
disabled by optimization. The program uses an arbitrary function R of all
four coordinates for the cutoff-region identities; it does not test only the
constant-cutoff neighborhood.

The wrong-sign mutation gamma+d(R v dv) breaks the exact third-form relation.
At a concrete admissible algebraic jet with q=d(R dv)=-dv∧dx/4 and u=v=1,
the three form values alpha, beta+q, gamma+v q have rank three. Therefore they
cannot all lie in a real anti-invariant plane at that point.

The omitted-cutoff-derivative mutation
beta+epsilon rho x dx∧dv has derivative
epsilon x d rho∧dx∧dv, generically nonzero in the transition region. This
control demonstrates why checking rho=1 alone would be insufficient. The
submitted formula includes the omitted terms and is closed.

Strongest verified result: the complete submitted local formulas produce a
smooth real J, matching J_0 near the boundary, preserving the closed local
three-form relation, with nonzero N at the origin for every sufficiently
small nonzero epsilon and full smooth convergence to J_0. No local
mathematical gap or central repair was found.

Exact remaining gap for this family: none within local geometry. The full
global h_J^- conclusion additionally depends on the separately audited
existence and cohomological independence of the input global forms, and
historical/source/priority conclusions remain wholly outside this verdict.
The symbolic checks verify finite algebra and differentiation identities;
the uniform, smoothness, kernel, and gluing claims are justified by the
proofs above rather than inferred from passing code.

All work stayed in this family folder. No branch, index, ref, canonical
source, original file, goal, service record, or external communication was
modified. Temporary write failures were reported honestly; no other agent's
or frozen files were removed. Checkpoint publication is delegated to the
root, as this child was expressly prohibited from changing index/HEAD/refs.
