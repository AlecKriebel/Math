# Independent adversarial audit: problem 30005902

Date: 2026-10-05 UTC. Target code: OWR-14298370-002. Catalog rank: 802.

## Verdict

**ACCEPT, with the author's explicit scope restrictions.** The frozen argument gives a counterexample to universal vanishing over an unrestricted field, including within finite-dimensional Hopf algebras. No mathematical correction is required. This is an independent AI-assisted mathematical and computational audit, not human peer review, formal proof-assistant certification, a priority decision, or editorial acceptance.

The accepted statement is:

For H = F₃[x,y,z]/(x³,y³,z³), with x and y primitive and Δz = z⊗1 + 1⊗z + x⊗y, the tensor-induction Gerstenhaber bracket on Ext_H(k,k) satisfies [f_x,f_y] = −f_z ≠ 0 in Ext_H¹(k,k). H has dimension 27, is non-quasitriangular, and has S² = id.

Both input degrees are one. The finite-dimensional characteristic-zero variant and a separate variant requiring both inputs to have degree at least two are **not settled by this packet or this audit**. No assertion of their current global status is made. There is no new-theorem or discovery-priority claim.

## Frozen input and reproducibility

The input ZIP is HOPF_LIE_30005902_AUTHOR_SAFE_FREEZE.zip, 21,055 bytes, SHA-256 ff9116239038710665c590fa392318df98aa368171545db229cebb912a7cd2f8.

Its manifest SHA-256 is 0fcd8510f2eede331a5a2bb9c2c55d21d2448e21515cdc494a2771d8c33ee281. All 13 files match. Its historic author-stage review status remains unchanged.

The original verifier reproduces the result bytes and passes 26,584 assertions, including four mathematical false alternatives. All eight original packet-integrity mutations are rejected. A separate closed-form implementation, independent of the author code, passes 29,708 assertions, including four mathematical mutations. In particular, it verifies the relevant bar-comparison maps rather than merely accepting a sign convention.

Assertion counts describe test coverage, not the number of distinct mathematical ideas. The written argument remains essential: checking finite arithmetic does not establish the cited comparison theorem or determine the intended scope of an open problem.

## 1. Adversarial source-scope check

The publisher's report was reopened, and the complete Witherspoon contribution on printed pp. 1114–1117 was read. Its cohomology uses the natural cohomological grading on self-Ext of the monoidal unit. Its Hopf-algebra setup imposes no field-characteristic restriction. Restricting to finite modules when the algebra is finite-dimensional is permitted. The characteristic-zero convention on p. 1117 belongs to the next contribution. Degree one is not excluded from the positive cohomological degrees under discussion. The text's connection to Hochschild cohomology is by tensor induction with the antipode embedding. [Publisher report](https://ems.press/content/serial-article-files/49480)

Thus this is not a counterexample obtained by silently replacing Hopf cohomology with Hochschild or Gerstenhaber–Schack cohomology. Nor does it refute only an artificially weakened finite-dimensional formulation: the example itself is finite-dimensional. Possible unstated editorial intent cannot be settled by an audit of the printed wording.

The live unsolvedmath entry could not be read through the web reader. Its contents are not claimed as independently inspected. The full cached source record and the publisher report were inspected instead.

## 2. Hopf structure and non-quasitriangularity

The 27 residue monomials are linearly independent by the monomial-ideal quotient presentation. All tensor factors commute. In characteristic three the cube of each displayed coproduct generator is zero, so Δ descends to H. This step would fail for the same truncated presentation in characteristic zero; no such substitution is allowed.

Coassociativity on z has precisely six terms: three placements of z and the three placements x⊗y⊗1, x⊗1⊗y, and 1⊗x⊗y. These match in both iterated coproducts. Coassociativity and the counit identities extend from generators as algebra identities.

The required antipode is Sx = −x, Sy = −y, Sz = −z + xy. Omitting xy leaves a nonzero antipode defect. The cube relations are preserved and both convolution-inverse identities hold. Because H is commutative, the convolution expressions here are algebra maps, so generator checks suffice. Direct substitution gives S² = id.

The tensor monomials x⊗y and y⊗x are distinct basis elements. Thus Δz − Δᵒᵖz is nonzero. Any candidate R commutes with Δ(a) in the commutative algebra H⊗H, so conjugation by R cannot produce Δᵒᵖ. Hence no quasitriangular structure exists. Commutativity of H is not being mistaken for cocommutativity or for a braiding on its module category.

The independent code derives Δ and S by binomial/multinomial formulas, rather than importing the author's generator-expansion routines. It checks all basis coassociativity, antipode, involution, bialgebra, associativity and counit identities.

## 3. Actual cycles and actual nonboundaries

For the augmentation ideal I, each f_t vanishes on 1 and I². Therefore it satisfies the scalar bar 1-cocycle identity. This is an Ext_H(k,k) calculation with the trivial action, not a statement about arbitrary linear functionals.

Every scalar 0-coboundary is a ↦ ε(a)c − cε(a) = 0. Hence B¹ = 0. Since f_z(z) = 1, its cohomology class is nonzero. The independent unnormalized δ¹ matrix has rank 24 in a 27-dimensional 1-cochain space, confirming dim Ext_H¹(k,k) = 3. The result is therefore stronger than a display of nonzero cochains.

The scalar bar resolution is free in every degree. Its tensor powers give projective resolutions with the coproduct action: tensoring a free H-module with an H-module is free after the usual Hopf untwisting isomorphism, direct summands handle projectives, and exactness of tensor products over the field gives the resolution property. Consequently the power-flatness requirement for the cited monoidal bracket is satisfied. The finite-dimensional subcategory causes no issue because the bar terms here remain finite-dimensional in each degree.

## 4. Embedding and orientation challenge

Karadağ–Witherspoon Theorem 4.1 identifies the homotopy-lifting bracket with the restricted Hochschild bracket for the induction embedding H → Hᵉ, a ↦ Σa₁⊗S(a₂). Their field is unrestricted and their antipode hypothesis holds. [Author PDF, §§2–4](https://people.tamu.edu/~sjw/pub/KW13.pdf)

The audit checked the explicit degree-one comparison in Karadağ §5 against the PDF's mathematical layout. The induced scalar cocycle takes (a⊗c)⊗_H(1⊗b) to af(b)c. Applying the comparison therefore gives aΣf(b₁)b₂c. Hence the relevant derivation is R_f = (f⊗id)Δ. [Preprint, §5](https://arxiv.org/pdf/2010.07505)

The independent verifier represents both the Hochschild bar complex and the induced complex. It checks both comparison-inverse identities and both chain-map identities in degrees one and two, on every inner basis tuple. H-bimodule linearity covers arbitrary outer factors. It also evaluates the actual induced scalar cochain after the comparison and confirms that it is R_f on every basis element.

For further sign diagnosis, let convolution be (f*g)(a) = Σf(a₁)g(a₂). Coassociativity gives R_f R_g = R_(g*f), so the right-translation commutator reverses the convolution-commutator sign. In this example:

- R_x = ∂_x + y∂_z
- R_y = ∂_y
- R_z = ∂_z
- [R_x,R_y] = −R_z

The other embedding L_f = (id⊗f)Δ instead gives L_x = ∂_x and L_y = ∂_y + x∂_z, and [L_x,L_y] = L_z. That orientation occurs in Farinati–Solotar. The two conventions must not be conflated, although both establish nonvanishing. [Farinati–Solotar preprint](https://arxiv.org/abs/math/0207243)

These are derivations on the quotient because derivatives of the cube relations vanish in characteristic three. Their equality as derivations follows from their generator values, and all basis values were independently checked. Applying ε gives −f_z, while εR_f = f. In addition, because H is commutative, every Hochschild inner derivation is zero. There is no hidden Hochschild boundary killing this bracket. By the bracket-compatible injection and the scalar B¹ calculation, the bracket in the stated Ext group is genuinely nonzero.

## 5. Identity and prior-artifact audit

All bytes of the complete cached catalog, problems corpus and research-results corpus were rehashed. Counts are 15,458, 15,458 and 6,701 respectively. Their sizes and digests agree with the author record and pinned repository metadata. There is exactly one matching ID/code record and no exact prior research-results key. The missing-key value is the empty object, verified against the pinned queue implementation.

The full-record review hash is d1bf47bd416b9d9b7c54c39b2e32861fa2d09c207aa92a75f192d3f377f69b0c. It uses the entire source record and prior value with default Python sorted-key JSON serialization. Four mutations detect changes in a nonstatement field, the prior record, statement-only input and compact separators. These are identity checks; the catalog's status does not prove mathematical openness.

The cached attempts tree was reconstructed as a Git tree object and its object ID recomputed exactly. It contains 63 entries, is untruncated and has no target directory. The related-target-groups blob was independently rehashed; no declared group contains this ID. Fresh exact-ID PR, branch and commit queries, plus a title/code PR query, found no match. A fresh direct target-directory request returned 404. Broader cached Hopf search evidence was also inspected. The related corpus screen agrees with the author metadata. These bounded checks cannot exclude deleted, unindexed, inaccessible or differently named work.

## 6. Literature, limits and disposition

The present audit reopened the primary papers and the current author bibliography. The listed March 2026 corrections to Witherspoon's book were also read; they do not alter the embedding used here. [Book corrections](https://people.tamu.edu/~sjw/pub/Corrections_March2026.pdf)

Farinati's public 2019 explanation already describes the augmentation-derivation/invariant-vector-field mechanism. This defeats any claim that the general mechanism was newly discovered in this packet. It is historical attribution, not a substitute for the displayed proof or a certificate that this exact finite example was previously published. [Public answer](https://mathoverflow.net/questions/310314/lie-algebra-of-a-compact-lie-group-and-derivations-of-the-hopf-algebra-of-repres)

The author's one-approach accounting is unchanged. This audit checks the completed example; it does not consume additional proof-search approaches or solve the untouched variants. No remote repository writes were performed. The original freeze is preserved. This companion includes authored mathematics, code, results and public verification metadata only; source PDFs, source extracts, page images, full source records, raw corpora and private coordination are excluded.
