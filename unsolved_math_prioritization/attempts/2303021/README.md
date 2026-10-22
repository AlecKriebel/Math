# Function Theory 3.21: credited prior affirmative result

Rank 853; problem 2303021; AMR-022-3021. Disposition: **already_solved**, authored effort **1/5**. This is a credited literature verification and independent scope audit, not a new solution, human peer review, or formal verification.

FitzGerald, Rodin, and Warschawski, *Estimates of the harmonic measure of a continuum in the unit disk*, Transactions AMS 287(2), 681–685 (1985), Theorem 2, supplies the general bound. See the [published theorem record](https://doi.org/10.1090/S0002-9947-1985-0768733-1), [author-posted text](https://www.researchgate.net/publication/243079947_Estimates_of_the_Harmonic_Measure_of_a_Continuum_in_the_Unit_Disk), [Hayman–Lingham Problem and Update 3.21](https://arxiv.org/pdf/1809.07200v2#page=68), and [Solynin's corroborating publisher abstract](https://www.mathnet.ru/eng/znsl/v144/p146).

## Exact scope

For a nonempty compact connected set E in the closed unit disk, with 0 outside E, let U be the component of D minus E containing 0. Then

    omega_U(0, E intersect boundary(U)) >= asin(diam(E)/2)/pi.

Contact on the unit circle counts. Minor boundary arcs, including the degenerate singleton and the semicircle, attain the bound for each diameter in [0,2]. No exhaustive equality classification is claimed. When 0 belongs to E, the separately declared absorbing convention gives value 1; it is not a classical interior-point harmonic-measure statement at an obstacle point. Connectedness is essential.

Read [the authored result](author/RESULT.md), [the mathematical audit](independent_audit/MATHEMATICAL_AUDIT.md), and [the acceptance](independent_audit/ACCEPTANCE.md). The independent audit accepts the original author freeze unchanged; no correction patch or replacement archive is needed.

## Source-access limits

The author-posted FRW extraction was inspected, but it has damaged mathematical symbols. Hayman–Lingham's complete PDF was independently rehashed and its relevant page freshly rendered and inspected during the audit. Solynin's publisher abstract corroborates the exact formula and domain. FRW PDF bytes and page images, Solynin's full text, and Gaier's original proof were unavailable. The published general theorem and Gaier dependency remain disclosed external mathematical inputs; this package does not reconstruct their full proofs. Source retrieval records describe actual historical access, not a new claim of complete access or current website status.

## Integrity and reproduction

The immutable author archive has 7 members, 9,912 bytes, SHA-256 `a89e522bc8d06a249f96ab4eb0c3351325b3bab9e21876900fab919df3c12e5f`. Its manifest SHA-256 is `3770f2377bd62309dc72af56862be11ad97115964d7efab36ed2014d503ada2c`; its external bootstrap SHA-256 is `e50c19ff0fe418e4c61aeabdcefa50fcb59f322c26a7c735fac94d269b3cd889`.

The immutable audit archive has 18 members, 23,257 bytes, SHA-256 `c5b97acd352e714c894656b7325037e3c9eef3c642fceeea0c0cf3b4fcf6ff64`. Its manifest SHA-256 is `0dfc23c434add4b5d8d23a61712cfd646dfd85afc8439a7f59ad1242f39cf53a`; its external bootstrap SHA-256 is `eb6e912374aa7b880f2226fc5542e1a63338bb7349c63eaf5eceb5dadc018328`.

Independently compare bootstrap bytes to these trusted hashes before executing them. From this directory:

    python -I -S -B FUNCTION_THEORY_2303021_AUTHOR_BOOTSTRAP.py author
    python -I -S -B FUNCTION_THEORY_2303021_INDEPENDENT_AUDIT_BOOTSTRAP.py independent_audit

Repeat with `-O`. Only after the audit gate passes:

    python -I -S -B independent_audit/replay_author.py . author

Repeat with `-O`. This reproduces the 8-positive/38-negative author matrix, including relocation, import-shadow, content-tampering, symlink, inventory, and missing-isolation controls. The separately recorded audit-bootstrap matrix covers 8 positive and 40 negative controls. Both matrices were rerun under normal and optimized outer interpreters for publication. Authorized holders of the exact local corpora can run the authenticated `independent_audit/verify_corpus.py` on the complete catalog, problems, and research-results JSON files; no dataset contents are redistributed.

The gates authenticate frozen bytes and declared scope. Finite diagnostics do not prove the general continuum theorem, and concurrent hostile filesystem writers are outside the tested model. Historical `pending` and `publication_performed: false` fields remain unchanged in frozen artifacts and describe their original checkpoints; the external acceptance and publication record supply the later status.

## Publication boundary

This draft publishes authored mathematics, audits, acceptance, checker code, and public verification metadata only. It contains no copied third-party source documents, source text or images, dataset contents, private sources, private personal data, or private coordination material. The queue changes only this row's Status, Turns, and Findings cells; every other queue byte is preserved. No merge, release, DOI creation, or outreach is part of this checkpoint. GitHub CI must be assessed separately for the exact published head; no reported checks is not a pass.
