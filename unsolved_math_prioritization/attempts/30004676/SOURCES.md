# Source and provenance audit

## Exact target

- Numeric ID: 30004676; code OWR-7155442-010; queue rank 212 in the recovered
  checkout. The queue's `queued / 0/5` entry predates the interrupted local
  work and is not being treated as a reliable attempt counter.
- Primary item: Vadim Puzarenko's entry in *Computability Theory*, Oberwolfach
  Report 21/2021, printed pp. 1181–1182, PDF pages 33–34 (1-indexed).
  [Publisher PDF](https://ems.press/content/serial-article-files/46899),
  [publisher landing page](https://ems.press/journals/owr/articles/7155442).
  The entire PDF was downloaded and the relevant pages inspected as text.
  SHA-256: `06ed94bdd946d4f3bf784759dd2e6edb0ba4f2dd1b3fd76e103ab7a75ed953af`.
- The source distinguishes atomic Delta pullbacks from preservation of all
  internal Sigma relations. The first implication is explicitly known; the
  second is the question. This package proves neither implication anew.
- The report's context is admissible structures, although the displayed
  condition does not repeat every quantifier or convention. The conditional
  lemma explicitly specifies relational KPU structures and parameters; it does
  not silently replace the original target with an arbitrary graph question.

## Dataset record and prior report

The user authorized [ulamai/UnsolvedMath](https://huggingface.co/datasets/ulamai/UnsolvedMath)
as fallback to the blocked problem site. Downloaded immutable revision
`37e53eabe540fb458758e198be61634bd02ee008` on October 1, 2026.

- `problems.json`: 68,931,837 bytes; SHA-256
  `04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf`
- `research_results.json`: 80,334,822 bytes; SHA-256
  `8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b`

The exact problem row was extracted. Its mathematical target agrees with the
primary report; its dated August 22, 2026 literature triage is not current proof
evidence. The research-results dictionary has no exact `OWR-7155442-010` key;
the repository's exact-key joining rule therefore attaches no prior report.
No similarly titled report has been substituted.

`review_v2/related_target_groups.json` contains no matching ID. The desk
assessment suggests universal predicates but is explicitly provisional; it
does not supply the missing definability or internal-bounding argument.

## Background literature and limits of this check

- [Antonio Montalban, *Rice sequences of relations*, Theorem 5.14](https://math.berkeley.edu/~antonio/papers/Rice.pdf)
  supplies primary-author corroboration of structural jump fixed points and
  explains that several jump conventions coexist. Its countable-structure
  setting is not automatically the full admissible-set theorem here.
- [Puzarenko, *Computability in special models* (2005)](https://www.mathnet.ru/php/archive.phtml?jrnid=smj&option_lang=eng&paperid=951&wshow=paper)
  and Avdeev–Puzarenko, *A computable structure with non-standard computability*,
  Siberian Advances in Mathematics 29 (2019), 77–115,
  [DOI](https://doi.org/10.3103/S1055134419020019), are the examples cited by the
  report. The publisher metadata was located; their complete proofs have not
  been reconstructed or claimed as new results.
- The dataset's old 2011 conference PDF link could not be fetched with the web
  tool during this recovery. The original 2021 report was available, so that
  unavailable background link does not block recovery of the exact question.
- Targeted searches on October 1, 2026 for the exact title, source DOI,
  admissible Sigma-reducibility and the named authors did not identify a full
  resolution. This was a bounded search, not a proof of current open status or
  historical novelty. No outside person was contacted.

Only original mathematical text and metadata are proposed for publication.
Downloaded full papers are local reading copies and are outside the attempt
folder. No third-party code was executed.
