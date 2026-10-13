# Fresh adversarial priority audit: PR 1033, problem 11000026

The submitted theorem is an elementary corollary of Lenzhen--Rafi's prior
uniform ball theorem. This audit supports an explicitly expository note,
with the attribution and bounded-search limits below. It does **not** clear
a claim of novel mathematical discovery, worldwide firstness, or present
worldwide openness of Farb's Question 3.5. I found no explicit full-scope
predecessor in the inspected primary theorem bodies; that negative finding
is distinct from the positive fact that the entire conclusion follows
straightforwardly from an existing theorem.

The correct classification is **known substantive theorem plus elementary
implicit corollary; explicit publication priority unresolved**. It would
overstate the evidence both to call this a verified first solution and to
report a located explicit prior solution to the identical theorem. The
original package already disclaims historical novelty, and nothing found
requires weakening its accepted mathematical quantifiers.

## 1. Scope, independence, and input identity

The reviewed submission is head
`6322305d37b8131f034a1b4c3c5e861e4b04844f`, comprising exactly the eight
files in `submitted/` and `SUBMITTED_PINS.json`. Initial and final hashes
also cover `ROOT_MATH_AUDIT.md` and `ROOT_MATH_ACCEPTANCE.json`. All eight
copies match their pinned SHA-256, byte counts, and the corresponding Git
objects at that head. The live shared `main` checkout was at a different
commit when the audit began; no checkout, branch, index, or Git mutation
was performed. `SUBMISSION_VERIFICATION.json` records the object checks.

I used the root records only to fix the accepted mathematical claim. I
independently derived comparisons and wrote `INDEPENDENT_COMPARISON.md`
before reading the original audit's prior-art verdict. Neither an older
PASS label nor its negative literature search was a priority premise.
No external person, other shard reviewer, PR, queue, service, release,
publication, or original submitted file was contacted or changed. All
writes are confined to this review directory. Raw third-party bodies,
extracted text, and page images remain in `sources/raw/` for private review.

The exact target is: for each fixed closed oriented genus `g >= 2`, one
finite `c_g >= 0` works for all centers `o`, all `R >= 0`, and all
`x,y` in the original closed half-log Teichmuller ball, giving an actual
continuous rectifiable path in that ball with length at most
`d_T(x,y)+4c_g`. This implies `N_g(k)=k+4c_g`, including `k=2`. The claim
does not assert numerical or genus-uniform constants, optimality within
Teichmuller space, convex balls, a thickness restriction, or another metric.

## 2. Positive prior evidence and the exact residual deduction

[Lenzhen--Rafi, JDG 88 (2011), Theorem C, printed p. 268, and Theorem 17
with its proof, pp. 284--285](https://www.math.toronto.edu/rafi/Papers/Convexity.pdf)
provide the uniform all-center/all-radius radial inequality

`d_T(o,z) <= max(d_T(o,a),d_T(o,b)) + c_S`

on the minimizing segment from `a` to `b`. Their comparison constants
depend only on the fixed topology. The extremal-length antecedent is
Theorem A's extremal-length part, stated as Theorem 15, printed p. 282.
Using Kerckhoff's formula, `c_S=(log K_S)/2` is available. The primary
pages were read and visually checked. The source states an enlarged-ball
geodesic conclusion, rather than the submitted intrinsic-ball conclusion.

The only residual argument is general metric geometry. For `R >= c_S`,
move `x` and `y` inward on radial minimizing segments by
`alpha=min(c_S,d_T(o,x))` and `beta=min(c_S,d_T(o,y))`. The new endpoints
`a,b` have radius at most `R-c_S`; the prior inequality puts their minimizing
segment in radius `R`. Concatenating radial end pieces and that segment
gives

`length = alpha+d_T(a,b)+beta <= d_T(x,y)+2alpha+2beta <= d_T(x,y)+4c_S`.

For `R<c_S`, the path through the center has length at most `2R`. Constant
segments handle zero and coincident cases. Every part uses the original
metric and original closed ball. This reconstruction is my checkable
deduction from the prior source; it is not a claim that LR wrote those
sentences or historically noticed the corollary.

Thus the all-pairs scope, original-ball containment, continuous rectifiable
paths, and additive bound are not evidence of a new Teichmuller mechanism.
They are obtained at once from the already uniform theorem. There is no
further research obstacle in the bridge and no new estimate on geodesics.
Absent an explicit prior statement, the bridge may still be useful
exposition, but missing search matches do not certify its novelty.

The source chronology is already earlier than the submitted 2026 note:
[arXiv:1002.3939v1](https://arxiv.org/abs/1002.3939v1) is recorded as
submitted February 20, 2010. In that version, Theorem C is on PDF p. 2 and
the ball theorem is body **Theorem 15**, PDF p. 16; the extremal-length
theorem is body Theorem 13. In JDG, the body ball theorem is **Theorem 17**.
The currently served v1 PDF also has an internal March 21, 2022 typesetting
date. The archive's version date, current PDF byte identity, and internal
typesetting date are recorded separately; the 2011 journal edition alone
suffices for the prior-substantive-theorem finding.

## 3. Full-body comparison matrix

| Primary item and checked body | What it establishes | Relationship to exact target |
| --- | --- | --- |
| [Farb 2006 book](https://www.math.uchicago.edu/~farb/papers/mcgbook.pdf), printed pp. 24--25, PDF pp. 31--32; complete definition and Question 3.5 | Same-sphere distance-two bounded paths inside the same radius ball; asks the Teichmuller question | Exact question and terminology antecedent. No answer in those pages. |
| [Lenzhen--Rafi JDG 2011](https://www.math.toronto.edu/rafi/Papers/Convexity.pdf), Theorems C/15/17, topology convention, and full Theorem 17 proof | One topology-only additive radial allowance for every center, radius, pair, and interior geodesic point | Decisive substantive predecessor. Full target is an elementary implicit corollary, not an explicitly located intrinsic-ball theorem. |
| [Lenzhen--Rafi archive v1](https://arxiv.org/pdf/1002.3939v1), Theorem C and complete body Theorem 15 proof | Earlier version of the same ball statement and radial inequality | Same implicit consequence; theorem numbers and archive/internal dates must not be conflated. |
| [Masur survey, SDG XIV (2009)](https://archive.intlpress.com/site/pub/files/_fulltext/journals/sdg/2009/0014/0001/SDG-2009-0014-0001-a011.pdf), printed pp. 302--303, Theorems 3.6/3.7 and surrounding text; [author copy dated January 20, 2010](https://math.uchicago.edu/~masur/chapter3.pdf), PDF pp. 8--9 | Theorem 3.6 repeats LR's uniform ball result. The adjacent path result is about paths **outside** the ball, with quadratic dependence on radius | Material early record of known ball geometry. The outside-ball theorem is not a full predecessor. Volume/copyright year is not a verified precise online posting date. |
| [Fortier Bourque--Rafi v3, August 29, 2017](https://arxiv.org/pdf/1606.05170v3), complete introduction pp. 1--3 and relevant preliminaries pp. 4--6; published JDG 110 (2018), 379--412 | Nonconvex balls for complex dimension greater than one; p. 3 explicitly recalls topology-only LR ball quasiconvexity; equation (2.2) records Kerckhoff's formula | Material antecedent and normalization source. Nonconvexity of the direct segment permits the alternative path. No full exact-ball almost-convexity theorem located. |
| [Rafi, GT 18 (2014), 3025--3053](https://www.math.toronto.edu/rafi/Papers/Hyperbolicity.pdf), introduction and exact bodies/proofs of Theorems 7.1 and 8.1, printed pp. 3045--3048 and 3050--3051 | Fellow travel with thick endpoints; a thin-triangle conclusion assuming a sufficiently long thick subinterval | No unrestricted exact-ball theorem. Thickness restrictions cannot be silently promoted to all points. The article explicitly cites LR in its references. |
| [Petyt--Zalloum version of record, September 15, 2026](https://link.springer.com/article/10.1007/s00208-026-03534-1), Theorem I and discussion p. 7; complete Lemma 4.2/Proposition 4.6 bodies and definitions pp. 17--19; Lemmas 7.9/7.10 p. 42 | `N(k)=k+6` almost convexity in dual `X_C(S)`, whose metric is integer valued and whose map from `S` is quasiisometric; normal wall paths | Full adjacent almost-convexity result in a different space/metric. It is not the submitted original-metric theorem. It must be acknowledged, but its constant is not a Teichmuller constant. |
| [Petyt--Zalloum v1](https://arxiv.org/pdf/2404.12057v1), April 18, 2024, p. 6; [v2 accepted version](https://arxiv.org/pdf/2404.12057v2), July 6, 2026, p. 6 | Both contain Theorem I and the statement about not directly answering Farb. V1's preceding definition omits the separation condition; v2 and published version include `d(x,y)=k` | Relevant 2024 antecedent. Use the corrected accepted/published definition, rather than interpreting the omission as an all-pairs uniform bound. |
| [Davis--Shapiro, Geom. Dedicata 39 (1991), 55--57](https://people.math.osu.edu/davis.12/old_papers/almostconvex.pdf), entire three-page body | Cannon's `AC(k)` terminology and `AC(2)=>AC` citation; Coxeter-specific original-ball detours via shorter common coset points | Older endpoint-shortening/concatenation mechanism and standard terminology. It does not state the general uniform-radial lemma or a Teichmuller conclusion. |
| [Petyt--Spriano--Zalloum, arXiv:2207.14127v4, July 1, 2024](https://arxiv.org/abs/2207.14127v4), Appendix A, pp. 47--49, full Proposition A.2 and proof | Uniformly quasiconvex balls in a quasihyperbolic/weakly roughly geodesic setting, used for coarse injective-hull/Helly conclusions | Search-discovered generic ball antecedent, but different assumptions/conclusion. No same-ball additive path lemma found in the read body. |

Every critical claimed comparison above uses an actual primary body, not an
abstract or search snippet. Whole-document term screening supplements the
complete relevant theorem/body readings; it is not represented as reading
every technical proof in a 57-page or 402-page source. Twenty-six critical
source page images were newly rendered and inspected. `VISUAL_LOCATORS.json`
records exact PDF pages, while the report supplies printed-page mappings.

## 4. The 2026 comparison and permissible current framing

PZ is not merely an inaccessible abstract: the entire published PDF was
retrieved and its applicable theorem, definitions, gated-ball lemma,
rough-geodesic proposition, and map from `S` were read. Its all-center and
all-radius quantifiers are genuinely relevant. The mismatch is metric and
space, not a missing radius quantifier. In particular, Lemma 7.10 gives a
quasiisometric embedding, rather than an isometry preserving original balls
and continuous original-metric path lengths. Its proof even compares chain
counts and original distances with a multiplicative lower estimate. Thus
one cannot identify its `B_r` with the submitted Teichmuller `B_r`.

The sentence following Theorem I describes the scope of that wall theorem.
It does not establish that no other argument answers Farb, or that the
older LR theorem has no elementary corollary. Conversely, the mismatch is
not proof of newness. An eventual note should acknowledge PZ explicitly
and explain that the exact-ball conclusion is derived directly from LR.
There is no supported claim of an improved numerical constant over PZ:
`c_g` is unspecified and the metrics differ.

## 5. Generic lemma priority and unsuccessful access

The general radial-retreat lemma could have appeared as a routine observation
in older almost-convexity, hyperbolic, or coarse-ball literature. I searched
the mechanism, intrinsic-distance language, uniform quasiconvex balls,
additive ball distortion, and accented/unaccented Teichmuller terminology.
I did not rely solely on the exact submitted title or on the phrase
Farb Question 3.5. `QUERY_LEDGER.json` preserves 43 discovery queries plus
two bibliographic-verification queries, grouped by tool call. Results in
a multi-query call are merged, so the ledger does not falsely assign a
single hit or negative result to a particular constituent query.

[Cannon, Almost convex groups, February 1987, 197--210](https://link.springer.com/article/10.1007/BF00181266)
is a material antecedent for the term. Its full original body was not
obtained: requesting the PDF returned subscription-preview HTML, preserved
with its hash in `sources/raw/cannon_published.html`. The exact failure
locator is the publisher's subscription/access section. No conclusion that
Cannon lacks the general lemma is made. Davis--Shapiro's complete primary
paper verifies the cited definition and records Cannon's Theorem 1.3 on
p. 198, but is not a substitute for reading the original Cannon body when
claiming lemma firstness.

The initial International Press survey fetch returned HTTP 403. The full
published body was subsequently obtained from `archive.intlpress.com`,
and the author's copy was also obtained. That critical comparison is
resolved, rather than left clear on a snippet. DOI opens for LR and
Kerckhoff failed in the web tool; the author-hosted LR journal PDF was
successfully read. Kerckhoff's bibliographic DOI was verified through an
[AMS reference list](https://www.ams.org/journals/bull/1988-19-02/S0273-0979-1988-15685-6/)
and the formula through FR equation (2.2). No claim of auditing Kerckhoff's
entire original proof is made.

No candidate with an unread body was marked disproved or irrelevant on
abstract evidence alone. The remaining original Cannon-body and exhaustive
generic-lemma priority gaps preclude worldwide firstness clearance. They
do not prevent a no-novelty-claim expository note, and they are not
mathematical gaps in the already accepted implication.

## 6. Exact presentation decisions

Eligible scope: an expository corollary with the complete accepted theorem,
its original-ball construction, attribution to LR for all substantive
Teichmuller geometry, and the distinction between the implicit deduction
and an explicit historical answer. The existing package largely already
satisfies this scope. Suggested manuscript framing is:

> We record an elementary original-ball path corollary of Lenzhen--Rafi's
> uniform quasiconvexity theorem. For every fixed closed surface, the
> resulting bound is ambient distance plus a topology-dependent constant,
> which gives an affirmative derivation of Farb's Question 3.5. We make no
> claim to historical priority for this deduction.

That is proposed authored wording, not a quotation from a primary source.
It does not require inventing a new theorem premise or shrinking the scope.

For any later publication package, apply the following across the abstract,
introduction, conclusion, README, acceptance/status metadata, PR description,
and any public problem-status announcement, rather than leaving a disclaimer
only deep in the proof:

1. Label the work an elementary corollary/expository deduction. Do not
   advertise a new substantive Teichmuller theorem or independently new
   discovery from the accepted proof alone.
2. Cite LR by its exact title, *Length of a curve is quasi-convex along a
   Teichmuller geodesic*, and distinguish journal Theorem 17 from arXiv-v1
   Theorem 15. `ROOT_MATH_AUDIT.md` calls it *The shape of a Teichmuller
   geodesic*; that title should be corrected in the root record. The
   submitted package has the correct title.
3. Cite [Kerckhoff, The asymptotic geometry of Teichmuller space, Topology
   19 (1980), 23--41](https://doi.org/10.1016/0040-9383(80)90029-4) for the
   distance formula when spelling out the extremal-length conversion, with
   the checked modern locator FR equation (2.2). Cite FR for nonconvexity
   and normalization and Farb for the exact question.
4. Acknowledge PZ Theorem I in its 2024/2026 versions and explain the metric
   mismatch. Do not present its scope sentence as a certificate that Farb
   remained globally open in 2026.
5. Keep every negative-search statement explicitly bounded to this audit.
   Avoid worldwide-first, previously-unsolved, recent-open-problem, and
   no-prior-art-found claims. The positive prior material is extensive.
6. Do not add generic coefficient-4 sharpness as a novelty claim for this
   PR. The root's separate new metric review contains a circle construction;
   it is outside the eight submitted originals and has its own unresolved
   publication priority. It also does not prove a best Teichmuller constant.

## 7. Strongest verified result, remaining gap, and release status

Strongest verified priority result: the required substantive uniform
Teichmuller input is established in primary prior literature, and the
full submitted theorem follows by an elementary general deduction.
No explicit source located in the inspected bodies states the entire
intrinsic-ball theorem, so `explicit_full_predecessor_found=false` means
a bounded no-match, not established absence.

Remaining gap for a novelty or first-solution claim: establish whether the
general lemma or exact corollary was previously stated, including legitimate
access to Cannon's original body and broader citation-chain coverage.
The current audit does not certify exhaustive coverage. A materially new
mechanism or verified result beyond the prior theorem plus elementary
bridge would be needed to promote this package as new mathematical
discovery; searching alone cannot create one.

No mathematical repair is requested by this priority audit. No publication,
merge, release, DOI snapshot, or outreach was prepared or performed.
`VERDICT.json` gives the machine-readable classification and exact eligible
scope. Initial/final input pins, source retrievals and pins, query ledger,
visual locators, and authored-output pins provide the checkable audit record.
