# A smooth harmonic sphere with unbounded distortion for Reshetnyak energy

Problem 30006419, OWR-14299521-012, rank 969. Authored candidate, 7 October 2026. AI-assisted and unrefereed. Independent audit pending. No historical novelty claim.

## 1. Exact claim and the energy distinction

**Theorem.** There is a compact smooth Riemannian surface (X), diffeomorphic to (S^2), and a smooth homeomorphism (u:S^2\to X) such that:

1. (X) is geodesic, satisfies a local quadratic isoperimetric inequality, and every sufficiently small-diameter continuous sphere in (X) is null-homotopic.
2. (u) is locally minimizing for the Reshetnyak energy (E_+^2): each point has a neighborhood (U) on which every relatively compact Lipschitz subdomain admits no lower-energy Sobolev competitor with the same trace.
3. No finite constant (Q) bounds the ratio of the largest to the smallest infinitesimal stretch almost everywhere.

Consequently the general-energy version of the question is **negative**. This example is not harmonic for the Korevaar–Schoen/ordinary Dirichlet energy. It does not contradict the classical conformality theorem for Dirichlet-harmonic spheres, and it does not answer a separately restricted Korevaar–Schoen question.

The energy parameter is essential. The Oberwolfach discussion fixes a suitable energy before posing Question 1. Its cited paper, Meier–Vikman–Wenger, arXiv:2503.08553v1, permits the Reshetnyak energy in Definition 3.1 and uses the neighborhoodwise, fixed-trace definition in Definition 6.1. The same question appears as Question 1.9. This is the precise interpretation addressed here. Global minimization in a homotopy class is a different hypothesis.

For a map into a smooth Riemannian target, write

\[
 E_+(v;\Omega)=\int_\Omega \|dv\|_{\rm op}^2\,dA.
\]

This agrees with the source's (E_+^2). In dimension two it is invariant under conformal changes of the domain metric. If the singular values of (dv) are (\sigma_1\geq\sigma_2\geq0), then its density is (\sigma_1^2), whereas the Korevaar–Schoen normalization used in the source has density (\sigma_1^2+\sigma_2^2).

## 2. Two comparison lemmas allowing arbitrary competitors

### Lemma 1: a scalar calibration in a flat target patch

Let a target neighborhood have Euclidean coordinates ((s,y)). Suppose a smaller neighborhood (V) has the property that its coordinate (y) is 1-Lipschitz for the distance of the entire target. Let (U\subset\mathbb R^2), with coordinates ((t,x)), and let

\[
 u(t,x)=(h(t),x)\in V,\qquad |h'(t)|\leq1.
\]

Then (u) minimizes (E_+) on every relatively compact Lipschitz (\Omega\subset U), against all target-valued (W^{1,2}) competitors of matching trace, including those leaving (V).

**Proof.** The McShane formula

\[
 F(q)=\inf_{p\in V}\{y(p)+d_X(p,q)\}
\]

extends (y) to a globally 1-Lipschitz real function on (X). The finite values of (y) on (V) make this formula finite in the compact target used below. For a competitor (v), put (f=F\circ v). The Sobolev chain and trace properties give (f\in W^{1,2}(\Omega)), (\operatorname{tr}f=x), and

\[
 \int_\Omega |\nabla f|^2\leq E_+(v;\Omega).
\]

Writing (w=f-x\in W^{1,2}_0(\Omega)), density of compactly supported smooth functions gives (\int_\Omega\partial_xw=0). Hence

\[
 \int_\Omega |\nabla f|^2=|\Omega|+\int_\Omega|\nabla w|^2\geq|\Omega|.
\]

On the other hand (du=\operatorname{diag}(h',1)), so (E_+(u;\Omega)=|\Omega|). This proves the claim. Domain conformal factors cancel from every displayed energy. \(\square\)

The distance requirement on (V) is important: a local coordinate need not be globally 1-Lipschitz merely because its pointwise gradient has norm one. In a smooth Riemannian target one may take a sufficiently small strongly geodesically convex ball contained in a flat coordinate patch. The minimizing geodesic between any two of its points stays in that ball, and the coordinate difference is at most its length. Thus (V) satisfies the required ambient-distance condition.

### Lemma 2: conformal patches on an oriented smooth sphere

Let (X) be any oriented compact smooth Riemannian sphere and let (u) be a smooth orientation-preserving conformal map on a domain neighborhood. Every point has a smaller neighborhood (U) such that (u|_\Omega) minimizes (E_+) for every relatively compact Lipschitz (\Omega\subset U), against all (X)-valued (W^{1,2}) competitors of the same trace.

**Proof.** Let (A=\operatorname{Area}(X)). Shrink (U) so that (u(\overline U)) lies in an open target set supporting a smooth function (\eta:X\to[0,1]) with (\eta=1) near (u(\overline U)) and

\[
 0<m:=\int_X\eta\,dA<A/2.
\]

Such a cutoff exists by taking a sufficiently small image neighborhood. Put

\[
 b=\frac{m}{A-m}<1,\qquad
 \omega=((1+b)\eta-b)\,dA.
\]

The two-form (\omega) has comass at most one, is the area form near the image of (u), and satisfies (\int_X\omega=0). Since integration identifies (H^2_{\rm dR}(S^2)) with (\mathbb R), there is a smooth one-form (\alpha) on (X) with (d\alpha=\omega).

For every Sobolev competitor (v), the pointwise singular-value inequality gives

\[
 v^*\omega\leq |\operatorname{Jac}v|\,dA_{\rm domain}
 \leq \|dv\|_{\rm op}^2\,dA_{\rm domain}.
\]

For (u), both inequalities are equalities because (u) is conformal and orientation-preserving and (\omega=dA) on its image. It remains to verify the boundary-invariance identity for Sobolev, rather than merely smooth, competitors:

\[
 \int_\Omega v^*\omega=\int_\Omega u^*\omega. \tag{1}
\]

Here is a direct justification that does not assume density of smooth sphere-valued maps. A smooth one-form on a compact smooth manifold has a finite representation

\[
 \alpha=\sum_j f_j\,dg_j
\]

with globally smooth real functions (f_j,g_j). To obtain it, use a finite coordinate cover, a subordinate partition of unity, and extend the coordinate functions with cutoffs equal to one near the supports of the partition. The scalar functions are bounded and Lipschitz. For a metric Sobolev map (v), define (v^*\alpha=\sum_j(f_j\circ v)d(g_j\circ v)). The scalar Sobolev product identity, proved by ordinary Euclidean mollification, gives distributionally

\[
 d(v^*\alpha)=\sum_j d(f_j\circ v)\wedge d(g_j\circ v)=v^*(d\alpha).
\]

The left pullback is locally (L^2) and the two-form on the right is (L^1). Strong (W^{1,2}) scalar approximation justifies the wedge products in (L^1); bounded coefficients justify the one-form limit. The usual chain rule identifies this definition with the differential pullback almost everywhere.

Glue (v) inside (\Omega) to (u) outside (\Omega), obtaining a Sobolev map (\widetilde v:U\to X), since the traces agree. The (L^2) one-form (\beta=\widetilde v^*\alpha-u^*\alpha) is supported in (\overline\Omega\Subset U). Pair (d\beta) with a smooth cutoff equal to one near (\overline\Omega). Integration by parts gives zero because the derivative of the cutoff misses the support of (\beta). Since (d\beta=\widetilde v^*\omega-u^*\omega), this proves (1). Integrating the energy inequality now proves minimality. \(\square\)

The elementary Sobolev facts used here are Lipschitz composition, the trace/gluing property on Lipschitz domains, and scalar weak product/chain rules. No continuity, image restriction, homotopy constraint, or bound on the energy of a competitor is imposed.

## 3. An explicit compact smooth target

Use the cylinder (\mathbb R\times(\mathbb R/2\pi\mathbb Z)), with coordinates ((s,\theta)), and adjoin one point at each end. These are the usual two-pole coordinates on a smooth sphere: near the negative end use (z=e^{s+i\theta}), and near the positive end use (\zeta=e^{-s-i\theta}).

Choose a smooth function (\chi:[0,\infty)\to[0,1]), equal to zero for (r\leq2) and one for (r\geq3), and set

\[
 \rho(s)=\exp(-|s|\chi(|s|)),\qquad
 g_X=\rho(s)^2(ds^2+d\theta^2). \tag{2}
\]

For an entirely specified cutoff one may take (B(x)=0) for (x\leq0), (B(x)=e^{-1/x}) for (x>0), and (\chi(r)=B(r-2)/(B(r-2)+B(3-r))). The denominator never vanishes. The apparent absolute value in (2) causes no nonsmoothness at zero because the exponent is identically zero near zero.

For (s\leq-3), (\rho(s)=e^s), so the metric is exactly (|dz|^2). For (s\geq3), it is exactly (|d\zeta|^2). Thus (2) extends to a positive smooth metric at both added points. In particular (X) is a compact smooth Riemannian sphere. The belt (|s|\leq2) is a genuine flat cylinder.

All target assumptions can be checked without singular-space existence results:

- Compactness gives completeness; the Riemannian length metric is geodesic, hence 1-quasiconvex.
- Compactness supplies a uniform radius for contractible normal balls. Any map whose image diameter is smaller than that radius has its image in one such ball, and is null-homotopic there.
- A finite collection of uniformly biLipschitz coordinate charts proves a local quadratic isoperimetric inequality. Indeed a sufficiently short loop lies in a smaller chart and in a convex Euclidean coordinate ball. Cone it to one of its points. If (L) bounds the two chart Lipschitz constants, its cone area after returning to (X) is at most (L^4\ell(\gamma)^2/4): the Euclidean loop length is at most (L\ell(\gamma)), its distance from the chosen loop point at most (L\ell(\gamma)/2), and the cone area is at most half the product. A uniform sufficiently small length threshold ensures that this cone remains in the chart. The cone is a Sobolev filling with exactly the prescribed boundary parametrization.

## 4. A smooth homeomorphism with a compressed equator

Give the domain (S^2) its standard round metric. On its cylinder coordinates ((t,\theta)), that metric is

\[
 g_0=\operatorname{sech}^2(t)(dt^2+d\theta^2).
\]

Choose a smooth even cutoff (\eta_0:\mathbb R\to[0,1]), equal to one for (|t|\leq1/4) and zero for (|t|\geq1/2). For example put (H(x)=B(x)/(B(x)+B(1-x))), using (B) above, and

\[
 \eta_0(t)=1-H((16t^2-1)/3).
\]

Define

\[
 a(t)=\eta_0(t)t^2+1-\eta_0(t),\qquad
 h(t)=\int_0^t a(r)\,dr. \tag{3}
\]

Then (a) is smooth and even, (0\leq a\leq1), it vanishes only at zero, it equals (t^2) for (|t|\leq1/4), and equals one for (|t|\geq1/2). Hence (h) is a smooth strictly increasing odd homeomorphism of the real line and

\[
 h(t)=t^3/3\quad(|t|\leq1/4),
\]

\[
 h(t)=t-c\quad(t\geq1/2),\qquad
 h(t)=t+c\quad(t\leq-1/2),
 \quad c=\int_0^{1/2}(1-a(r))\,dr\in(0,1/2). \tag{4}
\]

Define

\[
 u(t,\theta)=(h(t),\theta), \tag{5}
\]

and send the two domain poles to their corresponding target poles. Strict monotonicity of (h) proves that (u) is a homeomorphism. It is also a smooth map, although its inverse need not be smooth: in the negative pole charts (4) gives (z_{\rm target}=e^c z_{\rm domain}), and in the positive pole charts it gives the same linear scaling. Away from the poles smoothness follows from (3). Smoothness on a compact domain implies (u\in W^{1,2}(S^2,X)).

## 5. Local harmonicity with the exact quantifier

Let (p) be a domain point with (|t(p)|<1). Since (|h(t)|\leq|t|), a small neighborhood of (p) maps inside the flat belt. Choose a still smaller source coordinate neighborhood (U) whose image lies in a strongly convex target ball, lift its angular coordinate to a real coordinate (x), and apply Lemma 1. This proves minimality for every relatively compact Lipschitz (\Omega\subset U), against every (W^{1,2}(\Omega,X)) map with matching trace.

If (|t(p)|>1/2), or if (p) is a pole, (4) shows that (u) is orientation-preserving conformal on a neighborhood of (p). At finite (t), its coordinate derivative is the identity and both metrics are scalar multiples of the cylindrical Euclidean metric. The pole maps are complex linear scalings. Lemma 2 therefore supplies exactly the same fixed-trace minimality conclusion.

The open sets ({|t|<1}) and ({|t|>1/2}\cup\{\text{poles}\}) cover the sphere and overlap. There is no untreated seam at (|t|=1/2) or (|t|=1). Thus (5) is (E_+)-harmonic in the precise neighborhoodwise sense stated in Section 1.

## 6. Failure of infinitesimal quasiconformality

On (0<|t|<1/4), the target is flat and the differential in the cylindrical Euclidean metrics has singular values (1) and (t^2). Multiplication by the domain conformal factor changes both singular values by the same amount. Consequently

\[
 \frac{\sigma_{\max}(du)}{\sigma_{\min}(du)}=\frac1{t^2}. \tag{6}
\]

For every finite (Q\geq1), the open band

\[
 0<|t|<\min\{1/4,\,1/(2\sqrt Q)\}
\]

has positive round area, and on it (6) is larger than (Q). The failure is therefore an essential-unboundedness failure on positive-measure sets, not merely the rank defect on the measure-zero equator. There is no finite infinitesimal quasiconformality constant. This completes the theorem. \(\square\)

## 7. Checks distinguishing the nearby statements

### It is not a global homotopy minimizer

The coordinate map (f(t,\theta)=(t,\theta)) is a smooth conformal degree-one homeomorphism from the domain to (X), and is homotopic to (u). It has (E_+(f)=\operatorname{Area}(X)). In contrast, the only nonconformal part of (u) lies in the flat belt, and change of variables (s=h(t)) gives

\[
 E_+(u)-\operatorname{Area}(X)
 =2\pi\int_{-1/2}^{1/2}(1-a(t))\,dt=4\pi c>0. \tag{7}
\]

This directly verifies why the previously proved global-homotopy-minimizer result does not rule out the example.

### It is not Korevaar–Schoen harmonic

In a small belt rectangle with (0<t<1/4), the Korevaar–Schoen energy density is (1+h'(t)^2=1+t^4). Choose a nonzero nonnegative smooth compactly supported function (\psi) in that rectangle and vary only the first target coordinate, (h_\varepsilon=h+\varepsilon\psi). The derivative of that energy at zero is

\[
 2\int h'(t)\partial_t\psi=-2\int h''(t)\psi=-4\int t\psi<0. \tag{8}
\]

Small variations remain in the flat belt and have identical trace. Thus (u) fails the Dirichlet/Korevaar–Schoen local-minimizer condition. Equivalence of the *Sobolev spaces* or comparability of the *energies* must not be used to equate their minimizers.

### Reshetnyak energy is an admissible general energy

On two-dimensional seminorms, (I_+(s)=\max_{|v|=1}s(v)^2) is continuous, monotone, 2-homogeneous, and rotation-invariant. Its unit sublevel is compact: its seminorms are uniformly bounded and 1-Lipschitz on the unit circle, and the seminorm axioms persist under uniform limits. This proves properness by Arzelà–Ascoli.

It also has the quasiconvexity required in the source. For a finite-dimensional normed space (Y), the function (A\mapsto\|A\|_{\mathbb R^2\to Y}^2) is convex. If a smooth map (v:\overline D\to Y) agrees on the boundary with a linear map (L), the average of (Dv) is (L), by the divergence theorem applied componentwise to (v-L). Jensen's inequality yields

\[
 \int_D\|Dv\|_{\rm op}^2\geq |D|\|L\|_{\rm op}^2.
\]

This proves the required inequality, even without restricting the competitor to an immersion.

## 8. Scope, dependencies, and provenance

The mathematical construction and comparison arguments above are authored here. Standard tools used explicitly are McShane extension, scalar Sobolev calculus and gluing, convex normal neighborhoods, compactness of bounded equicontinuous functions, and the computation of degree-two de Rham cohomology of the sphere. No source theorem asserting the desired conclusion is assumed.

The known result for homotopy minimizers is credited to Meier–Vikman–Wenger and the earlier Lytchak–Wenger energy/area theory, not claimed as a new result. The counterexample needs the Reshetnyak member of their general energy class. The current published article's existence is verified through the author's bibliography, but its final text was not retrieved: source-level scope has been checked against the full arXiv v1 PDF and the Oberwolfach report. No assertion of exhaustive literature coverage or first priority is made.

References:

- D. Meier, N. Vikman, S. Wenger, *Energy minimizing harmonic 2-spheres in metric spaces*, arXiv:2503.08553v1, especially Questions 1.9, Definitions 2.3, 3.1, 6.1, Theorem 3.2, and Corollary 3.3: https://arxiv.org/abs/2503.08553 and https://arxiv.org/pdf/2503.08553v1.
- D. Meier, joint work with N. Vikman and S. Wenger, Oberwolfach Report 30/2025, contribution pp. 1624–1626, Question 1 on p. 1625: https://ems.press/content/serial-article-files/52249 ; report DOI https://doi.org/10.4171/owr/2025/30.
- Author-maintained publication record, listing *J. Reine Angew. Math.* 838 (2026), 137–169: https://people.math.ethz.ch/~damameier/research.html ; journal DOI https://doi.org/10.1515/crelle-2026-0042.

The supplied finite checks test algebraic identities and useful negative controls. They do not formally verify the analytic proof, replace independent review, or establish historical novelty.
