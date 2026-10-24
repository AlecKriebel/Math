# Dense torsion, coset identities, and Lie locality — 21.136

Independent research begun 2026-10-24. Current outcome: **partial structural results and explicit obstructions; no complete solution**. Initial discovery estimate: **8%**. No assertion of originality is made for these elementary controls or restricted deductions.

The original target is every profinite group G with fewer than continuum ambient G-conjugacy classes of infinite-order elements. Finite generation, metrizability, and countability cannot be inserted into that target. This approach principally investigates the pro-p case. The parent separately addresses countable-base reductions and general fusion.

## 1. The precise Lie bridge that requires repair

Wilson, *Profinite groups with few conjugacy classes of elements of infinite order*, Archiv der Mathematik 120 (2023), 557–563, DOI [10.1007/s00013-023-01851-4](https://doi.org/10.1007/s00013-023-01851-4), Theorem C, proves finiteness for a **finitely generated** pro-p group under both of the following assumptions:

1. Torsion elements are dense.
2. Some open coset has finite exponent.

His proof obtains a polynomial identity for a Zassenhaus Lie algebra from the coset identity and obtains ad-nilpotence from torsion representatives in homogeneous cosets. Zelmanov's theorem and the p-adic analytic conclusion then use finite generation.

At least two distinct failures occur if finite generation is removed:

- Zassenhaus terms need not be open. Topological density alone need not supply any torsion representative in a homogeneous coset.
- Even an open filtration with finite homogeneous pieces and locally finite restricted Lie data can complete to a group with infinite-order elements. Passing from local graded information to the full compact group needs an additional theorem.

Neither failure is a technical inconvenience that can be silently ignored. The next sections give exact controls.

## 2. A countercontrol to dropping finite generation, for every prime

Fix any prime p. For n≥1 put

\[
V_n=\{(x_0,\ldots,x_{p-1})\in(\mathbb Z/p^n\mathbb Z)^p:
\textstyle\sum_i x_i=0\}.
\]

Let σ cyclically permute the p coordinates, let A=∏_{n≥1}V_n, and form

\[
G=A\rtimes\langle t\rangle,\qquad |t|=p,
\]

with t acting as σ on each factor. This is a countably based pro-p group: truncating the product after n gives finite p-group quotients with trivial kernel intersection.

For each j∈{1,…,p−1}, the automorphism σ^j is another p-cycle. Consequently

\[
(1+\sigma^j+\cdots+(\sigma^j)^{p-1})v=0
\quad(v\in V_n).
\]

The semidirect-product power formula therefore gives

\[
(a t^j)^p=1\qquad(a\in A,\quad j\ne0).
\]

Thus every nonidentity quotient coset At^j is an open coset of exponent p. The subgroup

\[
D=\left(\bigoplus_{n\ge1}V_n\right)\rtimes\langle t\rangle
\]

is dense and locally finite: each finite set of elements is supported on finitely many factors together with t, and lies in a finite semidirect product. In particular torsion is dense in G.

Nevertheless G is not torsion. In V_n the vector v_n=(1,−1,0,…,0) has order p^n, so a=(v_n)_n has infinite order. The p=2 case is exactly

\[
\left(\prod_{n\ge1}C_{2^n}\right)\rtimes C_2
\]

with the involution acting by inversion.

This proves the following obstruction, with no appeal to a computational search:

> Dense torsion plus a single finite-exponent open coset does not imply torsion or local finiteness for an arbitrary pro-p group, for any prime p.

This group is **not** a counterexample to 21.136. For a∈A, conjugation by A is trivial, and its G-conjugacy class is {a,σa,…,σ^{p−1}a}, of size at most p. There are continuum many infinite-order elements in A: choose v_n or 0 independently for an infinite subset of indices n. Every such infinite subset gives an element of unbounded coordinate orders, hence of infinite order. Quotienting a continuum-sized set by finite classes still gives continuum classes. G itself has cardinality continuum, so the number is exactly continuum.

The norm-zero finite-order action used here is a standard semidirect-product mechanism. For related p-adic analytic examples see Kionke–Otmen–Toti–Vannacci–Weigel, [arXiv:2507.19086v2](https://arxiv.org/abs/2507.19086v2), Examples 5.9 and 5.11. Their hypotheses and conclusions do not claim that the present infinite product satisfies the original few-classes condition.

## 3. Density need not lift to a Zassenhaus coset

Let B=∏_{n≥1} C_{p^n}, written additively, and b=(1 mod p^n)_n. Finite-support torsion elements are dense in B. For an abelian pro-p group the second Zassenhaus term is pB, which is closed here. But B/pB≅∏_{n≥1}C_p is infinite, so pB is not open.

Every element of b+pB has a unit in its n-th coordinate. Its n-th coordinate therefore has order p^n. Thus **b+pB contains no torsion element**. Density of torsion has not supplied a torsion representative even in this first nontrivial homogeneous coset.

This control does not have a bounded-exponent open coset, and is used only to isolate the false density-to-homogeneous-lift inference.

## 4. An open filtered replacement still has a completion gap

The same abelian B admits an open p-filtration illustrating why repairing openness alone is insufficient. Give the standard generator e_n of C_{p^n} weight p^n, and p^j e_n weight p^{n+j} for 0≤j<n. For integer m≥1 let F_m consist of those elements whose n-th coordinate is divisible by p^{r(n,m)}, where

\[
r(n,m)=\min\bigl(n,\max(0,\lceil\log_p m\rceil-n)\bigr).
\]

Equivalently, the allowed nonzero coordinate monomials have weight at least m. The filtration is descending, separated, and open, and defines the product topology. Only finitely many coordinates are restricted for fixed m. It satisfies pF_m⊆F_{pm}; all commutator conditions hold because B is abelian.

The associated graded restricted Lie algebra is abelian. Its nonzero homogeneous pieces occur at degrees p^k; that piece has one basis vector for each integer n with n≤k≤2n−1, hence is finite-dimensional. The restricted p-map carries the vector for p^j e_n to that for p^{j+1}e_n, and kills it after at most n steps. Every element of the graded direct sum has finite support in these strings, and every finitely generated restricted Lie subalgebra is finite-dimensional. Thus the graded restricted Lie algebra is locally finite and every one of its elements is p-nilpotent.

The compact completion B nevertheless contains the infinite-order element b. No assertion that locally finite graded data imply torsion of the completion can be used without additional hypotheses.

## 5. The genuinely stronger coset condition still available

For a pro-p group satisfying the original class bound, Wilson Corollary 2.3 provides the property

**P:** Every nonempty open coset contains an open subcoset of finite exponent.

This is stronger than the two assumptions of Theorem C. It is equivalent to the interior of Tor(G) being dense:

- P directly implies that this interior meets every nonempty open set.
- Conversely, take any open set meeting int(Tor(G)), and a compact open coset K contained in that intersection. The closed subsets {x∈K:x^{p^n}=1}, n≥0, cover K. By the Baire theorem, one has nonempty relative interior in K, and it contains a bounded-exponent open coset.

This reasoning works without a countable base, since a compact Hausdorff space is a Baire space; only the countable sequence of possible p-powers is used.

Property P passes to open subgroups and continuous quotient groups, directly from its definition. It has not been shown to pass to arbitrary closed subgroups. The all-prime control in Section 2 fails P: every open coset contained in A permits free variation in all sufficiently far factors V_n and consequently contains elements of unbounded order.

A replacement theorem

> Every pro-p group satisfying P is torsion

would be strong enough to settle the pro-p stage, but is **not proved here**. Replacing the missing Lie argument by this assertion merely transfers the central difficulty and is marked blocked.

## 6. Restricted positive conclusions

If Tor(G) happens to be a subgroup, dense torsion together with one open torsion coset already implies G torsion: taking differences in that coset gives an open subgroup contained in Tor(G), so Tor(G) is open and closed, and density gives equality. In particular this applies to nilpotent groups, in which torsion elements form a subgroup. Passing to an open nilpotent subgroup proves the analogous torsion conclusion for virtually nilpotent groups with P. No claim that an arbitrary pro-p group is locally nilpotent is made.

Separately, there is a useful fusion obstruction under the original class bound. Suppose A◁G is closed abelian, G/A is torsion, and C≅Z_p is contained in A. If g normalizes C, some positive power g^m belongs to A and centralizes C. Hence the induced power automorphism of C has finite order. The torsion subgroup of Aut(C)≅Z_p^× is finite (order p−1 for odd p, order 2 for p=2). Each ambient G-conjugacy class therefore meets the continuum-sized set of topological generators of C in only finitely many points. This contradicts the strict-continuum bound.

Wilson Lemma 4.2 excludes infinitely many primes under the original global hypothesis. An infinite-order element of A then has an infinite pro-p component for at least one of those finitely many primes. The preceding argument forces A torsion; since G/A is torsion, G is torsion. Induction on finite derived length settles soluble profinite groups under the original class bound. The induction uses quotient inheritance, **not** arbitrary normal-subgroup inheritance. It does not settle prosoluble groups of unbounded derived length or arbitrary groups.

The parent construction approach independently derived this fusion lemma and is responsible for its broader audit and synthesis. These restricted conclusions are not claimed to be original.

## 7. A stronger metabelian coset theorem

An independent child of the Lie adversary found a new proof mechanism while examining the stronger coset condition. Define the weaker property

**P0:** Every open subgroup contains some open coset of finite exponent.

The self-contained proof in [metabelian_locality.md](lie_adversary/strong_subclass/metabelian_locality.md), checked in [metabelian_adversarial_audit.md](lie_adversary/metabelian_adversarial_audit.md), establishes:

> A virtually metabelian pro-p group with P0 has finite exponent and is locally finite.

The essential mechanism is a finite sequence of drops in a conjugation action's exponent. Keep A=closed G' fixed and put V=A⊗_(Z_p)Q_p. The abelian quotient G/A inherits P0 and has exponent q=p^e. Its action on V is commuting and has exponent dividing q. A bounded-exponent open coset xU gives the norm identity N_q(T_(xu))=0 on V for every u∈U: the original coset identity annihilates A∩U, which spans V, and its exponent can be enlarged to a multiple of q.

For any fixed u, the two commuting finite-order operators T_x,T_u generate a finite abelian group, even if V is infinite-dimensional. Its finitely many character idempotents decompose V after adjoining q-th roots of unity. On a nonzero character space write the eigenvalues as ξ,η. Norm vanishing for every xu^i means ξη^i≠1 for every i. If η had order q this would be impossible. Hence U's action has exponent at most q/p. Repeat inside U, always keeping the original A and V, until an open subgroup acts trivially. A final bounded-exponent coset then gives a nonzero scalar times Id_V equal to zero, so V=0.

Thus A is torsion. Compact abelian torsion is bounded-exponent by Baire; G/A already has bounded exponent, so G does also. Local finiteness follows elementarily by taking a finitely generated abstract subgroup, using its finite image in G/A, and applying Schreier to its torsion abelian intersection with A. The proof also passes to finite extensions.

This argument genuinely uses full P0, rather than the disproved weak assumptions of Section 2. It needs no finite-dimensional global representation decomposition. It does not extend by the same inference to arbitrary noncommuting bounded-exponent actions: in the faithful two-dimensional characteristic-zero representation of Q8, every element of i⟨j⟩ has no eigenvalue 1, while ⟨j⟩ still acts with exponent 4. Thus the attempted universal exponent-drop lemma fails already in a finite example.

This is a restricted theorem with a checkable proof and a completed child/parent AI audit, awaiting the root's additional fresh review. No originality claim or publication eligibility follows from it. In particular, arbitrary pro-p groups and soluble groups of derived length at least three remain outside the argument.

## 8. Current exact gap and outcome

The weak dense-torsion/one-coset extension is disproved by Section 2. Pure Lie locality and completion are inadequate by Sections 3–4. The stronger property P is preserved by the operations used above but has not been inherited by the finitely generated closed subgroups needed for Wilson's finite-generation proof. No rigorous substitute has been found for an arbitrary pro-p group, nor for the arbitrary ambient fusion in non-soluble normal-series factors.

No complete affirmative proof or actual few-classes counterexample is established. The original problem remains **unsolved** in this approach; no solution or publication gate is passed.
