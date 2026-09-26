# Fresh adversarial preprint review, round 1

**Checkpoint:** 2026-09-26T21:21:40Z (26 September 2026, America/Los_Angeles).

**Object:** *Radial orthogonality does not imply dual 1-conformal flatness*, version 1.0.1, dated 26 September 2026.

**Reviewer:** independent Codex adversarial subagent; this is an AI review, not external human peer review.

**Completion estimate:** 100% of this bounded preprint review. This percentage does not estimate historical novelty or certify the absence of all possible errors.

## Verdict and actionable findings

**No actionable preprint issue found.** The manuscript is ready for circulation as an **unrefereed, carefully attributed counterexample to the printed implication**, with the historical-priority limitations it already states. I found no mathematical gap requiring correction, no unsupported first-resolution claim, and no rendering defect that impedes reading.

| Severity | Findings |
| --- | --- |
| Blocking mathematical error | None found |
| Major mathematical or attribution issue | None found |
| Minor issue requiring a manuscript change | None found |

This verdict applies to the source and PDF identified below. It is not a verdict on journal acceptance, originality, or sources that remain unread. No manuscript edits were made by this reviewer.

## Independence, method, and inspected material

I first read the manuscript and reconstructed its mathematical argument directly, before consulting any earlier review. I checked the curvature transformation, endpoint first variation, cubic tensor, dual connection, and parameter conversion myself. I did not consult earlier mathematical proof reviews. Only after reconstructing these arguments did I inspect the source-audit records and portions of the priority-review documentation to test whether the manuscript describes those records fairly.

I visually inspected all four pages of the final preprint PDF, the scanned original question on printed p.126 (PDF page 2), item 3(a) on printed p.125, Kurose's definition and Proposition 1 on printed p.428 (PDF page 2), and Matsuzoe's equation (2.1) and its surrounding explanation on printed p.178 (PDF page 4). The original question PDF has no usable extracted text; the finding about its quantifiers is based on its rendered page, not a text-search failure. The PDF and TeX contain the same mathematical statements and version/date. Displayed equations, references, and page boundaries are legible and unclipped.

Primary-source PDFs inspected:

- Furuhata, Matsuzoe, and Urakawa (1998), *Open Problems in Affine Differential Geometry and Related Topics*, pp.125-126, local `tmp/original_1998.pdf`.
- Kurose (1994), *On the divergences of 1-conformally flat statistical manifolds*, p.428, local `tmp/kurose_1994.pdf`.
- Matsuzoe (1999), *Geometry of contrast functions and conformal geometry*, p.178, local `/Users/alec/Downloads/Download.pdf`.

No person was contacted, no outreach was prepared, and no additional agents were spawned.

## Accepted mathematical reasoning and attempted falsifications

### 1. Exact target, quantifiers, and allowed examples

The printed Question 3(e) takes an arbitrary center in an n-dimensional statistical manifold, constructs the distribution using the connection-geodesic inside a connection-convex neighborhood, explicitly removes the center, and asks about the **dual** statistical manifold when **every** such distribution is integrable. There is no nonzero-cubic-tensor condition or exclusion of Levi-Civita connections. Item 3(a) explicitly calls a metric paired with its Levi-Civita connection a statistical manifold. The manuscript therefore does not answer a weakened or altered question.

Kurose permits a more general nondegenerate metric; a positive-definite example is still an admissible counterexample. No premise from a different item in the problem list must be imported into 3(e). Dimension three is enough to refute the general implication, and the manuscript separately proves the extension to every n at least three.

### 2. First variation for every admissible center and neighborhood

For a fixed center p and the smoothly varying unique affine connecting segments in a convex neighborhood, define

\[
E_p(q)=\frac12\int_0^1 h(T,T)\,du.
\]

For an endpoint variation, metric compatibility gives the derivative of the integrand, torsion-freeness exchanges the two variation derivatives, and integration by parts yields

\[
dE_p|_q(w)=h_q(w,T(1))-h_p(V(0),T(0))
-\int_0^1h(V,\nabla_TT)\,du=h_q(w,T(1)).
\]

The two discarded terms vanish because the initial endpoint is fixed and the selected curves are affine geodesics. If q differs from p, T(1) cannot vanish: uniqueness for the geodesic initial-value problem would otherwise make the geodesic constant. Positive definiteness then gives dE_p(T(1))>0. Consequently D is a smooth regular kernel of an exact one-form on the punctured neighborhood, and the connected pieces of energy level sets are integral hypersurfaces.

This proof does not require the selected segment to minimize the distance in the entire manifold. Thus a global distance cut locus does not invalidate the assertion for an admissible convex neighborhood. The manuscript properly limits its distance-squared identification to sufficiently small normal neighborhoods. The center is excluded in both source and proof. No global foliation through the center or across a cut locus is claimed. No choice specific to one center occurs in the argument.

### 3. The 1-conformal convention and pointwise obstruction

At alpha=1, the formula on Kurose p.428 is precisely

\[
\widehat h=e^\varphi h,\qquad
\widehat\nabla_XY=\nabla_XY-h(X,Y)\operatorname{grad}_h\varphi.
\]

It is a prescribed simultaneous metric and connection change. Ordinary conformal flatness of the round cylinder is irrelevant to this implication.

For the Levi-Civita connection, put V=grad(phi) and B(X,Y)=-h(X,Y)V. Independently expanding the curvature difference gives

\[
(\nabla_XB)(Y,Z)=-h(Y,Z)\nabla_XV,
\qquad B(X,B(Y,Z))=h(Y,Z)h(X,V)V.
\]

Therefore

\[
\widehat R(X,Y)Z=R(X,Y)Z-h(Y,Z)A(X)+h(X,Z)A(Y),
\quad A(X)=\nabla_XV-h(X,V)V.
\]

All signs agree with the curvature convention stated in the manuscript. Flatness necessarily forces equation (3); treating A as an unrestricted endomorphism only weakens the necessary condition and cannot produce a false obstruction.

For an orthonormal sphere pair e1,e2 and a Euclidean direction e3, the product curvature is

\[
R(e_1,e_2)e_2=e_1,\qquad R(e_1,e_3)e_3=0.
\]

Equation (3) would force A(e1)=e1 and A(e1)=0 at the same point. This contradiction is pointwise, so it rules out flat conformal changes on every nonempty open subset. Metric compatibility gives the required self-duality of the base structure. Extra Euclidean factors preserve the same three-vector calculation for every n>=3. Nothing relies on a spherical coordinate chart, so the poles are not exceptions. No dimension-two conclusion is inferred.

I also checked the optional three-dimensional projective-curvature calculation. With the stated sign convention, Ric=diag(1,1,0) and W(e3,e1)e1=-e3/2. Kurose's Proposition 1 supports the stated dual projective-flatness criterion. This paragraph is an additional check, not a premise needed to establish the direct contradiction.

### 4. Non-self-dual deformation, parameter domains, and duality

Writing eta=dt, the proposed connection change is symmetric in X,Y and hence preserves torsion-freeness. Direct differentiation of h1=e^t h0 yields

\[
(\nabla^1_Xh_1)(Y,Z)
=-\eta(X)h_1(Y,Z)-\eta(Y)h_1(X,Z)-\eta(Z)h_1(X,Y).
\]

It is totally symmetric and its value on three copies of partial_t is -3e^t, which is nonzero at every finite t. Thus the example is statistical and nowhere self-dual.

For a base affine parameter u and a new parameter s, the transformed geodesic equation requires

\[
\frac{d^2u}{ds^2}+2\frac{dt}{du}\left(\frac{du}{ds}\right)^2=0,
\quad\text{equivalently}\quad
\frac{ds}{du}=C e^{2t(\gamma(u))},\ C>0.
\]

This agrees with the manuscript. On every compact connecting segment, this derivative is smooth, strictly positive, and bounded above and below away from zero. The parameter can therefore be normalized to [0,1], with a smooth inverse. The inverse conversion exists as well. Hence the connections have the same connecting geodesic paths within the relevant convex neighborhoods, not merely a formal equality of accelerations at one point. Uniqueness of paths is preserved. No global affine completeness is needed. The terminal tangent is multiplied by a nonzero scalar, while h1 is a positive scalar multiple of h0, so the radial orthogonal distributions agree. Lemma 1 applies for every center and admissible neighborhood.

Substituting the defining duality identity gives

\[
(\nabla^1)^*_XY=\nabla^0_XY-h_0(X,Y)\partial_t.
\]

In a further 1-conformal change, h1 grad_h1(psi)=h0 grad_h0(psi) as a tensor product. Thus its changed connection is the base 1-conformal connection with potential t+psi. The changed metric is also e^psi h1=e^(t+psi) h0. Any local flattening would contradict the already established base obstruction. This is a genuine reduction to a proved statement, not a transfer to an unsupported equivalent claim.

Matsuzoe p.178 prints exactly the projective formula with tau=dpsi and the accompanying metric factor exp(psi), identifying it as (-1)-conformal equivalence. The attribution in the manuscript is accurate and explicitly disclaims novelty for the deformation.

## Supplemental computation

I read both checker implementations and reran them after the analytic reconstruction:

- `python3 verification/verify_exact.py`: passed the complete pointwise systems in n=3,4,5, constant-curvature controls for 0,+1,-1, the dimension-two boundary control, and the stated Ricci/projective-Weyl evaluation.
- `/Users/alec/Documents/Math/.venv/bin/python verification/verify_symbolic.py`: passed all **403** checks under Python 3.9.6 and SymPy 1.14.0. This includes the independently derived coordinate curvature, all 81 arbitrary-potential curvature-transformation components, cubic and dual formulas, and connection-change composition.

The system and bundled Python interpreters initially lacked SymPy; the existing project environment supplied the documented pinned dependency. This is not a manuscript or reproducibility defect. The checks are correctly described as supplemental tensor calculations, not validation of the quantified first-variation argument or a proof-assistant formalization. Finite checks in n=3,4,5 do not establish all n; the dimension-independent three-vector proof does.

## Historical wording and exact remaining gaps

The current title, abstract, and scope paragraph claim a negative answer to the printed implication, **not** a first resolution or a verified open problem as of publication. They explicitly identify unresolved historical priority, acknowledge classical ingredients, and attribute the exact deformation to Matsuzoe. The dated source and priority records support the narrowly reported fact that their bounded search did not locate an earlier explicit answer. The later live-database inspection is accurately distinguished from the older access limitation, and its generated status report is expressly not treated as a priority certificate.

I did not independently repeat the literature search or inspect Kurose's 1999 affine-realization paper, Binder-Simon's 2000 problem list, or the full content of Kurose's 2016 talk. An earlier explicit or implicit resolution remains possible, as the manuscript says. This is an unresolved **historical gap**, not an unfilled step in the counterexample proof. No new novelty clearance follows from this review. The report makes no claim about external human peer review or formal verification.

## Exact review identities

SHA-256 digests were checked after visual inspection and again at the concluding checkpoint:

| Object | SHA-256 |
| --- | --- |
| `manuscript/paper.tex` | `3a9e3cd1e012480afcb30438e5e292a6ff03c045f63b7f06dbc22654351a4482` |
| `output/pdf/paper.pdf` | `0dc15e4fa038dcb80cbfd062ac7636f2c790e42885c940626ea726626b62fd8a` |
| `tmp/original_1998.pdf` | `fa552d73c0f1e1017608102a7a80eff048cd3d95ed413ae04c2fdf710da3b8f5` |
| `tmp/kurose_1994.pdf` | `adfe06cd01217b31e82d3371dd7cd50803c3ff24380a168b2db215883875d138` |
| `/Users/alec/Downloads/Download.pdf` (Matsuzoe 1999) | `a10835acdc04536bfacb9a4c2698a5ce7d5546fd7f48cf8af4ff708baeda2bea` |

**Strongest verified conclusion:** the paper supplies a valid explicit counterexample in every dimension n>=3, including the stated nowhere-zero-cubic example in dimension three. **Required preprint corrections found in this round: none.**
