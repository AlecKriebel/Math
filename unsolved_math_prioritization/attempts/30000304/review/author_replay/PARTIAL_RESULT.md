# Regenerative allelic partitions: a four-sample obstruction and a bounded-parent case

**Target:** 30000304 / OWR-1061-006.  
**Status:** candidate partial results; original conjecture unresolved; separate review pending.  
**Budget:** three substantive approaches. Priority is unestablished.

## 1. Exact target and interpretation

Martin Möhle's contribution, *Coalescent theory – simultaneous multiple collisions and sampling distributions*, [OWR 40/2005, printed pp. 2279–2282](https://ems.press/content/serial-article-files/46019?nt=1), puts independent Poisson mutations of rate r>0 on each ancestral branch, with every mutation producing a new allele. Its final conjecture, on p. 2281, concerns the family allowing simultaneous multiple mergers. It proposes that a regenerative composition structure can correspond to the resulting allelic partition only in the Kingman and star-shaped exceptions.

“Correspond” means that **some sampling-consistent ordering** of the exchangeable allelic partition is a regenerative composition structure. It does not mean that the chronological order of freezing must be regenerative. In a regenerative composition, conditional on its first part having size m, the remainder has the law of the composition on n−m. See Gnedin–Pitman [Definition 1.1 and Corollary 7.3](https://arxiv.org/abs/math/0307307). Their uniqueness statement does not assert that such an ordering always exists.

The source had already established the non-simultaneous Λ-coalescent case; the [2007 published theorem](https://doi.org/10.1017/S0963548306008212) is therefore prior work, not a resolution of this extension. We use the modern Ξ-measure description in [Dong, §2, equations (6)–(9)](https://arxiv.org/abs/0707.1606), which describes the same exchangeable simultaneous-merger family as the source's compatible measures Λ_j. No arbitrary independent choice of the Λ_j is assumed.

Write

    Δ = {x₁≥x₂≥⋯≥0 : Σxᵢ≤1},     Ξ=κ₀δ₀+Ξ₀,

where Ξ is a finite nonnegative measure and Ξ₀ has no atom at zero. Put S_k(x)=Σ_i x_i^k. The usual Poisson paintbox event measure away from zero is Ξ₀(dx)/S₂(x); κ₀ supplies the binary Kingman component. Every specified pair of ancestral blocks merges at total rate Ξ(Δ). Finite-sample rates are finite even when the paintbox event measure is infinite.

Equivalently, run the coalescent with freezing: each active ancestral block freezes at rate r and never merges again. The terminal frozen partition has the allelic law. This equivalence and the general sampling recursion are in Dong, §§2–3. All arguments below retain fixed r>0 and begin with singleton lineages.

## 2. A necessary identity from four samples

Define rates of **specified mergers**, not their total multiplicities:

    a = λ_{2;2;0},     b = λ_{3;3;0},
    c = λ_{4;4;0},     d = λ_{4;2,2;0}.

Thus d is the rate of one specified pairing of four blocks into two pairs; there are three such pairings. In terms of Ξ,

    a = κ₀ + Ξ₀(Δ),
    b = ∫ S₃/S₂ dΞ₀,
    c = ∫ S₄/S₂ dΞ₀,
    d = ∫ (S₂²−S₄)/S₂ dΞ₀.

In particular d>0 precisely when Ξ₀ gives positive mass to vectors with at least two positive coordinates. If d=0, the process is a Λ-coalescent, possibly including a Kingman component.

**Proposition 1.** If the allelic partition admits a regenerative composition ordering, then

    3d(a+r) = 2b(a−2b+c).                                      (1)

If d>0, there is consequently **at most one positive mutation rate** compatible with regeneration for this fixed coalescent:

    r* = 2b(a−2b+c)/(3d) − a.                                 (2)

If the displayed value is nonpositive, no r>0 can work. A positive value in (2) is only a candidate rate, not a sufficient condition.

### Proof

Restriction consistency, or direct expansion of the paintbox probabilities, gives the following table:

| Number of current blocks | Merger pattern | Number of specified possibilities | Rate of each |
|---|---|---:|---:|
| 2 | 2 | 1 | a |
| 3 | 2,1 | 3 | a−b |
| 3 | 3 | 1 | b |
| 4 | 2,1,1 | 6 | e:=a−2b+c−d |
| 4 | 3,1 | 4 | b−c |
| 4 | 2,2 | 3 | d |
| 4 | 4 | 1 | c |

For example, the restriction of one specified binary merger among three labels, after adding a fourth label, has three disjoint possibilities: that label remains separate, joins the merged pair, or joins the other singleton. Hence a−b=e+(b−c)+d. All rates in the table are nonnegative. Let g_n be the total rate of effective mergers among n blocks. Then

    g₂=a,   g₃=3a−2b,   g₄=6a−8b+3c−3d.                      (3)

Let P_n be the probability that n sampled individuals all have the same allele, and E_n the probability that they all have different alleles. Set P₁=E₁=1. Conditioning on the first effective merger or freezing event gives

    P₂ = a/(a+2r),
    P₃ = [3(a−b)P₂+b]/(g₃+3r),
    P₄ = [6eP₃+(4(b−c)+3d)P₂+c]/(g₄+4r),                 (4)
    E_n/E_{n−1} = nr/(g_n+nr).                              (5)

For (4), freezing before a single active block remains makes monomorphism impossible. Any merger reduces the number of active blocks as specified by the table. For (5), any merger creates a non-singleton terminal block, so the first event must freeze a singleton; delete that frozen singleton and use the remaining (n−1)-sample process.

Suppose a regenerative ordering exists and denote its first-part decrement probabilities by Q(n,m). A composition consisting entirely of singletons has probability Q(n,1)⋯Q(2,1). Therefore (5) fixes

    Q(n,1)=nr/(g_n+nr).

The regenerative-composition identities of Gnedin–Pitman, equations (25), (26) and (35), determine a normalized sequence Φ₀=0, Φ₁=1 by

    Φ_n/Φ_{n−1} = (g_n+nr)/(g_n+(n−1)r),                 n≥2,  (6)

and require its monomorphic probability to be

    P_n^reg = [Σ_{j=1}^n (−1)^{j+1} binom(n,j) Φ_j]/Φ_n.     (7)

These identities are necessary for **every possible regenerative ordering**; they do not assume a particular order of alleles. All denominators in (4) and (6) are positive because r>0.

Substitute (3) into (6), and (4) into the left side below. Straight rational simplification gives

    P₄−P₄^reg
      = 2r[3d(a+r)−2b(a−2b+c)]
        /[(a+2r)(3a−2b+3r)(6a−8b+3c−3d+4r)].                (8)

For clarity, the quantities needed to check this identity are

    Φ₂=(a+2r)/(a+r),
    Φ₃=Φ₂(3a−2b+3r)/(3a−2b+2r),
    Φ₄=Φ₃(g₄+4r)/(g₄+3r),
    P₄^reg=(4−6Φ₂+4Φ₃−Φ₄)/Φ₄.

Equality of the true and regenerative monomorphic probabilities forces the numerator in (8) to vanish. This proves (1) and (2). ∎

### Check against the already-known Λ case

When d=0, write a=∫1 dΛ, b=∫x dΛ and c=∫x² dΛ, including any atom at zero. Equation (1) reduces to

    (∫x dΛ)(∫(1−x)² dΛ)=0.

Nonnegativity implies either support at 0 or support at 1. This recovers the necessary part of Möhle's known theorem and excludes nontrivial mixtures of those two atoms. The zero measure gives the pure-singleton partition and is included as a degenerate exception. We do not claim the Λ conclusion as new.

## 3. A valid model passing the four-sample test and failing at five

This example shows why Proposition 1 does not settle the conjecture.

Consider independent paintbox events of these two kinds:

1. At rate 10, each active block independently chooses a common parent with probability 1/2; otherwise it remains a separate singleton parent. All common-parent choices merge.
2. At rate 1, each active block independently chooses one of two parents, each with probability 1/2, and blocks choosing the same parent merge.

These are standard exchangeable, restriction-consistent coalescent events. They correspond to

    Ξ = (5/2)δ_(1/2,0,…) + (1/2)δ_(1/2,1/2,0,…),

because event rate is Ξ-mass divided by S₂. Set r=3. Directly,

    a=3, b=3/2, c=3/4, d=1/8,

and both sides of (1) equal 9/4.

For n=5 the total transition rates of the block count to 4,3,2,1 respectively are

    25/8, 25/8, 5/2, 3/8,

so g₅=73/8. To check these numbers, in a type-1 event a binomial(5,1/2) number k chooses the common parent, leaving 6−k blocks for k≥2. In a type-2 event all choices agree with probability 1/16, and otherwise there are two blocks. Combine these probabilities with their event rates.

Equations (4)–(7), extended by this first-event recursion, give

| n | g_n | True P_n | Necessary regenerative P_n^reg |
|---:|---:|---:|---:|
| 2 | 3 | 1/3 | 1/3 |
| 3 | 6 | 1/5 | 1/5 |
| 4 | 63/8 | 7/53 | 7/53 |
| 5 | 73/8 | 2857/30687 | 934/10229 |

The last difference is 55/30687, so no regenerative ordering exists for this model. Passing the earlier identity was insufficient. Finite matching is not being promoted to an infinite composition structure.

## 4. A class with full nonregenerativity: bounded-parent full replacement

Here is a distinct structural exclusion, with no small-sample cutoff.

**Proposition 2.** Suppose κ₀=0 and Ξ₀ is a finite nonzero measure supported on vectors x with

    Σ_i x_i=1  and  #{i:x_i>0}≤M

for some fixed finite M. If Ξ₀ gives positive mass to vectors with at least two positive coordinates, then for every r>0 its allelic partition admits **no** regenerative composition ordering. If all its mass is at (1,0,…), it is the already-known star-shaped exception.

The full-replacement and uniform finite-parent bound are assumptions of this proposition, not conclusions about an arbitrary Ξ-coalescent. No Kingman component is allowed here.

### Proof: the allelic partition has at most M positive-frequency blocks

On this support, Cauchy–Schwarz gives S₂≥1/M. Hence the paintbox event intensity

    K = ∫ [1/S₂(x)] Ξ₀(dx)

is finite and strictly positive. Construct the process by these Poisson events, with no Kingman component. Its first event time T is exponential of rate K.

Before T, every ancestral lineage is a singleton. Each independently survives without mutation with conditional probability exp(−rT). Those mutated before T become distinct frozen singleton blocks. At T, let the drawn vector have m≤M positive coordinates. The surviving lineages independently choose these m parents. By the conditional strong law, the resulting m active blocks have positive frequencies

    exp(−rT)x₁, …, exp(−rT)x_m.

There is no remaining active dust because the coordinates sum to one. Thereafter only these finitely many active blocks can merge or freeze. Merging takes unions and freezing retains a block, so at most M positive-frequency terminal blocks are possible. All earlier frozen singleton blocks have frequency zero. Positive mutation rate makes this finite active process terminate almost surely; every effective merger or freezing reduces its number of active blocks, and freezing has positive rate whenever any remain.

There is positive probability of at least two positive-frequency terminal blocks. Indeed, with positive probability m≥2 at the first event. Conditional on that vector, all m active blocks can freeze before the next paintbox event. That event has probability

    Π_{k=1}^m [kr/(K+kr)] > 0.

The resulting m distinct frozen blocks have the displayed positive frequencies.

### Proof: regeneration contradicts a finite bound larger than one

For an exchangeable partition with frequencies (V_i), the EPPF for a specified partition into two blocks of size two is

    p(2,2)=E[Σ_{i≠j} V_i²V_j²].

It is positive when at least two positive frequencies occur with positive probability. Conversely, a bound of M positive-frequency blocks forces p(2,…,2)=0 when there are M+1 twos: dust cannot create a repeated sample allele.

Suppose there were a regenerative ordering with decrements Q. The unordered shape (2,2) has only the ordered size sequence (2,2), so

    P(C₄=(2,2))=3p(2,2)=Q(4,2)Q(2,2)>0.

Use the Gnedin–Pitman representation of regenerative composition structures by a drift δ≥0 and a measure ν on (0,1], with ∫xν(dx)<∞. Its decrement formula for n≥m≥2 is

    Q(n,m) = binom(n,m) ∫ x^m(1−x)^(n−m) ν(dx) / Φ_n,

with the usual killing mass permitted at x=1. The drift contributes only to m=1. In particular Q(4,2)>0 forces ν((0,1))>0. It follows that Q(2j,2)>0 for every j≥1, including j=1. The regenerative product rule then implies

    P(C_(2M+2)=(2,…,2)) = Π_{j=1}^{M+1} Q(2j,2) > 0,

contrary to the bound of M positive-frequency alleles. This proves the proposition. ∎

For the star-shaped control, the first event leaves exactly one positive-frequency allele of mass exp(−rT), with all other individuals in singleton alleles. A regenerative ordering is furnished by the multiplicative range of a subordinator with drift r and killing rate K: it has initial dust and one terminal interval. This is the classical hook example, not a new family.

## 5. Exact remaining gap

Proposition 1 excludes every mutation rate except possibly one for a genuinely simultaneous coalescent. Proposition 2 excludes all rates for bounded-parent full replacement. Neither proves the conjecture for an arbitrary Ξ measure.

In the remaining regime, equation (1) may hold at a positive r, while further finite-sample constraints still have to be imposed. The example in §3 proves that equation (1) alone is not sufficient. No argument here forces the double-pair rate d to vanish from **all** the regenerative identities, and no compatible nonexceptional infinite family has been constructed. In particular, a nonnegative finite collection of inferred rates or decrements would not establish an admissible Ξ measure or a regenerative composition structure in all sample sizes.

The bounded-parent proof does not extend automatically to events with residual dust, unbounded parent number, an infinite event rate, or a Kingman component. In those situations the final partition may have unboundedly many positive-frequency alleles, so its key support contradiction disappears.

The original target is therefore **unsolved**, with the precise restrictions above. All classical representation and sampling-recursion inputs are credited; no priority or exhaustive-literature claim is made.

## 6. Checks

The accompanying verifier uses exact rational arithmetic and labeled finite set partitions to compute small-sample coalescent-with-freezing probabilities for explicit finite paintbox models. It checks the four-sample identity, the five-sample witness, positive Kingman/star controls, and bounded-parent zero-probability controls. These computations are finite diagnostics; the general necessary identity and the all-sample bounded-parent result are proved above.
