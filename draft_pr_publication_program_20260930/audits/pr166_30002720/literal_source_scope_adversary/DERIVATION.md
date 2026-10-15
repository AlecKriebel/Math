# Independent derivation and adversarial checks

This derivation was written without reading the author source audit, verifier, verification outputs, review files, status, gate, or frozen verdicts. Its target is the exact candidate SHA256 `c72a38099e93b4d593be231e8f0c4ad726a399c3d61283da9f7b1f7e55801a5c`.

## Target and success criteria

Fix the stationary binary Markov source with initial probabilities `(1/2,1/2)`, same-symbol probability `q=3/4`, and change-symbol probability `r=1/4`. Input strings are independent copies of that source. The target is the existence of one deterministic rank proportion `t` strictly between zero and one, outside all probability-cylinder boundaries, such that for every deterministic sequence of real numbers `c_n`, the distributions of `(Y_n(floor(nt)+1)-c_n)/sqrt(n)` are not tight.

Checking only process non-tightness, a boundary marginal, a changing rank proportion, a cost that charges singleton reading, random rank, or random centering would not establish this target. Numerical finite identities are diagnostics; asymptotic success requires a proof.

## Quantile coordinates preserve the actual algorithm

For a finite word `w`, assign an ordered interval of length `pi(w)` by recursive subdivisions with the source probabilities. The resulting almost-everywhere order-preserving map from a uniform `U` to its infinite string `h(U)` gives the correct Markov distribution. This is a quantile coordinate change, not a replacement of the algorithm's original equidistant digit buckets. A digit prefix is the same algorithmic bucket and is represented by its probability interval in the new coordinates.

All singleton string probabilities are zero since the probability of every depth-d prefix is at most `q^(d-1)/2`. Thus independent strings are distinct almost surely, every sample avoids the countable probability-cylinder endpoints almost surely, and the k-th string equals `h(U_(k))` almost surely. The infinite words ending in all zeros and all ones encode adjacent interval endpoints but are null sample outcomes.

If two strings share a nonempty prefix `w`, their profile sums through that prefix agree. Each remaining profile tail lies between zero and `pi(w) sum_{l>=1} q^l=3pi(w)`, giving `|m(s)-m(s')|<=3pi(w)`.

## A uniform cost error that applies to the random selected string

Let `D_n` be the supremum discrepancy of the empirical uniform distribution function. A grid with spacing `n^-2` has `n^2+1` points. Hoeffding's two-tail bound at `epsilon=sqrt(2log(n)/n)` is `2n^-4`; therefore `P(D_n>epsilon+n^-2)<=4n^-2`. The constant follows from `(n^2+1)*2n^-4<=4n^-2` for `n>=1`.

Take `H_n=ceil(5log(n)/log(4/3))+1`. For any pair, the probability of sharing depth H is `sum_{|w|=H} pi(w)^2`, at most `max_w pi(w)<=q^(H-1)/2`. A pair union bound gives at most `n^2q^(H-1)/4<=1/(4n^3)`.

Outside that pair event all counts at depth H, and hence at greater depths, are at most one. The actual cost therefore has no contribution there. For depths less than H, the probability interval representation gives `|count-npi|<=2nD_n` uniformly over every prefix. Replacing a count by `count*1_{count>1}` changes it by at most one. The discarded profile tail is at most `2q^(H-1)`. Consequently on a measurable event of probability at least `1-4n^-2-1/(4n^3)`, every infinite string s satisfies

`|Z_n(s)-nm(s)| <= 2nH_n(sqrt(2log(n)/n)+n^-2)+H_n+2n^-4 =: R_n`.

This is a simultaneous deterministic consequence of two measurable events. It can therefore be substituted at the data-dependent string `h(U_(k))`; no unjustified fixed-string-to-random-string transfer is made. Its order is `sqrt(n)(log(n))^(3/2)`.

The stopping cost has finite expectation for every n: the same pair-prefix tail bounds the maximum depth at which any sample bucket has multiplicity greater than one, and the total cost is at most n times that depth plus one. Therefore the candidate's inclusion of expectation centering is meaningful.

## Sparse fixed rank and nearby jumps

Let v have a one exactly at the positions `j^2`, `j>=2`. Write `W_j=v_1...v_{j^2-1}`. Its `j-2` isolated ones cause `2j-4` transitions that change the symbol; among the `j^2-2` total transitions the other `j^2-2j+2` preserve the symbol. Hence

`P_j=pi(W_j)=(1/2)(1/4)^(2j-4)q^(j^2-2j+2)`.

The lower boundary of the cylinder starting `W_j1` equals

`tau_j=sum_{i=2}^j qP_i`.

This follows by summing the left child mass skipped at every one of v. The infinite rank is `t=sum_{i=2}^infinity qP_i=F(v)`. The consecutive mass ratio is `P_{j+1}/P_j=q^(2j-1)/16<1/16`, so the series is effective and converges. The exact checks give an enclosure near `t=0.2165825105484832`, strictly inside `(0,1/2)`.

For every fixed prefix of v, its infinite suffix contains both symbols infinitely often. There is positive mass strictly below and strictly above that suffix within the prefix cylinder. Thus t is strictly inside each of its prefix cylinders. It is not any cylinder endpoint; `h` is continuous at t in the prefix topology and the profile estimate above makes `m o h` continuous there.

The two adjacent endpoint strings are `a_j=W_j0 111...` and `b_j=W_j1 000...`. Set `C_j=sum_{d=0}^{j^2-1} pi(v^(d))`. Beyond that common prefix, geometric summation gives

`m(a_j)=C_j+(3/2)P_j` and `m(b_j)=C_j+(1/2)P_j`.

Their profile gap is exactly `P_j`. The first term after `W_j` is included once, so there is no depth-zero or terminal singleton convention error in these formulas.

Between the one at position `j^2` and the next one there are `2j` zeros. The probability cylinder `W_j1 0^(2j)` has lower endpoint `tau_j` and length `P_j q^(2j)/12`, whence

`0<t-tau_j<P_jq^(2j)/12`.

Let `w_j=P_jq^j`, `K_j=floor(j/2)`, and `n_j=ceil(w_j^-2)`. The adjacent cylinders `W_j0 1^(K_j)` and `W_j1 0^(K_j)` have respective lengths `P_jq^(K_j)/4` and `P_jq^(K_j)/12`. Their length-to-window ratios tend to infinity. For all sufficiently large j, the left and right rank windows of width w_j lie in those cylinders and their profiles are within `P_jq^(K_j)` of the respective endpoint values.

These scales satisfy

`sqrt(n_j)w_j -> 1`, `sqrt(n_j)P_j >= q^-j -> infinity`, and `log(n_j)=O(j^2)`.

Consequently `R_(n_j)/(n_jP_j)=O(j^3q^j)+o(1)->0`, and `(t-tau_j)/w_j<=q^j/12->0`. These are proved limits, not extrapolations from the finite diagnostic table. The crude error bound is quite large at j=20 or 40 but already small at j=80; slow entry into the asymptotic regime is not a failure of the theorem.

## Positive-probability separated cost bands

For `k_n=floor(nt)+1`, `sqrt(n)(U_(k_n)-t)` converges in distribution to `N(0,t(1-t))`. To verify the rounding and triangular CLT directly, write `P(U_(k_n)<=t+z/sqrt(n))=P(Bin(n,t+z/sqrt(n))>=k_n)`. The parameters stay uniformly inside `(0,1)` and the bounded Bernoulli summands satisfy Lindeberg's condition. The threshold after standardization tends to `-z/sqrt(t(1-t))`; the one-unit rounding error tends to zero. Normal continuity then yields the assertion.

Because t is much closer to `tau_j` than to either end of the width-w_j windows, each of the events placing `U_(k_(n_j))` in the left or right window has probability tending to

`rho=Phi(1/sqrt(t(1-t)))-1/2 > 0`.

In fact `rho>=Phi(2)-1/2`. Intersecting with the good cost event loses only a probability tending to zero; independence between these events is not needed.

For large j, each of the deterministic cost intervals centered at `n_jm(a_j)` and `n_jm(b_j)`, with radius `n_jP_j/8`, has probability at least `rho-o(1)`. Their distance is `3n_jP_j/4`. For any fixed M, an interval of length `2M sqrt(n_j)` eventually intersects at most one cost interval. Uniformly over every real a,

`limsup_j sup_a P(|Y_(n_j)(floor(n_jt)+1)-a|<=M sqrt(n_j))<=1-rho`.

For any deterministic centering sequence this gives a positive tail probability for every fixed M along a subsequence, which is exactly the failure of tightness required. It excludes convergence to any real-valued probability law.

## Falsification attempts and remaining limitations

1. Boundary substitution: fails as an objection, since t lies inside every finite prefix cylinder and has infinitely many zeros and ones.
2. Moving-rank substitution: fails, since only the nearby boundaries and sample-size subsequence change; t is one fixed real number for all n.
3. Algorithm mismatch: fails, since the digit cylinders and singleton-stopping count agree with the source equations.
4. Selected-string dependence: fails, because the cost estimate is simultaneous, not merely pointwise.
5. Random centering contradiction: fails, because the two-band argument only treats deterministic centers. The empirical profile center may move between the bands.
6. Constant, exponent, or endpoint bookkeeping: exact fraction checks reproduce the prefix probabilities, rank boundaries, jump gap, long-zero cylinder, adjacent-cylinder lengths, and ceil(n) inequalities for `2<=j<=30`.
7. Asymptotic claim from finite computation: avoided. The CLT and all limiting rates are analytical arguments above.

The mathematical target passes. The result does not classify other fixed ranks, prove any statement for almost every rank, or establish historical priority. The original OWR wording does not itself specify a quantifier over ranks or a Markov centering function; its displayed center is deterministic, and the later primary manuscripts specify `n(m o h)(t)`. The theorem disproves the universal deterministic fixed-rank interpretation, including an interpretation restricted to nonboundary continuity ranks. No stronger interpretation should be promoted.
