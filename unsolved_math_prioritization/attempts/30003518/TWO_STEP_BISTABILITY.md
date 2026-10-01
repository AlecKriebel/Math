# An exact two-step bistability certificate

**Unreviewed scoped partial result, author turn 3.** This concerns the independently parameterized Lck-only network of Brechmann (2024), equation (2.2). It does not assert bistability for the original calibrated shared-rate model, for the model with ZAP-70, or for every conservation class.

## Network and parameters

Write R+M ⇄ C0 with association rate k=1 and dissociation d0=2. For i=0,1 use C_i+E ⇄ B_i → C_(i+1)+E, with association u0=u1=8; dissociation v0=2, v1=256; catalysis w0=2, w1=256. The reset reactions C1→R+M and C2→R+M have rates d1=4 and d2=1/128. All rates are positive. Fix conserved totals Rtot=Mtot=256 and Etot=8, including bound enzyme complexes in all appropriate totals.

**Theorem.** This class has exactly three physical positive equilibria. Two are hyperbolic sinks and one is a hyperbolic saddle with one unstable eigenvalue, all relative to the five-dimensional conservation class. Consequently there is an open neighborhood of these positive rates and totals admitting two locally asymptotically stable positive equilibria. No classification of all trajectories or basin boundaries is asserted.

## Exact equilibrium reconstruction and complete root count

Let e be free enzyme. The scalar reconstruction in TURN2_REDUCTION.md specializes to

Q(e)=4+4e,
g(e)=8+(129/16)e,
h(e)=Q(e)+4e+2048e²+eg(e).

Its eliminated equation is P(e)=0, where

P(e)=1082212609e⁶−15125744400e⁵+54877391424e⁴−14188516224e³
     +1182559232e²−31653888e+262144.

More exactly,

P(e)=256{[256eg(e)−(8−e)h(e)]²−(2+4e)(8−e)Q(e)eg(e)}.

The positive constant 256 does not affect roots. Every candidate with 0<e<8 reconstructs

C0=(8−e)(4+4e)/(eg), C1=4(8−e)/g, C2=2048e(8−e)/g,
B0=2eC0, B1=eC1/64,
r=m=256−C0−C1−C2−B0−B1.

It is physical exactly when r>0. All the other listed concentrations and free enzyme are already strictly positive on (0,8); enzyme conservation is B0+B1+e=8. The original source balance and all receptor/enzyme equations follow from the reconstruction lemma. No unfiltered root of the degree-six equation is counted as an equilibrium.

The exact certificate verifies that P has degree six, is squarefree, and has six distinct real roots all in (0,8). Its rational isolating intervals are recorded in two_step_certificate.json. Ordered by e, only roots 2,3,6 have positive r; the other three have rigorously negative r. Their approximate e values, for orientation only, are 0.0220866, 0.109486, and 6.859263. These decimal values are not used as proof. Rational interval bounds prove every physical-filter decision. The six isolated roots exhaust the polynomial degree, so there are exactly three physical equilibria.

## Original Jacobian and exact stability signs

Use coordinates (C0,C1,C2,B0,B1); eliminate free pools by their conserved totals. Write z=−2r. The Jacobian is

[[z−2−8e, z, z, z+8C0+2, z+8C0],
 [0, −4−8e, 0, 2+8C1, 8C1+256],
 [0, 0, −1/128, 0, 256],
 [8e, 0, 0, −8C0−4, −8C0],
 [0, 8e, 0, −8C1, −8C1−512]].

The checker derives this matrix by symbolic differentiation of the original reduced ODE, and checks all 25 entries. Thus stability is assessed in the original dynamical system, rather than inferred from the slope of a scalar equilibrium equation.

For each physical root, exact rational interval arithmetic encloses every Jacobian entry. The coefficients a0=1,a1,...,a5 of det(lambda*I−J) are obtained as sums of principal minors of −J. The Hurwitz matrix has entries H_ij=a_(2j−i+1), with zero for indices outside 0,...,5 and i,j starting at zero. Its leading determinants are Delta1,...,Delta5. Interval arithmetic is applied to the determinant permutation formulas, with no rounding or floating-point rank/eigenvalue decision.

At roots 2 and 6, every Delta_j has a strictly positive lower bound. The classical Hurwitz criterion proves these equilibria are hyperbolic sinks. For orientation, outward integer enclosures of a5 are respectively [749618,749619] and [4746781,4746782]; the full determinant enclosures are supplied in the certificate.

At root 3, Delta1,...,Delta4 have strictly positive lower bounds, while a5 has enclosure [−361309,−361308]. The Routh first column is

1, a1, Delta2/Delta1, Delta3/Delta2, Delta4/Delta3, a5.

It has exactly one sign change and no zero entries, with the regular Routh construction defined throughout. Therefore there is exactly one eigenvalue in the open right half-plane and none on the imaginary axis; the other four have negative real part. In particular the equilibrium is a hyperbolic index-one saddle. Complex eigenvalues come in conjugate pairs, so its single unstable eigenvalue is real.

## Open parameter region and limitations

Hyperbolic equilibria persist under small changes of the original positive rates and conserved totals by the implicit-function theorem. Their positivity is strict and therefore persists, as do the signs of the real parts of their eigenvalues. Hence the two sinks establish an open bistable parameter region, not just an exceptional parameter point. No claim is made that this entire neighborhood has an explicitly quantified radius. The original certificate proves exactly three equilibria at the displayed rational class; the local persistence statement only needs the three hyperbolic branches.

The witness was located by a bounded numerical diagnostic scan, but the proof depends only on the displayed rational data and the exact checker, verify_two_step.py. That checker performs 101 exact assertions, including Sturm counts, original-ODE differentiation, physical filtering and rational Hurwitz/Routh bounds. The numerical scan is separately labeled and is unnecessary for verification.

Existing multistationarity of this core is credited to Brechmann's 2024 dissertation, Theorem 3. This partial result additionally certifies two attracting equilibria in an explicit class; no historical novelty is asserted. The different François/phosphatase network in PR145 is not used. The broad OWR asymptotics problem remains unresolved.
