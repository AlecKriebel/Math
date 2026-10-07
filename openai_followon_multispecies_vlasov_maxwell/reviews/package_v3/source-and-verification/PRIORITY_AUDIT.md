# Independent candidate-specific priority and attribution audit

Audit access date: 2026-10-07 UTC / 2026-10-06 America/Los_Angeles. Candidate: immutable `reviews/package_v1`. This is a bounded primary-source attribution and duplication review, **not mathematical verification or an exhaustive firstness certificate**. No external individual was contacted. No Git, publication, or candidate-packet mutation was performed.

## Disposition

The candidate's conservative attribution and intended metadata are defensible **contingent on independent verification of the mathematical dependencies and coupled estimates**. The inspected primary statements do not supply an exact duplicate of its arbitrary-data, finite-species theorem. This negative finding is limited to the material and versions listed below; it does not establish firstness.

The prospective increment is the full analytic transfer and simultaneous closure of the pinned one-species signed-impulse machinery for distinct charge-to-mass ratios, particularly opposite signs. The underlying global one-species claim belongs to OpenAI. Multispecies equations, mass normalization, signed Maxwell source sums, positive energy, the pointwise kinematic cancellation identity, and ordinary conditional continuation are inherited or direct algebra. Species with a common nonzero charge-to-mass ratio already reduce to one species, as shown below.

The theorem-bearing title and manifest cannot serve as evidence that the PDE proof has passed. The immutable packet explicitly calls itself an internal proof candidate, makes no firstness or complete Lean-formalization claim, acknowledges extensive AI use and lack of conventional human peer review, and withholds staging pending mathematical, priority, and package approval. Those qualifications matter. This review does not discharge the mathematical or package gates.

## Claim and exact packet inspected

The original target and main theorem require a fixed arbitrary finite number of species, positive masses, arbitrary real charges (including zero), nonnegative smooth compact phase data, compatible Maxwell fields in `C_b^∞ ∩ L²`, and the Gauss constraints. They claim unique global smooth classical solutions with compact phase support on every finite time interval. No data-size, symmetry, or neutrality condition is imposed. Constants need not be uniform as a mass tends to zero.

I read all of `main.tex`, all four proof supplements (`SUPPLEMENT_PAIR_IDENTITY.md`, `SUPPLEMENT_TRANSFER_LEMMA.md`, `SUPPLEMENT_UNIFORM_LEMMA_CHAIN.md`, `SUPPLEMENT_LOCAL_THEORY.md`), the intended `zenodo-deposit.json`, the packet README, the dependency ledger, primary-reference provenance, preliminary priority audit/search log, references, and review inventory. Other inventoried packet files were hash-checked, not proof-verified. All 24 inventory hashes matched; the machine-readable record is `sources/priority_final/candidate_reviewed_hashes.json`. In particular:

| File | SHA256 |
|---|---|
| `source-and-verification/main.tex` | `64e2f3f4d7972274b29a77d7980bc9255d38d86879eff5fc2143dcb5ba9b8696` |
| `zenodo-deposit.json` | `db57320f7afa483e9940b8ce1e3c419e50003719784007f261712bdcb6330fa3` |

The supplements distinguish their algebraic identities from conditional analytic transfer inputs. I assessed that distinction and provenance, not the truth of all analytic estimates, the polynomial certificates, the formal source, or a Lean build.

## What belongs to the input, and what could be new

1. **Physical model and mass normalization.** With physical momentum `p=m_a v`, the candidate sets `f_a(t,x,v)=m_a³ F_a(t,x,m_a v)`, giving common velocity `u(v)=v/sqrt(1+|v|²)`, force multiplier `λ_a=e_a/m_a`, and Maxwell sources `Σ_a e_a∫f_a` and `Σ_a e_a∫u f_a`. This is a convention change and known mechanics. Glassey–Schaeffer 1988 already uses the rescaling and its `m_a³` source Jacobian; Glassey's 1996 book explicitly treats different masses, signed charges, species transport, sources, and iterate differences.
2. **Positive energy and cone flux.** The mass-weighted positive kinetic energy with field energy, and cancellation of work through `m_a λ_a=e_a`, are ordinary deductions from this model. Finite sums and fixed species constants do not by themselves solve a momentum-support problem.
3. **Pair identity.** The candidate's primitive/residual cancellation is the pinned upstream `can:identity`, with renamed geometry and the constant `c_ab=e_a e_b/m_a` multiplying it. The upstream identity is kinematic for differentiable timelike curves; its derivation does not require equality of the source and receiver accelerations. Redoing this identity is useful validation, but is not a new cancellation discovery. A differentiated source acceleration carries `c_ab λ_b=e_a e_b²/(m_a m_b)`. The sign and multiplier must be retained through the estimates.
4. **Hard prospective transfer.** Unequal `λ_a` require a coupled transport system. A sum of unrelated one-species solution theorems does not prove it. The candidate must justify occupation estimates, direct terms, direction counts, selected coefficient and derivative estimates, and every dependency/budget with the fixed signed coefficients; then close one simultaneous species momentum bootstrap. That full chain, if valid and absent elsewhere, is the narrow incremental analysis.
5. **Local theory and the broad field class.** Ordinary momentum continuation is prior theory. The passage from `C_b^∞∩L²` fields to Sobolev local/continuation inputs requires a separate argument because bounded smooth derivatives are not automatically square integrable. The Coulomb-plus-curl cutoff, vacuum correction, and finite propagation mechanism already appears in upstream `continuation.tex` and is credited in the candidate. It should not be sold as an independent new field-class breakthrough.

### An equivalent common-ratio case

This is an independent algebraic deduction, not a literature-first claim. Suppose all charged species satisfy `e_a/m_a=λ≠0`. Define

\[
g=\lambda\sum_a e_a f_a=\lambda^2\sum_a m_a f_a\geq0,
\qquad \widehat E=\lambda E,\quad \widehat B=\lambda B.
\]

Every charged species obeys the same transport operator with force `Ehat+u×Bhat`; so does `g`. Multiplying Maxwell's equations by `λ` gives unit-charge source `∫g` and current `∫u g`. The Gauss constraints transform in the same way. Thus the charged system reduces to the normalized one-species model, and the individual species are recovered on the common characteristic flow. Uncharged species move freely and do not source the fields. Hence the arbitrary-parameter one-species case, identical-species aggregation, and the more general common-ratio case are algebraic consequences of the supplied one-species theorem, conditional on that theorem's validity. For distinct ratios this aggregation fails to produce one scalar transport equation. Opposite nonzero charge signs, with positive masses, necessarily have distinct ratios.

## Exact predecessor comparisons

These comparisons use displayed quantitative statements, not titles or abstracts alone, except where an abstract-only limitation is explicitly stated.

### Glassey–Schaeffer 1988: nearly neutral is a restricted theorem

Robert T. Glassey and Jack Schaeffer, *Global existence for the relativistic Vlasov–Maxwell system with nearly neutral initial data*, Communications in Mathematical Physics **119** (1988), 353–384, [DOI 10.1007/BF01218078](https://doi.org/10.1007/BF01218078). The primary Euclid copy was inspected at printed pp.354–356, including visual formula inspection. Its recorded hash was independently rechecked.

Their notation is `g_a(t,x,u)=F_a(t,x,m_a u)` rather than the candidate's number-density convention `m_a³g_a`. Printed p.354 exhibits common normalized velocity and the signed phase-space source `Σ_a e_a m_a³g_a`. For fixed positive support radius `k` and species norm bound `M`, the datum class on p.355 requires nonnegative `g_a0∈C_c²(R⁶)` supported in `|x|,|u|<k`, compact `C²` fields supported in `|x|<k`, the divergence constraints, and

\[
\sum_a\|g_{a0}\|_{C^2}<M,
\qquad
\left\|\sum_a e_a m_a^3g_{a0}\right\|_{C^1}
+\|E_0\|_{C^2}+\|B_0\|_{C^2}<\varepsilon.
\]

For some sufficiently small `ε=ε(k,M)>0`, they obtain a unique global continuously differentiable solution. Their constants can depend on the fixed species charges and masses (p.356). Large individual species populations are allowed, but the signed **phase-space** cancellation and field smallness are required. It is not merely a theorem for small scalar net charge. Compact electric support together with Gauss also enforces zero integrated charge. This theorem does not duplicate the candidate's arbitrary-data, possibly nonneutral finite-energy fields. The candidate's precise comparison is substantially accurate.

Fresh retrieval of the Euclid PDF on this audit returned a 1,056-byte HTML response despite HTTP 200. That failure is recorded separately. It was not treated as failure to inspect the theorem: the earlier successful primary reading copy was used read-only, with SHA256 `085f25cf473b97836e8a6203827211f35237521ce3e01054ab48aeef8377311e` verified against its acquisition manifest. Neither that PDF nor new private page rasters are publication material.

### Glassey 1996: multispecies continuation is inherited

Robert T. Glassey, *The Cauchy Problem in Kinetic Theory*, SIAM, 1996. I independently rendered and visually inspected printed pp.140 and159. [Publisher chapter](https://epubs.siam.org/doi/10.1137/1.9781611971477.ch5).

Theorem5.2.1 on p.140 has nonnegative `C_c¹` species data and `C²` fields satisfying the displayed constraints, including `∫ρ0 dx=0`. It additionally assumes a continuous common momentum-support bound, then gives unique global `C¹` solutions. Page159 replaces the single transport operator by species operators, uses signed source sums, and estimates iterate differences separately. This is conditional continuation, not an unrestricted a priori bound. Its neutrality condition must not be omitted when citing the printed theorem. The candidate expressly records this limitation. The book hash was verified as `baa46dbab0531f4aca93ebc77a0720618a2ac0c1f4fd3468624fe81f86b207eb`.

### Luk–Strain: unconditional satisfaction of a criterion is not supplied

[arXiv:1406.0165v1](https://arxiv.org/abs/1406.0165v1), submitted June1,2014; Communications in Mathematical Physics **331** (2014), 1005–1027, [DOI10.1007/s00220-014-2108-8](https://doi.org/10.1007/s00220-014-2108-8). I read complete Theorems1.1–1.3, Footnote1 and Remark1.2. Theorem1.1 uses nonnegative phase-compact `H⁵` particles and `H⁵` Maxwell fields with Gauss constraints, and bounded full momentum as continuation hypothesis. Theorem1.2 uses a bounded two-plane momentum projection; Theorem1.3 uses an integrability condition. Remark1.2 explicitly extends the criteria to multispecies, with details omitted. No neutrality requirement occurs in these displayed statements. None supplies the candidate's unrestricted a priori estimate or automatic `H⁵` field membership.

[arXiv:1406.0169v1](https://arxiv.org/abs/1406.0169v1), also submitted June1,2014; the combined published work is Archive for Rational Mechanics and Analysis **219** (2016), 445–552, [DOI10.1007/s00205-015-0899-1](https://doi.org/10.1007/s00205-015-0899-1). I inspected Theorems1.1–1.4 and adjoining hypotheses. The first compact-support statements concern approximations with a common bounded momentum support; later continuation uses a field integral along characteristics and weighted regularity/tail conditions. It is not an arbitrary-data existence theorem. The final combined publication's complete proof was not independently inspected.

### Other global and scattering results

| Primary version and inspected scope | Restriction relevant to duplication |
|---|---|
| Léo Bigorgne, [2208.08360v2](https://arxiv.org/abs/2208.08360v2), v1 Aug17,2022, v2 Aug31,2023; Analysis & PDE **18** (2025),629–714, [DOI10.2140/apde.2025.18.629](https://doi.org/10.2140/apde.2025.18.629). Introduction, full Theorem2.10, adjoining definitions. | Explicitly permits multispecies positive masses and differing charges. Weighted field size is bounded by `Λ`; weighted particle size is `ε`; the theorem requires `ε exp(DΛ)≤ε0`, with `N≥3`, `Nv≥15`, `Nx>7`. Large fields are possible, but the particle distribution is sufficiently small relative to them. The final publisher PDF retrieval was not successful; the exact preprint statement was checked. |
| Xuecheng Wang, [2203.01199v2](https://arxiv.org/abs/2203.01199v2), first March2,2022, revised July16,2026; PartI Theorem1.1 and adjoining remarks. Companion [2607.14685v1](https://arxiv.org/abs/2607.14685v1), July16,2026, title/abstract/structure. | No smallness, but cylindrical symmetry of `f(Rx,Rp)` and corresponding field covariance, `H^s` with `s≥6`, and a particle weight of order `N0=10^10` in PartI. Not the general nonsymmetric finite-species theorem. The companion's full proof was not reviewed. |
| Grace Mattingly, Stephen Pankavich, Jonathan Ben-Artzi, [*Sharp Time Decay and Scattering of Small Data Solutions to the Relativistic Vlasov–Maxwell System*,2609.29013v1](https://arxiv.org/abs/2609.29013v1), public submission Sept24,2026 04:25:34 UTC. Physical model pp1–2, exact Theorems1.1,1.5,1.6, relevant bibliography. | Multispecies `m_a>0,e_a∈R`. Recalled Theorem1.1, credited to earlier Glassey–Strauss, requires `f_a0≥0` in `C¹` supported in `ΓL×ΓL`, `C²` fields supported in `ΓL`, Gauss and global neutrality, and `Σ||f_a0||C¹+||E0||C²+||B0||C²≤ε0(L)`. It gives unique global classical solutions with a uniform momentum bound. New results construct/analyze sharper small-data asymptotic profiles, not arbitrary Cauchy data. PDF printed Sept25 differs from public submission date. |
| Stephen Pankavich and Jonathan Ben-Artzi, [2306.11725v2](https://arxiv.org/abs/2306.11725v2), first June20,2023, revised March10,2024; exact Theorem1.1 and adjoining model/compatibility. | Multispecies positive masses/charges, nonnegative compact `C²` particles, compact `C³` fields, Gauss and zero total charge; `Σ||f_a0||C²+||E0||C³+||B0||C³≤ε0`. Subsequent scattering results use this small-data solution. |
| Emile Breton, [2503.01677v2](https://arxiv.org/abs/2503.01677v2), first March3,2025, revised June19,2025; Hypothesis1.1, Theorem1.5 and Remark1.4. | Hypothesis1.1 starts with a global `C¹` multispecies solution and sufficient decay. The theorem proves modified scattering. The remark supplies restricted known existence subclasses. It does not establish unrestricted global existence. |
| Gerhard Rein, *Generic global solutions of the relativistic Vlasov–Maxwell system of plasma physics*, CMP **135** (1990),41–78, [DOI10.1007/BF02097656](https://doi.org/10.1007/BF02097656). Primary publisher abstract only. | A stability/perturbation result around specified decaying reference solutions. The full quantitative theorem was not inspected in this audit; the abstract alone is not used as an exhaustive scope certificate. |

The recent Mattingly–Pankavich–Ben-Artzi paper was not listed in the early packet audit. It belongs in an updated literature record, and can be acknowledged in a short prior-small-data paragraph without implying a new existence result is theirs. Its bibliography led to the Pankavich–Ben-Artzi and Breton comparisons above, Bigorgne's scattering-map paper2312.12214, and the original Glassey–Strauss1987 small-data paper. The two latter items were identified in the citation chain, not fully inspected here. Thus this was an explicit citation-chain check, not just a keyword scan.

### Bouchut–Golse–Pallard local/continuation input

[arXiv:math/0301175v1](https://arxiv.org/abs/math/0301175v1), *On classical solutions to the 3D Vlasov–Maxwell system: Glassey–Strauss' theorem revisited*. I inspected Theorem1.1, exact Lemma3.1 wave-derivative division coefficients/zero residue, and relevant Sections4–5 equations. Its displayed Theorem1.1 uses compact `C²` fields and conditional bounded momentum support. It cannot simply certify the candidate's noncompact field class. The candidate supplement explicitly borrows the local division calculation and supplies a localization argument. This review checks provenance; mathematical compatibility and reconstruction remain with the mathematical audit. The PDF's printed date is not taken as the initial public-version date.

## Current source, corrections, companions, disclosure dates

The primary repository endpoints were queried afresh at 2026-10-07 04:34–04:37 UTC. [Repository](https://github.com/openai/math), [pinned family README](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Global-classical-solutions-of-the-three-dimensional-relativistic-Vlasov-Maxwell-system-September-23-2026/README.md).

The observed repository and family-path histories each return one commit, `adc7f1241b42e322a6451854ab7e4b4c146bf78a`, with author/committer timestamp 2026-10-06 21:58:50 UTC. The branch endpoint returns only `main` at that pin; the releases endpoint is empty. Current family README and catalogue hashes match the pinned copies. The exact family introduction calls its unrestricted theorem one-species with `m=e=c=1`, compact nonnegative smooth particles and `C_b^∞∩L²` compatible fields; it is not a stated arbitrary multispecies theorem. The repository README warns of mixed verification status.

The initial recursive root-tree endpoint was truncated, so no completeness inference was made from it. I then queried the full `preprints` subtree (`272ca94583c1dca3188bbc3a1caa068cb7af4b55`, `truncated=false`). Title/path keywords and the current catalogue show only the family362 manuscript in the Vlasov–Maxwell area. This checks filenames/catalogue scope; it is not a semantic proof that no equivalent theorem is hidden in any differently titled manuscript. The prior audit also records a pinned full-TeX search; I did not substitute that record for a fresh proof reading of every preprint.

Within these inspected official endpoints, I found no subsequent main correction or distinct multispecies companion. Searches for correction/companion/equivalent terminology did not reveal an additional primary theorem matching the candidate. I did not comprehensively inspect all forks, issues, unpublished versions, theses, non-English literature, or every citation descendant. Absence in search results is not novelty evidence.

The GitHub metadata says repository creation on Oct6,2026 21:47:02 UTC and last push Oct6 22:01:11 UTC. These and the observed commit date support the candidate's description of an October2026 public repository release. They do not establish the exact first public visibility event; commit author dates alone are not public disclosure timestamps. In particular, the manuscript's September23 heading is **not** evidence of public priority on that date. At audit time the source is publicly accessible. The candidate does not claim a September public disclosure.

## Metadata and attribution recommendations

The intended manifest correctly identifies Alec Kriebel and ORCID0009-0001-9320-500X, uses an `isDerivedFrom` relation to the exact upstream pin, credits the one-species analytic machinery, and distinguishes established normalization/continuation. Its AI and peer-review statements are candid. The repository-root pin is reproducible; a manuscript-specific pinned URL can additionally improve reader navigation, but is not required to cure a misleading attribution.

For a future mathematically verified version, keep the increment narrowly worded: extension of supplied signed-impulse estimates and a joint bootstrap to finite species with distinct ratios. Explicitly treat the common-ratio reduction and the pair identity as inherited. Add the recent primary small-data/scattering reference to the literature record if revising it. Do not claim that all multispecies global classical theory was previously unknown, that mass normalization is new, that the one-species breakthrough is independent, or that keyword searches establish firstness. The packet presently makes none of those broad firstness claims.

The immutable packet was not edited to implement these recommendations. Any later amended version requires new hashes and candidate-specific review; this report refers only to package_v1.

## Evidence records and limits

`sources/priority_final/retrieval_log.json`, `retrieval_log_extra.json`, `preprints_tree_retrieval.json`, `primary_pdf_response_hashes.json`, `cached_primary_hash_check.json`, `candidate_reviewed_hashes.json`, and `upstream_reviewed_hashes.json` preserve access URLs, UTC times, versions, byte lengths and hashes. `SEARCH_LOG.json` records queries, actual inspected scope and failures. The fresh arXiv PDF responses were hashed in memory; full copies were not newly saved. The two previously acquired historical primary PDFs were read only and hash-checked. Private copyrighted PDF/page-image caches must remain excluded from publication; hashes and our own factual notes can be retained.

The source pin, theorem statements, and candidate provenance are checkable. Mathematical validity is not established by this audit. No exhaustive novelty clearance, reproduced formal build, independent refereeing, or authorization to publish is supplied. A central failed analytic dependency would block the proposed global theorem regardless of the favorable bounded attribution finding.

## Handoff boundary

The root reports incorporating these findings into the current working manuscript and bibliography, including the common-ratio reduction and recent small-data reference. Those later edits were not reviewed here and are outside the immutable package_v1 hashes. This report can accompany a new freeze as evidence of the priority findings, but the new candidate needs its own mathematical and package review. No new mathematics or publication authorization is inferred from that handoff.
