# Orbital, transition-chain, tower, and germ approach

Researcher: independent dynamics subagent. Author metadata for project: Alec Kriebel, ORCID https://orcid.org/0009-0001-9320-500X .

## Checkpoint 2026-10-17 21:02 UTC — 10% discovery estimate

The exact target is the Brin–Sapir dichotomy for every subgroup of the finite dyadic PL group F. No full proof or counterexample is established here. A finite-generation reduction is valid because elementary amenability is closed under directed unions. All statements below keep the distinction between an orbital of a group and an orbital of an element.

### Primary evidence checked

* Brin, *The ubiquity of Thompson’s group F in groups of piecewise linear homeomorphisms of the unit interval* (1999), Theorem 1: an element approaching exactly one endpoint of a **group orbital** forces a copy of F. Original preprint: https://arxiv.org/abs/math/9705205 . Locally cached full text: dynamics_sources/brin_ubiquity.txt .
* Bleak, *A geometric classification of some solvable groups of homeomorphisms* (2006), Theorem 1.1: finite tower depth equals derived length. https://arxiv.org/abs/math/0602036 . This is a solvability theorem, not an elementary-amenability classification. Its final open question about finitely generated chainless nonsolvable groups is obsolete; see the next source.
* Bleak–Brough–Hermiller, *Determining solubility for finitely generated groups of PL homeomorphisms*, Theorem 3.1: a finitely generated group is nonsoluble iff it admits a transition chain iff a one-sided overlap iff an infinite tower. Corollary 1.1 gives a copy of the Brin–Navas group B in every finitely generated nonsoluble group. Primary institutional full text: https://research-repository.st-andrews.ac.uk/bitstream/10023/21656/1/infiniteDescent33.pdf . This cannot replace B by F: B is elementary amenable and nonsoluble.
* Bleak–Brin–Moore, *Complexity among the finitely generated subgroups of Thompson’s group* (2021): https://arxiv.org/abs/1711.10998 . The normal-form, ordinal, and well-foundedness theorems apply to a specified family of fast standard generating systems. Extending coverage to arbitrary F-free groups is conjectural, not a proven reduction step.
* Bromlyn Cameron, PhD thesis *Abstract ping-pong systems in subgroups of Thompson’s groups*, repository date 02/07/2026, https://research-repository.st-andrews.ac.uk/handle/10023/33513 . Search-indexed full-text excerpts identify Conjectures 3.1.37/38 concerning bounded/unbounded transition-chain length and the EA/F dichotomy. Exact full-text hypotheses still need verification: repository PDF retrieval has returned 503/timeouts. The repository metadata and abstract are accessible. No unpublished or outside communication was used.

### Verified deductions, reproduced independently

**Proposition 1 (endpoint rank obstruction).** Let H ≤ F have no subgroup isomorphic to F. Let J=(a,b) be any orbital of H. For h∈H set L(h)=log_2 h′(a+) and R(h)=log_2 h′(b−). Then L,R:H→Z are homomorphisms, ker L=ker R, and the joint image (L,R)(H) is either zero or infinite cyclic. If an endpoint is approached by an element, the image is nonzero.

**Proof.** Every h fixes a and b. Finite PL structure gives one-sided affine germs, and the chain rule makes their logarithms additive. A germ has slope 1 exactly when h is the identity on some corresponding one-sided neighborhood, because h fixes that endpoint. A nontrivial germ is exactly an element orbital approaching that endpoint. If ker L differed from ker R, Brin’s theorem would yield F in H. Hence the kernels agree. If the joint image had rank 2, choose two integer image vectors (p,q),(r,s) with ps−rq≠0. The element h^r k^(−p) would have left logarithm 0 and right logarithm rq−ps≠0, again impossible. Every subgroup of Z² of rank ≤1 is cyclic. The zero case is allowed for infinitely generated H with no element approaching either endpoint. ∎

A concrete finite certificate follows: if two elements h,k approach the endpoints of a group orbital J and their two endpoint-log vectors have nonzero determinant, a power product has exactly one active endpoint, so H contains F by Brin. This conclusion is a known theorem’s elementary corollary, not a novelty claim.

**Proposition 2 (global endpoint-kernel normal form).** Let H=〈S〉≤F be finitely generated and F-free. Use open support Supp(H)={x:some h∈H moves x}. Write the finitely many group orbitals as J_i=(a_i,b_i), i=1,…,r. Let λ_i be the left endpoint logarithm on J_i and λ=(λ_1,…,λ_r):H→Z^r. Then N=ker λ consists exactly of the elements which are identity near both endpoints of every J_i. The image is a free abelian group of rank ≤r. Consequently, if N is elementary amenable then H is elementary amenable.

**Proof.** Supp(H)=⋃_{s∈S}Supp(s), so it has finitely many components. Each λ_i is a homomorphism. Proposition 1 identifies the vanishing of the left and right endpoint germs. Thus an element is in ker λ precisely when all these finitely many pairs of germs vanish. The image is a subgroup of Z^r. Closure of EA under extensions proves the last assertion. ∎

For one group orbital, λ(H)=dZ with d>0, because a finite generating set realizes the endpoints. Choose t∈H with λ(t)=d and put k_s=s t^(−λ(s)/d). Then

    H=〈t,{k_s:s∈S}〉,
    N=〈t^(−j) k_s t^j : j∈Z, s∈S〉,
    N=⋃_{n≥0}〈t^(−j) k_s t^j : |j|≤n, s∈S〉.

Every finite-window subgroup is supported in a compact subset of the group orbital. This is an exact normal-form reduction. It supplies no rank decrease by itself and must not be promoted to an EA proof.

### Mechanism status and exact gaps

1. **Brin endpoint imbalance:** verified detection mechanism. F-free groups are balanced, including all their subgroups. The converse has not been assumed.
2. **Tower height/solvability:** verified for finite depth and for the finitely generated chainless case. Blocked as a full route because nonsoluble EA groups already exist; infinite towers are not an F certificate.
3. **Controlled wreath decomposition:** verified when an explicit generating family has the disjoint fundamental-domain conditions needed for a restricted wreath product. Blocked for arbitrary groups because compactly supported kernel generators can have overlapping conjugates; no-F alone has not been shown to organize them into a well-founded decomposition.
4. **Endpoint-kernel recursion:** exact reduction above. Blocked at the crucial claim that all finite-window compact kernel subgroups have strictly smaller complexity. No such universally defined well-founded complexity has been established. Calling support intervals strictly smaller is insufficient, since the intervals can shrink forever and conjugacy can relocate arbitrary copies.
5. **Fast standard systems/ordinal normal forms:** validated published coverage only. The assertion that an arbitrary F-free finite generating set can be transformed into a covered system would transfer the central difficulty to a known stronger conjecture. Route blocked unless a new transformation is proved.

### Adversarial checks already applied

* An **element** orbital (a,c) sharing one end with another element orbital (a,b) is not necessarily an orbital approaching exactly one end of the **group** orbital (a,b). The same element may have a second bump reaching b. Hence one-sided overlaps do not automatically yield F.
* “F-free implies soluble” is false: the elementary amenable Brin–Navas group B is finitely generated and nonsoluble.
* Splitting bumps need not preserve H. It need not even preserve the standard dyadic F when an element fixes a nondyadic point inside an affine segment: the cut introduces a nondyadic breakpoint.
* The endpoint logarithm argument uses slopes in 2^Z. In general PL_+(I), endpoint log images can be nondiscrete subgroups of R, so the cyclic quotient conclusion requires a separate theorem or the discrete slope hypothesis.
* A restriction projection is a quotient. A copy of F in a quotient must not silently be treated as a copy in H without a lifting argument.

No solution, no novel contribution, and no verified counterexample are currently claimed.


## Checkpoint 2026-10-17 21:03:39 UTC — 10% discovery estimate

Independent adversarial audit by subagent `audit_germ_reduction` found Propositions 1–2 and the one-orbital normal-closure formula valid, including nondyadic endpoints, and specifically confirmed the zero-germ exception for infinitely generated groups. The audit does not validate any missing complexity descent. No solution has emerged, so the discovery estimate remains 10%.

### Additional rigorous corollary: compact-kernel descent

**Proposition 3.** If a finitely generated counterexample H_0≤F to the dichotomy exists, then there is an infinite sequence of finitely generated counterexamples H_0≥H_1≥H_2≥… such that H_{n+1} lies in the endpoint-germ kernel N_n of H_n and

    closure(Supp(H_{n+1})) ⊂ Supp(H_n),

where support is open support. The inclusion is proper as a containment of subsets of [0,1].

**Proof.** H_n/N_n is finitely generated free abelian by Proposition 2. If N_n were EA, the extension H_n would be EA. Thus N_n is not EA. It is the directed union of its finitely generated subgroups, so some finitely generated H_{n+1}≤N_n is not EA. It remains F-free as a subgroup of H_n. Every one of its finitely many generators is identity near every one of the finitely many endpoints of H_n orbitals, and outside their union. Its total support therefore has closure compactly contained in Supp(H_n). The nonempty support of H_n cannot equal this closed compact subset of itself. Induction completes the construction. ∎

This construction uses actual subgroups throughout, not projections, and therefore avoids quotient lifting. It provides a useful necessary structure for a counterexample. It is **not** a contradiction: nested compact supports can persist indefinitely. Even their nonempty nested intersection is consistent with all stated hypotheses. A proof that nonEA cannot persist along this descent would itself require a new mechanism.

### Explicit boundary-case artifact: bump cutting can leave F

Define f:[0,1]→[0,1] by

    f(x)=x/2                  for 0≤x≤1/4,
    f(x)=4x−7/8               for 1/4≤x≤3/8,
    f(x)=x/2+7/16             for 3/8≤x≤7/8,
    f(x)=x                    for 7/8≤x≤1.

At the successive breakpoints the values are 1/8, 5/8, and 7/8. Hence f is a strictly increasing continuous PL homeomorphism, all breakpoints are dyadic, and all slopes are powers of 2: f∈F. Its orbitals are (0,7/24) and (7/24,7/8). The right bump restriction equals identity immediately left of 7/24 and has slope 4 immediately right, so it introduces the nondyadic breakpoint 7/24 and is not in F. This is a counterexample only to an invalid proof step, not to the research conjecture.

### Updated literature boundary, exact indexed text

Cameron thesis p88, Conjecture 3.1.37, is explicitly for finitely generated G≤PL_+(I): elementary amenability is conjecturally equivalent to a universal bound on transition-chain length. The accompanying remark explains why finite generation is indispensable: an EA directed limit can contain groups with arbitrarily large chain complexity. Indexed p89 Conjecture 3.1.38 posits the equivalence of unbounded chain length and F containment; Theorem 3.1.39 proves only F containment ⇒ unbounded chain length. Thus attempting the reverse implication without a new argument merely restates an open companion conjecture.

Second independent audit confirmed Proposition 3 and the explicit f bump-cut obstruction at approximately 2026-10-17 21:03:39 UTC. No error was found; neither result closes the central gap.
