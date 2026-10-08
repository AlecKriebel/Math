# Portable publication context

The complete original authored addendum follows this preamble unchanged. Its original-file preservation, 115 executions across five modes, 12 optimized original-checker false PASS results, source retrievals and original-layout links describe the earlier audit. The assertion-only original checker, original status/README, historical harness, original outputs and full legacy packet are excluded here. Their portable replay is NOT_RUN. This delivery freshly runs only the accepted hardened checker, independent checker and current semantic controls in normal, -O and -OO modes. Source-body replay and a new source search were not performed during packaging. The five mathematical proof files and source audit remain byte-for-byte unchanged. Current layout and noncircular verification are documented in README.md and VERIFICATION.md.

---

# Independent mathematical and executable audit

Audit date: 8 October 2026. Problem: 30004454 / OWR-1703863-003.

## Decision and scope

Accept the five authored files as proved sufficient conditions, a valid reduction, and two genuine obstructions to proposed mechanisms. No proof of the full assertion and no counterexample to it has been obtained. The full target remains **unresolved, with the five allowed substantive approaches exhausted (5/5)**. This review adds no sixth approach and makes no novelty claim.

No mathematical statement in the five files requires a correction. The executable verification does require correction: the original checker uses Python `assert` for every mathematical test and can report PASS after those tests are removed by optimization. The separate `verify_calculations_hardened.py` preserves the original checks as explicit exceptions. The independent verifier supplies additional checks. Original files, including the original checker and status records, are preserved byte-for-byte; this audit is the later acceptance addendum.

This is an independent proof review supported by exact computation, not formal proof-assistant certification and not an exhaustive literature census.

## Current-source authority and hypotheses

The publisher's 2026 version, *Coxeter quotients of the automorphism group of a Coxeter group*, Algebraic & Geometric Topology 26(7), 2353–2362, controls the paper's current numbering and hypotheses. The inspected publisher record and PDF date publication to 1 September 2026, with revision on 16 May 2025 and acceptance on 1 July 2025. The published PDF was independently fetched again and its 415227 bytes match SHA-256 `cb3f0d0ad30795a12c63b7bbe6016d26664c9b7f1e65780ada391529e877babc` and the previously inspected local copy exactly.

- The full finite-rank infinite-Coxeter assertion remains Conjecture 1.2 in the publication.
- Lemma 1.3 applies when the Coxeter group is infinite and its outer automorphism group is finite. Its quotient can be an infinite irreducible special factor, rather than all of a possibly noncenterless group.
- Theorem 1.4 requires either a nonspherical odd factor with finite outer automorphism group or a disconnected finite-edge defining graph. These are sufficient hypotheses, not an assertion covering every Coxeter group.
- Corollary 1.5 covers all infinite even Coxeter groups, including universal Coxeter groups.
- Theorem 2.7 is the finite-index clique-conjugating subgroup theorem used throughout this packet. The cliques are complete finite-edge subgraphs, with label-2 edges retained; they need not be spherical.
- Theorem 2.8 uses trivial centralizers of the specified nonempty multiple clique intersections. The packet's finite-centralizer tree criterion is an independently proved variant and is not falsely attributed verbatim to that theorem.
- Definition 2.11 and its following discussion give the finite-index subgroup fixing the conjugacy classes of all involutions. This is precisely enough for the direct-factor proof.

The original OWR 16/2020 contribution, pp. 890–891, states the earlier centerless-maximal-clique assertion. Current arXiv metadata for 2003.04111 explicitly identifies an incomplete earlier Theorem A proof and lists v3 (1 September 2022) as the latest version. The historical assertion is therefore not accepted as a proved input here. No claim is made that the cocycle example disproves its statement or completely diagnoses the historical proof.

Mihalik–Tschantz's *Visual Decompositions of Coxeter Groups*, Theorem 28, independently gives the clique-conjugating input. Its proof can be read precisely using induced **outer** restriction classes: on the finite-index subgroup stabilizing all maximal-clique conjugacy classes, choose a conjugating element for each clique and pass the resulting restriction automorphism to the outer automorphism group. Corollary 13 makes each maximal complete special subgroup self-normalizing, so different choices change the restriction only by an inner automorphism. Composition is then well-defined modulo inner automorphisms. The common kernel has finite index because the finitely many complete special subgroups have finite outer automorphism groups, and that kernel is exactly the required clique-conjugating subgroup. One need not rely on arbitrary choices yielding a homomorphism directly to an automorphism group. This also prevents accidentally reintroducing the cocycle error audited in Attempt 4.

The Howlett–Rowley–Taylor primary author-repository abstract confirms the finite-rank 2-spherical finite-Out theorem. Its complete original proof was not re-audited. The standard special-subgroup theorem, finite conjugacy classes of involutions, and trivial center of infinite irreducible Coxeter groups were checked against their use in the 2026 paper and remain cited background inputs.

Public sources:

- Publisher: https://msp.org/agt/2026/26-7/p01.xhtml
- Publisher PDF: https://msp.org/agt/2026/26-7/agt-v26-n7-p01-s.pdf
- DOI: https://doi.org/10.2140/agt.2026.26.2353
- Revision notice: https://arxiv.org/abs/2003.04111
- Historical report: https://ems.press/content/serial-article-files/46853
- Mihalik–Tschantz: https://arxiv.org/abs/math/0703439
- Howlett–Rowley–Taylor: https://www.maths.usyd.edu.au/u/ResearchReports/Algebra/HowRowTay/1996-26.html

The web-reader could not render the publisher XHTML/PDF during this independent pass. Direct retrieval of the official publisher PDF succeeded; this is a format/tool limitation, not a source-access denial. Fresh retrieval hashes and byte counts are recorded separately. The author publication-list search contains older “to appear” metadata; the publisher's version of record controls. Targeted later-literature searches did not establish a solution, which is not a certification that none exists.

## Attempt 1: equivariant presentation quotients

### Invariant normal closures

Accept. Every given relator lies in a complete special subgroup, which is contained in a maximal one because the Coxeter generating set is finite. A clique-conjugating automorphism sends that relator to a conjugate of itself. Normality gives the forward inclusion for the normal closure; applying the same argument to the inverse automorphism gives equality. The inverse step is essential. Neither setwise stability of the original relator list nor a common conjugator for different cliques is needed.

Killing a generator and adding a power relation for an already finite-labelled edge meet this hypothesis. A relation supported on a missing edge does not automatically meet it.

### Finite-Out lifting

Accept. Inner automorphisms belong to the clique-conjugating subgroup and descend through every invariant quotient. Surjectivity of the group quotient implies that the induced automorphism image contains every inner automorphism of the target. Taking the preimage of the target inner automorphism group has finite index because the target outer automorphism group is finite. The restriction is onto the entire inner automorphism group, not merely a finite-index subgroup of it. Projection from the target modulo its center to an infinite irreducible standard factor is valid because that factor has trivial center. No surjectivity onto the entire target automorphism group is asserted or needed.

### Separated odd components

Accept. Identifying vertices along odd edges gives one generator for each odd component. Reducing even edges to exponent 2 produces exactly the commutation relations between components that had a finite connecting edge. Distinct components have no odd edge between them. When generators outside the selected two components are killed, every boundary edge is even, so no surviving involution is accidentally killed. The absence of any finite edge between the two selected components leaves the presentation of C2 * C2. This infinite dihedral group is centerless and has finite outer automorphism group.

The criterion would fail if “no finite-labelled edge” were weakened to “no odd-labelled edge,” or if only part of an odd component were retained. Both failures are explicitly tested.

### Common-divisor cycle quotient

Accept. Partitioning a simple cycle into three nonempty consecutive arcs gives pairwise adjacent connected parts. A spanning forest rooted on the cycle assigns all remaining vertices to these parts without destroying connectivity. Contracting tree edges inside the parts identifies their generators. Imposing exponent d on every finite edge eliminates all original finite-edge relations because d divides every old exponent. Every target pair has an exponent-d relation, while no absent source edge supplies a relation. This is an exact presentation reduction, rather than an unsupported statement about an image of finite index.

For d=3 the resulting triangle group is Euclidean; for d>3 it is hyperbolic. In both cases it is infinite, irreducible, centerless and 2-spherical. The finite-Out input therefore applies. The assumptions d>=3, divisibility of all finite labels, and connected parts all matter. The displayed five-cycle example meets them.

The exact remaining gap is unchanged: no universal construction of such an invariant infinite finite-Out quotient has been established.

## Attempt 2: finite-centralizer overlap counting

Accept. Normalize a representative by left composition with a root-clique conjugator's inverse and then take root conjugator 1. On an overlap, equality of conjugations gives w_child^-1 w_parent in its centralizer. Since a subgroup is closed under inversion, this is equivalent to w_child lying in w_parent times the same centralizer. Recursing through a rooted tree gives at most the product of those finite centralizer sizes. Nonunique choices can only identify tuples or automorphisms, so they do not invalidate this upper bound. A tuple specifies at most one automorphism because every standard generator lies in a maximal clique. Every coset modulo the inner automorphisms has a normalized representative, establishing the index bound.

The one-clique boundary case has an empty product equal to 1 and works directly. Requiring only selected overlaps is sufficient; all multiple intersections need not be used. Infinite centralizers destroy this finite-counting argument and are not silently treated as finite.

For the path with both labels 3, the presentation is S3 amalgamated with S3 over their common transposition subgroup. Enumeration of S3 verifies that this subgroup's normalizer and centralizer both have order 2. At each endpoint of the base edge in the Bass–Serre tree, only that incident edge is fixed by the transposition. The fixed subtree is connected, so it is exactly the base edge. A centralizing element preserves it; the action has no inversions and its stabilizer is the amalgamated C2. Thus the claimed centralizer is exactly C2. The special subgroup on the nonadjacent endpoints is C2 * C2, proving infinitude. The stated bound 2 is valid.

## Attempt 3: direct-factor restriction

Accept. The special automorphism subgroup fixes each involution's conjugacy class and has finite index. Each standard generator in a normal direct factor is therefore mapped into that factor. The inverse gives equality. Consequently the full factor stabilizer is a finite-index subgroup of the full automorphism group.

Every automorphism of the factor extends by the identity on the complementary direct factor. The full stabilizer's restriction map is thus onto the **entire** factor automorphism group. Taking the inverse image of the given successful subgroup retains surjectivity onto that subgroup and then its prescribed infinite Coxeter quotient. This proves the reduction to infinite irreducible standard factors.

The warning against replacing this restriction by a finite-index image is correct and important: the index-two translation subgroup of D_infinity is Z, and neither it nor any of its finite-index subgroups has an infinite Coxeter quotient. No hereditary finite-index argument is being used. Nor can arbitrary automorphisms of a mere odd factor be extended by identity without the direct-product hypothesis.

## Attempt 4: retraction and conjugator obstruction

Accept. For a purported retraction onto Inn(W), its kernel is normal and intersects Inn(W) trivially. Commutators of a kernel element with inner automorphisms lie in both groups, so the kernel centralizes all inner automorphisms. When the center of W is trivial, conjugation of inner automorphisms by an automorphism records its action on every element of W faithfully. The kernel is therefore trivial, forcing the whole domain to equal Inn(W). If Out(W) is infinite, no finite-index domain containing Inn(W) can have this retraction.

The free product S3 * C2 * C2 is centerless. Its S3 anchor has trivial centralizer in the whole free product, so its anchor conjugator is unique. With composition right-to-left, the exact identity is c(fg)=f(c(g))c(f). The partial conjugation fixing S3 and the final C2 factor and conjugating the first C2 generator b by a is an involutive clique-conjugating automorphism. It has conjugator 1, whereas its composite with inner_b has conjugator aba, different from b by free-product normal form. The unique-conjugator function is therefore not a homomorphism.

The semidirect-product conclusion is valid in this example: unique decomposition uses the proved C_W(P)=1. Merely knowing Z(W)=1 would not establish uniqueness for an arbitrary anchor. The action of the pointwise anchor stabilizer on W is nontrivial, so projection to the inner factor is not a group homomorphism. This refutes the proposed construction, not the original quotient conjecture or the historical theorem's statement.

## Attempt 5: standard reflection obstruction

Accept. The partial conjugation of u by st and its inverse preserve the universal Coxeter presentation. Iterating gives alpha^n(u)=(st)^n u (st)^-n because alpha fixes s and t. Reduced free-product normal forms show that its positive powers are nontrivial. Every finite-index subgroup of Aut(W), whether normal or not, contains a positive power of alpha: use the action of the cyclic group on the finite coset set and the orbit of the subgroup coset.

The displayed reflection matrices follow from r_i(x)=x-2B(e_i,x)e_i with column vectors. Their product, the polynomial formula for v_n, its unit norm, and the pairing B(e_t,v_n)=-4n-1 are correct. The new independent verifier checks the recurrence and both bilinear identities coefficient-by-coefficient as polynomial identities in n, as well as 257 exact numerical values. This goes beyond, but does not replace, the written induction.

A B-isometry implementing alpha^n must map the one-dimensional -1 eigenspaces of the reflections as stated. Unit norm forces the scaling factors to be signs, even though B is indefinite. Preservation of the absolute pairing contradicts 4n+1>1 for every positive n. The n=0 boundary is correctly excluded. This proves the assertion for every finite-index automorphism subgroup, not merely for a particular subgroup or a coherent choice of implementing maps.

The universal rank-three group is even, so the current theorem already gives it a virtual infinite Coxeter quotient. This obstruction is deliberately about the standard geometric construction, not the desired abstract quotient.

## Executable acceptance and its limits

The frozen read-only run comprises 115 subprocess executions in five modes: normal Python, -O, -OO, PYTHONOPTIMIZE=1, and PYTHONOPTIMIZE=2. Each process reports actual UID=EUID=1000 and verifies failure of both file creation in its working directory and append-opening its target script. Frozen directories use mode 0555 and files use 0444; the denied operations return EACCES. HOME and TMPDIR point at that read-only directory, and bytecode writing is disabled. Every frozen file's hash is unchanged afterward.

Per mode:

- Original checker baseline passes.
- Three original semantic corruptions are rejected in normal mode but falsely pass in each of the four optimized modes: 12 observed false PASS results.
- The assertion-free corrected checker baseline passes and all three corresponding corruptions fail in all five modes.
- The independent baseline passes 6066 explicit checks and all 14 independent semantic corruptions fail in all five modes.

The independent suite covers universal polynomial reflection identities; the finite-index coset return step; all 626 connected cyclic labeled graphs on 3–5 vertices and their connected three-part partitions; the separated odd-component presentation and invalid boundary mutations; the S3 normalizer/centralizer and fixed-edge calculation; finite tree tuple counts; exact free-product partial conjugation and crossed composition; full factor-stabilizer restriction on a finite elementary abelian model; and the D_infinity index-two translation obstruction. It uses only Python's standard library, integer/rational arithmetic, permutation and normal-form calculations, and explicit exception checks.

These computations do not enumerate infinite groups or prove the universal structural source theorems. The mathematical proof reviews above supply the universal arguments; the finite models are adversarial supporting tests. The program-specific mutation tests do not claim that an arbitrary future alteration will always be caught.

## Final acceptance boundary

Accepted: all five bounded authored mathematical claims, with their stated hypotheses and exact gaps, and the current-source distinctions.

Rejected: the original checker as optimization-safe evidence; a claim that this audit solves the full conjecture; a worldwide priority or unsolved-status certificate; any use of the old incomplete centerless-clique theorem as a proved input; and any replacement of a surjection onto the required Coxeter target by only a finite-index image.

Use the correction and independent verifier as the operative computational evidence. Keep the original files as historical records. No GitHub publication, queue change, new proof approach, or external communication was performed by this audit.
