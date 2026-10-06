# Historical Alexander priority audit: PR124 / AMR-103-0231

Audit date: 2026-10-06 UTC. Scope: historical Alexander modules, covering homology, elementary divisors, and realization interfaces. This is a source/priority audit, not a new central-proof turn. Independent findings were checkpointed at 19:56:46 UTC before receiving any other current priority family's mathematical findings.

## Verdict

**FORMAL PRIOR CONSEQUENCE VERIFIED; EXPLICIT PRIOR REFUTATION NOT LOCATED.** The same mod-p torsion-rank obstruction follows directly from a published construction in Turaev's 1986 proof, with an elementary determinant-rank deduction. This is substantially stronger prior evidence than citing the rank lemma alone. It does not establish that an earlier author explicitly refuted Ohtsuki--Turaev Conjecture 12.26 or published the candidate family. The strongest verified historical interface in this audit is dated 1986; this is not an earliest claim.

Three priority levels must be kept separate: (A) the published integral square-interface and a formal determinant deduction are verified here; (B) no earlier explicitly stated modular necessary-condition theorem has been verified in this family; (C) no explicit earlier Conjecture 12.26 refutation has been located. The parent's later lead to modular torsion statements in Truman and Turaev's 2002 book is not counted as verified evidence in this independent historical report.

The remaining potentially new contribution is the explicit application to the literal prescribed-pair conjecture and the displayed counterexample family. Its novelty is **unestablished**. The new cut-surface proof may be an independent exposition of the needed interface, but the necessary determinant/specialization mechanism already appears in a published proof.

## Exact interface and formal deduction

The decisive primary source is V. G. Turaev, [*Reidemeister torsion in knot theory*](https://webhomes.maths.ed.ac.uk/~v1ranick/papers/turaev1.pdf), *Russian Mathematical Surveys* **41**(1) (1986), 119--182, [DOI 10.1070/RM1986v041n01ABEH003204](https://doi.org/10.1070/RM1986v041n01ABEH003204). Received 22 February 1985. Printed p.133, Theorem 1.6.1 **proof**, is the exact location. This is evidence in the proof, not the augmentation-only theorem statement.

For connected compact rank-one manifolds with boundary and Euler characteristic zero, that proof constructs a spine X containing a primitive circle Y and an integral Laurent square boundary matrix B for the relative complex. It identifies det B with the ordinary Alexander polynomial and B(1) with the integral relative boundary matrix. For closed orientable rank-one M, the same page drills a primitive knot to obtain V and explicitly identifies H1(V) with H1(M) and Delta(V) with Delta(M). Definitions and dependencies were checked at printed pp.126--128 and pp.131--132. There is no cyclic-torsion hypothesis.

The precise deduction from this published interface is:

1. The integral relative sequence gives coker B(1) = H1(V; Z)/<[Y]>.
2. Write H1(V; Z) = Z direct-sum T and [Y] = (1,a). The map (n,b) -> b - n a identifies the quotient with T. Thus coker B(1) = T, including its isomorphism type.
3. If r_p = dim_Fp(T tensor Fp), then B(1) mod p has corank r_p. Constant invertible row/column operations make its last r_p rows zero at 1; their Laurent entries are divisible by t-1. Hence

   (t-1)^r_p divides det B mod p = unit times Delta_M mod p.

This yields exactly ord_1(Delta_M mod p) >= r_p. A zero reduced determinant causes no exception; its order is infinite. Laurent units and reversing the deck generator preserve the order. No refined finite-group variable or primitive-content normalization enters the interface.

The authenticated candidate already supplies

H_p = Z direct-sum (Z/p)^3,
Delta_p = t + (p^3-2) + t^-1,
t Delta_p = (t-1)^2 + p^3 t.

Therefore the candidate violates this formal historical corollary: its reduced order is 2 and r_p = 3. This deduction is a full negative resolution of the candidate realization claim under the literal target. It is not evidence of earlier explicit recognition of that application.

## Other historical families and their exact gaps

- **Milnor 1968:** John W. Milnor, [*Infinite cyclic coverings*](https://webhomes.maths.ed.ac.uk/~v1ranick/papers/milncycl.pdf), in J. G. Hocking (ed.), *Conference on the Topology of Manifolds* (Michigan State University, 1967), Prindle, Weber & Schmidt, Boston (1968), 115--133. Printed pp.116--120 inspected in pixels. Assertion 4 identifies a field-coefficient order with a characteristic polynomial; pp.118--119 give the covering exact sequence and its tensor/Tor formulation. These are historical ingredients. The missing interface, if one cites these statements alone, is equality of the full integral polynomial reduced modulo p with the field order when finite integral torsion is retained. Rational coefficients erase precisely the relevant p-torsion. No prescribed-pair refutation was located there.
- **Blanchfield 1957:** R. C. Blanchfield, [*Intersection theory of manifolds with operators with applications to knot theory*](https://www.maths.ed.ac.uk/~v1ranick/papers/blanch2.pdf), *Annals of Mathematics* (2) **65**(2) (March 1957), 340--356, [DOI 10.2307/1969966](https://doi.org/10.2307/1969966). Received 29 March 1956. Printed pp.354--356 inspected in pixels; Section 4's determinant-divisor definition was read in text. Theorem 5.5 and Corollary 5.6 supply symmetry of principal determinant divisors for the maximal free-abelian cover. That condition does not separate the candidate, which is already reciprocal. No exact mod-p torsion-rank inequality or full prescribed-pair realization/refutation was verified from this source.
- **Turaev 1975:** [*The Alexander polynomial of a three-dimensional manifold*](https://www.mathnet.ru/php/archive.phtml?jrnid=sm&option_lang=eng&paperid=3655&wshow=paper), *Math. USSR-Sbornik* **26**(3) (1975), 313--329, [DOI 10.1070/SM1975v026n03ABEH002483](https://doi.org/10.1070/SM1975v026n03ABEH002483); Russian original *Mat. Sb.* **97**(139), 341--359. Received 1 July 1974. Primary extracted text of Theorem A at printed p.314 was obtained once: closed orientable cyclic reduced torsion equals the reduced polynomial divided by (t-1)^2. Turaev 1986 p.127 attributes the closed formula to this paper, reference [44]. Local downloads returned HTML and later page/pixel requests timed out. Accordingly this audit does **not** promote an exact 1975 integral-specialization construction or a 1975 date for the entire obstruction.
- **Realization scope:** The 1986 printed p.141 Remark 2, inspected in pixels, realizes reciprocal rank-one polynomials with nonzero augmentation while prescribing the rank, not the finite torsion group's isomorphism type. It therefore cannot establish sufficiency of Conjecture 12.26. The three-component link-module realization statement at printed p.171 (Theorem 5.6.1) was read in text, but was not used as a target-subsuming theorem.
- **Unclosed elementary-ideal lead:** Turaev, *Elementary ideals of links and manifolds: symmetry and asymmetry*, *Algebra i Analiz* **1**(5) (1989), 223--232; English translation *Leningrad Math. J.* **1**(5) (1990), 1279--1287, [primary record](https://www.mathnet.ru/php/archive.phtml?jrnid=aa&option_lang=eng&paperid=49&wshow=paper). Received 1 March 1989. Bibliography verified; full relevant pages were inaccessible. No substantive theorem claim from this paper is counted. The 1976 *Reidemeister torsion and the Alexander polynomial* lead likewise remains unclosed; bibliographic DOI is 10.1070/SM1976v030n02ABEH002269.

## Target and search limitations

Ohtsuki (ed.), [*Problems on invariants of knots and 3-manifolds*](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf), *Geometry & Topology Monographs* **4** (2002), printed p.542 / PDF p.170, was inspected in pixels. Conjecture 12.26 prescribes the rank-one integral group and the ordinary polynomial over its torsion-free quotient. The remark records torsion-free and cyclic finite-torsion cases. These are compatible with the obstruction and do not cover the candidate.

Exact-number, title, torsion-rank, finite-field, vanishing-order, and historical citation searches are recorded in QUERY_LOG.json. No primary source explicitly giving this candidate or expressly refuting this target was located in this bounded audit. Inaccessible sources and finite search coverage prevent an absence-of-prior-art or novelty certification. Outside input could reduce the residual historical gap, but no outreach was prepared or initiated.

## Controls and completion

All writes are confined to this audit directory. Downloaded PDFs, extracted source text, HTML failures, and rendered pages reside only under ignored private_sources/. Public files contain audit conclusions, bibliographic provenance, search controls, and logs; no source PDF is released. No repository branch/index, PR, tracked global/native document, service publication, commit, push, or external communication was changed. The source-browser navigation attempt timed out and supplied no evidence.

Scoped audit completion: 100% as a bounded, sealed report. Mathematical priority/novelty certification remains incomplete. SHA256SUMS.json records path, byte count, and SHA-256 for every public file except itself and excludes private_sources/.
