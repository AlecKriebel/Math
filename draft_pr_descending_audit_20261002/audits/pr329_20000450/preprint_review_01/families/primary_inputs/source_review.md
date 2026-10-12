# Independent primary-input review 01

Status: assigned primary-citation, modular and arithmetic-source review complete; no substantive defect found within this family. This is an unsealed family report, not publication clearance or a verdict on the entire manuscript.

## Scope and independence

Read `/Users/alec/Documents/Math/AGENTS.md`; then read AIM physical page 51, Question 17 and all four remarks; then read the entire candidate `evidence/candidate_stage1/inputs/manuscript.tex` supplied in the assignment. The source-first initial sequence had no pre-candidate written strategy freeze. That limitation is reported honestly; no retrospective freeze is claimed. No previous family/root report, verdict, candidate archive or supplied script was read. All subsequent derivations and checking code were authored independently here. No repository, publication, tracker or external-message action was taken.

## Exact primary support

| Input | Directly checked primary locations | Candidate claim assessed | Result |
| --- | --- | --- | --- |
| AIM original | Physical/printed p.51, Q17 and remarks (i)–(iv); cover physical1 | Regular pentagon plus circumcircle-square pencil; five infinity torsion points; Sha/twist motivation; pencil interpretation; nonregular/star variants. Workshop Dec.11–20,2002; version Nov.22,2004. | Supported. The candidate correctly limits its answer to its specified regular-pentagon equation/origin. |
| Fisher 2001 | Printed172 (physical4), Lemma1.1 and equation(2); printed173 (physical5), equation(4); printed179 (physical11), triples/action/quotient; printed181–182, equations for X(5) and elliptic family; printed194 (physical26), Lemma3.4/proof. | Tate equation/discriminant; absence of automorphisms fixing P0; labelled full-level degree-five cover; f,g,epsilon,iota and exact parameter map. | Supported. Lemma3.4 is stated for rational parameters, but Section2 supplies the algebraic full-level family and quotient; the manuscript's finite-etale extension argument supplies all-fiber validity. |
| Verdure 2006 | Printed75–88 (physical1–14) read visually; particularly Prop.3 pp.80–81, Cor.1 p.81, Thm5 p.84 and entire proof pp.84–88. | Degree-one-or-five field; all-fiber criterion (beta−c)/(beta+c⁻¹) a fifth power; nonsingular specialization validity. | Supported exactly. Theorem5 assumes characteristic different from5 and P5(t)≠0. At pp.87–88 the proof explicitly notes all factors needed for nonvanishing survive every such specialization. Characteristic-zero candidate meets these assumptions. |
| Morton v4 | Printed/physical5 D5 table, physical6 radical and equation(2.1), physical7 Thm2.1, physical7–9 proof, physical9–11 order-five verification. arXiv abstract-page submission history/journal reference. | All twenty nonmarked Tate-family points already have explicit formulas; residual table under b=−beta; radical map; operative version/date/metadata. | Supported. Every table coefficient and the radical's sign are independently checked. v4 is June11,2018; title includes Rogers–Ramanujan continued fraction; JNT200(2019),380–396; DOI10.1016/j.jnt.2018.12.013. |
| Morton v1 | Physical3 table, physical3–4 radical, physical5 Thm2.1; page1 arXiv stamp and separate manuscript date; primary arXiv history. | The residual table and radical predate v4 and already appear in v1 pp.3–5. | Supported. Public submission was Dec.19,2016,17:06:49UTC; the document itself also has a Dec.17,2016 author date. The candidate's version date is the correct submission date. Its claim does not rely on v1's subsequently corrected transformation wording. |
| Sutherland Lecture5 | Header physical1; Thm5.8 physical3–4 and proof; sections5.5–5.6 physical10–14, division recurrences/Thm5.21/proof, degree/relatively-prime lemmas, Thm5.25/proof. | [5] has separable degree25 and25 distinct kernel points in characteristic0; classical division-polynomial context. | Supported. Theorem5.25 gives degree n² and separability; Thm5.8 identifies kernel cardinality with separable degree. Date is Sept.26,2023. |
| Sutherland Lecture23 | Header physical1; section23.5 physical10–13, pairing definitions and rationality/Galois context; Thm23.29 and Cor.23.30 physical13. | Nondegenerate Weil pairing forces zeta into the full torsion field. | Supported. Thm23.29 includes nondegeneracy, Galois equivariance and surjectivity; Cor.23.30 states the required field inclusion. Date is Dec.5,2023. The lecture refers nondegeneracy to standard primary references, while giving the other pertinent arguments. |

Fisher's author PDF and publisher page independently corroborate JEMS3(2001),169–201 and DOI10.1007/s100970100030. The author PDF says online Feb.15,2001; the current publisher landing page gives June30,2001 as publication. The candidate gives only the year2001, so this creates no bibliographic conflict. Verdure's scanned title page corroborates IJPAM33(1)(2006),75–92 and the title/author. No wrong date, title, DOI or pinpoint found.

Primary sources: [Fisher author PDF](https://www.dpmms.cam.ac.uk/~taf1000/papers/jemspaper.pdf), [Fisher publisher](https://ems.press/journals/jems/articles/124), [Verdure author PDF](https://math.uit.no/ansatte/hugues/papers/IJPAM.pdf), [Morton v4](https://arxiv.org/pdf/1612.06268v4), [Morton v1](https://arxiv.org/pdf/1612.06268v1), [arXiv metadata/history](https://arxiv.org/abs/1612.06268v4), [MIT Lecture5](https://math.mit.edu/classes/18.783/2023/LectureNotes5.pdf), [MIT Lecture23](https://math.mit.edu/classes/18.783/2023/LectureNotes23.pdf).

## Independently verified deductions

`independent_derivations.md` gives checkable derivations and the all-fiber cover/field proof. `check_primary_arithmetic.py` is a new standard-library program with eleven passing exact checks, including:

* c*h=−1 and the conversion of Verdure's alpha5,beta5 to c,−c⁻¹;
* the exact Fisher Mobius/fifth-power identity;
* coprimality and degree five of its parameter map, and derivative numerator (tau²−tau−1)⁴;
* all four excluded source-base values and the absence of ramification on the allowed base;
* iota(beta)=−1/(lambda+c), Verdure ratio=−c(lambda+c), Morton ratio=c(lambda+c);
* all eleven residual-table coefficients under b=−beta.

The finite-etale argument is complete on the allowed base: the complementary-basis scheme and the Kummer scheme are both finite etale and normal, have the same generic function-field cover, and hence coincide as the integral closure. Marking P0 removes the j=0,1728 stabilizers. Split fibers are allowed. Verdure gives a separate arithmetic proof: after adjoining theta, the criterion makes all torsion rational; the degree-one-or-five result and failure of the criterion before adjoining theta force equality of the torsion and radical fields. The field degrees, norm descent, dihedral product, independent delta involution and real odd-torsion subgroup follow by the elementary arguments recorded in the derivation file. No central difficulty has been transferred to an unsupported generic-specialization assertion.

No fixed-class sign mistake was found: field equality is distinct from equality of Kummer classes, and the candidate explicitly states that [−1/a]=[a]⁻¹. No all-fiber exclusion beyond the stated Tate cusps is imposed by these primary inputs.

## Novelty and wording limits

The primary record establishes that full universal Tate-family Kummer torsion and explicit coordinates substantially predate this note. The candidate explicitly credits this and confines its asserted contribution to the bridge from the specified regular-pentagon plane model. Its absence of a first-priority claim is appropriate. This family does not establish a literature-wide novelty claim or verify the separate geometric bridge.

Optional editorial precision only: candidate line94 groups “local conditions” with the question's remarks. The four actual Q17 remarks explicitly concern infinity torsion, Sha/twist motivation, pencil interpretation and nonregular/star variants. Local conditions arise implicitly through the Sha motivation, rather than being a separately stated Q17 remark. The candidate's scope exclusions are mathematically clear, so this does not constitute a mandatory correction or mathematical failure.

## Evidence, replay, failures and remaining gap

Each direct retrieval has its own `native/<label>/run.json`, with actual argv, UTC start/end and exit code, plus raw `stdout.bin`, `stderr.txt`, and `http_headers.txt`. Eight retrievals were performed; all exited0 and returned the expected source/document. There were no failed direct source requests. `native_retrieve.py` is the independently written harness. Replaying a download requires a fresh label, e.g. `python3 native_retrieve.py fisher_replay01 https://www.dpmms.cam.ac.uk/~taf1000/papers/jemspaper.pdf`; the harness intentionally refuses to overwrite evidence.

`source_identity_hashes.json` records computed SHA256 identities only; these are not substituted for native receipts. Decisive rendered pages include `fisher_p172.png`, `fisher_p179.png`, `fisher_p194.png`, `verdure-10.png` through `verdure-14.png`, `morton_v4_p5.png`, `morton_v1_p3.png`, `morton_v1_p4.png`, and the MIT page images. Raw sources remain available for independent rereading. The original AIM PDF was the separately retrieved parent evidence at `evidence/source/qptsurface2.pdf`; this family extracted/rendered pp.1–2 and51 but did not perform an additional AIM HTTP request.

The independent check initially guessed an extra factor5 in the Fisher derivative numerator. That own exploratory error failed visibly, was corrected, and its stdout/stderr remain in `arithmetic_failed01_*`. Current `arithmetic_stdout.json` shows eleven passes and `arithmetic_stderr.txt` is empty. No candidate script was executed. The original published large resolvent polynomial identities were read in the proof, not reconstructed term-by-term by this family; source theorem/proof use is explicitly distinguished from independent arithmetic-substitution replay.

Strongest verified result: the manuscript's cited modular, Kummer, specialization, division-kernel and pairing inputs support the exact uses made of them, with correct signs, version chronology and pinpoints. Remaining gap within this assigned source/arithmetic family: none identified. The pentagon geometry and package reproducibility remain separate review responsibilities.
