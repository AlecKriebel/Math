# Stationary SIS thresholds: scoped partials, 30003676

**Unsolved, 5/5 approaches. NO RESOLUTION of the general conjecture. No novelty claim.**

**The frozen author report alone remains REVISE_REQUIRED. The audit's PASS applies only to the frozen author package read together with the mandatory [AUTHORITATIVE_CORRECTIONS.md](independent_audit/AUTHORITATIVE_CORRECTIONS.md). That overlay takes precedence over the specified passages in REPORT.md. Do not read or cite the report's summaries without it.**

## Mandatory interpretation

1. C1: Fix complete-graph weights w_uv=a/N independently of theta, and set beta=theta*a. The restricted theorem includes the critical case. Holding beta fixed in beta/(theta*N) while changing theta is not the model.
2. C2: Choose one deterministic threshold sequence before quantifying over all sufficiently slowly vanishing immigration sequences and all fixed positive gaps. Neither the source nor this package supplies a universal numerical slow scale. The subexponential condition log(1/epsilon_n)=o(n) belongs only to the restricted constructions proved here.
3. C3: The negative control epsilon_N=exp(-N^2) is fast-vanishing immigration and exceptionally rare external seeding. It is not fast seeding and does not refute the original conjecture.

## Retained results and limits

The [complete proofs](author/safe/PROOFS.md) establish finite-chain attractiveness and subcritical upper certificates; exact complete-graph stationary asymptotics; a connected clique/dimer construction separating prevalence onset from inverse spectral radius; exact graphical-duality identities; and an abstract monotonicity obstruction. The connected spectral example itself has a sharp threshold. The abstract Bernoulli example is not an SIS realization. Neither is a counterexample to Aldous's original conjecture.

The [independent audit](independent_audit/AUDIT.md) accepts these scoped results with the overlay. A graph-uniform lower-tail argument with the original quantifiers remains missing. This is an unrefereed mathematical investigation and finite audit, not formal proof-assistant certification. Public-listing and literature findings have the bounded scope recorded in the audit.

## Frozen identities

- Author archive: 22,001 bytes; SHA-256 70191b3887e8863701651cdb54382958e1f8190fd889889a2ed81c46f16ee6a6
- Author manifest: SHA-256 bb24c27fef83fcc14106cbcc068a02f740c0b35385b79e6c7799371764ea9bdb
- Audit archive: 27,205 bytes; SHA-256 00b486a241fb56a1fb9a935756384e1a0943ec8669fb61ffa825fdf2db3ee325
- Audit manifest: SHA-256 2afb4fb797ff8db6b265ba97799681b31c29219d709b3a0b83e8e5cebb0828aa

All 21 frozen files and both original ZIPs are unchanged. Historical no-remote-write labels refer to creation of those freezes. Only authored proofs, code, audit, outputs, and public verification/source metadata are included. Source PDFs, extracts, screenshots, raw datasets, private sources and coordination are excluded.

## Portable offline replay

Python 3.10 or later, standard library only. From any working directory:

    python3 /path/to/30003676/verify_publication.py --expected-manifest <SHA256_FROM_PR> --queue /path/to/unsolved_math_prioritization/QUEUE.md

Use the external publication-manifest SHA-256 recorded in the PR as the trust anchor, not a freshly computed value from an untrusted checkout. The wrapper checks exact inventories, hashes, sizes, both archive-to-directory identities, the mandatory overlay, and optional queue bytes. It replays 436 exact author checks byte-for-byte, 1,407 exact independent assertions and eight wrong-model controls, the author and audit integrity checks, and a deliberate false-assertion execution control. Floating diagnostics are compared with explicit tolerances and remain diagnostics, not asymptotic proofs. The wrapper rejects optimized Python (-O/-OO or PYTHONOPTIMIZE) because disabled assertions cannot count as verification.

## Queue scope

Exactly two cells change in rank 738 / 30003676: Status queued to unsolved, and Turns 0/5 to 5/5. Findings, Chat, DOI and every other byte remain unchanged. PUBLICATION.json records identities computed from the actual base and updated queue bytes. Legacy SHA/size text embedded at the start of the queue remains untouched and is not actual file metadata.
