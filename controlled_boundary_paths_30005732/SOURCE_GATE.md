# Source gate: ordered row 1845

Identity: ID 30005732 / OWR-14298011-003, “Well-Defined Trajectories in Controlled Set Motions.” Checked 2026-10-21 UTC. Verdict: exact problem recovered; general regularity/orthogonal-trajectory question remains open in inspected later primary literature. No mathematical resolution claimed.

## 1. Exact source and target

Alberto Bressan, “Optimal control strategies for moving sets,” in Control Methods in Hyperbolic PDEs, Oberwolfach Report 52/2023, pp. 2958–2960. Q1 is on printed p. 2959 (PDF page 19). Report volume year is 2023; publication date is 23 July 2024. Official source: https://ems.press/journals/owr/articles/14298011 and https://ems.press/content/serial-article-files/48173 .

The question concerns regularity of optimal planar regions and whether their boundaries admit trajectories t ↦ x(t,ξ) ∈ ∂Ω(t) orthogonal to each instantaneous boundary. The context is the regularity needed for necessary optimality conditions, not existence of a point trajectory inside a prescribed moving constraint.

The basic OP fixes T, M and bounded Ω₀⊂R², minimizes |Ω(T)|, and controls the inward normal speed β(t,x), with β≥−1 and ∫∂Ω(t)(1+β)dσ≤M. No control means β=−1, hence unit outward expansion. The preceding general functional also includes running area and effort costs, with E(β)=max(1+β,0), and either quadratic effort penalty or a hard effort bound. The abstract does not impose convexity in Q1. Its preceding convexity theorem is a special result, not an additional hypothesis silently inherited by every open question.

## 2. State space, controls and weak dynamics

The cited foundational paper is Bressan–Chiri–Salehi, Optimal Control of Moving Sets, J. Differential Equations 361 (2023), 97–137; inspected preprint: https://arxiv.org/abs/2201.01723 (v1).

Its §2 uses bounded finite-perimeter space-time sets Ω⊂(0,T)×R², so 1Ω∈BV. Time slices are represented in L¹(R²), with one-sided endpoint traces; equality is modulo planar null sets. The natural slice distance is |A△B|, not Hausdorff distance. Weak normal velocity uses the generalized inward space-time normal ν: β=−ν₀/√(ν₁²+ν₂²). Effort is encoded by the measure √(ν₁²+ν₂²)E(β)H² restricted to the reduced boundary; its time projection must have density ℰ(t). This formulation does not presuppose classical boundary-point paths.

Theorem 4.1 proves existence for compact finite-perimeter initial data under convexity/coercivity assumptions on E and φ, with positive running/terminal coefficients. It must not be cited without checking coefficients as a literal theorem for every variant of terminal-only OP. §5 assumes a nondegenerate C² parametrization and continuous β satisfying x_t=βn. §6 allows certain piecewise-smooth extensions. These hypotheses are assumptions in the necessary-condition argument, not regularity proved for all weak minimizers.

## 3. Precise bounded-effort formulation and distinctions

Bianchini–Bressan–Chiri, Optimal Solutions for a Class of Set-Valued Evolution Problems, https://arxiv.org/abs/2307.03599 (v1), Definition 1.1: admissibility requires t↦1Ω(t) Lipschitz into L¹(R²), and ∫∂Ω(t)max(1+β,0)dH¹≤M for almost every t. Its OP permits nonnegative running/terminal coefficients, including the terminal-only case. The OWR writes its smooth constraint at every t; do not conflate that exposition with the a.e. weak formulation. The preprint effort extension permits β<−1 at zero effort; the OWR basic OP explicitly imposes β≥−1.

Our audit distinction: an L¹-continuous trajectory of sets is not a boundary-orthogonal Lagrangian flow. Null-set representatives do not determine topological boundaries. Existence of optimal sets, existence/uniqueness of a boundary characteristic from each label, and uniqueness of the optimizer are three separate assertions. Q1 does not state a standalone quantified uniqueness theorem. A smooth ODE theorem cannot close the gap by assuming the very joint regularity being sought.

Also, d|Ω|/dt=Per(Ω)−M uses saturated effort. For a smooth admissible unsaturated motion the correct identity is Per(Ω)−ℰ(t), hence only ≥Per(Ω)−M follows from the budget alone.

## 4. Later status and exact regularity gap

Bressan, Results and Open Questions on the Boundary Control of Moving Sets, https://arxiv.org/abs/2502.06050 (v1, February 2025), §5, pp.16–17, explicitly retains this issue as Problem 2. Assumption A5 requires a jointly C¹,¹ map (t,ξ)↦x(t,ξ), derivative bound 1/C≤|x_ξ|≤C, and x_t=βn with continuous β. It contrasts this with finite-perimeter existence and asks to justify orthogonal curves for optimal sets. Thus the required regularity is space-time parametrization, not merely smoothness of each fixed-time slice.

The survey's Theorem 7.1 gives spatial C¹,¹ boundaries for interior times in the bounded open convex minimum-time case, alongside maximal-curvature control. That special result does not supply a general nonconvex joint parametrization. Publication metadata now lists the survey in Journal of Mathematical Sciences 300(2),122–150, June 2026, DOI https://doi.org/10.1007/s10958-026-08509-w . Metadata verified at https://pure.psu.edu/en/publications/results-and-open-questions-on-the-boundary-control-of-moving-sets/ ; final publisher text was not inspected, so no assertion of verbatim identity with the preprint is made.

Bressan–Marchini–Staicu, Optimally Controlled Moving Sets with Geographical Constraints, https://arxiv.org/abs/2502.05968 , published Milan J. Math. 93 (2025),263–329, https://doi.org/10.1007/s00032-025-00419-x , §17 expressly leaves regularity open. It conjectures an interior-ball property for a.e. time and treats the BV-to-classical gap as unresolved. Geographic constraints change admissibility, so this is corroborating context, not an equivalence theorem.

The dataset's cited Bianchini–Zizza spiral-barrier article https://arxiv.org/abs/2508.05324 concerns a firefighter constructing a spiral wall at bounded construction speed, not normal-speed-controlled boundaries of arbitrary optimal contaminated sets. Its abstract does not resolve this question. Neither that result nor generic sweeping-process theory should be substituted for Q1.

## 5. Evidence and disposition

Official OWR page 2959 was rendered and visually checked, including OP, speed sign, effort formula, and Q1. Copied source PDFs, extracted source text, and dataset excerpts are excluded from this package. SOURCE_METADATA.json records public retrieval URLs, bytes and SHA-256 hashes. DATASET_METADATA.json records fresh hashes and exact-ID match counts of the existing local corpus; it does not claim fresh dataset download. No dataset contents are included.

Resolution disposition: source gate passed; current evidence supports “open in inspected primary literature,” not solved and not a proof of absence of all later work. Searches covered exact title, cited foundational and convex papers, Bressan's publication pages, the later survey, and geographical-constraint development. This checkpoint makes no claim of exhaustive coverage of later literature.
