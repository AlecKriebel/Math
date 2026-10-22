# Tree-language audit for Kourovka 21.143

Scope: the standard finite dyadic piecewise-linear Thompson group F with finite generating set {x0, x1}. This note independently audits constructive tree-pair, caret-type, and forest routes. It does **not** prove that F is nonautomatic. The elementary obstructions below concern specified encodings; no novelty or priority claim is made for them.

## Research log and claim boundary

- **2026-10-17 21:06:50 UTC — opening checkpoint.** Target hypothesis: a suitable finite-alphabet encoding of reduced diagrams might yield a regular domain and synchronous generator multipliers, and possibly a classical automatic structure. Success requires the whole group, an exact evaluation map, a regular representative language, all equality/multiplier relations, and the appropriate classical fellow-traveller property. Initial estimate toward resolving 21.143: **1%**; toward this narrower audit: **10%**. Early independence: no other route verdicts were read.
- **2026-10-17 21:08:56 UTC — verified obstruction checkpoint.** Established theorems 1–4 below, with an independent adversarial check of the comb and tree-automaton arguments. Finite corroboration: all 203,456 equal-caret-count tree pairs through seven carets; opposite comb formulas through 100 carets. Estimate toward resolving 21.143 remains **1%**; toward this audit: **90%**. A complete affirmative structure and a general negative obstruction both remain absent.
- **2026-10-17 21:11:42 UTC — final audit checkpoint.** Completed the five encoding-specific proofs, verified the published result boundaries, and added binary/zipped partial repairs and the exact frontier first-return obstruction. Independent adversarial review passed the frontier recurrence and bounded-length-difference lemma; the implicit-zero-stream limitation was made explicit. All 203,456 tree-pair checks and 5,461 negative-exponent checks passed. Estimate toward resolving 21.143: **1%**; completion of the assigned audit: **100%**. No automaticity or nonautomaticity theorem for F is claimed.

The exact boundary matters: disproving regularity of one injective encoding, proving that no regular geodesic language exists for the standard generators, or obtaining a counter-automatic diagram calculus does not settle classical automaticity.

## What the different conclusions would mean

| Structure | Representatives and required tests | Consequence for this problem |
| --- | --- | --- |
| Classical automatic group | Regular words over a finite group generating alphabet, with their ordinary product evaluation; synchronous equality/right-generator multipliers, equivalently a suitable fellow-travelling regular combing | Would answer 21.143 affirmatively |
| Graph/Cayley automatic Cayley graph | Regular words over an arbitrary finite symbol alphabet, a specified bijection to group elements, and synchronous finite-state edge relations | Does not by itself supply classical generator-word paths |
| k-counter graph automatic Cayley graph | Domain and edge relations accepted by the specified counter-machine class | Finite-state regularity is still missing |
| Tree-automatic Cayley graph presentation | Finite ranked-tree representatives and finite-tree-automaton domain and edge relations | Changing the input objects is substantive; a theorem about strings of caret types is not such a theorem |
| Automatic presentation of (F, multiplication) | The entire ternary group-multiplication relation must be automatic | Stronger requirement than automaticity of fixed-generator Cayley edges; do not substitute it for 21.143 |

The graph-automatic convention above is the one in Elder–Taback, Definition 2.3. Their normal-form bijection is arbitrary; alphabet symbols need not evaluate as fixed group generators. Comparability between symbol length and group word length alone does not identify paths obtained by reading prefixes. [Elder–Taback, primary paper](https://arxiv.org/pdf/1501.04313).

## Published constructive results and their exact gaps

**Caret-type encoding.** Taback–Younes use infix strings over six caret types in each tree, paired by caret number. Their Theorem 4.1 supplies a deterministic nonblind 3-counter graph automatic structure. The diagram domain uses two counters; Lemma 4.5 proves that this specific domain is not context-free. Its reduction condition is regular. The x0 construction uses two counters, while the presented x1 construction uses three. Thus neither local reduction checks nor boundedly many caret-label changes remove the global tree-validity tests. The paper discusses a possible two-counter refinement, but the stated theorem is the three-counter result. [Taback–Younes, §§4–5](https://arxiv.org/pdf/1501.04315).

**Infinite-normal-form encoding.** Elder–Taback's regular domain L_infinity over {a, b, #} gives a deterministic nonblind 1-counter graph automatic structure (Theorem 3.6). The x0 inverse multiplier is regular; the x1 inverse multiplier is not (Lemma 3.7). Its witness is the convolution of b^n and b^n #^(n+1) b: pumping the common initial b-run changes the exponent without changing the required separator count. This is an explicit example where a regular domain succeeds while a multiplier fails. Both papers expressly leave alternative encodings open. [Elder–Taback, Propositions 3.4–3.5 and Lemma 3.7](https://arxiv.org/pdf/1501.04313).

**Forests.** Belk–Brown give unique reduced pointed forest diagrams. In their left-action convention, x0 moves the top pointer by one tree; x1 joins the current and next top trees by a caret, with a possible cancellation. These are useful local geometric actions, but their existence is not a regular-language or synchronous-multiplier theorem for a linear encoding of every forest. [Belk–Brown, Propositions 3.2.4 and 3.3.1](https://arxiv.org/pdf/math/0305412).

**Dated status check.** A later primary paper states in its conclusion that F was not known to be automatic or Cayley automatic, despite the one-counter result. This is a dated literature statement, not a proof of the present status; the main problem's October 2026 official listing should supply the current problem-status evidence. [Berdinsky–Elder–Taback, IJAC 2022, §7 item (4)](https://arxiv.org/pdf/2008.02381).

None of the cited counter constructions is a theorem that F has a tree-automatic Cayley graph presentation. This audit does not assert either existence or nonexistence of such a presentation with a different encoding.

One stronger signature can be excluded, by a **deduction from existing theorems**: a tree-automatic presentation of the full group multiplication would imply a decidable first-order group theory. Tree-automatic structures have decidable first-order theories, while Bardakov–Tolstykh prove the elementary theory of F hereditarily undecidable. Hence the full multiplication structure (F, multiplication) is not tree-automatic. Generator-edge relations do not make arbitrary multiplication first-order definable by a bounded formula, so this inference does not exclude a tree-automatic Cayley graph and does not answer 21.143. [Tree-automatic decidability, Theorem 4](https://www.comp.nus.edu.sg/~sanjay/paps/autotree.pdf), [Bardakov–Tolstykh](https://arxiv.org/abs/math/0701748).

## Elementary obstructions with complete proofs

Let a finite full ordered binary tree be either a leaf, written 0, or a binary internal node N(T1,T2). Define its preorder code by

    p(leaf) = 0,
    p(N(T1,T2)) = 1 p(T1) p(T2).

A tree with n internal nodes (carets) has n+1 leaves, so its code contains n symbols 1 and n+1 symbols 0. A code also obeys the usual proper-prefix slot condition, but the balance condition alone will suffice for our negative tests.

Define L_n = N(L_(n-1), leaf), R_n = N(leaf, R_(n-1)), starting with L_0 = R_0 = leaf. Inductively,

    p(L_n) = 1^n 0^(n+1),       p(R_n) = (10)^n 0.

For n >= 2, (L_n,R_n) is a reduced tree pair: its sole exposed caret is at the first two leaves in L_n and at the last two leaves in R_n. These positions differ. For n=1 they coincide and the pair reduces, which is why all filters below exclude that case. Each such pair has the same number of leaves in its two trees and is an actual representative of an element of F.

### Theorem 1: separated preorder pairs are not regular

Let P_sep be the language of p(T)#p(S) for all reduced tree pairs with equal leaf counts, with any fixed convention for the identity. Then P_sep is not regular.

Proof. Intersect with the regular language

    R_sep = 1^(>=2) 0^(>=3) # (10)^(>=2) 0.

The first tree must be L_n and the second R_m: balance forces each exponent in the first code to be n and n+1 respectively, and the second pattern is a right comb. Equal leaf counts force m=n. The resulting pair is reduced for every n>=2. Therefore

    P_sep ∩ R_sep = { 1^n 0^(n+1) # (10)^n 0 : n>=2 }.

The prefixes 1^n, n>=2, are pairwise distinguishable: appending 0^(n+1)#(10)^n0 gives an accepted word precisely for the prefix 1^n, since any other initial 1-count violates tree balance. Infinitely many right-congruence classes contradict regularity. QED.

This argument is stronger than observing that arbitrary trees form a Dyck-like language: it exhibits the obstruction *inside reduced, equal-size pairs*, so cancellation restrictions cannot invalidate the witness family.

### Theorem 2: synchronized preorder pairs are not regular

Let P_conv be the language of synchronous convolutions p(T) ⊗ p(S) for all reduced equal-leaf-count pairs. The strings have equal length, so no padding symbol is needed. Then P_conv is not regular.

Write the column letters as

    A=(1,1),  B=(1,0),  C=(0,1),  D=(0,0).

Intersect P_conv with the regular language (AB)^+ (CD)^+ D. A word (AB)^k(CD)^ell D has top and bottom projections

    1^(2k) 0^(2ell+1),          (10)^(k+ell) 0.

Validity of the top tree forces k=ell. Conversely, when k=ell>=1 these are exactly L_(2k) and R_(2k), a reduced pair. Hence

    P_conv ∩ (AB)^+(CD)^+D = { (AB)^k(CD)^kD : k>=1 }.

The homomorphism A->a, B->empty, C->b, D->empty maps this language onto {a^k b^k:k>=1}. The latter is not regular, whereas homomorphic images of regular languages are regular. QED.

The same proof works if reducedness is dropped: synchronizing the rows fixes their total lengths, but not their individual tree balances.

### Theorem 3: finite-state decoration cannot repair these domains

Let P be either P_sep or P_conv. There is no regular language D of annotated or otherwise recoded words with a finite-state transduction whose exact image is P.

Proof. Images of regular languages under finite-state transductions are regular. Theorems 1 and 2 contradict this. Letterwise erasure of finitely many annotation tracks is a special case. QED.

The exact-image condition is essential. The theorem does not rule out a regular encoding from which diagrams can only be recovered by a non-finite-state procedure. It also does not rule out regular redundant generator-word representatives whose evaluation is a different map.

### Theorem 4: exact regular multipliers imply a regular domain

Let L be any language representing all elements of a group, and let x be a fixed group element. Define the *exact* multiplier language

    M_x = {u ⊗ v : u,v in L and eval(v)=eval(u)x}.

If M_x is regular, then L is regular.

Proof. For each u in L there exists a representative v in L of eval(u)x. Thus projection to the first row, followed by erasure of padding, maps M_x onto L. This is a regularity-preserving homomorphism. QED.

Consequently, every exact generator multiplier fails regularity for each of the two naive preorder domains. Showing a regular relation of possible local edits on arbitrary strings is insufficient: intersecting that relation with a nonregular domain still has to validate the input. This explains how a small geometric operation and a non-finite-state multiplier can coexist.

### Theorem 5: two separate subtrees under one root are not a regular tree domain

Consider the ranked alphabet with leaf symbol e of rank 0, caret symbol N of rank 2, and pair symbol P of rank 2. Let Q consist of the terms P(T,S) for reduced full-binary tree pairs with equal leaf counts. Then no finite bottom-up tree automaton recognizes Q.

Proof. If necessary determinize such an automaton. Among infinitely many left combs L_n, n>=2, two distinct indices n,m give the same state at the tree root. Since P(L_n,R_n) is a valid reduced pair, replacing L_n by L_m leaves the automaton's root calculation unchanged and is accepted. But P(L_m,R_n) has unequal leaf counts, so it is not in Q. Contradiction. QED.

Thus even the first step of a naive tree-automatic presentation fails in this separated-tree encoding. This theorem makes no assertion about encodings in which the two shapes share a more intricate common tree structure.

## New encoding mechanisms examined

| Family/mechanism | Evidence and present status | Exact gap or reopening condition |
| --- | --- | --- |
| Preorder pairs plus finitely many labels, markers, pointer flags, or bounded-state certificates | **Blocked for exact finite-state decoding** by Theorems 1–3 | Reopen only with an encoding whose decoding is not a finite-state transduction, or with representatives whose underlying diagram codes do not exhaust these exact domains |
| Infix caret pairs with locally checked cancellation | Existing counter construction; domain not even context-free | A new mechanism must remove whole-tree validity counters, not merely optimize local caret changes |
| Pointed forests serialized by component preorder | Pointer shifts are attractive; arbitrary component depth retains balance obligations | Need a precise complete regular domain and exact join/cancellation multipliers. Merely stating that joins are local transfers the central problem to unproved parsing |
| Two diagram trees as two branches of a ranked tree | **Blocked in this encoding** by Theorem 5 | A common leaf-rank/alignment skeleton would be a different encoding and must prove its own tree-regular domain and all generator relations |
| Binary arithmetic recoding of exponent/index data | Basic unary witness is not invariant under recoding; regular arithmetic slice proved below | Must handle arbitrary multi-block normal forms, canonical deletion, and index shifts, then separately produce classical generator-word paths |

### A surviving but limited arithmetic idea

The infinite-normal-form multiplier witness compares an exponent n with a later index n+1 in unary. That comparison can be made finite-state by changing the coordinates of this slice.

Let g_n=x0^(-n), h_n=x0^(-n)x1^(-1), n>=1. These two families are disjoint, since their images in the abelianization Z^2 have different x1 coordinates. Define partial codes

    c(g_n) = U bin_LSB(n),       c(h_n) = V bin_LSB(n+1),

where bin_LSB is canonical binary with the least significant digit first. Both tagged code sets are regular. The restricted right-x1-inverse relation c(g_n) ⊗ c(h_n) is regular: after reading the tags, maintain a carry initially 1; each digit pair checks b ≡ a+carry modulo 2, and updates carry=floor((a+carry)/2). Padding after a track ends is treated as zero, and finite-state canonical-format tests exclude trailing zeros and require that the carry is zero at the end.

This is a concrete mechanism that defeats the particular unary counting witness. It is a partial encoding of a very small vertex/edge family, not a complete encoding of F. It shows why an encoding-specific pumping argument cannot be promoted to nonautomaticity. The unresolved task is to align unboundedly many index/exponent blocks, including all canonical reductions, so that every exact multiplier is regular; a successor automaton alone does not do that. Even a successful graph-automatic result would still need an additional argument to answer classical automaticity.

### Zipping the unary witness: what is repaired and what remains

A further local repair uses zipped rather than binary arithmetic. On the same two families, take

    z(g_n) = U (b#)^n,          z(h_n) = V (b#)^n #b.

This partial code has a regular domain and a regular restricted x1-inverse multiplier, since only tags and a fixed suffix change. Zipping the target alone, while leaving the source b^n, would fail: their code-length difference grows with n.

The reason is a useful general test. If a synchronous regular relation is a bijection between unique representative words, then there is a uniform bound on the absolute input/output length difference. To prove the upper bound, suppose an accepted convolution has more than N trailing symbols with the first row already blank, where N is the number of automaton states. Repeated states give a nonempty loop entirely in that tail; pumping it leaves the first representative unchanged while changing the second, contradicting uniqueness of the function. Apply the same argument with the two rows swapped for the lower bound. This test applies to unique-code multipliers, not arbitrary many-representative relations.

The forest/frontier proposal exposes the remaining cost. Consider just descending negative normal forms g=x_M^(-s_M)...x_0^(-s_0), with exponents s_i>=0 and only finitely many nonzero s_i. Zero blocks beyond the largest stored index are implicit. The relation

    x_i^(-1) x_j^(-1) = x_(j+1)^(-1) x_i^(-1),  i<j,

shows that, while an appended x1^(-1) crosses the blocks of smaller index, its current index is 1 plus the sum of the negative exponents already crossed. Thus define

    H_i = 1 + sum_(j<i) s_j - i,
    H_(i+1) = H_i + s_i - 1.

The insertion/merge index is the first t for which H_t=0. Before it, H_i>0; the first nonpositive height is exactly zero because the downward steps have size at most one. Eventually a return occurs because all sufficiently large s_i vanish. This derivation uses only the negative cone, so positive/negative cancellation is not being silently assumed away in a claim about the whole group.

Encode a processed block in this abstract, implicitly zero-extended stream as b^(s_i)#. For g_n the return stream b^n#^(n+1) extends beyond its finite source code b^n; it is not an already stored input substring. Starting with one available slot, each b adds one slot and each # consumes one. The exact first-return prefix language W is the set of words whose height stays positive before the end and becomes zero at the end. It satisfies

    W ∩ b*#* = { b^n #^(n+1) : n>=0 },

and is therefore nonregular. For n=0 the word is #; excluding the identity or imposing n>=1 does not change the obstruction. A finite-state machine on this *unchanged* stream cannot simply identify the return point. The zipped comb (b#)^n# is a regular slice of W, while b^n#^(n+1) is another slice; their equal counts do not mean the underlying degree sequences agree. Arbitrarily sorting or zipping all b/# tokens erases which exponent belonged to which index. Any complete recoding must preserve that information and prove exact domain/multiplier regularity anew. Describing insertion as a local first-return operation alone transfers the central difficulty to this unbounded return test.

This does not prove that every frontier-based or compressed encoding fails: the binary slice and zipped slice explicitly show that substantial recoding can remove a particular return-count witness. The blocked route is finite-state first-return detection on the original slot stream, or arbitrary zipping without a recoverable encoding of the degree sequence.

## Validation and strongest verified result

The accompanying `tree_language_verify.py` independently constructs all full binary trees through seven carets and tests reducedness via shared exposed-caret leaf positions. It checks the exact serial and convolution filter descriptions, including the first admissible case n=2, and checks opposite-comb formulas through n=100. It reported 203,456 examined pairs, serial matches n=2,3,4,5,6,7, and convolution matches n=2,4,6; every assertion passed. These bounded computations corroborate the formulas but are not substitutes for the proofs.

The script also checks that a direct letter-by-letter index-bubbling simulation agrees with the frontier return index on all 5,461 exponent vectors of length at most six with entries 0,1,2,3. This includes empty input, leading/trailing zeros, immediate merging, delayed insertion, and long pending-slot cases; it validates only the negative-cone calculation stated above.

An independent agent adversarially checked the projected strings, k=ell balance implication, reducedness at the boundary k=1, erasing homomorphism, and determinization step in Theorem 5. A second pass checked the negative-cone recurrence, first-return boundary cases, and synchronous-bijection pumping argument. No gap was found in those checks. Theorem 3's exact-image restriction, Theorem 4's total representation assumption, and the frontier stream's implicit extension have been made explicit to avoid overreach.

Strongest verified conclusion: the two explicit naive preorder domains, any regular encoding that decodes onto them by finite-state transduction, and the naive separated ranked-tree domain cannot supply the needed automatic presentation. Published counter results and a binary successor slice do not close the remaining gap. **The automaticity of F is not resolved by this audit.**

No outside individual was contacted; no outreach was prepared. No Git operation or shared queue/status edit was performed by this audit agent.
