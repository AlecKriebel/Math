# Vertex-distribution-free graph testing: accepted complete negative comparison

Problem 30004127 / OWR-16931-012.

The fixed property P consists of K4-free graphs that become 3-colorable after
deletion of at most one vertex. It is hereditary, extendable and edge-monotone.
The complete proof gives:

- A one-sided classical canonical tester with O(epsilon^-6 log(1/epsilon)) vertex samples on every finite input size without knowing n; full induced adjacency cost is quadratic, and no polynomial runtime is claimed.
- An exp(Omega(log^2(1/epsilon))) worst-case total sample-plus-adjacency lower bound for adaptive two-sided VDF testers along an explicit positive-rational sequence.
- A separate vertex-sample lower bound when queries are restricted to sampled labels, even with free induced adjacency queries.
- A direct doubled-wheel proof that P is not blowup-avoidable, explaining why the known restricted positive comparison does not apply.

The theorem does not claim a sample-only lower bound with unlimited free
arbitrary named adjacency queries. It refutes any universal polynomial
comparison of classical and VDF complexity, including fixed constant proximity
rescaling. The universal proof needs no omitted computation or dataset.

## Files

- [PROOF.md](PROOF.md): complete theorem, construction and proof
- [MATHEMATICAL_AUDIT.md](MATHEMATICAL_AUDIT.md): full substantive independent audit and historical finite-check results
- [ACCEPTANCE.json](ACCEPTANCE.json): complete acceptance, exact scope and distributed proof/audit pins
- [STATUS.json](STATUS.json): accepted negative answer and limitations
- [SOURCE_REVIEW.md](SOURCE_REVIEW.md): attribution, inspection coverage and source boundaries
- [SOURCE_METADATA.json](SOURCE_METADATA.json): public titles/URLs, recorded PDF hashes/sizes and historical retrieval/inspection metadata
- [MANIFEST.json](MANIFEST.json): exact eight-file inventory, hashing the other seven members

## Attribution and review limits

The original question is Gishboliner’s joint work with Shapira. Their
hereditary-and-extendable classification and blowup-avoidable comparison are
credited. Earlier Goldreich–Goldwasser–Ron and Alon–Krivelevich colorability
methods, Behrend’s sphere construction and the Ruzsa–Szemerédi arithmetic host
are credited, with every needed argument supplied in full. Goldreich’s model
reductions are contextual. No novelty or priority is claimed.

This AI-assisted manuscript and audit are unrefereed. Acceptance refers to the
accompanying independent mathematical audit; it is not external human peer
review, journal acceptance or proof-assistant certification. Bounded literature
searches do not establish exhaustive current status or novelty.

The full mathematical proof and audit findings are preserved. All edition edits
are editorial, and no required mathematical correction remains. Historical
finite checks are supplementary and do not establish the universal theorem.
Programs, raw outputs, generated certificates, datasets, copied third-party
source documents/text/images and private coordination material are excluded.
Edition preparation rechecked frozen input bytes and publication integrity,
without new source retrieval, source-text inspection, literature search or
rerunning historical mathematical computations. QUEUE.md and unrelated
repository content are unchanged. No merge, release, DOI, journal submission
or external outreach is implied.
