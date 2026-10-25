# Independent adversarial review: Zenodo 23409904

The full stated mathematical theorem is supported by the inspected proof and the independently checked differential-topology imports. I found no substantive defect, counterexample, hidden compactness requirement, or unresolved proof dependency in the construction. This is an adversarial mathematical assessment, not formal certification. Historical novelty and the absence of an earlier unrestricted realization remain **unverified**.

This review concerns the fresh actual six-page version 1.0 PDF, *Global Hessian realizations of statistical manifolds*, dated 15 October 2026. The PDF SHA-256 is `b874d63619ec7abbd3d9109639eb017b69435118c4cc9d5fec450605e4316e42`; the complete matching TeX SHA-256 is `97a749910fe2f340f000d82e1f1f46a4f0b26c975b1e5d54d2ce572a9cefed28`. Both were read in full before external research or supplied audit commentary. All six PDF pages were subsequently inspected visually. Source integrity is recorded in `CUSTODY.json`.

## Exact claim and success criteria

For every smooth, Hausdorff, second-countable, boundaryless manifold of one fixed finite dimension n >= 1, every smooth positive metric g and specified ordered mutually g-dual torsion-free pair (nabla, nabla*) admit a proper smooth embedding into an open U in R^N, N = binomial(2n+4,3), and one global smooth Psi on U with positive ordinary Hessian G. Orthogonal tangential projection of the standard ambient D and its G-dual D* gives the specified pair in that order. Both ambient affine connections are flat and torsion-free. The corollary asserts that vanishing of **both** torsions is necessary and sufficient for a general positive dual pair. Countable discrete dimension-zero inputs and the empty input are covered separately.

The unrestricted noncompact claim is the target of this review. No extra boundedness, completeness, connectedness, finite atlas, global normal frame, convexity of U, injectivity of the gradient map, probability model, or compactness was inserted. The theorem does not assert boundary or indefinite-metric extensions, optimal dimension, or a finite sample space. A failure of a strengthened statement outside this scope is not a counterexample.

## Independence and attack mechanism

The independent early ledger was sealed before browsing, examining supplied scripts, or reading historical audit statements. Its SHA-256 is `90d13376a927cabbfd93573f3ecbfcc1bd629792ce4d5ac46ab415b15aaa431b`, with creation bounded by 2026-10-24 23:25:45 and 23:27:19 PDT. It records seven distinct attacks: scalar-jet compatibility, pair signs and global periods, positive Hessian extension on noncompact and compact inputs, proper topology imports, local versus global dual coordinates, degenerate cases, and historical source scope.

No current sibling analytic/scope review or current root scientific conclusion was read. After sealing, the distributed authoring notes and two READMEs were read as support documentation; they contain historical audit summaries. Those summaries were not used as evidence of correctness. The distributed original proof and original finite mathematics script were read after the independent derivation and controls. Historical report bodies and root receipts were not opened. No supplied executable was run, imported, or promoted from a PASS wrapper.

## Checkable reconstruction and falsification results

### 1. The scalar third jet is legal globally

Put L = Levi-Civita(g), K = nabla-L and K* = nabla*-L. Both torsion conditions make K and K* symmetric in their two vector inputs. Duality gives g(K_X Y,Z) = -g(Y,K*_X Z). Combining these symmetries makes the lowered K fully symmetric, hence K* = -K and C = nabla g = -2g(K.,.,.). Consequently the ordered formulas nabla = L-C-sharp/2 and nabla* = L+C-sharp/2 are correct.

The quantity Q_ijk = partial_k g_ij + Gamma_ijk equals one half of the sum of the three first metric derivatives minus C. It is symmetric, but it is **not a tensor**. This is the correct transformation type for the third ordinary derivative of a scalar germ with zero first derivative and Hessian g. The exponential-germ definition q_p(exp_p v) = g_p(v,v)/2-C_p(v,v,v)/12 has precisely these jets: in L-normal coordinates its third derivative is -C/2, and conversion to ordinary derivatives adds the three lowered Levi-Civita terms. Only a smooth germ near each zero vector is used. Incompleteness or a vanishing injectivity radius at infinity does not interfere.

Under x=x(y), the three inhomogeneous terms in the manuscript's equation (7) are required. They arise from one connection transformation term and two differentiated-metric terms. My independent exact two-dimensional check uses x=(u+v^2,v+u^2), valid as a chart near the origin, Euclidean old metric and a nonzero symmetric old cubic. All eight ordered index choices satisfy the stated scalar-jet law. The incorrect tensor-only law fails in all eight cases. This is a useful negative control against silently dropping coordinate-change terms.

The section J of the scalar jet bundle need not be holonomic. The values q_p(p)=0 do not force its second component to vanish, since the base point and the germ variable have distinct roles. The independent one-dimensional computation explicitly finds a(t)f(t)=0 identically while the frozen-coefficient expression a(t)f''(t)=g(t)>0. Differentiating the identically zero scalar includes derivatives of a. This closes the most apparent potential contradiction.

### 2. Finite features and the right inverse require no uniform control

Given a proper e:M -> R^(2n+1), all degree-at-most-three monomials, including the constant, give the stated N. The degree-one coordinates recover e. Thus f is an embedding, and for compact B its inverse image is a closed subset of e^{-1}(projection(B)), which is compact. Its image is closed.

The fixed polynomial feature space spans every scalar third jet at every point. Choose n ambient linear functions whose restrictions are local coordinates. Every scalar third jet in these coordinates is a polynomial of degree at most three in their translated values, hence belongs to the same fixed ambient polynomial space. No globally chosen coordinate chart or finite chart cover is needed. Smoothness and surjectivity of the evaluation bundle map E give the global smooth right inverse E-adjoint(EE-adjoint)^(-1) after choosing smooth bundle metrics. Invertibility is pointwise; its least singular value may approach zero at infinity. Paracompactness supplies the bundle metrics.

As exact local rank controls, the full value-through-third-derivative matrices for (1,t,t^2,t^3) and all bivariate monomials through degree three have constant determinants 12 and 576. These are rank minors/local coordinate models, not a replacement for the arbitrary-manifold spanning argument. The manuscript's logarithmic lift example also has exactly the stated derivatives despite its unbounded coefficient field.

### 3. The pair and its global compatibility form have the correct signs

The frozen identities a f=0, a f_i=0, a f_ij=g_ij and a f_ijk=Q_ijk, with phi=-a, imply after base differentiation

    f_i partial_j phi = g_ij,
    f_ij partial_k phi = Q_ijk-partial_k g_ij = Gamma_ijk,
    phi df = 0.

The last identity is global vanishing, not local closedness. It eliminates a period/primitive obstruction even on nonsimply connected M. Positivity of g makes dphi injective on each tangent space. It does not imply global injectivity of phi, and the extension proof does not require it. This matters because Marugame's named Lauritzen embedding definition includes embeddings in both factors, whereas the present construction only needs f embedded and phi a smooth conormal covector field with these identities.

My independent noncompact field takes M=R, g=dt^2/(1+t^2)^2 and C=t^5 dt^3. The metric is positive but incomplete, since the distance integral to either infinity is finite. The cubic is unbounded. Solving the full scalar jet system with f=(1,t,t^2,t^3) gives the exact pair identities and zero form. Reversing the cubic sign produces the dual connection instead, a detected failure of the ordered connection requirement. The four active coordinates can be included in the manuscript's twenty-coordinate feature construction for e(t)=(t,0,0).

### 4. A single positive Hessian neighborhood exists without uniform estimates

For a variable-radius Euclidean normal tube, the normal-addition inverse r,nu is smooth and dr=P_T, dnu=P_N along S. Since phi annihilates TS, Psi_0(z)=phi_{r(z)}(nu(z)) has value zero and first derivative phi along S. Differentiating this covector equality along S gives every tangent Hessian column, not merely its tangent-tangent restriction. Normal-normal Hessian vanishes because a fixed normal fiber is an affine straight line and Psi_0 is linear on it. Thus H_0=[A B;B^T 0], where A is the positive tangent metric expressed using the Euclidean metric.

The proposed t=tr(A^{-1})||B||_HS^2 and lambda=1+t are smooth, invariantly defined scalars even when the normal bundle is nontrivial. Derivatives of lambda introduce no unwanted tangent column: nu=0 along S, so lambda(r)|nu|^2 has vanishing value and first derivative and Hessian exactly 2lambda P_N along S. The completed square gives the positive Schur complement because

    B^T A^{-1} B <= t I,
    2lambda I-B^T A^{-1} B >= (2+t)I.

All estimates are pointwise. They remain valid when A has eigenvalues approaching zero and lambda becomes unbounded. The positive-definiteness locus of the **one already-defined** smooth Hessian is open and contains every point of S. Selecting that locus does not require a common tubular radius, a common spectral lower bound, or a convergent gluing series. Properness persists after restriction to U because its compact subsets remain compact in R^N.

For the incomplete noncompact field above, I formed the actual tangent-column completion using v=f', w=phi', P_N=I-vv^T/|v|^2 and

    H_0=(v w^T+w v^T)/|v|^2-g vv^T/|v|^4.

The one-dimensional invariant t is |P_N w|^2/g. At t-base 0,1,3,10,100 all leading principal minors of H_0+2(1+t)P_N are **exactly** positive, and Hf'=phi', f'^T Hf'=g hold exactly. A constant lambda=1 already has negative Schur complement at base 1, so this control distinguishes the actual variable mechanism from an invalid uniform replacement. The Euclidean tangent eigenvalue tends to zero at infinity. The B=0 case separately yields lambda=1 and a positive block diagonal completion.

Compact S contained in Psi=0 is not a contradiction to positive Hessian on an allowed nonconvex domain. The explicit annular potential Psi=rho^2-rho on rho>1/2 has radial eigenvalue 2 and tangent eigenvalue 2-1/rho, both positive, and vanishes on the unit circle. This tests a tempting but inapplicable global-convexity objection.

### 5. Ambient dual flatness and both induced connections are established

For G=Hess(Psi), the manuscript's formula (Gamma*)^C_AB=G^{CE}partial_A G_BE follows directly from metric duality with the standard D. Symmetry of third derivatives gives zero torsion. The components eta_E=partial_E Psi have invertible Jacobian G and zero D*-covariant Hessian, hence furnish local affine charts. This proves zero curvature as a local tensor identity. It does not need a global inverse to eta. For example a positive quadratic potential on each component of (-2,-1) union (1,2) can give duplicate gradient value zero at two different points. The paper does not assert otherwise.

Along S, the preserved first jet gives G f_k=partial_k phi. Therefore f*G=g and the lowered induced D-connection is G(f_ij,f_k)=f_ij partial_k phi=Gamma_ijk. Ambient duality and metric-orthogonal projection then give the specified second connection by uniqueness of the g-dual. The order has been checked directly rather than inferred from an unsigned cubic identity.

For necessity, project the torsion identity separately for each ambient connection. Both induced torsions must vanish. Neither one may be silently omitted: with constant Euclidean metric on R^2, set the sole nonzero coefficient Gamma^0_01=1 and define the dual by Gamma*^k_ij=-Gamma^j_ik. Exact duality holds, the first torsion is nonzero, and the second torsion is zero. This pair is correctly excluded. The zero cubic/Levi-Civita case is included, as is arbitrary smooth cubic. Countable components cause no finite-chart or uniformity requirement. A countable discrete zero-manifold embeds properly as a subset of the nonnegative integers with Psi=z^2/2; empty input is vacuous.

## External theorem scopes and historical limits

The construction's substantive external existence inputs are proper smooth Whitney embedding, smooth bundle metrics/partitions of unity, and a smooth variable Euclidean normal tube. None is imported from a numerical experiment or from a theorem having unverified parameter restrictions.

* **Whitney 1936:** actual scan of definitions on printed pp.646-647, Theorem 1 on p.654, and Lemma 19/footnote 32 on p.665 was read. The definitions allow nonconnected manifolds and finite or infinite differentiability. The theorem gives dimension 2n+1. The footnote explicitly modifies the embedding to remove finite limit points, which supplies modern properness. The older usage of “proper” inside the proof alone was not taken as sufficient. [Actual published scan](https://www.math.ucdavis.edu/~saito/data/high-dimensions/whitney-diffmanifolds.pdf).
* **Gualtieri course notes, part 11:** all five actual pages were read. Definition 3.53 and Theorem 3.54 on printed pp.43-44 use a variable positive radius and apply to every regular Euclidean submanifold. The compact-only embedding statements earlier in these notes were not used. The normal-addition theorem applies to the closed smooth S here. [Primary author notes](https://www.math.toronto.edu/mgualt/courses/17-1300/docs/17-1300-notes-11.pdf).
* **Amari 1997 and FMU 1998:** visual reading of actual Amari pp.84-88, in particular definition/theorem on pp.84-85 and question on p.87, confirms local dual-affine coordinates and flatness of both affine connections. Actual FMU p.125 item 1(a) states the corresponding realization question. Neither inspected statement imposes global injective gradient coordinates, convex target, or a probability simplex. [Amari body](https://bsi-ni.brain.riken.jp/database/file/166/169.pdf), [FMU body](https://www.jstage.jst.go.jp/article/iis/4/2/4_2_125/_pdf/-char/en).
* **Marugame v1:** actual §§2.1-2.4, Definition 2.1 and Theorem 2.2 were read, together with the nearby proof conclusion and references. The result is a **local** pair/Hessian equivalence. Its proof uses a local primitive of the compatibility form and a transverse quadratic penalty. It credits the separate Lauritzen Lancaster note. The present proof supplies the global zero form and a variable correction explicitly, so no unjustified global version of Marugame is imported. [Exact v1 body](https://arxiv.org/pdf/2103.10102v1).
* **Loi-Matta v1:** all eight actual pages were read after independent work. Theorem 1 assumes already N-induced statistical data. Proposition 6 gives a minimum-norm right inverse for its free-map linearized system. This supports the manuscript's limited antecedent description; it does not establish arbitrary global realization here. This is the v1 titled *Robustness of statistical models*, not an asserted identical publisher body. [Exact v1 body](https://arxiv.org/pdf/2110.06145v1).

The original separate Lauritzen pair note was not obtained. Its existence is independently listed in the author's institutional bibliography, but that metadata does not establish its theorem scope. The IMS chapter is a distinct source; an unsuccessful DOI access is not counted as its reading. A fresh attempted Matumoto download returned HTML rather than PDF and was rejected by signature validation. The original Matumoto body, Lê's final 2006 and 2007 bodies, Abe, the full 2017 book chapter, the specified Osipov papers and accepted/publisher variants were not independently inspected in this lane. No claim about their precise proof coverage or priority is promoted from supplied audit summaries. These are **historical coverage limits**, not dependencies needed to complete the explicit construction above.

Two priority observations in the paper can be checked without unavailable prior bodies. In simplex mixture coordinates, differentiating sum p_a log p_a gives the Fisher metric and third derivative minus the Amari-Chentsov cubic, so a valid unrestricted finite-simplex embedding theorem with the chosen cubic sign would imply the historical conclusion. Also an embedded Euclidean image is locally closed, hence open in its closure; removing closure(S) minus S makes it closed in an allowed open ambient, so properness by itself cannot certify novelty. Neither establishes a predecessor or firstness. I leave all novelty claims unverified.

## Computation custody, defects, and final disposition

`independent_checks.py` was authored without importing supplied code. The 25-second isolated-process-group watchdog completed in 0.6683 seconds with return code 0, no timeout and empty stderr. Cleanup attempted SIGKILL on the isolated process group in `finally`. Its UTC receipt is 2026-10-25T06:32:19.011130+00:00. Exact output is in `independent_results.json`; stdout SHA-256 is `b7a5668b3c8d8be7771fe770223f84cd9c83d70af180eb084d3bfce204c9afa9`.

The finite controls corroborate formulas and distinguish several invalid modifications. They do not prove arbitrary-manifold topology or a universal existence theorem. The universal argument was assessed by the reconstruction above with authenticated standard imports. No numerical tolerance was used in my checks. The distributed package's finite checks and its advertised transport policy were not replayed or independently certified by this lane.

**Strongest verified result:** the full stated proper global Hessian realization in the stated N, with exact specified connection ordering and the both-torsions criterion, supported as a mathematical proof under the checked standard topology inputs. **Exact remaining mathematical gap:** none found in this adversarial audit. **Defect classification:** no substantive defect found; no counterexample found; no new required repair. **Limits:** no formal proof-assistant verification, independent human review, optimal-dimension result, exhaustive bibliography or novelty certification. Parent must inspect the actual paper and all completed independent reports before any promotion. No source or shared artifact was edited and no external communication or publication action occurred.
