# Independent review:6700069

**Verdict: PASS_FULL_CREDITED_SOURCE_APPLICATION_GEOMETRIC_COCYCLE_SCOPE. Recommended already_solved0/5. No mandatory correction.**

Reviewer: research_outer_inversion_ratio, 1October2026. I did not contribute to the author's source application. This is an independent audit of the exact target, theorem hypotheses, analytic application and reproducibility. It does not claim to replace the published theorem with a new proof. Parent retains publication authority.

## 1. Frozen input

This verdict binds FROZEN_MANIFEST.json SHA256 **691e0bccdf08004edd01189658312a891c6a3cd4add4f708ef46e2a795fda4cb**, containing nine author entries, and STATUS_CORRECTION.md SHA256 **9e045ad8cbf0107905986bc2e0b8eac8a0123b3767bf9eae3c3cae83f0a60b16**. Every entry and all three complete source PDFs hash-match. The author's remote backup is reported at b5ece2be00d4b5cfb4274ef2adc27c516c8e5010 on math/6700069-gromov-ball-source-wip; the audit binds the exact local bytes, not merely the branch label.

## 2. Full source correspondence

The original passage and surrounding metric-cocycle discussion were read and visually inspected. The target permits unrelated maps at different radii. The final published BGM Theorem2.3 is uniform over each map of a unit ball, and so answers that quantifier directly. Its hypotheses are closedness, connectedness, orientation and failure of the specified real-cohomology algebra embedding. The containing paper's separate formal/scalable-manifold and global-map results are not substituted.

The published bound has the form C L⁴(log L)^(−α), with α>0 for this target. The exponent is not L raised to a logarithmically changing power; rendered mathematical notation was checked rather than trusting search extraction. No explicit numerical value of α is needed. The relevant proof section and its annular extension were read; they introduce no boundary-constancy or formality condition.

## 3. Topological obstruction and metric scope

Mayer–Vietoris for connected sum gives Betti numbers(1,0,40,0,1). In middle degree the intersection form is the orthogonal sum of twenty hyperbolic planes. Therefore a graded embedding would inject a40-dimensional space into Λ²R⁴, of dimension6. Even if grading were ignored, a real-algebra injection would be an injection of real vector spaces of dimensions42 and16. Both are impossible.

These invariants are preserved by the assumed homeomorphism. No assertion about the existence or equivalence of exotic smoothings is necessary. For each allowed Riemannian metric on S, the theorem supplies its constants. Those constants may depend on that fixed metric; the source does not ask them to be uniform over changing metrics. No scalar-curvature inequality is used.

## 4. Scaling and signs

For f_R on B⁴(R), the rescaled map F_R(u)=f_R(Ru) is R-Lipschitz. Pullback and change of variables identify the two signed integrals exactly. The dilation's R⁴ is already incorporated in the pulled-back differential form; placing another R⁴ outside would be an error. The author does not do so.

The stated theorem initially gives an upper bound for a signed integral. Precomposition with a Euclidean reflection of the ball preserves its Lipschitz constant and negates that integral. Applying the same bound to both maps yields the absolute value of the signed integral. This does not bound the integral of the absolute Jacobian or unsigned multiplicity; the packet explicitly avoids that inference.

The constants are independent of the chosen f_R. Thus after division by R⁴ the logarithmic factor tends to zero uniformly, even along arbitrary unbounded sequences of radii and unrelated choices of maps. A theorem only about restrictions of one global map would not have sufficed; that issue has been resolved by the actual ball theorem.

## 5. Arbitrary fixed fundamental forms and the boundary

Fix orientation and normalize the smooth top form h to integral1. Since H⁴(S;R) has dimension1, h minus normalized Riemannian volume is dη for a smooth three-form η. Compactness makes its comass finite. This is a fixed primitive for a fixed representative, not an R-dependent choice.

For a Lipschitz map, a particularly direct rigorous justification of Stokes is to push forward the integration current of the closed ball. Lipschitz pushforward commutes with boundary. Pairing with η gives the stated boundary identity, and the boundary current has mass at most Lip(f_R)³ times the area of S³(R). Thus the absolute error is at most 2π²||η||R³. This proof does not assume a smooth map, vanishing boundary data, positive Jacobian, or that the boundary map is an embedding.

If the domain is the open ball, the map extends continuously and with the same Lipschitz constant to its closure because the compact Riemannian target is complete. The same current argument then applies. Equivalent approximation arguments are possible, but no unjustified derivative trace at a boundary point is required.

Combining the two bounds gives, uniformly in f_R,

 |∫f_R^*h|/R⁴ ≤ C_h(log R)^(−α)+C'_h/R →0.

Every fixed smooth fundamental representative is covered, including sign-changing representatives. Reversing orientation or taking another fixed nonzero normalization changes constants, not the conclusion. Choosing forms or metrics depending on R with unbounded norms would change the problem and is not asserted.

## 6. Cocycle interpretation

The smooth-form result is unconditional under the stated geometric hypotheses. The broader cocycle statement is accepted with the author's explicit controlled geometric convention. In a cochain model whose difference from h has boundary evaluation O(R³), the same calculation transfers immediately. The original preceding paragraph discusses quantitative Lipschitz control of precisely such evaluations, and expressly includes forms.

This verdict does not certify a statement about arbitrary unbounded algebraic singular cochains evaluated on noncycles. Such a reading would not supply a controlled metric invariant from a cohomology class. Nor should “bounded geometric coboundary” be rephrased as a claim that the fundamental class has a globally bounded singular representative. Retain the actual convention in the final summary; the frozen packet already does.

## 7. Exact controls and final classification

The inspected author checker uses only the standard library. Replayed in a separate review directory, its287-assertion receipt is byte-identical. AUTHOR_REPLAY.json records the checksum. The independent checker imports no author code and passes **4,759 exact assertions** covering connected-sum and exterior-algebra dimensions, the exterior middle pairing, signed permutation/reflection determinants, three-dimensional comass powers, four-dimensional dilation and elementary oriented Stokes controls.

These finite checks validate bookkeeping and model identities. The published analytic estimate, the de Rham comparison and the Lipschitz-current argument are verified by the written source/application audit, not by finite enumeration.

The author has performed a later-literature status correction and standard application, with no fresh substantive research turn. The recommended classification is **already_solved0/5**, credited to the2024 published BGM theorem, and the answer is negative in the original geometric sense. No mandatory mathematical or source correction remains. The seven portable review files are the six entries in REVIEW_MANIFEST.json plus that manifest; reading/ is excluded.
