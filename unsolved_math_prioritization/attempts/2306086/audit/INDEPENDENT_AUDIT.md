# Independent adversarial audit: real-coefficient pre-Schwarzian improvement

Target: UnsolvedMath 2306086 / AMR-022-6086 / Hayman-Lingham 6.86. Rank: 687.

Audit date: 2026-10-05 UTC.

## Disposition

**PASS for the stated qualitative theorem and exact partial results. No blocking mathematical defect found.**

The frozen argument establishes that, for every fixed nonreal point in the disk, the classical centered pre-Schwarzian radius has a strictly smaller bound uniform over all normalized real-coefficient univalent functions. Real points have the original sharp radius. The proof also establishes a uniform gap on compact subsets away from the real diameter, the real-automorphism reduction, the two exact lower bounds, and the failure of the proposed convex-hull relaxation.

This is a complete answer to the qualitative, fixed-point existence interpretation of the source's improvement question. It does not compute an explicit positive improvement or the best radius, and it does not establish novelty or the problem's present literature status. The primary wording does not explicitly require a sharp formula. Therefore neither an unqualified new-solution claim nor an unqualified assertion that the literal qualitative question remains unanswered is warranted.

Recommended status: **Qualitative fixed-point improvement established; explicit/sharp quantitative result not determined; novelty and current literature status unverified.** Retaining a partial-results label is reasonable if its quantitative meaning is stated. No mathematical amendment to the frozen result is required for that scoped disposition.

## Immutable input and replay

The reviewed ZIP has 19,163 bytes and SHA-256:

`6897b0a5f2efc08daddd87ff4ce44c35d61fc29ba44b1dc5a8179df2dc7f35a5`

All ten ZIP members match the reviewed directory byte for byte. The nine payload records in the author's manifest have correct sizes and SHA-256 values. The manifest itself is separately bound by the audit binding. No extra member, traversal path, source document, source transcription, dataset body, or private coordination document occurs in the archive.

Both ordinary and optimized Python replay of the author's exact controls produce the saved result: 3,558 passing checks each, including their negative controls. The independently authored audit program produces 96 passing checks: 48 binding/replay/preservation checks, 32 independent symbolic or exact mathematical checks, and 16 numerical-reproduction checks. Its ordinary and optimized JSON outputs are identical. Those counts do not turn the analytic proof into a formal proof certificate.

The audit code never runs the author's numerical optimizer or imports a module from the freeze. The frozen ZIP and all directory members were checked again after execution and remain unchanged.

## Load-bearing proof review

### 1. Normalization and the disk center

With A_f(z)=(1-|z|^2)f''(z)/f'(z)-2 conjugate(z), the original centered expression is z A_f(z)/(1-|z|^2). Its center is consequently the real number 2|z|^2/(1-|z|^2), and its radius scales by |z|/(1-|z|^2). There is no missing conjugation or angular factor. At zero, the original displayed expression degenerates to zero; A_f(0)=2a_2 is a different auxiliary quantity. The freeze makes that distinction.

A univalent analytic function real on the real interval can be normalized by a real affine postcomposition; this does not change f''/f'. Its derivative at zero is real and nonzero. The chapter's normalized schlicht class is the appropriate analytic interpretation, rather than an unrestricted meromorphic class.

### 2. Area theorem and equality classification

The exterior square-root construction is legitimate: F(z)/z is nonzero on the simply connected disk and has a logarithm normalized at zero. Writing the exterior function as w times that analytic factor gives a single-valued, odd, nonvanishing function on |w|>1. Equality of two values reduces, by injectivity of F, to equal or opposite preimages; oddness and nonvanishing exclude the latter.

The area identity on each circle |w|=R>1 has the correct sign and weights. Its limiting inequality forces all higher negative coefficients to vanish when |a_2|=2, giving F(z)=z/(1-lambda z)^2 with |lambda|=1. No stronger coefficient theorem or uninspected literature classification is needed.

The normalized Koebe transform has second coefficient A_f(a)/2. Thus equality at a point forces the transformed function to be a Koebe rotation. Importantly, this does not directly say that the original f is a Koebe rotation: it first says that f maps onto a complex affine image of a one-ray complement. The frozen proof uses this valid intermediate conclusion.

### 3. Real symmetry eliminates the other equality domains

The omitted ray of a real-symmetric image is invariant under conjugation. Its unique finite endpoint must be real, and its direction must be real. Since zero is in the image, the ray lies entirely on one side of zero. A scaled positive or negative Koebe map onto that slit, compared by inverse composition with f, has a disk automorphism fixing zero. The derivative modulus forces the endpoint distance to equal 1/4; normalization then forces precisely k_+ or k_-.

This argument checks all affine-ray possibilities, rather than merely checking that a Koebe rotation has real second coefficient. For ordinary normalized rotations the latter condition would independently force lambda=+1 or -1, but alone it would not handle the initial inverse Koebe transform.

Direct independent differentiation gives |A_{k_+}(z)|^2=|A_{k_-}(z)|^2=16-48(Im z)^2/|1-z^2|^2. Thus neither equality map can attain modulus 4 at a nonreal point. On the real diameter they attain +4 and -4. At a nonzero real point these two opposite boundary values also rule out a smaller containing disk obtained merely by changing its center.

### 4. Compactness supplies the uniform quantifier

The derived pre-Schwarzian estimate integrates to the stated derivative and growth bounds, so the normalized schlicht family is locally bounded. A local-uniform limit keeps derivative one at zero and cannot be constant. The univalent-limit theorem, or Hurwitz applied to divided differences, preserves injectivity. Real symmetry is closed under the same convergence.

Derivatives converge locally uniformly, and the limiting derivative is nonzero at the evaluation point. Consequently f''/f' is continuous there. A maximum over the compact real class is attained, so strictness for every function becomes a strict maximum below 4. There is no invalid interchange of pointwise strictness and supremum. The joint continuity argument for a compact set of nonreal evaluation points is also valid.

### 5. Real automorphisms and exact lower bounds

The real-parameter Koebe transform preserves the class and has inverse with the opposite parameter. The multiplier in the covariance formula is (1+a conjugate(w))/(1+a w), not its reciprocal. The audit verifies that phase symbolically with an arbitrary pre-Schwarzian value, independently of the two test maps used by the author.

The invariant delta=|Im z|/|1-z^2| is correct, lies below 1/2, and the stated quadratic selects a real automorphism carrying z to the imaginary diameter. Conjugation handles the lower half-disk. Thus the one-parameter reduction is justified without assuming rotations preserve the real class.

The second map h(z)=z/(1-z^2) is injective by its exact difference factorization. Its imaginary-axis value yields 8 delta after using the bijective transformation. Both lower bounds, their crossing at delta=1/sqrt(7), and the comparison at i/2 are correct. They are lower bounds, not upper bounds. They force failure of a single positive gap over all nonreal points through delta tending to zero or to 1/2.

### 6. Convex-hull obstruction

The mean of the two real Koebe maps is typically real and has a simple critical point at i(sqrt(2)-1). The derivative formula and nonvanishing second derivative were checked independently. Its pre-Schwarzian has a pole there.

This also obstructs a bounded relaxed functional at the fixed critical point even if functions with zero derivative at that point are excluded: perturb the equal weights by a small real imbalance. The difference of the two Koebe maps has nonzero derivative there, while the mean has nonzero second derivative. The perturbed ratios become unbounded as the imbalance tends to zero. No convex extreme-point principle for a linear functional applies automatically to the derivative ratio.

### 7. Loewner admissibility versus numerical evidence

The two-atom real-symmetric Herglotz function has positive real part. Its finite-time flow stays in the disk, is holomorphic and injective, preserves conjugation, and has derivative exp(-T) at zero. The tail satisfies z h'(z)/h(z)=1/p(z), so it is a normalized real starlike map. Composition and the factor exp(T) give admissible real normalized univalent functions. The derivative-jet equations and composition formula for the pre-Schwarzian are correct.

The four saved controls were independently reevaluated using RK45, with independently differentiated vector fields and direct Koebe-tail formulas. All four agree within 5.4e-14 of their saved values. This is reproducibility evidence only: it is not an interval enclosure, a certified strict lower-bound theorem, a proof of optimizer convergence, or evidence that two control intervals suffice globally. The original disclaimers are adequate and must remain attached to those values.

## Source scope and provenance

The primary manuscript was retrieved independently from the official arXiv versioned PDF URL, with HTTP 200, 1,706,228 bytes, and the recorded SHA-256. Fresh renders of printed pages 114 and 147 were inspected; the versioned landing page and cover were also checked. The normalization and target/update page references match the frozen metadata.

The primary question concerns possible improvement at a fixed point and contains no explicit sharpness or numerical-effectiveness requirement. The qualitative result is therefore substantively responsive to the wording. Whether a historical research audience intended a useful explicit quantitative region cannot be settled by silently adding that requirement. Conversely, the source's dated progress statement is not evidence of present-day openness or of novelty for this argument.

Primary reference: Walter K. Hayman and Eleanor F. Lingham, Research Problems in Function Theory (New Edition), arXiv:1809.07200v2, revised 2018-09-21. Public manuscript status: draft copy.

- Record: https://arxiv.org/abs/1809.07200v2
- PDF: https://arxiv.org/pdf/1809.07200v2

The audit does not independently establish the frozen repository-search history, retrieve the full dataset corpora, inspect the selected upstream AI report, inspect the subscription 2019 chapter, or conduct an exhaustive subsequent-literature search. The freeze already discloses these limits. Public dataset hashes remain manifest-observed metadata rather than independently rehashed corpus bytes.

## Nonblocking wording clarifications

1. In the equality discussion, the conformal comparison should be called inverse composition, rather than the quotient of two maps. The next normalization argument supplies the intended correct reasoning.
2. Describe the vanishing-gap obstruction as allowing delta to approach zero, or approaching an interior point of the real diameter. Merely having Euclidean imaginary part tend to zero near the boundary points +1 or -1 does not by itself force delta to zero.
3. Keep any partial or unresolved label explicitly tied to the uncomputed quantitative/sharp problem. The literal qualitative existence result has been proved.

These are presentation and scope refinements, not failures of the stated theorem. The immutable authored freeze was not edited.

## Safe artifact boundary

This packet contains an authored audit, authored read-only verification code, generated test results, hashes, byte counts, binding information, public scholarly metadata, and retrieval/inspection history. It excludes scholarly PDFs, extracted source text, source page images, dataset contents, private source material, and private coordination files. The audit performed no remote mutation, commit, push, PR update, external message, or publication.
