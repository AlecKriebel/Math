# Independent adversarial disposition review of PR117

**Verdict: PASS for the proposed `already_solved` priority disposition and closure without merging or a new solution publication.** The candidate's counterexample is correct, but the same ideal and failure of the same existential singleton-augmented-image condition are explicit in Takagi's published 2013 Example 4.4. I found no substantive new target resolution or reasonable repair that makes this a novel solution of the original open problem. This is a priority finding, not a mathematical invalidity finding.

The incoming head is `8163ee0dc7a0f944570925984cef2dc0fb291ad8`, target `30001234` / `OWR-3471-008`. The original ledger is 1/5 and remains 1/5. This audit adds no proof-search turn and makes no Git/index/native/PR/publication mutation. Its only writes are within this dedicated audit folder. No individual was contacted.

## Independence, exact mandate, and source acquisition

I first read the complete supplied target and original candidate/source record, acquired the official primary PDFs independently, and inspected actual full-page 240 dpi pixels of all operative pages. I sealed `SOURCE_SCOPE_CHECKPOINT.md` and its JSON at `2026-10-06T19:01:04.747224+00:00` before reading either root proposal. I did not read any sibling family's report. Only after sealing did I read `ROOT_PROPOSED_DISPOSITION.md` and `PROPOSED_CLOSURE_COMMENT.md`; `DISPOSITION_INPUTS.json` records their exact bytes and hashes.

I subsequently read the complete authoritative human goal at `/Users/alec/.codex/attachments/4df73d3d-641f-4907-b9ad-c47c468f2589/goal-objective.md`. It requires literal incoming `claimed_solved`, rigorous mathematics first, then priority establishing that the original problem was genuinely open and its resolution absent from the literature; the manuscript must decisively resolve that original unsolved problem. Reasonable repairs precede closing without merging when a valid novel full resolution cannot be supported. The parent's trusted message also supplies the human steering to close as `already_solved` if there is nothing new. There is no general authorization to publish a merely qualified exposition instead. A separately authorized historical exception for another PR is immaterial here.

The official [Takagi 2013 PDF](https://msp.org/ant/2013/7-4/ant-v7-n4-p06-s.pdf), DOI [10.2140/ant.2013.7.917](https://doi.org/10.2140/ant.2013.7.917), is 1,075,287 bytes, SHA256 `6ada6b6669124acda5bb4b0bd25a98d07b39808c07e7d41c1f0ae1ba49e085e5`. Printed pp. 937, 939, 940 were independently extracted and visually inspected. The official [OWR 2009 report](https://ems.press/content/serial-article-files/46224), DOI [10.4171/owr/2009/21](https://doi.org/10.4171/owr/2009/21), is 572,213 bytes, SHA256 `ee3b3e545a5d613abbb63e51a4d4c15224db017ae5d54887803b824ae076450b`; printed pp. 1137-1139 were independently inspected. Full source bodies, extracted text, and rendered pixels remain under ignored `private/`. No copyrighted prose is quoted in this report or checkpoint.

## Exact claim and independently checkable bridge

Question 8 on OWR printed p. 1139 asks whether the hypothesis of Proposition 5 (pp. 1137-1138) always holds for a monomial-free binomial ideal with minimal binomial generators. In precise notation the claim is

```
exists z in F such that for every z' in F with z' != z, A*z' != A*z,
```

where `F` is the rational optimal set of `max sum(mu_i+nu_i)` subject to nonnegative rational variables and all augmented inequalities `A*z<=1`. It is a singleton fiber of one optimizer; it is not uniqueness of the optimal image vector and not merely nonuniqueness of the optimizer.

Let the candidate's generators be

```
f1 = x1*y2 - x2*y1,
f2 = x2*y3 - x3*y2,
f3 = x3*y1 - x1*y3.
```

In the 2013 example the third generator is `g3=-f3=x1*y3-x3*y1`. The published term coordinates are paired within each polynomial, while the candidate's coordinates are blocked. In row order `(x1,x2,x3,y1,y2,y3)`, set `q=(q11,q12,q21,q22,q31,q32)`. The source augmented matrix reconstructed from those exact six terms is

```
B = [1 0 0 0 1 0
     0 1 1 0 0 0
     0 0 0 1 0 1
     0 1 0 0 0 1
     1 0 0 1 0 0
     0 0 1 0 1 0
     1 1 0 0 0 0
     0 0 1 1 0 0
     0 0 0 0 1 1].
```

For `z=(mu1,mu2,mu3,nu1,nu2,nu3)`, define

```
q=P*z=(mu1,nu1,mu2,nu2,nu3,mu3).
```

The zero-based permutation is `(0,3,1,4,5,2)`. Direct multiplication gives

```
B*P = A = [1 0 0 0 0 1
           0 1 0 1 0 0
           0 0 1 0 1 0
           0 0 1 1 0 0
           1 0 0 0 1 0
           0 1 0 0 0 1
           1 0 0 1 0 0
           0 1 0 0 1 0
           0 0 1 0 0 1].
```

This bijection preserves all nine image coordinates, every inequality, the objective, rationality, optimality, and singleton-fiber cardinality. The third-pair swap is essential; simply interleaving without that swap is false.

Here is an unrestricted independent proof, so the conclusion does not rely on a remembered threshold formula or finite sampling. The three last rows give objective at most 3. For every rational `t` in `[0,1]`,

```
z(t)=(t,t,t,1-t,1-t,1-t),
q(t)=(t,1-t,t,1-t,1-t,t),
A*z(t)=B*q(t)=1_9,
sum(z(t))=sum(q(t))=3.
```

Conversely, an optimizer must saturate all three last rows, so `nu_i=1-mu_i`. The first three rows of `A` then imply `mu1<=mu3`, `mu2<=mu1`, `mu3<=mu2`. These force all three to be one `t`, with `0<=t<=1` by nonnegativity. Thus the displayed segment is the entire rational optimal face. Choose the distinct rational partner `s=0` when `t!=0`, and `s=1` when `t=0`. Both endpoints and every interior optimizer have a second optimizer with the same full image. The exact existential claim fails everywhere on the face. Both matrices have rational rank 5, with candidate kernel spanned by `(1,1,1,-1,-1,-1)`.

The original question's ideal hypotheses also hold independently. Evaluation at the all-ones point kills each generator and cannot kill a nonzero scalar multiple of any monomial, proving monomial exclusion. All six monomials are distinct and degree two. The three generators are therefore linearly independent in degree two, and their classes are independent modulo the homogeneous maximal ideal times the ideal. At least three generators are needed globally and at the origin. Taking the negative of the third generator preserves this property. No primeness or regular-sequence theorem is needed for the target.

## Attempts to falsify the scope comparison

The primary 2013 matrix on printed p. 937 contains the exponent rows and a sum row for every polynomial. Remark 4.3 on printed p. 939 states rational nonnegative coordinates, nonstrict inequalities, the singleton-fiber hypothesis, and one ambient equation. Example 4.4 on printed p. 940 uses affine six-space, those same minors, and explicitly records failure of the condition and optimum 3. This published statement supplies the prior negative answer directly. [Primary operative pages](https://msp.org/ant/2013/7-4/ant-v7-n4-p06-s.pdf).

| Challenge | Independent test and result |
| --- | --- |
| General ambient or complete-intersection restriction | `X` is the ambient affine six-space and `c=0`. The additional equality is `0=0`; it does not restrict `Z` to a complete intersection. All three minors define `Z`. With `c=1`, the equality becomes nontrivial and the objective changes to only four term coordinates, bounded by 2. That is a different problem. |
| Other assumptions of the remark | Affine space is smooth, normal, and a complete intersection with no equations, and is log canonical at the origin. A failure cannot be blamed on a singular ambient variety. |
| Generic coefficients from Theorem 4.1 | Remark 4.3 does not retain algebraic independence of coefficients. Its actual coefficients may be `+1,-1`; importing the preceding theorem's extra coefficient hypothesis would contradict the example's stated role. |
| Local versus polynomial-ring ideal | The pure LP adds no local constraints. The homogeneous minimality argument remains valid at the origin, so localization does not remove a generator. |
| Strict or positive substitutes | Replacing `<=` by `<` removes all optimal points, yielding an unattained supremum 3; replacing `>=0` by `>0` incorrectly deletes rational endpoints. Neither is the printed LP. |
| Sign reversal versus internal sign change | Multiplication by `-1` is valid and swaps term columns. Replacing `x1*y3-x3*y1` by `x1*y3+x3*y1` is different: `y2*(x1*y3+x3*y1)-y3*f1-y1*f2=2*x3*y1*y2`. In characteristic zero the altered ideal contains a monomial. This meaningful sign mutant is rejected. |
| Paired/blocked order | Omitting the third swap or using the identity conversion fails exact column equality and makes a segment endpoint infeasible. Midpoint-only testing would miss the last-pair error. |
| Exponent-only image | All nine rows are retained. For this example dropping the last rows can conceal an error because the same optimum remains; the one-generator diagnostic `x1-x2` separates the programs: exponent caps allow objective 2, the generator cap bounds it by 1. |
| Quantifier weakening | A collision between two optimal solutions alone does not prove that every optimizer lacks a singleton fiber. For the simplex `x+y+z=1`, projection `(x+y,z)` has a collision between `(1,0,0)` and `(0,1,0)` but a singleton fiber over `(0,1)`. Our complete-face proof avoids this error. |

## Chronology and mathematical materiality

The 2009 source posed the question. The journal cover and first article page identify the exact checked source as 2013, which precedes the original candidate's ledger date `2026-09-30`. The supplied catalog's August 2026 open-status triage missed that explicit prior. The candidate's September 2026 bounded literature search also missed it; its own text correctly did not assert novelty. I verified the published-2013 chronology, not the earliest discovery date. An article's received/revised/accepted dates alone cannot authenticate the contents of an earlier version; I do not infer a 2011 priority claim from them or rely on the parent's separately authenticated earlier version.

I challenged the proposed no-novel-full-resolution conclusion by examining the strongest content added in the candidate: full rational-face parametrization, constant full augmented image, rank/kernel, elementary monomial exclusion/minimality/primeness proofs, and reproducible exact checks. The full-face formula is mathematically finer detail than the printed example's short threshold-based explanation, and I do not claim to have proved that its exact phrasing or all its checks had previously been printed. It nevertheless explains the same published counterexample to the same target. It adds no new class of ideals, new obstruction theorem, new repaired threshold theorem, or answer to a remaining case. Primeness is classical and unnecessary here. New code or exposition does not establish a new negative answer.

Reasonable repair consists of correcting attribution/current assessment and preserving the valid exposition and explicit-exception diagnostics as audit material. A guard repair changes reliability of verification, not the theorem's priority. These repairs cannot make the original problem genuinely open in 2026 or its negative answer absent from the literature. A newly generalized claim would be a new target and is outside the original 1/5 ledger and this validation-only task. Under the actual human goal, there is no supported new solution manuscript or publication package for this PR.

## Verification receipts, failures, and exact remaining gaps

`verify_bridge.py` uses only standard-library exact fractions and explicit exception guards, with no bare `assert`. `run_checks.py` ran the specified Python 3.14 executable with `-E -S -B -P`, in the exact clean environment requested. Both normal and `-O` baselines exit 0 and produce identical mathematical results. They examine 5,005 active bases, of which 1,792 are nonsingular, obtain 15 feasible vertices and precisely two optimal vertices, and check 495 rational segment/partner controls. The symbolic proof above establishes all parameters; sampling does not establish the theorem.

Eight injected mutations each actually exit 2 in both modes: omitted third-pair swap, paired/blocked confusion, internal plus sign, ambient `c=1`, strict inequalities, dropped generator rows, redundant fourth generator, and positivity substitution. Sixteen expected failed processes are preserved as stdout/stderr files with byte/hash pins and full process receipts. No unexpected test failure occurred. The source acquisition and rendering processes all exit 0.

Diagnostic failures are also retained honestly: an initial read-only file probe found no `AGENTS.md` at the nested checkout root (the supplied repository-root policy was read); the web tool could not open the official XHTML article page or DOI landing URL. Neither probe supported a mathematical or chronology claim. The independently downloaded official PDF succeeded and is the primary evidence. These tool-level diagnostics appear in `DIAGNOSTIC_EVENTS.json` with their scope; they are not misrepresented as successful process receipts.

No mathematical or exact-prior gap remains for this disposition. The exact earliest priority date and independent priority of the unprinted full-face exposition are not established by this audit, and neither gap can rescue novelty of the original negative answer. Root alone must authenticate integration records and execute any permitted native assessment, comment, or PR closure; this report performs none of those actions and is not their receipt.

## Mandatory findings

1. The original result passes the exact mathematical target; do not label it an invalid proof or conflate failed novelty with failed mathematics.
2. The exact target is already answered negatively by the checked published 2013 source, with the monomial-free and minimal-generator restrictions verified here. Record `already_solved` for the new additive assessment.
3. No substantive novel full resolution or permissible exposition-only publication route is established under the actual human standard. Close without merging or publishing a new solution paper, after the root's authorized recordkeeping.
4. Preserve the immutable original candidate, source/prior pair, historical review, and 1/5 ledger. Apply attribution/status/guard clarification additively; do not rewrite historical assertions as though the prior had originally been found.
5. Use the explicit coordinate/sign/ambient bridge in the explanation. The proposed detailed closure comment already contains this essential scope comparison and is accurate; no blocking correction to it was found. Its action sentence belongs with actual execution, not with an unexecuted receipt.

Final adversarial disposition-review completion estimate: 100%. Novel complete target-resolution estimate for this construction: 0%. This percentage concerns discovery of a new answer to the original problem, not the correctness of the counterexample, which passes.
