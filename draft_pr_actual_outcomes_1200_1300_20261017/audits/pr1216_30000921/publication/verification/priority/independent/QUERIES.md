# Exact query ledger

All queries executed on 2026-10-17 between the recorded start at 18:21 UTC and this report's freeze. These are bounded discovery queries, not an exhaustive database search. The first three tool responses were displayed but not separately retained in full; some displayed output was truncated. Later raw responses are retained in ignored `sources/`. Search-engine crawl/publication labels were not used as authoritative scholarly dates.

## B01

Receipt: tool response only; raw local copy not retained.

1. `"Which maps preserve universal functions"`
2. `"hypercyclic" "polynomial" "multiplication" Costakis differentiation`
3. `"Common Cesàro hypercyclic vectors"`

## B02

Receipt: tool response only; raw local copy not retained.

4. `"hypercyclic" "polynomial multiples"`
5. `"hypercyclic" "polynomial multiplication"`
6. `"hypercyclic" "preserve" "Costakis" multiplication`

## B03

Receipt: tool response only; raw local copy not retained.

7. `"Costakis" "Which maps" "Question"`
8. `"MacLane" "multiplication" polynomial hypercyclic`
9. `"differentiation" "hypercyclicity preservers"`

## B04

Receipt: `sources/search_exact.json`.

10. `"hypercyclic" "polynomial multiples"`
11. `"hypercyclic" "polynomial multiplication"`
12. `"Which maps preserve universal functions" -site:researchgate.net -site:grafiati.com`

## B05

Receipt: `sources/search_preservers.json`.

13. `"hypercyclicity preserving" operators`
14. `"hypercyclic" "multipliers" "differentiation"`
15. `"hypercyclic" "preservers"`

## B06

Receipt: `sources/search_author_zf.json`.

16. `George Costakis publications hypercyclic universal functions 2025 2026`
17. `"hypercyclic vectors" "preserve" "multiplication" polynomial`
18. `"differentiation" "hypercyclic" "zf"`

## B07

Receipt: `sources/search_coeff1.json`.

19. `"hypercyclic" "zf" differentiation polynomial`
20. `"MacLane" "coefficients" "lower" universal`
21. `"hypercyclic" "coefficient" "prescribed" differentiation`

## B08

Receipt: `sources/search_coeff2.json`.

22. `"On the set of hypercyclic vectors for the differentiation operator"`
23. `"On the growth of D-universal functions"`
24. `"universal functions" "multiplication by a polynomial"`

## B09

Receipt: `sources/search_shkarin2010.json`.

25. `"On the set of hypercyclic vectors for the differentiation operator" pdf`

## B10

Receipt: `sources/search_random.json`.

26. `"Frequent hypercyclicity of random entire functions" pdf`
27. `"hypercyclic" "polynomial" "Gaussian" "multiplication"`
28. `"hypercyclic" "coefficients" "bounded away"`

## B11

Receipt: `sources/search_exact_quantifiers.json`.

29. `"Costakis" "polynomial" "HC(D)"`
30. `"hypercyclic" "pf" "polynomial" "Costakis"`
31. `"universal with respect to derivatives" "polynomial"`
32. `"hypercyclic" "polynomial" "counterexample" "multiplication"`

## B12

Receipt: `sources/search_mult_question5.json`.

33. `"On the universality of multipliers on H(C)"`
34. `"multiplication" "Costakis" "Question 5"`
35. `"preserve hypercyclic" entire functions`

## B13

Receipt: `sources/search_earlier_random.json`.

36. `"Mixing operators and small subsets of the circle" "random entire"`
37. `"hypercyclic" "Gaussian" "n!" "2006"`
38. `"Frequent hypercyclicity" Nikula "multiplication"`

## B14

Receipt: `sources/search_preservation_exact2.json`.

39. `"differentiation" "preserves hypercyclicity" multiplication`
40. `"multiplication" "MacLane-universal" polynomial`
41. `"polynomial" "MacLane universal" "not"`

## B15

Receipt: `sources/search_mult_recent.json`.

42. `"On the universality of multipliers" filetype:pdf`
43. `"Multiplicative structures of hypercyclic functions" -site:researchgate.net -site:zenodo.org -site:github.com`
44. `"hypercyclic" "polynomial" "multiplier" 2024 2025 2026`

## B16

Receipt: `sources/search_citation_exclude.json`.

45. `"Which maps preserve universal functions" -site:mortini.perso.math.cnrs.fr -site:ems.press -site:researchgate.net -site:users.math.uoc.gr -site:github.com -site:zenodo.org -site:math.ucsd.edu`
46. `"Common Cesàro hypercyclic vectors" "polynomial" -site:researchgate.net -site:zenodo.org -site:github.com`
47. `"Nikula" "polynomial" "hypercyclic" multiplication`

## B17

Receipt: `sources/search_bg2006.json`.

48. `"Frequently hypercyclic operators" Bayart Grivaux 2006 pdf`
49. `"MacLane" "Gaussian" "2004" hypercyclic`
50. `"Frequent hypercyclicity of random entire" citations polynomial -site:researchgate.net`

## B18

Receipt: `sources/search_nikula_citing.json`.

51. `"Frequently hypercyclic random vectors" arxiv`
52. `"Rate of Growth of Frequently Hypercyclic Random Functions for Weighted Shifts"`
53. `"On random frequent universality" Mouze Munnier`

## Directed source and citation requests

Opened/read source-specific URLs are documented in SOURCE_LEADS.md and SOURCE_RECEIPTS.json. Additional discovery/metadata requests included:

- Crossref DOI endpoint `/works/10.4171%2FOWR%2F2008%2F06`.
- OpenAlex DOI lookups for `10.7900/jot.2017sep27.2162` and `10.1007/s11785-013-0328-0`.
- OpenAlex `/works?filter=cites:W2766234775&per-page=50&select=id,doi,title,publication_date` (one result returned).
- OpenAlex same filter for `W2042512829` (eight results returned).
- Costakis home page, linked CV, and linked `publicat.html`; the latter yielded an image-only in-progress page.
- Versioned arXiv PDFs `1209.6209v1`, `1209.0984v1`, `1112.1289v1`.
- Current author manuscript `matheron.perso.math.cnrs.fr/recherche_fichiers/Mixing.pdf` via indexed source excerpts; its later explicit Nikula remark was not assigned a 2011 date.
- DOI resolver web opens for the original three references failed, while direct publisher PDFs succeeded; Crossref separately authenticated the 2008 DOI.
- Attempted direct AMS Bayart–Grivaux 2006 PDF returned 403; no body inspection claimed.

Raw `open_*.json`, `find_*.json`, metadata JSON, and downloaded files under ignored sources record the responses actually retained. Requests did not contact any person, initiate outreach, or edit an external service.

