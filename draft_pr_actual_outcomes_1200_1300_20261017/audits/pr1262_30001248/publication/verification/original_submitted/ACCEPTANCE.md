# Internal acceptance: sharp triangle modular threshold

Verdict: ACCEPT_CREDITED_TRIANGLE_THRESHOLD_AND_2K2_OBSTRUCTION.
Problem 30001248 / OWR-3473-009.

Review and distribution status: AI-assisted and unrefereed. Acceptance means an
internal AI mathematical audit, not external human peer review or formal
proof-assistant certification. This is a prose edition, not a computational
reproduction package. No new LLT, first-resolution, or priority claim is made.

## Exact accepted scope

For fixed p in (0,1) and ordinary unlabeled triangle count T in G(n,p),
relative modular uniformity max_a|q_n P(T=a mod q_n)-1| tends to zero if
and only if q_n=o(n^2), for all positive integer modulus sequences.
The exact mean, positive standard deviation, span-one convention, quantitative
all-integer LLT error, bounded-differences tails, finite residue window,
Gaussian-grid control and CLT/Fourier necessity argument are all retained.

The CLT is independently obtained from the leading edge projection. Necessity
handles nonmonotone and supercritical sequences via subsequences and the
varying-frequency bound E|Z_n|<=1. Sufficiency handles arbitrarily slowly
subcritical, bounded, composite and unit moduli. No surjective-support premise
or prime-modulus restriction is silently introduced.

The accepted coverage proof contains the two required repairs: n>=3 for
nondegenerate sigma-normalized concentration, and f in L1(R) for the general
shifted-mesh lemma. The exact variance coefficient 12 and leading denominator
sqrt(2) are preserved. Density and Gaussian unit-cell conventions are reconciled.

The complete ordinary-unlabeled 2K2 argument is accepted: its conditional wedge
variance, cancellation of order-n^4 terms, conditional concentration and
pigeonhole atom, central binomial mass and exact unconditional variance yield
an atom larger by order sqrt(n) than a uniform Gaussian LLT permits.

## Credit and bounded review

Sah–Sawhney Theorem 1.1, arXiv:2006.11369v1, is the substantive imported
quantitative LLT; their Theorem 1.3 receives credit for the 2K2 obstruction.
Scott–Tateno's OWR 23/2009 contribution receives historical question and
triangle/modular-result credit. This is no new LLT, first-resolution or
priority claim. The deep source proof is imported, not fully reconstructed.

The independent audit checks core triangle mathematics, the source premise,
density/cell normalization and 2K2 obstruction; it does not certify every
peripheral literature-table assertion. Berkowitz defects are confined to the
specified displays in the byte-identified PDF, not all source versions.
Connected, induced, disconnected and joint counts retain distinct hypotheses.

The adjacent target 30001249 / OWR-3473-010 overlaps the general-subgraph
coverage and counterexample and is not counted as a separate discovery.
No arbitrary disconnected modular-range classification, sparse p(n) result,
or theorem at all induced-copy densities is accepted here.

## Exact report recovery and editorial retention

Recovery scope: all three complete authored mathematical reports were recovered
byte-for-byte and match the previously recorded SHA-256 hashes. The earlier
full evidence packages and their external seals are unavailable in this edition.
Statements below about earlier source inspection and finite checks describe
historical work recorded in those exact reports; they are not claims that the
old supporting packages were recovered or that the checks were newly rerun.

The recovered original coverage proof is 18,430 bytes; the independent
derivation 15,152 bytes; the cross-audit 6,150 bytes. Each matches its original
accepted SHA-256 pin. All mathematical text is retained unchanged through
exact editorial replacement maps. PROOF.md contains the complete coverage
proof; AUDIT.md contains the complete derivation and cross-audit.

Only nonmathematical provenance, historical evidence availability and review/
distribution wording are edited. The earlier 72-member creator and 30-member
audit package seals are not represented as recovered or freshly revalidated.
Finite computational claims in the exact historical reports are not fresh
replays. Newly run edition checks concern byte identity, editorial retention,
strict patch reproduction and Git object identity, not the imported theorem.

No source bodies, datasets, code, raw numerical outputs or private coordination
are included. The eight-file manifest hashes seven non-self members and is
itself independently pinned. Publication remains a separate review decision.
