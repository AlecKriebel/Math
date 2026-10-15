# Checkable bridge from pre-existing theorems to the negative answer

This is a deduction from prior results, not a claim that a prior author literally
printed this deduction or this rational witness. It uses the frozen target and
the independently retrieved versioned primary bodies identified in SOURCE_MANIFEST.json.

1. Let S have exactly three ends, all accumulated by genus. Choose a compact
connected subsurface K such that the complement has three components U1,U2,U3,
each containing exactly one end. Existence follows from the classification of
orientable surfaces, or by taking the central pair of pants in the standard model
with three one-ended infinite-genus surfaces attached. If h(K) misses K, its
connectedness puts it in one Ui. The other two end regions and K then lie in one
component of the complement of h(K), carrying at least two ends. But h transports
the three one-ended complementary components of K onto those of h(K). This is
impossible. Thus K is nondisplaceable.

2. ARSVW v1, Theorem 1.6, printed/PDF p. 3 (31 October 2023), applies to every
translation structure on an infinite-type surface with such a finite-type
nondisplaceable subsurface and implies finite Isom(M). It makes no flat metric
completeness or tameness assumption. Its p. 15 proof invokes its Corollary 2.21
and Lemma 2.19(2). The corresponding v2 statement is Theorem 1.8, p. 3.

3. Their v1 Section 3.1, p. 12, defines Isom(M) = D^{-1}(SO(2,R)), where D is
the derivative map Aff(M) -> GL+(2,R). Therefore

   D(Isom(M)) = Gamma(M) intersect SO(2,R)

   is finite. This identity follows from the definition of image and inverse
image; it does not require a splitting, a faithful affine action of Gamma, or
trivial kernel. The same definition appears in v2 p. 14. If the source convention
omits finite cone points, use its underlying Riemann surface with those points
omitted; if it includes them, the conformal structure extends across their
integer-angle local models. Infinite-angle completion points need not be added.
The frozen proof supplies the bridge on either convention. Orthogonal derivatives
are holomorphic in the regular charts. Thus incompleteness does not create an
escape from the prior proper-discontinuity mechanism.

4. Put A = (1/5)[[3,-4],[4,3]]. Exact multiplication gives A^t A = I and det A = 1.
Every integral power preserves all Euclidean lengths, so G = <A> is countable
and has no strict contraction. To check infinite order algebraically, let
B = 5A and u_n = tr(B^n). The identity B^2 - 6B + 25I = 0 gives
u_0 = 2, u_1 = 6, u_(n+1) = 6u_n - 25u_(n-1). For n >= 1, u_n = 1 mod 5.
If A^n = I for positive n, u_n = 2*5^n = 0 mod 5, a contradiction. Negative
powers reduce to the positive case by inversion. Hence G is infinite.

5. The finite subset {0,2/3,1} is closed in the middle-thirds Cantor set and is
an admissible nonempty end space in OWR Question 4. Realization of its prescribed
matrix subgroup G would contradict step 3. In fact no eligible Veech group can
even contain A. This disproves the universal question, while neither classifying
all end spaces nor excluding abstract infinite cyclic Veech groups.

Thus the qualitative negative answer is a direct consequence of an explicit
translation-surface theorem available in 2023. This is stronger evidence than
merely finding old ingredients, but weaker historical evidence than locating an
earlier literal negative-answer statement. This audit does not identify the
earliest implicit consequence in the entire literature.

Version caution: v1's ordinal formula at p. 7 does not handle alpha = 0 consistently;
v2 p. 8 explicitly defines a finite d-point space to have characteristic system
(0,d). The bridge above uses the unambiguous nondisplaceable-subsurface theorem
and avoids this historical indexing issue. V2 Theorem 1.10(3), p. 4, supplies a
second check for finite n >= 3 ends.
