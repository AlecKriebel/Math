# A sharper local-purity filter for smooth DTH violations

## Theorem

Let \(z\in(\mathbb C^3)^{\otimes3}\) be a unit tensor at which

\[
 \mathcal F(z)=\sum_{j=1}^4s_j(D_z)^2
\]

is differentiable and critical on the unit sphere.  If
\(\mathcal F(z)>1/2\), then

\[
 \boxed{
 P_{\rm loc}(z)=\sum_{i=1}^3\operatorname{Tr}(\rho_i^z)^2
 >{29\over21}.}
 \tag{1}
\]

This strictly improves, on the smooth critical locus, the unconditional
output-purity threshold \(P_{\rm loc}>15/11\).  It does not exclude the
remaining high-purity region.

## 1. Orthogonal one-body projection bound

Let \(\omega\) be any trace-one Hermitian operator on three qutrits, with
one-site marginals \(q_i\).  The Hilbert--Schmidt orthogonal projection of
\(\omega\) onto the scalar-plus-one-body operator space is

\[
 \omega_{\le1}
 ={I\over27}
 +{1\over9}\sum_{i=1}^3
   (q_i-I/3)\otimes I_{\widehat i}.
 \tag{2}
\]

The four summands in (2) are mutually orthogonal.  Therefore

\[
 \operatorname{Tr}\omega^2
 \ge \operatorname{Tr}\omega_{\le1}^2
 ={1\over27}+{1\over9}\sum_i
   \left(\operatorname{Tr}q_i^2-{1\over3}\right)
 ={3\sum_i\operatorname{Tr}q_i^2-2\over27}.
 \tag{3}
\]

Positivity of \(\omega\) is not needed for this projection inequality.

## 2. Apply the critical equal-marginal theorem

Put

\[
 S=D_z^\dagger D_z,
 \qquad F=\mathcal F(z),
\]

and let \(P\) be the isolated top-four spectral projector.  The exact
critical equations proved in `agent_dth_full_rank_euler.md` give two
orthogonally supported states

\[
 \tau={PS\over F},
 \qquad
 \sigma={S-PS\over1-F}
\]

with common marginals

\[
 \tau_i=\sigma_i=q_i={I-\rho_i^z\over2}.
 \tag{4}
\]

The top state has rank at most four, so

\[
 \operatorname{Tr}\tau^2\ge{1\over4}.
 \tag{5}
\]

Writing \(P_{\rm loc}=\sum_i\operatorname{Tr}(\rho_i^z)^2\), equation
(4) gives

\[
 \sum_i\operatorname{Tr}q_i^2={3+P_{\rm loc}\over4}.
\]

Thus (3), applied to \(\sigma\), becomes

\[
 \operatorname{Tr}\sigma^2
 \ge {1+3P_{\rm loc}\over108}=:L.
 \tag{6}
\]

Since the supports of \(\tau\) and \(\sigma\) are orthogonal,

\[
 \operatorname{Tr}S^2
 =F^2\operatorname{Tr}\tau^2
  +(1-F)^2\operatorname{Tr}\sigma^2
 \ge {F^2\over4}+(1-F)^2L.
 \tag{7}
\]

The exact output-purity identity is

\[
 \operatorname{Tr}S^2={1+P_{\rm loc}\over32}.
 \tag{8}
\]

For \(1\le P_{\rm loc}\le3\), one has
\(L\le5/54<1/4\).  Hence the right side of (7) is strictly increasing in
\(F\) on \([1/2,1]\).  At \(F=1/2\), equations (7)--(8) imply

\[
 0\le {1+P_{\rm loc}\over32}
       -{1\over16}-{1+3P_{\rm loc}\over432}
 ={21P_{\rm loc}-29\over864}.
 \tag{9}
\]

If \(F>1/2\), the inequality in (9) is strict.  This proves (1).

## Scope

The result is a necessary condition only for a smooth critical violation.
It does not cover a nonsmooth point at which the fourth and fifth squared
singular values meet, and it leaves the region
\(P_{\rm loc}>29/21\) open.  Its value is that it combines the full Euler
equal-marginal geometry with the output-purity identity, rather than using
the output spectrum alone.

