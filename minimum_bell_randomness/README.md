# Minimum Bell-test complexity for maximal global randomness

This directory contains an independent research program on the minimum
measurement-setting resources needed to certify \(2\log_2 d\) bits of
device-independent global private randomness from projective \(d\)-outcome
measurements.

The central questions are:

1. Can one Bell score in the \((2,2,d,d)\) scenario certify \(d^2\) private
   joint outcomes for every \(d\ge 2\)?
2. If not, can a \((2,3,d,d)\) construction do so, and can its setting count
   be proved optimal?
3. Which broad classes of Bell functionals are obstructed by
   spectrum-permutation degeneracy?

Current exact status:

- if either party has only one input, the complete behavior is local and
  admits a compatible pure realization in which Eve guesses every joint
  output perfectly;
- for \(d=2\), an explicit \(2\times2\) score attains this setting lower
  bound and certifies exactly two private joint bits;
- the standard all-dimensional two-input Fourier-phase strategy has no
  uniform joint input pair;
- perfectly anchoring one additional Bob setting to either of its Alice
  bases fails for every \(d\ge3\);
- a positive-factor theorem identifies a broad first-harmonic polar-linear
  class whose score is blind to cyclic permutations of a relative-unitary
  spectrum;
- the same explicit phase permutations attain the exact maxima of both cyclic
  Bell families in arXiv:2606.21362 while producing nonuniform designated
  outputs for every \(d\ge4\);
- the all-dimensional \(2\times2\) and \(2\times3\) questions remain open.

The strongest currently justified resource interval is therefore

\[
2\leq m_A,\quad 2\leq m_B,
\]

with an all-dimensional single-score construction known at
\(2\times(d^2+1)\) settings (allowing zero-padded projective outcomes on the
three-outcome Bob tests when \(d\ge3\)).  Nothing in this directory proves
that \(2\times2\), \(2\times3\), or any other smaller all-dimensional
scenario is impossible.

The work is divided into logically separate tracks:

- exact constructions and equality analysis;
- active falsification by direct sums, Eve-held flags, conjugation, and
  reducible representations;
- exact and numerical verification;
- literature and priority auditing, deferred until a candidate mathematical
  result exists.

No theorem in this directory should be treated as established until it is
listed as proved in `CLAIMS_LEDGER.md`, supported by a complete proof, and
independently checked.

## Main artifacts

- `manuscript.pdf` and `manuscript.tex`: publication-ready research note;
- `STRUCTURAL_RESULTS.md`: proof-oriented working statement of every result;
- `verify_second_family_d4_exact.py`: independent exact verifier over
  \(\mathbb Q(\zeta_{16})\);
- `test_cases.py`: dependency-free regression suite for \(d=2,\ldots,6\);
- `second_family_discovery.py`: matrix discovery/regression code through
  \(d=12\) (requires NumPy);
- `satwap_ideal_audit.py`: dependency-free ideal-table and third-anchor audit;
- `verify_binary_2x2.py`: exact formal binary SOS check and ideal matrix test;
- `family_certificate.json`: machine-readable all-dimensional formulas;
- `MANIFEST.sha256`: integrity hashes for the frozen research package;
- `PRIOR_ART_AUDIT.md`: targeted primary-source audit;
- `CLAIMS_LEDGER.md`, `ASSUMPTIONS_LEDGER.md`,
  `FAILED_APPROACHES.md`, and `RESEARCH_LOG.md`: scope and provenance.

Run the portable verification suite from this directory with:

```text
python3 test_cases.py
python3 satwap_ideal_audit.py
```

The NumPy regression can be run with any scientific Python environment:

```text
python3 second_family_discovery.py
```

The programs support the written all-dimensional proof; they do not replace
it.
