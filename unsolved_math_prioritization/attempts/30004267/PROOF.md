# Fixed-fiber orbits in the maximal flat flag degeneration

This is an AI-assisted, unrefereed proof-and-audit edition. Acceptance denotes a separate internal AI mathematical audit of the scoped partial results, not external human peer review, journal acceptance, or formal proof-assistant certification. No novelty or exhaustive current-open-status claim is made. This is not a computational reproduction package: supplementary programs, raw outputs, and third-party source documents are not distributed. The complete written mathematical arguments and their public citations are retained.

## Status and exact target

This is a partial result, not a resolution of Reineke's Problem 5 in Oberwolfach Report 46/2019, printed page 2889 (PDF page 21). The problem asks, for arbitrary n, whether the group Aut_Q(M) has finitely many orbits on the fixed maximal-flat fiber and, if it does, for a parametrization and the orbit-closure relation. Here Q is 1→2→⋯→n, V=C^(n+1) with basis e_1,…,e_(n+1), f_i kills e_i and e_(i+1) and fixes all other basis vectors, M=(V,f_i), and

X_n = { (U_1,…,U_n) : dim U_i=i, f_i(U_i)⊂U_(i+1) }.

The action is g·U=(g_i U_i), where g_(i+1)f_i=f_i g_i and every g_i is invertible. This is not the action of GL(V)^n on varying map tuples. In interval notation [a,b],

M ≅ ⊕_(j=1)^n [1,j] ⊕ ⊕_(i=2)^n [i,n] ⊕ ⊕_(i=1)^n [i,i].

This agrees with rad(CQ) ⊕ CQ/rad(CQ) ⊕ (CQ)*. We use the usual n≥1 convention; if n=0 is allowed, the fiber is one point and its action is trivial.

Results below:

1. For every n≥3, the two path-rank arrays of U and M/U together fail to classify the requested orbits. In fact, explicit examples with the same arrays have incomparable orbit closures.
2. For n=1 and n=2, the full orbit classification and closure order are elementary and given below.
3. For n≤4, finiteness follows from the existing representation-finiteness theorem for commutative ladders. This is an application of an earlier result, not a newly claimed finiteness theorem.

General finiteness for n≥5, an arbitrary-n parametrization, and an arbitrary-n closure order remain unresolved by this work. No priority or novelty claim is made.

## 1. The rank-pair obstruction, for every n≥3

For a subrepresentation U, let R^U_(i,j) be the rank of f_(j−1)⋯f_i on U_i, for i<j. Let R^(M/U)_(i,j) be the rank of the induced quotient map. Together with the dimensions at the vertices, each array determines the isomorphism class of its equioriented type-A representation: indeed the multiplicity of [a,b] is

r_(a,b) − r_(a−1,b) − r_(a,b+1) + r_(a−1,b+1),

with r_(i,i) equal to the vertex dimension and terms beyond the left/right boundary zero. This follows either by applying the formula to each interval summand, or by the elementary interval decomposition of a chain of linear maps.

### Construction

Put r=n−2 and F=span(e_1,…,e_(r−1)), with F=0 if r=1. Define U^A and U^B identically except at vertex r+1:

- U^A_i=U^B_i=span(e_1,…,e_i), for 1≤i≤r;
- U^A_(r+1)=F ⊕ span(e_r,e_(r+2));
- U^B_(r+1)=F ⊕ span(e_(r+1),e_(r+3));
- U^A_n=U^B_n=F ⊕ span(e_r,e_(r+1),e_(r+3)).

These subspaces have the required dimensions. For i<r, f_i(U_i)=span(e_1,…,e_(i−1))⊂U_(i+1). At arrow r, f_r(U_r)=F, which lies in both middle subspaces. At the last arrow, the images are respectively F⊕C e_r and F⊕C e_(r+3), both contained in U_n. Thus both points belong to the exact fiber X_n.

### Equality of both rank arrays

For i<j, the composite f_(j−1)⋯f_i kills precisely e_i,…,e_j. If i≤r, its restriction to U_i has image span(e_1,…,e_(i−1)), independent of which point was chosen. At i=r+1, the last-arrow images displayed above both have dimension r. Consequently

R^(U^A)_(i,j)=R^(U^B)_(i,j)=i−1, for every i<j.

For any U and any such path map T:V_i→V_j,

rank(T on M/U) = rank(T) − dim(im T ∩ U_j).

This identity holds because the quotient map has image (im T+U_j)/U_j; the subrepresentation condition makes it well defined on V_i/U_i.

If j≤r, im T ∩ U_j=span(e_1,…,e_(i−1)). If j=r+1, with i≤r, this intersection has dimension i: its common F-part has dimension i−1 and the remaining basis vector is e_(r+2) for A or e_(r+3) for B. If j=n, the whole image of T lies in U_n, since im T omits e_n while U_n is precisely the hyperplane omitting e_n. It follows that both quotient arrays are

R^(M/U)_(i,j) =
- n+1−j, if j≤n−2;
- 1, if j=n−1;
- 0, if j=n.

Thus U^A≅U^B and M/U^A≅M/U^B. This is a statement about the representations alone, not about their embeddings in M.

### Separation and incomparability of orbit closures

At vertex r+1 set

W = im f_r ∩ ker f_(r+1) = C e_(r+2),
H = im f_r + ker f_(r+1) = span{e_k : k≠r}.

Every g∈Aut_Q(M) preserves both im f_r and ker f_(r+1), hence also W and H. Therefore

α(U)=dim(U_(r+1)∩W),  β(U)=dim(U_(r+1)∩H)

are constant on each orbit. Their values at the constructed points are

(α(U^A),β(U^A))=(1,r),
(α(U^B),β(U^B))=(0,r+1).

They distinguish the orbits. Moreover, for a fixed subspace L⊂V, the condition dim(U_(r+1)∩L)≥d is closed in the Grassmannian: it is a rank bound on U_(r+1)→V/L. Hence α and β can only increase in an orbit-closure specialization. If U^B were in the closure of the orbit of U^A, α would have to be at least 1, contrary to α(U^B)=0. If U^A were in the closure of the orbit of U^B, β would have to be at least r+1, contrary to β(U^A)=r. This proves incomparability.

In particular, no criterion depending only on these two rank arrays can be equivalent to orbit-closure containment: the arrays are equal on A and B, while containment fails in both directions. This disproves that proposed shortcut, not the original finite-orbit question.

For n=3 the example is especially small:

U^A=(⟨e_1⟩, ⟨e_1,e_3⟩, ⟨e_1,e_2,e_4⟩),
U^B=(⟨e_1⟩, ⟨e_2,e_4⟩, ⟨e_1,e_2,e_4⟩).

## 2. Complete answer for n≤2

For n=1, X_1=Gr_1(C^2), and Aut(M)=GL_2(C) acts transitively. There is one orbit.

For n=2 write f=f_1, K=ker f=⟨e_1,e_2⟩ and I=im f=⟨e_3⟩. A point is a line L=U_1 and a plane P=U_2 with f(L)⊂P. There are precisely three orbits:

- O_10: L is not contained in K; necessarily I⊂P. Representative (⟨e_3⟩,⟨e_1,e_3⟩).
- O_01: L⊂K and I is not contained in P. Representative (⟨e_1⟩,⟨e_1,e_2⟩).
- O_00: L⊂K and I⊂P. Representative (⟨e_1⟩,⟨e_1,e_3⟩).

The labels are (rank f|_L, rank of the induced quotient map).

To verify transitivity, split the domain as K⊕C e_3 and the codomain as I⊕J, where J=⟨e_1,e_2⟩. Every automorphism pair has the form

g_1 = [[A,b],[0,c]],   g_2 = [[c,d],[0,D]],

where A∈GL(K), D∈GL(J), c≠0, b∈Hom(C e_3,K), and d∈Hom(J,I). The single shared entry c expresses g_2 f=f g_1. A acts transitively on lines in K; the choices of b make the action transitive on lines outside K. Independently, D acts transitively on planes containing I (equivalently lines in J), and the choices of d act transitively on the graphs J→I, which are the planes not containing I. These operations prove the claimed three transitivity statements, despite the shared scalar c.

Set C_K={L⊂K} and C_I={I⊂P}. The incidence relation implies X_2=C_K∪C_I. There are natural isomorphisms C_K≅P^1×P^2 and C_I≅P^2×P^1, and C_K∩C_I≅P^1×P^1. They are closed irreducible subvarieties. The preceding orbit description gives

closure(O_10)=O_10∪O_00=C_I,
closure(O_01)=O_01∪O_00=C_K,
closure(O_00)=O_00.

The two dimension-3 orbits are incomparable; the common dimension-2 orbit is closed. This is the full closure order for n=2.

## 3. Finiteness for n≤4 from the existing ladder theorem

Let CL_n be the bound quiver with two equioriented A_n rows and vertical arrows from the top to the bottom, subject to commutativity of every square. Associate to U⊂M the representation E(U) whose top row is U, whose bottom row is M, and whose vertical maps are the inclusions.

Then E(U)≅E(U') if and only if U and U' are in the same Aut_Q(M) orbit. In one direction restrict an automorphism of M carrying U to U'. In the other direction, an isomorphism of the two ladder representations has bottom-row component g∈Aut_Q(M), and commutation with the inclusions says g_i U_i=U'_i. This argument is elementary and works for every n.

Escolar and Hiraoka, “Persistence Modules on Commutative Ladders of Finite Type,” arXiv:1404.7588v2, Theorem 3 (PDF p.11), prove that CL_n is representation-finite for n≤4, for all common orientations of the two rows. Therefore there are finitely many isomorphism classes of ladder representations of the fixed dimension vector (1,…,n; n+1,…,n+1). A fortiori, its subcollection with fixed bottom row M and injective vertical maps is finite. This proves finiteness for the requested action when n≤4.

For the cited source's upward vertical-arrow convention, interchange the placement/names of the two rows; this leaves the horizontal orientation and commutativity relations unchanged. Take the common horizontal orientation entirely forward. The source's field K can be C; its definition starts at n=2, while n=1 is treated separately above.

This also gives an existing finite parametrization in principle: use multiplicities of the finite set of indecomposable CL_n representations, retain only those with injective vertical maps, prescribed bottom-row isomorphism type M, and prescribed top-row dimensions. Krull–Schmidt uniqueness makes the multiplicity data complete. We have not explicitly enumerated that parametrization or its closure order for n=3,4 in this packet.

The ladder theorem does not prove the arbitrary-n target. Its statement of representation-infinite behavior for n≥5 concerns the whole ladder category. That does not prove infinitely many orbits in this particular fixed-bottom, injective-vertical subfamily. Likewise the 2×2 matrix obstruction displayed in §5 of Asashiba–Escolar–Hiraoka–Takeuchi, arXiv:1706.10027 (PDF pp.28–29), uses a row interval [2,3] absent from our M at n=5, so it cannot simply be imported.

## 4. Dependencies and limits

The all-n obstruction and the n≤2 classification are self-contained linear-algebra and algebraic-group arguments. The ladder finiteness corollary depends on the cited existing theorem; its Auslander–Reiten classifications have not been independently recomputed here. Historical computational checks summarized in AUDIT.md validate the explicit constructions in finitely many dimensions and fields, not arbitrary-n finiteness.

The 2017 paper “Linear degenerations of flag varieties” gives affine cell decompositions in §6.4 (PDF pp.30–33). Cells whose points are isomorphic as Q-representations need not automatically be single Aut_Q(M) orbits. Its ambient representation-space rank parametrizations and the corresponding statements in Di Trani's 2025 preprint are also different from the target action.

No source-author code was run. Source documents and supplementary computational material are excluded from this prose edition.

## Public source links

- Reineke's original report and Problem 5: https://ems.press/content/serial-article-files/46825 (PDF pp.19–21).
- Cerulli Irelli–Fang–Feigin–Fourier–Reineke, Linear degenerations of flag varieties: https://eprints.gla.ac.uk/124027/7/124027.pdf ; DOI https://doi.org/10.1007/s00209-016-1839-y .
- Escolar–Hiraoka, Persistence Modules on Commutative Ladders of Finite Type: https://arxiv.org/abs/1404.7588v2 ; Theorem 3, PDF p.11.
- Asashiba–Escolar–Hiraoka–Takeuchi, Matrix Method for Persistence Modules on Commutative Ladders of Finite Type: https://arxiv.org/abs/1706.10027v2 ; §5, PDF pp.28–29; published version https://doi.org/10.1007/s13160-018-0331-y .
- Di Trani, Regularity in Linear Degenerations of Flag Variety: https://arxiv.org/abs/2507.23055 ; used only to distinguish the scope of regularity results.
