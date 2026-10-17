# Independent acceptance of adjoining-minimum concentration transfer

Shared PASS 2,14 October2026. Reviewed artifact: `pass2_protected_tail_extension/MERGE_TRANSFER_THEOREM.md`,12243 bytes, SHA-256 `d8a88fb75f5f2c78509e0610420cb8701d5445de0ae1be856d2c0e0b9d919d34`.

## Verdict and exact scope

**Accepted without a requested mathematical correction.** For a fixed pattern q of length at least two that starts with1, exponential fixed-deviation anti-diagonal concentration transfers from uniform Av_n(q) to exact uniform Av_n(1 direct-sum q).

With the accepted PASS1 seed, this proves the fixed families `I_d direct-sum231`, d>=1, and after exact symmetries the target cases

`alpha=132 skew-sum J_(d-1)` and `alpha=213 skew-sum J_(d-1)`.

The d=1 instances are the seed. The theorem also proves the conditional closure under appending another minimum to any target pattern already satisfying exponential diagonal concentration. It does not establish an arbitrary seed, the alpha312 case, growing d, or the universal conjecture. No novelty claim is certified.

## 1. Prior growth theorem: verified with its hypothesis

The exact credited input is Bóna's arXiv:math/0403502v2, Theorem5.4 via Lemma5.3, printed page7: the inner pattern must start with1. The recovered primary PDF is independently pinned in `SOURCE_AND_ENCODING_SCOPE.md`. Its Theorem5.2 explicitly gives the family growth `(d-1+sqrt8)^2`.

The draft does not extend that equality to231 or213. The starts-with1 assumption also makes q skew-indecomposable, so Av(q) is skew-closed. Supermultiplicativity and the existing growth limit rigorously imply `a_k<=lambda^k` for every k, including k=0. The denominator bound `b_n>=Lambda^n exp(-gamma n)` follows directly from its nth-root limit. No unproved coefficient ratio, exact asymptotic, or polynomial valid-encoding fraction is needed.

## 2. Canonical law versus ambient law: verified

Deleting all left-to-right minima gives a q-avoiding remainder exactly when the original avoids1 direct-sum q. The proof correctly uses the first/minimum entry of a q occurrence. The positions, values and standardized remainder reconstruct the original permutation uniquely.

The author then deliberately enlarges to all subset/remainder triples. These triples are not asserted to be uniformly distributed under the actual avoider law. Independent uniform position/value subsets are used only within the ambient count at fixed remainder size. Each bad actual permutation contributes one canonical bad triple, which is enough for an upper bound. Division by the full actual class count, using matching exponential growth, completes the exact-law transfer.

This is a valid counting argument even if compatibility conditioning has severe subexponential bias. The source's protected-tail sampler, finite table and heatmap are not used as a substitute for a limit theorem.

## 3. Deterministic transport estimate: verified, including endpoints

I independently derived the same center-cost bound. If core positions and values have prefix count discrepancies E(P),E(V), then each coordinate comparison has rank error at most E/k plus the stated center correction. Weighting the k core points by1/n gives the core contribution

`(k/n)ell_k + (E(P)+E(V))/n + (1-k/n)/n`.

The complementary decreasing sequence contributes the same discrepancy term and `(1-(n-k)/n)/n`. Their sum is exactly the bound in equation(9), including the1/n remainder. Prefix discrepancy is unchanged by complementation.

The k=0 merge is decreasing and k=n is the unchanged core, so no division-by-zero endpoint is used. The difference between the square-spread cost D and center cost ell is at most1/n. The explicit coupling gives d_BL<=D, while the bounded1-Lipschitz function `|x+y-1|/sqrt2` gives D<=sqrt2*d_BL. Consequently exponential fixed-positive-deviation concentration is equivalent for these costs, as claimed.

## 4. Hypergeometric and bad-count steps: verified

For k samples without replacement from a population of n with j ones, the Doob increment for the final count is indeed

`(n-k)/(n-r) * (Y_r-p_(r-1))`.

When0<k<n and1<=r<=k its absolute value is at most1. Azuma's two-sided bound with denominator2k implies the displayed weaker denominator2n. The deterministic k=0,n cases are handled separately. Union over prefix positions and both subsets gives the claimed4(n+1) prefactor. The argument never imposes independent actual minima.

For delta=epsilon/16 and n>=4/epsilon, a bad full merge on a good allocation forces `(k/n)ell_k>epsilon/2`. Since ell_k<=1, it forces both k>epsilon*n/2 and a fixed-positive core deviation. This checks small-component and boundary proportions without needing a separate limit law for the number of minima.

The conditional bad-core probability is bounded by C exp(-c*k), with finitely many small k absorbed into C. On the relevant sizes this is at most C exp(-c*epsilon*n/2). Multiplying by ambient counts, summing, applying `T_n<=Lambda^n`, and using the denominator lower bound with gamma=r/2 yields the claimed exponential decay. The final polynomial absorption is legitimate.

## 5. Symmetry and fixed-parameter scope: verified

Reversal gives `reverse(I_d direct-sum231)=132 skew-sum J_d`. Inversion followed by reversal gives `213 skew-sum J_d`. These maps preserve exact uniform finite-class laws and induce the stated square isometries, so their geometric effect is justified, not inferred from Wilf equivalence.

For the general target closure, reversing a pattern ending in1 produces a pattern starting in1. Reversing its added initial minimum produces one more final minimum. The length-at-least-two hypothesis holds throughout the target setting. Repeated use is only for fixed finite iteration counts, and all rates may depend on those counts.

## Independent finite checks

`check_merge_encoding.py` reconstructs every canonical triple for all permutations through n=7, and checks the exact deletion equivalence for q1342 andq12453. It also checks all15125 ambient merge triples through n=6 using exact integer arithmetic, including k=0,n, and verifies the center-cost inequality. All checks pass; `MERGE_FINITE_CHECKS.json` records them. These are diagnostic checks only, not the asymptotic proof.

No mathematical edit is required to the pinned proof. The accepted PASS1 files and receipts remain unchanged.
