# Merge report

## Outcome

The three standalone manuscripts have been rebuilt into one logically
continuous paper rather than concatenated. The equality phases are the
central bridge: they arise in the exact polar upper bound, permit paired
weighted-cycle permutations, and explain why a sharp scalar score can fail
to determine the target distribution.

## Source packages audited

### 1. Exact cyclic value

Directory: `cyclic_bell_tsirelson_bound/`

Used: `main.tex`, `certificate.json`, `verify_certificate.py`,
`tests/test_certificate.py`, `MANIFEST.md`, `PRIORITY_AUDIT.md`,
`RESEARCH_LOG.md`, `SOURCE_SNAPSHOT.md`, `SHA256SUMS`, and the frozen PDF.

Imported conclusions: polar factorization, scalar extremum, exact first
value, finite attaining strategy, commuting-operator extension, augmented
value. The earlier proof was reconstructed independently and its kernel
handling strengthened in exposition.

### 2. First-family nonuniform maximizer

Directory: `cyclic_randomness_counterexample/`

Used: `manuscript.tex`, `certificate.json`, `cycle_family.py`,
`generate_certificate.py`, `verify_exact.py`, `test_cases.py`,
`compare_reference_behavior.py`, `run_all.sh`, prior review/claim ledgers,
`MANIFEST.sha256`, and the frozen PDF.

Imported conclusions: paired root permutations, weighted-shift
admissibility, first-harmonic invariance, target Fourier formula, final-two
swap, quantitative guessing lower bound, exact (d=4) certificate, and the
finite-dimensional equal-supported-multiplicity theorem.

### 3. Second-family and setting consequences

Directory: `minimum_bell_randomness/`

Used: `manuscript.tex`, `test_cases.py`, `second_family_discovery.py`,
`verify_second_family_d4_exact.py`, `verify_binary_2x2.py`,
`satwap_ideal_audit.py`, `mub_obstruction_check.py`, structural/claim ledgers,
`MANIFEST.sha256`, and the frozen PDF.

Imported conclusions: second-family Fourier compression and SOS saturation,
one-input flagged locality realization, canonical two-input qudit tables,
direct third-anchor failure, and the narrowly scoped computational-MUB
obstruction. The valid private-MUB composition lemma and complete binary
benchmark were restored with repaired state-supported proofs and explicit
prior-art attribution.

## Frozen historical artifacts

| Historical paper | Current public PDF SHA-256 | Immutable source |
|---|---|---|
| Exact cyclic value | `c4e80e0956595c28cbf0323639dcf5b84f5ffbd0785362cc4233e2c19812b96f` | commit `21126e384677d8bb5ebb796c695ce48904fd5e72` |
| First-family counterexample | `3bef4205ead0c1629cc78120dd701f2464ab3a38f855c8f01891412ce7b38975` | commit `0055250a009b5f7f0a8283cba4e8813c98b700f8` |
| Permutation-blind/setting note | `2c9e4d864f5b617f0d99c1b199f8b3546e3d3aa27ac96356e399a860fd1263c3` | commit `e3ae7a1ac175071b14f2f5c83ddc86149c366da5` |

Earlier publication-history hashes are also recorded: exact-value initial
`947b6019…` and counterexample initial `73c2e2ab…`. Git history and
`PUBLICATION.md` retain the complete chronology.

## Claims retained, narrowed, and omitted

The detailed disposition is in `CHANGELOG.md`, `audit/CLAIMS_LEDGER.md`, and
the line-anchored `audit/THEOREM_CROSSWALK.md`.
The central exact-value and counterexample claims were retained. Equality was
narrowed from any possible classification reading to exact scalar phases,
state-level positive-factor conditions, a necessary finite-dimensional
support-multiplicity theorem, and a sufficient permutation theorem. The
second-family theorem is explicitly tied to the source SOS. Low-setting
conclusions are confined to the one-input DI baseline, the complete prior-art
binary benchmark, the sufficient private-MUB criterion, and the exact
hypotheses of the retained obstruction.

The author-ready revision restores both valid results omitted from version
1.0: equal supported multiplicities and the private-MUB composition lemma.
It also restores the full binary benchmark, source-observable identification,
the exact low-dimensional value table, and the coefficient-normalization
derivation. Unproved repair experiments and any all-dimensional minimum-
setting claim remain outside the scientific narrative for explicit reasons
recorded in the crosswalk.

## Independent review disposition

Three skeptical reconstructions covered the exact operator theorem, the
randomness/second-family mechanism, and the setting/site preservation work.
The merged theorem set passed after the convention, equality-scope,
verification-independence, and endpoint-quantifier qualifications documented
in `audit/ADVERSARIAL_REVIEW.md`.

## Priority disposition

The originating families, canonical strategies, lower bounds, and
second-family SOS are fully credited. The exact first upper bound,
commuting-operator strengthening, and family-specific biased permutation
maximizers were not found in current primary literature and are classified
as plausibly new or a new strengthening, never as definitive priority.

## Scope controls

- No external communication was initiated during this merger or revision.
  Repository history records earlier author contact about the companion
  exact-value result, so the canonical paper makes no categorical claim that
  no prior contact ever occurred.
- No email, cover letter, endorsement request, or authorship proposal was
  drafted.
- No DOI, release, arXiv submission, or journal submission was created.
- No historical source directory or PDF was changed.
- No unrelated paper or site section was restructured.
