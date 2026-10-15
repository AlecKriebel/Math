# Fresh complete-package adversarial review 02

Review of frozen candidate-v2, begun 2026-10-07 05:01 UTC (October 6, 2026 PDT).
Reviewer: new independent complete-package reviewer, with new scoped children.
The original REQUEST.txt and root AGENTS.md were read first. Target conclusions were treated as hypotheses; no prior complete-package verdict was consulted.

## Verdict

**CLEAN COMPLETE-PACKAGE VERDICT: no substantive mathematical, priority, scope, metadata, reproduction, PDF-layout or package issue was found in this exact frozen-v2 candidate. No repair is requested.**

This is a fresh independent integration of the whole package, including the complete positive-cost input, not an aggregation of earlier favorable verdicts. The new positive-cost and priority/metadata reports were read in full, and their checkable evidence was integrated with my own reconstruction. This is manual mathematical review assisted by AI, not a formal proof certificate, conventional human refereeing or a certificate of worldwide firstness. It does not establish that a production deposit or tracker update has occurred.

## Exact reviewed candidate

The reviewed input is the preserved `verification/frozen-v2` snapshot and its receipt `receipts/frozen_package_v2.json`. Initial and final checks match every one of its nine frozen files against both the snapshot and the working candidate.

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| main.tex | 20054 | 7475979d063f5ad6e9e85f09fca5eca6f1beb83a83f654bc9011854dc8c4182a |
| paper.pdf | 89312 | d2af46715d94a23d4c51b25a4b78e5e2dab64cd7cae3fa61f2349194e5fc6f75 |
| source-and-verification ZIP | 182215 | d88ca91ab6d75388f61e5103c7f4a189fe3bab4a7349312313e4d06ea3a72d8b |
| zenodo-deposit.json | 3106 | 2c8d034e5ab30787c747b8e9bb195f332cd6a63f421147a8e2656cd1d39ae4de |
| README.md | 4574 | 8d6624ff1ef3030a50ea94fb8b346d2e70d4fa234b17ea398fcb700c50adcdba |
| PACKAGE_CONTENTS.json | 7861 | 79098518017e1d287f13b6b3e9a55b27580a81aaea8a4cab90d3fd62a50dae14 |
| DEPENDENCY_LEDGER.md | 3742 | e26bad5ff0661aba2c92cabdab681680a0ed883c39574c8aee4d1b066b26ca04 |
| THEOREM_LEDGER.md | 1631 | 5abdf8bef5dfb5227d59993c099028f48d8c821457c6bfd89fc0eb1a125b9697 |
| REQUEST.txt | 15302 | 50693da7fdd251335c7772ca10ef108d21f9e7f5e28fc51c579c85c2f4f0d1f8 |

`hash_inventory_receipt.json` and `final_candidate_integrity.json` preserve all checks. The archive has exactly 35 regular members: 34 manifested payload files and its manifest. All sizes and hashes match; no unmanifested, duplicated, path-traversal, absolute-path or symlink member was found.

## Actual coverage and independence

I read the complete frozen manuscript, all six deposited PDF pages visually, the entire README and intended deposit metadata, both theorem/dependency ledgers, and every material archive supplement. This includes the dated priority audit and both addenda, all source/web manifests, all nine scoped proof/audit documents, the four Python verifiers and their certificates, software/adaptation/reproduction records, and the upstream manifest. The historical audit reports were read after reconstructing their mathematical mechanisms; their favorable verdicts were not used as premises.

The pinned upstream clone was used read-only. Its HEAD is `adc7f1241b42e322a6451854ab7e4b4c146bf78a`, with a clean status. I read its root and manuscript READMEs, INPUTS warning, full family-259 TeX source including figure/bibliography, catalogue and Lean scope listings. All twenty entries in the archived upstream manifest match actual source bytes. No relevant family-259 Lean declaration/build was identified; no formalization claim is being made.

A new child independently reconstructed the full positive-cost input, with original instructions and sources. A separate new child reconstructed priority, additional-content eligibility and metadata; its own fresh child checks inventory, rights, provenance and disclosures. Their scopes and evidence are retained under `positive_cost/` and `priority_metadata/`. No external individual communication, upstream write, Git mutation, branch change, release, deposit or tracker operation was performed. Writes are confined to this review directory. The shared workspace branch was read and remains main.

## Direct cellular proof: independent reconstruction and attempted falsification

The source free-basis substitution is genuinely invertible: with u_0=1 and u_i=u_(i-1)ab_i, b_i=a^-1 u_(i-1)^-1 u_i. The two substitutions recover each generator by induction. Thus F=<u_1,...,u_99> is free of rank 99 inside A and Gamma.

The bipartite graph has edges g_L--(gu_i)_R for i=0,...,99. The zero matching and two-edge generator paths prove connectivity and degree 100. A nonbacktracking cycle produces an alternating word u_i u_j^-1... . Consecutive edge labels differ. Deleting zero labels joins only equal signs; every remaining adjacent opposite-sign pair has distinct labels. A nonempty freely reduced word remains, so the graph is a tree. This explicitly checks the identity-label issue rather than assuming a Cayley graph identification.

For adjacency Af=0 on a d-regular tree, the layer energies E_n satisfy E_(n+1)>=E_(n-1) for n>=2, by Cauchy--Schwarz at each depth-n vertex and exactly d-1 counts per parent. The positive odd and even layer sequences are summable and nondecreasing, hence zero; the depth-one equation kills the root. This is valid for complex functions and d=2. It gives actual injectivity, without a least-singular-value or bounded-inverse assertion.

With T f(g)=sum_i f(gu_i), adjacency is the block matrix with T,T*. Coefficient right multiplication by S=sum u_i is T*. Decomposition over left cosets gF transfers injectivity to l2(Gamma). Right multiplication by t-1 is injective because t has infinite order and a kernel vector is constant on each infinite right-t orbit. The opposite coset convention would be wrong; the paper uses the correct one.

I derived the boundary from the lifted attaching loops with left cellular coefficients and right multiplication in coordinates. D_a w=S and D_bi w=P_i=u_(i-1)a. For r_v=tvt^-1v^-1, evaluation gives D_x r_v=(t-1)D_x v for x different from t, and D_t r_v=1-v. Consequently:
- (d_2 q)_a=q_w(t-1)S;
- (d_2 q)_bi=q_i(t-1)+q_w(t-1)P_i;
- (d_2 q)_t=sum_i q_i(1-b_i)+q_w(1-w).

No factor is commuted through S. Injectivity first kills q_w(t-1), then q_w, then each q_i. The telescoping identity checks d_1d_2; its w-row is tw-wt. This avoids any transposed Fox-matrix assumption.

Integral cellular chains have finite support and embed in the completed chains. Thus ordinary d_2 is injective. The universal cover is simply connected and two-dimensional, so it is acyclic; successive Hurewicz and CW Whitehead imply contractibility. Asphericity is deduced rather than assumed. The displayed complex is therefore a finite two-dimensional K(Gamma,1).

The adjoint kernel of d_1 consists of vectors invariant under every generator, hence constants on infinite Gamma and zero. Its image is dense. Hilbert-module rank and trace faithfulness give dim ker d_1=100 and dim closure(im d_2)=100, so reduced first homology is zero. Injective d_2 and the two-dimensional classifying space handle degree two and higher degrees. The Euler characteristic alone would only equate beta_1 and beta_2; it is not used as a substitute for injectivity.

These arguments use neither cost bound. Degenerate variants were checked: d=2 remains valid; S=1 in the zero-b_i variant is directly injective; finite-order t would break the orbit argument, but t is infinite here.

## Actions, upper graphing, comparison and exact scope

Amalgam normal form embeds A and B=J x <t>, and the displayed reduced-word argument freely generates J. Gamma is countably infinite and generated by the 101 displayed elements; t has infinite order. The exponent homomorphisms agree on J and extend to chi, including chi(w)=100 rather than an incorrectly assumed zero.

For each g!=1, a Bernoulli fixed point forces two independent continuous coordinates x(g)=x(1), a null event. Countability gives the invariant Borel conull free set. The height formula obeys the right-action law, preserves the product probability and stays free by its first coordinate. The countable product and finite products are standard atomless spaces.

The t-transformation is mixing: two finite coordinate supports become disjoint for sufficiently large powers because t has infinite order, and cylinder approximation extends independence. Hence X is ergodic. Each invariant height-section of Y_M is t-invariant, and a cycles all heights, so every Y_M is ergodic for any positive M. The proof does not require coprimality with 100.

The marker C_p has measure p and meets every t-orbit after including its null exceptional part. Full t plus the 100 J generators restricted to that marker gives the B-relation at cost 1+100p, by the commutation path. The initially supplied a-edges at heights 0,...,98 cost 99/M. The w path propagates each window of 99 source heights to its next height. k=0,...,M-100 supplies exactly heights 99,...,M-1, including the final edge to zero. Thus the graphing generates Gamma, and its infimum gives the stated bound for every M>100. No graphing attainment is asserted.

I retrieved the actual [published Gaboriau 2002 PDF](https://numdam.org/item/10.1007/s102400200002.pdf), and visually checked printed pp. 106, 126 and 128: Hilbert-module rank/faithfulness, infinite-class zeroth vanishing, free-action invariance in all degrees, and the cost comparison with its zeroth correction. The hypotheses are countable standard p.m.p. relations/free group actions and do not impose ergodicity. The equality question immediately follows on p.129. These exact uses are justified by the constructed actions. [Gaboriau 2000](https://perso.ens-lyon.fr/gaboriau/Travaux-Publi/Cout/Cout.pdf), Definitions I.5, distinguishes group infimum cost from action cost. [Fox 1953](https://www.maths.ed.ac.uk/~v1ranick/papers/fox1.pdf), pp.547--549, was inspected for the classical derivation convention. Lueck's Theorem1.11 supports the alternate dimension citation.

The finite-group boundary has beta_0=1/q and cost 1-1/q, so dropping the zeroth term would be wrong. An infinite group's nonfree action need not have infinite orbits, but every action used here is free. For a hypothetical nonergodic free action the same primary invariance theorem still applies. A free p.m.p. action of an infinite countable group cannot have a positive-mass atom, because its infinitely many translates would have equal mass.

The height limit bounds one fixed invariant beta_1(Gamma), not a varying sequence of unrelated relation invariants. It independently gives beta_1=0. Every free action has cost at least one; the Y_M sequence bounds the infimum above by 1+99/M. Hence group infimum cost is one, with no assertion that an action attains it. The refuted equality is relation/action-specific; the group-infimum equality holds.

## Positive cost input: independent reconstruction and integration

The full source chain was read and reconstructed independently. The new child's final report, `positive_cost/REVIEW.md`, finds no substantive gap and supports the exact lower bound. I read its full proof review and its independent boundary checker/receipt. My own reconstruction and attempted falsification cover:

1. Compression counts finite supplied classes with kappa and retains infinite classes. The marked finite partitions supply small exact complete sets without selecting a transversal for infinite classes. One indexed edge per excluded finite class descends the quotient distance; opposite orientations cannot select the same instance. The many-to-one contraction is split at both endpoints using ambient partial isomorphisms, preserving each indexed piece's cost. Recovery uses T-completeness of the retained set, not an unjustified assertion x T f(x).

2. Deployment uses finite near-optimal graphings justified by finite generation, finite unnormalized internal sheets and sheetwise projection. Its factor relations increase while replacement graphings need not. Compression costs telescope to c-1+kappa(S_n)+error. Alternating normal form exhausts the pulled-back J relation, and dominated convergence uses infinite J and fixed finite measure. Projection and the final normal-form argument occur at each finite stage; only scalar bounds pass to a limit.

3. The cocycle remembers group labels, not merely endpoints of finite models. It kills all J labels by the defining w-row and b_i values. The original free action fixes path labels equal to a before cylinder approximation. Every signed-domain test uses the correct prefix or additional inverse displacement. Tests are fixed before model limits; local independence is needed only at one source. The generating-list bound holds for every labeling and includes x_v at all failed sources, so expectation yields the asserted rank transfer.

4. Independent random permutations in the actual free basis give expansion. The binomial/containment bound has residual exponent 99-1-95=3 and constant K=e^96 96^99/95^95. The fixed-size plus geometric-tail argument and diagonal asymptotic freeness use the same sequence. Repeated columns and two-column overlaps force fixed points of nonidentity words from fixed finite lists. An additional independent exact enumeration of all index-equality/zero patterns over 0,...,4 passes 260 cases; it is recorded in independent_overlap_receipt.json.

5. Saturation seeds at most 100b+90 beta<2 alpha n columns. At s=floor(alpha n) row additions the union would have fewer than 96s columns, contradicting expansion. Thus |S|<=92 alpha n<n. Mixed rows have at least 91 distinct positive exterior letters and pairwise overlap at most one. The coefficient group H is the actual subgroup of D; the two maps proving the relative presentation are inverse on generators. H-injectivity is supplied by that isomorphism, without a circular Freiheitssatz.

6. The planar proof minimizes mixed relator number in the actual free product, with finitely many true coefficient relations per filling. Generic exterior tracks pair opposite signs. A disconnected cluster surrounds a coefficient element trivial in D; H-injectivity makes the cluster removable. Same-relator adjacent copies give inverse loops based at the unique exterior occurrence, so a dipole is removable without an extra coefficient conjugator. Face equations give exact H-valued intervening gaps. The Euler sign is correct and repeated face walks are counted with multiplicity. Every positive non-full inner vertex has one exceptional gap, at most three internal edges, and a matching interval of m-3 exterior occurrences. Total contribution at least two gives two distinct, occurrence-disjoint intervals.

7. The shortest loop is linearly H-reduced by deleting trivial detours or sliding/folding distinct edges. Cyclic reduction creates at most one seam letter or seam gap. At least one long interval avoids it, giving 88 exterior occurrences whose matched row complement has at most 12 original letters. Saturated arcs force a traversal with at least 31 exterior edges. Distinct exterior indices keep Q_1 and Q_2 out of the chosen removable arc interior. Adding the complementary path and deleting that arc preserves connectivity, rank and surjective loop values, including coincident endpoints, and saves at least 19 edges.

The exact choice alpha=2^-61 is valid because K<3^97 96^4 and 2*3^97 96^4<2^183. Thus eta=1/(100*2^61)>0. The source's final combination uses the same model sequence, obtains delta_X>=eta and then Cost(R_X)>=1+eta. No finite Gamma-model, uniform estimates over growing word lengths, closed-range assertion or formal proof certificate is assumed.

As an extra adversarial route, I tested the precise one-generator criterion stated immediately after Gaboriau 2000 VI.24, printed p.91, and used to prove VI.24(3): a subgroup G_1 has fixed price one, the whole group is generated by G_1 and gamma, and gamma^-1 G_1 gamma intersect G_1 is infinite. Under those hypotheses the whole group has fixed price one. VI.24(3) iterates this through an increasing union of infinite groups starting at a fixed-price-one group. The proposed one-step application here is G_1=B and gamma=a. Both the initial fixed-price hypothesis and generation hypothesis hold: VI.23 gives fixed price one for B=J x <t>, since t has infinite order and J is infinite, and Gamma=<B,a>. The infinite-intersection hypothesis fails.

Indeed chi(a)=1 and chi(J) is contained in 100Z, so a is not in J. If b lies in B intersect a^-1 B a but not J, the alternating amalgam word aba^-1 is reduced and cannot belong to B. Hence b is in J. Then aba^-1 is in A intersect B=J; conversely these two J conditions suffice. Thus B intersect a^-1 B a equals J intersect a^-1 J a. The folded core graph for J has 199 vertices and 298 unoriented edges: the w-cycle plus the 99 base b_i loops. Deleting the base loops and the final a-edge gives a spanning tree, verifying exactly the subgroup J. The first a-edge leads from vertex 0 to vertex 1, so loops at vertex 1 represent a^-1 J a.

The full common-label product component based at (0,1) is the six-vertex, five-edge path (1,3)--(0,2)--(0,1)--(198,0)--(197,0)--(196,198). Exhausting all common outgoing labels gives no other edges or vertices. Its rank is zero, so it has no nonempty reduced closed word and J intersect a^-1 J a={1}. The criterion therefore cannot be applied with B and a. This is not a general malnormality claim or an exclusion of every possible application of classical criteria. The full finite receipt and exact checker are retained in `conjugate_intersection_receipt.json` and `check_conjugate_intersection.py`. The positive-cost child independently obtained the same path before reading my receipt.

## Reproduction, visual review and package hygiene

All four scripts were executed from a new extraction of the frozen archive, with Python 3.14.6 and no preexisting build outputs:
- verify_exact.py: PASS exact parameter and free-group chain identities.
- finite_boundary_check.py: PASS 329,027 cases on equal-weight finite atomic spaces, including two loop/repetition/noninjective cases.
- check_fox.py: PASS basis, derivatives, commutators and telescoping boundaries at ranks0,1,2,99.
- verify_constants.py: PASS arbitrary-precision rational/integer inequalities.

The scripts and recorded certificates were read. They use Python's standard library and clearly state their limited scope. Neither finite checks nor successful compilation validate infinite-dimensional injectivity, Borel contraction or the positive-cost theorem; the written proof reconstruction supplies those checks.

Tectonic0.16.9 builds the exact archive main.tex successfully. The desktop native compiler also reports success. The rebuilt PDF has the same 89,312 bytes and extracted text as the deposited PDF; every one of its six PNG page renders is byte-identical to the corresponding deposited-page render. PDF hashes differ because creation metadata is not fixed; bit-identical build bytes were never promised. Every deposited page was individually inspected for formula typography, glyphs, references, breaks, clipping and overlap. No defect found. All 23 font entries are embedded; author/title/subject metadata agree, and the PDF is unencrypted, with no JavaScript/form content.

The pinned upstream TeX was independently rebuilt in an isolated review copy. Exactly the three disclosed pdfTeX metadata primitives were guarded, matching the adaptation hash; mathematical sources were unchanged. TeX, bibliography and crossreference reruns all complete successfully. This verifies the source-build claim, not the cost theorem by compilation.

There was one initial review-local rendering attempt before its output directory existed; it was corrected by creating that local directory. No candidate or deposited file changed. The raw receipt retains that attempt, and the final render/build receipts document the successful checks.

No common credential/private-key signal was found in the archive. There are no source PDFs, substantial copied source paragraphs, third-party code, caches, build directories or credentials. Original-note/code/audit licensing is consistently CC BY4.0 and inferable from the repository's established upload-kit default. The upstream source's own Apache license is not relabeled. The separate metadata-rights report records concrete text-overlap checks, provenance and license basis. This is a bounded package check, not legal adjudication.

Useful receipts: hash_inventory_receipt.json; final_candidate_integrity.json; upstream_hash_receipt.json; classical_sources_receipt.json; reproduction_summary.json; pdf_build_visual_receipt.json; native_compilation_receipt.json; upstream_rebuild_receipt.json; package_hygiene_receipt.json; independent_overlap_receipt.json; conjugate_intersection_receipt.json.

## Priority, contribution and publication limits

The new priority child independently retrieved primary statements, current upstream version records and the author's pinned public triage. Its report is `priority_metadata/REPORT.md`, with fresh evidence manifests. No later source correction was detected in the checked public channels; this does not exclude criticism elsewhere.

The core limit proof and conditional counterexample were already literally public in the preliminary triage; the general fixed-price implication was already explicit in PSV Remark6.6 v1 (2018). The frozen package acknowledges both. The basis substitution is already upstream; Fox calculus, the dimension/topology steps and the special free-group operator's injectivity are classical. No firstness claim or independent fixed-price discovery is justified or made.

The direct cellular/operator proof adds separately checkable content independent of both cost bounds. It verifies the exact presentation's asphericity and all-degree vanishing rather than restating the earlier limit proof. The all-degree conclusion alone is also predictably obtainable from graph-of-spaces, the earlier first-Betti vanishing and Euler characteristic; the degree range itself does not certify novelty. The current neutral title, abstract, introduction, README and metadata accurately describe an expanded attributed consequence and verification note with a direct calculation. That product meets the original request's additional-content condition, with the mathematical checks above completed.

Author/ORCID/date match instructions. Extensive AI use and the lack of conventional human refereeing are stated. Automated reviews are not called human peer review or machine formalization. The group-infimum boundary and source's intermediate/non-final warning appear throughout. Historical supplement statuses describe their dates and scopes; the README points to external frozen/review records for complete-package validation.

This review does not inspect a production draft/record, assigned DOI, remote checksums, DOI resolution, tracker row or final publication commit. Those operations have not been performed in this subtask. This clean package verdict permits the separately authorized publication process; it does not itself establish publication. Any material change to the paper, archive or metadata requires another fresh whole-package review.


## Final checkpoint

Review coverage is complete: mathematics 100%; publication/package 100%. These are coverage estimates for this review, not estimates that the overall production-publication task is complete. No substantive issue or repair remains from this review. The exact frozen hashes were rechecked after integration. `VERDICT_RECEIPT.json` records the integrated report hashes, reviewed candidate hashes and limits.
