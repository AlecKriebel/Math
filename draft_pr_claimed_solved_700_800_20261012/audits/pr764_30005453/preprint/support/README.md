# A vertex maximum principle for subcritical reinforcement

Alec Kriebel, Independent researcher. ORCID 0009-0001-9320-500X.
Version 1.0, 13 October 2026. Preprint and companion materials: CC BY 4.0.

The note supplies a self-contained alternative proof of unique strictly
positive equilibrium and simultaneous almost-sure coordinatewise
homogenization for countable undirected simple graphs of bounded degree,
positive vertex rates bounded above (their infimum may be zero),
0 <= alpha < 1, and arbitrary finite deterministic positive integer initial
edge counts. Isolated vertices are discarded; the empty edge array is
vacuous. No uniform bound on initial counts is needed.

Literal unrestricted uniqueness among nonnegative equilibria is false:
the alternating matching on Z with unit rates has weights 2 and 0. This
boundary example is credited to the older finite-WARM matching mechanism
and Qin's Remark 1.3. The positive theorem is an explicitly corrected
formulation. No fractional-initialization, spatially uniform convergence,
critical exponent, negative exponent, zero initial edge, unbounded-degree,
loop or multigraph extension is asserted.

Qin, *Homogenization of weakly reinforced Polya urns on countable networks*,
arXiv:2610.11780v1, Theorem 1.1 (submitted 8 October 2026), proves the entire
positive theorem with broader positive real initialization. His connected
formulation extends to countably many components. This note presents a
different vertex proof, without asserting novelty of the shared
power/incidence reduction or complete-limit strategy. Couzinie's 2018
thesis, the 2021 Couzinie-Hirsch results and the finite-WARM construction
are credited. Angel-Hermon-Yao work is reported by Qin; its full manuscript,
public date and full scope were not independently established.

GitHub records PR764's creation on 5 October 2026. This is not certification
of first public availability of the current proof bytes, or priority over
all work. The audits are bounded literature searches, not exhaustive
absence proofs. No first, sole, new-theorem or currently-open claim is made.
The final publisher MATRIX chapter body was not obtained: question wording
was checked against the official hosted pre-publication version.

AI tools were used extensively in development, writing, reproduction,
verification and adversarial review. This is an unrefereed preprint with
no external human peer review or formal proof-assistant certification.

## Contents and dated records

The complete six-page note source is paper.tex. The historical_candidate
directory preserves all 63 original candidate files, including the four
frozen archives. These bytes are historical evidence and have not been
edited. The audit directory contains two distinct fresh mathematical
families, two fresh priority reviews, root derivations, bibliographic
receipts and scope gates.

Historical pending labels, historical prior-work conclusions and disk-space
failures retain their dates; they are superseded by later root and priority
gates where applicable. In particular, MATH_GATE.json predates the priority
review, and PRIORITY_GATE.json predates the separate whole-preprint reviews.
The latter reviews and final publication receipts are subsequently retained
in the repository, outside this noncircular frozen source archive:
https://github.com/AlecKriebel/Math/tree/main/draft_pr_claimed_solved_700_800_20261012/audits/pr764_30005453

The closed MANIFEST.json inventories every regular source-archive file
except itself with size and SHA-256. Verification also rejects extra files,
directories and symlinks. Third-party source bodies are not redistributed;
primary URLs, retrieval hashes and inspected page scopes are recorded.

## Offline verification

Extract source-and-verification.zip into an empty directory. Use Python
3.11 or newer with its standard library. Do not write outputs inside this
closed directory. From it run:

    python3 -B verify_bundle.py
    python3 -O -B verify_bundle.py
    PYTHONOPTIMIZE=2 python3 -B verify_bundle.py

The --integrity-only option checks the complete inventory and fixed
source/review pins without replaying diagnostics. Full replay creates
temporary scratch outside the closed package; TMPDIR may select a suitable
writable location. The wrapper uses explicit exceptions under outer
optimization and forces normally executed children by clearing
PYTHONOPTIMIZE. The historical publication verifier itself runs both normal
and optimized children: normal author assertions are required evidence,
while optimized author assertions are inactive and contribute only
integrity replay.

The replay checks the original publication/archives and stored result
bytes, independent finite-volume and exact strip diagnostics, exact jump
drift and bracket identities, high-precision harmonic-transform bounds and
nonunit offsets, boundary/critical examples, and eight historical negative
controls. The unmodified historical mutation script is run with a storage
wrapper that removes each preceding fixture before copying the next;
the tests and their expected rejection conditions are unchanged.
These computations neither formally prove the infinite stochastic
theorem nor certify historical priority. The analytic proof must be read.

## Compile and rebuild

Compile with a LaTeX installation supporting the listed standard packages,
for example:

    tectonic paper.tex --outdir /absolute/external/pdf-directory

The rendered note is six A4 pages. A new compiler may change PDF bytes.
To reproduce the two ZIPs and matching metadata byte for byte, use the
original deposited PDF and an output directory outside the extracted
source archive:

    python3 -B build_package.py --output-dir /absolute/external/rebuild \
        --pdf /absolute/path/to/original/paper.pdf

Deterministic ZIP entry timestamps and ordering fix archive bytes. The
generated inventory's built_at is a new timestamp; its six listed content
identities should equal the repository's publication inventory.

Upload paper.pdf and source-and-verification.zip as the two Zenodo files
with the exact enclosed metadata. The outer zenodo-upload-kit.zip is a
convenience kit and is not an extra deposit file. The descriptor in that
kit uses flat paths; the separately generated descriptor uses the PDF
output subdirectory. All metadata objects are identical.
