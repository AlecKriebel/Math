# Feedback disposition

## Fresh adversarial review — 21 August 2026

| Supplied review item | Disposition | Action |
|---|---|---|
| Threshold written as $s_*(H,D)$ although its location depends on $a,b$ | ACCEPT | Replaced it by $s_*(a,b,H,D)$, including the mode band and ray-scaling identity; added an exact $m=3$ dependence regression. |
| The 77-term certificate does not by itself prove multiplicity one at zero | ACCEPT | Printed and verified the exact all-dimensional characteristic derivative and its equality to $-(163/45)\ell_m^Tr_m>0$. |
| Row scaling needs an explicit algebraic-simplicity argument | ACCEPT | Printed the unchanged kernel, transformed left vector, and generalized-vector contradiction. |
| The network application leaves the last matrix-theorem hypothesis implicit | ACCEPT | Derived rank $n-1$, the simple conservation zero, and the positive order-$(n-1)$ coefficient from homogeneous stability. |
| The general matrix theorem should state $n\ge2$ | ACCEPT | Added the domain restriction; all applications already have $n\ge4$. |
| The Crandall--Rabinowitz interface is implicit | ACCEPT | Printed the fixed-mass domain/codomain, Fredholm index, kernel, cokernel, and exact transversality pairing. |
| The full Jacobian image is described as two-parameter | ACCEPT | Separated the two-flux factor $A_m(a,b)$ from arbitrary positive right-diagonal scaling $H$. |
| Supplement S9 has a comma splice | ACCEPT | Replaced it with a complete sentence. |
| GitHub release and Zenodo DOI are unresolved | REJECT AS STALE | The public v1.0.4 release and both the concept and version DOIs resolve; no reserved-DOI qualification is needed. |

## Fresh adversarial review — 20 August 2026

| Supplied review item | Disposition | Action |
|---|---|---|
| S9 prints $\nu$ instead of Latin $u$ | REJECT AS STALE | Current source, v1.0.3 source, and rendered PDF already use Latin $u$. Added a regression forbidding the alleged typo. |
| S9 omits the affine critical vector and induced diffusion profile | ACCEPT | Printed $r^{\rm aff}$, all five diffusion formulas, and $(A_m-D)r^{\rm aff}=0$; added exact reconstruction tests. |
| Scaled-family transversality numerator is implicit | ACCEPT | Printed $\widetilde\ell^T\mathsf H\Delta r=\ell^T\Delta r<0$ and the positive quotient for $\eta_m(L)$. |
| Localization minimum includes a formally undefined empty block | ACCEPT | Restricted the minimum to $\varnothing\ne I\subseteq[n]$ in the theorem and proof summaries. |
| Publish a new immutable snapshot | ACCEPT | Prepared v1.0.4 metadata and the stable Zenodo concept DOI; release publication follows final replay and audit closure. |

| Requirement or prior criticism | Disposition | Final action |
|---|---|---|
| One central all-spectrum topology | APPLY | No competing old family appears in the title, abstract, or theorem suite. |
| Exact diffusion design | APPLY | General principal-minor diffusion-ray theorem, network one-bad-minor corollary, omission table, criterion, and threshold band are integrated. |
| Asymptotic/heterogeneity transparency | APPLY | Sharp linear bounds, improved unit contrast, product lower bound, and square-root endpoint are explicit. |
| Do not overclaim the Pareto frontier | APPLY | Only exponent optimality is claimed; constants remain open. |
| Semipositive terminology | REQUIRES REPAIR | All “conservative network” language was removed or replaced by codimension-one semipositive conservation. |
| Main-text proof sufficiency | APPLY | SCC exhaustion, one-bad-minor proof, omission table, certificate architecture, normal form, and exchange of stability are visible in the main text. |
| Certificate visibility | APPLY | Full 14/22/35/77/84-term tables and commands are in the supplement and public verifier. |
| Precise stability meaning | APPLY | Local exponential asymptotic stability is stated in fixed-mass $H^1$ with hypotheses. |
| Local well-posedness and positivity | APPLY | Quasi-positivity, local semilinear theory, and the local-in-phase-space forward-global conclusion are stated. |
| Robustness or removal | APPLY | A retuned codimension-one theorem is retained; no uniform radius is claimed. |
| Near-threshold behavior | APPLY | The rigorous subcritical $m=3$ control path is supplementary; no universal nonlinear gap is inferred. |
| Exact literature distinction | APPLY | Fixed-J, projected-injectivity, parameter-rich core, atlas, and mass-action scopes are separated. |
| Cross-reference and DOI audit | APPLY | Literal and automated audits completed; correction notice included. |
| Old minimum-reaction and reaction-minimal claims | REMOVED | They belong to a different full-rank topology. |
| Superseded high-contrast diffusion profile | REMOVED | Superseded by the improved unit profile and stable trade-off family. |
| Projected-injectivity sharpness | NOT APPLICABLE | Not implied and not claimed. |
| T-ALG integration | REMOVED | No private complexity result enters the paper. |

| Stale current-profile numerical table | REPAIRED | All finite values now derive from `data/current_profile_exact.json`; old-profile mutations fail. |

## Pre-submission adversarial review — 16 August 2026

| Supplied review item | Disposition | Action |
|---|---|---|
| `Theorem 3.1` should be `Lemma 3.1` | ACCEPT | Replaced the mixed-counter `cleveref` output with an explicit lemma reference and added source/PDF semantic gates. |
| `Theorems 4.1 and 5.1` mixes a theorem and proposition | ACCEPT | Replaced it with explicit theorem and proposition references and added a PDF-text regression. |
| Figure 1 says “shaded” although the set is outlined | ACCEPT | Caption now describes the dashed outline. |
| Scalar pencil-root simplicity implies ordinary eigenvalue simplicity | ACCEPT OBJECTION | Removed the invalid implication; ordinary simplicity now follows from the already-proved characteristic-polynomial derivative. |
| Top-level replay is portable without historical inputs | ACCEPT QUALIFICATION | The five frozen lineage archives are explicit prerequisites; the public replay remains self-contained. |
| Two code docstrings call the family conservative | ACCEPT | Replaced with codimension-one/semipositive terminology. |
| Improve Figure 2 grayscale robustness | ACCEPT | Stable curves, lower bounds, and endpoint markers now share dimension colors and use distinct markers/dotted bounds. |
| No further theorem work is warranted | REJECT | Independent determinant reconstruction found that the old scaled-family endpoint is homogeneously unstable at `m=149`. The invalid 34-term certificate was replaced by an exact 22-term certificate and a narrower endpoint that preserves the square-root theorem. |
| Recreated archive is byte-identical to the lost release | NOT CLAIMED | Release documentation describes a recreated corrected release and regenerates a current project manifest and canonical bundle hashes after rebuilding. |

Additional independent findings applied in the same pass include the corrected
14-term boundary-triad display, the missing `m=3` homogeneous-stability base
case, a definition of `chi_stable`, S-prefixed supplement numbering, a runnable
verifier command, a corrected Figure 2 endpoint caption, and a close-literature
comparison with Haas--Goldstein (2021).
