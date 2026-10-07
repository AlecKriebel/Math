# Independent selection and simultaneous-closure review

Final binding date: 2026-10-07 04:52:09 UTC. Scoped review completion: 100% (best guess).

**Scoped verdict: PASS, conditional on the separately reviewed force/energy/local-theory inputs.** No counterexample or missing species-dependent step was found in the occupation, angular-direction, representative-selection, derivative summation, bootstrap removal, or joint momentum-doubling machinery. This verdict does not independently certify the full global theorem or the entire upstream manuscript.

## Claim and review boundary

The target is the original arbitrary-data claim for a fixed finite collection with arbitrary positive masses and real signed charges. On a compact classical prefix, write `lambda_a=e_a/m_a`, `q(v)=sqrt(1+|v|²)`, and `u(v)=v/q(v)`. The scoped claim is that, given the positive spatial/cone energy budgets and the pairwise signed identity with all printed direct/projected/cutoff majorants, the analytic chain produces one increment bound

`|V_a(t_2)-V_a(t_1)| <= M P sqrt(I) + A I P² log(2+P)/w`

for every supported species receiver simultaneously, with constants independent of the prefix endpoint. The resulting joint first-hit argument excludes finite-time momentum blowup. A matching local/continuation theorem is a separate final input.

Success criteria were: actual pinned proofs rather than theorem-statement transfer; no equation asserted for the positive aggregate; no equality between source and receiver acceleration; no species multiplicity inside an angular logarithm or field budget; no bootstrap-dependent final weighted-force constant; and no assumption that successive joint maxima occur in one species.

I read the frozen v2 supplements as candidate evidence and then independently read the actual pinned proofs. The final verdict is bound to **package_v4**. I inspected the complete v2-to-v3 main-source diff: the only changes name Glassey–Strauss as the original continuation criterion and add its bibliography entry; that attribution/local-theory change belongs to the parent review. `V3_DELTA_RECEIPT.json` preserves that comparison. I then inspected the complete v3-to-v4 diff: it adds only a small-font ragged-right bibliography group and 3pt item spacing. Removing those exact three formatting additions reproduces all v3 main-source bytes. The entire reviewed core is byte-identical to v2, and both audited supplements, the selection certificate, and the pin manifest are byte-identical across v2, v3, and v4. `V4_DELTA_RECEIPT.json` and `V3_TO_V4_MAIN.diff` record the final comparison. I did not read earlier review verdicts. All seven upstream proof-file hashes match commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a`. Full absolute paths and final v4 hashes are in `SOURCE_RECEIPT.json`; the original v2 and v3 receipts are preserved separately.

## Verified mechanisms and attempted falsifications

| Mechanism | Frozen v4 evidence | Actual pinned proof evidence | Adversarial conclusion |
| --- | --- | --- | --- |
| Disjoint label spaces and aggregate density | `main.tex:162–168,300–355`; uniform supplement:52–141 | occupation:108–179,223–300,373–416 | A scalar Vlasov equation for `f_*` is unnecessary. The fixed-time spatial map is receiver-only. Every source component preserves its own label mass and has its own bootstrap. Summing components at a common cell time gives `C/p`. |
| Shared angular energy | `main.tex:334–355`; uniform supplement:111–140 | occupation:304–351,379–415 | Both indicator families have bounded overlap in `p,phi` at every phase point. The retarded receiver time is unique. Integrating `q sum_b f_b` therefore gives one aggregate budget; its bound is independent of `theta,h,M,A`. |
| Shared field budgets and direct sums | `main.tex:357–410`; uniform supplement:143–220 | direct:37–136,138–243,245–428 | The aggregate `N=sum_b N_b` obeys the same density and `N²` inequalities. Apply Cauchy–Schwarz to this aggregate before spending the cone `G²` or spatial `B²` budget. Every `|c_ab|` and `|c_ab lambda_b|` enters one fixed exterior constant. |
| Direction counts without circularity | `main.tex:438–454`; uniform supplement:222–249 | direction:22–209 | Fixed selection `theta<kappa phi,p theta sqrt(h)<=1` uses baseline occupation only. Bulk terms over disjoint intervals share a single upper length. Receiver/projector errors cost `C(M,A)sqrt(w)L³`; only time-weight derivatives cost `CL²N_c`. `w delta>=P^(6/25)` absorbs the latter. |
| Separate source/receiver direction partitions | `main.tex:456–477`; uniform supplement:251–278 | direction:222–371 | Bad hits occupy `O(h)` source time per receiver boundary without assuming bounded `dt/ds`. Good hits admit a fixed relative-velocity projection on each common refinement interval. Refinement counts add; no product of source and receiver counts occurs. Different signed accelerations do not alter these arguments. |
| Pure representative selection and coefficient | `main.tex:479–526`; uniform supplement:280–310 | selection:40–270 | Species constants remain outside `M_*` and `U`; they do not enter the representative inequality. The unsafe selected range is incompatible with the raw exact exponent inequalities. Independent arithmetic receipt confirms the positive contradiction margin below. |
| Source and spatial cutoff reassignment | `main.tex:412–436,527–535`; uniform supplement:312–351 | cancellation:127–169,207–270; selection:272–443 | `sum beta_j=1` is differentiated in each component's own state variables. The common multiplier is factored before reassignment. Different species kernels are never canceled against one another. The extra `lambda_b` changes only the fixed direct-error constant. |
| Uniform simultaneous bootstrap removal | `main.tex:540–569`; uniform supplement:353–379 | closure:8–87 | Edge ramps use signed increments of the same receiver. Choose the ramp fraction, then `M`, then `A`, then `P_0`. The finite compact-force bound is used only for relative openness. It does not enter the uniform constants. |
| Changing maximizing species in joint hits | `main.tex:571–586`; uniform supplement:381–394 | setup:69–102 | For the species-label attaining `Q(t_n)=2^n`, its last half-energy time `s_n` has `Q(s_n)>=2^(n-1)`, hence `s_n>=t_(n-1)` by continuity and first-hit definition. The selected trajectory stays in the needed range regardless of which species attained the previous maximum. |

## Independent selected-exponent derivation

Set `p=P^(1-alpha)`, `w=P^z`, `c=1-z`, `p theta=P^b`, `phi=P^(-y)`, `h=P^(-H)`, and `Delta=epsilon(alpha+b+y+H)`, with `epsilon=1/100000`. All exponents are nonnegative and `c+z=1`.

Near selection and `I<=(w/P)²` give

`2alpha + H/2 + 2y < z+Delta`.

Pure energy far selection gives `b<H/2-alpha+Delta` when `H<=2c`, and `b<H-c-alpha+Delta` otherwise. In particular `b<H-alpha+Delta`. Thus, with `d_*=alpha+b+y+H`, one has `d_*<2H+y+Delta<4z+5Delta`, so

`Delta < (4/99995)z < z/1000`.

Unsafety of both entries of `U` implies

`b>2H/3+z/6-Delta/3`, and `b<H+2y-z/2+Delta`.

The `H<=2c` branch forces `H+z+6alpha<8Delta`, which is impossible. The other branch gives `H>z/2+3(alpha+c)-4Delta>.496z+3(alpha+c)`. Combining with near selection yields `3.5alpha+1.5c+2y<.753z`. The identity `c+z=1` then gives actual separation before any bootstrap constants are absorbed: both `z-y` and `1-alpha-y` exceed `.623`, hence `m phi>P^.3` for large `P`.

For `rho=max(alpha,c)`, the actual stable-cell entry and the uniform positive lower bound on `z` allow `lambda^(-1/2)<=P^(rho+y+.001z)` after a threshold depending on fixed `M,A`. Its far selection then gives

`b<H/2-min(alpha,c)+y+.002z`.

Comparing it with unsafety and near selection gives `H<.8076z`, `alpha+c<.105z`, `z>200/221`, and `1-alpha>.895`. The two unsafe inequalities also give `y>.19z>.171`; the earlier upper inequality gives `y<.49min(z,1-alpha)`. Therefore both momenta and both ends of the improved-occupation angular window are satisfied. This step does not merely assert the window from high receiver energy.

The improved entry now yields

`beta y>H/3+z/3+2min(alpha,c)-8Delta/3`,

while near selection gives

`beta y<(beta/2)z-(beta/4)H+(beta/2)Delta-beta alpha`.

For `beta=29/25`, discarding only nonnegative terms and using `Delta<z/1000` forces

`H/z < 37487/93500`.

But the previous inequality forces `H/z>62/125`. Their exact strict gap is `8889/93500>0`. No species coefficient occurs in these inequalities. The independent script also checks the actual-to-window roundings, the enhanced occupation absorption power `56/3125`, and positivity of the spatial/time-weight geometric-tail exponents.

The printed candidate arithmetic script was reproduced separately. Both scripts exited zero; neither one is a proof of its analytic premises. The separate raw derivation above explains how those premises imply the checked arithmetic.

## Summation and parameter dependencies

The small-sector spatial transition is safe because `R` depends on `p,phi` but not on `theta,h`. Its near/far product is `I R² p² phi²`, and `n_0` is a strictly positive geometric power of `theta`. Both tails therefore sum to `C sqrt(I) R p phi`; the aggregate angular-energy budget supplies the final `C B(I,w)` without another logarithm. Structural neighbors have bounded multiplicity. Deficit bins use their near estimates and `h<=C/P²` rather than an unavailable far estimate. The central residual and short-radius weight term fit the same budget. Long-radius weight terms have positive radial and angular exponents and geometric sums. I found no omitted species-count or time-piece factor in these transitions.

The dependence order is valid. Baseline constants depend on data, horizon, and the fixed finite species list. Direction counts may depend on `M,A`. Their factor `C(M,A)L^7` is absorbed using the positive power `phi^(-4/25)>=P^(56/3125)`, above a threshold depending on `M,A`. The final occupation and weighted-force constants are independent of `M,A`; choose the ramp fraction, `M`, `A`, and finally that threshold. Large charges or small fixed positive masses enlarge the chosen constants, but do not require contraction or smallness.

For the printed closure choices, the nontrivial weighted estimate improves each bootstrap coefficient to at most one quarter: `C_eta/M<=1/8`, `2sqrt(eta)<=1/8`, `C_eta M/A<=1/16`, `C_eta/sqrt(A)<=1/16`, and `2eta<=1/8`. The large-bound endpoint case gives a half bound. Consequently the finite union of species satisfies one strict half bootstrap. Fixed-prefix force boundedness then proves openness uniformly over that finite union.

At joint dyadic hits, one term in the increment inequality is at least `2^(n-2)`, giving `t_n-t_(n-1)>=c/log(2+1024*2^n)`. Its divergent sum excludes finite-time joint momentum blowup. All-neutral species have constant momenta; empty components can be omitted. Repeated species, opposite charges, nonzero net charge, and arbitrary fixed positive mass ratios cause no change in this scoped chain. Constants are not uniform for a massless or infinite-species limit, and neither limit is claimed.

## Exact remaining gap

There is no identified gap within the reviewed occupation-to-closure mechanism. The strongest independently checked result is its **conditional finite-species closure**, together with exact selected-exponent margins and verified transfer of its analytic inputs. Promoting this to the full global theorem still requires separately validated (i) signed retarded pair identity and all direct/projected/cutoff/boundary majorants, (ii) positive energy/cone flux and volume-preserving species flows in the exact class, and (iii) matching local theory, uniqueness, and bounded-momentum continuation for the stated `C_b^infinity ∩ L²` fields. These are neither proved by the arithmetic tests nor discharged by citing the one-species theorem's statement. No priority, Lean-build, publication, or DOI claim is made by this subaudit.

## Evidence files

- `SOURCE_RECEIPT.json`: absolute reviewed paths, SHA-256 hashes, all seven upstream pin matches, test exit statuses, and confirmation that all input files stayed unchanged.
- `V4_DELTA_RECEIPT.json` and `V3_TO_V4_MAIN.diff`: final v4 binding, exact typography-only comparison, and byte-identity evidence for the core and all supporting inputs audited here.
- `V3_DELTA_RECEIPT.json`, `SOURCE_RECEIPT_V2.json`, and `SOURCE_RECEIPT_V3.json`: preserved receipts from the earlier frozen v2/v3 review stages.
- `independent_exact_arithmetic.py` and its `.stdout.json`: fresh exact checks derived from the printed raw inequalities.
- `frozen_rational_selection_certificate.stdout.json`: reproduction of the candidate's separate arithmetic certificate.
- `reproduce_subaudit.py`: standard-library reproduction command; writes only this audit directory.
- `VERDICT.json`: machine-readable scoped verdict.

The final frozen v4 main source hash is `9d72d239677c1066ba22ffbea8ff36f26251a2eae532921bd5e8e12b5f9fdb8c`. The earlier v3 main source hash is `2f98fe5e29570675d4d583b1151a247ead90c6ed0d44302aa5d47c74c4964872`, and the initial v2 main source hash is `8c6d45b8408bb89da4412263becc6956e1b63229ef81daec1caa28272fedad21`. No candidate or upstream source was mutated, no git operation was performed, and no external individual was contacted.
