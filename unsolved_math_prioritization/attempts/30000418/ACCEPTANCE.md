# Acceptance of an eleven-vertex tree list-labeling counterexample

## Decision

Accept the full negative answer and exact values without mathematical correction:

    chi^(2,1)(T) = 5 < 6 = chi_l^(2,1)(T).

The ordinary parameter counts the smallest initial-segment palette {1,...,k}; its conventional zero-based span for this tree is 4. The list parameter is the least cardinality guaranteeing a labeling from every assignment of arbitrary lists of that size. On edges labels differ by at least 2; at graph distance two they differ. The example therefore answers Kohl's stated universal tree-equality conjecture negatively under its actual definitions.

This AI-assisted manuscript is unrefereed. Acceptance records an independent internal AI audit, not external human peer review, journal acceptance, or formal proof-assistant certification.

The stated universal tree-equality conjecture is answered negatively. No historical novelty, priority, minimal-order, exhaustive-literature-review, or current-openness claim is made.

## Complete accepted construction and proof

The spine is a–b–c–d–e. Attach two leaves a1,a2 to a, one leaf b1 to b, one leaf d1 to d, and two leaves e1,e2 to e. There are 11 vertices, 10 edges, maximum degree 3, radius 3 and diameter 6. Let A={1,2,3,4,5} and B={1,3,4,5,6}. Give A to every spine vertex and to b1,d1; give B to a1,a2,e1,e2. Every list has five elements, and the source permits noninterval lists such as B.

The three A-list neighbors of b force b into {1,5}, because an interior label in A has only two A-values differing by at least 2. The same holds at d. Their distance-two constraint forces opposite labels, and c=3. If b=1,d=5, then a is 4 or 5. At a=4 both a-leaves are forced to 6; at a=5 both are forced to 3, since their distance-two constraint with b excludes 1. Either alternative violates their mutual distance-two constraint. For the reverse orientation, the identical argument applies at e. Thus this five-list assignment is impossible.

The ordinary witness assigns the spine (1,5,3,1,5), a-leaves (3,4), b1=2, d1=4, and e-leaves (2,3). Every edge has difference at least 2 and every neighbor set has distinct labels. A degree-three vertex cannot be labeled from the common four-palette because it has at most two sufficiently separated palette values for its three distinct neighbors. The exact ordinary palette size is therefore 5.

For arbitrary lists of size Delta+3 on any finite tree, process vertices in breadth-first order. A non-root vertex has only its parent as an earlier neighbor, excluding at most three integer values. Its earlier distance-two vertices are its grandparent and earlier siblings, at most deg(parent)-1<=Delta-1. At most Delta+2 values are forbidden; a list of Delta+3 distinct values always leaves a choice. The root is immediate. For Delta=3 this proves the exact list value is 6. The isolated-vertex and single-edge cases are audited separately; no false isolated-vertex degree lower bound is used.

Attach independent pendant paths beyond any of the six leaves. The ordinary witness extends because each new vertex sees only its parent and grandparent among earlier vertices at distance at most two, excluding at most four labels of A. Distances among the original vertices do not change; their bad lists remain an obstruction. Maximum degree stays 3. Both exact values persist, giving an infinite family with unbounded diameter.

For an n-vertex graph with k-element integer lists, rank-compress the union of at most nk labels. Any valid compressed labeling lifts to an original labeling: original positive differences are at least rank differences. Therefore every bad original assignment has a bad representative on {1,...,nk}. The reverse feasibility implication is not claimed, nor is exhaustive enumeration of this finite universe.

PROOF.md contains the full accepted proof and certificate recurrence. AUDIT.md retains the full nine-part independent logical review, both orientations of the contradiction, complete edge and distance-two constraints, all boundary cases, and the source scope. The construction itself is mathematical proof content and has not been suppressed as data.

## Source and historical verification limits

Kohl's OWR Report 7/2006, printed pages 414–416, uses arbitrary lists and states the universal conjecture as Conjecture 4. The 2006 dissertation, printed page 124, confirms the palette-size versus span convention and repeats Conjecture 4.4. The historical special-family results do not cover this Delta=3, radius-3 tree with four degree-three vertices. In particular, the caterpillar theorem requires Delta>=4 with specified major-vertex separation. The ordinary-span algorithm of Hasunuma, Ishii, Ono and Uno provides no all-list theorem and is not used as one.

Independent historical exact enumerators agreed on the bad-instance and ordinary-palette counts. All 258 candidate states, including 63 Hall-deficient states, were checked as data by separately authored code; candidate scripts were neither run nor imported by the audit. The audit checked 16,954 greedy runs over all labeled trees through order 6 and all roots with two list patterns, 1,000 further deterministic random cases, and 860 pendant-path extension vectors. These finite checks support the proof and do not establish an all-list theorem by themselves. Saved independent outputs agree byte-for-byte across normal Python, -O and -OO; candidate outputs differ only in their explicit optimization field. No mathematical program was rerun during preparation.

The complete human-readable proof, explicit graph, bad lists, ordinary labeling, infinite family and logical audit are retained. This is not a computational reproduction package: raw state tables, Hall-certificate datasets, enumeration tables, executable code, copied source documents and images, and private coordination material are omitted. Historical counts and hashes are supporting metadata. The historical computations cannot be reproduced from this edition alone; all mathematical conclusions rest on the written proofs.

SOURCES.json records public citations, PDF hashes and sizes, and bounded historical retrieval and inspection. ACCEPTANCE.json binds the exact distributed proof, audit and acceptance note. Hashes authenticate bytes and recorded matches; they do not by themselves certify mathematical truth.
