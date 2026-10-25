# Asymptotic LOCC dense coding with the symmetric four-qubit W state

Alec Kriebel, independent researcher. ORCID: https://orcid.org/0009-0001-9320-500X.

This research note answers the specific asymptotic local-unitary question in Bruß and collaborators' 2004–2005 distributed dense-coding model. Two senders encode independent messages and send one qubit each to different receivers. After routing, the decoding cut is A1B1:A2B2. Receiver-to-receiver classical communication and collective operations inside each laboratory are allowed.

The proved achievable sum-rate supremum is at least `3/2 + h2(1/4) = 2.311278124459...` bits per resource copy; every strictly interior pair of the displayed cqMAC region is achievable with uniform average error tending to zero. In particular `(9/8,9/8)` has sum `9/4 > 2`. This resolves the original W-state LOCC-DC classification in that model. It is a lower bound, not an exact optimal capacity. The construction gives no one-copy, zero-error, maximal-error, or explicit finite-blocklength guarantee.

The Bell decomposition, Bell forwarding, general multiple-access dense-coding framework and cqMAC theorem are established ingredients, attributed in the paper. PRIORITY_AUDIT.md records the bounded literature comparison and access limitations. No categorical worldwide firstness or continued global openness through 2026 is asserted.

AI tools were used extensively in solving, drafting and verifying the result. AI adversarial reviews do not constitute conventional human peer review or refereeing. The note is an unrefereed preprint.

## Files

- `w4_locc_dense_coding.pdf`: research note.
- `w4_locc_dense_coding.tex`: standalone editable source with inline bibliography.
- `verify_channel.py`: portable exact rational verifier, Python 3.9 or later, standard library only.
- `verification_results.json`: recorded successful verifier output.
- `PRIORITY_AUDIT.md`: original-target provenance, credited ingredients, corpus comparisons and limitations.
- `LICENSE.txt`: CC BY 4.0 license notice for this package's original material.
- `SHA256SUMS.txt`: file digests for the seven files above; excludes itself to avoid self-reference.

## Reproduce the finite algebra

From this directory run:

```sh
python3 -E -B verify_channel.py
```

Expected status is `PASS_EXACT_FINITE_CHANNEL_ALGEBRA`, with 551 checks. The verifier refuses Python optimization (`-O` or `-OO`). It reconstructs the four-term W ket in A1,A2,B1,B2 order, the Pauli encodings, all 64 unnormalized Bell branches, and their conditional/full averages using `fractions.Fraction`. Power sums through matrix dimension 16 certify the stated spectra exactly. The entropy coefficients in the basis `(1, log2(3))`, original marginals, the exact inequality `27 < 32`, and the particular both-Bell instrument are checked. Floating-point rates are for display only. This computation does not certify the coding theorem, priority, or the whole proof by itself.

The portable verifier is adapted from ROOT's independent pre-author-code reconstruction, repository audit commit `f203c604c8db564423fbd3f6b5f367580745b9f2`, path `draft_pr_publication_program_20260930/audits/pr80_30000177/ROOT_channel_check_20261004/check_channel.py`, original SHA256 `aba7caad269a39aaaebb28c0914678eaa31b00a4b9b57a6f9c01e98d5e52d99e`. The adaptation adds an explicit optimization guard and reports its provenance; it is not a claim that a new independent reconstruction was made after manuscript preparation.

## Rebuild the PDF

The source is standalone. With Tectonic installed:

```sh
tectonic --untrusted w4_locc_dense_coding.tex
```

A standard LaTeX installation can instead use `pdflatex` twice. Fonts and compiler versions can alter PDF bytes; the source, theorem and exact verifier determine the reproducible content. No external images, bibliography files, private source PDFs, credentials or unpublished datasets are required.

## Provenance

Original submitted result: https://github.com/AlecKriebel/Math/pull/80, immutable head `dcfeb5d8ad68b397ec509c70e85c6fca46cd01e3`, problem `30000177` / `OWR-785-003`. Its submitted QUEUE status was literally `claimed_solved`, historical substantive-turn ledger `1/5`. Verification and publication preparation did not require new central proof-search turns. Original candidate SHA256: `fb8646bbe3cd8512ec7736fc180fa08a76740ac8b0dbb60b539a0320328c6404`.

Licensed source papers are cited and linked, not redistributed. This package contains the author's original note, code and audit summary.
