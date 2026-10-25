# Kourovka Notebook 16.63

## An explicit odd-order p-group with as many automorphisms as elements

**Version:** 1.1.0 · 15 September 2026  
**Archive DOI:** [10.5281/zenodo.22770864](https://doi.org/10.5281/zenodo.22770864) (assigned for this edition; Zenodo publication pending when prepared)  
**Author:** Alec Kriebel · [ORCID 0009-0001-9320-500X](https://orcid.org/0009-0001-9320-500X)  
**Result:** an explicit finite group satisfies

```text
|G| = |Aut(G)| = 1009^52359.
```

Here `Aut(G)` is the **full** automorphism group. The group is the BCH group of an explicit rank-31 Lie ring modulo `1009^1689`, with nilpotency class at most `846 < 1009`.

- [Paper (PDF)](report/kourovka_16_63.pdf) · [editable LaTeX](report/kourovka_16_63.tex)
- [Fixed publication snapshot](https://github.com/AlecKriebel/Math/tree/kourovka-16-63-v1.1.0/kourovka_16_63)
- [Zenodo copy-and-paste metadata](publication_v1_1/zenodo/COPY_PASTE.md)
- [Public paper page](https://aleckriebel.github.io/Math/papers/kourovka-16-63/)
- [Independent verification report](audit/VERIFICATION_REPORT.md)
- [Explicit group description](data/group_lie_presentation.json)

**Status:** computer-assisted proof independently checked by separate AI audit agents and exact computational reproduction. No external human peer review or proof-assistant formalization is claimed. Neither the prime nor the order is claimed minimal.

## Reproduce the computation

From this folder, run:

```sh
python3 scripts/resume.py
```

Requirements: Python 3 and a GCC or Clang C++17 compiler supporting `__int128`. Select a compiler with `--compiler /path/to/compiler`. The command installs nothing and uses no network. It rebuilds the C++ verifier, reconstructs all brackets and the complete derivation matrix, replays the Smith certificate, checks exhaustive small-group controls, and rejects a deliberately corrupted certificate. Expected final status:

```text
REPRODUCTION_PASSED: exact certificate checks and corrupted-certificate rejection.
```

The C++ reconstruction reads only the proposed pivot plan; each pivot is checked rather than assumed. A failed build cannot fall back to an old binary. Its main exact matrix requires approximately 112 MB.

For full Python regeneration, with NumPy and SymPy installed:

```sh
python3 scripts/resume.py --full
```

Two additional independently written audits are provided:

```sh
python3 audit/check_finite_flag.py
python3 audit/independent_exact_audit.py
```

The first uses the standard library. The second uses NumPy only to read and compare the supplied NPZ arrays; its mathematical arithmetic is unbounded Python integer arithmetic. It reconstructs the matrix and checks the Smith plan at precision five, distinct from the original precisions twelve and six.

Successful fresh full regeneration used Python 3.12.14, NumPy 2.3.5, SymPy 1.14.0, and Apple Clang 21.0.0 on macOS 26.6.2 arm64. The default path also passed with Python 3.14.6. An indentation-only correction makes the original C++ source pass strict Clang warnings. AddressSanitizer and UndefinedBehaviorSanitizer checks also passed.

## What establishes the equality

An asymmetric lattice and rigid finite-field flag force **every** finite Lie-ring automorphism into an integral logarithm–exponential domain. A precision-preserving bijection identifies the full automorphism set with the complete kernel of a derivation matrix. The exact Smith certificate for this `14415 × 961` matrix has rank 931, nullity 30, and valuations:

| Valuation at 1009 | 0 | 1 | 2 | 3 | 4 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Multiplicity | 87 | 55 | 758 | 6 | 25 |

Their sum is 1689. At depth `i >= 7`, the full **Lie-ring** automorphism group has order `1009^(30*i+1689)`. At `i = 1689`, this equals the ring's order `1009^(31*i)`. The class bound `846 < 1009` permits the finite Lazard correspondence, which preserves the full automorphism group.

The proof closes the possible finite-precision gap: 30 independent inner derivations give an exact rational rank upper bound, and the 931 verified pivots give the matching lower bound. Higher-valuation invariants cannot be hidden beyond the computation's precision.

The executable checks do not replace the finite-field stabilizer proof, lifting lemma, analytic argument, or Lazard theorem. Independent written audits inspect those steps. No Cayley table or enumeration of the enormous full automorphism group is claimed.

## Explicit group data

`data/group_lie_presentation.json` specifies the ordered basis, 199 nonzero skew-half bracket coefficients, modulus, and canonical finite BCH rule through bracket length 846. Parse its integers exactly: some exceed `2^53`. The paper fixes all seven raw transvectants, the unimodular basis change, and weights `(0,0,1,2,...,2)`.

## Publication revision

Version 1.1.0 adds standalone versioned artifact links, author contact details, two mathematical clarifications, and scope-based audit wording. All mathematical data and verification scripts are unchanged from the independently checked first publication. The external AI feedback supplied for this revision was text only; its linked checker was not available and is not counted as a new local verification.

## Package map and integrity

- `report/`: publication manuscript and LaTeX source.
- `scripts/`, `data/`: supplied construction, verification code, and exact certificates.
- `audit/`: independent reviews, new verification implementations, fresh reproduction evidence, and input-integrity checks.
- `logs/`: supplied historical logs plus the latest default run in `resume_*`; fresh full regeneration is recorded separately in `audit/reproduction/`.
- `notes/`, `literature_ledger.*`: original research provenance.
- `RESEARCH_LOG.md`, `progress.json`: publication and verification checkpoints.
- `SHA256SUMS`: hashes for this publication package. Reproduction intentionally changes run logs; check hashes before running it.
- `audit/ORIGINAL_SHA256SUMS`, `audit/original_progress.json`: original delivery provenance. Original hashes were checked before changes; they do not describe the reformatted edition.

To rebuild the paper, use Tectonic from this folder:

```sh
tectonic -X compile report/kourovka_16_63.tex
```

Alternatively, run two or three `pdflatex` passes in `report/`. TeX is not required for the mathematical verifier.

## Attribution

The construction, proof development, and initial verification software were generated using ChatGPT-6 Astra Pro. Separate Codex sessions performed additional AI-assisted reviews and exact computational checks. These checks do not constitute external human peer review or proof-assistant formalization.

The underlying Lie-algebra template is credited to Omirov–Ruan, arXiv:2605.04602v1, Theorem 4.8. The manuscript independently supplies the integer normalization and finite-characteristic arguments. It develops the asymmetric lattice and exact full finite-automorphism count. The original finite Lazard correspondence is credited to Lazard, with its applicable hypotheses checked in Cicalò–de Graaf–Vaughan-Lee (2012), pp. 433–434.

No individual was contacted. The literature search found no earlier resolution of the exact equality question, but search absence does not establish absolute priority. See the literature audit for sources and limits.
