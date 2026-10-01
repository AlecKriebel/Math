# No unrestricted pattern characterization of a noninteger power threshold

## Exact claim and scope

Let a **pattern** be a finite nonempty word whose letters are variables. Variables are replaced by nonempty finite words; there are no constant letters, length constraints, or injectivity conditions on these replacements. A word contains a pattern if one of its contiguous factors is such a replacement.

For a finite nonempty word `w`, a positive integer `d` is a period if `w[i]=w[i+d]` whenever both positions exist. For real `alpha>1`, let `B_alpha` be the words having a nonempty factor of length `l` and period `d` with `l/d >= alpha`. This is the source's threshold convention, including irrational alpha, rather than requiring a factor with exponent exactly alpha.

**Theorem.** For every real noninteger `alpha>1`, there is no set `P` of patterns, finite or infinite, whose occurrence characterizes `B_alpha` for words over arbitrary finite alphabets. More precisely, for every such alpha there is an explicit finite number `D` for which no such `P` works even on a single fixed alphabet of size `D`, or any larger alphabet. The set `P` is allowed to depend on alpha and on that fixed alphabet.

This does not assert nonexistence on *every* fixed small alphabet. Section 5 gives a genuine exception. It does answer the alphabet-unrestricted formulation of Shallit's Problem 38. The source does not prescribe a binary or other bounded alphabet in that question. Independent review must assess this quantifier interpretation separately from the proof. No priority or novelty assertion is made.

## 1. Closure forced by pattern occurrence

For a fixed alphabet `Sigma`, let `L_P(Sigma)` be all words containing an instance of a member of `P`. It is closed under every nonerasing endomorphism `h:Sigma* -> Sigma*`.

Indeed, write `w=u g(p) v`, where `p in P` and `g` is a nonerasing substitution. Then

`h(w)=h(u) (h composed with g)(p) h(v)`.

The composite is still nonerasing, so the displayed middle word is a pattern instance and a factor of `h(w)`. No enumeration, finiteness, or computability assumption on `P` enters this argument. Equally, a characterization valid on all finite alphabets must respect nonerasing morphisms between them.

## 2. Exact exponent of a distinct-letter cycle

Let `c_0,...,c_(s-1)` be pairwise distinct letters, `s>=2`, and put

`C=c_0 ... c_(s-1)`,

`W=C^n c_0 ... c_(r-1)`, where `n>=1` and `1<=r<s`.

The largest exponent of any nonempty factor of `W` is exactly

`E(W)=n+r/s`.

The entire word has period `s` and realizes that value. For the upper bound, take a factor `z` of length `l` with period `d`. If `d>=l`, then `l/d<=1`. Otherwise the first letter and the letter `d` places after it agree. In the infinite periodic word `C C C ...`, two letters agree if and only if their positions are congruent modulo `s`. Hence `s` divides `d`, so `d>=s` and

`l/d <= |W|/s = n+r/s`.

This checks every factor and every period, including factors that begin inside a cycle or inside a substituted block. It does not merely compare the exponents of two selected whole words.

## 3. Crossing an arbitrary noninteger threshold

Write `alpha=n+delta`, where `n=floor(alpha)>=1` and `0<delta<1`. Choose integers

`q=ceil(1/(1-delta))`, `r=q-1`, `D=floor(r/delta)+1`.

Then `q>=2`, `1<=r<q`, and

`r/q >= delta`, `D > r/delta >= q`.

In particular `D>q` and `r/D < delta`.

Work on the single fixed alphabet

`Sigma={c_0,...,c_(D-1)}`.

Define

`w=(c_0 ... c_(q-1))^n c_0 ... c_(r-1)`.

By Section 2, `E(w)=n+r/q >= alpha`, so `w in B_alpha`.

Define an endomorphism of this very same alphabet by

- `h(c_(q-1))=c_(q-1)c_q ... c_(D-1)`;
- `h(c_i)=c_i` for all other `i`.

It is nonerasing, and direct concatenation gives

`h(w)=(c_0 ... c_(D-1))^n c_0 ... c_(r-1)`.

Applying Section 2 again,

`E(h(w))=n+r/D < alpha`.

Thus `h(w)` contains no alpha-power anywhere, although `w` does. This violates the closure in Section 1, proving the theorem. The construction stays inside one finite alphabet; it is not a comparison that changes the allowed alphabet between the two sides of a fixed-alphabet characterization.

If a larger fixed alphabet is prescribed, use the same words and set `h` equal to the identity on its remaining letters. The proof is unchanged. The elementary Archimedean choices of `q,D` apply to irrational as well as rational delta; no rationality of alpha is required.

## 4. Concrete checks and the integer boundary

For `alpha=5/2`, take `q=2,r=1,D=3`. The word `ababa` has maximal factor exponent `5/2`. The map `a->a,b->bc,c->c` sends it to `abcabca`, with maximal factor exponent `7/3 < 5/2`.

For `alpha=19/10`, take `q=10,r=9,D=11`; the exponents are `19/10` and `20/11`. Equality at the input threshold is intentionally allowed, while the image inequality is strict.

For an integer `k>=2`, the single pattern `X^k` does characterize occurrence of a k-power: an instance is a k-power, and a factor of exponent at least k contains its first k complete periods. Consequently the noninteger restriction is essential. The proof does not address the different strict-threshold convention `alpha+`.

## 5. Why the alphabet qualification is necessary

On a unary alphabet, `B_alpha` is characterized by `X^ceil(alpha)` for every `alpha>1`: a unary word is bad precisely when its length is at least `ceil(alpha)`.

On a binary alphabet and `1<alpha<=3/2`, the two patterns `XX` and `XYZ` characterize `B_alpha`, where `X,Y,Z` are three distinct variables, with no requirement that their images differ. Every word of length at least three matches `XYZ`. Every binary word of length three either has adjacent equal letters, giving a square, or has the form `aba` with `a!=b`, giving exponent `3/2`. Thus all longer words are bad. The only bad length-two words are the squares, and words of length zero or one are not bad. Conversely, `XX` forces a square and `XYZ` forces length at least three, so both kinds of instances are bad in this range.

These examples rule out reading the theorem as an impossibility result for every individually fixed finite alphabet. No classification of all fixed-alphabet threshold exceptions is claimed or needed for the unrestricted question.

## Attribution and verification

Definitions and target: Jeffrey Shallit, “On Patterns and Pattern Avoidance,” in *Mini-Workshop: Combinatorics on Words*, Oberwolfach Reports 7 (2010), pp.2230–2236, especially Problem38 on p.2231, DOI [10.4171/OWR/2010/37](https://doi.org/10.4171/OWR/2010/37). The report credits James Currie and Julien Cassaigne with partial negative approaches. The campaign's earlier desk assessment already suggested the morphism-closure route. This proof develops that route explicitly; it does not claim it was historically unknown.

The accompanying standard-library checker exhaustively verifies bounded finite examples, all factor periods in those examples, pattern-matching closure controls, and the small-alphabet exceptions. Those checks are supplementary. The all-real-alpha theorem is proved in Sections1–3.
