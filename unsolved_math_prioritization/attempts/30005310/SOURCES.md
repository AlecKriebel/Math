# Primary-source and scope audit

## Original question

Numeric30005310, codeOWR-11695865-009, rank232. The full pinned dataset record is saved as source_record.json. No exact-key upstream research_results entry was found; prior_imported_report.json is explicitly null, not an inferred earlier attempt.

The complete source is [Oberwolfach Report55/2022](https://ems.press/content/serial-article-files/46992), DOI10.4171/OWR/2022/55, printedpp3121-3170. Roser Homs's contribution, joint with Olga Kuznetsova, is printedpp3146-3149, PDFpages26-29. The formal colored-model definition is onp3147; the sufficient-statistic projection, elimination ideal, existence criterion and Proposition3 are onp3148; Conjecture4 is onp3149. The latter two pages were rendered and visually inspected.

The definition allows arbitrary partitions of vertices and of edges, including singleton classes. It imposes zero concentration entries on nonedges and equality of concentration entries within each color class. The candidate's base graph is ordinary K4,4 through singleton colors. Its stronger variant ties the concentration diagonals of vertices1,2, with all other vertices and all edges individually colored. Both are connected and contain all16 cross edges.

The report's ideal uses all(r+1)-minors of the full symmetric matrix and linear equations for color-class sums. It is not a PSD ideal or merely a principal-minor ideal. The MLE criterion is positive-definite completion with identical sufficient statistics. WMLT is positive probability and MLT probability one. Our open-data-box argument establishes the former, not just one exceptional data point.

## Crucial interpretation boundary

The supplied cleaned question retains the numerical threshold conclusions of Proposition3. The counterexample disproves those literal conclusions: at n=3 it has WMLT=2. It is actually in the second bullet's intersection hypothesis. Thus the proof does not claim a third Boolean alternative to “strict SOS separator versus positive-definite intersection.” A repaired certificate-only conjecture is left open here.

The report illustrates the proposition using colored4-cycles, and the paragraph preceding Conjecture4 discusses those examples. Its displayed Proposition3 and general model definition do not restrict G to four vertices. If a4-cycle-only restriction was intended but omitted, the current eight-vertex example does not settle that separately restricted problem. This limitation is explicit in the proof and must remain in any PR.

## Sample rank and known thresholds

The report indexes the elimination ideal by sample-covariance rank. Its cited [Bernstein-Dewar-Gortler-Nixon-Sitharam-Theran paper](https://arxiv.org/abs/2108.02185), introductionpp1-2, explicitly defines the graph model using N(0,Sigma) and iid observations. The candidate uses that zero-mean/scatter-rank convention. The positive1/r covariance normalization rescales every completion and does not change existence. Estimating an unknown mean first would create a different observation-count shift and is not silently substituted.

[Blekherman-Sinn, arXiv1703.07849v2](https://arxiv.org/abs/1703.07849v2), Theorem2.7, gives the exact complete-bipartite MLT formula. The entire author PDF is available; the theorem and its surrounding definition were read. The cited published result is *Maximum likelihood threshold and generic completion rank of graphs*, Discrete & Computational Geometry61(2019),303-324, DOI10.1007/s00454-018-9990-3, also identified in the primary rigidity paper's references. The DOI page was unavailable to the web reader, so no claim of reading its publisher PDF is made.

For K4,4, the theorem gives MLT4; Theorem2.1 gives generic completion rank4. The current proof independently establishes the needed elimination-ideal conditions and WMLT2, so the negative answer does not depend on accepting the exact MLT value. The connected tied-diagonal variant's exact MLT is not asserted.

The displayed threshold formulas in the downloaded rigidity preprint contain apparent adjacent inconsistencies in its running bipartite example. They are not used for the numeric MLT claim; the exact Blekherman-Sinn theorem is used directly.

## Prior-attempt gate, credit and limits

Live all-state target-ID PR search, target branch search and default-branch attempt-path commit history were empty. related_target_groups.json contains no targetID. The queue row was queued0/5. No prior campaign attempt was located, and no historical counter is reset.

This is a literal source correction and a consequence of established Gaussian completion facts. No historical novelty or new statistical discovery is claimed. No outside researcher has been contacted. Full source PDFs and renderings are local reading copies outside the public attempt package. Verification code is locally authored and uses preinstalled SymPy only; no downloaded executable was run.
