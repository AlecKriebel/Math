# A7-power restricted recognition record

The mathematical argument is in `A7_power_recognition.md`. It is a restricted theorem whose mathematical proof passed a fresh adversarial review; priority remains unresolved, **not a complete solution of Kourovka21.135**. No originality or publication claim is attached.

Reproduce the ordinary degree witnesses using Python3, with no GAP/Sage installation required:

1. Run `python3 fetch_primary_table_data.py` to download the exact primary CTblLib1.3.11 archive, verify its recorded SHA256, and recover only the whitelisted source files with matching hashes.
2. Run `python3 check_primary_degree_witnesses.py` for the author's ordinary first-column/projective-row reader.
3. Run `python3 review/independent_degree_witnesses.py` for the adversary's independent lexical reader.
4. Compare the exact integers in `primary_degree_witnesses.json` and `review/independent_degree_witness_results.json`.

The finite-linear classification is an external theorem of Lindsey (1971), cited by exact DOI and section in the mathematical note. The character tables are external primary ATLAS/GAP data, independently read and checked here; no computation from a presentation or matrix generators of the groups is claimed. The two readers are independent code paths, not independent constructions of the character tables.

Raw publisher PDFs, table files, and the archive are local source caches. The authored proofs, readers, exact result JSON, review, and hash/provenance JSON form the persistent research record. The exact source archive allows the cache to be recovered without committing complete third-party bodies.
