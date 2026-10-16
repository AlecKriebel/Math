# Independent whole-package adversarial preflight03

Review completed 2026-10-14 UTC. Review completion estimate: 100%. Best-guess progress toward an apparent-new, submission-ready original-target resolution: 70%, provisional and permitted to decrease when the three unread material sources become available. This percentage is a workflow judgment, not a probability of mathematical correctness or originality.

**Overall HOLD.** The mathematical proof and portable frozen verification package pass this review within the stated classical premises. The frozen deposit description needs a source-gap repair. The three material complete-source comparisons remain missing, so this review grants neither apparent-new-resolution acceptance nor publication clearance. No formal proof-assistant certification or human peer review is asserted.

## Frozen objects and review independence

| Object | Exact SHA-256 |
|---|---|
| Five-page PDF | `134c3e24a4a2d1db58a2f9744477491e05b0bc14297b3e23621138c00a22ecbc` |
| Verification ZIP | `1115899b96895d6e3a06eee1d42fd621450518b5e282f3d6898fdf76cac80be3` |
| Archive producer | `5e6a400191a77597e5a1858f26270c7e7960d9738fd651d76c4408012134519a` |
| Current TeX | `c46d521e893a46466cf26b50c54294d1923e93dad4076e4b5dfa16c52d42830a` |
| Historical primary comparison baseline | `eaf22e2617d2dbbe240b4adc7661801cff2cfa3751ba834379002789c4e7eb83` |

I read AGENTS.md, the complete current manuscript, the original candidate proof, the exact Hayman–Lingham question, and Duren's relevant classical geometry before reading older review conclusions. `INDEPENDENCE_AND_INPUTS.json` preserves that order and dated input hashes. The original target page was also inspected visually. Current source-attribution claims were then tested against the archived new comparisons, priority10's complete-primary adjudication, and selected primary passages at the highest-risk distinctions. I do not reissue seven fresh complete-text exclusion certifications: priority10's separately sealed sixty-body-page review is the package's evidence for that task. In particular this package review does not replace any of the three missing full texts.

All authored work and scratch mutations stayed in this review folder. I did not change canonical files, the Git index/branch/remotes, or contact any individual or other source reviewer. The observed branch is main. Root was promptly informed of the actionable metadata issue and test results.

## Mathematical adversarial review

The exact hypothesis tested is that every full-S global maximizer of the real part of `a2+i*10^-24(a4-3a3)` has nonmonotone continuous polar argument, signed outward radial angle, and ordinary unsigned outward radial angle on its actual omitted arc. The statement is stronger than the existential counterexample needed for Problem 6.72, but its quantifier is supported by uniform estimates. The book asks both target questions; tangent direction alone is not one of them. Its 2018 no-progress update is not evidence of continued openness in 2026.

The topology and functional hypotheses are appropriate. Cauchy's coefficient maps are continuous complex-linear maps on H(D); normal-family compactness of S excludes constant limits through the derivative normalization. Re L takes values 2 and 0 at Koebe and identity, respectively, so each attained maximizer meets the support theorem's nonconstancy condition. Coefficient bounds are invoked as classical inputs, not inferred from finite controls. The proof does not optimize within a smaller coefficient slice or select one differentiable maximizing branch.

The coefficient and area estimates have the right direction and sufficient margins. Comparing with Koebe gives Re a2 >= 2-13 epsilon, |a2-2|^2 <= 52 epsilon, and area defect at most 13 epsilon. The odd-root transform is analytic and univalent because f(z)/z is nonvanishing and the normalized odd root distinguishes the opposite inputs. Its exterior coefficients give the a3 bound and weighted H tail. The tail and derivative sums are bounded by 16/135 < 1/4 and 56/25 < 9/4. No boundary convergence of f or continuity of slit tips is being presumed.

The actual-tip step survives a deliberately skeptical check of the conformal-radius inequality. An inscribed disk maps under the normalized inverse into D, so Schwarz's lemma gives distance <= conformal radius, not its reverse. At z*=-2/3 the reciprocal-square error is (28/15) eta after multiplication by |z*|, below 2 eta. The two derivative contributions fit below 6 eta and 2 eta. Thus the actual omitted tip has modulus below 7/25+7 eta < 3/10. The closed omitted arc is the full complement, hence the boundary is available to the distance estimate; increasing modulus makes its minimum the tip. This is a bound on the actual tip rather than a formal Schiffer zero.

Independent coefficient extraction has the prescribed signs:

    Phi(w) = -a/w - b/w^2 - c/w^3,
    a = 1+i epsilon(2a3+a2^2-6a2),
    b = i epsilon(3a2-3), c = i epsilon.

The substitution w=-v^-2 gives 4(a-bv^2+cv^4)dv^2. The support-slit equation uses Duren's positive convention. Rationality here concerns the functional/Phi and cannot make the extremal map rational. The near-identity square-root primitive is analytic on a neighborhood of |v|<=3; Rouché applies to G(v)-t for |t|<2 with a margin of at least 1. Nonzero G' patches the unique roots into the holomorphic odd inverse. Neither a numerical solver nor a converse sufficiency theorem for arbitrary trajectories is used.

Actual slit membership is proved, not transferred to another unsupported extremality claim. On the lifted actual tail, positivity of 4P(v)dv^2 makes Im G constant and its limit zero. The two real rays are the same projected w-arc by oddness. The membership set is relatively closed because the omitted complement is closed. Local uniqueness at regular nonzero Q points makes it relatively open. Throughout the entire selected segment |W|>25/81, while the actual tip has modulus <3/10; the quantitative separating gap is 7/810. Consequently no continuation can stop at the finite tip. Formal nonvanishing alone would have been insufficient and is not the mechanism used. The cover has no zero V(t) for t>0 and no projected self-intersection, since equality requires inverse coordinates t1=±t2.

The orientation proof is independent of the fine endpoint expansion: |Z-1|<=222 epsilon/(1-111 epsilon)<223 epsilon, where Z=tV'/V. Therefore Re Z>0 on the entire tail and segment. Increasing t moves inward, and -W' is the outward tangent. This avoids silently confusing the tangent orientation or radius ordering.

The analytic remainder constants check. The square-root coefficient uncertainty costs 161 epsilon eta and its quadratic remainder can be absorbed into the next epsilon eta; integration produces 486, inversion adds at most 18315 epsilon^2, and the derivative expansion adds 45621 epsilon^2 in total. Exact rational margins establish all absorptions for the specified epsilon. Subtraction before division yields the stated 1541 epsilon eta+4662 epsilon^2 bound, below 2000 epsilon eta. The endpoint values 3/5 and -441/640 exceed opposite epsilon/2 sign margins after their errors. These calculations are quantitative analytic deductions supported by finite rational arithmetic, not a scan, floating-point plot, or a claim of formalization.

For a continuous lift of polar argument, theta_t=-2 Im Z/t has both derivative signs at regular points. The signed radial angle beta=arg Z uses the fixed small branch, tends to zero at infinity, and has opposite signs at the two interior witnesses. That limit excludes either monotone direction. Unsigned |beta| is positive at both witnesses and vanishes between them, excluding monotonicity even on the compact subarc. An inward tangent gives the supplement pi-|beta|; an acute tangent-line angle gives |beta|. Neither convention repairs monotonicity. Argument lifts differ only by an additive multiple of 2pi and do not change the conclusion. At epsilon=0 the strict witnesses disappear, and a shortened segment with both endpoints before sqrt(5/2) does not by itself witness a reversal. These are checked negative controls, not extensions of the theorem.

I found no required mathematical repair, circularity, hidden optimizing assumption, or target-angle mismatch. The remaining analytic assumptions are the explicitly invoked classical compactness, coefficient, exterior area, and support-slit theorems. Their full historical proofs have not all been independently re-proved here.

## Source scope and priority framing

The current attribution credits the classical framework and distinguishes the relevant source mechanisms correctly. Zemyan2003's actual Brown evaluation extremizer has tangent wavering while its primary p.792 retains polar and radial-angle monotonicity. Zemyan2005/2007's hypothetical wiggle bounds, eventual sign stability, and Koebe/Pearce examples are different claims. A count bound is not an actual support construction with a target reversal. Duren–Leung–Schiffer1983 and Zhang–Ma1991 address saturation of the finite-tip angle; they do not impose global interior monotonicity. Brickman1984 classifies rational-type functionals and truncation, while Goh1994's rigidities assume rational f or two independently maximized derivative functionals. Maximizing one sum does not maximize its summands separately. None of the disputed source-local derivative/elimination/count steps is a premise of the current proof, and the package does not incorrectly label auxiliary diagnostics as support-realizable counterexamples or theorem refutations.

The current manuscript says only that no earlier negative answer was verified in the inspected corpus. It does not assert historical firstness, newness of the classical method, or an open status in 2026. Older sealed status statements and unread-source lists are historical and are reconciled by CURRENT_PRIORITY_ASSESSMENT.json. The historical source06..10 manuscript inputs have hash eaf22e..., matching the archived baseline rather than the newly edited attribution. The first 12056 bytes, including the proof, match the current TeX exactly before the unique attribution-section marker. My independent mapping tests reject a changed epsilon in the baseline and a changed attribution boundary. Hashes attest consistency, not authorship, truth, novelty, or access to an unread source.

The three material gaps remain affirmative obligations for apparent-new original-target/publication acceptance:

1. Duren2014 commentary, DOI 10.1007/978-1-4614-7949-9_22: a later author retrospective whose prose may contain relevant attribution or constructions; metadata/bibliography and the older DLS article cannot replace it.
2. Goh1992 journal article, DOI 10.1080/17476939208814600: directly relevant coefficient-functional geometry, with intermediate examples/remarks unread; Goh1994 and the 1992 thesis are different sources.
3. Hibschweiler1995, HJM21(1), pp95-102: directly relevant eventual polar/radial and support geometry; tail monotonicity permits a bounded reversal but does not exclude further constructions in the uninspected complete paper.

Haario and the subsidiary citation trails remain disclosed leads. They are neither declared harmless from titles nor promoted to equal blockers without a concrete target-specific mechanism. No conclusion of novelty is drawn from the absence of a verified collision. Outside expertise could improve confidence, but this review does not prepare or initiate outreach under the independent-research policy.

## Actionable finding

**F1 — Repair the deposit description before the next accepted freeze.** `publication/zenodo-deposit.json`, copied to archive `metadata.json`, currently says the 2014 Duren commentary and Goh1992 remain material uninspected comparisons, but omits Hibschweiler1995. The manuscript, README, CORRECTIONS and CURRENT_PRIORITY_ASSESSMENT name all three. Add Hibschweiler1995 to the material-gap sentence and make the preparation/publication-HOLD status explicit in the description. The omission does not break the mathematics or offline jobs, but it makes the outward-facing metadata an incomplete statement of the current clearance limits. Root acknowledged the repair and kept the current frozen objects unchanged during this review.

No other mandatory repair was identified. The changed metadata will change the archive digest and must receive a new exact freeze and fresh acceptance review; this report certifies only its listed frozen objects. A repair cannot close any unread-source gap by itself.

## Reproduction, archive custody, and PDF

I extracted the ZIP into an empty scratch destination, created a fresh virtual environment, and installed the pinned mpmath1.4.1 package. This environment uses Python3.14.6; I did not run a multi-version Python matrix. Two complete independent replay runs each passed all15 jobs, verified 220 outer payloads and 140 inner entries, and preserved every sealed payload. Fourteen inner seals include the source06 `authored_outputs` schema and the hidden `.gitignore` payloads. Full five-family wrapper records correspond exactly to their original mathematical records. Only the explicitly registered source-bridge timestamp is normalized; mathematical values, interval records, evidence fields, and limits are compared.

The 54-check independent script tests changed mathematical detail for each of the five new families while preserving the reported counts and retargeting the outer digest to let replay comparison, rather than the first hash gate, reject it. It also tests a missing interval field, a source06 hidden sealed payload removed from the outer inventory, a missing new registered seal, absent mpmath in another fresh venv, wrong reported dependency version, and both -O and PYTHONOPTIMIZE. Every expected rejection occurs. Baseline/attribution mutation controls are independent review checks, not a claim that the offline runner semantically parses LaTeX.

The archive has exactly221 unique safe relative paths, with no symlinks. Its authored JSON/Markdown/Python/TeX content and inventories contain no third-party fulltexts, PDF payloads, image/cache/venv files, or account data. A content screen's two matches were reviewed and were benign: the human source authorization statement and a Python test for an HTML magic string. Source PDFs and institutional-download wrappers are local raw custody artifacts outside the ZIP. Optional custody helpers are not among the offline jobs and openly depend on external PDFs/historical inputs; the README's disclosure accurately limits their portability. Historical fulltext digests are not passed off as revalidated fresh copies.

The frozen producer was copied, with its audit inputs, into this review's cache and run there. It generated a byte-identical ZIP with the expected producer digest, 431526 bytes, 221 members/220 payloads/140 inner entries. Tectonic0.16.9, under SOURCE_DATE_EPOCH1791892800, regenerated the PDF in a separate output directory byte-identically: 86600 bytes and five pages. No canonical artifact was rebuilt in place.

Following the PDF skill, all five rendered pages were inspected. I found no clipping, overlap, missing glyphs, broken equations, unreadable references, or inappropriate page transitions. The title/author/date/ORCID are consistent, the embedded title/author/subject metadata is exact, and the PDF is A4, unencrypted, and has no JavaScript or forms. The text explicitly discloses extensive AI assistance, unrefereed status, no human peer review, and CC BY4.0. The deposit author/ORCID, date, version, title, language and licence agree, subject to F1's source-gap correction. A deterministic creation timestamp is a build setting, not discovery/priority evidence.

| Component | Verdict |
|---|---|
| Exact target and full-S quantifiers | PASS |
| Mathematical argument under stated classical inputs | PASS |
| Actual omitted-slit membership, orientation, limiting cases | PASS |
| Five-page PDF layout and exact rebuild | PASS |
| Offline reproduction and archive integrity | PASS |
| Attribution and bounded-source framing in manuscript | PASS WITH EXPLICIT SOURCE HOLD |
| Deposit metadata completeness | NEEDS REPAIR F1 |
| Historical-first/apparent-new resolution | NOT CERTIFIED |
| Submission/publication acceptance | HOLD |

The strongest verified result is a technically sound, reproducible preparation draft proving the target failures on every actual maximizing slit, within its explicit classical premises. The exact remaining gaps are F1 and the three material complete-source comparisons, followed by review of the repaired freeze. No submission, DOI, tracker change, release, merge, or external communication is authorized or performed by this report.
