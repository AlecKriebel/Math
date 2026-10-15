# Independent review: 30005299, five-turn Weddle partial package

**Verdict: PASS_SCOPED_PARTIALS. Overall disposition remains `unsolved`, 5/5.** All four substantive partial theorem families and the exact dimension/smoothness certificates pass this audit over the stated complex field. No mandatory mathematical correction was found. This is not a solution of the unrestricted singular/nonreduced characterization and does not certify novelty.

## Frozen version and independence

- `FROZEN_MANIFEST.json`: `c76441ac9dea8c85a9337bb5a0be75aee757a1895685d20066bd52c73da6a6d0`
- `RESULT.md`: `344988c27729d03994e51c6b1f855a205baff62bd97d8cf0aa7e58d8eeb61ee8`
- Smooth intrinsic theorem, `turns/TURN_3.md`: `4cb35c4767dcab0deec1f513d9f3cd9a4c6de7700518401f9dfcce96a42986f3`

All 17 manifest entries and both locally pinned primary PDFs match. The reviewer did not contribute to the author turns. Author files were not edited. The author checkers were inspected and replayed only in a separate copy, because they write their output receipts. Both reconstructed receipts are byte-identical to the frozen ones.

## Exact target and primary inputs

The source is Chiantini's Question 2, [OWR 54/2022](https://ems.press/content/serial-article-files/46990), printed p. 3103, PDF p. 11. The full statement was read and visually inspected. It asks about arbitrary projective three-dimensional systems of quadrics in P3 and includes the general-determinantal subquestion. It does not impose six base points. The packet correctly uses four independent quadrics, not a three-quadric net.

The source does not explicitly name the field. The packet expressly works over C, consistent with the later [Chiantini–Fagioli v2](https://arxiv.org/abs/2510.16571v2), whose notation and Definition 2.2 were checked. Its equation (4) agrees with the column-gradient matrix. The scheme-theoretic nonreduced cases are a deliberate retained extension of the unrestricted determinant setting; they are not silently discarded.

The reviewer read the full relevant statements/proofs of Beauville's [Ulrich introduction](https://math.univ-cotedazur.fr/u/beauvill/pubs/UlrichIntro.pdf), Propositions 2.1–2.2. Only the rank-one, smooth-hypersurface case is used in the smooth theorem. The singular theorem defines its linear presentation directly and does not import that smooth equivalence. The primary [Antonelli–Casnati manuscript](https://iris.polito.it/retrieve/handle/11583/2998088/84586345-55a3-453e-99d2-8a31b701d3d2/SteinerPfaffianFINAL.pdf), p. 17 before Proposition 5.7, explicitly records the ordinary determinantal-quartic dimension 33. The relevant sections of [Dolgachev–Kondo](https://sites.lsa.umich.edu/idolga/wp-content/uploads/sites/1334/2024/08/EnriquesTwo.pdf) support the classical Steinerian/polar and Enriques context; their special-web assumptions are not used as an unproved replacement for the packet's direct argument.

## 1. Fixed-representation symmetrizer and transpose obstruction

The 24 equations are exactly equality of mixed derivatives of the four transformed columns. Constant right multiplication merely changes their basis, so allowing it does not alter the existence of an invertible left symmetrizer. The coordinate-change law C^t U R^(-1) is correct. A nonzero element of the kernel is insufficient; the determinant polynomial on that kernel must be nonzero. Over C this is equivalent to an invertible specialization.

The independent checker reconstructed both 24-by-16 matrices directly from the tensor entries. It confirmed the integer minors **80862** and **5006784**, the identity in the original kernel, and the resulting ranks 15 and 16. The two determinant polynomials agree, and the coefficient/evaluation at (1,0,0,0) is **-12**. The gradient construction is integrable column by column. The later independent smoothness certificate also applies to this same sample. Thus a genuinely smooth Weddle quartic has a supplied transpose presentation that cannot be symmetrized in that fixed equivalence class. The packet correctly avoids the false inference that the quartic itself is not Weddle.

## 2. Smooth intrinsic theorem

Smoothness of the determinant forces corank exactly one on X. Its cokernel is a line bundle, and the left kernel defines a regular morphism to the original projective space. Symmetry of the column slices swaps the two factors in the polar equations. Since each kernel is one-dimensional, this gives a genuine involution.

The base-point singularity calculation is valid: at rank three the adjugate factors as a right-kernel vector times the row of the proposed fixed point, and every directional derivative of the determinant vanishes by slice symmetry. At lower rank all cofactors already vanish. Therefore a smooth Weddle quartic has no common base point and its polar involution is fixed-point-free.

The quotient defining the cokernel is evaluated by the left-kernel row. The resolution gives four global sections, so this map is the complete linear system of that same cokernel line bundle. Consequently it is sigma*H, with the given polarization retained.

In the converse, twisting the linear resolution yields the entire multiplication kernel K, of dimension four, and a 12-dimensional quotient with vanishing higher cohomology. The canonical factor-exchange linearization is essential: it identifies the domain with a tensor square whose eigenspaces have dimensions 10 and 6. Fixed-point-freeness gives zero alternating trace; vanishing higher cohomology makes this the ordinary trace on the quotient. Equivariant surjectivity in characteristic zero then leaves all four dimensions of K in the symmetric eigenspace. This forces symmetric slices of the selected intrinsic presentation; it does not claim arbitrary presentations are symmetric.

The K3 numerical/effectivity reformulation checks out. H and sigma*H are ample, their squares are four, and their intersection is six. The two relevant differences have square -4. The first is orthogonal to their ample sum, eliminating both signs from the effective cone; the second has negative H-degree, while its Serre-dual sign is explicitly excluded by hypothesis. Riemann–Roch then gives all required vanishings. The non-effectivity hypothesis is not redundant merely from the intersection number, and the packet does not assert otherwise.

## 3. Singular scheme extension

The constant-corank hypothesis is used scheme-theoretically, not just on the underlying point set. Where a 3-by-3 minor is invertible, the matrix reduces to a diagonal matrix with three units and one local equation. Its cokernel is O_X there, including nilpotents. Conversely a presentation of a line bundle has this rank at every closed point by right-exactness on fibers. Fitting ideals identify its determinant with the hypersurface equation, including multiplicity.

On the same charts, the bilinear incidence equations solve three projective y-coordinates and leave exactly the equation of X. Therefore they define the graph scheme. Symmetry preserves its ideal under exchanging x and y; both projections are isomorphisms, yielding an involution on the entire scheme. The multiplication and trace argument then works verbatim with the stated line-bundle presentation. Fixed points are allowed, and the explicit trace-zero hypothesis replaces the smooth free-action argument.

No claim about arbitrary torsion-free or higher-rank-fiber cokernels is proved. The quadruple-plane and coordinate-plane examples are correct and show failure for the specified presentations only. They do not rule out different presentations of those hypersurfaces. This restriction is stated consistently in the packet.

## 4. Dimensions, smoothness, and generic fibers

The independent checker rebuilt every differential coefficient by integer polynomial arithmetic and permutation determinants in dual numbers, without using the author's symbolic-algebra implementation. The saved original minors were independently evaluated modulo 101:

- Weddle differential, 35 by 40: rank at least 25, minor **2**
- General determinant differential, 35 by 64: rank at least 34, minor **81**
- Degree-nine Jacobian-ideal matrix, 220 by 336: full row rank, minor **93**

These nonzero reductions certify nonzero integer minors and hence characteristic-zero lower bounds. The degree-nine ideal certificate excludes every common projective zero of the four partial derivatives over C, so it establishes actual smoothness.

The universal upper bounds are also correct. The Grassmannian has dimension 24, and an ordered web adds only the determinant scalar to its affine image. For arbitrary linear matrices, the displayed coefficient tuple has zero-dimensional infinitesimal stabilizer under SL4 times SL4: the identity slice forces opposite infinitesimals, the distinct diagonal slice makes them diagonal, and the nonzero off-diagonal slice makes them scalar; trace zero then kills them. Generic 30-dimensional orbits give the 34-dimensional affine upper bound. No unsupported assertion about every fiber being one orbit is needed.

Both affine images are cones, so projectivization yields dimensions **24 and 33**. The Weddle image closure is irreducible, and the certified smooth example gives a nonempty dense smooth locus. Equal dimensions of the Grassmannian and image imply generic finiteness, without uniqueness. The general-determinantal smoothness argument via avoidance of the rank-two locus and Bertini is valid in characteristic zero.

## Final scope and disposition

Codimension nine settles the named generic subquestion negatively. It does not classify the special boundary. The rational Grassmannian projection has an actual indeterminacy locus, and the packet does not identify its image closure with the realized nonzero determinants. The smooth and constant-corank-one criteria are exact within their stated scopes only.

All retained partial results pass. Keep the complete original question **unsolved at 5/5**, preserve the separate review and exact certificate receipts, and retain classical/source attribution without a novelty claim. No additional author proof turn is supplied by this audit.
