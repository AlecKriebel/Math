# Targeted prior-art audit

This audit began only after the first exact structural theorems had been
derived.  It is a targeted search, not proof of worldwide priority.

## Exact binary \(2\times2\) construction

The score

\[
A_0B_0-2A_0B_1+2A_1B_0+2A_1B_1
\]

is not new.  It is the \(\delta=\pi/6\) case of Proposition 1 in:

- Lewis Wooltorton, Peter Brown, and Roger Colbeck, “Tight analytic bound on
  the trade-off between device-independent randomness and nonlocality,”
  *Physical Review Letters* **129**, 150403 (2022),
  [arXiv:2205.00124](https://arxiv.org/abs/2205.00124),
  [DOI](https://doi.org/10.1103/PhysRevLett.129.150403).

Their coefficient matrix is

\[
\begin{pmatrix}
1&\csc\delta\\
\csc\delta&-\sec(2\delta)
\end{pmatrix}.
\]

At \(\delta=\pi/6\) this is
\(\bigl(\begin{smallmatrix}1&2\\2&-2\end{smallmatrix}\bigr)\).
Flipping Bob's second binary outcome gives exactly the matrix used in this
project.  That work already proves the quantum value \(3\sqrt3\), uniqueness
up to local isometries, and two global Eve-private bits at the target pair.
The independent SOS/Fourier proof here is retained as a self-contained
verification and benchmark, not a novelty claim.

## Current all-dimensional rigorous benchmark

Farkas, Mironowicz, and Augusiak give an all-dimensional, single-score
projective construction:

- Máté Farkas, Piotr Mironowicz, and Remigiusz Augusiak, “Maximal global
  device-independent randomness from projective measurements in every
  dimension,” [arXiv:2606.21369](https://arxiv.org/abs/2606.21369).

Their scenario has two \(d\)-outcome Alice settings and \(d^2+1\) Bob
settings.  The first \(d^2\) Bob settings have three outcomes and the final
randomness setting has \(d\) outcomes.  For \(d\ge3\), the three-outcome
measurements can be represented in the present \(d\)-outcome convention by
padding with zero projectors.  Their single Bell score has exact value
\(\sqrt{d(d-1)}+1\), and their equality analysis yields

\[
\rho_{ABE}^{\mathrm{cq}}
=
\frac{I_{d^2}}{d^2}\otimes\eta_E
\]

for the designated pair.  This is private global randomness, not merely
observed uniformity.

Thus the rigorous all-dimensional setting upper bound presently recorded in
this project is \(2\times(d^2+1)\), while the universal lower bound is two
settings on each wing.

The closest lower-setting claims are the two families in:

- Ignacio Perito et al., “Bell inequalities tailored to optimal global
  randomness certification,”
  [arXiv:2606.21362](https://arxiv.org/abs/2606.21362).

Their first family uses \(2\times(d+1)\) settings and their second augmented
family uses \(d\times(d+1)\).  The arbitrary-dimensional global-randomness
statements were conjectural; the first family is defeated by the explicit
cycle-permutation maximizers already recorded in the companion project.
The present project proves that the same construction defeats the
Bell-value reading of the second family for every \(d\ge4\), by annihilating
its published SOS factors with exact order-\(d\) observables.

## Minimal two-input qudit self-test

The standard two-setting maximally-entangled-qudit self-test is:

- Shubhayan Sarkar et al., “Self-testing quantum systems of arbitrary local
  dimension with minimal number of measurements,” *npj Quantum Information*
  **7**, 151 (2021), [arXiv:1909.12722](https://arxiv.org/abs/1909.12722),
  [journal](https://www.nature.com/articles/s41534-021-00490-3).

It certifies \(\log_2d\) local random bits.  The paper explicitly leaves
certification of \(2\log_2d\) global bits using two projective measurements
as an open direction.  The exact ideal-table audit in this project shows why
the unmodified strategy does not immediately solve that problem: none of
its four input pairs is uniform.

## Neighboring MUB construction

Kaniewski et al. construct modified Buhrman--Massar inequalities with
analytic quantum values and MUB strategies:

- Jędrzej Kaniewski et al., “Maximal nonlocality from maximal entanglement
  and mutually unbiased bases, and self-testing of two-qutrit quantum
  systems,” [arXiv:1807.03332](https://arxiv.org/abs/1807.03332).

The construction uses \(d\) settings per party for prime \(d\), and the
standard self-testing statement is proved for \(d=3\), not all dimensions.

Other nearby distinctions:

- Farkas et al., “Maximal device-independent randomness in every dimension,”
  [arXiv:2409.18916](https://arxiv.org/abs/2409.18916), concerns
  \(2\log_2d\) *local* randomness from a \(d^2\)-outcome nonprojective
  measurement, rather than global projective randomness.
- Woodhead et al., “Maximal randomness from partially entangled states,”
  [arXiv:1901.06912](https://arxiv.org/abs/1901.06912), includes exact
  two-bit global qubit constructions, but with more than \(2\times3\)
  settings and no all-dimensional result.
- Tavakoli et al., “Mutually unbiased bases and symmetric informationally
  complete measurements in Bell experiments,”
  [arXiv:1912.03225](https://arxiv.org/abs/1912.03225), uses many settings
  and certifies an operational MUM notion; in dimensions \(4,5\) its
  maximizers need not extract standard MUBs.
- Pereira Alves and Kaniewski show that any pair of incompatible rank-one
  PVMs is optimal for some nontrivial Bell inequality,
  [arXiv:2112.07582](https://arxiv.org/abs/2112.07582), but optimality is not
  a rigidity or private-randomness theorem and their construction is not a
  \(2\times2\) all-dimensional self-test.
- Coccia, Padovan, and Vallone, “Systematic derivation of Tsirelson bounds
  in arbitrary dimensions,”
  [arXiv:2606.21626](https://arxiv.org/abs/2606.21626), derive
  MUB-saturated inequalities with two Alice and \(2d\) Bob settings.  Their
  compression obstruction is specific to a linear-transformation SOS
  ansatz, not a universal \(2\times2\) or \(2\times3\) lower bound.

No primary source was found that rules out \(2\times2\) for
\(2\log_2d\) global private bits when \(d>2\), or that proves one party
requires three settings.  The one-input flagged-realization theorem is
therefore the only universal setting lower bound currently justified here.
With one input on either wing the complete nonsignalling behavior is local,
so the lower bound is a standard baseline rather than a novelty claim.

## Search conclusion and limits

The targeted primary-source search has not located an all-dimensional
\(2\times2\) or \(2\times3\), \(d\)-outcome projective protocol that
certifies exactly \(2\log_2d\) global private bits from one maximal Bell
score.  This is a report of what was not located, not an impossibility or
priority proof.
