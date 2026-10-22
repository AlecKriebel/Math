# Analytic reduction, geometric sufficient conditions, and two shortcut obstructions

## Scope and notation

This note addresses the discrepancy

    ψ = log J_m f − κ log |Df|,       κ = dim_H(m).

The original source's hypotheses and centering convention are recorded separately in `LITERATURE.md`. Here every lemma states its own assumptions. A branch Jacobian means

    m(f A) = ∫_A J_m f dm

on measurable sets A where f is injective. It is positive and finite m-almost everywhere in the setting under discussion. Use the spherical derivative for global rational maps; a fixed smooth conformal metric can be used locally. Zero-measure critical sets are removed when taking logarithms.

Let a = ∫ψ dm when ψ is integrable, and put φ = ψ − a. Write S_n φ = Σ_(j=0)^(n−1) φ∘f^j. The centered convention must not silently be changed. If the separate identities

    ∫log J_m f dm = h_m(f),     κ = h_m(f)/χ_m,
    χ_m = ∫log|Df| dm > 0

are available with finite integrals, then a=0. We make no assertion that these identities hold for every measurable dynamical system. For rational maps the positive-Lyapunov dimension formula is part of the published theory discussed in the references. In an uncentered formulation the bounded-sum hypothesis itself implies zero mean.

## 1. The Hilbert-space reduction (classical; reconstructed proof)

**Proposition 1.** Suppose T preserves a probability measure m and φ∈L²(m). Then

    sup_(n≥1) ||S_n φ||₂ < ∞

if and only if there exists u∈L²(m) with φ=u∘T−u m-almost everywhere. If the supremum is C, a transfer can be chosen with ||u||₂≤C. Conversely any such u gives ||S_nφ||₂≤2||u||₂. Neither ergodicity nor invertibility is needed.

**Proof.** The Koopman operator Uv=v∘T is a linear isometry on L²(m). Define

    A_N = (1/N) Σ_(n=1)^N S_nφ.

Its norm is at most C. Since (I−U)S_nφ=φ−U^nφ,

    (I−U)A_N = φ − (1/N)U S_Nφ.

The last term has norm at most C/N. A bounded sequence in a Hilbert space has a weakly convergent subsequence; let A be its weak limit. Bounded linear operators preserve weak convergence, whereas the displayed right side converges strongly to φ. Thus (I−U)A=φ and ||A||₂≤C by weak lower semicontinuity. Set u=−A. The converse follows from the exact telescoping identity S_nφ=u∘T^n−u. Finally, invariance gives ∫S_nφ dm=n∫φ dm, so the hypothesis implies ∫φ dm=0. ∎

The cohomology step is standard, not a newly solved part of the historical question. A published formulation appears in El Abdalaoui–El Machkouri–Nogueira (2010), p.109. The proof above does not require summable correlations or an asymptotic variance formula.

**Corollary 1.1.** For an L² transfer u,

    S_nφ/√n → 0   m-almost everywhere.

**Proof.** For ε>0, invariance and the tail-sum bound for the integrable variable |u|² give

    Σ_n m(|u∘T^n|>ε√n) = Σ_n m(|u|²>ε²n) < ∞.

Borel–Cantelli, followed by ε through positive rationals, yields u∘T^n/√n→0. The telescoping formula completes the proof. ∎

This is a growth estimate, not pointwise boundedness of the sums.

## 2. What the exponential change of measure actually proves

**Proposition 2.** Let f preserve m, let the positive branch Jacobian J_m f exist, and suppose

    log J_m f − κ log|Df| − a = u∘f−u,

where u is finite m-almost everywhere. Then

    dν = e^(−u) dm

defines a measure equivalent to m and sigma-finite. On injective branches,

    J_ν f = e^a |Df|^κ.

It is a finite measure precisely when ∫e^(−u)dm<∞. In that case it can be normalized to a conformal probability measure. When a=0 the factor e^a disappears.

**Proof.** Positivity and finiteness of e^(−u) almost everywhere imply equivalence. The sets {|u|≤k}, together with an m-null exceptional set assigned ν-measure zero, cover the space up to a null set and have ν-measure at most e^k; hence ν is sigma-finite. For any measurable A on an injective branch, the change-of-variables identity, valid also for extended nonnegative integrals, gives

    ν(fA) = ∫_A e^(−u∘f) J_m f dm
          = ∫_A e^(−u∘f+u) J_m f dν
          = ∫_A e^a |Df|^κ dν.

The formula for total mass is the definition. ∎

In general ν is not f-invariant. It is the geometric conformal reference measure obtained by changing an invariant measure. Reversing the sign to e^u would not cancel the coboundary.

When f is ergodic and u,v are two finite real transfers for the same φ, u−v is f-invariant and hence constant almost everywhere. Thus exponential nonintegrability cannot be repaired by selecting another finite transfer in that same cohomology equation.

## 3. A finite-alphabet obstruction to exponential integrability and pointwise bounds

Let Ω={0,1}^N with independent fair bits, probability m, and the left shift T. Let K(ω) be the number of initial zeros before the first 1. The exceptional all-zero sequence is null. Then

    m(K=k)=2^(−k−1),     k=0,1,2,... .

The geometric recursion gives

    E[K]=1, E[K²]=3, E[K³]=13, E[K⁴]=75.

For completeness, K has the mixture distribution 0 with probability 1/2 and 1+K' with probability 1/2, where K' has the same distribution. For j≥1 its moments therefore satisfy

    M_j = Σ_(i=0)^(j−1) binom(j,i) M_i,   M_0=1,

giving the four displayed values directly.

Set

    u=3−K²,        φ=u∘T−u.

Then ∫u dm=0 and ||u||₂²=75−9=66, so φ∈L² and

    sup_n ||S_nφ||₂² ≤ 264.

However

    ∫e^(−u)dm = e^(−3) Σ_(k≥0) e^(k²) 2^(−k−1) = ∞,

since the summands do not tend to zero. Ergodicity of the fair shift implies every other finite transfer is u plus a constant, so its negative exponential also has infinite integral.

For every fixed L, the event {K≥L} has positive probability; ergodicity implies almost every orbit visits it infinitely often. Intersect over L. Then K(T^nω) is unbounded and

    S_nφ(ω)=u(T^nω)−u(ω)

is unbounded below for almost every ω. Its absolute value is therefore unbounded along the orbit, despite the uniform L² bound.

This example has positive entropy and a finite alphabet. It is **not** a counterexample to Problem 2.5: the chosen φ has not been shown to equal the particular Jacobian-minus-derivative discrepancy for a holomorphic map with κ=dim_H(m). It refutes only the proposed deductions from abstract L² boundedness to exponential integrability or pointwise boundedness. Replacing u by −u gives the analogous obstruction for the opposite exponential sign.

## 4. A sufficient geometric bridge, with the missing hypotheses explicit

**Proposition 3 (all-scale finite-landing criterion).** Let κ>0 and let ν be a Borel measure on a metric space X, with m equivalent to ν. Suppose there is a ν-conull set X₀ such that, for each x∈X₀, constants a_x>0, M_x<∞ and r_x>0 exist with the following property. For every 0<r<r_x there is an integer n=n(x,r)≥1 such that:

1. f^n is injective on B(x,r)∩X;
2. the iterated branch change-of-variables identity holds there with Jacobian |Df^n|^κ;
3. |Df^n(y)|≥a_x/r for ν-almost every y∈B(x,r)∩X;
4. ν(f^n(B(x,r)∩X))≤M_x.

Then m≪H^κ.

**Proof.** By the branch identity,

    M_x ≥ ∫_(B(x,r)∩X) |Df^n|^κ dν
        ≥ (a_x/r)^κ ν(B(x,r)∩X).

Consequently ν(B(x,r))≤C_x r^κ for all sufficiently small r, with C_x=M_x/a_x^κ. One can replace X₀ by the countable union of sets E_j on which C_x≤j and r_x≥1/j. If A is H^κ-null, cover A by sets U_i of diameters 0≤d_i<1/(2j), with Σ_i d_i^κ arbitrarily small. For each positive-diameter U_i meeting A∩E_j choose x_i in that intersection. Then U_i⊂B(x_i,2d_i), and

    ν*(A∩E_j) ≤ Σ_i ν(B(x_i,2d_i)) ≤ j 2^κ Σ_i d_i^κ.

Thus ν*(A∩E_j)=0. Any zero-diameter cover member meeting A∩E_j is a singleton {x} with x∈E_j, and ν({x})≤j r^κ for every 0<r<1/j, so ν({x})=0. There are at most countably many such members. Discard their zero-mass contribution and apply the preceding estimate to the positive-diameter members. Countable union and the conull property give ν(A)=0, hence m(A)=0. ∎

Here ν* is the outer measure induced by ν. Consequently no measurable selection of n(x,r), a_x, M_x, or r_x is needed, and the E_j need not themselves be measurable.

**Corollary 3.1.** Assume the hypotheses of Proposition 2 with a=0 and ∫e^(−u)dm<∞. If properties 1–3 of Proposition 3 hold for ν-almost every point at all small scales, property 4 follows with the global constant M=ν(X). Thus m≪H^κ.

This allows unbounded transfers; the required one-sided exponential moment suffices. An essentially bounded-below transfer is a simpler sufficient hypothesis. No claim is made that these analytic or all-scale geometric conditions follow from the original L² hypothesis.

The criterion also works when ν(X)=∞, provided the image of each chosen branch lands in sets with the uniformly finite mass required in property 4. Sigma-finiteness alone does not supply such a bound.

## 5. Why a subsequence of good scales cannot replace all scales

Here is an independent elementary geometric obstruction. Define integers b_n starting with b_0=0 as follows. In stage j≥1, start at −(j−1), increase by 1 at each step to +j, and then decrease by 1 at each step to −j. Stage j uses 4j−1 steps. Hence b_n=O(√n), it takes the values +j and −j along subsequences, and |b_(n+1)−b_n|=1.

Set

    ℓ_n=4^(−n)(4/3)^(b_n),        ℓ_0=1.

At each level replace every parent interval by its two endpoint subintervals of length ℓ_n. The ratios ℓ_n/ℓ_(n−1) are 1/3 or 3/16, so the construction is separated. Let E be its compact limit set and let μ assign mass 2^(−n) to each level-n interval.

**Proposition 4.** This probability measure is exact dimensional with dimension 1/2, but H^(1/2)(E)=0 and

    liminf_(r↓0) μ(B(x,r))/r^(1/2)=0   for every x∈E.

**Proof.** Two distinct level-n intervals are separated by at least ℓ_n. Indeed, at the first level k at which their ancestors differ, the gap is ℓ_(k−1)−2ℓ_k≥ℓ_k≥ℓ_n. Thus a ball of radius ℓ_n intersects at most three level-n intervals. If ℓ_n≤r<ℓ_(n−1), the ball B(x,r) contains the level-n interval containing x up to an endpoint of μ-measure zero, and intersects at most three level-(n−1) intervals. Therefore

    2^(−n) ≤ μ(B(x,r)) ≤ 3·2^(−n+1).

The endpoint issue can also be avoided by replacing open balls by closed balls; μ has no atoms since the cylinder masses tend to zero. Since b_n=o(n), log ℓ_n=−n log4+o(n). The two mass estimates and the bounded adjacent-length ratios show that the local dimension exists and equals log2/log4=1/2. The usual elementary mass-distribution covering argument then gives dim_H(μ)=1/2: for any s<1/2 the eventual ball upper bounds by r^s on countably many uniform subsets yield a lower dimension bound; the level covers give dim_H(E)≤1/2.

At the end of stage j, b_n=−j. The 2^n level-n intervals cover E and have total half-dimensional cost

    2^n ℓ_n^(1/2)=(4/3)^(−j/2)→0.

Their maximum diameter tends to zero, proving H^(1/2)(E)=0. At the positive peak of stage j, use r=ℓ_n and the bound by three level-n intervals:

    μ(B(x,ℓ_n))/ℓ_n^(1/2) ≤ 3(4/3)^(−j/2)→0.

This proves the lower-density assertion. ∎

This is **not** a holomorphic dynamical counterexample. It shows precisely why recurrence producing good endpoint values of u at infinitely many iterates, even combined with an exact-dimension formula, cannot by itself replace the all-scale estimate in Proposition 3.

## 6. Exact remaining gap

The L² assumption yields a measurable transfer. It does not, as an abstract matter, supply the one-sided exponential moment, locally finite landing masses, or an all-scale Hausdorff upper-density estimate. The two examples above certify failures of these shortcuts outside the original constrained class; they neither prove nor disprove that holomorphic quasi-repeller structure repairs the failures. Resolving that repair for the original general class remains the missing step.
