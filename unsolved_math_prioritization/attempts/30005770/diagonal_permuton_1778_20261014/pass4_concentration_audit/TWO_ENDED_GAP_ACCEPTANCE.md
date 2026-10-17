# Independent acceptance of two-ended local gaps and their all-window obstruction

Shared PASS4, 14 October 2026.

## Verdict and exact versions

**Accepted:**

- `pass4_window_gaps/TWO_ENDED_WINDOW_GAPS.md`, 9099 bytes, SHA-256 `45ff7bb650efb0d579cd9a8cb9c7093b78c4cf2224aef2c18e369a2af0245286`.
- `pass4_adaptive_profiles/TWO_ENDED_CERTIFICATE_OBSTRUCTION.md`, 4686 bytes, SHA-256 `94f85ecc86ea8d2e43b2009751be442c0a1a986677d82c5a7c0425566b89229f`.

The outgoing-cut count, exact bidirectional minimax, finite coefficient bound and mountain comparison are valid. This strengthens the available local certificate while retaining its summability and its limited relationship to the true gap.

## 1. Outgoing-cut reconstruction

Cutting the marked nonterminal state's outgoing edge and rotating puts that unchanged marked state last. The old terminal state is inflated once and connected to the old first state by the already accepted bridge. When the cut immediately preceded the old terminal state, no incoming lift survives; the proof explicitly handles this case.

A bridge index determines the original state order, marked position, inflation location and all retained edges. The sole missing edge is counted by binom(p+q,p). Thus the bound (n+1)binom(p+q,p)Last_(n+1)(q) is correct. The new terminal tail includes its factor two from the parity-dependent symmetry. No reversal of the canonical chain or uniform conditional cell law is assumed.

## 2. Exact two-ended minimax

If the maximum local penalty is d, the left recurrence bounds x_j<=d y_j and the right recurrence bounds x_j<=d y_(K+1-j). The maximum is positive because the first positive coordinate has zero predecessor. Summing the smaller of the two bounds proves the lower bound for the minimax.

The candidate v_j=min(y_j,y_(K+1-j)) attains it. The y sequence is strictly increasing. At every index, a neighbor toward a nearest endpoint is y_(s-1), where s=min(j,K+1-j), and the other neighbor is at least that large. Entropy is increasing in either variable, so the larger local penalty is exactly the recurrence value one. Odd and even central cases, and K=1, all satisfy this argument. Normalization and homogeneity give the claimed reciprocal sum.

The even/odd formulas follow directly. A fixed vector's zero-padding preserves its score, so enlarging the dimension cannot increase the minimax. This does not confuse fixed-vector padding with positivity of the optimizing profile.

## 3. Counts and K dependence

For each profile, choose its maximizing state and direction deterministically. First or last states use their direct endpoint tails; interior states use the appropriate exact cut count. A zero coordinate cannot be selected because the maximum is positive. The terminal factor two supplies a valid common prefactor, and no separate factor for a choice already determined by the profile is needed.

Summing at most(n+1)^K profiles gives the displayed all-size inequality. Taking n to infinity at fixed K, then eta up to gamma by the finite recurrence's continuity, proves the true-gap lower certificate. The recurrence estimates make y_j comparable to R^(j-1), so the two-ended minimax has order R^(-K/2). Its sum over K is finite. The all-size inequality does not justify discarding the profile factor or the growth defect when K varies with n.

Summability of this lower certificate is not summability of the true gap. It only fails to meet the independently proved divergence-based sufficient condition.

## 4. The mountain comparison is exact

The symmetric ratio-two finite test vector has total weight T_(2h)=2(2^h-1) or T_(2h+1)=3*2^h-2. Endpoint outward penalties equal eta/T_K; every nonendpoint penalty is negative because its smaller neighbor has half its mass and H(1/2)>eta. K=1 and K=2 are correctly separated. Thus the test vector supplies the stated upper envelope for the certificate.

For a center-containing ratio-half window of length K, the exact entropy ratio is Hs/(3-s), with s=2^(-l)+2^(-r) and l+r=K-1. Balancing l and r minimizes s, and the ratio is increasing in s. The two parity minima are exactly2H/T_K. Since2H>eta, every such window has negative score against the certificate.

The companion profile note also covers every one-sided window: its inward neighbor has mass twice the inward endpoint, while its total mass is less than twice that endpoint, so E/M>H>gamma>=V_K^pm. This continues to hold at the finite chain's outer boundary. For any fixed cap B, the canonical finite mountains with parameter greater than B reproduce the relevant center-window ratios exactly. Their whole chain has unbounded width and is not covered by this fixed-cap obstruction.

Using a larger cap than the actual width cannot improve the certified score because the minimax decreases under zero-padding. The independently calibrated true one- and two-cell gaps may replace those two certificates without repairing the failure; the relevant singleton/two-cell comparisons were separately audited.

## Scope

Both endpoint estimates and their full local minimax are genuinely used. The deterministic mountain still defeats this specific bounded-window certificate collection. This does not upper-bound every true gap, rule out stronger joint counting, or show positive uniform probability of a non-diagonal profile. The conditional adaptive theorem remains valid and unresolved at its true-gap hypothesis.
