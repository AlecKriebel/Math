# Function Theory 6.86: qualitative fixed-point improvement

UnsolvedMath 2306086 / AMR-022-6086; rank 687. Queue disposition: `claimed_solved`, five substantive approaches (`5/5`), strictly for the qualitative theorem below.

For the normalized real-coefficient univalent class, define

    A_f(z) = (1-|z|^2) f''(z)/f'(z) - 2 conjugate(z).
    M(z) = max_f |A_f(z)|.

For every fixed nonreal point z in the unit disk, **M(z)<4**, uniformly over the entire class. Consequently the source's centered disk radius can be strictly decreased at each such point. On the real diameter M(x)=4; at nonzero real points the classical displayed radius is sharp. At zero that displayed expression degenerates to zero.

The proof combines the area-theorem equality case, Koebe transforms, real-slit rigidity, and compactness. It also gives a gap uniform on each compact subset away from the real diameter, a real-automorphism reduction, two exact lower bounds, and a convex-hull obstruction.

**No explicit positive improvement, sharp formula, or full variability region is determined. Novelty and current literature status are unverified.** The source does not explicitly require sharpness, so the literal qualitative fixed-point improvement question is answered; this does not settle every quantitative interpretation. The status is an audited, scoped claim, not a formal proof certificate or a claim of a new discovery.

Read [SCOPE_CLARIFICATION.md](SCOPE_CLARIFICATION.md) first. It supersedes historical pending-audit/partial labels only as to the qualitative question and corrects two presentation details without changing any frozen byte.

## Evidence and provenance

- [Full authored proof](author/PROOF_PARTIALS.md) and [five-approach record](author/APPROACH_LOG.md)
- [Complete independent adversarial audit](audit/INDEPENDENT_AUDIT.md)
- [Source verification](author/SOURCE_VERIFICATION.json) and [independent source recheck](audit/SOURCE_RECHECK.json)
- [Publication binding](BINDING.json), [manifest](PUBLICATION_MANIFEST.json), and [research log](RESEARCH_LOG.md)
- `author/` and `audit/` preserve all 16 frozen files exactly. `archives/` preserves both safe ZIPs exactly.

## Portable verification

Python 3, SymPy, NumPy and SciPy are required for the complete replay. The authored exact controls alone use only the standard library. From this directory run:

    python3 -B verify_publication.py --replay --numerical --selftest
    python3 -O -B verify_publication.py --replay --numerical --selftest

Without `--numerical`, replay omits the 16 floating-point reproduction checks. The verifier uses isolated temporary copies and rejects extra files, malformed manifests, symlinks and claim inflation. It checks 3,558 authored exact controls in both modes; the independent audit has 80 binding/replay/symbolic checks, plus 16 non-certified numerical-reproduction checks when requested. The numerical optimizer is not rerun, and ODE reproduction is not interval certification or a sharp-bound theorem.

Primary scope reference: Walter K. Hayman and Eleanor F. Lingham, *Research Problems in Function Theory (New Edition)*, [arXiv:1809.07200v2](https://arxiv.org/abs/1809.07200v2), revised 2018-09-21; publicly marked draft copy. The 2018 progress statement does not establish present-day openness. Dataset hashes are manifest-observed public metadata; full dataset corpora and the selected upstream AI report were not inspected.

This package contains authored mathematics/code, generated tests, the complete safe audit and public verification metadata. It excludes source PDFs/text/images, dataset contents, private sources and private coordination files. Only this problem's Status, Turns and Findings cells change in the existing queue; all other bytes are preserved.
