# Independent full review: group-ring cohomology, 30000590

**PASS for all stated scoped results, with the additive bibliographic correction applied. Original question remains unsolved, 5/5. No mathematical revision is required.**

This is an independent AI-assisted source and proof audit, not peer review or a novelty certification. It covers all five frozen author turns, the original FP/right-module scope, the final interpretation and both additive locator notes.

## Frozen evidence and source match

The original 41-file packet has FINAL_AUTHOR_MANIFEST.json SHA-256 a8881d305f9fa739590bfe47b8bd8ef6b28027e9523102498621e94c9085e255 and commit a52e939b8302cde1e047bd9397de5a65de218e97. The repository folder is problems/30000590_group_ring_cohomology. Every original raw file was independently fetched and matched; the Git blob IDs and sizes also match. The two-file review correction is at f8e50ea952ab99932aa6cddd57ba2a6f348c42a0, with all 43 tree blob IDs matching local bytes. Both new files were independently fetched. REMOTE_BINDING.json records these bindings.

The exact OWR contribution was read and printed p2590 was visually checked. It asks about total H*(Gamma;ZGamma), finite generation as a Gamma-module, for virtually-FP groups. The preceding Coxeter result and the companion DDJO paper distinguish the commuting **right** group-ring action from integral abelian-group generation. The source asks for a module, not a cup-product algebra.

Davis's survey definition was visually checked at printed/PDF4: FP means a finite-length resolution by finitely generated projectives. The filtered-colimit criterion after Theorem3.3 on p5 supports the extension argument. The bound book confirms the same convention at printed229/PDF233. It does not mean merely FP-infinity. A finite-index FP subgroup can be torsion-free even when the ambient virtually-FP group has torsion.

The cited positive Coxeter/Artin/acyclic Bestvina–Brady classes and their hypotheses were checked in the relevant primary passages. Associated-graded or integral splittings are not silently treated as equivariant decompositions. The broad graph-product sentence is not promoted to a solution for arbitrary factors. The predecessor KOU21.70 concerns fieldwise versus integral Poincaré duality, a genuinely different question; this packet neither retries it nor infers integral finiteness from all fields.

Primary links:
- https://ems.press/content/serial-article-files/46073
- https://msp.org/agt/2006/6-3/agt-v6-n3-p09-s.pdf
- https://people.math.osu.edu/davis.12/pdgroup.pdf
- https://people.math.osu.edu/davis.12/IGAP.pdf
- https://people.math.osu.edu/davis.12/papers/do3final-okun.pdf
- https://math.ucla.edu/~sharifi/homalg.pdf

## Turn 1: finite-index equivariance and the top-syzygy test

The pairing Phi(a)(g)=pr_H(ga) is correctly left-G/right-H equivariant. Its basis identification works for nonnormal finite-index H: inversion switches the chosen left cosets to the appropriate coefficient representatives. Evaluation at the identity gives the coinduction adjunction on cochains. The resulting cohomology isomorphism retains the natural right H-action. Finite-index restriction and extension of a finite generating family prove both directions of the exact question; no division by the index occurs.

The finite-degree consequence is justified by the finite resolution of the subgroup. H^0 is controlled by finite support. The top cohomology is finitely presented because its image is finitely generated. Right coherence is a sufficient condition, not assumed universally.

For any bounded finite-projective cochain complex, the FP_2 characterization of the top cokernel is correctly shifted: its second syzygy is the kernel one degree below the top. Quotienting that kernel by a finitely generated preceding boundary preserves the equivalence with finite generation. Schanuel's lemma removes dependence on the chosen presentation. The monomial ring control really has a non-finitely-generated right ideal, because right multiplication cannot create new initial y-exponents. It is clearly distinguished from a group ring or an augmentation resolution.

## Turn 2: ascending HNN and free products

The chosen relation t^{-1}at=phi(a) matches the transport Tf=t f(phi(-)). The identity at=t phi(a) verifies the first cochain differential term, and right coefficient multiplication commutes with transport. The Bass–Serre edge has one identity incidence map in the ascending case. Inducing the finite projective base resolutions and taking the tree mapping cone proves finite-length FP.

Finite-type projectivity makes cohomology commute with the direct sum of coefficient-height pieces. Every individual class has finite height support. The minimum nonzero height survives under 1−T, even if T has a kernel. This proves injectivity without a completion, infinite-product argument or surjectivity of phi. It would not prove the same assertion for two arbitrary nonascending incidence maps, as the author explicitly states.

The induced-coefficient tensor identity uses the correct flat side of ZG. The Baumslag–Solitar Fox factor t(1+a+...+a^{m−1}) and right-ideal presentation have the correct orientation and are well-defined. Finite free products have the claimed high-degree direct sums; the degree-one extension has finitely generated ends. No kernel over a noncoherent ring is assumed finitely generated without an argument.

## Turn 3: products, torsion and field detection

The tensor resolution is a finite projective resolution over the product group ring. Its cochains identify with the tensor of the two dual complexes because each projective is finitely generated. These complexes are free as abelian groups. The cohomological Künneth exact sequence has tensor terms with i+j=n and Tor terms with i+j=n+1, and it is natural for the two commuting group actions.

Only the tensor term is automatically finitely generated from the factor hypotheses. The criterion using the actual Tor modules is an equivalence, with the correct quotient direction. An abelian splitting is not claimed equivariant. Torsion-free abelian cohomology supplies Z-flatness and kills the obstruction.

Over a fixed field, the nonzero-factor detection argument is valid. A finite dual projective complex with zero cohomology would be contractible; double duality would contradict the original resolution's nonzero degree-zero homology. Finite tensor generators then expose finitely many first coordinates, and faithful flatness of a nonzero vector space detects the quotient. This does not imply an integral conclusion from all fields.

The PD-factor orientation action only multiplies by signs and cannot change right-module finite generation. The Bockstein exact sequence and its conditional finite-generation equivalence have the correct adjacent-degree torsion term. Reduction of the integral resolution stays exact because it resolves the Z-flat trivial module. The prime-torsion Tor formula is natural and does not assume all torsion has a fixed exponent.

## Turn 4: normal extensions and the full right action

The bounded Hochschild–Serre spectral sequence proves cd(G)<=cd(N)+cd(Q). Finite-type resolutions make the two cohomology functors commute with filtered direct limits, including the natural quotient action. Exact filtered limits and uniformly finite filtrations allow the comparison at the abutment. Together with the finite-cd criterion, this proves G is FP.

The operator C_g on N-cochains composes as C_g C_h=C_{gh}; m·g=C_{g^{-1}}m is therefore a right action. The homogeneous prism has the correct boundary sign and proves that the usual inner cochain action induces identity. Retaining coefficient right multiplication gives C_n(m)=mn^{-1}, hence the extended action restricts to the natural right N-action. No inner twist is discarded.

The explicit map from ZQ tensor M to M tensor_ZN ZG is balanced and independent of the choice of a lift. The inverse and both commuting actions check directly. In particular, the coefficient right G-action becomes the diagonal action q tensor m -> q bar(g) tensor mg. A homomorphic section is unnecessary; the proof covers nonsplit extensions.

The quotient dualizing module is expressly assumed Z-flat. The integral cochain universal coefficient sequence consequently has only the stated tensor column. Hochschild–Serre collapses with one surviving term per total degree, so no unsupported equivariant splitting of a multi-piece filtration is used. Its right action is natural through the construction.

Splitting exact tails of a bounded projective complex proves that the quotient dualizing module is finitely generated over ZQ. The finite diagonal-generation argument uses right N-generators of M and right Q-generators of D, transporting the former through a lift. D need not be finitely generated as an abelian group. The original question is not solved by removing any of these explicit hypotheses.

## Turn 5: the actual group-ring bad matrix

The two free-kernel bases follow from the infinite cyclic covering roses. The semidirect product decomposition of the three-generator height kernel is correct, including the opposite shifts on u_i and v_j. The product of the countable roses is aspherical, and the loop-permutation mapping torus supplies the two-column homology calculation.

Finite support kills the H_1 invariant term. The H_2 permutation orbits are indexed by i+j; a zero-sum finite chain on one orbit telescopes through finitely many adjacent differences. Thus H_2(H;Z) has countably infinite rank. An FP_2 resolution would force H_2 to be finitely generated over Z, so the obstruction is valid without assuming finite presentation.

The augmentation ideal is generated by the three displayed right-module elements. Its relation kernel is not finitely generated, or it would extend the presentation to FP_2. Inducing to Z[F2×F2] preserves the kernel and detects finite-generation failure by a direct finite-coordinate argument and faithful flatness. This is a genuine bad finite matrix over an actual group ring.

The ambient group's own regular cohomology remains positive. The free-group cochain cokernel is torsion-free over Z by the finite-support mod-m invariant argument. Integral Künneth then gives one finitely generated cohomology module in degree two. The bad matrix is explicitly not asserted to be the group's dual augmentation differential. The observation about adding finitely generated preceding boundaries is correct but cannot supply that missing realization.

## Locator corrections, reproduction and disposition

The pre-existing Sharifi correction is correct: Theorem4.3.12 and proof are on printed/PDF97 of the bound download. This page was visually checked. During this audit, the Davis book reference was corrected additively from printed223 to printed229, with PDF233 unchanged. The new correction is bound by REVIEW_CORRECTION_MANIFEST.json SHA-256 76d2ab2d1dcbb83b71ed87d8e60b75ad198e0c54554fa583a1803550a5cf3fa7. It changes no mathematical statement, source bytes or author turn count.

All 747,103 author assertions replay exactly. The original 28 historical bindings, 40 final entries and six primary PDFs verify; the original final manifest and the additive correction are pinned separately. The independent checker imports no author code and passes 23,463 exact controls: nonnormal S4 pairing, prism identities, noninjective height transport, integral gcd/Tor controls, a genuinely nonsplit Z/16 to Z/4 lift model, affine Baumslag–Solitar Fox identities, free-word shifts and finite orbit telescoping.

The finite controls support the analytic audit; they do not establish infinite finite-generation claims by enumeration. The exact unresolved problem is still whether an actual finite projective augmentation resolution can have non-finitely-generated dual cohomology, or whether its group-specific constraints prevent that in general. Recommend preserving the scoped packet as unsolved, five turns completed, with the additive locator note included.
