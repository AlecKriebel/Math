# A countable resolvable Boolean group without expansive finite blocks

**Target:** KOU-21.107, record 2616.  
**Outcome:** a full negative answer in ZFC, presented as an authored proof candidate pending independent audit.  
**Mathematical approaches used:** one, an ultrafilter-defined Boolean-group topology. Source checking, finite tests and packaging are not additional approaches.

## 1. Scope and source reconciliation

The target concerns a countable **topological** group admitting a partition into countably infinitely many dense sets. Its proposed conclusion requires one sequence of pairwise-disjoint finite subsets whose intersections with each nonempty open set are eventually nonempty. The eventual threshold may depend on the open set. Neither first countability nor metrizability is assumed. The dense pieces need not be subgroups; the finite blocks need not cover the group. “Resolvable” here refers to dense partitions, not algebraic solvability. The example below is nevertheless abelian.

The primary source literally says “for every open subset”; as usual in this context, the intended quantification excludes the empty open set. The counterexample addresses that meaningful interpretation, rather than exploiting the omission.

The official arXiv version 48, dated 6 October 2026, was retrieved and inspected. Problem 21.107 occurs on printed/PDF page 193 with the countability restriction and without a solution annotation. Its predecessor 15.80 is discussed on page 97 (page 98 in version 47): the box-product counterexample recorded there is uncountable. It cannot decide the present target. The official solution-repository page contained no 21.107 entry when checked on 8 October 2026. These are bounded status observations, not a certification of novelty or of the absence of unindexed work. Public source metadata and retrieval pins are in `sources.json`.

## 2. Set-theoretic ingredient

Fix a free ultrafilter \(\mathcal U\) on \(\mathbb N=\{0,1,2,\ldots\}\). We use only these facts:

1. Every cofinite set belongs to \(\mathcal U\), and no finite set does.
2. Intersections of finitely many members belong to \(\mathcal U\).
3. For every \(C\subseteq\mathbb N\), exactly one of \(C\) and \(\mathbb N\setminus C\) belongs to \(\mathcal U\).

For completeness, such an ultrafilter exists in ZFC: apply Zorn's lemma to the proper filters extending the cofinite filter. A chain has its union as a proper-filter upper bound. A maximal proper filter decides every subset, since failure to add a subset means that an existing filter member is disjoint from it. It contains no finite set, because that finite set's cofinite complement already belongs to it. No selective, Ramsey, rapid, or other special ultrafilter is needed.

## 3. The group and topology

Let
\[
G=[\mathbb N]^{<\omega}
\]
be the finite subsets of \(\mathbb N\), with symmetric difference \(s\triangle t\) as addition. Its identity is the empty set. This is a countably infinite Boolean abelian group: the finite subsets of \(\{0,\ldots,r\}\) form a finite set, and their union over \(r\) is \(G\).

For each \(A\in\mathcal U\), put
\[
H_A=[A]^{<\omega}.
\]
Each \(H_A\) is a subgroup, and \(H_A\cap H_B=H_{A\cap B}\). Declare all cosets \(s\triangle H_A\) to be a base for the topology. They cover \(G\); whenever two intersect at \(x\), their intersection is \(x\triangle H_{A\cap B}\). Thus this is a topology.

It is a group topology. Given a basic neighborhood \((s\triangle t)\triangle H_A\) of a sum, the sum of \(s\triangle H_A\) and \(t\triangle H_A\) is contained in that neighborhood. Inversion is the identity map. Translations are homeomorphisms.

The topology is Hausdorff. If \(s\ne t\), choose \(k\in s\triangle t\) and let \(A=\mathbb N\setminus\{k\}\). This cofinite set belongs to \(\mathcal U\), and the cosets \(s\triangle H_A\) and \(t\triangle H_A\) are disjoint: their equality would imply \(s\triangle t\in H_A\), although that set contains \(k\notin A\). Every basic neighborhood is infinite, so the topology is nondiscrete. The subgroups and their cosets are also closed, since their complements are unions of cosets.

## 4. An explicit countable dense partition

For \(j\ge0\), let
\[
D_j=\{s\in G:\nu_2(|s|+1)=j\},
\]
where \(\nu_2(m)\) is the exponent of 2 in the positive integer \(m\). These sets are pairwise disjoint and cover \(G\). The identity lies in \(D_0\).

Fix \(j\), a finite set \(s\), and \(A\in\mathcal U\). The integers
\[
q=2^j(2r+1)-1\qquad(r\ge0)
\]
are unbounded and satisfy \(\nu_2(q+1)=j\). Choose such a \(q\ge |s|\). Because \(A\setminus s\) is infinite, choose \(t\subseteq A\setminus s\) of size \(q-|s|\). Then \(t\in H_A\), and
\[
s\triangle t=s\cup t\in(s\triangle H_A)\cap D_j.
\]
Hence every \(D_j\) meets every basic open coset and is dense. In particular all the \(D_j\) are nonempty, giving exactly countably infinitely many dense pieces. This proves the target hypothesis directly, without importing a resolvability theorem.

## 5. No expansive sequence exists

Let \((F_n)_{n\ge0}\) be any sequence of pairwise-disjoint finite subsets of \(G\). We exhibit a nonempty open set missed by infinitely many blocks.

If infinitely many \(F_n\) are empty, the open set \(G\) already works. Otherwise omit a finite initial segment so that all remaining blocks are nonempty. The identity belongs to at most one block, by disjointness, so omit a further finite initial segment containing that block if necessary. Every element in the remaining blocks is now a nonempty finite subset of \(\mathbb N\).

For each remaining index define the finite nonempty set
\[
M_n=\{\max s:s\in F_n\}.
\]
For each \(k\in\mathbb N\), exactly \(2^k\) members of \(G\) have maximum \(k\): they are \(\{k\}\cup t\) with \(t\subseteq\{0,\ldots,k-1\}\). Since the blocks are pairwise disjoint, \(k\) belongs to \(M_n\) for at most \(2^k\) indices. Thus \((M_n)\) is point-finite.

Inductively select strictly increasing indices \(n_0<n_1<\cdots\) such that the sets \(M_{n_i}\) are pairwise disjoint. At each step the union of the already chosen sets is finite. Point-finiteness means that only finitely many indices have their maxima set intersecting that union. There remains a later eligible index. This also proves that the construction continues infinitely.

Put
\[
C_0=\bigcup_{i\text{ even}}M_{n_i},\qquad
C_1=\bigcup_{i\text{ odd}}M_{n_i}.
\]
These are disjoint. A proper filter cannot contain both, so choose \(\varepsilon\in\{0,1\}\) such that \(C_\varepsilon\notin\mathcal U\). By the ultrafilter property,
\[
A=\mathbb N\setminus C_\varepsilon\in\mathcal U.
\]
If \(i\equiv\varepsilon\pmod2\) and \(s\in F_{n_i}\), then \(\max s\in C_\varepsilon\), hence \(s\not\subseteq A\). Consequently
\[
F_{n_i}\cap H_A=\varnothing
\]
for infinitely many, arbitrarily large indices \(n_i\). But \(H_A\) is a nonempty open neighborhood of the identity. The sequence was therefore not expansive.

Since the original block sequence was arbitrary, this proves the negative answer.

## 6. Provenance, limitations and verification boundary

The proof above was independently developed in this investigation. Subsequent lineage checking identified the underlying topology as the standard free Boolean linear, or Mathias, topology: Sipacheva's survey, Section 8, p. 25, gives precisely the subgroup base used here. The topology itself is therefore not claimed as a new construction. The density/maxima argument is presented with a self-contained proof; no literature result asserting this target counterexample was located in the bounded search, and priority is not claimed. The standard ultrafilter existence principle is the only non-elementary set-theoretic ingredient, and its ZFC derivation is included. The source status and lineage checks are imported factual observations. Stronger selectivity assumptions in Sipacheva's discussion concern different properties and are not used here.

The proof is infinite and nonconstructive. No finite computation constructs a free ultrafilter or proves its existence. The accompanying standard-library verifier tests finite Boolean-group identities, the support-size coloring, finite versions of the maxima obstruction, and strict input-validation controls. Those checks supplement the written proof and do not replace its universal quantifiers. In particular, tests involving finite principal ultrafilters are explicitly excluded from being evidence of a free ultrafilter.

Only one substantive mathematical approach was used. Further approaches were unnecessary once the construction yielded the full target counterexample. No publication or source redistribution is part of this package.

## References

- E. I. Khukhro and V. D. Mazurov (eds.), *Unsolved Problems in Group Theory. The Kourovka Notebook*, version 48 (6 October 2026), Problem 21.107, p. 193; predecessor 15.80, p. 97: <https://arxiv.org/pdf/1401.0300v48>.
- Official version history: <https://arxiv.org/abs/1401.0300>.
- Official solution repository, checked for the target identifier: <https://kourovkanotebookorg.wordpress.com/repository/>.
- O. Sipacheva, *Free Boolean Topological Groups*, Section 8, p. 25, Mathias/free Boolean linear topology: <https://arxiv.org/pdf/1612.04878v1>. This reference is for construction lineage, not a proof dependency or a claim that it solves the target.
