# Acceptance of partial results

Problem 3900016 / AMR-038-0016; reviewed 8 October 2026 UTC.

Disposition: accepted partial results, exhausted 5/5. Full target unresolved. No mathematical correction patch is required.

## Accepted conclusions

- The compatible distinct-area triangle-packing construction proves t(n) >= ceil((sqrt(16n-23)-3)/8), asymptotic to sqrt(n)/2.
- A maximum vertex triangle has strict smaller-area caps when there are at least five extreme polygon vertices. The cap recursion supplies the separately stated logarithmic lower bound.
- t(3)=t(4)=1 and t(5)=t(6)=2, with exact rational/integer witnesses and all their triangulations checked. The corresponding stated bounded-lattice small cases follow under the report's explicit m ranges.
- Coplanar integer vertices in [0,m]^3 with primitive integer normal u have triangle areas |k| ||u||_2/2. Coordinate projection, the bound |k| <= floor(m^2/max|u_j|), and the total-mass inequality provide spectrum constraints. A primitive plane normal does not imply every unit k is attained; the independent audit includes a sublattice-index-two example.

The accepted domain is distinct extreme polygon vertices and vertex-only noncrossing triangulations. An alternative weak-boundary-point convention would require separate analysis. No sharp general t(n), sharp t_L(n,m), forced triple-repetition decision, novelty, best-known bound, or comprehensive current-openness certification is accepted.

## Evidence and preservation

The accepted author report has SHA-256 65c34cdf480507a3ac514364df7091eccc2e47c579f9cb9ddcbc537d3eb1f3ed (15,426 bytes). The independent audit is audit/authored/AUDIT.md, SHA-256 3d809a9d24c2e59641b8b9d4ea1e1432e98bac9648e9a534716359a29ec374ca (15,941 bytes). The original eight-file author packet and complete accepted source-free audit packet are unchanged. The separate audit acceptance supersedes the author's historical pending-audit field without rewriting frozen evidence.

The independent audit checks the proofs and performs diagonal-subset enumeration distinct from the author's Catalan and ear-deletion recursions. It checks every P5/P6 triangulation and all twenty P6 triples. Full normal/-O/-OO expected outputs are preserved, including seven semantic mutations per mode and eight independent negative controls per mode.

The publication wrapper reproduces each full stdout/stderr byte sequence and the entire stored fresh REPLAY_RESULTS.json object with exact JSON types. Genuine real/effective UID 1000, read-only modes, actual denied create/write-open attempts, unchanged input hashes, external-output success, internal-output rejection, and rejection of a writable input tree are checked. The externally fixed bootstrap binds the entire delivered directory, including outer acceptance and receipts; its trusted hash is recorded outside the candidate directory to avoid circular self-certification.

Fresh source/corpus/PDF verification is NOT_RUN. Earlier public-source checks are retained only as dated verification metadata. The packet contains neither copied source documents nor corpus bodies. This is an independent agent audit and reproducible finite checking, not proof-assistant formalization or conventional human peer review.
