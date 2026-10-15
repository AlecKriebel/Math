# An explicit SU(5) lens-space counterexample to the printed Guadagnini-Pilo conjecture

Alec Kriebel, independent researcher. [ORCID 0009-0001-9320-500X](https://orcid.org/0009-0001-9320-500X). Research note, 2026-10-05.

In full ordinary SU(5), WZW level 5 and shifted level 10, the S3-normalized squared magnitudes are 3475 + 1550 sqrt(5) for L(5,1) and 4025 + 1800 sqrt(5) for L(5,2). Both are positive; both fundamental groups are Z/5. This contradicts Conjecture 7.5 as printed on p.474 of Ohtsuki's collection (volume nominally 2002, published 1 June 2004), conditional on established RT/modular-category and Hansen-Takata formula inputs.

Historical priority remains unresolved. Takahito Kuriya's directly relevant preprint, The LMO invariant and the Guadagnini-Pilo conjecture for lens spaces, could not be obtained. We cannot establish that it does not already contain or circumscribe this result. No firstness, exhaustive novelty clearance or new historical resolution is claimed. See PR95_PRIORITY_QUALIFICATION.md.

## Files

- pr95_note.pdf: research note.
- pr95_note.tex: standalone LaTeX source and embedded bibliography.
- pr95_support.zip: source, authored support, exact programs, provenance and actual recorded runs.
- PR95_PRIORITY_QUALIFICATION.md: priority and source-read boundaries.
- README.md, LICENSE.txt, SHA256SUMS.txt: instructions, license and digests.

## Reproduction

Verify the separately trusted archive digest, extract the ZIP into a fresh directory, then run from its root:

    python3 -E -B verification/run_all.py --output-dir /a/new/empty/directory

Use Python 3.9+ with NumPy installed for the full modular-word route. The two root-lattice programs use only the standard library and may be run separately:

    python3 -E -B verification/independent_checks.py
    python3 -E -B verification/root_lattice_check.py

The runner performs the full payload hash guard, rejecting every symlinked path component beneath the package root, then six fresh positive processes (three routes in normal and optimized modes) and six false arithmetic targets which must fail. Output must be outside the supplied package and empty/absent. It records argv, actual PIDs, UTC times, sanitized Python environment, versions, source snapshots/hashes, exits and full streams. Stored successes are historical evidence, never proof that a new invocation passed. See verification/VERIFY_README.md.

The analytic proof has an exact five-survivor table. The full-weight computation enumerates 126 labels, 120 permutations and 8,001 symmetric entries with seven final polynomial identities. The historical root-lattice field exact_assertions=2005 counts explicit finite checks, not a quality score or distinct theorems. Repeating under -O does not double mathematical evidence. Fresh lattice output includes explicitly diagnostic floating fields; exact identities and positivity do not depend on them.

## Assistance and review

AI tools were used extensively in solving, drafting, literature comparison, reproduction and adversarial validation. The work is unrefereed and has not undergone conventional human peer review. No global historical priority or publication clearance follows from the certificate suite.

The LaTeX source uses standard article/AMS/geometry/booktabs/lmodern/microtype/hyperref packages. Cited source PDFs, extracted texts, source-page images, private audit receipts and credentials are excluded.

# changed bytes
