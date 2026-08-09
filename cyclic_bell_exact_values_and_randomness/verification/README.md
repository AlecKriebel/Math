# Verification guide

## Full replay

```sh
cd cyclic_bell_exact_values_and_randomness
./reproduce.sh
```

The command intentionally uses the Python standard library for the unified
regressions. Tectonic, Poppler (`pdfinfo`), and a POSIX shell are needed for
the build/metadata stages. No network access is required.

## Component checks

```sh
python3 verification/verify_merged.py
python3 verification/verify_rigidity.py
python3 verification/verify_exact_benchmarks.py
python3 verification/verify_private_mub_binary.py
python3 ../cyclic_randomness_counterexample/verify_exact.py
python3 ../minimum_bell_randomness/verify_second_family_d4_exact.py
python3 verification/verify_mub_obstruction.py
python3 verification/verify_site.py
```

The two exact $d=4$ programs are independent implementations over
$\mathbb Q(\zeta_{16})$. They share the theorem statement, but not their
field/matrix implementation.

## What the hostile tests cover

- scalar equality phases and strict off-equality controls;
- the polar identity with a genuinely nonunitary partial isometry;
- source exact radicals, NPA comparison decimals, Fourier coefficients,
  canonical Bob observables, and the explicit qutrit formula;
- equal supported phase multiplicities, adjacent-reflection wraparound,
  exact rank inequalities, and hostile incompatible dimension counts;
- weighted-cycle order, spectrum, first-family value, first harmonics, and
  target distributions for canonical/reversed/random/final-two orders;
- exhaustive $d=2,3$ permutation flatness;
- primes and composites through a stated finite range;
- deliberately mismatched polar phases, repeated labels, and perturbed roots
  that must fail;
- second-family Fourier compression, order, and SOS saturation;
- cosecant-square coefficient normalization through $d=100$;
- canonical Fourier flatness and the final-two guessing lower bound;
- the exact $d=4$ entropy $5-\log_2 3$;
- the binary $3\sqrt3$ SOS, attaining strategy, and all three nontrivial
  operator-valued Fourier coefficients;
- private-MUB normalization and three deliberately dropped-hypothesis
  controls;
- one-input local reconstruction;
- legacy hashes, PDF metadata, redirects, canonical metadata, sitemap, and
  local links.

## Evidence boundary

Finite regression does not prove an all-dimensional theorem. In particular,
finite direct-sum matrix tests cannot probe genuinely nonspatial
commuting-operator representations. The $qc$ conclusion rests on the
analytic von Neumann-algebra functional-calculus proof. Likewise, the tests
sample the sufficient permutation theorem; they do not classify the full
maximizing face.

The support-rigidity replay is finite-dimensional evidence only; its theorem
rests on the state-support and reflection-rank proof and is not extended to
$qa$ or $qc$. The binary privacy replay checks exact matrices and Fourier
normalization, while privacy for arbitrary finite-dimensional purifying Eve
rests on the test-operator proof.

The historical exact-value unit tests call the same underlying verifier and
are regression tests, not an independent proof. The new polar hostile test
was added specifically because the historical singular tests used unitary
extensions of singular polar factors.
