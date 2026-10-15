# Independent priority audit: literal Ohtsuki–Turaev Conjecture 12.26

**Disposition: priority unestablished; confirmed old proof mechanisms and a material unread source.** This audit does not certify a first resolution, or certify that the conjecture remained open in October 2026. The submitted counterexample may be described as an explicit negative answer to the literal printed conjecture, conditional here on the separate mathematical verification supplied by the parent. Its novelty requires further source resolution.

This is a literature and source audit, not a fresh proof search. The audited target is PR124 / numeric10400231. The parent supplied a mathematical/source PASS timestamp of 2026-10-06T19:54:21Z. No other current priority family was consulted before the independent checkpoint at 19:57:14Z. Later parent messages about Turaev 1986 and book-access gaps are identified as corroboration, not substituted for source reading. All new files are confined to this dedicated directory; no external contact or publication action occurred.

The precise target and historical status

[Ohtsuki, official collection](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf), printed p.542 / PDF p.170, prescribes the entire finitely generated rank-one group H. The ordinary polynomial is in Z[H/Tors H]. Its two proposed conditions are reciprocal symmetry with even exponent and augmentation ±|Tors H|. The adjacent remark establishes H=Z and H=Z⊕Z/n for n>=2. The nominal volume is 4 (2002); the article itself records publication on 1 June 2004. [Publisher metadata](https://msp.org/gtm/2002/04/p024.xhtml) identifies DOI 10.2140/gtm.2002.4.377 and pp.377–572.

The candidate prescribes H=Z⊕(Z/p)^3 and Δ=t+(p³−2)+t⁻¹. It satisfies the printed two conditions. The supplied necessary condition ord_(t=1)(Δ mod p)>=dim_Fp(T⊗Fp) gives 2>=3, which fails. This assessment uses the parent's established genuine integral square presentation and full coker A(1)=T; an arbitrary rational or localized presentation would not support this conclusion.

Turaev's own [2002 book back matter](https://link.springer.com/content/pdf/bbm:978-3-0348-7999-6/1), printed p.187, Open Problem 5 asks for refined-torsion realization from VIII.5.1 and an analogous Alexander-polynomial realization problem. This independently authenticates a historical realization problem, without establishing all of the later conjecture's exact hypotheses. It is not evidence of current open status. Open Problem 3 asks for the boundary extension of Chapter III, consistent with Truman's later boundary work.

The [editor's public solved-problem page](https://www.kurims.kyoto-u.ac.jp/~tomotada/solution.html), reached from the update site named in the original preface, lists other problems and no entry for 12.26. It supplies neither a completeness guarantee nor a usable current-status date. An omitted entry cannot certify that 12.26 is still open.

What the directly read antecedents establish

| Primary text and exact relevant location | Authenticated content | Priority implication |
|---|---|---|
| [Turaev 1986, Reidemeister torsion in knot theory](https://webhomes.maths.ed.ac.uk/~v1ranick/papers/turaev1.pdf), Russian Math. Surveys 41:1,119–182, Theorem 1.6.1 proof p.133 | Boundary rank-one proof uses an integral square relative matrix B(t), determinant ordinary Δ, with B(1) the relative integral boundary. A primitive circle gives the full relative torsion group. The closed case uses a primitive knot exterior preserving H1 and Δ. | The core integral square-presentation mechanism and full-group specialization predate the candidate by decades. |
| Same source, Remark2, pp.140–141 | Polynomial realization with prescribed first Betti number and rank-one nonzero augmentation. | Does not prescribe an arbitrary full finite torsion group. |
| [Nicolaescu author notes](https://www3.nd.edu/~lnicolae/Torsion.pdf), title Notes on the Reidemeister Torsion, January 2002, Theorem 2.39 proof, pp.69–70 | Rank-one Alexander augmentation formula proved by a square relative boundary complex after choosing a primitive circle; its integral specialization presents relative H1. Closed case reduces to a knot exterior. | Independent early exposition of the same mechanism; no explicit conjecture refutation was found in the relevant text. |
| [Turaev 2002 survey](https://arxiv.org/pdf/math/0211084), GT Monographs 4,295–302, realization paragraph p.301 | An already realizable refined-torsion pair (H,τ) remains realizable after multiplication by symmetric augmentation-one λ in Z[H]. | Conditional refined-torsion multiplication is not arbitrary ordinary-polynomial realization for a prescribed H. This eight-page survey is not the Birkhäuser book. |
| [Alcaraz 2014](https://arxiv.org/pdf/1406.2042), pp.2,6–10,15–17 | Rank-one polynomial characterization prescribes b1. Section 4.3 displays an integral square presentation including constant torsion relations; Section 4.4 Lemma 3 discusses specialization at one and full torsion order. | Clear immediate antecedent. The publication cannot claim invention of this presentation method. No exact full-H negative answer was located in the read sections. |
| [Truman 2006](https://arxiv.org/abs/math/0611210v1), p.14 and Theorem 3.3 pp.20–21 | Boundary modular augmentation-power theorem; explicit b1=1 polynomial-part extension; old-book attribution. | Potentially decisive prior modular obstruction. Exact hypotheses and access limitations are authenticated in TRUMAN_SOURCE_NOTE.md. |
| [Massuyeau2009 author text](https://massuyea.perso.math.cnrs.fr/papers/torsion_FTI.pdf), §4.2.2 p.28 and §5.1.2 p.32 | Closed b1=1 polynomial part in Z[H]; for zero-Chern-class Euler structure, ordinary Δ=|T|−pr([τ])(t−1)(t⁻¹−1). | Supplies a precise ordinary/refined bridge; does not independently supply the missing modular closed-manifold filtration theorem. |
| [Suciu, arXiv1901.01419](https://arxiv.org/pdf/1901.01419), §6.2 and references | Discusses ordinary Alexander polynomials and cites Alcaraz's Betti-number realization; refers to Turaev's book. | Citation follow-up, not proof that arbitrary noncyclic torsion is realizable or that the conjecture was resolved. |

Alcaraz's displayed block form is recorded as an antecedent, without certifying its full torsion analysis; the confirmed standard mechanism comes from the earlier sources.

The old integral presentation plus the elementary determinant/nullity argument immediately yields the candidate's obstruction once the full coker B(1) is retained. That bridge is a deduction in this audit, not a quotation of a previously printed named criterion. The 1986 theorem therefore defeats any assertion that the integral mechanism is new. It does not, by itself, authenticate a previously explicit published negative resolution of Conjecture 12.26. A new explicit application of old standard mathematics is logically possible, but this audit has not established its novelty or mathematical significance.

Alcaraz's multiplication construction changes augmentation through a surgery coefficient; its statements guarantee b1, not a fixed torsion decomposition. For example, a cyclic group of order p³ is a different target from (Z/p)^3. The ordinary Δ discards finite-group variables, whereas refined τ and its polynomial part retain them. Consequently neither a refined-torsion realization theorem nor a polynomial-only characterization answers the original full-group question without an additional verified bridge.

The material full-text gap

The publisher's [complete free front matter](https://link.springer.com/content/pdf/bfm:978-3-0348-7999-6/1.pdf) authenticates the detailed contents. Required unread material is:

- II.3, pp.22–23: rank-one polynomial-part definition and normalization.
- II.4, pp.23–26: exact II.4.4 modular augmentation-power assertion and boundary hypotheses.
- II.5, pp.27–30: ordinary-polynomial relation, including rank-one normalization.
- III.4, pp.45–51: complete Theorem III.4.3 and its last proof paragraph, including closed rank-one polynomial part, modular rank, admissible r, prime 2, and precise augmentation exponent.
- VIII.5, pp.114–118: exact full realization problem and theorem hypotheses; compare full H, refined τ, and the ordinary quotient polynomial.

The full book and chapters II/III were requested directly from the publisher. They returned HTML subscription pages, not PDFs. Only front/back matter and two-page chapter previews were accessible; the previews do not contain the central statements. Chapter abstracts have not been promoted to hypothesis verification.

Truman's explicit attribution makes the unread modular statement a concrete priority risk, not a hypothetical gap. In the candidate group, modular rank is four even though integral b1 is one. A suitable old closed polynomial-part filtration, combined with Massuyeau's displayed ordinary/refined relation, could rule out the same candidate through a constant-term contradiction. The exact closed filtration and its hypotheses must be read before asserting this bridge as authenticated prior literature.

Further unresolved full texts are Alcaraz's Oxford thesis cited by the 2014 paper, and Turaev's 1975 original Alexander-polynomial paper. Direct repository/search requests for the thesis and MathNet full text returned HTTP403. Neither missing text is treated as silently clear. Obtaining a lawful full copy would help, but no outreach was prepared or initiated.

Search result and permissible wording

SEARCH_LOG.md records the actual targeted queries and follow-ups; SOURCE_PROVENANCE.json records successful and unsuccessful full-text requests. The bounded search followed exact-conjecture queries, prescribed homology/torsion queries, modular leading-term citations, and primary realization sources. It found no directly read text explicitly giving this exact negative answer or the same noncyclic counterfamily. This is a limitation of the search, not proof of absence.

Defensible present wording is: “An explicit counterexample to the literal Conjecture 12.26 follows from standard integral Alexander presentations and a modular rank obstruction; priority is not yet established.” Do not claim “first,” “previously unresolved as of 2026,” a new square-presentation theorem, or a full classification of realizable pairs. A future discovery of the book's exact modular antecedent may require reducing the contribution to an explicit observation or reformulation.

The bounded audit is complete; estimate 100% of assigned search/report work and 60% of a decisive priority determination. The remaining uncertainty is bibliographic/source access, not a defect asserted in the separately verified candidate proof. The public seal excludes private PDFs, extracted text, renders, and the manifest itself. Public files are stable after seal.
