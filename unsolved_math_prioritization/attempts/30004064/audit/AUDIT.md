# Independent adversarial audit: binary-tomography exact dual recovery

Problem **30004064 / OWR-16766-003**, rank 550. Reviewed 2026-10-04.

## Verdict

**PASS, for the literal exact-minimizer formulation stated in the catalogue and analyzed in the frozen package.** Both recovery assertions in that formulation are false. No mathematical correction to the frozen proof is required.

The decisive fact is that, whenever the datum has a preimage in the box [-1,1]^N, the displayed unprojected objective has unique minimizer zero. The supplied full-row-rank row/column example really has exactly two binary solutions and five common pixels. The sign of the exact back-projected minimizer loses all five.

This verdict is deliberately narrower than a claim that every possible meaning of the authors' numerical "dual approach" has been disproved. The full paper already recognizes the scalar zero-minimizer obstruction and discusses other ways to select or recover image information. The frozen package makes that distinction adequately and disclaims novelty. Its scoped description is suitable for publication; an unqualified claim to have disproved the empirical algorithms or achieved a new binary-tomography breakthrough would not be supported by this audit.

The review was independent of the candidate's construction. The frozen files were read and replayed without modification. No remote publication or repository mutation was performed.

## 1. Precisely what was audited

The frozen manifest SHA-256 is:

`22b5cbbe1abebdfc10e068cf433382bb3b802b22376d9e8bfb17e5fcae73af0d`

All six authored files listed by that manifest match both their recorded sizes and SHA-256 hashes. The manifest itself matches the supplied hash.

The catalogue's clean statement expressly selects an exact minimizer mu* of

\[
F_y(\mu)=\tfrac12\|\mu-y\|^2+\|A^T\mu\|_1
\]

and asks whether sign(A^T mu*) recovers the unique binary image or the coordinates common to all binary solutions. This is not merely an inference from the problem title.

The relevant catalogue record was independently matched to the record in the public dataset at revision `372682f27c1b0d3d39e75fa63ad7932c7a2e1bde`. The dataset file SHA-256 is `37067f43734b76ee886b032469836767c34d892de14397ce6aa71da01500e252`, matching its pinned LFS object metadata. The locally supplied record bytes have SHA-256 `28829ea1f1382b9ca371f8988008c2d029c71623c6492154bde0f4150af6d96b`. The dataset's status labels were not used as proof of mathematical openness or correctness. [Pinned catalogue source](https://huggingface.co/datasets/ulamai/UnsolvedMath/blob/372682f27c1b0d3d39e75fa63ad7932c7a2e1bde/problems.json).

## 2. Primary-source reconciliation and the strongest interpretation objection

The complete contribution on printed pp. 256-259 of Oberwolfach Report 4/2019 was inspected. The crucial p. 258 was also checked visually. Its Theorem 1 displays the same unprojected objective under full row rank and explicitly retrieves the image by taking the sign of the exact back-projected optimizer. Conjecture 1 then gives the unique-solution and common-intersection claims for noiseless data. Thus the exact-recovery rule is present in the primary report, not invented by the candidate. [Publisher report](https://content.ems.press/assets/public/full-texts/serials/owr/16/1/16766/online/10.4171-owr-2019-4.pdf), [DOI](https://doi.org/10.4171/OWR/2019/4).

However, Conjecture 1 uses the broader phrase "dual approach," and the surrounding motivation is numerical. The full arXiv v3 manuscript was inspected, especially Sections II-IV, VI, and Appendix A; p. 3 was also checked visually. It contains all of the following distinctions:

- Section II adopts sign(0)=0. The numerical discussion uses zeros as undetermined pixels.
- Section II-A, equations (10)-(11), gives the scalar optimizer by soft-thresholding. At the noiseless endpoints y=+1 and y=-1 it is zero. That section also says that zero coordinates require other means of determining the image and discusses useful signs of approximate iterates.
- Section II-B, Corollary 1 and Remark 2, gives the projected and full-row-rank objectives, respectively. These match the two objectives handled in the candidate.
- Section II-C discusses smoothing the one-norm, which changes the optimization problem, and numerical iterative approaches.
- Section III introduces z in the subdifferential of the one-norm at A^T mu. Algorithm 2 returns sign(z^T), not sign(A^T mu*).
- Section IV explicitly describes approximate CVX output and thresholding. Its experiments do not evaluate an exact zero optimizer's sign.

These source facts make it essential to distinguish the exact formula from algorithmic recovery. The candidate already does so in its opening scope, interpretation section, conclusion, README, and source gate. Therefore the audit accepts the claimed literal result and rejects any broader inference about all numerical implementations. [arXiv v3](https://arxiv.org/abs/1807.09196v3), [full manuscript](https://arxiv.org/pdf/1807.09196v3).

For additional precision, at mu*=0 the auxiliary optimality conditions can be satisfied by any z in [-1,1]^N with Az=y. In the two-solution example the common-coordinate vector itself is such a z. Consequently there is no contradiction between a zero multiplier and a useful auxiliary reconstruction. This is a concrete reason, rather than merely a disclaimer, for the stated boundary.

Source integrity was checked independently: the report PDF has SHA-256 `8d9d44137ed3246a1e5819e6518d4c4033c35188df351a0963fa0c3e8951ec2f`; the arXiv v3 PDF has SHA-256 `e65aa0919a97a9e1634b2a14c8dfe56d8c92d009e853321b02d6a1bc5feea4ac`, equal to the supplied CWI manuscript bytes.

## 3. Independent mathematical check

For any s in [-1,1]^N and y=As, expand the square:

\[
F_y(\mu)-F_y(0)
=\tfrac12\|\mu\|^2-\langle s,A^T\mu\rangle+\|A^T\mu\|_1
\geq\tfrac12\|\mu\|^2.
\]

Each scalar inequality is simply s_j q_j <= |q_j|. The inequality is strict for every nonzero mu because the Euclidean quadratic is positive. Hence zero is the unique global minimizer; no existence theorem, rank assumption, solver property, or unverified source theorem is needed.

Equivalently, zero satisfies the subgradient condition because y=As belongs to A[-1,1]^N, and the quadratic makes the objective strongly convex. This independently confirms the calculation but is not needed for the proof.

For the projected objective with P=AA-dagger, y belongs to range(A), so Py=y and A^T P=A^T. Expansion gives

\[
G_y(\mu)-G_y(0)
\geq\tfrac12\|P\mu\|^2.
\]

Every minimizer therefore has P mu=0. Conversely, P mu=0 implies A^T mu=0 and equality. Thus the minimizer set is exactly ker(A^T), and every minimizer has zero back-projection. The projected and unprojected claims were not conflated.

The genuine binary least-squares Lagrangian also has zero primal and dual values when binary-feasible data are present. The candidate's zero-gap argument is valid. It does not establish image recovery: at zero multiplier every binary vector minimizes the multiplier's binary term, while the data-feasibility condition still has to be imposed. The source's auxiliary sign-variable formulation also admits zero entries, but that does not invalidate this independently formulated binary argument or the exact-objective result.

## 4. Counterexample stress tests

**Tomographic geometry and rank.** The displayed 5-by-9 matrix really measures three horizontal lines and two vertical lines. The third vertical sum is a linear combination of those five sums. Its removal preserves the data fiber. Inspecting the omitted column first proves row rank 5 exactly. With all six lines retained, the rank-deficient projected formulation still fails in the same way.

**Exhaustiveness of the two solutions.** A row sum of 3 forces the first row to +1, and a column sum of 3 forces the first column to +1. The residual 2-by-2 block has row and column sums zero and must be a checkerboard with one free sign. There are exactly two choices. Five entries are shared and four vary. This is a proof of exhaustiveness, not a conclusion drawn only from enumeration.

**Meaning of intersection and both pixel signs.** The candidate defines a common-coordinate vector, retaining either common sign and using zero only for variation. This agrees with the paper's common-pixel interpretation. The positive shared pixels already refute recovery. The independent tests also checked the complemented example, with five fixed negative pixels, and a mixed-sign example with datum (3,-1,-1,-1,1). Its common-coordinate image is

\[
\begin{pmatrix}1&1&1\\-1&0&0\\-1&0&0\end{pmatrix}.
\]

It also has exactly two binary solutions. Thus neither a foreground-only misunderstanding nor a fixed alternative value assigned to sign(0) rescues universal recovery. A separate mixed-sign uniquely determined 2-by-2 image confirms the latter point for the unique-solution clause. A set-valued sign convention would change the question and require a further selection rule; it is not the convention used in the source or candidate.

**Strong undersampling.** The k-by-k extension is valid for every k>=3: all but the bottom-right 2-by-2 block are forced by saturated row or column sums, leaving exactly two checkerboards. Its measurement matrix has 2k-1 independent rows, so the measurement/pixel ratio tends to zero. The report's informal m much smaller than n qualification cannot rule out this family.

**Finite-iterate signs.** The scalar positive and negative epsilon sequences both converge to the exact minimizer and optimum value, but have opposite signs. Hence convergence of the objective alone does not prove sign recovery. This does not show that any particular fully specified iterative rule fails, nor does it purport to.

## 5. Reproducibility checks

The supplied dependency-free verification was executed against the frozen files. Its output is byte-for-byte equal to the supplied results:

- 1,044 binary images examined
- 1,458 exact objective identities
- 729 exact projected-objective checks
- 8 exact scalar approximation checks

The independent `audit_verify.py` additionally reconstructs the matrices and fibers without importing the candidate's functions. It checks:

- all 512 binary 3-by-3 images, forming 328 distinct data fibers and 230 unique images, plus all 16 binary 2-by-2 images;
- the positive, negative, and mixed-sign two-solution fibers with five fixed coordinates;
- 1,400 exact objective identities for scalar, signed, invertible, and rank-deficient matrices, including fractional box-feasible images;
- the ranks and line-sum data of the larger family for sizes 3 through 9;
- the compatibility of the common-coordinate vector with an auxiliary box/subgradient variable.

All checks pass using only integers and rational arithmetic. The tests supplement the universally quantified proof; they do not replace it. The audit does not reproduce or certify the authors' numerical experiments, prior repository searches, or an exhaustive literature search.

## 6. Credit, publication scope, and final disposition

The scalar degeneracy is already in the cited primary paper. The frozen package gives that credit and does not claim priority. The all-noiseless-data inequality and actual line-sum example establish the complete negative answer to the precise catalogue formula without depending on a novelty claim.

No required changes were identified. Retain the exact-minimizer qualifier and the limitations already present whenever summarizing or publishing this result. Keep algorithm-specific, smoothing-limit, subgradient-selection, and historical-priority questions outside the claimed resolution unless they receive separate precise statements and proofs.

The audit files contain authored analysis, independent code, exact results, and hashes only. They include no source-paper copies, copied source code, catalogue dumps, account data, or private coordination records. `AUDIT_MANIFEST.json` binds this review and its reproducibility files to the original frozen manifest.
