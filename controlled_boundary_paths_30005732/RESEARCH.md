# Controlled moving sets: research checkpoint

Row 1845, ID 30005732. Status: UNSOLVED; five research approaches completed. Original optimal-motion question not solved.

## Scope fixed from original source
OWR 52/2023, printed p.2959, Q1 asks regularity of optimal sets and whether boundary-orthogonal trajectories needed for necessary conditions can always be defined. This is not a sweeping-process existence problem, and a counterexample among arbitrary admissible trajectories does not settle it. The later survey arXiv:2502.06050, section 5, Problem 2 retains the corresponding optimal-motion regularity problem. Survey assumption (A5) is joint C^{1,1} space-time regularity, a nondegenerate boundary parametrization, and normal trajectories. Convex spatial C^{1,1} slices alone do not prove (A5).

The five approaches examined are: (1) orthogonal reparametrization ODE; (2) lower regularity and uniqueness thresholds; (3) BV trace/superposition formulation; (4) optimality-based special cases; (5) exact admissible counterexamples and endpoint/topology obstructions. No claim of full resolution will be made without optimality proof and matching quantifiers.

## Approach 1: remove tangential velocity by an ODE

Let I be a compact time interval on which the boundary has fixed topology, and let Y:I×S¹→R² be a smooth family of embeddings with |Y_s|≥m>0. Define

F(t,s)=−(Y_t·Y_s)/|Y_s|²,
φ_t(t,ξ)=F(t,φ(t,ξ)), φ(t₀,ξ)=ξ,
X(t,ξ)=Y(t,φ(t,ξ)).

The chain rule gives X_t·Y_s=Y_t·Y_s+|Y_s|²F=0, so X_t is normal to the boundary. The scalar flow φ is an orientation-preserving diffeomorphism: φ_ξ=exp(∫F_s(t,φ)dt)>0. Thus X parametrizes the same boundary without tangential velocity. This gives a complete conditional construction, not an optimal-motion regularity theorem. For smooth Y everything is smooth; Y∈C^{2,1} is a safe sufficient hypothesis for joint C^{1,1} X on a compact nondegenerate cylinder. If Y is merely joint C^{1,1}, F is Lipschitz and the ODE still has a unique bi-Lipschitz label flow; do not automatically promote that flow to C^{1,1}, because differentiability in initial labels needs more than a Lipschitz vector field. In particular, “reparametrize” does not itself establish the survey’s full (A5).

Obstruction to finishing: the finite-perimeter existence theorem does not supply the starting cylinder Y, fixed boundary topology, or the necessary time/space estimates. Assuming them would assume the principal missing conclusion.

## Approach 2: uniqueness thresholds and a precise local failure

A weaker conditional version takes F measurable in t, continuous in s, |F(t,s)|≤a(t), and |F(t,s)−F(t,r)|≤L(t)|s−r|, with a,L∈L¹(I). The Carathéodory ODE gives a unique absolutely continuous label flow; Gronwall yields exp(−∫L)|ξ−η|≤|φ(t,ξ)−φ(t,η)|≤exp(∫L)|ξ−η| on compatible lifts. With enough regularity of Y for the AC chain rule, this yields AC normal paths. An integrable Osgood modulus can replace the Lipschitz modulus for uniqueness, but these are sufficient assumptions, not a proven minimal characterization and not consequences of the control budget.

An exact local geometric example shows why C¹ boundaries alone do not suffice for uniqueness. Translate the graph Y(t,s)=(s,t−(2/3)|s|^{3/2}) upward. Then

F(s)=sgn(s)√|s|/(1+|s|).

From φ(0)=0, one solution is φ≡0. For any waiting time a≥0 another has φ(t)=0 for t≤a and φ(t)=q(t)>0 thereafter, where

t−a=2√q+(2/3)q^{3/2}.

The negative branch works as well. Each X=Y(t,φ) has normal velocity by the preceding calculation. The graph is C^{1,1/2}, not C^{1,1}; the nonuniqueness is genuine, not a failure of a theorem’s hypotheses alone. A compact C¹ Jordan boundary can contain this graph patch and be smooth elsewhere; translating that entire bounded domain at unit speed gives |β|≤1 and effort P, because ∫∂Ω β dσ=0. Hence taking M=P produces an admissible example with local nonunique normal paths. This is not an optimality counterexample.

Obstruction to finishing: spatial normal continuity and an integrated effort bound give no integrable Lipschitz/Osgood modulus for the moving normal field. The local example tests weakened assumptions only.

## Approach 3: BV normals, transport, and superposition

The finite-perimeter formulation encodes a space-time characteristic function and its measure-theoretic normal. Where the spatial normal component is nonzero, its ratio with the temporal component recovers a scalar normal speed (with the source’s orientation convention). This is an Eulerian flux description almost everywhere, not a pointwise path parametrization.

One might try to use a superposition principle: obtain a nonnegative measure μ_t supported on ∂Ω(t), and a Borel field b=β n satisfying ∂_t μ_t+div(b μ_t)=0 with the required integrability. A continuity-equation solution can then admit a measure on AC integral curves. But the supplied perimeter measure μ_t=H¹|∂Ω(t) does not generally satisfy this conservative equation. Already for a shrinking circle its total mass is 2πR(t), whereas a conservative continuity equation preserves mass. A curvature/source term or a transported label density would be needed. Constructing that density without an existing flow is part of the missing work. Topology change can destroy whole components of boundary labels. Even successful superposition gives a measure on curves, usually almost-everywhere statements, not unique curves from every point or a nondegenerate C^{1,1} cylinder.

Primary reference checked: Stepanov and Trevisan, “Three superposition principles: currents, continuity equations and curves of measures,” https://arxiv.org/abs/1512.05109. Its continuity-equation hypothesis is substantive and cannot be replaced by finite perimeter of the moving set. No new superposition theorem is claimed here.

Obstruction to finishing: neither the appropriate conserved boundary-label measure nor uniqueness and pointwise coverage follows from the existing admissibility data. General sweeping-process results address different dynamics and do not repair this gap.

## Approach 4: use optimality, convex results, and an exact disk

Bianchini–Bressan–Chiri, arXiv:2307.03599, Theorem 5.1 constructs an admissible optimal motion for bounded open convex initial sets and proves area domination over every other admissible strategy. Its introduction covers terminal and integrated area objectives. The survey’s Theorem 7.1 records spatial C^{1,1} boundaries for 0<t<T in the convex minimum-time problem. These results are not statements of joint space-time C^{1,1} normal coordinates for general initial sets. In particular, the source explicitly separates the finite-perimeter existence theorem from the assumptions required for its maximum principle.

For an initial disk of radius R₀ and M>2πR₀, put k=M/(2π). The centered disk trajectory obeys

R'=1−k/R,   0<R≤R₀.

Its inward speed is β=k/R−1≥0 and its effort is 2πR(1+β)=M. Its area A=πR² obeys A'=2πR−M. The convex theorem specializes to this concentric disk evolution: the one-step perimeter minimizer inside the expanded disk is a disk of the prescribed area; the concentric choice fits the admissible construction. Alternatively, in the class where the weak area balance A'≥P−M holds, the planar isoperimetric inequality gives A'≥2√(πA)−M and scalar comparison up to positive-area times proves the disk’s area minimality. The latter route explicitly requires that balance; it is not asserted for arbitrary representatives of an unspecified weak class.

The extinction time is

T*=k log(k/(k−R₀))−R₀.

As t↑T*, R(t)~√(2k(T*−t))=√(M(T*−t)/π). Radial boundary paths X(t,θ)=R(t)(cosθ,sinθ) are smooth before extinction and absolutely continuous up to their limit at the origin, since ∫₀^{T*}|R'|dt=R₀. Their speed diverges near extinction, so they are not Lipschitz up to extinction. If Ω(T*) is chosen to be empty, their endpoint limit is not in ∂Ω(T*). If the singleton representative is used instead, the paths reach its topological boundary, but the parametrization degenerates and the reduced boundary is empty. For any later time with Ω(t)=∅, boundary paths cannot continue. Choosing a horizon T>T* yields a terminal-area minimizer with an interior extinction time, simply because its terminal area is zero.

This identifies essential qualifications (positive-area phase, representative of the set, endpoints and extinction) in any literal “always” formulation. It does NOT resolve the intended nondegenerate interior optimal-motion regularity question: on every compact subinterval before extinction, this example has perfectly smooth normal coordinates. Do not label the original open problem solved via this endpoint issue.

## Approach 5: exact admissible tests, topology, and representatives

### A. An optimal critical-budget disk: smooth slices need not give joint C¹ time regularity
Let Ω(t)=B_R(c(t)) with c(t)=a(|t−t₀|−t₀)e₁, 0<a≤1. For t≠t₀ and outer radial direction e, β(t,e)=−c'(t)·e∈[−a,a]. Thus β≥−1 and ∫(1+β)dσ=2πR. With M=2πR it is admissible in the a.e.-time weak setting, and t↦1_Ω(t) is Lipschitz into L¹. Every slice is C∞. At t₀ the required one-sided normal velocities differ by 2a(e₁·e)e, so any jointly C¹ normal parametrization covering points with e₁·e≠0 is impossible. Unique AC normal curves do exist here, since their angle solves a scalar ODE with measurable time dependence and spatially Lipschitz coefficient. Therefore this example disproves promotion of slice regularity to joint C¹, not existence of AC curves.

In fact this example IS optimal for the terminal-area problem at the critical budget M=2πR. The stationary disk has area A₀=πR² and effort M. It is the concentric-disk specialization of the convex optimal construction in Theorem 5.1 of Bianchini–Bressan–Chiri: in (5.3), a(t)≡A₀ solves a'=2√(πa)−M=0, and the fixed disk lies in the t-expanded initial disk. Hence no admissible competitor has terminal area below A₀. The translating disk has exactly A₀ at every time and is therefore also optimal, including for nonnegative integrated-area-plus-terminal objectives. One can also prove this via A'≥2√(πA)−M, provided the weak area balance holds in the stated comparison class: the scalar equilibrium A=A₀ is locally Lipschitz in positive area, and comparison prevents A from crossing below A₀. Fix 0<a<1 if strictly positive control density everywhere is desired.

This is a genuine optimal counterexample to a universal claim that EVERY optimal motion admits joint C¹ (and thus C^{1,1}) normal coordinates across all positive-area interior times. It is NOT a counterexample to existence or uniqueness of AC normal paths, and NOT a counterexample to existence of a regular optimal motion for the same data: the stationary disk is smooth. Thus it sharpens the quantifier/regularity issue in Q1 without resolving its intended weakest normal-trajectory or regular-optimal-selection formulation.

### A2. Stronger all-times version: continuous speed but no joint C^{1,1}

To avoid any ambiguity about normal speed at the reversal time, replace the preceding center by

c(t)=ε(|t−t₀|^{3/2}−t₀^{3/2})e₁,

where 0<t₀<T and (3ε/2)√max(t₀,T−t₀)<1. This center is C¹, with

c'(t)=(3ε/2)sgn(t−t₀)√|t−t₀| e₁, and c'(t₀)=0.

The moving disk has a continuous normal speed at EVERY time, β(t,e)=−c'(t)·e, and β>−1. Its effort is exactly 2πR at every time. At critical budget M=2πR its constant area is optimal by the same stationary-disk comparator proved above. Thus this version respects the original pointwise-in-time speed/effort formulation, not only the weak a.e.-time formulation.

Suppose it had a joint C^{1,1} normal parametrization X covering the full boundary on a neighborhood of t₀. Write e(t,ξ)=(X(t,ξ)−c(t))/R. Differentiating |X−c|²=R² and using that X_t is normal gives

X_t(t,ξ)=(c'(t)·e(t,ξ))e(t,ξ).

Choose a label ξ₀ with e(t₀,ξ₀)=e₁. At t₀, X_t(t₀,ξ₀)=0. By continuity, e₁·e(t₀+h,ξ₀)≥1/2 for sufficiently small h>0; hence

|X_t(t₀+h,ξ₀)|≥(3ε/4)√h.

Joint C^{1,1} would instead imply |X_t(t₀+h,ξ₀)−X_t(t₀,ξ₀)|≤Lh. These inequalities contradict one another as h↓0. Therefore NO such joint C^{1,1} normal parametrization exists, regardless of the initial labeling.

There is nevertheless a joint C¹ normal parametrization. With e(θ)=(cosθ,sinθ), τ(θ)=(−sinθ,cosθ), let

θ_t=−c'(t)·τ(θ)/R,
X(t,ξ)=c(t)+R e(θ(t,ξ)).

The angular field is continuous in time and smooth with uniformly bounded derivatives in θ. Its unique flow is continuously differentiable in labels and time; its positive label derivative gives a nondegenerate parametrization. The chain rule verifies X_t=(c'·e)e. Thus the obstruction is specifically the Lipschitz regularity of the time derivative demanded by (A5), NOT well-definedness or uniqueness of normal trajectories. A smooth stationary optimal selection remains available for the same data. This example does not settle the full Q1/Problem 2.

### B. A whole boundary component disappears with positive budget
Fix 0<r₀<R and let r(t)=(r₀−t)_+. For t<r₀ set Ω(t)={r(t)<|x|<R}; for t≥r₀ set Ω(t)=B_R. The outer circle is stationary, β=0 and effort 2πR. On the inner circle the inward normal of the annulus is +e_r; r'=-1, hence β=-1 and zero effort. Take M=2πR>0. The motion is L¹-Lipschitz, since its area derivative before closure is 2πr(t), and it has finite-perimeter space-time boundary. Every inner normal path has fixed angle and tends to the origin. After closure the only boundary is |x|=R. No such path admits a continuous boundary-valued continuation through closure; the failure affects the entire initial inner component. With the open-disk representative it already fails at closure itself. With a punctured-disk representative at that one time it still fails immediately afterward. The reduced-boundary formulation also has no inner component at closure. This is an admissible positive-budget topology obstruction, not an optimal trajectory counterexample.

The topology example explains why a fixed collection of circles and nondegenerate embedding flow cannot describe all admissible motions. A valid optimality theorem would need either to prevent such events or to allow creation/termination of labels and exceptional times. Neither conclusion has been established for general optimal initial sets in this research.

## Current verdict

Five substantive approaches completed. Conditional smooth/AC constructions and exact scoped counterexamples are proved above, including optimal critical-budget disks refuting universal joint-C¹ regularity in the weak a.e.-time setting and universal joint-C^{1,1} regularity even with continuous, all-times normal speed. The general optimal, nondegenerate interior regularity/normal-path problem remains unresolved here. The result is a precise hypothesis audit, an optimal non-C¹ time example, and explicit tests against invalid generalizations, not a full solution to the original open question. Independent auditor verified the strengthened continuous-speed critical-disk proof, including the √h versus h contradiction, joint C¹ normal-path existence, and critical-budget optimality. The complete independent mathematical audit is included as AUDIT_CONTROLLED_BOUNDARY_PATHS.md.

## Source identifiers (no source-text publication intended)
- Alberto Bressan, “Optimal control strategies for moving sets,” Oberwolfach Report 52/2023, printed pp.2958–2960; Q1 on p.2959.
- Alberto Bressan, “Results and open questions on the boundary control of moving sets,” https://arxiv.org/abs/2502.06050, §5 (A5), Problem 2, and Theorem 7.1.
- Stefano Bianchini, Alberto Bressan, Maria Teresa Chiri, “Optimal Solutions for a Class of Set-Valued Evolution Problems,” https://arxiv.org/abs/2307.03599, Definition 1.1 and Theorem 5.1.
- Eugene Stepanov, Dario Trevisan, “Three superposition principles: currents, continuity equations and curves of measures,” https://arxiv.org/abs/1512.05109.

The survey arXiv record inspected on 2026-10-21 lists v1 dated 2025-02-09. The June 2026 publication metadata was independently verified at the author’s university record: https://pure.psu.edu/en/publications/results-and-open-questions-on-the-boundary-control-of-moving-sets/ . It lists Journal of Mathematical Sciences 300(2), 122–150, DOI https://doi.org/10.1007/s10958-026-08509-w . This confirms publication metadata; the inspected Problem 2 text is the arXiv version, not a separately compared publisher PDF.
