# Independent review request: central completeness counterexample

Please review SOURCE_SCOPE.md and all of TURN_1.md, bound by TURN_1_MANIFEST.json. Proposed scope is a complete negative answer to the source's central universal no-reshuffling tester-completeness question at author turn1. The separate bundled mixed-multipartite fixed-test comparison/classification questions have not been resolved.

Critical checks:

1. Original OWR p2697 and Jivulescu–Lancien–Nechita arXiv:2010.06365v1 Definition3.1/Corollary3.3 and Section13 p35 really quantify over the stated local complex S1-to-Hilbert contractions and the output projective norm, without input index permutation.
2. The finite fourth-root phase ensemble and its basis-vector correction have the exact second moment (I+F)/(d(d+1)); no assumed SIC or Haar normalization enters the proof.
3. The energy bound applies to arbitrary testers with arbitrary unequal output dimensions. Its weaker pure-projector condition includes, rather than substitutes for, the required complex-linear S1 contraction class.
4. The Hermitian Hilbert–Schmidt basis gives F=sum G_a tensor G_a with the correct conjugations, and rho_f has coefficient1/d at G_0 tensor G_0.
5. Triangle inequality followed by two Cauchy–Schwarz inequalities gives an all-tester bound1 throughout f in [2/d-1,1]. Verify the d=3,f=-1/6 coefficients, positivity, trace, and flip witness.
6. The witness proves entanglement, while the scalar trace testers give exact optimized value1. No finite search is used for the universal bound.
7. Product and isometric-embedding extensions retain their stated full-separability scope, with no hidden input reshuffling or postselection.

The known fixed realignment/SIC Werner threshold is credited in Section8.2 of the source; the all-tester upper bound is the additional claim. The full2022 journal PDF was not retrieved. Source PDFs and exact hashes are in SOURCE_MANIFEST.json. No historical novelty certification is sought.

Run python verify_turn1.py and compare stdout byte-for-byte with TURN_1_CHECKS.json. The controls supplement the complete written proof.
