# Independent priority audit: logarithmic assemblies and Gamma marking

Audit sealed independently on 2026-10-15. Scope: PR218 / problem 30006020. Mathematical/source-validity gates were supplied as separate PASS gates and were not inherited as a novelty conclusion. No sibling priority lane, old review, or root priority report was consulted. All downloaded third-party material and OCR are in ignored `private/`; only authored audit files are in the public manifest.

## Finding

**The composition model and the unmarked mesoscopic Poisson mechanism have definite prior coverage. This lane does not establish that the full geometric claim was already proved. Full novelty remains unresolved.**

The most concrete overlap is stronger than a general resemblance to Ewens theory: the candidate's composition law is exactly the weighted permutation law `P_{n,∞,1/2}` introduced in DGZZ, with `θ_j=ζ(2j)/2` and `n=3g-3`. DGZZ Lemma 3.6 explicitly supplies the ordered composition/exponential-formula representation. The candidate should credit this exact model, as well as DGZZ's cylinder-count estimates. [DGZZ final primary paper](https://webusers.imj-prg.fr/~anton.zorich/Papers/Large_Genus_Asymptotic_Geometry_2022_Inventiones_published.pdf).

The strongest located general theorem is ABT 2000, Theorem 3.1: every initial segment of component counts through `b_n=o(n)` is asymptotically independent Poisson in total variation. Its hypotheses hold here with parameter `1/2`; hence the unmarked local PPP on every scale `q_n→∞`, `q_n=o(n)` is already an immediate corollary. AT 1994 Lemma 5 is exactly the factorial-moment identity used in the candidate. [ABT full primary paper](https://www.columbia.edu/cu/simontavare/STpapers-pdf/ABT00.pdf), [AT full primary paper](https://www.columbia.edu/cu/simontavare/STpapers-pdf/AT94.pdf).

A complete checked deduction for the Gamma-marked and normalized analytic model is in `PARAMETER_COMPARISON.md`. It uses ABT plus ordinary marking, an explicit intensity sum, Gamma tails and AT moments. That deduction demonstrates how little independent analytic machinery is needed, but it is labelled an auditor deduction: I did not find a full primary theorem already stating this exact marked mixture with all count moments. No located assembly paper proves the geometric identification of its parts with cylinder areas.

## Positive coverage matrix

Legend: **Exact** = a verified earlier theorem/formula covers the same claim; **Corollary** = the parameter substitution and additional deduction are written out in the companion comparison; **Input** = prior result supplies a needed ingredient but not the claimed conclusion; **No** = no coverage established.

| Candidate component | Prior primary result | Coverage | Exact remaining issue |
|---|---|---|---|
| Ordered composition weights `∏ζ(2j_i)/(2j_i)/(h_n k!)` | DGZZ (2022), eqs.(1.7)–(1.8), Lemma 3.6 / eqs.(3.20)–(3.23) | **Exact** | No novelty in the discrete law itself. |
| Conditioning representation by independent Poisson `Z_j` | AT (1994), general conditioning framework; ABT (2000), CR | **Exact** | No integer combinatorial interpretation is needed. |
| Unmarked compact-window local PPP, every `q→∞`, `q=o(n)` | ABT (2000), Theorem 3.1; intensity Riemann sums | **Corollary**, full rate range | No missing slow-growth range. |
| Unmarked all fixed joint count moments | AT (1994), Lemma 5 / (126); coefficient ratio | **Corollary**, full rate range | Not justified merely by TV. |
| Gamma(2j) marked analytic PPP and all fixed joint moments | ABT/AT + explicit kernel calculation in companion file | **Checked deduction**, no exact earlier marked theorem located | Need marking/tail/normalization argument; it is short but distinct from citing an existing theorem. |
| Entire geometric area multiset TV-close to the marked model (Theorem A) | DL (online 2024; issue 2025), Theorem 1.4, 3.2, 4.1, (6.1), Lemma 6.4; DGZZ graph/count estimates | **Input**, very close to a direct distributional corollary | Uniform latent density comparison, normalization across `k`, and negligible exceptional graphs still must be assembled. No located prior statement explicitly gives this full area-multiset TV model. |
| Geometric mesoscopic PPP, all fixed joint moments | Above analytic results plus the bridge and geometric uniform integrability | **No full prior coverage established** | Precisely the cylinder-area transfer. |
| Requested `[g^-1/2,2g^-1/2]` law `Po(log 2/2)` | Unmarked theorem supplies the analytic constant after mapping `q=(3g-3)/sqrt(g)` | **Analytic corollary**, geometric claim not located | Same geometric bridge and moment transfer. |

## The geometric overlap is substantial but should be described accurately

DL's Theorem 4.1 proof already reduces the exact geometric law to a conditional one-vertex mixture by discarding an event of probability tending to zero; that reasoning gives a TV comparison to its exact restricted mixture. Its monomial expansion and uniform correlator estimate, and its proof of Theorem 6.3, already display the `ζ(2j)/(2j)` composition sum. A positive monomial simplex density is a Dirichlet mixture. Thus Theorem A is strongly supported as a short strengthening/repackaging of published inputs. This is a more precise criticism of the novelty pitch than saying “Poisson–Dirichlet limits are well known.” [DL full final paper](https://ems.press/content/serial-article-files/51451?nt=1).

Nevertheless, the exact claims in those theorems concern fixed-genus law formulas, graph concentration and macroscopic limits. An explicit uniform whole-law assembly comparison and the geometric moment transfer were not found as prior statements. A new corollary can still be a contribution, especially when it resolves a separately stated open problem. This lane therefore does not turn the shortness of the derivation into a positive assertion of full anticipation.

The source report, from the 8–13 September 2024 workshop, explicitly asks about intermediate areas after citing the microscopic and macroscopic laws. Its reference [5], *Small components of random multicurves on large genus hyperbolic surfaces*, is “in preparation.” The microscopic intensity matches the independent Gamma-marked assembly calculation, but a fixed microscopic limit does not control windows escaping to infinity. [Full OWR report, p.2387](https://publications.mfo.de/bitstream/handle/mfo/4255/OWR_2024_41.pdf?isAllowed=y&sequence=1).

## Other approached source families and their precise limits

- AST 1995 Theorem 3 fits the analytic generating function but its quantitative range is `b=o(n/log n)`. Its fixed-coordinate moment theorem is not a moving-window moment theorem. ABT 2000 is the stronger route for the full range.
- Zhao 2012, Theorems 4.2 and 1.1, applies through the summable ULC and the perturbation `η(c)=∏ζ(2j)^{c_j}`. Smooth compactly supported statistics at scale `q` satisfy the Feller insensitivity test, with error `O(d/q)` after changing the first `d` Bernoulli variables. Indicator window counts fail the theorem's uniform continuity test at the endpoints; smooth approximation or ABT is needed. The theorem also has no random Gamma marking or moment conclusion.
- Nikeghbali–Storm–Zeindler 2013 fits the generating-function class with `(r,ϑ,K)=(1,1/2,(log 2)/2)`. The increasing-window theorem 3.3 requires `n/d_n` to dominate every fixed multiple of `log n`; it does not cover all `d_n=o(n)`. It is not the strongest all-rate citation here.
- ABT 1999a identifies the limiting PD process with a conditioned scale-invariant PPP and gives a small-coordinate TV formula. ABT 1999b treats largest components. Neither statement alone supplies a shrinking-window result for the finite geometric laws.
- ABT's 2006 coupling gives an order `log n/n` global `l1` approximation to PD under Ewens. Such a bound alone loses control when divided by `s=q/n` and `q` grows slower than `log n`. It is not an all-rate substitute for local component control.
- Bahier–Najnudel (online 2021; issue 2022), Theorem 1.1, has every-rate mesoscopic scale-invariant PPP functionals for Ewens permutation eigenvalues, including the conditions `δ_n→0`, `nδ_n→∞`. Those observables differ from Gamma-marked cycle areas; no geometric bridge is present.
- Storm–Zeindler's polynomially growing weight model has a different hypothesis regime from the bounded weights `ζ(2j)/2`; its conclusions cannot be invoked merely because the paper title mentions TV.

Full primary PDFs were downloaded for these families except the two expressly unavailable leads below. No theorem claim is based only on a search snippet.

## Chronology and outstanding leads

Key chronological pins: AT printed 1 March 1994; AST printed July 1995; ABT99a/b printed 1999; ABT00 printed 2000; ABT monograph official publication 15 December 2003; three-couplings author revision 7 June 2005 / journal 2006; Zhao v1 5 May 2011 and v2 23 April 2012; weighted-large paper v1 24 February 2013; Bahier–Najnudel published online 11 August 2021. DGZZ v1 9 July 2020, final journal online 20 June 2022, v2 5 July 2022. DL arXiv v1 21 February 2022, journal accepted 26 February 2024, published online 7 June 2024, volume 27 (2025). The retrieved arXiv page lists only DL v1, so final theorem numbering was taken from the publisher PDF, not assumed to match the arXiv version.

The official ABT monograph download requires a subscription; its preface and contents were available, but I did not use unverified book theorem numbering from third-party snippets. Hirth 1997's primary Euclid endpoint returned a blocked HTML payload; its title concerns Dirichlet/GEM counts, but without the full theorem it is an unresolved lead, not positive coverage. The ABT92 primary Euclid endpoint was similarly inaccessible; the stronger ABT00 full theorem was available. The in-preparation DL small-components manuscript was not located by the exact-title/current-date searches in this lane. No outreach was prepared or initiated.

Search coverage is through the audit date 2026-10-15, not a claim of exhaustive literature coverage. The missing small-components manuscript is the most relevant unavailable lead; an eventual full primary version could materially change the priority conclusion.

## Recommended priority disposition

Record **exact prior overlap for the discrete model and direct prior-theorem coverage for the unmarked every-scale analytic law**. Record the marked analytic result as a straightforward checked extension of that literature. Do not record a full novelty FAIL from this lane: no located prior complete theorem covers the original geometric mesoscopic problem and all-moment transfer. Do not record a novelty PASS either: Theorem A is extremely close to the published geometric expansions, and the unavailable small-components work must remain explicit. The most defensible potential contribution is the uniform distributional bridge and its use to resolve the stated geometric intermediate-area question.
