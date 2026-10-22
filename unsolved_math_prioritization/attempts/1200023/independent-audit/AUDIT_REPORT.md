# Independent audit: AMR-011-0023 / 1200023, rank 638

## Verdict

**PASS as a conservative, reproducible, unsolved research packet.** No blocking mathematical or computational defect was found in the frozen twelve-file submission. Retain `status: unsolved`, `turns_used: 5`, and `full_resolution: false`. This audit does not certify a solution, mathematical novelty, exhaustive literature coverage, or peer review.

The connected locally finite nonunimodular case remains unresolved by this packet. The disconnected union-of-triangles observation is a valid literal-wording control and must not be promoted to resolution of the intended connected problem.

Frozen input:

- Tree SHA256: `06b401911f19d2483353f6d5957359f593f856d0cf24a36b51d32a04efbd1fba`
- Archive SHA256: `3f4ac5aa460f57ed75bd55423c536ac7f6edc528c06fa35aefac1883e66efb93`
- Archive size: 18,470 bytes
- Twelve authored files, exactly matching the freeze receipt and archive members
- Originals were preserved. This audit made no repository or other remote changes.

## 1. Mathematical scope and source check

The primary source was independently opened at [Ábert's author-hosted PDF](https://www.renyi.hu/~abert/questions.pdf), and an independently rendered page 4 from the hash-matching PDF was visually inspected. The target uses the outer vertex boundary, ambient graph distance, arbitrary finite A, and arbitrary basepoint b. Its accompanying note supports the unimodular case only. Connectedness and local finiteness are not explicit in the printed question.

The report correctly separates the customary connected interpretation from the literal disconnected failure. For simple graphs, infinite degree means infinitely many distinct neighbors: removing finite A leaves infinitely many boundary vertices, all but possibly b having weight at least one. Thus reduction to the locally finite connected case is valid. Empty A is immediate.

The [DeVos notes](https://www.sfu.ca/~mdevos/notes/misc/vertex-trans.pdf) were independently opened. Theorem 2 has the stated diameter/outer-boundary content and applies here because an infinite connected locally finite graph has infinite diameter. The stored Lyons–Peres PDF and independently re-extracted relevant passages were checked against the submitted hash and size. Its Theorem 8.7, Corollary 8.8, and equation (8.4) support exactly the weighted/unweighted distinction used in the proof. The web reader rejected this 21 MB book as too large; this audit therefore does not describe that book as independently downloaded anew. The stored document's title page carries the claimed 19 August 2026 version.

The independent search pass did not verify a general later resolution. This is a bounded non-detection, not evidence of definitive present-day open status. The Benjamini–Schramm full article was not independently inspected; the packet correctly limits its own claim to an institutional abstract. Historical repository-search metadata and corpus provenance were not freshly re-queried in this audit, whose scope excluded remote repository operations.

## 2. Geodesic-incidence proof and the endpoint gap

The reconstruction of the already-known unimodular result is valid.

1. In the locally finite case, the number of oriented n-geodesics meeting any fixed finite set is finite. Transitivity makes total vertex incidence N_n uniform. Reversal makes the ending count equal to the starting count M_n without invoking unimodularity.
2. For n greater than the ambient diameter D of nonempty A, no n-geodesic has both endpoints in A. Exactly 2|A|M_n segments have an endpoint in A. Each geodesic has at most D+1 vertices in A, even when A is disconnected.
3. A segment with both endpoints outside A has distinct boundary vertices immediately before its first A-vertex and immediately after its last A-vertex. Their index difference equals their ambient distance because a subpath of a geodesic is geodesic. The number of A-vertices is at most this distance minus one. The triangle inequality through arbitrary b then yields the required boundary-weight bound. No assumption b in A is used; b can be one of those boundary vertices and contribute zero.
4. After summation, replacing the subset of boundary incidences by all boundary incidences is legitimate because weights are nonnegative. The resulting endpoint-error inequality is correct.
5. For the invariant transport counting n-geodesics with prescribed starting and i-th vertices, unimodular mass transport equates incoming and outgoing totals. Summing i=0,...,n gives N_n=(n+1)M_n. Dividing the endpoint-error inequality and taking n to infinity proves the target in that class.

The report does not use this identity in the nonunimodular case. Its sufficient condition liminf M_n/N_n=0 is stated as an unproved extension. The binary grandparent transport's outgoing mass 1, incoming mass 4, and incoming tilt 1/4 correctly expose why deleting the modular factors is invalid. Finite checks of modular ratios do not themselves prove automorphism invariance; that structural fact is supplied by the cited example.

## 3. Diameter and expansion controls

The Babai–Szegedy diameter bound is reconstructed correctly by uniform geodesic incidence; it does not require the unweighted mass-transport principle.

The one-sided ray control is valid: a finite initial interval has a single outer boundary vertex, which can be chosen as b. Its distance sum vanishes while the diameter inequality still holds. This refutes deduction from the diameter estimate alone, not the transitive target.

The directed-orbit expansion count is sound for a transitive directed adjacent-pair orbit of out-degree p and in-degree q. All p|A| arcs leaving vertices of A land in A union its outer boundary; each target has at most q incoming arcs. The resulting lower expansion constant need not be one and does not control the exceptional zero-weight boundary vertex.

The hairy-tree control has positive vertex expansion: if C is its core part and O its leaves whose parents are outside C, then the boundary has at least |C|+2 vertices when C is nonempty, and at least |O| distinct vertices. Combining these lower bounds with |A|<=2|C|+|O| gives the stated 1/3 bound. A single attached leaf with b its parent nonetheless fails the distance-sum inequality. This graph is nontransitive, as disclosed.

## 4. Spanning-tree proposition

The proposition is valid for arbitrary finite nonempty A and every b, without connectivity of A.

Let a=|A|, B its outer boundary in a spanning (q+1)-regular tree, and e_A the number of internal tree edges. Counting all tree edges touching A gives (q+1)a-e_A distinct edges inside the forest induced on A union B. That forest has at most a+|B|-1 edges. Hence |B|>=qa-e_A+1>=(q-1)a+2, because e_A<=a-1. For q>=2 this is at least a+2.

As T is spanning, every member of B remains outside A and adjacent to A in G. Extra edges cannot remove these boundary vertices. Whatever shortcuts extra edges introduce, every distinct boundary vertex other than possibly b remains at ambient distance at least one. Consequently the distance sum is at least a+1.

This genuinely covers the usual q-ary grandfather/grandparent graphs, q>=2, in their shortcut metric. It makes no claim that every nonunimodular transitive graph has such a spanning tree.

## 5. Exact finite-support cut identity

The reduction is correct for every finite support U, including empty or disconnected U, and for arbitrary nonnegative finite vertex weights c. Graph distances are the relevant special case.

A cut with selected a-nodes A has source contribution K minus the sum over A of c(v)+1. Any minimum cut avoids each L-edge because L=K+1 and the empty cut has capacity K. Therefore all z-nodes in the closed neighborhood of A must be selected. The cheapest canonical choice contributes the sum of c over that closed neighborhood. Cancellation of the c-values on A leaves K plus the outer-boundary weight minus |A|. Extra zero-weight z-nodes do not change the value or the selected A. This proves both inequalities in the claimed exact minimum-cut formula.

The submitted implementation constructs the full closed neighborhood using an infinite-graph neighbor oracle. For U=B(b,R), BFS through R+1 includes every relevant boundary vertex and determines its true ambient distance; no induced-ball metric is substituted. Integer capacities, residual cut separation, flow bounds, conservation, and flow/cut equality are checked. Replayed assertions certify all subsets of each declared support simultaneously.

The stored JSON summarizes generated certificates; it does not contain every arc's flow. This is consistent with the report's claim that certificates are generated and checked on replay. No universal theorem follows from these finite supports.

## 6. Independent replay and new checks

All checks in `audit_verify.py` passed under Python 3 with only the standard library:

- Exact twelve-file receipt, tree hash, archive size/hash, and archive-member byte binding.
- Byte-identical replay of `verify.py`; submitted eleven-entry manifest check passed (the manifest excludes itself, while the external receipt binds all twelve files).
- All 31 networks independently rebuilt and re-solved with Edmonds–Karp rather than the submitted Dinic routine. Every minimum deficit was zero.
- Independently encoded regular trees as a distinguished spine with ordinary rooted branches. Their grandfather graph and two-tree horocyclic products reproduce complete neighbor sets and BFS distances through the needed radii. This checks 2,729 grandfather vertices, 1,894 DL(2,3) vertices, and 2,540 DL(3,4) vertices, as well as the line and lattice controls.
- All connected labelled simple graphs with 1–4 vertices: 44 graphs, all supports and all basepoints, 2,538 networks, and 12,657 direct subset-objective evaluations. Both flow algorithms matched brute force, including negative minima in finite graphs.
- All weights in {0,1,2} on C4 and every support: 1,296 networks and 6,561 direct subset-objective evaluations. This independently stresses the closed-neighborhood cancellation and multiple zero-weight vertices.
- Twenty off-center infinite-graph controls across the five models, using basepoints at center distances 0,1,2,3 and every subset of each radius-one support: 3,488 direct subset-objective evaluations, all agreeing with the independent network result.
- Tree-boundary inequality on 1,117 nonempty subsets, covering q=2 at radius 2 and q=3,4 at radius 1.
- Submitted auxiliary totals replayed as stated: 872 small-support subsets, 30,595 interval cases, 15 tree-boundary subsets, three modular ratios, and the disclosed hypothesis-violating controls.

These checks add adversarial support but remain finite tests. The analytic proof review supplies the general conclusions explicitly identified above.

## 7. Clarifications and limits

No correction is required for acceptance at the reported unsolved status. Optional clarifications are listed separately in `CORRECTIONS.md`; none justifies silently changing the frozen artifact.

The five log entries record substantive approach families, not independently timed model turns. The report expressly discloses that convention. The 15% completion figure is a subjective planning estimate and receives no mathematical validation here.

This audit is bound to the exact hashes above. Any changed mathematical file requires a new artifact hash and review of the change. Publication decisions and current repository conflict checks remain outside this read-only audit.

## Reproduction

Place this audit directory beside the unchanged submission directory, freeze receipt, and authored ZIP. Run:

```
python3 -B independent-audit/audit_verify.py /path/to/rank638-1200023 > audit-replay.json
cmp audit-replay.json independent-audit/AUDIT_RESULTS.json
```

The audit script consumes only the authored packet and public freeze metadata. It neither needs nor reads scholarly PDFs, extracted source text, public corpora, private coordination material, or network resources.
