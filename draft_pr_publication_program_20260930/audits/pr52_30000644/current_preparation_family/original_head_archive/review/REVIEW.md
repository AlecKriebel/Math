# Independent adversarial review: special-automorphism reduction

**Problem:** 30000644 / OWR-1452-008.  
**Reviewed artifact:** `KNOWN_THEOREM.md`, SHA-256 `ebe9dceba18b33b858265d3f74e9898dc4e7f5ab533d7204d1f1c2c23621bae3`.  
**Reviewer:** separate gpt-6-astra agent, xhigh; September 30, 2026.  
**Verdict:** PASS for the credited exact known theorem and source-status correction. No mandatory mathematical correction. Recommended `already_solved`; no discovery credit to this campaign.

## 1. Exact source matching

I first requested the problem page, which was unavailable to the web reader, and read the preserved complete source record. I then read Vénéreau's full contribution on printed pp. 24–27 of the [original Oberwolfach report](https://ems.press/content/serial-article-files/46087?nt=1), and visually inspected p. 26. The reduction-map question there is immediately followed by an affirmative answer credited to van den Essen and Maubach. The source defines “special” by Jacobian determinant exactly one. This is not an inference from the title or from unrelated usage of SAut.

The motivating example on p. 25 assumes reducedness for its units argument. The stronger general coefficient-ring scope of the selected target is independently explicit in Vénéreau's entry on printed p. 317 of the [Acta Mathematica Vietnamica collection](https://math.ac.vn/public/uploads/files/0702303.pdf), which I read and visually inspected: every ring containing Q and all m,n at least 1 are covered. That source separately discusses the remaining non-Q-algebra questions.

The [Basel institutional abstract](https://edoc.unibas.ch/entities/publication/65022835-950e-4439-9383-7a104c3aa40e) also states the exact Q-algebra surjectivity theorem for the published paper by van den Essen, Maubach and Vénéreau, JPAA 210 (2007), 141–146, [DOI 10.1016/j.jpaa.2006.09.013](https://doi.org/10.1016/j.jpaa.2006.09.013). I did not recover the complete JPAA article. Accordingly, this review certifies the displayed reconstruction and its exact source coverage, not a line-by-line reading of that unavailable article. The package states this limitation accurately.

## 2. Audit of the reconstructed proof

### Arbitrary Q-algebras and the divergence-free decomposition

There is no hidden reducedness, domain, Noetherian or finite-generation assumption. In a Q-algebra, every positive integer is a unit. Therefore polynomial integration is well defined coefficientwise, and a polynomial with zero partial derivative is independent of that variable, even when coefficients have nilpotents or zero divisors.

For n at least 2, subtracting the vector with components `(∂n H_i, -∂i H_i)` in positions i and n eliminates the i-th component and preserves divergence. Later steps do not change earlier zero components. The remainder is independent of the last variable and is itself a shear. This establishes the reduction to finitely many two-coordinate Hamiltonian vectors, without requiring an unjustified infinite decomposition.

The binary forms `(yi + q yn)^d` for q = 0,...,d span the homogeneous degree-d forms. With rows indexed by the yn exponent, the determinant is the product of the binomial coefficients times the ordinary Vandermonde determinant. It is a nonzero rational number, hence remains invertible in every Q-algebra. Coefficients depending on the other variables are unchanged by these two-coordinate translations. Constants in the binary variables have zero Hamiltonian vector and cause no missing term.

### Genuine polynomial lifts, not a Jacobian-conjecture step

For every resulting shear datum, the direction v has constant rational entries and its coefficient h is invariant under translation along v. Thus `Y ↦ Y + a h(Y)v` has the explicit inverse `Y ↦ Y - a h(Y)v` over R[t]. Its Jacobian is the rank-one perturbation `I + a v(∇h)^T`, whose determinant is `1 + a(∇h)^T v = 1`. The rank-one determinant identity is a universal polynomial identity over commutative rings; it does not divide by any coefficient of h or v.

This verifies both invertibility and exact determinant one before reduction. A composition of these maps has the same properties. No claim that an arbitrary determinant-one endomorphism is invertible is used.

### Finite jet correction and induction

The representation of the next coefficient modulo t^(r+1) is unique because R[t]/(t^(r+1)) is a free R-module with its usual monomial basis. Extracting the t^r coefficient from the determinant is therefore legitimate in the presence of nilpotents. Since 2r is at least r+1, all cross terms disappear at the required order; determinant one forces zero divergence of that coefficient over R.

The products of shear lifts add their vector coefficients to first order in t^r. Their inverse composition removes that coefficient, improving the residual from identity modulo t^r to identity modulo t^(r+1). All intermediate residuals are actual special automorphisms. Exactly m−1 corrections suffice. The proof does not require convergence, completion, compactness, or a single lift valid for infinitely many jets.

The initial reduction modulo t is an actual R-automorphism because the original inverse reduces with it. Its constant extension is therefore a valid lift, even if it is nonlinear or wild. This correctly avoids a claim that every special automorphism over R is generated by the displayed shears.

### Boundary and excluded cases

For n=1, derivative one over a Q-algebra forces translation, so the argument and lifting conclusion hold. For m=1, the constant extension alone suffices. The characteristic-p example is genuinely outside the hypotheses: modulo t², `y + t y^p` has inverse `y - t y^p` and derivative one, while a one-variable automorphism over the domain k[t] must have degree one in y; determinant one then makes it a translation. This is a valid warning against dropping the Q-algebra condition, not a counterexample to the target.

## 3. Reproduction and independent diagnostics

The submitted verifier was copied and run outside the author's directory, alongside an unchanged copy of the frozen artifact. All 211 submitted assertions pass; the resulting JSON is byte-for-byte identical to the author's recorded result.

`independent_checks.py` checks exact Vandermonde determinants, three-variable divergence-free decomposition, universal shear invariance, explicit two-sided algebra needed for inverse composition, exact Jacobians, nonlinear finite-jet elimination over Q, a dual-number coefficient ring, an idempotent coefficient ring with zero divisors, a nonlinear constant reduction, and the one-variable, m=1 and positive-characteristic controls. Run it with Python 3 and SymPy from this review directory. All 142 independent assertions pass. The nonlinear Q-algebra, dual-number and idempotent-ring reconstructions use 72, 4 and 56 explicit shear factors respectively. Details are in `independent_results.json`. To replay the unchanged submitted script, place a copy of the reviewed `KNOWN_THEOREM.md` beside `submitted_verify.py` in a temporary directory and run that script there; its output file is named `verification.json`.

The initial independent test fixture accidentally designated an already divergence-free vector as a negative diagnostic. That fixture alone was corrected before the final run; no issue in the submitted mathematics was involved. No author file was modified.

These finite controls are evidence against transcription errors, not exhaustive checks of all Q-algebras. The general polynomial reasoning in Section 2 is the mathematical justification of that scope.

## 4. Disposition and publication limits

The known affirmative theorem covers the exact source target for all stated parameters. No unresolved mathematical gap was found in the reconstruction. An `already_solved` source-correction disposition is justified. Preserve the attribution, the explicit lack of access to the full JPAA article, and the distinction between the solved Q-algebra target and separate questions over other rings. This is an AI adversarial review, not external refereeing or a new priority claim.

## Final snapshot coverage

At 06:40 UTC the status header alone changed from review pending to review passed, linking this report. An exact diff confirms no mathematical or source changes. This PASS therefore also covers final artifact SHA-256 `84adb170c5ff1d9a1f875daabdf1bf8b3397b8532acf95434f8c811513ff0a7a`. The original reviewed hash above is retained for audit history. Administrative attempt accounting as known-result validation rather than fresh proof search does not alter this mathematical verdict.
