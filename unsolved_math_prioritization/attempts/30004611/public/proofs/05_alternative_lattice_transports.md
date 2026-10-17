# Generic marked hyperplanes and limits of lattice transport

14 October 2026 UTC. Row 1775 / 30004611, shared substantive pass 4. Authored mathematical development; a partial answer to Mücksch's Problem 6.3, not a full solution or novelty claim. This report uses the accepted elementary constructions of passes 1 and 2 and proves the additional claims below.

## 1. Setup and a new sufficient class

Let A be central essential in V over a field K, dim V=ell>=2. Mark H=ker(alpha), put A'=A minus H, S=Sym(V*), R=S/(alpha), and B=A^H. Let P be the nonzero flats of A, ordered by geometric inclusion, and Q={X in P:X subset H}. These carry the upper Alexandrov topology. Write i:Q->P for the closed inclusion.

Use the accepted sheaves

- D_X=D(A_X), F_X=D(A'_X), E_X={theta in D_X:theta(alpha)=0};
- I_X=alpha S on Q and S off Q, with inclusion transition maps;
- T_X=D(B_X), and Z_X=D(B_X,m^H restricted to B_X), on Q.

The independently identified pass-1 left-exact sequences are

0 -> I tensor F -> D -> i_*T,
0 -> I tensor E -> E -> i_*Z.

All maps are the actual multiplication/reduction maps, with the original coefficient grading. In particular I is not replaced by a uniform grading shift.

Call the marked hyperplane **flat-transverse** if it contains no nonzero flat of A'. This condition is equivalent to alpha being nonzero on every one-dimensional flat of A'. Indeed every nonzero deletion flat contains a one-dimensional deletion flat when A' is essential. If A' is nonessential here, its center is one-dimensional and every deletion flat contains that center, on which alpha is nonzero by essentiality of A.

**Theorem 1.** For a flat-transverse marked hyperplane, both displayed sequences are genuine short exact sequences in every rank and over every field. Consequently they give the full ordinary and Ziegler long exact lattice-cohomology sequences, with precisely the original pass-1 terms and transports.

**Proof.** For X in Q put C_X=intersection{L in A':X subset L}, with empty intersection V. This is a nonzero deletion flat, since it contains X. Flat-transversality gives C_X not contained in H. Choose v in C_X with alpha(v)=1. The localized deletion A'_X has every defining form vanishing on v, so in the decomposition V=H direct_sum Kv all its equations are independent of alpha. The localized marked arrangement A_X is therefore the product of its restriction to H and the single normal hyperplane H. Thus H is a coloop of A_X, although H need not be a coloop of A globally.

More explicitly, R embeds in S by projection along v, and the tangent derivations of (A_X)^H lift with alpha-independent coefficients. This proves surjectivity of the ordinary map at X. Two distinct hyperplanes containing v cannot have the same intersection with H, so the localized Ziegler multiplicities are one, and those same lifts kill alpha. This proves Ziegler surjectivity at X. Outside Q the targets are zero. The kernels and naturality were already proved on all P, so stalkwise surjectivity completes both short exact sequences. The choices of v are only used to prove local surjectivity; no compatibility or global splitting of those choices is asserted. QED.

This is equivalently the condition that H be a coloop of A_X for every nonzero X subset H. If a nonzero deletion flat Y were contained in H, then C_Y=Y, and H would not increase the localization rank; conversely the preceding proof establishes the coloop condition from flat-transversality.

Over an infinite field the condition holds for a nonempty Zariski-open set of new marked hyperplanes: for each of finitely many nonzero deletion flats Y, the forbidden equations form the proper linear subspace Y^perp in V*. A finite union of such proper subspaces does not exhaust V*. For finite fields, Theorem 1 is conditional on the stated incidence condition; it does not assert existence of such a hyperplane.

### Exact transports and actual cohomology

Let P'_geom be the deletion lattice with the literal zero subspace removed if present. Its canonical inclusion into P has the exact direct image from pass 1, with stalk F_X=D(A'_{C_X}); hence H^k(P,F)=H^k(P'_geom,D'). The closed inclusion i_* is exact and preserves H^k(Q,-). Theorem 1 does not alter either transport. Its ordinary long exact sequence therefore has the actual named restriction cohomology and the same identified deletion ideal twist:

... -> H^k(P,I tensor F) -> H^k(P,D) -> H^k(Q,T) -> H^(k+1)(P,I tensor F) -> ... .

The deletion twist is related to actual deletion cohomology by the independently identified exact sequence

0 -> I tensor F -> F -> i_*(R tensor i^*F) -> 0.

The Ziegler sequence, together with 0->E->D->I->0, gives the parallel long exact sequences. No automatic freeness equivalence follows. For a nonessential deletion the center-retaining and source center-deleted conventions must still be separated; the accepted pass-2 product formula supplies the source comparison. The rank-one restriction boundary when ell=2 is unchanged.

## 2. Flat-transverse does not imply locally free deletion

Here is an explicit example outside the local-free-deletion sufficient class. Work over Q in coordinates x,y,z,u,v and set

A': xyz(x+y+z)uv=0,
H: alpha=x+2y+3z+u+v=0,
A=A' union {H}.

The deletion is the product of C={x,y,z,x+y+z} in Q^3 and two one-hyperplane line arrangements. Its one-dimensional flats are the u-axis, the v-axis, and the following six lines in the xyz factor, with u=v=0:

(1,0,0), (0,1,0), (0,0,1), (1,-1,0), (1,0,-1), (0,1,-1).

Alpha has respective nonzero values 1, 1, 1, 2, 3, -1, -2, -1 on these eight chosen generators. Thus H contains no nonzero deletion flat.

The line

X={x=y=z=0, u+v=0}

is a nonzero flat of A inside H. Its localized deletion consists of precisely the four planes of C, with two free directions u,v. This localization is not free.

For a direct proof, write a derivation of C as x f partial_x+y g partial_y+z h partial_z and impose tangency to x+y+z. Its degree-zero part is zero and its coefficient-degree-one part is one-dimensional, generated by the Euler derivation. In coefficient degree two, (f,g,h) are arbitrary linear forms subject to the three independent conditions that x f+y g+z h vanish on z=-x-y. These conditions are independent because the restrictions of x f+y g already span all binary quadratics. Hence dim D(C)_2=9-3=6. The multiples of its degree-one generator span a three-dimensional subspace in degree two. Consequently D(C) requires at least one degree-one and three degree-two minimal homogeneous generators, hence at least four generators at the homogeneous maximal ideal, despite having rank three. It is not free. Adding polynomial variables and two free derivation summands leaves this minimal-generator excess unchanged. Therefore D(A'_X) is not free.

The same reasoning shows D(A_X) is not free: the local marked arrangement is the product of C, the one normal hyperplane, and one free direction. Its logarithmic module is the scalar-extended nonfree C module plus two free rank-one summands. Thus this example also lies outside the sufficient hypothesis that every marked localization of A be free. Both genuine short exact sequences nevertheless follow from Theorem 1.

## 3. The tempting open-complement transport: exact identification, derived defect

Let U=P minus Q and let u:U->P be the open inclusion. Every original flat outside H is an intersection of deletion hyperplanes alone; hence

U={Y in P'_geom:Y not contained in H}.

Moreover D|U=F|U is the actual deletion functor restricted to this open subset.

**Proposition 2.** There is a canonical sheaf identity

u_*(D|U)=F.

**Proof.** At X in P, the left stalk is the space of sections on U intersect {Y:X subset Y}. This subposet contains V and every deletion hyperplane L containing X. All coefficient maps are actual inclusions into Der(S). A section is therefore a single derivation lying in the intersection of the modules at these points. The hyperplane points impose exactly the tangencies to A'_X, and every other point imposes only a subset of those same conditions. Thus the intersection is D(A'_X). The identification commutes with every X->Y arrow. QED.

This underived identity is useful, but it is not a statement that u_* is exact, that F is the derived direct image, or that RΓ(U,D|U) is the original deletion cohomology.

Under flat-transversality, U=P'_geom. For every X the set U intersect {Y:X subset Y} has the least element C_X. Thus in this case u_* is exact on every coefficient sheaf and preserves derived global sections, recovering the accepted deletion transport. This gives a second geometric explanation of why Theorem 1 is especially well behaved.

### A concrete higher-direct-image obstruction

Work over Q in V=Q^4 with coordinates x,y,z,w. Set

A': xyz(x+y+z)w=0,
H: x+2y+3z=0,
A=A' union {H},
X={x=y=z=0}.

The line X is contained in H. Above X, the factor w=0 disappears. The form x+2y+3z is nonzero on all six one-dimensional flats of the three-dimensional factor C={x,y,z,x+y+z}. Thus U intersect {Y:X subset Y} is exactly the punctured nonzero-flat lattice of C, lifted along the w direction. On it the coefficient sheaf is the polynomial extension of D_C plus the constant free w-derivation sheaf.

One can compute the complete positive cohomology of D_C without a freeness criterion. Consider its tangency complex

Der(Q[x,y,z]) -> direct_sum over l=x,y,z,x+y+z of Q[x,y,z]/(l).

At every retained flat of C there are at most two independent defining forms. The local derivative map is therefore onto, so the sheaf cokernel is zero. The constant degree-zero sheaf is acyclic, and each hyperplane-supported degree-one summand is the closed extension of a constant sheaf on a poset with a maximum, hence is acyclic. The complex is therefore an acyclic resolution computing lattice cohomology.

Its global cokernel is Q: if e_1,e_2,e_3,e_4 label the four rows, the constant derivative columns give e_1=e_2=e_3=-e_4; the diagonal relations then give x e_4=y e_4=z e_4=0. It follows that

H^1(P_C,D_C)=Q concentrated in coefficient degree zero,
H^k(P_C,D_C)=0 for k>=2.

Polynomial extension commutes with the finite-poset cochains, and the constant w-direction is acyclic. The usual stalk formula for the right derived direct image, (R^k u_*G)_X=H^k(U intersect {Y:X subset Y},G), now yields the explicit result

(R^1 u_*(D|U))_X=Q[w] != 0,
(R^k u_*(D|U))_X=0 for k>=2.

Thus replacing Ru_* by u_* silently drops a genuine deletion coefficient correction, even though Proposition 2 identifies its degree-zero sheaf with the named deletion sheaf.

### Why the other half of recollement does not repair this

The ordinary open/closed short exact sequence is valid:

0 -> u_!(D|U) -> D -> i_*i^*D -> 0.

But i^*D has stalk D(A_X) over S, not D(B_X) over R, and its cohomology cannot be relabeled as restriction cohomology. The open term u_!(D|U) also does not have deletion cohomology: its degree-zero global sections are zero. Indeed its stalk at H is zero, its stalk at V is Der(S), and the arrow H->V forces the V component of a global section to vanish. All U structure maps into V are injective, so every remaining component vanishes as well. In contrast, the actual deletion sheaf has nonzero global sections, for example the Euler derivation. The recollement sequence is a legitimate sequence of different terms, not a solution through unnamed transport.

## 4. Exact cohomology-preserving transport cannot erase a visible canonical defect

The following gives a scoped obstruction to correspondence-poset repairs of the standard sequences. It does not address arbitrary new maps or arbitrary new choices of the deletion term.

**Proposition 3.** Let K->M->N be one of the standard left-exact three-term sequences on P, with injective first map, equality of its image with the next kernel, and cokernel C. Let T be an exact additive transport to sheaves on a finite poset W. Suppose there is a functorial derived-global-sections comparison between the original and transported objects and maps, sufficient to give

RΓ(W,T[K->M->N]) ≅ RΓ(P,[K->M->N]).

For example, a natural isomorphism RΓ(W,T(-))≅RΓ(P,-) on the derived category generated by these terms is sufficient. If T[K->M->N] is a short exact sequence, then RΓ(P,C)=0.

**Proof.** Place the three-term complex in degrees 0,1,2. Its only cohomology sheaf is C in degree 2, so it is quasi-isomorphic to C[-2]. Exactness of T makes the transported complex acyclic if its last map becomes onto. The displayed comparison then forces RΓ(P,C)[-2]=0. QED.

Individual abstract isomorphisms between the three endpoint cohomology groups are not the hypothesis: comparison must be compatible with the arrows and the derived construction. Without that requirement the proposed transport has not preserved the named long exact sequence.

In ambient dimension four, both ordinary and Ziegler canonical defects are supported on line flats, by the accepted rank-two surjectivity proof. These are minimal points of P; distinct such points are incomparable. Thus

H^0(P,C)=direct_sum over line flats X of C_X,
H^k(P,C)=0 for k>0.

Every nonzero such defect is therefore visible to derived global sections. In particular the credited four-plane Ziegler example xyz(x+y+z), marked z=0 and promoted by w=0, has defect Q[w](-1) at the nonzero w-axis, as proved in pass 2. No transport satisfying Proposition 3 can make its standard Ziegler sequence short exact by discarding that line or otherwise annihilating that defect. The credited promoted ordinary example gives the same conclusion for the ordinary canonical sequence.

There is also the elementary pointwise version: inverse image along a surjective monotone map f:W->P is exact and conservative, because (f^*C)_w=C_{f(w)}. Such pullbacks cannot kill any nonzero defect even without the derived-global-sections hypothesis. A correspondence using these faithful inverse-image legs cannot make the canonical failed sequence exact by base change alone.

## 5. What the Everitt–Turner construction does and does not transfer

The primary source inspected for this comparison is Everitt–Turner, *Deletion-restriction for sheaf homology of graded atomic lattices*, arXiv:1902.00399v2, §§2.1–2.4 and Theorem 2, pp. 7–12. Its sheaves are contravariant functors and its invariant is higher colimit homology. The theorem removes the lattice minimum and deletes an atom. For the usual reverse-inclusion intersection lattice, that minimum is V and an atom is a hyperplane. Mücksch instead removes the zero subspace and takes derived sections of the geometrically covariant derivation functor. These are different endpoints and different derived functors.

There is a mathematically valid graded duality, but it changes the deletion operation. In each coefficient degree d, D(A_X)_d is finite-dimensional. Dualizing the finite cochain complex gives

H^n(P,D_d)^* ≅ H_n(P,D_d^*),

where the right side is homology of the contravariant dual on the same geometrically ordered poset. The full intersection lattice in geometric order is graded atomic: inside any k-dimensional flat X, choose k independent restricted arrangement forms; their k coordinate lines are original arrangement flats spanning X. Its atoms are therefore one-dimensional flats. Applying Everitt–Turner on this order, with zero removed, deletes a line atom and uses the interval above that line, not deletion of the marked hyperplane H and not the flat poset inside H. Unless ell=2, H is a coatom rather than an atom. Thus this legitimate dual construction is a different lattice operation.

There is a second independent coefficient issue. Restricting the original functor to deletion flats does not in general recompute D(A'_Y). At a deletion flat Y contained in H, choose a constant derivation partial_v with alpha(v)=1 and put q=product of defining forms of A'_Y. Then q partial_v lies in D(A'_Y), but its alpha derivative is q, not divisible by alpha. Hence it does not lie in D(A_Y). The inherited and recomputed deletion modules are genuinely different. Likewise an inherited D(A_X) is torsion-free over S, whereas the named ordinary/Ziegler restriction module is annihilated by alpha as an S-module. They cannot simply be identified.

Accordingly, Everitt–Turner supplies useful incidence-chain machinery, not an uncorrected transfer of its deletion–restriction homology theorem to the three named logarithmic derivation sheaves. This report neither asserts a literature-wide impossibility theorem nor rules out a new construction with genuinely different terms and proved comparison maps.

## Scope and references

The positive contribution is Theorem 1: actual named-target short exact sequences for every flat-transverse marked hyperplane, including higher-rank examples with nonfree marked deletion and original localizations. The transport contribution is the exact underived identity of Proposition 2 together with an explicit nonzero derived correction, the sharp mismatch in the standard recollement terms, and Proposition 3's conditional derived obstruction. These expand the accepted partial answer but do not settle the unrestricted source problem.

- Mücksch, original problem and lattice functor: https://arxiv.org/abs/2008.13700v3 , Problem 6.3, p. 18.
- Everitt–Turner, exact primary version compared above: https://arxiv.org/abs/1902.00399v2 .
- The credited four-plane and seven-plane module examples: Abe–Kawanoue, https://arxiv.org/abs/2406.00305v2 , Example 4.3. This report reuses their previously audited promotion; it does not claim to discover those examples.
