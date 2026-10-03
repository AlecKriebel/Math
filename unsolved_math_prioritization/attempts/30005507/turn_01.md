# Attempt 1: induce from the universal solvable model

## Proposed mechanism

Replace an arbitrary block with a canonical block built from its defect pair, calculate every indicator there by induction, and try to transfer the calculation back. The first step works for every index-two pair; the transfer is the unresolved part. The model is already present in Sambale's paper after Definition 7. The following gives the indicator calculation explicitly, with no novelty claim.

Let D be a finite 2-group, D normal in E with [E:D]=2, and Q=C3. Let E act on Q through E/D by inversion. Put G=Q semidirect E and H=Q times D. Choose a nontrivial linear character theta of Q and t in E outside D. The inertia group of theta is exactly H.

For lambda in Irr(D), define

    psi_lambda = Ind_H^G(theta tensor lambda).

## Character and height calculation

The two conjugates of theta tensor lambda have restrictions theta and its complex conjugate on Q, hence are distinct. The index-two Clifford criterion shows that psi_lambda is irreducible. Every irreducible character over the orbit {theta, conjugate(theta)} is obtained uniquely this way, with degree 2 lambda(1).

The block facts for this model are standard and are recorded in Sambale, after Definition 7: G has a unique nonprincipal 2-block B_model; it is real and nilpotent and has defect pair (D,E). Its irreducible characters are precisely the psi_lambda. This can also be seen by starting with the single block theta tensor OD of H and applying the block form of Clifford correspondence. The characteristic-two algebra of the 2-group D has one block. The pair comes from a nonidentity element q of Q: C_G(q)=Q times D and C_G(q)^*=G.

Since |G|_2=2|D| and the defect is |D|, the equation

    psi_lambda(1)_2 = 2 lambda(1)

makes the height of psi_lambda exactly log_2(lambda(1)).

## Indicator calculation

Identify an element of G with (a,e), a in Q and e in E. When e lies in D, (a,e)^2=(a^2,e^2). The induced character on H is the sum of theta tensor lambda and its t-conjugate. Summing either theta(a^2) or its conjugate over a in Q gives zero, because squaring permutes Q and theta is nontrivial. Consequently elements of H contribute zero to the Frobenius–Schur sum.

When e lies outside D, it inverts Q, so (a,e)^2=(1,e^2), independently of a. Thus

    psi_lambda((a,e)^2) = lambda(e^2) + lambda(t^(-1)e^2t).

Conjugation by t permutes E outside D. Summing the second term over e therefore gives the same sum as the first. There are three choices of a, and |G|=6|D|. It follows exactly that

    epsilon_G(psi_lambda)
      = (1/|D|) sum_{e in E outside D} lambda(e^2).

This proves the full desired formula for B_model for every pair (D,E), including D=1. In the boundary case D=1 the model is S3 and its nonprincipal defect-zero character has indicator +1.

## Attempt to transfer to arbitrary B

The model establishes that every local signed pattern is realizable. It does not establish that every real nilpotent block with the same pair has that pattern. An ordinary nilpotent-block character bijection gives degrees, and a Morita equivalence forgets the symmetry type of invariant forms unless additional duality data are controlled.

For a concrete warning, take D=C4 and E=D8 with the rotation subgroup embedded as D. All outside elements square to 1, so all four model characters have indicator +1. The model G is D24. The four characters of D itself have indicators +1,+1,0,0. Both blocks are nilpotent with defect C4, but ordinary nilpotent-block equivalence does not identify these real-character patterns. Their extended defect pairs differ; this is a warning about forgetting E, not a counterexample to the conjecture.

Sambale's Theorem E carries out a much deeper induction for solvable groups. Extending that induction to arbitrary groups requires an additional structural theorem; it is not supplied by the model construction.

**Outcome:** complete calculation for an existing solvable family; no transfer theorem and no resolution for arbitrary B.

Source: [Sambale, Real characters in nilpotent blocks](https://arxiv.org/abs/2301.13440), Definition 7 and following paragraph, Theorem E.
