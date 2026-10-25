# Independent publication-scope review — Zenodo 23205034

Conclusion: no publication-scope defect identified in the stated reduction and its explicitly attributed corollary. Candidate page content requires the independent analytic and adversarial mathematical gates, including an appropriate treatment of the imported prime-field/Hecke dependency. This scope review does not certify that deep dependency or exhaustive novelty.

The complete nine-page fresh published PDF, its title-page rendering, original `SPARSE_CANDIDATE_DERIVATION.md`, and manuscript bibliography were read. The independent scope conclusion was logged at 60% before any sibling mathematical opinion or dedicated archived review report was consulted. The published paper itself describes historical AI audits; these assertions were not validation evidence. The original derivation's older candidate status is preserved as provenance and does not replace the fresh public edition.

## Source and edition

Fresh record [23205034](https://zenodo.org/records/23205034), DOI 10.5281/zenodo.23205034, supplies publication date 2026-10-06 and no `metadata.version`. The PDF prints October 6, 2026 with no numbered version. Consequently `content.version` identifies that printed date. `PUBLICATION_FILESET.json` carries internal label `publication-candidate-v5`, created 2026-10-07T06:08:52.863807+00:00; this is package provenance, not a numbered Zenodo/manuscript version. The page must not infer or silently insert v5 or v1.0.

All published assets were freshly acquired: nine-page `paper.pdf` and `verification.zip`. Their live Zenodo MD5, receipt SHA-256 and sizes match. The ZIP passes CRC; all 58 fileset entries match byte counts and SHA-256. Its sole PDF, `manuscript/paper.pdf`, is byte-identical to the separately published main PDF. No supplementary PDF is missing. `source_integrity.json` records the checks. Original files are unchanged.

The entire abstract, including upstream-dependency disclosure, is retained with whitespace/typography normalization only; AI status is separate. The first-page render confirms the edition and abstract boundaries.

## Exact theorem and distinctive content

K is explicitly supplied as F_p[T]/(h), with binary prime p and a monic irreducible h of degree m. The sparse input is nonzero and univariate, with t distinct nonnegative binary exponents and nonzero field coefficients. N is its total degree and b=max(1,ceil(log2(N+1))). Distinct irreducible factors are returned densely; their unweighted degree sum D controls output size, and multiplicities are binary. Zero is rejected; constants/monomials have direct cases.

Theorem 1 is a deterministic reduction to complete dense factorization over K: at most 2b calls, each of degree at most (b+1)D, and nonoracle bit complexity polynomial in t,b,D,m,ceil(log2 p). It does not require p-coprime multiplicities. The direct p-fixed-algebra reduction yields at most 2b(b+1)D prime-field calls with the same degree bound. This is distinct from polynomial cost in sparse output support alone, finding a small GCD, or factoring arbitrary arithmetic circuits.

The compressed invariant is the proposed addition: F=U/V remains a polynomial with sparse U and dense V; the numerator degree shrinks by p and the denominator degree grows by at most the original radical degree at each step. Visible factors come from exact logarithmic-derivative reconstruction. Residue recursion recovers full multiplicities while visiting occupied exponent classes. Cartier sections and inverse coefficient Frobenius maintain the representation. Signed residues are necessary because temporary factors may cancel. No loop of numerical length p or N is licensed by the argument.

Dense extension-field factoring and prescribed-degree construction are explicitly inherited reductions. Construction is polynomial in numeric d, the dense output size; a binary encoding of d does not make the bound polynomial in log d. Optional fixed-r extraction has numeric-r cost. The tiny exhaustive prime oracle is not an implementation of prime-field derandomization, and finite runs do not establish practical performance or asymptotic complexity.

## Imported theorem boundary

Fresh original PDFs were retrieved at commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a`, with independent receipts under `primary-sources/`:

- [OpenAI, Deterministic Polynomial Factorization over Prime Fields](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Deterministic-Polynomial-Factorization-over-Prime-Fields-October-4-2026/Deterministic-Polynomial-Factorization-over-Prime-Fields.pdf): 48 pages, SHA-256 `ed88aa5ba802311a21c4f265bcef43515a16019f4b5afdd7f52ecbd36ce0204d`. Read the abstract, Theorems 1.1–1.2 and introduction/dependency discussion. Theorem 1.1 supplies the cited uniform polynomial bound; Theorem 1.2 separately depends on the numerical auxiliary-prime bound.
- [OpenAI, Primitive roots for every admissible integer base](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Primitive-roots-for-every-admissible-integer-base-October-4-2026/primitive-roots-all-integer-bases.pdf): 92 pages, SHA-256 `671ac4b3ece879f614ed8f4b782e61a07805e533f385a694fe4d7afbda3c9365`. Read the abstract and initial theorem/dependency discussion. The required Theorem 1.2 concerns every finite-order Hecke character over every cyclotomic field containing μ12, in the common strip Re(s)>1−10^-6, permitting the principal pole.

The entire 48/92-page proof bodies were not independently re-proved in this scope review. No Dirichlet-only statement, archived AI audit, or finite computation substitutes for that general input. Public explanatory prose separates the oracle-independent sparse theorem from the source-dependent unconditional corollary and does not claim ownership of the upstream work. Raw primary-source PDFs are locally ignored, not proposed website assets.

## Primary comparisons and access limits

- [Mattarei, arXiv:math/0512239v2](https://arxiv.org/html/math/0512239v2), Theorem 2 and its proof: directly inspected the p-adic multiplicity/weight inequality and residue argument. The new note correctly attributes this structure; its known-factor routine is a constructive use, not a new multiplicity-versus-sparsity theorem.
- [Rowland–Yassawi, arXiv:1310.8635v2](https://arxiv.org/html/1310.8635v2), Proposition 1.9 and proof: directly inspected the Cartier pull-out identity. The paper's extension-field use must include coefficient Frobenius; the elementary section identity itself is established.
- [Demin–van der Hoeven, arXiv:2312.17380v2](https://arxiv.org/pdf/2312.17380v2): inspected abstract/introduction, complexity discussion, and relevant squarefree-scope passages. Their probabilistic sparse framework allows polynomial dependence on numerical total degree. This supports the described model distinction, not an exhaustive exclusion of every consequence of their algorithms.
- [Rai, arXiv:2410.04071v1](https://arxiv.org/html/2410.04071v1), Algorithm 2 and Theorem 4.1: inspected the exact degree-md lift, factorization over the extension field, and lexicographic choice. The lift is prior work. Its random/pseudo-deterministic subroutines should not be confused with the deterministic substitution here.
- [Shoup's author manuscript](https://www.shoup.net/papers/detirred.pdf): its primary indexed abstract states deterministic reduction of prescribed-degree construction to prime-field factorization. The body returned garbled text, and the publisher PDF request was denied; precise complete theorem-body verification is not claimed here. Rai supplies a directly readable primary account of the inherited construction mechanism.
- [Lecerf (2008)](https://doi.org/10.1007/s00200-008-0062-4): author-hosted indexed abstract and publication identity inspected. Direct original-body retrieval timed out/was refused. Sections 2.1–2.2 were therefore not independently read in this review, and the source is not ruled out as a closer antecedent.
- [Dutta–Saxena–Sinhababu, arXiv:1710.03214v1](https://arxiv.org/pdf/1710.03214): inspected the accessible 2017 version's introduction and model assumptions. It is not the 2022 journal body containing the cited §6.3; no exact section-level comparison is claimed. The manuscript also credits Kaltofen's reconstruction and Berlekamp's classical factoring reduction; those complete original bodies were not re-reviewed here.

No firstness, new primitive method, or exhaustive priority conclusion follows from these bounded comparisons. The candidate content credits established components and identifies the particular compressed invariant without promoting a limited audit into priority certification.

## Page disposition

The candidate contains exact abstract, plain explanation, assumptions, reduction/corollary distinction, prior links, source downloads, short mechanism discussion and professional collaboration invitation. Extensive AI assistance and unrefereed status remain visible. `follow_up` is null: sparse-only output, circuit generalization, practical improvements and replacing deep inputs are broad programs, not supported new conjectures meeting the requested bar. No published proof was repaired and no external person was contacted.
