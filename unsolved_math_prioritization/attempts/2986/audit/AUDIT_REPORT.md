# Independent audit: KP-4.110, problem 2986, rank 922

## Decision and exact accepted object

**ACCEPTED as a bounded mathematical partial, with no repair to the frozen author artifact.** The investigation remains unresolved after four of five allowed approaches. No example answering KP-4.110, universal Weinstein-existence theorem, novelty claim, formal proof certification, or human peer review is established by this audit.

The exact accepted author archive is `WEINSTEIN_TWO_HANDLEBODIES_2986_AUTHOR_SAFE_FREEZE.zip`, 15,453 bytes, SHA-256 `d322363aa52fb7f45110c3a66be3ed3381cba5cd23ce2dbe6ce20c283734b25b`. Its original external manifest is 2,111 bytes, SHA-256 `febab4c31b53b7d4a6f5844b22c808b1593f17e4006fa1c3260e5f0818a42cad`. All nine members match their independent external pins. Those two files are included unchanged in this audit packet. No corrected author archive is needed or asserted.

Accepted mathematical scope:

1. A specified primitive of the standard symplectic four-ball has a nonconstant periodic Liouville orbit, yet is joined to the standard Weinstein primitive by a boundary-fixed Liouville homotopy.
2. Every covering of a genuine smooth 2-handlebody has vanishing homology above degree two; the analogous assertion for local coefficients holds.
3. Ordinary handle attachments of index at most two preserve homology in every degree at least three. Thus low-index attachment does not repair the known product construction's nonzero third homology.
4. An exact mixed-torus split can be reassembled as a Weinstein filling when each particular split component has a compatible Weinstein replacement on that same smooth component, with the boundary identifications preserving all marked attaching data.

The fourth conclusion includes the parameterized smooth/contact attaching neighborhoods and the corresponding framing, not merely an unmarked boundary contactomorphism or Weinstein fillability on some other manifold. The author report's phrase “marked round-handle attaching data” and its proof that the marked smooth attaching data agree are essential to acceptance. Dropping that hypothesis is not accepted.

## 1. Target and inherited-record identity

The problem concerns existence of a compact smooth four-dimensional handlebody with only indices 0, 1, and 2, carrying an exact convex symplectic filling whose induced contact boundary is not filled by any Weinstein structure on the same smooth manifold. An obstruction to one primitive being gradient-like, or even to one Liouville-homotopy class becoming Weinstein, is insufficient.

The entire catalog, complete problem dataset, and research-result dataset were independently read and SHA-256 checked, at 21,735,099, 68,931,837, and 80,334,822 bytes respectively. Their pins agree with the author's SOURCE_AUDIT.json. Exactly one catalog record and one complete problem record match ID 2986. The catalog records rank 922 and KP-4.110. The catalog ID is a decimal string; the complete-problem ID is an integer, and the audit handles those actual types explicitly.

The full exact-ID record, including background and dated literature triage, was inspected. The KP-4.110 research-report entry is empty. No inherited substantive proof or computation was found. The statement digest is `fbb338574ae36b73600c45c1e1af5f6354092a54dc046bec9917d003718863ac`. The digest of the full record/report pair is `10aa12fe2316986e19051d6c3fb596d6d28abd9ae9fd65629d36e81301aba8f6`, using the author's specified default `json.dumps([record, report], sort_keys=True)` UTF-8 serialization. Both match the independently read catalog fields. This identity check does not turn historical triage into a proof of continued openness.

The directly inspected K3 author preliminary text, Problem 4.110 on printed page 282, agrees with the target. The author's failed retrieval of the public problem page is disclosed; this audit does not attribute unobserved contents to that site. Historical bounded GitHub search records are provenance, not a comprehensive novelty or prior-work certificate.

## 2. Complete mathematical review

### 2.1 Smooth primitive, symplectic form, and periodic orbit

Use coordinate order (q1,q2,p1,p2), omega = dq1 wedge dp1 + dq2 wedge dp2, and lambda0 = (q dot dp - p dot dq)/2. The report's f equals -p1 q2 + p2 q1 - (p1 q1 + p2 q2)/2. The signs in both the differentiated primitive and the Liouville field are correct.

The cutoff is genuinely smooth. The function eta(u) is zero on the nonpositive half-line and exp(-1/u) on the positive half-line; all one-sided derivatives at zero vanish. The two denominator terms cannot simultaneously vanish: that would require s at least 3/4 and at most 1/2. Thus chi is smooth, equals one for s at most 1/2, and zero for s at least 3/4. Consequently F = chi(|q|^2+|p|^2) f is smooth and zero on an open collar of the unit sphere.

For every parameter t in [0,1], d(lambda0 + t dF) equals omega exactly, including the transition shell. The shell's derivatives of the cutoff do not threaten nondegeneracy. The symplectic form is constant and nondegenerate. The Liouville field on the boundary collar remains (q,p)/2, and its derivative of the squared-radius defining function is one on the unit sphere. It is strictly outward. The induced boundary contact form is literally unchanged, not only contactomorphic. The path is therefore a Liouville homotopy of compact domains fixed near their boundary.

Where the cutoff is one, differentiating the polynomial yields coefficients (-p1+p2, -p1-p2, -q2, q1). Contraction with omega sends a field (a,b) to a dot dp - b dot dq. Hence the field at t=1 is (Jq,p+Jp), with J(q1,q2)=(-q2,q1). On p=0, q evolves by rotation. The circle q=(cos(theta),sin(theta))/2 has constant squared radius 1/4, remains inside the cutoff-one region, has nonzero velocity, and closes after time 2 pi.

For a Weinstein gradient-like Lyapunov function, its derivative along the nonstationary orbit would be strictly positive. Integrating over the closed orbit contradicts return to the same function value. Thus this primitive admits no such Weinstein Lyapunov function. In contrast, the standard primitive with the squared norm has one nondegenerate index-zero critical point and strictly increasing squared norm away from it. Reversing the displayed homotopy returns the example to a Weinstein structure on the same ball with the same boundary form. Proposition 1 is correct and specifically refutes a primitive-level obstruction test, not the original problem.

Independent finite algebra was performed with rational 4 by 4 matrices, without importing the author's sparse-polynomial functions. Writing Omega for the matrix of omega and H for the symmetric Hessian of f gives A = (1/2)I + Omega H for the linear field in the cutoff-one region. The independently reconstructed A has q-block J and p-block I+J. It satisfies A-transpose Omega + Omega A = Omega, trace(A)=2, invariance of p=0, and J squared = -I. The coefficient matrix of the primitive gives the required exterior derivative. These calculations corroborate the algebra; the smoothness, closed-orbit existence, and Lyapunov contradiction are arguments above, not inferred from numerical trajectories or finite samples.

### 2.2 Covers and local coefficients

A smooth handle decomposition of indices at most two gives a homotopy-equivalent CW complex with one cell in each handle's index. For an arbitrary covering of the manifold, pull back that covering to the CW model. A homotopy equivalence lifts to a homotopy equivalence of the corresponding covers, since it induces the appropriate fundamental-group identification. Lifting cells cannot increase dimension, even for infinitely many sheets or components. The covering CW complex has no cells in degrees greater than two, so its cellular homology in those degrees vanishes for every constant abelian coefficient group.

For local coefficients on the original manifold, the cellular chains with the coefficient module are obtained from the universal-cover chain complex. Its groups above degree two are zero, and remain zero after forming those local-coefficient chain groups. Proposition 2 is correct. The converse inference from homological vanishings to existence of a smooth handle decomposition is neither proved nor used.

### 2.3 Persistence under low-index attachment

A sequence of finitely many handle attachments of indices zero, one, or two gives a relative CW model with cells only in those dimensions. For each k at least three, both adjacent relative groups in the homology long exact sequence, in degrees k+1 and k, vanish. The induced map H_k(X;A) to H_k(X';A) is therefore an isomorphism. This proves Proposition 3 for the stated constant coefficients, not only over a field.

For a closed connected oriented three-manifold M, projection from M times an interval is a homotopy equivalence, and its third integral homology is Z. Subsequent finite low-index attachment preserves this group. A true 2-handlebody has no such third homology. Christian–Menke's round symplectic 1-handle consists of a Weinstein 1-handle followed by a Weinstein 2-handle, so it falls within this argument. This excludes attachment-only repairs of the product-type constructions. Removing or replacing a piece, or attaching a 3-handle, lies outside the proposition; the report correctly leaves those possibilities unproved.

### 2.4 Boundary-marked mixed-torus reconstruction

The source theorem required here is Christian–Menke arXiv:1807.03420v4, Theorem 1.1 in its exact case. A mixed torus with the prescribed two-basic-slice neighborhood is required. A merely convex torus is not enough, and the splitting slope belongs to the finite allowed interval fixed by the contact neighborhood. The split filling may be disconnected.

Assume the exact split filling's particular smooth components admit Weinstein structures with coorientation-preserving boundary identifications compatible with the marked attaching neighborhoods and framing. Contact forms related by a positive factor have canonically isomorphic symplectizations: for a contactomorphism psi satisfying psi-pullback(alpha2)=g alpha1, the map (s,x) to (s-log(g(x)),psi(x)) identifies the symplectization one-forms. Taking sufficiently long collars accommodates the finite shifts; changing the transverse boundary graph and its collar is a Weinstein-preserving boundary adjustment. This justifies using the prescribed local attaching data with the replacement structures.

Remark 2.6 then realizes the prescribed round attachment as a Weinstein 1-handle and a Weinstein 2-handle. The same marked smooth attaching embeddings/framing reconstruct the same underlying W, and the contact handle attachments recover the designated outgoing contact boundary. An arbitrary boundary diffeomorphism that changes the attaching data would not suffice; no extension of an arbitrary boundary mapping class over the interior is silently assumed. With the stated markings, Proposition 4 is correct.

Taking the contrapositive gives only failure of at least one compatible replacement if a target example admits such a split. It does not establish existence of the mixed torus. Applying Proposition 3 gives H3(W') isomorphic to H3(W)=0 for a hypothetical target handlebody, but this necessary homological statement does not prove W' itself has a 2-handlebody decomposition. The original report is appropriately explicit on both limitations.

The source's Theorem 1.4 and Corollary 1.5 do cover Legendrian surgery on a knot in the standard contact sphere that has been stabilized with both signs. They reconstruct exact fillings from the sphere's standard filling by the corresponding symplectic 2-handle, yielding the stated special-case Weinstein conclusion. Neither one-sign stabilizations nor arbitrary contact boundaries are included.

## 3. Primary sources and current status

All seven complete PDF byte streams were independently hashed, magic-checked, and matched to the frozen source metadata. Fresh downloads from the stated public primary-source URLs independently produced the same seven byte streams. The source-specific audit records the bibliographic metadata, exact page/theorem scope, and fresh retrieval checks without redistributing source documents or text.

The crucial correction is confirmed: Christian–Menke v4 (21 May 2025), Remark 1.3, withdraws the earlier strong-filling formulation. The theorem is stated for exact or weak fillings. The authored proof uses only exact fillings and does not assert that the strong-filling decomposition survives. The distinct 2019 higher-genus splitting preprint is not substituted for this corrected theorem.

Cieliebak–Eliashberg's higher-dimensional existence results do not provide the needed dimension-four theorem. Their separate four-dimensional cobordism alternative has additional overtwisted negative-boundary hypotheses. Neither provides the fixed positive contact-boundary conclusion required here.

Breen–Christian's inspected v3 states an accepted-version notice. That attribution is accurate. Supplementary current publisher metadata now identifies the article as published in Journal of Topology 18(4), e70052, first published 20 November 2025, DOI 10.1112/topo.70052. This is a bibliographic update, not a correction to the accepted mathematical argument or a change to the immutable author archive. Stabilization changes dimension, and its homotopy questions do not imply the requested fixed-manifold, fixed-boundary conclusion.

Hozoori's arXiv entry still has the inspected v1 of 23 September 2024. The selected theorems concern Liouville interpolation/product-type and dynamical hypotheses. They do not furnish a compact exact 2-handlebody answering the target. The current source review is bounded and does not certify the external papers' complete proofs or exhaustive literature coverage.

## 4. Artifact integrity, replays, and adversarial scope

The frozen author package is immutable. Its checker was read in full before execution. It uses explicit raising checks rather than Python assert for mathematical conditions, validates exact member hashes, reconstructs exact rational polynomial data, fixes partial-status limits, and checks deliberately corrupted controls. Normal and optimized isolated executions from relocated directories each passed 85 positive checks and three internal negative controls, with byte-identical output. This is a diagnostic result, not proof certification.

The direct author-checker adversarial suite exercises unrehashed content corruption, consistently rehashed algebra and status changes, missing and extra members, nested directories, symlinks, duplicate manifest entries, and unchecked command arguments, in both normal and optimized modes. All expected outcomes are recorded in AUDIT_TEST_RESULTS.json.

Two additional controls deliberately replace the inner trust root: a source-metadata rewrite and a rank rewrite with a recomputed internal manifest. The author's checker accepts these. This is disclosed as a trust-boundary limitation: its finite semantic checks do not validate every metadata assertion, and an attacker-supplied manifest is not an independent signature. The independent wrapper hard-pins the exact author archive and external manifest and separately checks rank, so consistently rewritten author packets are rejected before replay. Replacing executable code inside a rewritten author ZIP is also rejected at this boundary. Do not use an arbitrary rehashed copy as the accepted author artifact.

The audit packet's own member manifest is an integrity index, not an unforgeable trust anchor. Its external manifest and a separately pinned bootstrap bind the exact audit ZIP before extraction. The bootstrap rejects missing, altered, or unsafe archives and uses isolated normal and optimized replay. External source/corpus checks require both explicit input directories; a replay without those files explicitly reports that they were not supplied. Full-input normal and optimized runs verified all three entire datasets, the unique record/report bindings, and all seven PDFs. Changed or missing source inputs fail closed. Source hashes attest byte identity, not theorem truth.

## 5. Remaining obstruction and stopping decision

A positive answer still requires one and the same W to satisfy all of the following: an actual smooth 0/1/2-handle decomposition; a smooth exact, everywhere nondegenerate symplectic form; a convex boundary carrying the specified contact structure; and an obstruction to every Weinstein structure on that W inducing that contact boundary. A negative answer requires a Weinstein-existence theorem for every such pair.

The current work supplies neither. The explicit ball example is already Weinstein-fillable, cover homology cannot distinguish the required subclass, the standard product obstruction cannot be removed by low-index attachment alone, and the mixed-torus criterion has unestablished splitting/classification hypotheses in general. There is no justified fifth route in this artifact. Accepting the four bounded propositions therefore leaves the target **partial, stalled after 4/5, unresolved**.

No GitHub writes, queue changes, release, DOI creation, external outreach, or publication of source documents or dataset contents was performed during this audit. The safe audit packet contains authored audit material, exact diagnostics, immutable authored-artifact copies, and public verification metadata only.
