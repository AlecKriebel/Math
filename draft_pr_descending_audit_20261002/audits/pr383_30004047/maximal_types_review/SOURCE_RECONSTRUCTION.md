# Source-first reconstruction

Recorded 2026-10-03 02:23 UTC, before candidate proofs or prior verdicts were read.

OWR 2019/1, DOI 10.4171/OWR/2019/1, Paul Seymour's contribution *Concatenating bipartite graphs* (joint with Chudnovsky, Scott, Spirkl), printed pp. 46-47, physical PDF pp. 42-43, states the following question. For real x,y in (0,1] and every integer k >= 1 satisfying x+ky>1 and kx+y>=1, does every finite graph with disjoint nonempty sets A,B,C, minimum A-to-B degree x|B| and B-to-C degree y|C| have a c in C reaching at least |A|/k distinct A vertices by two-edge paths? The contribution separately states this result for psi after imposing reverse minimum degrees B-to-A and C-to-B. Those reverse bounds are not hypotheses of the phi question.

The journal version (EJC 29(2), 2022, P2.47, DOI 10.37236/8451), definitions on printed p. 4 and Conjecture 5.1 on printed p. 21, makes A,B,C a tripartition into stable sets and forbids A-C edges; this makes two-edge reach equal distance exactly two. Phi is the universal guaranteed fraction. Conjecture 5.1 uses exactly the strict first and weak second inequalities above. Counts are distinct endpoints, not path counts. Success here requires arbitrary graph sizes, all real parameters, and every integer k; weighted-support or bounded-|A| statements alone cannot establish it.

Primary URLs: https://ems.press/content/serial-article-files/46780 and https://www.combinatorics.org/ojs/index.php/eljc/article/download/v29i2p47/pdf/ . Local source copies and extraction/rendering artifacts are under primary_sources/.

Falsifiable audit checks: preserve one-way degrees and exact endpoint unions under normalization; verify all aggregate masses, positivity/denominators and strictness; distinguish uniform A size from weighted A support; test boundary deletion and size-reduction extrapolations. Counterexamples at equality x+ky=1 do not contradict the stated conjecture.
