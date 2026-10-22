# 10400107: a natural quandle space exists

**Recommendation:** `already_solved`, one complete verification response (`1/5`).
No new discovery is claimed.

Ohtsuki's 2002 Problem 5.11 asks for a natural topological space realizing
quandle cohomology. Ishikawa and Tanaka's corrected construction gives such a
CW complex. Its integral cellular chain complex is the normalized quandle
complex, so the cohomology comparison is natural for every abelian coefficient
group in every degree.

The historical caveat matters: Nosaka's literal 2013 mapping-cone definition
does not have the required homology. Ishikawa–Tanaka §6.1, Remark 6.1 identifies
that error and supplies the corrected construction (preprint 2020; publication
2024). This verification uses the correction.

## Files

- `PROOF.md`: exact target, corrected construction, normal forms, CW structure,
  cellular cochain comparison, naturality, and counterchecks
- `SOURCE_STATUS.md`: full provenance, published correction, and duplicate checks
- `APPROACH_LOG.md`: the single completed verification response and checks
- `../controls/check_controls.py`: deterministic, exact, standard-library controls
- `../controls/CONTROL_RESULTS.json`: recorded passing output and limits

Run from this attempt's root:

    python3 controls/check_controls.py > /tmp/10400107-checks.json
    cmp controls/CONTROL_RESULTS.json /tmp/10400107-checks.json
    sha256sum -c SHA256SUMS

The public package contains original verification text and code only. Source
PDFs, imported corpora, and repository snapshots are not redistribution artifacts.

## Principal references

- [Ohtsuki, Problem 5.11, printed p.465](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf)
- [Ishikawa–Tanaka, §6.1 and Remark 6.1, inspected preprint pp.17–18](https://arxiv.org/pdf/1912.12917v2)
- [Published article, Topology and its Applications 345 (2024), 108832](https://doi.org/10.1016/j.topol.2024.108832)

Independent adversarial audit is required before promoting this verification.
