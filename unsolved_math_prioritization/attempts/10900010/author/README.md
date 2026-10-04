# Agol tree action and Thurston norm research packet

Problem 10900010 / AMR-108-0010, campaign rank 672.

**Result: NO RESOLUTION.** Five approaches produced rigorous special cases and obstruction tests, with no proof or counterexample for the general problem.

Main deliverables:

- PROOF.md: complete authored proofs of the partial statements, including translation-line actions and geometric surface-group splittings; explicit examples separating homology and norm claims.
- APPROACH_LOG.md: the five approaches and their stopping points.
- SOURCES.md and SOURCE_METADATA.json: public references, inspected locations, hashes, retrieval and inspection status.
- verify.py and CONTROL_RESULTS.json: deterministic exact controls, using only Python's standard library.
- LIMITATIONS.md: scope and unresolved steps.
- REPRODUCTION.json: exact replay command and expected checks.
- MANIFEST.json: SHA-256 and byte counts for every other safe packet file.

Run `python3 verify.py` from this directory. Its stdout must agree byte-for-byte with CONTROL_RESULTS.json. It does not need the private research inputs. The mathematical proofs require human review independently of these controls. No novelty or general-solution claim is made.
