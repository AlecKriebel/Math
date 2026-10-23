# Canonical tightening can lose the natural wavelet indexing

A direct, quantitatively audited canonical-tight analysis of a classical wavelet perturbation family.

## Result

Let h be the normalized Haar wavelet, Df(x)=√2f(2x), T_kf(x)=f(x−k), and φ=h+(1/100)Dh. The full affine family {D^jT_kφ : j,k∈Z} is a Riesz basis of L²(R) with valid frame bounds 9801/10000 and 10201/10000. If F is its ordinary frame operator, then

    ||F^(−1/2)T_1φ − T_1F^(−1/2)φ|| > 1/1000.

Thus the canonical normalized tight family cannot be written as {D^jT_kη} with the original dilation, integer translation lattice, single generator, and natural indexing. The index (0,0) forces η=F^(−1/2)φ, and the identity already fails at (0,1).

This supplies a negative answer to Michael Frank's 2004 source question under its usual indexed single-generator meaning. It does not settle arbitrary permutations, altered lattices/dilations, or additional generators. No novelty or present-day literature-wide openness claim is made.

## Read in this order

1. [Source-scope and prior-art adjudication](scope_adjudication/SOURCE_SCOPE_ADJUDICATION.md): why the indexed contract matches the source, precise disposition, and prior credit.
2. [Full original proof](accepted/core/COUNTEREXAMPLE.md): all-space Haar basis, exact frame operator, convergent inverse-square-root expansion, and quantitative translation defect.
3. [Independent acceptance audit](accepted/audit_a/ACCEPTED_AUDIT.md): separate operator audit; obtains the stronger bound ≥19/5000.
4. [Second independent check](accepted/audit_b/INDEPENDENT_HAAR_CHECK.md): separate norm-convergent estimate obtaining >3/1000.
5. [Optional dual-to-tight bridge](optional_bridge/BRIDGE_LEMMA.md) and its [separate acceptance audit](optional_bridge/BRIDGE_ACCEPTANCE_AUDIT.md): an independent existence argument for complex Hilbert spaces. The explicit real-valued Haar counterexample does not depend on it.

The [original formulation contract](accepted/core/CONSTRUCTION_CONTRACT.md) is retained verbatim as a historical scope record. Its bounded-search status predates the accepted construction and final scope adjudication. Likewise, earlier proof and audit context is preserved unchanged; the final source adjudication and [scholarly notes](SCHOLARLY_NOTES.md) supply the additional historical credit.

## Classical provenance

The family η+ε√2η(2·) is classical. Daubechies–Han (2002), p.271, equation (1.6), explicitly records it and credits Daubechies (1990) and Chui–Shi (1993). Daubechies (1990), pp.988–989, attributes the perturbation to P.-G. Lemarié, communicated by Y. Meyer, and uses the corresponding basis-index partial-isometry mechanism for canonical-dual analysis.

The authored proof here directly evaluates F^(−1/2). Canonical-dual failure alone would not establish the required conclusion for the same generator. The checked bibliography does not determine whether this canonical-tight argument or conclusion was previously published.

## Verification and reuse

All proof, audit, and adjudication originals are preserved byte-for-byte, with [exact copy pins](ORIGINAL_ARTIFACTS.json). [MANIFEST.json](MANIFEST.json) seals the complete reader membership. The package contains authored work and public verification metadata only; no source PDFs or dataset contents are attached.

Run with Python 3 and its standard library:

    python verify_bundle.py
    python -O verify_bundle.py
    python -OO verify_bundle.py
    python replay_diagnostics.py
    python test_negative_controls.py

The scalar replay checks exact rational constants already displayed in the proof. It neither truncates the Hilbert space nor proves any frame/operator statement. Its recorded successful runs and active failure controls are in [REPLAY_EVIDENCE.json](REPLAY_EVIDENCE.json). See [validation details](VALIDATION.md) and [publication boundary](PUBLICATION_BOUNDARY.md).

## Independent integration review

The [integration acceptance](INTEGRATION_ACCEPTANCE.md) records a corrected 2002 author field, strengthened integrity validation and independently repeated scalar checks. All ten original artifacts remain byte-identical. The [complete input manifest](INPUT_MANIFEST.json) is preserved verbatim; [link review](LINK_REVIEW.json) discloses retrieval limitations. No new mathematical pass or publication is implied.
