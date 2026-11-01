# Independent adversarial review: planar Maslov benchmark

Review date: 2026-10-21 UTC. This review covers only the exact versions identified below.

## Verdict

The fixed benchmark's mathematical conclusion passes: for the stated outward weak conormal trace and symplectic convention, the Maslov index is −1, with a unique simple crossing in [895/448, 3583/1792]. The normal and optimized executions reproduce the stored results exactly. This is a valid elementary planar spectral-path benchmark using established elliptic Cauchy-data theory, not a general validated boundary solver or a solution of the original challenge.

The review discovered and reproduced a checker-hardening defect in the original version: an unvalidated tail_floor input could yield an accepted, reversed root interval. The author repaired it before this final review. The reviewed version pins the proved floor to 5, checks correction/root ordering, and rejects the offending input. Independent reruns below verify that repair. There is no remaining blocker for the fixed benchmark; certificate() is still not a general PDE-certificate verifier.

## Hash-bound inputs

SHA-256:

- REPORT.md: 9ad7e6b09c0b31bfb9ac347219cfee8b236841ecac1ef2ecbbc85bd1a004c4d9
- CHECK.py: 899f4f27366dface71624f4472cfff39bfdae8709b22e83d4698db2becc76846
- CHECK_RESULT.json: 957059e0110d1499090eade39093c04af710a962f73ce2fd71a7d0989f71a8f1
- CHECK_RESULT_OPTIMIZED.json: 957059e0110d1499090eade39093c04af710a962f73ce2fd71a7d0989f71a8f1

The supplied HASHES.sha256 validated all four files. Changes to any of these files require a refreshed review rather than reuse of this verdict.

## Actual execution results

The original review ran the checker in normal and optimized modes, compared both outputs against each other and the two stored results, and validated its four-entry hash manifest. Execution locations are omitted from this public projection.

All completed with exit status 0. All comparisons were byte-identical; all four manifest entries reported OK. Output status was PASS, with tail gap 7/4, coupling 1/16, squared coupling 1/256, correction range [1/1792, 1/448], derivative range [−785/784, −1], root interval [895/448, 3583/1792], crossing box [199/100, 2], and Maslov index −1. All six named mutations were rejected under both modes. The tests remain active under optimization because they use explicit exceptions, not assert statements.

## Mathematical audit

1. Operator and weak traces. The form domain H¹₀ on the bounded square and distributional operator domain {u in H¹₀: −Δu in L²} correctly define the self-adjoint Dirichlet realization. Bounded real multiplication by V preserves this domain, and the resolvent is compact. No smooth-boundary H² identification is needed. For H¹ weak solutions, Lu=tu is in L², so the graph-space weak conormal trace applies. The extension-independence argument for its definition is correct.

2. Cauchy-data theory and source scope. The retained primary text of Cox–Latushkin–Sukhtayev, https://arxiv.org/abs/2206.07677, was inspected at its domain/ellipticity hypotheses, §4.1 Proposition 4.1 and Green identities, and §8.1 equations (8.1)–(8.7). These supply precisely the real boundary Hilbert space, symplectic sign, analytic Lagrangian path, Fredholm-pair property, eigenvalue identification, and negative counting convention used here. The domain is permitted to be bounded Lipschitz; principal-coefficient Lipschitz hypotheses do not demand a smooth boundary. The constant principal part and smooth bounded real potential satisfy the relevant conditions. This checks applicability of the cited theorem, not a new proof of that theorem. No third-party source text is reproduced here.

3. Boundary sign. Green's identity gives <γ_N u,γ_D u'>=||u||² when u is Dirichlet and (L−t*)u'=u. Consequently ω(Tr u,(Tr u)')=−||u||² for the displayed convention. This matches the source's negative eigenvalue count. Unique continuation for the smooth potential prevents a nonzero Dirichlet eigenfunction from having zero full Cauchy trace. Local analytic lifts are legitimate under the invoked Cauchy-data construction, not a Dirichlet-to-Neumann graph across its pole.

4. Exact coupling. The normalized basis is orthonormal. Multiplying e_11 by (1/4)cos x cos y gives e_22/16 exactly, while the e_11 and e_22 potential diagonal elements vanish. Thus the off-diagonal term is genuinely nonzero and ||b||²=1/256. Nonseparable here means not additively separable for the Cartesian Schrödinger operator; the potential is of course a product of two one-variable functions.

5. Infinite tail and domain. On the complement of e_11, the Dirichlet Laplacian's spectral lower bound is 5. Its bounded potential compression has norm at most 1/4. Therefore C(t)≥7/4 uniformly for t in [1,3]. The orthogonal projection preserves the Laplacian operator domain, and the compressed bounded perturbation preserves self-adjointness there. The inverse estimate ||C⁻¹||≤4/7 concerns the entire infinite complement, not a truncated matrix. The Schur elimination with bounded off-diagonal blocks is valid on this domain.

6. Lower correction, derivative, and root. The energy Cauchy–Schwarz inequality gives <e_22,C⁻¹e_22>≥1/(8−t)≥1/7, since e_22 is in the operator domain and its potential diagonal vanishes. Therefore 1/1792≤r≤1/448. The norm-resolvent derivative is (C⁻¹)'=C⁻², yielding S'=−1−<b,C⁻²b>, with the stated bounds. Endpoint signs and continuity establish existence; strict monotonicity establishes uniqueness. Schur kernel identification proves simplicity. The root interval lies strictly inside [199/100,2]; the exterior pieces are zero-free by monotonicity. In particular, the actual crossing is strictly below the one-mode value 2.

7. Independent count and homotopy. The min–max bounds put λ₁ in [7/4,9/4] and λ₂ at least 19/4, independently proving the unique eigenvalue count. The same bounds apply uniformly to the potential homotopy; the referenced analytic theory and transverse endpoints justify the homotopy check. These are independent count routes, not independent discoveries or novel general methods.

8. Conditional nested chart statement. E*AE=S and its differentiated kernel restriction correctly give congruence of crossing forms. The full inverse-derivative term has the correct sign. The report explicitly distinguishes this bounded-chart theorem from the fixed-domain unbounded interior example, requires a verified boundary symplectic identification, and does not claim numerical chart overlap certification. Scalar simple-root tests do not certify a multiple crossing, as acknowledged.

## Adversarial checker finding and claim boundaries

The initial additional test imported the original CHECK.py (SHA-256 357f2bb496f448a4205086ab3161c9d36eb556031da0b321c0a47b6e2c42c1f6) and called certificate(tail_floor=Fraction(100)). That original version returned normally with tail_gap=387/4, r_lower=1/1792, r_upper=1/24768, root_lower=49535/24768, and root_upper=3583/1792. The lower correction exceeds the upper correction and the alleged root lower endpoint exceeds its upper endpoint. That original version had no check preventing either inconsistency. Also, 100 is not a legitimate Laplacian tail lower bound for this fixed problem.

Repair verified: the final version pins tail_floor to 5 and explicitly checks positive ordered correction bounds and ordered internal root endpoints. Its strict crossing-box endpoint inequalities imply that the entire root enclosure is inside the owned box. The reviewer reran both modes after this change and independently imported the repaired module. Inputs tail_floor=100 and tail_floor=6 now raise ValueError("fixed benchmark tail spectral floor"); coupling=−1/16 raises ValueError("nonzero exact coupling"); a reversed box [2,199/100] raises ValueError("left endpoint positive"); and box [1,3] raises ValueError("single owned box inside transverse endpoints"). All five additional probes were rejected. Such guards improve defensive validation but do not turn arithmetic into a PDE proof.

The existing derivative-sign and Maslov-sign mutation tests check equality to an expected supplied convention; they do not mechanically derive either sign. The encoded mode shift verifies simple coefficient arithmetic, not a symbolic Fourier-analysis engine. The tail gap relies on the report's analytic spectrum and norm bounds. Accordingly, “computer-checked rational bounds attached to analytic arguments” is justified, while “independent machine verification of the analytic theorem,” “general certificate verifier,” and unrestricted “fails safely for finite-model derivative/coupling errors” are not. The original report generally states these limits correctly; its broad failure-safety prose should be read only for the actual covered hypotheses/tests, not arbitrary adversarial inputs. The public report projection narrows that prose explicitly; this editorial change is not a fresh independent review.

No substantive blocker remains for the fixed mathematical benchmark. The checker-hardening defect has been repaired and independently rerun; its discovery is retained above for auditability. No claim about full worldwide open status, novelty, or completion of the general physical-planar validation problem follows from this review.
