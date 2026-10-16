# PR946 / 6000001 first manuscript authoring record

Checkpoint: 2026-10-15T12:40:38.305830+00:00. First complete manuscript authoring is 100% of this assigned authoring task; submission readiness, source/package freezing, compilation, pixel inspection, fresh whole-package adversarial review, and authorized external operations remain root obligations. This percentage is not a novelty estimate or publication gate.

Authored files, and only these files:

- `preprint/research_note.tex`: standalone article, working/final-candidate title *Global Hessian realizations of statistical manifolds*.
- `preprint/AUTHORING_NOTES.md`: this map and limitations.

Author: Alec Kriebel, independent researcher; ORCID `0009-0001-9320-500X`. The manuscript states extensive AI involvement, unrefereed status, absence of independent human peer review and formal certification, and author responsibility. No claim of firstness, historical novelty, or present openness appears. The manuscript supplies an explicit mathematical answer to the historical question in the specified category, with the priority qualification in the abstract and a full literature-scope section.

## Proof and assumption map

| Manuscript locator | Exact content and source/check mapping |
|---|---|
| Theorem 1, opening conventions | Smooth Hausdorff second-countable fixed finite dimension, boundaryless, positive metric, ordered mutually dual torsion-free pair; `ROOT_INDEPENDENT_RECONSTRUCTION.md`, `MATHEMATICAL_GATE.json`, original `public/PROOF.md` §§1–2. No connectedness/completeness assumption. |
| `eq:difference`, `eq:Q` | Cubic sign `C=∇g`, ordered `∇=L−C♯/2`, `∇*=L+C♯/2`; `Q=∂g+Γ` is symmetric ordinary third-jet data, not a tensor. |
| `eq:feature`, `eq:rightinverse` | Proper Whitney embedding into `R^(2n+1)`, all degree≤3 monomials including constant, `N=binom(2n+4,3)`. Linear projection recovers original embedding; closed-image and compact-preimage proof. Pointwise scalar jet surjectivity uses ambient linear coordinates. Smooth adjoint right inverse requires no uniform singular-value bound. Whitney1936 Theorem1 p654/Lemma19 p665/footnote32 are declared external topology input. |
| Unbounded `q_t` example | `e(t)=(log t,0,0)` is a proper example. `q_t(log s)=t³(log s−log t)³/6` has lower derivatives zero and third derivative one at `s=t`; coefficients are smooth and unbounded. Explicitly not asserted to be the minimum-norm right inverse. Addresses the optional noncompact-lift exposition finding. |
| `eq:germ`, `eq:chartlaw` | Basis-independent exponential germ; local smooth dependence, no uniform injectivity radius or complete exponential map. Nonholonomic smooth scalar-jet section is distinguished from one global scalar function. Three second-coordinate-change terms are displayed; third coordinate-change term vanishes because gradient zero. Normal-coordinate third derivative `−C/2` and all three Levi–Civita corrections give `Q`. |
| `eq:jetidentities`–`eq:zeroform` | Hold `a(p)` fixed only in evaluation of the germ jet, then differentiate its basepoint dependence. Both ordered pair identities and the identically zero potential-compatibility one-form are proved with signs. No global injectivity of `φ` is inferred. |
| `eq:psi0`–`eq:U` | Closed Euclidean embedded image has a variable normal-addition tube. Gualtieri2017 part11 Definition3.53/Theorem3.54 pp43–44 is the explicit noncompact tubular input. `dr=P_T`, `dν=P_N`, `dΨ0=φ`, tangent Hessian columns, zero normal-normal Hessian, mixed block retained, and vanished correction first jet are explicit. Frame-independent `λ=1+tr(A⁻¹)||B||HS²` and completed square prove pointwise Schur bound `≥(2+t)I`. Positivity locus itself defines one open global domain; no uniform bound is asserted. |
| `eq:dualcoeff`–`eq:gradient` | Ambient `D*` coefficients, zero covariant Hessian of `η=dΨ`, local affine charts, torsion/curvature zero without global gradient injectivity. Exact metric and first ordered connection follow from gradient equality and pair formulas; ambient duality plus uniqueness proves the second ordered connection. |
| Corollary 2 | Both torsions are necessary by projection of the ambient torsion identities, and sufficient by Theorem1. No unmentioned “statistical” assumption is inserted into the general dual-pair criterion. |
| Final paragraph of §4 | Countable discrete zero-manifold embeds properly as a subset of nonnegative integers with `Ψ=z²/2`. Empty case vacuous. Boundary/indefinite extensions absent. |

The entire saved proof is presented, not a new proof-search mechanism. No target proof-response turn, native event, or historical author invocation has been added. The original 4/5 declaration and its absent native per-turn provenance are not reinterpreted in the paper.

## Primary-source and priority map

Read authoring inputs: complete original proof; root reconstruction and current synthesis; mathematical gate; both classical full report/comparison; complete fresh-priority-falsifier full report/comparison; recent report's material source discussions; `ROOT_AJLS2017_ACTUAL_THEOREMS.json`; root additional-primary comparisons, implication comparison, and GANITA Nash-bridge record. Source-map entries and material original primary excerpts were inspected for bibliography and conventions. This authoring pass does not claim a fresh full reading of every downloaded primary body; root/family authenticated readings remain the provenance.

| Manuscript reference/discussion | Credited result and precise boundary |
|---|---|
| Amari1997 pp84–85,87; FMU1998 p125 item1(a) | Historical question and local dual-affine, torsion/curvature interpretation. A historical listing is not current-openness evidence. |
| Lauritzen IMS1987 pp163–216 | Statistical/cubic/dual and induced-connection framework. Kept distinct from separate Lancaster1987 pair note. |
| Separate Lauritzen1987 note; Abe1994 | Exact original bodies not obtained. Pair attribution qualified through Marugame and institutional bibliography. No negative theorem about either unseen source. |
| Matumoto1993 Theorem1 pp328–331 | Compatible scalar third-order data/global contrast function, with flat embedding explicitly a further question. Name spelled Matumoto. |
| Lê MPI43/2003 pp33–39; Loi–Matta accepted2023 | Nash–Gromov/free-map/smooth minimum-norm right-inverse ancestry. Loi–Matta's already-induced hypothesis is explicit. No universal existence deduction from mere linearized surjectivity. |
| Marugame arXiv2103.10102v1 and accepted manuscript, §2.4/Theorem2.2 | Local pair/Hessian equivalence, local primitive, positive normal penalty. Preprint and accepted body are not mislabeled publisher version of record. |
| Lê early texts; final2006/final2007 | Older unrestricted claims remain visible. Missing compatibility in inspected noncompact globalization is a proof-coverage gap, not a proof the theorem is false. Final bodies remain distinct, unauthenticated, and not identified with an arXiv version. No unsupported formal erratum claim. |
| Lê arXiv v6, MainTheorem,5.1,5.6 | Actual compact finite-model theorem and revision scope. The note does not imply a noncompact finite-probability theorem. |
| AJLS2017 actual Theorem4.10 p222 and4.11 p238 | **Later material access correction is incorporated.** Actual Springer-authorized preview statements are finite-compact/countable-noncompact. Neither theorem is still described as wholly unseen. Entire chapter/p239 proof remains partial access. Root personally read primary images; see `ROOT_AJLS2017_ACTUAL_THEOREMS.json`. |
| Osipov specified preprints | Genuine global positive Hessian-cone realization for constant-statistical-curvature classes; not rejected for lacking one Euclidean global chart. No claim to validate every endpoint/corollary in those papers. |
| Entropy/simplex and properness comparison | A valid unrestricted smooth finite-simplex embedding would settle the old target with cubic sign adjustment. Removing `closure(S)\S` recovers properness in the allowed ambient category. Neither candidate properness nor stricter dimension alone is used as a firstness shield. |

The exact four core original-body gaps are stated in §5. Additional audit-coverage limits and raw source pins belong to the companion records. No literature audit is represented as exhaustive. No third-party paper, screenshot, OCR, or other copyrighted raw source was authored into this public manuscript.

## Root handoff and required downstream checks

No compilation, PDF creation marker, rendering, browser action, dependency installation, Git mutation, native queue mutation, PR mutation, Zenodo operation, or tracker update was performed by this authoring subagent. Root must compile and visually inspect every actual page, verify all final metadata against the package, and supply at least two sequential fresh whole-package adversarial reviews, resolving every required and optional issue globally before acceptance. The source assumes standard TeX packages only; the URL `%20` in the accepted Loi–Matta link is escaped for TeX. No bibliography processor or ancillary project file is needed.

The paper's verification-material paragraph is forward-facing for the companion package root is constructing: preserve original strict floating-output failures; describe a typed bounded transport comparison as a policy rather than a proved roundoff bound; do not call finite diagnostics a universal proof. If root changes the package contents or provenance, align that paragraph and all metadata before freezing.

Citation handoff check: actual primary first-page extractions confirm Marugame's exact title/author, both specified Osipov titles/authors and version markers, Matumoto's title and pages, and Loi–Matta's accepted cover/title/publication. The author-institution Lauritzen bibliography independently confirms the edited-volume title *Differential Geometry in Statistical Inference*; the actual chapter starts with its title/contents on p163 and introduction p165, explaining a 165-start variant in that bibliography. Actual Springer metadata confirms Marugame volume4 pp363–376. The inspected body and metadata locators, not recalled titles, support these citations.

Static handoff checks: 21 unique equation/theorem labels; all references resolve; 16 bibliography keys, all cited and defined; balanced unescaped braces; no raw unescaped percent. These are source checks only, not compilation or layout verification.
