# PR1211 mathematical and original-source scope adversary

Review completed 2026-10-17 UTC. Assignment completion estimate: 100% for mathematical correctness and original-target scope; no exhaustive priority audit attempted.

**Disposition:** The eleven-vertex construction proves the stated counterexample and exact values. I found one explicitness defect in the retained supplementary DP recurrence. The parent's proposed domain-guard clarification repairs it. I also confirmed a bibliographic page-range correction: the mathematical text is on printed pp.414–416, but the complete OWR contribution includes references continuing onto p.417.

## Identity and independence boundary

Reviewed immutable head: `d96c9fca74195a8706fd9481eeb35a4c3c0d384c`.

- Submitted `PROOF.md`: SHA256 `2037b27ff80f81551008000c07aee5e7bb8cb27d957c15170790015509ecbea4`.
- Submitted `AUDIT.md`: SHA256 `cc974ae5570248c62b0cc5886c7233dc34b50ff5d0779c5a1768dffc9c3c18be`.
- Submitted `SOURCES.json`: SHA256 `9a8c3fa549b2a26e8433749cb98bd9c491c40b907c7b55584e5bb3c33cbf2f1f`.

Read-only `git show` independently matched these three files to the pinned commit; see `IMMUTABLE_BINDING_CHECK.json`. I read the candidate, so this is not a blind review. I did not read another review family's work. Historical acceptance, computational counts, and source-inspection assertions were treated as claims, not evidence for themselves. I wrote and executed only my own checker from the explicit graph and definitions. No submitted code/certificates were executed or imported, no Git writes or external mutations were performed, and no other individuals were contacted.

## Exact strongest verified result

Let T be the path a-b-c-d-e with leaves a1,a2 attached to a; b1 to b; d1 to d; e1,e2 to e. The graph has 11 vertices, 10 edges, maximum degree 3, diameter 6, radius 3, and 13 unordered distance-two pairs. It is a tree and a caterpillar.

For ordinary labels from the common initial segment {1,...,k}, T has optimum k=5, equivalent to zero-based span 4. For arbitrary k-element positive-integer lists, the least universal k is 6. Thus the exact result is ordinary palette parameter 5 < arbitrary-list cardinality parameter 6. It disproves the historical universal tree equality under its actual quantifiers.

All finite trees obtained by independently appending any nonnegative finite path length beyond each of T's six original leaves have the same two exact parameters. The result includes infinitely many nonisomorphic trees and unbounded diameter.

## Proof verification

The obstruction argument is complete. All three neighbors of b have A={1,2,3,4,5}; pairwise distance two forces their labels distinct. A center labeled 2,3,4 has only two A-values at distance at least two. Consequently b,d are the two different values 1,5, and c=3. In the orientation b=1,d=5, a can only be 4 or 5. From B={1,3,4,5,6}, the two a-leaves then have the same singleton allowable set: {6} or {3}, respectively. Their mutual distance-two inequality gives the contradiction. The other orientation is the reversal automorphism, preserving the lists; alternatively the identical contradiction occurs at e. No unstated label-complement symmetry is used.

The ordinary witness checks all 10 edge constraints and 13 distance-two inequalities. With four consecutive palette labels, every possible center value permits at most two separated neighbor values; any degree-three vertex excludes a four-palette labeling. Monotonicity of the universal list property follows by selecting sublists, so the one bad five-assignment establishes the lower bound 6.

The six-list proof is a genuinely arbitrary-list theorem and is self-contained. Under breadth-first labeling, the previously labeled vertices constraining a nonroot vertex v are precisely its parent p, plus already labeled members of N(p)-{v}. The parent excludes at most three integers; the latter set excludes at most deg(p)-1 further integers. This gives at most Delta+2 forbidden values. A (Delta+3)-element list therefore supplies a choice, regardless of overlap, gaps, magnitudes, or sign of the integer labels. No central difficulty is transferred to an external theorem.

Boundary cases are sound. The isolated vertex has both exact parameters 1; its loose Delta+3 upper bound remains valid. A single edge has both exact parameters 3 (not 4); the general upper bound is simply loose. The Delta-2 sibling branch cannot arise in a maximum-degree-1 tree with a nonroot parent having a child, so there is no negative-count case. An empty graph has its unique empty labeling if that convention is permitted. The argument requires finite trees and distinct list elements, exactly as stated.

Each pendant extension step sees only its parent and grandparent among already assigned vertices at distance at most two. These exclude at most four of the five common palette values. Different appended paths' new vertices have mutual distance at least four, including when their original leaves share a parent. Appending paths cannot shorten old distances and preserves maximum degree 3. Therefore restriction preserves the bad assignment, the ordinary witness extends, and the six-list theorem applies. Nonisomorphism and unbounded diameter follow by lengthening just one path.

The rank-compression argument has the correct direction. If the ordered label union is x1<...<xm with integer entries, then xj-xi >= j-i. Hence any labeling after replacement by ranks lifts to an admissible original labeling. An original bad assignment therefore compresses to a bad assignment with m<=nk. The converse enumeration claim is then correct. Feasibility need not survive compression: K2 with both lists {1,3} has two solutions, but both rank lists {1,2} have none. Zero vertices makes the bad-assignment assertion vacuous; no exhaustive all-list test is claimed.

## Actionable recurrence finding and evaluated repair

Submitted `PROOF.md` line66 says feasibility is exactly an SDR of child-label sets without explicitly stating the local state domain. The literal rule over unrestricted triples is false: a leaf state with parent label p=1 and own label q=1 has no child sets, hence an empty SDR, but violates edge separation. Likewise q outside L(v) cannot be feasible. This does not affect Sections1–5, the exact values, the infinite family, or Section7.

Minimal repair: before applying the child test, require q in L(v), and for nonroot v require p in L(parent(v)) and |p-q|>=2; invalid local pairs are infeasible. At the root require p=null and omit the parent-edge test. For a valid local state, each child w may use r with Fw(q,r)=true and r!=p, and child labels must be distinct. This condition is necessary and sufficient by induction: the only cross-child-subtree constraints are between the two child roots; all other such pairs have distance at least three. Leaf feasibility is exactly the local condition.

After completing the original-file checks, I examined the parent's proposed `repairs/PROOF.md`, SHA256 `884db1d388a3528bd197b0346d2ea8586fe76993edb82ab93876f41b51d7a95e`. Its sole change adds exactly these guards and correctly resolves the finding. The historical counts 133 bad-instance states and 125 common-five states also independently equal the counts of locally edge-compatible states at root a. This supports the interpretation that the original issue was an omitted explicit domain, not a failed obstruction or failed historical algorithm. It does not authenticate omitted historical certificates.

If retaining the recurrence in another public file, make the same domain convention explicit there, including `AUDIT.md` line108. Rebuild any changed public hashes/manifests; this review does not authorize treating a changed proof as byte-identical to the submitted one.

## Original-source scope

I freshly downloaded and visually read [OWR7/2006](https://ems.press/content/serial-article-files/46037?nt=1), printed414–417 (PDF36–39), and [Kohl2006](https://webdoc.sub.gwdg.de/ebook/dissts/Freiberg/Kohl2006.pdf), printed124–130 (PDF128–134). OWR explicitly uses arbitrary natural-number sets of equal cardinality, universal over assignments, with common {1,...,k} for the ordinary parameter. The conjecture is on416. Dissertation124 defines chi=lambda+1 and repeats the equality. The positive, noninterval B-lists are allowed; no interval-only theorem is established here.

The dissertation's special families do not contain T: its radius is3, it has four branch vertices, and the caterpillar theorem's alternatives require Delta4/separation4, Delta5/separation3, or Delta>=6/separation2. Its ordinary Delta+3 route is irrelevant because T's ordinary value is Delta+2. Full OWR bibliographic range is414–417 because references continue on417; use414–416 only as a locator for the mathematical text. These checks concern hypotheses and definitions, not a full audit of those sources' proofs.

The [0810.0906 abstract](https://arxiv.org/abs/0810.0906) expressly optimizes labels in {0,...,k}. That is ordinary span. It supplies no arbitrary-list theorem used here. I did not audit that paper in full or conduct an exhaustive later-literature/priority search.

## Reproducible quantitative evidence

Run `verify_independent.py`; it uses the standard Python library and writes `INDEPENDENT_CHECKS.json`. Its global search builds constraints from shortest-path distances and does not use Hall certificates or the submitted state tables. A separately implemented guarded tree recurrence agrees with it for all11 possible roots.

| Check | Result |
| --- | --- |
| Exact solution counts: bad lists / common4 / common5 / common6 | 0 / 0 / 8 / 6336 |
| All labeled trees of orders1–6, every root, three list patterns (dense, sparse noninterval, deterministic random) | 1,442 trees; 8,477 rooted cases; 25,431 successful greedy runs |
| Independent path-extension vectors | All4^6 lengths0–3 plus3 uneven/long controls; 4,099 cases; maximum611 vertices |
| Rank direction over all8 labeled graphs on3 vertices and all2-list assignments from1–5 | 8,000 cases; 1,588 original bad cases remain bad; 5,461 compressed feasible witnesses lift |
| Single-edge3-list assignments from1–6 | All400 feasible; common2-lists infeasible |
| Empty graph / singleton with one arbitrary label | One solution each |

These bounded checks corroborate the deductions. They do not prove minimality, general interval-list equivalence, priority, current openness, or omitted certificate history. No mathematical gap remains in the core counterexample after the stated domain clarification; bibliographic precision and updated changed-file bindings remain packaging tasks.
