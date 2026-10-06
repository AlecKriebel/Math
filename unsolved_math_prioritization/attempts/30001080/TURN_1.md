# Turn 1: canonical-law characterization by symmetric lazy Markov transports

**Corrected historical author version.** This first-turn canonical theorem remains valid. Its mathematical Sections 1–6 below are preserved literally from the original snapshot. The later abstract-state repair is Theorem A in TURN_2.md. Current scope and source credit are in SCOPE_AND_CREDIT.md; the narrower non-discrete strict Cox allocation question remains unresolved.

## 1. Setting

Let G be a locally compact second countable Hausdorff Abelian group, additively written. Let M* be the standard Borel space of nonzero locally finite Radon measures on G, with its vague topology and evaluation σ-field. Define θ_sµ(B)=µ(B+s). Let Q be a σ-finite measure on M*.

A Markov transport is a measurable kernel K(µ,s,dt) from M*×G to G, with row mass one, satisfying covariance

    K(θ_uµ,s−u,B−u)=K(µ,s,B).

It preserves µ if ∫K(µ,s,B)µ(ds)=µ(B) for every µ and B. Suppose that for every such invariant preserving Markov kernel,

    ∫Q(dµ)∫K(µ,0,dt) f(θ_tµ)=∫f(µ)Q(dµ)             (A)

for all nonnegative measurable f. Then Q satisfies the full Mecke identity

    ∫Q(dµ)∫g(θ_tµ,−t)µ(dt)=∫Q(dµ)∫g(µ,t)µ(dt)       (M)

for all nonnegative measurable g. Consequently Q is mass-stationary, by the established Mecke/Palm characterization and its equivalence with mass-stationarity (Last–Thorisson 2009, (2.7), Theorem 6.3). Conversely mass-stationarity implies (A) by their transport invariance theorem.

The exclusion of the zero measure is essential and inherited from the source. It is not an optional technical convenience: the Dirac law of the zero measure cannot be used as a meaningful counterexample to the nonzero source problem.

## 2. A finite symmetric test measure

Choose a symmetric compact neighborhood C of 0. Since Q is σ-finite, there is a Borel h:M*→(0,1] with ∫h dQ<∞: use a countable partition into finite-Q sets and positive summable weights. This h is a function of the measure itself, so it does not violate measure-only measurability.

For µ∈M* and s,t∈G put

    a(µ;s,t) = h(θ_sµ)h(θ_tµ) 1_C(t−s)
               /[(1+µ(s+C))(1+µ(t+C))].

This function is measurable, symmetric in s,t, and covariant under simultaneous translation. Its row integral r(µ,s)=∫a(µ;s,t)µ(dt) obeys

    0≤r(µ,s)≤h(θ_sµ) µ(s+C)/(1+µ(s+C))≤h(θ_sµ)≤1.

Write R(µ,t)=(θ_tµ,−t). This is a Borel involution on M*×G. Define the finite measure

    m(dµ,dt)=Q(dµ) a(µ;0,t) µ(dt).

Indeed m(M*×G)=∫r(µ,0)Q(dµ)≤∫h dQ<∞. Also a(µ;0,t)=a(θ_tµ;0,−t).

## 3. Every symmetric gate gives an admissible Markov kernel

Let b:M*×G→[0,1] be any measurable R-invariant function, so b(µ,t)=b(θ_tµ,−t). Define

    a_b(µ;s,t)=a(µ;s,t)b(θ_sµ,t−s),
    r_b(µ,s)=∫a_b(µ;s,t)µ(dt),
    K_b(µ,s,dt)=a_b(µ;s,t)µ(dt)+(1−r_b(µ,s))δ_s(dt).

R-invariance of b makes a_b symmetric. Thus 0≤r_b≤1 and K_b is Markov. Its covariance is immediate from the displayed definitions. Tonelli and symmetry give, for nonnegative φ,

    ∫µ(ds)∫a_b(µ;s,t)φ(t)µ(dt)=∫φ(t)r_b(µ,t)µ(dt).

Adding the holding term proves µK_b=µ. In particular every b used below is genuinely allowed by (A); no bounded weighted non-Markov kernel is substituted.

For a Borel A with Q(A)<∞, apply (A) to 1_A. Subtract the finite holding contribution to obtain

    ∫[1_A(θ_tµ)−1_A(µ)] b(µ,t) m(dµ,dt)=0.            (B)

The two marginal measures of b m are finite. They agree on all finite-Q sets by (B); partitioning M* into countably many finite-Q sets shows that they agree on every Borel set. Consequently (B) holds with 1_A replaced by any bounded measurable f, even when Q(f) is infinite. This step avoids an infinity-minus-infinity cancellation.

## 4. Recover reversal off the stabilizer

Let ν=m−R_*m, a finite signed measure. It is antisymmetric: R_*ν=−ν. For any bounded f, put d_f(µ,t)=f(θ_tµ)−f(µ). Then d_f∘R=−d_f. Equation (B) and change of variables by R imply

    ∫b d_f dν=0

for every measurable R-invariant b∈[0,1]. The signed measure d_fν is R-invariant. For any Borel E⊂M*×G, use b=(1_E+1_(R⁻¹E))/2. It follows that (d_fν)(E)=0. Therefore d_fν=0 as a signed measure.

The standard Borel space M* admits a countable family (A_j) of Borel sets separating its points. Take f=1_(A_j). Whenever θ_tµ≠µ, at least one d_f equals ±1. The preceding identities imply ν vanishes off

    H = {(µ,t): θ_tµ=µ}.

Countability is essential here. It is supplied by the canonical Radon-measure state space, not tacitly assumed for an arbitrary auxiliary probability space.

## 5. The stabilizer contributes no reversal defect

Fix µ. Its period subgroup H_µ={t:θ_tµ=µ} is closed because translations act continuously on Radon measures in the vague topology. Hence H_µ is locally compact Abelian. The restriction µ|_(H_µ) is a locally finite invariant measure on H_µ: translation by any h∈H_µ preserves both µ and H_µ. It is therefore either zero or a constant multiple of Haar measure on H_µ. In either case it is invariant under t↦−t.

For t∈H_µ, θ_tµ=µ and µ(t+C)=µ(C). Thus

    a(µ;0,t)=h(µ)² 1_C(t)/(1+µ(C))²,

an even function of t because C is symmetric. On H, the reversal R fixes µ and sends t to −t. The preceding pointwise Haar argument gives m|_H=R_*(m|_H), without requiring a measurable choice of Haar normalizations as µ varies. The set H itself is Borel, as the equalizer of the Borel translation map and the coordinate projection.

Together with Section 4, this proves m=R_*m on the whole product space. Periodic measures, measures supported on a subgroup, discrete stabilizers, and diffuse measures with zero mass on their stabilizer are all included.

## 6. Remove the positive weight and exhaust G

Let c(dµ,dt)=Q(dµ)µ(dt), the canonical Campbell measure. The previous equality reads

    w c = w R_*c,        w(µ,t)=a(µ;0,t)=w∘R.

On M*×C the weight w is strictly positive. Division by w, or monotone use of min(k,1/w), shows c and R_*c agree there, allowing infinite values after deweighting.

A locally compact second countable group admits an increasing sequence of symmetric compact neighborhoods C_n covering G. Repeat the argument for each C_n. Monotone convergence proves c=R_*c globally, which is exactly (M).

The classical Mecke characterization now gives a stationary σ-finite measure whose Palm measure is Q; Last–Thorisson's mass-stationarity/Palm equivalence finishes the stated canonical theorem. No finite intensity, absolute continuity with respect to Haar measure, ergodicity, finite total random mass, or positive density is added.

## 7. Historical gap and later disposition

At the original turn-1 checkpoint, the arbitrary ambient joint-state issue and the Cox subclass issue were separate gaps. TURN_2 Theorem A closes the former while retaining arbitrary measurable Ω and possibly non-σ-finite ξ-marginal. Theorem B only establishes the canonical intensity-background singleton-matching theorem; its identification with Last's narrower OWR closing allocation class was not verified and is withdrawn in the corrected version. TURN_3 supplies separately scoped probability-law Markov and discrete σ-finite allocation results without closing the full non-discrete allocation gap.

This is the first of the original two author turns. The unchanged original file is bound in HISTORICAL_INPUT_MANIFEST.json and preserved in the original audit snapshot. No historical novelty or full original-OWR resolution endorsement follows from this corrected first-turn document.
