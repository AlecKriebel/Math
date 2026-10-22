# Joint independent review: PR1270 / 2200014 and PR1277 / 2200015

**Verdict: full credited prior negative coverage for both original conjectures.** The weighted degree-24 integer polynomial has 22 distinct simple negative roots and parity count 20. The unweighted degree-15 integer perturbation has 13 distinct simple negative roots and parity count 11. Both have strictly positive coefficients. I found no mathematical or original-target coverage gap in either complete symbolic proof.

The prior disproof and primitive family are credited to **Olga Katkova, Boris Shapiro and Anna Vishnyakova**, *In search of Newton-type inequalities*, Journal of Mathematical Analysis and Applications 538(1) (2024), article 128349, [DOI 10.1016/j.jmaa.2024.128349](https://doi.org/10.1016/j.jmaa.2024.128349). The inspected mathematical body is [arXiv:2403.12200v1, §5](https://arxiv.org/pdf/2403.12200v1), not the publisher-formatted body. The finite degrees and explicit root splitting here are credited reconstructions and robustness certificates, with no novelty, construction-priority or minimum-degree claim. This new joint review is AI-only and unrefereed; it is not external human peer review, journal acceptance of these reconstructions or formal proof-assistant certification.

## Inputs and exact original scope

PR1270 is pinned at `04d220746dd5e5475c821ac1c2626e7ac5d3d884`; PR1277 at `a6d802ac5a86fcb1f50245ac51b5d7490a4a3f43`. Both have base `4b27092a448d53b61408355ce44ec38d103a1ce4` and exactly seven additions in their own problem directories. I read both live bodies, both complete proofs, the full mathematical reports/audits, acceptance and source metadata. All fourteen actual immutable blobs are separately bound by hash; editorial-map JSON and manifests were parsed as metadata, not treated as mathematical evidence. Historical checker execution or export-integrity assertions have not been borrowed as new mathematical runs.

The original source is Boris Shapiro, [arXiv:1503.05295v1](https://arxiv.org/pdf/1503.05295v1), p.4, Conjectures 9 and 10, credited there to Forsgård and Shapiro. I freshly downloaded the eight-page PDF, 149,888 bytes, SHA-256 `1649d0c0b67131e42f6a9f7bbc8563e9d03cfa0419aa7aadbcc2a86e33b6a2b0`; read pp.1,3–5 and visually inspected p.4. The adjoining tropical conjecture, polynomial-like-function questions and subsequent Hawaiian topic are distinct. The original cached research triage is not a current source-status determination; its uncertainty is superseded here by inspection of the exact later disproof.

Both targets concern a real polynomial of actual degree `n`, with every coefficient `a0,…,an` strictly positive and `a−1=a(n+1)=0`. Define:

| Target | Difference | Selected indices |
| --- | --- | --- |
| Conjecture 9 / 2200014 | `(k+1)ak²−k a(k−1)a(k+1)` | strictly positive differences |
| Conjecture 10 / 2200015 | `ak²−a(k−1)a(k+1)` | all nonnegative differences, including zeros |

The statistic counts changes between consecutive parities of the increasing selected indices. It is not a sign-change count of the differences themselves. The endpoint differences are positive in each convention. There is no cyclic comparison. Both source displays define `k1,…,km` but print a parity-sequence lower index zero, leaving `k0` undefined. Using the actual expressly defined list is the coherent indexing correction, reproduced by KSV. It does not add a new term. Even an arbitrary single extra initial parity comparison could add at most one, while each exhibited root-count gap is two; that artificial extra term would not save either bound. No author-authenticated erratum is claimed.

The source does not specify root multiplicity explicitly in either conjecture. KSV's Notation 3, p.3, explicitly counts multiplicities, and §5 uses the repeated root at minus one. The explicit split-root witnesses below refute both distinct-root and multiplicity interpretations, without relying on which convention the original intended. Positive coefficients exclude all nonnegative real roots, so the real roots exhibited are necessarily negative. No monic or constant-term-one restriction is imported from other notation in the paper; positive scaling would in any case preserve the statistic and roots.

## Weighted example: complete independent argument

Set `Q(x)=38x²−188x+326` and `P(x)=(1+x)^22 Q(x)`. Binomial expansion gives, for `0≤k≤24`,

`ak=326 C(22,k)−188 C(22,k−1)+38 C(22,k−2)=C(24,k)((k−18)²+2)`.

Out-of-range binomial coefficients are zero. The identity proves strict positivity, including both endpoints and the nonzero leading coefficient. For `qk=ak²/(a(k−1)a(k+1))`, direct rational substitution gives

`q17=108/119<17/18`, `q18=133/243<18/19`, `q19=18/19<19/20`.

For positive coefficients, the weighted difference is negative exactly when `qk<k/(k+1)`. Thus indices 17,18,19 are excluded. Any selected index list is a subsequence of `0,…,16,20,…,24`, which has 20 parity changes: 16 in the first block, zero across the even-to-even gap, and four in the last block. Removing entries cannot increase variation, because `1(u≠w)≤1(u≠v)+1(v≠w)` for binary values. Hence the parity statistic is at most 20 without requiring the signs at every other index. The discriminant of `Q` is `−14208`, so `P` has 22 real roots counted with multiplicity at minus one; this repeated-root witness alone is not a distinct-root counterexample.

For the distinct-root conclusion use `D=10^6` and

`R(x)=Q(x) ∏(Dx+D+j)`, with `j=1,…,22`.

Write `F=R/D^22`, `δj=j/D`, and `S=Σδj=253/10^6`. To verify coefficient positivity and strict weighted signs without a coefficient table, first put `H=Q(1+x)^21`. Its coefficient is

`hk=C(23,k)(552k²−19032k+164956)/506`.

The numerator has positive leading coefficient and discriminant `−2005824`, so all these coefficients are positive. With zero extension, `ak=hk+h(k−1)`, hence `0≤hk≤ak`. Expand `F` in elementary symmetric functions `es` of the positive `δj`:

`F=Σ es Q(1+x)^(22−s)`.

Here `e1=S` and `es≤S^s/s!`, since expansion of `S^s` includes each product of distinct shifts at least `s!` times. At any index, the absolute coefficient in `Q(1+x)^(22−s)` is bounded by

`Tk=326 C(22,k)+188 C(22,k−1)+38 C(22,k−2)`.

This follows term by term from monotonicity of fixed-bottom binomial coefficients in their upper argument. Moreover

`Tk/ak=1+376k(24−k)/(552((k−18)²+2))<51`.

For `S<1`, the sum of the terms `S^s/s!` for `s≥2` is at most `S²/(2(1−S))`. The first-order coefficient is bounded by `S ak` using `H`, so every coefficient `rk` of `F` obeys

`|rk−ak|/ak ≤ S+51S²/(2(1−S)) =169712147/666498000000 <1/2000`.

All `rk` are therefore positive. Their adjacent ratios are strictly below the old ratios times `(2001/1999)²`. Exact rational comparison gives

`(2001/1999)² qk < k/(k+1)` for `k=17,18,19`.

This preserves the three strict exclusions and thus the sufficient parity bound 20. Scaling by `D^22>0` preserves coefficient signs and selected indices. The real roots of `R` are exactly `−1−j/D`, `j=1,…,22`: they are distinct and simple, while the unchanged quadratic contributes two nonreal roots. The actual degree is 24. Thus `22>20≥v(R)` under either root-count convention. This is a complete finite explicit counterexample with a symbolic uniform estimate, not an unspecified continuity or numerical-root argument.

The independent exact checker additionally establishes that the weighted differences of `R` are negative exactly at 17,18,19 and positive elsewhere, with none zero, so its exact statistic is 20. This stronger finite statement is supplemental; it is not required by the sufficient proof above.

## Unweighted example: complete independent argument

Let `U(x)=(1+x)^13(38x²−89x+83)`. The source seed is `Q15=U/720720`. Direct convolution gives

`ak=83 C(13,k)−89 C(13,k−1)+38 C(13,k−2)=C(15,k)((k−9)²+2)>0`.

Its quadratic has discriminant `−4695` and takes value 210 at minus one. Thus `U` has exactly 13 real roots counted with multiplicity, all at minus one, and only one distinct real root. The positive ratios at indices 8,9,10 are `27/28`, `140/243`, `99/100`, respectively. They are below one; it is the unweighted differences, rather than the ratios themselves, that are negative. The selected list is therefore a subsequence of `0,…,7,11,…,15`, which has eleven parity changes. This proves the multiplicity-counted disproof.

The seed's complete strict sign pattern has an elementary proof. For `t=k−9`,

`qk−1=(14t^4−6t^3+177t²+15t−206)/(k(15−k)(t^4+2t²+9))`.

The denominator is positive at interior indices. At `t=−1,0,1` the numerator is `−24,−206,−6`. For `|t|≥2`, its first part `t²(14t²−6t)` is positive, and the remainder is at least `(339/2)|t|²−206≥472`. Hence no other interior difference is negative or zero. The endpoint differences are positive. This supplies `v(U)=11` without a table, while preserving the original nonnegative selection rule.

For distinct roots set `D=10^7` and

`V(x)=(38x²−89x+83) ∏(Dx+D+j)`, `j=1,…,13`.

It suffices to study `V/D^13`. If `bk` is the corresponding linear-product coefficient and `Bk=C(13,k)`, then each elementary symmetric summand lies between one and `(1+13/D)^13`. Consequently `0≤bk−Bk≤E Bk`, with

`E=(1+13/D)^13−1 ≤169/(D−169)<1/50000`.

The binomial bound uses `C(13,r)≤13^r` and a geometric series. The last strict inequality is the exact integer comparison `8450000<9999831`. On convolution with the quadratic, the absolute error is at most `E sk`, where

`sk=83 C(13,k)+89 C(13,k−1)+38 C(13,k−2)` and

`sk/C(15,k)=(32k²−1110k+17430)/210≤83`.

Since `ak/C(15,k)≥2`, the relative coefficient error is below `83/100000<1/1000`; every coefficient remains positive. The three ratios are strictly below their old values times `(1001/999)²`, and their maximum is `99/100`. The comparison

`99·1001²=99198099<99800100=100·999²`

proves that all three remain below one. Indices 8,9,10 therefore remain strictly excluded even though zero differences elsewhere would be selected. The parity-deletion inequality gives `v(V)≤11`. Its thirteen displayed negative rational roots are distinct and simple; the quadratic has no real roots. Hence `13>11≥v(V)` under both root conventions.

The new exact checker confirms the complete perturbed strict sign pattern and equality `v=11`. It also independently checks the separate `D=10^6` frozen witness mentioned in the PR audit. The table-free uniform estimate just given is specifically the main `D=10^7` proof; the smaller-denominator witness is an additional exact finite check, not silently substituted into that estimate.

## KSV primitive family and the actual source correction

The fresh KSV PDF is 410,816 bytes, SHA-256 `ec72ce38fdaff53fd7c18ede202dc27fcded75ce77add7f79ea7a5c053185f37`, 21 pages. I read pp.1–3 and 19–21, including the entire relevant §5 proof, and visually inspected pp.3,20,21. KSV's Conjectures 2 and 3 explicitly identify original Shapiro Conjectures 9 and 10. Their seed, ratio calculation, repeated primitives and asymptotic weighted argument are actual inspected primary mathematical content. No nonstandard theorem elsewhere in KSV is needed for these explicit reconstructions; other sections and their dependencies were not fully audited.

For `t=x+1`, define

`Pn=t^(n−2)(38t²−11nt+n(n−1))`, `n≥15`.

Then `P15=720720 Q15`, `Pn'=n P(n−1)`, and `Pn(−1)=0`, so the based primitive family is exactly

`Qn=(15!/(720720 n!)) Pn`.

In fact direct binomial expansion gives the useful general identity `coefficient_k(Pn)=C(n,k)((n−k−6)²+2)>0`. The remaining quadratic has discriminant `n(152−31n)<0` for `n≥15`, so `Pn` has exactly `n−2` real roots counted with multiplicity. These formulas independently fill the source's brief positivity/root assertions. At `n=24`, `P24` is exactly the weighted repeated-root polynomial above; at `n=15`, it is the unweighted seed.

A primitive takes coefficient `ak` to coefficient `a(k)/(k+1)` at the next index. Thus

`q(k+1)(Q(n+1))=qk(Qn)·k(k+2)/(k+1)²`.

For a seed index `s` and `r=n−15` integrations, the product runs over `i=s,…,s+r−1` and telescopes to `s/(s+1)·(s+r+1)/(s+r)`. Starting from indices 10,9,8 in degree 15 gives the corrected exact formulas

`q(n−5)=(9/10)(n−4)/(n−5)`,

`q(n−6)=(14/27)(n−5)/(n−6)`,

`q(n−7)=(6/7)(n−6)/(n−7)`.

In contrast, the inspected arXiv v1 pp.20–21 end all three finite products at the factor indexed by `n−1`, yielding `(n+1)/n` instead of the correct shifted factors. The discrepancy is already visible at degree 15: the first printed expression yields `24/25`, while the actual seed ratio is `99/100`. It can change a finite weighted sign: at degree 22 the printed value for `q17` is `207/220<17/18`, but the actual value is `81/85>17/18`. No least-degree conclusion is drawn from this test. The corrected limits remain `9/10,14/27,6/7`; they still justify KSV's sufficiently-large-degree weighted disproof. The finite degree-24 argument here uses direct coefficients and strict rational bounds and does not rely on the incorrect endpoints.

This is a proved local correction to the inspected arXiv v1 expressions, not an author-authenticated erratum or a claim about unseen publisher typography. The journal mathematical body was not retrieved: its PDF endpoint returned 403 and text API 429. The DOI itself redirected successfully to a publisher linking page, which is not article text. Crossref, primary publisher bibliographic search metadata and author/institutional indexed publication metadata authenticate the same title, three authors, journal, volume, issue and article DOI. The current arXiv history has one version, submitted 18 March 2024; the manuscript's own date is 20 March. The freshly retrieved unversioned PDF equals the explicit v1 bytes. Its canonical arXiv DOI and versioned/unversioned URLs are aliases of the same KSV work, not additional solutions.

Shapiro's original journal identity is independently corroborated by Crossref as Arnold Mathematical Journal 1(1) (2015), 91–99, DOI `10.1007/s40598-015-0008-4`. This is an original-source reference, not a solution DOI. Only the identified arXiv v1 mathematical statement was relied upon; no original journal-body inspection is claimed.

## Independent exact checks and adverse controls

Two new standard-library checkers were written after reading the sources; no source-author program or historical checker was read, imported or executed. They use arbitrary-precision integers and rational arithmetic, explicit exceptions and no floating-point roots. Polynomial convolution, an independent Newton-sum expansion, exact integration, factor division, rational evaluations and derivative tests provide independent routes through the stated formulas.

The weighted checker verifies all 25 coefficients, all 25 weighted signs, exact selected order and parity, every simple rational root and the residual quadratic, the compact formulas for `P24` and `H`, every perturbation constant, and all three robust strict margins. It performs based rational integrations through degree 24, checks the general family formulas through degree 64, and checks all 150 corrected quotient products in that range. It also checks 3,586 binary deletion cases as supplemental controls for the universally proved variation inequality. Eighteen corruptions are rejected per mode, including wrong quadratic signs, root multiplicities, too-large shifts, source weight/zero conventions, coefficient endpoints, primitive basepoint, the printed finite formula, a tampered factor identity and an overstrong error budget.

The separate unweighted checker verifies all seed coefficients and complete signs, the quartic identity and positivity estimate, both specified perturbation denominators, all exact roots and residual factors, and the `D=10^7` uniform bounds. Sixteen corruptions are rejected per mode, including strict-only zero selection, the weighted substitution, cyclic coefficient endpoints, false negative-ratio claims, conflating multiplicity with distinctness, a missing/repeated root factor and a changed quartic constant. A toy polynomial with a zero difference explicitly distinguishes the two selection rules, even though the actual witnesses have no zero differences.

Each checker was actually run in normal Python, `-O` and `-OO`. Its three outputs are byte-identical and pass. In total the two checkers reject 102 adverse cases across modes (18+16 per mode). Finite range checks supplement the written identities and inequalities; they do not replace a quantified proof by extrapolation. No formal proof-assistant certification is asserted.

## Ledger, later publication leads and one combined proposal

The initial own numeric-gid duplicate read was completed before weighted mathematics. The parent then explicitly extended this still-open packet to PR1277; a second own numeric-gid read preceded inspection of the new unweighted proof. Both snapshots contain 191 nonempty rows in the 43-column range `A1:AQ1178`, gid `1254632077`. No exact problem, source arXiv or solution DOI match was found. The only broad “unweighted” hit is row53, DOI `10.5281/zenodo.23205294`, concerning binary rational hafnians, perfect matching approximation and sampling. Its objects and conclusion were read and are distinct from coefficient-parity real-root bounds. This semantic distinction is recorded privately without distributing the raw ledger body.

A bounded current publication-lead search also found Ferudun's later [weighted alternative note](https://eulersolve.org/papers/amr-021-0014/), DOI `10.5281/zenodo.23056319`, and [unweighted alternative note](https://eulersolve.org/papers/amr-021-0015/), DOI `10.5281/zenodo.23056466`. Their current primary pages expressly credit KSV2024 as already disproving both conjectures and disclose corrected v1.1 context and unrefereed AI-assisted status. These are separate later constructions, not KSV aliases. I inspected those pages as publication leads, not the alternative proofs or complete packages; their mathematical correctness and historical version genealogy are not certified here. Their existence rules out any suggestion that the present reconstructions are new whole-problem closures. It is not necessary to verify those alternative mechanisms to authenticate the older, directly inspected KSV disproof.

The local proposal contains **one** row with four literal strings, B exactly blank and C the existing KSV journal DOI. A names both original problems; D credits the common publication, distinguishes weighted/strict from unweighted/nonnegative selection, states the two exact root-count gaps, and records the source correction, publisher access limits, later-note leads and AI-only review status. It does not duplicate rows for the same DOI, reserve a DOI, write a tracker or imply project authorship of the disproof.

The exact remaining mathematical or original-target coverage gap is **none for either conjecture**. Publisher-body inspection, exhaustive historical priority, minimal degrees, independent-discovery genealogy, the later alternative proofs and other KSV/original conjectures remain unverified or outside scope. Bounded ledger/release observations are not worldwide absence or novelty proofs. Previous sealed PR1235/1239/1253/1260/1263 review directories remain unchanged and are reverified read-only at closure. The whole joint-scope seal covers all source inputs, both PR copies, both checkers and all nested manifests, excluding only its exact own seal path. Raw source/ledger bodies remain private. No service, Git, CASE/cursor, publication or external-contact action was performed.
