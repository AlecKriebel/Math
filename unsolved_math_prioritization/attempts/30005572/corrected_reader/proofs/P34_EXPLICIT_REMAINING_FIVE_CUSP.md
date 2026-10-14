# A concrete remaining wild-five cusp test

14 October 2026. Within the final shared PASS5. This is a rigorously identified test of the actual accepted construction, not a nonzero computation and not a counterexample.

## 1. Field, level, and already available arithmetic map

Take F=Q(i), O=Z[i], pi=2+i, q=(pi), and N=q^2. The Gaussian norm is Euclidean, so Cl(F)=1. Also Nq=5. The four units 1,-1,i,-i have distinct reductions modulo q, so this level is unit-injective. The ray exact sequence gives

   Gal(L/F)=(O/q^2)^times/O^times,    |Gal(L/F)|=5,
   L=F(q^2).

Thus the ray group G is cyclic of order five. The conjugate prime qbar does not divide N, so the ideal-divisibility condition (5)|N^2 is false. The accepted PASS4 arithmetic theorem and its full unaugmented corollary therefore provide the actual source-calibrated unaugmented R-valued open map at this level: the five block is nonexceptional, and h=1 handles the p>=7 conditions. This uses the previously accepted result, not a new assertion that arbitrary compatible smoothing data can be divided.

The accepted PASS2 residue-module theorem is an unconditional module computation over R: since h=1, q is totally ramified in L/F and the unique residue field above q is F5. Its multiplicative group has order four. Localization consequently gives an isomorphism

   K2(O_L) tensor R -> K2(O_L[1/q]) tensor R.

Applying this to the accepted PASS4 open map gives an actual integer-ring-valued open map. Its good-prime Hecke relations, including at qbar above five, are unchanged. No compactification or bad-U identity is being inferred.

## 2. Two explicit cusp loops

Use the principal component and

   tau=[[1,0],[pi,1]],        lambda tau=(pi,1).

The cusp is the line spanned by (1,pi)^t. In its adapted coordinates, strict unipotent loops have parameter z in q, because pi z=0 modulo q^2 if and only if z is divisible by pi. A Z-basis is pi, i pi. Direct multiplication gives

   gamma(z)=tau [[1,z],[0,1]] tau^{-1}
           =[[1-pi z,z],[-pi^2 z,1+pi z]].

In particular

   gamma_1=[[1-pi^2,pi],[-pi^3,1+pi^2]],
   gamma_2=[[1-i pi^2,i pi],[-i pi^3,1+i pi^2]].

Both matrices have determinant one, lower-left entry divisible by N, and lower-right entry congruent to one modulo N. They therefore belong to the actual strict Gamma1(N).

The cusp valuation is r_q=1, whereas n_q=2 and e_q=v_q(2)=0. Both strict reflection inequalities fail. More generally, distinct Gaussian units are distinct modulo q. The general-unit criterion of CUSP_REFLECTION_AND_COMPACTIFICATION.md requires epsilon=1 and delta=1 at this middle cusp, so no unequal diagonal-unit pair occurs. Consequently the ambient first homology of this boundary component has rank two over R.

This rank statement does not assert that its two loops remain independent in H1(Y), or that either has a nonzero K2 image.

## 3. Actual values lie in G-invariants

There is a useful further constraint which does not evaluate them. For every t in O, the matrix gamma(t) belongs to Gamma0(N), even if t is not in q: its lower-left entry is -pi^2 t, and its lower-right residue is 1+pi t. The coefficient actions

   R_N(1+pi t),    t in O,

range through all of G. Indeed 1+q modulo q^2 is a subgroup of order five, and its map to the ray quotient is injective because the global units already inject modulo q.

The matrices gamma(t) commute with gamma(z). For the actual Gamma0 crossed homomorphism z_N, conjugation by gamma(t) therefore gives

   z_N(gamma(z))=R_N(1+pi t) z_N(gamma(z)),    z in q.

Consequently both of the actual, still unevaluated values

   x_1=z_N(gamma_1),    x_2=z_N(gamma_2)

belong to (K2(O_L) tensor R)^G. This statement also holds for the auxiliary family and is independent of the choice of cocycle representative because its restriction to Gamma1 is a genuine homomorphism.

For every rational p>=7, the source's already accepted compactification theorem applies here: no prime over p divides N, the squared-cyclotomic exclusion is automatic, and the residual-character exclusions at primes over p are automatic. The PASS4 comparison identifies those p-parts with the source maps. Hence x_1 and x_2 have only a possible five-primary part, and in fact lie in

   (K2(O_L) tensor Z_5)^G.

It is essential not to replace G-invariants by descent to K2(O_F). This is a degree-five extension, and the restriction/transfer composite is multiplication by five. The accepted prime-to-five descent argument cannot cancel that degree here. Likewise no computation of K2(O_L)[5], its G-invariants, or the values x_1,x_2 has been supplied.

## 4. The exact remaining obligation

Compactification at this cusp requires x_1=x_2=0. The source-calibrated map already exists here, the five smoothing factor is invertible on the relevant block, and the arithmetic residue module has been removed integrally. What remains is the actual parabolic restriction, with a possible wild-five issue, together with the other cusp restrictions and the bad-U/relative-calibration obligations of the full contract.

Thus this example separates the cusp problem from exceptional smoothing, small-level model descent, class-group assembly, and prime-power arithmetic residues. It is not claimed to be the smallest possible unresolved example, or to have a nonzero K2 value. It is an explicit sharp stopping point for the present actual-value argument.

## Inputs

- Accepted PASS4 ARITHMETIC_DESCENT_AND_AUXILIARY_REMOVAL.md, especially Sections 7-8 and its full-R corollary.
- Accepted PASS4 OPEN_HOMOLOGY_GOOD_HECKE.md.
- Source Theorem 5.2.9, used only in its restricted scope for p>=7 with p not dividing N, as discussed in this reader.
- Accepted PASS2 ABSOLUTE_INTEGRALITY_AND_RESIDUES.md, Sections 2-3, using the unconditional residue-module calculation at its stated R coefficient scope.
- New CUSP_REFLECTION_AND_COMPACTIFICATION.md, Sections 2, 3 and 8.

No external tame-kernel table or unproved numerical group-order assertion is used.
