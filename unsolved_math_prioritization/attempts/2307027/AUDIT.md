# Editorial acceptance and dependency audit

This is an AI-assisted, unrefereed mathematical draft. Acceptance records one independent internal AI mathematical reconstruction of an identified prior theorem, with explicit local proof repairs. It is not human peer review or formal proof-assistant certification. This is a prose proof-and-audit edition, not a computational reproduction package. No novelty, priority, sharp-constant, or worldwide-current-openness claim is made.

## One reconstruction and its exact scope

PROOF.md preserves the full accepted authored mathematical reconstruction from the original audit, identified by SHA-256 16d2329386f6230b128b061b7b78e80f68810e1c65a11cc71b3d0a2e94eb9c1d (18,732 bytes). This document records editorial acceptance and dependency checks of that same argument. It is not a second independent mathematical audit, a fresh proof search, or a new theorem claim.

The accepted result is MacMahon’s arXiv:2609.20607v1 Theorem 1.2, with its exact constant c_0 = exp(-8 exp(9/2)/(3 sqrt(2 pi)))/2. It holds for every nonempty simply connected planar domain and every pair of interior points. Boundedness of the domain, finite inner diameter, boundary smoothness and boundedness of the admissible function are not hypotheses. The whole plane and equal points are handled separately. The original arbitrary-domain qualitative question remains broader.

## 1. Metrics and normalization

Polygonal connectivity makes the inner distance finite for each fixed pair. The curvewise derivative integral gives rho <= d on every planar domain. The admissible identity function gives rho >= |p-q| and separates points. No extremizing function or length-minimizing path is presumed.

For a proper simply connected domain and two distinct points, Riemann mapping and disk automorphisms place their disk preimages at 0 and r in (0,1). The explicit strip map T(w) = tanh(pi w/4), with inverse (2/pi) log((1+z)/(1-z)), places the points at finite real coordinates a < b. The image of [a,b] is a compact interior curve of length L >= d(p,q). No boundary extension or Gehring–Hayman length comparison is used.

## 2. Logarithm and coefficient estimate

Univalence makes psi' nonzero, and simple connectedness of the strip gives its holomorphic logarithm g = A+iB. The complete coefficient-area appendix proves the only distortion coefficient estimate used: |a_2| <= 2 for a normalized univalent disk map. Its odd square-root transform is shown injective, the exterior Laurent-area identity is justified on each circle of radius r > 1, and monotone finite partial sums give the bound as r decreases to 1.

The disk radii 1 and 1/2 give |g'(x)| <= 4 on the real line and |g'| <= 8 on the closed half-strip. Cauchy’s estimate then gives |g''(x)| <= 16. Thus |B'| <= 4, |B''| <= 16 and B has at most linear growth. The uncontrolled constant B(0) cancels in the imaginary-part estimate.

## 3. Four local source repairs

C1: The pointwise Taylor remainder for displacement -s is B(a-s)-B(a)+sB'(a). The printed minus sign is false. The full univalent witness psi(w) = exp((1+i)w) is retained: equality of images would force a nonzero imaginary displacement of at least pi > 2; its logarithmic phase is affine, giving printed remainder 2 but claimed bound zero at a=0,s=1.

C2: Taylor’s remainder needs control along the segment, rather than the single value |B''(a)|. The integral remainder and the global bound 16 give 8s^2.

C3: The normalized variance-sigma^2 Gaussian has second moment sigma^2, so integrating 8s^2 gives 8sigma^2, not 4sigma^2. With sigma=1/3, the phase error is 8/9 < 1 < pi/3. The source’s cone bound and exact c_0 still hold unchanged.

C4: The modulus of the imaginary part of the complex Gaussian is bounded by, not equal to, the full modulus. At imaginary coordinate zero the asserted equality already fails. The corrected inequality |Im k_sigma(s+iv)| <= |k_sigma(s+iv)| <= exp(1/(2sigma^2)) k_sigma(s) is sufficient.

These are repairs of specific printed intermediate steps, not counterexamples to Theorem 1.2. The additional source theorem-number slips and missing domain/analytic justifications are recorded separately in the complete correction ledger.

## 4. Entire convolution and universal strip control

Linear growth of B and a compact-uniform Gaussian majorant justify convergence and differentiation of G(w) = integral B(x) k_sigma(w-x) dx to all orders. This establishes entire holomorphy without leaving a parameter-integral theorem unchecked. Gaussian normalization, oddness and integration by parts establish the first two moments used in the Taylor estimate.

For J(v) = integral k_sigma(s+iv) ds, differentiation and Gaussian decay give J'(v)=0 and J(v)=1. Subtracting B(a) before bounding the imaginary part removes the branch-dependent constant. The Lipschitz bound 4 and first absolute Gaussian moment 2sigma/sqrt(2pi) give

    |Im G(w)| <= lambda = 8 exp(9/2)/(3 sqrt(2pi))

throughout the strip. This bound is independent of Omega, p, q, the Riemann map, the segment length and the logarithm branch.

## 5. Admissibility and lower bound

The strip’s simple connectedness supplies a primitive F of h = psi' exp(-lambda-iG). For f = F composed with psi inverse, the chain rule gives |f'(psi(w))| = exp(-lambda+Im G(w)) <= 1. The plus sign before Im G is checked explicitly.

On the real axis, Re h = exp(-lambda)|psi'| cos(B-G) >= exp(-lambda)|psi'|/2. Integration along the normalized finite segment yields |f(q)-f(p)| >= c_0 L >= c_0 d(p,q), proving the universal lower bound. No claim of sharpness follows from this conservative cone estimate.

## 6. Bounded adjacent consequence and exclusions

For Theorem 1.1’s existence assertion alone, functions normalized at p and normed by sup |f'| form a Banach space isometric under differentiation to H-infinity(Omega). Evaluation at q has norm rho(p,q). Infinite inner diameter gives evaluation functionals with unbounded norms, and uniform boundedness provides one function with unbounded evaluation values. A subsequence is chosen to obtain divergence of their moduli; full-sequence divergence is not asserted. The reverse implication follows from |f(q)-f(p)| <= sup |f'| d(p,q).

This gives the existence equivalence for all simply connected planar domains, including the whole plane. It does not certify higher derivatives, Theorems 1.3–1.4 or later Rubel(k) assertions. The convex-domain equality follows immediately from straight segments, but no characterization of equality or strict inequality for every nonconvex pair is claimed.

## 7. Dependencies and inspection limits

The principal imported facts are Riemann mapping, disk automorphisms, holomorphic logarithms and primitives on simply connected domains, Cauchy estimates, dominated differentiation, elementary Jordan-curve area and Laurent-series formulas. The coefficient estimate and Gaussian calculations are proved in full. Banach–Steinhaus is used only for the explicitly bounded Theorem 1.1 consequence. Gehring–Hayman, Whitney and later source sections are not dependencies of the metric theorem.

The original audit read MacMahon’s Theorem 1.2 proof pages 6–10 in full and visually checked those pages, plus page 2; it read context pages 1–5 and references page 15. It did not inspect the whole PDF or accept the remaining theorems. Hayman–Lingham Problem 7.27 on PDF page 169 / printed page 168 was read and visually checked. A fresh version-specific request failed with a cache miss, so the authenticated retained complete PDF was used. Public abstract/version checks showed v1 and no journal reference at inspection time. LLM-assistance and author-correction disclosures on source pages 4–5 are recorded without treating them as evidence for or against the theorem.

## 8. Exact editorial and integrity boundary

The entire original text from “Verdict and exact scope” through the end of the bounded consequence is retained verbatim. Only the title/opening disclosure and the verification paragraph’s description of undistributed programs are changed. All four calculation repairs, the full proof, appendix, edge cases, dependency limits, public bibliography, exact constant and bounded corollary remain unchanged.

The original closed audit tree has 29 payload files plus its manifest. Its fixed manifest and external seal, together with separately pinned validation history, were reauthenticated. The public edition distributes only authored prose and public verification/source metadata. Original scalar arithmetic and integrity checks are rerun privately; the original 24 adverse rejections per optimization mode are authenticated history, not a newly executed independent mathematical review. Public-edition controls check exact editorial replay, eight-file membership, strict additions-only patch replay, native Git identities and externally sealed closure.

Finite scalar or integrity checks do not prove a statement quantified over all planar domains. The complete analytic argument in PROOF.md supplies that reasoning; no formal proof-assistant certification is claimed.
