# Turn 4: transferring tail information through finite-mean finitary codes

This turn proves a coding transfer theorem, including the measurability of the outside-only reconstruction. It gives an entropy-free route for an additional class of processes and identifies a precise integrability obstacle. It does not represent every stationary finite-alphabet process by such a code, nor infer equality of two subfields merely because they lie in a common field.

## 1. Definitions that make the reconstruction valid

Let X be a stationary finite-alphabet process. Let Y=F(X) be a shift-equivariant measurable finite-alphabet factor. Work on a shift-invariant conull set G on which the code is defined. A finite centered input block is decisive if every point of G having that block has the same output at its center. Blocks with no compatible point of G can be ignored. Assume that almost every input has a decisive centered block of some finite radius.

Let R(x) be the least such radius for the coordinate at0, and R_k(x)=R(shift^k x). These are measurable: for each radius there are finitely many input blocks, and decisiveness and its output label can be fixed once for each block. No algorithm for deciding admissibility or computing these labels is asserted. Assume

    E[R]<infinity.                                         (1.1)

**Theorem.** In the common input probability space,

    T_Y^- subset T_X^-,  T_Y^+ subset T_X^+,
    T_Y^bilateral subset T_X^bilateral,                     (1.2)

with completed fields throughout.

The hypothesis refers to an actual cylinder-determined coding radius, not an arbitrary random variable after which a chosen sample path happens to agree. The common conull set is part of the definition.

## 2. A measurable remote-future decoder

Fix m and N>=m. For each k>=N, inspect only the input coordinates at least m. If some decisive centered block around k has radius at most k−m, output its prescribed value. If none does, output a fixed default symbol. The possible blocks in this test all lie in[m,2k−m], a finite observed interval. If more than one decisive block is found, their prescribed values agree on G; on exceptional or inconsistent inputs choose by a fixed ordering. The resulting entire vector Yhat_[N,infinity) is measurable in sigma(X_j:j>=m).

On G, its kth entry agrees with Y_k whenever R_k<=k−m. The probability that the two infinite vectors differ anywhere is consequently at most

    e_(N,m)=sum_(k>=N) P(R>k−m).                           (2.1)

Stationarity is used only to identify the coding-radius distributions, and the union bound requires no independence. For integer-valued nonnegative R, E[R]=sum_(j>=0)P(R>j). Hence e_(N,m)→0 as N→infinity with m fixed.

If A belongs to the completed future tail of Y, then for each N there is a Borel subset B_N of the remote output product with 1_A=1_{B_N}(Y_[N,infinity)) almost surely. Replace that vector by Yhat to obtain an event A_N measurable in sigma(X_j:j>=m). Its symmetric difference with A has probability at most e_(N,m). Passing to an almost-surely convergent subsequence shows A belongs to the completion of this input field. Since m was arbitrary, A lies in the completed right tail of X.

This avoids an unjustified prescription to fill the missing past with arbitrary symbols: such a filling need not be in the support or the conull coding domain. Only decisive blocks compatible with the actual observed input are used.

## 3. Past and bilateral transfer

For the past, inspect centered decisive blocks at k<=−N having radius at most−k−m, so they remain inside the input half-line j<=−m. The same bound(2.1) applies after changing k to−k.

For the bilateral outside field, decode separately at every |k|>=N using radius at most|k|−m. Each block then lies wholly in one of the two input half-lines outside the central interval. The union bound is at most2 e_(N,m), which again tends to0. The identical approximation-of-events argument proves the bilateral inclusion in(1.2).

All intersections here are intersections of completed subfields in the measure algebra. Equivalently one can use representatives: for decreasing fields and representatives agreeing almost surely, the limsup of the representatives is measurable in every earlier field and agrees almost surely with the original event.

## 4. Consequences and limits

If X is iid, each of its three tails is trivial. For the bilateral tail this follows directly from independence of a fixed central cylinder and every sufficiently remote outside field, followed by a monotone-class argument. Therefore a finite-mean finitary factor of iid has all three tails trivial. The same conclusion holds for a finite-mean finitary factor of an aperiodic irreducible finite stationary Markov chain, by Turn1.

If F is an isomorphism modulo null sets and its inverse is also finitary with finite mean coding radius, apply(1.2) in both directions. Corresponding left, right and bilateral tail fields are equal under the identification of the two probability spaces. Thus equality of the two one-sided tails transfers through such an isomorphism.

For a factor of a process with a nontrivial common input tail H, (1.2) alone gives only that the two output tails are subfields of H. Two subfields of H need not coincide. No equality conclusion is inferred from that alone. An arbitrary measurable factor is not covered either.

## 5. Almost-sure finitariness does not imply finite mean radius

For a two-sided iid fair binary input, let L_k be the number of consecutive zeros starting at k before the first1. Define

    Y_k=X_(k+2^(L_k)).

On the conull shift-invariant set where every such run is finite this is a shift-equivariant finitary code. Its least centered decisive radius is R_k=2^(L_k). To see the lower bound, change the bit at k+2^(L_k) while leaving a smaller centered block unchanged. That bit is strictly after the first1, including L_k=0, and does not alter L_k. Both extensions remain in the conull domain and give opposite outputs. Conversely the radius2^(L_k) block contains the first1 and the queried bit, so it determines the output.

Since P(L_k=l)=2^(−l−1),

    E[R_k]=sum_(l>=0) 2^l 2^(−l−1)=infinity.

Thus finitariness alone does not provide the summability needed in(2.1). This example is a limitation of the proof's sufficient condition; no unequal-tail example or failure of the source theorem is asserted. Its future-only dependence in fact makes the right-tail inclusion immediate without an integrability argument.

## 6. Controls and the remaining source gap

verify_turn4.py exhaustively checks decisive-block reconstructions for a truncated version of the variable-radius code, using truth tables rather than an oracle for the unseen symbols. It tests eventwise boundary errors against the union bound and exact tail-sum identities for finite and heavy-tailed radius laws. These finite controls support the decoder algebra; the measure-theoretic theorem is established above.

The missing step remains a representation or direct probability argument for every stationary finite-alphabet process. Neither finite expected coding radius nor an invertible finite-mean code has been established in that generality, and imposing either would discard part of the source's scope.
