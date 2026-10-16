# PR 164 literal source and exact problem-coverage audit

The independent bounded result is positive: the manuscript computes the ordinary Gerstenhaber graded Lie algebra of the intended upper triangular algebra over every field of characteristic two, including degree zero and all higher degrees, and its injective map is the gamma in the original coefficient sequence. No source-hypothesis or literal problem-coverage gap was found. This is not global novelty, priority, current-open-status, restricted-operation, or publication clearance.

Original submission: head `7c8acab3ff84c6c8caadec8998296936a156e0bd`, with directly read manuscript SHA-256 `439bb5ac541dcc7cb0e6fbf5b30a22501f23f330b4f970fe641fb54234bd46be`. The source record's literature/open-status claims were treated as hypotheses, not evidence.

## Independence and evidence

Only the original PROOF.md, source_record.json, source_manifest.json, and case ORIGINAL_FILE_MANIFEST.json were read as candidate inputs. No original independent_review file, verification.json, README, research log, candidate checker, root mathematical verdict, or other-family verdict was read. The first assessment and its seal were created at 2026-10-12T08:21:03.697542+00:00 and made read-only at mode 0444. Their original bytes and modes remain unchanged. A dated addendum corrects a subsequent publisher-date interpretation; it does not rewrite the seal.

The [OWR original](https://ems.press/content/serial-article-files/46571?nt=1), [Hermann v2](https://arxiv.org/abs/1411.0836v2), and [Xu v2](https://arxiv.org/abs/0805.3295v2) PDFs were independently obtained. All three hashes match the submitted source manifest. Relevant pages were read as extracted text and visually inspected. Bodies, acquisition headers, and renderings remain private and are excluded from the public whitelist.

SOURCE_CROSSWALK.md records exact locations for each manuscript equation or source use. SOURCE_DERIVATIONS.md gives the independent all-degree argument. The independently written source_checks.py verifies the action, opposite-algebra conversion, associativity, stratifying multiplication, and two negative controls. Ordinary and optimized Python produce identical results, and all checks use explicit exceptions rather than removable assertions.

## Corrections and qualifications

**Fixed orientation must be stated explicitly.** Hermann v2 9.6 fixes multiplication to categorical composition. From its arrow endpoints, the source category has a right A-module in the lower-left corner; the displayed upper algebra is its opposite. This is not an unspecified convention in that source. The literal same-orientation assertion of Lemma 9.7 fails: primitive right-projective dimensions are (4,3) for that category algebra and (6,1) for the upper algebra. The manuscript's existing opposite caveat protects the calculation, but its opening source explanation should state the fixed correction rather than merely saying that orientation depends on conventions. This finding does not refute the directly computed upper algebra or its bracket.

**The source squaring sentence is not a usable polynomial formula.** The ordinary cup-square interpretation of the formula printed in Hermann 9.4 fails the target-degree test from Definition 3.4 and 3.8. A degree-two class has squaring target degree three, while its nonzero polynomial cup square has degree four. The manuscript uses only the ambient ring and generator-bracket formulas, not this separate statement. No squaring or restricted-power formula is certified here.

**2015 and 2016 label different dates.** The [EMS publisher page](https://ems.press/journals/owr/articles/13681) identifies the canonical journal citation with 2015 and the actual publication date as 15 February 2016. The workshop/report is 2015. The source record's parenthetical 2016 is defensible as publication year; it is not a proven provenance error. Clear citation wording should distinguish the two dates. The immutable first assessment's premature contrary wording is expressly withdrawn in FIRST_ASSESSMENT_ADDENDUM.md.

## Exact mathematical conclusion

Write A=K[x,y]/(x^2,y^2), M=A/(y), and B=[[A,M],[0,K]]. The source permutation action is recovered by x=g+1 and y=h+1: x has rank one and square zero, while y annihilates M. The basis conversion 1 -> alpha, x -> alpha+beta proves this identification over any characteristic-two field. The trivial two-dimensional module is excluded by the independent center-dimension control (four instead of three).

The lower-right e is stratifying because eBe=K, multiplication Be tensor_K eB -> BeB is an isomorphism, and every higher Tor over K vanishes. All algebras and modules required by the source theorems are K-projective. No claim that M is A-projective is needed.

The explicit tensor resolution and derivation cup powers identify the ambient ring as R=K[x,y,u,v]/(x^2,y^2). The characteristic-map comparison with the y-periodic M-resolution proves in every degree that chi sends x to x, y and u to zero, and v to eta. Consequently chi is onto and ker chi=(y,u)R. Happel's sequence gives the positive-degree injectivity and kernel image; the center gives image K+yA in degree zero.

The normalized relative bar decomposition for E=Kf direct-sum Ke independently identifies the original coefficient gamma with the same restriction map: A-valued cochains have only an all-A input/output component. Its projection commutes with cups and every insertion on all-A inputs. Thus gamma is injective in every degree, and

HH^*(B) = L = K+(y,u)R

with inherited bracket

[F,G]=F_x G_u+F_u G_x+F_y G_v+F_v G_y.

The proof of closure, structure constants, degree-zero exception, and coefficient Ext groups is recorded in SOURCE_DERIVATIONS.md. Every coefficient and chain comparison uses only characteristic-two field identities, so the conclusion covers arbitrary, possibly infinite or nonperfect fields. Finite GF(2) checks serve as convention controls, not as a substitute for this argument.

## Literal scope and remaining gap

OWR Question 5 asks for the Lie algebra and whether its particular coefficient sequence can be used. The preceding theorem and lemma concern the cup product and Lie bracket; no divided squaring, restricted powers, or all higher brace operations are requested. Hermann's definition separately names the additional squaring structure. The manuscript's explicit limitation to ordinary graded Lie structure therefore matches the literal question. Its additional cup-product identification is supported, but a claim of the full strict Gerstenhaber structure would require more work.

The bare exact sequence of vector spaces would not determine a bracket. The computed injective compatible gamma and its precise image do determine the bracket, so the manuscript answers the original sequence question rather than replacing it with an unrelated sequence.

Strongest verified result: the complete ordinary graded Lie presentation, with the original coefficient gamma, for all characteristic-two fields and all cohomological degrees of the intended algebra. Exact mathematical coverage gap: none found in this assigned audit. Remaining editorial qualification: make the fixed opposite convention and the two date types explicit. Additional squaring/restricted structures and global priority remain unassessed. No publication clearance follows from this result.

## Scientific-repair candidate source authentication

At 2026-10-12T08:27:31.152405+00:00, after the first assessment had been sealed, the parent explicitly requested a source/provenance/scope-only check of mathematical_candidate_v1. Its PROOF.md and source_record.json match the pinned candidate manifest. Sections 2-5 independently compare byte-for-byte with the original (7964 bytes; SHA-256 e2d9fb79cd1dfeabd7f4de28622c269cd203cb12e2648d77ca8e438377e9a54f).

The corrected source paragraph now states the source's fixed composition and the required opposite precisely. Its opposite comparison is valid for cohomological cup product and bracket in characteristic two. The added source-record provenance clarification agrees with both the PDF and authenticated publisher metadata. The explicit ordinary Lie/cup scope matches the literal question. The revised diagnostic prose correctly distinguishes bounded checks from the all-degree proof; this source-only review did not read or run the repaired checker and therefore does not separately authenticate its execution.

One small wording improvement remains optional: replace the potentially ambiguous phrase about x acting regularly with “g acts regularly, so x=g-1 acts by a rank-one square-zero operator, and y=h-1 acts as zero.” The intended module is already unambiguously defined and this does not affect a mathematical conclusion. The original independent verdict remains preserved. This source repair authentication is not a priority or publication gate.
