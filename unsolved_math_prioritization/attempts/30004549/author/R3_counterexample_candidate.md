# R3: A compactly supported three-form deformation candidate

Problem 30004549 / OWR-2654829-012. Date: 2026-10-07.
Status: FULL-TARGET COUNTEREXAMPLE CANDIDATE, AUTHOR-ONLY, NOT INDEPENDENTLY AUDITED.
This is a separately directed third resumed author turn. The inherited author count remains unknown. No publication or final acceptance is asserted. The intended target is the integrability clause h_J^- >= 3 implies J integrable, for smooth closed connected almost-complex four-manifolds. The generic-vanishing clause is a known prior theorem.

## Claimed result

There is a smooth closed connected four-manifold M and a nonintegrable almost-complex structure J on M with at least three linearly independent closed J-anti-invariant real two-forms. In fact J may be chosen arbitrarily C-infinity close to a product complex structure and to equal it outside a coordinate ball; the three retained forms stay in fixed linearly independent de Rham classes.

No novelty claim is made. The argument must receive a fresh independent audit, especially the positive-plane realization, compactly supported patching, and the simultaneous third-form relation.

## 1. Explicit compact starting surface and three classes

Let C be the compact smooth hyperelliptic curve obtained by completing

y^2=z^6-1.

The polynomial has six distinct roots. Its compact double cover of CP^1 is connected and has genus two, by Riemann-Hurwitz (six simple branch points). The differentials

eta_0=dz/y,     eta_1=z dz/y

extend holomorphically over C and are linearly independent. For example, at finite branch points z-r=t^2, dz/y is a nonzero holomorphic multiple of dt. At each of the two points over infinity, s=1/z gives dz/y a nonzero holomorphic multiple of s ds, and z dz/y a nonzero holomorphic multiple of ds. Thus neither has a pole.

Let T=C/(Z+iZ) be an elliptic curve and theta=dw its nowhere-zero holomorphic one-form. Let M=C times T, with product complex structure J_0. Define global holomorphic two-forms

Omega_0=eta_0 wedge theta,     Omega_1=eta_1 wedge theta,

and real closed forms

alpha=Re Omega_0,     beta=Im Omega_0,     gamma=Re Omega_1.

These are J_0-anti-invariant and their de Rham classes are real linearly independent. For completeness, fix any product Kähler metric. Holomorphic two-forms are closed; their real and imaginary parts are self-dual and harmonic. A linear combination c_1 alpha+c_2 beta+c_3 gamma that is exact must consequently vanish. It is the real part of (c_1-i c_2)Omega_0+c_3 Omega_1. A (2,0)-form with zero real part vanishes (compare its distinct (2,0) and (0,2) components). Independence of Omega_0,Omega_1 then gives c_1=c_2=c_3=0.

## 2. Exact local normal form

Choose the point z=0,y=i on C and w=0 on T. Work on a small product chart where y=y(z) is holomorphic and nonzero and w is an honest coordinate. Set

zeta=z,     xi=w/y(z).

These are holomorphic coordinates since the coordinate Jacobian has nonzero determinant 1/y(z). Direct differentiation gives

Omega_0=d zeta wedge d xi,     Omega_1=zeta d zeta wedge d xi.

Write zeta=u+i v and xi=x+i t. In the rest of this proof t is a real coordinate, not a deformation parameter. Then

alpha=du wedge dx-dv wedge dt,
beta=du wedge dt+dv wedge dx,
gamma=u alpha-v beta.                                                        (1)

In particular du wedge alpha-dv wedge beta=0, which is precisely why gamma is closed. Take a relatively compact coordinate ball B around the origin and a smooth real cutoff rho supported in B, equal to one on a smaller neighborhood of the origin.

## 3. Global exact perturbations preserving three closed forms

For a sufficiently small nonzero real epsilon set

R=epsilon rho x^2/2

on B. The one-forms R dv and R v dv have compact support in B and therefore extend smoothly by zero to all of M. Define globally

alpha_epsilon=alpha,
beta_epsilon=beta+d(R dv),
gamma_epsilon=gamma-d(R v dv).                                                (2)

All three forms are closed. Their cohomology classes equal [alpha],[beta],[gamma], so remain linearly independent without any continuity argument. On B, since d(v dv)=0,

d(R v dv)=v d(R dv),

and hence (1) becomes the exact pointwise identity

gamma_epsilon=u alpha-v beta_epsilon.                                       (3)

Thus the three forms still lie in a single real two-plane at every point of the perturbed region. There is no modification of the forms outside B.

## 4. Positivity and realization by an almost-complex structure

Put vol=du wedge dv wedge dx wedge dt, the complex orientation volume in this chart. Set R_u=partial_u R, R_x=partial_x R, R_t=partial_t R. The R_v term disappears when wedged with dv. Explicitly,

beta_epsilon=du wedge dt+(1-R_x)dv wedge dx-R_t dv wedge dt+R_u du wedge dv.

A direct exterior-algebra calculation gives

alpha^2=2 vol,
alpha wedge beta_epsilon=R_t vol,
beta_epsilon^2=2(1-R_x) vol.                                                  (4)

Define

s=R_t/2,     D=1-R_x-R_t^2/4.

For all sufficiently small epsilon, D>0 everywhere in B: R_x and R_t are uniformly O(epsilon) because rho is fixed with compact support. For instance it is sufficient that |R_x|<=1/4 and |R_t|<=1. These inequalities are achieved by taking |epsilon| small enough, and then D>=1/2.

Now set

B_epsilon=(beta_epsilon-s alpha)/sqrt(D),
Psi_epsilon=alpha+i B_epsilon.                                               (5)

Equations (4) imply alpha wedge B_epsilon=0 and B_epsilon^2=alpha^2. Therefore

Psi_epsilon wedge Psi_epsilon=0,
Psi_epsilon wedge conjugate(Psi_epsilon)=2 alpha^2=4 vol>0.                   (6)

A nonzero decomposable complex two-form satisfying the second condition defines an almost-complex structure by declaring

T^{0,1}_{J_epsilon}={Z in TM tensor C : contraction_Z Psi_epsilon=0}.

Indeed a nonzero two-form in complex dimension four with square zero has rank two and is decomposable; its kernel is complex two-dimensional. The nonzero product with its conjugate says that the two kernel planes are complementary, which gives a real almost-complex structure. Smooth dependence follows from the smooth rank-two kernel subbundle. Equivalently, Psi_epsilon is a local nowhere-zero (2,0)-form for this J_epsilon.

Where R=0 on a collar of the boundary of B, one has s=0, D=1, B_epsilon=beta, and Psi_epsilon=Omega_0. Thus the just-defined J_epsilon equals J_0 on that collar. Set J_epsilon=J_0 outside B. This defines a smooth almost-complex structure on the entire closed connected M. For small epsilon it is arbitrarily close to J_0 in any prescribed finite smooth norm; as epsilon tends to zero it converges to J_0 in the full C-infinity topology.

On B, alpha and beta_epsilon are real linear combinations of the real and imaginary parts of Psi_epsilon, so are J_epsilon-anti-invariant; (3) proves the same for gamma_epsilon. Outside B the three forms agree with the original J_0-anti-invariant forms. Consequently all three global closed forms in (2) are J_epsilon-anti-invariant. Their independent cohomology classes show

h_{J_epsilon}^- >= 3.                                                       (7)

The fact that Omega_0 vanishes on some other fibers causes no patching issue: J_epsilon is defined there to be the original J_0. The positive-plane construction is used only inside B, where Omega_0 is nowhere zero.

## 5. Direct nonintegrability check

On the neighborhood where rho=1,

R=epsilon x^2/2,     k=1-epsilon x>0,
beta_epsilon=du wedge dt+k dv wedge dx,
Psi_epsilon=alpha+i k^{-1/2} beta_epsilon
            =(du+i sqrt(k) dv) wedge (dx+i k^{-1/2} dt).

Thus a (1,0)-coframe is

phi_1=du+i sqrt(k)dv,     phi_2=dx+i k^{-1/2}dt.

Writing k'=partial_x k=-epsilon, direct differentiation and wedging give

d phi_1=i k'/(2 sqrt(k)) dx wedge dv,
d phi_1 wedge phi_1 wedge phi_2=(k'/(2k)) vol.                               (8)

This top form is nonzero for epsilon!=0. If J_epsilon were integrable, d of a (1,0)-form would have no (0,2) component, and its wedge with the (2,0)-form phi_1 wedge phi_2 would vanish in complex dimension two. Equation (8) therefore proves nonintegrability.

An independent equivalent coordinate check uses the unnormalized Nijenhuis tensor

N(X,Y)=[JX,JY]-J[JX,Y]-J[X,JY]-[X,Y].

The coframe gives J partial_u=k^{-1/2}partial_v, J partial_v=-sqrt(k)partial_u, J partial_x=sqrt(k)partial_t, and J partial_t=-k^{-1/2}partial_x. Hence

N(partial_u,partial_x)=k'/(2k) partial_u,

which at the origin equals -epsilon/2 partial_u and is nonzero.

## 6. Conclusion claimed by the candidate

Equations (2)-(7) give three independent closed anti-invariant classes on a smooth closed connected four-manifold, while (8) gives nonintegrability. If all steps survive independent review, this refutes the remaining integrability clause of the canonical target. It does not challenge generic vanishing, which is compatible with special deformations retaining three classes.

The original source target is OWR 33/2020, printed page 1687, Conjecture 2.5, and Draghici-Li-Zhang, *On the J-anti-invariant cohomology of almost complex 4-manifolds*, arXiv:1104.2511, Conjecture 2.5. The withdrawn Lejmi-Upmeier arXiv:1507.00282 is not used. All mathematics in the construction above was newly authored in this resumed pass; no missing earlier campaign artifact is reconstructed or assigned a counterfeit hash.

## Audit checklist

1. Verify the exact compact curve and the extension/independence of eta_0,eta_1.
2. Verify the simultaneous normal form for Omega_0 and Omega_1 with ratio coordinate zeta.
3. Verify d(R v dv)=v d(R dv), including the cutoff region.
4. Verify all signs in (1), (3), and (4).
5. Verify that positive two-plane realization supplies the claimed J and glues to J_0.
6. Verify the original and perturbed cohomology classes are independent.
7. Verify the nonintegrability computation and its convention.
8. Check for any known theorem or hidden hypothesis excluding this construction; do not infer validity from symbolic checks alone.
