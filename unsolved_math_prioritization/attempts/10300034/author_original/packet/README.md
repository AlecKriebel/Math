# Calegari Question 9.1: source-free author packet

Problem 10300034 / AMR-102-0034, rank 1005. **Unsolved, 5/5 approach families.**
Independent mathematical audit is pending. This packet does not prove or
refute universal transverse surgery and makes no novelty claim.

Read PROOF.md for all hypotheses, proofs, failed steps and classical credit.
APPROACH_LEDGER.json records the five distinct mathematical routes. The
source audit and pins identify the inspected scholarly material without
including source documents or text. CORPUS_BINDINGS.json contains only
public verification metadata; the private inputs are not in the packet.

The strongest partial is the surgery quotient
pi1(M) -> pi1(N)/normal(L), giving b1(M)>=b1(N)-rank span[L]. A fixed target
would require unboundedly many components on Sigma_g x S1. Explicit positive
sections can normally generate the whole product group, so this obstruction
can vanish. Additional results identify the original-fibre-class extension
slopes, disprove a naive contact-to-foliation transversality transfer, and
construct transverse links from a geometrically realized recurrent graph.

## Verification and trust

Authenticate the bootstrap SHA-256 and manifest SHA-256 from an independent
trusted receipt before executing anything. A substituted program cannot
authenticate itself. From the author root run:

    python3 -I -S -B bootstrap.py
    python3 -I -S -B -O bootstrap.py
    python3 -I -S -B -OO bootstrap.py

The bootstrap pins the manifest, requires the exact regular-file inventory,
and authenticates every payload byte before executing verify.py under
isolated Python. It compares output against the authenticated diagnostics.
It does not write into the packet, and works from a read-only copy. The
trusted interpreter, standard library, operating system, filesystem stability,
and externally supplied trust anchors are assumptions.

The separately invoked packet/test_bootstrap.py tests fail-closed corruption,
malformed JSON, hostile path, and read-only cases in all three modes. Its
bytes are authenticated by the bootstrap before it should be executed.
packet/verify_corpus.py optionally replays the metadata binding against the
two complete external input files. Use --help for its explicit arguments.

Finite rational and graph controls check calculations and algorithms, not
3-manifold topology, infinite quantifiers, literature completeness, or
mathematical proof truth. Source metadata is historical inspection evidence;
hashes do not certify the contents of a theorem. No source PDF, extraction,
dataset content, private coordination, remote write, PR, or publication is
included or claimed.
