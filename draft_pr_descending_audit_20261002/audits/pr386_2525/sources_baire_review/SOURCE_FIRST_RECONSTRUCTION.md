# Source-first reconstruction (recorded before candidate mathematics)

Recorded UTC: 2026-10-03T01:24:42.474460+00:00

Exact review target: PR386 head `76d804cffb0cdbd2c88416dad1ead6e2a89989d6`.

This record was written after inspecting only the candidate source manifests, obtaining independent primary sources, and reading their relevant pages. No candidate Turn5 proof, current result, or old final-review verdict has yet been read.

## Exact original question

Kourovka Notebook 21st issue, October2026 maintained main PDF, printed/PDF179, problem21.16 asks whether a group can have finite width for every generating set in the group sense and fail finite width for some generating set in the monoid sense. The individual width bound may depend on the set. No countability, topology, measurability, or uniform bound over all sets occurs. The maintainer home currently links to exactly the October2026 URLs in the candidate manifest. The target has no solved mark or AI proposal mark; an updates-only full-text search for21.16 has no hit. This is evidence of current maintained listing, not a universal proof of unsolvedness.

Use identity padding throughout. Define `CB(G)` as: every set X with `<X>_grp=G` has `sup_g length_(X union X^-1)(g)<infinity`. Define `MB(G)` as: every set S with `<S>_mon=G` has `sup_g positive_length_S(g)<infinity`. A proper positive cone which merely group-generates G cannot witness failure of MB.

## Bergman source scope

Independently retrieved arXiv math/0401304, exact hash match; its margin says v2/27May2005 and displayed manuscript date30September2018. This is the preprint cited by the2006 published paper, not a downloaded typeset2006 version. Read/visually inspected pages4–6. Condition(3) is absence of a proper countable increasing subgroup cover; condition(4) is CB. The proof on page5 establishes CB plus(3) implies MB by intersecting forward and backward bounded word balls. Question9 asks both whether CB without(3) can fail MB and whether such groups can satisfy MB. Lemma11’s proper monoid in Sym(Omega) group-generates in three signed factors; it is deliberately a warning that group generation does not imply monoid generation.

## Rosendal scope and independent reconstruction

Independently retrieved the author-hosted Property(OB)10.pdf, exact manifest hash match. Read/visually inspected pages4,8,9, including Definition3.5, Theorem3.6 and Proposition3.9. The paper states compact *Polish* groups are topologically2-Bergman for increasing exhaustive sequences whose members have the Baire property. This directly supports compact Polish analytic-generator applications. It does not by itself state all abstract generators are bounded.

Independent mechanism: in a Hausdorff compact group, if increasing exhaustive B_n each have the Baire property, some B_a is comeagre in a nonempty open V f. Choose symmetric identity-neighborhood U with U^2 contained in V and finite cover G=union g_i U. Exhaustivity and Baire category give an index b>=a such that B_b is nonmeagre in each g_i U, then nonempty open W_i contained in g_i U where B_b is comeagre. Pick h_i in W_i. Each g_i U is contained in h_i V, so the h_i V f cover G. For any x in W_i V f, W_i intersect x(V f)^-1 is nonempty open. Two comeagre sets B_b and xB_b^-1 meet there, giving x in B_b B_b. Thus G=B_b B_b. No symmetry of B_b is required. The independent proof uses products, not differences; it generalizes the source’s Polish statement to compact Hausdorff groups via their Baire property.

For an analytic S in compact Polish G, each (S union {1})^n is analytic (finite products and continuous images preserve analyticity), hence has the Baire property. Algebraic monoid generation makes these balls exhaustive; the product theorem gives a finite positive bound. Baire property of S alone does not automatically propagate through continuous multiplication to every word ball.

## Other source scope established so far

Khelif2006 exact four-page announcement retrieved and read. It explicitly says full demonstrations will appear later and gives brief indications. Its index2 counterexample separates CB from strong Bergman; Theorem10 excludes countably infinite groups embedded in compact groups from CB. Neither solves21.16. JOO arXiv2206.10712v2/29April2023 exact retrieved bytes establishes an unbounded Cayley graph for countable MIF groups, and records the unrestricted countable Cayley-graph question as historical open. This is narrower than the present all-cardinal CB-versus-MB target and is not a2026 status authority.

Maltcev thesis PDF requested independently from the primary repository; first request503 and subsequent requests time out. Its source/provenance audit remains explicitly pending. No conclusion below will rely on its uninspected statements until its content is obtained.

## Provisional falsification controls, before candidate

1. Remove identity padding: lengths in C2xC3 with a single Cartesian pair do not equal coordinate maximum; common exact word lengths require congruence compatibility.
2. Unbounded factor widths: S_i={0,1} in additive C_(i+2) gives element (i+1)_i in the full product requiring unbounded positive lengths. S=product S_i is therefore not an abstract monoid generator.
3. Remove closedness from inverse-limit recovery: dense subgroup Z in Z_2 maps onto every finite quotient; its one-step quotient width is1 while nonintegral2-adics are never reached.
4. Replace algebraic generation by topological generation: {1} densely generates Z_2 but its positive hull is only nonnegative integers.
5. Remove compactness: B_n=[-n,n] in additive R have the Baire property and exhaust R but B_n+B_n never cover R.
6. Replace arbitrary sets with all Baire word balls silently: compactness is insufficient for the abstract original problem. A full algebraic basis in infinite elementary abelian2-group gives unbounded abstract word length; its balls must fail Baire regularity in the compact product topology.
