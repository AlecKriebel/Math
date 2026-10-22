# PR 872: independent spectral/probability adversarial audit

**Decision: CLEAR for the stated mathematical scope.** No blocking mathematical defect or required proof repair was found in the frozen candidate's endpoint spectrum, random-link concentration, degree comparison, or application of the triangular-presentation criterion. This is an AI-assisted mathematical audit, not human peer review, formal verification, or a priority certificate.

Audited target: property (T), with probability tending to one, for the specified free-product syllable density model at fixed `d>1/3`, fixed finite inverse-closed generating alphabets, and **at least three factors**, along every length residue. This report does not assess publication-package correctness or establish novelty.

Frozen PR head: `e3d77731b45b5f463df46e769faa01d65fe193ec`.

Frozen `PROOF.md`: 19,961 bytes; SHA256 `3bed7a81c5562d793bc4991fe62e1c06703818a9046495a7fe96d0b38e1ac100`. Its hash was rechecked unchanged after the audit computations.

## Independence and success criteria

I first read only `PROOF.md`, its source manifest, and applicable project instructions. I saved `INDEPENDENT_RECONSTRUCTION.md` before opening external theorem bodies or any original audit reports. I never read the inherited independent/second review reports or ran, imported, or consulted the author's checker. All finite computations below were independently implemented in this audit's dedicated directory.

The adversarial objective was to invalidate any step that would prevent a strict actual normalized Laplacian gap above one half, or reveal that the retrieved property-(T) criterion does not apply to this formal triangular multigraph. The main candidate's stated exclusions were retained throughout. No new unfinished central proof route was pursued.

## Findings

### Uneven endpoint weights and block types

The exact corner kernel is consistent with fixed-position cuts, both incidence orientations, all three cyclic boundaries, and deletion of inverse-fixed blocks. Destination endpoint multiplicity is essential. Summing its Perron leading term gives the stated expected degree, including the exponent `ell-t+1` and factor `h_t`.

The compressed mean walk converges to `Q tensor P tensor R` with the last-coordinate distribution `r_f^2`. Entire-class stationary masses are proportional to `h_t r_a^2 r_b^2`; the numbers of vertices of the two lengths do not supply an additional uncancelled length factor. This is shown explicitly in `DERIVATIONS.md`.

The complete multipartite letter matrix has one positive eigenvalue, and primitivity strictly separates the remaining eigenvalues in modulus. Consequently the nonprincipal spectrum of `P` is nonpositive. In the unequal-length cases this does **not** imply a nonpositive nonprincipal tensor spectrum: multiplication by the type eigenvalue `-1/2` produces positive eigenvalues up to `rho/2`. The candidate keeps those eigenvalues. Its chosen mean-gap constant `gamma=1/2+(1-rho)/4` has a strictly positive spare margin below the limiting gap. Exact compression, fixed dimension, real spectra, and eigenvalue continuity justify the eventual mean bound and uniqueness of its principal eigenvalue.

### Independent samples, common nullspace, and constants

The independent objects are the three-edge matrices of individual sampled relators, with zero matrices for rejected samples. Each is positive semidefinite and has norm at most six. Each fixed formal vertex has degree contribution at most three per sample; inverse-pair deletion is relevant to this bound. Repeated edges and relators do not invalidate either estimate.

The deterministic expected-degree normalization gives the common kernel vector `z=barD^(1/2)1`. Restriction to its deterministic orthogonal complement is legitimate and required; an unmodified full-space positive-minimum argument would fail. Applying the retrieved lower-tail inequality with summand bound `6/delta` gives the stated exponent `epsilon^2 gamma delta/12`. The degree upper tail, with scalar summand bound three, gives `epsilon^2 delta/9`. The proof needs independence across samples and a union bound across vertices; it does not assume independence of the three edges or of different vertices' degrees.

The floor in the sample count changes constants only. Fixed `d>1/3` makes minimum expected degree exponentially large, whereas the logarithm of the vertex count is linear in length. Both stated failure bounds therefore vanish. The asymptotic statement is not supplied by a numerical simulation.

### The actual degree matrix

The candidate's generalized max-min step is correct. Its chosen subspace has codimension one and need not be the actual `D`-mean-zero subspace. The Laplacian lower bound first forces connectivity, which supplies positive actual degrees before normalizing by `D`.

As an independent check, `DERIVATIONS.md` gives a direct variance proof: `D <= (1+epsilon)barD` implies `Var_D <= (1+epsilon)Var_barD`, and the matrix event bounds energy below by `(1-epsilon)gamma Var_barD`. Therefore the actual gap is at least `(1-epsilon)gamma/(1+epsilon)`. The candidate's interval for epsilon makes this strictly greater than one half. No actual/expected orthogonality substitution is hidden in that argument.

### Formal generators, torsion, and the property-(T) criterion

I retrieved and read the exact presentation graph and criterion in [Kotowski--Kotowski, arXiv:1106.2242v2](https://arxiv.org/pdf/1106.2242v2), including the multigraph Laplacian on printed page 6, Definition 2.12 and Theorem 2.13 on page 7, the repeated-relator convention on page 4, and quotient/finite-index facts on pages 5--6. The relevant complete criterion page was also visually inspected. The candidate's global inversion of the link vertices is an isomorphism of the source graph convention.

The formal block generators are inverse pairs. Source involutions are removed; quotient torsion or equal generator images are not a prohibition in this presentation criterion. Consecutive block inverses cannot occur because of source factor reduction, so the link has no loops. Parallel edges and repeated triangular samples carry their actual multiplicities. The statement being applied has no torsion-free hypothesis.

The formal triangular group maps onto the subgroup generated by its block images. The supplied suffix argument includes source torsion and gives all products of two alphabet letters for sufficiently large length. The algebraic index-at-most-two conclusion follows without replacing the original groups by free groups or claiming model preservation under such a replacement. Thus the established quotient and finite-index facts complete the stated implication to the original quotient.

## Retrieved theorem bodies and access limits

The probability theorem was checked in [Tropp, arXiv:1004.4389v7](https://arxiv.org/pdf/1004.4389v7), printed pages 20--21 (Corollary 5.2 and Remark 5.3) and the nearby proof discussion in section 5.1. I visually inspected complete pages 20--21 to resolve the positive-semidefinite glyph, which plain extraction misrendered. The matrix dimension, summand eigenvalue bound, expectation minimum, threshold ranges, and scalar specialization all match the application. The theorem itself remains an external established input.

I additionally retrieved [Einstein--Krishna--Montee--Ng--Steenbock, arXiv:2502.08630v2](https://arxiv.org/pdf/2502.08630v2) and read Definition 1.1, Remark 1.3, and Question 1.9 on printed pages 2 and 4 with their surrounding context. Definition 1.1 uses replacement and fixes the alphabet through finite word balls. Its broader model includes two factors. Thus the result should be described as the **at-least-three-factor case** of that paper's Question 1.9, rather than an unqualified solution of every case in its general formulation. For two factors, odd-length relator sets are empty, as that source itself notes. The frozen theorem already expressly excludes two factors; this is a wording boundary for any eventual paper, not a defect in its stated theorem. Matching the narrower OWR problem is reserved to the parent's target-scope audit.

Independent downloaded-PDF pins:

| Source | Bytes | SHA256 |
| --- | ---: | --- |
| KK v2 | 297794 | `88f10cadc0d38a37436b585a84c6b8e92040c67b87423b734949211f957f694b` |
| Tropp v7 | 324039 | `0536851fddb683a2c46da844e2e75c9f1a343320b43366683baa5916c60efba5` |
| EKMNS v2 | 641954 | `3aeca620da64fd462dc59c42bf049fddfdbb15f1d629e370a205390031570c29` |

Retrievals returned HTTP 200 and valid PDF bytes. Full source PDFs, extracted text, and page renders remain private/ignored. Hashes and read scopes are published as receipts. I did not obtain the final Wiley KK article body (ordinary DOI fetch returned HTTP 403), nor independently establish final-version identity of these arXiv theorem texts. Tropp's final DOI fetch returned publisher HTML, not the final article PDF. The original Zuk publisher page is a subscription preview; its Proposition 6 body was not read. Accordingly the exact read mathematical criterion is KK's explicit reformulation, with its attribution to Zuk. There was no access-control bypass or communication with authors or other individuals.

## Independent finite evidence

`independent_finite_checks.py` uses only the Python standard library and explicit runtime guards. It was run independently under both normal and optimized Python, with isolated startup. Their JSON outputs are byte-identical, SHA256 `26ef5059cf21b6ebefeee8d81a01b9f6c5b644d951aaa53cdc5bb5d086dde99e`.

Across nine exhaustive cases it enumerated **275,012 cyclic words** and performed **63,928 ordered vertex-pair comparisons** of direct actual link corner counts against the exact expected-kernel formula. The profiles were three involutory letters, an uneven `C2*C2*C4` alphabet, and mixed `C2*C3*C3`; each profile tested all three length residues. Palindromic inverse-fixed deletion counts were independently compared against an exact matrix-power formula. Every retained sample was loopless and obeyed the degree bound; degree-three examples were found.

For the uneven profile `(1,1,3)`, the Perron root is exactly three and endpoint probabilities are `(3/10,3/10,2/15,2/15,2/15)`. Rational characteristic-polynomial computations establish the spectrum of `P` and both unequal-type products exactly. Their nonprincipal positive walk eigenvalues include `1/3` and `1/6`; this refutes a tempting stronger zero-upper-bound claim. Exact compressed endpoint rows at block lengths 8, 16, and 32 converge to the stated row formula for every residue. These finite calculations are consistency and mutation evidence, not a replacement for the general Perron/asymptotic proof.

Seven deliberately wrong formulas or assertions were exhibited as false: omitting inverse-fixed completion deletion; changing oriented type multiplicities; dropping the link inverse without global relabeling; using a degree bound of two; dropping destination endpoint-class multiplicities; replacing the uneven endpoint weights by uniform weights; and asserting that every nonprincipal tensor eigenvalue is nonpositive. Their witnesses and comparison counts are in the JSON results. These are seven distinct bad models, not seven formal proofs of general correctness.

## Boundary checks and remaining gap

The audit explicitly considered all-involution alphabets, nontrivial inverse pairs, unequal part sizes, repeated block letters/edges, discarded samples, different length residues, isolated actual vertices, possible duplicate principal eigenvalues, fixed versus actual degree orthogonality, and integer rounding of the sample count. None invalidates the stated conclusion.

The strict density threshold, at least three factors, and fixed parameters are essential to this argument. With two factors, the letter walk is periodic with a `-1` eigenvalue; with part sizes `(1,1,s)` and growing `s`, the spectral margin shrinks to zero; at density one third the stated concentration domination is not established. No assertion about those excluded regimes is accepted here.

**Strongest verified result in this scope:** conditional only on the explicitly read established matrix and presentation criteria, the frozen proof supplies the mean spectral gap, high-probability actual gap strictly above one half, and the resulting property-(T) implication for its stated at-least-three-factor fixed-parameter model. **Remaining mathematical gap found within this scope: none.** Novelty, full target identification, source redistribution rights, and final preprint-package readiness require their separate reviews. No external human or formal certification is represented.
