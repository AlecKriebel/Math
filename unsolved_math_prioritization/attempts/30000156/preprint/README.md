# Prepared PR280 preprint package

A fixed birational map without a prime-field cycle-distribution limit

Alec Kriebel; ORCID 0009-0001-9320-500X; version 1.1; 21 October 2026 UTC.

This directory contains the paper, TeX source, verification archive and local metadata. Review, integration, publication and ledger outcomes are recorded separately in the repository audit receipts. This README does not itself certify those actions.

The two intended uploads are the paper PDF and source/verification ZIP. The TeX source is also included inside the ZIP. zenodo-deposit.json is a conventional local metadata manifest for the existing repository client; loading it does not create or publish a record. RELEASE_FILES.json binds exactly the PDF, TeX, ZIP, metadata manifest and this README by length and SHA256.

Extract the ZIP and run python3 -B verify.py inside birational-cycle-verification. It requires Python 3.9+ and the standard library, verifies the exact file set/hashes, rejects symlinks and replays the original 147,619 finite checks and a separate 46,298 all-odd-prime robustness check set. The latter covers all 167 odd primes through 1000 and exceptional assignments beyond p. Finite controls do not prove the analytic limiting assertions.

The original 17 files are retained byte for byte. Historical mathematical/source audits retain their dates and former scope/priority qualifications. The current paper supplies the stronger positive-upper-density selection proof with classical credit. Original SymPy script replay is not claimed for this preparation. No third-party full source bodies, private account records, ledger bodies or credentials are included.

The specific unrecovered Neumarker–Roberts–Viallet–Vivaldi 2011 manuscript remains a disclosed historical limit. No worldwide-firstness or current-open claim is made. AI involvement covers research, model/proof development, computation, literature, writing and audits; formal independent human peer review has not occurred.
