# Adversarial mathematical review of pull request 9

PR: [30005473: reviewed proof of discotope exposed-point irreducibility](https://github.com/AlecKriebel/Math/pull/9). Reviewed head: `a29887ed0e341851d02fa992c26500d4089267be`. Review date: September 29, 2026, America/Los_Angeles; the corresponding UTC date is September 30.

**Mathematical verdict: PASS. No actionable mathematical or computational defect was found.** Theorem 1 proves complex irreducibility of the exposed-point closure for every finite sum of discs of dimension at least two, including nongeneric and lower-dimensional sums. Theorem 4 correctly proves equality with the 2022 paper's purely nonlinear part under the explicit general-position condition. Both match the source questions they claim to settle. The computations reproduce, and the proof artifacts agree.

This conclusion follows from a fresh review of the proofs and three independently assigned mathematical audits, not from accepting the PR's prior review verdict. Historical priority remains unestablished. No assertion is made about degrees, birationality, or irreducibility of the full complex critical locus.

## Exact claims and source scope

For discs \(D_i=A_i(B^{m_i})\subset\mathbb R^d\), with injective real \(A_i\) and \(m_i\ge2\), write
\[
D=\sum_iD_i,\qquad
E(D)=\overline{\operatorname{Exp}(D)}^{\mathrm{Zar},\mathbb C}.
\]
The main claim is that \(E(D)\) is irreducible without a genericity hypothesis. Success requires a proof for all permitted dimensions, all positive finite numbers of summands, and all arrangements, rather than a finite collection of examples.

The official 2023 Oberwolfach report, printed p. 830, Definition 1 and Conjecture 1, formulates its target using the exposed-point closure. Its disc definition agrees with the candidate's linear images of balls. Theorem 1 therefore proves the exact target with stronger hypotheses removed. The separate rank-one-convexity question elsewhere in the report is not part of this target. [Official report](https://publications.mfo.de/bitstream/handle/mfo/4031/OWR_2023_15.pdf?sequence=4).

The 2022 paper instead uses
\[
S(D)=\overline{\left(\sum_i\partial_{L_i}D_i\right)\cap\partial D}^{\mathrm{Zar},\mathbb C},
\qquad L_i=\operatorname{im}A_i.
\]
Definition 3.3, p. 149, and Conjecture 8.2, p. 167, concern this variety. Section 2, pp. 146–147, parametrizes genericity by bases and restricts to a full-dimensional span. The candidate distinguishes these definitions and supplies a separate proof of their generic equality. It does not silently substitute the exposed-point target for the older question. [Published paper](https://lematematiche.dmi.unict.it/index.php/lematematiche/article/download/2338/1156/6734).

## Independent approach families

The three mathematical auditors initially read the candidate without reading the earlier `REVIEW.md` or verdict. Their mechanisms, evidence, and gaps were kept separate before synthesis.

| Approach family | Mechanism and evidence | Status | Exact remaining gap |
|---|---|---|---|
| Convex and real analytic | Exact maximizing faces, connected normal complement, complex prime vanishing ideal; full independent derivation | Pass | None identified in Theorem 1 and Lemmas 2–3 |
| Generic face geometry | Direct-sum rank argument, explicit real transpose solution, positive perturbations, real Vandermonde generic witness, extreme-point cross-check | Pass | None identified in Theorem 4 or its generic scope |
| Exact algebra and reproduction | Independent polynomial derivation and ideal certificate, denominator analysis, non-orthonormal perturbations, recorded-output and transcription comparison | Pass | None identified in the examples or computations |
| Root source and artifact audit | Original conjecture pages, definitions and parameter convention, immutable hashes, all five proof PDF pages, fresh head check | Pass | Historical priority is not established |

The detailed reports are [analytic and convex audit](analytic_convex_audit.md), [generic face audit](generic_face_audit.md), and [algebra and reproduction audit](algebra_reproduction_audit.md).

## Theorem 1 checked step by step

The relevant candidate locations are lines 21–41, 47–78, and 82–84.

1. **Every disc admits the stated injective representation.** Restricting a singular-value decomposition to its nonzero singular directions gives an injective \(A_i:\mathbb R^{m_i}\to\mathbb R^d\) with the same image ball. This does not assume an orthonormal basis or a full-dimensional summand.

2. **The normal domain covers precisely every exposed point.** For a normal \(u\), Cauchy–Schwarz gives the unique maximizing point
   \[
   p_i(u)=\frac{A_iA_i^Tu}{\|A_i^Tu\|}
   \]
   when \(A_i^Tu\ne0\). When it is zero, the entire positive-dimensional disc is the maximizing face. Support values add, and equality in their sum forces equality term by term. A sum of nonempty faces is a singleton exactly when every face is a singleton: fixing all other summands translates any nonsingleton face into the sum. Thus no cancellation or nonunique-decomposition loophole exists, and
   \[
   \operatorname{Exp}(D)=F(U),\qquad
   U=\mathbb R^d\setminus\bigcup_i\ker A_i^T,
   \quad F(u)=\sum_i p_i(u).
   \]

3. **The whole domain is connected.** Each excluded kernel has real codimension \(m_i\ge2\). For any \(x,y\in U\), choose \(z\) outside all subspaces \(\ker A_i^T+\mathbb Rx\) and \(\ker A_i^T+\mathbb Ry\). Each is proper, so such a \(z\) exists. The two segments through \(z\) avoid every kernel. This proves path connectedness even at codimension exactly two, with repeated spans and arbitrary intersections.

4. **The chosen branch is real analytic globally on that domain.** All radicands are \(u^TA_iA_i^Tu=\|A_i^Tu\|^2>0\). The positive real inverse square root is real analytic on \((0,\infty)\). Hence \(F\) is real analytic everywhere on \(U\). Complex isotropic normals, monodromy, and dependent quadratic radicals do not invalidate a real-analytic assertion. No global holomorphic square-root branch is needed.

5. **Complex, rather than merely real, irreducibility follows.** Let \(I\) be the ideal of complex polynomials vanishing on \(F(U)\). If \(PQ\in I\) and \(P\notin I\), continuity supplies an open neighborhood on which \(P\circ F\ne0\), so \(Q\circ F=0\) there. The real-analytic identity theorem applies to its real and imaginary parts on connected \(U\), giving \(Q\in I\). Thus \(I\) is proper and prime. It is exactly the ideal of the complex Zariski closure, which is therefore irreducible. This verifies the critical algebraic passage and requires no image smoothness, injectivity, or Jacobian rank assumption.

The argument is a complete proof. Finite numerical or symbolic examples are not being asked to justify the universal claim.

## Theorem 4 checked independently

The relevant candidate locations are lines 98–131. Let \(T=(\sum_i\partial_{L_i}D_i)\cap\partial D\). Exposed points are in \(T\), giving \(E\subseteq S\).

For \(x=\sum_i x_i\in T\), full dimensionality provides a nonzero supporting normal \(u\). Every support deficit is nonnegative and their sum is zero, so each summand maximizes \(u\). Let \(J=\{j:A_j^Tu=0\}\). The spans of these summands lie in \(u^\perp\). If their total dimension were at least \(d\), (GP) would force their span to have dimension \(d\), a contradiction. Thus (GP) makes their concatenated matrix \(B=[A_j]_{j\in J}\) injective.

Writing \(x_j=A_jv_j\) with \(\|v_j\|=1\), stack the vectors into \(v\). An explicit simultaneous solution is
\[
w=B(B^TB)^{-1}v,\qquad B^Tw=v.
\]
This uses a real positive-definite Gram matrix and works for non-orthonormal ellipse matrices. For positive \(\varepsilon\), the normal \(u+\varepsilon w\) exposes exactly \(x_j\) in every killed summand. All other projected normals remain nonzero for sufficiently small \(\varepsilon\), and their support points converge to \(x_i\). Consequently every point of \(T\) is a Euclidean limit of exposed points. The complex algebraic set \(E\) is Euclidean closed, so \(S\subseteq E\).

The genericity claim is also justified over the reals. Partition distinct Vandermonde columns \((1,t,\ldots,t^{d-1})^T\) into blocks of the prescribed sizes. Every subset of blocks attains the maximum rank, simultaneously giving a real witness for (GP). The maximal-rank minor conditions define a nonempty Zariski-open parameter set. For feasible full-dimensional types, this matches the published convention.

The relative-boundary convention is essential and explicitly written. The generic auditor supplies a counterexample to an incorrect ambient-boundary substitution. The proof has no omitted sign condition: negative epsilon would choose antipodal killed-summand points, and the candidate correctly requires positive epsilon.

## Counterexamples and exact computational checks

The nongeneric example is valid in the stronger algebraic sense claimed. For two identical unit \(xy\)-discs and one unit \(xz\)-disc, introduce \(a=2u_1/r\) and \(b=u_1/s\). Then
\[
X=a+b,\quad a^2+Y^2=4,\quad b^2+Z^2=1,
\]
which directly gives
\[
P=(X^2+Y^2+Z^2-5)^2-4(4-Y^2)(1-Z^2)=0.
\]
Every exposed point satisfies this polynomial, so \(E\subseteq V(P)\). Meanwhile \(e_3=e_1+(-e_1)+e_3\) is a sum of relative-boundary points on the support face \(2B^2_{xy}+e_3\), and \(P(e_3)=16\). Therefore \(e_3\in S\setminus E\). It is insufficient merely to check that a chosen normal fails to expose the point; the candidate supplies the necessary Zariski separation.

The rational substitution's denominator is \(r^4s^4\), nonzero on all regular real normals. Independent polynomial ideal-membership and auxiliary-circle elimination checks establish the identity. Saturation would be relevant to claiming an exact complex image ideal, but the manuscript only needs and only claims containment in \(V(P)\).

The segment and stadium examples correctly show that allowing one-dimensional summands can yield reducible exposed-point closures. The two stadium circle components are distinct for \(a>0\); the excluded limit \(a=0\) merges them. Single discs, repeated discs, products of discs, rank-two cases, and lower-dimensional sums all survive the other checks.

The inspected source script exits successfully under SymPy 1.14.0 and mpmath 1.3.0. Its output equals the recorded JSON. Additional exact checks use arbitrary rational unit targets and non-orthonormal killed-summand matrices, rather than only reproducing the original coordinate example. Evidence is preserved in [independent check code](algebra_independent_checks.py), [independent results](algebra_independent_results.json), [source rerun](checks_rerun.stdout.json), and [artifact consistency](algebra_artifact_consistency.json).

## Artifact and provenance checks

- The immutable candidate SHA-256 is `df5d9bd86562152cb72fd286055b62ded8ce0b4cdcf7d4a5ca1e001eb49ca47e`.
- Candidate, reviewed candidate, and PDF hashes agree with the PR's verification record. Mathematical Sections 2–6 are byte-identical to the earlier reviewed Markdown snapshot.
- All 154 mathematical blocks match between final Markdown and LaTeX after whitespace normalization. All five PDF pages were visually inspected, including the genericity condition and separating polynomial; no missing formula or mathematical transcription defect was found.
- The original source PDFs were independently downloaded, their relevant complete pages inspected, and their hashes match the PR's source audit. The [download manifest](primary_sources/download_manifest.json) records provenance. Third-party PDFs, extracted text, and rendering scratch files remain local and are excluded from the published review bundle.
- A fresh GitHub head check confirmed the same reviewed head remained open. This verdict is attached to that head, not to unknown future mathematical edits.

## Provisional queue finding withdrawn

An initial concern was that the changed `QUEUE.md` row at line 38 says `claimed_solved`, `1/5`, while `state.json` has no entry for this target. Actual PR-head `rank()` in an isolated, source-hash-verified one-record database regenerates the displayed row as `queued`, `0/5`. The source catalog was already eligible with that old state; the reproduction does not demonstrate a new eligibility change or live data loss. The [reproduction](reproduce_queue_finding.py) and [output](queue_reproduction.json) preserve this fact without changing the live queue.

An adversarial follow-up found material counterevidence to calling it a new PR defect: the base repository's `unsolved_math_prioritization/RESEARCH_LOG.md`, line 29, explicitly documents direct manual edits because the older generator would discard maintained live statuses and Chat/Findings/DOI columns. Fourteen manual active/claimed/published rows already existed at the base. The newer `apply_impact_scores.py` recognizes these statuses and preserves existing fields. The PR's readiness record says local accounting was required by its task instructions, and its committed `turns.jsonl` does preserve a durable one-turn ledger. Manual tracking therefore predates this PR, and this review cannot infer the author's separate user authorization from repository guidelines alone.

**The provisional P2 finding is withdrawn.** The old generator's incompatibility is a documented repository-wide conditional regeneration risk, not a mathematical error or a new merge blocker introduced by this proof. The [independent challenge](queue_finding_adversarial_check.md) records the classification and conflicting legacy workflow instructions. No queue/state correction is made by this review.

## Priority and recommendation

Fresh focused searches for mathematical discotope irreducibility, the exact conjecture number, analytic proofs, and later results did not identify a later primary-source resolution. The [original arXiv record](https://arxiv.org/abs/2111.01241) still lists v2, revised July 28, 2022. The official original sources and their generic conventions were checked directly. Some author-bibliography and talk-slide URLs were inaccessible through the web tool; a negative bounded search cannot certify priority or exclude unpublished work. The PR's existing historical-priority qualification is appropriate.

**No mathematical revision is requested.** The strongest verified result is the complete stated Theorem 1 plus Theorem 4 under (GP). No remaining mathematical gap was identified in those claims. Mathematical readiness to merge passes this audit; historical novelty, formal certification, and human peer review remain separate questions. The proof PR has not been merged or given a GitHub approval by this review.

Review completion estimate: **100%** of this requested audit, not 100% of a new-discovery or publication goal. Review notes are checkpointed on `main`; no outside individual was contacted, no release was created, and no DOI was minted.
