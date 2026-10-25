# Independent adversarial mathematical review — Zenodo 23358014

**Disposition: PASS for Theorem 1, Lemma 2 and Corollary 3 at their stated hypotheses.** No substantive mathematical defect or unresolved proof gap was identified. This is an independent AI mathematical review, not human peer review, formal proof verification, or a novelty/priority certificate.

Reviewed work: *Failure of strong quadratic growth in unregularized sparse control of a critical wave equation*, Alec Kriebel, version 1.0, dated 14 October 2026, six pages. The public PDF has SHA256 `a68d8d47dcf625f9ab8818924071200bff2b2280d67665e1e67dd7b83effe988`; the public source ZIP has SHA256 `1da933750640177045808de748dd7f5732c33277377285b688a411f9f89771a0`. The archive contains 113 regular files and no additional reader PDF or nested archive. Exact final custody, read coverage and evidence hashes accompany this report.

## Exact model, claims and adversarial targets

The spatial domain is the **unit ball in R³**, the time interval is [0,1], and H=L²(B). Controls and states are real. The equation is the defocusing Dirichlet equation y_tt−Δy+y⁵=u with zero position and velocity initial data. The state is the energy/Strichartz mild solution in the compatible space with position in C(H¹_0)∩L⁴(L¹²) and velocity in C(H). The constraint is **pointwise in time on the spatial H norm**: ||u(t)||_H≤ρ. It is not a pointwise bound on u(t,x). The notations A=||u||_1 and r=||u||_2 mean the Bochner L¹(0,1;H) and L²(0,1;H) norms, respectively.

The cost is terminal position tracking plus (ν/2)||y_t(1)||²_(H^−1), one quarter of the fourth power of the L⁴(L¹²) state norm, and A. Thus the sparse and state-penalty coefficients equal one, the quadratic control penalty equals zero, and ν is any **fixed finite nonnegative** coefficient. The target is d=πe, where e is the normalized first radial Dirichlet eigenfunction, −Δe=π²e.

The exact conclusions are:

1. There is a positive small-cap threshold ρ_* such that, for every fixed 0<ρ≤ρ_* and every finite ν≥0, zero is the unique global optimizer, with gap Δ(u)≥A³/(12ρ²).
2. The ordinary critical cone is {0}; strict positivity of the source's substitute second variation on nonzero cone directions is therefore vacuous.
3. The feasible centered pulses u_h=h e 1_(|t−1/2|<h) approach zero in L∞(H), have r_h²=2h³, and have gap (π²/3+2/π²)h⁴+O(h⁶). Consequently positive L²-squared growth fails in either L² or L∞ neighborhoods.
4. Global optimizers exist for all terminal targets in H in this small-cap model. For the radial targets (π+ε)e, every global optimizer has ||u_ε||_2/ε→∞ as ε decreases to zero.
5. Local L¹-squared growth survives: Δ(u)≥A²/(4π²) for A small. For arbitrary small target changes w, every optimizer has A=O(||w||_H) and r=O(sqrt(||w||_H)), uniformly in ν. Along the positive radial ray, every optimizer satisfies A=Θ(ε) and cε^(3/4)≤r≤Cε^(1/2), with a lower-bound neighborhood allowed to depend on fixed ν.

The review targeted false transfers from a linear mode to the nonlinear solution; missing critical-wave estimates; an incorrect cap or Bochner norm; cone/topology confusion; loss of compactness at criticality; a candidate control substituted for an actual optimizer; nonuniform constants silently treated as uniform; and overstatements of the original open question.

## Reading and independence

I read all six actual published PDF pages, the complete current TeX, and the original mathematical support `original_submission/COUNTEREXAMPLE.md`. I reconstructed the estimates and wrote and ran fresh falsification controls before inspecting the packaged checkers. Only after those controls succeeded did I read and run five relevant mathematical checkers, including the weaker-norm addendum controls, in isolated temporary copies.

I read the original three-page Oberwolfach contribution, the precise PDE/optimization interfaces in the pinned Kunisch–Meinlschmidt preprint, and the needed primary theorem statements and surrounding argument for the bounded-domain Strichartz estimate and classical comparison frameworks. The primary ledger states exact coverage; it does not claim every cited primary paper was read in full or reproved.

No current sibling or scope finding, dedicated historical assessment body, historical verdict, or priority audit body was read. Incidental exposure consisted of the published paper's own descriptions of internal reviews, the original mathematical support's header saying independent review was pending, source file names and opaque hashes, and status fields emitted by the selected mathematical checkers. These statuses were not accepted in place of proof. No source repair, website or spreadsheet change, Git operation, publication action, or external communication occurred.

## Independent reconstruction and attempted falsification

### Critical dimension and the small-input estimates

The load-bearing estimate is L: L¹(H)→Y for the zero-data linear wave, with ||Lu||_Y≤K||u||_1 on the fixed interval. The cited Kunisch–Meinlschmidt Lemma 2.9 states this energy plus L⁴(L¹²) estimate on a smooth bounded three-dimensional domain. Its underlying Blair–Smith–Sogge boundary theorem permits p=4,q=12,γ=1: the scaling identity is 1/4+3/12=3/2−1, and the boundary restriction is 3/4+2/12=11/12≤1. The smooth ball fits the hypothesis. No whole-space dispersive estimate is silently substituted for a bounded-domain estimate.

Spatial interpolation gives 1/10=(4/5)/12+(1/5)/6, while time interpolation uses four fifths of L⁴ and one fifth of L∞. With H¹_0 embedded in L⁶, this gives

||y||⁵_(L⁵L¹⁰) ≤ C ||y||⁴_(L⁴L¹²) ||y||_(L∞H¹_0).

More directly, four spatial L¹² factors and one L⁶ factor multiply into L², and four temporal L⁴ factors and one L∞ factor into L¹. These are precisely the critical exponents required for the quintic and its difference estimate. The quintic is a bounded polynomial from the compatible Y space to L¹(H).

On the zero-data compatible subspace, y↦L(u−y⁵) preserves a ball of radius 2KA and contracts for sufficiently small A. It follows that ||y_u||_Y≤EA and ||y_u−Lu||_Y≤RA⁵, with E,R independent of d and ν. The derivative of y+L(y⁵)−Lu at zero in y is the identity, so the local implicit-function argument has the correct compatible domain and yields S'(0)=L and S''(0)=0. It does not require a wave inverse onto arbitrary unrelated position and velocity pairs.

The contraction supplies the solution on the entire fixed interval for these small inputs. Its identification with the source mild solution is legitimate. Uniqueness within Y can also be checked locally in time: the quintic difference is bounded by the fourth power of the two states' L⁴(L¹²) norms times the difference's energy norm; partitioning time so those L⁴ norms are small permits absorption in the linear energy estimate. Thus no uncontrolled global well-posedness assertion is needed to fill the small-input proof. The paper does not assume that a nonlinear state forced along e remains a scalar multiple of e; y⁵ would in general mix modes.

### Global uniqueness and the cap-dependent lower bound

The radial eigenfunction normalization includes the actual ball volume factor: 4π∫_0^1 sin²(πr)/(2π) dr=1. Its apparent singularity at r=0 is removable, and it satisfies the Dirichlet boundary value. The linear projection formula follows from the scalar forced oscillator:

<e,z_u(1)> = (1/π)∫_0^1 sin(πt)<e,u(t)>dt.

For f(t)=||u(t)||_H, the cap gives 0≤f≤ρ, A≤ρ, A≤r and r²≤ρA. Since sin(πt) is nonnegative on this interval, projection and Cauchy–Schwarz yield the cost bound

Δ(u) ≥ ∫(1−sin(πt))f(t)dt−C_0 A⁵.

All discarded costs, including the velocity term, are nonnegative. Therefore C_0 is independent of ν. The inequality 1−sin(πt)≥2(t−1/2)² is valid throughout [0,1]. For b=A/(2ρ), comparing f with the centered saturated density ρ1_(|t−1/2|<b) gives ∫(t−1/2)²f≥A³/(12ρ²). The product used in the printed comparison is pointwise nonnegative both inside and outside the centered interval, including A=0 and A=ρ.

Consequently Δ≥A³/(6ρ²)−C_0 A⁵. If ρ≤ρ_* and C_0ρ_*⁴≤1/12, then C_0A²ρ²≤1/12, proving Δ≥A³/(12ρ²). For nonzero controls as Lebesgue equivalence classes, A>0, so zero is the unique global optimizer over the whole admissible set. This is not merely a stationary-point argument. The proof makes an existence choice of a sufficiently small positive cap; it does not invent a numerical Strichartz or nonlinear PDE constant.

### Cone, topology and pulse growth

In L¹(H) and L²(H), zero need not be an interior point of the pointwise capped set. The manuscript correctly proves the full tangent cone by bounded truncations of a direction, followed by sufficiently small scaling. Its cone calculation therefore does not rely on the invalid inference from pointwise slack to norm interiority.

At zero, the sparse subgradient λ(t)=sin(πt)e cancels the adjoint p(t)=−sin(πt)e, and the constraint multiplier is zero. The first directional derivative is

DJ(0;v)=∫(||v(t)||_H−sin(πt)<e,v(t)>)dt ≥∫(1−sin(πt))||v(t)||_H dt.

This is strictly positive for any nonzero L¹ or L² direction: the weight vanishes only at a single time, a null set. Hence C(0)={0}. The source really defines the substitute sparse j''(0;v²) as zero. It is not the classical Hessian of the nonsmooth norm. The strict condition on nonzero critical directions is satisfied vacuously and is described that way in the paper.

For a general e-mode pulse of amplitude a, center c and half-width b, independent integration gives terminal position coefficient 2a sin(πb)sin(πc)/π² and terminal velocity coefficient −2a sin(πb)cos(πc)/π. At c=1/2 the latter vanishes exactly. Setting a=b=h yields A_h=2h², r_h²=2h³ and the printed terminal position. The linear tracking-plus-sparse gap expands as

(π²/3+2/π²)h⁴−(π⁴/60+2/3)h⁶+O(h⁸).

The actual nonlinear position error is O(A_h⁵)=O(h¹⁰), the quartic state cost O(h⁸), and the velocity cost O(νh²⁰). For fixed finite ν these do not alter the leading term or the stated O(h⁶) remainder. Thus Δ/r_h² tends to zero even though ||u_h||∞=h tends to zero. Both source neighborhood formulations are genuinely covered.

The normalized v_h=u_h/r_h is weakly null in L²(H): its pairing with any L² test is bounded by that test's norm on the shrinking pulse support. The displayed second-order expression tends to zero with coefficient π²/6+1/π². The velocity part of F'' vanishes on this centered sequence, while the quartic state's second derivative at zero is zero. These computations are consistent with the known nondegeneracy obstruction; they are not a claim that strengthened sufficient conditions fail.

### Existence is for actual nonlinear optimizers

U_ρ is closed, convex and bounded in the Hilbert space L²(H), hence weakly sequentially compact. Along any minimizing sequence, the small-input estimates give uniform energy and L⁴(L¹²) bounds. Compact H¹_0→H and the uniform bound on y_t give compactness of positions in C(H). The equation and the pointwise control cap also bound y_tt in L∞(H^−1): Δy is energy-controlled, y⁵ belongs to L∞(L^(6/5)), and L^(6/5) embeds in H^−1. The compact embedding H→H^−1, together with this equicontinuity, gives velocity compactness in C(H^−1). The optional terminal velocity cost is therefore continuous along the extracted subsequence.

Almost-everywhere convergence of positions, with bounded quintics in the reflexive space L^(6/5) over the finite spacetime cylinder, identifies the weak nonlinear limit as y⁵. The limit retains the weak energy and mixed-norm bounds; interpolation therefore puts its quintic in L¹(H), as required for Duhamel. Distributional passage gives the equation and the strong endpoint convergences preserve the initial traces. Subtracting the linear Duhamel solution with forcing u−y⁵ leaves a homogeneous Dirichlet wave with zero data. Testing its coefficients against a complete Dirichlet eigenbasis proves it is zero. This identifies the limit with the actual mild state in Y, rather than an arbitrary weak solution.

Finally the endpoint costs converge, and the sparse and quartic norm terms are weakly lower semicontinuous. The direct method proves existence for every d∈H and every finite ν≥0 at the fixed small cap. Criticality is addressed through the mixed norm and nonlinear-limit identification, not ignored by a generic compactness assertion.

### Target perturbations and every-optimizer quantifiers

Hold ρ fixed and put a=ρ/2. The comparison pulse has half-width πε/(2a), which is feasible and contained in the time interval for sufficiently small ε>0. Its mass is πε, its linear endpoint is εe+O(ε³), and its linear terminal velocity is zero. Independent expansion gives linear perturbed gap −ε²/2+(π⁵/(24a²))ε³+O(ε⁵). The quartic state term is O(ε⁴), the nonlinear endpoint error O(ε⁵), and the optional velocity cost O(νε¹⁰). Thus the actual gap is at most −ε²/4 eventually, for each fixed ν. This is a comparison control, not an asserted optimizer.

For every feasible control, the lower estimate uses g_ε=[(1+ε/π)sin(πt)−1]_+. It obeys g_ε≤[ε/π−2(t−1/2)²]_+. The height-times-square-root-support estimate gives ||g_ε||_2≤2^(1/4)π^(−5/4)ε^(5/4); the exact integral of the squared enclosing parabola is smaller, confirming the stated constant is safe. The cost lower bound is −||g_ε||_2 r−C_1A⁵.

If a global optimizer had r≤Kε for a fixed K, then A≤r and this lower bound would be −O_K(ε^(9/4))−O_K(ε⁵)=−o(ε²), incompatible with the comparison pulse's negative quadratic improvement. Because the contradiction excludes **all** optimizers with that norm for each fixed K, it proves the stated divergence for every selection of global optimizers. It does not require perturbed uniqueness.

### Weaker growth, nonradial changes and uniformity

Let x=<e,y_u(1)> and b=A/π+RA⁵. The estimate x≤b is one-sided; no lower bound on x is assumed. Orthogonal projection of the tracking square gives Δ≥q_A(x)=A−πx+x²/2. On x<π this function decreases. Choosing A≤δ with b≤π/2 makes q_A(x)≥q_A(b) valid even for negative x. Direct expansion gives

q_A(b)=A²/(2π²)−πRA⁵+(R/π)A⁶+(R²/2)A¹⁰.

The condition πRδ³≤1/(4π²) proves the local A²/(4π²) growth. There is no silently omitted monotonicity domain.

For a target πe+w, comparison of a global optimizer with zero gives the exact inequality Δ(u)≤<w,y_u(1)>≤E||w||_H A. The cubic bound first gives A≤sqrt(12ρ²E||w||_H), placing A in the local neighborhood uniformly in ν. The quadratic bound then improves this to A≤4π²E||w||_H, and r²≤ρA gives r≤2πsqrt(ρE)sqrt(||w||_H). All these bounds discard nonnegative velocity costs, so their uniformity in ν is justified.

Along w=εe, the now-known A=O(ε) makes the nonlinear lower-bound error O(ε⁵). Comparison with −ε²/4 then forces r≥cε^(3/4). Using ||g_ε||∞≤ε/π similarly gives A≥c'ε, completing A=Θ(ε). The smallness threshold of the negative comparison pulse can depend on fixed ν; the manuscript explicitly allows that dependence. It does not assert a uniform radial lower-rate neighborhood as ν tends to infinity.

## Primary-source checks and attribution

The primary-source ledger binds the following exact raw versions and reading scope.

- Kunisch–Meinlschmidt, arXiv:1907.02744v1 (5 July 2019): model and function spaces; Lemma 2.9 and its Duhamel setting; local uniqueness/existence interfaces; Theorem 3.7 statement; control-space convention r=1 when β_2=0; Proposition 4.4; Lemma 4.6; ordinary cone and substitute j'' definitions; Theorem 4.17 and its L∞ localization. Its quadratic-control assumption is explicit. This is the pinned proof version, not an unverified substitution of the final journal body. https://arxiv.org/pdf/1907.02744v1
- Original Oberwolfach Report 9/2021 contribution, printed pp.438–440, read in full. It includes the optional H^−1 terminal velocity cost, states the strong L² growth implication, and places the β_2=0 question immediately after it. The present result answers retaining that implication unchanged. It does not claim to settle every possible β_2=0 theory. https://publications.mfo.de/bitstream/handle/mfo/3850/OWR_2021_09.pdf
- Blair–Smith–Sogge, published 2009 body, Theorem 1.1 and surrounding bounded-boundary/inhomogeneous discussion: the exact L⁴(L¹²) energy exponents are admissible on this compact smooth domain. L¹(H) forcing also follows from homogeneous estimates and Duhamel/Minkowski, with constants for the fixed finite interval. https://www.numdam.org/article/AIHPC_2009__26_5_1817_0.pdf
- Casas–Tröltzsch 2015, Example 4.16 and following extended-cone discussion: the Dunn example already demonstrates exact-cone insufficiency, even with a coercive condition on the exact cone. It is not the same nonlinear-wave realization. Historical credit is appropriate; this review did not read Dunn's original paper or the separate 2012 Casas–Tröltzsch body. https://www.mathematik.de/images/DMV/Jahresberichte/Jahresberichte_Archiv/2015.117Heft1.pdf
- Christof–Wachsmuth author v1, Theorem 4.4 and NDC; Borchard–Wachsmuth author v1, Theorem 2.6 and its NDC expression; Wachsmuth–Wachsmuth author v1, introduction and weaker-L¹-growth framework. These establish the relevant distinction and prevent presenting the concentration mechanism as new. No theorem from these frameworks is required to prove the displayed counterexample. https://arxiv.org/pdf/1707.07579v1 ; https://arxiv.org/pdf/2311.14538v1 ; https://arxiv.org/pdf/2111.10238v1
- Herzog–Stadler–Wachsmuth 2012, mixed-norm sparsity/subgradient context; Casas–Herzog–Wachsmuth 2017, extended-cone definition (5.1) and surrounding sufficient-condition distinction. These were checked as credit/context, not transplanted from parabolic or box-constrained models to the wave equation. https://math.nyu.edu/~stadler/papers/HerzogStadlerWachsmuth12.pdf ; https://numdam.org/item/10.1051/cocv/2015048.pdf

The core source interfaces are authenticated and fit the exact assumptions. The nonlinear-wave realization is distinguishable from the classical abstract mechanism, but this bounded reading is not a worldwide priority search and does not certify continued openness or firstness. The paper's own bounded-audit statement is not used as independent evidence of novelty.

## Fresh controls and submitted replay

`fresh_controls.py`, written before submitted-helper reading, passed **13,201 exact rational/symbolic assertions** and **428 separately identified 80-digit numerical diagnostics**. Exact controls exhaust all 6,561 densities with levels {0,1/2,1} on eight time cells, using exact cell integrals, and check both moment and norm inequalities. They include empty/full masses and saturated comparators at three rational caps, general-center pulse kernels, eigenfunction normalization and boundary/origin behavior, series coefficients, the exact enclosing-parabola integral, the L¹-growth polynomial identity, and the critical Hölder/boundary-exponent arithmetic.

An additional amplitude-width family computes the normalized powers for amplitude h^α and half-width h^β. It confirms the displayed choice α=β=1 and distinguishes the threshold α<2β from choices where the first-order ratio does not tend to zero. Negative diagnostics show that shifting the pulse to quarter time loses the cancellation, and reinstating a positive quadratic control penalty adds its positive constant to the normalized gap. High-precision tests of actual g_ε and asymptotic coefficients are explicitly numerical diagnostics, not certified analytic inequalities or PDE simulations.

Five selected unmodified packaged mathematical checkers then passed, totaling **5,575 submitted assertions**: author3937, original_independent1385, source17, variational215 and addendum21. They cover rectangular and triangular pulses, threshold integrals, rational moment controls, the actual weaker-norm constants and target-change identity. All mathematical JSON output fields matched the archived reference output; only dynamically emitted UTC fields were excluded in source17 and addendum21. Python 3.14.6, SymPy 1.14.0 and mpmath 1.3.0 were used. The pinned dependency versions were satisfied.

The selected helpers were inspected and executed in temporary isolated copies with assertions enabled and bytecode writes disabled. No full historical priority/status wrapper or unrelated audit script was run. All 113 extracted source-file hashes were checked before and after, and final custody rechecks the ZIP and manifest against those same bytes. Finite control counts do not prove nonlinear PDE well-posedness, compactness, unknown constants, or the universal optimizer quantifiers; the analytical reconstruction above addresses those requirements.

## Strongest supported result and exact remaining gap

The strongest supported result is the full stated small-cap example: an actual unique nonlinear-wave optimizer with zero ordinary critical cone and no strong L²-squared growth, plus existence and every-optimizer target-displacement bounds, while local L¹-squared growth survives. **No remaining mathematical gap was identified in these scoped claims.**

The review does not establish a numerical value of ρ_*, sharpness of the ε exponent bracket, perturbed optimizer uniqueness, pairwise Lipschitz selection, L∞ convergence of perturbed optimizers, failure for every target or cap, a negative coefficient ν, or other PDEs/dimensions/constraints. In particular, target zero has J_(0,ν)(u)≥A≥r²/ρ, so unregularized growth does not fail universally. The claimed obstruction concerns the unchanged ordinary-cone implication, not strengthened-cone or weaker-norm theories. No firstness or human-peer-review claim is warranted by this review.
