# Existing external publication: exact-result comparison

2026-10-21 UTC. Overall sweep planning completion estimate:20%.
This is an existing-publication reconciliation, not a new Zenodo upload plan.

## Observed publication and chronology

The Zenodo public API for record23284413 reports `state=done`, `submitted=true`,
creator `Ferudun, Alper`, version1.0 and publication date2026-10-10. Its server
creation is2026-10-10T15:37:46.904959Z. The DOI resolvesHTTP200 to that record.
Root downloaded all three archived files directly, checked their declared
sizes and MD5 values, and recorded independent SHA256 digests; the source ZIP
has139 members and passes CRC. Actual bodies remain in the ignored raw folder.
The PDF is22 pages. This is the external author's publication, not Alec
Kriebel's paper, a joint paper, or an upload from this effort.

PR293's server creation is2026-10-02T04:32:33Z, with the inspected mathematical
head and a current publicly accessible claim. Its previous server update was
also October2. Historic repository visibility on that day was not separately
archived here. These observations establish the order of the recorded dates;
they do not settle first public disclosure, derivation, or plagiarism in
either direction. No such accusation or firstness claim is warranted.

## Exact scientific overlap

The archived paper's Theorem1.3 and Corollary1.4 cover the same line question:
arbitrary algebraically closed characteristic, finite nonempty reduced unions
of lines in P³, symbolic-square initial degree exactly one above the radical
ideal's, and the coplanar-or-pseudostar classification with the ACM conclusion.
Neither proof imposes general position on all plane intersection points.
The external paper's additional arbitrary-field and reduced-curve claims are
not needed to establish coverage of this PR and are not certified here merely
by recording the DOI.

Root read the operative conductor/cohomology argument and line factorization
in Sections4--5 (printed pages8--15), rather than relying on the abstract.
For the needed nonvanishing, its pg=0 split and Picard restriction argument
suffice; the stronger obstruction-dimension estimate is unnecessary. The
restriction kernel is finite: a prime-to-characteristic torsion line bundle
trivial on an ample reduced connected curve would give a connected finite
cyclic cover whose inverse image of that curve is disconnected, contrary to
ample-divisor connectedness on the normal surface. This yields the required
Picard-dimension bound. Finite normalization duality and the conductor then
give the degree-(e-2) form. This is compatible with the independent root
resolution/Hodge/Albanese proof recorded separately.

The external proof uses a finite-normalization/Picard restriction/cyclic-cover
route; the PR uses a smooth resolution/Hodge/Albanese route. Shared classical
ingredients and the same conclusion do not alone identify dependence.

## Deduplication consequence

The requested result already has a published paper, source archive and
verification report with a resolving DOI. The user's instruction says that an
existing publication with a missing spreadsheet entry should be verified and
recorded rather than republished. Therefore, if the remaining independent
mathematical and priority checks pass, record this external DOI with its actual
author, precise common theorem and chronology limits. Preserve the earlier
dated PR proof and its original scope. Do not label it mathematically invalid,
invent an historical priority failure, change external metadata, or create a
second Zenodo record for the same result.

## Primary references inspected

- Original question: https://arxiv.org/pdf/1306.4387, field convention p1 and
  Question3.1 p8; https://ems.press/content/serial-article-files/46557, p514.
- External reading copy: https://eulersolve.org/papers/owr-13494-011/paper.pdf
  (SHA256 matches the actual archived PDF).
- Published record: https://zenodo.org/records/23284413.
- DOI: https://doi.org/10.5281/zenodo.23284413.
- Exact custody receipt: `EXTERNAL_PUBLICATION_CUSTODY.json`.

This comparison supports publication coverage of the line theorem. It does not
certify every ancillary claim or rerun an external exhaustive enumeration of
all2^35-1 finite configurations.
