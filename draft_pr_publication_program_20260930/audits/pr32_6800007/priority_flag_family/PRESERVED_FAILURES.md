# Preserved failures

The scholarly retrieval receipts preserve HTTP failures and successful responses with the wrong content format, including their returned bytes in ignored `sources/`. `SOURCE_BYTE_CATALOG.json` also hashes every retained response and derivative. An HTTP status or filename is never treated as proof of PDF possession.

- Direct ResearchGate author-page and PDF routes for the 2020 Falbel–Veloso manuscript returned HTTP 403. The complete public author text was read with the web reader, with this access mechanism recorded separately from PDF identity.
- Springer PDF routes for the 2020 original, 2020 survey and 2025 reductions paper returned HTML previews with HTTP 200; the AMS surgery PDF route similarly returned HTML. Elsevier's published-paper PDF route returned HTTP 403, and its text-mining route HTTP 400 XML. The accepted reductions URL returned HTTP 404. All bodies are retained.
- HAL survey `/document` routes and exact metadata-provided `/file/article.pdf` routes, including this family's versioned v1 attempt, returned bot HTML with HTTP 200. Those failures remain retained. A separate successful root primary retrieval later supplied raw PDF bytes; this family independently verified them and read the full applicable main body. No source-access gap is claimed after that read.
- An attempted local HTML parsing command failed with `ModuleNotFoundError: No module named 'bs4'` (exit 1). A standard-library HTML parser was used instead. This does not recover missing journal main-body text.
- The first run of `priority_binding_controls.py` failed with `KeyError: 'files'` (exit 1) while reading the immutable PR31 manifest. PR31 uses `first_party_artifacts` and `bytes`; PR32 uses `files` and `size`. The reader was corrected to support both actual schemas. No closed file was edited. The corrected run and full preservation result are in `CONTROL_RESULTS.json`.

These failures are limitations or implementation repairs, not evidence of historical openness, novelty, or mathematical correctness.
