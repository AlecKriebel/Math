# Frozen prior-result audit: fractional coloring

ID 30002271, row 1910. Disposition: already_solved1. This verifies the prior King–Edwards clique-with-pendants construction, not a novel result. No resolution of maximal-clique, outer-subgraph, or local-demand variants is claimed.

Run `python -B validate.py`, `python -B check_exact.py`, `python -B replay_certificates.py`, and `python -B mutation_tests.py`. Repeat with `-O`. Do not permit Python bytecode files inside this exact inventory.

AUDIT.md, check_exact.py, EXACT_CHECKS.json, INDEPENDENT_REVIEW.md, INDEPENDENT_CHECKS.json, and VERIFICATION.json are byte-preserved originals; ORIGINAL_MANIFEST.json is their original manifest. No assert hardening was necessary. New replay evidence contains every graph edge, primal class and weight, dual vertex weight, maximal independent set, local value, neighborhood average, and local-demand finite palette for k=1 through 12. The helper is compared to brute-force enumeration on 1,099 graphs.

The manifest hashes every payload but not itself; the external receipt binds manifest and archive bytes. Validation inventories all entries including the manifest using lstat before reading any content, rejects nonregular and hardlinked entries, and strictly rejects Boolean/float integer fields. This is an offline integrity check, not protection from concurrent hostile filesystem mutation.

Source metadata is an allowlisted projection of recorded public bibliographic and retrieved-byte metadata. No copied source text, datasets, private paths, or coordination records are included. No sockets are opened, repository publication performed, or queue edited. Mutation tests operate only on disposable copies and simulate the socket file type.
