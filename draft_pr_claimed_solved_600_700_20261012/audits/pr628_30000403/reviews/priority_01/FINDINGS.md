# PR628 independent priority audit

**Verdict: PRIORITY OBJECTION CONFIRMED.** The accepted mathematical statement survives; its presentation as a novel resolution of a still-unsolved problem does not. One mandatory finding is recorded below. This review changes no PR, queue row, native proof, branch, external record or spreadsheet.

Input: PR628, problem 30000403 / OWR-1188-004, immutable head `677673860f9e67dffc610f52384f0bd60e65e363`. The original proof SHA-256 is `20cb77c2ac8befd8d2f9be9a421d2925580c29e24002a1abc8e3dedb13caeb5a`. Both fresh mathematical-family reports were read and both say PASS with zero findings. The priority review does not revoke those mathematical results.

## Mandatory finding P1: the central result follows from prior compression theory

The packet and original audit acknowledged neighboring results but did not work through the generality of Bresciani's compression method. That omission is material to the requested publication decision. Theorem/proposition statements in the 2022–2024 primary sources are more general than the divisor titles suggest.

The complete bridge is in IMPLICATION_DERIVATION.md. For the ordinary coarse fiber F and H=PGL2, form G=[F/H] and P=[(F x P1)/H]. The coarse compression Y of P is a genus-zero curve; the dense open where stabilizers on P1 are trivial is an open subset of P itself. A point on that open gives an H-torsor with an associated conic section, hence a trivial torsor and an ordinary coarse point over the **same** field. A degree-at-most-two point of Y proves the universal bound. Earlier Bresciani ramification theory forces Y split whenever the geometric cover-point stabilizer is noncyclic, including V4. Cadoret already supplied examples needing degree two.

The prior chain is checkable without assuming that an actual marked cover descends or that the cover-point stabilizer equals the full branch-divisor stabilizer. It is not a transfer to an unsupported equivalent conjecture. Parent and reviewer independently reconstructed the quotient bridge during this audit; that corroboration is not human peer review.

Required publication repair: do not call the constant-two theorem, its uniform sharpness, or V4 degree-one assertion a new solution of a still-open problem. Credit the prior compression framework and the exact implication. A first-priority claim is unsupported. Adding a few citations while retaining the new-open-problem-resolution claim is insufficient.

## Comparison of approach families

| Family | Evidence and mechanism | Status | Exact gap |
|---|---|---|---|
| Cadoret 2006/2008 | Original coarse lifting question; normalizers; nonoptimal upper bounds; actual degree-two lower-bound examples | Essential prior framework and sharpness | Does not itself state the full new packet theorem; Remark 3.14 uncertainty is not a solution |
| Bresciani–Vistoli 2022 general compression | Faithful structured objects, universal family, coarse compression, free open | Implies universal upper bound after explicit split-target bridge | No mathematical implication gap remains; earliest historical recognition not known |
| Bresciani divisor 2022 / published 2024 | General gerbe Proposition 2 / 28; noncyclic band excludes nonsplit compression | Implies V4 degree one, and more generally every noncyclic stratum | Exact Hurwitz wording not located in this paper |
| Bresciani structures 2023 / published 2024 | Twisted finite-group quotients, faithful structures, cohomological normalizer criterion | Explicitly corroborates applicability to the coarse orbit construction | No need to turn an actual cover into a faithful target structure |
| Huggins 2004/2007 | Noncyclic reduced hyperelliptic descent; V4/S3 quotient and odd-degree conic point argument | Earlier related mechanism | Not used as an unproved universal marked-Hurwitz theorem |
| Hidalgo 2013 rational dynamics / Doyle–Silverman 2018–2019 | Quadratic descent for rational maps under conjugation; higher-dimensional bounds | Different objects/action, strongly related mechanism | Not equated directly with all G-marked cover points |
| Hidalgo 2024 general rational-map actions | Universal-action quadratic bound and branch-signature argument | Additional earlier neighboring theorem | Rational-map-action domain differs from the full Hurwitz input |
| Marinatto 2013 point divisors | Publisher abstract verified; Bresciani explains even-cardinality nonsplit-target examples | Earlier sharpness lead | Complete original primary PDF not obtained; no same-formula or earliest-Q claim |
| Fuertes–González-Diez cubic obstruction | Erratum record verified; Lercier–Ritzenthaler–Sijsling 2013 section 3D gives corrected explicit descent | Apparent counterexample rejected | Direct author corrigendum byte retrieval failed; no invented hash or detailed correction quote |

## Versions, locators and dates that matter

* Bresciani–Vistoli: arXiv:2210.04789v1, 10 October 2022 15:45:48 UTC; section 5.1 and Definition 5.3, Theorem 5.4 and its free-open proof, Corollary 5.5, manuscript pp.10–11. Published DOI 10.1112/S0010437X2400705X, online 27 March 2024. The arXiv v1 PDF was directly downloaded and hashed.
* Bresciani, divisor: arXiv:2211.03438v1, 7 November 2022 10:40:25 UTC; general Proposition 2, pp.3–4. Directly downloaded published version, Journal of Algebra 647 (2024), 72–98, DOI 10.1016/j.jalgebra.2024.02.021: section 3.4 p.88, Proposition 28 pp.89–91. The proof, rather than a title or search snippet, supplies the generality used here.
* Bresciani, structures: arXiv:2303.01409v1 dated 2 March 2023, v2 dated 28 November 2023; published Bollettino UMI 17 (2024), 613–624, DOI 10.1007/s40574-023-00399-z, online 27 November 2023. Both preprint versions and the published PDF were directly downloaded. Theorem 2, Definition 5, Lemma 6, Corollary 10 and Proposition 14 formalize precisely the relevant twisted quotients; Theorem 4's H1(N)->H1(N/E) surjectivity alone would not suffice for a **split-target** conclusion.
* Cadoret: author manuscript GPGL2, Remark 3.14, p.15, and the original OWR2006 question, printed p.326. Publisher confirms Israel Journal of Mathematics 164 (2008), 19–59, DOI 10.1007/s11856-008-0019-0. Author bibliography instead lists 19–61; a publisher-PDF request redirected to HTML, so manuscript labels are not misrepresented as verified publisher labels.

The earliest complete implication chain independently checked here is available by November 2022. This is an upper bound on the date of the verified prior theory, not a claim that no earlier argument exists.

## Assessment of reasonable repair

The packet has useful checkable exposition: a direct elliptic-2-torsion realization and an unusually small exact six-point example. A short note crediting the earlier result could be worthwhile as exposition or an explicit verification example. We have not established a new theorem or a new unresolved problem within that material. Changing the objective to a novelty claim about an unverified explicit formula would not be a reasonable repair of the requested decisive-open-problem paper.

For the user's present process, I recommend **close rather than publish/merge as a new solved-open-problem result**, after an independent adversary verifies the prior implication and the parent makes the final disposition. If the parent instead considers a separately scoped expository publication, it must explicitly state that the theorem follows from prior theory; this priority report does not certify new mathematical novelty for that alternative. Do not discard the valid proof or label it mathematically false.

## Limits and provenance

Searches covered the named source and follow-ups, finite PGL2 normalizers and homogeneous spaces, divisor and hyperelliptic descent, the three supplied DOI leads, related general-structure results, and indexed literature through 2026. This was extensive but not exhaustive. A 2026 IMRN article still discussing individual rational lifts does not contradict the uniform extension bound: deciding degree one for each point is a stronger separate question. No exact earlier paper printing the complete Hurwitz theorem verbatim was found. The positive prior implication, not that negative search statement, supports the verdict.

SOURCE_RETRIEVAL.json records successful and failed direct requests, hashes and byte counts. Full primary PDFs/extractions are confined to ignored tmp/. SOURCE_LEDGER.json and SEARCH_LEDGER.md contain authored comparisons and bibliographic records. INPUT_BINDINGS.json rechecks all 36 native files and the four mathematical review inputs. No source text or figures were redistributed in these public review artifacts. No human/outside individual or other shard agent was contacted.
