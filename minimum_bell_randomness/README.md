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

- if either party has only one input, the complete behavior always admits a
  compatible realization with joint guessing probability at least \(1/d\);
- for \(d=2\), an explicit \(2\times2\) score attains this setting lower
  bound and certifies exactly two private joint bits;
- the standard all-dimensional two-input Fourier-phase strategy has no
  uniform joint input pair;
- perfectly anchoring one additional Bob setting to either of its Alice
  bases fails for every \(d\ge3\);
- the all-dimensional \(2\times2\) and \(2\times3\) questions remain open.

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
