# Kourovka 21.122: authoritative scope contract

Prepared 2026-10-24 UTC. Source and priority preparation only; discovery estimate 0%.
No original solution attempt or top-level problem status is recorded by this package.

## Authoritative source and provenance

The official [Kourovka Notebook website](https://kourovkanotebookorg.wordpress.com/)
currently links issue 21 (2026), edited by E. I. Khukhro and V. D. Mazurov, in the
[current main PDF](https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/10/21tkt-3.pdf).
The source was freshly retrieved at 2026-10-24T23:07:05 UTC. Problem 21.122 is on
printed page 197, also PDF page 197 (one based), text extraction line 9492.
The proposer is P. Shumyatsky. There are no lettered subquestions.

The exact entry reads:

> 21.122. Let w be a group word, and G a profinite group. Is it true that the cardinality
> of the set of w-values in G is either finite or at least continuum?
> An affirmative answer is known for several important words; see (E. Detomi,
> B. Klopsch, P. Shumyatsky, J. London Math. Soc. (2), 102 (2020), 977–993).
> P. Shumyatsky

The main file SHA-256 is
`f133b4547caae29822fb65455b2115c4af075aa168983996a2aac1c2b21bc118`.
The [current official updates PDF](https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/10/21upd-3.pdf)
was freshly retrieved in the same batch; its SHA-256 is
`3371fa96766d35e18256af9eeac299785d95fb211b31d5e1b31bfab6da2beb71`.
It has no occurrence of `21.122`. The entry in the main PDF has neither a solution
star nor an unverified-AI sharp. Absence of a mark or update is only an initial
screen; the mathematical literature must be checked separately.

Chronology limitation: the current official site's update announcement is dated
20 October 2026, but the linked update PDF is headed **November 2026 update**.
This package reports the actual retrieved file rather than treating that heading
as an independently established future publication date. No more precise original
submission date for 21.122 is supplied in the entry.

## Exact quantifiers and notation

For every ordinary group word \(w\in F_d\), where \(d\) is finite, and every profinite
group \(G\), put

\[
G_w=\{w(g_1,\ldots,g_d):g_1,\ldots,g_d\in G\},\qquad
\mathfrak c=2^{\aleph_0}.
\]

The target implication is

\[
|G_w|<\mathfrak c\quad\Longrightarrow\quad |G_w|<\infty.
\]

Here profinite means compact Hausdorff and totally disconnected, equivalently an
inverse limit of finite groups. The word is evaluated on all tuples. There are
no assumptions of finite generation, countable basis, metrizability, linearity,
solubility, nilpotency, or pro-p structure. Generalized words containing group
constants, restricted coprime commutator values, and order-dependent word sets are
not the original target. No Continuum Hypothesis is assumed: merely eliminating
countably infinite value sets would not address every cardinal below continuum
when CH fails.

The target concerns the **set** \(G_w\), not the closed verbal subgroup
\(w(G)=\overline{\langle G_w\rangle}\). Strong conciseness asserts the stronger
conclusion \(|w(G)|<\infty\) under the same small-value hypothesis. Ordinary
conciseness assumes the value set is already finite and asks whether the verbal
subgroup is finite. An open-status statement for strong conciseness alone does
not certify openness of 21.122. A finite-value-set example with infinite verbal
subgroup does not refute 21.122, which permits finite value sets.

## Success criteria and source-level boundary checks

An affirmative resolution must prove this implication for every ordinary word and
every profinite group. A negative resolution must give an ordinary word and a
profinite group with \(\aleph_0\leq |G_w|<\mathfrak c\), with all claims proved.
A theorem restricted to one group class or word family is a partial result.

The identity word has value set \(\{1\}\); finite groups meet the conclusion
immediately. For \(w=x\), the issue is the established finite-or-at-least-continuum
cardinality of profinite groups. These checks introduce no restriction on the
full question.

The continuous word map has compact image, but no general finite-or-continuum
theorem for arbitrary continuous maps between profinite spaces may be substituted
for the problem. Detomi–Klopsch–Shumyatsky, Proposition 2.1, assumes that the map is
**nowhere locally constant**. Its contrapositive supplies one nonempty open
constancy patch for a small-image word map, not finiteness of its whole image.

## Preliminary selection recommendation

`provisionally_eligible_no_complete_resolution_located`, as of this bounded
2026-10-24 audit. See PRIORITY.md and the independently prepared
independent_status/AUDIT.md. This is not a proof that no prior solution exists,
not a solved label, and not an originality or publication claim.
