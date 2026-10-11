# PR370: independent definitions, normalization and geometric-asymptotics audit

**Verdict: PASS for the frozen claims, with their two source scopes preserved. No mandatory mathematical or reproduction fix identified.** This audit concerns head `567c2e493854b32d0cd325ad96e4c5b69c9c1e1b`, base `efd29c05204703acca9a0860812f54b94fae54b1`, and the 18 files for problem 30004811 plus its QUEUE row. Audit completion estimate: 100%; this is completion of the assigned audit, not a historical novelty certification or evaluation of the exact global capacity-volume mass.

The candidate proves a counterexample to the unrestricted all-AF reading, not to the globally nonnegative scalar curvature conjecture in Jauregui's full paper. The latter equality is already a consequence of credited prior theorems. Both claims survive independent source-first review and independent analytical derivation.

## Independence and frozen inputs

Seven primary PDFs were independently fetched from the allowed URLs, and all SHA-256 hashes and byte lengths match the source routing manifest. Raw PDFs, extracted text and the copied replay bundle remain in ignored `private/`. `SOURCE_FIRST_BASELINE.md` was sealed before candidate mathematics; its SHA-256 is `40d1ee281889781f4ea5e1712ee72d236a1954e4bc7a6410dc86366d1935d3cd`. `INDEPENDENT_MATHEMATICAL_VERDICT.md` was sealed after reading SOURCE_GATE, TURN_1 and PRIOR_RESOLUTION, but before all verifier code, recorded outputs, final/status documents and reviews; its SHA-256 is `5098f7fbf2c3d35a471ce9cf105fb224510cf17b0432e4620b8d281d2c8fa49c`. Both seals were revalidated at the end. No sibling findings were consulted.

The snapshot's 19 inputs were checked against byte length, SHA-256 and Git blob hash in `snapshot_manifest.json`. All agree. The target QUEUE row says `already_solved`, `1/5`; publication prose keeps the historical pending-review snapshots distinct from the superseding reviewed publication status.

## Exact target and prior result coverage

The source mass is

\[
 c_g(K)=\frac1{4\pi}\inf\int_M|\nabla\phi|_g^2\,dV_g,\qquad
 m_{CV}=\sup_{\{K_j\}}\limsup_j\left[\left(\frac{3|K_j|_g}{4\pi}\right)^{1/3}-c_g(K_j)\right].
\]

Here \(\phi=0\) on \(K\) and tends to one at infinity, and the supremum is over compact exhaustions. Euclidean balls have capacity equal to radius. The OWR prose's absent energy prefactor cannot be used to change the question: its own inequality/examples and the full paper explicitly fix the normalized convention. Jauregui Lemma 10 establishes equivalence with the cubic deficit after an exhaustion-level near-optimal reduction; it is not a pointwise identity between the two local quantities.

The original full paper's intended class is smooth, complete, connected and one-ended, with two-derivative AF decay of order \(\tau>1/2\), integrable scalar curvature, globally nonnegative scalar curvature and empty/minimal compact boundary. The candidate's standard-class chain

\[
 m_{ADM}\le m_{CV}\le m_{iso}=m_{ADM}
\]

is valid under these assumptions. Jauregui Theorem 5 supplies the first inequality; BFM Theorem 5.6 at \(p=2\) supplies the middle comparison; the known isoperimetric/ADM equality supplies the last. The \(p=2\) normalization and exhaustion-supremum conversion are correct. Smooth outer approximations with arbitrarily small capacity error suffice for arbitrary compact sets, as also supplied by Jauregui Lemma 12.

BFM Theorem 1.3 does have an additional \(H_2(M,\partial M;\mathbb Z)=0\) assumption. The candidate does not discard it; it instead uses the separately stated comparison Theorem 5.6. The older proof has a signed-multiplier issue, explicitly identified in Benatti's later §3. In the stated physical class, \(m_{iso}=m_{ADM}\ge0\), so the comparison can use a strictly positive upper parameter before taking its limit. No unsupported negative-sign version of that argument is being used. Benatti's all-\(p\) theorem with other global assumptions is not used to erase those assumptions.

The broader OWR sentence is distinguished from the intended full-paper hypotheses. That distinction is substantive: its removal allows the candidate's negative scalar curvature in a compact interior.

## Complete negative example: independent checks

Set \(U=1-\chi(r)/r\), where \(0\le\chi\le1\) is smooth, zero for \(r\le2\), and one for \(r\ge3\), and \(g=U^4\delta\) on \(\mathbb R^3\). This is exactly Euclidean near zero and satisfies \(U\ge1/2\), so it is smooth, complete, positive and boundaryless. Its single end is exactly \(U=1-1/r\), with order-one decay of every derivative. The ADM integral reduces to

\[
 m_{ADM}=\lim_{r\to\infty}-2r^2U^3U_r=-2.
\]

The scalar curvature is smooth and compactly supported, hence integrable. In fact

\[
 \Delta U=-\chi''(r)/r,\qquad R_g=8U^{-5}\chi''(r)/r.
\]

Because \(\chi'\) vanishes at both ends of the transition and integrates to one, \(\chi''<0\) somewhere. Thus the violation of global nonnegative scalar curvature is analytically necessary, without relying on a numerical cutoff or the positive mass theorem.

For \(K_R=\overline B((R/2)e_1,R)\), \(R\ge6\), the interior contains \(B(0,R/2)\) and the exterior lies in \(r\ge R/2\ge3\). These balls are nested because center separation plus earlier radius is at most the later radius. Therefore they are an admissible smooth compact exhaustion; off-center placement is not an illicit relaxed competitor.

The candidate's \(\phi=(1-R/|x-a_R|)/U\) is the actual metric harmonic potential:

\[
 \operatorname{div}(U^2\nabla(f/U))=U\Delta f-f\Delta U=0.
\]

It has the correct boundary values and finite exterior energy. Uniqueness follows from the maximum principle. Its far-field coefficient yields \(c_g(K_R)=R-1\), as claimed. This is also the harmonic-capacity identity from Jauregui equation (41), whose derivation comes before the following volume paragraph introduces nonnegative mass.

A distinct exact check uses inner-boundary flux. On \(\partial B(a,R)\), \(\partial_\nu f=1/R\), so

\[
 c_g(K)=\frac1{4\pi R}\int_{\partial B(a,R)}U\,dA_\delta.
\]

For \(d=|a|<R\), direct angular integration gives the boundary average of \(1/r\) equal to \(1/R\). Hence with \(U=1-a_0/r\), this flux equals \(R-a_0\), independently of the off-center location. This confirms exact capacity rather than merely the energy of a test function.

The volume integrand satisfies \(U^6=1-6/r+O(r^{-2})\) outside the fixed core. The core replacement error is \(O(1)\); integrating the remainder over \(K_R\subset B(0,3R/2)\) gives \(O(R)\). Neither can alter the radius's constant-order term.

Independently of the candidate's center-shell computation, integrate along rays from the origin. The outer radius is

\[
 t(z)=d z+\sqrt{R^2-d^2+d^2z^2},\quad -1\le z\le1.
\]

The cross term in \(t(z)^2\) is odd. Thus

\[
 \int_{B(a,R)}\frac{dx}{|x|}
 =\pi\int_{-1}^{1}(R^2-d^2+2d^2z^2)\,dz
 =2\pi(R^2-d^2/3).
\]

At \(d=R/2\), this equals \(11\pi R^2/6\), yielding

\[
 V_g(K_R)=\frac{4\pi}3R^3-11\pi R^2+O(R),\qquad
 v_g(K_R)=R-\frac{11}4+O(R^{-1}).
\]

Consequently \(v_g-c_g\to-7/4\), and the exact supremum definition gives

\[
 m_{CV}\ge-\frac74>-2=m_{ADM}.
\]

The fixed gap is \(1/4\). No claim of optimality of the balls, finite-radius empirical extrapolation, or value of the full supremum is needed.

## Scaling, sign, and limiting boundaries

| Control | Verified result | Implication |
|---|---|---|
| Euclidean normalization | \(c(B_R)=R\), deficit zero | The \(1/(4\pi)\) factor is correct. |
| Centered Schwarzschild | Deficit limit \(m\) | Centered-ball tests alone miss the counterexample. |
| Fixed off-center fraction \(0<\lambda<1\) | Limit \(m(1-\lambda^2/2)\) | Strict improvement over ADM for \(m<0\); smaller than ADM for \(m>0\). |
| Zero mass | Zero deficit | Consistent Euclidean limit. |
| Homothety by \(b>0\) | Capacity, volume radius, ADM and gap multiply by \(b\) | Units and normalization are consistent. |
| Compact fill changes | Volume error \(O(1)\), radius error \(O(R^{-2})\) | Filling cannot create or erase the constant gap. |
| \(\lambda\to0\) | Gap tends to zero | Correct centered boundary. |
| \(\lambda\to1^-\) | Exhaustion valid for each fixed \(\lambda<1\) | No uniform error claim is made; \(\lambda=1\) itself is not an exhaustion of growing centered cores. |
| Curvature sign | \(R_g<0\) somewhere in the transition | Counterexample lies outside the credited physical class. |

The explicit metric is order one, so it remains safely inside \(\tau>1/2\). The proof does not use borderline decay or limiting error estimates that might survive at \(\tau=1/2\).

## Reproduction and output semantics

All candidate code was read before fresh replay. Runs used the pre-existing SymPy environment and a private copy of the 18 target files; raw source files were linked privately. No package installation, full repository copy, candidate modification, Git mutation or external individual communication occurred.

- The author checker replays byte-exact and reports 5,529 scalar assertions. Every field (`dependency`, `exact_assertions`, `scope`, `status`) matches the frozen output.
- Original review replay reports 3,128 assertions, nine author-manifest-bound files and seven independently hash-checked source PDFs; the entire JSON object equals the frozen review output, including nested author receipt and scope.
- Publication replay checks all public hashes and reports both assertion counts and seven raw-source hashes checked in this run. Every field was checked explicitly.
- The portable checker with sources intentionally held out produces the same mathematical output and an honest `source_pdfs: 0`. This does not contradict the historical review output's seven checked sources.
- `independent_controls.py` adds 23 named exact calculations using inner-boundary flux, origin-ray integration, continuous remainder control, signed formulas, homothety and limiting checks. All residuals are zero. Their number is not evidence for untested geometry; the analytical proof is the evidence.

The code correctly limits its scope. It does not prove completeness, cutoff existence, capacity minimization, source theorem applicability or the global mass supremum merely by assertion counts. Those obligations were audited analytically and against primary sources.

One non-mathematical failed lookup is preserved: initially looking for `snapshot/QUEUE.md` returned no file; file discovery located the real `snapshot/unsolved_math_prioritization/QUEUE.md`. Poppler reported a recoverable xref-reconstruction warning for the Jauregui–Lee PDF, whose bytes still match and whose relevant text was successfully extracted. No mathematical control or replay failed.

## Exact remaining gap and required disposition

No repair is required for the frozen mathematical claims. The exact full \(m_{CV}\) of the filled negative-mass example is not evaluated; the proved lower bound is enough. Historical novelty and the earlier campaign's search completeness are unverified by this audit. Those are limitations already retained in the candidate. A priority claim, exact-mass claim or assertion that this disproves the global-\(R_g\ge0\) conjecture would exceed the evidence.

Recommended disposition: accept the credited `already_solved` status for the intended physical class and retain the separately scoped counterexample to the unrestricted literal reading. Preserve both source scopes prominently and preserve the stated prior-theorem credits. `PUBLIC_MANIFEST.json` enumerates only original audit proof/code and generated metadata/outputs in this audit's own root, excludes itself, and explicitly excludes every private/raw/imported replay artifact.

Primary sources read: [OWR 40/2021](https://ems.press/content/serial-article-files/46918), [Jauregui capacity-volume paper](https://arxiv.org/pdf/2002.08941), [BFM nonlinear mass paper](https://arxiv.org/pdf/2305.01453v2), [Benatti signed correction](https://arxiv.org/pdf/2511.11155v2), [Jauregui–Lee isoperimetric mass paper](https://arxiv.org/pdf/1602.00732), [Jauregui–Lee–Unger note](https://arxiv.org/pdf/2408.08871), and [BFM isoperimetric Penrose paper](https://arxiv.org/pdf/2212.10215). Source applicability is discussed at the relevant claims above; these are metadata links, not redistributed primary content.
