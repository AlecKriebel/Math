# Two-loop SLE versus loop-model pair measures: five bounded approaches

8 October 2026. Target: the comparison question at OWR 52/2024, p. 3049.

## Outcome and scope

**Partial results only. The full comparison is not proved, disproved, or located as a prior theorem.** Five different approaches yield exact finite-model identities, a CLE kernel reduction, a precise obstruction to an invariance argument, explicit consequences of known annulus integrability, and a conditional scaling-limit theorem. None determines the complete Radon–Nikodym derivative between the source's cascade measure and the same-ensemble CLE pair-counting measure. No novelty is claimed for the elementary deductions below.

The OWR question asks for a relationship with concrete O(n) models and CLE counting measures. It does not prescribe a lattice, boundary condition, phase, sampling rule, or normalization. Its surrounding discussion concerns nonintersecting Jordan curves on the sphere, annular partition functions, and possible rate functions. A full answer must declare these choices rather than turn an arbitrarily selected special case into a resolution of the whole programme. [OWR]

Here are the explicit choices used for the partial results:

* Lattice calculation: a finite simple graph, vertex-disjoint unoriented simple cycles, free boundary, weight n^number_of_cycles times x^number_of_occupied_edges; n>0 and x>0. This includes finite hexagonal-lattice domains. No critical or scaling-limit assertion is built into this definition.
* Prospective dilute comparison: n=-2 cos(4π/κ), 8/3<κ≤4, with the hexagonal candidate x_c(n)=(2+sqrt(2-n))^(-1/2). Identifying the continuum law for this entire family is not an assumption we have proved. The dense phase is not silently included; its nonsimple curves require a different state space.
* CLE: nested full-plane/sphere CLE_κ, 8/3<κ≤4. Pair counting means the expected counting measure on **ordered distinct pairs from the same realization**. The source's informal independent sampling from counting measure must not be confused with using two independent CLE realizations.
* A scoped CLE calculation below restricts to loops separating 0 and infinity, with the first loop outside the second. This is not the whole sphere pair space.
* SLE: unrooted, unoriented simple loops. Fix the one-loop normalization by the CLE intensity ν when the parameter lies in the CLE range. Restrict this same normalization to domains using the usual SLE restriction kernel. Write c=(6-κ)(3κ-8)/(2κ).
* All measures are unnormalized unless a finite restriction is explicitly normalized. For a symmetric ordered-pair measure, unordered pair counting is half its pushforward under forgetting the order. No uniform probability distribution on all loops of an infinite CLE is used.

The reference cascade measure is

M(dγ,dη)=1_{γ∩η=∅} exp((c/2)Λ*(γ,η)) ν(dγ)ν(dη).

Luo–Maibach's Theorem 2.1 constructs this measure for 0<κ≤4 via the one-loop domain restriction kernel. Their §1.2 explicitly separates alternative CLE constructions. The author PDF is dated April 22, 2025 internally despite its June 30 filename; the publisher records acceptance May 2 and publication May 23, 2025, in IMRN 2025(11), rnaf133. It is published work, not a new result here. [LM]

The one-loop identification ν=C_κ μ_Zhan is already Theorem 1.1 of Ang–Cai–Sun–Wu. Choosing ν as normalization absorbs that constant at the one-loop level; it does not identify second moments. [ACSW]

## Approach 1. Exact O(n) partition-function surgery

Let G be finite, and let ℒ(G) be its collections of vertex-disjoint simple cycles. Put

Z_G(n,x)=Σ_{L∈ℒ(G)} n^{|L|}x^{Σ_{γ∈L}|γ|}.

For a vertex set U, G-U denotes the induced graph on its complement. For a cycle γ, write V_γ for its vertices. The probability measure is P_G(L)=weight(L)/Z_G. Define

ν_G(γ)=E_G[1_{γ∈L}],
N_G(γ,η)=E_G[1_{γ∈L}1_{η∈L}], γ≠η.

### Proposition 1

For every cycle γ,

ν_G(γ)=n x^{|γ|} Z_{G-V_γ}/Z_G.

For vertex-disjoint γ,η,

N_G(γ,η)=n² x^{|γ|+|η|} Z_{G-(V_γ∪V_η)}/Z_G,

and consequently

N_G(γ,η)/(ν_G(γ)ν_G(η))
=Z_G Z_{G-(V_γ∪V_η)}/(Z_{G-V_γ}Z_{G-V_η}).                         (1)

For intersecting distinct cycles, N_G(γ,η)=0.

**Proof.** Removing the prescribed cycle or cycles is a weight-preserving bijection, apart from their displayed n and x factors, between configurations containing them and arbitrary configurations on the vertex-deleted graph. The empty configuration makes every denominator positive. Division gives (1). ∎

In a planar nested configuration, vertex deletion separates the remainder into pieces inside, between, and outside the marked cycles; the partition function factors over these graph components. Boundary vertices, their incident edges, and any external boundary condition must be kept exactly as prescribed by the deletion operation. Replacing these component partition functions by continuum disk/annulus expressions is a separate theorem, not part of the bijection.

### Proposition 2: a low-fugacity interaction check

Fix G and x>0. Let R_n be the right side of (1), and let S_H=Σ_{α a simple cycle in H}x^{|α|}. Then

log R_n = n Σ_{α: V_α∩V_γ≠∅, V_α∩V_η≠∅} x^{|α|} + O(n²), n→0.

**Proof.** Since Z_H=1+nS_H+O(n²), the linear coefficient in log R_n is S_G+S_{G-(V_γ∪V_η)}-S_{G-V_γ}-S_{G-V_η}. Inclusion-exclusion counts exactly the cycles meeting both vertex sets. ∎

This is a finite-graph expansion with a graph-dependent remainder. It is consistent with a positive first-order interaction for disjoint marked loops, but it is not a uniform critical-mesh estimate or a derivation of the Brownian loop term Λ*. At n=0 the unmarked model is empty, and marked measures need rescaling; invoking c=0 at κ=8/3 does not solve self-avoiding-polygon convergence.

**Exact gap.** Prove an appropriately normalized scaling limit of (1), including boundary terms, and show its limit equals exp((c/2)Λ*) times the required model-dependent annular factor. Pointwise convergence of a few partition functions or a formal Coulomb-gas expression does not provide this.

## Approach 2. Campbell disintegration and the CLE successor kernel

Let Γ be a simple locally finite point process of loops on standard Borel loop and configuration spaces, with σ-finite intensity ν. For example, a countable exhaustion by windows with finite expected loop count suffices. Almost-sure local finiteness alone does not imply this intensity hypothesis. Its counting measure is C_Γ=Σ_{γ∈Γ}δ_γ. Then

N_2=E[C_Γ⊗C_Γ]-Δ_*ν,  ν=E C_Γ,                                  (2)

where Δ(γ)=(γ,γ). Formula (2) is an identity of nonnegative test-function integrals after removing the diagonal; it is not a subtraction of two infinite numerical totals.

Disintegrate the one-point Campbell measure EΣ_{γ∈Γ}δ_(γ,Γ) over ν. Let P_γ be its Palm probability kernel and

R_γ(B)=E_{P_γ}[#((Γ\{γ})∩B)].

Then Tonelli's theorem gives

N_2(dγ,dη)=ν(dγ)R_γ(dη).                                           (3)

No conditional independence is needed for this identity. In particular, ν alone does not determine R_γ. For a finite loop window B, same-realization counting has total E[N_B(N_B-1)], whereas two independent realizations give (E N_B)². Normalizing the counting measure separately in each realization instead produces an additional random factor 1/(N_B(N_B-1)) on nonempty pair sets, and changes the result again.

For loops of a nested sphere CLE surrounding 0, let Q(γ,dη) be the law of the next inner loop obtained from a CLE in the interior of γ. The nested Markov construction and full-plane intensity measure are established by Kemppainen–Werner; their §3.3 describes the adjacent annulus measure as ν(dγ)Q(γ,dη). [KW]

### Proposition 3

For the restricted outer-to-inner pair measure,

N_2^>(dγ,dη)=ν_0(dγ) Σ_{j≥1}Q^j(γ,dη).                            (4)

Here ν_0 is ν restricted to loops surrounding 0. The j-th term counts pairs with exactly j-1 intervening loops surrounding 0.

**Proof.** Every strict descendant on the nested chain has exactly one positive generation gap j. Conditional on the starting loop, the j-th successor has kernel Q^j by the Markov construction. Sum the nonnegative test-function identities over j; Tonelli justifies the sum without a preliminary total-mass bound. ∎

The cascade restriction in this sector is

M^>(dγ,dη)=ν_0(dγ)ν_{D_γ}^{0}(dη),                                (5)

where D_γ is the interior and the superscript 0 restricts to loops surrounding 0. Thus N_2^>=aM^> is equivalent, for ν_0-almost every γ and in the sense of kernels, to

Σ_{j≥1}Q^j(γ,·)=a ν_{D_γ}^{0}(·).                                 (6)

For general absolute continuity the same comparison is between these two kernels. This turns the desired equality into a testable statement, but does not prove (6). The one-loop intensity theorem on the whole sphere cannot be applied to replace the disk descendant-counting kernel by the SLE disk restriction kernel: those are different constructions with an annular complementary region.

**Exact gap.** Determine the reduced Palm kernel, or the descendant resolvent in (4), relative to ν_{D_γ}. If the claim concerns all sphere pairs, also handle pairs outside the sector separating 0 and infinity. Proving the cascade identity for an artificially independently resampled second loop only reproduces M.

## Approach 3. Does conformal invariance force a modulus-only density?

The answer is no for global conformal invariance alone. The distinction between a conformal map of an annulus and a conformal automorphism of its ambient sphere matters.

### Proposition 4: geometric obstruction

There are analytic pairs with identical annulus modulus that are not related by a Möbius transformation.

**Proof.** Choose 0<r<1 and 0<ε<1/2, and set f(z)=z+εz². If f(z)=f(w) for z,w in the closed unit disk, then (z-w)(1+ε(z+w))=0. The second factor cannot vanish, so f is injective there. Therefore the pairs

(rS¹,S¹) and (f(rS¹),f(S¹))

bound conformally equivalent annuli. The second outer boundary is not a circle. Otherwise f would be a conformal bijection from a disk to a disk, hence a Möbius function; a polynomial of degree two cannot be Möbius. Since Möbius transformations take generalized circles to generalized circles, the pairs cannot be Möbius-equivalent. ∎

For example, the indicator that both curves are generalized circles is a Möbius-invariant measurable function on analytic pairs that is not a function of modulus. This counterexample invalidates a general geometric implication; it does not claim that this particular indicator is a useful nonconstant observable on SLE-typical pairs.

### Proposition 5: the missing probabilistic hypothesis

On a common measurable restriction B of finite positive mass for both measures, normalize μ and ν to probabilities, and let T be the measurable annulus modulus. Let f be a nonnegative measurable function. Assume standard Borel spaces, so regular conditional probabilities exist. Then ν=f(T)μ if and only if ν's modulus law is f(t) times μ's modulus law and their conditional laws of the **embedded pair given modulus** agree almost everywhere on the ν-modulus law.

**Proof.** If dν=f(T)dμ, integrate a bounded measurable h(pair) by disintegration over T. The conditional kernel of μ is also a conditional kernel of ν, with the modulus law reweighted by f. Conversely, inserting the common kernel and the assumed modulus marginal density into the disintegration formula gives ∫h dν=∫h f(T)dμ. ∎

The normalization of B multiplies a density by a constant. Compatibility must be verified if such restrictions are exhausted to recover an infinite measure.

The determinant-line/CFT programme imposes more than Möbius invariance. For example, suppose two putative laws really arise from the same line-valued pair measure, with trivializations whose ratios on disks and the sphere are constants and whose ratio on an annulus is A(τ)>0. The ratio of the disk–annulus–disk partition products is then C A(τ), hence the scalar pair laws differ by that factor. This is an algebraic conclusion **conditional on identifying those actual trivializations for the actual model laws**. It does not identify the same-CLE law by itself.

**Exact gap.** Establish that model law identification, or prove the conditional-law equality required in Proposition 5. Neither a one-loop uniqueness theorem nor matching central charges supplies it. Knowing only the two modulus marginals is insufficient.

## Approach 4. Annulus integrability and a quantitative descendant test

Ang–Remy–Sun give the modulus transform for the j-th CLE loop surrounding a marked point in a disk (Theorem 1.7), and an annular counting/partition-function interpretation (Theorem 1.9). These are prior exact results, substantially stronger than merely a heuristic CFT analogy. They concern specified annulus observables, not the full embedded-pair comparison with M. [ARS]

The following calculation uses their Theorem 1.7 directly. A source-checking caution: the line below Corollary 1.10 in the inspected v3 PDF prints χ=(1-κ/4)π, inconsistent with χ=(1-4/κ)π in (1.9). At κ=3 these give n=√2 and n=1 respectively. We use (1.9) for the dilute parameter relation and do not import the inconsistent line. For 8/3<κ<4, set

a=4/κ-1, C=cos(πa), s²=a²-8λ/κ,

H_κ(λ) = a sin((κπ/4)s)/(s sin(π(1-κ/4))),
r_κ(λ) = C/cos(πs).

Theorem 1.7 permits λ>3κ/32+2/κ−1; our λ>0 lies strictly in that range for 8/3<κ≤4. Its modulus convention is A_τ={z:e^(−2πτ)<|z|<1}. For λ>0, s is either nonnegative real or positive imaginary; the displayed expressions have their removable values at s=0 and are real and positive. The prior transform reads

E[exp(-2πλ τ_j)]=H_κ(λ) r_κ(λ)^j.                                (7)

Here τ_j is the modulus between the disk boundary and its j-th loop around the origin. Since 0<r_κ(λ)<1, Tonelli and the geometric series give a finite resolvent transform:

E[Σ_{j≥1} z^{j-1} exp(-2πλ τ_j)]
=H_κ(λ) r_κ(λ)/(1-z r_κ(λ)), 0≤z≤1.                              (8)

**Proof of the convergence claim.** If 0<s<a<1/2, cos(πs)>cos(πa)>0. If s is imaginary, cos(πs)≥1>C. The case s=0 follows by continuity. Sum (7). ∎

The parameter z marks the number of intervening origin-surrounding loops, so z=0 selects adjacent pairs and z=1 counts all strict descendants. At κ=4 the continuous limit is particularly simple. Put u=πsqrt(2λ). Then

E[exp(-2πλτ_j)]=sinh(u)/(u cosh(u)^j),

E[Σ_{j≥1} exp(-2πλτ_j)]=sinh(u)/(u(cosh(u)-1)).                    (9)

To obtain (9), use a/sin(π(1-κ/4))→1/π as κ→4 and s→i sqrt(2λ), then sum the positive geometric series. These formulas have the correct single-loop normalization as λ↓0, whereas the all-descendant expression diverges, as it must.

An immediate finiteness consequence, useful for the measure comparison, is

E[# {j: τ_j≤T}] ≤ exp(2πλT) H_κ(λ)r_κ(λ)/(1-r_κ(λ)) <∞

for finite T and λ>0. Therefore (4), restricted to a finite-ν_0 outer-loop window and τ≤T, has finite mass. The same argument also applies at κ=4 using (9).

This provides an exact modulus diagnostic for a proposed answer. Any claimed equality with the cascade kernel must reproduce (8) after its kernel is pushed forward by annulus modulus with the same marked-point and pair convention.

**Exact gap.** We have not calculated the matching cascade modulus transform, and equality of such transforms would still require the embedded-shape comparison in Proposition 5. A known CLE annulus partition function cannot simply be asserted to be the desired two-loop RN derivative. Uniformly choosing a pair, choosing adjacent loops, and counting all descendants yield different modulus statistics.

## Approach 5. Passing a discrete pair measure to a continuum law

The inspected Glazman–Harel–Zelesko v3 (April 19, 2026), §1.2, distinguishes macroscopic-loop results from general CLE convergence; it cites established percolation and critical-Ising cases. Benoist–Hongler, Theorems 1 and 6, prove nested CLE_3 convergence for critical Ising interfaces in square-grid discretizations of a simply connected Jordan domain with + boundary conditions and their specified loop-collection metric. This is a model- and boundary-specific result; it is not a theorem for arbitrary finite graphs or all boundary conditions. These facts permit a special-model strategy but do not erase the source's broader scope or its two-loop density question. [GHZ, BH]

### Proposition 6: sufficient convergence criterion

Let Γ_m and Γ be random locally finite simple configurations on a Polish loop space. Fix a bounded loop window K. Suppose their restrictions to K can be coupled so that, almost surely, the loops admit a finite matching converging in the loop topology, with counts N_m=N eventually. Equivalently one can assume a suitable point-process convergence and continuity conditions yielding this matching. Assume additionally that {N_m(N_m-1)} is uniformly integrable. Then, for every bounded continuous f on K×K,

E Σ_{γ≠η∈Γ_m∩K} f(γ,η) → E Σ_{γ≠η∈Γ∩K} f(γ,η).                (10)

**Proof.** Under the matching, the finite sum converges almost surely. Its absolute value is bounded by ||f||∞N_m(N_m-1), a uniformly integrable family. Truncation followed by dominated convergence, and then removal of the truncation, proves convergence of expectations. The same bound and Fatou ensure integrability of the limiting sum. ∎

A sufficient stronger bound is sup_m E[N_m^{2+ε}]<∞ for some ε>0. A first-moment bound is insufficient, and even convergence of first intensity measures does not cure the defect.

### Exact counterexample to omitting uniform integrability

For m≥2, let Γ_m be empty with probability 1-m^(-2), and otherwise contain m distinct concentric circles of radii in [1,2]. Let Γ be empty. Then Γ_m→Γ in probability in any topology in which equality of configurations implies closeness. Indeed, on any common probability space carrying these configurations, Σ_m P(Γ_m≠∅)<∞, so the first Borel–Cantelli lemma gives Γ_m=∅ eventually almost surely. Thus the finite-matching hypothesis also holds. Its first intensity has total mass 1/m→0. But the ordered distinct-pair intensity has total

m(m-1)/m² = 1-1/m →1,

rather than zero. This example consists of simple mutually disjoint loops; it is not merely a multiplicity artifact. The point-process law is overwhelmingly empty while its second moment retains rare large configurations.

Applied to a lattice model, Proposition 6 would justify convergence of the marked pair-counting measures, provided the model-specific topology, cutoff boundary conditions, and moment bounds are supplied. One must then compare the limiting CLE pair measure with M using Approaches 2–4. A convergence theorem for a single interface cannot replace these two stages.

**Exact gap.** Establish the needed full configuration limit and pair-moment control for the selected lattice family, then solve the continuum comparison. Even in an Ising setting with known ensemble convergence, the full RN identity with the cascade measure is not obtained by (10).

## Validation and disposition

The handwritten arguments above use bijections, Tonelli/disintegration, an injective polynomial, a geometric series, and uniform integrability. The accompanying executable exhausts the configurations of five selected finite subcubic graphs, verifying the lattice identities and first fugacity coefficient with rational arithmetic. It also checks the central-charge conversion and geometric-resolvent algebra symbolically and verifies the rare-event moment formulas exactly. These checks do not certify the imported CLE theorems or prove any continuum claim.

The executable uses explicit exceptions rather than Python assertions. It is run normally, with -O, and with -OO, and an intentional failure is required to fail in each mode. Each run verifies 1,482 single/pair identity checks across those five graphs, six symbolic identities, and 60 rare-event moment identities. Numerical simulation is not used as evidence. The source PDFs were retrieved privately and are excluded from the authored deliverable.

The strongest established results here are Propositions 1–6 and the elementary consequences (8)–(9) of a credited prior theorem. The missing core is an actual identification of the CLE/model annulus factor **and** its action on the complete embedded-pair law, together with any required lattice convergence. The five-approach bound has been reached. The appropriate disposition is scoped partial progress with an exact gap, not solved or verified prior resolution.

## Public primary references

* [OWR] Mini-Workshop: Critical phenomena of the XY model, OWR 52/2024, Maibach contribution pp. 3048–3050, especially p. 3049. https://ems.press/content/serial-article-files/50762
* [LM] Yan Luo and Sid Maibach, Two-Loop Loewner Potentials, IMRN 2025(11), rnaf133. https://academic.oup.com/imrn/article/doi/10.1093/imrn/rnaf133/8142356 ; inspected author version: https://sidmaibach.eu/articles/Two_Loop_Loewner_Potentials_2025_06_30.pdf ; arXiv: https://arxiv.org/abs/2411.02232
* [ACSW] Morris Ang, Gefei Cai, Xin Sun, Baojun Wu, SLE Loop Measure and Liouville Quantum Gravity, arXiv:2409.16547v2, Theorem 1.1. https://arxiv.org/abs/2409.16547v2
* [KW] Antti Kemppainen and Wendelin Werner, The nested simple conformal loop ensembles in the Riemann sphere, PTRF 165 (2016), 835–866, §§3.1–3.4. https://arxiv.org/abs/1402.2433 ; https://doi.org/10.1007/s00440-015-0647-3
* [ARS] Morris Ang, Guillaume Remy, Xin Sun, The moduli of annuli in random conformal geometry, arXiv:2203.12398v3, Theorems 1.7 and 1.9. https://arxiv.org/abs/2203.12398v3
* [GHZ] Alexander Glazman, Matan Harel, Nathan Zelesko, Planar percolation and the loop O(n) model, arXiv:2508.20917v3, §1.2. https://arxiv.org/abs/2508.20917v3
* [BH] Stéphane Benoist and Clément Hongler, The scaling limit of critical Ising interfaces is CLE(3). https://arxiv.org/abs/1604.06975

Bibliographic inspection is bounded through 8 October 2026. No claim of worldwide novelty or exhaustive absence of later resolutions is made.
