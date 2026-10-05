# 30001860: audited scoped classical-group bounds

**Disposition: unsolved, five approaches retained (5/5), zero full resolutions.**
Assigned rank 707; OWR-11129-006, *Asymptotic Proportion of Q in Classical Groups*.
This is a draft research package, not a claim of novelty, global openness, human refereeing, or a full asymptotic-value solution.

## Read this guide first

The original author files in `release/` and independent audit in `independent_audit/safe/` are preserved byte for byte. Historical statements there such as "audit pending" and "remote_writes: false" describe their frozen preparation stage. The completed independent automated audit is in [AUDIT_REPORT.md](independent_audit/safe/AUDIT_REPORT.md); its [scope clarifications](independent_audit/safe/SCOPE_CLARIFICATIONS.md) control interpretation of the frozen author files.

In particular, the heading "Exact rank-two and quotient controls" in PROOF.md section 7 must be read as **"Exact dimension-two and quotient controls."** GL_2 and SL_2 have natural dimension 2 and semisimple Lie rank 1. GL_3 and Sp_4 are the Lie-rank-two controls. LNP's positive lower bound requires Lie rank at least 2 and must never be applied to SL_2, whose target proportion is zero.

## Strongest scoped result

For even-order g in a natural classical matrix group on an N-dimensional module, Q requires

    N/3 <= dim ker(g^(ord(g)/2) - I) < 2N/3.

The strict upper endpoint is essential. Let p(G)=|Q(G)|/|G| and use natural logarithms. For every odd prime power q, the audited infinite proof gives:

- GL_N(q) and the full unitary **isometry** group U_N(q), N>=2: p(G)<=min(1,512/log N).
- Sp_(2r)(q) and SO_(2r+1)(q), r>=2: p(G)<=min(1,512/log r).
- SO^+_(2r)(q) and SO^-_(2r)(q), r>=2: p(G)<=min(1,1024/log r).

These bounds are uniform in odd q. Combining them with Lübeck–Niemeyer–Praeger's (LNP) published lower bound 1/(5000 log_2(ell)), for semisimple Lie rank ell>=2, gives the scoped Theta(1/log ell) order of magnitude. For GL/U, ell=N-1, so this combination requires N>=3. For the other listed groups, ell=r>=2.

For SL_N(q)<=H<=GL_N(q) and SU_N(q)<=H<=U_N(q), the finite-index transfer gives only Theta_q(1/log N) as N tends to infinity with q fixed, using the LNP lower bound for N>=3. It establishes no q-uniform upper bound for these determinant-constrained intermediates. Rank growth and field growth at fixed rank are different limits.

The proof explicitly imports the LNP maximal-torus counting transfer, including the connected reductive algebraic group/Frobenius hypotheses and the natural-module conventions. The signed Weyl model handles the extra odd-orthogonal fixed line and the even-orthogonal parity conditioning separately. Finite enumeration, coefficient checks, and numerical stress tests are controls, not proofs of the infinite estimates.

## Statement, source, and remaining limits

The inspected OWR source literally prints O(log N). This is vacuous for a probability, since p(G)<=1. The nontrivial reciprocal-log target is separately sourced to the cited LNP discussion; the printed question is not silently repaired.

No leading equivalent, limiting log-scaled probability, oscillation classification, or full asymptotic value is obtained. Uniform SL/SU, similitudes/conformal forms, disconnected orthogonal groups, Spin/half-spin forms, and central/projective predicate completion remain outside this proof. The arbitrary-lift counterexample is distinct from LNP's separately defined projective image-set predicate.

The public catalog body and raw prior AI records were unavailable. The OWR source statement was checked directly, but the assigned catalog identifiers were not independently matched to an accessible current catalog body. Bounded historical/literature searches are not exhaustive absence certificates. Source retrieval and inspection limits, including the audit's LNP web-reader failure and use of a matching existing local PDF, remain recorded in the unchanged source metadata and audit.

Public references:

- LNP, *Finding involutions in finite Lie type groups of odd characteristic*, Journal of Algebra 321 (2009), 3397–3417: [DOI](https://doi.org/10.1016/j.jalgebra.2008.05.009), [inspected author version](https://www.math.rwth-aachen.de/~Frank.Luebeck/preprints/powerinvReprint.pdf).
- *Computational Group Theory*, Oberwolfach Reports 8 (2011), 2113–2161, problem session p. 2154: [primary publication](https://ems.press/journals/owr/articles/11129), [DOI](https://doi.org/10.4171/OWR/2011/37).

## Portable verification

From this directory, with standard-library Python 3:

    python3 -B verify_release.py --self-test
    python3 -B -O verify_release.py --integrity-only --self-test

The first command verifies exact file and directory boundaries, frozen SHA-256/byte bindings, audit-to-author bindings, controlling status, and the package manifest; then reruns the author's complete bounded controls and independent controls using temporary output paths. Author results must match exactly. Independent JSON must match after removing only its elapsed_seconds timing field. It also applies real file, metadata, and boundary corruptions to temporary copies and requires rejection.

The optimized command reruns only explicit integrity and corruption checks. It does not represent assertion-disabled execution as mathematical verification. The verifier cannot establish that a prose theorem is correct; consult the proof and independent audit. Manifest hashes are integrity bindings, not digital signatures.

The independent controls include five exact matrix counts, 198 coefficient comparisons, 28 orthogonal field/rank cases, 255 avoidance identities, 105 cyclic-color cases, 406 exact cycle-pointing cases, and 2,000 numerical dyadic stress cases. Negative controls target the endpoint, 2-adic layers, orthogonal parity, unitary arithmetic, rank threshold, projective lifts, and missing avoidance decay.

Only authored mathematics/code and public verification metadata are included. No source PDFs, extracts, images, raw catalog/prior-AI records, or private coordination files are distributed. The repository queue edit is restricted to this problem's Status=unsolved and Turns=5/5; Findings, Chat, DOI, all other rows, and the existing header are preserved.
