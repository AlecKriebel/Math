# Independent audit of Problem 2306040 checkpoint

Date: 2026-10-04 UTC.

## Verdict

**Accept as an unsolved five-approach research checkpoint. Do not classify as a solution or counterexample.** I found no material mathematical defect in the stated partial results, no quantifier substitution, and no unsupported extension of the finite checks to the full problem. The claim left unresolved is precisely

`sum_{j=0}^{n-1} |a_{2j+1}| >= |a_n|^2` for every normalized holomorphic injective `f` on the unit disk and every integer `n >= 1`.

There are no mandatory mathematical corrections. Two low-severity presentation/reproducibility improvements are listed below. This audit does not certify that the problem is open in all current literature, nor provide expert peer review or novelty certification.

## Frozen artifact identity

The submitted directory was not edited. Reproduction was performed in a separate copy because the supplied scripts write their output files.

- MANIFEST.json SHA-256: `d1b1cb62e9c46000c4473a28278cc7751de562a2c77418b97737fd9e3a29b9ab`
- PARTIAL.md SHA-256: `aa64b22c3be399baf27eecd75b5de5da21f5b90ea9b6a1d7c8afc628c27c33f5`
- All 14 listed files match both manifest byte counts and SHA-256 values.
- All JSON and JSONL files parse successfully.
- No remote writes were made. No source PDF, source scan, or raw imported corpus is included in this audit deliverable.

The initial check is in `frozen-hash-check.json`; the final repeat is in `frozen-hash-check-final.json`.

## Proof and exact subclass audit

### 1 Positive measure argument

The Chebyshev identity `U_(n-1)^2 = sum_{j=0}^{n-1} U_(2j)` is correct for all n, including n=1 and t=+/-1. The sine-sum derivation is valid on (-1,1), and polynomial identity extends it to the endpoints. Coefficient extraction under the probability integral is legitimate: for each r<1 the kernel expansion converges uniformly over |z|<=r and t in [-1,1], for example using |U_m(t)|<=m+1.

All coefficients of the represented function are real. Consequently the variance identity is exact, rather than an inequality obtained by losing complex phases. Both the variance and each correction |a_k|-a_k are nonnegative. The signed stronger inequality for this subclass is also established by the proof.

The represented class is the normalized typically-real class; it is not asserted to equal S. The implication from real-coefficient univalence to typical reality is sound: f(conjugate z)=conjugate f(z), so injectivity prevents a nonreal z from mapping to the real axis. Continuity on the connected upper half disk and f'(0)=1 fix the sign. Rotation preserves S and all coefficient moduli.

The symmetrization obstruction is correct. The displayed mean of the two Koebe rotations and its derivative agree algebraically; the derivative vanishes at sqrt(2)-1 inside the disk. Thus averaging does not supply a route to arbitrary complex coefficients.

**Accepted scope:** all n for the normalized positive-measure/typically-real class, including all real-coefficient members of S and their normalized rotations. No all-S representation follows.

### 2 Area theorem argument

The reciprocal exterior map is holomorphic and injective on |zeta|>1 because f has no nonzero zero. Its leading Laurent terms are correct. The first area-theorem coefficient gives |a_2^2-a_3|<=1, and the triangle inequality proves n=2. The n=1 case is equality.

The supplied area-formula proof is valid: for R>1 the image circle is a positively oriented analytic Jordan curve, Fourier orthogonality gives its enclosed area, and monotone convergence as R decreases to 1 yields the area theorem. The displayed third reciprocal coefficient is also correct.

**Accepted scope:** n<=2 for every f in S. The higher coefficients do not furnish an unproved elimination step.

### 3 Square root and formal obstruction

The normalized analytic odd square root exists. The nonvanishing of f(z^2)/z^2 permits an analytic logarithm, and oddness plus f's injectivity proves the square root is injective. The coefficient convolution and the Cauchy-Schwarz implication from Robertson to Bieberbach are correct.

For B(w)=1+w^2-w^4/2, every Robertson numerical partial sum is bounded as asserted. The finite initial sums and constant tail 9/4 prove this for every positive integer m, not merely m<=20. Squaring gives exactly f(z)=z+2z^3-z^7+z^9/4. Its target deficit at n=3 is -1, and all its numerical Bieberbach bounds hold.

This f is not univalent: its derivative on z=iy is the real polynomial stated in the submission, whose value at t=y^2=1/4 is -391/1024, whereas its value at t=0 is 1. The intervening derivative zero lies strictly inside the disk.

**Accepted scope:** Robertson partial sums and Bieberbach coefficient bounds alone, viewed as numerical constraints on coefficient sequences, do not imply the target. This is not a counterexample in S and does not exclude stronger consequences of de Branges's theorem.

### 4 Asymptotic argument

The epsilon estimate for the odd-coefficient sum is valid, because the sum of the first n positive odd integers is n^2. With |a_k|/k -> alpha, the normalized deficit tends to alpha-alpha^2. For 0<alpha<1 this establishes eventual strict positivity for each fixed function. Koebe rotations give exact equality for every n. The quoted Hayman regularity theorem and its equality characterization match the cited Bshouty-Hengartner paper.

For bounded f, Parseval and monotone convergence give square summability, hence a_n -> 0. Since the odd-modulus sum includes a_1=1, eventual |a_n|<=1 proves eventual validity. The same argument applies whenever a_n -> 0 is independently known.

**Accepted scope:** eventual validity for positive Hayman index and for bounded functions (or coefficients tending to zero). The argument does not cover the general zero-index class, every initial n, or a uniform threshold over S. The separate unpublished attribution in the source is not promoted to a proved general result here.

### 5 Slit-map constructions

For |u|=1, k_u maps the disk to the plane with the ray starting at -1/(4u) removed. Multiplication by 0<q<1 extends the omitted ray toward the origin, so q k_u(D) is contained in k_u(D), with the inclusion direction as written. Thus the inverse branch defines a holomorphic injective self-map, of derivative q at zero. Composition, application of k_1, and division by the product of q values preserve injectivity and restore derivative 1.

The Lagrange-inversion coefficients are correct, as are both exact controls u=1 and u=-1. Finite Taylor truncation through degree N is exact for the needed coefficients because every composed series has zero constant coefficient. The analytic construction, not the coefficient computation, supplies univalence.

**Accepted scope:** all constructed parameter choices are actual members of S. The exact checks prove only the listed 120 inequalities. Neither a finite grid nor differential evolution certifies a continuous box, all switch counts, or all S.

## Computational audit

The supplied exact verifier was inspected and run in a copy. It completed successfully, and regenerated CHECKS.json byte-for-byte. Its 20 Chebyshev polynomial tests are correct finite controls, subordinate to the separate all-n analytic proof.

The Gaussian-rational modulus enclosure is valid: applying integer square root to floor(x D^2), where x is a nonnegative rational squared modulus and D=10^40, obtains floor(D sqrt(x)); checking the endpoints makes the rational enclosure explicit. Squared target coefficients are evaluated exactly, without enclosing a squared floating modulus.

A second implementation, `independent_checks.py`, derives slit coefficients from the implicit equation

`s(z)(1-u z)^2 = q z(1-u s(z))^2`

and derives final coefficients directly from

`F(z)(1-s(z))^2 = s(z)/q`.

This avoids the submission's Catalan inverse and Horner composition for the one-switch grid. Results:

- All 240 degree-0-through-9 coefficients match the packet's values across the 24 maps.
- All 120 inequalities certify using rational modulus bounds of denominator 10^50.
- The tighter resulting intervals lie inside the corresponding archived intervals.
- There are 38 zero lower bounds and 82 strictly positive lower bounds on this grid.

Both supplied differential-evolution searches were rerun with their recorded parameters and completed successfully. Their JSON outputs are byte-for-byte identical to the frozen results in this environment. The supplied 80-digit recheck also reproduces its JSON byte-for-byte.

An independent 120-digit recheck using the implicit recurrences and direct series powers again finds positive values at all seven saved parameter vectors. In increasing order of search family and n, the deficits are approximately:

- one switch n=3: 1.889404268700644e-15
- one switch n=4: 3.198234192505675e-17
- one switch n=5: 7.966488137785893e-16
- two switches n=3: 7.655766091075892e-16
- two switches n=4: 7.542312333360864e-16
- two switches n=5: 6.889710101898172e-14
- two switches n=6: 2.163170925256408e-12

These are high-precision numerical diagnostics, not directed-rounding interval certificates. They corroborate the submitted correction of the double-precision apparent negatives; no certified counterexample was obtained. Optimizer reruns do not prove global minimality.

## Source and provenance audit

- Visually inspected the exact 2018 Problem 6.40 page: printed p.132, PDF page 133. The target is |a_n| squared, not a_(2n), and the real-coefficient signed inequality is background. The all-f/all-n quantifiers, the per-function eventual attribution, and the update's limited wording match the checkpoint. The local PDF SHA-256 matches the value in PROVENANCE.md. The live [arXiv landing page](https://arxiv.org/abs/1809.07200v2) still identifies v2 dated 21 September 2018 as the latest version.
- The indexed [1977 primary-PDF excerpt](https://citeseerx.ist.psu.edu/document?doi=ea1cdeb32c106ad049da5f856f5bb77162129243&repid=rep1&type=pdf) independently corroborates printed p.140, equations (6.2)-(6.3), attribution, and quantifiers. This audit does not claim a fresh full retrieval of that PDF.
- Read the relevant local Bshouty-Hengartner primary text, especially pp.228 and 231-233. Its Hayman regularity statement, existence of the coefficient-ratio limit, upper bound 1, and Koebe equality characterization agree with the checkpoint. [Source DOI](https://doi.org/10.5169/seals-40764).
- Checked the [de Branges primary paper](https://archive.ymsc.tsinghua.edu.cn/pacm_download/117/6366-11511_2006_Article_BF02392821.pdf), pp.137-138, for the odd-series Robertson inequality and square-root relationship. It supports the background theorem used here, not the stronger target.
- Independently corroborated the measure representation with Theorem 2.1 and its proof in [Two integral representations](https://people.math.osu.edu/edgar.2/preprints/two/Two%20integral%20representations.pdf). Its plus-sign kernel is equivalent by replacing t by -t.
- The selected cached and pinned dataset records match exactly and state the same target. The imported prior report is triage only, with no candidate proof to reuse. The saved repository-ref evidence and recorded queue/prior-attempt checks are consistent with the provenance narrative. I did not freshly re-query the repository or re-download the entire pinned corpus; this limits independent validation of those administrative negatives and historical hashes.
- The full 2019 Springer chapter was not read; neither the submission nor this audit claims otherwise. A bounded search is not an exhaustive current-status certificate.

## Corrections and limitations

No correction is required to the mathematical partial results or the unsolved classification.

1. Low severity, reproducibility: the README command `python3 verify.py` overwrites CHECKS.json, including environment-specific Python version metadata. Running it in the frozen directory with another interpreter version changes the manifest-bound output. Prefer documenting a scratch-copy run followed by comparison, or eventually adding a non-mutating verification mode. This audit ran everything in a copy and preserved the frozen packet.
2. Low severity, precision of wording: the sentence calling the seven apparent negatives cancellation artifacts and not counterexamples is strongly supported by the reproduced high-precision checks, but those checks are explicitly non-rigorous. For maximal precision, say the high-precision reevaluations are consistent with floating-point cancellation and do not produce a verified counterexample. The existing adjoining warning about non-interval diagnostics already prevents a substantive proof overclaim.

The five log entries describe five distinct mathematical mechanisms and honestly share a final recording timestamp; they do not fabricate a per-tool chronology. Their percentage estimates are clearly labeled planning judgments. Audit acceptance does not convert five approaches into a complete mathematical result.
