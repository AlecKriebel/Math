# Quasi-conical domains with pure point Dirichlet spectrum

**Full existential proof candidate for problem 30005613 / OWR-14297736-021, rank 800, after 2/5 substantive approaches. Two independent adversarial mathematical AI reviews returned PASS without corrections. External expert review and historical novelty remain pending.**

For each integer d≥2, the candidate constructs a connected open quasi-conical tower of expanding cubes, joined through positive windows tending to zero, whose Dirichlet Laplacian has a complete orthonormal eigenbasis. Its spectrum and essential spectrum are [0,∞); zero is not an eigenvalue, and both absolutely continuous and singular continuous spectral subspaces vanish. Pure point spectral type does not mean every real number in the spectrum is an eigenvalue.

**Both cube widths and apertures are chosen inductively.** This is not a theorem for arbitrary preassigned widths, smooth boundaries, Neumann conditions, or positive-length connecting passages. No numerical aperture modulus is supplied.

The argument transports whole finite spectral clusters into fixed-rank norm limits and proves completeness on a dense repeated test schedule. The geometry and finite-window convergence are credited to Krejčířík and Lotoreichik, [Quasi-conical domains with embedded eigenvalues](https://doi.org/10.1112/blms.13113), specifically Sections 2.2 and 3 of the [accepted author version](https://arxiv.org/abs/2205.08172v2).

## Read the mathematics

- [Frozen complete candidate](author/PROOF.md) and [two approaches](author/APPROACHES.md)
- [First independent audit](audit/AUDIT.md) and [independent analytic reconstruction](audit/ANALYTIC_CHECKS.md)
- [Second targeted independent audit](second_audit/SECOND_AUDIT.md), including the dimension-two capacity limit, multiplicities, strong exhaustion and the completeness diagonal
- [Exact current verdict and limitations](VERDICT.json)
- [Author source metadata](author/source_metadata.json) and [first audit's source checks](audit/SOURCE_CHECKS.md)

This is AI-assisted, unrefereed work, not human peer review or formal proof certification. The frozen source review records the question as open in Open Problem 1 of the [September 2026 survey](https://arxiv.org/abs/2609.28602v1). Bounded searches do not establish historical priority or complete current literature coverage.

## Reproduce

Python 3 standard library only:

```sh
python3 -B verify_publication.py
python3 -O -B verify_publication.py
```

The wrapper verifies the recursive inventory, sizes and SHA-256 hashes, every manifest, all three untouched archives and their 31 extracted-file matches, and the embedded author snapshot. It replays the author checker (4,187 finite controls), first audit in portable mode (2,911) and with the author ZIP (2,923), and second audit (2,304 exact tail checks). The optional author-archive checks account for the 12-check difference. The author and first portable output are reproduced byte-for-byte; the second input verification is compared to its recorded frozen fields.

These are finite arithmetic and integrity checks, not formal verification of the infinite-dimensional PDE theorem. The wrapper launches frozen checkers in isolated, non-optimized Python children with assertions enabled, including when invoked with -O or PYTHONOPTIMIZE. It works after relocation and from an unrelated working directory.

Add `--queue /path/to/unsolved_math_prioritization/QUEUE.md` to verify the whole queue hash and reconstruct the original queue by reversing exactly this row's Status, Turns and Findings changes. All other bytes, including the existing stale header, are preserved. No queue generator is run.

Full optional input replay additionally accepts `--catalog`, `--problems`, `--research-results`, and `--source-dir`. The last directory must contain paper.pdf, report.pdf and survey.pdf matching the published source hashes. With all inputs, the first audit has 2,944 checks. These external source inputs are deliberately excluded from this package; when absent the wrapper reports NOT_RUN for that stage.

The original author, first review and second review packets and their ZIPs are immutable. Their pending-audit or no-remote-write statements remain creation-time records. This later wrapper records both PASS reviews without altering historical evidence. Source PDFs, extracts, images, raw corpora and private coordination files are excluded. Draft research checkpoint only; no merge, release, DOI deposit or outreach.
