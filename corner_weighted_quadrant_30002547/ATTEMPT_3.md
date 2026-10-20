# Attempt 3: Signed shuffles expose a false refined positivity conjecture

Date: 2026-10-20 UTC. Target: the negative-weight interval of Albert–Bousquet-Mélou (ABM) Conjecture 11. This report contains authored deductions and public citations only.

## Outcome and scope

**The radius conjecture is not proved or disproved here.** A proposed route through nonnegative fixed-projection contributions fails much more strongly than coefficient positivity alone:

1. For every fixed −1 < a < 0, there are horizontal and vertical Dyck projections whose complete signed shuffle sum is negative.
2. The stronger positivity assertion (P2) in ABM §6.3.1 is false. A fixed vertical Dyck path of half-length 13, with horizontal half-length 2, gives the exact polynomial

   G₁₃(a) = 13769 + 27300a + 13741a²
            = 210 − 182(a+1) + 13741(a+1)².

   Its negative coefficient directly contradicts (P2). This is **not** a counterexample to the unrefined positivity Conjecture 10 or the radius Conjecture 11.
3. An exact marked-corner convolution identifies why the parity theorem at a = −1 cannot simply be differentiated into a nonnegative representation.

The formulas below have proofs, not only finite tests. Two independent exact enumerators additionally verify the explicit counterexample.

## Primary-source inputs

- Michael Albert and Mireille Bousquet-Mélou, *Permutations sortable by two stacks in parallel and quarter plane walks*, [arXiv:1312.4487v3](https://arxiv.org/abs/1312.4487v3), §6.3.1 (P2), §6.3.2 (N2), and Conjectures 10–11. The inspected source states (P2) for a fixed vertical Dyck path, with the quarter-plane loops counted by length and corner count. Fixing total length therefore fixes horizontal length as well.
- William Kuszmaul, *Signed Enumeration of Upper-Right Corners in Path Shuffles*, [arXiv:1510.00777v2](https://arxiv.org/abs/1510.00777v2), Theorem 2.16 and Theorem 3.13. For fixed projections with r E's, l W's, u N's and d S's, the signed statistic D = #NW − #ES has distribution

  #{w : D(w)=k} = binom(r+u,u−k) binom(l+d,d+k).

This theorem concerns a different statistic from C = #NW + #ES. They agree in parity, not generally as nonnegative integers. The binomial convention is zero outside 0 ≤ bottom ≤ top.

All words are linear rooted walks. No last-to-first corner is included.

## 1. An exact family with two horizontal Dyck paths

Let n ≥ 1, fix the vertical path Vₙ = NⁿSⁿ, and consider the only two horizontal Dyck paths of half-length 2:

- Hₘ = EEWW, the mountain;
- Hₐ = EWEW, the alternating path.

Every shuffle of either horizontal word with Vₙ stays in the nonnegative quadrant: each coordinate is a prefix height of its own Dyck projection. Every shuffle has total half-length n+2.

Write Pₘ,ₙ(a) and Pₐ,ₙ(a) for the respective ordinary corner-count polynomials. Set

  Fₙ(a) = binom(n+2,2)²
          + [n(n+1)(n+2)²/3] a
          + 2 binom(n+2,4) a²,

and Kₙ = binom(n+1,2)².

### Lemma 1: Exact formulas

  Pₘ,ₙ(a) = Fₙ(a),
  Pₐ,ₙ(a) = Fₙ(a) + Kₙ(a²−1).

#### Proof

Kuszmaul's signed-count theorem, with r=l=2 and u=d=n, gives the same distribution of |D| for both shuffle classes. The support is 0,1,2. Its polynomial is

  binom(n+2,n)²
  + 2 binom(n+2,n−1) binom(n+2,n+1) a
  + 2 binom(n+2,n−2) binom(n+2,n+2) a²,

which simplifies to Fₙ(a).

In a shuffle of Hₘ and Vₙ, NW and ES cannot both occur. If an NW occurs before an ES, then a W precedes an E, contradicting Hₘ=EEWW. If the ES occurs first, then an S precedes an N, contradicting Vₙ=NⁿSⁿ. Hence C=|D| on every shuffle, proving Pₘ,ₙ=Fₙ.

For Hₐ=E₁W₁E₂W₂, the only way both corner types can occur is an N immediately before W₁ and an S immediately after E₂. Such a shuffle has exactly one corner of each type: C=2 and |D|=0. All other shuffles have C=|D|.

Count these mixed shuffles by the rank j of the N before W₁ and the rank k of the S after E₂. Here 1 ≤ j,k ≤ n. Before the marked NⱼW₁, E₁ may occupy any of j slots among N₁,…,Nⱼ₋₁. Between W₁ and E₂Sₖ, the remaining N's and the first k−1 S's are forced in their projection order. After Sₖ, W₂ may occupy any of n−k+1 slots among the remaining S's. Thus the number is

  sum(j=1,…,n) sum(k=1,…,n) j(n−k+1)
  = [n(n+1)/2]² = Kₙ.

Each of these Kₙ shuffles replaces the weight 1 in the |D|-polynomial by a² in the C-polynomial. This proves the second identity. ∎

The mechanism is especially transparent: the absolute-signed statistic erases two opposite corners. Their combined weight equals 1 at a=±1, but differs in the interior of [−1,0]. Positivity for the erased statistic cannot be transferred to the original one.

### Expanded alternating formula

Lemma 1 yields

  Pₐ,ₙ(a) = (n+1)³
     + [n(n+1)(n+2)²/3] a
     + [n(n+1)(2n²+2n−1)/6] a².

A direct check of its constant term is available without the signed-count theorem. Encode a shuffle by 0 ≤ x₁ ≤ x₂ ≤ x₃ ≤ x₄ ≤ 2n, where xᵢ is the number of vertical steps before the i-th horizontal letter. Each EᵢWᵢ gap avoids both corner types if it is empty or if it strictly crosses the N/S transition. At most one gap can cross. Both gaps empty give (2n+1)(n+1) choices; either crossing gap gives n²(n+1)/2 choices. Their sum is (n+1)³.

### Corollary 1: Negative entire shuffle classes throughout the open interval

For each fixed a,

  Pₐ,ₙ(a) = [a(a+1)/3] n⁴ + Oₐ(n³).

If −1 < a < 0, the leading coefficient is strictly negative. Therefore Pₐ,ₙ(a)<0 for all sufficiently large n. For example,

  Pₐ,₈(−1/2) = 729 − 2400/2 + 1716/4 = −42.

Thus no representation as a sum of nonnegative contributions preserving every pair of fixed Dyck projections can enumerate the original signed weights throughout this interval. This is stronger than ABM's already known fixed-class coefficient-positivity counterexample (N2).

## 2. Exact disproof of the stronger fixed-vertical assertion (P2)

For the fixed Vₙ and horizontal half-length 2, summing all possible horizontal Dyck projections gives

  Gₙ(a) = Pₐ,ₙ(a) + Pₘ,ₙ(a) = 2Fₙ(a) + Kₙ(a²−1).

Explicitly,

  Gₙ(a) = [(n+1)²(n²+8n+8)/4]
      + [2n(n+1)(n+2)²/3] a
      + [n(n+1)(5n²+5n−4)/12] a².

Its coefficients in b=a+1 are

  Gₙ(b−1) = (n+1)(n+2)
      − [n(n+1)(n²−11n−20)/6] b
      + [n(n+1)(5n²+5n−4)/12] b².

The linear coefficient is negative for every integer n ≥ 13. In particular,

  G₁₃(a) = 13769 + 27300a + 13741a²
          = 210 − 182b + 13741b².

This is the coefficient of total half-length 15 in the series of quarter-plane loops with vertical projection N¹³S¹³. If length rather than half-length is marked, it is the coefficient at length 30. Either convention gives the same negative coefficient in a+1. Consequently the precise assertion (P2) in ABM §6.3.1 is false.

The source reports checking (P2) for vertical half-length at most 5 and total half-length at most 10. The present example lies outside those reported ranges. The conclusion does not rely on suggesting that those finite checks were incorrect.

The same family even invalidates pointwise nonnegativity of the fixed-vertical slice for some negative weights:

  Gₙ(a) = [(a+1)(5a+3)/12] n⁴ + Oₐ(n³).

For every fixed −1<a<−3/5, Gₙ(a)<0 for all sufficiently large n. For instance,

  G₂₁(−9/10) = −6919/100.

### What this does not say

The unrefined coefficient Qₙ(a) sums over all vertical Dyck projections as well. The negative contribution above can be compensated by other vertical projections. There is no inference that Qₙ(a), its coefficients in a+1, or its conjectured radius are incorrect.

The conclusion is that a positivity proof must permit essential cancellations or regrouping across vertical projections, not merely across horizontal projections at fixed vertical path. In particular, proving the stronger (P2) can no longer be used as an intermediate target for Conjecture 10.

## 3. Exact signed marked-corner convolution

The following supplies a general algebraic route for investigating coefficients in a+1, while making their sign difficulty explicit.

For arbitrary horizontal and vertical words H,V, define

  S(H,V) = sum(w in Sh(H,V)) (−1)^{C(w)}.

If H contains r E's and l W's, and V contains u N's and d S's, Kuszmaul's theorem gives

  S(H,V) = sum(k in Z) (−1)^k binom(r+u,u−k) binom(l+d,d+k)
          = (−1)^u [z^{u+d}] (1−z)^{r+u}(1+z)^{l+d}.

Although this depends only on the four letter counts, it need not be nonnegative for non-loop subwords. For example, S(W,NN)=−1. If both words are balanced loops of half-lengths i,j, it reduces to binom(i+j,i).

Let H=h₁…hₚ and V=v₁…v_q. An admissible cell (i,j) is one with (hᵢ,vⱼ)=(W,N) or (E,S). It specifies the marked corner NW or ES, respectively.

### Lemma 2: Coefficient formula

The coefficient of bᵏ in P_{H,V}(b−1) is the sum over all chains of admissible cells

  i₁<…<iₖ,  j₁<…<jₖ

of

  product(r=0,…,k) S(h_{iᵣ+1}…h_{iᵣ₊₁−1}, v_{jᵣ+1}…v_{jᵣ₊₁−1}),

where (i₀,j₀)=(0,0) and (iₖ₊₁,jₖ₊₁)=(p+1,q+1). Empty words are allowed.

#### Proof

Expand each corner weight b−1 by marking a subset of corners with b and leaving all other corners with −1. A marked corner consists of an outward letter N/E followed by an inward letter W/S. Such corners cannot overlap. Their occurrences select a strictly increasing chain in both projection indices.

After removing the marked two-letter blocks, the remaining parts are independently shuffled intervals of H and V. There is no unmarked corner across a boundary of a marked block: its first letter is outward and its final letter inward. Therefore the signs factor into the signed shuffle sums of the intervening intervals. Conversely every chain and choice of interval shuffles reconstructs exactly one marked word. ∎

For k=1 this specializes to the useful derivative identity

  P′_{H,V}(−1)
   = sum(admissible (i,j)) S(h₁…hᵢ₋₁,v₁…vⱼ₋₁)
                         S(hᵢ₊₁…hₚ,vⱼ₊₁…v_q).

Even when H and V are Dyck loops, these prefix/suffix interval words need not be balanced loops. Their kernels can be negative. This is the exact obstruction to extending the positive a=−1 parity evaluation by naively marking corners.

## 4. Reproducible checks

The companion `verify_attempt_3.py` uses only the Python standard library and performs no network or repository operations.

- A dynamic program counts corner polynomials for both projection families and checks the formulas for n=1,…,40 with integers.
- A second algorithm enumerates all 54,810 shuffles for the n=13 counterexample by choosing horizontal positions, independently checks quadrant confinement, and directly inspects all adjacent letters.
- It checks the marked-corner derivative convolution against the DP.
- It evaluates the two negative examples with exact rational arithmetic.

The exhaustive n=13 histograms (corner counts 0,1,2) are:

- EWEW: (2744, 13650, 11011), with 8281 mixed-corner words;
- EEWW: (11025, 13650, 2730), with no mixed-corner words;
- total: (13769, 27300, 13741).

Both individual evaluations at a=−1 equal binom(15,2)=105, as required. Both total numbers of shuffles equal binom(30,4)=27405. These are normalization controls, not substitutes for the proofs.

## 5. Consequence for the requested radius problem

No bound with the desired exponential constant follows from these refined polynomials. The examples keep horizontal half-length fixed at 2, so their counts grow only polynomially with n. They cannot by themselves determine the exponential growth of the full Qₙ(a).

The value of the calculation is structural: it eliminates both fixed-shuffle nonnegativity and the stronger fixed-vertical (P2) positivity route. Any successful negative-weight proof of the piecewise radius must address cancellations across both Dyck projections or use another analytic representation. Equality with unconfined/half-plane radii cannot be inferred by positive-weight containment after either of these insufficient regroupings.
