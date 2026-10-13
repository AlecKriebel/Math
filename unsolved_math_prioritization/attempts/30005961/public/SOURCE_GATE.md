# Source, scope, and novelty gate

Checked 2026-10-03. Target: **30005961 / OWR-14298581-008**.

## Provenance and exact target

The requested first endpoint was
[UnsolvedMath 30005961](https://www.unsolvedmath.com/problems/30005961).
The live page was inaccessible. The pinned problem record was used only to
recover the identity and source link; its assessment was not treated as proof.
The pinned research-results corpus contained no record under this problem code
or numeric identity. No upstream AI proof was available to validate.

The primary source is Keiji Oguiso's contribution, pp. **1821–1823**, in
[Oberwolfach Report 32/2024](https://doi.org/10.4171/owr/2024/32), from the workshop
held 7–12 July 2024. Question 1 poses the broad examples problem; Question 12
explicitly asks for a strict Calabi–Yau threefold beyond X3 and X7. This package
uses that narrower, non-vacuous target. A new map on an old variety is not enough.

Required conditions: complex dimension three; smooth and projective; trivial
canonical **line bundle**, not only numerical triviality; simple connectedness;
a everywhere-defined algebraic automorphism with everywhere-defined inverse;
positive topological entropy; no equivariant dominant rational fibration to a
normal projective curve or surface. The weaker Hodge vanishings do not substitute
for simple connectedness. The definitions are fixed throughout PROOF.md.

## Primary dependencies and exact locations

1. **Oguiso, OWR 32/2024**, pp. 1821–1823, Definitions 2–3, Theorem 5,
   Proposition 11, Question 12.
   [Official report PDF](https://ems.press/content/serial-article-files/50039?nt=1).
   Checked against [author preprint arXiv:2407.17297v1](https://arxiv.org/html/2407.17297v1).
2. **Oguiso–Truong**, *Explicit Examples of Rational and Calabi–Yau Threefolds
   with Primitive Automorphisms of Positive Entropy*, J. Math. Sci. Univ. Tokyo
   22 (2015), 361–385. Sections 3–4, especially Theorem 4.1, Lemma 4.3,
   Proposition 4.4. [Primary preprint](https://arxiv.org/abs/1306.1590) and
   [journal record](https://www.ms.u-tokyo.ac.jp/journal/abstract/jms220112.html).
3. **Oguiso**, *Endomorphisms of a variety of Ueno type and Kawaguchi–Silverman
   Conjecture*. Example 4.1, Theorems 4.2–4.3, Lemma 4.6.
   [Primary text, arXiv:2401.04386v3](https://arxiv.org/html/2401.04386v3).
   This supplies the actual X7 action 1+g and its biregular lift.
4. **Oguiso–Sakurai**, *Calabi–Yau threefolds of quotient type*, Asian J. Math.
   5 (2001), 43–77. Theorems 3.3–3.4 and Lemma–Definition 4.1.
   [Primary preprint](https://arxiv.org/abs/math/9909175).
   Their broader Calabi–Yau definition permits other fundamental groups.
   Theorem 3.4 includes extra quotient examples with nontrivial fundamental
   groups. Restricting to simple connectedness leaves X3 and X7.
5. **Gachet**, *Finite quotients of abelian varieties with a Calabi–Yau
   resolution*, J. École polytechnique Math. 11 (2024), 1219–1286.
   Theorems 1.1–1.2 on p. 1221, and the definition on p. 1220.
   [Published primary source](https://jep.centre-mersenne.org/articles/10.5802/jep.277/).
   It confirms the exact two-variety classification for the isolated
   abelian-quotient construction. The action must be free in codimension two.
6. **Oguiso**, *Automorphism groups of Calabi–Yau manifolds of Picard number two*,
   Theorem 1.2. [Primary preprint](https://arxiv.org/abs/1206.1649).
   This independently confirms the stronger known finite-group obstruction
   behind the elementary entropy-only proof in PROOF.md.
7. **Cantat–Oguiso**, *Birational automorphism groups and the movable cone
   theorem for Calabi–Yau manifolds of Wehler type via universal Coxeter groups*,
   Theorems 1.3 and 3.3. [Primary preprint](https://arxiv.org/abs/1107.5862).
   Generic Wehler threefolds have infinite birational group and trivial
   biregular group; their even-dimensional examples are not threefolds.

These are explicitly imported theorems. The package does not claim to supply
new proofs of the classification of crepant resolutions, the relative
product formula, or the entropy theorem.

## Two source-transcription hazards

- The arXiv v1 OWR preprint states d1>d2 for the X7 map, whereas the final
  official report on p. 1822 states d2>d1. The direct calculation for 1+g in
  PROOF.md gives the latter. The inverse has the former inequality. This has
  no effect on primitivity, whose criterion is the unequal degrees.
- OWR Definition 6 describes the maximal factorization in the opposite verbal
  direction from the original OS Lemma–Definition 4.1. We use the explicit
  original equation: every contraction Φ satisfies Φ=μ∘φ0. This direction
  supports the equivariance argument. No claim relies on the reversed wording.

## Bounded current-literature check

Searches included the target title, strict Calabi–Yau / primitive / positive
entropy combinations, and 2025–2026 variants. They recovered the sources above
and the following tempting but nonresolving matches:

- Kaur–Prendergast-Smith, *Remark on a theorem of Oguiso*, 2024, concerns a
  criterion for **birational** primitivity, so it does not establish a new
  biregular example. [Primary article](https://link.springer.com/article/10.1007/s11565-024-00506-8).
- A [May 2026 KIAS talk by Oguiso](https://www.kias.re.kr/kias/activities/seminars/view.do?edate=&menuNo=404003&mjrcdnm=&pageIndex=1&sdate=2026-04-29&seqno=PGN1720260402-0006)
  likewise advertises birational primitive maps of Wehler manifolds.
- Lee, [*Updates on Calabi–Yau manifolds from pairs of non-compact Calabi–Yau
  manifolds*, arXiv:2608.07694](https://arxiv.org/html/2608.07694v1), discusses
  smoothing and non-Kähler constructions. It does not provide the required
  primitive positive-entropy biregular threefold example. Nonprojective examples
  would not meet this target in any case.

No primary source settling the exact further-threefold question was found.
This is a bounded negative search result, not an exhaustive literature theorem
or a claim that no subsequent example exists.

## Duplicate check

The main-branch queue was read; rank 504 still named this target as queued.
Bounded repository checks covered root directory names, the attempts directory,
state entries, file searches for 30005961, Calabi, and 30005963, and branch-name
searches for calabi and the two numeric targets. No corresponding prior
mathematical attempt was found. Recursive whole-tree retrieval failed; no
exhaustive all-branch content inspection is claimed.

Related corpus record 30005962 is a preamble/extracted context, not a construction.
Record 30005963 combines the rational c2-null nef-class question with the further
primitive-example question. Its second part overlaps this target. That overlap
must not be counted as a separate discovery or evidence of a prior attempt.
The repository's related-target-group file listed neither target.

## Acceptance and publication boundaries

Success would require an explicit X not isomorphic to X3 or X7, a defined
biregular f, and checked proofs of every geometric and dynamical condition.
No such artifact exists in this package. The honest disposition is unresolved,
with the five-attempt budget exhausted. Only this small original commentary,
proof/checker package, and its own generated results are public candidates;
source PDFs, full extracted source texts, corpus data, and private records are
excluded. No external contact was made and no remote repository change was made
by the author of this checkpoint.
