# New adversarial review of the complete PR521 publication package

**Reviewer:** package01. **Review date:** 2026-10-13 UTC / 2026-10-12 PDT. **Completion:** 100% of the assigned bounded whole-package review.

**Verdict: PASS for the precisely stated theorem and present unrefereed publication package. No unresolved mathematical, source-scope, integrity, or metadata blocker was found.** This verdict does not certify historical first priority, human peer review, or a live Zenodo deposition. The specific unrecovered 2025 Naumann habilitation remains an unresolved priority lead. One minor operational documentation improvement is listed below; it does not affect the proof or delivered artifacts.

## 1. Exact artifacts and independent review boundary

The review was against these frozen artifacts throughout:

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `publication/positivity_loss.pdf` | 72986 | `d5c31033f40afaa8dbd1f8642d7c729dfd7a858553e1c1c0856520a10f23bedd` |
| `publication/verification_package.zip` | 92065 | `4f8e60e72f9ff51125f54513426f2c7f7f96bc253e2004a0245c61e55b9e27ad` |
| `publication/positivity_loss.tex` | 13221 | `2f38b06e7243966af7afda844edc4b6672be38bb9c10759816c2cce2e4e75bfe` |
| Archive `MANIFEST.json` / outer `PACKAGE_MANIFEST.json` | recorded in `PACKAGE_CHECK.json` | `4c349fccaf933ae57495e53bcebe587e4309620046729d1578f80c92929428d8` |
| `publication/run_all.py` | 2973 | `3c7e7ce7d54b866fee6a8d248c0a5aef03d3a4c305d2355e9275803ca1ed2d16` |
| `publication/zenodo-deposit.json` | recorded in `PACKAGE_CHECK.json` | `e69ab127960d05dad12d250b57ebafd1f6b152d22eca08a81de8cb3bb31a644b` |
| `publication/zenodo_check.json` | recorded in `PACKAGE_CHECK.json` | `027722b36b63a1fc2e05f61523341d365e929fe88854935e0068f34f155bf5bc` |

All publication-file sizes/hashes before and after reproduction are in `PACKAGE_CHECK.json`. The standalone source, all four rendered paper pages, archived original proof/code/manifests, audit records, build script, README/corrections, source receipts, and local deposit metadata were examined. Prior PASS verdicts were treated as claims requiring evidence: I independently derived the mechanism and consulted the primary source clauses before accepting them. No candidate file was edited. No outside contact, other-shard communication, remote mutation, commit, or push was performed. Outputs are confined to this review directory. Copyrighted primary-source extracts and source-page renders are private scratch excluded by this directory's `.gitignore`; they must not be added to the authored publication package.

## 2. Exact claim, hypotheses, and source scope

The theorem concerns the weight on `L=O_E(2)=O(2,2)`, for `E=O_P1(1)⊕O_P1(1)` and the convention `f_*O_E(1)=E`. Both fiber measures in the defining flow are probabilities. The initial metric is smooth and strictly positive on every tangent direction of the compact product surface. The claimed actual solution has

`phi_ssbar(0,0,t) = 1/96 - (1-exp(-2t))/24`,

hence `-1/96` at `t=log(2)/2`. Fiber positivity persists. The root metric is positive on `O_E(1)` and squares to the prescribed initial metric.

I independently read the original Naumann contribution pp2440–2443 and the published article's setup and §§3.1–3.3. The report p2441 expressly moves from an induced vector-bundle metric to a general positive metric directly on `O_E(1)`; the final question p2443 concerns total-space positivity of its rank-power flow. Published pp1520–1521 identify the same initial-data category and leave positivity of `c(phi_t)` open for equation(13). Thus the construction does not evade an induced-metric requirement: none is imposed on that question.

The catalogue's narrower construction question was already answered by the source. The preprint consistently identifies the positivity-preservation question instead. One rank-two example suffices to refute universal preservation; this does not establish failure for every bundle or every initial metric. The chosen bundle already has Griffiths-positive metrics. No statement in the present paper purports to settle the Griffiths conjecture, limiting horizontal regularity, or all flow normalizations.

## 3. Flow, frames, analytic existence, and parameter derivatives

The canonical line identity has the correct determinant inverse:

`K^-1_X/S = O_E(2) ⊗ f*(det E)^-1 = O(0,2)`.

With a compatible local determinant frame and planar fiber area, `g=phi_zzbar` has fixed mass `M=2*pi`; the canonical density has mass `I=∫e^-phi dA`. Therefore the exact scalar equation is

`phi_t = log g + phi + log I - log M`.

A determinant frame change multiplies numerator and denominator of the canonical probability by the same base factor. A fiber-coordinate/frame transition transforms `g dA` and `e^-phi dA` as densities. The finite/infinity logarithmic transition weights match `O(2,2)`. Adding a fixed base function changes neither fiber probability: the equation is equivariant under that fixed addition. It does not permit an arbitrary time-dependent base adjustment while remaining the same solution. These facts resolve the most consequential possible gauge errors.

Published Naumann Theorem5, printed p1519, explicitly states existence and smoothness over the full `X×[0,infinity)`. Its proof pp1519–1520 reduces the fiberwise equation to normalized anticanonical Kähler–Ricci evolution. Theorem4 p1517 imports Berman Theorem4.1 for finite-time smooth family existence. I checked Berman's Section2C existence/stability assumptions and Theorem4.1 directly. The fibers here are smooth compact `P1`, with positive anticanonical class and positive initial fiber metrics; the base is smooth compact `P1`. The inputs apply. The automorphism-group restrictions attached to convergence assertions do not obstruct the all-time smooth existence used here. No base regularity of an infinite-time limit is imported.

The nonlocal normalization is a smooth functional of smooth weights on a compact fiber; on every finite interval it creates no derivative-under-integral problem. Smooth family dependence is included in the primary theorem, not inferred from symbolic checks. Dynamical uniqueness is also independently checkable: differences are global functions; at a fiber maximum the log-Hessian contribution is nonpositive and the log-integral difference has absolute value at most the fiber sup norm. The resulting upper Dini derivative bound `D+||v||∞≤2||v||∞` and Grönwall imply uniqueness for common initial data. This argument does not require uniqueness of all Kähler–Einstein stationary metrics modulo constants.

## 4. Global initial positivity and every boundary

Writing `E=O(1)⊗C²` gives `X=P1×P1` and `O_E(1)=O(1,1)`, which is very ample via the Segre embedding; hence the bundle is ample. The displayed logarithmic weights are standard weights and all added terms are global smooth functions. Under `s→1/s` and `z→1/z`, subtracting the stated degree-two transition weights gives smooth local expressions, including the joint infinity chart. Dividing by two gives legitimate degree-one transition weights and half the positive curvature; there is no square-root obstruction.

I independently differentiated the local weights in all four charts. The normalized diagonal coefficients and mixed squared modulus are exactly the displayed `A`, `B`, and `Q`. The delicate finite corner is `A=1/96,B=2,Q=0`, strictly positive rather than semipositive. All four projective corners pass direct local-origin tests. The same continuous frame-normalized polynomials cover every boundary edge and interior point of the closed square `0≤p,x≤1`.

The manuscript's inequalities are correct throughout that square. Their residuals are explicitly nonnegative:

- `A-A0 = delta*x² + 2*delta*p*(1-x²)`;
- `B-B0 = 2*delta*((1-p)+p*(1-x)*(1+3*x))`;
- `Q0-Q = 4*delta²*p*(1-(1-p)*x³*(1-x))`.

Here `A0=1/96+(167/48)p`, `B0=3/2`, `Q0=p/4`. The last residual is nonnegative because each of `1-p`, `x³`, and `1-x` lies in `[0,1]`. An explicit full determinant decomposition is

`AB-Q = 1/64+(159/32)p + (A-A0)*B + A0*(B-B0) + (Q0-Q)`.

All terms after the positive baseline are nonnegative. Thus the claimed continuum certificate proves strict positive definiteness in every direction, with no grid inference or hidden chart degeneration. The archived geometry verifier also reproduces its stronger Bernstein bound `AB-Q≥1/48`; the paper's weaker sufficient bound is valid.

## 5. Actual nonlinear evolution and exact sign

The base circle action lifts to the line bundle, preserves the equation and initial metric, and is retained by dynamical uniqueness. In the fixed central affine frame it forces `phi_s=phi_sbar=phi_s zbar=0` on the entire central fiber. The initial central restriction is `2log(1+|z|²)+2-epsilon`. Its normalized curvature and canonical density are the same Fubini–Study probability. Fiberwise uniqueness therefore makes that restriction stationary for every finite time.

These two exact properties close the equation for the true second base derivative. Differentiation of the nonlinear scalar equation yields `(log g)_ssbar=w_zzbar/g_F` because first derivatives of `g` vanish. Differentiating the canonical mass yields `I_s=0` and `I_ssbar=-I*mean(w)`, because the usual squared first-weight derivative term vanishes. Hence

`w_t = Delta_F w + w - mean(w)`, `w(0,x)=epsilon+delta*x²`.

Higher base jets do not enter this second derivative. This is an identity for the nonlinear solution, with smoothness supplied as above; it is not an approximate linearization. The Schur complement equals `w` on the central fiber because the mixed coefficient is zero.

I solved the polynomial coefficient system independently. The operator on `(1,x,x²)` has matrix `[[0,0,-1/3],[0,0,2],[0,0,-2]]`; putting `q=exp(-2t)` gives

`w=epsilon-delta*(1-q)/6 + delta*(1-q)*x + delta*q*x²`.

Its initial value, residual, conserved mean, and agreement with the quoted eigenmode form check exactly. The radial pushforward of the probability is uniform on `[0,1]`; the radial Laplacian and eigenvalues `-1,-3` are correct. Linear-solution uniqueness follows from mean conservation and the heat maximum principle, so the formula identifies the true jet. At `x=0,q=1/2` it is exactly `-1/96`; it crosses zero at `q=3/4`, and is negative for every `t>(log(4/3))/2`. Moreover `w_x=delta*(1-q+2qx)≥0`, so the opposite pole or an interior fiber point cannot defeat the stated central minimum. The fiber coefficient stays exactly `2/(1+|z|²)²` on this fiber. Negative curvature is therefore on the actual vector `∂/∂s`, not merely an incorrectly formed quotient.

As an additional independent check, I directly differentiated the initial nonlinear RHS, rewriting the canonical mass as `pi*exp(-B(u))*∫_0^1exp(-delta*p(u)*x²)dx`. Its pole time derivative is `-1/12`, agreeing with the exact formula. The new `check_math.py` imports none of the candidate or prior-review modules and passes40 explicit algebraic/boundary checks. This computation supplements the analytic reasoning and does not claim to prove the existence theorem.

## 6. Normalization attacks and historical claims

The stationary product weight has `c=2` at the central fiber, vanishing fiber Laplacian and Kodaira–Spencer contribution, and `(log I)_ssbar=-2`. The defining equation gives `c_t=0`, whereas a literal same-weight/time `+r*c` term at rank two gives `2`. This independently confirms the discrepancy in printed equation(14). The paper appropriately derives its special equation from defining(13), shows the calibration, and does not claim a full general correction or speculate about editorial intention.

The root/time transformation `psi=phi/r`, `tau=t/r` is coherent: `psi_tau=phi_t`, `g_phi=r*g_psi`, and the density is `exp(-r*psi)`. It produces the displayed coefficient `r` only with the simultaneous Laplacian, weight, density and time changes. Such positive scaling preserves the occurrence of a negative sign. Using a fixed unnormalized curvature-volume numerator adds a constant to the RHS and a function of time to the weight, without changing curvature. Removing the canonical integral denominator is different: the initial pole derivative becomes `epsilon>0`, not `-1/12`. The candidate does not confuse these alternatives.

Berman's Corollary4.9 is explicitly for the nonnormalized weight flow. His Remark4.11 concerns normalized Kähler–Einstein weights on effectively parametrized Fano families; it is an earlier negativity warning and bars a broad first-negativity claim. The present bundle's complex-structure family is locally isotrivial, so the remark does not supply this specific projective-space finite-time initial-metric example. Wan's curve positivity theorem evolves by a total-space Laplacian with an additional horizontal metric, a different defining equation. Demailly's v1 warning records uncertainty rather than a proof. The Cao–Guenancia–Păun example has Calabi–Yau fibers and a relative Ricci-flat limiting metric. I checked these principal distinctions directly rather than accepting the archived audit's labels.

A fresh five-query source refresh and direct university-page inspection independently reconfirmed the Naumann habilitation dated4 June2025. Its title is directly relevant; the inspected listing does not provide its mathematical contents, and no full text was recovered. I cannot exclude a precise prior result there. The existing source01 audit records76 queries and19 primary PDFs; those counts are archival claims with logged provenance, not an exhaustive novelty certificate. Neither that audit nor this bounded refresh establishes historical first priority or absence of all corrections. The paper, README and deposit description expressly disclose the unresolved lead and avoid a first-priority assertion. No currently stated theorem depends on its absence.

## 7. ZIP, reproduction, immutability, and provenance

The ZIP has40 unique members under one expected root, no unsafe paths or symlinks, and passes CRC testing. Its inventory is exactly39 manifest-hashed files plus the manifest. Every recorded size and SHA-256 matches; the archive manifest is byte-identical to the outer copy and records the frozen PDF hash. The manifest's self-exclusion convention is explicit and is backed by the separately frozen outer ZIP hash.

A genuinely fresh extraction in this review directory was checked with Python3.14.6, SymPy1.14.0 and mpmath1.3.0. Running `run_all.py` twice gave the same successful output: author40 identities, archived independent43, geometry57, and flow17. Both runs had no stderr and left every extracted file and hash unchanged. The wrapper runs the report-writing geometry/flow scripts as scratch copies and removes its temporary directory; the archived verifiers run without output-file writes. The publication tree also remained byte-identical during these runs. Runtime checks contain no network use. The pinned dependency versions agree with the README; Python3.9 compatibility is supported by the scripts' syntax/dependency requirements, but this review's executed interpreter was3.14.6.

The optimization guard was tested with `-O` and correctly refuses execution. All14 original archive files equal the **actual locally available Git blobs** at head `91385a9ba0d445a2fae4629cd60b70026584e24b`; this is stronger than relying on their archived hash claims. The original snapshot and four historical manifests independently match their respective preserved files. The five current paper/wrapper inputs match the publication originals. The source ZIP contains authored material and receipts, with no downloaded papers, full external-paper text, credentials, or private coordination records found. The original `nu/u` typo is genuinely preserved in historical proof material and clearly explained in corrections; the current TeX fixes it without altering the mathematics. No historical manifest is misleadingly claimed to hash the current rewritten manuscript.

Evidence files: `PACKAGE_CHECK.json`, `PROVENANCE_CHECK.json`, `MATH_CHECK.json`, the three new checker scripts, and the private scratch stdout/stderr receipts. Their limitations explicitly separate algebra/integrity checks from analytic and historical validation.

## 8. PDF, source, disclosure, and exact deposit metadata

All four pages were independently rendered at125dpi and visually inspected. The title, theorem, every displayed equation, coordinate definitions, inequalities, proof transition across pages2–3, normalization comparison, disclosure and references are legible. No clipping, overlap, broken glyphs, unresolved references, or missing mathematical content was found. The rendered PDF matches the current TeX's four-page argument. Embedded PDF title/author/subject identify the paper and its unrefereed AI-assisted status. The current paper's source hash agrees with its QA receipt. The critical primary Naumann pp1519–1521 and Berman pp167–168 were independently rendered and read; publisher extraction warnings did not compromise the checked displays.

The local Zenodo manifest's exact title is `Loss of total-space positivity for the normalized relative Kähler–Ricci flow`. It specifies `upload_type=publication`, `publication_type=preprint`, version1.0, date2026-10-12, English, open access, CC BY4.0, and one creator `Kriebel, Alec`, `Independent researcher`, ORCID `0009-0001-9320-500X`. The PR relation is `isDerivedFrom` and all three cited DOIs agree with the paper. Its only two files are the frozen PDF and ZIP; the companion production check has exactly matching names, sizes and hashes. Its description states the correct compact example, exact value/time, finite-time analytic input, prior-flow scope, AI use, absence of human review, and unrecovered habilitation. Metadata and file checks therefore pass locally. No live Zenodo draft, DOI assignment, remote upload, or published record was inspected or inferred from the local production label.

AI tools are disclosed as extensively used in development, writing, reproduction and adversarial review. Internal AI reviews are expressly distinguished from human peer review in PDF, README and deposit description. The archive's prior positive reviews should be read with that disclosure, not as independent human referee endorsement. The CC BY4.0 wording and deposit license agree; external-source papers are excluded.

## 9. Actionable issue and final promotion boundary

**Optional low-priority reproducibility wording:** README's rebuild command `tectonic paper/positivity_loss.tex` can put a new PDF in the verified extraction. A later `run_all.py` then correctly rejects that extra file under its strict-inventory rule. I confirmed the rejection mechanism with a review-only added PDF and restored the pristine tree. Consider directing rebuild output outside the verified extraction (for example an existing external output directory with `--outdir`), or explaining that the verification tree must remain pristine. This is a documentation convenience, not an integrity weakness, failed advertised clean run, or publication blocker.

**No mandatory repair found for the frozen theorem/package.** The strongest verified claim is the explicit compact, globally strictly positive initial metric on `O_E(2)` whose actual solution of Naumann's defining probability-normalized weight equation has exact negative horizontal coefficient `-1/96` at finite time `log(2)/2`, with fiberwise positivity. The cited smooth finite-time existence input was authenticated and its hypotheses checked; no remaining analytic gap was identified.

**Outstanding limitation:** the2025 habilitation and nonexhaustive literature search prevent certification of historical first priority or a blanket claim that nobody previously answered the precise question. That limitation is already disclosed and does not contradict the proved theorem. If promotion requires certified historical novelty rather than publication of a precise checked unrefereed theorem with this disclosure, that separate requirement is unresolved. No external input was solicited or outreach prepared.
