# Independent reduction audit

Timestamp: 2026-10-07 05:16:45 UTC (2026-10-06 22:16:45 America/Los_Angeles).

Scope: classical face-to-TSP projection, exact real PSD lift monotonicity, parity/padding, and finite construction checks. Source exponential matching theorem remains a separately audited hypothesis.

Strongest verified result: PM(n), for every even n>=2, is a coordinate projection of an explicitly defined face of TSP(3n) (Yannakakis original), and also of a compressed 2n-city face with mandatory diagonal edges. Arbitrary N>=m>=3 padding via a forced path shows xc_psd(TSP(N))>=xc_psd(TSP(m)) without increasing matrix dimension. Full proofs and exact constraints are in proofs/tsp_reduction.md.

Primary literature: Yannakakis JCSS43(1991), Theorem2 printed p454, uses 6k cities for matching2k, hence3n after renaming. Rothvoss arXiv1311.2369v4 pp3-4 records the linear-size consequence near Cor2. The2n contraction is an independently checked simplification, not a new lower-bound method and not attributed as the original printed count.

Finite checks ran inline successfully on Python3.14.6 after attempted script writes failed because the host disk was full. Pair enumeration n=2,4,6,8 checked 1,9,225,11025 matching pairs; each gadget had 1,6,120,5040 Hamiltonian tours, and every matching had respectively1,2,8,48 preimages. Ambient complete-graph enumeration checked60(K6),3(K4),2520(K8) tours and obtained face sizes1,1,6. Padding checked all face tours for(3,4),(3,5),(4,5),(4,6),(5,6),(5,7), proving finite-instance surjectivity against all old tours. Negative controls caught absent diagonal forcing and disconnected union-of-matching subtours.

Checkpoint estimates for this assigned route: mathematical reduction resolution100%; reproducibility artifact packaging100%. Overall project percentages are not estimated here; source theorem and publication conditions remain outside this route.

The runnable checks/tsp_reduction_check.py and exact output checks/tsp_reduction_results.json were persisted after disk recovery and reproduced successfully. Script SHA256: 26513383197675599b7f9157c763cac38334ec369dce8cbf25808a4dcc3bfd05.

Exact remaining gap: none in the reduction proof or assigned finite checks. No external communication or Git/publication operation was performed.
