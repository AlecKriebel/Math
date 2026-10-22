# Independent adversarial audit: positive-exponent boundary accessibility

Date: 3 October 2026  
Target: rank 545; problem 5300049 / AMR-052-0049; Przytycki (1992), Problem 1.2  
Disposition: **PASS AS AN UNRESOLVED FIVE-APPROACH RESEARCH NOTE.**

No blocking error was found in the six auxiliary propositions, their control examples, or the packet's final unresolved conclusion. This is not a certificate that the original problem is solved, a certificate of global literature completeness, or a formal verification of the cited theorems. The source-sensitive positive result is genuinely pointwise for positive **lower** exponent under its additional hypotheses. It must neither be reduced to an almost-everywhere statement nor extended to an arbitrary basin covered by the 1992 question.

## 1. Frozen identity, scope, and reproducibility

The audited public manifest has SHA-256:

    58a8e9903b32eb6a5f918fbc150194cc359c8288e96cef3b568a793e4320c1c5

Its eight entries were checked individually, with no missing, duplicate, extra, or altered public file. The frozen verifier was executed without its write option, and its JSON output equals the saved `verification.json`. Integrity was checked again after testing. No frozen file was modified and no remote write was made.

The audit read `PROOF.md`, `ATTEMPT_LOG.md`, `SOURCE_GATE.md`, `README.md`, `STATUS.json`, the verification program and output, and the source-byte identification record. The asserted five approaches are distinct: empirical measures, expanding-time selection, inverse contraction, nested approach domains, and coding-tree compactness. There are exactly six numbered auxiliary propositions. Their outcomes support an unresolved 5/5 designation as a count of attempted approaches, not as a completion percentage for the original theorem.

A separately written standard-library program, `verify_independent.py`, computes the finite controls independently. Run it with the public packet as its argument:

    python3 verify_independent.py ../public

It intentionally does not import the packet's functions. It does also run the frozen program separately to compare that program's output with the saved result. Its deterministic audit output is `verification.json` in this audit bundle. All audit deliverables are covered by this bundle's own `SHA256SUMS`.

## 2. Primary-source gate and exact question

The original question was checked in the complete 46-page [1992 collection](https://www.math.stonybrook.edu/preprints/ims92-7.pdf), including the setup on printed p.29 and Problems 1.1-1.2 on printed p.30. Printed p.30 was independently rendered from the PDF and visually inspected. It is PDF page 32 when counting from 1.

The relevant setup is a proper holomorphic self-map of a simply connected domain in the sphere, degree at least two, with iterates converging to a point inside the domain, together with holomorphic extension to a neighborhood of its closure. The question quantifies over individual boundary points and uses a **liminf**, rather than assuming a Lyapunov limit exists. It does not insert complete invariance or genericity for a measure.

The packet's use of the spherical derivative is appropriate. Any two smooth nonsingular metrics on the compact boundary differ by a positive bounded density; the difference of the normalized logarithmic derivative cocycles is an endpoint-density coboundary divided by the iteration number. It tends to zero. This observation does not license use of a singular Euclidean chart at infinity; the spherical convention avoids that issue.

The four available source PDFs have the exact sizes and SHA-256 values recorded in the frozen source-identification file. The page counts checked are 46, 20, 23, and 20 for the 1992, 1994, 2018, and 2021 sources respectively. Source PDFs, source text, and rendered source images are not redistributed with this audit.

## 3. Literature boundary: what the proofs actually support

### 3.1 The 1994 accessibility paper

The audit read the definitions and statements, the complete periodic-source proof in section 1, the complete significant-telescope proof and proof of Corollary 0.1 in section 2, and the external-ray argument in section 3 of [Przytycki (1994)](https://matwbn.icm.edu.pl/ksiazki/fm/fm144/fm14435.pdf). The [author's version](https://www.impan.pl/~feliksp/access.pdf) is an alternative reference.

The hypothesis connecting pullbacks to the specified domain is substantive. A shrinking ambient pullback is not automatically a pullback in that domain. The periodic-source proof explicitly assumes inverse-branch preservation. In the general proof, telescope domains already lie in the designated domain and their compatible pullbacks are part of the hypothesis.

The general telescope argument uses uniform edge shrinking, significant terminal pieces, quantitative separation, positive time density, and shrinking traces. Its diagonal selection retains those geometric controls. It is therefore much stronger than compactness of symbolic itineraries. Notably, the proof does not require a new distortion estimate once the telescope data are supplied. Corollary 0.1 obtains such data almost everywhere using a stated Pesin inverse-branch input and recurrence; that input was checked as a dependency, not reproved from foundations. Remark 0.4 supplies the completely invariant attracting-basin application; Remark 0.7 explicitly flags the missing basin-preservation issue.

### 3.2 The 2021 lower-exponent statement

The complete accessibility section and its surrounding coding-tree definitions were read in the 20-page [2021 survey](https://www.impan.pl/~feliksp/Siles.pdf). Theorem 8.1, on PDF page 18, was independently rendered and visually checked: the chi is underlined. That is the positive **lower** Lyapunov exponent, consistent with the lower/upper notation elsewhere in the survey.

The theorem is pointwise on the relevant closure of the coding-tree limit set, with uniform shrinking and local backward invariance. These hypotheses remain necessary to the cited application. Section 8 is a statement-and-citation presentation, not a new complete proof of the pointwise lower-exponent implication. The packet acknowledges this dependence. Reading the older almost-everywhere corollary alone would miss the stronger later statement; conversely, neither publication supplies a license to discard domain-side requirements.

The [2018 survey](https://www.impan.pl/~feliksp/FP_ICM_Survey_home.pdf), section 10, was also checked through its full measure-lifting proof. Its description makes clear that the relevant telescope domains must lie in the designated domain. The lifting argument does not transfer a typical-point conclusion to every starting point.

### 3.3 Admissible consequence and limit

The packet correctly recognizes the known positive-lower-exponent pointwise consequence for a completely invariant rational attracting basin. Here complete invariance supplies the needed pullback-side condition, and the attracting-basin coding-tree construction supplies uniform shrinking and boundary accumulation. This is a cited consequence, not a new result of the packet.

For the original broader setup, citing that consequence is insufficient. Nor does failure to establish its hypotheses prove that accessibility fails. The note correctly makes neither assertion.

## 4. Auxiliary proposition audit

### Proposition 1: empirical limits have positive derivative-potential integral

**Pass.** Compactness yields weak subsequential limits. The telescoping test-function identity proves invariance. The one-step logarithmic derivative is bounded above and continuous as an extended-real function with value minus infinity at critical points; truncating below produces continuous real-valued functions.

The inequality direction in the truncation argument is correct: every fixed truncation has limit integral at least the orbit's positive lower average. Applying monotone convergence to an upper bound minus the truncation then gives the same lower bound for the integral of the untruncated potential. Its negative part is integrable, not merely formally allowed to be infinite. An orbit encountering a critical point cannot have the assumed positive lower exponent.

An ergodic component with positive integral follows from decomposition. The proof does not assert that the original point is typical for that component or lies in its support. Those unsupported conclusions would be serious errors; neither occurs here.

The square-digit example correctly blocks the support-transfer shortcut. The number of exceptional length-m windows is bounded by m times the number of square positions up to the relevant endpoint. Its exceptional density tends to zero for fixed m, and then uniform continuity supplies convergence of empirical measures to the point mass at 1. Infinitely many ones separated by unbounded gaps rule out eventual periodicity, hence the starting angle is nonzero and is not eventually mapped to 0. Its exponent is log 2 and it is radially accessible. It is therefore a counterexample only to the proposed measure-to-starting-point inference.

### Proposition 2: strict record times give the claimed quantitative bound

**Pass.** Subtracting cn from the partial sums converts each required suffix inequality into comparison with every earlier adjusted sum. Every strict record is consequently a valid time. At a record the running maximum increases by at most A-c, even when some individual terms have arbitrarily large negative magnitude. No lower bound on the terms is silently needed.

The terminal adjusted sum is at least (b-c)N. Since the running maximum begins at zero, at least (b-c)N/(A-c) strict records are required. As a count, this entails the appropriate integer ceiling. Once the lower average exceeds b, the same estimate holds for every sufficiently large endpoint N, proving positive **lower** density of the fixed set of record times. It is not just a subsequence-dependent density statement.

Application to the derivative cocycle is legitimate because the compact orbit set gives a finite upper bound for the one-step logarithmic derivative, and positive lower exponent excludes critical hits. But scalar suffix expansion is not by itself a uniform-radius inverse-branch theorem, a bounded-distortion theorem, or a selection of pullback components in the designated basin.

### Proposition 3: the dyadic-spike obstruction

**Pass.** For 2^m <= N < 2^(m+1), the losses already incurred sum to 2^(m-1)-1. Thus the exact partial-sum expression and lower average 1/2 are correct. The dyadic terms divided by their indices tend to -1/4. For each fixed cutoff, the last sufficiently large dyadic term alone gives the stated negative-tail lower bound.

The quantifier order is adequate: each fixed cutoff is followed by arbitrarily large dyadic endpoints. The claimed lower bound is conservative; there is no need to claim an exact negative-tail limit. Most importantly, no holomorphic realization of this scalar itinerary is offered. It blocks an inference based only on numerical average and upper-bound data. It does not refute the pointwise theorem and does not establish recurrence behavior in a genuine basin.

### Proposition 4: a contracting inverse map and a returning component

**Pass.** The same-component hypothesis provides a finite polygonal bridge inside the intersection of the disk and the basin. Basin preservation keeps every iterate of this bridge in the basin. The endpoint identity makes the consecutive curves concatenate. Convexity of the disk justifies the uniform distance contraction from the derivative bound, while the chain rule gives geometric decay of lengths. Both finite total length and continuity at the limiting endpoint follow.

The hypotheses are stronger than accessibility and are presented only as sufficient conditions. A repelling periodic multiplier supplies an analytic inverse branch on a sufficiently small disk, but does not by itself prove either basin-side preservation or return to the same local component. The argument does not smuggle these topological facts in through the inverse-function theorem. It also does not claim that its elementary component condition is a replacement for every hypothesis in the published coding-tree theorem.

### Proposition 5: nested connected approach sets

**Pass.** From an access curve, choose successively later tails lying in successively smaller balls and take their components in the basin-ball intersections. Containment of the smaller tail in the earlier component gives nesting; openness and planar local path connectivity give open connected components. The endpoint is in each closure and the diameter bound tends to zero.

Conversely, the chosen points in consecutive nested open sets can be connected inside the earlier one. Every later path lies there as well. Approximation of the boundary point by that set bounds its distance from every point in it by the set's diameter, proving endpoint continuity of the concatenation.

The slit-comb control is valid. The removed collection is relatively closed, its possible accumulation outside the rectangle causes no failure of openness, and the remaining domain is connected by paths above the slits. Its spherical complement is connected, so the plane-domain criterion gives simple connectivity. Horizontal approaches reach the stated slit points. A hypothetical final curve tail at heights between 1/8 and 3/8 must cross one of the intervening vertical slits by the intermediate value theorem, a contradiction. No holomorphic dynamics on this domain is constructed; accessibility is therefore shown not to be closed under pointwise limits in this topological example only.

### Proposition 6: an abstract tree with a nonclosed endpoint set

**Pass.** A nonzero edge at generation n can occur only if the first one was at position k with k < n <= 2k. Its length is exactly 1/(k+1), bounded by 2/(n+2). A branch with first one at k makes exactly k such drops, ending at 1/(k+1); the all-zero branch stays at 1. Every branch consequently converges, but the resulting endpoint set omits its accumulation point 0.

The branches whose first ones occur successively later converge in the symbolic topology to the all-zero branch, yet their endpoints converge to 0 instead of 1. This precisely refutes the claim that uniform edge shrinking and convergence of every branch imply continuity, or closed image, of the endpoint map. Uniform edge shrinking is not uniform control of whole branch tails.

The construction is explicitly a map of an abstract binary tree with overlapping or degenerate edges. It is neither an embedded geometric tree nor a coding tree generated by a holomorphic map. Its role is correctly restricted to testing a bare diagonal argument. The significant-telescope proof has extra information that this example does not meet.

## 5. Independent finite replay

Every check below passed with exact integers or rational arithmetic:

- **5,460 scalar sequences:** every word of lengths 1 through 6 over {-2, 0, 1, 3}. There are 1,644 words meeting the average hypothesis. All suffix inequalities were independently enumerated, and every strict record was checked against them and against the record-jump bound. A total of 11,161 suffix-valid indices occurred over the entire enumeration.
- **4,096 dyadic terms:** losses were constructed by adding spikes at powers of two rather than using the packet's bit-test helper. Every partial-sum identity and lower-average bound passed. There are 2,736 strict records for c=1/4. Four fixed negative-tail cutoffs passed.
- **2,046 binary-tree edges:** all edges through generation 10 were independently calculated by summing individual drops. Both the exact nonzero-edge condition and the uniform bound passed.
- **384 stabilized-endpoint checks:** six terminal generations were tested for each of the first 64 possible first-one positions, plus 64 all-zero controls.
- **72 square-digit window checks:** affected shifts were independently assembled as intervals contributed by square positions and compared with a direct window enumeration. All counts and bounds passed.
- **90 monomial chain-rule controls:** degrees, derivative coefficients and derivative exponents were updated recursively for degrees 2 through 10 and iterates 1 through 10.

For the monomial control, the mathematical justification beyond those integer tests is simple: an orbit beginning on the unit circle remains there, the Euclidean derivative of the n-th iterate has magnitude d^n, and the spherical density ratio is exactly one. The radial path approaches each prescribed boundary point from the disk. These controls are therefore consistent with the statement but do not test general Julia-set accessibility.

The tests do not prove infinite density, limiting measures, limiting tree endpoints, topological simple connectivity, holomorphic realizability, or the original universal assertion. Those claims stand or fall with the written mathematical arguments and cited hypotheses. The frozen packet correctly makes this limitation explicit.

## 6. Exact remaining gap and final assessment

The missing step is to obtain compatible, significant, basin-side shrinking telescopes at the **prescribed** positive-lower-exponent boundary point from the original hypotheses alone, or to provide a different valid mechanism producing an access curve. The known theorem can be invoked after its domain-preserving hypotheses are met; the packet does not derive them in the original general setting. Removing a sufficient hypothesis from that theorem is a research objective, not an established implication and not a necessary-condition claim for accessibility.

The following proposed bridges remain unsupported, and the note correctly rejects them:

1. A positive-exponent empirical limit makes the original starting point a typical accessible point.
2. Scalar record-time estimates automatically give every desired critical-recurrence, distortion, or basin-side pullback estimate.
3. An ambient contracting inverse branch automatically preserves the chosen basin and its local component.
4. Limits of accessible boundary points are automatically accessible.
5. Uniformly shrinking coding edges alone make the branch-endpoint map continuous or its image closed.

A genuine negative resolution would require a holomorphic proper self-map with the original extension and attraction assumptions, a specified positive-lower-exponent boundary point, and a proof that no access curve from that basin lands there. None of the scalar, comb, or abstract-tree controls provides these data. A positive resolution would require a proof closing the basin-side step for all points in the original scope. Neither resolution is claimed or established.

**Recommendation:** retain the unresolved status, five attempted approaches, six auxiliary propositions, and the carefully qualified known subcase. No mandatory mathematical correction is identified in this frozen packet. Keep the lower-exponent notation and both additional theorem hypotheses prominent wherever the result is summarized.

This audit does not independently certify the historical repository searches, catalogue availability, novelty, or absence of all differently worded later solutions. Those bounded provenance statements are not used as proof of the mathematical outcome. The audit's affirmative verdict concerns the internal correctness and source scope of the frozen unresolved research note.
