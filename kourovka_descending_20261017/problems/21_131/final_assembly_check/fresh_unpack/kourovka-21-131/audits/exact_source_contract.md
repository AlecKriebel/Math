# Kourovka Notebook 21.131: exact target and source scope

Source audit checkpoint: 2026-10-24 18:35:20 UTC. Source/definition audit **95%** complete; best guess toward a complete new mathematical resolution **5%**. The remaining source gap is original 1986 PDF byte/raster acquisition. No substantive construction, impossibility proof, or computational search has been undertaken in this preliminary screen.

## Authoritative problem

A. V. Timofeenko, *The Kourovka Notebook*, 21st edition, official 20 October 2026 revision, printed p.199, Problem **21.131**. [Official PDF](https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/10/21tkt-3.pdf).

The requested object is a surjective homomorphism from **a subgroup of a Golod group**, in the sense of 9.76, to **an infinite AT-group**, in the exact sense of A. V. Rozhkov, *Math. Notes* 40(5) (1986), 827–836. The problem refers to 13.55.

Equivalently, exhibit a characteristic-p field k, r≥2, a free nonunital associative algebra F=k⟨x₁,…,xᵣ⟩₊, an ideal I for which B=F/I is nil and nonnilpotent, a subgroup

\[
S\le G=\langle1+\bar x_1,\ldots,1+\bar x_r\rangle\le1+B,
\]

an infinite group H with an original AT realization, and an epimorphism S→H. An explicit kernel description S/N≅H is an equivalent acceptable formulation.

This is **existential**. It does not demand the construction for every prime, every Golod algebra, or every AT-group. The subgroup need not be finitely generated, finite index, or the entire G. Surjectivity and actual infinitude of H are essential.

## Golod means the definition in 9.76

The definition on printed p.38 allows **any field of characteristic p>0**. It requires a finitely generated **nil, nonnilpotent associative algebra** with the displayed canonical group generators. It does not expressly require I homogeneous, k finite, residual finiteness, or a specified Golod–Shafarevich inequality. Familiar homogeneous residually finite examples form an available subclass, not the entire printed definition.

Every element 1+b has p-power order because b is nil and
\[
(1+b)^{p^e}=1+b^{p^e}=1
\]
for sufficiently large e. Thus S and H in any successful construction are torsion p-groups. This follows from the Golod hypothesis; it is not a definition of general AT-groups.

## Original AT definition

Primary: A. V. Rozhkov, *Theory of Aleshin type groups*, Russian *Mat. Zametki* 40(5) (1986), 572–589; English *Math. Notes* 40(5), 827–836; DOI [10.1007/BF01159699](https://doi.org/10.1007/BF01159699), [MathNet mzm5213](https://www.mathnet.ru/eng/mzm5213). Definition: Russian printed pp.573–575; prime-cyclic specialization: p.580.

Take the prefix tree over A=(A₀,A₁,…), with arbitrary |Aₙ|≥2. Root mutations act only on coordinate0. Each longitudinal mutation d fixes its directing ray γ(d), has **infinite support in coordinate levels**, and changes only the coordinate immediately after the first divergence from γ(d). At level n≥1 its accompanying permutation is πₙ(d,a)∈Sym(Aₙ), indexed by the preceding off-ray symbol a∈Aₙ₋₁. The on-ray value is identity.

Choose **C a subgroup** of root mutations and **D a subset** of longitudinal mutations. Then H=⟨C,D⟩ is AT when
\[
\Pi_0=\langle\pi_0(c):c\in C\rangle,
\qquad
\Pi_n=\langle\pi_n(d,a):d\in D,\ a\in A_{n-1}\rangle\quad(n\ge1)
\]
act transitively on their respective Aₙ.

Every designated d∈D must itself have infinitely many changed coordinate levels. Identity is excluded from D; C contains identity. D need not be a subgroup, and directing rays need not coincide. Neither finite branching, periodicity, finite generation, a fixed prime, cyclicity, nor regularity is part of this general definition. Original ATω, defined separately, restricts level portraits to prime cyclic groups; even its primes may vary.

[Independent exact definition audit](independent_definition/definition_audit.md) preserves original coordinate formulas, scope, and the source limitation. Original primary indexed text was successfully inspected, but only a clearly labeled **manually preserved relevant OCR excerpt** was saved; the original PDF bytes were not obtained. The actual 2022 publisher PDF was obtained independently.

**Do not substitute the later definition:** Rozhkov2022 Def2 omits the explicit infinite-support clause. It corroborates geometry/transitivity but cannot justify a construction relying on only finite-support longitudinal generators under the original1986 definition.

## Comparison with 13.55

Problem13.55, printed p.72, asks whether a Golod group itself can be isomorphic to an AT-group. Such an example would settle21.131 affirmatively. Failure to make the whole ambient group AT does not establish a negative answer to21.131, whose subgroup/image latitude is greater.

## Current source-screen status

21.131 and13.55 remain unstarred in the current official main file; neither number occurs in the official October20 updates-only file. A bounded current primary/literature audit found **no complete resolution of21.131**. This is a qualified eligibility finding, not a proof of global absence of prior work. The 2023/2024 Rozhkov–Barsukova discussion suggests a negative answer to13.55 but explicitly qualifies it as apparent and supplies no general subgroup-quotient obstruction.

No `solved_verified`, `already_solved`, `unsolved` after substantive effort, or `published` outcome is assigned by this preliminary source screen. No publication is authorized by these findings alone.
