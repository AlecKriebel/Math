# Boundary conditions preserving homogeneous Sobolev and Hardy constants

## Status and scope

**SCOPED PARTIAL RESULT; NOT A COMPLETE CLASSIFICATION.** This report addresses queue row 1878, ID 30001414 (OWR-4209-004). It gives a nonlocal transparent-boundary sufficient class outside the known Navier sandwich, a first-order local mixed-boundary classification in an explicitly restricted family, and counterexamples to kernel-removal and finite-constraint strategies. No novelty priority is asserted. In particular, no theorem here classifies all local higher-order boundary operators.

Assume throughout that Ω is a bounded connected smooth domain in R^n, 0∈Ω, m≥1 is an integer, 1<p<∞, and mp<n. Smooth means C∞ for convenience; no claim of optimal boundary regularity is made. Write q=np/(n-mp) and

- L_m u=Δ^k u if m=2k;
- L_m u=∇Δ^k u if m=2k+1;
- E_G(u)=∫_G |L_m u|^p;
- S=inf E_Rn(U)/||U||_q^p and H=inf E_Rn(U)/∫_Rn |x|^{-mp}|U|^p over the homogeneous completion D^{m,p}(R^n).

For a linear space X⊂W^{m,p}(Ω), S_X and H_X denote the corresponding interior quotient infima. Only these original energies and denominators are used. No boundary-energy or lower-order correction is inserted.

The primary source establishes S,H>0, the Dirichlet and Navier equalities, and the original broader question. The Hardy equality for spaces containing W_0^{m,p}(Ω) uses 0∈Ω. Our source gate and public source metadata are in hardy_boundary_30001414/SOURCE_GATE.md and PUBLIC_SOURCE_METADATA.json; the source copies themselves are not deliverables or publication material.

## Approach 1: kernel obstruction, and why eliminating it is insufficient

If X contains a nonzero u with L_m u=0, then S_X=H_X=0. Indeed both denominators are positive and finite for u∈W^{m,p}(Ω). For the weighted denominator, localize with a smooth cutoff equal to one near the interior origin: the cutoff product belongs to W_0^{m,p}(Ω), where the known Hardy inequality gives finiteness, and the weight is bounded on the remaining region. In particular, for smooth witnesses finiteness also follows directly from mp<n.

For even m, every harmonic smooth function is a zero-energy witness, not just constants. For odd m=2k+1, every smooth function with Δ^k u constant is a witness. Thus checking only whether a boundary condition excludes constants misses a much larger obstruction. For example homogeneous derivative constraints can admit affine harmonic functions.

This necessary test is not sufficient. Approach 4 below constructs a Robin family with trivial Laplacian kernel and still a strict loss in the sharp Sobolev constant. Consequently neither Poincaré coercivity nor elimination of constants classifies preservation of both constants.

## Approach 2: zero-exterior-energy extensions (positive theorem)

Define

Z_Ω={U∈D^{m,p}(R^n): L_m U=0 almost everywhere on R^n\Ω},

X_ext={U|_Ω: U∈Z_Ω}.

These are linear spaces. The definition is a nonlocal boundary condition, not an additional bulk equation on Ω: the exterior continuation is constrained, while the interior source is arbitrary in the even-order realization below.

### Theorem

X_ext is a closed linear subspace of W^{m,p}(Ω), contains W_0^{m,p}(Ω), and

S_Xext=S,     H_Xext=H.

For every m≥2, X_ext is not a subspace of the Navier space. Thus this result is not obtained by the W_0⊂X⊂W_Navier sandwich.

### Proof of well-definedness and closedness

We use the standard homogeneous Sobolev realization: D^{m,p}(R^n) embeds in L^q(R^n), its L_m norm is equivalent to the full mth-derivative norm by Riesz-transform multiplier estimates, and its lower derivatives satisfy the corresponding homogeneous Sobolev bounds. Restriction to a bounded domain is therefore continuous into W^{m,p}(Ω). This realization avoids polynomial ambiguities.

Z_Ω is closed in D^{m,p}, since convergence of L_mU in L^p preserves its vanishing on the exterior. Restriction is injective on Z_Ω: if U vanishes on Ω, L_mU vanishes there distributionally and, by definition, almost everywhere outside; hence its global homogeneous norm is zero and U=0 in D^{m,p}. For U∈Z_Ω and u=U|_Ω,

||U||_{D^{m,p}}^p=E_Rn(U)=E_Ω(u).

If u_j∈X_ext converges in W^{m,p}(Ω), its unique lifts U_j are Cauchy in D^{m,p} by this equality. Their limit lies in Z_Ω and restricts to the original W^{m,p} limit. Hence X_ext is closed.

The zero extension of each W_0^{m,p}(Ω) function belongs to Z_Ω, by approximation with C_c∞(Ω). This proves inclusion.

### Proof of the constants

For u∈X_ext with lift U,

E_Ω(u)=E_Rn(U)≥S ||U||_{L^q(R^n)}^p≥S ||u||_{L^q(Ω)}^p,

and

E_Ω(u)=E_Rn(U)≥H ∫_Rn |x|^{-mp}|U|^p≥H ∫_Ω |x|^{-mp}|u|^p.

Thus S_Xext≥S and H_Xext≥H. The reverse inequalities follow from W_0^{m,p}(Ω)⊂X_ext and the established sharp Dirichlet constants, with 0∈Ω for Hardy. This proves equality. There is no claim that the interior and exterior denominators coincide.

### Explicit realization for even m=2k

Let I_{2k} denote the Riesz potential normalized as the inverse of (-Δ)^k. Then

X_ext={ (I_{2k}(f 1_Ω))|_Ω : f∈L^p(Ω) }.

Indeed the whole-space potential belongs to D^{2k,p}, solves (-Δ)^kU=f1_Ω, and has the required zero exterior energy. Conversely, for U∈Z_Ω its source (-Δ)^kU is supported in Ω and belongs to L^p; uniqueness in D^{2k,p} identifies U with that potential. The conditions 1<p<n/(2k) are exactly those assumed above. This is not a boundary prescription of the source f: f can be any interior L^p function.

Prior-work warning: this potential-image boundary class is established Kac/polyharmonic Newton-potential territory, not a new class invented here. Rozenblum–Ruzhansky–Suragan (2016), equations (1.10)–(1.11), identifies nonlocal boundary conditions for these potential images and cites Kal’menov–Suragan (2012). The contribution asserted here is only the explicitly proved sufficient sharp-constant transfer, without any novelty-priority claim.

For m=2, this is the transparent Laplace boundary relation: u and its normal derivative match those of the exterior harmonic continuation, with the normal on both sides taken in the same geometric direction. Equivalently, ∂νu=T_ext(γu), where T_ext maps boundary values to the same-direction normal derivative of the exterior harmonic continuation. The continuation is selected by its whole-space homogeneous integrability and appropriate matching, not by allowing arbitrary growing harmonic functions. This description includes bounded complementary components. The abstract definition is controlling; no unsupported trace-domain characterization of higher-order operators is needed.

### Explicit witnesses outside Navier for all m≥2

Choose nonnegative nonzero f∈C_c∞(Ω).

- If m=2k, set U=I_{2k}f. The Riesz kernel is positive since 2k<n; U is strictly positive on ∂Ω. Its energy is supported in Ω. Thus u=U|_Ω belongs to X_ext but violates the zeroth Navier trace u=0.
- If m=2k+1≥3, set U=I_{2k}f. Then ∇Δ^kU=(-1)^k∇f is supported in Ω. Also U∈D^{2k+1,p}(R^n). One verification uses D^{2k+1}U as Riesz transforms of ∇f, together with cutoff approximation; at infinity U and its derivatives decay as |x|^{2k-n-j}, and cutoff errors in the order-m norm tend to zero because their pth powers are O(R^{n-p(n+1)}). Here p>1 implies n-p(n+1)<0. Lower-order cutoff terms have the same rate. U is smooth everywhere and positive on ∂Ω. Again u violates the Navier zeroth trace.

For the cutoff approximation, the global mth derivatives are L^p (outside large balls they decay as |x|^{-n-1} in the odd case), and the cutoff transition estimates just stated handle every Leibniz term. Thus membership is established directly rather than inferred merely from a distributional equation.

### First-order multiply connected specialization

For m=1, suppose Ω has finitely many smooth bounded complementary components K_1,...,K_N (holes). Then X_ext consists exactly of W^{1,p}(Ω) functions whose trace is zero on the boundary facing the unbounded component and is a constant c_i on each ∂K_i. Extend u by c_i in K_i and by zero in the unbounded exterior. Matching traces makes this a global W^{1,p} function with compact support, hence an element of D^{1,p}; its gradient energy outside Ω is zero. Conversely, zero gradient implies a constant on each connected exterior component, and L^q integrability forces the unbounded-component constant to be zero.

These nonlocal constant-trace conditions on entire hole boundaries preserve both constants and need not be Dirichlet. The assumption 0∈Ω requires the holes to avoid the origin. If the exterior is connected, this particular first-order extension space reduces to W_0^{1,p}(Ω). This does not classify every other conceivable first-order nonlocal condition.

## Approach 3: local mixed Dirichlet/free boundary concentration

This approach gives a negative classification in a precise first-order family. Set m=1. Partition ∂Ω, up to a surface-measure-zero interface, into relatively open Dirichlet and free parts Γ_D and Γ_N. Let

X_D={u∈W^{1,p}(Ω): γu=0 on Γ_D}.

If Γ_N is empty, X_D=W_0^{1,p}(Ω), so both constants are preserved. If Γ_N is nonempty, then

S_XD≤2^{-p/n} S<S.

Thus within this partition family both constants are preserved if and only if there is no free boundary patch. No classification is asserted for arbitrary fractal trace sets, capacity conditions, or nonlocal trace coupling.

### Proof of the strict upper bound

Take a point in Γ_N, and flatten the boundary locally by a smooth chart with derivative equal to an orthogonal map at that point. Choose a smooth compactly supported radial near-minimizer φ for the whole-space first-order Sobolev quotient. Such radial near-minimizers follow from symmetric decreasing rearrangement and approximation (or cutoff approximation of the classical radial optimizer). Scale φ by ε^{-(n-p)/p} and transplant its half-space restriction into the chart; for small ε its trace is supported entirely in Γ_N, so the function is in X_D.

The rescaled metric and Jacobian converge uniformly to their flat values on the fixed support. Consequently the numerator tends to one half of the whole-space energy, while the qth-power denominator tends to one half of the whole-space qth-power norm. The quotient therefore tends to

(1/2)/(1/2)^{p/q} · Q_Rn(φ)=2^{-p/n}Q_Rn(φ).

Take φ arbitrarily close to S. This proves the bound. No Hardy analysis is needed to disprove simultaneous preservation.

The first-order hole condition above does not contradict this theorem: requiring a constant trace on an entire hole is a nonlocal coupling, and the localized half-bubble is not admissible.

## Approach 4: finite side constraints and a coercive Robin counterexample

### Finite-codimensional obstruction lemma

Let Y⊂W^{m,p}(Ω) be a linear space. Suppose u_ε∈Y is bounded and weakly converges to zero in W^{m,p}(Ω), with ||u_ε||_q bounded below and its Sobolev quotient tending to c. For any finitely many continuous linear functionals ℓ_1,...,ℓ_N on W^{m,p}(Ω), let

Y_0=Y∩⋂ker ℓ_j.

Then S_Y0≤c. To see this, retain an independent basis of the restrictions of the ℓ_j to Y, and choose fixed v_1,...,v_r∈Y dual to this basis. Put

w_ε=u_ε−Σ_j ℓ_j(u_ε)v_j.

All retained coefficients tend to zero by weak convergence; redundant constraints vanish as well. Therefore w_ε∈Y_0 and w_ε−u_ε→0 in W^{m,p}, hence in the critical L^q space by continuous embedding. The energy and denominator converge to the same values, giving the claim. If the quotient alone converges, use boundedness and the denominator lower bound to pass this comparison directly; no limit of the individual energy is needed.

The boundary-concentrating sequences in Approach 3 have precisely these properties: their supports shrink to a boundary point, their derivative norms remain bounded, and their lower derivatives tend strongly to zero. Thus finitely many continuous moment conditions, including mean zero, cannot restore the whole-space Sobolev constant to the mixed space. This is stronger than merely observing that unrestricted Neumann conditions admit constants.

### Second-order Robin counterexample without a kernel

Take m=p=2, n>4. Choose a bounded smooth domain with a relatively open flat boundary patch, and a smooth strictly positive coefficient β on ∂Ω. Such smooth domains with a flat patch exist. Let

Y_β={u∈W^{2,2}(Ω): ∂νu+βu=0 on ∂Ω}.

This space excludes constants and has trivial Laplacian kernel. Indeed if Δu=0 and the Robin trace holds, Green's identity gives ∫Ω|∇u|²+∫∂Ωβu²=0, so u=0. The standard smooth-domain Robin elliptic estimate ||u||_{W^{2,2}}≤C(||Δu||_2+||u||_2), combined with Rellich compactness and this trivial-kernel fact, gives ||u||_{W^{2,2}}≤C_β||Δu||_2 on Y_β. Indeed a normalized countersequence has Δu_j→0 and a strongly L²-convergent subsequence; applying the estimate to differences makes it strongly W^{2,2}-convergent to a nonzero kernel element, a contradiction. Thus the example is coercive, not merely kernel-free.

Nevertheless

S_Yβ≤2^{-4/n}S_{2,2}<S_{2,2}.

Use flat coordinates (y,t) with Ω locally t>0 and ν=−∂t. Choose smooth compactly supported radial whole-space near-minimizers φ for S_{2,2}; these can be obtained by cutoff approximation of the classical radial biharmonic Sobolev optimizer. On a small neighborhood of the flat patch, use

u_ε(y,t)=exp(β(y)t) ε^{-(n−4)/2} φ(y/ε,t/ε),

with the tangential coefficient β extended smoothly into the collar. For sufficiently small ε the support avoids every other boundary piece. The evenness of φ in t gives ∂t u_ε(y,0)=β(y)u_ε(y,0), exactly the required Robin condition. On the rest of ∂Ω all traces vanish. The rescaled multiplier exp(εβ(εz')z_n) tends to 1 with its derivatives on fixed supports; the leading Δ energy is therefore half the global Δ energy, with every multiplier correction lower order. The critical norm has the same half-volume split. The quotient tends to 2^{-4/n}Q_Rn(φ), proving the claim after near-minimization.

These Robin bubbles weakly converge to zero in W^{2,2}. The finite-codimensional lemma therefore shows that finitely many continuous linear side constraints still do not repair the strict Sobolev loss. This argument is deliberately restricted to m=p=2 and a flat patch; no blanket curved-boundary or general-p Robin theorem is claimed.

## Approach 5: local higher-order conditions and limitations of extension transfer

The transparent theorem is not a local classification. For example, the local third-order space {u∈W^{3,2}(Ω):u=∂νu=0 on ∂Ω} is generally not the Navier space (whose traces are u=Δu=0), and is not automatically contained in X_ext. If one tries zero extension, a nonzero second normal trace produces an interface singularity in the third derivatives; it is not a D^{3,2} continuation. If one instead matches to an exterior harmonic function, zero Dirichlet data and the admissible decay force the exterior harmonic continuation to vanish, so matching the second traces again imposes the missing condition. This shows why the proved transparent transfer cannot simply be invoked for that local clamped-lower-trace space.

More broadly, extension with a positive exterior energy does not prove the desired inequality: E_global=E_Ω+E_exterior, and the extra term is on the wrong side for the required lower bound on E_Ω. Neither an arbitrary bounded extension operator nor a small relative extension cost yields exactly S and H. Proving a lower bound with a reduced constant would not answer the sharp-constant question.

Similarly, the first-order mixed boundary obstruction relies on admissibility of an even boundary bubble. Higher-order essential traces may exclude that bubble. The half-volume factor must not be applied to clamped or Navier spaces without verifying all trace constraints. A separate calculation in LOCAL_THIRD_ORDER_HARDY.md establishes the origin Hardy equality for this third-order local clamped-lower-trace space on a centered ball. That is a Hardy-only result: its critical Sobolev equality is not established, so simultaneous preservation remains unresolved. The local calculation is independent of the transparent-extension argument.

## What is and is not concluded

Established analytically in this report:

1. A closed, nonlocal transparent-boundary family preserving both constants for every admissible integer m and p.
2. Explicit outside-Navier witnesses for every m≥2, and first-order hole-constant examples.
3. A sharp-constant obstruction for any nonempty free patch in the specified first-order local mixed family.
4. Stability of that obstruction under arbitrary finite continuous linear side constraints.
5. A kernel-free, positive-Robin second-order counterexample on smooth domains with a flat patch, also robust to finite side constraints.
6. A local third-order, p=2, centered-ball Hardy-only result in the companion calculation; no simultaneous Sobolev conclusion.

Not established: novelty, a complete classification of local or nonlocal boundary conditions, a classification on rough/fractal boundary sets, a result for every higher-order Robin system, or sharp Hardy equality when the origin lies outside Ω. The five approaches include both successes and rigorously delimited failed routes; failure of an approach is not a negative theorem about every candidate space.

## Public primary sources and provenance

- Filippo Gazzola, “Higher order Sobolev-Hardy inequalities with remainder terms,” in Oberwolfach Report 08/2010, pp.351–354, boundary question p.352. DOI https://doi.org/10.4171/OWR/2010/08 ; report https://ems.press/journals/owr/articles/4209 ; public PDF https://ems.press/content/serial-article-files/46265 . Locally retrieved and text-inspected as recorded in the source gate.
- Filippo Gazzola, Hans-Christoph Grunau, Guido Sweers, “Optimal Sobolev and Hardy-Rellich constants under Navier boundary conditions,” Ann. Mat. Pura Appl. 189 (2010), 475–486. DOI https://doi.org/10.1007/s10231-009-0118-5 ; author PDF https://gazzola.faculty.polimi.it/bestconstant.pdf . Baseline theorems and homogeneous-space definitions locally inspected. Their Navier theorem is prior work, not a new result of this report.

- Grigori Rozenblum, Michael Ruzhansky, Durvudkhan Suragan, “Isoperimetric inequalities for Schatten norms of Riesz potentials,” Journal of Functional Analysis 271 (2016), 224–239. DOI https://doi.org/10.1016/j.jfa.2016.04.023 ; https://arxiv.org/abs/1506.06355 . The independent reviewer inspected the potential-image nonlocal boundary discussion, equations (1.10)–(1.11); this is a prior-work guardrail, not evidence of novelty for our deduction.
- T. Sh. Kal’menov and D. Suragan, “Boundary conditions for the volume potential for the polyharmonic equation,” Differential Equations 48(4) (2012), 604–608. Bibliographic provenance: reference [16] of the preceding inspected primary paper. Publisher DOI/abstract verified at https://doi.org/10.1134/S0012266112040155 ; original full text not independently inspected here.

Public web searches additionally surfaced the boundary sharp-Sobolev literature and the known fractional Navier extension; neither is used as evidence that this report resolves the source question. The proofs above state their required standard analytic tools explicitly. This is an analytic report, not an executable proof certificate.
