# Source and hypothesis audit for Erdős Problem 143

Audit date: 10 October 2026 UTC. Identifiers: record 1954, EP-143. The number 1954 is an identifier, not the date of the problem.

**Review scope.** This AI-assisted authored application and its independent internal AI audit are unrefereed. “Accepted” means only that the stated harmonic corollary follows from the explicitly imported theorem of Koukoulopoulos, Lamzouri and Lichtman. No external human peer review, journal acceptance, formal proof-assistant certification, novelty, or current worldwide open-status certification is claimed. The imported research theorem is not independently reproved. Scholarly-source retrieval and inspection statements describe the recorded audit; edition preparation performed no new scholarly-source retrieval or inspection.

## Decision

Accept the harmonic sparsity alternative as a prior consequence of [KLL25, Theorem 1](https://arxiv.org/pdf/2502.09539v1), with the exact application proved in COROLLARY.md. Do not classify the full two-part record as solved or give the present audit credit for a new mathematical theorem. Acceptance here concerns the correctness of the application of an explicitly imported research theorem. It is not a journal-acceptance certificate or a reconstruction of the theorem's full proof.

## Primary theorem checked

The entire 47-page versioned PDF was retrieved. Its bytes agree exactly with the independently authenticated earlier download. The full statement of Theorem 1, together with its preceding setup and following remark, was read on p. 2 and visually checked in a fresh render. The domain and discreteness convention were checked on p. 1. The direct harmonic formulation in equation (1.9) was checked on p. 3. The limitation discussion and the start of the proof reduction were checked on p. 6; the reduction roadmap in Section 2.6, pp. 14–16, and references on pp. 46–47 were read in the extracted text. These checks concern the complete theorem interface and relevant surrounding context. They do not certify every lemma in the remaining paper.

The following is the complete hypothesis-to-application checklist. The numbered proof steps refer to COROLLARY.md.

| Requirement or possible ambiguity | Resolution in the application |
| --- | --- |
| The set consists of positive real numbers | The stipulated domain is \((1,\infty)\), a subset of \(\mathbb R_{>0}\). No conversion to integers is made. |
| Discreteness means no real accumulation point | The \(k=1\) instance gives unit separation. The short-interval argument in Step 1 rules out every finite accumulation point, including 1. Merely assuming countability would not suffice. |
| Sums over bounded intervals are defined | Step 1 proves local finiteness; Step 2 proves finiteness and nonnegativity of every partial sum. |
| The density is harmonic upper density | It is \(\limsup H_A(X)/\log X\), not a counting density, a lower density, or \(\limsup H_A(X)/X\). |
| Lower and upper summation endpoints | \(A\subset(1,\infty)\) makes the theorem's \([1,X]\) cutoff identical to the authored \(x\leq X\) cutoff. Step 4 treats \(x<n\) explicitly. |
| Positive limit superior | This is assumed only in the contradiction argument. The nonnegative ratio's failure to converge to zero supplies exactly that premise. Its finiteness follows from the harmonic upper bound in Step 2. |
| Quantifier over approximation tolerance | Only the permitted value \(\varepsilon=1\) is needed. There is no demand for a single pair that works for every tolerance. |
| Distinct elements | The theorem supplies two unequal elements, which is exactly the scope of the separation hypothesis. No diagonal pair is used. |
| Positive integer multiplier | The integer produced by the theorem lies in the set of multipliers forbidden by the hypothesis. No nonintegral, zero or negative multiplier is substituted. |
| Strict versus weak distance inequality | The source supplies distance \(<1\); the hypothesis forbids it via distance \(\geq1\). Equality is handled correctly. |
| Rationality, linear independence, primitive integers | None is an additional hypothesis of Theorem 1. Older special cases are not silently substituted for the real-set theorem. |
| Stronger theorem conclusion about infinitely many pairs | Not needed: one forbidden pair suffices. |
| Removing a bounded initial segment | Not needed in the main application. If one follows the source's \(A\subset[2,\infty)\) proof reduction, at most one point below 2 is removed; its finite reciprocal contribution divided by \(\log X\) tends to zero. Thus this reduction adds no missing hypothesis. |
| Rescaling in the source proof | Not needed: the target separation threshold already equals the chosen tolerance. |
| From zero upper limit to a full little-o limit | Nonnegativity gives lower limit at least zero; Step 3 rules out a positive upper limit. This is a full limit, not only a subsequence assertion. |

## Boundary and attribution checks

The source distinguishes its two introductory conditions, and its p. 2 theorem addresses the harmonic-density condition. Its p. 6 discussion describes limitations on stronger quantitative estimates. The authored corollary consequently imports no weighted-convergence assertion. The summation-by-parts calculation in COROLLARY.md explains why the proved asymptotic does not itself bound the weighted series.

The classical integer primitive-set results are not an alternative proof for arbitrary real \(A\). In particular, replacing every real element by an integer part is not used: there is no established preservation of the full dilation separation under that operation. The floor function in Step 2 is only an injective binning device for a reciprocal upper bound.

No Behrend-rate estimate, zero upper natural density, or other stronger conclusion is accepted by this audit. The apparent natural-density goal in Section 2.1 of the source occurs inside a contradiction argument that also assumes positive harmonic upper density. It must not be detached from that assumption to produce a stronger universal claim.

## Historical source reconciliation

Paul Erdős, *On the density of some sequences of integers*, Bulletin of the American Mathematical Society 54 (1948), 685–692, [complete institutional archive PDF](https://www.renyi.hu/~p_erdos/1948-06.pdf), was retrieved in full. Problem II on printed p. 692 (PDF p. 8) was read and visually inspected. It poses both the weighted-series and harmonic-limit questions, confirming that resolving the latter is a partial resolution of the historical pair of questions. This is a newly checked historical source, not a new answer to either question.

The old printed shorthand ranges over integer indices without explicitly excluding equal indices. Read literally with \(k=1\) and equal indices, it would be inconsistent. The controlling modern formulation is the distinct-elements one stated above and in KLL Theorem 1. We do not exploit that shorthand to declare the problem vacuous. Likewise, a malformed unequal-symbol transcription is not interpreted as equality.

## Manuscript status and limits of the source check

The [arXiv record](https://arxiv.org/abs/2502.09539) retrieved on the audit date listed v1, submitted 13 February 2025, with 47 pages. [Lamzouri's institutional publication list](https://iecl.univ-lorraine.fr/membre-iecl/lamzouri-youness/), item 47, described the manuscript as submitted when retrieved. Accordingly, the citation is to a 2025 preprint. The PDF itself carries a 14 February 2025 title-page date; this is compatible with the arXiv submission date and does not identify a second arXiv version.

No journal acceptance, peer-review completion, or worldwide current-openness determination is asserted. Direct access to the problem tracker did not succeed in this pass; the mathematical acceptance rests on the complete primary theorem and the proof above, not on a tracker label or a search snippet.
