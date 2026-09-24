# Priority update after reading the three supplied papers

Date: 24 September 2026 UTC (23 September in America/Los_Angeles).

**Result:** three specific full-text gaps are now closed. None of the supplied
papers explicitly answers FMU (1998), Question 3(e), or presents the round
cylinder as its counterexample. Their actual theorem statements do not invalidate
the proof. They do confirm that its main ingredients, including the exact
non-self-dual deformation, were already established. Historical priority of the
assembled answer remains unconfirmed.

This updates the [23 September audit](priority_followup.md). The original paper
and version 1.0.0 archives remain unchanged historical snapshots. Current
attribution and coverage are recorded here and on the website.

## The supplied sources

| Source | Coverage and substantive finding |
| --- | --- |
| Matsuzoe (1999), *Geometry of contrast functions and conformal geometry*, [DOI](https://doi.org/10.32917/hmj/1206125160) | Complete text and all 18 PDF pages inspected (17 article pages and one blank). Equation (2.1), p.178, with its accompanying metric change, gives exactly the candidate's deformation as a standard statistical (-1)-conformal change. Sections 2.1–2.2 supply the established projective/dual-projective curvature obstructions. The Bartlett-tensor characterizations require additional conditions, not merely radial integrability. [Detailed review](priority_supplied_matsuzoe1999.md). |
| Matsuzoe (2010), *Statistical manifolds and affine differential geometry*, [DOI](https://doi.org/10.2969/aspm/05710303) | All 19 pages read; nine key pages visually inspected. Section 3.2.4, p.309, confirms the exact transformation conventions. Equation (10), p.311, is the Gauss-form curvature identity excluded by the cylinder. The affine realization and broader conformal-projective results do not deduce 1-conformal flatness from the question's radial premise. [Detailed review](priority_supplied_matsuzoe2010.md). |
| Kurose (2024; online 2023), *A certain ODE-system defining the geometric divergence*, [DOI](https://doi.org/10.1007/s41884-023-00110-3) | Complete 14-page paper read; relevant displayed definitions and equations visually checked. Definition 2, p.S544, confirms the same curvature obstruction. Proposition 7 concerns a transported covector; Corollary 8 adds 1-conformal flatness to obtain orthogonality to divergence level sets. Theorem 9 and Corollary 10 construct general contrast functions without asserting that missing identification in general. [Detailed review](priority_supplied_kurose2024.md). |

File identities, hashes, page counts, and inspection scope are preserved in the
[supplied-source manifest](../research/priority_evidence/supplied_papers.json).
The publisher PDFs remain local research sources and are not redistributed.
Each paper was assigned an independent reader; the main reviewer also checked
the important transformation formulas and Kurose's ODE argument.

## Why the newer general construction does not settle this question

Kurose's ODE constructs a scalar function and a covector along each selected
geodesic. On a general statistical manifold, the endpoint covector need not be
the differential of the resulting endpoint function. Proposition 7 gives
orthogonality for the covector. Proposition 5 and Corollary 8 identify it with
the relevant differential when 1-conformal flatness is already assumed.
Thus these statements establish the known sufficient direction, not the
converse in Question 3(e).

The [Kurose review](priority_supplied_kurose2024.md) includes an explicit
specialization of his ODE to our cylinder that exhibits this distinction.
The formulas were independently derived by two reviewers and checked by exact
symbolic differentiation. This is an application made in this audit, not an
example claimed to appear in Kurose's paper or an allegation of an error there.

## Consequence for attribution and priority

Matsuzoe (1999) supplies a directly inspected older citation for the deformation
than the Ueno (2025) discussion cited in our initial note. The original note
already disclaims novelty for the construction; the website now makes the
earlier source explicit. No novelty should be claimed for the Gauss lemma,
the curvature criterion, or the deformation law. Combining those established
facts gives the counterexample; the claimed contribution is the explicit
application to the printed question and its short verification.

The principal remaining source gaps are:

- **Kurose (1999),** *1-conformally flat statistical manifolds and their
  realization in affine space*, Fukuoka University Science Reports 29.
  The earlier author record gives pp.209–219; Kurose's supplied 2024 reference
  [7] instead prints pp.201–219. This pagination discrepancy is recorded for
  retrieval, not silently resolved without the original. No DOI has been located.
- **Binder–Simon (2000),** the problems/bibliography chapter,
  [DOI 10.1142/9789812792051_0001](https://doi.org/10.1142/9789812792051_0001).
  The user also could not obtain it. The accessible 2002 continuation does not
  substitute for it.
- **The actual notes or content of Kurose's 2016 Gauss-lemma/Hessian-structure
  talk.** The program and grant reports do not reveal the complete argument.

Narrower gaps from the previous citation audit, including the full 2008
tangent-bundle paper and uninspected bibliography records, remain. Matsuzoe
1999 cites a private letter for certain curvature facts; that unseen letter
cannot be checked for additional observations. No communication or outreach
was prepared or initiated.

**Disposition:** no direct prior-resolution conflict found in these three
complete papers; no proof revision required; stronger attribution to old
machinery; historical priority still unproved. These conclusions close named
source gaps, not all possible literature or unpublished-work gaps.
