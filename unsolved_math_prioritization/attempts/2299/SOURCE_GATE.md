# EP-776 source and status gate

Checked 2026-10-21 UTC. This is a source/novelty gate, not an independent proof audit.

## Decision

Do not treat the general exact threshold as an unclaimed open target. A pre-existing complete-threshold proof package exists. The safe next step is verification of that package and its statement correspondence. Neither a live official status change nor independent correctness of the full package was established here.

## Exact target and variants

Fix an integer r>=2. On [n], seek a family of distinct subsets, no member included in another, with at least r members of every occupied cardinality. Maximize the number g(n,r) of occupied cardinalities. The threshold n0(r) is the least integer N such that g(n,r)=n-3 for every integer n>N. This is a universal eventual threshold, not merely existence at one n, and uses strict n>N. The historical exactly-r condition is equivalent for this objective: retain r members on each occupied level. The r=1 question instead has extremum n-2 for n>3.

Historical sources: Erdős, Problem sessions, Ordered Sets, Eq. (10.28), pp. 860–861; Guy, A Miscellany of Erdős Problems, American Mathematical Monthly 90 (1983), 118–120, especially p.119. Historical wording and location are recovered through He–Tang's reproduction, not independently compared against original printed pages. Guy metadata was independently located at https://doi.org/10.1080/00029890.1983.11971168 .

## Established cited progress

He–Tang, arXiv:2602.09803v2, 21 March 2026, reports n0(2)=3, n0(3)=8; for r>=4, 2r+2 <= n0(r) <= 2r+2 log2(r)+O(log2 log2(r)). Hence n0(r)/r tends to 2. Its small cases use finite witnesses/search plus an infinite-tail construction. The manuscript is marked submitted, not verified here as journal-published. https://arxiv.org/abs/2602.09803 ; https://arxiv.org/html/2602.09803v2 .

## Subsequent full-solution claim

M. Thiim's public package, tag v0.4.1-proof-claim dated 17 July 2026, claims n0(r)=2r+4 for 4<=r<=10 and n0(r)=2r+5 for r>=11. It includes a human-readable PDF and Lean endpoint Erdos776.Uniform.erdos776_threshold for actual antichains, including leastness. The package states three bounded native_decide computations and a symbolic argument for r>=378. These are author-reported verification properties; this recovery did not run Lean, audit axioms, or independently certify the argument. The r=2,3 results remain attributed to He–Tang.

Primary package: https://github.com/mthiim/erdos_776/tree/v0.4.1-proof-claim . PDF: https://github.com/mthiim/erdos_776/blob/v0.4.1-proof-claim/paper/erdos776_complete_thresholds.pdf .

A separate r=4 candidate https://github.com/GiladR1979/erdos-trotter-n0-4 explicitly disclaims peer review and priority. September replication https://github.com/OV3RK177/erdos776-three-cases reports builds and three corollaries of Thiim. Those reports strengthen the need to inspect the prior package; they do not substitute for our own verification or official acceptance.

## Official status versus indexed evidence

Direct opens of https://www.erdosproblems.com/776 and its forum, LaTeX and proof-claims endpoints returned 403/unavailable. Thus LIVE OFFICIAL STATUS IS UNVERIFIED. Indexed official-page results, approximately three months old, say OPEN and cite Er81i/Gu83. Indexed forum text dated 10 April 2026 records Bloom considering the asymptotic result solved in spirit; this is discussion, not a status change. The later package and replication identify proof claim #78, but the live claims page was inaccessible. Do not repeat the old index statement that no proofs are claimed as current fact.

## Boundary of this recovery

No new theorem, novelty claim, publication, queue change, or external communication was made. AI assistance declarations are not mathematical certificates. The historical generalized deficit question n-delta is a different problem; indexed forum comments about delta>=4 are not imported as established results for this gate. Full original-print comparison and current official moderation remain unverified. Existing complete proof must be audited before declaring either a resolution or a remaining open gap.
