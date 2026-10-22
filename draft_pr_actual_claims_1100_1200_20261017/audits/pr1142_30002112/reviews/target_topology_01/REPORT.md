# Independent exact-target and topology review

Result: **PASS within this review family. No blocking or major mathematical finding.**

Reviewed source: PR1142 / problem30002112 / OWR-12005-004, supplied source head `c29139d2c2a98f1a0284d0dc794c88f51c680a0c`. The actual `inputs/PROOF.md` read was 10,412 bytes, SHA-256 `c4608dbf5f9e39b398f7db20100273fdab085598382293f8224488585015f658`. This is a fresh review, not adoption of the source's prior acceptance language.

Completion estimate for this assigned review family: 100%. This is not a percentage estimate for historical novelty or for a formal machine proof.

## Independence and sequence

The original question was established and written to `TARGET_FINDING_BEFORE_PROOF.md` at 2026-10-17T23:15:53.473164Z before reading the proof. The entire Colbois talk, printed pages 2034–2036 of OWR33/2012, was visually inspected from rendered PDF pages 22–24. The CEG paper was checked for standing definitions, all main theorem hypotheses, min-max indexing, and its relevant examples. Only after the independent target finding was saved was `PROOF.md` read. No old `AUDIT.md`, acceptance file, status file, parent's findings, or concurrent review was read. No outreach, other-agent delegation, git mutation, PR/tracker write, or release action occurred.

## Exact target

The precise question is the additive replacement of the estimate in Theorem 3 of the [Colbois OWR talk](https://ems.press/content/serial-article-files/46403), DOI [10.4171/OWR/2012/33](https://doi.org/10.4171/OWR/2012/33): for each dimension \(m\ge2\), do dimension-only constants \(A_m,B_m\) exist such that every bounded smooth domain \(\Omega\subset\mathbb R^{m+1}\) and every integer \(k\ge1\) satisfy

\[
\lambda_k(\partial\Omega)|\partial\Omega|^{2/m}
\le A_m I(\Omega)^{1+2/m}+B_m k^{2/m},
\qquad I(\Omega)=\frac{|\partial\Omega|}{|\Omega|^{m/(m+1)}}?
\]

The operator is the intrinsic scalar Laplace–Beltrami operator of the entire boundary with its induced metric. This is not an interior Dirichlet eigenvalue question. Eigenvalues include multiplicities and all zero modes, beginning with \(\lambda_1=0\).

The connected-boundary concern was tested against positive primary evidence. [CEG, arXiv:1007.0826v2](https://arxiv.org/pdf/1007.0826), Example 3.1, page 14, uses a product domain with two boundary components and explicitly has \(\lambda_1=\lambda_2=0\) and \(\lambda_3>0\). Its min-max formula on page 7 uses all \(k\)-dimensional subspaces of \(H^1(\Sigma)\). Thus the introductory shorthand calling \(\lambda_2\) the first positive eigenvalue does not establish a universal connected-boundary assumption. The talk and CEG impose no genus restriction in the target theorem. The conservative usual interpretation of “domain” as connected and open is satisfied by the proposed construction.

**Target verdict:** a two-component boundary is admissible for the actual stated question. A connected-boundary restriction would define a different question; this proof does not resolve that restriction. No such restriction was found in the full source context examined.

## Precise topological theorem and its applicability

The needed form is the generalized separation theorem for an arbitrary closed embedded hypersurface, rather than just a sphere:

For a connected closed compact embedded codimension-one manifold, the Euclidean complement splits into precisely two open connected regions sharing the hypersurface as boundary.

A primary proof and exact statement are [S. Alexander, *Local and global convexity in complete Riemannian manifolds*, Pacific J. Math. 76(2) (1978), Theorem 1, p. 284](https://msp.org/pjm/1978/76-2/pjm-v76-n2-p01-s.pdf). The PDF's page 3 was visually inspected. No spherical topology, simple connectivity, unknottedness, or preassigned orientation is required. Here \(d=m+1\ge3\). The constructed \(H\) is closed: CDE's standing hypothesis on page 1 is compact, connected, without boundary, and its Theorem 1.4 supplies embeddings within this class. Smooth approximation preserves the same abstract closed manifold.

For clarity, the theorem's “without boundary” hypothesis is essential. A smoothly embedded compact disk is not a separator. That edge case does not occur in the source construction.

## Independent detailed topology derivation

Let \(H\subset B_{1/2}\subset\mathbb R^d\) be smooth, compact, connected, embedded, and without boundary. Let \(U,E\) be the two complementary components, with \(E\) the unbounded one.

1. **Exactly one unbounded component.** Choose \(r\in(\max_{h\in H}|h|,1/2)\), possible by compactness and strict containment. The connected exterior \(\mathbb R^d\setminus\overline B_r\) avoids \(H\), lies in a single complement component, and is unbounded. Any unbounded component meets this exterior, so that component is uniquely \(E\). Consequently \(U\subset\overline B_r\subset B_{1/2}\).

2. **Compact smooth cavity closure.** The separation theorem gives \(\partial U=H=\partial E\). Thus \(\overline U=U\cup H\subset\overline B_r\subset B_{1/2}\), and \(\overline U\) is compact. Near every point of \(H\), a smooth ambient chart flattens \(H\) to a coordinate hyperplane. The two local sides are connected. Since both \(U\) and \(E\) have that point on their boundary, one local side lies in \(U\), the other in \(E\). Therefore \(\overline U\) is a smooth compact manifold with boundary \(H\). Its outward normal is globally defined; in particular orientability is a consequence, not an omitted extra assumption.

3. **Identity of the retained open set.** The disjoint decomposition of the ambient space is \(U\sqcup H\sqcup E\), so \(\mathbb R^d\setminus\overline U=E\). Hence

   \[
   \Omega=B_1\setminus\overline U=B_1\cap E.
   \]

   This is open, nonempty, bounded, and contains the entire annulus \(\{1/2<|x|<1\}\).

4. **Connectedness inside the outer ball.** An open connected Euclidean set is path connected, so \(E\) is path connected. Fix \(x\in E\cap B_1\) with \(|x|<3/4\), and choose \(y\in E\) with \(|y|>1\). Take an \(E\)-path from \(x\) to \(y\) and stop it at its first intersection with \(S_{3/4}\). Continuity gives such a first time; the preceding path is contained in \(B_{3/4}\cap E\subset\Omega\). Its endpoint belongs to the full annulus. Points with \(|x|\ge3/4\) already belong to that annulus. Because this annulus is path connected when \(d\ge2\), all points of \(\Omega\) are joined inside \(\Omega\). No assertion that an arbitrary intersection of connected sets is connected is used.

5. **Exact boundary and smoothness.** Near \(H\), the outer sphere is absent, and the local halfspace argument gives boundary exactly \(H\). Near \(S_1\), the cavity is absent and \(\Omega\) agrees locally with \(B_1\). Any other point lies locally inside one of the open sets \(U,E,\mathbb R^d\setminus\overline B_1\), and is not a boundary point of \(\Omega\). Therefore

   \[
   \partial\Omega=S_1\sqcup H.
   \]

   Both components are smooth compact connected hypersurfaces, with positive mutual distance. There are exactly two boundary components and no corners or hidden additional boundary. Reversing the normal on the cavity does not change its induced metric or intrinsic Laplacian.

6. **Volume control.** Since \(\overline U\subset B_{1/2}\),

   \[
   \omega_d(1-2^{-d})\le|\Omega|\le\omega_d.
   \]

   Boundary smoothness gives zero ambient measure to \(H\); subtracting open \(U\) or its closure yields the same volume. The bound is independent of the handles, knottedness, curvature, or area of \(H\).

These steps work for an inner torus, for a knotted tubular boundary, and for higher-genus or non-spherical \(H\). They do not claim that either complementary component is a ball. As a simple exact genus-one control, the standard torus with major radius \(1/4\) and minor radius \(1/16\) lies in \(B_{5/16}\subset B_{1/2}\); removing its closed solid torus from \(B_1\subset\mathbb R^3\) has the stated two-component boundary and connected exterior. This control illustrates admissibility, not the high-area/high-gap existence theorem. No numerical approximation to Jordan–Brouwer or Nash–Kuiper was substituted for proof.

## Geometric interface checked

The [CDE preprint, arXiv:0909.5346v1](https://arxiv.org/pdf/0909.5346), Theorem 1.4 and Section 5, supplies unbounded normalized first positive eigenvalues on smooth connected closed embedded hypersurfaces. Its zero-based \(\lambda_1>0\) corresponds to this proof's \(\lambda_2>0\). For \(m=2\), genus may grow. For \(m\ge3\), taking the initial abstract hypersurface \(S^m\subset\mathbb R^{m+1}\) is permitted. Section 5 explicitly uses \(C^1\) isometric embeddings and smooth approximation. Rendered pages 6,14,15 were inspected.

The [De Lellis–Székelyhidi statement, Theorem 1.2, p. 4]\(https://www.math.ias.edu/delellis/sites/math.ias.edu.delellis/files/contr_vol_Nash_11.pdf\), visually inspected, provides precisely the extra localization mechanism needed: a smooth short embedding of a smooth closed manifold into codimension at least one has arbitrarily \(C^0\)-close \(C^1\) isometric embeddings. Thus CDE's unbounded normalized gap does not merely move the main difficulty into an unsupported small-ball localization claim.

The proof's interface is valid: choose a metric with normalized gap \(>2LS^{2/m}\), scale it to area \(S\), make any hypersurface embedding strictly short and small by ambient scaling, apply that \(C^0\)-approximation theorem, then approximate in \(C^1\) by smooth embeddings. Their induced metrics converge uniformly to the chosen positive definite metric. The displayed metric comparison yields volume and numbered eigenvalue convergence by min-max; exact-area rescaling tends to one. The radius slack \(r/8,r/4,r/3,2r/3<r\) survives this final rescaling. Compactness of the parameter manifold supplies both a global strict-shortness factor and preservation of embedding under sufficiently small \(C^1\) perturbation. No uniform smoothing radius across different \(q\) is required.

This review checks the applicability and consequence of these established inputs. It does not independently rebuild the upstream large-eigenvalue metric constructions or the full Nash–Kuiper iteration.

## Universal target deduction re-derived

Fix \(m\ge2\). The construction supplies \(H_q\subset B_{1/2}\), \(|H_q|=q\), and \(\lambda_2(H_q)>T_q=q(q+m-1)\). Write \(a_q=q+\rho_m\) and \(v_m=\omega_{m+1}(1-2^{-(m+1)})>0\). The topology result gives connected smooth \(\Omega_q\) with \(|\partial\Omega_q|=a_q\) and \(|\Omega_q|\ge v_m\). Therefore

\[
I(\Omega_q)^{1+2/m}\le v_m^{-(m+2)/(m+1)}a_q^{1+2/m}.
\]

The exponent follows from \((m/(m+1))(1+2/m)=(m+2)/(m+1)\); there is no reversed volume inequality.

On \(S^m\), degrees \(\ell<q\) contribute

\[
N_q=\binom{q+m-1}{m}+\binom{q+m-2}{m}
\]

eigenvalues strictly below \(T_q\). This follows by summing the harmonic-polynomial multiplicities, a telescoping difference; it includes the sphere's zero. The inner component contributes exactly one more eigenvalue below \(T_q\), namely its zero. Hence the first sphere mode at threshold has global index \(k_q=N_q+2\), and \(\lambda_{k_q}(\partial\Omega_q)=T_q\). Its multiplicity causes no difficulty: \(k_q\) is the first index in that block. At \(q=1\), \(N_1=1,k_1=3\), correctly locating the first positive eigenvalue after the two zeros. For \(m=2\), \(N_q=q^2\) provides a useful exact special case.

For \(q\ge m\), each binomial coefficient is bounded by \((q+m)^m\le(2q)^m\), so \(k_q\le2^{m+2}q^m\) and \(k_q^{2/m}\le C_mq^2\), with the proof's \(C_m=2^{2+4/m}\). Thus for \(Q_q\), the ratio in the source's exact claim,

\[
\frac1{Q_q}
\le v_m^{-(m+2)/(m+1)}\frac{a_q}{q^2}
       +\frac{C_m}{a_q^{2/m}}
\longrightarrow0.
\]

Here the numerator was bounded below by \(q^2a_q^{2/m}\); all quantities are positive. Consequently \(Q_q\to+\infty\). This directly verifies the stronger unweighted-quotient statement, rather than only the contradiction for one selected pair of constants.

If arbitrary finite \(A_m,B_m\) existed, replacing them by larger positive constants would preserve the proposed bound. The divergent quotient rules out every such pair. All quantifiers are in the required order: \(m\) is fixed, constants would be fixed, and the domain and index may vary jointly with \(q\). No Weyl asymptotic uniform over varying metrics is required.

At \(m=2\), the denominator terms both grow at most quadratically while the numerator grows cubically. For \(m>2\), the \(k_q\)-term remains quadratic and the numerator has the extra factor \(q^{2/m}\). The argument does not extend to \(m=1\): the required unbounded normalized first gap on embedded closed curves fails. This is consistent with the stated \(m\ge2\) target.

## Findings, repairability, and limits

| Item challenged | Finding | Severity / repair |
|---|---|---|
| Hidden connected-boundary convention | Positively excluded by source's explicit two-component example and indexing | PASS; no repair required |
| Domain connectedness | Explicit path argument valid | PASS; no repair required |
| Non-spherical / knotted inner hypersurface | General separation theorem applies; no Schoenflies claim needed | PASS; no repair required |
| Compactness and smooth cavity closure | Follows from strict containment, common-boundary theorem and local graph charts | PASS; no repair required |
| Extra zero eigenvalue / spectral shift | Both zeros included; \(k_q=N_q+2\) correct | PASS; no repair required |
| Arbitrary dimension and topology | CDE interface permits varying genus for \(m=2\), \(S^m\) for \(m\ge3\) | PASS; no repair required |
| Original proof's Jordan–Brouwer citation lacks a specific reference | Mathematical statement is valid; primary reference supplied above | Optional bibliographic enrichment, not a proof defect |

Strongest verified result in this family: accepting the named established geometric existence theorems as standard mathematical inputs, the specified source proof produces admissible connected bounded smooth Euclidean domains with exactly two boundary components whose quotient in the original additive question tends to infinity, for every fixed \(m\ge2\). No exact-target or topological gap remains. The family finding does not certify connected-boundary analogues, external peer review, historical novelty, or a formal proof assistant verification.

Source versions, hashes, read scopes, exposure, and artifacts are recorded in `SOURCE_REGISTER.json`, `PROCEDURE_EXPOSURE.md`, and the externally hashed `RECEIPT.json` with its `.sha256` sidecar. The pre-proof target finding remains unedited. Third-party bodies, extracted text, and page renders were subsequently moved without byte changes into ignored `sources/private/` for distribution control; `sources/DISTRIBUTION_RELOCATION.json` preserves all original-to-current paths and hashes.

Distribution limitation reported by parent: the original source copies were included in checkpoint `ed1173c3a0b46dd271e68c32e5a853ed07b468eb` before their relocation. The parent initiated removal from current main, whose completion was not independently verified by this agent. Older history retains those copies; the subsequent local ignore rule and private-path receipts do not undo that earlier publication. This affects distribution provenance, not the mathematical findings.
