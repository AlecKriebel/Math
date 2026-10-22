# Independent adversarial audit: finite dyadic-set stabilizers in T

- Problem: 20001353 / AIM-DYNAMICAL_SYSTEMS-0011
- Date: 3 October 2026 UTC
- Frozen author manifest SHA-256: `075537777b11d8f5997233d29961440ec915f2e813f591eb75eb891d82545324`
- Verdict: **PASS_SCOPED_KNOWN_EXAMPLES**
- Mathematical blocking findings: **none**
- Novelty: **not claimed; the same theorem has an independently verified prior announcement**
- Broader research programme: **not classified or closed by this result**

## 1. Exact disposition and scope

The frozen proof correctly establishes, for **every positive integer k** and **every k-element dyadic subset A of the circle**, that its setwise stabilizer H_A in classical Thompson's group T is a maximal proper subgroup of countably infinite index, is isomorphic to F^k semidirect C_k with cyclic permutation action, and depends up to conjugacy only on k. Different values of k yield nonisomorphic groups. The argument covers k=1 and k=2 without exceptions and does not require k to be a power of two.

The theorem is a complete proof of this construction, rather than bounded experimental evidence. Its conclusion supplies a countably infinite collection of example types for the recovered open-ended AIM request. It does **not** establish that this packet contributes new mathematics, classify all infinite-index maximal subgroups, or make future requests for additional examples meaningless.

Recommended catalogue disposition: **already_solved / 1/5, scoped to the known example-producing construction**, if that status supports an explicit scope qualification. Recommended plain-language description: **“Known examples supplied, with a complete independent proof of the finite dyadic-set family; no novelty claim and no closure of the broader programme.”** An unqualified “the Thompson-group maximal-subgroup problem is solved” is not supported. If the receiving system requires a binary claim of complete resolution of an entire open-ended programme, this audit does not authorize that claim.

There is no proof-revision request against the frozen theorem. Source provenance remains qualified as described below, and any publication should preserve those qualifications.

## 2. Input integrity and audit independence

The seven author files match the supplied manifest, including the manifest's own supplied hash. `FROZEN_INPUTS.json` records all seven checksums. The audit does not change any author file. The final recheck is recorded in `AUDIT_MANIFEST.json`.

The author script was inspected and rerun with its stdout directed to the separate audit directory. It performs no file writes. The resulting `author_rerun.json` is byte-identical to the supplied `exact_results.json` and reproduces all **59,629** assertions.

The separate `audit_controls.py` imports no author code. It uses a different interval partition implementation, explicit exact PL-lift composition and inverse construction, exhaustive finite-grid local witnesses, combinatorial edge signatures, and graph search. Its **41,290** assertions pass, including six rejected faulty alternatives. These bounded controls are auxiliary; the all-parameter proof audit is in Sections 4–8.

This is a fresh AI-assisted audit of the frozen packet. It is not external human peer review, proof-assistant certification, or an audit of any inaccessible prior manuscript.

## 3. Source, attribution, and original-question gate

### Original question

The pinned extraction gives the title “Maximal subgroups in Thompson groups” and the sentence:

> Find new maximal subgroups of infinite index in Thompson groups.

The separate cached prior attempt agrees. These are correlated recovered records, not two independent primary witnesses. The auditor inspected their agreement but did not rederive the extraction from the full source corpus or independently recompute the corpus hashes cited in the author source note.

Fresh retrievals of the [AIMPL section](http://aimpl.org/groupdynamorigin/3/), its slashless form, and the [workshop problem-list root](https://aimpl.org/groupdynamorigin/) did not produce readable source content. The first and root requests returned 502 errors; the slashless route had a cache miss. The [catalogue page](https://www.unsolvedmath.com/problems/20001353) was also inaccessible. An exact-phrase search did not recover a fresh primary witness.

The [official AIM workshop report](https://aimath.org/pastworkshops/groupdynamoriginrep.pdf), page 1, independently confirms the June 2024 workshop context and Rachel Skipper's maximal-subgroups talk. It does not reproduce the particular question. This audit therefore approves the wording only as **recovered from the pinned extraction**, never as freshly primary-source verified.

The dyadic-pair title is narrower than the recovered question and must not substitute for it. The source sentence does not enumerate F, T, and V or require a classification. Choosing classical T is a disclosed interpretation within the ordinary Thompson-groups family. The theorem is responsive as a construction of examples, with “new” handled by the attribution and non-novelty qualification rather than silently claimed.

### Direct matching prior announcement

The auditor freshly retrieved [Alper Ferudun's EulerSolve landing page](https://eulersolve.org/papers/aim-dynamical-systems-0011/). It gives manuscript and release dates of 4 and 5 September 2026, respectively, and announces exactly the all-k maximality, index, wreath-product, conjugacy, and nonisomorphism results audited here. It identifies the work as an AI-assisted, unrefereed preprint and links DOI [10.5281/zenodo.22324898](https://doi.org/10.5281/zenodo.22324898).

The linked paper, verification report, and DOI route did not yield readable full proof content in this audit. Accordingly, this report verifies an existing announcement and the frozen independent proof, **not the correctness of the inaccessible earlier proof**. The accessible announcement is sufficient to prohibit presenting this packet as a first discovery. Its absolute historical priority is not established.

### Other literature statements

The source note's principal contextual distinctions survive fresh checks:

- [Golan Polak, EMS Press](https://ems.press/journals/ggd/articles/14297830), confirms the 2025 journal citation, the 23 May 2024 online publication date, the closedness result for infinite-index maximal subgroups of F, and an infinite family of nonisomorphic examples.
- [Belk–Bleak–Quick–Skipper, Type systems](https://eprints.gla.ac.uk/328840/2/328840.pdf), Corollary 2.3 on printed page 422, treats finite point sets in one Cantor tail class for V. Theorem 7.5 gives uncountably many pairwise nonisomorphic maximal subgroups. This is not a proof for T's circular-order action.
- [Belk–Bleak–Quick–Skipper, The maximality of T in V](https://eprints.gla.ac.uk/354070/3/354070.pdf), proves a different ambient-group statement. Its printed page 2 also records the familiar k=1 maximality F<T.
- [Golan, July 2026 preprint](https://arxiv.org/html/2607.04038v1), Theorem 1.1, supplies nested infinite-index maximal copies of F_n. Problem 1.4 explicitly discusses further classification questions. Those results are distinct from the circular finite-set construction.

These checks concern the cited result statements and relevant context; they do not claim full proof audits of those papers. The author's earlier bounded repository-duplicate search was not repeated in this audit, and no completeness guarantee for all prior work or all differently titled repository attempts is made.

## 4. Definitions and finite circular interpolation

The definition of T explicitly includes preservation of D=Z[1/2]/Z. This matters: dyadic breakpoints and power-of-two slopes alone, read vacuously for a breakpoint-free circle rotation, would admit rotations not preserving D. The proof does not make that error.

For a prescribed finite cyclic-order-preserving dyadic bijection, choose matching lifts p_0<...<p_m=p_0+1 and q_0<...<q_m=q_0+1. Each adjacent gap has positive dyadic length. A sufficiently fine common dyadic mesh partitions each particular gap into finitely many intervals of power-of-two length. Repeatedly bisecting a piece increases its partition's size by exactly one. Thus source and target partitions can be brought to the same size with finitely many operations; there is no congruence or parity obstruction on the number of pieces.

An affine map between two corresponding pieces has positive slope 2^n for an integer n. The affine intercept is dyadic because both corresponding endpoints are dyadic and the slope is a dyadic unit. The inverse slope and intercept have the same property. Consequently both the map and inverse carry dyadic points to dyadic points. Adjacent pieces agree at endpoints, and the final lift satisfies the degree-one condition f(p_0+1)=f(p_0)+1. Periodic extension yields a genuine element of T.

All of these assertions apply to a singleton prescription, where there is one full-circle interval, and to a two-point prescription. They also apply to source or target arcs that cross the usual zero cut. No orientation-reversing three-point permutation is used. This establishes the finite extension lemma and transitivity on the k-element subsets for every k>=1.

## 5. Local slides and the full primitivity argument

### Edge orbit, including k=1 and k=2

For k>=2, a slide has common set C of cardinality k-1 and two noncommon points in one component of the circle minus C. Equivalently, the noncommon points are adjacent in the circularly ordered union. Its circular membership pattern has one A-only point, one B-only point, and all remaining points common. Any two such patterns match by a cyclic-order-preserving bijection after exchanging the two configurations if necessary. Exchanging them is legitimate because the graph uses **undirected** edges and an equivalence relation is symmetric.

For k=2 the common set has one point, so its complement is a single interval and every pair of configurations sharing that point is a slide. The two directed orientations need not form one directed orbit, but their undirected edges do. For k=1 an edge is just an unordered pair of distinct dyadic points; any prescribed two-point bijection is realizable. Thus there is exactly one unordered slide orbit in every case required by the proof.

### Connectivity for arbitrary configurations

Choose a dyadic cut q outside U union V. The cut-open representatives of all configuration points lie strictly between q and q+1. There is a nonempty initial open interval before both first points, and dyadic density supplies k ordered auxiliary points b_1<...<b_k there.

During the move u_i to b_i, the already moved b_j (j<i) all precede b_i, and all unmoved u_j (j>i) follow u_i. Hence the positive interval between b_i and u_i contains none of the other configuration points. The two points belong to the same complementary component, so this is a legal slide. The auxiliary points are distinct from both original configurations and each other. The procedure reaches the same auxiliary configuration from U and V in k steps each. It gives a path of length at most 2k, with no collision or wraparound problem. At k=1 it remains a valid path in the complete singleton graph.

This is an all-k argument. The finite-grid graph checks below are not being extrapolated to prove it.

### Collapsing every invariant equivalence relation

Suppose A and B are distinct but equivalent under a T-invariant equivalence relation. Equal cardinalities imply A minus B is nonempty. Choose a in that difference. A sufficiently small arc around a contains no other point of A union B; a distinct dyadic a' in that arc avoids the finite union and remains in the same gap of A minus {a}.

Prescribing a to a' and fixing every other point of A union B is injective and cyclic-order preserving. The extension lemma realizes it by g in T. Crucially, a is **not** in B, so g fixes B pointwise, rather than merely approximately or setwise. Invariance gives gA equivalent to B; symmetry and transitivity together with A equivalent to B give A equivalent to gA.

This is a genuine nontrivial slide. Every slide then has equivalent endpoints by the one-orbit result and invariance. Connectivity makes every two k-configurations equivalent. Thus every nonidentity invariant equivalence relation is universal. This establishes primitivity, without needing to classify all other orbital patterns and without assuming any finite-grid permutation belongs to T.

## 6. Maximality, properness, and exact index

The orbit map gH_A to gA is a well-defined bijection of T-sets. For any intermediate subgroup H_A<=K<=T, equality of left K-cosets defines an invariant equivalence relation on left H_A-cosets. There is no requirement that K be closed, finitely generated, finite index, or infinite index.

If the equivalence is equality, every element of K lies in H_A, so K=H_A. If it is universal, every element of T lies in K, so K=T. Properness follows because the transitive configuration space has more than one point. This proves maximal properness among **all** subgroups, not only among infinite-index ones.

The collection of k-element subsets of a countably infinite set is countably infinite for each positive finite k: it injects into D^k after choosing an ordering and is infinite by fixing k-1 points and varying the remaining point outside them. Therefore the orbit-coset bijection gives index exactly aleph_0. Simplicity or an unsupported “proper implies infinite index” inference is unnecessary.

The nonempty condition is essential: at k=0 the stabilizer is all of T, so it is not proper. The frozen theorem excludes this case explicitly.

## 7. Wreath-product splitting for every k

A partition of the unit interval into exactly k standard dyadic intervals is obtained by k-1 successive bisections. This construction is available for every positive integer, including odd k. Using equally spaced points i/k would fail in general because these need not be dyadic; the proof correctly avoids that alternative.

For the set A_0 of left endpoints, the orientation-preserving cyclic action on the k marked points has image contained in C_k. Its kernel fixes all marked points and preserves each complementary interval. Normalizing an interval of power-of-two length to [0,1] has power-of-two slope and dyadic intercept in both directions. Under this normalization the allowed restriction is exactly F. Conversely, any k independently chosen such interval maps glue at fixed endpoints to an element of T. Thus the full kernel, not just a subgroup of it, is F^k.

The map r takes each interval affinely to its successor. Its slopes are ratios of power-of-two lengths, and its lifted endpoint images fit consecutively around the circle, including the final seam. In normalized interval coordinates it is precisely (i,t) to (i+1,t). After k steps both index and coordinate return, so r^k is the identity. For k>1 the permutation of the marked points has exact order k, which rules out a smaller positive order. For k=1 r is the identity circle map.

Thus the cyclic permutation image is all of C_k, and the cyclic subgroup generated by r intersects the kernel trivially. Every stabilizer element is a kernel element times a power of r. Conjugation by r sends a normalized F-action in interval i to the identical normalized action in interval i+1, with no hidden twisting automorphism. This proves F^k semidirect C_k with the regular cyclic action, hence F wr C_k.

For an arbitrary A, the finite extension lemma conjugates it to A_0. Equal-cardinality stabilizers are therefore conjugate in T, and the structure conclusion holds for every A, including those whose gap lengths are not individually powers of two.

At k>1 the cyclic complement moves marked points while preserving the set. Consequently the pointwise stabilizer F^k is strictly smaller than H_A and is not maximal in T. No statement about pointwise stabilizers has been substituted for the setwise claim.

## 8. Torsion invariant and different cardinalities

An increasing interval homeomorphism of finite order fixes every point: either f(x)>x or f(x)<x would yield a strict monotone finite orbit, contradicting return to x. Thus F, and then F^k, is torsion-free.

If an element u of the split stabilizer has finite order, its finite cyclic subgroup meets F^k trivially. Restriction of the quotient map therefore embeds that cyclic subgroup into C_k. Its order divides k. The explicit r has order k, so the largest order of a finite-order element is exactly k. For k=1 the maximum is 1, contributed by the identity, and there is no nontrivial torsion.

This invariant is preserved by abstract group isomorphisms, independently of a chosen action or a distinguished kernel. It separates every pair of different positive cardinalities, including values where one divides the other. In particular different-cardinality stabilizers cannot be conjugate either. Combined with equal-cardinality conjugacy, the theorem gives precisely one conjugacy class per k **within this family**; it does not classify all maximal subgroups of T.

## 9. Independent exact controls and negative controls

Run `python audit_controls.py` in the audit directory. The script uses only Python's standard library and exact rational arithmetic.

The 41,290 checks include:

- For all 6,307 unordered distinct pairs of k-configurations in the eight-point dyadic grid, for every 1<=k<=7: an explicit local point move, circular-order admissibility, legal PL extension, exact prescribed values, pointwise fixation of the other configuration, slide adjacency, and exact inverse composition.
- All 988 slide edges in these finite graphs: one canonical unordered circular-membership pattern for each k, together with connectedness of each of the seven finite graphs.
- All 78 cyclic shifts across deterministic nonuniform-arc examples for 1<=k<=12: legal extension, endpoint matching and exact inverse composition.
- Cyclic complements for all 1<=k<=32: exact equality or inequality of whole PL maps at every power through k, endpoint actions, legal interval factors, exact conjugation of a nontrivial F element through all 528 factors, and exact commutation of disjointly supported factors.

Whole-map equality is checked on the union of all exact breakpoints. Composition includes inverse images of the outer map's breakpoints, so these tests do not mistake agreement at a few sample interior points for equality of PL maps.

Six faulty alternatives are rejected: a slope of 3/4; a breakpoint-free rotation by 1/3; an equally spaced nondyadic triple; a three-point order-reversing prescription; a nonlocal replacement that shares k-1 points but crosses another marked point; and moving a common point while claiming to fix the other configuration. Additional written negative controls exclude k=0, a pointwise/setwise substitution, and inferring full-programme closure from the examples.

None of these finite checks certifies the infinite group theorem by itself. That theorem passes because every parameter and every logical implication has been justified in Sections 4–8 and in the frozen proof.

## 10. Release limits

No frozen author file was edited and no remote state was changed. The separate audit package contains original audit prose, exact diagnostic code and results, and integrity metadata. It contains no source PDFs, full-source extracts, source corpus, or private research records.

The approved claim is a complete elementary proof of the stated all-k family, with existing attribution and explicit source-access limits. No claim of original discovery, exhaustive literature search, certification of the prior inaccessible proof, or complete classification is approved.
