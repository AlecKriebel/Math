# Exact-threshold claims ledger

Last updated: 2026-08-08 audited preprint v1.0.0 release.

| Claim | Status | Exact basis | Remaining gap |
|---|---|---|---|
| `R_sim>=3/2` | **PROVED** | explicit rational center--triangle family; exact module chains, rare-edge bounds, endpoint audit | none |
| center--triangle family amplifies at `r=3/2` | **FALSIFIED FOR THIS FAMILY** | exact deficits `-4/(3N^2)+o(N^-2)` and `-16/(81N^2)+o(N^-2)` | says nothing universal |
| fixed-finite-rank no-direct-portal blade families work at or above `3/2` | **FALSIFIED FOR THIS CLASS** | affine supersolution, exact Bernstein certificate, stopped-trace fixation bound, hostile audit | growing/singular rank and direct portal edges open |
| fixed two-portal, one-blade-type direct network works at or above `3/2` | **FALSIFIED FOR THIS CLASS** | exact three-state portal trace and strict separator `T_B+(81/200)T_D<0`; 11-box rational Bernstein certificate | higher fixed rank/types and non-diffuse or portal-dependent growing rank open |
| diffuse regular growing-portal network works beyond `3/2` | **FALSIFIED FOR THIS CLASS, IN FACT FOR EVERY `r>1`** | exact finite-count trace, branching-episode limit, and complementary Bd/dB threshold factors | fixed-degree networks, portal-dependent incidence, mesoscopic classes, and singular scaling open |
| product inequality at `r=3/2` for positive weighted triangles | **PROVED** | 24-atom squared-difference certificate | arbitrary `n` open |
| product inequality at `r=3/2` for every graph | **EXACTLY FALSIFIED, WITH GROWING NONVANISHING GAP** | finite `G(31,4)` exact witness; growing `K_(8m+1)` plus `m` hub pendants has normalized limits `32/27,8/9`, product `256/243` | not a simultaneous amplifier because its dB ratio is below one |
| no graph simultaneously amplifies both rules at `r=3/2` | **OPEN** | the product shortcut is false; every exact endpoint witness still has at least one ratio at most one | universal disjunctive separator or actual simultaneous graph |
| balanced normalized-arithmetic separator at `r=3/2` | **EXACTLY FALSIFIED** | the same `G(31,4)` has normalized mean `1.0069129408...>1` | seek a weaker separator; Bd weight `1/3` is the strongest surviving fixed affine candidate |
| one-third affine separator `(x+2y)/3<=1` at `r=3/2` | **OPEN; COEFFICIENT PROVED OPTIMAL** | exact Green--Poisson identity; proved for all positive weighted triangles; growing clique--pendant rays prove every universal affine Bd coefficient is at most `1/3`; a rational dB witness forces `theta>=0.088542283991...` | global nonpointwise sign; no coefficient in the exact necessary window `[theta_-,1/3]` is proved universal |
| unit star maximizes dB among arbitrarily weighted stars at `r=3/2` | **EXACTLY COMPUTED THROUGH 20 LEAVES; ALL-ORDER SIGN OPEN** | exact arbitrary-weight star harmonic equations and square-drift coefficient recurrence over `QQ`; equality at 2 leaves and strict sign for 3--20 leaves | prove or refute the finite coefficient recurrence for every leaf count; Bd affine half also open |
| growing clique core with arbitrarily weighted hub pendants can cross the endpoint | **FALSIFIED FOR UNBOUNDED PENDANT COUNT** | uniform bound `rho_dB(G,r)/rho_dB(K_n,r) <= (c+A_r)/(c+m)` for arbitrary individual positive pendant weights | bounded pendant count has only a lower-order open sign |
| reversed-arrow orientation mean inequality at `r=3/2` | **OPEN; EXACTLY REDUCED** | skew/defect Dirichlet identities and electrical two-tree transfer formula | prove the scalar transfer sign; batching factor would still remain |
| `C`-to-dB endpoint batching ratio | **OPEN; EXACTLY REDUCED** | full marked event resolvent, Palm laws, rooted-arborescence/coverage covariance identity | prove paired root-mass transport; persistence, timing, and rootwise signs are each false |
| rankwise Johnson reduction of `T+C` | **PROVED IDENTITY** | exact degree-one/two Johnson Poisson equations and Green summation by parts | high-mode Schur feedback has no proved sign |
| scalar or degree-two Green-flow relaxation proves the endpoint separator | **FALSIFIED AS A ROUTE** | exact rational pseudo-Green laws on `P_3` and a seven-vertex graph | actual Green equations require higher modes |
| a universal fixed convex affine separator can have Bd multiplier above `1/3` | **FALSIFIED SHARPLY** | for every rational leaf proportion `alpha`, exact growing clique--pendant limits have crossing `1/(3 ell(alpha))`, decreasing to `1/3` | whether the sharp multiplier `1/3` is universal remains open |
| complete graph maximizes dB fixation at `r=2` | **OPEN** | exactly equivalent to `L<=V` | stationary cut surplus versus dispersion |
| sharp rank-weighted posterior reflection at `r=2` | **PROVED REDUCTION; FINAL SIGN OPEN** | sharp arithmetic--harmonic lemma `J<=n c G`, exact Brier/Cayley transport identities | prove `E[cG]<=m_K-E|A|`; edgewise and componentwise signs are false |
| symmetric-flow split `L<=S<=V` proves the `r=2` sign | **FALSIFIED AS A ROUTE** | exact complete-support undirected order-six witness has `L>S` while `L<V` | a direct cancellation in `V-L` is required |
| entropy reflection `M>=I(V;B)` at `r=2` | **OPEN** | exact identity and exact route counterexamples | would imply half density only |
| chi-square information bound `I_2(V;B)<=2` | **OPEN** | exact identity and diagnostics | would imply half density only |
| coarse rank/overlap product-Poisson certificate can prove the endpoint arithmetic inequality | **FALSIFIED AS A ROUTE** | exact five-atom Farkas law on the three-path | graph-sensitive within-rank certificate remains possible |
| a vertex-labelled bilinear pointwise correction can prove the endpoint arithmetic inequality | **FALSIFIED AS A ROUTE** | exact ten-atom Farkas law on the weighted `1:17` three-path | any surviving certificate is nonpointwise or nonlinear/higher-order |
| rank-convolution or all-`z` coverage domination proves the endpoint product | **FALSIFIED AS ROUTES** | exact order-four rational counterexamples | endpoint signs remain correct on witnesses |
| separate `1:2` orientation and batching signs prove the one-third separator | **FALSIFIED AS A ROUTE** | exact integer-weight six-cycle violates the orientation sign while the compensating batching term and full affine score retain the desired sign | any proof must keep orientation--batching cancellation |
| independent-lineage domination yields a universal fixation bound | **RETRACTED** | reproduction and another lineage's death are the same event; lower construction contradicts it | never reuse |
| exact value of `R_sim` | **OPEN; RIGOROUS LOWER BOUND `3/2`** | matching upper bound absent | preferred endpoint separator; fallback finite upper bound |
| phase-4 paper/release | **PUBLIC PREPRINT v1.0.0 AND ARCHIVAL DOI COMPLETED** | hostile-audited 18-page manuscript; all exact replays PASS; deterministic PDF SHA-256 `cfd9eb27...`; commit `db9c03ec`; public tag `simultaneous-amplification-below-three-halves-v1.0.0`; version DOI `10.5281/zenodo.21850042` | no journal submission or external outreach; universal upper theorem remains open |

Computational searches never change an `OPEN` entry.  A route counterexample
does not count as a counterexample to the endpoint theorem unless it violates
the endpoint fixation comparison itself.
