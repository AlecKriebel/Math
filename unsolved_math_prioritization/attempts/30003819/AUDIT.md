# Independent acceptance audit: differential-poset structural upper bound

This AI-assisted manuscript is unrefereed. Acceptance records an independent internal AI audit, not external human peer review, journal acceptance, or formal proof-assistant certification.

The complete written proofs and analytical constructions are retained. This is not a computational reproduction package: executable code, raw enumeration datasets, copied source documents and images, and private coordination material are omitted. Historical finite checks are supporting evidence; the uniform theorem and infinite sharpness follow from the written arguments. The historical computations cannot be reproduced from this edition alone.

The general local recurrence remains unresolved by this work. No novelty, priority, exhaustive literature-survey, or current-openness claim is made.

This document preserves the complete independent logical audit. Its computational and source-inspection statements describe the original audit, not new editorial executions or new scholarly-source inspection. The public proof now explicitly clarifies the integer-count convention and the projected triangle versus bipartite six-cycle terminology. These are editorial clarifications; no mathematical correction was required.

## Verdict

**ACCEPTED AS A STRUCTURAL PARTIAL RESULT. The full local recurrence is not proved or disproved.** No mathematical correction to the submitted argument is required. The audit accepts the uniform incidence-dependent correction, the stated sufficient conditions and equality criterion, the all-r rank-three consequence, and both sharp infinite examples. It does not certify novelty or the current worldwide status of the general conjecture.

The audited candidate is the 19-member packet identified by manifest SHA-256 `7a6b41179f1b82a877e730e4954eabdf975c4becccf820a841b9fb32bee841b5` (4567 bytes). Its outside seal has SHA-256 `4d6398ada0b59347dc0d04d0b162aae2ebf72a93d8c4b50ec148ca3a94632c5d` (236 bytes). The original audit authenticated every listed member size and hash, checked exact inventory closure, and confirmed agreement with the source-grounded target. The proof file has SHA-256 `a5672b9653d0bcf8eaef75511d823b750c90d979bd9e8bcdc1bc5b2a0ba0fa02` (14750 bytes).

During the original audit, the candidate was not modified, and no candidate program, source-author program, or externally supplied proof-checking program was executed. All computational results below came from a separately written implementation. No remote mutation or publication was performed in that audit. Editorial preparation likewise did not modify the original candidate or audit and did not rerun mathematical programs.

## Exact accepted statement

Let r be a positive integer. Let P be an infinite locally finite N-graded poset with finite ranks, a unique minimum, and ordinary unweighted up/down operators over Q satisfying DU-UD=rI, equivalently the corresponding integer incidence identities. Write p_j=|P_j|. For j>=1, let B_j be the bipartite incidence graph between P_(j-1) and P_j, and let b_j be its cycle rank.

For n>=2, put X=P_(n-1), Z=P_(n-2), and

    S={z in Z: there exists x in X whose entire lower-cover set is {z}}.

Let H_S retain every vertex of X, precisely the vertices S on the other side, and all incidences between them. In particular, retain the isolated vertices of X. Define

    q_n=|E(H_S)|-|V(H_S)|+c(H_S).

Then

    0 <= q_n <= b_(n-1),
    p_n <= 1+r sum_(k=0)^(n-2) p_k+(r-1)p_(n-1)-q_n.

Equivalently,

    p_n <= r p_(n-1)+p_(n-2)+b_(n-1)-q_n.

This is uniform over the specified class, but uses incidence data rather than only rank sizes. The correction is determined by the two preceding ranks. It can be positive and attained, and the coefficient 1 multiplying q_n cannot be replaced uniformly by any constant larger than 1.

Accepted consequences:

1. If every z in Z has such a singleton successor, then p_n<=r p_(n-1)+p_(n-2).
2. This condition holds whenever rank n-1 was itself produced by reflection-extension. The extension to rank n can be arbitrary; it need not be a reflection-extension.
3. If n>=3 and every z in Z has at least two distinct singleton successors, equality in that local bound holds precisely when the extension to rank n is reflection-extension, up to relabeling rank n.
4. For every positive integer r, p_3<=r p_2+r; equality holds precisely for reflection-extension from rank two.

The accepted operator convention is the standard characteristic-zero/integer-count convention. The cycle-space dimension formula is valid over any field, but that does not license interpreting the differential identity only modulo a positive characteristic.

## Target and source alignment

The original target asks for an improved upper bound toward p_n<=r p_(n-1)+p_(n-2), starting with Byrnes's 1+r sum_(k=0)^(n-2)p_k+(r-1)p_(n-1). A strictly sharper uniform structural inequality qualifies as partial progress under that target. The accepted result satisfies this narrower endpoint. It is not a proof of the general local recurrence and is not a replacement by a lower-rank-gap question.

Byrnes's Chapter 5 proves the global Fibonacci envelope by first proving the weaker cumulative-sum bound and then inducting against Fibonacci ranks. PDF page 51 states the separate local recurrence as Conjecture 5.9. A global Fibonacci envelope does not force a local recurrence on an arbitrary smaller sequence. The candidate consistently maintains this distinction.

The OWR problem statement's common-cover axiom ends with an erroneous '=1'. Under the standard differential-poset definition, distinct elements may have no common lower or upper cover. The operator definition on Gaetz-Venkataramana PDF page 2 supplies the appropriate convention. The candidate does not rely on the erroneous stronger axiom.

## Logical audit, step by step

### 1. Degree and pair identities

A diagonal matrix entry gives u(x)=d(x)+r. An off-diagonal entry gives equality of the number of common upper and common lower covers of two distinct same-rank elements.

If a pair had two common upper covers, it would have two distinct common lower covers. Those two lower elements themselves have the initial pair as common upper covers. Repeating descends one rank each time and eventually requires two different elements in rank zero, impossible with a unique minimum. This proves that all common-cover counts for distinct elements are at most one and that all adjacent-rank incidence graphs have no 4-cycle. Full lower-rank consistency is essential here.

### 2. Connectedness, edge counts and exact identities

B_1 is a star with r leaves. If B_j is connected, its projection onto the P_j side, with adjacency given by a common predecessor, is connected. Off-diagonal commutation identifies that adjacency with having a common successor. Hence all P_j vertices lie in a common component of B_(j+1). Every P_(j+1) vertex has a predecessor, so no other component exists. A projected one-vertex graph is connected; the induction includes r=1.

Summing u=d+r gives e_j=r sum_(k=0)^(j-1)p_k. As B_j is connected,

    b_j=e_j-p_(j-1)-p_j+1.

It follows by direct subtraction that

    p_n=1+r sum_(k=0)^(n-2)p_k+(r-1)p_(n-1)-b_n,
    b_n-b_(n-1)=r p_(n-1)+p_(n-2)-p_n.

Thus Byrnes's bound is b_n>=0. The desired local recurrence is the stronger statement b_n>=b_(n-1). The audit does not infer the latter from nonnegativity.

### 3. Restriction, isolated vertices and private-cover meaning

A singleton successor of z means a successor x with d(x)=1 and lower-cover set exactly {z}. It does not mean z has only one successor. A vertex can serve as such a witness for only one z.

H_S is genuinely a subgraph of B_(n-1), including all X vertices. Therefore 0<=q_n<=b_(n-1) by cycle-space inclusion. Counting its vertices and edges gives

    q_n=sum_(z in S)(u(z)-1)-|X|+c(H_S).

If S is empty, H_S consists of |X| isolated vertices and q_n=0. Dropping isolated vertices without adjusting c would corrupt this formula. The submitted proof retains them correctly. The independent Young-lattice tests include actual proper-S cases with many isolated X vertices.

### 4. Witness trees and disjoint internal vertices

Choose a witness a=x_z for z in S, and let N_z be all successors of z in X. For every y in N_z distinct from a, the pair a,y has exactly one common predecessor, z, so exactly one common successor t in rank n.

If w is any other lower cover of t, the pair a,w has a common upper cover, hence a common lower cover. Since a's only lower cover is z, w lies in N_z. Consequently every nonsingleton upper vertex incident to a has all lower covers in N_z.

Two such upper vertices cannot share any terminal other than a, because that would create a 4-cycle. Each y in N_z other than a belongs to exactly one such upper vertex. Their full stars consequently form a connected acyclic graph T_z on N_z and those upper vertices. In the case |N_z|=1 there are no internal vertices and the one-vertex graph is the correct tree.

A rank-n internal vertex cannot belong to both T_z and T_w for z!=w: it would cover both witnesses, whose lower-cover sets are disjoint. This contradicts the off-diagonal identity. Trees may share X terminals; this is precisely where cycles in their union can arise.

### 5. Replacement preserves cycle rank

Take K to be the union of the witness trees together with every vertex of X, including isolated vertices. It is a subgraph of B_n. Replace each original star centered at z in H_S by T_z.

If T_z has a_z internal vertices, the old star has |N_z| edges and one nonterminal vertex; the new tree has |N_z|+a_z-1 edges and a_z nonterminal vertices. Hence both E and V change by a_z-1. Both constructions connect exactly the same terminal set N_z. Component count is preserved, including isolated terminals. Internal vertices are disjoint between replacements, so the counts add without hidden identifications.

Therefore beta(K)=beta(H_S)=q_n. The inclusion K subset B_n injects cycle spaces, so b_n>=q_n. Substitution in the exact rank identity proves the accepted theorem. No unsupported assertion that all of B_(n-1) embeds into B_n is made.

### 6. Sufficient condition and reflection indexing

If S=Z, then H_S=B_(n-1) and q_n=b_(n-1), giving the local recurrence. Reflection-extension creating rank n-1 adds r singleton successors for each element of rank n-2, so it supplies S=Z at the correct preceding step.

Reflection-extension to rank n itself always has p_n=r p_(n-1)+p_(n-2) by its construction. These are two separate facts. The sufficient-condition theorem is stronger in a different direction: once rank n-1 is reflected, every admissible next extension satisfies the bound.

### 7. Equality with two witnesses

Under S=Z, K is connected and contains every X vertex. Each rank-n vertex t not already used in K is a new vertex all of whose d(t) incident edges attach to X. Adding it changes cycle rank by d(t)-1. Equality b_n=beta(K) thus forces every unused t to be a singleton.

For z, take distinct singleton witnesses a and b. Every nonsingleton upper vertex incident to b must be used in K; otherwise it contributes positive excess. It must belong to T_z, since belonging to T_w would put it above b and x_w and force z=w. Every internal vertex of T_z also covers a. There is a unique h above a,b. For each y in N_z other than b, its common upper cover with b is nonsingleton, belongs to T_z, and also covers a; uniqueness for a,b forces it to be h. Hence h covers all N_z. Another nonsingleton internal vertex would repeat a terminal pair, so there is exactly one.

For n>=3, every z has a lower cover, so u(z)=d(z)+r>=2. Thus all the h_z are genuinely nonsingleton. They are pairwise distinct, and x belongs to exactly d(x) of their predecessor neighborhoods. The degree equation leaves precisely r singleton successors over each x. This is reflection-extension, with no unaccounted upper vertices. The converse follows by counting the reflected upper rank.

The hypothesis 'two singleton successors' is not silently reduced to one; the r=1 sharp later-rank example does not satisfy this stronger hypothesis at every lower element and does not require it.

### 8. Universal rank-three case

There are r elements in P_1, each with one lower cover and hence r+1 upper covers. At a fixed z, each nonsingleton successor consumes at least one of the other r-1 rank-one elements. These consumed sets are pairwise disjoint, as repeated use would create a second common successor for a pair. There are therefore at most r-1 nonsingleton successors and at least two singleton successors of every z.

The equality theorem applies at n=3 for every r>=1. For r=1, P_2 has two singleton successors of its sole rank-one element and the rank-three bound is p_3<=3. The boundary is valid, not an excluded special case.

### 9. Rank-zero and n=2 boundary

No b_0 is introduced or needed; b_1=0. At n=2, Z is just the minimum and all r rank-one elements have singleton predecessor set. Thus H_S=B_1 and q_2=0. The result gives p_2<=r^2+1, exactly the usual rank-two local bound. For r=1, N_z has a single terminal and T_z is a one-vertex tree, with the star replacement removing one vertex and one edge. The n>=3 restriction in the equality theorem avoids relying on a nonexistent lower cover of the minimum.

### 10. Infinite realization and sharpness

A valid finite prefix can always be prolonged: for each z one rank below the current top, create a distinct new vertex covering all current successors of z, and add r distinct singleton successors over each current top vertex. At a current x this supplies d(x)+r successors. For a distinct current pair, the number of common new successors equals its number of common predecessors. All new vertices have predecessors, and each new rank is finite. Repeating indefinitely preserves earlier incidences, all commutator identities, the unique minimum and local finiteness.

For r=3, the independent reconstruction uses one rank-two vertex over each pair of three rank-one vertices and two singleton successors over each rank-one vertex. Reflection gives ranks (1,3,9,30), edge counts (3,12,39), b_2=b_3=1 and q_3=1. Byrnes gives 31; the corrected bound 30 is attained.

For r=1, an independent partition implementation constructs Young's lattice through rank five, then reflects twice. The ranks are (1,1,2,3,5,7,12,19); successive edge counts are (1,2,4,7,12,19,31). In particular B_6 has 19 edges and 19 vertices, so b_6=1; q_7=b_7=1. Byrnes gives 20; the corrected bound 19 is attained.

Both prefixes continue indefinitely by the verified reflection procedure. In either example, replacing q by c q for any c>1 would lower the claimed right side below the attained rank. This establishes coefficient sharpness; it does not claim that q_n exhausts all possible information in every prefix.

### 11. Relaxed incidence obstruction

For the relaxed layers of sizes (1,3,3,7), both interior integer commutators are I, but the minimum has three successors, so the rank-zero identity fails when r=1. The independent checker accepts the two interior identities and rejects the purported full differential prefix. Since 7>3+3, it correctly demonstrates insufficiency of a purely two-middle-commutator argument, not a counterexample to the target.

A harmless terminology clarification is available: the three pair-blocks form a triangle in the projected common-cover graph, while their bipartite incidence graph is a six-cycle. The candidate's final phrase 'three-edge cycle' can be understood in the projected graph. None of the proof or computations depends on treating the bipartite cycle as a triangle.

## Independent computation and limits

The independent code uses predecessor sets, integer intersection counts, union-find graph components and exact edge-clique decompositions. It neither imports nor executes candidate code or source-author code. It constructs both examples from the mathematical descriptions and explicitly checks the actual replacement trees K, not merely the final numerical inequalities.

For completeness of the finite extension enumeration: every nonsingleton new upper vertex is a clique in the required common-predecessor graph; the cliques partition its edges, because each pair must receive exactly one common successor. Once those blocks are chosen, the diagonal degree identities force the remaining singleton multiplicities. The enumerator selects the least uncovered edge and all eligible clique blocks containing it, with nonnegative residual degrees. This enumerates all extensions in its fixed canonical new-vertex labeling, retaining previous vertex labels and not quotienting by isomorphism.

Reconstructed counts:

- r=1, top ranks 1 through 7: 1, 1, 1, 1, 2, 7, 60 prefixes.
- r=2, top ranks 1 through 3: 1, 1, 4 prefixes.
- r=3, top ranks 1 through 3: 1, 2, 288 prefixes.
- Of the 60 r=1 rank-seven prefixes, 50 have q_7=0 and 10 have q_7=1.
- Of the 288 r=3 rank-three prefixes, 106 have q_3=0 and 182 have q_3=1.
- Reflection prefixes for r=1,...,5 through rank five pass all checks.
- Young's lattice through rank twelve passes all checks, including proper-S and isolated-vertex cases. At n=12, H_S retains 52 isolated X vertices; its computed q is zero.
- Removing a top vertex from a valid sharp example is rejected by the commutator check.
- The relaxed three-successor minimum is rejected, despite its two valid middle commutators.
- Subtracting 2q instead of q fails in both sharp examples.

The normal, -O and -OO execution outputs are byte-identical: 912318 bytes, SHA-256 `4cf44e1a611ee52374d6a60bb56315ef9319a151c0de628803606fe3d6700a78`. All mathematical guards in the independent program raise explicit exceptions and remain active under optimization.

These computations support implementation, examples and the stated finite cases only. They do not prove the general recurrence, novelty or exhaustive literature coverage. All logical acceptance rests on the complete graph argument audited above.

## Primary-source inspection scope

The audit reused the locally authenticated PDFs; it did not make a fresh network retrieval. Retrieval timestamps recorded by the candidate are provenance supplied by that packet, not independently observed retrievals during this audit.

1. Patrick Byrnes, *Structural Aspects of Differential Posets* (2012 dissertation). Text-read all PDF pages 47-51, covering Lemmas 5.5-5.7, the entire relevant Theorem 1.2 proof, and Conjecture 5.9. Visually inspected PDF pages 48-51. The source's rank-inconsistent sentence on PDF48 says a rank-k vertex covers x,y also in rank k; the intended lower pair is v,w. The audited candidate's independent connectivity induction does not rely on that sentence literally. PDF bytes: 598546; SHA-256: `793156b93f5d17f03f4f7b70ecdb353daa48944cc946cc680927ca97d620f0d8`. Public URL: https://conservancy.umn.edu/server/api/core/bitstreams/45a1bae8-402f-42a7-ad67-4caa7b55d104/content
2. Pritam Majumder, *Rank sizes of Differential Posets*, Oberwolfach Report 23/2018. Text-read PDF pages 72-73 and visually inspected page 72. This confirms the original improvement problem, the separate local recurrence, the weak bound and the erroneous terminal '=1'. PDF bytes: 1261683; SHA-256: `6512c6b53d12d362868ca481bc7445bb97fc465da1e37d2ffdf40127d600e97f`. Public URL: https://ems.press/content/serial-article-files/46745
3. Christian Gaetz and Praveen Venkataramana, *Path Counting and Rank Gaps in Differential Posets*, arXiv:1806.03509v3. Text-read PDF pages 1-4 and visually inspected page 2. This confirms the operator definition, Young-lattice example, reflection construction, global upper bound and separate lower-gap results. PDF bytes: 141194; SHA-256: `834026c42643dac5cd4d9289b4321779f7e2f94ea9bdb2ee9206ac5e15cd1c56`. Public URL: https://arxiv.org/pdf/1806.03509

No full-document inspection beyond these pages is claimed. No newer paper's proof, source-author code, exhaustive current-openness claim or novelty claim was reviewed or accepted. The copied source extracts and rendered images retained as local inspection evidence are third-party source material and are not part of an authored-result publication.
