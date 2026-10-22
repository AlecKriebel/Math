# Independent full five-turn review: PASS within scope

Problem30003973 / OWR-16627-005. All five proofs and both finite certificates were read. No mandatory correction was found. The original unrestricted2-to3 Ramsey-equivalence implication remains unsolved5/5. The abstract counterexamples and restricted-host collision are not target counterexamples.

## Exact source

The original Clemens contribution and Question6 on printed2736 were checked; the question page was visually inspected. The definitions concern ordinary monochromatic subgraph copies and equality of all finite Ramsey-host classes/minimal families. The reported additive/even-color and nested-target results agree with the cited primary statements and the additive proof. No equality of numerical Ramsey numbers, induced-copy condition or bounded-host scan is substituted. The related30004035 repeats the2-to3 question and adds other variants; only the exact overlap should be skipped later.

## Turn1: isolates

Ordinary copies allow unused ambient edges, so extending a monochromatic core with arbitrary extra vertices proves the padding identity. Isolate-free cores cannot use new host isolates. Padding arbitrary hosts establishes necessity of universal core equivalence, and complete hosts establish the exact max(order,Ramsey-number) cutoff. The edgeless cases and color monotonicity are handled correctly. Hence padding cannot create a forward counterexample. The P3 example is correctly only reverse-direction behavior.

## Turn2: color-family algebra

Keeping the spanning vertex set fixed handles isolated targets. Downward closure permits disjointification of unions, so family powers encode avoiding colorings exactly. The extra mixed inclusion gives equality of cubes by two opposite containments; it is not inferred from equal squares. The graph translation has the correct direction of the asymmetric arrow condition.

In a putative3-color separator, every H-free recoloring of two H'-free classes forces each crossed union with the third class to be2-Ramsey. This gives both target incomparability and the edge-count lower bounds with all quantifiers preserved. The five-element abstract example refutes only automatic mixed inclusion and indeed has equal cubes.

## Turn3: abstract obstruction

The facet closures and their union powers were independently expanded: the squares agree, A cubed is the full power set and B cubed omits precisely the full ground set. The direct triple-cover argument is valid even with repeated facets. The stated minimal forbidden pairs and triples are genuine. A single graph target's avoidance family on a fixed host has uniform minimal forbidden edge cardinality whenever copies exist, so neither abstract family directly realizes such a target. Equality on one ground set would in any event not establish universal host equivalence. No unretained optimizer certificate or minimality-of-seven claim is used.

## Turn4: star forests

A monochromatic host star supplies at most one nontrivial target component, including when that component is K2. Sorted capacities characterize ordinary star-forest embedding. Deficient thresholds give the quota obstruction; conversely quotas allocate each forced host component to one color and distribute all remaining edges below the other thresholds. The lattice-downset sum and row maxima correctly convert this to the all-size canonical host, including repeated component sizes and zero horizontal capacities.

Universal equivalence forces the other core to be a star forest by testing the canonical host, but equal canonical profiles are not asserted sufficient for arbitrary hosts. The separate star and matching rigidity arguments use actual universal Ramsey witnesses. Their isolate-padding classification is relative to the bare core and is consistent with the earlier cutoff result.

## Turn5: rejected candidate and minimal separator

The q-fold sum of{0,1,3,4} is the full interval for q>=2, proving the two targets have identical restricted canonical profiles at every such q. For a triangle component the exact two-color capacities are(2,0),(2,1),(1,2),(0,2); it cannot hold two vertex-disjoint nontrivial target components. The extended quota criterion is therefore valid.

The53-vertex,45-edge host satisfies all ten H-threshold equalities. Its displayed H'-avoiding coloring has the stated component capacities. Every star-edge deletion loses one forced component at its designated threshold, and every triangle-edge deletion loses one at(2,2). Absence of isolated host vertices then promotes edge-minimality to all-proper-subgraph minimality. This disproves the restricted-host recognition shortcut: the pair is already2-nonequivalent and thus cannot answer the original implication.

## Validation and disposition

All44 manifest-bound author files, five historical manifests and four source PDF hashes verify. The five author outputs replay byte-identically, totaling198,182 assertions. A separately written checker passes942 controls, including893 direct-edge-coloring comparisons with the threshold criterion on small star/triangle hosts, all45 explicit deletion colorings and independent expansion of the abstract square/cube pair. Its copied certificate is an unchanged portable input from the frozen author packet. These controls supplement the all-size proofs and do not certify universal2-equivalence of any new pair.

Publish original unsolved5/5, preserving frozen files and adding this review. The mixed asymmetric condition is still an extra hypothesis; the source implication remains open in this work. No novelty, formal-certification or human peer-review claim is supported.
