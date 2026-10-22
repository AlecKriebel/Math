## Accepted conditional partial result

For an ordinary real-valued additive function f with density-zero strict
decreases, suppose that for one fixed real c the residual f−c log is
approximable by periodic sequences in density. Then f(n)=c log n for every
positive integer, with c≥0. A sufficient condition is
Σ_p min(1,|f(p)−c log p|)/p<∞. Values at higher prime powers may be arbitrary
finite real numbers; complete additivity is not assumed.

The complete written proof uses a bounded arctangent transform, vanishing
mean variation, fixed-period averaging without a period-dependent loss,
tightness excluding either endpoint, and fixed coprime-dilation witnesses.
The prime-tail argument treats large-prime squares and finite-small-prime
valuation truncation separately, with the order of limits explicit.
Two lifting lemmas and all mathematical boundary examples are retained.
Absolute o(1) logarithmic approximation off o(X) exceptions already suffices,
even when its slope and offset vary with X, because the offset cancels.

The unrestricted EP 1122 / 2503 problem remains unresolved by this work.
Density-zero decreases alone have not been shown to imply the periodic
residual premise, the sufficient prime-tail condition, or absolute
vanishing-error approximation. No unrestricted counterexample, novelty,
priority, or exhaustive current literature-status claim is made.

## Full proofs and independent audit

The original mathematical Sections 1–4 are retained verbatim in PROOF.md,
and the independent reconstruction in mathematical Sections 2–6 is retained
verbatim in AUDIT.md. No mathematical correction was required. The written
proofs are self-contained; no computational premise or external analytic
theorem is omitted. Boundary examples include a bounded parity defect,
isolated exact-valuation defects with positive decrease density, a slowly
varying divergent scalar slope, and the arctangent endpoint obstruction.
None is a counterexample to the unrestricted density-zero problem.

Historical independent supporting checks include 729 exact rational variation
tests, 1,364 period-average contractions, 16,388 finite bad-set dilation
checks, 555 ordinary-additive coprime-pair checks with arbitrary prime-power
values, 512 valuation-truncation checks, and 27 finite tail/Markov checks.
The auditor independently reconstructed all 24 candidate prime-power
examples and the candidate's stated aggregate finite fields. Eight
mathematical overclaiming controls and fifteen inventory controls were
rejected in each of normal, -O, and -OO modes. The candidate program was
inspected as inert text but never imported or executed by the auditor.
Finite checks support the written proofs; they do not prove infinite
implications by extrapolation. Historical receipts were byte-reauthenticated
during edition preparation; mathematical programs were not rerun then.

## Versioned source context and publication boundary

[Erdős, On the distribution function of additive functions](https://users.renyi.hu/~p_erdos/1946-06.pdf),
Annals of Mathematics 47(1) (1946), identifies ordinary additivity and the
exact density-zero conjecture. [Mangerel, Additive functions in short
intervals, gaps and a conjecture of Erdős](https://arxiv.org/abs/2108.12351v1),
arXiv:2108.12351v1, supplies contextual comparisons whose normalized error
and scale-dependent parameters do not provide the missing absolute-scale
bridge. These comparisons are not complete external-paper proof audits and
are not theorem dependencies of the authored proofs. Historical retrieval,
text inspection, re-extraction, and visually inspected pages are separately
recorded. No new scholarly-source retrieval or inspection occurred during
edition preparation, and no later-version or global literature claim is made.

This AI-assisted work is unrefereed. Acceptance means an independent internal
AI audit; no external human peer review, journal acceptance, or formal
proof-assistant certification is claimed. Only eight authored proof, audit,
acceptance, provenance, and public-verification-metadata files are added
under unsolved_math_prioritization/attempts/2503. Copied source PDFs/text,
executable code, raw computational certificates, and private coordination
material are excluded. Ordinary authored proof formulas and mathematical
examples are included. QUEUE.md and all unrelated paths remain unchanged.

Base commit: `4b27092a448d53b61408355ce44ec38d103a1ce4`.

## Exact public-file identities

- `ACCEPTANCE.json`: 2,730 bytes; SHA-256 `851512878b9fcc36e8504033fd83a3c7e5a3f308d37443cc86c28f71e0c21a9a`.
- `ACCEPTANCE.md`: 3,925 bytes; SHA-256 `87078c7ec1ff8f240fb1a9bbe27dc27a8ef13a6123793a76d5ae8ec1c7344f9f`.
- `AUDIT.md`: 20,784 bytes; SHA-256 `93994f4aebdab4c80221846ab96c47211c601ebb400bb52e005741b5ab033e8d`.
- `MANIFEST.json`: 1,378 bytes; SHA-256 `a4532503ff145c785021bfd4271bfa7913328c94adbe517b3883bbf86fa2eb86`.
- `PROOF.md`: 17,287 bytes; SHA-256 `1f74f0a66e48631885d5849a98379427d77fa8cd64650a9eb322259de0831b6d`.
- `README.md`: 2,658 bytes; SHA-256 `cc2b6f3b34261625210e7d730f723d3176dd80a39b53a258caa53831226c72dd`.
- `SOURCES.json`: 4,405 bytes; SHA-256 `2ec5a6e67fc1faf8cbe06d997e4ac2523a9ee32d6f11551a494831fc99d67f8e`.
- `VERIFICATION.json`: 4,595 bytes; SHA-256 `a9607f1791ff4e41fa9cd6bc13aaa9ac9e5f5b04a138a5a2f3dfa383ce66d3f3`.

MANIFEST.json lists eight members and hashes the other seven; this body independently pins its digest.

