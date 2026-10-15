# Independent source reconstruction before candidate conclusions

UTC reconstruction start: 2026-10-03T01:48:11Z. Frozen head: fd4a71f2f7e08ece5f0d34d9d0df3fb6f460d8bf.

The primary target (Kourovka Notebook issue 21, October 2026 PDF, printed/physical p.177, problem 21.9; Barnea et al. arXiv:2507.04120v3, 22 September 2026, printed/physical p.53, Question 4) is:

For each prime p and each finitely generated nonabelian free pro-p group F (rank d>=2), find a finite family U={U_1,...,U_n} of open subgroups with F in U, such that

    { K <= F : K <= U_i and alpha(K)=K for all alpha in Aut(U_i), all i } = {1}.

The quantifier is over all common characteristic subgroups K; the wording does not restrict K to closed subgroups. The group F is part of the family, so K is characteristic and hence normal in F. Open subgroups have finite p-power index and are finitely generated free pro-p by Schreier. Continuous automorphisms are the profinite convention; strong completeness makes abstract automorphisms of each U_i continuous. Continuity implies closure preserves characteristic invariance, and K nontrivial implies closure(K) nontrivial. Therefore existence or nonexistence of a finite obstruction family is equivalent for all subgroups and for closed subgroups, although closure need not equal K.

The article p.53 treats the discrete statement only for some ranks (Observation 6.10), and explicitly leaves the pro-p counterpart unknown. Proposition 12.2 involves finitely many specified automorphisms and a normal-subgroup condition; Q4 involves all automorphisms of finitely many open domains. No interchange of these finite quantifiers is licensed. The paper specifically notes that Aut(free pro-p F) is not topologically finitely generated in its A-topology.

Theorem 3.11 (p.18) applies to a **closed**, topologically finitely generated subgroup H of a finite-rank free pro-p F: H is a free pro-p factor of some **open** subgroup V. Infinite index is not a theorem hypothesis but, when assumed additionally, it forces the complementary factor in V=H*L to be nontrivial. No corresponding conclusion is supplied for arbitrary infinite-rank closed subgroups or nonclosed subgroups.

Independent downloads of both target PDFs and the October update PDF are byte-identical to the historical manifest PDF entries. The update search has no standalone 21.9 entry. All 45 frozen snapshot files match bytes and SHA-256 in the externally frozen manifest. PNG screenshots and text extractions are renderer-dependent historical artifacts; their old bytes are not inferred from the reproduced PDFs.
