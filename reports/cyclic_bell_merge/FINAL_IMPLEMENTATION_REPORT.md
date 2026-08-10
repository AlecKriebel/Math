# Final implementation report — author-ready cyclic Bell revision

Date: 9 August 2026

Target and deployed branch: `origin/main`

Manuscript version: 1.1 (website metadata version 1.1.0)

Final scientific snapshot:
`609f8c6ffc083b665804890dd82fc739d414ea9d`

Deployed provenance tip:
`a1cf257a5e935faa3c01292a4f5cd5d6accbbb1d`

GitHub Pages status: **built**, 2026-08-10T04:02:30Z

Deployment-record commit: **forthcoming at the time this report is written**.
It will contain these three post-deployment reports, not a different
scientific implementation. Its hash must be reported separately at final
handoff.

## Delivered result

The three preserved standalone papers are consolidated into the author-ready,
unrefereed manuscript

**Exact Quantum Values and Permutation-Blind Maximizers in Cyclic Bell
Inequalities**

*Sharp operator bounds, equality structure, and limits of Bell-value
randomness certification*

Canonical route:
`/Math/papers/cyclic-bell-exact-values-and-randomness/`

The final manuscript is 28 pages. Version 1.1 contains 17 named theorem-like
environments. The claims ledger
contains 30 audited claims, and the source crosswalk accounts for 37 named or
quantitative source items: 10 from the exact-value manuscript, 12 from the
first-family randomness manuscript, and 15 from the permutation/setting
manuscript.

The earlier author-ready implementation commit `0dd9d030…` changed 43 scoped
files (5,396 insertions and 1,059 deletions) and added 10 new audit or
verification files. The final referee-explication snapshot `609f8c6f…`
changed 18 scoped files (272 insertions and 105 deletions); provenance tip
`a1cf257a…` then pinned that scientific snapshot in 7 scoped files.

## Source files used

The line-anchored disposition of every source theorem, lemma, proposition,
corollary, exact table, and verifier-backed identity is in
`cyclic_bell_exact_values_and_randomness/audit/THEOREM_CROSSWALK.md`.
The following source and provenance files were used.

### Exact-value package: `cyclic_bell_tsirelson_bound/`

- `main.tex` and the frozen PDF
  `output/pdf/cyclic_bell_tsirelson_bound.pdf`;
- `certificate.json`, `verify_certificate.py`,
  `tests/test_certificate.py`, and `verify_all.sh`;
- `MANIFEST.md`, `PRIORITY_AUDIT.md`, `RESEARCH_LOG.md`,
  `SOURCE_SNAPSHOT.md`, `README.md`, `SHA256SUMS`, and
  `requirements.txt`.

These supplied the historical polar/scalar derivation, exact-value candidate,
canonical Weyl strategy, source Fourier identification, low-dimensional
benchmarks, verification record, and provenance boundary.

### First-family randomness package:
`cyclic_randomness_counterexample/`

- `manuscript.tex`, `manuscript.pdf`, and
  `output/pdf/cyclic_randomness_counterexample.pdf`;
- `certificate.json`, `family_certificate.json`, `cycle_family.py`,
  `generate_certificate.py`, `verify_exact.py`, `test_cases.py`,
  `compare_reference_behavior.py`, `discovery_search.py`, and `run_all.sh`;
- `claims_ledger.md`, `assumptions_ledger.md`, `prior_art_audit.md`,
  `failed_approaches.md`, `RESEARCH_LOG.md`, `README.md`,
  `requirements.txt`, and `MANIFEST.sha256`;
- the frozen comparison, discovery, test, verification, and full-run output
  text files.

These supplied the paired root-order construction, target DFT, final-two
swap, exact four-outcome certificate, value-only randomness consequence, and
the restored reflection-rank/equal-supported-multiplicity result.

### Second-family and low-setting package: `minimum_bell_randomness/`

- `manuscript.tex` and `manuscript.pdf`;
- `family_certificate.json`, `verify_second_family_d4_exact.py`,
  `second_family_discovery.py`, `test_cases.py`,
  `satwap_ideal_audit.py`, and `verify_binary_2x2.py`;
- `CLAIMS_LEDGER.md`, `ASSUMPTIONS_LEDGER.md`,
  `STRUCTURAL_RESULTS.md`, `PRIOR_ART_AUDIT.md`,
  `FAILED_APPROACHES.md`, `RESEARCH_LOG.md`, `README.md`, and
  `MANIFEST.sha256`.

These supplied the second-family Fourier/SOS identities, one-input baseline,
binary benchmark, private-MUB composition lemma, ideal-table and direct-anchor
calculations, and the scoped computational-MUB obstruction.

### Primary literature and publication/site records

- Every public version and raw source archive of arXiv:2606.21362 available at
  the audit cutoff, its supplementary material/code record, and the primary
  papers listed in `audit/SEARCH_LOG.md`,
  `audit/SOURCE_COMPARISON_TABLE.md`, and
  `audit/SOURCE_QC_BIBLIOGRAPHY_AUDIT.md`;
- `PUBLICATION.md`, root `README.md`, `docs/index.html`,
  `docs/sitemap.xml`, `docs/assets/style.css`, the three historical landing
  pages and PDFs, their immutable Git snapshots, and repository history.

## Canonical package and new files

The canonical package contains 40 tracked files: 8 package-root files, 14
audit files, 8 verification files, 9 reviewer-packet files, and the canonical
PDF.

### Package root

- `README.md`, `RESEARCH_LOG.md`, `CHANGELOG.md`, `MERGE_REPORT.md`,
  `REVIEW_RESPONSE.md`, `main.tex`, `reproduce.sh`, and
  `manifest.sha256`.

### Audit

- `ADVERSARIAL_REVIEW.md`, `CLAIMS_LEDGER.md`,
  `CLAIMS_NOT_MADE.md`, `KNOWN_LIMITATIONS.md`,
  `LOW_SETTING_RESTORATION_AUDIT.md`, `PRE_REVISION_BASELINE.md`,
  `PRIORITY_AUDIT.md`, `PROOF_DEPENDENCY_MAP.md`,
  `RIGIDITY_RESTORATION_AUDIT.md`, `SEARCH_LOG.md`,
  `SOURCE_COMPARISON_TABLE.md`, `SOURCE_QC_BIBLIOGRAPHY_AUDIT.md`,
  `THEOREM_CROSSWALK.md`, and `UNRESOLVED_RISKS.md`.

### Verification

- `README.md`, `verification_report.txt`, `verify_merged.py`,
  `verify_mub_obstruction.py`, `verify_site.py`,
  `verify_exact_benchmarks.py`, `verify_private_mub_binary.py`, and
  `verify_rigidity.py`.

### Reviewer packet and PDFs

- `README.md`, `two_page_summary.md`, `two_page_summary.tex`,
  `two_page_summary.pdf`, `proof_roadmap.md`,
  `load_bearing_claims.md`, `theorem_to_artifact_map.md`,
  `focused_questions.md`, and `source_author_review.md`;
- `output/pdf/cyclic_bell_exact_values_and_randomness.pdf`.

### Version 1.1 additions

The 10 files added by implementation commit `0dd9d030…` are:

1. `REVIEW_RESPONSE.md`;
2. `audit/CLAIMS_NOT_MADE.md`;
3. `audit/LOW_SETTING_RESTORATION_AUDIT.md`;
4. `audit/PRE_REVISION_BASELINE.md`;
5. `audit/RIGIDITY_RESTORATION_AUDIT.md`;
6. `audit/SOURCE_QC_BIBLIOGRAPHY_AUDIT.md`;
7. `audit/THEOREM_CROSSWALK.md`;
8. `verification/verify_exact_benchmarks.py`;
9. `verification/verify_private_mub_binary.py`;
10. `verification/verify_rigidity.py`.

### Final referee-explication and provenance pass

Scientific snapshot `609f8c6ffc083b665804890dd82fc739d414ea9d`
made the final arXiv-readiness and proof-explication changes without altering a
formal theorem statement, theorem numbering, section structure, mathematical
verifier, historical source, redirect, or historical PDF. In particular, it:

- separated the canonical polar partial isometry from its harmless unitary
  kernel extension in the conditional permutation proof;
- derived the target table from explicit eigenvectors, proved canonical
  Fourier flatness, and supplied the complete short $d=2,3$ argument;
- displayed representative trace calculations for the second-family
  first-harmonic correlators;
- closed the nonscalar-implies-nonzero-corner hinge in Proposition F.1 and
  repaired the equality-root equation reference;
- clarified overbar and $q,qa,qc$ notation, improved originating-work
  attribution, and cited the source SOS as Perito et al., Eqs. (22)--(23),
  with prefactor $1/(2d)$;
- removed the redundant first-page status notice while retaining the detailed
  end disclosure, and added the author's public email and verified ORCID; and
- retained the single self-contained 28-page manuscript rather than creating
  a new supplement, and did not create or repurpose a DOI.

Provenance tip `a1cf257a5e935faa3c01292a4f5cd5d6accbbb1d`
then pinned the immutable scientific snapshot in the manuscript and canonical
page. The public page displayed that source commit during production-browser
validation.

The canonical website files are
`docs/papers/cyclic-bell-exact-values-and-randomness/index.html`,
`paper.pdf`, and `two-page-summary.pdf`. The original merger also created
`reports/cyclic_bell_merge/WEBSITE_REDIRECT_REPORT.md`,
`LINK_CHECK_REPORT.md`, and this report.

## Historical files preserved

The three historical source directories, their scripts, failed approaches,
ledgers, manifests, standalone manuscripts, publication chronology, and Git
history remain intact. Version 1.1 did not edit them.

The three historical public PDFs remain byte-for-byte unchanged:

| Historical paper/PDF route | SHA-256 | Immutable source |
|---|---|---|
| `/Math/papers/cyclic-bell-tsirelson-bound/paper.pdf` | `c4e80e0956595c28cbf0323639dcf5b84f5ffbd0785362cc4233e2c19812b96f` | `21126e384677d8bb5ebb796c695ce48904fd5e72` |
| `/Math/papers/cyclic-bell-randomness-counterexample/paper.pdf` | `3bef4205ead0c1629cc78120dd701f2464ab3a38f855c8f01891412ce7b38975` | `0055250a009b5f7f0a8283cba4e8813c98b700f8` |
| `/Math/papers/permutation-blind-bell-randomness/paper.pdf` | `2c9e4d864f5b617f0d99c1b199f8b3546e3d3aa27ac96356e399a860fd1263c3` | `e3ae7a1ac175071b14f2f5c83ddc86149c366da5` |

Earlier exact-value and counterexample PDF hashes `947b6019…` and
`73c2e2ab…` remain accessible through commit history. No history was
rewritten.

## Claims retained

- The first reduced cyclic operator has
  $\beta_q=\beta_{qa}=\beta_{qc}=2\csc(\pi/(2d))$ for every $d\ge2$, and its
  first augmentation has value one more.
- The kernel-safe polar positive-factor identity, scalar equality roots,
  exact global gap, and source finite-dimensional attainment are retained.
- The conditional paired phase-permutation theorem remains a sufficient
  all-dimensional construction preserving local first moments and the full
  complex first-harmonic correlator matrix.
- For every $d\ge4$, the final-two swap exactly maximizes both augmented
  families, has uniform local marginals and a nonuniform target table, and
  gives the stated guessing lower bound.
- The exact $d=4$ cyclotomic table $1/32,3/32$ and $G=3/32$ is retained.
- The credited second-family SOS, coefficient/Fourier compression, exact
  saturation, and transfer of the target table are retained.
- The scalar-value versus fixed-full-behavior randomness distinction,
  one-input flagged-locality baseline, ideal-table/direct-anchor calculations,
  and scoped computational-MUB obstruction are retained.

## Claims restored or strengthened in version 1.1

- The source's proved $d\sqrt2$ bound, all-dimensional lower strategy, and NPA
  evidence through $d=6$ are now separately and correctly credited; the exact
  radical table for $d=2,\ldots,6$ is restored.
- The commuting-operator polar proof now gives explicit strong limits for the
  support and canonical partial isometry in $\mathcal A''$ and the full
  bicommutant commutation argument.
- The finite-dimensional support-rigidity theorem and reflection-product rank
  lemma are restored. Every attained finite-dimensional tensor-product exact
  maximizer of the first augmented family has every equality root with equal
  multiplicity on $K=\operatorname{supp}\rho_A$, hence $d\mid\dim K$.
- The source-observable Fourier identification, transpose/conjugation
  convention, and explicit $d=3$ formula are restored.
- The cosecant-square derivation proving
  $\sum_\ell|\lambda_\ell|^2=1$ is restored.
- The complete prior-art binary $3\sqrt3$ benchmark is restored, including
  the two-square SOS, finite-dimensional operator-valued privacy conclusion,
  two bits at the target, and componentwise $(2,2)$ certification minimality.
- The private-MUB composition lemma is restored as a positive sufficient
  state-supported operator criterion.
- Guessing is indexed by the $q$, $qa$, and $qc$ adversarial models; the
  finite witness gives the common lower bound without asserting equality of
  the three suprema.
- Behavior-level nonuniqueness modulo local output relabelings and the exact
  displayed-realization entropy
  $5-\log_2 3=3.415037\ldots$ bits are explicit.

## Claims narrowed

- Support rigidity is restricted to attained finite-dimensional
  tensor-product exact maxima of the **first augmented** family. It is not
  asserted for $qa$, $qc$, approximate maxima, the unaugmented operator, the
  second family, infinite-dimensional support, or $K^\perp$.
- Equal supported multiplicities are necessary but do not imply a Weyl
  representation, uniqueness, self-testing, or a complete maximizing-face
  classification.
- The phase-permutation theorem is sufficient, not exhaustive.
- The normalized Conjecture 2 consequence is stated precisely:
  $\langle\overline{\mathcal I}_d\rangle=M_d+1$ does not imply
  $G(AB\mid1,d,E)=1/d^2$ for $d\ge4$. The canonical full-behavior computation
  is not challenged.
- Behavior-level inequivalence is proved modulo local output relabelings; no
  classification under every local isometry, ancilla, direct sum, or
  transposition convention is claimed.
- The final-two swap is not claimed to maximize guessing probability. Its
  $d=4$ entropy is an upper bound on value-only worst-case min-entropy, not
  the exact optimized value.
- The permutation orbit remains target-flat for $d=2,3$; those maximizing
  faces remain unresolved.
- The second-family main/SOS and all-Bob-adjoint appendix conventions are
  related only by consistent Bob outcome inversion and are never mixed
  termwise.
- The binary SOS proves the $q=qa=qc$ value, but its privacy theorem is kept
  at the attained finite-dimensional tensor-product scope.
- The private-MUB lemma is sufficient only and does not construct or prove
  the existence of a low-setting Bell functional.
- The one-input result is a DI forcing/certification statement about all
  compatible realizations, not an intrinsic-randomness statement.
- Endpoint nonrobustness retains the “deficit at most $\varepsilon$”
  quantifier.
- Higher-dimensional low-setting conclusions remain confined to the stated
  ideal bases, direct anchor, real operator span, coefficientwise bound, and
  separately bounded exposure route.

## Claims removed or deliberately not promoted

- Numerical power-harmonic and third-setting repair experiments remain failed
  or exploratory approaches, not theorems.
- A stray binary $2\times3$ comparison is not elevated into a claim.
- No general $(2,3,d,d)$ impossibility, all-dimensional minimum-setting law,
  or failure of every third-setting repair is claimed.
- No complete maximizing-face, exact worst-case guessing/entropy, or full
  strategy-equivalence classification is claimed.
- No $d=2,3$ nonuniform permutation conclusion is inferred.
- The phrase that the source $d\sqrt2$ bound is “asymptotically close” was
  removed: its ratio to the exact value tends to
  $\pi/(2\sqrt2)=1.110720734540\ldots$, so it is same-order but not
  asymptotically tight.
- The categorical statement that no source author had ever been contacted was
  removed because preserved repository history records earlier contact about
  the companion result. No external communication was initiated during this
  revision.

## Mathematical and attribution repairs

1. Reconciled the first-family normalization against the displayed operator
   and stated source qutrit value.
2. Separated the source $d\sqrt2$ theorem, lower strategy, conjecture, and NPA
   evidence from the new exact proof.
3. Hardened the arbitrary-Hilbert-space $q_c$ proof with the generated von
   Neumann algebra, strong closure, support projection, canonical partial
   isometry, and bicommutant commutation.
4. Restored and independently reconstructed every support, invariance,
   kernel, adjacent-reflection, multiplicity, and divisibility step in the
   finite-dimensional equality theorem.
5. Retained the genuine canonical partial isometry and eliminated any
   implicit invertibility or global unitary-extension assumption.
6. Derived the source-observable Fourier relations and coefficient
   normalization, including the exact qutrit formula.
7. Preserved the second-family source-SOS prefactor $1/(2d)$,
   $d\lambda_\ell$ compression, Alice conjugation, and global adjoint
   orientation.
8. Replaced one ambiguous guessing quantity by model-indexed definitions and
   kept value statements separate from finite-dimensional privacy statements.
9. Restored the binary and private-MUB operator-valued privacy proofs with
   every auxiliary anticommutation relation stated on the state and every
   $1/d$, $1/d^2$ normalization exposed.
10. Added the precise normalized Conjecture 2 implication, behavior-level
    nonuniqueness, and exact $d=4$ entropy without claiming an optimum.
11. Preserved the endpoint tolerance quantifier and corrected one-input
    wording to DI certification against all compatible realizations.
12. Added the NPA citation and verified the official Coccia--Padovan--Vallone
    names used in the canonical bibliography.

## Priority conclusions

The refreshed primary-source audit found no priority conflict at its cutoff.

- **Established prior art:** both family definitions and normalizations;
  canonical strategies and all-dimensional lower values; the source
  $d\sqrt2$ upper bound and NPA evidence through $d=6$; the second-family
  value/SOS; the general scalar-versus-complete-statistics distinction;
  one-input locality; and the binary $3\sqrt3$ benchmark.
- **Plausibly new:** the exact first-family all-dimensional upper bound; the
  sufficient family-specific phase-permutation mechanism; first-family
  nonuniform exact maximizers; the normalized family-specific Conjecture 2
  counterexample; and behavior-level nonuniqueness.
- **New strengthening of a known/conjectured result:** equality of
  $\beta_q,\beta_{qa},\beta_{qc}$ at $M_d$.
- **Plausibly new application of established prior art:** phase-permuted
  nonuniform maximizers of the second family using the credited source SOS.
- **Restored historical/internal results, not new lead claims:** support
  rigidity and the private-MUB sufficient criterion.
- **Novelty uncertain:** the scoped computational-MUB exposure obstruction.
- **Priority conflict:** none found.

All absence-of-prior-work language remains qualified by “to our knowledge.”
Concurrent or unindexed 2026 work remains a live risk.

## Old-to-new URL map

| Historical landing route | Canonical destination | Historical PDF |
|---|---|---|
| `/Math/papers/cyclic-bell-tsirelson-bound/` | `/Math/papers/cyclic-bell-exact-values-and-randomness/` | remains at `/Math/papers/cyclic-bell-tsirelson-bound/paper.pdf` |
| `/Math/papers/cyclic-bell-randomness-counterexample/` | `/Math/papers/cyclic-bell-exact-values-and-randomness/` | remains at `/Math/papers/cyclic-bell-randomness-counterexample/paper.pdf` |
| `/Math/papers/permutation-blind-bell-randomness/` | `/Math/papers/cyclic-bell-exact-values-and-randomness/` | remains at `/Math/papers/permutation-blind-bell-randomness/paper.pdf` |

Each compatibility page remains a valid `noindex,follow` HTML page with a
canonical link, three-second meta refresh, JavaScript fallback, ordinary
canonical link, historical-PDF link, and immutable-source link. No old PDF URL
redirects.

## Verification result

`./reproduce.sh` completed all **11 execution stages** successfully.

### Unified hostile checks

- scalar extremum/equality roots through $d=20$: 13,395 grid points;
- genuine nonunitary polar partial-isometry identity: PASS;
- first-family canonical, reversed, final-two, and seeded strategies: 125;
- exhaustive $d=2,3$ permutations: 8, all target-flat;
- final-two bias through $d=20$: PASS;
- mismatched phases, repeated labels, and off-equality controls: failed as
  intended;
- second-family Fourier/order/SOS strategies: 125;
- canonical Fourier flatness through $d=20$: PASS;
- exact-rational one-input reconstructions: 15.

### Restored-result checks

- support phases and adjacent reflections through $d=64$: 89,439 triples;
- reflection-rank subadditivity: 840 exact-rational hostile products;
- multiplicity/divisibility: 16,128 cases over $d=2,\ldots,64$ and
  $\dim K=1,\ldots,256$;
- exact $d=2,\ldots,6$ radicals and source decimals: PASS;
- $d=4$ entropy identity: PASS;
- cosecant-square/coefficient normalization through $d=100$, including
  hostile general shifts: PASS;
- independently reconstructed source/polar/Fourier observables through
  $d=12$: 77 Bob observables, including the exact qutrit formula;
- binary SOS over $\mathbb Q(\sqrt3)$ and exact strategy: PASS;
- private-MUB normalization through $d=12$: 1,980 checks;
- all three deleted-hypothesis private-MUB controls failed as intended.

### Independent certificates, retained checks, and integrity

- independent first-family exact $d=4$ certificate over
  $\mathbb Q(\zeta_{16})$: PASS;
- independent second-family exact $d=4$ full SOS certificate: PASS;
- retained binary, standard-table/direct-anchor, computational-MUB, and
  finite second-family regressions: PASS;
- computational-MUB replay: 209 indices, 1,672 admissible samples, and 1,368
  nonscalar two-sided spectral witnesses;
- all three historical integrity manifests: PASS;
- canonical package manifest: PASS.

Finite tests remain regression evidence. The all-dimensional $q_c$ theorem,
support-rigidity theorem, and privacy conclusions rest on the displayed
analytic arguments, not finite sampling.

## PDF results

| Artifact | Pages | SHA-256 | Result |
|---|---:|---|---|
| canonical manuscript | 28 | `9d0d23837aed20346f6e97234095ee146f7e7b852c7a4a4b5d646e5fa595c0f6` | PASS |
| reviewer summary | 2 | `0f3dfa78424a8934defdf9952593bf9a7269f7fec58dc6dd5c4824fa9db562d2` | PASS |

Both PDFs built with Tectonic without undefined references, undefined
citations, overfull/underfull boxes, or TeX errors. Every rendered page was
visually inspected; no clipping, overlap, broken glyph, or table overflow was
found. Title/author metadata passed.

The canonical production PDF and two-page-summary URLs both returned HTTP 200
as `application/pdf`, and their served hashes exactly matched the table.

## Website, redirect, metadata, and link result

Production validation after the Pages build passed:

- canonical page, homepage, sitemap, three compatibility pages, both canonical
  PDFs, and all three historical PDFs returned HTTP 200 with the expected
  content types;
- canonical citation, OpenGraph, and JSON-LD `ScholarlyArticle` metadata use
  version 1.1.0, the correct author/date/PDF/canonical URL, an AI-assistance
  disclosure, and no DOI;
- MathJax rendered 43 expressions in a real browser;
- no horizontal overflow occurred at a 1,280-pixel viewport, and MathJax and
  the page scripts produced no warnings or errors; the only console item was
  the repository-wide missing `/favicon.ico` request, outside this scoped
  paper-page revision;
- the canonical target was correct, the embedded PDF rendered, and the page
  displayed scientific source commit
  `609f8c6ffc083b665804890dd82fc739d414ea9d`;
- the selected-portfolio homepage retains one merged cyclic card and has no
  retired provisional-artifact count assertion;
- the sitemap contains the canonical route once and no compatibility route;
- all three redirect stubs retain `noindex,follow`, canonical, meta-refresh,
  JavaScript, ordinary-link, historical-PDF, and immutable-source elements;
- no redirect loop, metadata mismatch, broken required link, content-type
  mismatch, or byte-integrity failure was found;
- historical PDF hashes remain the three values in the preservation table.

## Commit and deployment record

The final scientific manuscript, reviewer-packet, PDF, and canonical-page
changes are frozen in snapshot
`609f8c6ffc083b665804890dd82fc739d414ea9d`. Provenance tip
`a1cf257a5e935faa3c01292a4f5cd5d6accbbb1d` pins that snapshot in the
manuscript and canonical page. Both commits are on and were pushed directly to
`origin/main` without a force push. GitHub Pages built the provenance tip at
2026-08-10T04:02:30Z, and live HTTP, content-type, byte-equality, rendering,
canonical-target, embedded-PDF, and source-commit checks passed.

The next commit is a **deployment-record commit** whose purpose is only to add
the three refreshed post-deployment reports. It is not the scientific snapshot
or deployed provenance tip and does not change the scientific result. A commit
cannot record its own hash without changing that hash, so the deployment-record
hash belongs in the final handoff response rather than inside this file.

For chronology, the earlier version 1.1 implementation
`0dd9d030cba128565744c1c7c83cf3956b32d744` was built at
2026-08-09T16:19:04Z with a 25-page manuscript, 41 MathJax containers, main-PDF
hash `5a7265057a07ef58883defb4c46993328ac418ccf937f3e416e96c61099b3a9b`,
and summary hash
`a52798ec6451b368ddc7e6777004a8b30a478e1104769587e94b466ceac2819c`.
Those values are retained as history and are superseded by the current
deployment above.

## Remaining specialist-review risks

1. **Support rigidity:** independently scrutinize vector-to-support
   cancellation, bad-kernel exclusion, $A_0K=K$, $V_yK=K$, the supported
   $d$-th-power step, adjacent reflections, and the finite-rank count.
2. **Convention stability:** a missing adjoint, transpose, conjugation, or
   termwise mixture of the two Bob conventions could invalidate a formula.
3. **Second-family phase algebra:** the coefficient normalization, geometric
   sum, parity exponent, Alice conjugation, and Fourier compression are dense
   and should be frozen or replayed after copyediting.
4. **Arbitrary-$q_c$ exposition:** preserve the strong-limit and bicommutant
   argument; finite matrix tests do not validate nonspatial representations.
5. **Guessing-model scope:** do not collapse
   $G_{\mathrm{val}}^q,G_{\mathrm{val}}^{qa},G_{\mathrm{val}}^{qc}$ into a
   claimed equality. The finite witness gives only a common lower bound.
6. **Optimization scope:** neither the guessing lower bound nor
   $5-\log_2 3$ is the exact worst-case optimized value.
7. **Behavior versus strategy:** nonuniqueness modulo output relabelings is
   not a complete self-testing or strategy-equivalence classification.
8. **Binary/private-MUB scope:** binary privacy remains finite-dimensional
   tensor-product; the private-MUB lemma is sufficient and nonexistential.
9. **Low-setting scope:** one-input is a DI certification baseline, and the
   higher-dimensional $2\times2$/$2\times3$ regimes remain open beyond the
   stated obstructions.
10. **Priority:** a later source version, concurrent preprint, unindexed note,
    or standard antecedent for the polar identity may require attribution
    updates.
11. **Review status:** no external specialist has reviewed or endorsed the
    revision; internal AI-assisted adversarial review and passing code are not
    peer review.

No email or outreach was sent, no coauthor was added, no DOI or release was
created, and no arXiv or journal submission occurred. Repository history does
record earlier author contact about the companion exact-value result; this
report makes no contrary categorical claim.
