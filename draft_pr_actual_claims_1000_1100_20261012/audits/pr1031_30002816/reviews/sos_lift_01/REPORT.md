# Independent family B: SOS, lift, source, and calibration audit

**Audit target:** PR #1031, problem 30002816 / OWR-13498-004. Submitted head: `f6570e093267a7f910faf9cdd60dfbc1c12f5681`. Authored 2026-10-13 UTC. This is an independent adversarial reconstruction, not an adoption of the submitted acceptance language.

**Verdict in the assigned family:** CLEAN, with the geometric section equality explicitly conditional. The source conventions, the all-affine-SOS-to-finite-lift implication, rational separating-coefficient existence, positive comass normalization, and the pointwise completion argument are correct. Assuming the independently audited geometric identity

\[
C_{4,12}\cap\{\Phi=1,Q=0\}\cong\operatorname{Sep}_{\mathbb C}(3,3)
\]

is an exact affine section followed by a real-linear isomorphism, the submitted existential negative conclusion follows from the actual published Fawzi theorem. No mathematical defect was found in this family's assigned steps. This report does not independently certify the geometry bridge, priority, minimal dimension, an explicit calibration, or publication readiness.

## 1. Independence and falsifiable claim

Only `submitted/current/PROOF.md` was read as a proposed proof; `submitted/historical/SOURCE_METADATA.json` supplied source URLs. Historical acceptance, current audit/priority reports, and other-family findings were not read. No other family was contacted. All files written by this family are under `reviews/sos_lift_01/`; there were no shared Git/index edits, service mutations, publication actions, or external communications.

The exact negative target is

\[
\exists c\in\mathbb R^{495}:\quad
 h_X(c)-c\cdot p\ne\sum_{j=1}^{r}(a_j+b_j\cdot p)^2\quad
\text{as functions on }X=X_{4,12},
\]

for every finite list of real coefficients, where `h_X(c)=max_{p in X} c.p`. Equivalently, the discrepancy does not lie in the real vanishing ideal. Its stronger proposed geometric antecedent is that `C=conv(X)` has no finite semidefinite lift.

Success criteria for this family were: original source quantifiers match the target; the external theorem applies to normalized complex `Sep(3,3)` and arbitrary projected finite lifts; the finite moment argument has no hidden closure, duality, degree, or ideal assumption; strict separation yields a rational coefficient vector; normalization has positive denominator; the four-form belongs to the original calibration setting; and a local completion would contradict the pointwise obstruction. Counterexample attempts are in Section 8 and in executable exact controls.

## 2. Original problem: what is actually quantified

Fresh original source: [Sanyal, Grassmann Orbitopes, OWR 13/2015](https://ems.press/content/serial-article-files/46561), printed pp.708-709, PDF pages 48-49. Both complete pages were extracted and rendered; the images were visually inspected. Source bytes match the submitted pin independently.

The report uses the orthogonal-group orbit corresponding to **oriented** planes, hence both signs of each unit simple vector. Its optimization target is `delta - ell`, and `D` bounds the degrees of the square roots `h_i`. The `n <= 7` sentence reports computational exploration; the following conjecture covers **all** Grassmann orbitopes. Its ideal is the vanishing ideal of the unit Grassmannian, with Plucker relations and the sphere relation. The immediately preceding equation fixes the meaning of the shorthand about calibrations: it concerns `1 - phi`, not a literal SOS for `phi`.

Thus the precise universal clause is

\[
\forall(k,n),\ \forall \ell,\quad
\delta=\max_{p\in X_{k,n}}\ell(p)
\implies\delta-\ell\in\Sigma_{\le1}+I(X_{k,n}).
\]

Polynomial degree at most one allows a constant term. Interpreting the shorthand as strictly homogeneous linear squares would make every nonzero supporting functional impossible by antipodal parity; the degree-bound formulation removes that ambiguity. The proposed counterexample fails even with constants allowed, the stronger certificate class.

An existential failure at `(k,n)=(4,12)` is a complete logical refutation of this universal clause. It does not settle the experimental low-dimensional cases. Also, `(4,12)` belongs to the nontrivial range `2 < k < n-2` discussed by the source. The source has an evident index typo in its representative wedge on p.708 (`e_n` in an exterior-power discussion); its oriented-plane description makes the intended unit `k`-vector unambiguous. The audit does not use that typo literally.

The argument below works with the **full** real vanishing ideal. It therefore remains valid even if the Plucker-plus-sphere generated ideal were smaller than the full ideal: ruling out a certificate modulo the full ideal rules it out modulo every subideal. No radicality or chosen generator presentation is silently needed.

## 3. Independent derivation of the finite compact moment lift

Let `X` be any nonempty compact subset of the Euclidean unit sphere in `R^N`, and let `C=conv(X)`. Compactness of `C` follows from Caratheodory's theorem: it is the image of the compact space of at most `N+1` points of `X` and their simplex weights.

Set

\[
J_2=I(X)\cap\mathbb R[p_1,\ldots,p_N]_{\le2}.
\]

This is a vector space, of dimension at most `(N+1)(N+2)/2`, so it has a finite basis, whether or not an effective basis-construction algorithm is supplied. The lift definition is existential and permits arbitrary real coefficients. For a real symmetric matrix `M` indexed by `0,1,...,N`, define

\[
L_M(1)=M_{00},\quad L_M(p_i)=M_{0i},\quad
L_M(p_i p_j)=M_{ij}.
\]

These values define a well-defined linear functional on all degree-at-most-two polynomials; off-diagonal monomials are taken once as polynomial coefficients, so there is no factor-of-two ambiguity.

Define

\[
S=\{M\succeq0:M_{00}=1,\ L_M(g)=0\text{ for a basis of }J_2\},
\quad T=\{(M_{01},\ldots,M_{0N}):M\in S\}.
\]

All equalities are affine linear in matrix entries; imposing a basis is equivalent to imposing every element of `J_2`. This is a finite spectrahedron with a linear projection. If one insists on the single-LMI definition without displayed equations, any equality `f(M)=0` can be imposed by the two scalar PSD blocks `f(M)` and `-f(M)`; alternatively, one can eliminate the equations and parameterize their affine solution space.

The rank-one matrix `v_p v_p^T`, with `v_p=(1,p)`, is feasible for every `p in X`: `L(g)=g(p)=0`. Taking convex combinations establishes `C subseteq T`, as well as nonempty feasibility.

Since `1-sum_i p_i^2` belongs to `J_2`, every feasible matrix satisfies

\[
\sum_{i=1}^N M_{ii}=1,\qquad\operatorname{tr}M=2.
\]

For a PSD matrix, `|M_ij|^2 <= M_ii M_jj`. Its diagonal entries are nonnegative and bounded by the fixed trace, so every entry is bounded. The PSD cone and the finite equations are closed. Thus `S` is compact, and its continuous image `T` is compact. This checks the normally dangerous projection-closedness issue directly. In block form `M=[[1,x^T],[x,Q]]`, the Schur complement is `Q-xx^T >= 0`, and taking traces gives `||x||^2 <= tr(Q)=1`. In particular `T` also lies in the Euclidean unit ball.

Now assume every support function has a finite affine SOS representation on `X`. For any real linear functional `ell`, set `delta=max_X ell`, and write

\[
\delta-\ell(p)=\sum_j(a_j+b_j\cdot p)^2\quad(p\in X).
\]

The polynomial difference has degree at most two and vanishes on `X`. It therefore lies in `J_2`, regardless of how an ideal generator expression might use higher-degree intermediate terms. If `u_j=(a_j,b_j)`, feasibility implies

\[
\delta-\ell(x)=\sum_j u_j^T M u_j\ge0
\quad(M\in S).
\]

Every `x in T` satisfies every supporting halfspace of `C`. If `x` were outside the compact convex set `C`, ordinary strict separation would produce a violated supporting halfspace. Hence `T subseteq C`, so `T=C`. This constructs a finite semidefinite lift. There is **no** optimization duality, Slater condition, dual attainment, hierarchy convergence, or equality between a generator truncation and `J_2` in this proof.

For the target `N=binom(12,4)=495`, the PSD moment block has size 496, and the ambient polynomial space in degree at most two has dimension 123256. Its finiteness is sufficient; no quadratic-ideal basis file is needed for the logical implication.

## 4. The exact external interface

Fresh primary body: [Fawzi, published Communications in Mathematical Physics article](https://www.repository.cam.ac.uk/bitstreams/e6e52df9-b317-4616-9462-c79a3cb4844b/download), DOI [10.1007/s00220-021-04163-2](https://doi.org/10.1007/s00220-021-04163-2). The journal header specifies volume 386, pp.1319-1335 (2021), accepted 30 June 2021, published online 31 July 2021. This is the published body, not an unpinned arXiv draft.

On pp.1319-1321 the paper defines `Sep(n,m)` using unit complex product projectors and defines a representation as a **linear image of an arbitrary finite Hermitian LMI spectrahedron**. Theorem 1 rules out such representations when `Sep != PPT`; `(3,3)` is expressly included and is treated in its proof. The paper distinguishes this result from positive-map-only representations and fixed hierarchy levels. Real symmetric LMIs are a subclass of Hermitian LMIs, so the real lift from Section 3 falls within the excluded class.

Affine sections preserve representability: if `C=pi(S)`, then `C intersect {Lx=b}` is exactly the image of `S intersect {L pi(s)=b}`. There is no need for the section to be a face, exposed, or transverse. Any additional real-linear map of the image preserves representability. A real-linear inverse on a subspace can be extended to the full ambient space by choosing a vector-space complement. Thus the stated exact section equality would contradict the published theorem if `C_4,12` had a lift.

### Dependency checks beyond reading a theorem label

I read the published general theorem and lift argument, pp.1322 and 1327-1331, including the downward-closed support condition, the finite semialgebraic factor functions, facial reduction/strict feasibility used in the external duality step, coefficient bounds, and the dehomogenized `(3,3)` application. These are dependencies of Fawzi's theorem, not assumptions imported into Section 3 above. This review is not a complete new proof of Fawzi's analytic/semialgebraic theorem.

The main hidden-assumption attacks have explicit resolutions:

1. **Complex versus real SOS.** The external paper uses squares of real-valued Hermitian polynomials, equivalent under `z=a+ib` to real polynomial squares. It is not using only holomorphic modulus squares. The target obstruction is genuinely to Hermitian lifts and covers real lifts.
2. **Nonhomogeneous supports.** The general theorem requires downward closure. The direct biform support is not downward closed, so the proof dehomogenizes before applying it. The `(3,3)` dehomogenization has degree at most one in each of the four complex/conjugate coordinate blocks, a downward-closed set.
3. **Dehomogenizing non-SOS forms.** This can fail for general Hermitian forms. For the Choi polynomial used in `(3,3)`, its restriction to real variables is non-SOS. A real SOS after dehomogenization would have square roots of separate degree at most one in the `x` variables and in the `y` variables, since sums of real squares cannot cancel their highest separate-degree terms. Multiplying each root by `x_3 y_3` after replacing affine variables by the corresponding ratios would give a real bilinear SOS for the original form, a contradiction. This does not assume the invalid general Hermitian dehomogenization rule.
4. **Normalized body versus cone.** This is not needed merely to invoke the printed normalized theorem, but the interface can be checked independently. Suppose the compact trace-one body has lift `pi{w:M0+M(w)>=0}`. Its cone has the homogeneous lift with `t>=0`, `t M0+M(w)>=0`, projected to `pi(w)`. For `t>0` the output is `t C`. If `t=0`, `M(w)>=0` is a recession direction: choose any feasible `w0`, and `w0+lambda w` stays feasible. Boundedness of `C` forces `pi(w)=0`. Thus there is no spurious nonzero output at `t=0`, and the cone is exactly represented. Conversely, the trace-one section of a cone lift represents the body.
5. **The closed affine moment slice.** In the `(3,3)` proof, the closure of the dehomogenized moment hull equals the cone slice where the last product diagonal coordinate is one. Generators with last product coordinate zero can be approximated by generators with nonzero coordinate; a finite sum approaching a slice point can be rescaled by its total last coordinate, which tends to one. This produces convex combinations of dehomogenized points. The reverse inclusion follows from closedness of the cone slice. This checks the zero-coordinate limit rather than silently discarding those generators.

A source boundary worth preserving: a blanket `n+m>5` shorthand cannot be extended to the trivial `m=1` case, where `Sep(n,1)=PPT(n,1)` is a trace-one PSD body for every `n`. The theorem's primary premise `Sep != PPT`, and its explicit `(3,3)` application, remove this issue for the submitted specialized statement. No general conclusion about the one-factor boundary is used.

## 5. Independently checked Choi constituent

This calculation checks a source constituent without claiming to reprove the external no-lift theorem. Write the published `(3,3)` biform as

\[
p(x,y)=\sum_i |x_i y_i|^2
-2\sum_{i<j}\operatorname{Re}(x_i\overline{x_j}y_i\overline{y_j})
+2(|x_1y_2|^2+|x_2y_3|^2+|x_3y_1|^2).
\]

Set `a=|x1|^2`, `b=|x2|^2`, `g=|x3|^2`. As a Hermitian quadratic form in `y`, its diagonal entries are `a+2g`, `b+2a`, `g+2b`; off-diagonal entries have modulus squared `ab`, `ag`, `bg`, and their cyclic product is `-abg`. All one- and two-dimensional principal minors are nonnegative. Direct exact expansion gives

\[
\det=4(a^2b+b^2g+g^2a+abg)\ge0.
\]

The principal-minor criterion proves complex nonnegativity, including zero-coordinate cases. The script verifies all polynomial expansions with exact fractions.

For real non-SOS, any hypothetical polynomial SOS must have real bilinear square roots: total and separate homogeneity follow by noncancellation of leading square terms. Zero coefficients of `x1^2 y3^2`, `x2^2 y1^2`, and `x3^2 y2^2` force those bilinear monomials to have zero coefficients in every root. Consequently the principal Gram block indexed by `x1y1,x2y2,x3y3` is forced to be

\[
G=\begin{pmatrix}1&-1&-1\\-1&1&-1\\-1&-1&1\end{pmatrix}.
\]

The other cross products that could share its coefficient monomials contain excluded monomials. But `(1,1,1) G (1,1,1)^T=-3` and `det(G)=-4`; it cannot be a principal block of any PSD Gram matrix. This independently establishes the needed real non-SOS property.

## 6. Strict containment, rational coefficients, and positive normalization

Assume the geometric section identity, hence the established no-lift conclusion for `C`. Section 3 gives `C subseteq T`, with `T` compact. Equality would itself provide a lift, so there exists `x in T minus C`. This is a nonconstructive existence statement, not a claim to have numerically identified such a moment matrix.

Strict separation gives a real `c` with

\[
\Delta=c\cdot x-h_X(c)>0.
\]

Because `X` lies in the unit sphere,

\[
|h_X(d)-h_X(c)|\le\|d-c\|.
\]

Also `||x||<=1` by the moment Schur-complement argument. Therefore

\[
d\cdot x-h_X(d)\ge\Delta-2\|d-c\|.
\]

Choose a rational `d` with `||d-c||<Delta/2`. The separation remains strict. Rational vectors are dense in the fixed real Plucker coordinate space; an open positive margin is exactly what makes this argument possible. For any feasible moment matrix projecting to `x`, an affine SOS for `h_X(d)-d.p` would evaluate to a nonnegative sum of quadratic forms, contradicting the strictly negative value at `x`.

This proves **existence of a rational coefficient vector**, not a displayed vector, a rational support value, or a rational coefficient vector after comass normalization. None of those stronger constructive assertions is made by the submitted proof.

Since each coordinate simple wedge and its negative belongs to `X_4,12`,

\[
\delta=h_X(d)\ge\max_I |d_I|>0.
\]

The final strict inequality holds because a separating vector is nonzero. Thus `phi=d/delta` has maximum one and, by antipodal symmetry, comass one. Scaling an SOS by the positive number `delta` in either direction preserves its existence, so `1-phi` remains non-affine-SOS. A compact maximum is attained. The use of spanning coordinate vectors is necessary here: on a nonspanning general `X`, a nonzero ambient linear functional can have maximum zero.

## 7. Harvey-Lawson: pointwise and local meanings

Fresh original body: [Harvey-Lawson, Calibrated geometries](https://archive.ymsc.tsinghua.edu.cn/pacm_download/117/6313-11511_2006_Article_BF02392726.pdf), DOI [10.1007/BF02392726](https://doi.org/10.1007/BF02392726). The complete relevant pages were read: printed p.56 defines comass on unit simple vectors; p.57 defines the maximizing geometry; p.59 defines a calibration by comass one and closedness; p.68 contains Question 6.5 and equation (6.6). The critical definition/question pages were rendered and visually inspected. The question allows a finite local collection of differential `p`-forms whose squared evaluations complete the norm on all simple `p`-vectors.

At one Euclidean tangent space, a differential `k`-form is exactly a real linear functional on `Lambda^k R^n`. Suppose such linear forms satisfy

\[
\phi(p)^2+\sum_j\psi_j(p)^2=\|p\|^2
\]

for every decomposable vector. On unit decomposable vectors,

\[
1-\phi=\frac12(1-\phi)^2+\frac12\sum_j\psi_j^2.
\]

Both roots `(1-phi)/sqrt(2)` and `psi_j/sqrt(2)` are affine linear on the Plucker ambient space. Therefore failure of the affine SOS property immediately prevents the pointwise completion.

For the reverse implication, assume `phi` has attained comass one and

\[
1-\phi(p)=\|a+Bp\|^2\quad(p\in X_{k,n}).
\]

Using `p` and `-p`, subtract and add the equations:

\[
a^TBp=-\phi(p)/2,\qquad \|a\|^2+\|Bp\|^2=1.
\]

The coordinate wedges span the full exterior space, so the first relation also identifies the ambient covector `B^T a=-phi/2`. Let `p0` attain `phi(p0)=1`. The SOS is zero there, giving `Bp0=-a`. At `-p0`, its squared value is `||2a||^2=2`; consequently `||a||^2=1/2`. The denominator in the projection below is therefore nonzero. Let `P=I-aa^T/||a||^2`. Then on `X`,

\[
\|\sqrt2 PBp\|^2
=2\|Bp\|^2-2\frac{(a^TBp)^2}{\|a\|^2}
=1-\phi(p)^2.
\]

Its components give the required homogeneous linear forms. For a nonzero simple vector `q`, write `q=||q|| p` with `p in X`; all forms are homogeneous, so multiplication by `||q||^2` extends the identity. The zero vector satisfies it trivially. This proves the **pointwise** equivalence under the exact antipodal, spanning, and attained-comass-one hypotheses present here.

A pointwise affirmative construction for arbitrary varying forms does not automatically prove smooth local choices; this report makes no such extra assertion. The negative direction is sufficient: a putative local collection of differential four-forms can be evaluated at any point, producing the forbidden pointwise completion.

Finally regard the normalized failing covector as the constant four-form

\[
\varphi=\sum_{|I|=4}(d_I/\delta)\,dx_I
\quad\text{on }\mathbb R^{12}.
\]

It is smooth and `d varphi=0` since its coefficients are constant. Its comass is one at every point, and its maximizing oriented planes are nonempty there. It therefore fits the original calibration/geometry definitions, not merely an unrelated unclosed tensor. No local completion is possible at any point because the same pointwise obstruction occurs in every tangent space.

## 8. Adversarial controls and boundaries

`exact_controls.py` uses only Python's exact `Fraction` arithmetic; all eight checks pass. Its output is `EXACT_CONTROLS.json`. The controls are intentionally small and independent of a SDP solver.

- **Full ideal cannot be discarded.** For `X={(1,0),(-1,0)}`, the sphere-only rank-one moment at `(0,1)` is PSD of trace two but violates the full-ideal relation `p2=0`. Its evaluation of the supporting function `0-p2` is `-1`. The full `J_2` excludes it.
- **Degree restriction is material.** Let `X={+/- (1,0), +/- (3/5,4/5), +/- (3/5,-4/5)}`. Exact degree-two evaluation rank is five out of six, so `J_2` is just the sphere relation and `T` is the disk, while `C` is a hexagon. For `ell=p2`, `delta=4/5`, the disk point `(0,1)` violates the support by `1/5`; no affine SOS is possible. Nevertheless on `X`,
  \[
  4/5-p2=(4/5)(1-25p2^2/16)^2
       +(8/5)(25p2^2/32-5p2/8)^2.
  \]
  This valid degree-two-root SOS has a degree-four discrepancy, outside the defined moment functional. It confirms that replacing the roots' degree bound by unrestricted SOS would break Section 3's inference. The hexagon also has a finite polyhedral/semidefinite lift, so the converse "a finite lift implies this particular affine SOS property" is false. The submitted proof uses only the correct forward direction.
- **Projection closure requires justification.** `[[x,1],[1,y]]>=0` projects to `x>0`, excluding its limiting point zero. Exact feasible pairs `(1/k,k)` confirm the issue. The submitted sphere-trace bound prevents this example's unbounded lift mechanism.
- **Normalization hypotheses matter.** A nonzero covector annihilating `X={(1,0),(-1,0)}` has support value zero, so one cannot infer a positive denominator for an arbitrary sphere subset. The target coordinate wedges span and prevent this.
- **Orientation hypotheses matter.** Sums of homogeneous squares are even under `p -> -p`; `delta-ell` is not even for nonzero `ell`. Constants and both orientations were independently checked against the original degree formulation.
- **Positive cases do not conflict.** On the unit circle, for any unit covector `u`, `1-u.p=||p-u||^2/2`; the completion is the projection orthogonal to `u`. A rational nontrivial example `u=(3/5,4/5)` and a rational interior moment matrix are checked exactly, including PSD principal minors and trace.
- **External constituent check.** The Choi principal-minor nonnegativity and forced non-PSD Gram block from Section 5 are independently verified by exact polynomial expansion.

These are meaningful falsification controls, not computation of the target's ideal, a target moment witness, or certification of a target SDP infeasibility claim. The target conclusion remains a deduction using the independently audited section equality plus a published theorem.

## 9. Frozen evidence and remaining gap

`INPUT_PINS.json` pins the read submitted proof and URL metadata. `sources/SOURCE_PINS.json` pins fresh downloaded source bytes, source URLs, redirect target, exact sizes, retrieval timestamps, printed/PDF pages, and visual-inspection status. All downloaded PDFs, their extracted text, and rendered original-source images are confined to `sources/raw/`. Authored reports and hash metadata are outside `raw/`. `OUTPUT_PINS.json` freezes the authored report, exact-control code/output, verdict, and final log checkpoint.

The strongest verified result in this family is the following conditional theorem:

> If `C_4,12` has the stated exact section isomorphic to normalized complex `Sep(3,3)`, then `C_4,12` has no finite semidefinite lift, and there exists a rational-coefficient linear functional whose supporting function admits no finite affine-linear SOS modulo the full real vanishing ideal. Its normalized constant closed four-form defeats the pointwise completion in Harvey-Lawson Question 6.5 and hence defeats any local completion.

The only mathematical input outside this family's independent derivation is the geometry bridge assigned to the other independent family, together with Fawzi's published no-lift theorem as the declared external theorem. No gap remains in the assigned SOS/source family. Novelty and priority remain unestablished; minimal dimension and an explicit rational coefficient list remain unproved and unclaimed. The full submitted result must not be promoted solely on this conditional family verdict.
