# Function Theory 7.54: partial coefficient bounds

**Unresolved.** This is a reproducible partial investigation of Rippon's question about the coefficients of iterates of `exp(tz)-1` at `z=-1`. It claims neither a full solution nor novelty.

- `proof.md`: exact recurrence, all-iterate finite-degree and diagonal-band bounds, complete bounds for the first four iterates, and the precise gap.
- `ATTEMPTS.md`: five substantive approaches and their outcomes.
- `SOURCE_GATE.md`: primary-source identification, wording correction, and limits of the literature/prior-attempt checks.
- `verify.py`: dependency-free exact verification.
- `verification_output.json`: expected deterministic output.
- `SHA256SUMS`: frozen-file checksums.

Reproduce from this directory with `python3 verify.py`; verify file integrity with `sha256sum -c SHA256SUMS`.
