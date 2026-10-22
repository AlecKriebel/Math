# Source identity and assumption map

## Source identity and verification

The catalog target is 4000018 / AMR-039-0018. The public original is [Yann Ollivier's Problem R](https://www.yann-ollivier.org/rech/publs/problems_curvmarkov.pdf), printed page 5. The document labels itself May 2008 but its currently served bytes refer to a 2009 result elsewhere; the label is not treated as proof that the bytes are an unchanged 2008 version.

The problem asks how the coefficient in an unequal-time transport estimate relates to dimension, especially the dimension in the generator curvature-dimension inequality. The title's “L2” describes the square-root-curvature diameter scale. The transport distance actually displayed is **T1, i.e. W1**.

The live problem webpage returned HTTP 403 in this investigation. A preexisting catalog record was used only to identify the target and then checked against the original PDF; its “OPEN-TRIAGE” label was not adopted as an authoritative theorem. Live repository checks are recorded as metadata in LIVE_VERIFICATION.json. No matching prior attempt was found; absence of a search hit is not proof of absolute absence.

Four full primary PDFs were retrieved. Their bytes, hashes, page counts and actual inspection coverage are in SOURCE_VERIFICATION.json. Full texts and rendered source pages are excluded from the authored packet. The later papers below establish important related theorems. Neither inspected paper claims to resolve Ollivier's exact Problem R, and no exact-target resolution was located in the search. This is a bounded literature assessment, not a claim that no such result exists.

## 1. Ollivier's actual theorem

Source: [*Ricci curvature of Markov chains on metric spaces*](https://www.yann-ollivier.org/rech/publs/curvmarkov.pdf), J. Funct. Anal. 256 (2009), 810–864; inspected author PDF, Proposition 52, printed pages 52–54. Its basic random-walk setting is a Polish metric space, measurably assigned Borel probability kernels, and finite first moments (Definition 1).

For the strong diameter theorem one needs an epsilon-geodesic space: each pair can be joined by a finite chain of steps at most epsilon whose summed lengths equal the distance. The displayed transport bound is assumed at all sufficiently small pairs of times, uniformly for points with distance between epsilon and twice epsilon. One additionally assumes

\[
\kappa>0,\quad C\ge0,\quad
\varepsilon\le\tfrac12\sqrt{C/(2\kappa)}.
\]

The actual conclusion is

\[
\operatorname{diam}X\le\pi\sqrt{C/(2\kappa)}+4\pi\varepsilon.
\]

The uncorrected limit requires availability at arbitrarily fine scales with fixed constants, as in a geodesic setting with the all-pairs condition. Zero-time kernels are used in the endpoint chaining proof. One must assume them or justify their limiting use by the appropriate moment continuity.

The author's Brownian normalization is generator \(\tfrac12\Delta\), \(\kappa=\tfrac12\inf\mathrm{Ric}\), and a sufficient Gaussian-type coefficient \(C=n\), not a proven identity \(C=n-1\). The surrounding text explicitly notes the resulting \(n\)-versus-\(n-1\) loss. The short open-problem statement is not a license to remove these distinctions.

## 2. Smooth diffusion and Kuwada's space-time theorem

Source: [Kazumasa Kuwada, arXiv:1308.5471v2](https://arxiv.org/abs/1308.5471v2), full 39-page preprint; [published article metadata](https://link.springer.com/article/10.1007/s00526-014-0781-2), Calc. Var. 54 (2015), 127–161. The arXiv revision is 24 July 2014; the served PDF also has an October 2018 typesetting date. Neither is confused with the issue year.

Equation (1.4) is a squared-W2 estimate. Corollary 2.4 identifies it with the finite-dimensional Bakry–Ledoux gradient estimate under specified assumptions, not for every arbitrary W1-contracting process.

The base space is Polish and geodesic. Two abstract routes are stated:

- A1 plus A4: time differentiability of \(P_tf(x)\) for bounded Lipschitz tests at every positive time and point, plus the strong Feller property.
- A2, A3 and A4: a locally finite full-support reference measure; bounded extension of the semigroup to an \(L^q\) space and positive-time generator differentiability there; existence of absolutely continuous W2 geodesics between bounded-support bounded-density probability measures whose densities have the local conjugate integrability specified in A3; and strong Feller regularization. The gradient statement is then for the indicated \(L^q\) Lipschitz tests and almost every point.

Corollary 2.4 uses finite positive \(N\) and all \(0<s<t\), with arbitrary probability inputs. The p=beta=2 specialization is relevant here; p=1 is not a permitted direct substitution in the duality theorem.

The concrete smooth route is Theorem 2.6: a complete \(m\)-dimensional Riemannian manifold without boundary, generator \(L=\Delta+Z\) for smooth vector field \(Z\), and finite \(N\in[m,\infty)\), with

\[
\mathrm{Ric}-(\nabla Z)^{\mathrm{sym}}-\frac{Z\otimes Z}{N-m}\ge K g.
\]

At \(N=m\), this means \(Z=0\) and \(\mathrm{Ric}\ge Kg\). Its p=2 statement gives (1.4). The diffusion kernel is the one generated by this operator, not an arbitrary process assigned to the manifold. FULL_PROOFS.md derives the W1 consequence with its horizon-dependent coefficient.

## 3. Metric-measure heat flow, CD and RCD

Source: [Erbar–Kuwada–Sturm, arXiv:1303.4382v2](https://arxiv.org/abs/1303.4382v2), full 48-page preprint; [published metadata](https://link.springer.com/article/10.1007/s00222-014-0563-7), Invent. Math. 201 (2015), 993–1071. The theorem numbers in this packet refer to the inspected arXiv v2, not to an uninspected journal typesetting.

Theorem 3 gives the W2 expansion bound used in Proposition 4 of this packet for the **canonical** heat flow on RCD*(K,N) spaces. In the paper's framework, the metric-measure space is complete and separable with full-support locally finite reference measure; the RCD* condition includes infinitesimal Hilbertianity (quadratic Cheeger energy / linear canonical heat flow) and the reduced finite-dimensional curvature condition. Probability inputs have finite second moments. Dirac inputs are allowed. The paper's regularity setup supplies moment-continuous extension to time zero.

Theorem 1 equates the entropic and reduced curvature conditions under essential nonbranching. The full equivalence diagram in Theorem 7 adds Assumption 4.2 when going back from analytic/transport bounds: length-space structure, full support, Gaussian integrability of the reference measure, and the Sobolev-to-Lipschitz property (a function with weak gradient at most one has a 1-Lipschitz representative).

These distinctions matter:

- The generator condition BE(K,N), also called Bakry–Émery CD(K,N), is not merely the same definition as synthetic CD(K,N).
- Synthetic CD allows Finsler phenomena. A linear heat semigroup and Hilbertian first-order calculus must not be inferred from CD alone.
- This packet retains the paper's **RCD*** notation and does not silently invoke later equivalences between starred and unstarred conventions.
- N is an upper effective dimension; it need not equal a manifold's topological dimension. In the smooth weighted case finite N greater than m penalizes drift; N=m prohibits nonzero drift under the stated convention.
- At N=infinity the dimension term disappears. The finite-N transport term cannot be obtained by inserting infinity as though it were a finite coefficient. Proposition 7 gives an explicit failure.

## 4. Assumptions in the counterexample

The reset examples are compact, complete, separable, geodesic, full-support, reversible, and Feller. Their probability measure is finite, so all moment and Gaussian-integrability conditions are automatic. The operator is nonlocal, fails strong Feller regularization on nondiscrete spaces, and its Gamma is not the canonical metric weak gradient. In particular it is **not** the canonical RCD heat flow. These failures are central, not technical details to suppress.

Thus it is consistent for the underlying interval to admit an ordinary finite-dimensional canonical geometry while the chosen reset generator has no finite BE dimension at K=1. Similarly, the same W1 constants can appear on normalized cubes of every dimension.
