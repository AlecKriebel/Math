# Independent mathematical and source review of the Hopf product example

Problem ID 2999, KP 4.123. Review date 6 October 2026.

## Verdict and exact acceptance scope

The construction is a valid counterexample to the genus-minimization question under the weak differential-form definition explicitly printed in K3, Problem 4.123. It is not a counterexample to the closed-positive-form question in Kronheimer's original Question 7.12. The distinction is present in the primary sources, not introduced by OCR or by the author's paraphrase.

This mathematical acceptance applies to the proof in the following exact submitted archive:

- Filename: TAUT_LEAF_GENUS_2999_AUTHOR_SAFE_FREEZE.zip
- Bytes: 15006
- SHA-256: a1f4ad02d89248ad6a1f0d499951ee0233a58d00083b0ca2d08156d0ac661b03
- Proof member: taut_leaf_genus_2999/PROOF.md
- Proof bytes: 7426
- Proof SHA-256: 054f40061c6f9bb2fbd93457d3149e33b58bd2e551f11ad0fbb5dfa3e1ee893c

No mathematical correction of the submitted counterexample is required. The limitations stated below are essential. This review does not certify novelty, settle the original question, establish its present literature-wide status, or replace the separate artifact-hardening audit. No publication was performed.

## Primary source comparison

Write E for the oriented tangent two-plane field. Define W by the existence of a smooth two-form omega positive on E such that d omega(v,w,z)=0 for v,w in E and arbitrary z in TM. Define C by the existence of a globally closed smooth two-form positive on E.

K3, printed and PDF page 292, states the smooth genus question for closed leaves of a coorientable smooth two-dimensional foliation of an oriented four-manifold. Remark (1) explicitly defines its tautness assumption by W. That statement and its definition impose neither a nonzero leaf class nor a closed transversal. I also checked the Chapter 4 introduction and the introduction of Section 4.11; neither supplies such a blanket restriction. The page separately identifies a symplectic special case and an S2 x S2 subquestion. Its attribution to Kronheimer does not make the two printed definitions identical. [K3]

Kronheimer's author PDF, PDF page 49 and printed page 47, introduces an oriented foliation on a closed oriented four-manifold and defines tautness there by C. Question 7.12 then asks about genus minimization for compact leaves of that kind. Its broader proposed adjunction inequality is qualified by positive pairing with the closed form. Compact leaves satisfying C necessarily have a nonzero real homology class, as follows directly from integration. The same page's affirmative fibration discussion occurs under this C hypothesis. It does not assert that every surface bundle, regardless of its fiber class, has a suitable symplectic form. [K98]

Scorpan, printed page 1235, Theorem 3.5 and its explanatory notation, records exactly the W condition in the geometric-tautness discussion. Remark 3.4 distinguishes the codimension-one transversal characterization from higher-codimension conditions. This supports reading K3's formula literally. For the construction below, neither that theorem nor a general tautness equivalence is needed: W is verified directly. [S03]

## Independent verification of the global construction

Let M=S3 x S1, with S3 the unit sphere in C2 and S1 the unit circle in C. Let h(z1,z2)=[z1:z2] be the Hopf map and q=h composed with projection onto S3. The map q is a smooth submersion onto CP1. Its fibers are connected embedded two-tori, so they are exactly the leaves of a nonsingular smooth foliation. M and every leaf are compact and have no boundary.

In real coordinates z_j=x_j+i y_j, use the Hopf generator

R=(-y1,x1,-y2,x2),

and on the second circle, with coordinates (u,v), use T=(-v,u). Pull both fields to M. The leaf distribution is E=span(R,T), and [R,T]=0. Both fields are everywhere nonzero, and the ordered pair (R,T) gives a global leaf orientation.

The normal quotient is q*TCP1, hence is oriented. Thus the foliation is coorientable in the usual transverse-orientation sense. Even a stronger normal-framing requirement would not invalidate this example. At z=(z1,z2), the complex vector U=(-conjugate(z2),conjugate(z1)) is orthogonal to z in the complex Hermitian inner product. The two real tangent vectors U and iU give a global frame of the horizontal normal complement on S3, and therefore on M. Choose the total orientation compatible with (R,T) and the complex orientation of the base.

Define on S3 and S1 respectively

alpha=x1 dy1-y1 dx1+x2 dy2-y2 dx2,

eta=u dv-v du,

and define omega=alpha wedge eta on M. These are restrictions and pullbacks of globally defined smooth ambient forms. There is no angular-coordinate singularity or gluing problem. Alpha is an invariant Hopf connection form: alpha(R)=1 and its curvature is horizontal. Eta is the global angular one-form on the circle, with eta(T)=1.

Although the ambient expression d eta=2 du wedge dv is nonzero on R2, its pullback to S1 is zero. Restriction commutes with exterior differentiation. Also alpha(T)=eta(R)=0. Consequently omega(R,T)=1, so omega is positive on every oriented leaf; its integral over each leaf is 4 pi squared.

Put Q=x1 squared+y1 squared+x2 squared+y2 squared. Direct differentiation gives

d alpha=2(dx1 wedge dy1+dx2 wedge dy2),

contraction_R(d alpha)=-dQ.

On TS3, dQ vanishes. Also contraction_T(d alpha)=0. On M, d omega=d alpha wedge eta, and therefore

d omega(R,T,z)=-d alpha(R,z)=0

for every tangent vector z. Since every pair of leaf vectors is a linear combination of R and T, alternating bilinearity proves W for all required inputs and at all points. This verifies the exact printed condition, rather than the vacuous restriction of a three-form to a two-dimensional leaf.

The form is genuinely nonclosed. At (z1,z2;u,v)=(1,0;1,0), take A=partial_x2, B=partial_y2, and T=partial_v. All three are tangent to M, and d omega(A,B,T)=2. Thus W does not imply that this particular form is closed.

## Integral homology and the genus comparison

For b=[1:0], the Hopf circle C consists of (z1,0) with |z1|=1. It bounds the embedded hemisphere

D={ (x1,y1,x2,y2) in S3 : y2=0 and x2>=0 }.

The set cut out by y2=0 is a standard two-sphere in S3, and x2>=0 selects a smooth hemisphere with boundary C. Thus D is a smooth embedded disk, not merely an immersed spanning surface. Orient D so that its boundary orientation agrees with R on C. The compact oriented embedded three-manifold D x S1 then has oriented boundary C x S1, the selected leaf L. Hence [L]=0 in integral H2(M).

Independently, the integral Kunneth calculation gives H2(S3 x S1;Z)=0. The factors have free integral homology, so there is no missing Tor term. Consequently every leaf has zero integral class.

Inside a coordinate four-ball in M, choose a small three-ball in a coordinate three-plane. Its boundary S is a smooth embedded oriented two-sphere and bounds that three-ball, so [S]=0. Both L and S are connected closed oriented embedded surfaces. They are integrally homologous, but g(S)=0 and g(L)=1. The genus conclusion fails without using a disconnected representative, an empty surface, a singular competitor, or rational rather than integral homology.

This is specifically a genus comparison. The truncated negative Euler-characteristic complexity chi_minus=max(0,-chi) is zero for both a sphere and a torus. The example therefore does not disprove a statement solely about chi_minus minimization. Nor would it refute a variant that excludes sphere competitors or requires a nonzero leaf homology class. Those would be changed hypotheses or a changed conclusion; the literal K3 genus question does not state them.

## Why the original closed form hypothesis fails

Suppose any closed two-form Omega were positive on this oriented foliation. Positivity on the compact leaf gives integral_L Omega>0. On the other hand, the explicit bounding three-manifold gives

integral_L Omega=integral_(D x S1) d Omega=0.

This is a contradiction. The obstruction excludes every closed positive form, not merely the displayed omega. It also excludes any compatible symplectic form. Indeed, M cannot carry any symplectic form: H2(M;R)=0 would make it exact, contradicting the nonzero symplectic volume integral on a closed manifold.

There is no conflict with the positive integral of omega. Its exterior derivative has integral 4 pi squared over D x S1. The weak condition only controls arguments containing two leaf directions. The interior tangent spaces of D x S1 are not constrained to contain two such directions, so W does not force this three-dimensional integral to vanish.

The hypothesis C also explains why null-homologous leaves are automatically absent from Kronheimer's original setting. A variant restricted to nonzero homology classes is untouched here. The S2 x S2 subquestion is untouched as well.

## Transversals and geometric minimality

No compact everywhere-transverse immersed surface exists for this foliation. If f:Sigma->M were such an immersion with a nonempty closed connected surface Sigma, then q composed with f would be a local diffeomorphism to S2. By compactness it would be a covering, and since S2 is simply connected it would be a diffeomorphism. After composing with its inverse, projection to S3 would give a section of the Hopf map. This is impossible: on H2 the identity of S2 would factor through H2(S3)=0.

Thus a definition additionally demanding an appropriate closed transverse surface would exclude this example. K3's explicit W definition has no such additional condition. Codimension-one closed transverse loops must not be silently carried over as a criterion in codimension two. Local transverse disks exist, as they do for every smooth foliation, but they are not closed global transversals.

For the product of the round metrics, each leaf is the product of a great circle in S3 and the circle factor. It is totally geodesic and has zero mean curvature. This independently verifies geometric minimality in the stationary sense. It does not establish stable or homological area minimization. For example, deform the selected Hopf circle to

C_t(theta)=(sqrt(1-t squared) exp(i theta),t), with real |t|<1.

The product C_t x S1 has area 4 pi squared sqrt(1-t squared), strictly smaller than the original area for small nonzero t. The original leaf is stationary but unstable. The submitted proof correctly refrains from using mean curvature zero as a genus or global area bound.

The leaves are also compressible: the Hopf-circle generator is killed in pi1(M), while the other circle generator survives. Neither source imposes an extra leafwise pi1-injectivity hypothesis in the statements reviewed here.

## Residual scope and acceptance recommendation

For a closed symplectic four-manifold, the symplectic Thom theorem supplies genus minimization for an embedded symplectic surface. That is an additional-hypothesis case and does not turn W into C or provide a symplectic structure for this example. The relevant closed-ambient hypothesis is explicit in Ozsvath and Szabo, Theorem 1.1. [OS00]

Accept the submitted mathematical result under the label:

Formulation counterexample under the literal K3 weak definition; Kronheimer's original closed-positive-form problem unresolved by this work.

Do not label it a solution or disproof of Kronheimer's original question. Do not infer novelty or current literature-wide openness from this focused review. The only fresh bibliographic-verification update needed is that this review successfully retrieved and visually inspected a local binary of the Kronheimer author PDF. The author's earlier reported HTTP 403 remains an accurate historical observation; the later successful retrieval supplements it.

The author's finite checker was also replayed in normal and optimized Python modes with its self-tests. Both passed, including the expected nonclosedness value 2. These runs support the polynomial identities only. The global topology, source interpretation, smooth competitor, and Stokes obstruction were reviewed mathematically above. This review did not rerun the large input datasets or certify packaging behavior.

## Public references and fresh source verification

[K3] R. Inanc Baykur, Robion C. Kirby, and Daniel Ruberman, K3: A New Problem List in Low-Dimensional Topology, author's preliminary version, Problem 4.123, page 292. Fresh binary downloaded and page 292 rendered and visually inspected. Chapter 4 and Section 4.11 introductions also checked in extracted text. https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf

[K98] P. B. Kronheimer, Embedded surfaces and gauge theory in three and four dimensions, Surveys in Differential Geometry III (1998), 243-298. Author PDF page 49, printed page 47, Question 7.12 and surrounding paragraphs. Fresh binary downloaded and page 49 rendered and visually inspected. https://people.math.harvard.edu/~kronheim/jdg96.pdf

[S03] Alexandru Scorpan, Existence of foliations on 4-manifolds, Algebraic & Geometric Topology 3 (2003), 1225-1256, Remark 3.4 and Theorem 3.5, printed page 1235. Fresh binary downloaded and PDF page 11 rendered and visually inspected. https://arxiv.org/pdf/math/0302318

[OS00] Peter Ozsvath and Zoltan Szabo, The symplectic Thom conjecture, Annals of Mathematics 151 (2000), 93-124, Theorem 1.1, printed page 94. Public arXiv text inspected directly. No fresh binary hash is claimed by this review for this source. https://arxiv.org/pdf/math/9811087

The accompanying manifest records the three fresh PDF hashes and sizes as verification metadata. It does not contain or authorize redistribution of those PDFs, their text, or rendered source pages.
