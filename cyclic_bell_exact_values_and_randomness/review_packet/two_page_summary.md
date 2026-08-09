# Two-page scientific summary

## Result and source credit

Perito, D'Avino, Jung, Mironowicz, Acín, and Augusiak introduced the two
cyclic Bell families, supplied the canonical maximally entangled strategies
and lower bounds, proved the general first-family upper bound $d\sqrt2$, and
conjectured that their strategy's sharper value was exact. Their NPA
calculations through $d=6$ agreed with that conjectured value to the reported
precision. They also proved the second reduced value by a sum-of-squares
identity and studied canonical full-behavior randomness. Version 1.1 adopts
those definitions and credits those results; it does not present the
$d\sqrt2$ bound, numerical evidence, canonical strategies, or second-family
SOS as new.

For

\[
\mathcal I_d=\sum_{y=0}^{d-1}
\operatorname{Re}[(A_0+\omega^yA_1)B_y],
\qquad \omega=e^{2\pi i/d},
\]

the paper proves, for every $d\ge2$,

\[
\beta_q(\mathcal I_d)=\beta_{qa}(\mathcal I_d)
=\beta_{qc}(\mathcal I_d)=2\csc\!\frac{\pi}{2d}.
\]

The upper bound assumes only cross-party commutation and does not use the
order-$d$ relations. The source's finite canonical strategy supplies the
matching lower bound. The first Hermitian augmentation by
$\operatorname{Re}(A_0B_d)$ has value one more.

## Exact-value and support-rigidity mechanisms

For $C=V|C|$ and a commuting unitary $B$,

\[
\frac{|C|+|C^\dagger|}{2}-\operatorname{Re}(CB)
=\frac12P^\dagger P,
\qquad
P=|C^\dagger|^{1/2}-V|C|^{1/2}B.
\]

The canonical polar partial isometry belongs to Alice's generated von
Neumann algebra by an explicit strong-limit argument, so it still commutes
with Bob's algebra. Its support projections handle kernels; no inverse or
unitary extension is used. With $U=A_0^\dagger A_1$, functional calculus
reduces the remaining gap to

\[
\sum_y|1+\omega^yz|\le2\csc\frac{\pi}{2d},
\qquad \text{equality exactly when }z^d=(-1)^{d-1}.
\]

There is also a necessary equality theorem for arbitrary exact maximizers,
at a deliberately narrower scope. If a finite-dimensional tensor-product
strategy exactly maximizes the **first augmented** family and
$K=\operatorname{supp}\rho_A$, then $K$ reduces the relative unitary $U$, all
$d$ equality roots occur in $U|_K$ with equal multiplicity, and
$d\mid\dim K$. The proof uses the augmented stabilizer, Schmidt-support
cancellation, kernel-safe polar cancellation, adjacent-phase reflections,
and a rank count. It does not extend to approximate or general commuting-
operator maximizers, sectors outside $K$, or a classification/self-test.

## Permutation orbit and nonuniform exact maximizers

Let $z_k$ be the $d$ equality roots. Under explicit product-one and paired
polar-phase hypotheses, any permutation $\kappa$ gives weighted shifts

\[
A_0=X,\qquad A_1=X\operatorname{diag}(z_{\kappa_j})
\]

and corresponding Bob observables that remain order-$d$, full-spectrum exact
maximizers. Their local first moments and complete complex first-harmonic
correlator matrix are permutation-independent. This is a sufficient orbit,
not a complete maximizing-face classification.

For the designated pair,

\[
q_0=1,\quad q_{j+1}=z_{\kappa_j}q_j,
\qquad
p_\kappa(a,b\mid1,d)=\frac{|\widehat q_{-(a+b)}|^2}{d^3}.
\]

The canonical order is Fourier-flat. For every $d\ge4$, swapping the final
two phases gives a nonzero lag-two autocorrelation of magnitude
$4\sin(\pi/d)\sin(3\pi/d)$. The joint table is therefore nonuniform while
both marginals remain uniform, and trivial Eve gives

\[
G\ge\frac1{d^2}+
\frac{2\sin(\pi/d)\sin(3\pi/d)}{d^2(d-1)}>\frac1{d^2}.
\]

At $d=4$, exact cyclotomic arithmetic gives probabilities $1/32$ and $3/32$,
so $G=3/32$. For the displayed trivial-Eve realization,
$H_{\min}=5-\log_2 3=3.415037\ldots$ bits rather than four. This is also an
upper bound on value-only worst-case min-entropy, not its exact optimum.

## Second family and exact randomness scope

The paper uses the originating second-family SOS, with its corrected
$1/(2d)$ normalization, to prove global optimality of the same permutation
orbit. Exact Fourier compression
$\widehat B_\ell=d\lambda_\ell D_\ell$, together with
$A_\ell=\overline{D_\ell}$, annihilates every SOS factor. Under the
alternative source-appendix convention that adjoints all Bob observables,
the target table changes only by Bob outcome inversion $b\mapsto-b$; the
maximum, nonuniformity, guessing probability, and entropy are unchanged.

Conjecture 2 of the originating paper says that maximal violation of the
first augmented functional certifies $2\log_2d$ random bits at
$(x,y)=(1,d)$. After resolving its isolated printed normalization discrepancy
by using the displayed operator, version 1.1 disproves precisely the scalar-
value implication

\[
\langle\overline{\mathcal I}_d\rangle=M_d+1
\Longrightarrow G(AB\mid1,d,E)=1/d^2
\qquad(d\ge4).
\]

It does not challenge an SDP conditioned on the complete canonical behavior,
does not show that the canonical strategy lacks maximal randomness, and does
not determine the exact worst-case guessing probability.

## Secondary benchmarks

The low-setting section is secondary to the cyclic theorem chain. It includes
the prior-art binary $2\times2$ benchmark: an exact two-square SOS gives
$q=qa=qc=3\sqrt3$, and every attaining finite-dimensional tensor-product
strategy has $\sigma_E^{ab}=\rho_E/4$ at the target pair. It also restores a
private-MUB composition lemma as a **sufficient** criterion: a private
reference PVM, perfect Bob matching, and a supported MUB sandwich imply
$\sigma_E^{a,\pi(b)}=\rho_E/d^2$. The lemma is neither necessary nor an
existence theorem for an open low-setting regime.

## Fast review commands

```sh
cd cyclic_bell_exact_values_and_randomness
python3 verification/verify_rigidity.py
python3 verification/verify_exact_benchmarks.py
python3 verification/verify_private_mub_binary.py
./reproduce.sh
```
