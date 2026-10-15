# Independent adversarial tomography audit

PR523 / problem 30004064 / OWR-16766-003. Completed 2026-10-13. Audit completion estimate: 100% for the assigned finite geometry/combinatorics and exact-rule scope checks. No external communications, remote changes, commits, pushes, candidate-code imports, or candidate-verifier replays were used. This is an audit, not a paper.

## Verdict and exact theorem

**PASS for the displayed exact-minimizer recovery question.** The frozen result is mathematically correct. The row/column matrix is genuine discretized tomography, its datum is binary-feasible, its rows are independent, its binary fiber has exactly two members, and five pixels are fixed. Both the unique-solution and common-coordinate clauses fail for the exact rule. No correction to those constructions is needed.

Let A be any real m-by-N matrix and let y=As for s in [-1,1]^N. Then

\[
F_y(u)=\tfrac12\|u-y\|^2+\|A^Tu\|_1,
\quad
F_y(u)-F_y(0)=\tfrac12\|u\|^2+
\sum_j\bigl(|(A^Tu)_j|-s_j(A^Tu)_j\bigr)
\geq\tfrac12\|u\|^2.
\]

Each summand is nonnegative because |s_j|<=1. Equality at the optimum is possible only for u=0. Thus **the unique minimizer is zero**, with no rank or tomography assumption. Under the source's sign(0)=0 convention, exact recovery is the all-zero vector. On a nonempty binary fiber this matches its common-coordinate vector if and only if every coordinate varies across the fiber. It never recovers a unique binary image with N>0. This is a universal algebraic proof; finite tests do not establish its universal quantifier.

For the projected objective G_y(u)=1/2 ||P(u-y)||^2+||A^Tu||_1, where P projects orthogonally onto range(A), noiseless box feasibility gives Py=y and

\[
G_y(u)-G_y(0)=\tfrac12\|Pu\|^2+
\sum_j\bigl(|(A^Tu)_j|-s_j(A^Tu)_j\bigr).
\]

Any minimizer has Pu=0. Conversely Pu=0 means u is orthogonal to range(A), hence A^Tu=0, so every such u is a minimizer. Therefore argmin G_y=ker(A^T), and **every minimizer has zero backprojection**. The absence of uniqueness in the projected formulation does not provide a recovery escape.

## Genuine ray geometry and the 3-by-3 binary fiber

Use a square partitioned into unit cells Q_(r,c)=[c,c+1]x[r,r+1], r,c=0,1,2. A pixel image is constant on each cell and zero outside the square. The horizontal rays at height r+1/2 and vertical rays at horizontal coordinate c+1/2 each traverse exactly one unit of every cell in their row or column. Selecting all horizontal rays and the first two vertical rays gives exactly

\[
A=\begin{pmatrix}
1&1&1&0&0&0&0&0&0\\
0&0&0&1&1&1&0&0&0\\
0&0&0&0&0&0&1&1&1\\
1&0&0&1&0&0&1&0&0\\
0&1&0&0&1&0&0&1&0
\end{pmatrix},\qquad y=(3,1,1,3,1)^T.
\]

Boundary conventions are immaterial because the rays pass through cell centers. Negative values are the signed normalization used by the mathematical formulation. If nonnegative physical attenuation is desired, recode each image by B=(S+1)/2. Its exact 0/1 line data are (3,2,2,3,2), obtained by adding the known all-one baseline and dividing by two. Thus the signed normalization does not hide an invalid projection datum.

The first row sum 3 forces the first row to +1. The first column sum 3 forces the first column to +1. The omitted third column is inferable as (3+1+1)-3-1=1. Each residual row and column in the lower-right 2-by-2 block must have sum zero. Its only possibilities are

\[
\begin{pmatrix}a&-a\\-a&a\end{pmatrix},\qquad a\in\{-1,1\}.
\]

This proves there are exactly two binary solutions. Their common vector is (1,1,1,1,0,0,1,0,0), containing exactly five fixed +1 pixels. The zero exact recovery loses all five. This exhaustiveness proof is independent of enumeration.

Full row rank follows directly: in a vanishing linear combination of row-ray coefficients alpha_r and the two column-ray coefficients beta_c, the entries of the omitted column give alpha_r=0; remaining entries give beta_c=0. Independently, the exact Gram determinant is det(AA^T)=81, also certifying rank 5. The independent verifier builds A from ray/cell intersection lengths, rather than copying the candidate's incidence constructor.

With the same A and datum (3,3,3,3,3), each row is saturated and every pixel is +1. This binary solution is unique, yet recovery is zero. Mixed saturated rows give uniquely determined mixed-sign images too, so a fixed replacement sign(0)=+1 or -1 cannot rescue the general unique-image claim.

## All-size family, rank, and undersampling

For each integer k>=3, place +1 outside the lower-right 2-by-2 block and place one of the two checkerboards inside it. Measure all k rows and the first k-1 columns. The reduced datum is

\[
y_k=(\underbrace{k,\ldots,k}_{k-2},k-2,k-2,
\underbrace{k,\ldots,k}_{k-2},k-2)^T.
\]

The full datum adds one last column sum k-2. Saturated first k-2 rows and columns force every exterior pixel to +1. The last two row equations and the measured penultimate column equation, together with the inferred last column, force precisely the two checkerboards. Hence there are exactly two solutions and k^2-4 fixed pixels for **every** k>=3. This proof does not depend on large-image enumeration. It also works at k=2, where the fixed-pixel count is zero and the common recovery control succeeds.

The omitted-column coefficient argument proves rank(A_k)=2k-1. A second independent certificate is the Gram block form

\[
A_kA_k^T=\begin{pmatrix}kI_k&J_{k\times(k-1)}\\
J_{(k-1)\times k}&kI_{k-1}\end{pmatrix}.
\]

Its Schur complement is kI_(k-1)-J_(k-1), whose eigenvalues are 1 once and k with multiplicity k-2. Thus det(A_kA_k^T)=k^(2k-2)>0. The ratio of independent measurements to pixels is (2k-1)/k^2=2/k-1/k^2 ->0, while the fixed-pixel fraction is 1-4/k^2 ->1. For any fixed positive undersampling threshold, sufficiently large k satisfies it. The source's informal m much smaller than n condition therefore does not exclude the construction.

The all-positive unique-image example extends to every k by saturating all row sums at k. A mixed-sign unique-image family follows by saturating some rows at k and others at -k. These are still severely underdetermined as real linear systems and unique as binary systems.

Keeping all 2k rays creates exactly the row dependency w=(1,...,1,-1,...,-1). Deleting the last column ray leaves the independent matrix just proved, so the full matrix has rank 2k-1 and ker(A_k^T)=span(w). Its orthogonal data projector is P=I-ww^T/(2k). At k=3 the full datum is (3,1,1,3,1,1); the projected minimizers are all real multiples of w, each with zero backprojection. The rank-deficient variant is correctly separated from the full-row-rank formula in the frozen proof.

## Source hypotheses and interpretation limits

I independently retrieved the official report and [v3 author paper](https://arxiv.org/pdf/1807.09196v3). Their SHA-256 hashes match the frozen source gate. I inspected the whole relevant report contribution and visually checked printed p258, plus v3 pp2-3 containing the sign convention and scalar example. The pinned [catalogue dataset](https://huggingface.co/datasets/ulamai/UnsolvedMath/blob/372682f27c1b0d3d39e75fa63ad7932c7a2e1bde/problems.json) gives exactly the minimized objective and recovery rule treated here. Its status labels were not used as mathematical evidence.

The [original OWR report](https://content.ems.press/assets/public/full-texts/serials/owr/16/1/16766/online/10.4171-owr-2019-4.pdf), printed p258, displays full row rank, an informal undersampling condition, the objective F, and recovery from an optimal multiplier. Its experiment models include row and column sums. Conjecture 1 uses the broader phrase “dual approach.” The later paper expressly sets sign(0)=0, identifies the scalar zero-minimizer obstruction, and discusses approximate signs and smoothing. Thus the **literal displayed exact rule is refuted**, but a universal interpretation of “dual approach” encompassing such algorithms is not settled. No historical priority claim is certified.

The construction is a discrete pixel model, exactly as in the source. It has a piecewise-constant continuum line-integral realization. It does **not** prove that unrestricted binary functions in the plane, with finitely many ray integrals, have the same two-element solution set or fixed regions; such a continuum reformulation has a different domain.

No assumption about positive objective curvature, duality gap, random imaging, generic data, or interior/non-saturated gray patterns is needed. The report does not impose a restriction excluding saturated rays or the two-direction subclass. The original grey-value description allows binary images; the displayed sign formula corresponds to the normalized +/-1 case used here.

## Negative controls and exact gaps

1. Complementing the 3-by-3 example gives five fixed negative pixels. A mixed-sign two-solution example with datum (3,-1,-1,-1,1) has common image (1,1,1,-1,0,0,-1,0,0). Therefore neither treating the intersection as foreground-only nor replacing sign(0) by a constant yields a general repair.
2. The 2-by-2 zero-margin checkerboard fiber has no common coordinate. The exact zero output is correct there, confirming the precise “if and only if no common coordinate” scope.
3. For A=(1), y=2 is outside the box image; F(1)<F(0). The noiseless-box hypothesis cannot be discarded. For y=1/2, zero remains optimal but there is no binary preimage; common-coordinate statements require a nonempty binary fiber.
4. Both u=epsilon and u=-epsilon approach the scalar optimum u=0 at y=1. Their exact gaps are epsilon^2/2 and 2epsilon+epsilon^2/2, respectively, but their signs disagree. Objective convergence alone cannot specify numerical sign selection.
5. With 3-by-3 row and column sums all equal to -1, the binary solutions are the six one-foreground-pixel-per-row/column images. They have no common coordinate. Their common vector is zero and is **not** data-feasible. The auxiliary box vector z=(-1/3,...,-1/3) is data-feasible, but sign(z) is the all-negative image and is not data-feasible. Thus one cannot silently repair recovery by choosing an arbitrary feasible box/subgradient variable or by claiming the common vector is always such a variable. The supplied existing audit only makes that compatibility assertion for its explicit checked fibers, so this control identifies no error in its stated scope.
6. Orthogonal data noise along w is removed by P. This behavior belongs to the projected formulation; it should not be confused with an exact binary datum for the full raw measurement vector.

**Exact remaining gaps:** historical first priority; any fully specified smoothed-limit or finite-iterate sign theorem; signs of a particular auxiliary-variable algorithm; and an unrestricted continuum imaging interpretation. None is required for the exact-minimizer negative theorem. No practical algorithm failure is inferred from the zero-multiplier theorem alone.

**Repair assessment:** the literal exact question needs no repair, because the candidate answers it negatively. A fixed zero-sign convention, rank adjustment, additional redundant rays, or arbitrarily strong undersampling does not rescue a positive exact-multiplier statement. To address the broader numerical meaning of “dual approach,” an amended target must specify the algorithm, initialization, precision, threshold/stopping convention or smoothing path, and auxiliary-variable selection. This audit does not pretend that such a reformulation follows from the exact theorem; solving it would require new argument and evidence.

A set-valued sign at zero would return a set of possible pixel values, not the common-coordinate vector. A data-dependent selection from that set would require an additional selection theorem or inverse-problem computation. Merely moving the unresolved recovery task into that selection is not a repair proving a positive recovery statement.

## Independent reproducibility artifacts

`verify_independently.py` uses integer bitsets to enumerate margins, ray/cell intersections for the matrix, fraction-free Bareiss determinants for rank certificates, and rational arithmetic for objective identities. It imports or replays no supplied code and uses explicit checks that remain active under optimized Python.

- 66,064 binary images fully enumerated: sizes 2, 3, and 4.
- All data fibers constructed: 15, 328, and 16,145, respectively.
- Singleton-fiber counts: 14, 230, and 6,902.
- Fibers with a fixed coordinate, hence failed exact common recovery: 14, 308, and 15,074.
- 4,550 exact box-objective identities and 729 projected-objective identities.
- Exact family geometry, data, common count, and Gram determinant checks for k=2,...,16 and k=31.
- Complemented, mixed-sign, non-binary-feasible, outside-box, no-common, auxiliary-variable, orthogonal-noise, and pixel-length-scaling controls.

`verification_results.json` records deterministic results. `RESEARCH_LOG.md` records timestamps and checkpoint completion estimates. `SOURCE_PROVENANCE.json` binds the original-source reading to hashes and URLs. `MANIFEST.json` binds the authored review and verifier artifacts to the frozen input hashes. Downloaded PDFs, extracted text, the selected catalogue record, and screenshots in ignored `source_reading/` are local reading copies and must be excluded from any publication package.

Normal and optimized Python executions produced byte-identical results; their SHA-256 and the active-check confirmation appear in `REPRODUCTION_RECEIPT.json`.
