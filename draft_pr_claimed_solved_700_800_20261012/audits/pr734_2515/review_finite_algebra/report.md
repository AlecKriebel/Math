# Independent adversarial review of PR734 / problem 2515

**Mathematical verdict: PASS.** The frozen argument gives a negative answer
to the exact current Kourovka Notebook 21.6. I found no mathematical gap in
the finite construction, the universal transitive-subgroup obstruction,
or its transfer to the infinite finitary group. This report clears only
the mathematical claim; priority and publication review are outside this
assigned scope.

The governing candidate is the frozen `author/PROOFS.md` for head
`7a00d71fdf01ffb785863c859d75e88f943d38cf`, SHA256
`e3eb35d6d94a9a28d14ef03ba3780b9da9d4195f8cfa45f780afbc6f0e602fc9`.
I read that source before reading any author verifier or other audit;
neither author code nor other audit reports were subsequently consulted.
All new files belong to the dedicated finite-algebra review directory.

## Exact claim and primary-source boundary

Problem 21.6, printed p.177, asks whether each transitive Sylow p-subgroup of
a transitive finitary permutation group contains a transitive subgroup
having the cyclic-block property. That property requires both total
imprimitivity and a block support for every individual cycle of every
element. The finite obstruction refutes the weaker cycle condition, and
therefore refutes the requested conjunction.

The original task URL for the October 2026 PDF returned HTTP 404. I followed
the official homepage independently to the [October 6 update 2
notice](https://kourovkanotebookorg.wordpress.com/2026/10/06/october-2026-update-2-for-the-21st-edition/)
and the [actual current
PDF](https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/10/21tkt-1.pdf).
The requested target text matches the candidate. I extracted and visually
inspected printed p.177 and printed p.89. On printed p.89, Problem 15.23 defines
total imprimitivity by containment of every finite point set in a finite
group block. The covering chain in the candidate meets that definition
directly. The PDF URL change is source access drift, not a mismatch in
the problem. Retrieval hashes, byte count, response metadata, and page
indices are in `source_metadata.json`; source bodies were private and
removed before closure of this review.

## Independent mechanism and strongest verified result

The alternate derivation is in `derivation.md`. Represent the function
module as R=F2[x,y]/(x^2,y^2), where x=1+T_e1 and y=1+T_e2. Its
augmentation ideal J is the three-dimensional parity kernel. For
arbitrary lifts q1=(f,e1), q2=(g,e2) in P, the parity conditions give

    q1^2       = (x+beta*xy,0),
    [q1,q2]    = (y+(alpha+eta)*xy,0),
    [q1^2,q2]  = (xy,0).

These are an independent basis of J. Thus any subgroup projecting onto
the fibre quotient V must equal P. The three preimages of the lines of V
are exactly the maximal proper subgroups, and their intersection is J:
Phi(P)=J. In particular, P has no proper transitive subgroup. This
calculation is uniform in the lifts and avoids a classification claim or
an assumption about regular subgroups.

The explicit cycle C={1,5} of b has z(C)={1,6}. It therefore fails the
block intersection test. If a finite ambient block has induced
stabilizer action P, any transitive H has transitive block-stabilizer
image, which must be P. Lifts of b and z within that stabilizer give the
same entire-cycle and crossing-block witness. Restrictions may have
kernels and the lifts may act outside the block; neither affects the
argument.

The restricted binary-wreath union is an increasing union of actual
finite permutation 2-groups, is transitive, and is finitary. The finite
covering blocks prove total imprimitivity in the precise source sense.
Its bottom-block stabilizer image is exactly P at every stage. Taking
S=G is valid because the source concerns Sylow subgroups of G, and G
itself is a locally finite 2-group. No assertion about Sylow subgroups of
FSym(Omega) is required.

## Independent reproducibility receipt

Run `independent_finite.py` with a standard Python 3 interpreter. It uses
only the standard library and imports no original code. The recorded
run used bundled Python 3.12.14. The code reconstructs the parity-kernel
group, checks its action and multiplication, exhausts its subgroup
lattice, and verifies every possible pair of fibre lifts.

| Check | Independent result |
|---|---|
| Faithful ambient action / parity group order |64 / 32|
| Full subgroup lattice |50 subgroups|
| Orders 1,2,4,8,16,32 |1,11,23,11,3,1 subgroups|
| Transitive subgroups |Exactly P|
| Maximal subgroups |Three of order 16, each orbit size 4|
| Frattini subgroup |Parity kernel, order 8|
| Derived subgroup |Order 4|
| Arbitrary e1/e2 lift pairs |All 64 generate P|
| Crossing-cycle witness |{1,5}->{1,6}, intersection size 1|
| First binary-wreath extension |2048 elements, transitive|
| Bottom-block stabilizer image |Exactly P, order 32|
| Regular untwisted positive control |Order 8, cycle-support property holds|
| Identity substitute for z |Does not create a crossing witness|

The full machine receipt is `finite_receipts.json`. Exhaustion supplements
the symbolic proof. The infinite claim is established by induction and
the transfer lemma, not inferred from checking one wreath level.

## Adversarial boundary checks

| Proposed failure | Resolution |
|---|---|
| Semidirect-product convention reversed |Composition checked directly for all 64^2 ambient pairs; symbolic derivation agrees.|
| Parity equation not a homomorphism |Translation preserves parity; the character law also checked for all pairs.|
| Generation established only for selected lifts |Uniform group-ring basis calculation and all 64 lift pairs.|
| Proper transitive subgroup hidden in lattice |Direct quotient argument; all 50 subgroups independently enumerated.|
| A purported cycle inside B could leave B |Its lifting element stabilizes B, so its restricted orbit is its full orbit.|
| A transitive H need not contain the local base P |Only the induced image is used; its surjectivity follows from transitivity and minimality.|
| Correlations between blocks avoid obstruction |Kernel and outside-block actions are unrestricted in the transfer proof.|
| Infinite union loses finite support or 2-power order |Each element lies in a finite stage and is extended by identity.|
| Success at a finite wreath level substituted for infinity |Block and bottom-image invariants proved inductively at every stage.|
| Total imprimitivity definition differs |The official finite-set-in-finite-block definition is met directly.|
| Source intended Sylow subgroup of FSym |Printed 21.6 explicitly says a Sylow subgroup of G.|
| S=G fails an infinite Sylow convention |G is both periodic of 2-power element orders and locally finite with all finite subgroups 2-groups; maximality in itself is immediate.|

One editorial improvement would make Lemma 6 easier to compare with the
Notebook: explicitly say that every finite subset of Omega lies in an
Omega_n. The candidate already proves the stronger covering-chain fact,
so this is not a mathematical repair or an outstanding gap.

No directly visible known-result obstacle was found in this limited
source check. Problem 21.6 remains unstarred in the retrieved current
Notebook. That is source-status evidence only; it does not establish
novelty or priority. No scholarly priority search was undertaken.

## Closure

Relevant discovery goal: verify or falsify the claimed counterexample.
Best estimate: 100% complete for this assigned mathematical approach
family. Strongest result: a checkable proof and independent finite
reconstruction certify the entire obstruction and its infinite transfer.
Exact mathematical gap: none found. Publication or immutable release
readiness: not assessed. No Git mutation, remote push, external outreach,
or PR write was performed.
