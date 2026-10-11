# Independent mathematical audit: row 1703 / problem 2100702

## Verdict

ACCEPT-BOUNDED, with the explicit formulation in `PROOF.md`.

The frozen candidate's Sard/Fubini equivalence is correct. Its compact scalar Berezin-Toeplitz application is also correct in the standard norm-controlled calculus. Two implicit conventions are made explicit in the audited proof:

1. The compact limiting volume is Liouville volume, normalized by its total mass. An arbitrary smooth density has the same null sets but need not produce the same limiting measure.
2. A standard scalar order-zero Toeplitz family with principal symbol `f` has leading approximation `T_k = Pi_k f Pi_k + O(k^(-1))` in operator norm. Merely assigning an informal symbol to bounded matrices would not suffice.

The result is a sufficient-framework theorem for spectral detection, not acceptance of an unrestricted solution to the source problem. The original problem remains outside the theorem's scope whenever the required counting measure or rank-free Weyl law is not known. No novelty finding or exhaustive present-day literature-status finding is asserted.

## Frozen input

The candidate was read without modification:

- Byte count: 4543
- SHA-256: `c89fe529308323441ad4dd34e5f6ae150b4fe7bd00e02b5f1b4239219295a658`
- Freeze: 2

The candidate's identity is recorded separately from the revised authored proof. The revised proof is a new artifact, not an in-place change to the frozen input.

## Original question and citation reconciliation

The primary source is by Bolsinov, Matveev, Miranda, and Tabachnikov. Section 7.1 of arXiv:1804.03737v2 introduces `n` self-adjoint, commuting semiclassical operators on a quantum space associated to a `2n`-dimensional phase space. Its independence axiom is independence of principal-symbol differentials almost everywhere. Problem 7.2, printed/PDF p. 36, asks for spectral detection using asymptotic joint eigenvalues or eigenfunctions. This matches the candidate's target.

The same item is Problem 6.2 in arXiv:1804.03737v1, printed/PDF p. 46. The original problem does not specify whether joint eigenvalues are supplied with multiplicities. This audit therefore explicitly accepts only the multiplicity-aware reading needed for the trace method.

The proof does not replace “almost everywhere” by “on an open dense set.” Those conditions are not interchangeable for a general smooth map. It also does not demand absence of singular points.

## Measure-theoretic adversarial checks

- **Sard:** Smoothness is sufficient. The critical-value set has Lebesgue measure zero. There is no rank assumption hidden in this use of Sard.
- **Measurability:** Under the usual second-countable manifold convention, the critical set is closed and has a countable compact exhaustion. Its image is a countable union of compact sets and hence Borel. Neither completed-measure ambiguity nor an analytic-set theorem is needed.
- **Regular-set direction:** Local submersion coordinates can be chosen with the first coordinates equal to the components of `F`. Fubini proves null-preimage statements in each chart. A countable cover closes the global proof.
- **Positive critical volume:** Its entire pushforward is supported on the Borel null set of critical values, hence gives a nonzero singular part. Positivity prevents cancellation.
- **Noncompactness:** No properness of `F` is used. Local finiteness is imposed on its pushforward and the spectral measure, and local spectral convergence is formulated with continuous compactly supported tests. A one-window result is not silently promoted to a global one.
- **Boundary:** Standard phase spaces have no boundary. With a smooth boundary and ordinary volume, boundary mass is zero and the interior proof suffices. Additional boundary-supported measure is excluded.
- **Choice of volume:** Smooth strictly positive densities have identical null sets. The result detects the rank condition in that volume class; equality of particular pushforward distributions still depends on the density.
- **Decomposition:** The proof also establishes that the singular part is exactly the pushforward of critical-set volume. In the compact normalized case its mass equals the critical-volume fraction.

No failure was found in either implication.

## Toeplitz and spectral adversarial checks

- **Quantization assumptions:** The revised theorem fixes `H_k=H^0(M,L^k)`, the usual orthogonal compression, positive prequantum `L`, scalar real symbols, norm-controlled leading approximation, and exact pairwise commutation and self-adjointness.
- **Very ample versus positive:** The older sources use a very ample convention. Ma-Marinescu's positive-prequantum setup, Theorems 0.1 and 0.3, supplies the trace and norm-product estimates without this additional restriction. This source check avoids relying on an unexplained passage from a cofinal subsequence to all `k`.
- **Multiplicity:** Every common eigenvector contributes once. Equivalently each joint eigenvalue is weighted by the dimension of its common eigenspace. Dimension alone plus the set of distinct eigenvalues does not recover these weights.
- **Remainders:** The errors used are operator-norm errors. An `O(k^(-1))` norm error contributes at most `O(k^(-1))` to the normalized trace because `|Tr R| <= N_k ||R||`. There is no mistaken unnormalized trace estimate.
- **Products:** For a fixed polynomial, telescoping replacements and the scalar product estimate produce a uniform-in-`k` operator-norm error. Constants may depend on that polynomial; uniformity in growing polynomial degree is not claimed or needed.
- **Trace normalization:** Applying the scalar trace formula to the constant symbol gives the asymptotic dimension, so its leading constant cancels after division by `N_k`. No guessed power of `2pi` is used.
- **Weak limit:** Uniform spectral bounds and compactness of the symbol image give one compact cube. Stone-Weierstrass and unit total mass extend polynomial moment convergence to every continuous test function. This is multivariate convergence, derived rather than assumed.
- **No circular use of integrability:** The analytic inputs concern arbitrary fixed smooth scalar functions. Neither Liouville tori nor full rank of the joint symbol is assumed.
- **Finite data:** Each empirical measure is atomic. The a.e. rank condition is read from the exact limiting measure, not from absolute continuity of a finite empirical measure or from an atom-only test.
- **No implicit operator-domain claim:** The compact Hilbert spaces are finite-dimensional. The result does not equate algebraic commutation of unbounded operators with strong commutation, and does not address continuous spectrum.

## Direct source inspection

All five PDF files listed in `SOURCE_PINS.json` were independently downloaded from their versioned public arXiv URLs. The original problem v1/v2 and the Schlichenmaier review are byte-identical to the previously supplied PDFs. Their existing files were not changed.

The following material was read directly:

- Original source v2: section 7.1, pp. 35-36; p. 36 rendered and visually checked.
- Original source v1: the context and Problem 6.2 on p. 46, rendered and visually checked. Page 49 was also inspected during numbering reconciliation but contains later problems, not Problem 6.2.
- Schlichenmaier review: setup and estimates, pp. 7-10; pp. 8-10 rendered and visually checked.
- Bordemann-Meinrenken-Schlichenmaier: setup, Theorems 4.1-4.2, and section 5 product/trace remarks; p. 12 rendered and visually checked.
- Ma-Marinescu: introduction and Theorems 0.1-0.3, pp. 1-5; pp. 1, 3, and 4 rendered and visually checked. The last PDF extracts some mathematical glyphs poorly, so visual checking was used to confirm the leading coefficient, remainder power, and operator-norm interpretation.

Inspection was confined to the cited assumptions and analytic statements. This audit is not a new proof of the full Bergman-kernel calculus. Its integrity verifier checks file identities, not the truth of mathematical statements.

## Publication boundary

The authored proof, authored audit, acceptance metadata, and public source pins can form a bounded public mathematical report. The source PDFs, extracted source text, screenshots, working scripts, and local coordination material are not part of that public report. No publication, repository change, queue edit, commit, or push was performed by this audit.

## Acceptance summary

Accepted:

- The equivalence between a.e. full rank and absolute continuity of a smooth-volume pushforward.
- The conditional multiplicity-weighted spectral criterion under an independently available rank-free joint Weyl law.
- The standard compact Kähler scalar Toeplitz application, with explicit norm approximation and Liouville normalization.

Not accepted as proved:

- A solution for arbitrary semiclassical operators.
- A criterion using only unweighted spectral sets.
- A stable or finite-data algorithm.
- A theorem detecting every rank-deficient point.
- A claim of novelty or a verified resolution of the full open problem.
