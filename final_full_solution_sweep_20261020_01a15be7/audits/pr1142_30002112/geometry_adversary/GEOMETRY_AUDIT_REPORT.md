# Independent adversarial audit of the geometry in PR 1142

Audited immutable head: `c29139d2c2a98f1a0284d0dc794c88f51c680a0c`.
Reference base: `f6caddda8f8be2cdb3e91494325d8f7f365bc3fc`.
Problem: `30002112`, alias `OWR-12005-004`.
Actual distributed proof SHA-256: `c4608dbf5f9e39b398f7db20100273fdab085598382293f8224488585015f658`.

## Verdict and scope

**Geometry accepted as stated.** I found no mathematical defect in the prescribed-area, high-gap, small-ball embedding lemma or in the connected two-boundary-component domain construction. These discharge the geometric existence obligations in the negative answer for every fixed `m >= 2`. The conclusion uses the established CDE and Nash-Kuiper theorems as explicit inputs; the report does not reprove those theorems or certify a new publication, historical priority, external review, or a connected-boundary result.

The strongest verified geometric statement is this:

> For each fixed integer `m >= 2` and all `S,L,r > 0`, there is a connected closed smooth embedded hypersurface `H` in the open Euclidean ball `B(0,r)` in `R^(m+1)` with induced area exactly `S` and first positive intrinsic Laplace-Beltrami eigenvalue greater than `L`. For `m >= 3`, its abstract manifold may be `S^m`; for `m=2`, genus is allowed to vary. When `r=1/2`, removing its bounded complementary component from the unit ball yields a connected bounded smooth Euclidean domain with boundary exactly `S^m` disjoint union `H` and volume uniformly bounded below by the fixed outer annulus.

The proof below checks all simultaneous quantifiers; a dilation of a high-gap hypersurface alone would not establish them.

## Independence and provenance

I read the complete immutable `PROOF.md` first. I then freshly retrieved and visually inspected the primary source interfaces, reconstructed the argument, and wrote `INITIAL_RECONSTRUCTION.md`. Only afterward did I read the historical `AUDIT.md` and its status metadata. The historical acceptance was not used as a premise.

An initially noted hash difference is resolved by the existing provenance fields. Historical `SOURCE_METADATA.json` binds its original reviewed proof to SHA-256 `0123ee87f7fe6ee04eed80939015df01e9c36a15bcb576085f30385c18d25ac9`; `STATUS.json` explicitly distinguishes that original from the distributed proof and records the correct distributed hash `c4608dbf...f658`. Historical `AUDIT.md` explains that the change was framing. This audit independently binds the actual distributed proof, so no assumption that the two historical versions are mathematically identical is needed for this verdict.

All work was confined to this audit directory. No external person was contacted, no original or captured code was executed, and no provider, PR, Google Workspace, Git index, branch, ref, release, or original candidate file was mutated. Third-party PDF bodies, extracted text and page images are private inspection material and are excluded from the authored artifact manifest.

## Primary-source scope and interfaces

The original Colbois talk is on printed pages 2034-2036 of OWR 33/2012. I inspected the entire talk. Its Theorem 3 addresses bounded smooth Euclidean domains and the following question asks whether its multiplicative bound can be replaced by the specified additive bound. There is no connected-boundary hypothesis in that theorem or the talk's standing context. The cavity construction therefore addresses the actual stated domain class, rather than a label inferred from a secondary summary. [Official report](https://ems.press/content/serial-article-files/46403).

CDE's standing setting is compact, connected, boundaryless submanifolds. Theorem 1.4 and Section 5 provide unbounded normalized first positive eigenvalue on smooth embedded orientable surfaces when `m=2`, and on a fixed hypersurface-embeddable manifold when `m>=3`; choose that manifold to be `S^m`. Their first positive eigenvalue is indexed from zero and corresponds to the candidate's second eigenvalue on a connected component. [CDE primary preprint](https://arxiv.org/pdf/0909.5346), [published DOI](https://doi.org/10.1112/blms/bdp100).

Theorem 1.2 in the inspected De Lellis-Szekelyhidi text applies to smooth closed Riemannian manifolds and smooth short immersions into `R^N` for `N>=n+1`, gives arbitrary uniform approximation by `C^1` isometries, and expressly preserves the embedded conclusion when the starting map is embedded. This is the needed codimension-one, embedding and containment interface. [Author-hosted precise theorem](https://www.math.ias.edu/delellis/sites/math.ias.edu.delellis/files/contr_vol_Nash_11.pdf).

CEG numbers the complete spectrum from index one and its Example 3.1 explicitly treats a two-component boundary and its two zero eigenvalues. That example is not the Euclidean counterexample being audited. It independently confirms that the cited source convention does not silently exclude disconnected boundaries. [CEG primary preprint](https://arxiv.org/pdf/1007.0826).

For topology, the chosen abstract manifolds are orientable. Hatcher's Alexander-duality Corollary 3.45, together with local smooth separation, verifies the general hypersurface form required below. [Author-hosted chapter, printed pages 255-256](https://pi.math.cornell.edu/~hatcher/AT/ATch3.pdf). The proof does not require a sphere-only separation theorem, simple connectivity of either side, or smooth Schoenflies.

## Checkable proof of the simultaneous realization lemma

Write `lambda_+` for the first positive eigenvalue on a connected closed manifold. Fix `m>=2` and `S,L,r>0` before choosing any geometric object.

By CDE choose a connected smooth manifold `M` admitting a smooth hypersurface embedding and a smooth metric `g0` with

`lambda_+(g0) Vol(g0)^(2/m) > 2 L S^(2/m)`.

One can choose `g0` to be induced by the smooth embedded hypersurface supplied by CDE; there is no unverified assumption that an arbitrary high-gap metric already admits a smooth isometric codimension-one embedding. Set

`g = (S/Vol(g0))^(2/m) g0`.

Scaling a metric by `b^2` multiplies `m`-volume by `b^m` and Laplace eigenvalues by `b^-2`. Consequently `Vol(g)=S` and `lambda_+(g)>2L`.

Take any smooth embedding `e0:M->R^(m+1)`. Since `M` is compact and `g` is positive definite, there is finite `K>0` with `e0*e_Eucl <= K g`. Also `max_M |e0|` is finite. Choose `t>0` small enough that `t^2 K<1` and `t max_M|e0|<r/8`. Then `e=t e0` is a smooth strictly short embedding for `g` and `e(M)` lies in `B(0,r/8)`.

Apply Nash-Kuiper with uniform error less than `r/8`. Its embedding conclusion gives a `C^1` isometric embedding `f:(M,g)->R^(m+1)` with `f(M)` inside `B(0,r/4)`. The target dimension is exactly `m+1`, which satisfies the inspected theorem's hypothesis.

Here is the precise smoothing justification. Componentwise smoothing in finitely many smooth charts with a partition of unity gives smooth maps `f_j` converging to `f` in `C^1`. To see that the maps eventually remain embeddings, work near a source point in a coordinate ball so that `Df` differs from its injective derivative `A` at that point by less than one quarter of the least singular value of `A`. On a smaller convex coordinate ball, for nearby `f_j`, integration along a straight segment gives

`|f_j(x)-f_j(y)| >= (sigma_min(A)/2) |x-y|`.

Finitely many such balls and a Lebesgue number control all sufficiently close source pairs and preserve immersion. For pairs outside a fixed neighborhood of the source diagonal, the continuous function `|f(x)-f(y)|` has a positive minimum, because `M` is compact and `f` is injective. Sufficient uniform closeness preserves separation for those pairs. Thus `f_j` are injective immersions eventually, and compactness makes them smooth embeddings.

Their induced metrics `h_j=f_j*e_Eucl` converge uniformly to `g`, since `Df_j` converges uniformly to `Df` and `f` is isometric. Positive definiteness and compactness imply constants `c_j>=1`, tending to one, for which `c_j^-1 g <= h_j <= c_j g`.

For any positive metrics satisfying `c^-1 g <= h <= c g`, determinant comparison gives

`c^(-m/2) dV_g <= dV_h <= c^(m/2) dV_g`.

The inverse metrics have the same two-sided comparison factors `c^-1,c`. Consequently Dirichlet energies compare by `c^(+/-(1+m/2))` and squared `L^2` norms by `c^(+/-m/2)`. For every nonzero Sobolev function,

`c^(-(m+1)) R_g(u) <= R_h(u) <= c^(m+1) R_g(u)`.

The metrics have the same Sobolev space by uniform equivalence. Apply the full min-max characterization over subspaces of dimension `k`, so that no metric-dependent mean-zero space is compared. It gives the same inequality for every numbered eigenvalue, including zeros. Thus `S_j=Vol(h_j)` tends to `S` and `lambda_+(h_j)` tends to `lambda_+(g)>2L`.

Because the smooth induced metrics are compared directly to the known smooth metric `g` on `M`, no spectral regularity theorem for an arbitrary `C^1` hypersurface is being smuggled into the argument.

Finally set `a_j=(S/S_j)^(1/m)` and `H_j=a_j f_j(M)`. Area is exactly `S`, and

`lambda_+(H_j)=a_j^-2 lambda_+(h_j) -> lambda_+(g)>2L`.

The factors `a_j` tend to one. For sufficiently large `j`, the smoothed image lies in `B(0,r/3)`, `a_j<2`, and `lambda_+(H_j)>L`. Hence `H_j` lies in `B(0,2r/3)`, strictly inside the required ball. Choose any such `j`. The final object is connected, closed, smooth and embedded. No uniform bound on its curvature, derivative sizes, smoothing index or topological complexity is asserted as `S,L,r` vary.

## Checkable proof of the cavity geometry

For an integer `q>=1`, apply the lemma with `S=q`, `L=q(q+m-1)`, `r=1/2`. Let `H=H_q` be the resulting smooth connected hypersurface. It is orientable: use CDE's orientable surface when `m=2`, or the abstract manifold `S^m` when `m>=3`.

For clarity, one can justify separation without assuming `H` is a standard sphere. Compact smooth `H` is locally contractible. Alexander duality in the one-point compactification gives

`reduced H_0(S^(m+1) minus H; Z) = H^m(H; Z) = Z`.

Thus the complement has exactly two path components. Passing back to Euclidean space does not split the component containing infinity: its puncture at infinity is connected, since a point in a connected manifold of dimension `m+1>=3` can be bypassed in a small coordinate ball. There are exactly two open Euclidean complementary components, one bounded (`U`) and one unbounded (`E`). Since an orientable smooth hypersurface has a two-sided tubular collar, each of the two connected collar sides lies in a complementary component. Every component has nonempty boundary in `H`, hence meets a collar side; the two sides therefore belong to different components. Each component has boundary all of `H`. This gives the required general smooth separation conclusion without Schoenflies.

Let `a=max_H |x|`; compactness and strict containment give `a<1/2`. Every point with norm greater than `a` has a radial ray to infinity avoiding `H`, so lies in `E`. Therefore `U` is inside the closed radius-`a` ball and `closure(U)=U union H` is inside `B(0,1/2)`. This also resolves any open-ball versus closed-ball ambiguity.

Define `Omega=B(0,1) minus closure(U)`. Since `R^(m+1) minus H = U disjoint union E`,

`Omega = E intersect B(0,1)`.

It is open and has boundary exactly the disjoint union of the unit sphere and `H`. Around `H` it occupies the exterior collar side; around the unit sphere it occupies the inner side, as the cavity stays strictly away. Both boundary components are smooth and connected.

To prove connectedness, fix `x` in `Omega`. If `|x|>=3/4`, it lies in the connected annulus `B(0,1) minus closed B(0,1/2)`. Otherwise choose an `E`-path from `x` to a point of norm greater than one, which is possible because `E` is open and connected. Stop at its first radius-`3/4` crossing. The whole stopped path stays within the closed radius-`3/4` ball, hence inside the unit ball, and in `E`, hence inside `Omega`. It joins `x` to the same annulus. All points join that annulus, proving connectedness.

The candidate's sentence saying this stopped path lies in the open radius-`3/4` ball includes an endpoint on the radius-`3/4` sphere. Replacing it by the closed ball makes that sentence literal. The next required inclusion in the unit ball is already strict, so this is a harmless exposition issue, not a mathematical gap or a required patch.

Writing `omega_(m+1)` for unit-ball volume and `rho_m=(m+1) omega_(m+1)` for unit-sphere area, the full annulus stays in `Omega`, giving

`omega_(m+1)(1-2^(-(m+1))) <= |Omega| <= omega_(m+1)`

and

`|boundary Omega| = q + rho_m`.

No lower bound on cavity volume or stability of enclosed volume under smoothing is needed. Reversing the cavity's normal reverses an extrinsic orientation, while leaving its induced metric and scalar Laplace spectrum unchanged.

## Boundary cases and falsification controls

| Proposed failure | Result of adversarial check |
|---|---|
| Codimension one gives only immersion | The inspected theorem includes an embedding clause for an initial embedding. |
| Three constraints cannot be imposed independently by scaling | Scaling alone is insufficient; short embedding followed by the arbitrary `C0` approximation interface supplies the missing mechanism. |
| `C0` smoothing might preserve the image but destroy the metric | Correct risk in a different argument; the present smoothing is `C1`, and the explicit Rayleigh comparison controls the induced metric. |
| Exact-area normalization destroys strict gap or containment | Both have strict margins and the normalization factor tends to one. |
| Fixed genus two-dimensional metrics may have bounded normalized gap | True, so fixed genus is not used. In particular the fixed-sphere route would fail by the classical sphere eigenvalue-area bound. |
| Dimension one should also follow | False. A connected closed curve of length `S` has first positive intrinsic eigenvalue `4 pi^2/S^2`; arbitrary `L` at prescribed `S` is impossible. Excluding `m=1` is essential. |
| In ambient dimension four the bounded side must be a smooth ball | No ball claim is required or made. The construction uses only separation and a smooth common boundary. |
| Knotted/high-genus cavities can disconnect `Omega` | The exterior-to-annulus path proves connectedness independent of knotting or genus. |
| Very large area in a tiny ball contradicts an isoperimetric bound | Isoperimetry supplies an upper bound on enclosed volume at prescribed area, not a positive lower bound. No such lower bound is used. |
| Smoothing must preserve the enclosed volume | It need not. Only the final containment supplies the uniform outer-annulus volume. |
| Repeated cavities cause accumulated boundary singularities or extra zero modes | Exactly one finite smooth cavity is used per `q`. The domains for different `q` are separate objects; no infinite accumulation, nesting, or repeated-hole limit is asserted. |
| Connecting the two boundary components is a routine extension | It would require additional spectral control and is not established by this geometry audit or the candidate. That route remains unsupported without a new mechanism. |

At `q=1` the geometric parameters are positive and the same existence proof applies. There is no exceptional critical parameter at small `q`; the later large-`q` argument is not needed for existence. The dimension is fixed before `q` varies.

## Handoff to the independent spectral family

The geometric output needed downstream is fully supplied: area `q+rho_m`, fixed positive volume lower bound, outer component the unit sphere, inner component connected with gap strictly above `T_q=q(q+m-1)`, and exactly two boundary components. These facts imply

`I(Omega_q)^(1+2/m) <= [omega_(m+1)(1-2^(-(m+1)))]^(-(m+2)/(m+1)) (q+rho_m)^(1+2/m)`.

The volume exponent follows from `(m/(m+1))(1+2/m)=(m+2)/(m+1)`. The exact sphere eigenvalue rank, zero-mode bookkeeping and final universal-constant contradiction are assigned to the independent spectral family. I have not made my geometric verdict depend on that family's result.

## Source access and verification limits

Fresh retrieval succeeded with HTTP 200 for CDE, DLS, OWR, CEG and Hatcher's chapter. Their metadata are in `SOURCE_RECEIPTS.json`. Relevant pages were rendered locally and visually inspected: CDE 6,14,15; DLS 4; OWR 22-24 (the complete talk); CEG 1,2,14; Hatcher chapter 71,72 (printed 255-256). Original/captured computational artifacts were not run, and no numerical embedding is claimed.

The original Nash and Kuiper papers were not separately retrieved; the exact modern theorem statement was inspected directly. Hirsch's book was not separately retrieved; CDE's explicit use of smooth approximation was inspected, and the needed compact smoothing/stability argument was reconstructed above. The underlying Colbois-Dodziuk and arithmetic-surface existence results were not independently reproved; CDE Theorem 1.4 is the established input. An attempted web access to McGrath's smooth Jordan-Brouwer note returned 403; it is not relied upon. Hatcher's accessible primary textbook interface supplied an independent topology check instead.

This audit does not determine whether the cavity combination already appears elsewhere. It does not turn an internal mathematical verdict into journal acceptance or a current-publication claim. The remaining external novelty/publication checks belong to the parent task; there is no unresolved geometric proof gap within the stated scope.

Final checkpoint: 2026-10-21T23:55:27.426005+00:00. Estimated completion of this geometric audit: 100%.
