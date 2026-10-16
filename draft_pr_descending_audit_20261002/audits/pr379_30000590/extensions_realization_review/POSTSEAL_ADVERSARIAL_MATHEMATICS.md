# Post-seal comparisons and further falsification

Candidate inspection started only after INDEPENDENT_SEAL.json, UTC 2026-10-03T04:04:12.326557Z. This document is explicitly post-seal. No sealed derivation or code was edited.

## 1. The two independently chosen bad matrices agree by an invertible matrix

The candidate uses t=ac^{-1}, u=ba^{-1}, v=dc^{-1}; the independent derivation uses x=ab^{-1}, y=cd^{-1}, z=bd^{-1}. They obey

    x=u^{-1}, y=v^{-1}, z=u t v^{-1},
    t=x z y^{-1}, u=x^{-1}, v=y^{-1}.

These are mutually inverse free-generator transformations, not merely an equality of exponent vectors. Let M_old=(t-1,u-1,v-1), M_new=(x-1,y-1,z-1). Define matrices with group-ring entries

    T = [[0,        0,       v^{-1}],
         [-u^{-1},  0,       t v^{-1}],
         [0,       -v^{-1}, -v^{-1}]],

    U = [[z y^{-1}, -x^{-1}, 0],
         [-y^{-1},   0,      -y^{-1}],
         [y^{-1},    0,       0]].

The suffix augmentation identity (pq-1)=(p-1)q+(q-1) yields M_old T=M_new and M_new U=M_old. Direct multiplication, using the displayed inverse substitutions, gives TU=UT=I universally. For example the (u,t) entry of TU is -u^{-1} z y^{-1}+t v^{-1}y^{-1}=-t+t=0; the diagonal entries are products of inverse units. Thus their kernels are isomorphic right modules. The code `realization_comparison_exact.py` records every matrix entry, both products, and both row-map identities over actual reduced integral F2×F2 words. This is a materially independent match of the two constructions.

## 2. Actual chain maps versus the arbitrary matrix

The same code additionally computes each of the four genuine product-tree 2-cell boundaries in the LEFT free augmentation resolution. In left coordinate notation

    partial_1(q_a,q_b,q_c,q_d)=sum_s q_s(s-1),
    partial_2(e_{s,t})=(s-1)e_t-(t-1)e_s.

Each partial_1 partial_2 residual is exactly zero over the actual group ring. The independent pre-seal code computes the Hom-dual maps on RIGHT modules:

    delta_0(f)_s=(s-1)f,
    delta_1(f)_{s,t}=(s-1)f_t-(t-1)f_s,

and verifies right linearity on nontrivial coefficients. Treating the free chain left coordinates as right coordinates changes the coefficient order and is rejected by a nonzero wrong-sided bad-matrix residual. Forgetting the product differential sign is rejected as well.

A fake 2-cell for the two same-factor generators a,b would have boundary -(b-1)e_a+(a-1)e_b. Its partial_1 is ab-ba, a nonzero element of the actual group ring. An exponent-vector substitution would incorrectly set it to zero. The code retains its complete nonzero residual. Contractibility of the product of trees, not the four zero finite residuals, proves exactness universally. The cohomological vanishing and degree-two finite generation are established by the pre-seal universal flat-cokernel argument.

The arbitrary bad complex has ranks 3 -> 1 and non-finitely-generated H^0. The actual regular complex has ranks 1 -> 4 -> 4 and H^0=H^1=0. There is no degree relabeling or finite extra preceding boundary that realizes the bad matrix as the group's regular cohomology. Candidate Turn 5 explicitly preserves this gap, and its added-boundary observation is correct: if B is finitely generated inside a non-finitely-generated K, then K/B cannot be finitely generated.

## 3. A genuine nonsplit extension control, and an ordinary-coefficient counterfeit

Let G be the integral Heisenberg group, with elements (a,b,c) and multiplication

    (a,b,c)(x,y,z)=(a+x,b+y,c+z+a y).

Let X=(1,0,0), Y=(0,1,0), Z=(0,0,1). Then [X,Y]=Z, Z is central, and

    1 -> <Z> = N = Z -> G -> Q = Z^2 -> 1

is nonsplit. Every lift of a quotient basis generator is XZ^i or YZ^j and their commutator is still Z, so commuting lifts cannot exist. The quotient is a dimension-two integral duality group and the kernel is a dimension-one integral duality group.

For REGULAR coefficients, the kernel's actual left free resolution has cochain differential left multiplication by Z-1. Its H^0 vanishes by finite support, and

    H^1(N;ZG)=ZG/(Z-1)ZG = Z[Z^2]

as left ZQ/right ZG bimodule; the right action factors through Q. The quotient's genuine two-variable Koszul complex has H^p(Q;ZQ)=0 except p=2, where it is Z. Therefore the regular-coefficient Hochschild–Serre sequence has only E_2^{2,1}=Z, and

    H^i(G;ZG)=0 for i != 3, H^3(G;ZG)=Z,

with trivial right G action. This is an actual nonsplit extension computation of the theorem, not an algebraic M=ZG test module substituted for A_q. One can alternatively model G as the oriented compact Heisenberg nilmanifold lattice; the above resolution/quotient computation already establishes the result.

With ORDINARY trivial coefficients Z, the quotient action on H^1(N;Z)=Z is trivial and E_2 has multiple columns. The central extension cocycle is beta((a,b),(x,y))=a y; its alternating value on quotient basis generators is 1, so the transgression sends the kernel's degree-one generator to the nonzero quotient degree-two class, up to orientation sign. The claim that every duality-by-duality extension spectral sequence collapses for arbitrary coefficients would falsely predict rank-three H^1(G;Z). In fact abelianization kills Z=[X,Y] and is Z^2, so H^1(G;Z)=Z^2. This negative control makes the REGULAR coefficient and one-column hypotheses essential. No counterexample to the actual extension theorem appears.

## 4. General bounded Q resolution versus length d

The pre-seal proof was phrased with a resolution of length d. Candidate Turn 4 assumes a finite resolution of possibly larger length b and regular cohomology concentrated in degree d. Its tail-splitting argument is valid: a zero top cohomology gives a surjection C^{b-1}->C^b; C^b is projective, so split off this contractible pair, and repeat down to d. This leaves a finite-projective dual complex ending in d and makes D_Q a finitely generated quotient. The universal coefficient argument uses the original bounded Z-free complex and the same Z-flat D_Q, so the independent result covers the candidate's exact hypotheses after this harmless algebraic tail removal.

G's finite-length FP claim was additionally checked from the freshly fetched, bound Davis PD survey, physical/printed pages 4–5. The paragraph after Theorem 3.3 records the finite-cd plus direct-limit criterion. The candidate supplies finite cd by the bounded extension spectral sequence and commutation with filtered limits by finite-type N and Q resolutions and exact filtered colimits. The N-cohomology comparison is natural and hence Q-equivariant. In each total degree the uniformly bounded filtration allows the abutment comparison. Thus this obligation also passes without presuming G was FP.

## 5. Failed routes and exact remaining gap

The generic finite-matrix/coherence route is BLOCKED as a general proof: Z[F2×F2] has the explicit bad finite-matrix kernel although its own regular cohomology is positive. Reopening it requires a new group-specific restriction, not another arbitrary kernel.

The bad-matrix route is BLOCKED as an original counterexample: induction realizes a non-FP_2 SUBGROUP augmentation syzygy inside the ambient ring, and does not realize bad dual cohomology of an FP GROUP. Reopening it requires an actual finite-projective augmentation resolution whose dual contains the required bad cohomology, with exactness and actions proved.

The unrestricted extension route is unresolved: quotient flatness/concentration are precisely the proved collapse conditions, and nothing in this packet controls arbitrary multicolumn spectral-sequence kernels or transgressions. Keeping this gap explicit supports the proposed scoped, unresolved five-turn disposition. It does not certify that the problem has no solution in current literature.
