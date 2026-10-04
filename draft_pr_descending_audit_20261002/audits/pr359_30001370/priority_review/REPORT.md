# PR359 / 30001370: independent source and priority audit

**Final priority audit. Root review approved package closure.** Candidate head `6be98eac0ba508368218179ecf80020c037dbece`, base `efd29c05204703acca9a0860812f54b94fae54b1`. Scope: this submitted claimed_solved candidate only. No other PR was audited. Audit date: 3 October 2026.

## Finding

No exact full-L1 common-boundary theorem was identified in the primary sources and bounded current literature inspected here. The candidate addresses the original question, and its principal additional result is the all-density closure formula

    W0 = closure_D union_{n>=0} F^{-n}({1}).

Together with its positive exact sections/open-map result and the published boundary seed at 1, this yields the original boundary identity. This goes beyond the genuinely restricted published Proposition 4 on the analytic mixture core. No identified priority duplicate requires downgrading that stated progress on the evidence reviewed. This is a bounded literature conclusion, not certification of universal novelty, current open status, or mathematical correctness of the entire packet. Final mathematical disposition belongs to the separate proof audit.

Attribution in SOURCE_SCOPE.md, SOURCE_ADDITION_T3.md and the proof is substantially accurate: global three-limit convergence, basin openness, analytic-core boundary seeds, invariant Herglotz mixtures, and the dimension-independent inverse-expansion algebra are already source inputs. The inverse rank-one norm estimate is especially close to the source and must retain that credit. The candidate explicitly declines a historical-priority claim; that restraint should remain.

## Source-first gate and exact question

Before reading the candidate, I sealed SOURCE_FIRST_BASELINE.md at UTC `2026-10-03T22:21:01.556048+00:00`, SHA256 `6a0d74b1b7378ae43b52d4a8d91579428c1e14f6140b30a86841b7f752cf8474`. The official [OWR report](https://ems.press/content/serial-article-files/46250), printed pp.2713-2715, was read as text and pixels. It fixes I=[-1/2,1/2], f_r(x)=((r+4)x+r+1)/(2rx+2), T_r=f_r or f_r-1 on the two sides of -r/4, and

    F(u)=P_{G(phi(u))}u, phi(u)=integral_I x u(x) dx,
    G(m)=A tanh(Bm/A), 0<A<=2/5, 6<B<=16.

D is **all** nonnegative L1 densities of mass one, with relative L1 topology. Define W0 by convergence to 1 and W± by convergence to the noncentral fixed densities. The target is W0=boundary_D(W+)=boundary_D(W-). OWR Theorem 2 already gives the all-D trichotomy and stable-basin openness; p.2715 calls the common-boundary assertion a conjecture and states density of W+ union W-. The narrower imported catalog statement is consistent, but its August2026 literature triage is dated metadata rather than an independent current-status proof.

The candidate preserves the exact domain, topology and A,B rectangle. It does not replace the conjecture with a finite-particle result, a smooth-density result, a boundary only at 1, or an ambient-L1 boundary. Example1 in readable BKZ preprints permits B<=18; that larger range is not claimed by this candidate. A=0 and B=6 are excluded from the bistable target, while A=2/5 and B=16 are included.

## Original-progress mapping

| Candidate result | Earlier inspected result/mechanism | Audit of incremental claim |
|---|---|---|
| Three fixed densities, convergence of every D orbit, and openness of W± | BKZ Theorem2/Proposition3; OWR Theorem2 | Published foundation, correctly credited; no new discovery claim warranted. |
| 1 and W0 intersect the analytic core belong to both boundaries | BKZ Proposition4, Lemma13 and stochastic-order perturbations toward endpoint atoms | Published seeds, correctly credited. Core D0/D-prime is compact and uniformly analytic, not L1 dense in D. |
| K(u)=P_{h_{r(u)}}u is a homeomorphism and F=P0 K | The normalized source lifted finite-particle map uses h_r=(x+r/4)/(1+rx); source Sec3 proves finite-dimensional invertibility | The all-density scalar-root inverse and joint strong L1 continuity are additional explicit probability-density statements in the candidate. They are a natural extension of the source mechanism, not a new general mean-field inversion principle. |
| Positive right inverse of P0 through every prescribed density, including zero fibers | Conditional branch disintegration for a two-to-one transfer operator is elementary; no corresponding all-D open-map theorem was located in inspected BKZ passages | The q=w/(P0w) composed with T0 formula, with q=1 on zero fibers, makes relative openness checkable. Positivity, mass and norm preservation are explicit. Full L1 openness of F and complete invariance of boundaries are useful added results. |
| Boundary property for symmetric/eventually symmetric densities and closures of core preimages | Published density of union of stable basins plus reflection already implies the symmetric boundary corollary | Candidate correctly declines novelty for this corollary and does not count it as resolution. |
| Strong stable functional L(f)=sum lambda^{-k} phi(P0^k f), H=ker L on zero-mass L1 | BKZ Lemma14/Prop5 identifies Q=P0+B[x] tensor phi, the unstable line and lambda=1/2+B/12; later rank-one spectral/resolvent methods also exist | Candidate supplies the invariant kernel, exact iteration formula, individual L1 decay, BV exponential bound and absence of uniform L1 decay. This is a concrete model-specific clarification, not a new abstract resolvent method or a nonlinear L1 stable-manifold theorem. |
| Forty rational intervals certify the inverse contraction for the exact A,B range | BKZ Sec3 Lemma4 already has dimension-independent inverse expansion, the same rank-one decomposition and the same 9/(16 sqrt3) term, with a numerical final bound | Additional exact certificate and arbitrary-probability-space presentation, with source algebra correctly acknowledged. Dimension independence itself is prior. |
| W0 is the L1 closure of finite preimages of 1 | BKZ Sec5.1 gives external-parameter shadowing for global convergence; Prop4 gives analytic-core boundary seeds | No inspected source states this all-D closure. The terminal cumulative correction, feedback solved backward with original branch labels, accumulated distortion, unweighted core bound, and total-variation passage are the candidate's substantive completion of the missing lifting step. |
| Full boundary identity | OWR explicitly conjectures it; readable BKZ Prop4 proves only the core restriction | The claimed conclusion is the original problem. Its derivation depends on the new closure/open-map steps, not on merely repeating published seeds or linear hyperbolicity. |

The strong-stable discussion must retain its current version qualification. The inspected preprint's one-step argument using ker(phi) is not by itself an invariant-kernel argument: f=x^3-(3/20)x has zero mass and phi(f)=0, but phi(P0f)=1/320. That exact counterexample was independently recomputed here. It does not falsify the source's hyperbolicity conclusion, global theorem, or conjecture, and it does not establish an error in an uninspected final journal proof. Turn2 explicitly states those limits and is not a dependency of Turn3.

## Current primary corpus and contrary-scope checks

The machine-readable SOURCE_QUERY_LEDGER.json records the exact bounded queries, their timestamps, complete native returned payload identities, downloads and inspection limits. The following comparisons use primary PDFs or publisher/author records; secondary search results were not relied on for mathematical claims.

| Primary work | Inspected claim and why it is not an identified resolution |
|---|---|
| [Galatolo2022](https://doi.org/10.1007/s00220-022-04444-4), complete journal PDF from institutional archival mirror | General existence, small-coupling uniqueness/convergence and linear response. Theorem6 applies in a sufficiently small coupling interval with specified regular spaces. It does not identify both basin boundaries of the bistable Möbius/tanh example on all D. |
| [Tanzi2023 review](https://doi.org/10.1007/s40574-023-00350-2), complete corrected publisher PDF | Its BKZ discussion concerns the pitchfork and coexistence of equilibria. Its model classes and stability surveys did not supply the exact full-D boundary theorem. The review itself does not purport to be exhaustive. |
| [Tanzi correction](https://doi.org/10.1007/s40574-023-00384-6), complete publisher PDF | Online26August2023, printed2024: copyright/OpenChoice change, not a mathematical boundary correction or solution. |
| [Bahsoun-Liverani2025](https://doi.org/10.1016/j.aim.2025.110115), publisher metadata plus complete primary arXivv3 | Abstract bifurcation and stability/physical-measure criteria; explicit Anosov example. Theorem2.13 classifies fixed-point curves under hypotheses, not all basins. Proposition5.3 supplies related resolvent spectral machinery. It cannot be counted as a proof of the specific original boundary identity without additional verified hypotheses and a boundary argument. |
| [Castorrini-Galatolo-Tanzi2025 differential paper](https://doi.org/10.1007/s00332-025-10177-0), complete publisher PDF | Theorem5 assumes an iterate of the differential contracts all zero-average vectors in a strong topology and proves local strong attraction. The original central density has an unstable direction, so this attracting-fixed-point hypothesis does not prove its separating basin boundary. The paper discusses loss of regularity explicitly. |
| [Castorrini-Galatolo-Tanzi2026 cone paper](https://doi.org/10.1007/s10955-026-03586-2), complete current publisher PDF | Definition2.5 and Theorem2.8 restrict stability to invariant cones and Hilbert metrics; the text expressly distinguishes cone stability from global measure-space stability. Strong-coupling and noisy examples do not establish the original all-L1 common-boundary assertion. |
| [Bahsoun-Froyland-Phalempin2026 Newton paper](https://arxiv.org/abs/2605.08803), additional complete primary arXivv1 | Fourier-Fejer discretization, W1,1 fixed-point approximation and small-coupling sequential/Newton convergence. No exact full-D basin-boundary claim was identified in its main theorems or model assumptions. |

Direct author/citation routes included [Keller's publication page](https://www.math.fau.de/stochastik/gerhard-keller/publikationen/) and [Zweimueller's publication page](https://mat.univie.ac.at/~zweimueller/PapersAndPreprints.html), the source title/author names, exact common-boundary/basin aliases, and direct later-paper BKZ references. A complete current Bardet publication inventory was not located by the targeted query; no negative conclusion follows from that. This review did not enumerate every forward citation, every unpublished manuscript, every non-English source, or every later preprint. Search-engine dates were not used as publication dates.

A second bounded pass added central/neutral basin, common basin boundaries, finite-preimage closure, globally-coupled Moebius/tanh/Schwarzian and exact-title citation aliases, French bassin/frontiere and German Einzugsgebiete variants. Several broad searches returned unrelated material and therefore furnish weak negative evidence; the domain-restricted primary-language variants returned no results. One potentially confusing alias match was checked in its complete primary [Gong-Toenjes-Pikovsky2020 arXiv PDF](https://arxiv.org/abs/2001.07593): its SectionII defines one-to-one maps on the complex unit circle/disc for phase synchronization, rather than the original two-covering-branch interval transfer map. It was excluded by model definitions, not by a search-result label.

## Earlier repository-publication comparison

A separate narrow read-only check looked for this target ID/OWR alias, source title and associated map/basin aliases in the repository's publication README/PUBLICATION/CITATION/bibliography/manifest metadata, excluding current/prior audit-program folders. It did not inspect excluded PRs' substantive proofs or verdicts. At captured live main `14f442bc0aadeef2798b3f0af88f677e0b9ca9b1`, the target's queue metadata still says queued0/5; available local all-ref subject history returned only the current audit commit. The publication-metadata alias search produced no matches. All28 returned GitHub release tags and names were checked and supplied no target/map/basin alias match.

Thus no equivalent own previous release was identified in the inspected publication metadata. This does not certify semantic absence from unnamed or renamed release assets, unavailable branches, untagged public manuscripts, or unrelated-title papers. Full native commands, exit codes and outputs are retained privately and bound in the ledger. No release asset, unrelated proof, or excluded PR was substantively audited.

## Version and access record

The official OWR PDF, author BKZ PDF, arXivv1 PDF and exact ESI2075 PDF are separate retained payloads with separate hashes. Own curl retrieval resolved the ESI access failure: 1544891 bytes, SHA256 `0628d7a9acb61435d6513d919966502821ee8a38f4a9ec0a49f8e55264af1dd4`. Its text layer is sparse; relevant original pages were inspected as pixels without installing OCR. ESI printed p.8 uses openness within **each** L1-compact set. In metric D this is equivalent to full relative openness: otherwise a non-basin sequence converging to a basin point forms a compact counterexample. Thus this is a version wording/proof distinction, not a weaker openness conclusion. ESI Prop4 remains genuinely restricted to D-prime.

The retained arXivv1 PDF prints both its arXiv version stamp, 21 December2008, and a separate internal date, 10 November2018. Both marks are retained as version provenance; the internal date is not treated as evidence of a later submission or mathematical revision.

The actual BKZ journal DOI is [10.1007/s00220-009-0854-9](https://doi.org/10.1007/s00220-009-0854-9), published4July2009, CMP292pp237-270. Zweimueller's older published-paper link points to obsolete Springer100467. The attempted actual journal PDF URL returned complete subscription HTML rather than PDF; its native response is retained and labeled non-PDF. **The final journal proof was not inspected.** No author preprint or ESI scan has been represented as that final version. The readable preprint proof plus original post-publication OWR conjecture give a substantive baseline, but do not eliminate the final-version comparison gap.

## Review and reproducibility limits

All38 supplied snapshot files were independently byte-checked against the immutable binding; candidate exposition was accessed only after the baseline seal. No current sibling substantive verdicts, or submitted historical reviewer conclusions, were used as evidence. One parent clarification about the elementary compact-set topological equivalence was incorporated and logged; early source reconstruction therefore remains independent, while subsequent review is not perfectly information-isolated.

The read-only check_priority_claims.py independently confirms the zero-field polynomial counterexample, normalized lifted-map factorization, and all40 rational interval inequalities. Its maximum squared upper bound is 31935269/35322000<91/100<(24/25)^2. Those finite checks corroborate algebra and the interval certificate; they do not prove the measure-theoretic closure theorem or literature completeness.

The sealed package binds public analytical files and private complete payloads/process receipts separately and includes a portable read-only namespace verifier. No installation, outreach, Git mutation, branch/index change, PR modification, push, release or publication was performed. This audit is agent-generated and has **no human peer review**. Additional outside expertise could strengthen final-version and literature comparison, but no contact or outreach was prepared or initiated.
