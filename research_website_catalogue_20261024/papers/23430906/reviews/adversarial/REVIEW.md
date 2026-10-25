# Independent adversarial review: Zenodo 23430906

**Verdict:** No substantive defect or unresolved central gap found in the literal
Theorem 1 of the deposited version. The strongest verified claim is the full
stated finite-n inequality, with its actual explicit constant and hypotheses.
This is a mathematical review result, not publication clearance, a novelty
certificate, human peer review, or formal proof-assistant certification.

Reviewer role: adversarial falsification. Model: explicitly assigned GPT-6.1 Sol,
ultra effort; no children spawned. Completed 25 October 2026 UTC. Inventory row 82.

## Published identity and custody

The reviewed work is Alec Kriebel, *A localized Gaussian-witness lower bound for
fractional iterated area on uniform grids*, version 1.0, publication date
14 October 2026, DOI [10.5281/zenodo.23430906](https://doi.org/10.5281/zenodo.23430906).
Fresh public API metadata identifies it as a published preprint. The record was
created on 17 October, which is distinct from its declared publication date.

| Deposited asset | Bytes | SHA-256 |
| --- | ---: | --- |
| `paper.pdf` | 93,113 | `33b90a4d846db58ea93efd453c13455fbeb3a29dcaa3e4cc49a68c0a8ebdff5b` |
| `PR1071_preprint_v1_0_support.zip` | 3,101,130 | `4e4a1b20c2da7f5a6e686256f7f8d7bba9c8db71e21f316f99da63285f7b0191` |

Their MD5 values agree with the fresh API: respectively
`655dd4be1adb3ab629d207c3adde4c93` and `2c012b29eda4305081acd5ac4d0d2b0b`.
The API raw response hash is
`50b895ad48cc40a5c948428fff572d53f69a3643fb8ebb22122812796d54730b`.
The local locator PDF was used only to start the reading; final conclusions are
bound to fresh deposited bytes and `sources/receipt.json`, not locator provenance.

The complete seven-page manuscript and actual TeX were read. The rendered fourth
page was inspected to resolve conjugation and formula layout. The embedded PDF
equals the standalone deposit. A separate independent read of all archive members
confirms 225 byte-equal regular extracted members, 224 manifest-pinned members
plus the intentionally self-excluded manifest, and no nested-archive magic.
The source-intake inventory also reports no nested archives. The detailed
identity output is `outputs/INDEPENDENT_PACKAGE_IDENTITY.json`.

The deposited files, metadata/receipt, all extracted support bytes, and all
quarantine support files remained unchanged. The two acquisition-sidecar changes
seen during parallel primary-source collection (`sources/.gitignore` and
`sources/primary-acquisition-receipt.json`) are disclosed in
`INPUT_HASHES_AFTER.json`; additional primary files are listed separately.
These are not changes to the deposited record, paper or support package. This
reviewer wrote only inside its assigned adversarial folder, and performed no
source edits, Git actions, spreadsheet/site/deployment/release actions, or outreach.

## Exact claim and success criterion

For each fixed $H\in(1/4,1)$, take two independent centered standard fBm
components with the printed covariance. Let $X_T=\int_0^T B_s^1dB_s^2$ be
the canonical polygonal $L^2$ iterated integral, and let $\mathcal G_{T,n}$
contain both components at every $jT/n$, $1\le j\le n$. The hypothesis
under attack was

\[
\|X_T-F\|_2\ge
\frac{2\pi(4/45045)}{D_H\sqrt{\overline P_f\overline P_g}}
T^{2H}n^{1/2-2H}
\quad(T>0,\ n\ge1,\ F\in L^2$\mathcal G_{T,n}$).
\]

Here $\overline P_r$ is literally equation (2), with the weak-derivative
norms of the zero extensions. It is not permissible to replace this target by
an unspecified smaller constant, only asymptotic positivity, linear estimators,
a different area normalization, a single-component information set, or a premise
equivalent to the desired lower bound. The proof survives those quantifier checks
without any such replacement.

## Independent reasoning and falsification families

The early proof and controls were written and sealed **before** inspecting the
submitted checker or archived proof/review bodies. `INDEPENDENCE_SEAL.json` pins
`independent/DERIVATION.md`, `independent/controls.py`, and the actual output
`outputs/independent_controls.json`. No current sibling scientific opinion was
consulted. Archived favorable verdicts were not used as evidence.

| Attack family | Mechanism and checkable evidence | Result / exact remaining gap |
| --- | --- | --- |
| Conditional Gaussian tensor projection | Reconstructed the target as an element of the cross-component second chaos; grid conditioning is $P_S\otimes P_S$. A tensor in $S^\perp\otimes S^\perp$ pairs with the residual of every nonlinear grid estimator. | The all-$F$ quantifier holds. No gap found. |
| Fourier sign and normalization | Directly multiplied $K_t$ by the conjugate of $u_h$, recovering $h(t)-h(0)$, $D_H$, and both factors of $2\pi$. Omitting the printed conjugation reflects the bump to negative time and destroys its useful pairing. | Printed convention is correct; the reflected sign control is outside the printed proof. No gap found. |
| Functional-analytic localization | Checked all endpoint traces needed for zero-extension $W^{3,1}$, Fourier decay, scale cancellation and periodization over every integer lag. | Uniform upper Gram bound holds for all cell counts and sizes. It is not false rough increment lower coercivity. No gap found. |
| Covariance and cancellation | Retained signed off-diagonal terms in $\operatorname{tr}(AC)$; proved the PSD trace bound without entrywise positivity or matrix commutation. A separate noncommuting 2-by-2 control is recorded. | No unjustified cell independence or cancellation. No gap found. |
| Canonical-area input | Independently used $P_m=L_m+Q_m$ and the exact covariance formula for $Q_m$, with all three summability regimes. Given established polygonal $L^2$ existence, this yields the needed left-sum convergence without exact Euler coefficients. | Classical canonical-area existence is the explicit external input, not the lower-bound conclusion. No unsupported central reformulation found. |
| Order of limits | At $m=n$, the finite pairing is zero. For fixed $n,T,j$, the refinement limit is positive. The paper holds those variables fixed during $m\to\infty$, then sums finitely many cells. | This apparent countercontrol exposes the danger but does not apply to the printed argument. No simultaneous-limit gap. |
| Brownian independent control | Exact rational projection of finite polygonal Brownian area onto coarse increments gives $T^2(1/n-1/N)/4$, tending to $T^2/(4n)$. Exact bump integrals give a stronger Brownian bump constant $1/\sqrt{54}<1/2$. | Recovers the target normalization and prior optimum independently, including $n=1$. No contradiction. |
| Boundary and information controls | $H=1$ is endpoint recoverable; $H=1/4$ has nonvanishing $Q_m$ diagonal; coincident components or enlarged information can defeat invisibility. | All are expressly excluded. No erroneous endpoint, correlation, arbitrary-mesh or adaptive conclusion is asserted. |

The complete independent derivation is in `independent/DERIVATION.md`; further
normalization, optional radical, noncommuting-matrix and source-version details
are in `independent/ADDITIONAL_VALIDATION.md`.

The core lower bound is short enough to summarize checkably. For the printed
scaled bumps, Fourier inversion puts every witness coordinate orthogonal to
the entire grid. The upper Gram bounds give

\[
\mathbb E Y^2=\operatorname{tr}(AC)\le nM_fM_g,
\qquad M_r=D_H\overline P_r/$2\pi$.
\]

Fixed-mesh refinement and ordinary deterministic Riemann sums give
\(\mathbb E[X_TY]=na(T/n)^{2H}\). Since $\mathbb E[FY]=0$ for every
allowed $F$, Cauchy-Schwarz yields the exact displayed constant. The auxiliary
isonormal directions do not need to be path measurable in an originally
specified model: equality in law of $(X_T,\text{grid})$ transfers the bound
to every Borel grid function. No finite-$n$ coercivity or theorem equivalent
to the desired conclusion was imported.

## Primary dependency and historical source boundary

Fresh [NTU institutional journal-formatted author bytes](https://www.math.purdue.edu/~stindel/publication/papers-online/discretize-levy-area.pdf)
were independently acquired and read at Proposition 6, Remark 10, Theorem 2
and its proof, and the near/far lag split. These supply the established area
existence/canonical interface used by the paper. The reader should distinguish
that input from this note's Gaussian-witness lower-bound argument. The review
does not certify every exact coefficient in that 32-page source or publisher-PDF
byte identity.

The pinned arXiv v1 equation (27) is indeed incompatible with its own positive
lag-2 integral in equation (26). A direct lower bound gives a nonzero normalized
lag-2 contribution. The journal author version keeps near lags and discards
only the diverging-lag tail. The deposited manuscript correctly records the
version boundary and does not rely on the defective exact coefficient. The
historical submitted proof/corollary/convention files were read after the early
freeze; their older source endorsements are superseded explicitly by the current
manuscript and dated addendum. They do not introduce a present theorem defect.

Primary read boundaries and hashes are in `PRIMARY_READ_LEDGER.json`.
The [OWR contribution](https://doi.org/10.4171/owr/2012/41) has the same target
and information. The actual NS author mathematical body has $H>1/2$, a
positive normalized liminf and finite limsup, and the Brownian optimum. The
read Wu-Xiao/Xiao proof bodies establish Fourier-bump/Gaussian-projection
antecedents. These are credited prior work, not newly established inputs of
this note. No completeness/firstness claim follows from this bounded reading;
complete Dickinson/Jackowski implications remain outside this review. The
manuscript already labels full novelty, priority and worldwide openness UNKNOWN.

## Support, readers and reproducibility

All current mathematical proof bodies were read directly, not inferred from
abstracts or PASS strings. Fifteen README/SUPPLEMENT reader variants, including
the original submitted README, were assessed through the complete current root
bodies plus all historical unique added lines and full diff structure. Identical
paragraphs were not repeatedly reread. All 60 intake-classified reader-document
paths and all 225 members are inventoried with exact read boundaries in
`SOURCE_READ_LEDGER.json`; `READER_VARIANT_LEDGER.json`, `reader_deltas.txt`,
and `reader_added_lines.txt` make the comparison reproducible.

Historical acceptance/adoption words were incidentally encountered in proof
headers, reader/status/provenance text, source qualifications and the partial
static inspection of `verify_package.py`. They were treated as dated authored
assertions only. Archived favorable review bodies/verdicts remained opaque;
the full package verifier was not executed. Historical support hold/readiness
flags describe their dated preparation workflow and are not treated as evidence
that the freshly verified Zenodo record is unpublished.

`independent/controls.py` is standard-library code written before checker
inspection. It produced exact $a=4/45045$, $L_f=1/128$, $L_g=1/630$,
$N_g=113/196$, $\int(\phi'')^2=24/5005$, and the Brownian squared bump
constant $1/54$. Sixteen exact finite Brownian projection controls and 72
floating finite Gaussian conditional calculations were run. The latter cover
$H=.2501,.26,.37,.5,.73,.75,.9,.99$, $n=1,2,4$, and 2,4,8 fine cells
per observed cell. Their target is finite polygonal area, not the limiting
canonical area; these diagnostics are not asymptotic proof or validated
quadrature. The universal conclusion rests on the derivation above.

Only after the independent freeze and full static reading of the selected
programs/import was the byte-identical submitted checker run in an own
225-file quarantine. Commands are recorded in `EXECUTION_LEDGER.json`.
Both normal and optimized wrapper invocations ran original normal and optimized
children under CPython 3.14.6. All four original executions returned 0 with
empty stderr. Every non-UTC field was checked under the wrapper's explicit
contract, same-runtime normal/optimized values agreed exactly, and the three
deliberate source/pairing faults were rejected in both modes. Per run the
contract covered 115 exact nonfloat leaves, 34 exact floating inputs, 25
relative-tolerance derived floats, and 84 covariance floats.

The wrapper's marker guards test presence of text, and its sampled floats are
not interval-certified or universal. The original program's assertions are
disabled in optimized mode; acceptance there comes from the wrapper's explicit
guards and result contract. The actual outputs are under `outputs/wrapper_*`,
including raw child stdout/stderr and `FINITE_CHECKS.json`. No installer,
builder, historical run-all, release, source-write or external service program
was executed. An initial optional SymPy import was unavailable; the independent
checks were then implemented with exact standard-library fractions. That
environment probe did not affect any input or mathematical conclusion.

## Final disposition

Strongest verified claim: the complete literal Theorem 1 for every allowed
$H,T,n,F$, with the specified explicit positive $H$-only constant, subject
to its stated canonical fBm area model and the classical existence interface.
**Exact remaining central gap: null.** No new substantive defect was found.

Limitations remain exactly those printed: no sharp constant or normalized-error
limit, no H-uniform or endpoint claim, no nonuniform/adaptive mesh theorem, no
unequal-H or correlated-component theorem, and no new-priority certification.
Default follow-up: **null**. This review neither proposes an extended repair nor
authorizes publication; the parent must read the actual manuscript and complete
independent reports before adjudicating the inventory row.
