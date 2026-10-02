# Turn 2 — Exact component counts for disjoint product blocks

AI-assisted mathematical proof candidate; independent review pending. Original unresolved2/5. This treats systems whose monomials have mutually disjoint variable supports; overlapping monomials in arbitrary multi-affine pairs remain outside the result.

## 1. Statement

Partition variables into disjoint nonempty blocks B_i of sizes k_i, for1≤i≤m, and put p_i=Π_(j∈B_i)x_j. Consider r equations

Σ_i A_(a,i)p_i=c_a,    1≤a≤r,

with arbitrary real matrix A and constants c. Extra unused variables and separate affine shifts x_j↦x_j−b_j are harmless. Let H={h∈R^m:Ah=c}. If H is empty, so is the common zero set X. Otherwise let I be the coordinates i for which h_i is a fixed nonzero constant on H. Then

b₀(X)=2^(Σ_(i∈I)(k_i−1)).

All these components are path connected. In particular |I|≤rank A≤r. If every block size is at most d, then b₀(X)≤2^(r(d−1)). For two equations of degree at most d, this is the sharp bound2^(2d−2) within the stated class.

A degree-sensitive version is b₀(X)≤2^(Σ_a max(deg F_a−1,0)), ignoring inconsistent constant equations in the empty case. In particular for two nonconstant equations of degrees d1,d2 the bound is2^(d1+d2−2).

## 2. Fibers and global sections

The map p:R^(Σk_i)→R^m taking block products is surjective, and X=p⁻¹(H). For a single block of size k and a nonzero product h, the fiber Πx_j=h has2^(k−1) path components, distinguished by the signs of its first k−1 coordinates. Each is path connected: linearly interpolate the positive absolute values of the first k−1 coordinates to |h|^(1/k), retaining their signs, and set the last coordinate equal to h divided by their product. None of the denominators vanishes. For h=0 the fiber is the union of coordinate hyperplanes and is path connected, since every point scales to the origin. These statements include k=1.

For every sign vector σ∈{±1}^(k−1), define a continuous global section of the one-block product map by

x_j=σ_j |h|^(1/k) for j<k,
x_k=sign(h)(Π_(j<k)σ_j)|h|^(1/k),

and set all coordinates to0 at h=0. The section is continuous at0, and its product is h. Taking products over the blocks gives finitely many continuous sections s_σ:H→X. Each image is path connected because H is affine and therefore path connected. Every point in X is joined within its product fiber to one of these sections.

## 3. Which section branches connect

If coordinate h_i is not a fixed nonzero constant on H, then H contains a point with h_i=0. Indeed an affine coordinate function on a nonempty affine space is either constant or has image all of R; a constant zero also satisfies this condition. At such a point all section choices in block i coincide at the zero vector. Therefore any two sections differing only in block i belong to the same path component of X. Repeating these single-block changes connects every pair of sections with the same branch choices on the fixed-nonzero blocks I.

Conversely, for i∈I every coordinate of the i-th variable block is nonzero throughout X, since its product is the fixed nonzero h_i. Their sign pattern cannot change along a connected subset. The first k_i−1 signs distinguish2^(k_i−1) choices, and all choices are realized by the sections. Thus different choices on I belong to different connected components, while the preceding argument makes each such class path connected. This proves the exact formula, without any compactness, genericity, or constant-rank assumption on a nonlinear projection.

## 4. Dimension-free and degree-sensitive bounds

For i∈I, the coordinate functional e_i vanishes on ker A, hence lies in the row space of A. These coordinate functionals are linearly independent, so |I|≤rank A. This proves the maximum-degree bound.

For the sharper bound, the columns of A indexed by I are linearly independent. Otherwise a nonzero vector v supported on I with Av=0 would contradict e_i∈row(A) for every i∈I. Some |I|×|I| minor on those columns is therefore nonzero. At least one term in its determinant is nonzero, giving a matching of the indices i∈I to distinct equation rows a(i) with A_(a(i),i)≠0. Because the blocks are disjoint, this coefficient contributes a genuine degree-k_i monomial to row a(i), without cancellation with another block. Hence k_i≤deg F_(a(i)), and

Σ_(i∈I)(k_i−1)≤Σ_(a matched)(deg F_a−1)≤Σ_a max(deg F_a−1,0).

Constant rows have no nonzero matching entries and do not affect the argument.

Sharpness is witnessed by independent equations p_1=1,…,p_r=1 on r blocks of size d, with any extra variables free. The product fibers have exactly2^(r(d−1)) components. For different row degrees use corresponding block sizes. These basic product examples are closely related to the credited sharp one-polynomial example of Basu–Perrucci; no discovery priority is asserted for them.

## 5. Exact computation and scope

For rational input, Gaussian elimination decides emptiness of H and produces a particular solution h⁰ and a basis of ker A. A coordinate i belongs to I precisely when every nullspace vector has zero i-th coordinate and h⁰_i≠0. The formula therefore computes b₀ exactly using rational linear algebra, without enumerating real components. This is an algorithm only for the disjoint-product-block class.

`python turn2/check_block_products.py` checks300 small rational systems including nine inconsistent cases, verifies coordinate-zero feasibility and the fixed-coordinate criterion, compares exact branch-graph counts, and checks balanced sign sections at perfect powers. All3,108 assertions pass; stdout is frozen in turn2/verification.json. These finite tests supplement the full path argument.

This does not bound components for arbitrary pairs of multi-affine polynomials: shared variables between distinct monomials invalidate the product-coordinate surjection with independent block fibers. In particular the symmetric elementary-polynomial three-equation construction has extensive overlapping supports and is not covered. Nor is this a bounded-box result, where the unrestricted sections/paths could leave the domain.

Primary problem and existing one-polynomial bounds: OWR9/2025 printed445–446, https://ems.press/content/serial-article-files/51353; Basu–Perrucci, https://arxiv.org/abs/2204.01595, Theorem2 and Example2.1. The proof here is elementary and self-contained, with no novelty certification. Original unresolved2/5; informal completion estimate25%.
