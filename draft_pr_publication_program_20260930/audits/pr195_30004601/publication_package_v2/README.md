# A seven-hyperplane counterexample to a generic-initial degree bound

Alec Kriebel, independent researcher. ORCID https://orcid.org/0009-0001-9320-500X.

The six-page note proves that, in characteristic zero, the ambient Jacobian ideal of `Q=xy(x-y)(x-2y)zw(x+z+w)` has reverse-lexicographic generic initial ideal with second-variable pure-power cutoff 8 and a degree 7 minimal generator whose largest variable is the third. This refutes the correctly transcribed general-dimensional conjecture of Bigatti–Palezzato–Torielli, also recorded in OWR Report 5/2021. The imported first-variable exponent was a transcription error; its correction is not a discovery.

The proof establishes the relevant dimensions throughout a nonempty open set of compatible flags over every characteristic-zero field. It uses four ambient partial derivatives before restricting. It does not replace these by the three partial derivatives of the restricted arrangement, so the prior valid three-variable theorem of Marchesi–Palezzato–Torielli remains intact. Exact finite-flag computations corroborate the proof; they do not certify genericity by sampling. No complete gin, smallest example, positive-characteristic extension, or particular generic exponent vector is claimed.

## Credit and historical priority

The arrangement is a classical parallel connection, as treated by Falk–Proudfoot. The logarithmic/polar argument, Hilbert–Burch theorem, strong stability and generic-sectional machinery are classical. Migliore–Nagel (2025) supplies an applicable resolution of the distinct five-generated unmixed part `J^top`; this substantive family overlap is credited. The paper studies the four-generated ambient ideal `J`.

A bounded audit completed on 15 October 2026 inspected 36 primary-source records and 120 targeted queries. It identified no complete predecessor within its checked corpus. Exact comparison certificates exclude three earlier Palezzato–Torielli examples and fourteen rigid Janasz–Pokora octics as earlier refutations of this bound. A later exact supplement also excludes the specific nine-factor examples of Nasrollah Nejad–Simis and Walther, giving 19 checked examples in total. This establishes no historical firstness, independent discovery, or worldwide current openness.

Ilardi (2018), DOI 10.1016/j.jalgebra.2018.04.029, remains a material full-text gap: publisher retrieval failed/reached a CAPTCHA and the institutional postprint was restricted. Its possible overlap is unexcluded. The 63 octic parameter families, related nine-factor gins and historical code/coordinate families were not exhausted; the candidate's first public-disclosure timestamp was not authenticated. The detailed evidence matrix distinguishes actual full-text inspection from abstract/metadata access. Bibliographic metadata and authored assessments are included; downloaded articles and private retrieval responses are excluded.

Extensive AI tools were used in solving, drafting, source inspection, computational verification and adversarial review. The work is unrefereed and has not undergone conventional human peer review. AI reviews are not human peer review or historical-priority evidence.

The two additional nine-factor comparisons use maximum low-degree ranks to prove cutoff 10 and no earlier third-variable generator. They do not compute full generic initial ideals. The original bounded audit remains a dated record of its earlier scope; the supplement closes these two specific example gaps while retaining the other literature limitations. The first whole-package adversarial review of v1 is included as a dated validation record. This v2 retains the identical manuscript and PDF, cleans cosmetic README spacing and adds those exact comparison materials. The v1 review does not claim to cover this later supplement.

## Files and reproducibility

The deposit contains the PDF, standalone LaTeX source and `verification-package.zip`. Extract the ZIP into an empty directory. Its root contains this README, the manuscript source, `SOURCE_REFERENCES.json`, `LICENSE.txt`, `ARCHIVE_INVENTORY.json`, `verify_package.py`, and an `audits/` directory with the authored public-safe mathematical and priority artifacts. The archive contains no third-party dependencies or downloaded publications.

With Python 3.11 or later, from the extracted directory run:

```text
python3 -E -S -B -P verify_package.py
```

The verifier checks every inventory hash and replays five deterministic standard-library programs. It performs no writes. Two programs reconstruct the counterexample certificates: exact differentiation, sectional ranks, complete left kernels, explicit syzygy, constructive Hilbert–Burch matrix, all 21 binary Buchberger pairs, coordinate-specific partial initial ideals, 12 additional flags and excluded-case controls. Two earlier programs reproduce 17 of the earlier-example comparisons; a fifth program reproduces the two nine-factor comparisons using a pinned dependency from the priority audit. All arithmetic is exact rational/integer or exact modular nonvanishing; no floating point is used.

Individual replay commands, from the corresponding extracted audit directory, are:

```text
python3 -E -S -B -P reproduce_exact.py --verify EXACT_CERTIFICATE.json
python3 -E -S -B -P orthogonal_checks.py --verify ORTHOGONAL_CERTIFICATE.json
python3 -E -S -B -P compare_known_examples.py --verify KNOWN_EXAMPLE_CERTIFICATES.json
python3 -E -S -B -P octic_scalar_check.py --verify OCTIC_CERTIFICATES.json
python3 -E -S -B -P check_nine_factor_examples.py --verify
```

The first two live in `audits/exact_reproduction_audit_01/`; the next two in `audits/priority_audit_01/`; the fifth lives in `audits/extra_priority_controls_01/`. The orthogonal verifier checks the frozen primary implementation hash before importing it. Python 3.11+ is required for the documented `-P` option; the original sealed mathematical audit README's 3.10+ wording is a historical command-line documentation error, corrected here without changing sealed bytes.

Audit reports and gates are dated validation records. Some provenance pins reference the original repository submission, which is not needed to run the self-contained mathematical verifiers. The original submission is PR195 at https://github.com/AlecKriebel/Math/pull/195, immutable HEAD e776a961293116775fed2cb2a3019d577b84c04a. `ARCHIVE_INVENTORY.json` hashes all archive payload files except itself; ZIP checksums and the top-level seal are separate. Hashes attest file integrity, not mathematical truth or priority.

The standalone source uses standard article/AMS packages and was compiled with Tectonic; all six pages were visually checked. CC BY 4.0 applies as described in `LICENSE.txt`.
