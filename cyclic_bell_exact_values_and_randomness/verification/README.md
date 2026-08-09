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
python3 ../cyclic_randomness_counterexample/verify_exact.py
python3 ../minimum_bell_randomness/verify_second_family_d4_exact.py
python3 verification/verify_site.py
```

The two exact (d=4) programs are independent implementations over
(\mathbb Q(\zeta_{16})). They share the theorem statement, but not their
field/matrix implementation.

## What the hostile tests cover

- scalar equality phases and strict off-equality controls;
- the polar identity with a genuinely nonunitary partial isometry;
- weighted-cycle order, spectrum, first-family value, first harmonics, and
  target distributions for canonical/reversed/random/final-two orders;
- exhaustive (d=2,3) permutation flatness;
- primes and composites through a stated finite range;
- deliberately mismatched polar phases, repeated labels, and perturbed roots
  that must fail;
- second-family Fourier compression, order, and SOS saturation;
- canonical Fourier flatness and the final-two guessing lower bound;
- one-input local reconstruction;
- legacy hashes, PDF metadata, redirects, canonical metadata, sitemap, and
  local links.

## Evidence boundary

Finite regression does not prove an all-dimensional theorem. In particular,
finite direct-sum matrix tests cannot probe genuinely nonspatial
commuting-operator representations. The (qc) conclusion rests on the
analytic von Neumann-algebra functional-calculus proof. Likewise, the tests
sample the sufficient permutation theorem; they do not classify the full
maximizing face.

The historical exact-value unit tests call the same underlying verifier and
are regression tests, not an independent proof. The new polar hostile test
was added specifically because the historical singular tests used unitary
extensions of singular polar factors.
