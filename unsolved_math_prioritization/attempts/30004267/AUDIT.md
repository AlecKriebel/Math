# Independent mathematical audit: fixed-fiber orbits

This is an AI-assisted, unrefereed proof-and-audit edition. Acceptance denotes a separate internal AI mathematical audit of the scoped partial results, not external human peer review, journal acceptance, or formal proof-assistant certification. No novelty or exhaustive current-open-status claim is made. This is not a computational reproduction package: supplementary programs, raw outputs, and third-party source documents are not distributed. The complete written mathematical arguments and their public citations are retained.

Target: **30004267 / OWR-17289-008**.
Verdict: **ACCEPT the stated partial results. The original arbitrary-rank problem is not solved.**
Audited proof SHA-256: `07c92b14c8b550b51c8a8c9189f00f9c02ed6fc2a768483fe3601f908227ada5` (11,095 bytes).
Audit date: 2026-10-11 UTC.

No mathematical correction is required. One bibliographic correction is applied in the distributed PROOF.md: the retained 2017 manuscript locates cell decompositions in §6.4, not §6.3. The harmless row-orientation convention in the ladder application is made explicit below. Acceptance is restricted to the claims listed here; it is neither an exhaustive literature review nor a novelty certificate.

## 1. Exact problem and acceptance boundary

The original report fixes a complex vector space of dimension n+1 and the projections f_i killing basis vectors e_i,e_(i+1), for 1≤i<n. Its maximal-flat fiber consists of subspaces U_i of dimension i satisfying f_i(U_i)⊂U_(i+1). The group is the stabilizer of this one representation M: its elements are invertible tuples g satisfying g_(i+1)f_i=f_i g_i. Reineke's Problem 5 asks for finiteness, parametrization, and closure order for this action for arbitrary n. These data were checked in the original report, PDF pp.19–21. [Original report](https://ems.press/content/serial-article-files/46825)

The audited report preserves that field, dimension vector, fixed module, action, and quantifier. It establishes:

1. For each n≥3, equal isomorphism types of U and M/U, equivalently equal pairs of path-rank arrays, can occur on two orbits whose closures contain neither other orbit.
2. For n=1 there is one orbit; for n=2 there are exactly three, with the stated complete closure order.
3. For n≤4 there are finitely many requested orbits, by application of an existing ladder theorem.

It does **not** establish finiteness for n≥5, an explicit list of n=3,4 orbits or their closure order, or an arbitrary-n classification. It does not assert that the two incomparable closures are disjoint. Changing bases in a varying ambient representation tuple is a different orbit problem. The audited report does not substitute that action or the indexing of irreducible components for the requested action.

## 2. Ambient module check

Each coordinate e_k traces a one-dimensional chain through the vertices, split precisely at arrows k−1 and k when those arrows exist. Decomposing these chains gives

M ≅ ⊕_(j=1)^n [1,j] ⊕ ⊕_(i=2)^n [i,n] ⊕ ⊕_(i=1)^n [i,i].

This has dimension n+1 at every vertex and exactly the prescribed maps. With the usual equioriented projectives P_i=[i,n] and injectives I_j=[1,j], the last two summand families identify with rad(CQ) and CQ/rad(CQ), and the first with (CQ)*. At n=1 the formula gives two copies of [1,1], as required. No special case is silently lost. If n=0 is admitted by convention, there is only the empty tuple and the action is trivial.

## 3. Independent verification of the all-n obstruction

Write r=n−2 and F=span(e_1,…,e_(r−1)). Both points use U_i=span(e_1,…,e_i) through vertex r and use the same final hyperplane, omitting e_n. At the middle vertex they use

A_(r+1)=F⊕span(e_r,e_(r+2)),
B_(r+1)=F⊕span(e_(r+1),e_(r+3)).

The final hyperplane is F⊕span(e_r,e_(r+1),e_(r+3)). Its dimension is r+2=n; the middle dimensions are r+1. Empty F at n=3 causes no degeneracy. The early arrow images are span(e_1,…,e_(i−1)), the arrow-r image is F, and the last images are F⊕Ce_r and F⊕Ce_(r+3). Hence both tuples satisfy every incidence condition.

For a path i→j its diagonal map kills exactly e_i,…,e_j. On either submodule its image therefore has dimension i−1, including the last-arrow case i=r+1. For the quotient, the image is (im T+U_j)/U_j, so its dimension is rank T−dim(im T∩U_j); there is no missing correction term involving U_i because T(U_i)⊂U_j. Direct intersection counting gives the common quotient ranks

- n+1−j when j≤n−2;
- 1 when j=n−1;
- 0 when j=n.

At the last vertex im T is contained in the common hyperplane because every such path kills e_n. These cases exhaust all i<j and include n=3. The vertex dimensions also agree.

For completeness, the interval multiplicity formula used in the report is correct: the rank r_(a,b) counts intervals containing [a,b], and the two finite differences isolate intervals with endpoints exactly a,b. Taking out-of-range left/right terms to be zero handles a=1 and b=n. Thus the equal rank arrays really do imply U^A≅U^B and M/U^A≅M/U^B as representations. This does not identify the embeddings.

### Intrinsic invariants and both directions

At vertex r+1 let W=im f_r∩ker f_(r+1) and H=im f_r+ker f_(r+1). The commuting equations and invertibility imply g_(r+1)(im f_r)=im f_r and g_(r+1)(ker f_(r+1))=ker f_(r+1). Thus W and H are intrinsic invariant subspaces under the exact fixed-fiber group, not merely under a smaller coordinate subgroup.

Computing the subspaces gives W=Ce_(r+2), while H is the hyperplane omitting e_r. The two pairs of intersection dimensions are

(α(A),β(A))=(1,r), and (α(B),β(B))=(0,r+1).

For a fixed L, the locus dim(U_(r+1)∩L)≥d is a determinantal closed set in the Grassmannian: it says that the tautological map U_(r+1)→V/L has rank at most r+1−d. Restriction to the closed fiber preserves closedness. Consequently every point in the closure of an orbit has intersection dimension at least the orbit's constant value.

- B cannot specialize from A: α(B)=0<1=α(A).
- A cannot specialize from B: β(A)=r<r+1=β(B).

This is the correct semicontinuity direction in both cases. Orbit closures are group stable, so the pointwise exclusions also exclude either orbit closure containing the other. A criterion using only the two rank arrays cannot recover closure containment: it sees identical input data for the true reflexive comparison (A,A) and the false comparison (A,B). This conclusion disproves that proposed invariant scheme, not finiteness.

## 4. Small-rank classification

For n=1, GL_2(C) acts transitively on lines in C².

For n=2, let K=ker f and I=im f. The incidence condition for a line L and plane P divides the fiber into precisely the following possibilities:

- O_10: L is outside K; then P contains I.
- O_01: L is in K and P does not contain I.
- O_00: L is in K and P contains I.

The fourth Boolean possibility is impossible. The block matrices in the proof correctly describe all automorphisms. The common scalar c can be fixed to 1 for the transitivity argument: A and the domain shear move L as required; D and the codomain shear independently move P. There is no additional compatibility invariant hidden by the shared scalar.

The loci C_K={L⊂K} and C_I={I⊂P} are closed products P¹×P² and P²×P¹. Their intersection is P¹×P¹. O_01 and O_10 are the respective nonempty dense open complements of that intersection, while O_00 is exactly the intersection. The claimed closures and dimensions follow, and they exhaust the fiber.

## 5. Ladder dependency and orientation

An inclusion U→M is a representation of the commutative two-row equioriented ladder. Isomorphic ladders give isomorphisms h:U→U' and g:M→M with g∘inclusion=inclusion∘h; hence g is an automorphism of the fixed module taking U to U'. Conversely such a g restricts to h. This proves a bijection between ladder isomorphism classes in this subfamily and Aut_Q(M)-orbits, even though bases on the top row are allowed to change.

Escolar–Hiraoka's Definition 3 (PDF p.9) draws vertical arrows upward, whereas the audited proof draws them downward. Interchanging the names/placement of the two rows identifies these bound quivers; horizontal arrows and square relations are unchanged. Use τ_n consisting entirely of forward arrows. Their base field K convention allows K=C. Their Theorem 3 (PDF p.11) states representation-finiteness for lengths at most four. Definition 3 starts at n=2; n=1 was handled separately above. [Versioned primary source](https://arxiv.org/pdf/1404.7588v2)

With finitely many nonzero indecomposable classes, only finitely many multiplicity vectors have any one fixed total dimension vector. Krull–Schmidt then gives finitely many ladder classes. Restricting to injective vertical maps and bottom row isomorphic to M leaves a finite subset. This proves the asserted n≤4 conclusion. It also validates the proposed multiplicity parametrization in principle, with the restrictions stated in the report; no explicit enumeration was supplied or accepted here.

The finite-type theorem is an external mathematical dependency. Its Auslander–Reiten classifications were not independently recomputed. The paper's representation-infinite statement for n≥5 concerns the full category and does not imply infinitude in this fixed-bottom subfamily. The separate matrix example uses the target-row interval [2,3], which is absent from M at n=5. That example is not directly applicable. [Matrix-method source, §5](https://arxiv.org/pdf/1706.10027v2)

## 6. Source and computational verification

The separately retained creator and audit evidence are authenticated by their byte counts and SHA-256 identities. This is byte-identity evidence, not a claim about current worldwide open status. Public metadata identifies the original reviewed proof, the citation-corrected copy, and this edited distribution separately.

The audit executed only newly written audit code, never author or source-author code. Normal, -O and -OO runs independently passed:

- coordinate witness and both path-rank checks for n=3,…,64: 87,358 point/path pairs, each checking both U and quotient ranks;
- ambient interval decomposition checks for n=1,…,64;
- full n=2 orbit enumeration over F₂ and F₃ using explicit automorphism generators, giving orbit sizes (9,12,12) and (16,36,36);
- twelve actual mathematical mutations per mode, all rejected, including false containment in each direction.

These are supplementary checks. Finite-field enumeration does not establish the complex classification, and finitely many n cannot establish the all-n statement; the preceding written arguments do. Finite-prime exploratory rank defects from the author investigation are not accepted evidence for complex moduli. Input fingerprints, source-inspection metadata, and the separate integrity verifier/controls bind the exact reviewed deliverables.

## 7. Final acceptance

Accept the all-n obstruction, n≤2 complete classification, and correctly attributed n≤4 finiteness corollary at the audited proof hash. The distributed proof applies the supplied one-line citation correction; it does not change any mathematical assertion. Preserve PARTIAL status and the exact unresolved gap: fixed-fiber finiteness and a full parametrization/closure order in arbitrary rank, with n≥5 finiteness unproved here. Neither this audit nor the author investigation certified novelty or an exhaustive absence of later solutions.
