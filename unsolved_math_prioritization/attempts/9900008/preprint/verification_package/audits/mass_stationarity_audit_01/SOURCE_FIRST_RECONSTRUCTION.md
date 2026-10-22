# Independent source-first mass-stationarity reconstruction

UTC: 2026-10-15T11:26:44.206862+00:00. Completion estimate: 15% of this audit family.

## Reading order and independence limit

I read the exact target record, Thorisson Some Open Probability Problems section 4, and Last--Thorisson (2009) flow definitions and Definition 6.1/Remark 6.2 before author/PROOF.md, all historical audit/acceptance files, the prior report, other auditors, or the root memo. However, the inherited parent-context summary already described a two-line construction and a proposed 1/3 witness. This is therefore an independently checked source-first derivation, not a blind discovery. I will not conceal this exposure.

## Exact source contract

G may be R^2. A locally finite diffuse measure can be singular to two-dimensional Lebesgue measure. The accompanying random element can be constant. The source test is the joint equality (theta_V, U+V) =d (theta_0,U), where U is uniform in an admissible relatively compact C and the conditional law of V is normalized measure on C-U. A first-marginal discrepancy suffices to disprove the joint equality. Rectangles with positive side lengths have positive Haar measure and Haar-null boundary. The canonical shift is theta_s nu(B)=nu(B+s). Probability laws are permitted within the sigma-finite formulation.

## Own analytic reconstruction

For a,b>0, a != b, let nu=a delta_0 tensor lambda + b delta_1 tensor lambda on R^2. It is nonzero, Radon, sigma-finite, has no point atoms, and contains the origin in its support. Its vertical stabilizer is all of {0} x R.

Take C=[0,L] x [0,H], L>1, H>0, U uniform in C. Except for Haar-null boundary values, the root line at x=0 intersects C-U in a segment of vertical length H for every U. The line x=1 intersects it iff U_x<=L-1. On that event the two line masses are aH and bH. Thus

P(V_x=1) = ((L-1)/L) b/(a+b) > 0.

On that event theta_V nu has lines x=-1 of mass a and x=0 of mass b, while nu has lines x=0 of mass a and x=1 of mass b. They differ. Consequently the first marginal of the source mass-stationarity identity fails. With a=1,b=2,L=2,H=1 the probability is exactly 1/3. A measurable separating observable is nu((-1/4,1/4) x [0,1]), equal to a before and b on a horizontal jump. The fixed law delta_nu cannot satisfy the joint equality.

This calculation does not rely on a stationary probability measure, finite total mass, stochastic simulation, a density w.r.t. planar Haar measure, or independent auxiliary background. It normalizes only the finite strictly positive mass of C-U.

## Conditional-law and phase controls

An explicit sampler is independent U_x~Unif[0,L], U_y~Unif[0,H], R,S~Unif[0,1]. Put I=1 when U_x<L-1 and R<b/(a+b), otherwise I=0; set V=(I,H S-U_y). This gives exactly the conditional normalized measure law (boundary events arbitrary). U_y+V_y=HS. The horizontal first marginal alone refutes mass-stationarity.

For the other supported root phase theta_(1,0)nu, the other line lies at -1; it is accessible when U_x>=1 and has conditional share a/(a+b), giving reverse-jump probability ((L-1)/L)a/(a+b)>0. A root mixture weighted a:b balances these two transition probabilities; delta at either root does not. This is an independent Palm-weight consistency control, not yet a proof of a stationary Palm representation.

## Allocation condition to be checked separately

For a candidate allocation depending only on the shifted pair, exact covariance and the vertical stabilizer force constant displacement along each line. Preservation must push entire line masses onto target lines. A surjective two-line map is a permutation; unequal weights forbid swapping. This should imply all preserving allocations leave the rooted state unchanged, but must be checked with full definitions, measurability, and possible almost-everywhere conventions. Identity must be admissible, so the quantified class is not empty.

## Falsifiable acceptance criteria

1. Original Problem 4.1 permits singular diffuse R^2 measures and constant X without a free-action assumption.
2. The candidate is a genuine jointly measurable flow-adapted random measure with a probability law, and every needed finite-window normalization is strictly positive and finite almost surely.
3. Re-derive the normalized conditional law and positive first-marginal discrepancy without inherited verdicts.
4. Demonstrate that pair-dependent preserving allocations cannot exploit hidden randomness or root-null exceptional sets to evade the stabilizer argument.
5. Verify the product-lift primary source and distinguish its already known statement from any new claimed consequence.
6. Reject stronger claims about absolutely continuous, free-action, or Markovian-kernel settings absent a proof.

Exact remaining gap: authored proof and all central cited bodies have not yet been read; universal allocation validity, full measurable realization, and prior-literature scope remain open in this audit. No candidate code has been executed.
