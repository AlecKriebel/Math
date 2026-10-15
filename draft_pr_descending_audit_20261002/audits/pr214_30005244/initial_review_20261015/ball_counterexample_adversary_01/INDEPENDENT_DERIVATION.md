# Independent derivation, frozen before inherited review comparison

Recorded before reading any earlier independent-review files. The reconstruction below derives the submitted mechanism; it makes no author proof edits.

## Exact object and falsifiable checks

On B={|x|<1}, H=L²(B;C³), A₀ is the compression of the whole-space longitudinal Fourier projection Q(ξ)=ξξᵀ/|ξ|²; S₀=A₀−I/3. For real κ=10⁻⁴, check a rank-three cluster of Sκ with at least one nonreal eigenvalue. Then check its persistence on a compact positive-measure nowhere-dense F_j while every rational sampling grid sees only an added volume-null origin. A counterexample must use Sκ=Aκ−I/3 and the source's omitted diagonal, and its surviving continuum eigenvalue must lie off the real lattice interval.

## Ball decomposition and gap

The gradient image of H¹(B)/constants is closed by Poincaré. Dirichlet projection of any potential gives the orthogonal decomposition ∇H¹=∇H₀¹ ⊕ ∇H_harm¹. The orthogonal complement of ∇H¹ consists exactly of fields whose zero extension has zero distributional divergence: testing restrictions of whole-space smooth functions gives one direction, and density of smooth functions on the closed ball in H¹ gives the reverse. This is the weak divergence-free/zero-normal-flux summand.

For ∇v with v∈H₀¹, zero extension equals ∇(zero-extended v), so Q acts as identity; on the complement Q acts as zero. For solid harmonic H_l=r^lY_l (l≥1), div(1_B∇H_l)=−lY_l δ_{∂B}. The positive Newton single layer of Y_l equals H_l/(2l+1) inside B, since matching c r^l and c r^(−l−1) gives the outward derivative jump −(2l+1)c=−1. Hence −∇g*div(1_B∇H_l)=l∇H_l/(2l+1). Orthogonality follows from Green's formula and spherical harmonic orthogonality. Harmonic H¹ expansion converges in the Dirichlet norm, so there is no missing harmonic spectrum.

Thus σ(A₀)={0,1,1/2}∪{l/(2l+1):l≥1}, with degree-l multiplicity 2l+1 and infinite-dimensional 0 and 1 eigenspaces. The value 1/2 is an accumulation spectral point, not an eigenvalue in this decomposition. For S₀, l=1 is precisely the three constant vectors, and l≥2 yields (l−1)/(3(2l+1)), whose minimum is 1/15. The negative value −1/3, positive 2/3 and accumulation 1/6 are farther away. This proves an isolated rank-three zero at gap 1/15.

## Kernel coefficients and explicit constants

Radial differentiation gives Kκ=e^(iκr)[(1−iκr−κ²r²)I+(κ²r²+3iκr−3)eeᵀ]/(4πr³). Writing z=κr, the coefficients for n≥2 of f=e^(iz)(1−iz−z²)−1 and g=e^(iz)(z²+3iz−3)+3 are i^n(n−1)²/n! and −i^n(n−1)(n−3)/n!. Therefore Kκ−K₀=−κ²(I+eeᵀ)/(8πr)−iκ³I/(6π)+remainder.

The diameter of B is 2; |κ|≤1/2 gives |z|≤1. For n≥4 both numerator coefficients have magnitude ≤n²/n!, and Σ_{n≥4}n²/n!=2e−9/2<1 using e<11/4. The remainder Frobenius norm is ≤(√3+1)|κ|⁴r/(4π)<3|κ|⁴r/(4π). Its HS norm is ≤3|κ|⁴·2·|B|/(4π)=2|κ|⁴. This uses |B|=4π/3, not an unbounded whole-space kernel.

For C₂ kernel −(I+eeᵀ)/(8πr), ||I+eeᵀ||_F²=6 and ∫_{B²}r⁻²≤|B|∫_{|z|≤2}|z|⁻² dz=32π²/3. Thus ||C₂||≤||C₂||_HS≤1. J has norm |B|, so ||J/(6π)||=2/9. Then ||Cκ||≤|κ|²[1+(2/9)|κ|+2|κ|²]≤(29/18)|κ|²<2|κ|². The correction is an entire norm-analytic family: on any bounded κ-disk, the differentiated series converges in HS norm by its factorial majorant on r≤2. There is no outgoing-kernel boundedness assertion over all of R³.

## Perturbation, graph, trace

On |z|=1/30 the S₀ resolvent bound is 30; the circle is halfway across the 1/15 gap. If ε=||Cκ||≤1/60, the Neumann inverse bound is 60. The resolvent identity and contour length give ||Pκ−P||≤(1/30)·60·ε·30=60ε≤120|κ|²=:η. This contour argument is on L²(B); its global zero extension would have an infinite-rank zero eigenspace and is deliberately excluded.

At η<1 the two projections have equal rank even though Pκ need not be orthogonal. For v∈ran Pκ, ||(I−P)v||≤η||v|| and ||Pv||≥(1−η)||v||. Hence ran Pκ={w+Γκw:w∈V}, with ||Γκ||≤η/(1−η)≤240|κ|² when η≤1/2. The finite-dimensional representation Hκ=P Sκ(I+Γκ)|_V is similar to the restricted operator because P and I+Γκ are inverse coordinate maps; it therefore preserves algebraic multiplicity and Jordan structure.

Since PS₀=0, Hκ=PCκ|_V+PCκΓκ. The error relative to κ²PC₂|_V−iκ³PJ|_V/(6π) is bounded by 2|κ|⁴+(2|κ|²)(240|κ|²)=482|κ|⁴. For real κ, PC₂|_V is selfadjoint (real symmetric kernel), hence has real trace. J|_V=(4π/3)I, so Im tr Hκ≤−(2/3)κ³+3·482κ⁴. At κ=10⁻⁴ this is ≤−(7831/15000)κ³<0. The trace equals the sum of the three eigenvalues counted algebraically, so at least one has negative imaginary part. No eigenvalue approximation or simplicity is needed.

The common sufficient frequency range is |κ|≤1/√240 and |κ|≤1/√120 and |κ|≤1/2, plus real κ>0 with κ<1/2169 for strict trace negativity. κ=10⁻⁴ satisfies each by exact rational inequalities. Individual nonreal spectral points are isolated with finite algebraic multiplicity because Sκ is a compact perturbation of selfadjoint S₀, and analytic Fredholm applies on C\R (or C\[−1/3,2/3]). The 3-cluster alone also has finite algebraic rank inside the contour. The Riesz projection rank argument permits defective clusters.

## Compact support and persistence

Enumerate distinct Q³∩closed B as q_k, k≥1. For j≥1, let U_j=∪_k B(q_k,2^(−j−k−4)) and F_j=closed B\U_j, then Ω_j=F_j∪{0}. Radii are positive, U_j open, F_j compact; Σ_k vol balls=(4π/3)2^(−3j−12)/7. Hence |B\F_j| tends to zero and F_j has positive measure. U_{j+1}⊂U_j, so F_j increases, and the residual removed measure tends to zero. Thus 1_{F_j}→1_B almost everywhere, as well as in measure. Every rational point of closed B belongs to its own removed ball, so F_j contains no rational point. Its interior is empty by density of Q³ in every open ball; adding one point cannot produce interior. Ω_j is compact with positive volume and empty interior; 0 is actually isolated because its enumerated removal ball is disjoint from F_j.

Every point of every (1/n)Z³ is rational. Hence Ω_j∩(1/n)Z³={0}, so the source's omitted self block leaves exactly a 3×3 zero matrix. Adding 0 has no continuum effect in Lebesgue L².

Persistence uses H=L²(R³;C³), static D=p.v.K₀, B_j=M_jDM_j and B_B=M_BDM_B. Strong mask convergence and bounded D give B_j→B_B strongly, and selfadjointness gives adjoint convergence. Their spectra lie in [−1/3,2/3]. With κ fixed, the dynamic kernel lies in L²(B²), and dominated convergence gives C_j→C_B in HS norm. This is not operator-norm convergence of static compressions.

For z outside the real static interval, R_j=(z−B_j)⁻¹ converge strongly, as do adjoints, uniformly over compact z-sets. With compact C_B, F_j(z)=R_jC_j→R_BC_B in norm. On an off-real isolating circle for a nonreal ball eigenvalue, the Fredholm factors I−F_j are eventually invertible. The full resolvent is R_j+(I−F_j)⁻¹F_jR_j. Its first summand integrates to zero around the off-real disk. Its compact second factor converges in norm, including right multiplication by R_j using strong adjoint convergence. Thus the Riesz projections converge in norm and eventually have equal nonzero finite ranks. This gives a nonreal eigenvalue of the fixed F_j for all sufficiently large finite j. The added global zero eigenspace is harmless because the contour misses zero. The set index j is existential, not supplied quantitatively by the proof.

## Source scope before consulting inherited reports

The OWR contribution printed 2580 says permittivity differs from a constant only in a compact subset Ω; printed 2581 explicitly uses grid-center membership x_n∈Ω and omission n=m; printed 2582 asks to describe and prove the observed off-interval behavior, without a universally quantified theorem or explicit boundary condition. The constructed Ω_j meets literal compact subset and point-membership conventions and refutes the unrestricted universal statement. It is a pathology of sampling a volume-null representative change together with a positive-volume nowhere-dense material, and does not falsify the usual regular-particle interpretation of the observed behavior. CDN's later main description repeatedly uses bounded domains, so Ω_j is not an instance of that geometric usage. The counterexample neither proves condition (G) necessary nor supplies a full necessary-and-sufficient characterization or a proof of the numerical eigenvalue-density picture within the interval.
