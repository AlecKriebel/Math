# Independent adversarial audit: 6800009 / AMR-067-0009

**Verdict: PASS for the literal fixed-group-law question. No required repair.**

Audited on 3 October 2026 UTC. The reviewed public packet has nine files and manifest SHA-256 `327e376b1d14851e89294fbe8a67e1476a14eacbac3ffb3dab35c5f9313a08a9`. All eight payload hashes match the manifest. No frozen file was modified and no remote write was made.

This is a credited negative consequence of prior constructions. It is not a new-construction claim, a first-priority claim, a compact-simple-group result, or a result for an isometry-class reformulation. Classifying this packet as `already_solved` is sound provided its explanatory text continues to say “consequence of prior constructions,” rather than implying a located publication explicitly solving the named question.

## 1. Exact original target

Independently opened the author-hosted [Morgan–Pansu PDF](https://www.imo.universite-paris-saclay.fr/~pierre.pansu/problems_MTDG.pdf). Printed page 8, Section 8, Question 9, proposed by Claudio Gorodski, asks whether even index for every segment forces a left-invariant metric on a compact connected Lie group to be bi-invariant. There is no simple-group assumption or qualification that the conclusion is only up to an isometry. The adjoining discussion specifies energy on fixed-endpoint H¹ path spaces. The certificate therefore uses the correct boundary conditions and algebraic conclusion.

The [2011 MathOverflow question](https://mathoverflow.net/questions/66924/conjugate-points-in-lie-groups-with-left-invariant-metrics) is consistent with that reading. Its two currently visible answers do not supply a resolution. This check does not establish exhaustive literature priority or a current UnsolvedMath site status.

## 2. Global metric construction

For unit quaternions and the curvature-one metric q, define h=2q⊕q and F(a,b)=(a,ba⁻¹). The inverse (u,v)↦(u,vu) is global, so g=F*h is smooth, positive definite, and complete on compact SU(2)×SU(2).

Conjugating each ordinary left translation gives the exact formula

F L_(x,y) F⁻¹(u,v)=(xu,yvx⁻¹).

Each factor operation is an isometry of its independently scaled round metric. This proves left invariance for the original direct-product multiplication, for all group elements and all points, not merely at the identity.

A separate differential check gives the same conclusion: at (a,b), left-trivialized tangent vectors (A,B) map to (A,Ad_a(B−A)). Orthogonality of Ad_a for q yields 2⟨A,C⟩+⟨B−A,D−C⟩, independently of the basepoint.

The identity matrix is [[3I,−I],[−I,I]], positive definite with scalar-block determinant 2. The infinitesimal Ad defect on X=(i,0), Y=(j,0), Z=(0,k) is −2 because [i,j]=2k and the two ideals commute. A finite independent witness is even simpler: Ad_(i,1) sends (j,0) to (−j,0) and fixes (0,j), changing their g-inner product from −1 to +1. Thus g is not bi-invariant for the original law. Diagonal Ad_(i,i) preserves that cross term, as expected, so the witness does not confuse diagonal right invariance with full right invariance.

## 3. Geodesics, curvature normalization, and endpoints

For arbitrary A,B, the complete geodesic from the identity is

γ(t)=(exp(tA), exp(t(B−A))exp(tA)).

Its F-image is the product geodesic (exp(tA),exp(t(B−A))). Its derivative at zero is (A,B). Since F is an isometry, these exhaust all initial velocities; left translations then exhaust all starting points. In particular, the argument does not wrongly assume γ is a one-parameter subgroup in the original group.

Writing c₁=|A|_q and c₂=|B−A|_q is correct. Constant scaling from q to 2q divides sectional curvature by 2 while multiplying squared speed by 2. Thus the first normal Jacobi frequency remains c₁, not c₁/√2 or √2 c₁. Both factors have two normal directions. The Killing normalization is also consistent: with [i,j]=2k, the negative Killing form is exactly Q=8q. Replacing q by Q rescales the whole construction by 8.

For a moving factor, the normal Dirichlet operator has signs determined by (mπ/T)²−c², each repeated twice. The tangential operator is positive. For a stationary factor all three directions are positive and no conjugate time occurs. Product splitting rules out additional mixed Jacobi solutions; simultaneous conjugate times add their dimensions.

Consequently, if N(r) counts positive integers m with mπ<r, then

index = 2N(Tc₁)+2N(Tc₂),

nullity = 2·1_(Tc₁∈πN_positive)+2·1_(Tc₂∈πN_positive).

The strict inequality is essential. A terminal conjugate point creates nullity, not a negative direction. Both quantities are even, including coincident conjugate times and arbitrarily long segments. Constant segments have index and nullity zero for T>0. No minimizing-segment, nonconjugate-endpoint, or free-loop assumption is used.

## 4. Source correspondence and prior credit

Independently checked [Fusi–Lafuente–Stanfield v1](https://arxiv.org/html/2608.25619v1#S7), submitted 26 August 2026. Its Section 7 uses X±=(X,±X)/√2 and P=[[1,1],[1,3]] for g_(1,3,1). Direct conversion yields [[3,−1],[−1,1]], exactly the certificate's matrix with q replaced by Q. Proposition 7.3 explicitly identifies the underlying Riemannian metric with 2Q⊕Q. In source parameters its orbit map is Φ(x,y)=(x⁻¹,yx⁻¹), and FΦ(x,y)=(x⁻¹,y); the extra inversion is an isometry of 2Q⊕Q. Thus the global maps, not merely their linearized matrices, agree up to a target isometry. Theorem E's additional torsion and flow conclusions are unnecessary here. No named-question resolution is attributed to the authors.

Independently checked Barbaro [v2 Example 4.1](https://arxiv.org/html/2307.10207v2#S4), and also the [original v1](https://arxiv.org/html/2307.10207v1#S4), submitted 14 July 2023. The same example is already in v1; the certificate's older-credit dating is accurate. The invariant SU(3)×T² metrics with nonzero mixed parameter are not bi-invariant for the product law; their lifts are isometric to bi-invariant SU(3)×R² metrics. The parity implication descends because lifting a fixed geodesic segment identifies its Dirichlet variation fields and index form, including a segment whose projected endpoints coincide. No descent of the cover's isometry itself is required. This genuinely supplies older compact-connected examples, though not the same simply connected semisimple product example.

Neither checked paper was found to discuss Morgan–Pansu or Gorodski's question. The packet accurately separates a source construction from its consequence for the present problem. No earliest-priority claim is established or needed.

## 5. Independent diagnostics and adversarial controls

The packet's verifier was executed with its file-output call intercepted, preserving the frozen directory. Its output matched the saved JSON: 128 rational-quaternion action cases and 28,224 parity cases passed.

Added `independent_controls.py` in this separate audit directory. It imports no candidate-verifier code and uses only Python's standard library. Results:

- Derived the Levi-Civita connection from the non-diagonal metric and direct-product brackets using the Koszul formula.
- Verified torsion freedom and metric compatibility, and equality of the resulting curvature with the pulled-back round-product curvature on all 216 basis triples.
- Checked 729 exact characteristic polynomials for curvature Jacobi operators, with roots 0,0,c₁²,c₁²,c₂²,c₂².
- Checked the explicit geodesic's left-velocity derivative against the Euler–Arnold equation on 729 ternary velocities.
- Independently enumerated signs of rational normalized Dirichlet eigenvalues on 244 endpoint ratios. Forty-one integer ratios detect the erroneous inclusive-endpoint alternative.
- Included finite Ad positive/negative controls and an S² odd-index control, which would reject a parity argument that ignored normal dimension.

All checks passed. These are finite algebra and convention controls, not a replacement for the global all-geodesic proof.

## 6. Accounting and audit limits

Retaining one investigative turn is consistent with the supplied chronology: a substantive shear candidate was derived before the prior construction was located. Source identification, finite diagnostics, and this audit do not create additional proof-attempt turns. No attempts 2–5 are present in the frozen ledger. The appropriate recorded result is `already_solved`, 1/5 used, with the qualified prior-construction explanation retained.

I verified the local frozen packet, source correspondence, original target, mathematical proof, diagnostics, and ledger consistency. I did not independently rerun every remote repository-history search recorded in GATE_REPORT.md, nor verify live UnsolvedMath access or queue state. Those are provenance/publication-process limitations, not defects in this negative mathematical answer.

Optional clarifications, not repairs: state Q=8q explicitly; give the displayed γ(t); cite Barbaro v1 beside the 2023 claim; retain a sentence explaining the covering-space index argument if the older example is emphasized. The existing packet is mathematically and attribution-wise publishable at its exact stated scope, subject to whatever separate publication authorization applies.
