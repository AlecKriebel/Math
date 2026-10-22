# Compact inventory review

Focused review complete (100% for this change; no overall sweep completion
claim). **No material safety or coverage regression was found.** The compact
refresh is acceptable for the reviewed versions:

- `collect_rest_inventory.py`: `9b9247380f5ff99e512ecafda0d1177ede6578902c079ae4dd1886511bf05c37`
- `sweep_io.py`: `23f840ba1c7318d7fe3bec8f06beb868e4fbfdbb4d9db861f5323f5a8f130697`

Seven small offline collector fixtures verify plain and gzip success, rejection
of a previously known larger maximum, empty newest response, independent-count
mismatch, duplicate PR, and unsafe raw-directory symlink. Every rejected run
preserves its prior canonical inventory. Both formats yield identical decoded
page bytes, identical normalized PR rows and counts, and an empty terminal page.
Encoded and decoded SHA-256 values verify for every page, including that terminal
page. REST and GraphQL calls explicitly pin `github.com`.

The new `atomic_json` serialization matches the prior UTF-8 JSON bytes, including
Unicode, escapes, indentation, and final newline. Injected partial-write ENOSPC
and replacement failures preserve the old complete file and remove temporary
files. UUID page naming, raw containment, boundary/count/gap checks, and maximum
regression protection remain intact. Compression does not alter classification
or the collected PR sequence.

The compressed receipts preserve the exact JSON serialization of the decoded API
response, as the old plain receipts did; they do not newly claim to preserve the
original HTTP wire whitespace. Readers of manifest pages must honor `encoding`
and decompress gzip before checking `decoded_json_sha256` or parsing JSON. No
active non-review source in this program was found to parse raw inventory pages
directly; the normalized canonical inventory remains ordinary JSON.

Atomic replacement still requires temporary space for the normalized inventory.
If space runs out, the verified old canonical file is preserved; compression
reduces raw-cache growth but does not remove that requirement.

Reproduction: `python3 reviews/inventory_adversary_02/compact_inventory_review/check_small_fixtures.py`.
`CHECKS.json` records results and source hashes. All allocations are tiny local
fixtures under this review folder. No live service call, production inventory
write, external mutation, credential inspection, or skill generation occurred.
