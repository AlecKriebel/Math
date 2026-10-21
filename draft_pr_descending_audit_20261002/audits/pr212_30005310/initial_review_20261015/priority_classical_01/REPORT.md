# PR212 / 30005310 classical-source priority and target audit

Audit date: 2026-10-15 UTC. Family: `priority_classical_01`. Scope: frozen OWR-11695865-009, the singleton-colored K4,4 candidate, and its K11=K22 variant. This is an independent source audit, not a promotion decision.

## Disposition

**Recommend a credited, already-covered source correction for the full literal numerical question. Do not promote the current construction as a novel Gaussian-threshold discovery or a qualified novel decisive original-problem paper.**

The singleton K4,4 counterexample is mathematically valid against the full printed numerical scenarios. The exact needed facts were already covered by Gross–Sullivant, arXiv:1404.6989v3 (2015), Section 5, and Blekherman–Sinn, arXiv:1703.07849v2 (2017), Theorems 2.1 and 2.7. The ideal translation is elementary and exact for this graph; it does not hide an unresolved generic-rank/MLT identification. The cited old results cover substantially more than this one graph.

This is different from proving that a prior author explicitly identified the error in the 2022 report. The two older papers predate that report. I did not find an explicit erratum or correction in the bounded authoritative search described below, and I make **no first-recognition claim**. The recent Homs/Kuznetsova/Stolz source is assigned to another priority family and was not read in this audit.

The antecedents-only interpretation of Conjecture 4 remains **unresolved by this example**: a strict signed-SOS certificate versus a positive-definite intersection is a different claim after the numerical conclusions are removed. The candidate has the positive-definite intersection.

## Independence, access, and evidence

The frozen native `source_record.json` and submitted `PROOF.md` were read first. I then read the original primary mathematics before opening any inherited review. The first substantive reasoning was frozen in `RESEARCH_LOG.md` at 09:51:31 UTC. No inherited review or sibling priority report was read at any point.

Frozen input SHA256 values: `source_record.json` = `827a4e3f4e23435472126ba1585557a8663f950b458352704715e16dc1bcfbda`; submitted `PROOF.md` = `69ffeade6c2ee758e3c2869d9c5b7dd607c9a1b6782f7ecebfb81d0812fdb676`.

Primary sources were read from the supplied private local PDFs, whose hashes were independently checked:

| Source | Exact source coverage read | SHA256 |
| --- | --- | --- |
| Official OWR 55/2022 report | Complete Roser Homs / joint Olga Kuznetsova contribution, printed pp. 3146–3149, including definitions, Proposition 3, Conjecture 4 and references | `56e4555409c330099d6ff15cdda3f8b3d5415af067c1800b0aac846ca5701b65` |
| Gross–Sullivant v3 | Introduction definitions/model convention; complete Section 5, including Definition 5.1, Lemma 5.2 proof, Corollary 5.3 and following bipartite statement, Corollary 5.4 and Example 5.5 | `eeea065ccdbb6149eaca84144c0a040460339a75393758ff76d22fb94b37a497` |
| Blekherman–Sinn v2 | Definitions 1.1/1.4; Propositions 1.2/1.5 and proofs; Section 2 through Theorem 2.7, its full proof chain (Theorem 2.5, Lemmas 2.8–2.10), and Corollary 2.11/proof | `dd87cd09fd9a133f182e73a536233b12aaa6dd698e40f2a2da2a5406633a3572` |

I visually inspected the original-page renders for OWR pp. 3146–3149, GS pp. 13–14, and BS pp. 13–18. Existing sibling private source renders were reused. Only one additional small GS page-13 render was made, under `private/`. No full paper was duplicated, and no PDF, extracted full text, or page render is included in the authored manifest.

Version-history and publisher metadata were checked directly on the [GS arXiv v3 page](https://arxiv.org/abs/1404.6989v3), [BS arXiv v2 page](https://arxiv.org/abs/1703.07849v2), [EMS report page](https://ems.press/journals/owr/articles/11695865), and [MFO repository record](https://publications.mfo.de/handle/mfo/4016). The read GS version was posted 2015-09-16; the read BS version was posted 2017-05-23. The official OWR article was published 2023-07-27, reporting the December 2022 workshop. Both old mathematical sources therefore predate the October 1, 2026 candidate cutoff and the report itself.

## Exact target and model class

The frozen native record asks about a **general colored Gaussian graphical model** with

\[
I(G,n+1)=0,\qquad I(G,n)\ne0.
\]

It incorporates the numerical conclusions of the report's Proposition 3:

1. A generator that becomes a strict, everywhere nonvanishing signed sum of squares on positive-diagonal Cholesky factors is said to force WMLT=MLT=n+1.
2. A positive-definite S0 whose statistics lie in V(I(G,n)) is said to force WMLT=n and MLT=n+1.

The report prints `n=WMLT≤MLT=n+1`; the cleaned record uses a strict inequality between the two thresholds. With the printed endpoint values n and n+1 this does not change the numerical target. Conjecture 4 refers back to the two cases of Proposition 3. An interpretation retaining the complete numerical scenarios is therefore both present in the frozen question and a natural literal reading of that cross-reference.

The report discusses colored 4-cycles as examples, and immediately after Proposition 3 explains their computation. Its definition of colored models, its elimination criterion, Proposition 3 and Conjecture 4 impose no explicit four-vertex or 4-cycle restriction. An unstated intended 4-cycle restriction cannot be resolved from this example and should not be silently inserted into the frozen general question.

The original model definition permits arbitrary partitions of vertices and edges into color classes. Singleton classes recover precisely the ordinary concentration model: positive-definite K with Kij=0 for missing edges, and otherwise free diagonal and edge entries. For K4,4 this is a valid colored Gaussian graphical model under the written definition. No uniform vertex or edge coloring is assumed in either old graph theorem. The tied variant merges only vertices 1 and 2, imposing K11=K22. Its sufficient-statistic map replaces s11,s22 by s11+s22. The report imposes no restriction that would forbid this model either.

## Exact coverage map

Write the bipartition as L={1,2,3,4}, R={5,6,7,8}; all sixteen cross edges have distinct colors. Distinguish the graph-theorem part sizes a,b from the rank index n in the OWR question.

| Needed statement for singleton K4,4 | Older written coverage | Exact bridge / assessment |
| --- | --- | --- |
| Same model and statistics | GS introduction; BS definitions: ordinary Gaussian concentration graph, diagonal plus edge-coordinate projection | Exactly the report with singleton color classes; observed target dimension is 8+16=24 |
| WMLT=2 | GS Definition 5.1, Lemma 5.2 and Corollary 5.3; the text immediately after the corollary explicitly specializes to every bipartite graph with an edge | Directly covered, not a new derivation of a threshold invariant |
| GCR=4 | BS Theorem 2.1: GCR(Ka,b)=a for a≤b≤binom(a,2), else a+1 | a=b=4≤6 gives 4; the m=4 discussion after Corollary 2.11 again explicitly gives 4 for b=4,5,6 |
| I(G,4)=0 | GCR definition is dominance of the projection of the symmetric rank≤4 variety | Any element of the exact elimination ideal vanishes on this dense image, hence is identically zero; no equality MLT=GCR is assumed |
| I(G,3)≠0 | BS cross-block rank obstruction in Remark 2.3 | det(B) is an actual 4-minor and belongs directly to the exact elimination ideal; it is a nonzero polynomial in observed coordinates |
| MLT=4 | BS Theorem 2.7: min(M,a+1), M=min{k:binom(k+1,2)≥a+b} | Here binom(4,2)=6<8≤10=binom(5,2), so M=4 and min(4,5)=4. This result is credited old mathematics |
| Positive-definite intersection at rank index n=3 | GS splitting construction plus completion geometry; easy explicit specialization | diag(J4,J4) has the same observed coordinates as I8 and rank 2≤3; an exact-rank-three witness is also supplied below |
| Neither full numerical scenario holds | Immediate conjunction of the above | n=3 but (WMLT,MLT)=(2,4), whereas the printed scenarios require (4,4) or (3,4) |
| Prior explicit correction of Proposition 3 / Conjecture 4 | Neither old source could discuss a future report | **Not established** by these papers or by the bounded search |
| Antecedents-only SOS-versus-PD-intersection dichotomy is false | No coverage, and this example does not prove it | The second antecedent is true here; that repaired question is not resolved |
| Exact MLT of K11=K22 variant | Neither old ordinary-graph theorem states it | Do not transfer MLT=4 to the tied model |

There is no need for K4,4 to be the first counterexample graph: the same old theorems already give GCR=MLT=4 and WMLT=2 for K3,4, also contradicting the full numerical scenarios at n=3. This observation is another consequence of those same theorems, not an additional novelty claim.

## Challenge to the older proof chains

### Gross–Sullivant Section 5

Definition 5.1 asks for a PSD matrix of rank at most r whose observed coordinates admit a PD completion. The reason one witness suffices for the weak threshold is openness of the PD cone and continuity of the data-to-statistics map. More explicitly, a small change in the observed coordinates can be lifted by a fixed linear right inverse of the coordinate projection; adding that lift to a PD completion preserves PD for sufficiently small change. Thus nearby data still have a PD completion. Nondegenerate Gaussian data have positive density on every nonempty Euclidean open set.

In Lemma 5.2, split vertices into induced subgraphs, use a PSD/PD pair for each block, and form block-diagonal matrices. All cross-block observed edges have coordinate zero in both block-diagonal matrices, irrespective of how many such edges there are. PSD ranks add, PD is preserved, so weak thresholds add as an upper bound. For a proper graph coloring, every color class is edgeless, hence each has a rank-one all-ones PSD matrix matching the identity diagonal. This gives WMLT≤χ. An observed edge with two singleton endpoint diagonals rules out one observation because its observed 2×2 principal submatrix is singular. Hence every bipartite graph with an edge has WMLT=2, as the paper explicitly says.

One printed explanatory inequality after Definition 5.1 is reversed: it says `wmlt(G)≥n` in the sentence claiming positive probability with n data points; the definition requires `wmlt(G)≤n`. This does not undermine the actual definition, splitting proof or explicit bipartite statement. I used the definition and proofs, not the incorrect inequality.

### Blekherman–Sinn Theorem 2.1

The lower bound a comes from the a×b fully observed cross block B. For b=binom(a,2), their explicit construction uses a row ei+ej for each unordered pair. In the annihilator calculation, off-diagonal equations force each diagonal multiplier on the second part to vanish, then the cross and first-part diagonal multipliers vanish. This gives dominance at rank a. Deleting vertices from the second part down to b=4 preserves the upper bound, and the cross-block minor prevents a smaller value. For a=b=4 this is exact.

There are harmless source slips: the proof refers to its Theorem 2.5 as a proposition, and Remark 2.2 calls the treewidth a+1, whereas under the GS convention treewidth is a. The upper completion-rank bound a+1 is correct. The K4,4 specialization lies on the b≤binom(a,2) branch, so that off-by-one treewidth wording is not used. The independent exact Jacobian certificate below also verifies this specialization directly.

### Blekherman–Sinn Theorem 2.7

The proof does not identify generic completion rank with MLT by assumption. Proposition 1.5 uses PSD sparse annihilators, whereas Proposition 1.2 uses arbitrary sparse annihilators. Lemma 2.8 constructs open sets of low-dimensional data subspaces contained in kernels of PSD sparse matrices. Lemma 2.9 addresses the real positivity/interior issue; a mere nonzero complex kernel vector would not establish this. Lemma 2.10 dimension-counts the sparse-PSD kernel family, factoring out a one-dimensional stabilizer, to prove almost-sure success at the matching upper threshold.

For K4,4 the numerical specialization is unambiguous, and the following explicit rational real certificate reconstructs the lower-bound mechanism without relying on a general complex-to-real density claim. Dominance gives the matching upper bound independently. This verifies the needed specialization; it is not a claim to re-audit all parameters in the published general theorem.

## Exact independent derivation and finite certificates

`check_certificates.py` uses only Python's standard library and exact rational arithmetic. It makes no network requests or writes. Its captured output is `certificates.json`. All column indices in that output are zero-based. No floating-point ranks or sampled success frequencies are used.

### Elimination ideals and generic completion rank

The report's J(G,r) consists of the (r+1)-minors of a symmetric 8×8 S and equations identifying the statistic variables with the diagonal and cross entries. Substituting the linear statistic equations shows that every f∈I(G,r) vanishes on the projected rank≤r variety.

Consequently, BS's dominance at r=4 immediately implies I(G,4)=0: a polynomial vanishing on a Zariski-dense subset of the full 24-dimensional target is the zero polynomial. This implication needs neither primality nor radicality of J. The reverse nonzero assertion at r=3 is stronger than merely knowing a polynomial in a radical: det(S[L,R]) is itself one of the defining 4-minors. Replacing its entries by the observed statistic variables changes it by an element of the linear statistic ideal. Thus det(B)∈I(G,3), and det(B) is not the zero polynomial (it equals 1 at B=I4). These two elementary arguments fully bridge the exact algebraic ideals for this candidate. A general ideal-versus-variety equivalence beyond these directions is unnecessary here.

As an independent check, let Φ(X)=πG(XXᵀ), X∈R^(8×4). Set the top four rows to I4 and the bottom rows to e1+e2,e2+e3,e3+e4,e4+e1. Order outputs by eight diagonals followed by sixteen cross entries; order inputs by rows. The checker finds a 24×24 Jacobian minor equal to **256**. Hence Φ is a submersion at this real point, its image contains an open set, and I(G,4)=0 follows even without the old dominance theorem.

### Weak threshold and the second antecedent

Use data rows e1 on L and e2 on R in R². Its Gram matrix is S*=diag(J4,J4), of rank 2, and πG(S*)=πG(I8). There is a nonempty open success set: if each data entry differs from this X* by less than ε=1/100, form a completion with observed diagonal and cross entries and zero within-part off-diagonals. Its diagonal is at least (1−ε)², while each of four cross entries has absolute value at most 2ε(1+ε). The diagonal-dominance margin is at least **8993/10000>0**, so it is PD throughout the box. The data there have rank 2. The positive Gaussian density gives positive probability, and a single observed edge prevents any rank-one PD completion. Therefore WMLT=2.

For the source's second antecedent at n=3, πG(I8)=πG(S*) belongs to V(I(G,3)), since rank S*≤3. Even if one insists on exact rank three, take the first two L rows to be e1, the next two L rows e3, and all R rows e2 in R³. This rank-three Gram matrix has the same diagonal and cross statistics as I8. Thus the counterexample is not caused by a rank-at-most versus exact-rank convention.

Every polynomial of I(G,3) vanishes at these statistics of I8. Its positive-diagonal Cholesky factor is I8 itself. No such ideal polynomial can therefore be everywhere nonvanishing on the PD Cholesky domain. The first antecedent cannot hold, while the second antecedent does hold and its claimed WMLT conclusion fails.

### An exact open failure set at three observations

Take V with rows e1,e2,e3,(1,1,1), put a=(1,2,3,4)ᵀ, and let H=I4−aaᵀ/15. Then H is a rational orthogonal Householder matrix and W=HV has rows

\[
(2/3,-2/5,-7/15),\quad(-2/3,1/5,-14/15),\quad
(-1,-6/5,-2/5),\quad(-1/3,-3/5,-13/15).
\]

Regard X=[V;W] as eight rows of three-observation data. Form C with six rows indexed by 1≤i≤j≤3 and eight columns: four entries vk,i vk,j and four entries −wk,i wk,j. We have C·1=0. The first six columns have determinant **1148/3375**, so C has rank 6. Under any sufficiently small perturbation of X, fix the last two coordinates of a kernel vector to 1 and solve for the first six. Invertibility persists, and the solution stays close to the all-ones vector, hence strictly positive.

Write that kernel vector as positive diagonal weights α,β. The equation is Vᵀdiag(α)V=Wᵀdiag(β)W. Let DL=diag(sqrt(α)), DR=diag(sqrt(β)). Both weighted frames retain column rank 3. Equality of their Gram matrices gives an isometry between their spans; extend it to an orthogonal 4×4 B satisfying DRW=BDLV. Then

\[
M=\begin{pmatrix}D_L^2&-D_LB^TD_R\\-D_RBD_L&D_R^2\end{pmatrix}
=\begin{pmatrix}D_L\\-D_RB\end{pmatrix}
\begin{pmatrix}D_L&-B^TD_R\end{pmatrix}
\]

is nonzero PSD, supported on the graph's diagonals and cross edges, and MX=0. For any matrix P with the same observed statistics as XXᵀ, tr(MP)=tr(MXXᵀ)=0. A PD P would give tr(MP)>0, impossible. Thus a full Euclidean neighborhood of rank-three data fails to admit a PD completion. It has positive probability under every nondegenerate zero-mean Gaussian model.

At the exact displayed data, B=H; the checker verifies rank(M)=4 and MX=0. The C minor supplies the missing neighborhood/positivity certificate, so this is not merely an exceptional failure point.

The full-rank Φ Jacobian gives almost-sure success at four observations: its displayed minor is a nonzero polynomial in the data, so almost every four-observation X is a submersion point. Its statistics then have a neighborhood inside πG(PSD), hence lie in its interior. An interior point y has a PD completion because for small t>0, y−tπG(I8) still has a PSD completion Q, and Q+tI8 is PD with statistics y. This proves MLT≤4. Open failure at three observations gives MLT≥4, using ordinary sample-count monotonicity: appending an observation yyᵀ to a successful scatter matrix preserves a PD completion by adding yyᵀ to it. Therefore MLT=4 independently of the old theorem.

### Sample convention

GS explicitly fixes mean zero in its introduction. Its sample-rank formulation matches r observations arranged as columns of X with scatter XXᵀ. BS defines the threshold by generic rank-r PSD matrices, the same convention. The report's elimination theorem also indexes n observations by the rank≤n ideal. Positive factors such as 1/r do not affect the homogeneous completion question. No unknown-mean centering convention or its one-observation shift is imported. All probability claims above use full support of a nondegenerate Gaussian data density and open sets, not one exceptional covariance matrix.

### Tied variant: what follows and what does not

Let q sum the first two diagonal statistic coordinates. Then πtied=q∘πsingleton. The old rank-four dominance, composed with the surjective linear map q, proves I(tied,4)=0. The cross determinant remains an observed polynomial in I(tied,3), so that ideal is nonzero. The checker independently finds a 23×23 Jacobian minor equal to **128**.

Every singleton PD completion is a tied-statistic PD completion, so GS's rank-two success witness gives WMLT(tied)≤2. The edge 3–5 retains both singleton diagonal statistics and its own edge statistic, so its rank-one 2×2 obstruction proves WMLT(tied)≥2. The exact-rank-three intersection witness still works after applying q. Therefore this tied model also contradicts the full numerical WMLT scenarios.

The older papers do not state a theorem for this tied concentration class. These properties follow by an elementary projection argument from their old singleton results plus the report's written statistic map. The tie supplies a valid genuinely colored example, but it does not supply a new mechanism or justify calling the already-covered singleton threshold result novel. **No exact tied-model MLT is established here.** In particular, the sparse dual matrix used in the singleton rank-three failure argument need not satisfy the tied diagonal equality after perturbation, so that lower bound is not silently transferred.

## Bounded historical search and exact remaining gaps

I opened the official publisher/repository records and the two arXiv version pages. Narrow searches included the report DOI with “erratum”, Homs/Kuznetsova plus “correction”, and Proposition 3 plus their names. Further primary-domain searches were restricted to EMS and arXiv. They produced the official report or no results. The official EMS page presents the same report and no displayed erratum link. An initial guessed EMS URL was incorrect; it returned an error and was not used as evidence. The correct report article number is 11695865.

This is not an exhaustive literature census and does not prove that no author has already recognized or corrected the mistake. I did not read the recent 2026 Homs/Kuznetsova/Stolz paper, author webpages, unpublished correspondence, theses, or every citing paper. No search snippet or unread article is used as evidence for mathematical coverage. No outside individual was contacted or messaged, and no outreach was prepared.

The strongest verified conclusion is that **the exact singleton numerical counterexample is an immediate consequence of fully read old primary results**, and that a small independent exact derivation corroborates every needed mathematical fact. The gap about prior explicit recognition of the 2022 error remains open in this family. The bare antecedents-only dichotomy and an intended-but-unstated 4-cycle-only formulation are separate unresolved targets here.

If the human chooses to retain a correction note, it should plainly credit GS for WMLT=2 and BS for GCR=MLT=4, state that the exact ideal implications are elementary, identify the source's incorrect numerical lower conclusion, and avoid a new-discovery claim. No publication or eligibility decision is made by this audit.

## Artifact and operational boundary

Authored files are `REPORT.md`, `RESEARCH_LOG.md`, `check_certificates.py`, `certificates.json`, `MANIFEST.json`, and `SEAL.sha256`. The manifest uses only safe relative paths and records bytes and SHA256 for the first four; the separate seal authenticates the manifest. The private GS page render is excluded. Source PDFs, extracted source texts and sibling artifacts are excluded. No Git/index/ref, queue, database, PR, provider, tracker, or publication state was changed. The parent retains all promotion authority; the wider user goal remains active and incomplete.
