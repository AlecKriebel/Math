# Independent source, original-scope, and priority audit of PR523

Review completed 2026-10-13 UTC. Target: problem 30004064 / OWR-16766-003. Frozen candidate read only. All review work is under this `source01` directory. No outreach, remote mutation, commit, push, preprint preparation, or publication occurred.

## Verdict

**Reject promotion as a novel full resolution of the original research question.** The candidate's exact mathematical theorem is correct, but (1) it narrows the source's experimentally motivated conjecture to an exact-multiplier reading which the cited paper already distinguished from its useful numerical output, and (2) the *same general theorem*, including the projected/rank-deficient extension, was explicitly published in a prior public preprint. These are independent defects in the publication gate; neither is repaired by disclaiming novelty while marking the effort as a novel discovery.

For the catalogue's displayed exact-minimizer rule, the defensible classification is **already_solved**, with the prior result and its scope recorded. For the original Kadu conjecture, the strongest independently verified conclusion is that the unique-image sign-recovery clause is false even when the multiplier is allowed to be an arbitrary approximate/numerical value. The prior 5×5 construction gives that result. This does not rely on a theorem about central paths, solver stopping rules, or the prior author's broader numerical assertions.

## Exact original source and hypotheses

I independently downloaded and read Kadu's complete contribution in [OWR 4/2019](https://ems.press/content/serial-article-files/46783), printed pp.256–259, PDF pages48–51 (one based). All four pages were rendered and visually inspected. Theorem1 and Conjecture1 are on printed p.258/PDF page50. The report uses full row rank `rank(A)=m` and qualitatively limited tomography `m << n`; it does not specify a numerical solver, tolerance, or limiting procedure in the conjecture. The data name changes from `b` to `y` at its dual equation, without changing the reconstruction problem.

Theorem1 displays

\[
 \min_{\mu\in\mathbb R^m} \frac12\|\mu-y\|^2+\|A^T\mu\|_1,
 \qquad x^*=\operatorname{sign}(A^T\mu^*).
\]

Conjecture1 includes: “If the problem has a unique solution, then the dual approach retrieves it.” It also asks for all binary solutions' common pixels when there is more than one solution. The surrounding small-image experiments use row, column, diagonal, and opposite-diagonal projections. Printed p.259 expressly lists proving Conjecture1 among the open questions. Thus a literal exact-rule reading is textually available; it is not a faithful substitute for every meaning of the experimental approach.

## Catalogue provenance and the correction boundary

I also independently retrieved the full [Hugging Face catalogue at its frozen revision](https://huggingface.co/datasets/ulamai/UnsolvedMath/blob/372682f27c1b0d3d39e75fa63ad7932c7a2e1bde/problems.json). The exact target30004064 is retained in `sources/catalogue_target_exact.json`. Its `original_statement` asks about the dual approach, without an exact-minimizer definition. Its `clean_statement`/current `statement` inserts the exact optimizer and sign rule used by the candidate. The catalogue labels that change `corrected_verified` and claims preservation of source hypotheses, but it omits the report's full-row-rank/limited-data restriction and does not preserve the paper's approximate-output distinction. These source claims must be audited, not treated as authority. The earlier scalar discussion prevents the clean statement from being silently equated with the complete experimentally motivated conjecture. The independently found prior preprint expressly covers this catalogue identifier as a duplicate.

## Version and formulation reconciliation

Primary files were obtained independently; URLs, retrieval timestamps, byte counts, and SHA-256 digests are in `sources/retrieval.json`. [arXiv's history](https://arxiv.org/abs/1807.09196) dates v1 to 24 July2018, v2 to 13 December2018, and v3 to 15 December2020. The CWI manuscript is byte-identical to v3. The [IEEE version of record from Utrecht](https://dspace.library.uu.nl/bitstream/handle/1874/407504/A_Convex_Formulation_for_Binary_Tomography.pdf?sequence=2) was separately obtained; it is not v3.

| Primary version | Checkable clauses | Consequence for this audit |
|---|---|---|
| arXiv v1 | pp.2–3, §II and equations10–11 | Zero-sign initially left undefined; scalar soft threshold already yields zero at noiseless endpoints `y=±1`. |
| arXiv v2 | pp.2–3, §II; p.4 numerical discussion | Defines `sign(0)=0`, yet scalar prose still calls recovery at zero undefined. Approximate-iterate signs are distinguished. |
| IEEE version of record | printed pp.2–5, §IIA–C, §III, equations10–14, Algorithm1 | Defines zero sign as zero; scalar discussion explicitly yields a zero recovered pixel. Numerical enumeration solves approximately in CVX and thresholds at `10^-9`. |
| arXiv v3/CWI | pp.2–3, §II; pp.4–6, §IIC, §III, Algorithm2, §IV | Retains exact zero-scalar formula and the approximate/smoothing discussion. Adds an auxiliary subgradient/primal variable `z`; Algorithm2 returns `sign(z^T)`. |

The v2/v3 prose inconsistency about zero does not affect the explicit optimizer formula or the distinction between exact and approximate output. The scalar sections propose approaching the zero optimum “from the correct side”; smoothing also shifts the optimizer. Both mechanisms were already discussed before OWR2019. The v3 auxiliary-variable algorithm is a later formulation and cannot silently be inserted into OWR Theorem1.

The public [author CVX script](https://github.com/ajinkyakadu/BinaryTomo/blob/db4965de499981be13ddf7a979f1cd0e9e1fd51f/test_tomo_cvx.m) confirms the actual protocol: lines42–48 remove dependent rows and scale matrix/data; lines103–111 choose Gurobi with SDPT3 mentioned and minimize the stated objective approximately; lines114–117 threshold `A'*p` at `10^-10` and take its sign. [getA.m](https://github.com/ajinkyakadu/BinaryTomo/blob/db4965de499981be13ddf7a979f1cd0e9e1fd51f/bin/getA.m), lines27–58, supplies two to four lattice directions. These files were read, not executed. The latest repository commit is dated18 January2023; the all-state issue list was empty at retrieval.

## What was known, and what is positively duplicated

The old scalar obstruction is **not** by itself evidence that the authors had settled their numerical/tomographic conjecture. They knew exact scalar multiplier recovery degenerates, and their experiments concerned approximate output. The frozen candidate correctly acknowledges the scalar fact, but its conclusion that it resolves the original question must remain qualified by this difference.

There is now positive, dated overlap beyond the scalar case. Alper Ferudun's [*A Negative Answer to the Kadu–van Leeuwen Conjecture on Dual Binary Tomography*](https://eulersolve.org/papers/owr-16766-004/paper.pdf), version1.0, pp.3–7, explicitly states the same universal projected zero-optimum theorem as Lemma2.1 and supplies original-scope counterexamples. The note identifies OWR-16766-003 as a duplicate of its target. It is unrefereed.

Chronology does not rest on the author's web date. The [DataCite DOI record](https://api.datacite.org/dois/10.5281/zenodo.23110494) is `findable`, version1.0, and gives creation, registration, and update at **2026-10-02T20:09:16Z**, with issued date2026-10-02. The publisher metadata matches the independently downloaded PDF hash `b374bbc76792418e60fa96a329a5ae6b6f5e596b12b5572b69466d6467bab43b`. The source ZIP and verification-report hashes also match its metadata. The frozen candidate's source gate is dated4 October2026. An author's claimed publication date alone would be weaker evidence; the DOI registration is independent chronological corroboration.

| Frozen candidate content | Explicit earlier content |
|---|---|
| Universal `y=As`, `s∈[-1,1]^N`, unique zero optimizer for full row rank | Ferudun Lemma2.1, p.3, same feasible-box hypothesis and full-row-rank conclusion |
| Projected objective and minimizer set `ker(A^T)` | Same lemma, same projected objective, same complete minimizer set |
| Zero multiplier certifies no informative exact signs | Same lemma and Proposition2.2, p.3 |
| Difference between exact optima and numerical signs | Ferudun §2–3, pp.3–5, explicit reconciliation |

I independently checked the universal deduction: set `P=AA†`, `w=Pμ`, and use `y=As` with `|s_j|≤1`. Then

\[
 G_y(\mu)-G_y(0)=\tfrac12\|w\|^2+
 \sum_j\bigl(|(A^Tw)_j|-s_j(A^Tw)_j\bigr)
 \geq\tfrac12\|w\|^2.
\]

Equality is attained exactly when `w=0`, because `A^Tμ=A^Tw`; this is exactly `μ∈ker(A^T)`. For full row rank, `P=I`, so zero is unique. This validates the overlapping theorem without accepting any numerical assertion in the prior preprint. An audit-local exact checker also verifies 2,000 rational identities on an arbitrary rectangular matrix and box-feasible data.

## Strongest independently checked result about the original conjecture

The intended sign-recovery question has a materially stronger obstruction than exact degeneracy. The prior Theorem4.2 uses this 0/1 image:

\[
 X=\begin{pmatrix}
0&0&0&1&0\\0&1&0&0&0\\1&0&0&0&1\\1&0&0&0&0\\0&0&1&0&0
\end{pmatrix},\qquad
 c=\begin{pmatrix}
1&0&0&-1&0\\0&-2&0&1&1\\0&0&1&0&-1\\-1&1&0&0&0\\0&1&-1&0&0
\end{pmatrix}.
\]

Let `A` measure rows, columns, and diagonals `j-i=constant`; put `s=2X-1`. I independently verified in exact arithmetic that `Ac=0`, every nonzero `c_j` has `s_jc_j<0`, and `s+c` lies in the cube with the same measurements. An independent constrained enumeration of 6,250 binary candidates finds exactly `X`. The full 19×25 matrix has rank16. The earlier source's row-space potential plus an independent rational rank calculation on the 11 supported pixels proves that the entire box solution set is the segment `s+tc`, `0≤t≤1`, with14 fixed pixels.

Here is an independent, solver-free consequence of that checked certificate. If any real multiplier `μ` had `sign(A^Tμ)=s`, then each nonzero term `c_j(A^Tμ)_j` would be strictly negative. But

\[
 \sum_j c_j(A^T\mu)_j=\mu^TAc=0,
\]

a contradiction. Therefore **no real multiplier whatsoever** can return that unique binary image by a componentwise sign. Taking a small-entry threshold first cannot repair unique-image retrieval: a successful complete binary output still requires all signs to agree with `s`. The witness falsifies the unique-recovery clause independent of exact optimality, approximation quality, solver choice, stopping rule, or central-path claims.

Padding the 0/1 image by zero rows and columns gives every sufficiently large square size: outside pixels are forced by zero row/column sums. There are at most `4k-1` measurements on `k²` pixels; removing dependent measurement rows preserves the feasible set, the certificate, and full row rank. Thus arbitrarily strong undersampling does not save the claim.

I also independently checked the prior p.7/Theorem4.6 explicit 4×4 example: four binary solutions share four zero pixels, but the supplied rational box-feasible image moves two of those pixels to1/2. This establishes failure of the fixed-pixel/common-coordinate surrogate and also obstructs the *unthresholded* exact intersection sign pattern. It is not used here to assert a theorem about every possible finite threshold or every solver. I have not independently established the note's all-image counts, all numerical experiments, or cited central-path rates.

This distinction is historically grounded. [Fishburn–Schwander–Shepp–Vanderbei1997](https://vanderbei.princeton.edu/tex/myPapers/discreteRadonTransform.pdf), Theorems2–4 at printed p.47/PDF page9, already distinguishes uniqueness among binary sets from uniqueness among fractional sets, constructs a nonadditive unique set for three directions, and proves coincidence for two directions. The paper does not discuss the later Kadu conjecture. Inferring failure of strict full-sign recovery from a nonadditive unique set uses the row-space definition of additivity; it is an inference from the old theorem, not an assertion that the old paper announced a refutation of a later conjecture.

## Reasonable repair before disposition

A mathematical repair of the source-scope gap is concrete: replace reliance on the 3×3 two-direction exact-zero example by a three-direction nonadditive unique image, prove a kernel sign obstruction as above, and state carefully which multiple-solution reading is covered. Two directions are an integral bipartite-incidence system, so their box solution set is the convex hull of their binary solutions; the frozen example's common pixels remain fixed in the box relaxation. Its exact-zero failure does not disprove the useful numerical/fixed-pixel reading.

**That repair cannot recover novelty.** The explicit universal theorem and these original-scope witnesses are already public prior work with checked chronology. Citing them and reproducing them would produce an attributed explanatory/reproducibility note, not the novel original-resolution result required for promotion. Finding a different small witness or rewriting the inequality does not restore discovery priority. A materially new theorem about a separately specified algorithm would require its own research claim and full proof, and would not automatically solve this original target.

Recommended disposition: preserve the valid frozen derivation and this audit as research evidence; update the source/priority record to acknowledge the earlier theorem; classify the literal recorded question `already_solved` with a scoped explanation; do not publish a new claimed-solved preprint or release under the current gates. If a tracker has no `already_solved` state or conflates distinct solver formulations, record the precise mismatch and hold the claim rather than silently substitute `unsolved` or a stronger solved label. There is no need for outside input to decide the exact-theorem priority duplication, and no outreach was prepared.

## Search bounds and reproducibility

`SEARCH_LEDGER.md` records targeted query batches, primary-source retrievals, inaccessible endpoints, the author-code history/issue check, and all13 OpenAlex citation records screened as discovery metadata. No separate author erratum or later primary theorem repairing the conjecture was identified in those searches. Negative searches do not establish novelty; the rejection above relies on a positive matching prior theorem and independently checked counterexample.

Run `python3 verify_source_certificates.py` from this review directory to reproduce `certificate_checks.json`. Downloaded papers, extracted text, source ZIP, and page renders are local reading inputs excluded by this directory's `.gitignore`; do not add them to publication artifacts. `PRIORITY_VERDICT.json` provides the machine-readable decision and exact remaining gaps.
