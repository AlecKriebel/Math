# Attempt 2: a corrected flip and the missing Morita coherence

## Proposed mechanism

A nilpotent-block equivalence might transport the duality and the symmetry type of invariant forms from the local pair. The following calculation identifies exactly what must be transported. It was derived independently of the local projective-indicator approach; it does not construct the required equivalence for general blocks.

## Tensor lemma

Let D be any finite group normal of index two in E. Choose t in E outside D and put

    alpha(d)=t d t^(-1),    z=t^2.

Then alpha^2=Ad(z) and alpha(z)=z. For an irreducible complex representation rho on V, with character lambda, define on V tensor V

    pi(d)=rho(d) tensor rho(alpha(d)),
    P=(1/|D|) sum_d pi(d),
    S(v tensor w)=w tensor v,
    R=(I tensor rho(z)) S.

Here P projects onto W=(V tensor V)^D for the action pi. Direct multiplication gives

    R pi(d)=pi(alpha(d)) R,
    R^2=rho(z) tensor rho(z)=pi(z).

The first relation shows that R commutes with P. The second shows that R^2 is the identity on W. Furthermore

    dim W = dim Hom_D(V*, V composed with alpha)

is zero or one by Schur's lemma. It is one precisely when lambda composed with alpha is the complex conjugate of lambda.

The matrix identity Tr((A tensor B)S)=Tr(AB) now gives

    Tr(R|W) = Tr(PR)
      = (1/|D|) sum_d Tr(rho(d) rho(alpha(d)) rho(z))
      = (1/|D|) sum_d lambda(d alpha(d) z)
      = (1/|D|) sum_d lambda((dt)^2)
      = g(lambda).

Consequently g(lambda) belongs to {-1,0,+1}; it is nonzero exactly for the twisted-real characters. Crucially, the twisted-real condition gives only dim W. The sign of the corrected flip on this line contains additional information.

## Bilinear-form formulation

Put tau(d)=alpha(d)^(-1), an anti-automorphism. Then tau^2=Ad(z) and tau(z)=z^(-1). Define the contravariant duality V^dagger on the vector-space dual by

    (d f)(v)=f(rho(tau(d))v).

Under vector-space biduality the natural map j_V:V -> V^(dagger dagger) is v -> rho(z)v. A morphism f:V -> V^dagger corresponds to a bilinear form B(v,w)=f(v)(w) satisfying

    B(rho(d)v, rho(alpha(d))w)=B(v,w).

Its adjoint is

    T(B)(v,w)=B(w,rho(z)v).

Since alpha(z)=z, invariance gives T^2(B)(v,w)=B(rho(z)v,rho(z)w)=B(v,w). This form space is the dual of W, and T is the transpose of R. Its trace is therefore g(lambda).

## Exact sufficient condition on an equivalence

Suppose F is a complex-linear equivalence from Rep(D) to the ordinary representation category of a real block B, taking degree-2^h simple objects to height-h characters. Let * be ordinary contragredient duality on the block and j its ordinary biduality map. A natural isomorphism

    a_V : F(V^dagger) -> (FV)*

must also satisfy the positive coherence relation

    a_(V^dagger) F(j_V) = a_V* j_(FV).                    (C)

If it does, the character bijection induced by F has the desired indicator property. Indeed f -> a_V F(f) gives an isomorphism between local and block form spaces. Naturality and (C) imply

    a_V F(f^dagger j_V) = (a_V F(f))* j_(FV),

so their adjoint involutions are intertwined. Their traces are respectively g(lambda) and the ordinary Frobenius–Schur indicator of FV. This proves the conditional claim.

An ordinary Morita equivalence alone supplies no proof of (C). Even a correspondence commuting with the permutation of simple objects under duality supplies only the zero/nonzero pattern. A negative coherence on a fixed simple reverses its form sign. Rescaling a natural isomorphism cannot turn negative coherence into positive coherence on that simple: duality here is complex-linear on morphisms, so both sides scale by the same scalar.

## Concrete sign obstruction

If alpha is the identity, z is central and

    g(lambda)=omega_lambda(z) epsilon_D(lambda),

where rho(z)=omega_lambda(z) I. This follows directly by moving the scalar rho(z) out of the trace in the tensor lemma.

For D=Q8, its four linear characters kill -1, while its degree-two character takes -1 to -I and has ordinary indicator -1. Thus t^2=1 and t^2=-1 give the same twisted duality permutation but opposite corrected-flip signs on the degree-two character. All linear indicators stay positive. These are two different extensions of D, not two blocks violating the same-pair conjecture.

The elementary algebra analogue is M_2(C) with transpose versus symplectic transpose. Its unique simple object is fixed by either duality, while its invariant form is symmetric in one case and alternating in the other. The ordinary algebra and the permutation of simples alone cannot distinguish that information.

## Remaining gap

Constructing F with the specified weak duality (tau,z), its positive coherence, and the height compatibility would settle the target. No construction for arbitrary nilpotent blocks has been obtained. At the semisimple category level, requiring (C) already encodes the desired indicator signs; it cannot be assumed merely because the ordinary block is Morita equivalent to a group algebra.

**Outcome:** complete tensor/form calculation and a precise conditional equivalence criterion. The block-theoretic existence step remains open in this attempt. These local calculations are not claimed novel.

Context: [Sambale, Real characters in nilpotent blocks](https://arxiv.org/abs/2301.13440), Theorem A and Conjecture B distinguish twisted realness from indicator signs.
