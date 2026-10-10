# Connected limit sets in arbitrary hyperbolic spaces

**6200083 / AMR-061-0083. Status: unsolved. Five substantive approaches.**

This is an unrefereed research checkpoint, not a solution or a claim of new
priority. The target is local connectedness of a connected orbit limit set for
a finitely generated discrete isometry group of a Gromov-hyperbolic space.

The strongest result recorded here is a rigorous obstruction to two proposed
general proof routes: there are proper isometric actions of closed surface
groups on locally finite hyperbolic graphs with connected limit set for which
no equivariant Cannon--Thurston boundary map exists and the restricted boundary
action is not geometrically finite. This follows from Matsuda--Oguni's existing
embedding theorem and the elementary connected-tail lemma proved here. It is
not a counterexample to local connectedness.

Known affirmative cases are distinguished carefully: Mj's theorem applies to
Kleinian groups acting on hyperbolic 3-space, and Dasgupta--Hruska's theorem to
connected Bowditch boundaries. Neither identification is an assumption of the
full target.

- `analysis.md`: definitions, five approaches, proofs and exact remaining gaps
- `source_map.md`: primary-source identities, versions and inspection scope
- `research_log.md`: dated author checkpoint history
- `result.json`: machine-readable disposition
- `verification_metadata.json`: public provenance and source hashes
- `verify.py` and `controls.json`: reproducible finite controls

Run `python3 verify.py` from this directory. It recomputes its output in memory
and compares it with `controls.json`; it does not download or publish anything.
These finite checks do not verify the infinite topology or the cited theorems.
The latter require the written proofs and primary-source inspection.

No source PDFs, source full text, dataset records, or private coordination files
are included. No merge, release or DOI is requested.
