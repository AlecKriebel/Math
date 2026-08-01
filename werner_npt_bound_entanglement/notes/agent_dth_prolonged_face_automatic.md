# Prolonged DTH faces are automatic under positive extension

## Theorem

Let (T) be a degree-three moment with degree-two marginal

\[
 R=\operatorname{Tr}_{A_3}T.
\]

Suppose the anchored degree-three contraction is, up to a fixed output
permutation,

\[
 C_3=C_2\otimes I_{A_3}.
\]

Then

\[
 \boxed{
 T\succeq0,quad C_2RC_2^\dagger=0
 \quad\Longrightarrow\quad
 C_3TC_3^\dagger=0.}
 \tag{1}
\]

Consequently, for an extension of the established five-replica DTH
pseudomoment:

1. positivity of (T) automatically prolongs the holomorphic Omega face;
2. positivity of (T^{\Gamma_{A_1}}) automatically prolongs the mixed
   support face, because
   \(\operatorname{Tr}_{A_3}T^{\Gamma_{A_1}}=R^{\Gamma_{A_1}}\).

Thus the prolonged face equations do not have to be imposed as additional
large linear systems once the corresponding positive extension cone and
the fixed constrained marginal are enforced.  This does not remove the
need to prove the relevant partial-transpose positivity.

## Proof

The exact contraction identity is

\[
 \operatorname{Tr}_{A_3}
 \left(C_3TC_3^\dagger\right)
 =C_2RC_2^\dagger.
 \tag{2}
\]

If (T\succeq0), then

\[
 A:=C_3TC_3^\dagger\succeq0.
\]

Under the degree-two face hypothesis, (2) gives
\(\operatorname{Tr}_{A_3}A=0\), hence
\(\operatorname{Tr}A=0\).  A positive semidefinite operator of trace zero
vanishes, proving (1).

For Omega, use the holomorphic maps

\[
 C_{\Omega,3}(w_1,w_2,w_3,z)
 =q(w_1,z)w_2\otimes w_3
\]

and (C_{\Omega,2}(w_1,w_2,z)=q(w_1,z)w_2).  They have precisely the
anchored tensor-product relation above.

For support, apply the same argument to

\[
 \widehat T=T^{\Gamma_{A_1}}\succeq0,
 \qquad
 \widehat R=R^{\Gamma_{A_1}},
\]

and the maps

\[
 C_{S,3}(\bar w_1,w_2,w_3,z)
 =w_2\otimes w_3\otimes W_1^\dagger z,
\]

\[
 C_{S,2}(\bar w_1,w_2,z)
 =w_2\otimes W_1^\dagger z.
\]

Partial transpose on (A_1) commutes with the trace over (A_3), so the
same proof applies verbatim.  The five-replica pseudomoment already obeys
both degree-two face equations exactly.  Therefore the next genuine
degree-three decision is the positive/PPT extension problem, not a separate
prolonged-support feasibility problem.

## Scope

The implication depends essentially on positivity of the extended moment
in the representation where the contraction is applied.  A merely
Hermitian affine extension need not prolong a zero face.  In particular,
the support conclusion requires (T^{\Gamma_{A_1}}\succeq0), not just
(T\succeq0).

