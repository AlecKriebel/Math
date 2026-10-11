# Independent audit of density degree transfer

## Verdict

**Accept the bounded mathematical results, with the expanded justifications in PROOF.md.** The two transfer directions, the Galois divisor restriction, both optimal minimum bounds, the cubic residue-degree example, and the \(r\ge2\) curve-component inclusion are valid. The original broad restrictions problem remains only partially addressed. This is not a novelty claim or a formal proof-assistant verification.

Target: problem 20000357; AIM-ALGEBRAIC_NUMBER_THEORY-0009; AIM Problem 1.18, *Degree d points on algebraic surfaces*.

The prior proof input has 14,686 bytes and SHA256 `7597bad9bf4351a4f94447a1f05f2dd521230b542286b374a238f429af7544ff`. Its closed 144-entry inventory has SHA256 `5ef905a31d445f3f161ab0272881e3f809a966b85d957b350d19bcd9607515ec`. These are aggregate integrity identifiers; the complete accepted proof is PROOF.md.

## Mathematical checks

1. **Finite étale open: pass.** Characteristic zero gives a generically separable extension. Shrinking removes nonflatness and ramification and gives constant rank \(n\). All residue-degree bounds are applied on this open. Exact degree and density are unchanged by restricting to a dense open.
2. **Upstairs to downstairs: pass.** The finitely many relative-degree strata cover a dense set. Irreducibility forces one dense stratum. Surjectivity makes its image dense, and the residue-field tower law gives the exact quotient \(d/m\).
3. **Downstairs to upstairs: pass.** For every nonempty open upstairs, the finite image of its proper closed complement is proper by the dimension theorem. A dense base point outside that image has its entire nonempty fiber in the open. The full inverse image is consequently dense, and finite partitioning yields one exact degree \(em\).
4. **Galois refinement: pass with an explicit normal-model explanation.** A generic Galois extension does not by itself provide a globally defined action on an arbitrary nonnormal model. Shrinking to a smooth target and its finite étale inverse image produces normal models, where normalization extends the group action. The étale restriction is a constant-\(G\) torsor. Stabilizer order equals residue degree and divides \(n\). The compressed torsor step has a standard valid completion.
5. **Minimum inequalities: pass.** They follow immediately from the two transfer directions, with minima assumed to exist as stated. No claim that the same multiplier works for every degree is made.
6. **Sharp upper example: pass.** Clark's Corollary 4 has exactly the needed every-number-field/every-index scope. Index gives an actual degree-\(n\) divisor. Riemann–Roch and geometric global generation for genus-one line bundles of degree \(n\ge2\), together with infinitude of \(k\), give a degree-\(n\) pencil over \(k\). Hilbert irreducibility produces closed degree-\(nr\) fibers for every \(r\ge1\). Index excludes all other point degrees. The constructed spectrum is \(n\mathbb Z_{>0}\).
7. **Non-Galois example: pass.** The cubic factorization and negative quadratic discriminant are exact. The full fiber discriminant is also nonzero for every rational parameter, placing the examples on the étale locus. Distinct parameters give distinct quadratic closed points. The generic cubic discriminant is nonsquare, verifying the non-Galois designation.
8. **Curve \(\mathbb P^1\) inclusion: pass.** Degrees multiply under composition; the equivalence with parameterized points is exactly the cited curve result over a number field.
9. **Curve AV inclusion for \(r\ge2\): pass.** Norm after pullback is multiplication by \(n\), so the pulled-back positive-rank abelian variety retains positive rank. Effective classes pull back correctly. Multiplication by \(r\) is used as a surjective morphism of the abelian variety, without incorrectly asserting surjectivity on rational points. Viray–Vogt Proposition 5.2.1 supplies the required fiber class \(r[x]\), and Hilbert irreducibility for the composition supplies an actual closed point of degree \(rne\). The proof never identifies the possibly reducible \(f^*x\) with a closed point.
10. **Ancillary cyclic examples: pass.** The \(t\mapsto t^n\) examples were checked. Over \(\mathbb Q(\zeta_n)\), Eisenstein at unramified rational primes realizes every divisor \(m\mid n\) as a dense relative-degree stratum. This supplies examples of allowed multipliers, not a stronger classification.

## Source verification

The successfully retained AIM HTML capture directly contains Problem 1.18 and the two attached remarks. It was captured at 2026-10-11 22:00:06 UTC, with 102,036 bytes and SHA256 `e2f8861e0cdd467d4fd4e64ce77ebe36bbc88bfa25df2092f29d855738645d5a`. The mathematical statement was checked in that complete capture. A new web-tool attempt during this independent audit timed out; it is not represented as a fresh successful page retrieval.

Clark's inspected author-hosted PDF is 108,179 bytes, SHA256 `269e1fbc2091c89d69fb39ca27e157251b874eab5dc56609d62572980e153272`, five pages. The index definition on page 1 and Corollary 4 on page 2 were checked as text; page 2 was independently rendered and visually inspected. Only the existing theorem is invoked. Its deeper arithmetic proof was not re-audited end to end.

The published Viray–Vogt PDF is 2,458,194 bytes, SHA256 `ac8cbbe225d28040d37ffcb7b7c460f2cfa431b9ab4937835aa5267c5f686179`, 48 physical pages. The inspection covered the pencil and Picard definitions, Lemma 3.2.5, Proposition 3.3.1, Lemmas 4.1.1 and 4.1.4, Definition 4.3.1, Definition 5.0.2, Proposition 5.1.1, and Proposition 5.2.1 with its proof. Printed pages 26–27, physical pages 27–28, were visually inspected. The current arXiv record independently identifies the journal reference as Essential Number Theory 5 (2026), 1–47, DOI 10.2140/ent.2026.5.1. The proof uses the published PDF, not an assumed equivalence of page numbering across preprint versions.

Public source URLs, capture facts, hashes, sizes, and inspection locations are collected in SOURCE_PINS.json. Source documents, extracted source text, and rendered source pages are not authored deliverables and are outside the publication-eligible allowlist.

## Exact residual

The result does not classify possible density spectra under finite covers, identify every dense multiplier for a given map, prove reverse component-wise curve inclusions, or prove the undilated inclusion \(n\delta_{\mathrm{AV}}(D/k)\subseteq\delta_{\mathrm{AV}}(C/k)\). At degree \(ne\), it establishes an effective-class translate; a closed-point representative is an additional requirement. Failure of the formal pullback argument is not a counterexample to the stronger inclusion. Likewise, the cubic example's relative degree \(2\nmid3\) does not refute every stronger possible set-level relation. No current global literature-closure claim is made for any of these residual questions.

## Integrity and verification limits

The full 144-entry input inventory was checked independently by recomputing every byte count and SHA256 and comparing the closed file set; no mismatch, missing file, or extra file was found. Publication preparation repeated that check. These integrity checks identify the material reviewed; they are not substitutes for the mathematical reasoning above.

The public packet contains the complete authored proof, mathematical audit and acceptance report, together with public source and aggregate integrity metadata. Copied source documents, extracted source text, source images, dataset contents, programs, and private coordination material are excluded.
