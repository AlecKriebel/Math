# Source and novelty audit

Original source audit 30 September 2026; updated acceptance assessment 1 October 2026. This is a bounded source audit, not a proof of historical first priority.

## Original target

The requested [UnsolvedMath page](https://www.unsolvedmath.com/problems/30005934) was attempted before other research. The web reader could not access it. The exact record was recovered from the repository's pinned dataset revision, `37e53eabe540fb458758e198be61634bd02ee008`; see `source_record.json`.

The original [Oberwolfach report](https://ems.press/content/serial-article-files/49484), contribution *Infinite-dimensional Wishart Processes*, pp. 1478–1480, labels the target Open problem 1 on p. 1480 and prints alpha not in N with injective noise when the semigroup need not be injective. The intended noninteger obstruction is verified, with the zero-convention qualification below. Its next open problem concerns noninjective noise and is a distinct target.

The [final published Cox–Cuchiero–Khedher paper](https://pure.uva.nl/ws/files/234720765/Infinite-dimensional_Wishart_processes.pdf), *Electronic Journal of Probability* 29 (2024), article 123, has:

- Open Problem 1.2 on printed p. 5
- Theorem 3.1 and Corollary 3.4 for Fourier–Laplace transforms
- Corollary 4.2 for finite-dimensional compressed transforms
- Theorem 4.3, pp. 26–27, using semigroup injectivity in an existence classification

The narrow noninteger obstruction does not require the full classification or its existence direction. Our finite-rank proof works directly from the weak equation and does not import a global trace-class covariance assertion.

## Imported finite-dimensional theorem

Graczyk, Małecki, and Mayerhofer, [*A characterization of Wishart processes and Wishart distributions*](https://arxiv.org/pdf/1607.00206), Theorem 1.3, establishes the full positive-definite-scale noncentral Wishart parameter domain. The normalization used in this note is shape parameter $\alpha/2$ and scale matrix $2C$. The relevant scalar restriction is $\alpha\in\{0,\ldots,n-2\}\cup[n-1,\infty)$. Negative parameters are separately ruled out by scalar Laplace-transform growth.

This established theorem is used as an external mathematical dependency. Its whole proof is not reproduced or formally verified here.

## Earlier public candidate found before proof work

The current search found [Evidence Press's 22 September 2026 release](https://evidencepress.org/releases/wishart-reachable-noise/), which links an unrefereed manuscript at [GitHub](https://github.com/ipitchford/wishart-reachable-noise) and [Zenodo DOI 10.5281/zenodo.22892681](https://doi.org/10.5281/zenodo.22892681). The immutable source inspected is:

- Repository commit: `73dd242a4450400e2f8f16b65929cb77fee76be1`
- Commit date: 22 September 2026, 07:27:04 UTC
- [Manuscript](https://github.com/ipitchford/wishart-reachable-noise/blob/73dd242a4450400e2f8f16b65929cb77fee76be1/paper.md): Lemma 3 gives the finite-rank transform; Corollary 2 gives the injective-noise noninteger obstruction

This manuscript is an earlier explicit claim of precisely the conclusion in our candidate note. It labels itself unrefereed and does not establish external verification or priority. Our note credits its argument and checks only the narrower proposition needed for this queue entry. We did not audit the full singular-scale classification, Gaussian continuity equivalence, or all existence constructions in that manuscript.

## Prior project attempts and duplicate checks

Before substantive work, the live queue showed rank 30, `queued`, `0/5`. All-state pull-request searches for the numeric ID and “Wishart,” matching branch searches, connector content searches, and a recursive main-branch path search found no prior project attempt. The pinned research-results dictionary contained no matching code, and no report entry for this ID was found. This is distinct from the external prior candidate above.

## Disposition

Three independent acceptance-audit families and a fresh complete adversary pass the narrow argument in `CANDIDATE.md`. Accepted QUEUE status is already_solved for the intended noninteger obstruction, accepted as a credited partial research record without a new paper or DOI. The earlier source is Anonymous (2026), version0.1.0-candidate, Lemma3/Corollary2 and its random-initial scope paragraph, DOI10.5281/zenodo.22892681. Four archived files, advertised checksums, both ZIP manuscript copies and the immutable Git blob have been matched. This is positive evidence of an earlier exact public claim, not earliest historical priority or external peer review. The external candidate's wider claims remain outside this audit.

The source prints alpha not in N. No explicit convention was found. If N includes zero, the literal answer is negative; if N means positive integers, alpha0 with X0=Xt=0 is a trivial affirmative exception. The independently verified negative conclusion is alpha not in N0; zero is retained. No author intention is inferred. See the current PRIMARY_PRIORITY_AUDIT.md for exact source, parameter and archive evidence.

No outside individual was contacted. No broad source correction or upstream status change was sent.
