# Fresh adversarial preprint review, round 1

Reviewer: independent AI subagent `preprint_adversary_r1`. Completed 2026-09-23, approximately 15:00 UTC. The review began with the manuscript and compiled PDF; no prior audit report was read. The original source papers, rather than previous audit conclusions, were used to check attribution and hypotheses. No external individual was contacted. No manuscript, package, website, prior audit, or git history was changed.

## Version binding and verdict

| Reviewed artifact | SHA256 |
| --- | --- |
| `manuscript/note.tex` | `5950e74b23cb2be12626cb0c8d266cf3e3d6040c0dcfe8908a1fb49741796c94` |
| `output/pdf/note.pdf` | `cbc84a37bc7735675d833236c68c8194c99389b1398b21175f43998b9926e171` |
| `output/note-source.zip` | `eb002c284e3bf15a10dbdee81a77aee22ba0d3d9ddd31274ab24e6673c792aae` |

**Preprint verdict:** mathematically sound as a concise, attributed, unrefereed note. No blocking mathematical issue, unsupported central claim, or material package inconsistency was found. One worthwhile clarification would improve the exact correspondence to Abbar's original theorem. This is not an assessment of journal suitability and is not formal proof verification.

Completion estimate: this review is 100% complete; best guess for the reviewed note's readiness as an attributed preprint is 99%, with the remaining action limited to the clarification below and rebuilding the distributed artifacts if it is adopted.

## Actionable finding

### R1-1 — Worthwhile clarification: explain the single-offset to finite-block conversion

**Location:** `manuscript/note.tex:82`, PDF p. 2, paragraph following Lemma 2.

The attribution is mathematically correct, but the sentence explaining equivalence mentions only finite sums versus finite maxima. Abbar's actual Theorem A is stated using the two single coordinates `omega(n_k+q)` and `omega(-n_k+q)` for each natural-number offset `q`; it is not stated with a maximum over a finite set of offsets. Obtaining the present finite-block form also uses boundedness of the backward shift. That estimate is already proved later in the manuscript, but naming its role here would make the source comparison immediately checkable.

**Exact minimal fix:** replace the semicolon clause “finite sums and finite maxima give equivalent conditions” with:

> “the passage from its single-offset condition to finite blocks uses `c_{t-d}^{1/p} <= ||S||^d c_t^{1/p}` for integers `d >= 0`, after which finite sums and finite maxima give equivalent conditions.”

In LaTeX, use the manuscript's existing `\norm{S}` notation. No theorem or proof change is required.

**Independent verification of the conversion:** for a finite set `F`, choose an integer `q >= max(F union {1})` and put `C_F = (sum_{j in F} ||S||^{p(q-j)})^{1/p}`. Both finite-sum expressions in (3) are bounded by `C_F` times their respective single-offset expression at `q`, with exactly the same `n` and `lambda`. Conversely, use singleton sets. This also preserves the requirement of arbitrarily large `n`.

**Other issue grades:** blocking: none. Cosmetic: none worth requesting for this preprint. The existing five-page layout is readable, and all pages were visually inspected.

## Independent mathematical checks

### Scalar necessity, including pathological scalar sets

The large-time assertion is valid even when `Gamma` is uncountable, nonmeasurable, nonclosed, very sparse, or has no multiplicative closure. For every fixed `N`, the finite union of complex lines `union_{n=0}^N C S^n x` is closed with empty interior. Removing it from any nonempty open set leaves a nonempty open set, so density supplies an orbit point at a time exceeding `N`. Approximating the nonzero finite-block vector by such points also ensures nonzero scalars.

An orbit vector with support bounded above could not approximate a coordinate vector above that bound; thus the fixed nonzero coordinate `x_k` used in the proof exists. The right-tail estimate tends to zero by summability of `x`, without any lower or upper bound on the allowed scalars. The left-tail estimate uses only boundedness of `S`, in the correct direction: `c_{t-d}^{1/p} <= ||S||^d c_t^{1/p}`. The choice `k >= max F` makes every exponent nonnegative. Both estimates use the same allowed scalar; there is no illicit normalization of `Gamma` or replacement of it by its closure or radial hull.

### Baire sufficiency and amplification

Finite-support sequences are dense because `p < infinity`. The right translations in the proof are used only on finite-support sequences, so boundedness of the inverse shift is not being assumed secretly in Lemma 2 or Proposition 3. Direct computation gives the stated two error estimates for `z = a + lambda^{-1} R_n b`.

`Y_E` is a separable Banach space under the stated assumptions. Each `G_q` is open even for uncountable `Gamma`, because arbitrary unions of open sets are open. The interpolation construction proves density for every pair of nonempty open sets, so the countable intersection argument applies. The surjection induced by a nonzero continuous linear functional is bounded, onto, and intertwining; consequently the reverse amplification implication holds. The cases `Gamma = emptyset` and `Gamma subseteq {0}` are correctly disposed of, and nonzero `E` is explicitly assumed.

### Measurable conjugacy

The two measure bounds give mutual nonsingularity, positive finite layer masses, and bounded translation in both directions. For every `j`, the measure `nu_j(C)=mu(f^j C)` is countably additive because the map is injective and bimeasurable. Its density bounds follow directly from bounded distortion. The integration formula in (4) has the correct change-of-variables direction.

Mutual nonsingularity makes `J` well defined on equivalence classes. For surjectivity, countably many measurable representatives glue to a measurable function on the wandering partition; no Bochner-measurability assumption is being smuggled in. The weighted norm bounds establish its integrability and the bounded inverse. The identity `JT_f=S_EJ` and the weighted-shift conjugacy both have the correct index direction and normalization. A null remainder is harmless because the union of all integer translates of `W` is invariant.

### Nonseparable counterexample

The example has total measure `sum_j 2^{-|j|}=3`, so it is even a finite measure space. With `W={0} x Omega`, bounded distortion holds with `K=1`, and forward and inverse measure ratios lie between `1/2` and `2`. For distinct coordinates `alpha,beta` of the Bernoulli product, the coordinate-indicator functions on layer zero have `L^p` distance `2^{-1/p}`. They form an uncountable separated family, proving nonseparability for every stated `p`.

Every complex projective orbit is contained in the separable closed linear span of its countable ordinary orbit. Thus the composition operator cannot be `Gamma`-supercyclic for any `Gamma`, whereas the scalar shift is hypercyclic: take `lambda=1` and note that both finite sums of `2^{-|j +/- n|}` tend to zero. This verifies the claimed separability boundary.

### Direct deduction from Abbar–Kuznetsova

The original Theorem B requires a second-countable locally compact noncompact group, a positive locally `p`-integrable weight, admissibility for the selected translation parameters, a nonempty set of nonzero allowed scalars, and an abelian subgroup generated by the translation parameters. Both `Z` and `Z^2` meet the group assumptions. Local integrability is automatic on these discrete groups, and the required translations are powers of the bounded shift. Full-group admissibility and generation of the whole group are not required.

Their convention is `T_s h(t)=h(s^{-1}t)`, hence the use of `s=-n` is correct. Counting measure with tolerance below one forces the retained subset to be the entire finite set. The product of the two positive maxima excludes every fixed finite collection of times when the tolerance is sufficiently small, independently of the scalar. The first-coordinate projection argument on `Z^2` is valid for every finite subset, including subsets with repeated first coordinates.

The map `R` is bounded by absolute convergence, contains every chosen `e_k` in its range, and has dense range. Its coordinatewise extension is bounded with dense range; approximate finite-support vectors one coordinate at a time. A continuous intertwining map with dense range sends a dense orbit to a dense orbit in the target, so surjectivity is unnecessary. This independently confirms the claimed prior-theorem deduction without relying on the proof of Lemma 2.

### Boundary tests attempted

Besides the degenerate scalar sets above, I checked the proof against singleton nonzero `Gamma`, scalar sets tending only to zero, unbounded sparse sets, and scalar sets with arbitrarily restricted phases. None of these introduces an unstated operation on `Gamma`. Constant weights fail the two-tail product condition as expected. Geometric weights `c_j=a^j` also fail it, while `c_j=2^{-|j|}` passes with `Gamma={1}`. The endpoint `p=1`, finite-dimensional nonzero coefficient spaces, and bounded shifts whose inverse need not be bounded cause no failure. The exclusion of `p=infinity` and nonseparable coefficient spaces is used precisely where it should be.

## Primary-source checks and attribution

- **Abbar (2019), Theorem A, printed p. 74; Theorem 2, printed p. 75.** I inspected the actual [publisher PDF](https://bulmathmc.enu.kz/index.php/main/article/download/55/93/364) and [publisher record](https://bulmathmc.enu.kz/index.php/main/article/view/55). Theorem A assumes the one-sided weight-ratio bound and arbitrary `Gamma` with a nonzero element. Its scalar criterion matches after the conversion identified in R1-1. Theorem 2 supplies the three usual approximate-inverse limits. A diagonal selection over finite blocks verifies those limits on the separable coefficient space used here. The record supports the stated 2019 date, volume, issue, and pages.
- **Abbar–Kuznetsova, arXiv:2005.11230v2, Theorem B, p. 3 and pp. 21–22.** I read the local primary PDF/text and checked the [arXiv record](https://arxiv.org/abs/2005.11230v2). The hypotheses and translation convention are as detailed above. The record confirms the 2020 preprint and 2021 journal reference. Local PDF SHA256: `4130805d90f54a9fc1bcc59efe6da0e77763a38a19abd3ba13f45f0957f8357a`.
- **Oberwolfach Report 19/2024.** The primary report states the separable Banach-space convention at the beginning of both relevant contributions, on pp. 1078 and 1081. The measure assumptions and bounded distortion are on pp. 1079–1080; the associated shift is on pp. 1080 and 1082; the arbitrary-`Gamma` question is on p. 1083, in D'Aniello's contribution explicitly identified as joint work with Maiuriello. The manuscript accurately retains this scope. The [EMS publisher record](https://ems.press/journals/owr/articles/14298367) confirms the report metadata. Local PDF SHA256: `620866807131964a6c0e4ceb53f6b1dfc08fe49911b836cf14cc913b82b37b6f`.
- **D'Aniello–Maiuriello, arXiv:2404.04028v2.** The primary preprint has the separability convention on p. 3 and the cited real/complex equivalences in Theorem 4.5 and Corollary 4.6. The [publisher record](https://link.springer.com/article/10.1007/s43037-025-00463-0) confirms the 2025 journal publication and article number 73. Local PDF SHA256: `70f4454d1d713937c8aefc3b4ff1af2fdebab1de645b6948cfe375828dff0dfd`.

The note consistently presents its contribution as an explicit application of earlier criteria. The mathematics supports that positioning. It does not need to establish that no one previously noticed the application, and it does not claim a new scalar criterion or new amplification mechanism. I found no inaccurate attribution requiring correction beyond the explanatory clarification above.

## Package and PDF checks

All five PDF pages were rendered and inspected. There are no clipped equations, missing symbols, unreadable references, or substantive layout obstacles. The compiled content matches the manuscript's theorem, assumptions, proof, counterexample, attribution, and preparation statement.

The source archive contains exactly the self-contained `note.tex`, source README, citation entry, and license. All four members are byte-identical to their current source files. The upload kit's `paper.pdf`, nested source archive, metadata, and metadata API wrapper are byte-identical to the intended files. Its two recorded checksums match. The root `.zenodo.json`, plain metadata, and API-wrapped metadata agree structurally. The author, ORCID, title, date, version, scope, attribution, license, and unrefereed/AI-assisted status are consistent across the inspected principal materials. The source archive contains no third-party full texts or hidden analytical dependency. The site text inspected also retains the separability hypothesis and restricted contribution claim.

No numerical computation is a premise of the proof. This review did not rerun the optional finite verifier or recompile the source archive: neither is needed to repair a discovered mathematical defect, and the existing PDF and archive identity checks were sufficient for the material-consistency question assigned here.

**Strongest verified result:** under the manuscript's explicit assumptions, the arbitrary-`Gamma` equivalence follows by the displayed self-contained proof and independently by the cited translation theorem plus the model. **Exact remaining gap:** no mathematical gap identified; only R1-1's explanation of how the source's formulation matches the displayed finite-block formulation.
