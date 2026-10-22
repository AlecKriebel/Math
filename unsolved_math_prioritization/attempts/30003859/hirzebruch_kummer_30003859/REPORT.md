# Report

## 1. What the source actually asks

The primary contribution is Ingrid Bauer, joint work with Fabrizio Catanese, “Symmetries and equations of Del Pezzo surfaces and applications,” in *Oberwolfach Report 28/2018*, printed pp. 1696–1698. Conjecture 2 on p. 1697 concerns eventual rigidity of the smooth Hirzebruch–Kummer surfaces belonging to a fixed rigid planar line configuration. It quantifies over all sufficiently large integer exponents, not just primes or a divisibility subsequence. The setup on p. 1696 permits distinct lines not all through a common point and n >= 2. The group has rank one less than the number of lines. Theorem 1 on that page already settles the complete-quadrangle case, with threshold n = 4. [OWR]

Work over C. For d = r+1 distinct lines L_i = {l_i = 0} in P^2, form the normal cover with function field

C(P^2)((l_1/l_0)^(1/n), ..., (l_r/l_0)^(1/n)).

Its deck group is (Z/n)^r. Denote the normal cover by X_n and its minimal desingularization by S_n = HK(n,L). Both have complex dimension two. Blowing up the points of valency at least three on the base gives a rational surface Y and a normal-crossings divisor D consisting of the strict transforms and exceptional curves. The smooth abelian cover of (Y,D) realizes S_n; the local inertia calculation is given in Proof 4.

“Configuration” fixes the full incidence pattern. Rigidity is modulo PGL(3,C). It is not the assertion that the coefficients of fixed equations cannot move before quotienting by changes of coordinates.

## 2. The low-cardinality scope problem

Take four distinct lines in general position. Their dual points form a projective frame, so this incidence type is a single free PGL(3,C)-orbit. In particular it is infinitesimally rigid as a line configuration. Its HK cover is

F_n = {z_0^n + z_1^n + z_2^n + z_3^n = 0} in P^3.

For every n >= 4 the family

F_(n,t) = {z_0^n + z_1^n + z_2^n + z_3^n + t z_0^(n-2) z_1^2 = 0}, |t| < 1,

is smooth and has nonzero Kodaira–Spencer class at t = 0. Proofs 1–2 establish this as an actual deformation, not merely a nonzero tangent vector that could be obstructed.

This disproves the formulation with **all** projectively rigid line configurations. It does not disprove a version restricted to configurations with four or more high-valency points and two such points per line. The distinction matters because Bauer–Catanese's Definition 1.2 uses the usual local orbit definition, but their Remarks 1.3/1.5 work as though those incidence hypotheses follow automatically. The relevant printed pages 5–6 were inspected visually. They do not follow for a four-line frame: the residual projective transformations account for the apparent movements. This packet treats that mismatch as a formulation issue, not evidence that the intended research question is trivial. [BC-config]

No novelty is claimed for the Fermat-surface example, the deformation calculation, or the diagnosis.

## 3. Rigidity notions and deformation functors

For a smooth compact complex S:

- Infinitesimal rigidity means H^1(S,T_S) = 0. The Kuranishi base is then a reduced point.
- Local rigidity means all sufficiently small fibers of every deformation are isomorphic to S. A nonreduced point can be locally rigid without infinitesimal rigidity.
- Global rigidity means every deformation-equivalent compact complex manifold is isomorphic to S.
- We use “strong rigidity” in Bauer–Catanese's stated sense: only finitely many isomorphism classes occur among compact complex manifolds homotopy equivalent to S, and they are globally rigid.
- Étale rigidity imposes rigidity on every finite unramified cover.

These notions must not be interchanged. The n >= 4 quadrangle theorem proves infinitesimal rigidity, and its source also proves global rigidity in that setting. It does not by itself prove strong or étale rigidity for every exponent. The n = 4 and n = 6 cases require separate character analysis, but are positive cases, not exceptions to the theorem. The n = 2 quadrangle cover is K3; the n = 3 case is nonrigid according to the cited later theorem. Our independently worked n = 3 calculation proves only a one-dimensional nonzero eigenspace in H^1, and is explicitly insufficient on its own to infer nonrigidity. [BC-rigid]

Three deformation questions are different:

1. deform the line configuration or the decorated branch pair (Y,D);
2. deform the cover together with its deck action;
3. deform S as an abstract surface, allowing the action or exceptional curves to disappear.

Proof 3 identifies the invariant tangent summand with H^1(Y,T_Y(-log D)). Vanishing of that summand leaves every nontrivial character uncontrolled. Likewise equisingular deformations of X_n do not represent all deformations of S_n without a proof that the exceptional locus persists and contracts in families.

## 4. Prior results and later literature

- [BC-rigid], Theorems 1.2/5.1 and Proposition 8.1, is the credited source for quadrangle infinitesimal rigidity. Its strategy involves all character summands, not just the invariant part.
- [BC-config], Theorem 0.3 and section 2, proves infinitesimal triviality of equisingular deformations of the **singular cover** under a singular saturation condition: at least four high-valency points, two on each line, and every line joining two such points included. It does not state abstract-surface rigidity for every arrangement. Its Conjecture 0.2 still asks for the extension.
- [BGBP-2021] studies abelian covers of specially engineered line arrangements and establishes a rigid surface with a nonreduced Kuranishi point. Its deformation-equivalence criteria impose extra vanishings. It supplies neither a general HK theorem nor a justification for replacing “rigid” by “infinitesimally rigid.”
- [SU-2022] constructs another explicit family of rigid surfaces and lists selected rigid HK families. Its principal construction is a cyclic cover of an abelian surface; it is not the all-configuration theorem sought here.
- [BC-syzygies] concerns equivariant equations for the degree-five del Pezzo surface. Its abstract is not a claim resolving general HK rigidity.

Targeted searches through 2026-10-05 for the exact title, conjecture, saturation terminology, and later HK rigidity did not identify a primary paper resolving the intended generality. This is a bounded search finding, not proof that no such result exists. The imported “partially solved” assessment was not accepted as independent literature evidence. Titles of the two main Bauer–Catanese papers have been corrected in the bibliography rather than copying the inaccurate short labels from the imported metadata.

## 5. Actual prior-attempt checks

The live repository queue contains rank 741 as queued, 0/5. That alone is not evidence of no previous attempt.

Additional read-only checks searched AlecKriebel/Math PRs in all states for the identifier, “Hirzebruch,” and “Kummer”; branches for the identifier, “hirz,” and “kummer”; commits for the identifier and “Hirzebruch”; and indexed files for the identifier and “Kummer.” No exact matching research attempt was returned. The broad Kummer PR results were unrelated number-theoretic, real-zero, and Voronoi topics. Relevant prior-conversation retrieval also returned no substantive proof or report for this target. We do not assert exhaustive absence across inaccessible, unindexed, or differently named work.

The public catalog record was checked against a fresh public dataset row at index 12643; its identifier and statement matched the earlier public corpus bytes. The direct problem webpage returned HTTP 403 and was not bypassed. The independent primary report was retrieved and inspected instead. Source metadata includes these limits, without exposing dataset contents or private prior-conversation material.

## 6. Five approaches and retained outcomes

1. **Direct boundary construction.** The four-line/Fermat example proves the unrestricted statement false. It is outside the evident nontrivial-incidence setting.
2. **Deck-equivariant deformation reduction.** The invariant direct-image formula proves exactly what branch rigidity controls. It does not control all surface deformations.
3. **Exceptional-character calculation.** For the quadrangle at n=3, the character (2,2,2,1,1) gives a logarithmic residue cokernel of dimension one. It is an exact negative control against deleting nontrivial characters or extending the positive result to n=3.
4. **Uniform large-exponent analysis.** For any fixed arrangement the relevant line-bundle classes and selected logarithmic divisors range over a finite set. A complete elementary argument proves that the set of exponents with H^1(S_n,T_S) nonzero is eventually periodic. This reduces infinitesimal eventual rigidity to finitely many cohomology types plus integer feasibility; it does not evaluate those cohomologies or establish their universal vanishing.
5. **Equisingular/contraction strategy.** The known singular-cover theorem supplies a possible endpoint, but the required persistence of exceptional curves and compatibility of contraction with arbitrary deformations remains unproved here. Fixed branch data, a rigid product of target curves, or a special ball-quotient exponent does not fill that gap. This route is stopped at that precise missing implication.

The five approaches are completed as a scoped investigation. There is no claimed full proof or counterexample within the intended restricted class. Do not classify the intended conjecture as solved on the strength of either the literal boundary example or the finite-state reduction.

## 7. Verification and limitations

The verifier checks the projective-frame ranks, Fermat monomial witnesses, exact integer smoothness bounds, degree-n Jacobian counts, the n=3 Picard residue matrix, and all quadrangle character types for 2 <= n <= 10. It includes deliberately invalid configurations and witnesses. Finite calculations support the written proofs; the all-n and arbitrary-arrangement deductions rely on those proofs, not extrapolation.

Neither the verifier nor the source hashes certify the full rigidity theorem. We do not provide a general logarithmic-cohomology algorithm, a numerical eventual period for a new arrangement, a computation of its Kuranishi obstruction map, or proof-assistant certification.

## Sources

[OWR] Ingrid Bauer (joint with Fabrizio Catanese), contribution in *Subgroups of Cremona Groups*, Oberwolfach Report 28/2018, pp. 1696–1698. DOI: https://doi.org/10.4171/owr/2018/28 . Public report: https://publications.mfo.de/bitstream/handle/mfo/3650/OWR_2018_28.pdf?isAllowed=y&sequence=1 .

[BC-rigid] Ingrid Bauer and Fabrizio Catanese, *On rigid compact complex surfaces and manifolds*, Advances in Mathematics 333 (2018), 620–669. https://arxiv.org/abs/1609.08128 . DOI: https://doi.org/10.1016/j.aim.2018.05.041 .

[BC-config] Ingrid Bauer and Fabrizio Catanese, *Del Pezzo surfaces, rigid line configurations and Hirzebruch–Kummer coverings*, Bollettino dell'Unione Matematica Italiana 12 (2019), 43–62. https://arxiv.org/abs/1803.02984 . DOI: https://doi.org/10.1007/s40574-018-0169-x .

[BGBP-2021] Christian Böhning, Hans-Christian Graf von Bothmer, and Roberto Pignatelli, *A rigid, not infinitesimally rigid surface with K ample*. https://doi.org/10.1007/s40574-021-00296-3 .

[SU-2022] Matthew Stover and Giancarlo Urzúa, *Rigid surfaces arbitrarily close to the Bogomolov–Miyaoka–Yau line*, American Journal of Mathematics 144 (2022), 1783–1804. https://preprint.press.jhu.edu/ajm/sites/default/files/AJM-stover-urzua-FINAL_0.pdf .

[BC-syzygies] Ingrid Bauer and Fabrizio Catanese, *S_5-equivariant syzygies for the Del Pezzo Surface of Degree 5*. https://arxiv.org/abs/1812.10715 .

[GS-1966] Seymour Ginsburg and Edwin H. Spanier, *Semigroups, Presburger formulas, and languages*, Pacific Journal of Mathematics 16 (1966), 285–296. https://msp.org/pjm/1966/16-2/pjm-v16-n2-p09-p.pdf . The finite-state argument below is a special case of classical semilinearity, not a novelty claim.
