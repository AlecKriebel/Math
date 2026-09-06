# Feedback disposition

## Independent full referee report — 5 September 2026

| Referee item | Disposition | Action |
|---|---|---|
| R1: modulus readers accept unlisted or duplicate monomials | ACCEPT | Reproduced the false acceptance, then enforced raw/declared/regenerated row counts, exponent arity and uniqueness, exact support, and exact coefficients in every reader and the generator. Added additions, omissions, identical duplicates, and conflicting duplicates in both orders as negative controls. Unknown descriptive metadata remains outside the polynomial claim. |
| R2: stacked fractions overlap in the 77/84-term tables | ACCEPT, BROADEN | Found the same defect throughout all four modulus tables. Printed exact rationals in single-line notation and added an objective 218-row bounding-box audit with a one-point minimum-clearance threshold. |
| R3: two determinant-proof sentences are inaccurate | ACCEPT | Replaced the false cycle-cover count with the existing Schur-complement calculation and stated the correct right-fragment/triad/left-fragment Frobenius order. Exact determinant formulas are unchanged. |
| R4: near-threshold cubic is hard-coded and onset is not certified | ACCEPT | Independently reconstructed the example from the reaction list. The verifier now derives the Hessian, $w_0$, $w_2$, left vector, cubic, transversality, simple zero, stable complement, and all $t>1$ modes exactly. The supplement states the fixed-$\varepsilon$, $m=3$ scope. |
| R5: v1.0.9 reference and declarations are unfinished | ACCEPT | The author confirmed no specific funding, no competing interests, and no other journal submission. Those facts replace every active placeholder; immutable release publication follows final qualification. |
| R6: Conradi et al. nonlinear numerics are omitted | ACCEPT | Verified the primary arXiv source and now records its numerical continuation and stable patterned-branch segments while distinguishing the present all-dimensional exact results. |
| Optional: clarify Turing convention | ACCEPT | Defined the paper's usage as a stationary nonconstant Neumann-mode crossing on a fixed interval and disclaimed intrinsic wavelength selection under domain enlargement. |
| Optional: scalar minimax is “equivalent” to the full frontier | ACCEPT | Replaced the false logical equivalence with “and, in particular,” so the two open problems remain distinct. |
| Optional: say “restricted well-mixed Jacobian” | ALREADY SATISFIED | The theorem already identifies the homogeneous mode as the well-mixed Jacobian restricted to $c^\perp$; no duplicate wording was added. |

## Independent submission rereview of v1.0.8 — 23 August 2026

| Rereview item | Disposition | Action |
|---|---|---|
| R1: top-level manifest contains 570 absent ignored scratch paths | ACCEPT | Replaced unrestricted `find` with sorted NUL-safe `git ls-files`, excluded only the manifest itself, and added a fresh-archive file-count and hash check. |
| R2: `FORMAT` and `LATEX` lock rows are not enforced | ACCEPT | The checker now skips only the separately banner-checked engine and Biber rows. All four special fields have impossible-value negative controls. |
| R3: two detached supplement passes accept stale TOC pages | ACCEPT | Detached builds now iterate until `.aux` and `.toc` stabilize and compare extracted main and supplement text with the canonical PDFs. |
| M1: one supplementary `\Delta` should read `\Delta_m` | REJECT AS CONTEXT-INCOMPLETE; CLARIFY | The supplement consistently defined and used a local `\Delta`; changing only the cited occurrence would create inconsistency. The definition now explicitly reads `\Delta:=\Delta_m`, making the intended improved profile unambiguous. |
| S1: SIADS bundle lacks review presentation items | ACCEPT | Added a separate 11-point main/10-point supplement review mode with a 6-by-8-inch text area and line numbers, visible keywords/MSC codes, a supplementary index, and a generated PDF cover letter. |
| S2: v1.0.8 DOI and declarations are stale or pending | ACCEPT WITH VERSION QUALIFICATION | Active files target distinct v1.0.9, cite concept DOI `10.5281/zenodo.21753404` and exact predecessor DOI `10.5281/zenodo.22074358`, and include the SIAM responsibility sentence. No v1.0.9 version DOI is asserted before minting; author-only funding, competing-interest, and exclusivity statements remain explicit pre-upload confirmations. |

The rereview independently classified the central mathematical result as
valid. These edits affect reproducibility, presentation, and metadata only.

## Independent journal-style referee audit — 23 August 2026

| Referee item | Disposition | Action |
|---|---|---|
| D1: replay fails a brittle PDF extraction probe and the document stack is not pinned | ACCEPT | Made the Latin-$u$ and positive-diagonal probes extractor-robust; pinned CPython, the scientific stack, TinyTeX 2022.04, pdfTeX 1.40.24, Biber 2.17, and load-bearing TeX packages; rebuilt every active PDF with the one enforced producer. |
| D2: 21 direct verifier entrypoints can run without assertions | ACCEPT | Added fail-closed guards to all 38 prior entrypoints and the new generic checker.  A dynamic test runs all 39 under `python -O` and requires rejection. |
| D3: some evidence described as all-dimensional or independent is finite, duplicated, floating, or aggregate | ACCEPT | Added a standalone symbolic recurrence-to-$R_m+C_m\mathfrak h_m$ bridge and documented the exact evidentiary role of every layer.  All 39 entrypoints were also run individually. |
| D4: replay rewrites the downloaded manifest and can self-certify a changed tree | ACCEPT | The shipped manifest is verified before generation and never rewritten; exact artifacts are checked against selected downloaded hashes, and a separately named regenerated-tree manifest is explicitly labeled self-consistency only.  Detached mutation controls reject changes under both manifests. |
| D5: fixed-mass Fredholm and sectorial steps are too compressed | ACCEPT | Printed the zero/nonzero Fourier blocks, exact range/kernel/cokernel, $O(k^{-2})$ inverse estimate, fixed-mass invariance, sectorial compact-resolvent setting, and finite-low-mode spectral-gap continuation. |
| D6: stored $m=200$/stale-tree/schema/DOI provenance can be mistaken for current output | ACCEPT WITH CLASSIFICATION | Restored $m=200$ to current integrated coverage, removed the redundant stale numerical sidecar, regenerated stale audits in their own scopes, added command/version/evidence-class provenance, labeled the schema descriptive, and recorded v1.0.7 DOI `10.5281/zenodo.22062080` as the exact predecessor. |
| State that the $b=2a$ edge belongs to neither long cycle | ACCEPT OPTIONAL | Added the statement to the manuscript, supplement, theorem summary, proof skeleton, and proof audit. |
| Print the $3\times3$ determinant remainder | ACCEPT OPTIONAL | Printed the distinct core matrix $B_m^{\rm core}$ and verified $\det B_m^{\rm core}=2a^2b$, including the empty-interior $m=3$ case. |

The referee found no mathematical defect and classified the result as valid
after minor corrections.  None of these accepted items changes the reaction
topology, theorem domain, repaired endpoint, numerical profile, or nonlinear
conclusion.

## Final adversarial review — 22 August 2026

| Supplied review item | Disposition | Action |
|---|---|---|
| Explicitly close positivity of both patterned branches | ACCEPT | Added the $H_N^2\hookrightarrow C^0$ closure for each fixed parameter choice and stated that positive diagonal physical rescaling preserves componentwise positivity. |
| “$L$ reduces the maximum” is ambiguous or false within the family | ACCEPT | Exact comparison gives $\chi_D(L)>\chi_H(L)$ throughout the certified interval; the maximum is $\chi_D(L)$, is strictly increasing, and is uniquely minimized at $L_0$.  The manuscript, supplement, summaries, and regressions now state this precisely. |
| Theorem 5.2 does not quantify $D$ | ACCEPT | Declared $D=\operatorname{diag}(d_1,\ldots,d_m,d_Z)\succ0$ in the theorem itself and propagated the domain to the proof-audit interfaces. |
| “Nontrivial SCC” includes a negative singleton | ACCEPT OPTIONAL CLEANUP | Recast the classification as negative singletons plus three non-singleton block forms. |
| Add exact v1.0.6 DOI to the current source metadata | ACCEPT WITH VERSION QUALIFICATION | Verified `10.5281/zenodo.22058969` as the exact immutable v1.0.6 DOI and recorded it as the preceding snapshot.  Because the accepted edits produce different files, they target v1.0.7 and do not misassign the v1.0.6 DOI to the new tree.  The concept DOI remains `10.5281/zenodo.21753404`; v1.0.7's exact DOI belongs in its release record after minting. |

## Fresh adversarial review — 22 August 2026

| Supplied review item | Disposition | Action |
|---|---|---|
| $r_m$ and $\ell_m$ denote both components and full vectors | ACCEPT | Reserved those symbols for the $X_m$ components and explicitly defined $r=(r_1,\ldots,r_m,r_Z)^T$ and $\ell=(\ell_1,\ldots,\ell_m,\ell_Z)^T$ for the full critical vectors, including the transformed vector $\widetilde\ell(L)$.  The final adversarial audit also replaced a residual dimension-offset $r$ by $\nu$ in the machine-readable certificate. |
| Theorem 7.1 does not state the PDE setting in the theorem | ACCEPT | Added $(0,\pi)$, homogeneous Neumann conditions, and physical diffusion $(1-\mu)D_m^{\rm phys}(L)$ to the statement. |
| The physical fixed-mass object is called a vector | ACCEPT | Replaced “vector” with “covector.” |
| Supplement S9 reuses $t$ as an affine-design parameter | ACCEPT | Renamed that local parameter $\omega$, including its base value $\omega=2/9$; $\tau_m(L)$ remains reserved for the zero-mode gauge. |
| The scaled cubic sign omits the displayed quotient | ACCEPT | Printed $c_m(L)=N_m(L)/(\widetilde\ell(L)^Tr)$ before the sign conclusion. |
| The release URL or Zenodo concept DOI may be private or merely reserved | REJECT AS STALE | Logged-out HTTP checks and the public APIs confirm that v1.0.5 is released, both GitHub links resolve, the concept DOI is Findable and open, and version DOI `10.5281/zenodo.22050742` is published.  The accepted source edits therefore target a new v1.0.6 tag. |

## Fresh adversarial review — 21 August 2026

| Supplied review item | Disposition | Action |
|---|---|---|
| Threshold written as $s_*(H,D)$ although its location depends on $a,b$ | ACCEPT | Replaced it by $s_*(a,b,H,D)$, including the mode band and ray-scaling identity; added an exact $m=3$ dependence regression. |
| The 77-term certificate does not by itself prove multiplicity one at zero | ACCEPT | Printed and verified the exact all-dimensional characteristic derivative and its equality to $-(163/45)\ell^Tr>0$. |
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
