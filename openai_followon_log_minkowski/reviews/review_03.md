# Fresh independent complete-package adversarial review 03

Completed 2026-10-06 21:39 PDT (2026-10-07 04:39 UTC). This is an automated mathematical and package review, not human peer review or a formal kernel certificate.

**Whole-package verdict: PASS.** I found no substantive mathematical, attribution, reproducibility, PDF, rights or package blocker in the exact final deposit identified below. The strongest supported result is the manuscript's two stated theorems, using the independently scrutinized analytic logarithmic Brunn–Minkowski input and the established existence/regularity inputs. A favorable audit is evidence, not a replacement for those proofs.

## Exact reviewed object and independence

| Object | Bytes | SHA-256 |
|---|---:|---|
| `main.tex` | 16302 | `a79834253a16ffd6258d53cde81494d812470052b4f11732636c9dcc39932f57` |
| `publication/upload-kit/paper.pdf` | 79097 | `6192382c55a3ac50ee76ce2514579a330dda1da6d873a32944a03bef26ed3179` |
| `publication/upload-kit/source-and-verification.zip` | 123632 | `fb1510e38281baffe92c176c34692e498725a61d221907435f77954bd6fc405c` |
| `publication/upload-kit/README.md` | 6229 | `386d94cd217b609a1509bc6b3015bc583e3c7470d86a999fa6cbb5dcc930dac6` |
| `zenodo-deposit.json` | 2875 | `e07287fadc017b6fd4f0a3db4853dadfbafa978fa23eb1e2934e3af77fd0ec91` |

The upstream source is the read-only `/Users/alec/Desktop/math` checkout at `adc7f1241b42e322a6451854ab7e4b4c146bf78a`. My read-only correction check still found that commit at both remote HEAD and main, with clean tracked working state. The final internal `PACKAGE_CONTENTS.json` has SHA-256 `179ca552376ecf8ccc92c445be70598fcace5eca48423274aabc2d5bb8a11614`.

Descriptive correction recorded before staging: the draft review table initially gave `main.tex` as 14731 bytes. Its measured size is **16302 bytes**, as corrected in the table above. The source SHA-256 stayed `a79834253a16ffd6258d53cde81494d812470052b4f11732636c9dcc39932f57`; no manuscript, upload file, frozen archive entry, metadata or mathematical finding changed. All three intended upload hashes were reconfirmed unchanged when this correction was recorded.

The original targets supplied for this review were: every ambient `n>=2`, every `p in [0,1)`, every strictly positive even smooth density, exactly one positive even smooth support solution with positive definite spherical curvature-radius matrix; and arbitrary full-dimensional origin-symmetric bodies with equal `L_p` surface-area measure are equal for `0<p<1`. General singular-measure uniqueness at `p=0` was expressly excluded.

I derived the follow-on arguments directly and read the raw upstream analytic sources and original external statements before inspecting the archived full-review bodies. Existing automated verdicts were not used to justify any mathematical claim. I also assigned a fresh independent upstream auditor, who read the raw analytic proof and exact premises without consulting previous follow-on opinions; its separate checker independently reproduced the tensor/variance calculation. No source or candidate manuscript was edited by these reviewers.

Scope includes the complete manuscript, ledger, theorem/status and research records, source inventories, mathematical audit notes, actual code, bibliography, README, precise intended metadata and public file set, archived reviews/responses, all five exported PDF pages, final archive entries, and the actual upstream Lean theorem's scope. This report and its evidence remain outside the frozen ZIP to avoid self-referential review hashes.

## Direct follow-on mathematical checks

**Nonsmooth Wulff first variation.** Positive continuous bounds make `W[a]` bounded and full-dimensional. At every boundary point an active half-space exists by compactness of the direction sphere. At a boundary point with a unique normal, any active constraint has that normal. Pushing forward boundary area therefore gives `h_W=a` surface-area-almost everywhere; no full support of that measure is assumed.

I independently obtained the displayed sandwich by using `h_A<=a`, `h_C<=b` and applying classical Minkowski first inequality in both orders. The upper bound follows from `nV_1(A,C)<=nV(A)+integral(b-a)dS_A`, and the lower from `nV_1(C,A)<=nV(C)-integral(b-a)dS_C`. Multiplicative support inclusions give Hausdorff convergence; weak surface-area convergence and uniform difference quotients then give the same limit. Negative parameter values reverse the bound ordering without changing that limit. Differentiating the upstream inequality at zero yields the stated logarithmic Minkowski normalization `1/n`.

**Positive-p rigidity for arbitrary bodies.** Strict Jensen for `exp(p x)` forces the support ratio to be constant only surface-area-almost everywhere. The manuscript correctly uses precisely this information to calculate classical `V_1`; it does not turn almost-everywhere equality into pointwise equality. The classical equality case supplies a positive homothety and a translation. Origin symmetry removes the translation because a bounded body cannot have two different centers. With a common prescribed measure, `V_p(K,L)=V(L)` and `V_p(L,K)=V(K)`. The mixed inequalities in both orders give equal volumes since `n-p>0`. Equality then gives `K=L`. All relevant integrals are finite because supports are positive and continuous and surface-area measures are finite.

**Smooth logarithmic endpoint.** Each prescribed smooth solution has volume `M/n`, where `M=integral f dω`, and the same cone-volume probability density `f/M`. The logarithmic mixed inequality makes both solutions global minimizers of the displayed scale-invariant functional. It also gives equal logarithmic integrals. For `q_t=h_0 exp(tw)`, positive curvature holds on a small interval around zero by openness on the compact sphere. Thus the local path is an actual smooth support path. The upstream inequality and global minimality force `V(q_t)=M/n` and minimization for sufficiently small positive `t`. Two-sided arbitrary even smooth support variations are admissible at each such path point. Stationarity yields `q_t det Q(q_t)=f`, with multiplier exactly one; even tests suffice because the discrepancy is even.

Writing `A=Q(hw)` and taking tangent dimension `m=n-1`, I rederived

```
Q(hw²)=2wA-w²Q+2h dw⊗dw,
tr(Q⁻¹A)=-w,
0=-tr((Q⁻¹A)²)-(m+2)w²+2h Q⁻¹(dw,dw).
```

The coefficient is consequently `n+1`. Similarity to the real symmetric `Q⁻¹/² A Q⁻¹/²` gives a nonnegative trace-square. Both extrema of `w` have zero gradient and hence value zero. Right differentiation is sufficient, and is justified by the smooth explicit extension of `q_t` across zero. For ambient `n=2`, the scalar trace-square is `w²`, so the extrema identity reads `0=-4w²`; there is no dimension-two exception.

I inspected actual [He–Liu v1 Theorem 4 and Section 3](https://arxiv.org/html/2510.21530v1). The theorem assumes the mixed inequality (5), with logarithmic interpretation (6). Its variational and second-derivative mechanism supports the attributed transfer. The follow-on's direct local proof avoids global Wulff-path regularity and does not rely on the source's dimension switches or omitted positive-p derivative terms.

**Existence and repaired regularity.** I read BBCY arXiv:1710.04401v2 Theorem 1.7, Proposition 7.3 and the invariant proof, including the unique fixed optimizing center, invariant deformation, Haar averaging of support tests, positive limiting multiplier and dilation exponent. Bounded positive even smooth data fit `-n<p<1`; `G={I,-I}` gives a full-dimensional symmetric body and therefore an interior origin. This conclusion does not improperly use Chou–Wang Theorem D's restricted positivity range.

I checked the original published [BBC Theorem 1.1(i),(iv)](https://link.springer.com/article/10.1007/s12220-019-00161-y) and published CW Proposition 1.2 (also compared with the author's version). Interior origin gives normal cone `{0}`, so BBC's exceptional boundary set is empty. The resulting `C1` boundary implies strict convexity of homogeneous support on affine hyperplanes avoiding zero, exactly the hypothesis needed by CW's support-chart proposition. CW then gives smoothness for smooth data. Convexity gives semidefinite `Q`, and the positive determinant makes every eigenvalue positive. The distributional circle equation separately verifies `n=2`. The repaired sentence is supported; positive bounded local Monge–Ampère density alone is not being claimed to ensure strict convexity.

**Scale, translation and endpoint counterexample.** Dilation multiplies the density/measure by `c^(n-p)`, and fixed data determine scale. Evenness fixes the center. A box facet has area `V/(2a_i)`; its `L_0` atom at each signed coordinate normal is `V/2`, and its cone-volume atom is `V/(2n)`. The distinct equal-volume boxes specified in the manuscript therefore disprove unrestricted singular endpoint uniqueness, while remaining outside the smooth positive-density class. The arguments do not silently promote the endpoint result to that larger class.

## Needed upstream analytic argument and pivotal assumptions

I read the pinned introduction, reduction, moment, identities, density, tensor and variance TeX directly. The theorem really covers all origin-symmetric convex bodies with nonempty interior in every `n>=1`, with a Wulff combination and no smoothness or unconditionality assumption.

The compact moment construction uses [Berman–Berndtsson Theorem 1.1](https://numdam.org/item/10.5802/afst.1386.pdf) on a closed ball with smooth positive `g=e^-V/Z_R` and centered barycenter. Its diffeomorphism and uniqueness up to source translation apply. [Klartag v1 Proposition 3.1 and Remark 3.5](https://arxiv.org/pdf/1309.2767v1) apply because every truncated ball is bounded, smooth and positively curved, and the density potential and its derivatives are bounded on that ball. Its Hessian lower bound is `epsilon I`, giving the upper moment-Hessian cap `4/epsilon`, independent of radius.

The supporting-plane coercivity and normalization estimates give a common integrable exponential bound. The determinant equation plus upper Hessian cap gives a positive lower Hessian bound on each fixed compact set. The smooth scalar spectral extension of logarithm is concave and uniformly elliptic. The independently checked Wang Corollary 2.3 and Schauder premises apply to already smooth truncated potentials; no arbitrary weak-solution regularity is smuggled in. Smooth local limits retain positivity, and pushforward plus tilted supporting-plane coercivity proves surjectivity rather than merely dense gradient image.

I checked the density lemma's exact cutoff expansion and the estimates proving `Ag in L2`; the harmonic/eigenvalue-one split then uses compact Hessian energy to leave only affine obstructions. Centering and evenness remove them. This is a proved density argument, not an unsupported spectral-gap assumption.

For the tensor estimate, negative weighted divergence gives exactly the vector Bochner matrix-square trace. I verified the twice-differentiated moment equation, cross-term integration by parts, and constant dual-coordinate normalization after integration by parts. At normalized Hessian, the three remaining contractions sum to

```
2||S+Sym J||²+(1/6)||J-J^(12)||²
```

plus a nonnegative symmetric `R` term. The calculation is dimension-independent and permits indefinite test Hessians. The two homogeneous Cauchy–Schwarz bounds give coefficients `q` and `q-1` with `m_i=q Eψ_i`; denominators are positive even for rank-deficient summand Hessians. The density step extends the bound to centered even `L2` functions. Gaussian domination supports differentiation and the ordered limits `q→∞`, then `epsilon→0`; decreasing finite-direction slabs containing a basis recover arbitrary bodies. No uniform lower Hessian bound on the whole space or uniform estimate through `epsilon→0` is needed. The additional fresh independent analytic checker found no gap in this same chain.

Actual Lean source definitions and final declaration `OAI.LogBrunnMinkowski.main` agree with the all-body theorem; its source SHA-256 is `bb798d24c3506422bc6ebdf064b71e3a1cf0f5f77835dd1985da2ff18a2c43a5`. Its comparator challenge is a distinct intentionally unfinished file. I did not rebuild the 24,490-line solution, extract its imported axioms, run Comparator or independently check its kernel. Lexical absence of placeholders and the repository's scope advertisement supply no formal certificate. The paper, metadata and public formal-scope excerpt accurately disclose these limits and the absence of follow-on formalization.

## Priority, attribution and public framing

Title, abstract, metadata and README accurately frame a consequence of OpenAI's newly released inequality and established reductions. They neither claim independent logarithmic Brunn–Minkowski proof nor first announcement of these uniqueness statements. OpenAI's supplied institutional authorship is retained. The upstream manuscript date is distinguished from located October 6 public repository disclosure.

I inspected the original Stancu 2018 report: Corollary 1 and its explanation announce smooth logarithmic uniqueness, and Theorem 2 announces the general logarithmic mixed inequality with flow asymptotics deferred. The publisher record for Stancu's later IMRN article distinguishes proportional from always equal centro-affine curvature. I did not obtain and certify its entire full text; no invalidity, retraction or firstness inference follows from its abstract. That caveat is explicit in the package.

My fresh search identified [Lu v3, September 28](https://arxiv.org/html/2608.20730v3). Its actual Theorem 1.4 and Corollary 1.7 still require common `n−2` pairwise orthogonal reflections in `n>=3`; the stronger equality/measure rigidity remains restricted. The lead added the accurate, expressly versioned paragraph before finalization. The original v2 history remains intact. This predecessor does not subsume unrestricted origin-symmetric targets.

I independently searched the pinned release corpus and read relevant candidates: the family 091 introduction/consequences and catalogue state volume inequalities and related measure applications, rather than this full smooth-PDE/arbitrary-positive-p-prescribed-measure package. The Petty consequence section and Mahler cone-volume equality section concern different statements; an algebraic Donovan cone-volume occurrence is unrelated. These searches are bounded evidence, not a certification that no predecessor exists. Established BLYZ/He–Liu reductions, BBCY/CW/BBC existence and regularity, and the earlier announcement remain attributed. The conservative framing is justified.

## Exact package, clean reproduction and PDF checks

The first assembled candidate ZIP had SHA-256 `df10bfeb3db51a6818f20bca558fcf2063cfed97ea726f38a4ec2e924a6ea3db`. I freshly extracted it, then separately extracted and tested the final ZIP. Final-versus-candidate comparison shows only:

1. `PACKAGE_CONTENTS.json` status becomes `final-reviewed-package`, and its inventory records the following changed file's updated size and hashes.
2. `agent_notes/priority_audit.md` gains exactly the Lu v3 paragraph independently checked above.

All other entries are byte-identical. The final ZIP has 40 regular-file entries: 39 declared payloads plus the manifest. All SHA-256/MD5/size entries and CRCs passed. There are no duplicate, absolute, traversal or symlink entries. Final `publication/build_package.py --final --check` with the recorded explicit historical review list reports `matches`; all three upload files and metadata manifest match the reviewed bytes.

From the fresh final extraction, `verification/reproduce.py --upstream /Users/alec/Desktop/math --compile --tex-engine /opt/homebrew/bin/tectonic` passed: 450 exact rational tensor cases, 200 exact endpoint identity cases, seven box cases and 28 rational scale cases; all 23 upstream source hashes; every declared archive payload; exact title, author ORCID, date, license and three upload names; standalone source and actual clean compilation. Tectonic 0.16.9 produced a fresh PDF with zero errors. A separate retained clean log has no warning, overfull, underfull or unresolved-reference marker. Rebuilt PDF timestamps/bytes differ from the publication export as disclosed; no byte-identical PDF rebuild claim is needed.

I visually inspected all five pages of the exact exported PDF at the reviewed hash. The title, author, ORCID, date, hypotheses, normalizations, all displayed equations, page breaks, corrected regularity paragraph, counterexample, disclosure and bibliography are legible, without clipping or overlap. All fonts are embedded. PDF metadata names the same author/title, and there is no JavaScript, encryption or form content.

Every public payload is owned proof/documentation/code or metadata identifying external sources. The ZIP excludes third-party PDFs/source copies, cloned dependencies, caches, build products, render trees, credentials and unrelated incident material. Manual inspection and credential-pattern scanning found no secrets. Downloaded primary copies used for this review remain in ignored reviewer-only `.txt`/`.pdf` paths. The CC BY 4.0 declaration is explicitly for the owned contribution. Archived prior reviews and responses are dated, hash-specific provenance, not silent certificates for newer ZIPs. The public formal-scope excerpt retains the substantive build/axiom limitations. Code only performs the advertised local computations/build/hash work; finite cases are consistently distinguished from universal proofs.

Review evidence: `review_03_candidate_inventory.json`, `review_03_candidate_reproduction.json`, `review_03_final_inventory.json`, `review_03_final_reproduction.json`, `review_03_pdf_and_exclusions.json`, `review_03_source_and_clean_compile.json`, and the closing `review_03_final_receipt.json`.

## Final limits and release gate

No material unresolved concern remains in this reviewed mathematical/publication package. Independent Lean kernel/axiom/Comparator reproduction is incomplete, the full Stancu 2022 relationship is not certified, and there has been no conventional human peer review; all are accurately disclosed. This review does not establish Zenodo staging/publication, assigned DOI, DOI resolution, spreadsheet/tracker insertion or external production read-back. It authorizes no communication with individuals and performed none. No Git mutation, candidate edit, external publication or upstream write was performed by this reviewer.

Audit-task completion estimate: **100%**. This is an estimate of the assigned review's completion, not a probability of theorem correctness or a statement that publication is complete. Any later payload, manuscript, PDF, metadata or upload change requires appropriate rechecking of the changed exact bytes.
