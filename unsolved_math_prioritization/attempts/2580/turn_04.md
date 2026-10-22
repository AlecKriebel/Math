# Attempt 4 of 5: coefficient-sensitive Bestvina-Brady groups

**Verdict: NO RESOLUTION.** Ordinary Bestvina-Brady groups cannot witness 21.71. If such a group is FL over both fields, the same finite face-count formula computes both Euler characteristics. This reconstructs a consequence of the established Leary-Saadetoglu homology calculation; it is not claimed as a new result.

## Why this family is a plausible candidate

For a finite nonempty flag simplicial complex L, let A_L be the right-angled Artin group with one generator for each vertex and one commutator relation for each edge. Let H_L be the kernel of the homomorphism A_L -> Z sending every vertex generator to 1. Bestvina-Brady finiteness properties are sensitive to the coefficient homology of L, making these groups a natural place to seek the higher-dimensional defect isolated in attempt 2.

The Salvetti complex T_L has one n-cell per (n-1)-simplex of L and is aspherical for flag L. Its infinite cyclic cover corresponding to H_L is therefore a K(H_L,1). Write A=F[t,t^{-1}], let D_j be the augmented simplicial chain complex of L over F, and put f_{-1}=1. The cover has chain complex

    C_n = A tensor_F D_{n-1},
    d_n = (1-t) tensor partial_{n-1}.

This chain model is Leary-Saadetoglu, Proposition 6; their Corollaries 7-9 give the resulting homology and Euler formula. Here is a direct field-linear derivation tailored to the proposed counterexample.

## Compute what changes with the field

Split the finite-dimensional complex D over F into boundary, homology, and complementary summands. More explicitly, choose D_j=B_j direct_sum E_j direct_sum U_j, where ker(partial_j)=B_j direct_sum E_j, E_j represents reduced homology, and partial_j maps U_j isomorphically to B_{j-1}.

After tensoring with A and multiplying the differential by 1-t, every isomorphism U_j -> B_{j-1} becomes multiplication by 1-t on a free A-summand. This map is injective and has cokernel F. Every E_j remains a zero-differential A-summand. It follows that, as F-vector spaces,

    H_n(H_L;F) is isomorphic to
       B_{n-1} direct_sum (A tensor_F reduced_H_{n-1}(L;F)).     (1)

For n=0, B_{-1}=F because L is nonempty, giving H_0=F as required.

Any nonzero reduced homology of L therefore yields infinite-dimensional ordinary group homology one degree higher. Consequently, if H_L is FL(F), then L is F-acyclic. We only need this necessary implication; no finiteness theorem in the converse direction is being silently used.

## The acyclic calculation eliminates the family

Suppose L is F-acyclic. Put z_j=dim_F B_j. Exactness of the augmented simplicial complex gives

    z_{-1}=1,
    f_j=z_j+z_{j-1},
    z_d=0 for d=dim L.

Equation (1) gives b_n(H_L;F)=z_{n-1}. Thus the Betti numbers are recursively determined by the face numbers f_j alone. In particular,

    chi_F(H_L)=sum_{j=0}^d (-1)^j (j+1) f_j.                 (2)

To verify the last identity directly, replace f_j by z_j+z_{j-1}, shift the second sum, and use z_d=0: the coefficient of z_{n-1} is (-1)^n. No field-dependent term survives.

If H_L is FL(F1) and FL(F2), both fields make L acyclic, so (2) gives equal characteristics. Choosing a link that is acyclic in one field but not the other fails a required FL hypothesis instead of creating an Euler difference.

## Explicit torsion test

Take the six-vertex 2-dimensional complex with facets

    012,013,024,035,045,125,134,145,234,235.

Pass to its barycentric subdivision, which is automatically flag: its vertices are nonempty faces of the original complex, and its simplices are chains of faces. It has face vector (31,90,60).

Exact rational and modular boundary-matrix elimination gives reduced link Betti vectors

    characteristic 0,3,5: (0,0,0),
    characteristic 2:    (0,1,1).

Therefore over Q,F3,F5 the kernel has group Betti vector (1,30,60), with Euler characteristic 31. Over F2 its group homology is infinite-dimensional in degrees 2 and 3 by (1), so it is not FL(F2). This finite torsion-sensitive example illustrates the obstruction rather than evading it.

The included standard-library Python checker constructs all faces and the barycentric subdivision, forms oriented augmented boundary matrices, and uses exact rational/modular Gaussian elimination. It also checks point, edge, path, simplex and square-cycle examples. These computations are small checks on the chain formula, not a search of all groups.

## What is still missing

More elaborate generalized Bestvina-Brady or branched-cover constructions are not excluded by the argument merely because their names are similar. Applying the same no-go result requires this precise single-link chain model. No modified construction with both FL hypotheses and unequal characteristics has been certified here. The last attempt returns to the two finite resolutions themselves to locate an exact algebraic obstruction to combining them.
