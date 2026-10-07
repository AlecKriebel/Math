# Output-sensitive sparse factorization over finite fields from dense factorization

Author: Alec Kriebel. ORCID: https://orcid.org/0009-0001-9320-500X
Manuscript date: October 6, 2026. This is a preprint, without conventional human peer review or refereeing. AI tools were used extensively in research, drafting and verification. Automated adversarial audits are not human peer review.

## Exact mathematical scope

For K=F_p[T]/h with promised prime p, supplied monic irreducible h of degree m>=1, sparse nonzero f with t distinct nonzero terms and binary exponents at most N, let b=max(1,ceil(log2(N+1))) and D be the total unweighted degree of all distinct irreducible factors. Return its leading coefficient, every monic irreducible in dense form and all positive binary multiplicities. The deterministic reduction uses at most 2b dense factorization calls of degree at most (b+1)D, and polynomial nonoracle bit work in t,b,D,m,ceil(log2 p). It handles arbitrary p-divisible multiplicities. Zero is excluded; constants and monomials are direct.

The quantitative contribution is the repeated sparse-numerator/dense-denominator implementation: numerator degree shrinks by p; after k levels the auxiliary denominator degree is at most kD. Signed multiplicity contributions cancel intermediate artifact factors. Padé reconstruction, logarithmic derivatives, known-root residue methods, Cartier identities and p-residue splitting are classical and explicitly attributed. No assertion of first priority is made.

The paper also establishes the requested complete dense factorization and prescribed-degree extension construction as inherited consequences through Berlekamp, Shoup and Rai. The prime-field breakthrough is OpenAI family142, pinned at adc7f1241b42e322a6451854ab7e4b4c146bf78a. It requires family029's all-cyclotomic finite-order Hecke zero-free theorem. Family003's narrower actual Lean scope cannot replace it. Needed source proofs were manually and adversarially inspected; no Lean build or full-follow-on formalization is claimed. The enormous prime-field branch was not implemented or executed.

Construction degree d is a numeric dense-output parameter, not log d. Optional fixed-r root extraction is polynomial in numeric r, not generally log r, and is an inherited consequence. The sparse theorem is not a bound in sparse output term count, an arbitrary-circuit theorem, or a small-common-divisor algorithm. No practical efficiency is promised by the enormous polynomial bound.

## Files and reproducibility

main.tex is standalone and contains the canonical inline bibliography. REFERENCES.bib preserves the supplied upstream citation entries and additional source metadata. paper.pdf is an actual exported PDF. PUBLICATION_FILESET.json identifies each authored file's byte size and SHA-256; it does not embed third-party manuscripts, caches, credentials or source clones.

After extracting the verification archive, from its root run:

    python3 code/reproduce.py --fileset PUBLICATION_FILESET.json --receipt receipts/clean_reproduction.json --compile-pdf

Python 3.10 or later suffices for arithmetic checks (tested with 3.14.6). PDF export was tested with Tectonic 0.16.9; Poppler pdfinfo/pdftotext provide build/text checks. The native desktop LaTeX compiler also checked the source. Font packages/runtimes are external build dependencies. Omit --compile-pdf to run only mathematical finite checks.

The consolidated reproduction verifies every frozen hash, creates a clean temporary copy, deletes saved generated JSON before regenerating it, compares all fixtures, runs dense and sparse test families, and executes separate independent prototype checks. The root sparse suite includes 960 small monic comparisons and huge binary exponents, extension coefficients and signed carries. Other independent counts overlap and are not summed as disjoint coverage. A final sparse factorization certificate uses exact original-input valuations and weighted degree; it never expands powers whose multiplicities have huge binary encodings.

The included prime oracle enumerates p only in bounded small examples. It is not a uniform bit-polynomial prime algorithm and does not certify OpenAI's theorem. Finite local analytic checks are consistency checks, not proofs of zero-freeness. Exact proof-node review limits and source identities are preserved in the ledgers and audit notes.

## Attribution, rights and review records

Newly authored prose, proofs, audits and data are CC BY 4.0; newly authored Python code is MIT. See LICENSES.md and LICENSE_CODE.txt. Cited work retains its original ownership. The PDF embeds licensed font subsets; standalone font packages and third-party source material are excluded.

The priority audits record exact primary statements, public-version dates and limits. They positively distinguish this degree-bound theorem from numerical-input-degree or partial-radical antecedents; failed searches are not novelty evidence. The complete Gianni–Trager1996 manuscript was inaccessible, so its classical dense mechanism was compared through Lecerf's exact primary treatment and precise citation chain. No claim that its full text was inspected is made.

Complete-package review reports, responses, exact reviewed fileset/ZIP hashes, final production receipt and tracker read-back are retained in the project repository separately. The earlier dense-only version-3 record and its historical reviews remain archived there. Those older reviews do not validate the new sparse theorem.
