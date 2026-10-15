# Fresh source bindings

First retrieval/read: 2026-10-03 07:40:57 UTC. Candidate, author verifier, old audit, root and sibling results had not been read.

- Exact OWR URL: https://ems.press/content/serial-article-files/46961 . Fresh download SHA256 `b94a5ab624e47ddb3db11370099db7ef4bf30acfc2f0993d5c365c2795ff6d79`. Visually inspected PDF pages 63 and 64, printed pp.1227-1228. Mubayi Problem 10 asks for the asymptotic maximum number of induced C4 at prescribed density. Conjecture 11 concerns density >1/2, with triangle-density construction; its cited theorem-number parenthesis is printed as Theorem 1.6, while the fetched LMR paper's matching result is Theorem 1.18.
- Exact LMR URL: https://homepages.math.uic.edu/~mubayi/papers/XizhiReiherInduced.pdf . Fresh download SHA256 `f9b7951b9926ffba50a886226fbe0ab4715cfdccffaf5c92e00f8eee783a270c`. Read definitions at pp.1-2, Construction 1.9 at pp.5-6 and Section 1.6 at p.10; visually inspected p.10. The induced density counts vertex subsets divided by binomial(n,4), rather than a fixed labeled embedding integral. Theorem 1.16 gives I(C4,p)=3p^2/2 on [0,1/2]. Conjecture 1.17 concerns all p in [1/2,1]; Theorem 1.18 gives upper bound 3p(1-p)^2, tight at 1-1/k.

These are actual fresh primary-source bindings, not source-free controls. The later audit will not infer novelty or current global status from this bounded reading.

Private raw PDFs, extraction, renders and copies are confined to `tmp/`, verified ignored by `git check-ignore -v` against the owning audit-root rule `**/tmp/`. No raw private artifact belongs in the public manifest.

## Retrieval/render imperfections preserved

2026-10-03: web screenshot for OWR PDF page index 63 returned Internal Error; local Poppler rendering of both relevant pages succeeded and was visually inspected. Poppler extraction/render reported unknown marked-content annotations for the OWR PDF; rendered target formulas and page headings were legible. No formula was adopted solely from garbled extraction. The fresh download hashes bind the actual bytes.

## Later scope-only fresh source

2026-10-03 07:49:42 UTC fresh open/read; bytes downloaded by 07:50:43 UTC; rendered pp.2,4 visually inspected after download. Exact URL https://homepages.math.uic.edu/~mubayi/papers/Semi_Inducibility.pdf , SHA256 `e178ea4009a84fbe6a3da2959ee1ccead2fe598f19b490f4755c0b7140bc60f7`. Read definitions, Theorem1.3 and Question1. The PDF is dated January8,2026. Its alternating AC4 event specifies two edges and two nonedges with two pairs free, and uses labeled-injection normalization. This scoped primary reading gives no full-resolution or novelty certificate for the induced-C4 target.
