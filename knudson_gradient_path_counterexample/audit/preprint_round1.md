# Fresh adversarial preprint review — round 1

Review completed: 2026-09-23 13:37:44 UTC.
Completion estimate: 100% of this assigned review. This is not a probability of historical novelty.
Reviewer: fresh AI adversarial referee, starting from the manuscript and primary sources, without using earlier mathematical audit verdicts. No person was contacted. No manuscript, code, package, or Git state was changed by this reviewer.

## Verdict

**PASS for the mathematics, target-source interpretation, stated scope, and executable verification. No new actionable mathematical or reproducibility error was found.** The reviewed package needs the citation-schema correction independently identified by the parent reviewer before an overall clean package verdict; that separate issue is recorded below. This review supports release as an explicitly unrefereed preprint after that correction, not a claim of external human peer review or proven priority.

## Independent checks and attempted falsifications

- **Source assumptions and claim.** I read Knudson's actual contribution, printed pp. 1628–1630 of the [publisher PDF](https://ems.press/content/serial-article-files/46173), especially Conjecture 2 on p. 1629. Its setup is a finite simplicial complex with a one-simplex-at-a-time filtration and mod-two homology; its field consists of incident persistence pairs. It does not impose a lower-star filtration or exclude degree-zero births. The conjecture refers to that fixed field. The four-vertex interval satisfies the setup, and later discussion of cancellations does not alter the conjecture's quantified field.
- **Pairing.** Independently reducing the ordered edge boundaries gives supports `{c,d}`, `{b,c}`, `{a,b}` and respective latest rows `d,c,b`. The component-merger calculation yields the same pairing. Each simplex is used at most once, only `(d,cd)` is incident, and `a` is the sole essential birth. No tie or reduced-versus-ordinary degree-zero convention changes the finite obstruction.
- **Gradient interpretation.** The six arrows in the proof exhaust the incidence graph. They contain no cycle. Both endpoints of the critical edge `ac` are unmatched vertices; the only vertices reachable after its initial downward step are `a,c`. Thus no alternating gradient path reaches `b`, even allowing a zero-length path at a facet. Treating column reduction as a path in a transformed algebraic basis would concern a different field.
- **All fields.** The three signed reductions printed in the paper are valid over the integers, with pivot coefficient one throughout, and therefore specialize to every field including characteristic two. No division by a potentially vanishing integer is needed. The finite-field executions are correctly presented as checks rather than the proof of this universal claim.
- **Cancellation comparison.** Reversing `bd → d → cd → c` produces exactly `{(d,bd),(c,cd)}`. The claimed subsequent path from `ac` to `b` follows. I checked [Bauer–Lange–Wardetzky's published PDF](https://link.springer.com/content/pdf/10.1007/s00454-011-9350-z.pdf), Lemma 9, printed p. 362: its unique path concerns an evolving cancellation sequence after descendant pairs have been removed, with a surface hypothesis. The manuscript's limited comparison is accurate; it does not apply that surface theorem to the interval or claim to refute it.
- **References.** Knudson's contribution title, author, page span and conjecture location agree with the original PDF. BLW's author list, title, journal, volume, year, pages and DOI agree with the publisher version. The [ELZ publisher PDF](https://link.springer.com/content/pdf/10.1007/s00454-002-2885-2.pdf) confirms its bibliography. DOI resolver access for the OWR item failed in the web tool; the direct publisher PDF was readable. No incorrect citation was found.
- **Scope and provenance.** The paper claims a counterexample to the printed statement, not minimality, first discovery, or a current catalogue status. Only after completing the mathematical/source checks did I inspect the priority-audit record to check that the manuscript's calibrated description matches the documented limits. It does. I did not repeat its entire search. The unrefereed and AI-assisted status and the author's ORCID are disclosed consistently.

## Executable and package checks

I read both programs, then executed both normally and with `-O`, using Python 3.14.6 on macOS arm64. All four executions exited zero, produced no stderr, and matched their stored expected outputs byte for byte. The checks cover filtration validity, mod-two reduction, union-find, independent component-partition ranks and mixed differences, signed reduction over Q and five prime fields, original and reversed paths, acyclicity, and label relabeling. They use exact arithmetic and the standard library. The documented Python 3.9 minimum is consistent with the syntax and standard-library features used; Python 3.9 itself was not installed/executed in this review.

`verification/verify.py` is byte-identical to its preserved input. I also compared the ZIP's manuscript source/PDF, two verifier files, README, CFF and deposition metadata to the reviewed working files; all were byte-identical. The upload PDF matched the manuscript PDF. Full visual/layout and build-system review was assigned to the parent reviewer and is outside this verdict.

## Actionable issues

1. **Package metadata, moderate; independently found by the parent during this review.** The reviewed `CITATION.cff` has top-level `type: article`, which the parent's official CFF 1.2 schema validation found invalid. Use valid top-level package metadata and place the article under `preferred-citation`, then validate and regenerate the distributed package. This is not a mathematical finding from this referee and is not claimed to have been fixed in the hashes below.

**No additional substantive correction requested.** A standalone companion-package URL and PDF author/title metadata would improve discoverability; these are optional presentation improvements, not mathematical objections. No stylistic preference is being elevated to a release blocker.

## Remaining gaps

There is no unresolved gap in the explicit counterexample proof within the printed conjecture's scope. Absolute historical novelty remains unverified, particularly the inaccessible book/dissertation and preparation item already documented by the priority audit; the paper acknowledges a bounded search. Human peer review and proof-assistant formalization have not occurred and are not claimed. The known CFF correction and regenerated artifacts require the parent's follow-up validation; this report records the initial reviewed snapshot.

## Reviewed SHA-256 snapshot

```text
b70401cbcdabf96e4b0a4f9a35b40ef5414619399f21ee984312fc4e85baf7f5  paper/paper.tex
fb0a1686db12ad4b518312fd2c8b3097d2e7b2fa161418164e55a92b400243fb  paper/paper.pdf
aed912e2ba41f1ce6ed400a65d9c0cc6dc7cdd6361b7e87eb924d303607f1df6  verification/verify.py
d3b5d2fc62636a7ed3d0e8ffa1b759348c715a9bf97016666454e712ce087359  verification/independent_check.py
21982a0e73a6327e1b93573d7b4504157f1e489ca00aee9b149f12c70ba407bc  verification/expected_output.txt
dba61bdd196c698596d987419ae4175d64dcdaf4fa1235ad77da503fba70a2dd  verification/independent_output.txt
3c30050c261576f92694f6559d40317fd83df0a3edd49521ea96acb55735d00c  verification/README.md
6e162e477bbbf417417ad2dc7a249110ccaa027db4fea7a60aab6e5b93ba001a  README.md
d5bcb0085d2708b2fc32e42e28758d7fc13033e92364a1fe673e4b4553ef686e  CITATION.cff
e3d902c11755626e5b730d836e3f52db9d07435d7f70fd0ff542296fdb57b9e7  LICENSE.md
a583823a4f6a64d74a48737b502616c95e3226533e71ca1a76175bb1028b3369  zenodo/deposition.json
0e514fb93709499f15e272cb166e4ab99c02439c76c9cd0ce2e8be3f4f3ed8c5  audit/priority_independent.md
a68b962a1c7a868e81f35d64d681e2ab4d31823fbe50636ae288a116d0c38531  zenodo/upload/source-and-verification.zip
```
