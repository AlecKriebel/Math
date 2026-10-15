# First fresh whole-manuscript and publication-package adversarial review

PR211 / 5100063 / AMR-050-0063 / k904,a. Reviewer: independent internal AI subagent `pr211_whole_manuscript_adversary_01_20261015_retry`. Review date: 2026-10-15 UTC.

**Verdict: the mathematics and qualified source/priority presentation pass this review; the frozen package requires documentary fix M1 below. It is not yet a clean publication package.** No unresolved mathematical gap or counterexample was found. O1 is an optional source-title metadata reconciliation, not a citation error or publication blocker. After the fix, the parent must reseal the complete working package and obtain the next fresh whole-package review. This first review alone supplies no publication clearance.

## Exact frozen scope and independence

The sole reviewed publication snapshot is `preprint/history/review01_frozen/`, with:

- manuscript source SHA256 `baf296a07ec1020859b5ef3725f38065ee88108fb93e36b47dc8d356d6cca1a1`;
- manuscript PDF SHA256 `6acd3f2f29421516a8635937dd7273700956be2ac203816d7c5c8e928670eb74`;
- 133-entry source ZIP SHA256 `e910e834e91e007ea6c6c929b0c5b91f22424861299081b1d61c08e373c357f9`;
- original native source head `9d7b623203b525386da3d9d91548c79e7445a11c`.

I read the entire manuscript source first, froze `INDEPENDENT_RECONSTRUCTION.md` at 11:06:30 UTC before reading inherited report/checker contents, and wrote the fresh `independent_controls.py` without importing those programs. The inherited team context already contained synopses of earlier work; this was therefore a source-first independent reconstruction and new calculation, not a claim of complete blindness to all prior team context. The parent subsequently supplied a documentary attack surface concerning active-looking imported source records. I independently inspected those files and expanded that finding to the current WIP and stale branch-head fields. No other reviewer was used as a mathematical premise.

The claim is the signed straight-segment shoelace area product for unit inversions of **outer tangent-intersection vertices**, centered at the **original billiard foci**, for a strict nondegenerate confocal ellipse pair and every odd least-period family, including coprime stars. Fixed repetitions, reversal, a separately treated circle, geometric scaling and inversion-radius scaling are also asserted. These are the objects actually audited. No original-vertex, inverse-arc, filled-face-area or outer-locus-own-focus substitute was accepted.

## Deductive verification of the all-period argument

### Coordinates, incidence and normalization

Stachel's published Theorem 4.3 and (4.9), actually read at printed p.1614, provide the caustic-eccentricity Jacobi modulus, canonical increment and coprime turning-number parametrization used here. Its notation `m` is the modulus; the numerical programs correctly pass the square to mpmath. The unused printed auxiliary dn real-shift sign error is identified in the supporting source notes and is not propagated into the proof: dn has real period 2K.

For any real phase the tangent coefficients are `(-sn(z)/a, cn(z)/b)`. Their determinant is nonzero because `sn(v), cn(v), dn(u)` are positive in the relevant factors and `1-k² sn²(u)sn²(v)>0`. Substitution gives the stated outer locus. The inequalities `Ao>a`, `Bo>b` imply every outer point lies strictly outside the original ellipse: its original-ellipse quadratic form is `(Ao/a)² sn²u+(Bo/b)² cn²u>1`. Both original foci lie inside. Thus neither a tangent intersection at infinity nor an undefined real inversion is hidden. Nothing requires the outer horizontal axis to be the larger one.

The focal squared-distance coefficients agree with the factorization into `(1+k sn u)(U+kV sn u)`. The following independent determinant expansion also checks the delicate normalization. Writing `s±=sn(u±v)` and `c±=cn(u±v)`, addition gives

`s+ c− − s− c+ = 2 h C dn(u)/D`, and `c−−c+ = 2 sn(u)h dn(u)d/D`.

Consequently the translated outer cross-product divided by two is

`Ao Bo h C dn(u)/D + c Bo sn(u)h dn(u)d/D`

`= alpha Bo h d dn(u)(d+kC sn(u))/(C D)`.

Each focal squared distance contributes `alpha²/q²`; their product supplies `alpha⁴/q⁴`. Dividing the determinant by the two distance products leaves exactly the manuscript's `C0=Bo h d q⁴/(alpha³ C)`. The q⁴ factor is correct. The two edge-factor product identities and the triple-angle polynomial numerators were additionally proved by fresh symbolic zero residuals, rather than inferred from the numerical tests.

The triple-angle quantities satisfy `L0=Z dn(3v)`, `L1=Z cn(3v)` with `Z>0`. For real arguments, `L0>0`, `L0²-k²L1²=k'²Z²>0` and `d²-k²C²=k'²>0` make both real linear denominator factors positive. All other edge factors are positive. This justifies the nonzero trace argument later; it does not assume the desired product invariance.

### Exhaustive poles and the critical triangle

The DLMF periods/poles/zeros and quarter-shift table were checked afresh at [22.4](https://dlmf.nist.gov/22.4), with addition formulas at [22.8](https://dlmf.nist.gov/22.8). On the sn torus with periods `(4K,2iK')`, sn has degree two and critical values `±1, ±1/k`. The quarter shift gives the two first-factor roots `r0±v`. Their common value has magnitude `d/(kC)>1/k`, so they are simple and exhaustive. The squared first factor permits double poles.

For the second factor, `L1≠0`: in `0<3v<3K` a cn zero would be at K, yielding `N=6tau`, impossible for odd N. The two roots are `r0±3v`. The dn/cn ratio has squared magnitude exceeding one unless `sn(3v)=0`; hence the only critical fiber inside this range is `3v=2K`. Coincidence modulo 4K gives the same condition. Coprimality forces `N=3,tau=1`. There the factor is `Z(1-k sn u)`, of order two at `K+iK'`, while dn has order one. Since cn there is nonzero, its simple dn zero follows also from `dn'=-k² sn cn`. Thus the net pole has order at most one. This point is not a first-factor root.

The first/second fibers are disjoint, because an intersection would require 2v or 4v to be a multiple of 4K, excluded by `0<v<K`. At a common Jacobi pole, numerator and denominator both have order three; the finite ratio is removable. No other analytic factor can supply a pole. In particular neither critical Jacobi zeros nor the branch coalescence add unlisted pole orders. This complete list is sufficient; no unproved residue formula is needed for the universal proof.

### Cyclic trace, divisor and original opposite focus

Jacobi parity and shifts give `e(2r0-u)=-e(u)`. If the quadratic coefficient at `r0+v` is a, reflection puts coefficient −a at `r0−v`; the sign is unchanged by squaring the local coordinate and changed by odd reflection. Their separation is exactly delta. Primitivity makes each translated first-root list have N distinct points, and the two lists coincide with a cyclic reindexing. Therefore at each translated point one coefficient of each sign occurs, cancelling the entire quadratic part. The second-root poles are already simple and lie in the same orbit; the N=3 collision does not create an extra double term.

Bézout gives the real trace period `L=4K/N` from delta and 4K. Its imaginary anti-period is `2iK'`, so the actual compact torus for the trace is `(L,4iK')`. On it the only possible poles are `R,R+2iK'`, each at most simple. Anti-periodicity pairs them. If both were removable, compactness and anti-periodicity would force the trace to be zero, contrary to its strictly positive real sum. Both therefore occur with order one.

Cyclic reindexing preserves odd reflection about r0. Adding the period `2v=delta` moves its center to R. At `R+L/2` reflection is a real-period translation; the trace vanishes there. Its anti-period yields the second distinct zero at `R+L/2+2iK'`. Neither is a pole. The degree-zero divisor of a nonzero meromorphic function on a compact torus then makes these the complete two simple zeros. Translation by L/2 interchanges the zero and pole divisors, proving the product holomorphic and constant. This step neither assumes the product nor relies on a finite enumeration.

The central-reflection identity uses the *original* centers: `J_fminus(Q(u))=-J_fplus(Q(u+2K))`. The determinant of central reflection is +1, so the two signed areas differ by the real shift 2K. For odd N that shift is L/2 modulo L, proving the target. Positivity gives a positive constant. Reversal negates each signed area. Repetition multiplies both by r. For a geometric scaling s and inversion radius rho, each area scales by `rho⁴/s²`, so the product has the asserted `rho⁸/s⁴` factor. The circular formula follows directly from the regular/star tangent polygon radius and central vertex inversion; the note appropriately treats it separately from `0<k<1`.

**No circular step, unsupported geometric transfer, excluded division, or unresolved all-period proof gap was found.** Hyperbolic and collapsed caustics are explicitly outside the claimed theorem. The source's nondegenerate confocal-ellipse setting, rather than a broader implicit extension, is the scope accepted here.

## Fresh falsification controls and reproduction

`independent_controls.py` proves five zero polynomial residuals, then independently solves the actual two tangent equations in Cartesian coordinates, inverts those intersections and computes shoelace sums. It imports no candidate or inherited checker. It passes:

- 72 families with moduli 0.01, 0.3, 0.83 and 0.999; N=3,5,7,9,11,15 and every coprime turning number below N/2;
- 216 actual real polygon phases and 216 independent complex direct-edge comparisons;
- opposite double-principal-part checks for every family;
- 36 contour neighborhoods of candidate first/second/Jacobi pole locations, plus trace-pole and complementary-zero checks in twelve convex/star/triangular families;
- fresh scaling, nonunit inversion-radius, odd/even repetition and reversal controls.

The new complex tests extract Laurent coefficients by a 32-point contour discrete Fourier sum. They show vanishing quadratic trace terms, nonzero simple trace residues, no residual quadratic second-fiber term, and removable common Jacobi poles. These are explicitly **uncertified numerical diagnostics**, not exact contour integrals or interval proofs. Their purpose is falsification of the analytic proof above. The largest scaled Cartesian/edge discrepancy is about `5.1e-98` at 100 digits. Numerical absolute-normalization limits are not misrepresented as relative accuracy for arbitrarily tiny values.

I also ran the supplied portable harness with `--run all` in disposable folders, with bytecode disabled. Every one of its ten jobs passed, **each output was byte-identical** to the frozen expected result, and the complete 87-file portable inventory was unchanged before/after. `HARNESS_REPLAY.json` records every job, digest, duration and environment. The five core assertion counts, lattice bounds and separately labelled numerical status agree with the checker implementations and README. Finite enumeration is expressly distinguished from the universal proof. Assertions are active; the harness rejects optimized Python and unsupported dependency versions.

The harness uses no network or repository checkout. Explicitly enumerated scripts/inputs are copied into temporary folders; archived checkers' output writes remain there. Inspection found no hidden downloaded code or provider mutation. The historical ledger builder is correctly documented as an excluded-input authoring utility, not a portable replay target. The own controls and result receipts are support for this review, not another claim of theorem priority.

## Source and priority checks

I read the exact v11 signed-area convention, §3.9 definitions and full Table10, and actually viewed its table page. The statement is precisely the odd product of the two primed original-focus inverse areas. I also actually viewed the v10 Table9 and independently checked fresh primary [v10](https://arxiv.org/abs/2004.12497v10) and [v11](https://arxiv.org/abs/2004.12497v11) release history: k808,a on 25 October 2020 becomes k904,a on 29 October 2020. The `10/20` source date is a month/year, and the active attribution should use 2020. The proof and package do not confuse this with the shorter journal companion's omitted product.

I read Chavez-Caliz's complete Theorem6 proof at printed pp.104–105. Its complementary pole/zero area mechanism deserves the explicit credit supplied; its observable is an even untransformed Poncelet/tangent-area product. KLS's primary title/introduction and the audited principal-part/half-period mechanism agree with the note's credit. The established complementary-divisor theorem is not represented as new.

The primary original-vertex statements of Garcia–Reznik Proposition15 and Reznik–Garcia–Helman Proposition7/Conjecture1, the recent Ferudun theorem's original-vertex definitions and related-work scope, and the final Roitman–Garcia–Reznik starred experimental area entries were checked at their actual passages. They concern important neighboring results. The outer focal norm is not an original-ellipse focal norm square: the note's strict `Ao²−Bo²−c²<0` identity is verified symbolically. A separately established k806,a inverse-area-ratio theorem would be a possible bridge, but neither the proof nor the priority conclusion assumes that missing premise.

The current priority summary, both independent family conclusions, source-to-claim scope ledger, provenance receipts and explicit source-access limitations were inspected. This review does **not** claim a third exhaustive search of all literature or full reading of every classification source. The package's qualified wording is appropriate: no exact earlier general proof was verified in the audited corpus, historical novelty is undetermined, no first-proof or present worldwide-open claim is made, and the subscription-limited final *Talented* text is not declared byte-equivalent to open author versions. Those limits remain material and must stay in the final package.

## Full package, PDF and metadata

`package_integrity.py` independently validates all byte sizes/hashes, inventories and archive members, without resealing inputs:

| Item | Verified |
|---|---:|
| source manifest payloads | 132 |
| ZIP entries, each byte-identical to the selected frozen payload | 133 |
| portable manifest payloads | 87 |
| native current packet manifest rows | 38 |
| native top-level presentation rows in each paired manifest | 12 |
| historical original files matching the intake, in each of two copies | 19 |

ZIP names have no duplicate, absolute, parent-traversal, symlink or excluded private/cache path. All five original audit-family manifests and their relocated authored payloads validate, with their documented original path bases; all 19 PROVENANCE original pins validate. The three original primary-PDF digests were rechecked against the private reading copies. No primary PDF/text/HTML/rendering is in the publication archive. `deposit.json` metadata is exactly equal to `metadata.json`; PDF/archive submission bindings are correct. No DOI or publication is invented.

I rendered all six PDF pages at 95dpi and actually viewed every page. The readable mathematical expressions, q⁴ normalization, torus periods, page transitions, links, references and review-status paragraph agree with the TeX source. There is no clipping, overlap, missing glyph, unreadable equation, placeholder or broken reference. Author/ORCID/date and extensive AI/unrefereed/no human-peer-review disclosure are visible and consistent with the metadata. Final changes to the bibliography require rebuilding/reviewing the resulting PDF; the frozen source/PDF were not edited in this review.

## Findings and exact global fixes

### M1 — Clearly separate active assessment from superseded native provenance

The proposed current `pr_update/5100063/` includes top-level files whose content is still actively worded:

- `source_record.json`: `status: open`, `research_classification: OPEN-TRIAGE`, `proposed_year: 2021`, and a truncated summary asserting current openness and April–May2020 experimental dating;
- `WIP.md`: begins “Unreviewed WIP”, says author turn1 is active and there is no reviewed result, leaves exact checker/review work pending, and ends at a75% working estimate;
- `metadata.json`: retains `remote_wip_head` as the stale `8a7f1b40b77fa5773bec242e66a046162292c04c` without labelling the field historical;
- the current `prior_imported_report.json` remains a historical triage payload and should receive the same explicit in-file provenance treatment, rather than relying solely on a separate README for its supersession.

These contradict the otherwise careful current mathematics/source acceptance and 2020 attribution. A preserved original is appropriate; an active-looking duplicate is confusing to humans and machine consumers. The portable README explicitly labels `original_submission/` historical, but that alone does not label these current native top-level copies.

**Required fix:** preserve both complete19-file historical originals exactly. For active files, replace obsolete WIP text with a current pointer plus a clearly dated historical provenance pointer, wrap or replace imported source/report records with an explicit immutable-original reference and current assessment/date override, and rename/remove/wrap stale head fields so they are not presented as the current branch head. Current target attribution should state v10/v11 October2020, and the planned target Queue provenance-year correction to2020 is supported while retaining author1/5. Do not rewrite historical originals or the shared database. Reconcile current README/PROOF header/PUBLICATION_STATUS and dated-preparation text so an immutable published bundle is not left asserting a permanently active prepublication state. That later lifecycle update should reflect actual reviewed status/receipts rather than claim a deposit or merge before it exists. Rebuild every affected current seal, ZIP and package binding.

This is a **documentary publication blocker**, not a mathematical refutation or a request to change archived research history.

### O1 — Optional reconciliation of printed and arXiv-record source titles

The manuscript's `bibitem{RGK}` currently gives “Eighty new invariants in the elliptic billiard”, which **matches the actual pinned PDF's first-page printed heading**. The primary arXiv v11 metadata record instead uses **“Eighty New Invariants of N-Periodics in the Elliptic Billiard”**. Both identify the same correctly pinned source; the arXiv identifier and theorem locator are already correct. An earlier provisional reviewer message called this a required bibliographic defect. After the parent identified the PDF/metadata distinction, I independently checked the actual PDF first-page text and corrected that overstatement here.

**Optional precision choice:** use the longer arXiv-record v11 title in the active reference to make machine metadata and bibliography agree. If changed, rebuild and inspect the PDF and update archive/source/package manifests. The v10 arXiv record uses *Seventy New Invariants of N-Periodics in the Elliptic Billiard*. The parent has elected to make this harmless reconciliation. Do not edit historical sealed submissions merely to standardize bibliography spelling.

No other mandatory finding remains from this review. No optional mathematical extension or extra computation is requested. A numerical explicit formula for the constant is not needed to prove this source assertion.

## Handoff and limits

This assigned review is complete (100% of its scope). The strongest result is a checkable independent analytic verification of the manuscript's exact all-period argument, fresh falsification controls, ten isolated byte-identical replays and complete package binding checks. The exact remaining gap is **global documentary repair and a new subsequent whole-package adversary on the repaired frozen bytes**. Historical first-proof priority remains undetermined as stated; this review supplies no stronger priority certificate.

No frozen publication file, native PR, Queue, Git/index/ref, database, provider, Zenodo record or tracker cell was changed. No external individual or other-shard chat was contacted. Writes are confined to this review folder, including disposable harness work that was automatically removed. Rendered derivative PNGs are excluded from the authored manifest. Parent retains every correction, promotion and publication decision.
