# Problem 2200006: isolated zeros of sums of squares

**Disposition: unresolved exact extremal problem; five scoped approaches completed.**

The question is Problem 3, attributed to Giorgio Ottaviani and Boris Shapiro, in
Boris Shapiro's 2015 *Problems Around Polynomials: The Good, The Bad and The Ugly…*,
printed page 93. For positive integers (k,l), determine the largest number

\[
M(k,l)=\widetilde\#(2k,l)
\]

of isolated real zeros of a real polynomial of degree exactly (2k) that is a
finite sum of squares of real polynomials of degree at most (k). No restriction
to a zero-dimensional complex common-zero set is present.

## What is established here

- The proposed answer (k^l), stated separately as Conjecture 4, is false. This
  is **prior work**, credited to DannyExperiments' public release of 10 August
  2026, DOI [10.5281/zenodo.21875290](https://doi.org/10.5281/zenodo.21875290).
  Its explicit quartic has exactly 1,152 isolated real zeros in ten variables.
  A self-contained verification is in `PROOFS.md`.
- The exact maximum asked for in Problem 3 has **not** been determined. In the
  concrete counterexample parameter pair, this packet proves only
  (1152\le M(2,10)\le29525).
- The packet verifies the credited even-degree lower-bound family, explains the
  failure of naive complex Bézout, proves a general perturbation/topological-degree
  upper bound, and gives exact product controls. No novelty or priority is claimed.
- A September 2026 unrefereed note advertises further low-dimensional cases.
  Its landing page was inspected; its PDF returned HTTP 403. Those advertised
  claims are **not** certified here and are not used in any proof.

## Reading and replay

1. `PROOFS.md`: precise hypotheses, complete proofs, and the remaining gap.
2. `APPROACHES.md`: five substantive approach families and their limits.
3. `SOURCES.md` and `SOURCE_METADATA.json`: source status and inspection evidence.
4. `STATUS.json`: machine-readable, narrowly scoped disposition.
5. Run `python3 verify_math.py` for exact integer/rational controls, or
   `python3 verify_package.py` to check the package manifest and replay receipt.

Both scripts use Python 3.10+ standard library only and work independently of
the current working directory. They do not contact the network or need the
source materials. `results.json` is the frozen deterministic replay output.
Finite checks corroborate the written proofs; they are not proofs of universal
claims or a determination of the maximum.

This is an authored research record prepared for independent adversarial review.
No human peer review, formal proof-assistant certification, complete literature
search, or proof of worldwide openness is asserted. The author freeze precedes
any later independent audit; a later review should preserve these historical bytes.
Only authored mathematics/code and public verification metadata are included.
No source PDF, source extract, source code from other repositories, dataset
contents, private correspondence, or private coordination file is included.
