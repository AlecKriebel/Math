# Source and scope review: Nonunique nearest stable complex quadratics

Scope complete; mathematical disposition remains unassigned. This lane found no source-identity or statement-scope obstacle to a carefully qualified conditional page candidate. It does not pass Theorem 1, Proposition 3, or any helper execution, and does not authorize publication.

## Authority, identity and independence

- Assigned edition: sheet row 75; inventory index 91; work Z-23306331; Zenodo record 23306332; DOI 10.5281/zenodo.23306332; version 1.0; published 11 October 2026. The public API, queue and manuscript agree. The record is an unrefereed preprint; the six-page manuscript labels itself a research note.
- Read the active goal at `/Users/alec/.codex/attachments/97d02095-52a0-400f-a038-cbc727c7c885/goal-objective.md`, applicable Math `AGENTS.md`, and programme `MODEL_POLICY.md`. Resumption uses GPT-6.1 Sol Ultra as explicitly requested by the human. No descendant was spawned; all available slots were occupied by other assigned work.
- Owned writes are confined to this paper's `sources` acquisition records/cache and `reviews/scope`. No Git, release, spreadsheet, site, UI, deployment, source repair, outreach or promotion action occurred. The root owns publication decisions and remaining mathematical review assignments.
- Reused and revalidated the earlier raw acquisition rather than restarting it. A process inspection before continuation found no live relevant acquisition or mathematical helper to resume. Historical/sibling opinion bodies stayed opaque.
- `SOURCE_PRIORITY.md` and `SOURCE_PROVENANCE.json` were inspected only as names, lengths and raw hashes. Their bodies were not opened. Incidental authored claims in the manuscript, README and metadata, plus authored `PASS` expected-output/print literals, were encountered and quarantined as author assertions. None is accepted as independent verification.

## Exact sources and reader coverage

The live API revalidation returned exactly the cached metadata SHA256 `82e624db015b8f612e7d1eb56463b6c035130e88d4579887c3b5306ef3dd9bdd`.

| Published object | Bytes | SHA256 |
|---|---:|---|
| `nonunique_nearest_stable_complex_quadratics.pdf` | 76336 | `6439bda84f32d9a5ac1680e184975df159f51f8c7e44e609fa873dfa8ae78e1f` |
| `nonunique_nearest_stable_complex_quadratics_verification.zip` | 37068 | `2fc6b62d67ab6681c36f7d3806db549073a3f0b2e0d039817f997fab9eb96dee` |
| Complete published TeX | 20024 | `caf327484a7068244ab98494eab835f50b84521a6d7ba364007bda31f7478677` |

All six PDF pages were read in extracted text and individually rendered and visually inspected. The 385-line TeX was read in full, including both proof bodies, every displayed formula, disclosures and bibliography. This PDF is searchable, six pages, no form, no JavaScript and zero embedded files. No second reader PDF is hidden in the ZIP.

The ZIP has 12 regular file members, no nested archives, symlinks, hidden members or duplicate/path-escape members. CRC checking and independent member-to-extracted-byte comparisons agree. The actual path is the double-nested published package under `sources/published-source/nonunique_nearest_stable_complex_quadratics_verification/nonunique_nearest_stable_complex_quadratics_verification/`. `reader-manifest.json` maps all 12 bodies, including the two deliberately opaque files. The allowed code, expected outputs, hash manifest, README, metadata and license were read completely and statically. No published helper was imported or executed.

## Exact claim, assumptions and quantifiers

Write a monic quadratic as `p(z)=z²+az+b`, identify complex coefficients with real coordinates `(Re a, Im a, Re b, Im b)`, and set `S={α(p)≤0}`. Here α is the maximum root real part. Stability includes all imaginary-axis roots, including repeated roots. The base is `(a,b)=(0,0)`, representing z².

Theorem 1 claims: **for each fixed** real symmetric positive-definite metric G, **every neighborhood** of that base contains **some unstable input** with **at least two distinct attained global minimizers** over S. The claim is existential per neighborhood and metric. It is not nonuniqueness for every nearby unstable input, merely two local algorithmic minima, or projection onto an open strictly stable set.

The full-degree statement uses `(ℓ,a,b)∈C³` with `ℓ≠0`, base `(1,0,0)`, and any fixed SPD real coefficient metric on R⁶. It includes both leading-coefficient directions. This stable set is not globally closed; the manuscript explicitly clips inside a metric ball avoiding `ℓ=0`, obtains a compact stable intersection, and compares outside-ball distances to establish that its minimizers are global in the original exact-degree set. An argument that silently treated the entire exact-degree set as closed would not justify this conclusion.

The whole-epigraph result uses α(c)≤r and a fixed SPD metric on coefficient/height space. A limiting support covector is horizontal; the representing vector can tilt if the metric mixes height and coefficient coordinates. It must not be advertised as a horizontal vector in every metric.

Proposition 3 is a separate positive claim about the monic quadratic function at the origin, in the **real Euclidean coefficient metric**, relative to **each fixed finite limiting subgradient**. Constants can depend on that subgradient. Failure of whole-epigraph set prox-regularity does not by itself refute this function condition, which tests the epigraph at normal `(v,-1)`. Do not extend the proposition to uniform constants, full degree, or all coefficient/height metrics without further proof.

The manuscript's explicit controls and exclusions matter: real monic quadratics give the convex orthant `a≥0,b≥0`; the path uses an imaginary constant coefficient. No all-degree or real-only classification, arbitrary-norm theorem, singular/moving metric theorem, general nonlinear parameter-metric transfer, or explicit unstable input together with its minimizing pair is supplied.

## Original question and load-bearing references

**Lewis 2003, §8, printed166–168:** the original body explicitly takes complex polynomials, the real Euclidean metric making `z^k` and `iz^k` orthonormal, monic normalization, and the closed half-plane. Quadratics correspond to `n=1` in his set `z^(n+1)+p`. The closing stable-monic prox-regularity question is therefore an exact historical match for the note's monic Euclidean specialization, conditional on its proof. §8 was read in full; the convention and question pages were visually inspected. This source also credits earlier Clarke regularity/partial smoothness; these are not the same property as prox-regularity.

**Oberwolfach 2005, publisher printed104–106:** acquired and read the whole Lewis contribution from EMS, and the full three-page author PDF. The inherited MFO link failed with404, but the original question is now available in both primary versions. The question asks about local unique nearest stable polynomials near `s^k`; it does not explicitly fix coefficient field, monic/full normalization or metric. The surrounding talk starts with a real Belgian-chocolate example, so its short question must not be unqualifiedly relabelled a real or a complex theorem. The note explicitly chooses the complex convention tied to Lewis2003 and says it asserts no real-only answer. Closed stability is independently confirmed by the talk's α≤0 definition. The publisher question page106 was visually inspected.

**Poliquin–Rockafellar–Thibault 2000, Definition1.1/Proposition1.2/Theorem1.3:** actual primary text and selected proof bodies were read; pages5233–5234 visually inspected. The theorem requires a closed set in a Hilbert space and base point in it. Equivalence of (a) set prox-regularity with (k) local single-valued global projection has an additional local weak-closedness hypothesis, automatic in finite dimension. Thus the note's use is accurately stated for closed S and its compact clipped full-degree set. `G^(1/2)` is a fixed linear isometry for a fixed SPD real metric; this does not license arbitrary nonlinear parameter transformations. Scope confirms the imported theorem's actual hypotheses, not the note's proof of their application.

**Poliquin–Rockafellar 2010, Definition1.1, p205 and Theorem3.1:** actual primary definition, epigraph correspondence, horizon constraint qualification and composition theorem/proof were read. The function definition localizes finite subgradients and function values. The epigraph correspondence is at `(v,-1)`. The composition theorem is conditional, rather than an unconditional general equality formula for subdifferentials; the manuscript gives its own diffeomorphism argument. That argument's correctness remains an independent mathematical gate.

These are the actual question and load-bearing theorem bodies, not summaries of archived opinions. Exact acquisition hashes/read extents and unexamined proof portions are recorded in `primary-read-ledger.json` and `PRIMARY_READ_LEDGER.md`.

## Prior-work credit, gaps and novelty restraint

Bounded original-body checks confirm Burke–Overton2001's complex monic abscissa framework, real coefficient pairings and classical Clarke regularity, and Burke–Lewis–Overton2005's complex exact-degree/root context. Kirillov–Overton2013 §1 documents related real-quartic Whitney-umbrella stability geometry and credits Bottema; its Hurwitz domain is open and its quartic normalization differs. This supplies related geometry credit, not an isometric derivation of the present complex quadratic/global projection theorem.

The official DIAL record and downloadable 214-page Orban de Xivry2013 thesis were recovered. Selected original sections confirm previous complex monic nearest stable coefficient work. Definition1.60 calls asymptotic stability open; Chapter2 formulation(2.3) minimizes over its closure and explicitly accepts marginal stability. Chapter4(4.14)/(4.16) uses complex monic coefficient/companion norms and algorithmic convex approximations. The reading also covers its Moses–Liu account and start of the weighted objective discussion. This is evidence that coefficient approximation is established prior work. It is not a complete thesis absence-of-overlap audit. Poppler reported a reconstructable xref warning1707; selected text and rendered equations were readable, and bytes were not repaired.

Cross's original body remains inaccessible through the cited ProQuest record (403 and tool access failure). The manuscript's precise Example5.38/pp131–133 comparison is therefore unverified in this lane. Moses–Liu's DOI resolved but yielded an empty IEEE response; direct original wording about possible global nonuniqueness was not acquired. Bottema's DOI yielded redirect HTML, not its original body. The candidate retains scholarly credit but does not assert these unchecked detailed comparisons as independent findings. Dedicated authored priority/provenance opinions remained opaque throughout.

No firstness, current worldwide openness, absence-of-prior-result, human-peer-review or formal-certification claim is warranted. None is present in the conditional public candidate. Focused primary reading does not support an unusually strong follow-up contribution; `followup` is null. The missing direct bodies limit priority comparisons, and do not change the literal self-contained mathematical claims needing the other review lanes.

## Reproducibility support and exact remaining gap

`verify_exact.py` statically describes 2,005 finite rational assertions over 80 positive t values and mixed SPD controls; `verify_function_boundary.py` uses deterministic 90-digit Decimal boundary/support controls with a fixed seed; expected outputs are authored JSON. Neither is a projection solver. Finite identity checks cannot alone establish limiting-normal membership, a universal fixed-metric claim, local-to-global projection equivalence, compact localization, or the whole analytic function proof. The Decimal controls are not interval-certified. No helper result is claimed by this review.

The strongest result of this lane is a source-bound, exhaustive reader inventory and statement/reference-scope assessment. Independent analytic and adversarial review of Theorem1/Proposition3 and meaningful reproducibility remain to the root. A substantive defect found there should defer the paper under the project workflow. This lane offers no repair and no promotion.

`public-candidate.json` contains the complete original abstract, exact dated edition metadata, conditional accessible/central-result wording, limitations, original literature credit, AI/unrefereed disclosure and null follow-up. It is an internal candidate with an explicit mathematical/publication gate. No public page or progress-sheet row was changed.

## Artifacts and disposition

- `CUSTODY.json`: fresh API/queue/file/ZIP/member custody.
- `reader-manifest.json`: complete published reader and support coverage, including opacity decisions.
- `SUPPORT_MAP.md`: what each allowed support file can and cannot support.
- `claim-map.json`: exact four-claim scope and boundary cases.
- `primary-read-ledger.json` and `PRIMARY_READ_LEDGER.md`: independent actual-primary read extents and access gaps.
- `public-candidate.json`: conditional full-abstract page content; no promotion authority.
- `verdict.json`: completed scope, no mathematical disposition.
- `LOG.md`: timestamped progress and estimates; `SCOPE_SEAL.json`: final hashes.

Assigned source/scope completion:100%. Overall inventory completion is not estimated by this lane. All remaining scientific and publication gates stay pending; no frozen other review was rewritten.

