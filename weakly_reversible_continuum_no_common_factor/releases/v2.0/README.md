# Version 2.0.0 exact release candidate

This directory freezes the manuscript, raw reaction data, exact rate family,
two distinguished positive integer rate vectors, proof notes, priority audit,
specialist audit packet, and mutually independent symbolic verifiers for:

> **A four-parameter family of reversible three-species mass-action continua
> without a common factor**

No Version 2 DOI had been minted when this candidate was frozen.  In
particular, neither `CITATION.cff` nor the machine-readable metadata invents
or reserves a Version 2 DOI.  DOI metadata can be added only after an actual
archive record exists.

## Principal results

- The fixed support has three species, ten complexes, ten reversible pairs,
  one linkage class, and stoichiometric rank three.
- The exact conic-preserving rate locus is a four-dimensional rational linear
  kernel.  Its positive part is the cone
  `a,b,c,d>0`, `b<c`, `192*a+221*c<154*d`.
- Every rate vector in that cone makes the same compact positive conic a
  continuum of equilibria in the unique positive compatibility class.
- Coordinate gcd one holds on a nonempty Zariski-open subset of this family,
  over both the rationals and their real or complex scalar extensions.
- The frozen Version 1 vector and a smaller primitive vector are exact
  coprime witnesses.  The smaller vector is simultaneously optimal for
  maximum entry and sum among positive integral vectors in this fixed-support
  family.
- The frozen Version 1 ellipse has an exact transverse-stability
  classification certified by Sturm sequences.
- Three species are globally minimal.  Any three-species weakly reversible
  target has at least five complexes; the current ten-complex support is not
  claimed globally minimal.

## One-command exact replay

From this directory, run:

```sh
./reproduce.sh
```

The script creates `.venv-release`, installs the two exact pinned Python
dependencies, and runs every included symbolic verifier.  It performs no
floating-point proof step.  The environment directory is disposable and is
excluded from every archive and checksum manifest.

The frozen outputs and the commands used to build and test the candidate are
recorded in `results/` and `RELEASE_CHECKS.md`.

## Layout

| Path | Contents |
|---|---|
| `source/` | Manuscript Markdown, PDF build inputs, directed rate table, and the cross-verifier wrapper |
| `output/pdf/` | Final Version 2.0.0 manuscript PDF |
| `data/` | Machine-readable theorem, metadata, rates, complexes, and reactions |
| `family/` | Canonical 21-by-20 remainder matrix, family proof note, and exact verifier |
| `strengthening/` | Clean integer optimum, radical decomposition, stability note, and verifier |
| `minimality/` | First-principles lower bounds and exact arithmetic verifier |
| `cleanroom/` | Independent frozen-v1 reconstruction and proof audit |
| `audit_v2/` | Independent 993-line v2 verifier and frozen JSON result |
| `priority_v2/` | Narrow post-solution primary-source priority audit |
| `audit_packet/` | Specialist-facing theorem statements, checklist, and one-page PDF |
| `dist/` | Complete, source, and verifier archives with their own checksum manifest |

`verify_construction.py` and `network.csv` at the release root are the
byte-for-byte frozen Version 1 verifier and reaction table.  They remain at
the root because both the original and family verifiers resolve that exact
relative path.

## Verification architecture

The archive deliberately contains overlapping checks:

1. `verify_release_metadata.py` checks the frozen PDF/source byte anchors,
   rate-table consistency, exact family formulas, and no-false-DOI state.
2. `verify_construction.py` reconstructs and proves the original theorem.
3. `cleanroom/verify_v1_cleanroom.py` independently reconstructs the frozen
   theorem and recomputes the radical decomposition by saturation and ideal
   intersection.
4. `family/verify_family.py` derives the canonical family matrix, rank,
   kernel, positive cone, and generic geometric gcd claim.
5. `strengthening/clean_rates_stability_verifier.py` certifies the smaller
   primitive optimum, both steady ideals, and the exact stability changes.
6. `minimality/verify_complexity_arithmetic.py` checks the finite arithmetic
   consequences of the manuscript's proved lower bounds.
7. `audit_v2/verify_v2_independent.py` redoes the main v2 calculations using
   different normal-form, integer-census, ideal, and Sturm implementations.
8. `source/verify_v2_claims.py` cross-checks the source rate table and replays
   the original, family, and strengthening layers as a final integration
   gate.

The machine-generated result is evidence only for the asserted finite
symbolic computations.  The prose arguments and novelty assessment remain
open to independent specialist review.

## Licenses and disclosure

Code is released under `LICENSE-CODE.txt`; manuscript and explanatory text
under `LICENSE-MANUSCRIPT.txt`.  `AI_AND_HUMAN_VERIFICATION.md` describes the
use of AI-assisted research and the boundary between executable checks and
human responsibility.
