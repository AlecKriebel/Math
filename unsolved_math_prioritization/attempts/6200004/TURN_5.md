# Turn 5: a global-cohomology obstruction to the Markov-compactum route

## Outcome and scope

This is the fifth and final substantive author turn. The original question remains unresolved. We distinguish the relative dimension of a compactum from its global cohomology, and exclude a specific tempting family: the **simplex-seeded, unsymmetrized** low-rational-dimensional building-block compacta from Dranishnikov's construction. They have the desired numerical profiles but cannot be hyperbolic-group boundaries. A sphere seed avoids this particular obstruction; it does not supply a group action. No sixth research direction is begun.

## 1. A necessary condition that a dimension profile does not capture

For a finite-dimensional compactum X and a field F, write dim_F X for relative Čech cohomological dimension and Hhat^j(X;F) for global Čech cohomology. For an actual boundary Z of a hyperbolic group, the credited global/relative boundary theorem gives

    dim_F Z = max { j : Hhat^j(Z;F) != 0 }.                 (1)

We use (1) only in positive degrees. Dranishnikov, *On Bestvina–Mess formula*, Theorem 1, proves this for Z-boundaries and every PID; hyperbolic boundaries qualify. Its introduction also derives it in the torsion-free case from the Bestvina–Mess dimension formula and compact-support cohomology. This is an external theorem, not a newly proved equality for all compacta.

Consequently, a compactum X with dim_F X=n>0 and Hhat^n(X;F)=0 cannot be such a boundary. Equality of rational, integral, and prime-field **dimensions** with an admissible numerical profile is insufficient.

## 2. A useful inverse-system test

**Proposition.** Let X be the inverse limit of finite n-dimensional polyhedra K_i with bonding maps b_i:K_(i+1)→K_i. Fix a field F. Suppose every (b_i)_*:H_n(K_(i+1);F)→H_n(K_i;F) is an isomorphism. Then

    Hhat^n(X;F) is isomorphic to H^n(K_0;F).                (2)

In particular, if dim_F X=n>0 and H_n(K_0;F)=0, then X is not a hyperbolic-group boundary.

**Proof.** Over a field, universal coefficients naturally identify H^n(K_i;F) with the vector-space dual of H_n(K_i;F). Thus each b_i^* in degree n is an isomorphism. Continuity of Čech cohomology for inverse systems of compact polyhedra identifies Hhat^n(X;F) with the direct limit of these cohomology groups. A direct system consisting of isomorphisms is isomorphic to any one term. This proves (2); (1) gives the last assertion. No surjectivity of a dual map over the integers, exchange with a homology inverse limit, or finite-stage approximation of relative dimension is used.

The isomorphism with a fixed term here concerns this coefficient and degree. It does not assert that the inverse limit is homotopy equivalent to its initial stage.

## 3. Application to a specific low-rational-dimensional tower

Fix n>=2 and a prime p. Use the **unsymmetrized** recursive maps f_m:L_m→Delta^m, 1<=m<=n, of Dranishnikov, *Cohomological dimension of Markov compacta*, Section 3, with the k=1 modification in Section 3.2. Start the pullback tower of Definition 1.3 at K_0=Delta^n. Denote its limit by X_(n,p).

The construction supplies two required facts:

- Theorem 2.7, Lemma 2.10(2), and the k=1 version of Lemma 3.8 give dim_Q X_(n,p)<=1 and dim_Fp X_(n,p)=n. They do not require the optional symmetrization for this top-dimensional prime-field conclusion.
- Every stage projection induces an isomorphism on H_n(-;F_p). This is Lemma 3.4's argument, with Proposition 3.12 replacing Proposition 3.3 in the k=1 construction.

For clarity, the second fact's extension to k=1 is checked next rather than inferred merely from the existence statement in Theorem 3.1.

At m=1 the building block is the identity of an interval. In the inductive step a lifted boundary B of an m-simplex is mapped by g:B→K' to an (m-1)-dimensional complex, and L_m is its mapping cylinder. The construction kills positive-degree mod-p homology under g. Collapsing K' in the mapping cone C_g gives the suspension Sigma B. In degree m the exact homology sequence has

    0 = H_m(K';F_p) → H_m(C_g;F_p)
      → H_(m-1)(B;F_p) --g_*--> H_(m-1)(K';F_p).

Since m>=2, the last degree is positive and g_* is zero. Therefore the middle arrow is an isomorphism. Combined with the induction hypothesis for B→boundary Delta^m, this proves that the relative local replacement induces an isomorphism on H_m. For a general finite m-complex K, decompose relative to its (m-1)-skeleton. The relative m-homology map is a direct sum of those local isomorphisms. The map on H_(m-1) of the lifted skeleton is an isomorphism by induction. The two exact rows identify absolute H_m with the respective kernels of the relative boundary maps; their commutative square therefore induces an isomorphism on those kernels. This is precisely the needed stage assertion.

Two printed notational slips in the source are not adopted: C_g/K' is Sigma B, the suspension of the **domain** of g; and a map between nonempty connected spaces cannot kill unreduced H_0. Our argument uses only positive-degree homology (or its reduced convention), so neither slip is needed as a hypothesis.

Now H_n(Delta^n;F_p)=0. Proposition (2) yields

    Hhat^n(X_(n,p);F_p)=0,   dim_Fp X_(n,p)=n.              (3)

Thus X_(n,p) cannot be a hyperbolic-group boundary. Its covering dimension is n: the n-dimensional inverse system gives the upper bound, and dim_Fp=n gives the lower bound. Also dim_Q=1, since rational dimension zero would imply covering dimension zero by the clopen-separation argument in turn 1. For n>=3 its formal group-dimension pair would be (2,n+1), with 2/(n+1)<2/3, but there is no corresponding group in this construction. Equation (3) rules out this specific boundary candidate outright.

This is a derived application of credited construction and boundary theorems. No claim of novelty or of a new construction is made.

## 4. Why this does not exclude all such Markov compacta

Changing the initial stage to a triangulated S^n changes the calculation. Whenever the same homology-preserving tower is used, (2) instead gives

    Hhat^n(X;F_p) = F_p.

The particular obstruction in (3) disappears. This is a negative control, not a realization theorem. We have not constructed a torsion-free hyperbolic group whose boundary is that sphere-seeded limit, or verified all the other boundary conditions for it. Nor have we proved that every compactum with dim_Q=1 and dim_Z>=3 violates some boundary condition. In particular, (3) cannot be used to contradict the known two-dimensional Pontryagin-surface boundary examples.

The remaining geometric task would have to supply a proper cocompact hyperbolic group action, the relevant boundary identification, and both cohomological dimensions. Repackaging a building block, declaring an inverse system Markov, or observing a surviving top class does not supply that action.

## 5. Reproducible finite controls and limits

verify_turn5.py checks, with exact arithmetic:

- cellular degree-p mapping-cylinder replacement on disk and sphere triangulations, including barycentric refinements;
- preservation of top mod-p homology, vanishing of rational top homology in the replaced cellular models, and surviving relative top mod-p classes in the disk models;
- the kernel-isomorphism linear-algebra step under invertible changes of coordinates;
- zero-seeded versus nonzero-seeded constant-isomorphism direct-system controls and the shifted strict inequality.

The cellular replacement is the two-dimensional prototype, not a computed construction of every higher-dimensional block. The direct-limit conclusions and the general induction are mathematical proofs above; finite matrices do not establish group realization or certify an infinite limit by sampling. Every earlier turn's checker was also rerun against its saved JSON output after byte-identical checkpoint recovery.

## 6. Terminal author status

Five substantive turns are now used. No source-admissible example and no universal 2/3 lower-bound proof has been obtained. Preserve the prior necessary conditions, the closed-manifold and construction-operation exclusions, the small-edge splitting reduction, the scoped subgroup obstruction, and the present simplex-seed nonrealizability result as partial work. Freeze this packet for independent review. Final publication and shared queue changes remain gated.
