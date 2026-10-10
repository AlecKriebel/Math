# Independent audit: ID 2999, KP-4.123

Date: 2026-10-06. Queue rank: 923. Mathematical disposition: **accept the formulation counterexample; retain unsolved, 2/5, for the original closed-form problem.** No novelty claim and no full-original-resolution claim are accepted. No GitHub write was performed.

## 1. Exact acceptance

The Hopf-product foliation of S³ × S¹ is a counterexample to genus minimization under the particular weak differential-form condition printed in K3 Problem 4.123. Its leaves are smooth oriented coorientable embedded tori, each integrally null-homologous and therefore homologous to an embedded sphere. A global positive leafwise form satisfies that weak condition. No globally closed form can be positive on these leaves.

This does **not** refute Kronheimer's original Question 7.12, does not resolve the S² × S² subquestion, does not refute a variant restricted to nonzero homology classes, and does not refute a version minimizing truncated negative Euler characteristic instead of genus. The torus and sphere both have zero truncated negative Euler characteristic. K3 explicitly asks about genus.

The author proof needs no mathematical correction. A three-field scope-guard omission in its checker was reproduced and repaired in a separate derivative. The original nine-file archive remains byte-for-byte preserved. Acceptance of the corrected package is confined to the exact externally pinned files and the claims specified here; a successful finite checker is not a proof certificate for arbitrary edited prose.

## 2. Primary-source distinction and hidden hypotheses

The auditor freshly retrieved and visually inspected the complete relevant pages of [K3](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf), p. 292, and [Kronheimer](https://people.math.harvard.edu/~kronheim/jdg96.pdf), PDF p. 49 / printed p. 47. K3 requires positivity on the leaf planes and dω(v,w,z)=0 for two leafwise vectors. Kronheimer requires an actually closed positive two-form on a closed oriented four-manifold. These are distinct hypotheses, not an OCR ambiguity.

K3's Chapter 4 introduction (pp. 189–190), Section 4.11 introduction (p. 288), the problem, and all four accompanying remarks were checked. No additional simply-connectedness, nonzero leaf class, or global closedness assumption there rescues the literal weak formulation. The example is closed even though the abbreviated K3 statement does not explicitly demand it. Coorientability means orientation of the rank-two normal bundle; the example also has a global normal framing.

[Scorpan, Theorem 3.5](https://arxiv.org/pdf/math/0302318), PDF p. 11 / printed p. 1235, uses the same two-leaf-vector condition for geometric tautness. The author correctly uses zero mean curvature as a corroborating geometric check, not as homological area minimization or global stability. [Ozsváth–Szabó, Theorem 1.1](https://arxiv.org/pdf/math/9811087), PDF p. 2 / printed p. 94, applies to symplectic surfaces in closed symplectic four-manifolds; it does not convert the weak condition into a genus bound. [Bowden, Examples 2.6–2.7](https://arxiv.org/pdf/1105.4444) concern general compact leaves and provide no closed-positive-form hypothesis for this example.

All five source binaries were freshly retrieved and hashed. Four match the author's pins exactly. Kronheimer's binary was also successfully retrieved during this audit, despite the author's earlier reported HTTP 403. That is new retrieval history, not a reason to overwrite the historical author record. SOURCE_VERIFICATION.json records the new pin and inspection. No source PDFs, extracted text, or screenshots are distributed.

A bounded public search for the original question and formulation distinction produced no verified general resolution. This is not a proof that the original problem remains open in all literature, and is not evidence of originality. The accepted statement is only that this work does not resolve it.

## 3. Independent mathematical audit

### Global foliation, orientations, and forms

The map q=h∘pr₁:S³×S¹→CP¹ is a submersion with connected fibers S¹×S¹. Therefore its fibers are exactly the leaves of a smooth nonsingular two-dimensional foliation. The free diagonal circle action on S³ has the nowhere-zero generator R=(-y₁,x₁,-y₂,x₂), while the second circle has T=(-v,u). Their product actions commute and span the leaf tangent bundle globally. Orient the leaves by (R,T); orient the quotient by CP¹. This produces a compatible ambient orientation and a transverse orientation.

There is no connection-form patching problem. The form α=x₁dy₁−y₁dx₁+x₂dy₂−y₂dx₂ is the restriction of a polynomial ambient form, not a local angular coordinate. It is invariant under the Hopf action and α(R)=1. Similarly η=u dv−v du is a global form on the second circle. Both pull back globally to the product. Writing η as dt would be harmless only as shorthand for this global circle form, not for the differential of a globally defined real angle.

Even a stronger normal-triviality convention would not exclude the example: at (z₁,z₂) the complex vector V=(-conjugate(z₂),conjugate(z₁)) and iV give a global real frame for the horizontal complex line on S³. Their images frame TM/TF.

The form ω=α∧η satisfies ω(R,T)=1. For Q=x₁²+y₁²+x₂²+y₂², the ambient identity i_R dα=−dQ restricts to zero on TS³. Also dη=0 on S¹ and i_T dα=0. Consequently dω(R,T,z)=0 for every tangent z; alternating multilinearity gives the full required condition for arbitrary two leaf vectors. At (1,0,0,0;1,0), the tangent vectors ∂x₂, ∂y₂, ∂v give dω=2, so the form is genuinely nonclosed.

The proof's supplementary metric statement is correct: a Hopf fiber is a great circle, hence a geodesic of round S³; its product with S¹ is totally geodesic for the product metric and has zero mean curvature. This is not needed to establish the differential-form hypothesis.

### Integral bounding manifold and actual competitor

The set D={y₂=0, x₂≥0} within S³ is a closed hemisphere of the smoothly embedded sphere {y₂=0}. Along its equator x₂=0 the boundary-defining function has nonzero differential on that sphere. Thus D is a smooth embedded disk with smooth boundary C={(z₁,0):|z₁|=1}; it has no hidden corner or singularity. Orient D so that its boundary orientation is R. Then D×S¹ is an oriented embedded compact three-manifold with boundary exactly the oriented leaf C×S¹. This proves integral null-homology directly.

Independently, integral Künneth gives H₂(S³×S¹;Z)=0, with no Tor summands because the factor homology groups are free. The author's rank check only checks the numerical convolution; the torsion assertion is supplied by this standard integral calculation and the explicit bounding manifold.

Inside a coordinate four-ball, take a small ordinary three-ball in a three-dimensional linear slice. Its boundary is an embedded connected oriented S², also an integral boundary. It is therefore homologous to the leaf. Comparing genus 0 with genus 1 proves failure of genus minimization without using the empty surface or any disconnected-surface convention. The coordinate ball can be chosen off the leaf if desired.

### Exclusion from the original question

A globally closed leaf-positive Ω would have strictly positive integral on this compact oriented torus. Stokes on D×S¹ forces that integral to vanish. Thus **every** globally closed positive candidate is excluded, not just the particular ω. The counterexample cannot be upgraded to the original question by selecting a different two-form.

## 4. Input, code, and artifact audit

The 15,006-byte author ZIP matches SHA256 a1f4ad02d89248ad6a1f0d499951ee0233a58d00083b0ca2d08156d0ac661b03. Its external manifest, receipt, exact nine-member allowlist, every size/hash, and CRC were checked. Source and corpus contents are excluded from the safe archive.

The three complete input corpora were independently rehashed and matched the supplied sizes and SHA256 pins. Exact ID 2999 occurs once in both catalog and problem array; the problem number, statement hash, and complete record/report hash match. The report key is actually absent from the report dictionary; its effective inherited report under the documented normalization is {}. This distinction is recorded rather than claiming an explicit empty record existed. The complete background was manually reviewed as literature/bibliography triage, not a prior proof or computation. No selection or novelty conclusion is inferred merely from absence of a report.

The original checker was copied to a path containing spaces and executed from an unrelated working directory under ordinary Python, -O, -I, and -I -O. Both ordinary and self-test runs pass. Complete corpus replays pass under -I and -I -O. Negative controls reject partial/missing inputs, same-length corruptions of each corpus, five guarded status errors, and deliberately wrong algebra/homology identities. All 39 expected outcomes were observed.

Three contradictory metadata edits escaped the original scope guard: overall status, S²×S² subquestion status, and recommended queue status. The finite math identities still passed, illustrating why a checker pass alone does not establish publication scope. The hardening patch adds explicit checks for exactly these fields. It changes only check.py; the other eight authored files are identical. It does not change the proof, corpus pins, approach count, or historical records.

The corrected checker passed 26 relocated replay/control cases, including rejecting all three formerly unguarded overclaims in isolated normal and optimized modes. Ten additional private synthetic controls, with deliberately rebased fixture digests solely to reach internal branches, rejected wrong schema, duplicate/missing IDs, mismatched problem number, nonempty report, changed statement/background, and changed catalog content pins. These controls never bypass the immutable corpus pins in production.

An independent checker uses direct tensor coefficients and exact integer arithmetic, without importing the author's differential-form engine. It verifies the ambient contraction identity on the complete 3^6 grid and all 4,374 resulting components, plus positivity pairings and the nonclosedness witness. Each coordinate degree is at most two, so the three-point grid is unisolvent: this establishes the polynomial identities, rather than merely numerical agreement at sample points. Both isolated normal and optimized runs pass. No computation is described as a formal verification of the global topology.

The archive verifier uses external archive and manifest pins, exact membership, every member size/hash, CRC, and unsafe-path/symlink/duplicate rejection; it extracts nothing. Integrity controls and patch-application results are separately recorded. This integrity layer, rather than text pattern matching in check.py, binds the proof and metadata to the audited bytes.

## 5. Publication scope and reproducibility

The accepted mathematical result is a formulation counterexample, with the original stronger problem unresolved by this work. Record status as unsolved, turns 2/5. Any findings summary should prominently retain the weak-versus-closed distinction, null-homology restriction, and S²×S² exclusion. The derivative's retained author metadata is historical; EXACT_ACCEPTANCE.json and this report give the completed independent decision.

For exact replay, verify each archive against its external manifest and trusted SHA256 pins with verify_release.py; extract only after successful verification, then run check.py normally and under -I -O, with --self-test. Optional corpus replay requires all three authorized local files explicitly. Run independent_algebra_check.py in both modes for the separate identity calculation. No source/corpus file is needed for the finite algebra replay.

Public deliverables comprise authored proof analysis, an actual narrow code patch, acceptance findings, code, and public verification metadata. They exclude third-party source documents/text, dataset records/contents, private source material, personal data, and private coordination. No external publication or queue edit was made by this auditor.
