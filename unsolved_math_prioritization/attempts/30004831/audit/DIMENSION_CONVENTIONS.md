# Why the dimension conventions agree here

This supplement expands standard homological algebra used by the frozen proof. It does not claim a new theorem or a new research attempt.

Let A be a Hopf algebra over a field, with trivial left module k. A projective resolution P of k can be tensored over the field with any left A-module M, giving a resolution of M with diagonal action. If P is free, diagonal A tensor M is free: the linear isomorphism from the ordinary free action to diagonal action is

F(a tensor m) = sum a_(1) tensor a_(2)m,

with inverse sum a_(1) tensor S(a_(2))m. Direct summands give the same claim for projective P. Therefore every M has projective dimension at most pd_A(k), and the reverse inequality is automatic. This proves left global dimension equals pd_A(k), including the infinite case.

The same resolution P tensor A carries the bimodule structure

b (p tensor a) c = sum b_(1)p tensor b_(2)ac.

For P=A the same F is an isomorphism from the ordinary free bimodule A tensor A to this bimodule. Direct sums and summands show that projective P yields projective bimodules. The augmentation gives the regular bimodule A, hence pd_(A^e)(A) is at most pd_A(k).

Conversely a projective bimodule resolution of A splits degree by degree as a sequence of right A-modules: its terms are projective on the right, and the terminal module A is projective on the right. Tensoring that split resolution on the right with k remains exact and gives projective left A-modules. Thus pd_A(k) is at most pd_(A^e)(A). These inequalities prove Hochschild dimension equals pd_A(k), hence equals left global dimension. For the algebras in this packet, the bijective antipode identifies the opposite algebra with the original and also gives the right-hand equalities.

Equivalently, projective dimension is detected by Ext^n_A(k,M) while allowing M to vary. It is **not** generally the supremum of the n for which Ext^n_A(k,k) is nonzero.

The present H is already an illustration. Every extension of its trivial module by itself has generator matrices

g = [[1,a],[0,1]], x = [[0,b],[0,0]].

The skew relation gives 2b=0, while x^2=1-g^2 gives 2a=0. Over C both vanish, so Ext^1_H(k,k)=0. Higher self-Ext also vanishes because global dimension is one. Nevertheless the trivial module is not projective: take

g = [[-1,0],[0,1]], x = [[0,1],[0,0]].

These matrices satisfy the defining relations. The span of the first basis vector is the sign module, and the quotient is trivial. A candidate lift of the quotient generator has the form e_2+c e_1; x sends every such lift to e_1, so no trivial submodule splits the extension. Thus Ext^1_H(k,k_sign) is nonzero and pd_H(k)=1.

For L, the frozen proof uses Ext over the embedded dual numbers, then restriction of projectives, to prove pd_L(k)=infinity. It never asserts that a comodule tensor equivalence is an equivalence of algebra-module categories. Nor does it replace the requested invariant by injective dimension, Gorenstein global dimension, or Gerstenhaber-Schack dimension.

The equality of conventions is also explicitly stated in [Bichon 2022, introduction](https://www.numdam.org/articles/10.5802/crmath.329/) and [Bichon 2026, before Theorem 3.2](https://arxiv.org/abs/2602.12731v1).
