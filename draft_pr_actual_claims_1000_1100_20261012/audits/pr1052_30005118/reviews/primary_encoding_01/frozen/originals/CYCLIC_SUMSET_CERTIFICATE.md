# Cyclic sumset recognition and the integer hardness theorem

Date: 2026-10-09. Target: rank 1200, problem 30005118, OWR-10252930-031.

## Conclusion and attribution

The following decision problem is NP-complete under deterministic polynomial-time many-one reductions: given a positive integer n and an explicitly represented subset B of Z/nZ, decide whether B=A+A for some subset A of that same group. This holds both when B is an n-bit characteristic vector and when n and the members of B are listed in binary. Hardness holds already for odd n and targets containing 0 whose canonical representatives lie strictly below n/2.

This conclusion combines the published integer NP-hardness theorem of Abboud, Fischer, Safier, and Wallheimer with the elementary transfer proved below. The underlying NP-hardness construction belongs to those authors. The transfer is supplied here as a source-applicability argument, without an originality claim. The consequence for the requested efficient algorithm is conditional: a polynomial-time algorithm in either of these input models exists if and only if P=NP. No unconditional separation, randomized lower bound, or classification of every possible meaning of “efficient” is claimed.

## Exact target and source theorem

The original target is Problem 15, communicated by Marcelo Campos and attributed to Alon and Granville, on printed page 1228 (PDF page 64) of Oberwolfach Report 22/2022, *Combinatorics, Probability and Computing*, DOI 10.4171/owr/2022/22. Both the input set and the unknown root are subsets of the same cyclic group. The operation is the ordinary self-sumset, allowing repeated summands. The problem does not specify its input representation or a precise running-time definition of “efficient.”

The prior result is Theorem 1.2 of Amir Abboud, Nick Fischer, Ron Safier, and Nathan Wallheimer, *Recognizing Sumsets is NP-Complete*, arXiv:2410.18661v2 (26 October 2024), published in SODA 2025, pages 4484–4506, DOI 10.1137/1.9781611978322.153. It proves NP-completeness for finite integer sets. Its proof on manuscript page 23 gives a polynomial-time reduction from a 3-CNF formula with v variables and c clauses to a set S contained in [0, 2^57(v+c)^4], such that the formula is satisfiable exactly when S=R+R for an integer set R. Page 2 also explicitly states the O((v+c)^4) universe bound. These are the prior statements used here; this certificate does not independently reprove the paper's gadget construction.

Theorem 1.3, concerning fixed-characteristic vector groups, is not needed. Such a group need not be cyclic. The finite-universe notation in the introductory Definition 1.1 does not replace the explicit integer quantifier in Theorem 1.2 and its proof.

Public primary sources:

- Original problem: https://publications.mfo.de/bitstream/handle/mfo/3964/OWR_2022_22.pdf?isAllowed=y&sequence=4
- Hardness manuscript, pinned version: https://arxiv.org/abs/2410.18661v2
- Hardness manuscript body: https://arxiv.org/html/2410.18661v2
- Published record: https://epubs.siam.org/doi/10.1137/1.9781611978322.153

## 1. Normalization over the integers

For a finite nonempty integer set S, put t=min S. If S=R+R, then R is finite and nonempty and

    min S = 2 min R.

Finiteness follows, even if it were not part of the root definition, by fixing r0 in R and injecting R into S by r↦r+r0. The displayed minimum identity follows because every sum is at least twice the minimum of R, and that minimum can be added to itself.

Consequently an odd t is an immediate NO instance. If t is even, define

    B = {s−t : s in S},       M = max B = max S−min S.

Then 0 belongs to B, B is contained in [0,M], and

    S has an integer self-sumset root
        if and only if
    B has an integer self-sumset root.

Indeed, a root R of S gives the integer root R−t/2 of B, and a root T of B gives the integer root T+t/2 of S. This argument works for negative as well as positive t. For a nonempty root T of B, min T=0 and max T=M/2; in particular T is a finite subset of [0,M]. If M is odd, this also shows directly that no integer root exists, although the reduction does not need this additional rejection test.

The source paper normalizes intermediate inputs in its positioning proof on manuscript page 8. That is not a statement that its final output S contains 0: the subsequent skeleton construction translates blocks. The independent normalization above avoids assuming any final-output minimum or parity beyond what is explicitly proved here.

## 2. Zero-anchor transfer lemma

**Lemma.** Let M be a nonnegative integer, let B be a nonempty subset of {0,…,M} containing 0, and let n be an odd positive integer with n>2M. Identify B with its image in Z/nZ. Then B is an integer self-sumset if and only if it is a self-sumset in Z/nZ. In fact, every cyclic root, represented in {0,…,n−1}, is an integer root of B.

**Proof.** The forward implication follows by reducing an integer root and all its pair sums modulo n. Equivalently, a root of normalized B has minimum 0 and maximum M/2, so its sums do not wrap.

For the converse, suppose A+A=B in Z/nZ. Since 0 belongs to B, there are a,c in A with a+c=0 in the group. Hence c=−a. The elements 2a and 2c=−2a are both in B, because repeated summands are allowed. Let b1,b2 be their canonical integer representatives in B. They satisfy

    b1+b2 ≡ 0 (mod n),       0 ≤ b1+b2 ≤ 2M < n.

Thus b1+b2=0 as an integer equality, and b1=b2=0. It follows that 2a=0 in Z/nZ. Since n is odd, multiplication by 2 is injective, so a=0. Therefore 0 belongs to A.

For every x in A, x=x+0 belongs to B. Let T be the canonical integer representatives of A. The preceding inclusion says T⊆B⊆[0,M]. Every ordinary sum x+y of two members of T lies in [0,2M], which is contained in [0,n−1]. Its residue lies in B, so the ordinary sum itself lies in B. This gives T+T⊆B.

Conversely, every b in B is represented by a pair from A. The corresponding representatives x,y in T have 0≤x+y<n and 0≤b<n. Their congruence x+y≡b modulo n therefore implies x+y=b. This gives B⊆T+T and proves equality. □

The two crucial ingredients are the zero anchor and the absence of 2-torsion. Arbitrarily reducing an unnormalized integer instance is unsafe: {1} has no integer root, but in Z/5Z it equals {3}+{3}. The lemma makes no assertion about all roots being anchored when n is even. For example, {n/2}+{n/2}={0} in an even-order group.

## 3. A total many-one reduction

The reduction accepts an explicitly listed finite integer set S, removes any duplicate encodings, and returns a cyclic instance as follows.

1. If S is empty, return n=3 and B empty. This is YES, witnessed by the empty root, on both sides.
2. If S is nonempty and min S is odd, return n=5 and B={0,1}.
3. Otherwise form t, B, and M as in Section 1 and return n=max(3,2M+1), with B interpreted in Z/nZ.

The fixed instance in step 2 is NO. To see this without brute force, apply the zero-anchor lemma with M=1 and n=5. Any cyclic root would be an integer root T contained in {0,1}. Representing 1 requires 1 in T, but then 2=1+1 belongs to T+T and is not in {0,1}, a contradiction.

For step 3, n is odd and n>2M, so normalization and the lemma establish the exact YES/NO equivalence. The zero-diameter case M=0 produces n=3 and B={0}, witnessed by A={0}. Thus empty sets, singleton sets, negative minima, odd minima, and M=0 are covered. The reduction uses only translation, comparison, parity, and ordinary integer arithmetic; it requires no prime search or factorization.

## 4. Input encoding and polynomial size

**Sparse encoding.** The input specifies n in binary and lists the distinct residues in B in binary, with 0≤b<n. An instance has size O(log(n+1)+|B| log(n+1)). For a sparse integer source, the difference max S−min S and n=max(3,2M+1) have polynomial bit length in that source's encoding length. Translation and output of at most |S| residues are polynomial-time operations. Thus Section 3 is a polynomial reduction for sparse input without using the stronger numerical universe bound.

**Dense encoding.** The input is n together with an n-bit characteristic vector for B. Applying Section 3 to an arbitrary binary-encoded integer instance might create an exponentially long bit vector. For the dense hardness result, instead compose Section 3 directly with the bounded-universe 3-SAT reduction from the prior theorem. For N=v+c≥1 its output satisfies S⊆[0,U] with U=2^57 N^4. Whenever step 3 applies, M≤U and

    n=max(3,2M+1) ≤ max(3,2U+1) = O(N^4).

The exceptional outputs have constant size. Producing the characteristic vector takes O(n) elementary writes, hence polynomial time. The large numerical constant in U affects practicality but not polynomial-time reducibility. A formula with no variables or clauses can be handled by a fixed constant YES instance.

These two separate arguments establish NP-hardness in both models. They also show hardness under the stated restrictions, since all nonconstant normalized outputs have odd n, contain 0, and lie below n/2; the fixed YES output may be chosen as (3,{0}) instead of (3,empty) if an everywhere-nonempty restricted target language is desired. The fixed NO instance (5,{0,1}) satisfies the same restrictions.

## 5. Membership in NP

For dense input, supply an n-bit indicator of A, compute every sum modulo n, and compare the resulting set with B. This has polynomial certificate size and O(n^2) pair operations.

Sparse input needs an additional size argument because n can be exponentially larger than its binary encoding. If B is nonempty and A+A=B, fix a0 in A. Translation a↦a+a0 is an injection from A into B, so |A|≤|B|. A root can therefore be given as at most |B| binary residues, requiring O(|B| log(n+1)) bits. The verifier checks the residues, computes the at most |B|^2 modular pair sums, removes duplicates or sorts them, and checks exact equality with the given set B. Binary arithmetic and sorting take polynomial time in the input length. For B empty, the empty certificate A suffices. This argument applies to all positive n, including even n; the odd-order restriction is used for hardness, not membership.

NP-hardness from Section 4 together with these verifiers proves NP-completeness for both explicit models.

## 6. Verification and limits

The universal correctness proof is Sections 1–5.

The original source page and the manuscript's theorem, positioning normalization, and final reduction-size calculation were visually inspected. Publication metadata was freshly checked against SIAM; the arXiv manuscript is the inspected proof version. The accepted published theorem is used as a mathematical dependency, not described as independently audited here.

The result addresses the literal same-cyclic-group target with ordinary self-sums. It does not concern restricted sums a≠b, two unrelated summand sets, compact circuit encodings of B, query-only input, approximation, or average-case recognition. For a single fixed n there is of course only a finite family of instances; the hardness concerns unbounded n supplied with the input. This certificate supplies no exhaustive novelty guarantee and no new NP-hardness gadget construction.
