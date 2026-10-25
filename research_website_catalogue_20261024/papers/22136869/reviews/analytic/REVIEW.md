# Independent analytic review — Zenodo 22136869

**Disposition: PASS for the published mathematical claims within their stated model and local scopes.** No substantive mathematical defect remains established after the complete review. The page-12 derivation sentence is context-dependent and merits a precision note, but does not refute the explicit witness or justify a defect disposition. This report supersedes the provisional stopping conclusion recorded earlier in the research log.

Paper: *Exact Tree–Theta-Trinet Collisions under the Kimura 2- and 3-Parameter Models*, [Zenodo 22136869](https://doi.org/10.5281/zenodo.22136869), inventory row 43. The Zenodo metadata version is **1.2.6**; the public PDF filename and package identify **v1.2.7**. The discrepancy is preserved. Completion: **100% of this analytic validation task**, not formal proof-assistant verification or an exhaustive literature-priority search.

## Exact binding and reading coverage

| Published asset | Pages | SHA-256 |
|---|---:|---|
| Main PDF, 178,692 bytes | 20 | `7f1ecd0e70504736146eb8f2d4ebfb43980fd1feef50cf39bbe7e751ad5afa8f` |
| `k2p_displayed_tree_clarification.pdf` | 2 | `14855c3cddf1aea47f2d8e014ab9ea2618a8f3fa76cf08a4ebb468dcf68f1c57` |
| `technical-summary-clarified.pdf` | 2 | `4864396b878ecdd6cbfb0b92df960fb9344e015866eaaa61ee2979cfc66e4637` |
| Published ZIP, 443,027 bytes | — | `7c603e15f6afb7546f618b88bbefdc52ee264b656399f6656fc742aeabb786c7` |
| Main TeX | — | `e4876619a27cdd7e91e051c89b0827da418d6d201a40400c2bc3c31e2f1f9a9a` |

All 20 main pages and all four supplement pages were read. Corresponding mathematical source passages, both supplement TeX files and the topology figure's TikZ edges were checked. The main PDF inside the archive is byte-identical to the separate public PDF. All three documents rebuilt successfully with Tectonic in an ignored private copy; each rebuilt PDF has the same page count and **identical complete extracted text** as its published counterpart. Rebuilt PDF hashes differ, so byte-for-byte PDF reproduction is not claimed. See `source_build_receipt.json`.

All load-bearing verifier implementations were read: the two root-level compact K2P checkers, `verify_k2p_extended.py`, `verify_k2p_four_leaf_graft.py`, `verify_k2p_rank_family.py`, `verify_k3p.py`, and `verify_source_conventions.py`. The strict JSON parser, three mutation-test scripts, compact-certificate generator, suite runner and document-build script were also read. All five canonical JSON certificates were structurally inspected, parsed and replayed; large numerical arrays were checked by exact reconstruction rather than claimed as individually hand-read. The source-convention and certificate-field-coverage notes were read. The latter correctly distinguishes recomputed mathematics from informational metadata and sidecar transport copies.

Historical `ADVERSARIAL_REVIEW_DISPOSITION.md`, package research log, changelog, provenance narratives and stored verification-report contents were not used or opened as prior verdict evidence. Hashing them for integrity is not counted as reading them. Release/deployment tooling was not run. `source_pins.json` hashes every acquired asset and explicitly does not imply every administrative asset was read.

## Exact model and boundary

The model has a uniform stationary root, symmetric group-based DNA transitions on the Klein group, and independent reticulation parent choices. K2P uses the fixed global identification `a_C=a_T`; K3P permits three independent nontrivial eigenvalues. Strict stochastic interior requires positive matrix entries, nontrivial eigenvalues in `(0,1)`, and inheritance probabilities in `(0,1)`. These are model assumptions, not biological facts established by the paper.

The ten rooted arcs are `rho→1`, `rho→u`, `u→p`, `u→q`, `p/q→r2`, `p/q→r3`, `r2→2`, `r3→3`. This is a binary DAG with nine vertices. The root is the only common stable ancestor of all leaves because leaf 1 has its separate root branch. Root suppression composes its two Fourier vectors and leaves the theta core with paths `p-u-q`, `p-r2-q`, `p-r3-q`. The core is biconnected, has cycle rank two, two reticulations and three pendant bridges. Both p and q have only reticulation children, excluding every compatible tree-child rooting.

The four literal retained graphs give core factors `A2_y A3_z U_(y+z)`, `A2_y B3_z U_y V_z`, `B2_y A3_z V_y U_z`, and `B2_y B3_z V_(y+z)`. An unobserved dangling branch has ordinary-state likelihood one, or character A and Fourier factor one. This establishes the model formula independently of accepting a supplied polynomial as a likelihood. Repeated witness labels do not constrain the unrestricted rank map: nine effective edges plus two inheritance parameters give 20 K2P or 29 K3P coordinates.

Continuous time is **edgewise**: every edge separately has a positive-rate symmetric generator. Solving the log-eigenvalue equations gives `g>s²` for K2P and `a_C>a_G a_T`, `a_G>a_C a_T`, `a_T>a_C a_G` for K3P. Composition and positive coordinatewise square roots preserve these strict inequalities. There is no common generator, shared rate ratio, clock or globally compatible node-time assumption.

## Reconstructed proof and exact evidence

### Lemmas 2–3, Theorem 4, Corollary 5: compact collision, pp. 6–7

The five rational edge vectors give exact core factorization `M_yz=P_(y+z)R_yR_z` over `Q(sqrt(71))`. The tree vectors are `K²⊙P`, `K⊙R`, `K⊙R`. Independent calculations verify every Fourier coordinate and all 64 ordinary-state probabilities by recursive Markov pruning on each retained graph and separately on the comparison tree. All probabilities are positive and normalized, with exact minimum `1188799/79626240`. Network, effective and tree edges are strict stochastic; the published suite also reproduces the transition minimum `1/120`. The compact network witness itself is not asserted to be strictly continuous-time.

K2P is a literal submodel of K3P on the same graph, root law and switching semantics. Thus this collision already refutes universal tree/theta disjointness in both models. The subsequent quartic example need not have an observably genuine K3P output for this conclusion.

### Fixed-order diagnosis and Theorem 7: CT K2P, pp. 7–9

The invariant is `Q=q_AGG q_GAG q_CCA² − q_AAA q_GGA q_TCG²`. Tree vanishing follows by matching edge exponents under C/T equality. The favorable-order sunlet factorization has positive factors including `delta(1-delta)(1-f_G)²`; it depends on which leaf is adjacent to the reticulation.

The CT witness uses the isolated middle real root ell of the displayed cubic and sqrt(1423). I independently counted the root in the stated interval, refined rational bounds, performed exact cubic-field arithmetic with a quadratic extension, and reconstructed every network/tree Fourier coordinate and ordinary probability. The published modular check establishes cubic irreducibility; a degree-three field cannot contain the quadratic subfield, so the six-element basis is valid. Strict CT inequalities hold, and the minimum margin `11/900`, minimum eigenvalue `1/16`, and claimed minimum-probability interval are reproduced.

Fixing an r3 switching leaves a child with Q between `−1.9200e−9` and `−1.9199e−9`; swapping leaves 2 and 3 gives Q between `3.4284e−9` and `3.4286e−9`. The separate rational point's six Q values match the published negative fractions, and its minimum probability is `2920987217429243/200000000000000000`. No CT conclusion is attached to that rational sign point. These are direct witnesses to the fixed-order obstruction, not counterexamples to the correctly ordered level-one inequality.

### Proposition 8, Lemma 9, Corollaries 10–11: K2P rank/families, pp. 9–11

The 16 consistent coordinates have ten C/T orbits; normalization leaves nine ambient coordinates. Independent forward-dual differentiation of the literal switching graph gives the compact nine-by-nine determinant

`−7²·11²·19·107·151²·15013 / (2^60·3^25·5^10)`.

The corresponding determinant at the CT witness lies in the stated negative interval. Holding the second root-adjacent vector fixed changes rooted to effective pendant derivatives by an invertible positive diagonal scaling. These minors therefore establish ranks of the intended semi-directed maps.

For each positive tree character g, the recovery formula `alpha_g=sqrt(q_ggA q_gAg / q_Agg)` and its cyclic counterparts select unique positive roots and supply a smooth inverse. The positive K2P tree image is an embedded six-dimensional manifold. A submersion to the nine-dimensional ambient space pulls it back to dimension `20−9+6=17`, with fixed-output fibers of dimension 11. Lemma 9's local-coordinate proof verifies the hypotheses; dimension arithmetic alone is not the argument.

In the eight-variable symmetric ansatz, the two displayed squared equations recover a positive factorization locally, because all factors and relevant entries are positive. Independent symbolic differentiation gives the `(v,x)` determinant `675554683609333/194995116803358720000000`, which is nonzero. The implicit-function theorem gives the claimed local six-dimensional semialgebraic family, not a global classification.

### Theorem 12 and Proposition 13: quartic K3P and rank, pp. 11–13

For h>0 with `5h⁴=1`, the stated U,V,S,T and K satisfy all strict stochastic inequalities. Exact factorization with `B=(1,h²/2,h²/2,h²/2)` and the stated P holds in all 16 core entries, all 64 Fourier coordinates, and independently all 64 ordinary probabilities. The quartic field follows from Eisenstein on the reciprocal polynomial. Rational bounds `2/3<h<7/10` validate signs.

The three nontrivial U eigenvalues are pairwise distinct, excluding every globally relabelled K2P edge-parameter specialization. The output nevertheless is C/G-symmetric: with `a=(5h³+h)/16`, `t=h²/4`, its tree is `(1,a,a,t)`, `(1,t,t,t)`, `(1,t,t,t)`. It is not JC because `a≠t`, also witnessed by unequal Fourier entries. Parameter-level and output-level symmetry breaking are correctly distinguished.

Independent graph differentiation gives the specified 15-by-15 determinant `h(10h²+1)/(2^61·3^4·5^14)>0`. The rooted/effective conversion is invertible. Positive tree recovery for all three characters yields tree dimension nine, collision dimension 23 and fixed-output dimension 14. Strict stochastic inequalities supply the needed open physical neighborhood. The supplied exact matrix, descriptor order, graph endpoints and sidecar bindings all replay successfully.

### Corollaries 14–16: CT continuation, genuine outputs, density, pp. 13–15

Only `U_C−U_G U_T` and `V_G−V_C V_T` saturate the CT inequalities at the quartic point. Increase U_C and V_G by epsilon and solve for the 15 pivot coordinates at fixed output. Invertibility gives a unique real-analytic local solution. I independently checked all coordinates of `J p'(0)+F_UC+F_VG=0`. The two formerly zero margins have derivatives `(21−20h²)/19>0` and 1. All other strict inequalities and the full-rank minor persist. Sufficiently small positive epsilon therefore gives a strictly positive-rate network with the same already-strict-CT comparison tree. The analytic theorem supplies a branch; a finite tangent check alone is not mistaken for a finite-epsilon witness.

Unique positive tree recovery identifies each character-transposition fixed locus with the corresponding six-dimensional globally relabelled K2P tree submodel. Their finite union is closed with empty relative interior in the nine-dimensional tree manifold. The local collision submersion admits a section over a tree neighborhood; removing these three loci gives a relatively open dense set of observably genuine K3P collisions. Starting at a positive-epsilon branch point gives the same result inside the open CT chamber.

Full-rank real points in both claimed chambers give ordinary ambient open sets, hence Zariski density. Only additional equality invariants of the whole theta image disappear. Normalization, inconsistent-coordinate zeros, K2P symmetry, physical inequalities and tree invariants remain. The tree varieties have codimension three or six; dominance makes their preimages proper. Generic theta parameters are consequently not tree-equivalent.

### Lemma 18 and Theorem 19: arbitrary-tree grafting, pp. 15–17

Deleting any internal vertex of a labelled binary tree leaves three components. Put the selected module's comparison-star matrices on the attachment edges and identical component-edge matrices in both histories. Their conditionally independent kernels define a linear transformation of the three-interface joint distribution, so equality persists for every full-leaf pattern. A component consisting of a leaf has identity kernel, covering n=3 and mixed terminal cases.

For genuine K3P outputs, choose positive-eigenvalue JC component edges. Marginalizing a component kernel to one leaf yields an invertible path matrix, so that kernel has column rank four and the tensor product is injective. A nonidentity-character permutation is dual to a state-group automorphism; JC kernels commute with it. If the extended output gained a K2P symmetry, injectivity would force that symmetry at the interface, a contradiction. This proves an output-level conclusion, not only persistence of unequal edge parameters.

The theta root is placed on the u-side attachment only. Its effective vector splits using positive square roots, strict stochastic near the witness and strict CT in the CT case. The attached components orient from their interfaces, with the u-side component starting from the root's other child. Binary degrees persist, exactly one nontrivial theta blob has two reticulations, and its contraction gives the original labelled tree. Any bijection of the three components works with its corresponding u-side choice. No simultaneous multi-blob composition follows.

The published four-leaf regression checks all 256 coordinates and probabilities. Fresh independent component-kernel controls use one-, two- and three-leaf components with distinct rational JC eigenvalues: all **36** normalization, positivity, explicit-left-inverse and six-automorphism equivariance checks pass. These corroborate, but do not replace, the universal linear-kernel proof.

## Primary interfaces

Fresh PDFs and hashes are in `primary_sources.json`. In [Brits et al. v2](https://arxiv.org/pdf/2607.12919v2), I checked Definition 2.1, Fourier/displayed-tree formulas, restricted parameter domain, the five explicit sunlet coordinates and Lemma 4.1 factorization, formal Lemma 5.6/Corollary 5.8, and the relevant induction. The concrete graph and strict parameters meet those interfaces, and the collision contradicts the old universal K2P claim. In [v3](https://arxiv.org/pdf/2607.12919v3), the removal, fixed-order explanation and concluding high-level Kimura questions match the paper's versioned description. Its preserved level-one and JC results are not refuted.

[Ardiyansyah](https://arxiv.org/pdf/2104.12479), §3.4 and Lemmas 3.8/5.1, confirms the nice/funnel-free restriction and exclusion of two-/three-leaf simple strict level-two networks. Those variety-noncontainment results do not rule out this non-nice theta's pointwise intersection. The Fourier likelihood formula was independently reconstructed through character multiplication and ordinary-state pruning. No external confirmation is needed for the collision proof. Other bibliography entries are background; this review does not claim exhaustive priority research or verification of every theorem in every cited article.

## Page-12 interpretation and nonblocking issues

The sentence after Theorem 12 says the positive ansatz and tau=1/3 force `e/d=6/5`. Under arbitrary factorization `M_yz=P_(y+z)B_yB_z`, that necessity is false: `counterexample_ratio.py` gives exact strict-interior factorization with d=e=1/4, the same P, and `B_T=5h²/12`. Its **225** checks remain as a boundary test.

But preceding equation (17) specifies equal nontrivial B entries. Under that contextual restriction, the ansatz gives `M_CC=4d²/5` and `M_TT=5e²/9`; equality implies positive `e/d=6/5`. This is the strongest plausible reading of a derivation of the selected witness. The counterexample therefore establishes **no unequivocal substantive defect** in context. The provisional DEFER was withdrawn, full review resumed, and all remaining claims were checked. See the corrected `INTERPRETIVE_NOTE.md`. No source repair was made.

The metadata/filename version discrepancy should remain visible in provenance. The manuscript describes Bareiss elimination whereas the verifier uses exact field Gaussian elimination; the same determinant was independently reproduced, so the algorithm-description distinction has no mathematical effect. Neither issue warrants a mathematical defect classification.

## Reproducibility and independence

`fresh_main_controls.py` passes **845** exact assertions; `fresh_ct_family_controls.py` passes **495** additional assertions. Both were written from the manuscript, with independent literal graph/pruning, algebraic-field, rational-bound and differentiation mechanisms, without importing supplied mathematical code or certificates. The latter imports only the former review script. The graft script adds 36 checks. The qualified ratio control adds 225. Counts are transparent deterministic assertions, not independent research replications.

The unchanged published suite ran in a private ignored copy using Python 3.14.6: exit 0, all ten stages passed, final `ALL EXACT CHECKS PASSED`. All 46 manifest-listed members were checked before execution. Current stdout/stderr and the execution receipt are retained. The independent scripts use project Python 3.9.6/SymPy 1.14.0 and run with `/Users/alec/Documents/Math/.venv/bin/python -E -B` plus each review script's absolute path. Build/replay receipts bind outputs and hashes.

No sibling review or dedicated historical verdict was read before this conclusion. Incidental validation language occurred in the required p.19 acknowledgments, reader summaries and source-convention/field-coverage notes; it was not used as evidence. The parent asked for reconsideration of page 12 in its fixed-B context, so this is not described as wholly blind after that exchange. No sibling substantive findings were used.

**Strongest verified result:** exact strict-interior collisions under the specified independent-switching Kimura models, including edgewise strictly continuous-time examples; full local ranks and claimed collision/fiber dimensions; nearby observably genuine K3P common outputs; and insertion of one theta at any internal vertex of any labelled binary tree preserving all full-leaf probabilities.

**Exact remaining gap within the stated theorem chain:** none identified. Validation is conventional analytic reasoning plus inspectable exact computation, not formal machine-checked proof. It does not establish common-generator/clock/global-time variants, correlated inheritance variants, JC collisions, generic indistinguishability, complete physical image coverage, simultaneous theta moves, genuine four-terminal blob results or a full intersection classification. No repair, outside communication, publication, Git, website or spreadsheet mutation was performed.
