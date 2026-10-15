# An even-strand Markov calculus for classical and virtual links

Alec Kriebel · ORCID [0009-0001-9320-500X](https://orcid.org/0009-0001-9320-500X)

The research note gives an explicit elementary affirmative formulation for the ordinary oriented, unframed closure interpretation of Problem 42 in the 2014 Fenn–Ilyutko–Kauffman–Manturov survey. Four classical and eight virtual reversible scheme families, together with defining relations, classify closures using only even-strand braid states. Positive padding lifts every edge of an established unrestricted Markov certificate and fixes its even endpoints exactly.

Arbitrary finite word blocks and the stated syntactic support bounds are part of the theorem. It does not claim minimality, uniformly bounded geometric support, a certificate-search algorithm, first discovery, contemporary openness, or a plat/framed/transverse/welded classification. The certificate height bound is `2 ceil(M/2)` for a supplied certificate.

The prior-work discussion explicitly acknowledges Nencka's related 1996 power-of-two braid announcement. Its generalized equivalence and ordinary-closure interpretation are not certified from the two-page source. This note makes no first-priority claim. We could not obtain the full texts of Nencka's identified 1998 article, 1999 chapter, or catalogued 1996 preprint CPT96/P.3381. The priority review is therefore incomplete, and historical ordinary-closure priority remains unresolved. This note establishes the displayed formulation from explicitly credited unrestricted theorems; it does not establish a historically new resolution. Unavailable text is not evidence of absence or invalidity of earlier work.

AI tools were used extensively in construction, drafting, adversarial review and computational verification. The note is unrefereed; no human peer review or formal proof certification is claimed. See `SOURCE_QUALIFICATIONS.md` for precise imported-theorem, priority and source-access qualifications.

## Portable verification materials

The verification ZIP contains ten small files:

- `even_strand_markov.tex`: standalone source with its bibliography; no external input or images.
- `verify_even_calculus.py`: the standard-library exact diagnostic checker.
- `expected_results.json`: full output of the genuine strengthened-checker author run.
- `VERIFICATION_RECORD.json`: source/result hashes and honest historical execution provenance.
- `SOURCE_QUALIFICATIONS.md`: target, source and prior-work precision.
- `README.md`, `LICENSE-TEXT.md`, `LICENSE-CODE.txt`.
- `build_verification_zip.py` and `SHA256SUMS`: reproducible archive instructions and member checksums.

No administrative audit corpora, third-party article bodies, credentials, DOI placeholders or raw database snapshots are included. The published PDF is a separate upload rather than a ZIP member.

## Reproduce the diagnostics

With Python 3.9 or later, from the extracted directory run:

```sh
python3 -B verify_even_calculus.py
```

No third-party modules or installation are required. The checker writes no files and makes no network requests. Its fixed local seed is 10600042. The expected JSON status is `PASS_BOUNDED_DIAGNOSTICS`, with **7,114 checks**, **316 lifted edge cases**, and **1,716 relation-context cases**. Its exact UTF-8 output equals `expected_results.json`; SHA-256 is `7020f461836f140681e88115a03cdc253aa26eed4bd97f4e59a797808d56b7ee`.

The checker covers both parities, both classical signs, virtual stabilization, right and left exchanges, reversals, empty blocks, one-strand padding, every defining relation family in bounded whole contexts, support/tags and the supplied-certificate height formula. Countercontrols reject false support enlargements. Exact Fox 3-coloring distinguishes `sigma1^3` from `sigma1`; ordered signed virtual crossing matrices distinguish an illicit exchange pair that has equal component counts. A buffered exchange countercontrol and idle-strand padding control are also included.

These finite diagnostics supplement the written universal proof. They do not prove the imported unrestricted Markov theorems, decide link equivalence, solve the braid word problem, certify novelty or establish publication status.

## Rebuild the ZIP

In an extracted copy without an existing `even-strand-markov-verification-v3.zip`, run:

```sh
python3 -B build_verification_zip.py
```

The builder first checks the complete ten-file member set against `SHA256SUMS`, then creates the ZIP and reads every member back exactly. It refuses to overwrite an existing ZIP. Paths, order, permissions and archive timestamps are normalized; ZIP timestamps are reproducibility conventions, not execution times. Compressed bytes may depend on the platform's zlib version; exact member content is the portable verification target.

New text is CC BY 4.0; Python code is MIT. The corresponding license files specify the mixed licensing. Cited publications are not redistributed or relicensed.

The strengthened diagnostics include primary-source literal nonempty L/BL endpoint controls. Their expected words do not use the shared shifting helper. A zero-shift mutant gives false left-exchange pairs with differing ordered crossing matrices even though component counts agree. These controls address a real common-mode weakness in the earlier diagnostics; they do not replace the universal proof. Fuller Nencka1998/1999 text remains unaccessed, and exact historical ordinary-closure priority remains unresolved.
