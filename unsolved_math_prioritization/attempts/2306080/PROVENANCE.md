# Source and status verification

Checked on 2026-10-04 UTC. Target: numeric ID 2306080,
AMR-022-6080, Hayman–Lingham Function Theory 6.80.

## Exact target

The question is whether every analytic injective function f on the open
unit disc has a normal based primitive F(z)=integral from 0 to z of f.
No boundary extension, growth bound, or normalization of f is imposed.
The surrounding discussion about other derivative orders is background,
not an additional unresolved part. One univalent f with a nonnormal
primitive answers the complete yes-or-no question negatively.

The [catalogue page](https://www.unsolvedmath.com/problems/2306080)
was attempted first and returned HTTP 403. Its current rendered content
was therefore not verified. The exact statement was checked against
Hayman and Lingham, [arXiv:1809.07200v2](https://arxiv.org/abs/1809.07200v2),
Problem 6.80 and Update 6.80 on printed page 145. That update says that
the editors had received no progress report. It is superseded by the
older primary publication identified below.

## Published resolution

Peter Lappan, *On the Normality of Derivatives of Functions, II*,
Journal of the London Mathematical Society (2) 24, no. 3 (December 1981),
495–501, [DOI 10.1112/jlms/s2-24.3.495](https://doi.org/10.1112/jlms/s2-24.3.495).
The [publisher abstract](https://academic.oup.com/jlms/article-abstract/s2-24/3/495/860269)
explicitly describes an example with a univalent integrand and a
nonnormal integral. Its scope is precisely the target's negation.
The paywalled original full text was not obtained and is not claimed
to have been read.

The formula and attribution were checked in Janne Gröhn, *On non-normal
solutions of linear differential equations*, Proceedings of the American
Mathematical Society 145 (2017), 1209–1220,
[DOI 10.1090/proc/13292](https://doi.org/10.1090/proc/13292), electronically
published September 8, 2016. In the inspected
[published-format author-hosted copy](https://integraali.com/defense/defense4/suomeksi/papereita/Grohn%20-%20On%20non-normal%20solutions.pdf),
equation (12) is on PDF page 9 and reference [16] is on PDF page 12.
It gives

\[
 (1-z)^{-(1+10i)/100}-(1-z)^{-1/100}
\]

and attributes it to Lappan (1981), Theorem 5. The page image, formula,
and bibliography were checked. PROOF.md supplies a complete direct
verification, including the global univalence step.

## Preprint discrepancy

The [arXiv preprint 1602.00161](https://arxiv.org/abs/1602.00161), equation
(12) on PDF page 9, instead prints the second exponent as −i/100, and
its reference [15] points to Lappan's 1978 paper without “II”. These are
actual visible differences between the inspected PDFs, not assumptions
based on text extraction. The published version corrects both details.
The counterexample in PROOF.md uses the published real exponent −1/100.
The arXiv formula must not be silently copied as evidence for this result.

For a check on why this matters, let a=1/100+i/10, b=1/100 and
J(z)=(1−z)^−a−(1−z)^−ib, the preprint's printed expression.
With r=|1−z| and |arg(1−z)|<pi/2, the first term has magnitude at least
exp(−pi/20) r^−b, whereas the second is bounded by exp(pi/200).
For all sufficiently small r, |J(z)| is therefore bounded below by
(1/2) exp(−pi/20) r^−b. Its derivative has magnitude at most
|a| exp(pi/20) r^−1−b + b exp(pi/200) r^−1.
Since 1−|z|²≤2r, we get (1−|z|²)J#(z)=O(r^b) as z tends to 1.
On the remaining portion of the closed disc, both J and J′ extend
continuously and J# stays bounded. Thus that misprinted expression is
normal and would not itself establish the desired counterexample.

## Dataset and prior report

The repository's source manifest pins UnsolvedMath revision
37e53eabe540fb458758e198be61634bd02ee008.
The [pinned problems file](https://huggingface.co/datasets/ulamai/UnsolvedMath/resolve/37e53eabe540fb458758e198be61634bd02ee008/problems.json)
was downloaded, hashed, and the selected record inspected. Its hash is
04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf
(68,931,837 bytes). Its selected target record agrees with the more recent
locally available catalogue record.

The pinned research_results.json hash is
8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b
(80,334,822 bytes). The matching complete prior record was read. It is
an OPEN-TRIAGE report describing a statement review and unsuccessful web
search, with no proof, counterexample, or substantive partial result.
The present known-result classification rests on primary publication
evidence and the complete verification, not that earlier assessment.

Dataset curation metadata is CC BY 4.0; underlying source publications
retain their own rights. The public package contains citations and
original explanatory proof text, no source PDF or bulk source corpus.

## Repository and duplicate checks

At the checked main reference
6a112842592930803e459f013484062787ce7772 in AlecKriebel/Math:

- The selected queue row was rank 588, queued, 0/5.
- The returned complete attempts-directory tree had no 2306080 entry;
  a direct lookup of that target directory returned 404.
- Target-specific PR searches for 2306080, “6.80”, and Lappan returned
  no matches in all PR states. The code search for 2306080 also returned
  no matches; code-search absence alone was not treated as conclusive.
- The related-target-groups file contained no group with this numeric ID.
- A pinned-source scan for statements containing “univalent” and either
  “normal” or “primitive” yielded ten candidates. Inspection found no
  second instance of this exact question. The other nine concern
  multipliers, convolution classes, quasiconformal extensions, coefficient
  convergence, interpolation, extremals, inverse decompositions, integral
  means, or neighbourhoods. This is a scoped duplicate check, not an
  assertion that every possible paraphrase in the literature was scanned.

## Classification and limits

Recommended classification: **already_solved**, negative answer,
attributed to Lappan (1981). One complete substantive reconstruction
uses 1/5 turns. There is no new-resolution or novelty claim. The source
page is inaccessible, the original Lappan full text is uninspected, and
the computational controls are finite checks rather than proof
certificates for the analytic theorem. None of these limitations leaves
a mathematical gap in the self-contained counterexample proof.
