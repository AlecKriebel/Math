# Verification of Ivrii's counterexample to Problem 5.57

## 1. Claim and credit

The counterexample and its random lacunary construction are due to **Oleg Ivrii**, [arXiv:2609.18785v1](https://arxiv.org/abs/2609.18785v1), Theorem 1.1. We verify the portions needed for Baernstein's question below. This is not a claim of an independently discovered resolution. The occupation estimate in §3 is a nonsharp proof variant; no novelty is asserted for it.

Write m for planar Lebesgue measure. There exists a holomorphic f on the unit disc and a full arc-length-measure set E of boundary points such that, for every ζ∈E:

1. liminf_(r→1) |f(rζ)|=0 and limsup_(r→1) |f(rζ)|=∞;
2. for every A>1, the image of Γ_A(ζ)={z∈D: |z−ζ|<A(1−|z|)} satisfies
   m(f(Γ_A(ζ))∩B(0,R))/(πR²)→0 as R→∞.

Both statements will hold for almost every sample of Ivrii's series. Standard probability facts used are Gaussian transition densities, independent increments, the strong Markov property, planar Brownian recurrence and unboundedness, the reflection-principle maximal inequality, Borel–Cantelli, and Tonelli/Fubini. Planar Brownian motion is normalized by E|B_t|²=t, with density p_t(x)=(πt)^−1 exp(−|x|²/t).

## 2. Holomorphic series and a uniform cone estimate

Let ξ_k be independent complex Gaussians with density π^−1 exp(−|z|²), put a_k=ξ_k/√k, and set

f(z)=Σ_(k≥1) a_k z^(2^k),    S_n(θ)=Σ_(k≤n) a_k exp(i2^kθ).

Since P(|ξ_k|>k^(1/4))=exp(−√k) and this is summable, almost surely there is a finite M such that |a_k|≤M k^(−1/4) for every k. Fix such coefficients. The series converges absolutely and uniformly on each compact subdisc: for ρ<1 it is bounded termwise by Mρ^(2^k), a summable sequence. Consequently f is holomorphic.

If ζ=exp(iθ), z∈Γ_A(ζ), and

2^(−n−1)<1−|z|≤2^(−n),

then, for k≤n,

|z^(2^k)−ζ^(2^k)|≤2^k|z−ζ|≤A2^(k−n).

For k>n, |z|^(2^k)≤exp(−2^(k−n−1)). Thus

|f(z)−S_n(θ)|≤M[A Σ_(k≤n) k^(−1/4)2^(k−n) + Σ_(k>n) k^(−1/4)exp(−2^(k−n−1))]
                 ≤C_A n^(−1/4),  n≥1.                         (1)

For completeness, split the first sum at floor(n/2). Its lower part is at most 2·2^(−n/2), and its upper part at most 2·(n/2)^(−1/4). These are O(n^(−1/4)). The second sum is at most n^(−1/4)Σ_(j≥1)exp(−2^(j−1)), also O(n^(−1/4)). The constants are independent of θ and z. Points with |z|<1/2 form a compactly contained initial portion and cause no asymptotic issue.

## 3. An elementary small-radius sausage bound

For 0<ε<1, let K_ε be the closed ε-neighborhood of the Brownian path B([0,1]). We prove

E m(K_ε) ≤ π exp(4)/log(1/ε).                                  (2)

For x∈C let τ_x=inf{t≥0: |B_t−x|≤ε}. On {τ_x≤1}, the stopping location y=B_(τ_x) has |y−x|≤ε. For ε²≤s≤1, the Gaussian transition density gives

P_y(B_s∈B(x,ε))
  = ∫_(B(x,ε)) (πs)^−1 exp(−|u−y|²/s) dm(u)
  ≥ exp(−4) ε²/s,

because |u−y|≤2ε. By the strong Markov property, the expected occupation time of B(x,ε) during [0,2], conditional on hitting its closed ε-disc by time 1, is at least

∫_(ε²)^1 exp(−4)ε² ds/s = 2 exp(−4)ε² log(1/ε).

The interval of integration after τ_x lies in [0,2]. Therefore

E ∫_0² 1_(B(x,ε))(B_t) dt
 ≥ P(τ_x≤1)·2 exp(−4)ε² log(1/ε).

Integrating over x, the left side is exactly 2π ε² by Tonelli. The integral of P(τ_x≤1) is E m(K_ε). Division proves (2). No precise asymptotic constant is required.

## 4. Exponentially shrinking Brownian neighborhoods have density zero

Fix γ>0 and define W_γ=∪_(t≥0) B(B_t,exp(−γt)). On the time slice n≤t≤n+1, this set lies in B_n+K_n, where K_n is the exp(−γn)-neighborhood of the increment path B_(n+s)−B_n, 0≤s≤1. For n≥1, (2) gives E m(K_n)≤C_γ/n. Moreover, K_n is independent of B_n.

Consequently, for R≥1,

E m((B_n+K_n)∩B(0,R))
 = E ∫_(K_n) P(B_n∈B(0,R)−u) dm(u)
 ≤ min(1,R²/n) E m(K_n)
 ≤ C_γ min(1/n,R²/n²).                                        (3)

Here p_n≤1/(πn). The n=0 slice has finite expected area: it lies in a disc of radius 1+sup_(t≤1)|B_t|, and the reflection-principle bound gives a finite second moment of that supremum. Summing (3) yields

E m(W_γ∩B(0,R))≤C'_γ(1+log(R+1)).                            (4)

For R=2^j, the expected normalized area is O((j+1)/4^j), a summable sequence. Tonelli implies that the sum of these nonnegative normalized areas is finite almost surely; they therefore tend to zero. If 2^j≤R<2^(j+1), monotonicity bounds the normalized area at R by four times the normalized area at 2^(j+1). Thus W_γ has density zero at infinity almost surely.

This proves the bound needed from Ivrii's Lemma 2.2 without importing a sharp Wiener-sausage asymptotic or the lower-envelope result used for his separate exact-range theorem.

## 5. Brownian representation and the quantifiers

For each fixed θ, the increments of S_n(θ) are independent circular Gaussians of variances 1/n. Hence the sequence (S_n(θ)) has the same law as (B_(H_n)), where H_n=Σ_(k≤n)1/k. This assertion is for one fixed θ at a time; no independent Brownian processes indexed by every θ are assumed.

Let γ=1/16. The elementary bound H_n≤1+log n implies, for all sufficiently large n,

n^(−1/8)≤exp(−H_n/16).

For a fixed θ, it follows from §4 and equality of sequence laws that

U_θ=∪_(n≥N_0) B(S_n(θ),n^(−1/8))

has density zero at infinity with probability one, where N_0 can be chosen absolute. The event is jointly measurable in (θ,ω): membership in this countable union of discs is measurable, disc-intersection area is a nonnegative integral, and density zero can be tested on the countable radii 2^j. Fubini therefore gives a probability-one coefficient event on which U_θ has density zero for almost every θ.

Fix coefficients in that event and the coefficient-bound event of §2. For every good θ and **any** A>1, (1) implies

C_A n^(−1/4)<n^(−1/8)

for all sufficiently large n. The image under f of the corresponding tail of Γ_A(exp(iθ)) is contained in U_θ. The finitely many initial annular pieces have closure in a compact subdisc, so their image is bounded. Bounded sets have density zero. Therefore f(Γ_A(exp(iθ))) has density zero. The good θ-set is independent of A, because U_θ is independent of A and (1) holds for every A with its own finite constant. There is no uncountable intersection of probability-one events in this step.

## 6. Radial oscillation rules out angular limits

Planar Brownian motion is recurrent and unbounded, so almost surely liminf_(t→∞)|B_t|=0 and limsup_(t→∞)|B_t|=∞. These conclusions survive sampling at H_n. Indeed the maximal inequality

P(sup_(0≤s≤t)|B_s|>r)≤4 exp(−r²/(2t))

and H_(n+1)−H_n=1/(n+1) imply

P(sup_(H_n≤t≤H_(n+1))|B_t−B_(H_n)|>n^(−1/3))
 ≤4 exp(−(n+1)/(2n^(2/3))).

This is summable, so the oscillations between consecutive sampling times tend to zero almost surely. The sampled Brownian moduli therefore also have liminf zero and limsup infinity. Equality in law, followed by Fubini in θ, transfers both statements to S_n(θ) for almost every θ, almost surely.

Take r_n=1−2^(−n). Estimate (1), on the radius, shows f(r_n exp(iθ))−S_n(θ)→0. Hence the radial moduli have the stated liminf and limsup. No finite or infinite angular limit is possible at these θ. Intersecting the finitely many full-measure coefficient events used above produces one deterministic holomorphic function with all the required properties. By the classical Plessner theorem, almost every such boundary point is also a Plessner point.

## 7. Passing from density zero to the original capacity question

Fix one of the good ζ and a cone Γ_A(ζ). Its image is open, because f is nonconstant. Density zero supplies R so large that the compact set

K=overline(B(0,R)) \ f(Γ_A(ζ))

has positive area. Compactness follows because the image is open. Positive area implies positive logarithmic capacity; here is a direct energy check. Normalize area on K to a probability measure μ. The positive part of its logarithmic energy is finite, since

∫_(|u|<1) log(1/|u|) dm(u)=π/2

and μ has bounded density. More explicitly, the positive energy is at most π/(2m(K)). The negative part is bounded on K×K because K is bounded. Thus μ has finite logarithmic energy, implying cap(K)>0 by the energy definition of logarithmic capacity. Monotonicity gives cap(C\f(Γ_A(ζ)))>0.

Every ordinary Stolz triangle S at ζ is contained near its vertex in some Γ_A(ζ); the remaining part has compact closure in D and bounded image. Its image also has density zero, so the same argument applies. One can alternatively disprove the universal assertion using only symmetric Stolz triangles contained in a fixed Γ_A. Truncating any cone only decreases its image and cannot restore the proposed capacity-zero property.

We have a full-measure set of boundary points with neither an angular limit nor polar omitted sets. This disproves exactly Baernstein's proposed dichotomy, and also Collingwood's weaker area-zero version. The omission is compatible with the classical dense-image conclusion and with infinite area counted with multiplicities.
