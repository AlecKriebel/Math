# Priority search log

Audit date: 2026-10-06, America/Los_Angeles. No external individuals contacted. Independent read-only search; source clone preserved.

## Sources inspected

- Pinned upstream commit adc7f1241b42e322a6451854ab7e4b4c146bf78a; README, CONTENTS, lean/docs/047.md, family 047 introduction/reference list and README, and companion Abhyankar–Sathaye manuscript of September 24, 2026.
- Nagamine arXiv:1811.04153v2 full PDF and HTML, especially Question 1.3, Proposition 1.4 and its entire proof, Theorem 2.5. Version 1 PDF separately checked for earliest appearance; it does **not** contain Proposition 1.4.
- Chakraborty, Dasgupta, Dutta and Gupta arXiv:1910.11023v1 full PDF and relevant HTML sections: original Costa Section 4 questions, Theorem 5.8, Remark 5.12, Questions 3.1–3.2.
- Chakraborty–Pal arXiv:2504.14382v2 full introduction and Section 5 final paragraph, Theorem 6.9, Corollary 6.11 and boundaries in Section 7; arXiv version-history page. Current title differs from version 1.
- Epstein–Nguyen arXiv:1301.3967v2 introduction, especially the exact polynomial-extension example and Costa/cancellation relationship, and arXiv version history.
- Gaifullin–Petrov arXiv:2607.13593v1 abstract and full introduction/concluding statements; no Costa/retract statement and no affine-space cancellation counterexample located. This is a current related primary source in family 047's bibliography, not a duplication of the target.
- Costa DOI Crossref metadata. Original full-text access attempted via DOI, ScienceDirect PII, PDF endpoint and Elsevier text-mining endpoint; all unsuccessful (403/400 or inaccessible). Question wording and Section 4 placement therefore rely on primary literature reproducing the original question, not an unperformed original full-text read.
- GitHub API repository metadata, entire available commit list and releases list; read-only `git ls-remote` of remote main. Only pinned initial commit available; no releases and no newer correction commit seen. `has_issues=false`; empty issues page is not evidence of mathematical correctness.

## Searches performed

Search engine queries included (verbatim):

- `Costa retracts polynomial rings 1977 D L Costa J Algebra 44`
- `"Costa" "retract" "2026" polynomial rings`
- `"An explicit failure of complex affine-space cancellation"`
- `"Retracts of polynomial rings" Costa 1977 DOI`
- `"Costa" "retract" "characteristic zero" "2026"`
- `"retract" "cancellation" "OpenAI" math`
- `"complex affine-space cancellation" OpenAI`
- `"Retracts of polynomial rings" "Costa" filetype:pdf`
- `"Monomial and binomial retracts" arxiv`
- `"Costa" "retract" "counterexample" "characteristic zero"`
- `site:arxiv.org "retracts of polynomial rings"`
- `"Douglas L" "Costa" "Retracts" pdf`
- `"Retracts of polynomial rings" "question" "Costa" 1977 3.5`
- `"Costa" "retract" "counterexample" complex`
- `"retract" "five variables" polynomial complex`
- `"retract" "characteristic-zero" "counterexample" polynomial rings`
- `"Costa" "polynomial" "retract" "October" "2026"`
- `"OpenAI" "Costa" retract rings`
- `"openai/math" "cancellation" error correction`

The whole upstream corpus was searched using exact word retract/retraction/Costa over all available manuscript TeX, Markdown and BibTeX sources (497 matches across 84 manuscript directories, none a relevant Costa counterexample). All upstream textual sources plus Lean were additionally searched for polynomial-retract adjacency, Costa-question adjacency, and idempotent-endomorphism adjacency; no exact target duplicate was found. Logs are `corpus_retract_matches.txt` and `corpus_exact_matches.txt`. This is a source-corpus search, not an assertion of independently reading every line of every manuscript or searching inaccessible material. The adjacent noncoordinate-polynomial paper was read because its ambient-four-dimensional statement is close in subject but concerns a polynomial image algebra, so does not settle Costa's question.

## Interpretation

No exact already stated characteristic-zero Costa counterexample in ambient dimension five was located in these searches. The target is nevertheless an immediate deductive consequence of the public upstream cancellation theorem plus a known elementary reduction. Failed keyword searches do not prove novelty. No claim to first priority or an independent cancellation breakthrough is supported.
