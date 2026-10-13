# A Robinson counterexample to ideal-only tangency certificates

Alec Kriebel, independent researcher, ORCID 0009-0001-9320-500X.
Research note version 1.0, 12 October 2026.

Robinson's classical nonnegative sextic refutes the proposed unrestricted
sum-of-squares certificates modulo tangency minors. For every epsilon >= 0,
R + epsilon is not SOS modulo even the full ideal of polynomials vanishing on
the real tangency variety. The same holds for the literal separate-product
reading printed in Schweighofer's 2007 report. Removing an attainment assumption
includes attained minima; it does not restrict the question to nonattaining
polynomials. A separate nonattaining diagnostic concerns only the product reading. Its
polynomial is a constant shift of the standard example in Schweighofer (2006),
Section 1.6, equation (6), and the original report p.810. The standard sphere
minimization argument is credited to the tangency-set discussion in Laurent
(2009), Section 7.2.3, Lemma 7.21; the additional truncation multipliers in related
certificates are retained in the comparisons.

The self-contained proof permits arbitrary real coefficients, arbitrarily many
square summands and arbitrary degrees. Classical Robinson/Schur/zero-set
ingredients are credited. The identical ten-zero cubic argument appears in
Reznick, Some concrete aspects of Hilbert's 17th problem (2000), Section 4(b),
printed p.259, DOI 10.1090/conm/253/03936. The publisher reprint hosted by the
author was authenticated and inspected. First historical priority and continued open status
through 2026 are not established or asserted; see the bounded priority audit.
Complete 2008 and 2009 Hà–Pham article texts were not obtained. The comparisons
with truncated certificates rely on later primary theorem statements. The
66-record citation graph is a metadata screen, with full-text follow-ups labeled.

AI tools were used extensively in development, verification, adversarial review
and writing. This is unrefereed mathematics, with independent AI-assisted audits;
it has not received independent human or journal peer review. Finite exact
arithmetic controls supplement the universal proof and are not formal proof
certification or an SOS-degree-cutoff argument.

The archive preserves the unchanged original candidate and historical audits,
a current standalone LaTeX note, fresh independent checkers/reviews and priority
evidence. Historical pending-publication statements in the original packet are
preserved and superseded by the released note and deposit record. No primary-source
PDFs, source renders/extracts, raw catalogue records, datasets, credentials or
private account data are redistributed. Source links and retrieval hashes remain.

## Reproduce after extracting the archive

Use Python 3.10 or later with SymPy 1.14.0 installed in the same interpreter:

```
python3 -m pip install -r requirements.txt
python3 verify_package.py
python3 -O verify_package.py
python3 verify_package.py --pdf ../robinson-tangency-certificates-v1.0.pdf
```

The supported wrapper checks exact payload membership, hashes, byte counts and
immutable original proof/manifest anchors. It reruns the original author and both
historical mathematical checkers, the 61 original integrity mutations, and the
fresh independent exact checkers. All replay occurs in disposable copies. Child
processes use isolated Python without optimization, so their mathematical
assertions remain active even when the wrapper is run with -O. Direct optimized
execution of historical raw assertion-based checkers is not a supported command.
The fresh independent checkers use explicit failure guards.

Use `--integrity-only` for consistency checks without SymPy. `--pdf PATH` checks
the separately distributed PDF digest and size. An optional
`--expected-manifest SHA256` binds the outer manifest to a trusted external hash.
Hash consistency alone does not authenticate a wholly substituted verifier and
package; obtain the archive/hash from the accepted publication record. A newly
computed hash of an untrusted download is not an authenticity anchor.

Once dependencies are installed, reproduction requires no network, numerical
solver, source PDF, credentials or original workspace. The manuscript source is
standalone and can be rebuilt with `tectonic note.tex`; compilation may need its
package bundle cached or online. PDF timestamps can change the rebuilt digest.
The released mathematical statements and proof, rather than reproducible PDF
bytes, are the reference.

## License and references

Authored manuscript, proofs, code and audits in this deposit are licensed under
Creative Commons Attribution 4.0 International:
https://creativecommons.org/licenses/by/4.0/ . External references retain their
own terms and are not redistributed.

Primary conjecture: Schweighofer, Gradient tentacles and sums of squares,
Oberwolfach Report 14/2007, pp. 810–811, DOI 10.4171/owr/2007/14.
Classical form in the same report: Reznick, p.798, equation (2).
Original proposal: https://github.com/AlecKriebel/Math/pull/905 .
