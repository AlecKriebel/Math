# Bounded predecessor audit for PR195

Read `REPORT.md` first. `EVIDENCE_MATRIX.json` states the exact inspection scope and gaps for every primary source; `QUERY_LOG.json` records 120 exact search queries in 30 UTC-stamped batches. Direct primary-source opens and local reading are additionally recorded in the report and metadata. The disposition is **bounded audit complete; historical priority unresolved**.

The arrangement construction and logarithmic, generic-section, Hilbert–Burch and triangular methods are prior mathematics. No firstness, current-openness or independent-discovery certificate is supplied. Ilardi2018 remains a material full-text access gap. The fourteen rigid octics are checked; their 63 one-parameter families and related nine-factor generic initial ideals are not exhaustively computed.

Use Python 3.11 or later because the isolation option `-P` was introduced in 3.11. Both programs use only the standard library. From this folder, replay:

```sh
python3 -E -S -B -P compare_known_examples.py --verify KNOWN_EXAMPLE_CERTIFICATES.json
python3 -E -S -B -P octic_scalar_check.py --verify OCTIC_CERTIFICATES.json
```

Both verification commands are deterministic and perform no writes. Without `--verify`, each prints the regenerated certificate to stdout. The first program uses integer polynomials and exact rational elimination for three earlier examples. The second proves characteristic-zero nonvanishing through exact nonzero minors modulo a splitting prime for fourteen rigid octics. Read the generic deductions in `REPORT.md`; a specialization alone is not treated as genericity proof.

`INPUT_PINS.json` authenticates the Root gate and frozen inputs. `SOURCE_RETRIEVAL.json` and `SAFE_METADATA.json` contain URLs, versions, hashes, retrieval outcomes and limitations without redistributing article text. Downloaded PDFs, extracted text, page renders and raw discovery responses stay in ignored `private_sources/` and are excluded.

`SAFE_ALLOWLIST.json` is the exact safe inventory. `HASH_MANIFEST.json` authenticates all ordinary safe files including the allowlist, excluding the manifest itself and the final seal to avoid a hash cycle. `FINAL_SEAL.json` authenticates the manifest and records final disposition. All safe files were set read-only after sealing. Any later revision requires a new seal.

No Git/index/branch/ref operations, remote writes, releases, publication edits or outreach were performed by this audit.
