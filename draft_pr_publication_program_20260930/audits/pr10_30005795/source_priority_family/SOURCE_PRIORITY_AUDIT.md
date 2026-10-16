# Independent source/status audit of PR10

Audited head: `925f9e9f46f2c7407fd142cedf36995a4519a378`. Family: source provenance, prior publication, and claim classification. Checked 2026-10-01 UTC. No external individual contacted, no outreach prepared, and no candidate/queue/publication state edited.

## Verdict and exact scope

**Accept as a known-method/source-status correction**, conditional on the separate mathematical families confirming the finite-support geometry and threshold argument. The narrow task is to find a finite constant, allowed to depend on the input surface and negative-part family, uniform over the specified surface divisors. This audit finds primary-source support for treating that task as already known. There is no evidence in the cited passage for a new sharp-constant conjecture, a numerical constant independent of the input, or an unresolved application-specific K-stability bound. No novelty or new-solution credit is justified.

If `already_solved` is the queue's available status for a known-in-literature task, it is defensible with an explicit note that the source is a teaching/method question and the literal extracted statement needs repair. The more precise prose label is `known bound / source-status correction`. A novel paper is unnecessary for this accepted outcome.

## Official statement and context

Visually checked [the official OWR report](https://ems.press/content/serial-article-files/48650), printed pp.836, 837, 839, 840, and 844 (PDF pages 10, 11, 13, 14, 18, counting from one). Section 1 chooses a Du Val surface. Section 3 expressly inherits its assumptions, states that the restricted positive part is nef, and uses surface discrepancies/valuations. The final sentence on p.839 prints **“over X”**; the preceding quantifier and p.840 example print **“over S.”** This is a real typesetting error rather than extraction corruption. The meaningful repair is a prime divisor over S. The delta invariant on p.837 only uses divisors whose center on S contains P, so the local application can use local thresholds; an all-centers formulation needs global thresholds.

The contribution identifies itself as a four-lecture abstract teaching K-stability techniques. Section 3 invokes reference [3] and immediately follows its question with a log-canonical worked example. That context does not support the dataset's assertion that it explicitly announces an unresolved 2024 technical problem. The body ends on p.843, but **its bibliography is on p.844**, where [3] identifies the 2023 paper below. Correct the candidate's bibliography locator `p.843` to `p.844`; quoting the whole contribution as pp.836–844 is more exact.

## Published prior bound: assumptions versus proof dependencies

The [published Cambridge article](https://www.cambridge.org/core/journals/nagoya-mathematical-journal/article/kstable-divisors-in-mathbb-p1times-mathbb-p1times-mathbb-p2-of-degree-112/999FB6032A21485AD71CF230CC802E6C), DOI [10.1017/nmj.2023.5](https://doi.org/10.1017/nmj.2023.5), was published online 28 April 2023. Appendix B begins on printed p.712; Lemma 27 and its proof span pp.712–713. Its setup does assume a del Pezzo fibration and a normal Du Val fiber. It also assumes a finite negative-part decomposition and uses local thresholds at P. The [author-hosted preprint](https://www.maths.ed.ac.uk/cheltsov/pdf/220608539.pdf) gives the same mechanism as Lemma 26 on printed p.23 (PDF page 23).

The lemma has two proof steps. The first uses the threshold discrepancy inequality for each restricted component; the second compares the residual volume term with an anticanonical surface volume. The fibration is used for the second step through the anticanonical restriction identity. The first step only needs the effective restricted components, their thresholds, a nonnegative weight, and the finite sum. **Removing the fibration assumption for the isolated negative-part bound is an inference from the displayed proof, not a claim that Lemma 27 is literally stated without that assumption.**

For clarity, the independent algebra behind that inference is as follows. If

\[
N(u)|_S=\sum_{j=1}^{r} f_j(u)D_j,\quad
w(u)=\frac{3(P(u)^2\cdot S)}{(-K_X)^3}\ge0,
\]

and \(c_j\) is a threshold valid for the chosen centers, then

\[
\operatorname{ord}_F(D_j)\le A_S(F)/c_j
\quad\Longrightarrow\quad
I(F)\le A_S(F)\sum_{j=1}^{r}\frac{1}{c_j}\int_0^\tau w(u)f_j(u)\,du.
\]

The auxiliary volume contribution in the published lemma appears identically on both sides of its first inequality, so isolating the negative-part contribution requires no anticanonical identity. Substituting global thresholds extends the componentwise discrepancy argument to every center on S. The report itself already gives its one-component log-canonical instance on p.840. Threshold positivity and coefficient integrability remain mathematical obligations; this source audit does not replace the independent checks assigned to the LCT and Mori families.

The published first display has a stray summation upper limit \(\tau\) where the decomposition and subsequent displays require \(r=l\). The same typographical slip appears in the downloaded preprint. The candidate's finite-component formula repairs it correctly; no dependence on an integer-valued pseudo-effective threshold should be inferred.

## Duplicate and immutable provenance

Read both numeric IDs directly from the cached `problems.json` pinned to dataset revision `37e53eabe540fb458758e198be61634bd02ee008`. Independently recomputed SHA-256 `04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf`, exactly matching the repository manifest. Record 30005796, code OWR-14298162-003, reproduces the same p.839 request, calls itself a duplicate, and says the official report confirms repetition. It has no independent target. Preserve the numeric identity but give it no separate discovery budget or credit. The complete selected records and provenance are in `duplicate_records.json`.

`source_manifest.json` records the exact fetched URLs, redirect destinations, byte counts, and SHA-256 hashes. Scratch downloads/renders live only in ignored `tmp/source/`. The official report hash is `34de186d27fc36bcf161f7d10db57f2572bdc03fa5b32c31204cedee2fe5378c`; author preprint hash is `070791cc38afca17a0dc331dcc7a1364a7b9bb743a536aead7405d0c444f33df`; publisher PDF hash for this retrieval is `daebfc6977caa561dadaa85517e3af85d590bab064c83ba02cdbee58aa944f56`. The publisher PDF includes a retrieval-specific footer, so that last hash identifies this downloaded copy rather than promising a stable hash for every future download.

## Actionable disposition

1. Accept the claimed known-bound/source-correction outcome if the independent mathematical families pass the stated assumptions. Preserve its absence of novelty claims.
2. Correct the official bibliography locator to p.844. Describe the generality beyond the published fibration setup as the first proof step's direct extension.
3. Keep the local/all-centers distinction and state finite-support/integrability hypotheses whenever the bound is abstracted away from the source geometry.
4. Mark 30005796 as the same target in later authorized queue maintenance. Do not treat extracting the same teaching question twice as two open problems.

Strongest verified result of this family: the question's typing/context and the 2023 prior-publication mechanism are independently established from visual primary-source checks. Exact remaining gap: separate verification of the candidate's general Fano finite-support/restriction justification and its threshold edge cases. No independent source evidence identifies a stronger unsolved target that this PR should claim to resolve.
