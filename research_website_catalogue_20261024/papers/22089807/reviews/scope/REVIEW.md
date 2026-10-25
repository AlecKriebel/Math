# Complete source and publication-scope review — Zenodo 22089807

Scope status: **COMPLETE, 100%**. The held article candidate is ready for the separate mathematical gate. This is a source-binding, substantive reading, interpretation, and primary-interface review. It does **not** authorize promotion, certify the analytic proof, certify novelty or priority, or represent human peer review. The independently assigned analytic and adversarial families must decide the scientific gate without relying on this conclusion.

## Exact work, version, and dates

The reviewed work is **A fitness-independent family of simultaneous amplifiers beyond relative fitness 3/2**, Alec Kriebel, ORCID [0009-0001-9320-500X](https://orcid.org/0009-0001-9320-500X). The selected record is [Zenodo 22089807](https://zenodo.org/records/22089807), version **2.0.4**, DOI [10.5281/zenodo.22089807](https://doi.org/10.5281/zenodo.22089807), concept DOI 10.5281/zenodo.22089806. Its publication date is **25 August 2026**. The fresh API records creation at 2026-08-25T04:10:23.911114+00:00 and metadata update at 2026-10-10T21:39:42.879238+00:00. The versions endpoint reports one published record in this concept.

A named earlier release of the **same beyond-three-halves work** is [Zenodo 21852072](https://doi.org/10.5281/zenodo.21852072), published **8 August 2026**, version `simultaneous-amplification-beyond-three-halves-v1.0.0`. Its primary paper's abstract, model, construction, and Theorem 2 were read for work identity and release history. This earlier release is not another completed work. It shares an older repository-release concept with several different named papers; that shared repository version chain does not make those papers one scientific work. The frozen reconciliation entry, rather than incidental repository co-location, governs deduplication.

The separate below-three-halves paper [21850042](https://doi.org/10.5281/zenodo.21850042) is credited as prior work, not counted here as another completion. `content.json` retains both original release date and reviewed-edition date explicitly. Its ordinary publication-date field uses the selected reviewed edition and labels that choice; it does not silently backdate version 2.0.4.

## Fresh acquisition and exhaustive asset accounting

The fresh unauthenticated public API and both complete deposited assets were acquired on **25 October 2026 UTC**. The complete API response is retained in `sources/record-raw.json`; its SHA-256 is `7bf65171d1b2237a7c516b213686de8e09de531fc4a7c12b450359daa466de39`. The receipt independently binds the API URL, retrieval times, public file URLs, byte sizes, API MD5 checksums, and SHA-256 hashes. Both assets match the frozen row-81 queue entry exactly, including its MD5 and byte counts; no locally modified development copy was substituted.

| Deposited asset | Bytes | SHA-256 |
| --- | ---: | --- |
| Standalone 21-page PDF | 214040 | `1d6d1d31a782776b07b9240467f02d624b47dcde5c83f4740a192136c2dfb8e3` |
| Complete source-and-certificate tar.gz | 6952578 | `e5b61e79d065a9abec0908e28db7e79366b5fccedeb6efbf22eadd7af3cc57ae` |

The tar has exactly **23 regular files**, unique safe paths, no links or special files, and no hidden members. All 22 payload hashes and the exact payload set match its `MANIFEST.sha256`. Two payloads are wheels, hence nested ZIPs: mpmath has **92** members and SymPy **1570**, for **1662** nested members in total. Every wheel CRC and every hashed RECORD entry was checked (91 and 1569 respectively). There are no deeper recognized containers, hidden nested members, or additional PDF readers. The full names, sizes, hashes, kinds, and reading dispositions are retained in `archive_inventory.json`, `nested_member_inventory.json`, and `support_read_ledger.json`. “All members inventoried” does not mean that every third-party library source file was independently audited.

There are **two current published PDF readers**, including the one inside the tar. The embedded 21-page reader is 214136 bytes, SHA-256 `1e73984abfd64a45797b8ad6dc8b473d82a8d5eb8061efe470a1e603c2d10ad9`. It is not byte-identical to the standalone deposit. The standalone's entire 21-page extracted text was read; the complete embedded extraction was compared, with every difference inspected. The only differences found are the title-page date (“August 2026” versus “August 22, 2026”), Figure 1 label placement/extracted order, and whitespace. No mathematical claim, formula, or proof-text difference was found. `reader_diff.patch` and `extraction_receipt.json` preserve the comparison. The standalone title/abstract first page was also visually inspected. The unchanged standalone deposit is the appropriate public primary reader; the archive preserves the alternative in place.

The archive and paper retain historical statements saying that no new persistent identifier has yet been assigned, and `main.tex` points to a v2.0.3 repository tag. These are stale historical packaging statements, not grounds to deny the fresh public v2.0.4 DOI or silently rewrite the archive. The vendor README also points to an omitted `submission/ENVIRONMENT.md`; the top README separately states the Python and external PDF-tool requirements. These are recorded source caveats. No substantive scientific scope defect follows from them alone.

## What is actually claimed

The main claim is the quantified hypothesis

`∃ {G_t}  ∀ fixed r ∈ (1,R_hyb)  ∃ t0(r)  ∀ t ≥ t0(r)`

that **both** uniformly initialized single-mutant fixation probabilities strictly exceed their own same-order complete-graph baseline. The graphs are finite, connected, loopless, undirected, and weighted; mutant fitness is r and resident fitness one. Bd chooses a fitness-weighted parent before its edge-weighted target; dB chooses a uniform death site before its fitness-and-edge-weighted competing parent. The baselines are `(1−r⁻¹)/(1−r⁻ⁿ)` for Bd and `((n−1)/n)(1−r⁻¹)/(1−r⁻(n−1))` for dB. Replacing the finite-n dB baseline by the Bd formula would change the comparison.

The family uses a clique of size `C=t⁴`, `q=t` internally heavy two-vertex satellites, and `m=floor(λ_*t)` hub leaves. Each satellite vertex connects weakly to **every** clique vertex. Its internal edge has weight `C/σ_*`. A least admissible positive dyadic weak weight is selected for each t by a real-algebraic decision procedure on the expanding compact interval `[1+1/t,R_hyb−1/t]`; early empty intervals have a stated fallback. This construction is effective in the theoretical sense. It supplies no useful running-time or practical graph-size guarantee.

The root `R_hyb = 1.5028569127905696…` is isolated in `(3/2,151/100)` by the sextic `R⁶−8R⁵+22R⁴−30R³+21R²−6R+1`. The asymptotic response coefficients, at gain scale `q/C`, are

`B(r) = 2(σ−1)/(1+σ(r²−1)) + λ/(r−1)`,

`D(r) = 2{r(2−r)−σ}/(σ+2r(r−1)) − λ`.

The paper optimizes their common positivity interval. Proposition 15's exact optimality is **only within the displayed first-order dilute response model with fixed positive σ and λ**. It does not classify singular or size-dependent parameters, zero first-order boundaries, alternate density scales, other modules, nonseparated dynamics, or arbitrary weighted graph families. The rational specialization `σ=19/137`, `λ=20/27` gives exact positive margins at r=3/2 and a smaller algebraic threshold still greater than 3/2.

The strict interval excludes r=1 and r=R_hyb. At neutrality the uniform average is 1/n; at the upper endpoint the optimized leading coefficients vanish, so no actual endpoint sign follows. There is no uniform onset near either endpoint, no theorem for fitness varying with t, and no assertion that every finite graph amplifies every beneficial fitness. The separate older center–triangle family's endpoint suppression is not a statement about the present hybrid endpoint.

The gain tends to zero: `q/C=t⁻³=Θ(n⁻³/⁴)`. Pair weights grow and the selected weak cut may be tiny. The paper provides no useful finite-size onset, fixation-time bound, bounded weight ratio, or empirical population model. The result is a qualitative lower bound for unrestricted `R_sim`, not its exact value or a universal upper bound. The full falsification targets and boundary map are in `claim_boundary_map.json`.

## What the supporting programs mean

All three paper certifiers, the integration checker, failure-propagation test, manifest generator, requirements, and replay/build/release wrappers were statically read in full. This reviewer did not execute the mathematical replay, leaving that independent check to the separately assigned families. Independent archive and wheel integrity checks were executed.

`verify_hybrid_lumping.py` constructs a single nine-vertex graph (`C=3,q=2,m=2`) at exact rational parameters and compares every parent/target event under both rules for **512** labelled configurations and **108** orbit fibres. It is a useful finite transition-aggregation audit, not an enumeration of the asymptotic sequence. The two symbolic certifiers verify response identities, rational margins, exact root counts and signs, the feasibility quadratic, and tangency; decimal values receive additional numerical checks. Those calculations are conditional on the response formulas.

`verify_paper_claims.py` reconstructs finite algebra and checks that specified strings occur in `main.tex`, with retired artifact names absent. The string checks do not validate the stopped-process arguments they name. The fail-closed tests reject optimized Python and use disposable mutations to check failure propagation; they do not provide an independent probability proof. The analytic Schur-limit, establishment, cleanup, reciprocal-invasion, and sweep arguments are in the manuscript. There is no separate complete asymptotic machine certificate hidden in the bundle.

The canonical bootstrap requires Python **3.14.6**, installs the supplied hash-pinned SymPy **1.14.0** and mpmath **1.3.0** wheels without an index, and invokes replay plus mutation tests. Python itself is not supplied. Document rebuilding separately requires external Tectonic and Poppler; Tectonic resources may require cache or network. The internal manifest establishes file consistency relative to the externally bound archive hash, not independent authorship or authentication of an unsigned tag.

The historical `RESEARCH_LOG.md` was deliberately inventoried and hashed without consulting its body. The release notes were read for package/version scope only. No favorable historical or current analytic/adversarial opinion was used as proof.

## Focused primary-source interfaces and prior credit

Acquisition URLs, UTC times, file hashes, exact read extents, and gaps are in `primary_acquisition_ledger.json`, `primary_read_ledger.json`, and `prior_archive_interface_ledger.json`. Raw third-party reading copies are locally cached in an ignored directory.

1. **[Svoboda, Joshi, Tkadlec and Chatterjee (2024)](https://doi.org/10.1371/journal.pcbi.1012008).** The primary published model, positive theorem, explanation, discussion, and the technical appendix's construction/theorem interface were read. It explicitly uses uniform singleton initialization, the same two update rules, and the same finite complete-graph benchmarks. It already establishes simultaneous amplification below fitness 1.2 using weakly linked weighted modules. The broad simultaneous-amplifier existence question was therefore answered before this paper. The claimed contribution here is a new interval and construction, not invention of that question, of modular weak links, or of update-order robustness.
2. **[Tkadlec, Pavlogiannis, Chatterjee and Nowak (2020)](https://doi.org/10.1371/journal.pcbi.1007494).** The primary SI model, theorem statements, and fixed-graph transience/boundedness proof interface were read. The noncomplete-support transience threshold is graph dependent (the SI gives a bound depending on N). It does not impose one finite fitness threshold on all growing families, and does not itself close complete weighted support. This is why the manuscript's quantifier distinction and separate complete-support credit matter.
3. **[Kriebel, fixed-graph obstruction, 21753405](https://doi.org/10.5281/zenodo.21753405).** The original public API, named manuscript abstract, model, theorem/corollary statements and quantifier discussion were read. It credits the preceding noncomplete result and claims an additional complete-directed-support sum-of-squares/equality classification. This separate unrefereed work is background, not a substitute for the current proof.
4. **[Kriebel, below-three-halves construction, 21850042](https://doi.org/10.5281/zenodo.21850042).** The original named paper's abstract, summary, introduction, model, and threshold definition were read. Its precise interval is below 3/2, with suppression at that family's endpoint and no universal upper bound. The current paper supersedes its lower-bound benchmark, while the separate work retains its identity.
5. **[Kriebel, earlier beyond-three-halves release, 21852072](https://doi.org/10.5281/zenodo.21852072).** The original named manuscript's abstract through main theorem were read. It states the same sextic threshold and pair–pendant mechanism, supporting the same-work version relationship and original release date. Its older proof and audit claims were not used to validate the expanded current proof.
6. **[Brewster, Huang, Mitzenmacher and Nowak (ITCS 2026)](https://doi.org/10.4230/LIPIcs.ITCS.2026.29).** The complete two-page primary extended abstract was read. It studies a per-step random mixture of Bd and dB. Its full arXiv paper was not read, and supplies no load-bearing current theorem input. Success under both pure kernels does not by itself prove success under every mixed kernel.

For the three large prior repository releases, the fresh public ZIP central directories and selected named manuscript members were fetched using validated HTTP 206 byte ranges. Member sizes and CRCs were checked and full selected-member SHA-256 hashes retained. The entire 450–480 MB ZIPs were not downloaded, so their complete MD5 values are explicitly **not** claimed as reverified. This bounded interface reading is sufficient for the stated credit/version comparisons; it is not completion of the separate prior-paper reviews.

A bounded current search was also made for subsequent simultaneous-amplifier and mixed-process work. It does not certify exhaustive novelty, priority, or worldwide openness. No source discovered in this focused check justified adding a new follow-up. No individual was contacted and no outreach was prepared.

## Held copy and follow-up decision

`content.json` contains the **complete published abstract** from standalone page 1, cross-checked with released TeX; only mathematical typography and whitespace are normalized. It also contains accessible model/mechanism text, exact result and restrictions, scholarly credit, edition/original-release dates, unchanged reader/archive bindings, a concise substantive collaboration invitation, and explicit unrefereed/AI-assisted status. It remains a **held candidate**, subject to independent mathematical decisions.

**Follow-up: null.** Finding the unrestricted threshold, designing other modules, changing singular parameter regimes, obtaining practical finite-size bounds, and controlling fixation times are meaningful broad directions. This review provides no new precise mechanism or supported conjecture meeting the user's unusually high bar. Repeating those directions would add a generic question rather than a justified research proposal.

The strongest result established by this scope family is exact current source acquisition, complete reader/support accounting, substantial reading of the published mathematical argument, accurate boundaries and prior credit, and held copy faithful to those limits. The exact remaining scientific gap is the independent verification or falsification of the current gain-scale analytic argument. The overall 203-work programme remains active; this scope completion counts neither an older version nor another paper as an additional finished work.
