# New complete independent acceptance gate: PR23 / 30002145

**PASS for the current scoped source-status partial result.** Recommend `already_solved` for the original whole-space/local blow-up interpretation of OWR-12008-005, with no new mathematical discovery, paper, Zenodo deposit, DOI, release, or publication-tracker entry. No current mathematical or source-claim edit is required. The parent owns integration and the separately reviewed durable accepted-state infrastructure.

This is a new complete review, not a transferred historical verdict or a hash-only delta check. It binds original PR head `ea6b192f7e3bc094b78bbc416bf61c609ffa5b2d`, current `SOURCE_STATUS.md` SHA256 `f3c383ff5a55ac755994b9af0108e9453f9715dc22d5b51f412ac5b15b2832eb`, and current 18-entry `MANIFEST.json` SHA256 `40d0e7dbcf5f8d15d8383c882994af6d2d9e47852d0f3595a07fff9baf653ad3`. All original 14 head-bound files and all current 18 entries verify. The preserved old PASS binds the old source hash and is not evidence that changed bytes were already reviewed.

The audit completed on 2026-10-01 UTC. Original substantive proof attempts remain **0/5**; validation added **zero**. This is extensive AI verification, not human refereeing or formal proof-assistant certification. Audit completion estimate: **100%**; completion toward a novel result: **0%**, because positive established coverage was verified.

## Independence, success criterion, and inputs

`FIRST_PASS.md` and `FIRST_PASS_SEAL.json` were written at 20:29:52 UTC before historical/root/family detailed reports, scripts, computation receipts or findings were read. The sealed SHA256 is `93e6a5f04610aabca5d9c193bf566d8e229eece0a3bb635bd8b6c7e54aa3afab`. The first pass read root and queue AGENTS instructions, the literal pinned source record, current scientific/source-scope claims, and freshly retrieved primary documents. Present candidate scope summaries mention earlier reviews; no earlier detailed proof, code or verdict was used to generate the first-pass reconstruction. No strictly blind claim is made about the subsequent reproduction stage.

The criterion required full primary coverage of signed strains, universal necessity rather than smooth sufficiency alone, correct oblique domain/displacement transformation, independent/parallel/zero/dimension-one cases, weak profile regularity, the rigid kernel, local versus arbitrary-domain scope, exact provenance and budgets, accurate current PR scope, and a conservative known-result disposition. An early defect would not end this audit. These criteria were not weakened after seeing earlier outcomes.

Primary inputs were independently downloaded into ignored `tmp/primary/`. `PRIMARY_DOWNLOADS.json` records URLs, UTC times, bytes and SHA256 values. I read the complete Rindler OWR contribution pp2247-2249; the complete published 2020 Theorem2.10 statement and proof pp399-402, including the separate third case; its relevant two-dimensional signed propositions and rigid-kernel lemma; the positive tangent Theorem3.2 and selected-good-blow-up context; and the 2011 two-dimensional prior with relevant Sections4.2-4.4 proof dependencies. Relevant statements/dependencies in both 2016 papers were also inspected. OWR p2248 and published pp399-402 were visually checked. Foreign PDFs, extracted text, renders and copied scripts remain ignored.

## The original target and established coverage

The imported record asks for structure under the fixed symmetric-product line inclusion but supplies no domain, regularity threshold or requested final conclusion. Its dated assessment asserts incomplete coverage while citing the 2020 paper. Its typography-only/self-contained extraction assertion is therefore too strong. The full [OWR36/2012 Rindler contribution](https://publications.mfo.de/bitstream/handle/mfo/3307/OWR_2012_36.pdf?isAllowed=y&sequence=1), pp2247-2249, explains a published lower-semicontinuity proof: the question introduces structural analysis of blow-ups, the simple separated guess is rejected, and a second blow-up produces the required structure. The initial variational domain is bounded Lipschitz; that introductory domain does not imply a single global profile theorem there. Whole-space/local blow-up interpretation is supported by context rather than explicitly specified by the extracted sentence.

[De Philippis-Rindler2020](https://www.aimspress.com/aimspress-data/mine/2020/3/PDF/mine-02-03-018.pdf), Theorem2.10, expressly assumes `u in BD_loc(R^d)` and `Eu=P nu` for a signed locally finite scalar Radon measure. Its symmetric-product cases give BV one-variable profiles; parallel profiles have locally Lipschitz primitives with BV first derivatives. The relevant content agrees with arXiv v2. Part(iii) is a separate elliptic smoothness assertion outside this target; reading it is not a claim to have independently certified every result in the paper.

The [2011 paper](https://arxiv.org/pdf/1008.2089), Section4.4, Propositions4.7/4.9 and Example4.8, treats the two-dimensional `LD_loc` version with absolutely continuous coefficients and explicitly omits its BD extension in that section. The quartic example is prior work. Earlier positive-polar/tangent lemmas have different hypotheses, including a wording caveat discussed below; they cannot substitute for signed arbitrary-strain coverage.

The [2016 A-free paper](https://arxiv.org/pdf/1601.06543), Theorem1.1 and its BD corollary, constrain singular polar directions. The [2016 Young-measure paper](https://arxiv.org/pdf/1604.04097), Lemmas2.10/2.14, gives selected good/very good singular blow-ups, using the polar and localization results. These types and quantifiers differ from a classification of every displacement with an arbitrary signed scalar strain. Current `CURRENT_SOURCE_SCOPE.md:9` correctly distinguishes them.

## Independent universal reconstruction

All arguments below concern connected product boxes or the full Cartesian space unless another domain is stated. They are deductions from distributional identities, not empirical extrapolation from finite symbolic dimensions. They independently check the two target mechanisms, including the closure that the published proof compresses into regularization.

Write `E_ij=(D_i u_j+D_j u_i)/2`. Commutation of distributional derivatives gives

```
D_ij u_k = D_i E_jk + D_j E_ik - D_k E_ij,
C_ijkl = D_ik E_jl + D_jl E_ik - D_il E_jk - D_jk E_il = 0.
```

If `Eu=0`, the first identity annihilates every second derivative. On each connected open component, each first derivative is constant; `u=Rx+c`, and the strain equation makes `R` skew. This kernel conclusion needs no simple-connectivity assumption. It closes necessity after constructing any field with the same strain.

### Independent inputs and oblique transformation

For independent `a,b`, form `S=[a b c3 ... cd]` with an orthonormal basis of their orthogonal complement and put `B=S^(-T)`. Then `B^T a=e1`, `B^T b=e2`. Use both transformations

```
x=By,       w(y)=B^T u(By).
E_y w(y)=B^T E_x u(By)B                    (smooth),
E_y w(A)=|det B|^(-1) B^T Eu(BA) B         (Radon measures).
```

Thus the transformed coefficient is `|det B|^(-1)(B^(-1))_#nu`. A spatial change alone is invalid, and replacing the absolute determinant by its signed value is invalid. Skew matrices stay skew under the corresponding congruence. Canonical coordinates are `y1=x.a`, `y2=x.b`; the transverse basis remains orthonormal. No orthogonality or unit assumption is imposed on the original independent vectors.

For canonical `E=(e1 odot e2)nu`, compatibility entries `C_1212`, `C_1r12`, `C_2r21`, `C_1r2s`, for `r,s>=3`, force

```
D12 nu=0;       D1r nu=D2r nu=0;       Drs nu=0.
```

Consequently every transverse first derivative is a constant distribution. Subtract its affine density. The remaining coefficient is independent of transverse variables and has zero mixed derivative in the first two variables, hence is the sum of two one-variable distributions. The product-domain rule follows by subtracting coordinate averages from test functions: a compact test of zero integral has a compact antiderivative, so a zero coordinate derivative forces tensoring with Lebesgue measure. Applying that fact to the mixed equation gives the separated sum. It works globally on `R^d` and locally on a box.

Because the coefficient is a Radon measure, fixed compact averaging tests in the other coordinates recover the separated distributions as locally finite signed measures, up to harmless constant-density redistribution. Their one-dimensional primitives are `BV_loc`. Integrating the affine transverse density gives precisely the three quadratic blocks in `SOURCE_STATUS.md:31-33`, with constant transverse `v`; their mixed strains cancel, and the surviving coefficient is the expression at line40 with factor `2x.v`. The rough version interprets the profile derivatives as lifted Radon measures. For a nonunit covector `a`, writing its derivative as hyperplane measure introduces the coarea factor `1/|a|`; the nonunit transformation must not omit it. Subtracting this constructed field from the original leaves only the rigid kernel.

For smooth coefficients, evaluation on coordinate axes after subtracting the transverse affine part selects smooth one-variable profiles; integrating gives smooth displacement profiles. There is no unsupported promotion of an arbitrary BV representative to smoothness. In dimension two the transverse space is zero, so no quadratic transverse term remains.

### Parallel inputs and weak regularity

For nonzero parallel vectors, `a odot b=kappa(e odot e)` for a unit direction `e` and nonzero real `kappa`. Every scale and sign, including negative `kappa`, is absorbed into signed `nu`. In adapted coordinates `(s,t)`, canonical compatibility for `E=e1 odot e1 nu` is exactly the zero transverse-Hessian condition `D_r D_s nu=0` for transverse indices. Product-domain integration gives

```
nu = mu(ds) tensor L^(d-1) + sum_j gamma_j(ds) tensor [t_j L^(d-1)].
```

These initially distributional coefficients are measures: choose compact transverse tests whose zeroth/first moment vectors form a dual basis. Pairing the original Radon measure with each fixed test extracts `mu` or one `gamma_j`, with local total-variation bounds controlled by its sup norm. Such tests exist even on boxes far from the origin, by invertibility of the moment Gram matrix of `1,t_2,...,t_d` against a positive compact weight. This does not rely on cancellation hiding an infinite-variation profile.

Integrate `mu` once, obtaining `H in BV_loc`. Integrate each `gamma_j` twice: its first primitive is BV and bounded on compact intervals, and the second primitive `P_j` is locally Lipschitz with `P_jprime in BV_loc`. Then the field at `SOURCE_STATUS.md:48-49` is locally integrable; its mixed measure terms cancel, and its strain is exactly line55. Subtraction again leaves the rigid kernel. The smooth specialization and absolutely continuous `W1,1/W2,1` specialization follow by smooth or `L1` coefficient extraction and integration. Arbitrary distributional profiles are not admissible BD profiles; the earlier family explicitly tests a derivative-of-Dirac violation, and its mechanism was checked.

### Zero, dimension one, and positive tangent scope

Over the reals,

```
2||a odot b||_F^2 = |a|^2 |b|^2 + (a.b)^2.
```

Thus a vanishing product means at least one input is zero. The inclusion then gives the componentwise rigid kernel; the scalar coefficient is undetermined. In dimension one a nonzero product spans every scalar strain: arbitrary sufficiently regular maps, and arbitrary locally BV maps in the measure formulation, are allowed. The zero case has constant maps on each component.

The positive tangent theorem is different. On the whole space, a nonnegative scalar measure cannot retain an independent affine transverse term: translations of a compact transverse test make its mass arbitrarily negative if that term is nonzero. The same translation argument kills each parallel transverse coefficient measure. On bounded boxes positivity alone does not do this. New explicit positive-on-box examples retain the independent `v` term and parallel variable coefficient. Hence neither signedness nor domain can be suppressed while importing a simpler tangent normal form.

## Local boxes and the exact globalization boundary

Every interior point of an open domain has a sufficiently small adapted product box. The above integration proves a local classification there. A connected arbitrary domain can have disconnected coordinate slices, so separate branches need not share global profiles. This is a genuine boundary, not an unfinished proof of the whole-space claim.

In addition to reproducing the prior connected polygonal countercontrols, this audit checks the smooth annulus `1<x^2+y^2<9`. Let `f(t)=exp(-1/(1-t^2))` for `|t|<1`, extended by zero; flatness makes it smooth. For independent `e1,e2`, put `u=(f(y),0)` on the right branch with `|y|<1`, and zero elsewhere on the annulus. The strain remains in the fixed line, and the branch joins smoothly. At `(-2,0)` and `(2,0)`, first components differ by `exp(-1)`. Every global two-dimensional independent template plus a rigid motion has equal first components at equal `y`, a contradiction.

For the parallel case put `u=(y fprime(x),-f(x))` on the upper branch with `|x|<1`, and zero elsewhere. Its strain is `y fsecond(x)(e1 odot e1)` there and zero elsewhere. At `(0,-2)` and `(0,2)`, second components differ by `-exp(-1)`. A global parallel template plus rigid motion has second component depending only on `x`, again a contradiction. These smooth-boundary examples supplement the prior simply connected polygonal examples; topology of the rigid kernel is not the issue. No arbitrary-domain global profile claim is certified. The original domain-free extraction does not specify a separate residual problem to pursue.

## Exact integrity, scope, provenance, and history

`INTEGRITY_RESULTS.json` records the complete read-only checks. The actual PR merge base is `01358d66fc67d1c462bddf31c0d4ee5b120e6737`; the base-tip is `60292bed09f59236aa192cb17aa138f7b4750e1a`. The merge-base diff equals the current live GitHub changed-file list: 14 numeric-folder files plus `QUEUE.md`. Exactly the selected30002145 row changes, retaining `0/5` and changing its status to `already_solved` with explicit source/domain/novelty qualifications. Main may advance under the parent while this audit runs; this certificate is bound to the fixed reviewed head and candidate bytes, not an arbitrary evolving main tip.

The current live PR readback, preserved in `LIVE_PR_READBACK.json`, confirms head, base, draft/open status and accurate current body. Its body equals current `PR_DRAFT.md` byte for byte and acknowledges both the numeric folder and selected queue row. It promises a known-result partial after the new gate and expressly excludes paper/DOI/release/tracker action and unrestricted global profiles. The checkpoint's pending-gate fields accurately describe the package being reviewed; the final acceptance evidence is this separate artifact, not a retroactive rewrite of earlier certificates.

All original14 snapshot bytes equal `git show` at the exact head. All current18 manifest lengths/hashes verify. Ten original paths remain unchanged in their current locations; original draft/provenance are retained byte-identically under `ORIGINAL_*`; current README and SOURCE_STATUS replace their administrative headers. Every original mathematical/source section from `## 1.` onward in SOURCE_STATUS remains byte-identical. Historical logs, source_record, turns, review, scripts and result receipts remain untouched. Old source hash `ff80528de521556c537c8dd67868b8cc4aaa680ba011c61ce594dfad70216ef3` differs from the current hash; the old reviewer certification explicitly remains about its frozen input.

The pinned dataset revision is `37e53eabe540fb458758e198be61634bd02ee008`. Complete cached source corpora match their head manifest: problems68,931,837 bytes/SHA256 `04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf`; research_results80,334,822 bytes/SHA256 `8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b`. The selected JSON record equals the unique numeric-ID record, has unique code within this corpus, and its bytes hash to `c8cd6673870f7bab593b64534a776ee406924e6fd5351bfdb57881ebc09aa4c2`. Full exact ID/code/title queries find no matching prior report; normalized exact statement comparison finds no other record; exact related-group queries find no entry. These precisely bounded absence checks are not worldwide novelty claims or proof that no differently worded relative exists.

The selected exact-head state/history contain no disposition/event; turns.json is an empty substantive-attempt list with used0/limit5; both original and current queue rows retain0/5. Historic branch/PR absence claims predate this PR and are not claims of current absence. `GIT_HISTORY.json` confirms that the queue-edit commit followed the attempt-package commit, explaining the stale exclusion sentence in the historical draft/provenance. Current qualifications supersede it without destroying that chronology. No readiness, proof-search, candidate-turn or verified-new-discovery lifecycle event was invented.

The unchanged legacy desk/catalog assessment would default this record back to queued if the old generator were run. Current acceptance notes disclose this operational mismatch; the parent is separately reviewing durable state/history synchronization. This gate does not certify that infrastructure or authorize overwriting queue/catalog/assessment history. No legacy queue/rank generator was invoked. The manuscript/publication result is known prior coverage, so new-result lifecycle gates are inapplicable rather than bypassed.

## Full reproduction and new falsification controls

I read the complete root reconstruction/source ledger/reproduction reports, all three full family reports/certificates/verdicts/logs, the historical review and both original scripts, and each family script. The family manifest hashes and every bound file verify (primary16, signed11, compatibility8). The root openly records that its persistent seal followed an early family message; it is not treated here as a strictly blind certificate. The families' separate earlier seals preserve their own declared independence. Their distinct mechanisms are universal compatibility/displacement nullspace, signed weak-action/regularity extraction, and primary-source/domain/type/provenance scrutiny.

`replay_all.py` runs ignored byte-identical copies with `/usr/bin/python3`3.9.6 and SymPy1.14.0. Original8 and historical11 outputs reproduce byte for byte. Compatibility19 and signed19 reproduce byte for byte. Primary10 matches all mathematical/source fields after excluding its timestamp and Python version text. The pinned-source script also reproduces all provenance fields; its scratch copy changes only one repository-path assignment and excludes the resulting script-hash/timestamp differences. `REPLAY_RESULTS.json` records each script/output hash, exit code and exact permitted exclusions. No copied script wrote to original or candidate directories.

The root's earlier receipts agree with these independently reproduced values. Primary-family missing-dependency runs, the signed-family Boolean conversion failure and initial17 versus final19 count correction remain preserved and were not concealed as successes. No mathematical contradiction was repaired by changing the candidate.

`fresh_controls.py` adds **13 new grouped controls**, recorded in `FRESH_RESULTS.json`:

| Mechanism | Exact evidence and adversary |
| --- | --- |
| Fully oblique4D compatibility | Independent coefficient Hessians have rank2 template span and constraint rank8; parallel Hessians have template rank4 and constraint rank6. The inputs use every coordinate. |
| Weak signed oblique strain | Direct integration of two signed jumps on an oblique parallelogram with determinant`-1/7` gives scalar action`-242905/979776`; absolute-Jacobian congruence matches the full strain matrix, while signed-Jacobian substitution fails. |
| Shifted-box measure extraction | Exact dual moment matrix on `(2,5)x(-3,-1)` equals identity; Gram determinant`22674816/765625` is positive. Atomic/density coefficient actions recover `-159713/272160`, `117/112`, `-5632/1701`. |
| Local positivity | Positive box coefficients `3+2z` and `4+(2+s)t` retain transverse structure; explicit whole-space negative witnesses prevent using them as positive global tangent measures. |
| Degenerate edges | Exact real zero-product norm identity and direct signed atomic BV weak pairing in dimension1. |
| Earlier positive-polar source wording | `u=(-x2,0)` has an allowed BV profile shape but the opposite polar to the printed2011 positive-polar lemma; arbitrary profile shape alone is not sufficient for that lemma's fixed positive polar. |
| Smooth-domain globalization | Both independent and parallel smooth annulus branch fields satisfy the inclusion but contradict one global profile family modulo rigid motion. |

The new suite initially completed all assertions and then failed serializing a SymPy integer to JSON. `CONTROL_RUN_HISTORY.md` and the ignored initial script preserve that run; the repair only adds a serializer fallback. A subsequent12-control run passed; after reading the2011 dependency wording, the13th source countercontrol was added and the final13-control run passed. Equations, expected values and tolerances were not changed to hide any assertion failure. There are no numerical tolerances or random searches.

Finite polynomial, symbolic and weak-action controls remain supplemental. C1 compact piecewise-polynomial weak tests vanish with first derivatives at their boundaries; strain action extends from smooth tests by C1 approximation for these L1 displacements. The universal distributional deduction and the signed primary theorem are the completeness evidence. Tests alone cannot certify arbitrary dimensions, regularity closure, a theorem on a new domain, or novelty.

## Findings, repairs, and disposition limits

| Item | Classification | Present consequence |
| --- | --- | --- |
| Old draft says no shared queue edits | Historical repaired P2 | Current draft/live body/provenance and CURRENT_SOURCE_SCOPE acknowledge the exact selected row. ORIGINAL_* and the historical log remain evidence. No current correction required. |
| Upstream extraction calls itself self-contained | Historical imported defect | Current scope explicitly qualifies missing domain/regularity/conclusion. Preserve source bytes; do not promote the extracted fragment to an unrestricted theorem. |
| Printed2020 `a!=+/-b` | Source precision issue, already handled | Unequal collinear or zero inputs satisfy that literal inequality. The candidate's independent/parallel/nonzero/zero split is correct and independently proved. |
| Printed basis-reduction shorthand and repeated parallel index/factor wording | Source precision issue, already handled | Proper two-sided oblique congruence and coefficient-based reconstruction avoid those slips. |
| Printed2011 positive-polar iff sufficiency | New source precision countercontrol | For canonical independent vectors, a negative linear BV profile has the right shape but wrong fixed positive polar. This does not affect the signed LD propositions or current signed theorem/formulas; no candidate edit is needed. |
| Original legacy machine default | Separate parent infrastructure work | No mathematical acceptance blocker; no generator executed or durable-state result certified by this gate. |
| Arbitrary connected nonconvex globalization | Explicit excluded assertion, positively falsified | The whole-space/local source correction remains valid. A differently specified global-domain research problem would need a new formulation and budget. |

There are **no unresolved actionable P0/P1/P2 findings against the current scientific/source package or live scope**. Historical repaired issues are not recycled as current blockers. Source print defects are not silently accepted as valid hypotheses; they are resolved by the precise geometric split, signed theorem type, correct transformations and independent deductions. No route transfers the central difficulty to an unsupported equivalent assertion.

Strongest verified claim: for each real fixed symmetric-product line, all locally BD whole-space displacements with signed scalar Radon strain have the indicated known independent or parallel normal forms modulo the infinitesimal rigid kernel, with the stated BV/derivative-BV regularity and every zero/dimension-one case. The corresponding smooth classification holds locally on adapted boxes. The whole-space/local interpretation is supported by the complete original explanatory blow-up context.

Exact remaining gap: the domain-free extraction does not define a separate arbitrary-domain global theorem; a naive single global profile representation on connected nonconvex domains is false. No new open-problem resolution, worldwide status conclusion, formal proof certification, or publishable discovery follows. The conservative accepted disposition is `already_solved` for the original interpreted source item, merged as a **known-result source-status partial** with the scope notes and immutable historical artifacts retained. Any accepted-state administrative update must preserve these bindings and conditions; a substantive scientific change requires fresh review.

Only files under this `final_adversary/` directory were written. No Git/PR/canonical/global mutation, installation, publication, external-person contact, or new proof-search attempt was performed. Reproduction commands and hashes are first-party artifacts; the final `MANIFEST.json` excludes itself and ignored scratch material.
