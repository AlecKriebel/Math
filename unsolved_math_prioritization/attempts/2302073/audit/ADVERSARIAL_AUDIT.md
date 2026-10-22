# Independent adversarial audit: Rubel Problem 2.73

Date: 4 October 2026 UTC. Target: rank 567, problem 2302073, AMR-022-2073.

## Exact verdict

**PASS — the complete original existence problem has an affirmative answer. Recommended disposition: `already_solved`, `1/5`.**

The frozen packet is a correct, attributed verification of the prior result of Yixin He, Quanyu Tang and Teng Zhang, arXiv:2603.20883v1 (21 March 2026), Theorem 1.2. The independently checked proof constructs a jointly entire function on all of C³, proves normality of every parameter slice on the whole z-plane in the usual spherical sense, and rules out every entire one-parameter factorization. No original subcase or extra condition remains open within this question. This is not a new-resolution or human-peer-review claim.

No blocking mathematical defect was found. No frozen file was edited. No remote writes were made by this auditor. This report was prepared by a separately assigned AI auditor from the frozen packet and the primary sources; it is an independent task-level audit, not a human referee report or a formal proof certificate.

## 1. Integrity and replay

The audit is bound to FROZEN_MANIFEST.json SHA-256:

`f8944c83f3131caa950cf466ff5c7332fc7db2f5ba271e49a9eb66429363858f`

All ten manifest-listed files have their stated byte counts and hashes. The public directory contains exactly those files and the manifest itself. Every hash was checked again after verification. In particular:

- PROOF.md: `857b6605b5316de18aded01a43aa652e21eed43f31df0e6cdbabec2c45c3edad`
- SOURCE_GATE.md: `5aa1886cc13e5a372582655926fee3f90ed28911b0b1cd3a79974d84f6ad21d4`
- verify.py: `6e9c02e1f94018fa3ccb5e2b0f9e0ba568c6487e5d8127a9942b9ea355928d1e`
- verification.json: `ba37d8bf787d1547fadd710e65b32b8417b78364b225ce75dabab430ec0bdfc3`

The author's verifier exits successfully with 35 assertions. Its standard output agrees **byte-for-byte** with verification.json. `sha256sum -c SHA256SUMS` passes all nine listed checks. Environment: Python 3.12.14, SymPy 1.14.0.

The separate audit_verify.py reports 68 assertions: 27 integrity/replay/immutability controls and 41 mathematical controls. These include genuinely independent symbolic expansions and boundary checks described below. All 11 author-file hashes are recorded in audit_results.json. Neither the author's 35 controls nor the audit's finite controls are represented as a machine verification of the global analytic reasoning.

Reproduction with this audit directory next to the frozen public directory:

```text
python3 audit/audit_verify.py
cd audit && sha256sum -c SHA256SUMS
```

The first output should agree with audit_results.json, apart from environment-version fields if a different compatible interpreter is used.

## 2. Original scope and primary-source gate

The original item and its complete update were read in [Hayman–Lingham, arXiv:1809.07200v2](https://arxiv.org/abs/1809.07200v2), printed pp. 50–51 (PDF pp. 51–52). Both source-page images were visually inspected. The selected catalogue record agrees with this primary text. The original asks for entire dependence on all three variables and normality as both parameters range over C, excluding a factorization through one entire scalar function of the parameters. Its differential condition is the same obstruction used by the packet.

There is no transcendence requirement on the z-slices, no demand that every slice have positive degree, and no hidden extra question in Update 2.73. Consequently affine z-slices, including any constant slices that arise, are admissible. The old no-progress update records the editors' historical knowledge; it does not outweigh a later verified solution.

The live [He–Tang–Zhang arXiv record](https://arxiv.org/abs/2603.20883v1) confirms all three authors, the submission date, ten-page length, and Theorem 1.2's exact conclusion. The complete ten-page manuscript was read, including Proposition 2.3, Lemma 3.1, and the entire final proof. Its mathematical construction and the packet coincide. The live record displayed only v1, without a journal reference; bounded title/identifier searches did not locate a correction or withdrawal. No journal publication, exhaustive literature search, or human peer review is inferred.

[Rosay–Rudin, *Holomorphic maps from C^n to C^n*](https://doi.org/10.1090/S0002-9947-1988-0929658-4), printed p. 49, complete Theorem 9.1 and proof on pp. 73–74, and the complete Appendix on pp. 80–86 were checked in the [primary-paper reading copy](https://www.math.stonybrook.edu/~ebedford/PapersForM655/RosayRudin.pdf). The theorem and constant-Jacobian conclusion support the construction. The special spectral hypothesis is satisfied here: every eigenvalue has modulus 1/√2, and 1/2 < 1/√2. The source explicitly warns against unjustified normalized-iterate convergence for arbitrary attracting automorphisms. The frozen packet avoids that error by proving its own summable estimate.

The actual source PDFs match the source manifest:

- Hayman–Lingham: 1,706,228 bytes; SHA-256 `8e28fd4403a07e4e19a9816b7efaafddf9f475d59cf8c34a8255cb03833ed4f0`
- He–Tang–Zhang: 473,957 bytes; SHA-256 `84d36a62151989dde4b1d710b447e5c9e7b5dbf72694e88736c47a0b9301dbd6`
- Rosay–Rudin: 2,620,375 bytes; SHA-256 `4d3d147b31bab0cf274554dc3f25f1cd756455a0274c9d06cdabe8564913ce0a`

Source PDFs, extracted source text, and rendered source pages are not included in this audit deliverable. The selected old research report was also read: it gives no proof attempt, only obsolete open-triage. Historical repository-search receipts in SOURCE_GATE.md were not independently rerun by this mathematical audit; those bounded provenance statements are not proof dependencies.

## 3. Full analytic proof audit

### A. Polynomial dynamics and the basin

The two displayed polynomial maps are genuine two-sided inverses. Their Jacobians and the identity M² = −I/2 are correct. In the weighted norm, the linear part has operator norm exactly 3/4 and its inverse exactly 3/2. These values were independently computed using conjugation by diag(3/4, 1), rather than assumed from the written inequalities.

For r < 1/6, the nonlinear second-coordinate estimate is r²/2 + 2r/3 ≤ 3r/4. Writing r = q/6 gives margin q(1−q)/72 for 0 ≤ q ≤ 1, verifying the full interval and its endpoints. Thus B is forward invariant and every point in it tends to zero. Eventual entrance into B is equivalent to convergence to zero. The exhaustion by increasing inverse images follows because f and g are global inverses. Its union is open and connected. No properness of f on a smaller set or unproved uniform entrance time is used here.

### B. Local normalized-iterate convergence

Writing the nonlinear remainder as R, the telescoping difference is precisely M^(−n−1) R(f^n(p)). Its norm is bounded by (3/4)(27/32)^n r². The inverse norm is used with the correct exponent. Since 27/32 < 1 and r is uniformly bounded in B, the differences are uniformly summable there. The tail constant 24/5 is correct, including the indexing at N = 0.

Uniform convergence on B implies local uniform convergence on every compact subset, hence a holomorphic limit. Derivative convergence follows by applying the Cauchy formula on smaller polydiscs inside B. Each normalized iterate fixes zero, has derivative I at zero, and has determinant identically one; these statements pass to the limit. Thus the limit has a genuine local holomorphic inverse at zero. This is stronger than an unsupported claim that a limit of automorphisms must be globally invertible.

The identity h_n ∘ f = M ∘ h_(n+1) has the right indexing and gives the local conjugacy. It was checked independently on explicitly expanded iterates through n = 3.

### C. Continuation and global biholomorphism

For any p in the basin, the continuation formula is available after some finite iterate enters B. The local conjugacy makes it independent of every subsequent choice of iterate. These formulas agree on nested open sets and therefore define one holomorphic map on the whole basin. The determinant remains one because det Df^n and det M^n cancel exactly.

The injectivity argument is complete: two points with equal images can both be iterated into one small neighborhood of zero on which the local limit is injective, and the conjugacy preserves equality of their images. Injectivity of the polynomial iterate then gives equality of the original points.

The surjectivity argument is also complete. A sufficiently small weighted ball lies in the local inverse-function neighborhood and is forward invariant. Its image contains a neighborhood of zero. Every w in C² can be linearly contracted into that image by some M^n, then pulled back using the local inverse and g^n. The resulting point lies in the basin and maps to w. Local inverse branches glue because the global map is injective. Therefore Ψ is an entire biholomorphism C² onto the basin with determinant one. All parameter values, not only a small neighborhood of zero, are covered.

### D. Containment and the parabolic tube

Both trapping inclusions were checked case by case, including the thresholds |x| = 5 and |x| = 10. At the first threshold strictness comes from |y| < 5; there is no boundary hole. With t = 5 + k the relevant margin is k² + 9k. With t = 10 + k the outer margin over 10 is k² + 17k + 80, so it remains strictly positive. B lies in the initial box. Induction therefore traps every inverse image and their union. The omitted point (0,10) proves the basin is proper.

The coordinate swap/scale and the shear are global automorphisms. Their tube inequalities are valid in both parts of the containing set, with strictness retained. Their combined determinant is −1/625. Composing with Ψ yields a globally defined coefficient map with exactly that constant determinant. There is no unjustified inference from nonzero Jacobian to global injectivity: global invertibility has already been proved for each factor.

### E. Normality on the whole plane

For any sequence of coefficient pairs in the tube, bounded slopes give bounded intercepts and hence a coefficient-convergent subsequence. Unbounded slopes admit a subsequence whose moduli tend to infinity. The lower bound t² − (R+1)t − 1 applies uniformly on every disk |z| ≤ R. The same subsequence works for all disks, so no unaddressed diagonal-subsequence issue remains. Its limit is the constant infinity in the spherical metric.

As an additional check, for t ≥ 2(R+2) the lower bound is at least t²/2. The spherical derivative is then at most 4/t³; for smaller t it is at most 2(R+2). This independently gives a locally uniform spherical-derivative bound, consistent with Marty's criterion. The sequential proof in the frozen packet already suffices and does not depend on this cross-check.

The infinity alternative is essential. Requiring only finite limits would be a different problem: even z+c fails that convention. Normality of all affine functions would also be false, as shown by nz near zero. The tube is the mechanism preventing that failure.

### F. Joint entire dependence and nonfactorization

The entire coefficient functions make F jointly entire, with no separate-to-joint analyticity gap. The differential expression cancels all z-dependent terms and equals minus the coefficient-map Jacobian, hence **+1/625**. The sign was independently checked using the combined coordinate map.

For every hypothesized entire G and H, direct chain-rule differentiation forces the same expression to vanish, including at critical points of H or of G. No division by derivatives, generic-rank argument, or converse factorization theorem is used. The positive constant contradicts every such factorization everywhere. This completes the exact original problem.

## 4. Additional independent checks and adversarial probes

The separate verifier does more than replay the author's formulas. It explicitly constructs early normalized iterates, checks their exact polynomial Jacobians and derivative normalizations, and solves the degree-two and degree-three conjugacy equations independently. The unique cubic jet is

```text
h_1(x,y) = x − (2/3)y² − (2/9)x²y + terms of degree at least 4
h_2(x,y) = y − x²/6 + (4/9)xy² + terms of degree at least 4.
```

Its Jacobian is one through degree two, as required. This is a finite consistency check, not the existence proof.

Negative controls detect the wrong linear sign, show that a crude Euclidean norm estimate is not summable, exhibit failure of the 3/4 bound if the ball is enlarged to radius 1/5, and flag both unrestricted affine-family normality and finite-only limiting conventions. These probes reinforce why the actual hypotheses and norm choices matter.

One minor editorial issue is the reuse of h₀: first it is the n = 0 normalized iterate, then it names the local limit. The context explicitly redefines the symbol and the subsequent reasoning is unambiguous. Reading the latter as h_local removes the collision. This is nonblocking and does not require alteration of the frozen packet.

## 5. Scope, disposition, and limitations

The claimed result is completely established at the level of ordinary mathematical proof, independently of trusting the prior paper's abstract or catalogue status. Attribution is correct. The special basin normalization is classical and is not presented as a novel result. The source-status and peer-review caveats are appropriate.

The authored attempt log records one substantive investigation/reconstruction turn, consistent with the known-resolution stopping condition. The auditor adds no new author attempt turns. Recommend the exact status `already_solved`, turns `1/5`; no five-turn exhaustion or original discovery claim is justified or needed.

This audit does not grant merge, release, publication-deposit, or outreach authority. Its conclusion is limited to the frozen mathematical packet and the stated queue disposition. The audit files are separately hash-bound in AUDIT_MANIFEST.json, preserving the author's freeze intact.
