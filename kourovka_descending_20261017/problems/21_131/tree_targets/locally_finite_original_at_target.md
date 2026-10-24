# A countable locally finite AT p-group with infinite-support longitudinal generators

Author metadata: Alec Kriebel, ORCID <https://orcid.org/0009-0001-9320-500X>.

Status as of 2026-10-24 18:39 UTC: self-contained proof independently adversarially verified; mathematical target subgoal 100% under the supplied original definition. The construction is not claimed novel. It supplies a target for Kourovka 21.131, not by itself a solution of the Golod realization problem.

## Exact target and definition

For each prime p, construct a countable, infinite, locally finite p-group H which is AT in the original 1986 definition. In particular, every selected longitudinal generator must have infinite level support. Infinitely many selected generators are permitted.

The original definition used is Rozhkov, *Theory of Aleshin type groups*, Russian original *Mat. Zametki* 40(5) (1986), 572–589; English translation *Math. Notes* 40(5), 827–836, DOI <https://doi.org/10.1007/BF01159699>. Its relevant primary OCR receipt, including the infinite-support clause and the subgroup/subset distinction, is copied in `sources/`. The receipt is not original PDF bytes; see its explicit access limitation. The group's construction and proofs below are independent deductions, not attributed quotations.

## Construction

Let T be the rooted regular p-ary tree with alphabet A={0,...,p−1}. Let a be the root automorphism whose local permutation is the cycle (0 1 ... p−1), with all lower sections trivial.

Let i(1),i(2),... be the concatenation

    1 ; 1,2 ; 1,2,3 ; 1,2,3,4 ; ... .

Thus every positive integer occurs infinitely often, and for every finite I⊂N some i(N) lies outside I. For each i≥1 define d_i by its portrait: its local permutation is the cycle a at exactly the vertices

    v_n = 0^(n−1) 1,   n≥1 with i(n)=i,

and is the identity at every other vertex. Here v_n has length n, and a portrait at v_n changes the coordinate numbered n, with coordinates numbered from zero.

Set C=<a>, D={d_i:i≥1}, and H=<C,D>.

All v_n are pairwise incomparable: if n<m, the nth symbol of v_m is zero while the last symbol of v_n is one. Therefore the prescribed local permutations act in mutually disjoint subtrees, so they define automorphisms unambiguously. They also show that all d_i commute, each d_i has order p, and the d_i are independent. In particular <D> is a direct sum of copies of C_p.

## Original longitudinal condition

Every d_i fixes the directing ray 0∞. If a finite or infinite tuple first differs from that ray at coordinate j, then:

- if its differing symbol is 1, d_i changes only coordinate j+1, by a when i(j+1)=i and by the identity otherwise;
- if its differing symbol is different from 1, d_i changes no coordinate.

No deeper portrait can act on this tuple because all later v_n lie along the zero ray until their final symbol. This is exactly a longitudinal mutation in the original definition. Since i occurs infinitely often, d_i has infinite level support. No d_i is a finitary substitute.

At level zero, the accompanying group of C is C_p, acting transitively on A. At each level n≥1, the accompanying group of D contains a, supplied by d_{i(n)} at v_n, and all accompanying permutations lie in <a>. It is therefore C_p and is transitive. Hence H is an original AT group (indeed an AT_ω group for ω=(p,p,...)).

For completeness, its infinitude does not need a quoted AT theorem. It is transitive on every finite level. Induct on depth: the root cycle is transitive at depth one; for n≥1, d_{i(n)} fixes v_n and its section there is a, so the stabilizer of v_n is transitive on its p children. Transitivity at depth n conjugates this property to every vertex at depth n. Thus the action on depth n+1 is transitive. Its orbit sizes p^n are unbounded, proving H infinite.

## Finite-subgroup certificate

Fix a finite I⊂N and let H_I=<a,d_i:i∈I>. Choose N≥1 with i(N)∉I. Write t_i=d_i|_{0^N} for the section of d_i at the zero-ray vertex of depth N. All later occurrences of i survive in this tail, so the t_i, i∈I, are independent commuting order-p automorphisms. Set B_N=<t_i:i∈I>≅C_p^{|I|}.

Every section at depth N of each selected generator lies in B_N:

- all depth-N sections of a are identity;
- d_i|_{0^N}=t_i;
- at the only possible other support vertex of length N, namely v_N, the section is identity because i(N)∉I;
- a portrait at v_n for n<N is a root permutation of its subtree with no lower sections, so it contributes no section at depth N;
- all portraits with n>N lie inside the subtree at 0^N.

The section identity (gh)|_v=g|_{h(v)} h|_v (or its equivalent with the opposite action convention) implies that every depth-N section of every element of H_I lies in B_N. Sections of inverses remain in B_N as well. The faithful decomposition of a tree automorphism into its action through level N and its depth-N sections now gives an injection

    H_I → B_N^{p^N} ⋊ Wr_N(C_p).

The right side is a finite p-group. In particular,

    |H_I| ≤ p^[ |I| p^N + (p^N−1)/(p−1) ].

Every finite subset of H is expressed using finitely many d_i, so belongs to one H_I. Consequently H is locally finite and is a p-group. It is countable because it has countably many generators.

The **common zero for a finite set of generators** is essential: it prevents a rooted cycle from occurring beside the infinite directed tail at the selected section depth. Replacing this argument by finite-support longitudinal generators would fail the original definition and is not being done here.

## A locally finite derived-subgroup overgroup

Let K=H wr C_p=H^p⋊<t>, with t cyclically permuting the p coordinates. It is countable and locally finite p: any finite subset uses finitely many coordinates from H, hence lies in F^p⋊C_p for a finite p-subgroup F≤H.

The diagonal map Δ:H→H^p is injective. Its image lies in K'. To check this without an abelianization formula, use the commutator convention [x,y]=x^−1 y^−1 x y and orient t so that

    t^−1(x_0,...,x_{p−1})t=(x_1,...,x_{p−1},x_0).

For any h of order p set w(h)=(1,h,h²,...,h^(p−1)). Then

    [w(h),t]=(h,h,...,h)=Δ(h),

because all consecutive exponent differences are 1 modulo p, including the last difference 0−(p−1). All generators a,d_i have order p, so Δ(H), generated by their diagonal images, is a subgroup of K'.

Thus the output includes not only the explicit AT target H but a countable locally finite p-group K with an explicit embedding H→K'. Its characteristic-p group-algebra augmentation ideal is locally nilpotent: every finite subset is contained in the augmentation ideal of F_p[F] for a finite p-subgroup F≤K, and that finite-group augmentation ideal is nilpotent. A separate realization argument must still connect this ideal to the canonical source Golod group required in 21.131.

## Falsifiable checks and boundary cases

- p=2 is allowed; the symbol 1 exists for every prime p≥2.
- An empty finite I causes no problem: H_I=<a> is finite; the proof gives a valid loose bound.
- A level with i(N) outside I exists even if I is not an initial interval.
- Infinite support of every selected d_i uses infinite recurrence of **each** i; mere surjectivity of i(n) would not suffice.
- All finite-level computations are supplementary. The proof of local finiteness uses exact sections on the infinite tree and does not infer stabilization from finite samples.
- This target does not establish that a given Golod group has such a section, nor that every prime must work for a particular Golod source. The problem's exact existential quantifiers must be checked separately.

## Independent verification

The independent audit is `adversary/adversarial_audit.md`, with its own evaluator and results in that directory. It found no algebraic gap and passed 11,778 exact portrait and section comparisons for p=2,3,5. It explicitly falsified the tempting bad variant where the cutoff level is not a common zero. The supplementary `verify_finite_levels.py` in this directory also passed; its binary singleton-generator images stabilize at order 32 for i=1 and order 8 for i=2, while its ternary i=2 image stabilizes at order 81. These samples are consistent with, and logically separate from, the infinite-tree proof.


