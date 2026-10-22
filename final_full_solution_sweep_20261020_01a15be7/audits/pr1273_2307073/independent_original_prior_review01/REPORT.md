# PR1273 / 2307073 — independent original/prior review01

The full original Hayman–Lingham Problem 7.73 has a negative answer: for every fixed radius R>0, no finite additive intersection constant A(R) works for arbitrary domains in the radius-R disk. The pinned PR proves this correctly. The same result and punctured-disk mechanism already appear in Yixin He and Quanyu Tang, *On Fuchs's additive intersection problem for the hyperbolic metric*, arXiv:2603.16676v1, Theorem 1.2 and §3. Recommend a credited existing-preprint accounting row, subject to root adoption. Do not publish this exposition as a new or first resolution.

This is an AI-assisted independent internal audit of the supplied argument, not external human review or a proof-assistant certificate. It is separate from the PR's authored acceptance note. No author, person, other agent, or chat was contacted. No source-author software was run. No service writes, CASE/cursor changes, Git mutations, or credentialed requests occurred. Only public primary-source GET requests and local review/diagnostics were used. `publication_ready=false`; `root_adopted=false`.

## Exact input and original target

The head is `32e8b9914ed26fbba30c102f7ce109458b0d521c`. All six actual attempt files were copied from existing immutable Git objects without fetching, checking out, or changing refs/index/worktree. Both their Git blob SHA1 and SHA256/size were authenticated. `INPUT_BINDING.json` records every identity. The full 7,575-byte proof has SHA256 `f7bc2c85584c827885912cb4adc748cb453777f4018c4c908e538ff386699a39`. The submitted manifest, editorial map, README, acceptance note, and source-verification record were also read completely; there is no QUEUE change among these six paths.

The primary original is Hayman–Lingham, *Research Problems in Function Theory (New Edition)*, [arXiv:1809.07200v2](https://arxiv.org/abs/1809.07200v2), Problem 7.73, printed p.183 / PDF p.184. Its question allows domains D1,D2 inside |z|<R and asks for the least A(R) making the hyperbolic density of their intersection strictly smaller than A(R) times the sum of their individual densities at every common point. It does not require simple connectivity, smooth boundary, or absence of isolated punctures. The listed proposer is W. H. J. Fuchs. The historical update reports no progress as of that edition; it is not evidence of current openness.

An intersection may have multiple components, but the construction below has a connected intersection. Thus there is no ambiguity about which component's hyperbolic density is used, and the obstruction holds even after imposing connected intersection.

## Fresh primary authentication and inspection

At 2026-10-22 09:49 UTC, both versioned PDF URLs returned HTTP200. Fresh binaries exactly match the submitted size/SHA256 pins:

| Source | Bytes | SHA256 |
| --- | ---: | --- |
| Original arXiv:1809.07200v2 | 1,706,228 | `8e28fd4403a07e4e19a9816b7efaafddf9f475d59cf8c34a8255cb03833ed4f0` |
| He–Tang arXiv:2603.16676v1 | 532,041 | `83b2cb1d7579ab337630c9613018ffd6816d5a5628f0aa475e74832c1e14946f` |

The original question at PDF184 and He–Tang PDF2,3,4,5,10 were read from text and visually inspected. These include all target-specific essential proof bodies: setup/component convention/normalization, Theorem1.2, equation2.1, Lemmas2.1–2.6, and the complete §3 argument. He–Tang PDF1/13–14 were additionally read for attribution, scope, concluding distinctions and references. This is not a whole-book or whole-paper acceptance.

The [versioned primary record](https://arxiv.org/abs/2603.16676v1) identifies Yixin He and Quanyu Tang, submission 17 March2026 15:41:23UTC. The current primary record lists only v1 and no journal reference. The [arXiv DOI](https://doi.org/10.48550/arXiv.2603.16676) freshly resolves to that current record. The [DataCite primary registration](https://api.datacite.org/dois/10.48550/arxiv.2603.16676) confirms the title, authors, arXiv publisher, preprint resource type and v1 submission timestamp. It does not supply a journal DOI. Treat this as an existing arXiv preprint; no journal publication or peer-review status was verified. Bounded searches are not proof that no other publication/refereeing exists.

The submission's 11October optional fresh-download failure is preserved as a historical statement in its unchanged files. It is superseded for present source access by successful fresh exact binary comparisons in this review. It is not a reason to label the target proof body unavailable.

`SOURCE_REVIEW.json` gives read scope and dependencies. All acquisition metadata, exact PDFs, fresh text extractions, landing pages, DataCite JSON and visual evidence are private local review evidence. They are not included in the proposed public accounting row. No source text/PDF redistribution or release is authorized here.

## Independent complete derivation

Use curvature−4 normalization λ_D(z)=1/(1−|z|²), where D is the unit disk. Multiplication of every metric by the same positive constant cancels from the quotient, so the conclusion does not depend on choosing this convention.

For a hyperbolic domain G and universal cover π:D→G, the metric is characterized by

\[
\lambda_G(\pi(\zeta))|\pi'(\zeta)|=\frac1{1-|\zeta|^2}.
\]

Composing coverings proves conformal invariance. In particular, for t>0,

\[
\lambda_{tG}(tz)=t^{-1}\lambda_G(z).
\]

For G⊂H, choose covers π_G,π_H taking0 to the same point z. The inclusion composed with π_G lifts as π_H∘f=π_G with f:D→D and f(0)=0. The Schwarz lemma gives |f′(0)|≤1. Therefore |π_G′(0)|≤|π_H′(0)|, and reciprocating shows λ_G(z)≥λ_H(z). This explicitly fixes the direction of the inequality needed below. Non-strict monotonicity suffices; no strict equality theorem is needed for the target.

Put H=C\{−1,1}. This connected noncompact domain has a disc universal cover. In detail, universal-cover existence and uniformization give sphere, plane, or disc as its simply connected covering surface. A compact sphere cannot map surjectively onto noncompact H. A plane cover would give a nonconstant entire function omitting both−1 and1, contradicting Little Picard. Thus a holomorphic covering π:D→H exists. Taking π(0)=0 defines

\[
m=\lambda_H(0)=|\pi'(0)|^{-1}\in(0,\infty).
\]

Its positivity and finiteness follow from the finite nonzero derivative of a local biholomorphism. H,π and m are fixed, independent of a and R. No numerical evaluation or explicit formula for m is needed. Universal-cover existence, uniformization, Little Picard, and Schwarz are standard foundational inputs, explicitly used here rather than silently transferred to an unsupported target lemma. Bounded punctured disks are hyperbolic as well: the plane possibility would produce a nonconstant bounded entire covering map, excluded by Liouville.

To derive the one-puncture formula, map the left half-plane L={Re w<0} to D by c(w)=(w+1)/(w−1). Direct algebra gives |c′(w)|=2/|w−1|² and 1−|c(w)|²=−4Re(w)/|w−1|². Hence λ_L(w)=1/(−2Re w). The exponential map L→D\{0} is a surjective unbranched universal cover. Its derivative has absolute value |exp(w)|. Writing z=exp(w), covering invariance yields

\[
\lambda_{D\setminus\{0\}}(z)=\frac1{2|z|\log(1/|z|)},\qquad0<|z|<1.
\]

This is a full derivation of the standard formula cited in He–Tang Lemma2.5; the target does not depend on an uninspected central assertion from the cited Beardon–Minda chapter.

For real0<a<1/2 take G_a=D\{a}, K_a=D\{−a}, and U_a=D\{−a,a}. The disk automorphism φ_a(z)=(z−a)/(1−az) sends G_a to D\{0}. Since φ_a(0)=−a and φ_a′(0)=1−a²,

\[
\lambda_{G_a}(0)=\lambda_{K_a}(0)=\frac{1-a^2}{2a\log(1/a)},\qquad
\lambda_{G_a}(0)+\lambda_{K_a}(0)=\frac{1-a^2}{a\log(1/a)}>0.
\]

All three sets are open, nonempty and connected. For connectedness, given any two allowed points in a convex disk, choose an intermediate disk point outside the finite union of lines through an endpoint and an excluded puncture. The two connecting segments stay inside the disk and avoid every puncture. The base point0 is interior for each a>0. Thus U_a is the entire intersection component containing0.

Now U_a⊂C\{−a,a}=aH. Monotonicity and dilation give

\[
\lambda_{U_a}(0)\ge\lambda_{aH}(0)=\frac ma.
\]

Dividing by the exact positive sum above gives the decisive lower bound

\[
Q_a=\frac{\lambda_{U_a}(0)}{\lambda_{G_a}(0)+\lambda_{K_a}(0)}
\ge\frac{m\log(1/a)}{1-a^2}\longrightarrow+\infty\quad(a\downarrow0).
\]

For every finite A>0 choose0<a<min(1/2,exp(−A/m)). Then m log(1/a)>A and1−a²<1, so Q_a>A. Nonpositive A are impossible because the densities are positive. This disproves both strict and non-strict finite uniform upper bounds, with no endpoint ambiguity. Infinity is the supremum, not a finite attained value proposed as an admissible constant.

Finally fix any R>0 and scale the domains to G_{R,a}=D_R\{Ra} and K_{R,a}=D_R\{−Ra}. The intersection is RU_a. Each of its three densities at0 is its unit-radius counterpart divided by R, so the quotient remains Q_a and is unbounded. R can be arbitrarily small or large but is fixed before a is chosen. This proves the exact original all-R assertion.

## Falsification families and boundary checks

| Approach family | Attempted obstruction / check | Result and exact limit |
| --- | --- | --- |
| Original-scope audit | Perhaps original assumes simple connectivity, regular boundary, or connected intersection | Original imposes none of the first two; present intersection is connected. Full original general-domain target is covered. |
| Covering/metric audit | Reverse monotonicity, lose a derivative or factor2, or let m vanish | Explicit lift/Schwarz argument, Cayley/exponential derivation and fixed-cover derivative establish correct sign, normalization and m∈(0,∞). |
| Degeneration/scaling audit | Taking a=0 illegally, confusing dependence on R, or using a limit where the base point leaves the domain | Only0<a<1/2 is used;0 stays interior for every selected a. All quantities exist before taking the limit. All-R scaling cancels exactly. |
| Prior-source audit | The attributed source merely announces an unavailable theorem or proves a different class | Fresh matched v1 PDF contains Theorem1.2 and the entire same §3 mechanism and essential metric lemmas. This is a verified existing proof, not merely an abstract announcement. |
| Accounting identity audit | Conflate all records named Fuchs or omit broad aliases | All returned ledger cells and complete raw record strings/keys were scanned. Three Fuchs rows concern D.Fuchs billiards/dodecahedra; twelve other generic-word leads concern different mathematical objects. No direct target alias hit. Root adoption remains required. |

The proof is decisive. The finite diagnostics are corroboration, not a numerical computation of λ_H(0), a proof by sampling, or a formalization of uniformization/Picard. No positivity threshold is inferred from floating point. A supplementary exact dyadic quantifier control uses log2=∫₁²dt/t>1/2: for positive m and any A>0, choose integer n>max(1,2A/m), a=2^(−n), and obtain m log(1/a)/(1−a²)>mn/2>A. This also makes the constructive quantifier choice transparent without evaluating m.

## Diagnostics and historical failure

`check_review.py` uses standard-library exact rational arithmetic for Gaussian-rational Möbius/Cayley identities, the abstract cover-derivative inclusion direction, formal positive-m quantifier choices and puncture-avoiding rational paths. Decimal arithmetic at85digits checks derived formula consistency and radius/normalization cancellation; it is explicitly labeled diagnostic. Independent inputs are in `CONTROL_INPUTS.json`. Guards use explicit exceptions and remain active under optimization.

The first edition completed source authentication and mathematical diagnostics, then failed an overly narrow record-description keyword guard: record23389367's full description concerns signed trajectory types but lacks the literal words billiard/dodecahedron. Its exact title and mathematical topic were already read. That normal run is failed, preserved, and not part of the accepted matrix. O/OO01 never ran. `private/replays01_failed`, `AUTHENTICATED_INPUTS01.json`, `private/historical/check_review01.py` and `FAILURE_INTERPRETATION01.json` preserve the raw output, old code and freeze. The correction binds exact known id/concept/DOI/title tuples in addition to retaining full raw-record hash anchors and separate explicit semantic adjudication. No mathematical or submitted source bytes changed.

Edition02 froze41local input pins before testing. Its checker SHA256 is `8b805077d4c6e22dd35865531574355f98bc8e3ba1aa5c1db14749b16b515535`. Normal,−O and−OO each complete with the same positive counts:20exact interior Möbius cases,20boundary cases,4Cayley cases,10dyadic formula cases,150radius/normalization cases,16abstract derivative-direction cases,16formal positive-m quantifier cases and12rational path constructions. Four deliberately wrong-science checks are rejected per mode. A separate deliberate unconditional failure exits1 in each mode, confirming optimization-safe guards. Every positive run exits0. All modes use the same frozen checker and input pins. `VALIDATION.json` and `private/replays02` retain exact commands, statuses, stdout/stderr and hashes. No source-author program, network call, or real service action occurs in the checker.

The earlier draft metadata utility also initially used the wrong key while reading the previous review's manifest; it was corrected to the actual `entries` schema before preservation checking. This was a preparation error, not a scientific test failure. All77manifested PR1267 payloads subsequently rehashed unchanged; no old review was modified. Its manifest remains SHA256 `b2a9c935b37a3154e911fb7979b69943e3ced54275c0badbeb2938a8ac5e5e5a`.

## Aliases, accounting identity and proposed row

The source identity is problem2307073 / Hayman–Lingham7.73 / W.H.J.Fuchs, not D.Fuchs's AMR-049 polygon/dodecahedron problems. `ALIASES.json` exposes12direct identifiers/author/title aliases plus broad Fuchs/hyperbolic/intersection searches. `ALIAS_SCAN.json` scans the complete root-provided09:24:02UTC snapshot at requested numeric43-column range A1:AQ1178:191returned rows including header,190data rows, maximum4nonempty returned columns. No direct target alias occurs. This is a point-in-time observation, not concurrency clearance or a fresh independent live read by this reviewer.

All15broad-word leads are preserved with their full returned row values and explicit reasoned distinctness. Rows61/92/103 and related record23267641 concern regular-polygon billiard types/lengths or dodecahedral endpoints. Cached raw records23267641/23308905/23384007/23389367 were read in full, including complete descriptions, titles, identities and references; every string key/value, links and unknown fields were scanned for direct target aliases and the complete bytes are pinned in `ROOT_ANCHORS.json`. They do not claim the planar hyperbolic-domain intersection result. The other generic-word hits concern group schemes, observability, Artinian algebra, noncommutative independence, elliptic billiards, foliated three-manifolds, knot filling, braids, mapping-class factorizations, convex hyperbolicity cones or Poisson geometry. These semantic distinctions are recommendations requiring fresh root adjudication before any action, not automatic exemptions.

The bounded visible local Markdown/JSON/text package search found the current PR/root records and shared copies of the Hayman–Lingham source in other problem audits. A common full-book text containing Problem7.73 is not itself a duplicate standalone publication of the result. The search is explicitly not a census of hidden files or archived source packages; no global absence or historical-firstness claim follows.

`LITERAL_FOUR_CELL_PROPOSAL.json` is exactly one array of four literal strings. A uses the exact original problem identifiers and versioned PDF page, B is the empty string, C is the authenticated existing arXiv DOI, and D credits He–Tang and limits acceptance to the full original general-domain negative result. D discloses preprint/journal-review limits and the AI-assisted internal audit. No new DOI, release, external upload, or mutation is proposed or performed. This audit does not accept the simply connected bound, its endpoint, sharp lower extremals/equality or capacity machinery; those additional statements are unnecessary to resolve the original question.

Root must separately adopt the exact conclusion, literal wording and semantic leads. Any eventual accounting action requires a new live ledger/publication-source check after intervening writes and a fresh whole-action review under root policy. Prior PR1131 operational approval or another batch's adoption cannot be reused here.

## Closure

The written proof has no remaining central gap for the target. The recommendation is complete credited existing-preprint coverage of the original question; no novelty, first-priority, continuing-openness, journal-refereeing or external-human-validation certificate is given. All actual tests and failed attempts are distinguished. Scientific review completion100%; overall research goal remains80%. Root adoption and publication readiness remain false.

`AUTHENTICATED_INPUTS.json` fixes the final tested source/control/identity inputs, `ROOT_ANCHORS.json` fixes external root observations, `MANIFEST.json` closes every local public/private payload by exact size/SHA256, and `SEAL_CHECK.json` separately records final source-anchored complete readback. Its only self-reference exclusions are the manifest and final receipt. Private source bodies/evidence remain local. The package stays below the assigned25MiB allocated-storage cap. Previously closed PR1267, PR1259, the25-row proposal and PR1131 operations were not edited.
