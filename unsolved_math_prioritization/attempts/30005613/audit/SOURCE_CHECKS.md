# Independent source and identity checks

Checked 5 October 2026. These are bounded provenance checks; they do not
replace the mathematical audit.

## Exact identity and full-corpus integrity

The target is ID 30005613, code OWR-14297736-021, rank 800. The target
numeric ID is unique in both full catalog and full problems datasets, and
the problem code is unique in the latter. The UTF-8 statement has 198
bytes and SHA-256
783db58de5f1183fa9abd1cbacee659b6029b8d4ab61dd04b0fb47fb986d9ea2.
This matches the descriptor. No source statement is reproduced here.

The full catalog and problems datasets each contain 15,458 records. The
full research-results mapping contains 6,701 top-level entries and has no
entry at the target's problem-code key. Using an empty matched report,
the repository's review-hash algorithm independently gives
6e61514d4909027d8a16bfdf209631bea89c9bee55339e5091c5f485cb756a69,
matching the descriptor. The algorithm was checked by reading, without
executing or modifying, the repository's queue.py:
https://github.com/AlecKriebel/Math/blob/main/unsolved_math_prioritization/queue.py .

The three dataset byte counts and hashes were independently recomputed
over the complete local files. They all match the frozen author metadata;
verification.json records them. Raw datasets and extracted records are
excluded from this package.

The live catalog URL https://www.unsolvedmath.com/problems/30005613 was
tried during this audit and the web reader returned a retrieval error.
This audit does not claim to have read that live page. The author's
separate HTTP 403 observation was not independently rerun.

## Primary sources

1. Geometric Spectral Theory, Oberwolfach Reports 36/2023, relevant printed
   pages 2077–2078. Official DOI: https://doi.org/10.4171/OWR/2023/36 .
   Official PDF: https://ems.press/content/serial-article-files/47475 .
   The public PDF endpoint was read anew. The two relevant pages of the
   hash-checked local copy were visually inspected. The target is the
   Dirichlet operator on a connected quasi-conical open set; the nearby
   bounded Neumann comparison does not alter that target.

2. D. Krejcirik and V. Lotoreichik, Quasi-conical domains with embedded
   eigenvalues, Bulletin of the London Mathematical Society 56 (2024),
   2969–2981, https://doi.org/10.1112/blms.13113 . Version inspected:
   https://arxiv.org/abs/2205.08172v2 and
   https://arxiv.org/pdf/2205.08172v2 . The abstract and parsed PDF were
   retrieved anew. The version is dated 20 May 2024, with accepted-author
   status and journal reference on arXiv. Propositions 2.2–2.3 and the
   shrinking-window step have the needed boundedness and Mosco hypotheses.
   Section 3 leaves successive cube widths free. Local PDF pages 3, 4,
   5, and 9 were visually inspected; the last retains the unresolved
   singular-continuous question. The independent analytic addendum checks
   the needed window lemma directly, including d=2.

3. D. Krejcirik, Spectral geometry: old questions and new answers,
   https://arxiv.org/abs/2609.28602v1 and
   https://arxiv.org/pdf/2609.28602v1 . The abstract and parsed PDF were
   retrieved anew. The submission date is 23 September 2026. The abstract
   reports revision at Annales de la Faculte des Sciences de Toulouse;
   acceptance is not claimed. Local PDF page 16 was visually inspected:
   its Open Problem 1 is still the singular-continuous question for this
   construction. The preceding theorem is numbered 2.9 in the PDF.

The inspected PDF byte counts and hashes match the frozen metadata. They
refer to the local source copies that were inspected, not to a new binary
download made during this audit. The web PDF screenshot tool failed for
two requested 2024-paper pages with a cache error; the corresponding local
PDF pages were rendered and inspected successfully. None of those source
files or renderings is included in the safe archive.

Three fresh public searches combined “quasi-conical” with “pure point,”
“singular continuous,” and “finite-rank.” No later primary resolution was
located in those bounded results. Direct inspection of the September 2026
primary survey is stronger evidence of the stated recent open status;
neither observation establishes historical priority or exhaustiveness.

## Fresh read-only repository checks

Repository: https://github.com/AlecKriebel/Math .

- Exact contents lookup for
  unsolved_math_prioritization/attempts/30005613 returned 404.
- The actual attempts directory lists 63 entries and no target directory.
  Its directory-tree SHA is c6b68b279db013a0511bfd9a3f3aa2cc2673dc5e.
- All-state PR searches for 30005613, quasi-conical, quasiconical, and
  “Dense Pure Point” returned no matching PRs.
- The exact-ID branch search returned no branch. The quasi topic search
  returned one unrelated quasiconformal branch, and its next page was
  empty with no remaining cursor.
- Exact-ID commit search returned no match. Default-branch code search
  also returned no match; because the direct queue read does contain the
  target ID, this negative code-search result is explicitly non-exhaustive.
- Direct QUEUE.md inspection shows rank 800, queued, 0/5, and blank
  findings. This is queue metadata, not a mathematical attempt.
- Direct state.json and RESEARCH_LOG.md reads have no target-ID or
  quasi-conical/quasiconical match. The state JSON was parsed successfully
  and has no target key.

The result is “no matching actual prior mathematical attempt located in
these bounded checks.” It does not mean that every repository branch,
private draft, deleted artifact, or external mathematical source was
exhaustively searched. The audit made no remote changes.
