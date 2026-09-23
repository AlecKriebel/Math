# Fresh adversarial preprint review — round 2

Completed: **2026-09-23T13:46:39Z**. Reviewed version: **1.0.1**.

**Verdict: preprint-ready. No actionable mathematical, scope, attribution, reproducibility, or PDF-presentation issue was found. No revision is requested.** Practical readiness of the reviewed manuscript: **100%**; completion of this bounded review: **100%**. These are completion estimates for the stated preprint review, not a probability that the proof is correct or a certificate of priority. The parent task's routine final archive refresh to include this report remains an expected staging operation.

## Independence, scope, and reviewed artifacts

I reconstructed and attacked the proof directly from `manuscript/paper.tex` before reading previous audit verdicts. In particular, I did not rely on the reported first-round pass. I then inspected the verification program and supporting materials, checked selected primary sources, reproduced the existing archives in an extracted scratch copy, and freshly rendered and inspected every page of the three-page PDF. I read the repository `AGENTS.md`; no person was contacted, no agent was spawned, and no manuscript or current package file was edited. This report is the only new non-scratch artifact produced by this review.

Reviewed SHA-256 hashes, independently measured before and after the checks:

| Artifact | SHA-256 |
|---|---|
| `manuscript/paper.tex` | `073f7e31a0037fa09ead605b5028d7c921e0188d2117734c7d1ba12a4b1ef051` |
| `output/pdf/paper.pdf` | `ff07b62aa5905544ab62b6cb04b5aa6ca528ccc61f18221fb2a0aa8c1e54f7b9` |

The exact mathematical target is the strict discriminant/gap inequality for every nonempty bounded open subset of Euclidean space, every integer dimension at least one, and every finite positive index, using form-defined Dirichlet eigenvalues counted with multiplicity. The stronger intermediate target is strict Yang inequality at every real threshold strictly above the lowest eigenvalue. The report does not assess journal acceptance or undertake a new exhaustive priority search.

## Independent proof reconstruction and attempted falsifications

### 1. Arbitrary open sets and operator domains

An enclosing box gives positivity through the Dirichlet Poincaré inequality. Zero extension embeds `H_0^1(Omega)` isometrically in the enclosing box's Sobolev space, giving compact inclusion in `L^2` and hence compact resolvent. This remains true with arbitrarily rough boundary or infinitely many connected components. A nonempty open set contains a ball, so the form domain is nontrivial and infinite dimensional. Bounded spectral intervals therefore contain only finitely many eigenfunctions, including multiplicities.

The manuscript uses the correct operator domain: functions in `H_0^1` whose distributional negative Laplacian belongs to `L^2`. It never substitutes an unjustified `H^2` boundary characterization. Bounded coordinate multiplication preserves `H_0^1`; the distributional product rule gives

\[
x_\alpha u\in\operatorname{Dom}H,\qquad
(H-E)(x_\alpha u)=-2\partial_\alpha u.
\]

The integration-by-parts normalization is also valid on arbitrary open sets. For compactly supported approximants the integral of the derivative of `x_alpha u^2` is zero, and boundedness of the coordinate permits passage to the `H^1` limit. Thus the value is exactly `||u||_2^2=1`. No classical normal derivative, boundary trace regularity, or pointwise boundary behavior is assumed.

**Attack outcome:** no missing regularity or connectedness hypothesis.

### 2. Finite spectral support lemma and circularity

The delicate step is whether the derivative may be put in the Dirichlet operator domain. The proof does this only under its contradiction hypothesis: a finite spectral expansion of `w=x_alpha u` implies `w in Dom(H^2)`, so `v=(H-E)w` belongs to `Dom(H)`. Constant-coefficient distributional differentiation then gives `(-Delta-E)v=0` inside the open set. The already-established domain membership identifies this distributional equation with `(H-E)v=0` for the self-adjoint operator. Consequently

\[
\|v\|_2^2
=\langle(H-E)w,v\rangle
=\langle w,(H-E)v\rangle=0,
\]

contradicting `⟨w,v⟩=1`. There is no inference that arbitrary eigenfunction derivatives satisfy Dirichlet boundary conditions. There is also no use of the strict Yang inequality or of the gap theorem in proving this lemma. The real eigenbasis is legitimate because the Dirichlet Laplacian is real; eigenvalue degeneracy creates no problem.

I also tried the obvious false-generalization tests. Neumann or periodic coordinates need not preserve the required operator domain, and a harmonic oscillator has a potential whose derivative changes the commutator calculation. Known equality mechanisms outside the stated class therefore do not refute the lemma. Translations merely add a multiple of the eigenfunction to `x_alpha u` and leave its finite-support obstruction unchanged.

**Attack outcome:** the finite-support obstruction is valid and noncircular.

### 3. Infinite series, cancellation, and the remainder sign

Parseval applied to `(H-E_j)x_alpha u_j` proves the second-moment identity. The first moment is absolutely summable by Cauchy–Schwarz between the second-moment series and `||x_alpha u_j||_2^2`. For a fixed lower eigenvalue, the summand used in the remainder is bounded in absolute value by a fixed linear combination of these two summable weights:

\[
\left|t_j(E_k-E_j)(E_k-z)\right|
\le t_j(E_k-E_j)^2+t_j^2|E_k-E_j|.
\]

Only finitely many lower indices and coordinates are summed. There is therefore no conditional-series rearrangement, hidden limit interchange, or infinite lower-block cancellation.

I recomputed the sign before cancellation. Subtracting the second moment multiplied by `t_j` from the first multiplied by `t_j^2` gives the weight `t_j(E_k-E_j)(z-E_k)`. The internal ordered pair `(j,k)` cancels with `(k,j)` by symmetry of the real coordinate coefficients. Terms with `E_k=z` are zero. Moving the surviving tail to the other side gives the positive weight

\[
(z-E_j)(E_k-E_j)(E_k-z)|a_{jk}^{(\alpha)}|^2
\quad(E_j<z<E_k),
\]

with the manuscript's factor `4` and dimension factor `n`. Neither a missing factor of two nor a reversed sign was found.

**Attack outcome:** the exact remainder and all its rearrangements are justified.

### 4. Strictness for every real threshold

For `z>E_1`, the ground index belongs to the finite lower block even when the ground level has multiplicity. If the nonnegative remainder were zero, every coordinate coefficient from `u_1` to every level `E_k>z` would be zero. All remaining coefficients lie in the finite-dimensional subspace at energies at most `z`, contradicting the lemma. The proof does not require `z` to be an eigenvalue, any spectral gap at `z`, ground-state positivity, or ground-state simplicity.

At `z=E_1` the lower sum is empty, so strictness would be false; the proposition correctly excludes this boundary. Repeated eigenvalues at a threshold contribute zero and do not change the reasoning.

As an additional independent model check, for an interval with energies normalized to `E_k=k^2`, the Yang deficit on the band `m^2<=z<=(m+1)^2` is

\[
F_m(z)=6z\sum_{k=1}^m k^2-5\sum_{k=1}^m k^4-mz^2.
\]

It is concave and its endpoint values are

\[
F_m(m^2)=\frac{m(m-1)(3m^2-m-1)}6,
\qquad
F_m((m+1)^2)=\frac{m(m+1)(3m^2+5m+1)}6.
\]

These independently recover positivity above `z=1`, with the required zero at the lowest threshold. Exact arithmetic checked the two formulas for 300 bands and positivity at 1,500 interior rational thresholds. This is supporting model evidence, not a substitute for the general proof.

**Attack outcome:** all-real-threshold strictness and its exact endpoint scope are correct.

### 5. Quadratic gap deduction, finite index, and multiplicity

Direct expansion gives

\[
Q(t)=t^2-2\frac{n+2}{n}A_Jt+\frac{n+4}{n}B_J
=(t-M_1)^2-D.
\]

At `E_J`, every eigenvalue below the threshold appears among the first `J`; any additional equal entries give zero summands. Thus `Q(E_J)<=0`, with equality allowed at a ground-level endpoint. At `E_(J+1)>E_1`, the same observation gives `Q(E_(J+1))<0`. It follows that `D>0`, the lower endpoint is at least the lower root, and the upper endpoint is strictly below the upper root. The nonnegative gap is strictly less than `2 sqrt(D)`; squaring is valid.

If `E_(J+1)=E_1`, all relevant eigenvalues are equal and direct calculation gives `D=4E_1^2/n^2>0`. This covers the otherwise exceptional disconnected-ground case, as well as zero gaps inside higher repeated levels through the main argument. At `J=1`, the proof correctly avoids demanding strictness of `Q(E_1)`.

**Attack outcome:** no endpoint, repeated-eigenvalue, or finite-index exception remains.

## Source normalization, contribution, and scope

I directly inspected the cached Harrell–Stubbe author source, Proposition 6(i)–(iii), and freshly rendered printed page 415 of the Oberwolfach report. The original discriminant uses the mean of squared eigenvalues. The report does visibly omit the square on `M_2` despite defining `M_p` with a `p`th root; this is not an extraction artifact. The manuscript's correction is explicit, dimensionally appropriate, and matches the original gap bound. All terms in the corrected gap inequality scale as the fourth inverse power of length. The paper does not silently claim to settle the literal misprint or the neighboring quantitative growth questions.

I also freshly rendered and inspected printed page 12 of Ashbaugh 2002. Its historical statement that strictness of Yang's first inequality was left undecided is accurately represented. The manuscript attributes the sum rules and non-strict bounds to classical work and describes its contribution as the explicit nonattainment conclusion with its equality argument. It does not claim an exhaustive priority certificate, an entirely new trace identity, formal verification, external peer review, or a uniform positive quantitative deficit.

The supporting priority audit is a bounded source/search record with explicit access and coverage limitations. Its limitations are compatible with the manuscript's wording. I did not repeat its entire literature search. The live Unsolved Math page could not be freshly retrieved in this round: the web tool could not access it, and direct retrieval returned HTTP 429. This is recorded as an access limitation, not evidence against the already documented source match. The historical primary report and original discriminant were independently checked. The manuscript's supporting-package landing page returned HTTP 200.

## Reproducibility and artifact inspection

- Read the full dependency-free verifier. Its exact rational arithmetic, finite synthetic remainder tests, certified omitted-mode bound for boxes, handling of multiplicities, and three negative controls agree with the stated scope. Synthetic finite matrices are explicitly not claimed to realize all Dirichlet sum rules.
- Ran the verifier normally and with Python optimization enabled. Both passed **7,016 exact checks across 1,312 certified box/index cases**, and both JSON outputs were byte-identical to `verification/results.json`.
- Verified all **28 entries** of the source archive's embedded SHA-256 manifest. Its manuscript, PDF, verifier, and recorded results matched the current files.
- Extracted the source archive under ignored scratch storage, ran its own verifier successfully, and confirmed the resulting JSON matched the recorded output.
- Ran `build_package.py` only in that extracted scratch copy. Both rebuilt archives — source/verification and Zenodo upload kit — were byte-identical to the current archives. The PDF compiler was not rerun; the existing PDF was freshly rendered instead.
- Reviewed the README, verifier documentation, citation metadata, Zenodo metadata, and site source for statement/scope consistency. The author name, ORCID, version 1.0.1, date, AI-assistance disclosure, licensing distinction, and lack of an invented DOI are consistent.
- Freshly rendered and visually inspected **all three PDF pages** at 130 dpi. Title, author, date/version, theorem displays, proof text, equation numbers, page numbers, footnote, references, and links are legible. No clipping, overlap, missing glyph, broken reference, or actionable pagination defect was found. PDF metadata supplies the intended title, author, subject, and keywords; the supporting-package hyperlink is present.

The provisional consolidated review and archives awaiting this report are expected staging state explicitly identified before this review. Their subsequent refresh is not a mathematical or preprint-readiness defect and does not require a further proof review if the reviewed TeX and PDF hashes remain unchanged.

## Final disposition

**No actionable issues.** The strongest verified result is the manuscript's full stated theorem, including the stronger strict Yang inequality for every real threshold above the ground energy, under exactly the stated arbitrary-bounded-open-set hypotheses. No proof gap or requested manuscript correction remains from this review. Version 1.0.1 is ready to circulate as an AI-assisted mathematical preprint with the already disclosed limits on priority and computational verification.
