# Independent mathematical audit: CMC min-max width

## Verdict and scope

**PASS: the frozen candidate proves the affirmative statement under the original referenced asymptotic convention, conditional on its accurately matched standard theorem dependencies.** No fatal gap or counterexample was found. The original-convention transplantation bridge is valid. The proposed `already_solved`, `1/5` disposition is defensible as a credited literature-based reduction, with the qualification about credit below.

Target: **30005144 / OWR-10252937-007**, Liam Mazurowski's conjecture in *Geometrie*, Oberwolfach Report 28/2022, pp. 1574–1576. The conclusion is

\[
\omega_c(M)<16\pi/(3c^2)\quad\text{for every }c>0.
\]

The audited manifold is smooth, connected, complete, three-dimensional, without boundary, with the entire complement of a compact set equal to one asymptotically Euclidean coordinate end, nonnegative scalar curvature, and not isometric to Euclidean space. The original preprint's definition includes smooth unweighted convergence of the metric perturbation, together with zeroth- and first-derivative rates. The audit does not add a weighted second- or third-derivative hypothesis, orientability, a topological assumption on the compact core, or positive scalar curvature.

Audited proof SHA-256:

`c7e98279d04995056224ca2a7bccd1a269519f205977138c2cbd7b507a4cd392`

All six frozen public files and the three supplied source PDFs matched the freeze's hashes. The original files were not modified. This is an AI-assisted mathematical audit, not human peer review or a formal proof certificate. Imported geometric-analysis theorems were checked for their precise statements and relevant proof dependencies; they were not reproved from foundational results.

## 1. Original statement and literature matching

The official OWR PDF was independently inspected, including rendered pp. 1575–1576. Equation (1) is the strict width estimate above. The conjecture adds nonnegative scalar curvature and the exclusion of Euclidean space to Theorem 2's hypotheses. It concerns the area-minus-volume mountain-pass value, not merely the existence of some CMC surface.

The referenced 2022 preprint was inspected at Definitions 5–6 and 26. Its formal path topology is the flat-plus-varifold topology, and its smooth convergence wording does not justify silently inserting weighted higher-derivative rates. The frozen proof correctly acknowledges this distinction.

Mazurowski–Zhu's version 1 was checked directly, including its scalar-free Theorem 1.5, Sections 2.1–2.2, Lemmas 2.3–2.5, Corollary 2.6, Lemma 2.20, and the proof of Theorem 4.3. The checked arXiv record lists the February 2025 version and no later version. Its CMC existence conclusion alone is insufficient for this audit; its flow theorem is the actual imported input. Its weighted-C3 convention is explicitly stronger than what the candidate assumes.

Theorem 1.5 supplies spherical smooth leaves; Lemma 2.20 identifies the inner and outer weak level surfaces. The spatial constant in Corollary 2.6 can be fixed using metric equivalence, independent of the finite time horizon and starting point. Only the required distance threshold changes. Lemma 2.3 allows scalar curvature of either sign. Its proof uses bounded curvature error, and the later regularity estimates retain small signed errors. Thus global nonnegative scalar curvature is not a hidden premise of these three imports.

## 2. Nonflat points arbitrarily far out

The candidate's use of positive-mass rigidity is legitimate, but the coordinate-change sentence compresses a worthwhile lemma. A detailed independent proof is included in `flat_end_rigidity.md`.

If the end were flat, its simple connectivity would give a global parallel orthonormal coframe. Integrating it gives a developing map F with g=F*delta. The original bounds imply Christoffel symbols O(r^-2), hence DF=Q+O(r^-1) for one orthogonal matrix Q, and F=Qx+O(log r). After rotation, the derivative is uniformly close to the identity far out. Joining exterior points by curves of length at most pi/2 times their Euclidean separation proves injectivity on a smaller exterior. Properness at infinity and an open/closed argument show that its image contains a Euclidean exterior. In these coordinates the metric is exactly Euclidean outside a compact set.

Consequently its ADM mass is zero, all weighted decay requirements hold, and scalar curvature is compactly supported and integrable. The original manifold, not the patched auxiliary manifold, satisfies positive-mass rigidity. The cited AMO Theorem 2.1 is a general three-dimensional rigidity theorem; its preceding H2-restricted Green-function theorem is not being substituted. Its topology reduction handles nonorientability, alternatively by an orientation double cover with two Euclidean zero-mass ends. Thus a non-Euclidean original manifold must have nonzero Riemann curvature arbitrarily far out.

## 3. Transplantation and quantifier order

The added bridge passes the adversarial checks:

1. For any prescribed finite radius and epsilon, smooth convergence gives uniform bounds for the perturbation and its first three coordinate derivatives on all sufficiently far-out balls. Since nonflat points exist beyond every compact set, choosing their centers subject to these bounds is valid. There is no lower bound on curvature that would conflict with making the perturbation arbitrarily small.
2. The supports centered at q_j=10^j e_1 with radii 2j are disjoint and locally finite. Multiplying the translated tensor by the smooth cutoff and extending by zero is smooth. Making its operator norm sufficiently small gives uniform positive definiteness and completeness.
3. Cutoff derivatives of order a contribute j^-a, and j>=1. Thus each derivative through order three is bounded by a fixed cutoff constant times epsilon_j. On each support, |x| is comparable to 10^j. With epsilon_j<=j^-1|q_j|^-5, the largest relevant weighted bound is O(j^-1|q_j|^-2), which tends to zero. Finitely many initial supports do not affect asymptotics. Off the supports the metric is Euclidean.
4. The metric is built once, independently of the requested volume and time horizon. Fixing its metric-equivalence constant fixes the spatial constant C. Choose finite T to make the lower volume estimate exceed the desired volume; only then choose j beyond the fixed-metric regularity threshold and with j>C exp(T/2). Both conditions hold for all sufficiently large j. No unjustified uniform threshold over a changing family of metrics is used.
5. Every relevant sublevel set, not only its boundary, stays in the isometric core. The volume lower bound uses the lower eigenvalue bound on the volume density, namely 2^-3/2 in dimension three. Hence there is sufficient volume before time T.
6. No claim of general locality or metric-independence of weak IMCF is needed. The weak flow is first constructed globally for the auxiliary metric. A portion known to be smooth and spatially trapped is then transferred by an actual isometry. Negative scalar curvature in the cutoff annuli cannot enter the ensuing smooth local monotonicity calculation.

The prescribed original end need not itself meet the later weighted convention. This proof really bridges the mismatch rather than renaming it.

## 4. Topology, Hawking mass, and strictness

The transferred leaves are embedded spheres with positive mean curvature, forming nested bounded regions. Including the initial point in each region is harmless for volume and perimeter and gives the usual open enclosed region. The smooth flow/level-set identification excludes a plateau or an unswept open set inside the relevant sublevel region. Its spherical topology supplies exactly the Gauss–Bonnet cancellation required by Geroch's formula.

The formula in the candidate has the correct normalization and agrees with the smooth calculation in Huisken–Ilmanen, pp. 395–396; their equality discussion on pp. 422–424 is consistent with the candidate’s local argument. One can check it directly by differentiating the Hawking mass, using A'=A, the smooth mean-curvature evolution, and the Gauss equation. Its remaining integrand is twice the squared gradient of log H, plus scalar curvature and the squared trace-free second fundamental form. All terms are nonnegative on the trapped flow. The initial nonnegative mass limit therefore gives m(t)>=0 at every finite relevant time.

If m(t0)=0, monotonicity and the initial limit imply m=0 for every earlier time. Each leaf is umbilic, H is constant on each connected leaf, and ambient scalar curvature vanishes along it. The zero mass relation gives H^2 A=16 pi. In normal flow coordinates, the induced metric evolves by gamma_t'=gamma_t and r=sqrt(A/(4 pi)) converts the normal lapse to dr^2. The swept metric is therefore dr^2+r^2 gamma with a fixed two-dimensional metric gamma. Its scalar curvature is r^-2(R_gamma-2), so R_gamma=2 and its Gaussian curvature is one. The cone is flat. Spatial bounds and absence of jumps ensure these leaves sweep a punctured neighborhood of the initial point. Smoothness at the point then implies zero Riemann curvature there, contrary to its selection. This establishes m(t)>0, including in the scalar-flat case.

Hölder's inequality yields A^(3/2)<=sqrt(integral H^2) V', and strictly positive Hawking mass gives (A^(3/2))'<6 sqrt(pi) V'. The initial area limit follows from the exact exponential area evolution; the initial volume limit follows from spatial containment. Integrating over an earlier finite interval and then sending its left endpoint to minus infinity gives the strict inequality A<(36 pi)^(1/3)V^(2/3) at every positive-volume leaf. No uniform positive lower bound for curvature or Hawking mass is needed.

## 5. Admissible path and every c>0

For each c>0 choose terminal volume v>((36 pi)^(1/3)/c)^3. Strict volume increase and the lower volume bound give a unique truncation at that volume. The stated exponential reparameterization turns (-infinity,t_v] into (0,1]. At zero, perimeter tends to zero by A'=A, and volume tends to zero by containment. The associated boundary varifold converges to zero because its mass does, so this is continuity in the actual flat-plus-varifold topology, not just Hausdorff convergence. Positive parameters are smooth; a single translated compact ball contains the entire path.

The terminal energy is negative. The comparison profile has global maximum 16 pi/(3c^2), attained at volume 32 pi/(3c^3). Every positive-parameter energy is strictly below that maximum; the empty endpoint has energy zero. Continuity on the compact parameter interval makes the path's maximum attained and strictly smaller. This is the step that prevents a merely pointwise strict comparison from losing strictness in a supremum.

The argument works for each c, using a possibly different sufficiently far-out transplanted region, all contained in the same original manifold. No uniform choice in c is required. Euclidean isoperimetry and continuity of volume give the reverse lower bound for Euclidean paths, while Euclidean ball paths give the matching upper bound. The exclusion of Euclidean space and the threshold constant are therefore correct.

## 6. Computation and portability

The author's twelve exact algebra checks were rerun and all passed, reproducing the recorded JSON under SymPy 1.14.0. The independent program reconstructs those twelve checks; in particular it calculates the cone scalar curvature from Christoffel and Ricci definitions rather than inserting the scalar formula under test. Four additional controls check the spherical Geroch cancellation, Hölder constant, round-fiber cone specialization, and weighted exponent.

All sixteen independent controls pass. Execution from the packet directory, an unrelated working directory, with Python optimization, and from an isolated copy produces byte-identical output. The program uses no network, source PDFs, repository files, or current-directory assumptions. Invalid command-line arguments fail explicitly. Neither algebra program proves the geometric theorem. Manifest verification, empirical portability, and exact symbolic identities are separate from mathematical audit conclusions.

## 7. Advisory clarifications; none blocks acceptance

- Expand the flat-exterior coordinate lemma and mention scalar-curvature integrability explicitly. The attached independent note supplies the details. The compressed claim in the frozen proof is correct.
- Where the proof says area and volume vanish by spatial bounds, attribute area decay to A'=A (also already stated there). Containment alone would not control area for arbitrary oscillating surfaces.
- Use the precise sublevel bounds of Corollary 2.6, as the candidate already does. The spatial sentence printed in Theorem 1.5 has an evident t/T mismatch; the correct corollary and its proof remove any ambiguity.

## 8. Credit and disposition

Mazurowski–Zhu supply the decisive geometric-analysis advance and the strict-width mechanism in the weighted-C3 class. The candidate supplies the explicit single-metric transplantation reduction to reconcile the original weaker derivative convention, and spells out the local equality/strictness and compact-parameter arguments. Acceptance must not erase that distinction or claim the full original-convention proof was quoted verbatim from the 2025 paper.

A credited literature-based `already_solved` classification is appropriate with that explanation. No first-resolution or historical-priority claim is justified by this audit. The substantive-attempt count remains 1/5; the audit is not a new attempt to solve the problem. Historical duplicate-search completeness and external queue edits are outside this mathematical audit.

## Primary references

- [Original OWR report](https://ems.press/content/serial-article-files/46965), pp. 1574–1576; [DOI 10.4171/OWR/2022/28](https://doi.org/10.4171/OWR/2022/28).
- [Mazurowski, arXiv:2204.07493v1](https://arxiv.org/abs/2204.07493v1), Definitions 5–6 and 26.
- [Mazurowski–Zhu, arXiv:2502.18455v1](https://arxiv.org/abs/2502.18455v1); [full primary text](https://arxiv.org/html/2502.18455v1).
- [Agostiniani–Mazzieri–Oronzio, published article](https://link.springer.com/article/10.1007/s00220-024-04941-8), Theorem 2.1 and its asymptotic convention.
- [Bray–Kazaras–Khuri–Stern, author-hosted primary paper](https://www.math.stonybrook.edu/~khuri/Bray_Kazaras_Khuri_Stern_PMT.pdf), Theorem 1.1 and Proposition 2.1.
- [Huisken–Ilmanen, original JDG paper, university-hosted copy](https://math.jhu.edu/~js/Math646/huisken-ilmanen.pdf), smooth Geroch formula and weak IMCF background.
