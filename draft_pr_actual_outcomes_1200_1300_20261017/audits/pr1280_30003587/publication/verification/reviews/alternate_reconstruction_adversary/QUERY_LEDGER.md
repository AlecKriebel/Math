# Literal query and retrieval ledger

No general web search query was issued. This is the complete literal primary-source web request ledger for the initial seal. These entries describe source retrieval/inspection only; they are not outside communication with an individual.

## Browser-provider operations, in order

1. `open`:
   - `https://ems.press/content/serial-article-files/46706`
   - `https://arxiv.org/pdf/1708.08258v3`
   - `https://journals.msp.org/mscand/article/download/221/220`
   - `https://arxiv.org/pdf/1101.4210v3`
2. `find`:
   - EMS PDF, literal pattern `Question 1`
   - arXiv 1708.08258v3, literal pattern `Corollary 2.8`
   - arXiv 1708.08258v3, literal pattern `Definition 2.5`
   - arXiv 1101.4210v3, literal pattern `maximal abelian`
3. `open`: `https://journals.msp.org/mscand/article/view/221`
4. `open`: `https://documents.uow.edu.au/~dpask/index_files/papers/ckaodg.pdf`
5. `find` on that KPR PDF, literal patterns `3.7 Theorem`, `hereditary`, and `saturated`.

The browser provider reported an internal parsing error for the final publisher PDF. The local fresh HTTP retrieval below succeeded. The final landing page was also inspected to confirm article identity.

## Independent HTTP acquisitions into private `_local/`

The following literal URLs were fetched through Python standard-library urllib, with actual timestamps, final URLs, response status, byte counts and SHA256 recorded in `SOURCE_PROVENANCE.json`:

- `https://ems.press/content/serial-article-files/46706`
- `https://arxiv.org/pdf/1708.08258v3`
- `https://journals.msp.org/mscand/article/download/221/220`
- `https://arxiv.org/pdf/1101.4210v3`
- `https://documents.uow.edu.au/~dpask/index_files/papers/ckaodg.pdf`

Relevant text extraction and local page renders stayed within `_local/`. No provider extract or third-party PDF is an output-manifest member.

## Local candidate scope

- Read assigned report, output manifest and source provenance under `reviews/corner_cohomology_adversary/`.
- Verified every assigned manifest member by byte count and hash without reading the other members as mathematical evidence.
- Read `submitted/PROOF.md` for the original statement and proof comparison.
- The initial inventory exposed filenames of other reviews and root outputs; their contents were not opened.
- Read PDF skill instructions and obtained bundled-runtime locations.
- No other report, current-edition proof, original-acceptance file, root crossfeedback, or subagent output was read before initial seal.

One attempted use of the system `python` launcher failed because of an unaccepted Xcode license. No source retrieval or file write occurred in that failed command. All subsequent Python work used the bundled runtime. An attempted optional PyMuPDF import failed because the module was unavailable; Poppler rendering succeeded. These environment issues did not alter the mathematical checks.
