# Source and status audit: 30003955

Checked 30 September 2026. The primary source is Dmitri Gekhtman's Problem 12 in [Oberwolfach Report 40/2018](https://publications.mfo.de/bitstream/handle/mfo/3662/OWR_2018_40.pdf?isAllowed=y&sequence=1), printed p. 2528, DOI [10.4171/OWR/2018/40](https://doi.org/10.4171/OWR/2018/40). The full problem paragraph, its regular-cover qualification, and its Teichmuller-theoretic motivation were read; the original page was also inspected visually.

## Exact target

The surfaces are closed surfaces of genera h>g>=2, and the cover is finite and unbranched. The question asks whether some embedded four-holed sphere with essential boundary in the base has disconnected full inverse image of its interior. It then asks the analogous question for a three-holed sphere. The source explicitly invites restricting to regular covers as a subproblem. It does not require the boundary components to be pairwise nonisotopic. In particular the usual four-holed sphere obtained by cutting a genus-two surface along a cut system is within the stated scope.

The source's motivation is a condition sufficient for an induced Teichmuller-space embedding to fail to be a holomorphic retract. It does not claim that the topological condition is necessary. A theorem resolving that analytic motivation would therefore not automatically answer the subsurface question.

## Prior-attempt and duplicate checks

Before proof work, the main-branch row was rank 44, queued, with 0/5 attempts. The pinned full dataset at revision `37e53eabe540fb458758e198be61634bd02ee008` had no matching research-results entry. Searches of the state, historical/reset records, related-target groups, attempt-path tree and commits, all 20 existing all-state PR titles/bodies, and the problem-specific branch reference found no earlier attempt. A full pinned-dataset title/statement search found no duplicate of the exact target.

The public source record is preserved in `source_record.json`, attributed to [ulamai/UnsolvedMath](https://huggingface.co/datasets/ulamai/UnsolvedMath), CC BY 4.0. The public UnsolvedMath problem-page retrieval failed; the pinned record and complete original mathematical statement were available. Shared queue and historical files were not changed by this attempt.

## Related primary literature checked

- [Gekhtman's current research page](https://sites.google.com/site/dmitrigekhtman/research), the institutional [2019 thesis record](https://thesis.caltech.edu/11515/), and [Gekhtman–Greenfield, Isometric submersions of Teichmuller spaces are forgetful](https://arxiv.org/abs/1901.02586). The latter paper's main theorem concerns holomorphic isometric submersions, not the required disconnected inverse image of a planar subsurface. No implication answering the exact topological question was found.
- [Detcherry–Le Fils–Santharoubane, Compatible pants decomposition for SL2(C) representations of surface groups](https://ems.press/content/serial-article-files/48667), particularly the main statement and finite-image section. These results construct pants decompositions with irreducible restrictions in specified target groups. They do not assert intransitivity on the fiber of every finite cover, and an example with connected lifts for one decomposition would not refute an existential statement over all subsurfaces.
- [Funar–Pagotto, Braided surfaces and their characteristic maps](https://arxiv.org/abs/2004.09174), version 2, 20 April 2023, Theorem 1.2. Its exact statement was read and visually checked. For each genus at least two it supplies finite simple characteristic quotients with no essential simple-loop class in the kernel. This prevents a universal extension of the stronger trivial-monodromy construction used in the partial note. It does not rule out proper monodromy images, and hence is not a counterexample to the original regular-cover question.

A related public 2018 discussion about disconnected lifts of nonannular subsurfaces also points toward monodromy and stable-genus arguments. The proofs in this package do not rely on that discussion or on an unverified version of the stable representation theorem.

This was a bounded literature search. No complete resolution of the exact problem was located, and no claim of exhaustive current open status or priority is made. The deductions in `PARTIAL.md` remain explicitly partial and are not presented as a new solution.
