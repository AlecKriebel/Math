# An ambient-module limitation and an intrinsic alternative

This is an audit refinement of Approach 3, not another approach to KP-4.98. The frozen author's abstract formula and sufficient quotient criterion are correct. Nothing here realizes the required positive monodromies or fixes their smooth total spaces.

## 1. The full closed-surface Johnson module has no proper nonzero saturated invariant submodule

Let g >= 3, Gamma = Mod(Sigma_g), and L = (wedge^3 H)/H, with H = H_1(Sigma_g; Z). The action factors through the surjective symplectic representation to Sp(2g,Z). The module L is free abelian, and L tensor Q is irreducible. For the latter statement, see Broaddus, Farb and Putman, *Irreducible Sp-representations and subgroup distortion in the mapping class group*, arXiv:0707.2262v2, Section 3, PDF page 10, together with their definition of irreducibility in Proposition 2.6 and Theorem 2.8: https://www.math.uchicago.edu/~farb/papers/distortion.pdf .

Suppose C is a nonzero Gamma-invariant subgroup of L. Irreducibility implies C tensor Q = L tensor Q, so C has finite index in L. If C is also saturated, L/C is torsion-free. Being both finite and torsion-free, it is zero. Thus C = L.

Consequently, in this particular full ambient group and target, a saturated invariant quotient killing a nonzero Lambda_0 necessarily kills all of L. The author's condition that the image of M remain nonzero cannot then hold. An effective application of that exact quotient criterion requires Lambda_0 = 0. The report's warning that the invariant saturation can consume the target is correct; here it is inevitable for nonzero Lambda_0. The author's reducible semidirect-product example remains valid, but does not remove this obstruction for the closed Johnson module.

This conclusion neither rules out other lattice invariants nor identifies the monodromy groups when the criterion fails. Replacing Gamma by a smaller group would require an independent reason all possible equivalence conjugators lie in it.

## 2. An intrinsic saturation index can retain nonzero Lambda_0

Retain all the hypotheses and notation of the author's exact identity

    Lambda_n = Lambda_0 + nM.

Assume that Lambda_0 is saturated in L, and that

    s = rank(Lambda_0 + M) - rank(Lambda_0) > 0.

Then all G_n, n >= 0, are pairwise nonconjugate in Gamma. No invariance of Lambda_0 under Gamma is needed.

Proof. For any subgroup A of a finite-rank free abelian group L, its saturation is

    Sat_L(A) = (A tensor Q) intersect L.

The integer j(A) = [Sat_L(A):A] is finite, and is invariant under every automorphism of L, including all actions induced by Gamma-conjugacy. For n > 0 the rational span of Lambda_n is independent of n, so

    Sat_L(Lambda_n) = S := Sat_L(Lambda_0 + M).

Since Lambda_0 is saturated in L, it is also saturated in S. Therefore S/Lambda_0 is a free abelian group of rank s. Let Mbar be the image of M there. It is a full-rank lattice. Taking indices gives

    j(Lambda_n)
      = [S/Lambda_0 : n Mbar]
      = n^s [S/Lambda_0 : Mbar]
      = n^s j(Lambda_1).

These positive integers strictly increase with n. At n=0, rank(Lambda_0) is smaller, so rank alone separates G_0 from all the other groups. If two G_n were Gamma-conjugate, normality of N and equivariance of tau would identify their kernel-image lattices by an automorphism of L, preserving both rank and j. This is impossible. QED.

This avoids the fixed-quotient difficulty: the quotient S/Lambda_0 is used to compute j, not asserted to carry the action of an arbitrary ambient conjugator. The final invariant is defined intrinsically on each image lattice in L.

Example: in the author's reflection example, Lambda_0 = Z e_2 is saturated, M = 2Z e_1, and j(Lambda_n)=2n for n>0. More generally, the argument applies inside the irreducible Johnson target if a geometric construction supplies the stated saturation and rank-increase hypotheses.

The saturation hypothesis is substantive for this simple all-n formula. With Lambda_0=2Z e_1 and M=Z e_1+Z e_2, one gets j(Lambda_n)=n gcd(2,n), rather than n j(Lambda_1). The independent checker tests the stated theorem through exact determinantal divisors and detects this omitted-hypothesis error.

## 3. Remaining geometric obligations

Both the original and strengthened criteria still need compatible positive boundary-multitwist factorizations, centralization in the appropriate boundary mapping class group, nonempty pencil base sets, diffeomorphisms after blowdown to the same original X, and the required symplectic-form compatibility. No such construction on every X is supplied. The universal problem remains unsolved here.
