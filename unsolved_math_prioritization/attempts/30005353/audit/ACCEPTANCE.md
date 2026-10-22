# Independent mathematical audit: cycle-filling problem 30005353

Date: 7 October 2026.

## Verdict and precise scope

**Accept the five partial approaches, with one minor explicit domain qualification supplied below. The main unbounded-ratio question remains unresolved, 5/5.** No substantive proof gap was found in the five main results. The report is an independent mathematical review with exact computational controls, not proof-assistant certification, a claim of novelty, or an exhaustive current-literature survey.

The accepted setting is finite connected simple unweighted graphs of positive cycle rank, with total attaching-cycle length as cost. The results apply to the minimum mod-2 homology-killing cost a₂ and the minimum fundamental-group-killing cost aπ. They do not assert that a general homology basis normally generates, that every normal-generating family can be shortened to a basis, or that every simply connected filling is contractible.

The sole correction is to say **nontrivial finite quotient Q** in the auxiliary quotient-systole paragraph of Approach 4. Without that qualification, s_Q has no definition when Q is the trivial group. This does not change any main result, proof, example, or unresolved-status conclusion.

The original files were preserved. A separate one-word insertion patch and a corrected review copy are supplied. Acceptance of the corrected copy does not authorize or imply publication.

## Frozen inputs and corrected output

- Original AUTHOR_MANIFEST.json: 1,917 bytes; SHA-256 `7afaa5bcbe41e3fc782f21a63580930840c753f8f0444b9d3dcc6c4986d48f87`.
- Original authored/PROOF.md: 27,223 bytes; SHA-256 `48eb7d0faff5972c9d24407c8639d0f1aff8b553904ac643f816092812b347cc`.
- All twelve authored/check files match the byte counts and SHA-256 values in that original manifest.
- Corrected audit/PROOF.reviewed.md: 27,234 bytes; SHA-256 `bbf6f37a385ad2f4688e5102980437461d45cff29f2710d0c92dcf50a91d4b9e`.
- audit/PROOF_SCOPE_CORRECTION.patch SHA-256: `c8d41cf9cc56a5cda53586a6ed8d705b8188de498e13e11e7c80a9a83137e731`.

The proof's increase from an earlier size does not indicate corruption: the manifest-pinned final 27,223-byte version was the actual input read in this audit. Its source-credit and planar-equality additions are included in the review. The companion AUDIT_MANIFEST.json pins the audit artifacts and repeats the accepted input pins.

## 1. Primary-source identification and coefficient check

The publisher record identifies the target as Karim Adiprasito's Question 12 in *Combinatorics*, Oberwolfach Reports 20 (2023), no. 1, 5–89, specifically printed pp. 83–84. The unrelated preceding Question 11 is Fox's binary-vector-space problem.

Sources inspected:

- Publisher record: https://ems.press/journals/owr/articles/12697684
- Publisher PDF, independently opened during this audit: https://ems.press/content/serial-article-files/46994?nt=1
- Official MFO PDF: https://publications.mfo.de/bitstream/handle/mfo/4018/OWR_2023_01.pdf?sequence=4
- DOI: https://doi.org/10.4171/OWR/2023/1

The retained MFO PDF is 773,437 bytes, SHA-256 `83e5cd242e80d277c9e863cab34cbaeb7ab38d6c6ec0da015fabe2c080e55468`. Both target-page renders were visually inspected. The independently fetched publisher PDF text agrees with those pages. A fresh MFO web fetch timed out, and publisher screenshot requests failed; these failures did not prevent inspection of the retained page images and independent publisher text.

The target is indeed the aπ/a₂ ratio and its bounded-degree form. The following additive-progress assertion on printed p. 84 expressly uses F₂ and RP². Thus the coefficient issue is present in the primary source, not introduced by OCR or attribution to the neighboring problem. The packet's proof that RP² triangulations have equal a₂ and aπ is sound; the resulting source observation should remain narrowly described as an apparent coefficient-specific inconsistency. It does not invalidate or solve the main question, and the analogous odd-characteristic construction does behave differently.

The source's phrase about vanishing homology must mean positive-degree or reduced homology. For a connected graph with 2-disks attached, selecting a boundary-vector basis from an H₁-killing family removes H₂ while retaining H₁=0 and not increasing cost. This justifies the packet's field-homology interpretation. No integral analogue of basis extraction is asserted.

## 2. Normalization and weakly fundamental fillings

The closed-walk normalization is correct for both invariants. Cutting a repeated-vertex loop gives a homological sum and a product of conjugates in the fundamental group. Hence replacing a walk by its simple-cycle pieces enlarges the normal closure of the available relators while not increasing total length. The conjugating paths establish the group identity; they are not additional attaching cycles or additional charged length. This is the right direction for proving that every admissible walk filling can be replaced by a cycle filling.

Over F₂, attaching-cycle boundaries span the r-dimensional graph cycle space exactly when the filling kills H₁. Basis extraction therefore gives the minimum cycle-basis characterization. Every homotopy-killing family also kills H₁, so aπ≥a₂ and every such family has at least r cycles. In a simple graph each nonconstant simple cycle costs at least three.

The stated weakly fundamental ordering yields a valid collapse proof. In reverse order, the distinguished edge of the current last disk belongs to no remaining disk. Later-index distinguished edges were absent from all earlier cycles, so earlier attaching circles remain intact. Each disk has an embedded boundary, making the disk-edge pair a genuine elementary collapse. Deleting that edge preserves graph connectivity because it lies on the cycle. After r collapses the remaining connected graph has rank zero. Thus a weakly fundamental basis provides a contractible filling, and a minimum such F₂ basis proves aπ=a₂. This is only a sufficient equality condition, as the packet correctly states.

## 3. Approach 1: Moore complexes and exact odd-torsion costs

### Construction and topology

The specified facets form a genuine simplicial mapping cylinder of the degree-p circle covering, capped by a disk. The a-circle has 3p distinct vertices, the b-circle has three, and each strip's two triangles form the appropriate quadrilateral. No prohibited identification within a simplex occurs. Multiple strips incident with a base edge are permitted in a simplicial complex. Attaching the cone cap consequently produces the degree-p mapping cone, with fundamental group Z/p and integral H₁=Z/p, H₂=0.

Counting vertices, edges, and triangles gives the stated original f-vector `(3p+4, 12p+3, 9p)`. In its barycentric subdivision, vertices are nonempty faces; edges are strict comparable pairs; triangles are three-term chains. The counts `(24p+7, 78p+6, 54p)` and rank `54p` follow. Pairwise comparable faces form a chain, so every graph triangle is indeed a 2-simplex. The subdivided base circle is an embedded six-edge representative of the cyclic generator.

### Short-loop lemma

The barycentric short-loop lemma is valid for arbitrary simplicial complexes. A spur or a monotonically nested face triple can be removed by an explicit homotopy. After these removals, inclusion directions alternate around any nonconstant loop, forcing even length. At length at most five, only two or four edges can remain. Selecting an original vertex in each local minimum and working inside the intervening maximum simplex replaces the loop by an original-complex edge walk of length at most two. Such a walk is constant or a backtrack. This is a homotopy argument, not merely a homology calculation.

Thus no cycle of length below six can detect the cyclic quotient, whereas B does. The same conclusion holds for nonzero mod-ℓ homology when ℓ divides p.

### Exact lower and upper bounds

For odd p, mod-2 acyclicity and exactly r triangles show that the triangle boundaries form an F₂ basis. Therefore a₂=3r. Any homotopy-killing family must contain at least r cycles and at least one cycle with nontrivial image in Z/p. If all projected relators were trivial, that quotient would survive. Hence every alternative family costs at least `3(r−1)+6`, including families with more than r relators.

The matching upper construction is also valid. Remove one cap triangle but retain all its edges. A dual-tree collapse removes each other cap triangle across a free interior edge toward its already removed parent. Boundary edges are never removed. The final connected rank-one graph contains the full cap boundary; all extra edges form attached trees and can be pruned. This remains correct if the omitted triangle meets the disk boundary: preserving boundary edges, rather than calling the remainder an ordinary annulus, is the essential point. The collapse extends over the attached cylinder because it fixes that boundary. The remaining complex has the homotopy type of the base circle, which is killed by the extra B disk.

The exact accepted formulas are therefore `a₂(G_p)=162p` and `aπ(G_p)=162p+3` for every odd p≥3. In particular, p=3 gives 486 and 489. For p=2 the rank defect over F₂ forces the same six-edge obstruction for homology, and both costs are 327. The ratio of the odd family approaches one, so this is not a positive solution of the unbounded-ratio question.

## 4. Approach 2: sums, subdivisions, and RP²

For a bridge-tree join or articulation sum with no new cycles, every simple cycle stays in one summand. Homology splits as a direct sum and the fundamental group as a free product. Since the relators lie in individual factors, the filled group is the free product of the separately filled groups; it is trivial precisely when each factor is trivial. This proves exact cost additivity for both invariants, rather than only an upper estimate. Their ratio is the corresponding a₂-weighted average, with zero-cost tree factors irrelevant.

Uniform L-fold subdivision produces a bijection of simple cycles and multiplies every cost by L. The graph homeomorphism preserves both relevant killing conditions. Thus subdivision preserves ratios exactly. Iterations of these operations cannot amplify uniformly bounded ratios. Fixed p=3 bridge sums have additive gap 3k and constant ratio 163/162; their maximum degree is uniformly bounded because only a fixed number of bridge incidences is added to each fixed finite summand.

For any simplicial RP² triangulation, Euler characteristic gives f₂=r. Every F₂-killing family needs r cycles and at least one whose image in RP² is nonzero, hence cost at least `3(r−1)+s`. Removing one open face gives a Möbius band containing the entire original graph. A simple curve nonzero mod 2 in RP² is a one-sided essential curve in that band and represents a generator of its infinite cyclic fundamental group. The classification of embedded curves in a Möbius band justifies this primitive-generator claim; odd winding alone for a nonembedded walk would not suffice. A curve running along some boundary edges can be pushed slightly into the surface before applying that classification.

The remaining r−1 face disks and the shortest essential curve therefore kill π₁, proving `a₂=aπ=3(r−1)+s`. This also covers s=3. Over an odd-characteristic field the r triangular boundaries instead form a basis and a_F=3r, giving the stated coefficient contrast when s>3. The primary-source criticism is accordingly supported, with the narrow interpretation already noted above.

## 5. Approach 3: maximum-degree-three reduction

The vertex trees with labeled ports and disjoint length-L external paths give a connected simple graph of maximum degree at most three. Contracting the vertex forest, followed by undoing subdivisions, is a graph homotopy equivalence. The original and expanded cycle ranks agree.

A simple original cycle uses each vertex tree at most once, so its lift is simple and has length between L|C| and (L+D)|C|. The induced isomorphisms preserve the two killing conditions separately, establishing both upper bounds without identifying homology spanning with normal generation.

Conversely, an expanded simple cycle cannot be contained in the vertex trees. Degree-two internal vertices force each used external path to be traversed in full. Its projection can revisit an original vertex; it must therefore be treated as a closed walk, not silently as a simple cycle. The normalization from Section 0 gives simple-cycle replacements of total original length at most |Z|/L. In homology these classes contain the projected span. In the fundamental group their normal closure contains each projected relator and therefore the full normal closure of the original killing family. This proves both lower bounds for all admissible families:

`L aτ(G) ≤ aτ(H_L) ≤ (L+D)aτ(G)`, for τ=2,π.

The displayed ratio squeeze follows by using the lower numerator with the upper denominator and vice versa. With G fixed, D is fixed and L tends through positive integers to infinity. Thus every original ratio is approximated by subcubic ratios. Since subcubic graphs are themselves a subclass, the extended-real suprema are equal. This is a valid equivalence of unboundedness questions, not a construction of unbounded ratios. The packet correctly does not promise a size-efficient reduction.

## 6. Approach 4: field homology and quotient obstructions

For a triangular complex with H₁(X;F₂)=0, its face boundaries span the graph cycle space. Selecting r faces gives a₂=3r even if there are more than r faces. A homotopy-killing family projects to a spanning family in H₁(X;Fℓ), so at least d of its cycles have nonzero images. Each costs at least s; the total family has at least r cycles. Since s≥3, every alternative relator family has cost at least `3r+d(s−3)`. The proof does not rely on one chosen presentation.

The sufficient family criterion follows immediately by dividing by 3r. The covering-space specialization uses the exact graph-rank identity `r_n=N_n(r_0−1)+1`. With a fixed base, this rank is at most a constant times the number of sheets; together with d_n bounded below linearly and s_n tending to infinity, the criterion forces unbounded ratios. The hypothesized simultaneous cover properties are not constructed or asserted to hold. If a degenerate base had r₀≤1, those same hypotheses could not supply such an infinite family; no positive conclusion is smuggled in through that case.

For a **nontrivial** finite quotient Q, the projected relators must normally generate Q. At least ν(Q) have nontrivial images, and each costs at least s_Q. Thus the auxiliary bound ν(Q)s_Q is valid after the supplied qualification. The warning that large simple quotients need only one normal generator is correct. Neither group size nor perfectness alone yields the desired metric lower bound.

## 7. Approach 5: deletion upper bounds and planar equality

Every cyclic edge is present in some vector of every F₂ cycle basis, so W≤a₂. The crude aπ≤rW bound follows from spanning-tree fundamental cycles in the bridge-free components.

For the stronger bound, delete bridges, suppress degree-two paths with their exact positive integer weights, and treat pure-cycle components separately. Each remaining noncycle component is a multigraph of minimum degree at least three, with loops and parallel edges allowed. Its vertex count satisfies N≤2r′−2≤2r−2. If it is simple, the stated breadth-first ball count ensures a cycle with at most `k(r)=2 ceil(log₂(2r))+1` suppressed edges; loops and parallel pairs already give shorter cycles.

Choosing the heaviest edge on that short suppressed cycle bounds the lifted cycle's length by k(r) times the retired path's length. The lifted cycle is simple, including the loop and parallel-edge cases. Removing one edge of the retired path lowers cycle rank by one; the rest of the path becomes dangling and can be pruned without changing rank. Its interior vertices had no other attachments. Pure-cycle retirement also lowers rank by exactly one.

Retired paths are disjoint and consist of originally cyclic edges. Their charges sum to at most k(r)W. The recorded cycles, in reverse order, are weakly fundamental because each contains a retired edge absent from all subsequently constructed cycles. There are exactly r of them. This proves aπ≤k(r)W and aπ/a₂≤k(r), with rank one correctly handled separately. Deleting bridges for bookkeeping does not lose a group relation: they carry no graph homology and only join the free factors.

For planar graphs, filling bounded facial boundary walks gives the elementary bound aπ≤2W; repeated vertices in facial walks are harmless because of the established normalization. The stronger equality already present in the final packet is also correct and appropriately credited. The cited survey's Theorem 5.34 supplies a minimum rational cycle basis that is weakly fundamental for every planar graph in its undirected weighted-graph framework, hence in particular for the finite simple unweighted graphs here. An oriented F₂ basis has an odd, hence nonzero, determinant in fundamental-cycle coordinates, so it is rationally independent. The rational minimum is at most the binary minimum. A weakly fundamental rational basis is also an F₂ basis, giving the reverse inequality; its collapse filling then gives aπ=a₂.

The relevant inspected author survey is:

Telikepalli Kavitha, Christian Liebchen, Kurt Mehlhorn, Dimitrios Michail, Romeo Rizzi, Torsten Ueckerdt, and Katharina A. Zweig, *Cycle Bases in Graphs: Characterization, Algorithms, Complexity, and Applications*, August 25, 2009 author version, subsequently *Computer Science Review* 3 (2009), 199–243. DOI: https://doi.org/10.1016/j.cosrev.2009.08.001 . Author PDF: https://www.mpi-inf.mpg.de/~mehlhorn/ftp/SurveyCycleBases.pdf . The inspected PDF is 2,546,952 bytes, SHA-256 `6564614ce0bd88a982707f993406716c58277d5108ebc690fee759a0e94e3413`.

Its Theorem 4.4 expressly attributes the logarithmic weakly fundamental construction to Rizzi (2007), and the preceding paragraph credits the presented proof to Kavitha and Rizzi. The packet reproduces this credit and claims no novelty for the deletion mechanism or logarithmic order. Theorem 5.34 supplies the planar structural conclusion used above. The packet's explicit cycle-rank constant and cyclic-edge bookkeeping are justified directly, not falsely attributed as the exact wording of the prior theorem.

## 8. Reproduction and genuinely independent finite controls

### Reproduction of the authored controls

The three original scripts were copied before running, so their ordinary output-writing behavior did not alter the frozen inputs. All three reruns passed. Their CHECK_RESULTS.json, DEGREE_RESULTS.json, and DELETION_RESULTS.json outputs are byte-identical to the pinned originals.

- Moore controls: p=2,3,5,7,9; field ranks, exact terminating presentation reductions, and short-cycle cocycle checks.
- Degree controls: 17 graphs, 51 expansions, 222 expanded cycles, including 21 nonsimple projected walks, and 51 trivial-presentation certificates.
- Deletion controls: 61 graphs and 340 rank-reducing deletion steps, with simple recorded cycles, disjoint valid charges, reverse weak fundamentality, and trivial-presentation certificates.

The checker code was inspected. Its formula-valued cost fields were not treated as independently computed optima, and the Tietze routine was not treated as a group-triviality algorithm that always terminates successfully.

### Auditor-written controls

`independent_checks.py` imports no author checker. It uses different face numbering, a different spanning tree, a different elimination order, exact integer determinants, explicit Tietze/Nielsen transformations, and independent short-cycle enumeration.

For p=2,3,4,5,6,9 it verifies the construction counts, original integral relation determinant of absolute value p, barycentric field ranks, the full cyclic presentation, a once-punctured free cyclic presentation, and the trivial presentation after adjoining B. With the alternative spanning tree, single-occurrence elimination alone stalls on some two-generator presentations; a length-decreasing Nielsen automorphism supplies a valid additional algebraic step. No inference from the stalled calculation or abelianization was substituted for a group certificate.

For p=2 and p=3, respectively, it enumerates all 1,980 and 3,313 simple cycles of length at most six. Greedy linear-matroid basis selection over this complete length prefix reaches full rank and gives the exact binary optima 327 and 486. Because all cycles up to the largest selected length were enumerated, longer cycles cannot reduce those costs. Reduction modulo the triangular span finds shortest nonzero quotient-homology length six. Combining that universal-relator lower obstruction with the independently reduced explicit upper presentations certifies aπ=327 and 489. This is an optimum certificate for these two finite examples, not a brute-force enumeration of all normal-generating families.

The same script checks every possible omitted small cap triangle for p=2 and p=3, totaling 36 and 54 choices. Free-edge collapses preserving all boundary edges terminate in the boundary circle with attached trees, and leaf pruning leaves exactly that circle.

`independent_graph_checks.py` uses only auditor-written primitives. It checks all connected positive-rank labeled graphs on three or four vertices and one degree-four articulation example: 24 cases and 48 tree/path expansions at L=1,3. Exact binary optima satisfy both degree-reduction inequalities. All 88 expanded simple cycles obey full external-path traversal and the projected length bound; two project nonsimply, confirming that case is actually exercised. Lifted fundamental families have exact trivial-group certificates. The auditor did not independently compute general aπ optima for these expanded graphs.

All finite tests supplement the reviewed symbolic proofs. None proves a universal statement by sampling, and none supplies the missing unbounded family.

## 9. Remaining gaps and publication interpretation

The accepted packet contains no sequence with aπ/a₂ tending to infinity and no universal constant bounding that ratio. More specifically:

1. The explicit torsion examples have ratio 1+1/(54p), decreasing to one.
2. Sums and uniform subdivisions preserve bounded ratios; the additive gap alone does not answer the question.
3. Degree reduction transfers a ratio but does not make it large.
4. The homology/systole route lacks a family satisfying its simultaneous quantitative hypotheses.
5. The logarithmic upper bound permits either boundedness or slowly growing unboundedness.

The source-gate and inherited-search narratives are appropriately bounded statements by the author. This review checked the primary target, the displayed coefficient, the invoked prior-method and planar theorems, the mathematical proofs, the full frozen packet, and the reported finite controls. It does not independently certify that every relevant current paper or inherited corpus entry has been found.

The publishable mathematical conclusion, if publication is separately authorized, is an independently audited partial investigation with the supplied nontrivial-quotient qualification. Preserve the prior-method credit, the restricted coefficient-specific source observation, and the unresolved 5/5 disposition. Do not present it as a solution, a novelty certification, or a general algorithm for group triviality.
