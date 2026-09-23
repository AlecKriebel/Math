# Independent priority audit

Audit checkpoint: 2026-09-23 04:09 UTC (2026-09-22 in America/Los_Angeles).
Auditor: independent research subagent; no external communication was initiated.
Completion estimate: 100% of the bounded public-literature audit described below;
this is **not** a percentage probability that mathematical priority is established.

## Claim and verdict

The claim audited is that every real positive-definite homogeneous polynomial
of positive degree admits an invertible real linear change of variables whose
**symmetric ordered-tuple coefficients** satisfy

\[
|A(x_{j_1},\ldots,x_{j_d})|
\leq \prod_{r=1}^{d}p(x_{j_r})^{1/d}.
\]

The candidate obtains this by clustering a basis near a direction minimizing
the polynomial on an auxiliary Euclidean sphere, then using the positive
transverse second variation of the normalized polarization.

**Verdict: no prior full resolution or equivalent general basis theorem was
identified in this bounded audit.** The 2015 precursor and the 2019 problem
must be cited. The search is clean in the limited sense of finding no priority
obstruction; it does not prove novelty or rule out unpublished, poorly indexed,
non-English, or differently formulated antecedents. Suitable public language
is: “We give an affirmative answer to Brandes's question in Problem 11 of the
2019 Oberwolfach report.” Avoid “first proof,” “priority established,” or
“independently confirmed by the mathematical community.”

## Original problem and direct precursor

1. **Primary statement.** *Analytic Number Theory*, Oberwolfach Report 50/2019,
   workshop 3–9 November 2019, DOI
   [10.4171/OWR/2019/50](https://doi.org/10.4171/OWR/2019/50).
   [Publisher PDF](https://ems.press/content/serial-article-files/46829),
   printed p. 3182, Problem 11 (PDF page 42, zero-based index 41).
   The printed inequality has absolute values. It asks for a linear change of
   variables, without an orthogonality, determinant, integrality, or conditioning
   restriction. The report's title is *Analytic Number Theory*.
   The supplied unsolvedmath URL could not be fetched by the web reader; the
   primary report is the source used here.

2. **Direct antecedent.** Julia Brandes, *Forms representing forms: the definite
   case*, J. London Math. Soc. 92 (2015), 393–410, DOI
   [10.1112/jlms/jdv028](https://doi.org/10.1112/jlms/jdv028),
   [arXiv:1506.05343v2](https://arxiv.org/abs/1506.05343),
   revised 14 August 2015. The introduction discusses a coefficient condition
   under the name “pseudo-diagonal”; Lemma 2.1 proves the quadratic case.
   This is an essential conceptual precursor, not a located proof of the
   general basis-existence theorem. The paper's unordered index convention
   and combinatorial factors require care before importing its formulas.
   The introduction also asserts invariance under linear changes; this must
   not be treated as a general resolution of the 2019 question.
   [Full-text PDF](https://arxiv.org/pdf/1506.05343).

There is a checkable reason to avoid using that invariance sentence for the
ordered-tensor condition. Let
\(p(x,y)=x^4+12x^2y^2+y^4\). In the standard basis its symmetric tensor entry
\(A(e_1,e_1,e_2,e_2)=2\), whereas both pure entries equal 1, so the condition
fails. Under \((x,y)=(u+v,u-v)\), the form is
\(14u^4-12u^2v^2+14v^4\). Its only nonzero mixed symmetric entry equals
\(-2\), whose absolute value is at most 14. Thus the ordered-tensor condition
is not invariant under arbitrary real changes of coordinates. This observation
is an independent elementary calculation, not a claim about the validity of
the analytic number theory results in the 2015 paper.

## Further primary-source checks

| Source or family | What was checked | Overlap assessment |
| --- | --- | --- |
| [Brandes's institutional publication list](https://research.chalmers.se/en/person/brjulia) and indexed [CV](https://www.math.chalmers.se/~brjulia/cv.pdf) | Titles, available abstracts and the identified form-representation papers | No title or abstract advertising a solution of the normalization question. The institutional list is not a complete record through 2026. |
| [Brandes, *On the number of linear spaces on hypersurfaces with a prescribed discriminant*](https://research.chalmers.se/publication/504331/file/504331_Fulltext.pdf), 2018 | Abstract, search within full text, and reference to the 2015 paper | Counting spaces with prescribed discriminant; no occurrence of “pseudo” in extracted text and no identified normalization theorem. |
| [Brandes–Dietmann–Leep, *Rational lines on cubic hypersurfaces II*](https://arxiv.org/abs/2307.09449), revised November 2025 | Primary arXiv abstract and version history | Rational lines and dimension bounds for cubic hypersurfaces; no claim resolving positive-definite even-degree coefficient normalization. |
| [Brandes–Wooley, *Structure and paucity in affine diagonal systems, I*](https://arxiv.org/abs/2602.02911), February 2026 | Primary arXiv abstract and version history | Counting solutions of affine diagonal systems; no normalization theorem in the stated results. |
| [Oberwolfach Report 51/2025, *Analytic Number Theory*](https://publications.mfo.de/bitstream/handle/mfo/4400/OWR_2025_51.pdf?isAllowed=y&sequence=1) | Contents, relevant text searches, and indexed Brandes problem-session entries | No located update to the 2019 coefficient question. This report is not a complete status registry. |
| [Carando–Rodríguez, *Symmetric multilinear forms on Hilbert spaces: where do they attain their norm?*](https://arxiv.org/abs/1810.09373), 2018 preprint / 2019 journal | Introduction, Theorem 1.1, and norm-attainment discussion | Studies a fixed Hilbert norm and the geometry of its maximizing tuples. It does not supply the requested basis with denominator built from the form itself. |
| [Harris, *Bernstein's Polynomial Inequalities and Functional Analysis*](https://www.ms.uky.edu/~larry/paper.dir/irish.pdf) | Introduction and the statements surrounding the Banach norm identity | Classical diagonal norm attainment bounds polarization by a global Hilbert-sphere maximum. The candidate requires a local, point-dependent product bound near a sphere minimum; these are different conclusions. |

The Banach identity is an important neighboring classical fact: the norm of a
symmetric multilinear form on a Hilbert space equals the supremum of its
diagonal polynomial on that sphere. Its bibliographic source is S. Banach,
*Über homogene Polynome in (L²)*, Studia Math. 7 (1938), 36–44, DOI
[10.4064/sm-7-1-36-44](https://doi.org/10.4064/sm-7-1-36-44).
The norm identity, by itself, does not replace the candidate's second-variation
step. In particular, \(p^{1/d}\) need not be a Hilbert norm or even a norm.

Other keyword searches covered hyperbolic/Lorentzian inequalities, positive
coefficients, and polynomial polarization. They did not locate the same basis
theorem. Hyperbolicity is a materially different hypothesis: for a positive
definite form in at least two variables, a line \(x+te\) with independent
\(x,e\) never reaches the origin, so its polynomial has no real zeros, whereas
hyperbolicity would require all roots to be real. Thus a hyperbolic-polynomial
inequality cannot simply be invoked for the class in question.

## Search record

All searches below were executed on 2026-09-22 local / 2026-09-23 UTC using the
available public web search. Quoted terms were supplied literally. This is a
compact record of the substantive queries; closely repeated variants and
irrelevant namesake results are omitted.

- `"OWR-17293-016"`
- `"Brandes" "Problem 11" "2019" Oberwolfach`
- `"positive definite" "Brandes" forms coefficients`
- `"Brandes" "Oberwolfach" "positive" "form"`
- `"Brandes" "coefficient normalization"`
- `"Brandes" "coefficient" "normalization"`
- `"Brandes" "normalisation" "forms"`
- `"Brandes" "normalization" "homogeneous"`
- `"Brandes" "coefficient" "problem" homogeneous`
- `"pseudo-diagonal" "Brandes"`
- `"pseudo-diagonal" "positive definite"`
- `"pseudo-diagonal" "homogeneous"`
- `"pseudo-diagonality"`
- `"pseudodiagonal" "forms"`
- `"Brandes" "pseudo-diagonal" site:arxiv.org`
- `"Forms representing forms" "erratum"`
- `"Forms representing forms: the definite case" -site:researchgate.net -site:wikipedia.org -site:scribd.com`
- `Julia Brandes publications research normalization`
- `"Julia Brandes" "2025" math`
- `"Julia Brandes" "2026" math`
- `"positive definite forms" "linear change" coefficients`
- `"positive definite forms" "coefficients" "basis"`
- `"positive definite" "multilinear" "basis" inequality polynomial`
- `"normalization" "positive-definite" "forms" polarization`
- `"positive definite" "polarization" "inequality" polynomial`
- `"homogeneous polynomial" "basis" "Hölder" positive`
- `"homogeneous" "polarization" "Cauchy-Schwarz" inequality`
- `"positive definite" "symmetric multilinear" "inequality"`
- `"Banach" "symmetric multilinear" "norm" theorem`
- `"positive definite" "homogeneous" "elliptic point"`
- `"homogeneous forms" "coefficient bounds" change variables`
- `"homogeneous" "form" "nearly parallel" basis`
- `"Symmetric multilinear forms on Hilbert spaces" arxiv`
- `Banach "homogene Polynome" 1938`
- `"Gårding" "An inequality for hyperbolic polynomials" 1959`

Searches produced many irrelevant namesake and terminology matches; those
were not treated as evidence. Citation searches for the 2015 paper found
later representation/counting and discrete maximal-operator papers, rather
than a located normalization solution. This was not an exhaustive forward
citation census, and no subscription MathSciNet or zbMATH full-text search
was available in this audit.

## Limits and publication recommendation

The audit distinguishes an absence of a located obstruction from a proof of
priority. Some relevant pages were inaccessible to the web reader (including
the supplied aggregator, parts of the author's personal site, and one
publisher DOI endpoint); indexed records or primary arXiv/institutional copies
were used where available. An indexed CV is a useful lead, not a current
complete bibliography. No private correspondence, unpublished workshop
discussion, or external expert confirmation was obtained.

If the separate mathematical verification passes, the audit supports preparing
and posting a concise paper that cites the 2019 question and the 2015
precursor, defines the ordered symmetric coefficient convention explicitly,
and states the affirmative theorem without a categorical first-discovery
claim. Any future evidence of an earlier equivalent result should lead to an
attribution update. A human specialist could supply additional bibliographic
context; this is recorded only as a research limitation, with no outreach
prepared or initiated.
