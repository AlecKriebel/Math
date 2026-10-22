# Independent acceptance of terminal marks and the pointwise completion lift

Shared PASS4, 14 October 2026.

## Verdict and final version

**Accepted.** `pass4_two_sided_mark/TERMINAL_MARK_AND_POINTWISE_LIFT.md`, 9576 bytes, SHA-256 `18af51f210a079b795f00a071271ff2e8839ecd2273316cfd188704a94136cac`.

The final version explicitly restricts the elementary product comparisons to u>=1, as requested during review. Without that restriction the inequality u^(cell size)<=u^(total size) would reverse. All intended exponential-mark applications already use u>1; this was a domain clarification, not a repair of the intended theorem.

The terminal tail, pointwise factor comparison, common incoming mark, joint endpoint marks and stated limitation of direct product estimates are valid. They do not establish the arbitrary-cell two-sided exponential mark.

## 1. Parity-dependent terminal symmetry

An even terminal cell is the only cell in the bottom row and consists of the smallest m values. Reverse-complement sends it to a top-value interval. Its induced pattern is rc(S(A))=A inverse, which avoids213.

An odd terminal cell is the only cell in the rightmost column and consists of the last m positions. Inversion sends it to the top m values, again with pattern A inverse. Both symmetries preserve1324 avoidance. The two parity branches are injective separately, so forgetting parity has at most two preimages.

The top interval may extend to a larger first greedy cell. The note uses only the correct inequality at this stage, not a false claim that the whole canonical chain is reversed. The terminal tail is consequently at most twice the first-cell tail with the same size threshold.

## 2. The guard fixes the first state exactly

After the symmetry, the top a values induce A inverse. The three guard entries create a top(a+2)-value pattern P(A)=12 skew-sum A inverse. This avoids213 and is injective in A. The next value is the middle guard point, which creates213 with the two upper guard points. Thus the first state is exactly P(A).

The new extreme guard points cannot participate in1324 because of their position and value ranks. If the middle guard point participates, it must be the first occurrence point; the remaining three would have to be old upper points forming213. The arbitrary old lower region is not assumed to avoid132. This explicitly verifies the extension of the earlier domino guard to a complete permutation.

Removing the first three global positions recovers the symmetric image; the parity bit then recovers the original permutation. The at-most-two fibre bound therefore applies for each fixed terminal state A and total size n.

## 3. Coefficient shift and incoming exponential mark

The source last-state series is z^|A| ell_A. The guard adds three points, while P(A) has size |A|+2. Therefore the coefficientwise inequality is exactly

    z ell_A(z)<=2 h_(P(A))(z),

not an inequality with the shift omitted. Dividing by z is legitimate at every real0<z<rho.

Multiplying by u^|A|z^|A| and summing over A introduces the factor2/(u^2 z^3). The image states P(A) are distinct, so their marked outgoing sum is bounded by the full outgoing sum. This proves the common incoming marking range1<u<C(rho) for every z<rho. It retains the inverse-pattern padding and does not compare ell_A with h_A at the same state.

## 4. Joint endpoint marks

The absolute first- and last-size moment bounds both hold with a fixed parameter exp(t)<exp(gamma). For log u+log v=t<gamma, finite-class Hölder with exponent theta=log u/t gives the claimed joint moment bound. The powers of lambda^n combine to lambda^n, not lambda^(2n). Endpoint cases with one parameter equal to one reduce to the corresponding one-sided bound; both equal to one reduce to a_n<=lambda^n.

This marks two endpoints of the same path. It does not mark an arbitrary state with both its independent prefix and suffix completion factors.

## 5. The direct product region is genuinely weaker

For z<r<rho and1<v<C(rho), the two sequences f_A=(vr)^|A|h_A(r) and g_A=(vr)^|A|ell_A(r) are summable. Nonnegative coefficients imply coordinate monotonicity from z to r. If uz<=(vr)^2, the desired product sum is bounded by sum_A f_A g_A, which is finite because both sequences are nonnegative and summable.

Independent radii and marks do not increase the supremum of the resulting size factor beyond rho^2 C(rho)^2. The Catalan equation gives this value as rho(C(rho)-1). For actual1324, lambda>4 and C(rho)<2, so this is strictly smaller than rho. At lambda=4 it would only equal rho. Thus the argument supplies no improvement over the elementary region uz<rho, let alone a fixed u>1 for every z<rho.

The termwise bound reducing the unresolved sum to h_A h_(P(A)) is also correct. No estimate for that paired outgoing product is established. Separate first and last exponential marks cannot simply be multiplied into a larger radius.

## Scope

The note supplies new exact incoming information without replacing the uniform finite-class law. It preserves the necessary two-sided completion factors and explicitly identifies the remaining radius mismatch. No weak-limit theorem follows from these statements alone.
