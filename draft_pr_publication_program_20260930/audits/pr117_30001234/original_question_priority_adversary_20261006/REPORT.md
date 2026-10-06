# Independent priority audit: PR117 / 30001234

**Decision: the exact original negative answer was already published.** The mathematics of the candidate remains valid, but it cannot be promoted as a novel resolution of an open problem. The dated catalogue assertion that this question remained open on21August2026 is contradicted by an explicit primary source available since2011.

This audit binds to immutable PR head `8163ee0dc7a0f944570925984cef2dc0fb291ad8`, original `CANDIDATE.md` SHA256 `1409e8ad35d34f3cc4a9bb14f7e42318c1dd1e0446ecba525c655fad8c978cdf`, and the complete authenticated source/prior pair with review hash `6ff8253c57c5544f0b33ac8a6303be8ec7f42ac0f5ce6b4976a8149ae1b28152`. The supplied prior report is the empty object. The actual mathematical/source gate was PASS before this family began. The incoming1/5 ledger and all original bodies are preserved; this source/priority audit adds zero central proof-search turns.

## Decisive earlier result

Shunsuke Takagi, *Adjoint ideals and a correspondence between log canonicity and F-purity*, [arXiv:1105.0072v1](https://arxiv.org/abs/1105.0072v1), posted30April2011, **Example4.4 on p19**, already gives the identical three generic2-by-3 minors as a counterexample to the augmented-image assumption of **Remark4.3, pp18–19**. The same result appears in **Example4.4, printed p940**, of the formal publication, *Algebra & Number Theory*7(4)(2013),917–942, [DOI10.2140/ant.2013.7.917](https://doi.org/10.2140/ant.2013.7.917), with the operative Remark4.3 on p939. The official [MSP full text](https://msp.org/ant/2013/7-4/ant-v7-n4-p06-s.pdf) is publicly accessible and was actually obtained. It records the failure of the assumption and LP optimum3, compared with log canonical threshold2. This is an explicit earlier counterexample, not a deduction made only during our review.

The2011v1 text and rendered pp18–19, and the2013 text and rendered printed pp937,939–940, were read. The later2013v5 author text also retains Example4.4. The earliest disclosure established here is30April2011; no assertion that it was the first disclosure anywhere is needed. Official MSP metadata binds the journal identity and publication date29August2013. The triangle-labelled augmented matrix on p937 must not be mis-cited as equation(4): text extraction confused its triangle tag with4, and a300dpi rendered detail resolved the glyph.

## Exact correspondence, independently checked

The source is not merely using the same familiar ideal for a different theorem. Its LP specializes to the target LP. In Remark4.3 take `c=0`, `n=6`, `s=3`, and two terms per generator. The ambient space is affine6-space, a smooth normal complete intersection; its log-canonicity assumption holds automatically. The extra equality indexed by the first `c` generators becomes the empty equality0=0. The objective consequently sums all six nonnegative rational coordinates. Each of the three bottom matrix rows is a cap on the two terms of one generator. Thus no extra constraint remains relative to OWRQuestion8 or Shibuta–TakagiQuestion2.2.

The candidate uses

\[
f_1=x_1y_2-x_2y_1,\quad f_2=x_2y_3-x_3y_2,\quad
f_3=x_3y_1-x_1y_3.
\]

The old example's third generator is `-f3`; its first two are identical. Multiplication by the unit-1 changes neither the ideal nor minimality. If `z=(mu1,mu2,mu3,nu1,nu2,nu3)` is the candidate's coordinate vector, the old interleaved vector is

\[
\sigma=(\mu_1,\nu_1,\mu_2,\nu_2,\nu_3,\mu_3).
\]

Let `A` be the candidate's9-by-6 matrix and `B` the old interleaved matrix. The six exact column identities give

\[
B\sigma=Az
\]

for every rational vector `z`. This coordinate permutation preserves nonnegativity, objective value, feasibility, and distinction of points. Therefore it preserves the existence or nonexistence of an optimal point with a singleton augmented-image fiber. Changing the orientation is not an escape from the earlier result.

For additional independent confirmation, the candidate's complete optimal face transforms into

\[
\sigma(t)=(t,1-t,t,1-t,1-t,t),\quad
t\in\mathbb Q\cap[0,1],\qquad B\sigma(t)=\mathbf1_9.
\]

The three generator caps give the upper bound3. They are saturated by these vectors. Substituting saturation into the six variable caps yields the same cyclic equalities that force all candidate `mu_i` to agree. Hence this is the entire optimal face. For every `t`, another rational endpoint parameter produces a distinct point of the same image fiber. The target failure is universal over optimizers; it is not merely a nonunique optimum. The independently established minimality and absence of monomials apply to the same ideal: evaluation at the all-ones point excludes monomials, and three disjoint degree-two binomials are linearly independent in the lowest homogeneous degree. No change from polynomial rings to Laurent rings is being made.

The public portable checker reconstructs both matrices from the exact exponents, verifies the column permutation on every basis vector, checks the rational segment and endpoint distinction, and detects the wrong permutation that forgets the third generator's orientation. These finite checks certify matrix identities; they do not substitute a sampled numerical calculation for the unrestricted argument. No log canonical threshold theorem is required to verify that the candidate duplicates the old explicit LP counterexample.

## Original question and version chain

The [official OWR report](https://ems.press/content/serial-article-files/46224), Takagi contribution pp1136–1139, retains the existential singleton-fiber condition in Proposition5 and asks Question8 without a regular-sequence or space-curve restriction. Its statement that the authors knew no counterexample is a2009 statement, not a2026 status certificate.

The original Shibuta–Takagi [arXiv:0810.1278v1](https://arxiv.org/abs/0810.1278v1),7October2008, asks a characterization as Question3.2 after Lemma3.1. The12March2009v2 and9April2009v3 express the universal minimal-generator question as Question2.2 after Proposition2.1. Their positive complete-intersection and space-curve results do not restrict that question. In particular, Example3.4(v1), renumbered Example3.2(v2/v3), contains both a suitable optimal point and an unsuitable one. That example is not a prior disproof of the existential assertion. The actual negative answer is the later TakagiExample4.4, on the same literal criterion after the `c=0` specialization above.

The [Springer2009 journal metadata](https://link.springer.com/article/10.1007/s00229-009-0270-7) confirms the Shibuta–Takagi paper's identity and publication dates. Its subscription full text was not obtained in this family. This access limit does not leave the priority decision unresolved: the operative original question is available in the official OWR report and author versions, and both the2011 and published2013 negative answer are fully accessible.

## Later literature and bounds of this search

I independently searched the exact question, wording variants, and cited-by records before reading any other new priority-family report. Semantic Scholar's19 entries and OpenAlex's20 entries were discovery aids; they include duplicate and issue-level records and are not exhaustive bibliographies. This chain located the decisive paper by the original question's coauthor.

The later Blanco–Encinas algorithm, Badilla-Céspedes–León-Cardenal splitting-polytope work, and LaClair binomial-edge LP work were also obtained from primary sources and screened. They provide useful context, but none is needed to infer priority here. Their different thresholds, additional assumptions, or modified polytopes must not be substituted for the precise original fiber question. Some less directly relevant citing papers were only keyword screened, and three discovered follow-ups were not read in full. The exact full read/access limits are recorded in `SOURCE_READ_BOUNDARY.json`. No assertion of exhaustive search or of absence of prior art is made. Positive primary evidence already decides the original question's status.

## What the candidate adds and required correction

The written all-degree ideal checks, explicit parameterization of the whole optimal face, and reproducible exact verification package are useful exposition and independent verification. The decisive ideal, target failure, and optimum3 already occur in Takagi's exact earlier example. This package does not establish a new core theorem, a stronger condition, a new threshold, or a new resolution of an open mathematical question. A more elementary proof of this very small known example alone does not meet the current program's novel-resolution publication requirement.

The corrected result classification should be **already_solved**, with credit to Takagi's2011Example4.4 and2013 publication. The math need not be withdrawn as false. The candidate's historical bounded search failed to locate this explicit source; its “no explicit earlier answer located” sentence cannot be used as current priority clearance. The source catalogue'sAugust2026 open-status assertion requires a separate native assessment correction that preserves the immutable source/cache history. This family has performed no such mutation.

Repair within the existing candidate's scope can correct attribution, citations, source status and reproducibility claims. It cannot turn the identical counterexample into a novel resolution. A claim of new results would require a materially different verified theorem, and no such theorem is present. Do not create a preprint, DOI or tracker row for the existing claimed solution under the current instructions. The parent must apply the authorized repository disposition and readback process; this report itself does not merge or close anything.

## Validation and provenance

The comparator passes in clean physical Python both normally and under `-O`. Deliberately false guards are rejected in both modes, including the acquisition/render helper guard functions. The private-source mode binds all retrieved source bodies and actual immutable candidate/source inputs by full byte counts and SHA256. Original proof bytes are unchanged. A dotted arXiv render-prefix receipt lookup initially failed after the first page had rendered; the failed helper and filename repair record are preserved, and the corrected two-page render succeeded. This was a filename defect, not a mathematical or priority defect.

`SOURCE_MANIFEST.json` pins private source/render bodies; they are excluded from public release. Acquisition/render journals record real process IDs, UTC times, URLs, HTTP outcomes and body hashes. `CHECK_PROCESS_RECEIPT.json` records actual normal/optimized/false-control runs. `RESULT.json` states the narrow decision. `OUTPUT_MANIFEST.json` seals the public-safe family artifacts. No outside person was contacted, no service/native/Git/index/ref/global state was mutated, and the overall persistent goal remains incomplete.
