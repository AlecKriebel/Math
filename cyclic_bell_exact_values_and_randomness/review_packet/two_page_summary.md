# Two-page scientific summary

## Result and attribution

Perito, D'Avino, Jung, Mironowicz, Acin, and Augusiak introduced two cyclic
Bell families for efficient maximal-global-randomness certification. They
defined the operators, supplied canonical maximally entangled strategies and
matching lower bounds, conjectured the first reduced value, and proved the
second reduced value by a sum-of-squares identity. The merged paper adopts
those definitions with explicit normalization and adjoint conventions.

For

\[
\mathcal I_d=\sum_{y=0}^{d-1}
\operatorname{Re}[(A_0+\omega^yA_1)B_y],
\qquad \omega=e^{2\pi i/d},
\]

the paper proves, for every (d\ge2),

\[
\beta_q(\mathcal I_d)=\beta_{qa}(\mathcal I_d)
=\beta_{qc}(\mathcal I_d)=2\csc\!\frac{\pi}{2d}.
\]

The upper bound assumes only cross-party commutation; it does not assume a
tensor-product representation or even the order-(d) relations. The
finite-dimensional canonical strategy supplies the matching lower bound. The
Hermitian augmentation by (\operatorname{Re}(A_0B_d)) has value one more.

## Exact-value mechanism

For (C=V|C|) and a commuting unitary (B),

\[
\frac{|C|+|C^\dagger|}{2}-\operatorname{Re}(CB)
=\frac12P^\dagger P,
\qquad
P=|C^\dagger|^{1/2}-V|C|^{1/2}B.
\]

The support projections of the canonical polar partial isometry handle
kernels; no inverse is used. With (U=A_0^\dagger A_1), functional calculus
reduces the remaining gap to

\[
\sum_y|1+\omega^y z|\le 2\csc\frac{\pi}{2d},
\]

whose equality phases are exactly (z^d=(-1)^{d-1}). This yields an explicit
positive-factor identity in the commuting algebra. State-level equality
annihilates those factors, but the paper does not infer a complete global
classification from one maximizing vector.

## Phase order and nonuniform maximizers

Let (z_k) be the (d) scalar equality roots. Any permutation (\kappa)
can be placed along a weighted shift,

\[
A_0=X,\qquad A_1=X\operatorname{diag}(z_{\kappa_j}),
\]

and paired with the correspondingly permuted polar phases in Bob's
observables. Exact product-one identities make every weighted shift an
order-(d), full-spectrum observable. All Bell-visible first-harmonic
correlators are symmetric sums of the phase set and hence are independent of
(\kappa).

The target pair depends on the cumulative sequence

\[
q_0=1,\qquad q_{j+1}=z_{\kappa_j}q_j,
\qquad
p(a,b|1,d)=\frac{|\widehat q_{-(a+b)}|^2}{d^3}.
\]

The canonical cyclic order is Fourier-flat. For every (d\ge4), swapping the
last two phases gives a nonzero lag-two autocorrelation of magnitude
(4\sin(\pi/d)\sin(3\pi/d)), so the target table is nonuniform although both
marginals remain uniform. With trivial Eve,

\[
G\ge\frac1{d^2}+
\frac{2\sin(\pi/d)\sin(3\pi/d)}{d^2(d-1)}.
\]

At (d=4), exact cyclotomic arithmetic gives the parity table (1/32) and
(3/32), hence (G=3/32>1/16).

## Second family and randomness scope

The source second-family SOS is

\[
dI-\mathcal F_d=\frac1{2d}\sum_\ell
(d\lambda_\ell I-A_\ell\widehat B_\ell)^\dagger
(d\lambda_\ell I-A_\ell\widehat B_\ell).
\]

The same permuted Bob cycles obey an exact Fourier compression
(\widehat B_\ell=d\lambda_\ell D_\ell). Choosing
(A_\ell=\overline{D_\ell}) annihilates every source SOS factor, proves the
global maximum, and gives the same target table (up to Bob outcome inversion
under the source appendix's dagger convention).

The conclusion is specifically about conditioning on the scalar Bell value.
It does not challenge an SDP that fixes the complete canonical behavior, and
it does not show that the canonical strategy lacks maximal global
randomness. Moving between those statements would require uniqueness,
self-testing, or enough extra correlators to exclude the permuted behavior.

## Review priorities

The specialist checks with the highest value are: support handling in the
polar identity; left/right functional calculus; exact paired-permutation
admissibility; the target DFT and guessing bound; the second-family Fourier
phase and SOS convention; and the scalar-value/full-behavior distinction.
