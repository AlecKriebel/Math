# Fresh search record

Searches performed 2026-10-07 UTC, during the independent package-review-03 priority subreview. Initial findings were saved before consulting existing priority conclusions. No earlier search log was read.

## Queries

1. `"weighted perfect matchings" "unweighted" rational binary reduction`
2. `"hafnian" "FPRAS" "rational"`
3. `"Approximating Holant problems by winding" "Lemma 27"`
4. `"A Fully Polynomial Randomized Approximation Scheme for Perfect Matchings in General Graphs"`
5. `site:openai.com "math" "October 6, 2026"`
6. `site:github.com/openai/math "Initial commit"`
7. `site:arxiv.org hafnian "FPRAS"`
8. `site:arxiv.org "weighted" "McQuillan" perfect matching`
9. `"hafnian" "fully polynomial" 2026` (requested arXiv domain restriction)
10. `"hafnians" "rational" "FPRAS"` (requested arXiv/ECCC/GitHub domain restriction)
11. `"weighted perfect matchings" "FPRAS" general` (requested arXiv/Dagstuhl/ECCC domain restriction)
12. `"Binary rational hafnians"`

The search engine returned some unrelated/out-of-domain hits even on requested domain filters. I did not use such hits as evidence. Positive useful leads were the public upstream release, McQuillan's already-known equivalence, restricted dense hafnian results, bipartite permanent results, and older general-graph estimators that do not claim an unrestricted FPRAS. No exact standalone duplicate of the note's full constructive proof and finite-check package was found. This is a bounded search outcome, not proof of novelty or nonexistence.

## Primary records freshly opened

- [McQuillan arXiv record](https://arxiv.org/abs/1301.2880): only v1, 14 Jan 2013 08:02:59 UTC.
- [Dell et al. arXiv record](https://arxiv.org/abs/1206.1775): only v1, 8 Jun 2012 14:29:52 UTC; journal citation ACM Trans. Algorithms 10(4), article 21 (2014).
- [ECCC TR10-078 record](https://eccc.weizmann.ac.il/report/2010/078/): original three-author report dated 27 Apr 2010, displayed publication 23:50; expanded five-author revision 8 Jun 2012 17:51. The site does not display a timezone for those times.
- [RSZ arXiv record](https://arxiv.org/abs/1409.3905): v1 13 Sep 2014 03:13:06 UTC; inspected v2 2 Sep 2016 12:55:45 UTC.
- [Barvinok arXiv record](https://arxiv.org/abs/1601.07518): v1 27 Jan 2016 19:46:45 UTC; inspected v5 13 Jan 2017 15:01:10 UTC.
- [Yi arXiv record](https://arxiv.org/abs/2609.04079): only v1, 3 Sep 2026 16:47:58 UTC.
- [OpenAI's official release announcement](https://openai.com/index/sharing-ai-progress-in-mathematics/): dated 6 Oct 2026, links public math repository. This is stronger public-release evidence than the papers' internal 23 Sep date.
- [Pinned initial GitHub commit](https://github.com/openai/math/commit/adc7f1241b42e322a6451854ab7e4b4c146bf78a): initial commit, zero parents. The web-rendered commit page did not show a usable timestamp. Saved project API metadata gives 2026-10-06T21:58:50Z author/committer time; commit times by themselves do not establish first public availability.

## Freshness / failure records

- A read-only remote-head query returned `adc7f1241b42e322a6451854ab7e4b4c146bf78a` for `refs/heads/main`, matching both the local read-only upstream clone and cited pin. No source correction was discovered at current remote main.
- Fresh unauthenticated GitHub commit API retrieval was refused with HTTP 403 rate-limit exceeded. No newly fetched commit JSON was saved. Existing saved API metadata was inspected and its limited evidential role is disclosed.
- The GitHub commit-history URL failed through the web tool. The current-head query and official dated announcement remained available, so the public date conclusion does not depend on that failed retrieval.
