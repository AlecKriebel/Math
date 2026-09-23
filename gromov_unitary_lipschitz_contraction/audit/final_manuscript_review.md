# Final adversarial manuscript and verifier review

Reviewed: 2026-09-23 UTC. Scope completion estimate: 100% of this final mathematical/manuscript review. This percentage does not certify exhaustive publication priority.

## Final verdict

**PASS after one corrected metric qualification. No remaining mathematical must-fix was found.**

The reviewed `paper/main.tex` proves the candidate's theorem for the explicitly defined unnormalized Hilbert–Schmidt and operator-norm length metrics. Its strict and closed sublevel statements, coefficient `(1-t^2)/(1+t^2)`, uniform continuity claim, fixed constant maps, finite-dimensional target, and parameter-family assertions match the verified construction. The paper distinguishes the stronger quantitative theorem from the weaker topological assertion and does not claim exhaustive priority clearance or external peer review.

Files inspected: the manuscript source, both verifier scripts, their README and recorded JSON results, the earlier algebra review, the priority review, and the source record. The original Gromov source was checked in the initial independent audit. For this final review, Neretin's cited Cayley-transform section was independently opened in the [author-hosted book](https://www.mat.univie.ac.at/~neretin/lectures/ems.pdf); its §1.7.9, Theorem 7.5, is on printed p. 42, as cited. No person was contacted. This is an AI-assisted internal adversarial review.

## Corrected qualification

The initial manuscript said that both norms have the source's shortest-closed-geodesic normalization. That sentence was too broad if geodesic for the nonsmooth operator-norm metric means a locally minimizing metric curve. The local metric on the diagonal two-dimensional torus is the maximum norm on the two angles. Its diamond path with angular vertices

    (a,0), (0,a), (-a,0), (0,-a), (a,0)

is a closed locally minimizing curve of length `4a` for arbitrarily small `a>0`: across each vertex, one angular coordinate stays monotone with speed one and witnesses the full local length. Thus arbitrary closed metric geodesics are not the right normalization claim for this nonsmooth norm.

The author corrected the manuscript to state that the Hilbert–Schmidt metric has the source's normalization and that **closed one-parameter subgroups** have minimum nonconstant length `2 pi` for either norm. This corrected sentence was reread and verified. It is true because a periodic diagonalized generator has integer winding numbers, so every nonzero such generator has operator norm, and hence Hilbert–Schmidt norm, at least one after a period of `2 pi`; a rank-one winding attains equality. This qualification does not affect any theorem, proof step, or verifier.

The two-point sphere paragraph was also clarified to say that each new absolute eigenangle is **at most** `q_t` times its original value. The earlier phrase about shrinking was ambiguous; the revised statement is precise and correct.

## Additional claims checked

- The nonsmooth length passage is now explicit: domain-geodesic restrictions are absolutely continuous; the ordinary chain rule and the matrix-norm speed integral supply the intrinsic length estimate. It never assumes a shortest target geodesic remains in the semicircle.
- The `S^0` addendum assigns the stated finite angular metric and uses the principal-angle distance formula. It does not misuse a path metric on a disconnected domain.
- For an arbitrary topological parameter space, a jointly continuous family remains jointly continuous after substitution into the finite matrix formula. No regularity or compactness of the parameter space is required for that assertion.
- Constant left/right frame changes satisfy `H_t(Q Phi R)=Q H_t(Phi) R`. The normalized matrix changes by conjugation with `R`, which verifies the formula directly.
- The Cayley identity is correct, with `C(W)=(I-W)(I+W)^(-1)`: `C(F_t(W))=((1-t)/(1+t))C(W)`. The manuscript attributes the classical chart and presents the displayed identity as its elementary application.
- The weaker principal-logarithm construction for `Lip < 1` is valid under the same two metrics: the diameter estimate confines eigenangles strictly between `-pi` and `pi`, so the principal logarithm is defined continuously. The manuscript does not assert that this alternative preserves the same Lipschitz sublevel.
- The source bounds and pagination match Gromov's text. The note explicitly avoids claims about nontrivial sphere fibrations or every bi-invariant metric having one normalization.
- The priority wording agrees with the bounded audit: no earlier explicit statement was located in the recorded search; first priority is not certified. Attribution to classical transforms is retained. Neither a current catalogue listing nor a DOI is treated as proof of novelty.

## Independent executable checks

The exact script was rerun under the available default Python and passed **10/10 checks**. The numerical script transparently refused to run under that interpreter because NumPy was absent. It was then rerun under the installed bundled Python with NumPy and passed **7,679 checks with zero failures**. Separate outputs are preserved at:

- `audit/recheck_exact.json`
- `audit/recheck_numeric.json`

The scripts and README are mutually consistent. The exact checker preserves ordered noncommuting words and uses rational coefficients; its sanity check detects `UV != VU`. The numerical checker evaluates the original rational formula with a right-sided linear solve and differentiates that formula independently by the product rule. Its cases include the noncommuting closed-boundary pair, both endpoint times, and scalar counterchecks outside the permitted region. The recorded counts, dimensions, times, seed, and tolerances match the implementation.

The README and paper appropriately limit these computations: they do not prove all-dimensional assertions, matrix positivity, curve-length facts, or continuity of the mapping-space deformation. The numerical tests use ordinary floating point and are not interval certificates. Thus their successful execution is supplementary reproducibility evidence, not an inflated claim of formal verification.

## Minor presentation note

At the inspected snapshot, the scalar formula in the two-point-sphere paragraph used `exp` without the LaTeX operator backslash. Rendering it as `\exp` is a harmless typography improvement and does not change the mathematical verdict. PDF layout inspection and release-package/link checks are outside this review.

The manuscript snapshot after the substantive corrections had SHA-256 `b596d2bfe21b5f80dd9a46dd6d9021ce53fc1401dc8afcd662174e5ef71a13f3`. Subsequent typography-only changes may alter that hash without changing the audited mathematics.
