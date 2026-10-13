# Public sources and inspection limits

This record accompanies the first edition of problem 8800049 / AMR-087-0049, dated 13 October 2026. It identifies the public sources supporting the accepted proof and the bounded comparison with nearby work. The accompanying [metadata](PUBLIC_SOURCE_METADATA.json) records PDF byte counts, SHA256 values, version notes, and source inspection scope. No source PDF or extracted source text is reproduced in the edition.

A retained complete PDF is not a claim that its entire proof was independently audited. Source availability checks establish that a link was tested; they do not verify the mathematics. The exact inspection scopes below and in the metadata take precedence over any informal shorthand such as “source checked.”

## Original question

Everett W. Howe's [Low-genus curves over finite fields: Problems and variations](https://ewhowe.com/talks/IPAM.pdf) was presented at IPAM in October 2006. PDF pages 37–38 ask for the connection between Deligne modules and either recognition approach for an ordinary absolutely simple threefold class given by its Weil polynomial; pages 29–36 give the descent and representation context. The repeated pages are animation duplicates. The source imposes no odd-characteristic restriction or complexity bound.

The author PDF and [IPAM copy](https://helper.ipam.ucla.edu/publications/SCWS1/SCWS1_6237.pdf) have different byte identities but matching complete whitespace-normalized extracted text. The IPAM copy's 2026 accessibility remediation does not redetermine the date of the mathematics. The relevant target and context pages were inspected; a new reading of every slide is not claimed.

## Dependencies of the accepted theorem

- Stefano Marseglia, [Computing square-free polarized abelian varieties over finite fields](https://arxiv.org/abs/1805.10223v3), Math. Comp. 90 (2021), 953–971. The exact count uses the square-free ordinary equivalence, conjugate trace dual, fixed CM type, positivity convention, and polarized unit action. Relevant theorem and algorithm portions were inspected, with the bars and sign in Theorem 5.4 visually checked.
- Stefano Marseglia, [Computing the ideal class monoid of an order](https://arxiv.org/abs/1805.09671v3), J. London Math. Soc. 101 (2020), 984–1007. Theorem 4.6, Proposition 5.1, Remark 3.8, and the ideal-isomorphism statements provide arbitrary-order enumeration and arithmetic. No Bass assumption is introduced.
- H. W. Lenstra, Jr., [Algorithms in algebraic number theory](https://arxiv.org/abs/math/9204234v1), Bull. Amer. Math. Soc. 26 (1992), 211–244. Theorem 5.4 and the following construction, PDF pages 23–24, give the unconditional units/class-group dependency. The separate tentative complexity discussion is not used.
- Arnaud Beauville and Christophe Ritzenthaler, [Jacobians among abelian threefolds: a geometric approach](https://arxiv.org/abs/1005.3683v1), Math. Ann. 350 (2011), 793–799. The complete seven-page text was read. Propositions 2.1, 2.4, 3.1 and Theorem 3.4 are central; the Clifford discussion and Proposition 3.5 support optional arithmetic variants. The retained PDF's internal September 2018 date is distinct from its arXiv v1 submission in May 2010. [Exact PDF](https://arxiv.org/pdf/1005.3683v1)
- Gregory G. Smith, [Computing Global Extension Modules for Coherent Sheaves on a Projective Scheme](https://arxiv.org/abs/math/9807170v1), J. Symbolic Comput. 29 (2000), 729–746. The introduction, Theorem 1, and Section 3 algorithms were inspected for exact global-section computations over arbitrary fields. [Exact PDF](https://arxiv.org/pdf/math/9807170v1)
- J. S. Milne, [Abelian Varieties course notes](https://www.jmilne.org/math/CourseNotes/AV110.pdf), version 1.1, 27 July 1998. Relevant portions of Sections 5–6 and 9–10 were inspected for very ampleness, torsion, and polarization/cohomology facts. The complete notes were retained but not independently audited in full.
- J. S. Milne, [Abelian Varieties](https://www.jmilne.org/math/articles/1986b.pdf), in Arithmetic Geometry (1986), Section 13. The relevant author-hosted extracted passages for Remark 13.2 and Theorem 13.3 were inspected. A complete local PDF was not retained in the supporting source work; this edition does not assert a full-text reading.
- Bjorn Poonen, [Rational Points on Varieties](https://math.mit.edu/~poonen/papers/Qpoints.pdf), Theorem 7.7.1 and proof, printed pages 222–223, PDF pages 236–237. These portions supply the inspected Lang–Weil estimate used in the termination argument; the complete book was not read in full. The original Lang–Weil paper, [Number of Points of Varieties in Finite Fields](https://doi.org/10.2307/2372655), was located bibliographically but its full text was not inspected.
- [Stacks Project, tag 023R](https://stacks.math.columbia.edu/tag/023R), fpqc descent of quasi-coherent sheaves. Public text was inspected for the descent formalism. The proof makes the invariant-section computation explicit.
- Everett W. Howe, [Kernels of polarizations of abelian varieties over finite fields](https://arxiv.org/abs/2001.05111v2), J. Algebraic Geom. 5 (1996), 583–608, Theorem 1.2. Its introduction and theorem statement were inspected for principal polarizability in simple odd dimension. The January 2020 arXiv copy reproduces the August 1995 preprint. This is context, not a realization oracle.

The Deligne classification and Honda–Tate interpretation are credited established inputs. Deligne's 1969 original and Howe's separate 1995 original were not fully inspected; the module interface was checked in the later primary expositions. The theorem is relative to the identified established results, not a reproof of their complete dependency chains.

## Nearby literature and the remaining question

The following sources informed the bounded scope comparison; they are not additional prerequisites of the counted-model proof.

- Meagher's [arXiv:0711.0415v4](https://arxiv.org/abs/0711.0415v4) has landing-page title Twists of genus three Jacobians and PDF title Torelli Revisited. The definitions and Theorems 2–4 on pages 1–3 were inspected. The base inverts 2, and its analytic reduction formula needs the specified lift and normalization data.
- [Lachaud–Ritzenthaler–Zykin](https://arxiv.org/abs/0802.4017v1), Jacobians among Abelian threefolds: a formula of Klein and a question of Serre, was inspected at pages 12–14 for its complex-field theorem and sign convention. It is not used as an unrestricted finite-field realization procedure.
- Ritzenthaler's [published 2010 article](https://doi.org/10.1112/S1461157009000576), Explicit computations of Serre's obstruction for genus-3 curves and application to optimal curves, was inspected at pages 192–197 for the odd-characteristic normalization and lifting hypotheses.
- [Kirschmer–Narbonne–Ritzenthaler–Robert](https://arxiv.org/abs/2004.08315v2), published as Spanning the isogeny class of a power of an elliptic curve, treats powers of an ordinary elliptic curve with stated technical hypotheses. The inspected introduction and algorithm restrictions do not cover an absolutely simple threefold class.
- [Lercier–Ritzenthaler](https://arxiv.org/abs/1907.07431v3), Siegel modular forms of degree three and invariants of ternary quartics, provides a modular-form/invariant dictionary; the introduction and Section 4 characteristic restrictions were inspected.
- [Costa–Dupuy–Marseglia–Roe–Vincent](https://arxiv.org/abs/2601.20979v1), Ordinary abelian varieties: isogeny graphs and polarizations, was inspected for its stated isogeny and polarization outputs; no complete Jacobian-recognition claim was verified in this bounded inspection.
- [Rybakov, arXiv:2608.16668v4](https://arxiv.org/abs/2608.16668v4), was inspected at its introduction and main theorem statements and searched for recognition scope. Its broader categorical description was not treated as a certified theta-construction algorithm.
- Howe's [Deducing information about curves over finite fields from their Weil polynomials](https://arxiv.org/abs/2110.04221v3), subsequently a 2023 chapter, was inspected at the introduction and principal-polarization discussion for context.

No worldwide novelty or openness conclusion follows from this finite selection. The accepted aggregate theorem leaves a direct marked-ideal-to-model construction, a useful direct obstruction criterion, and practical computation unresolved here.

## Source link availability

All 40 distinct public-source URLs recorded in this edition were reachable in read-only HTTP checks on 13 October 2026. The metadata records the observed status and resolved destination. This checks availability only; it does not extend the stated content-inspection scope or establish source validity.
Recorded PDF hashes refer to the retained inspected bytes. Availability checks do not compare live full-file contents against those hashes.
