# Author approach 5: repair the odd genus-one canonical integral by positivity

Problem 30004711. 7 October 2026. Fifth directed mathematical approach. Earlier frozen approaches are unchanged.

## Narrow result proposed for independent acceptance

For the **canonical Petersson metric** on F^dual over the odd-spin component of the once-NS-punctured genus-one moduli stack, the curvature extends as a finite positive current with no atom at the Ramond cusp. Its open integral is consequently the compactified characteristic number 1/32.

This supplies a current-level replacement for the smooth-extension shortcut tested in Approach4, in this particular rank-one component. The proof uses positivity in **all total-space directions** of the hyperbolic logarithmic canonical metric, followed by a singular direct-image theorem. It does not obtain derivatives by differentiating the norm inequalities. It does not identify the actual torsion measure, treat the other components/all genera, or resolve the literal OWR identity.

## 1. Work over the smooth part of the base first

Let B^o be the odd-spin genus-one, one-marked stack away from its nodal boundary. On a local manifold chart (and, where necessary, a finite cover carrying the spin square root), consider its proper smooth family

pi:C->B^o,

with marked section D. The coarse fibres are smooth elliptic curves; the complements C_b minus D_b carry the complete curvature-minus-one hyperbolic metrics. The pair is log-canonically polarized because deg(K_(C_b)+D_b)=1>0.

The morphism is projective: for example O_C(3D) is relatively very ample on this smooth elliptic family. We apply the direct-image theorem only over charts in B^o. No assertion about its hypotheses at a singular nodal fibre is needed in this step.

Let ell be the coarse spin line, with ell^2=K_(C/B^o), and put

L=ell(D),
L^2=K_(C/B^o)(2D).

The line whose Petersson metric we want is

E=pi_*(K_(C/B^o) tensor L)=F^dual.

On every smooth fibre its degree is1 and its zeroth cohomology dimension is1. Thus E is locally free of rank one and base change holds. The line itself extends over the odd Ramond boundary as E=H^3, H^2=lambda, by the algebraic calculation of Approach2.

## 2. Construct the exact twisting metric, including the divisor

Let h_K be the metric on K_(C/B^o) induced by the fibrewise hyperbolic metric. In a fibre coordinate z away from D, if the hyperbolic metric is rho^2|dz|^2, then

h_K(dz,dz)=rho^(-2).

Let h_D be the canonical singular metric on O(D) whose canonical section has norm1 away from D. In a frame e_D=1/z near D it has h_D=|z|^(-2); its curvature is the positive divisor current [D].

Set

h_(K(D))=h_K h_D,
h_L=(h_(K(D)) h_D)^(1/2)=h_K^(1/2) h_D.

The square-root metric is globally defined on L through the spin square-root isomorphism. A change of local holomorphic root frame changes its logarithm by a pluriharmonic term and does not change curvature.

Near an NS marked point, in the local frame (dz)^(1/2)/z of L,

h_L = rho^(-1)|z|^(-2) asymptotic to log(1/|z|)/|z|.

This is important: the direct-image twist is ell(D), not ell alone. Using the metric of ell alone would give the wrong divisor curvature and the wrong integrability condition for allowed simple-pole 3/2-differentials.

## 3. Verify semipositivity on the total space

[Philipp Naumann, Positivity of direct images with a Poincaré type twist, Forum of Mathematics, Sigma 10 (2022), e89](https://doi.org/10.1017/fms.2022.79), Theorem4.1, PDF p.14, proves semipositivity of the relative hyperbolic canonical curvature on the **total space minus the relative divisor** for a smooth family of log-canonically polarized pairs. It is not merely fibrewise positivity. Its hypotheses apply to the marked elliptic family above.

Across D the induced metric on K(D) has weight

phi_(K(D))=log(rho^2|z|^2)=-2 log log(1/|z|)+O(1).

The fibrewise cusp estimates and their local parameter control make this weight locally bounded above near D. The semipositive weight on the complement therefore extends plurisubharmonically across D. This is also the divisor-current calculation explained in Naumann's proof of Corollary5, PDF p.15; its local curvature assertion is the part used here, not its additional compact-base nefness conclusion.

Consequently, as currents on the total space over B^o,

c_1(L,h_L)=(1/2)c_1(K(D),h_(K(D)))+(1/2)[D] >=0.

Thus the singular twist satisfies the **base as well as fibre** positivity required by the direct-image theorem.

## 4. Multiplier ideal, metric identification, and the direct-image theorem

The local multiplier ideal is trivial. Indeed a bounded holomorphic function has squared norm integrable against h_L, because in the transverse coordinate

integral_0^epsilon [log(1/r)/r] r dr
 = epsilon(1-log epsilon)<infinity.

The same estimate is locally uniform in base charts away from their nodal boundary. There is no other singular divisor over B^o. Hence I(h_L)=O_C, and likewise I(h_L|C_b)=O_(C_b) for every smooth fibre.

[Păun–Takayama, Positivity of twisted relative pluricanonical bundles and their direct images, arXiv:1409.5504v1](https://arxiv.org/abs/1409.5504v1), Set-up3.2.1, PDF p.20, and Theorem3.3.4, PDF p.24, apply to a smooth projective morphism of complex manifolds, a semipositively curved singular line metric, a locally free adjoint direct image, and the indicated multiplier-ideal inclusion. All these hypotheses have just been checked. The conclusion is semipositivity of the **fibrewise canonical L2 metric itself**, with the stated base-change identification. This is stronger than merely the existence of some semipositive metric on the same line.

In our local frames a section of K tensor L is

eta=f(z)(dz)^(3/2)/z.

Its direct-image norm is, up to a fixed positive coordinate convention factor,

integral |f(z)|^2 rho^(-1)|z|^(-2) dxdy
 = integral bar(eta)eta/sqrt(hyperbolic metric).

This is exactly Norbury's canonical Petersson norm on F^dual. The possible universal factor from writing i dz wedge dbar z versus dxdy is constant and has zero curvature effect. It is not a change of the torsion measure's normalization.

In the nonzero frame s=(dz)^(3/2) from Approach4, write M=||s||^2 and u=log M. Since E is a line, the direct-image conclusion says

phi=-u is subharmonic on the punctured moduli disk.

Equivalently, c_1(E,M)=-dd^c u is a positive current there. Here dd^c=(i/(2 pi))partial barpartial. The construction is invariant under finite chart groups, so positivity descends to the spin stack.

## 5. Extend the scalar weight, with zero cusp atom

Approach4 gives, uniformly in the angular variable of q=exp(2 pi i tau),

u(q)=2 log log(1/|q|)+O(log log log(1/|q|)).

Thus phi=-u is bounded above near0, is locally integrable, and is not identically minus infinity. Its subharmonic extension across0 is therefore well-defined. It yields a finite positive curvature measure on every relatively compact disk.

The mass at0 is its logarithmic/Lelong coefficient. The estimate

phi(q)/log|q| ->0

uniformly in angle shows that coefficient is zero. Accordingly the extended current has no delta mass at the cusp. This is a genuine existence-and-zero-mass conclusion, not an assumption that a boundary-flux limit happens to exist.

A direct radial check gives quantitative control. Set t=log(1/|q|) and let m(t) be the angular average of u. Subharmonicity of -u implies m''(t)<=0 in the distributional sense; on the punctured disk the original metric is smooth, so the ordinary derivative can be used. The bounds of Approach4 imply

2 log t+C_- <= m(t) <=2 log t+log log t+C_+.

Concavity and the fact that m(t)->infinity show m'(t)>=0 and decreasing. Its limit is0 because m(t)=o(t). More explicitly,

0<=m'(t)<=2[m(t)-m(t/2)]/t
          <=2[C+log log t]/t

for large t. With the stated dd^c convention the curvature mass in |q|<exp(-t) equals m'(t)/2 after the zero atom is taken into account. Hence it tends to zero and is O((1+log log t)/t).

This argument obtains the derivative bound from curvature positivity plus concavity. It does not differentiate either side of an asymptotic inequality.

## 6. Recover the canonical open integral in this component

Let B be the compactified odd-spin component, and choose a smooth positive reference metric on its extended line E=F^dual. The logarithm of the ratio of the canonical and reference metrics is globally locally integrable: the only new behavior at the boundary is the polylogarithmic norm growth above. Their curvature currents differ by a globally exact dd^c current. Thus the extended canonical curvature represents c_1(E).

The current is a finite positive measure, has no atom at the Ramond cusp, and coincides with the canonical Chern form on B^o. Therefore

integral_(B^o) c_1(E,M)=integral_B c_1(E)=1/32,

using the same unrigidified stack convention as Approach2. For the dual line F with its inverse metric and its standard complex orientation the value is -1/32. These signs are fixed by the line identification, not subsequently adjustable.

This proof uses only the direct-image positivity theorem over **smooth** families. The nodal boundary is handled afterwards by scalar potential theory and the norm bounds in an independently specified extending frame. It does not invoke a smooth hyperbolic metric extension over the nodal family or apply the direct-image theorem to an unchecked singular fibre.

## 7. What this repairs and what remains unresolved

Subject to independent verification of the cited-theorem application, this repairs the canonical odd rank-one integral at the cusp using a positive current instead of a positive smooth metric. It is compatible with Approach4's obstruction to a smooth extension. In this component it supplies the missing existence of a finite curvature/flux limit left open there.

It does **not** prove:

- that the original OWR/SW torsion representative is this Chern form;
- that the two constructions have the same retraction, parity signs, boundary-spin trivializations, or stack normalization;
- a global current extension of higher-rank top Chern forms for every g,n;
- the fully geometric torsion recursion whose premise remains open in Approach3;
- the unqualified coefficient-one OWR formula.

Higher rank is not obtained simply by repeating the rank-one positivity argument: top Chern forms and products of singular curvatures require their own extension/integration analysis. The even genus-one component is likewise not silently included in the odd-line cusp proof.

Five substantive approaches are now complete. The literal original torsion-volume identity has not been proved or disproved. The cumulative report records the supported partial results and the precise remaining comparison.
