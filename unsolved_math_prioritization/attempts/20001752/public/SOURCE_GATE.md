# Source and scope gate

Checked 2026-10-03 (UTC).

## Recovered mathematical target

The queue label, “Midpoint projection and modular-period reductions for the
E8 and Leech magic functions,” describes a previous partial result. It is not
the original question. The original AIM item asks for the value 1/15 of the
radial Mellin transform at s=4 of the 8-dimensional magic function, including
equality with its Fourier transform, and the analogous value at s=12 in
dimension 24.

The live [problem page](https://www.unsolvedmath.com/problems/20001752)
returned HTTP 403. The authorized pinned problem record and its earlier
research record were inspected as a fallback, not treated as mathematical
authority. Its source is AIM's *Discrete geometry and automorphic forms*
problem list, item 1.28, [source location](http://aimpl.org/discreteaf/1/).
The AIM page could not be independently loaded in this run. The associated
primary research question is independently confirmed in Cohn--Miller's
Conjecture 5.3 and the following paragraph.

### Important corrections and normalization

- The primary source uses f(0)=f-hat(0)=1 and the Fourier exponential
  exp(-2 pi i x dot y). These conventions are retained throughout.
- AIM's extracted 24-dimensional decimal is 0.17786094729650....
  Cohn--Miller print 0.177860964729650276645646126241.... The primary source
  and independent quadrature agree on the latter prefix. The former is not
  silently used as an exact target.
- An ellipsis is not an exact specification of a real number. The unresolved
  24-dimensional request is interpreted as identifying/evaluating the actual
  normalized magic-function moment, rather than proving equality to an
  unspecified continuation of a finite decimal.
- The relevant positive-eigenfunction form in the 24-dimensional paper is
  equation (2.1). Equation (3.1) defines a different, negative-eigenfunction
  ingredient. This distinction is fixed in the present proof.

## Primary sources and what they establish

1. [Cohn--Miller, arXiv:1603.04759](https://arxiv.org/abs/1603.04759),
   equation (5.2), Conjecture 5.3, following paragraph (PDF page 18).
   Confirms the Mellin functional equation, E8 target 1/15, normalization,
   and correct Leech numerical prefix. It explicitly separates automatic
   midpoint equality from the numerical evaluation.
2. [Viazovska, arXiv:1603.04246](https://arxiv.org/abs/1603.04246),
   equations (28), (35), (38), (41), Propositions 1--4 and Theorem 4.
   Gives the positive/negative Fourier decomposition, exact root derivative,
   regularized Taylor expansion, and positive-eigenfunction contour.
   The E8 proof here uses those established data; it does not claim to
   reconstruct the sphere-packing proof.
3. [Cohn--Kumar--Miller--Radchenko--Viazovska, arXiv:1603.06518](https://arxiv.org/abs/1603.06518),
   Section 2, especially (2.1), (2.6), and the normalized values on page 1023.
   Supplies the dimension-24 eigenfunction and exact first two root data.
4. [Cohn--Kumar--Miller--Radchenko--Viazovska, arXiv:1902.05438](https://arxiv.org/abs/1902.05438),
   Lemma 2.2, Theorem 1.7, Corollary 1.8.
   The Gaussian density lemma directly justifies extension of our summation
   identity to all radial Schwartz functions. The interpolation/uniqueness
   results do not themselves evaluate the midpoint integral.
5. [Alfes--Kiefer--Mazáč, 2025](https://doi.org/10.1007/s00220-025-05313-6),
   Section 2 and Lemma 2.2. Confirms the broader modular/Gaussian summation
   framework and cites the same density lemma. Not used as a prior proof of
   the specific E8 moment.

## Prior work and claim boundary

The earlier cached attempt already established midpoint Fourier invariance
and equivalent modular periods. Repeating those reductions alone would not
constitute new progress. The present substantive step is the proved
E2-squared/E2-cubed summation formula and its exact finite evaluation to 1/15.
The real-contour reduction, dimension-24 weighted-tail identity, and explicit
failure of a direct higher-power ansatz are additional results of this run.

Read-only repository searches for the exact problem ID and for “Mellin E8”
and “magic” returned no indexed result; the main queue row was independently
read and still listed the old title at rank 513. Such search results are not
an exhaustive repository-history or priority proof.

The full text of Seewoo Lee’s 2026 Berkeley thesis, [Positive Quasimodular
Forms and Linear Programming Bounds](https://escholarship.org/uc/item/2j65b950),
was additionally searched for Mellin, midpoint, 1/15, and the Leech decimal;
no matching passage was found. This is a targeted text check, not a claim
that every result in the thesis was reviewed.

Current searches combining Mellin, Cohn/Miller, Viazovska, 1/15, and the
Leech decimal did not locate a later primary-source evaluation. The four
central papers were read at the relevant sections. Recent modular-summation
work was also checked. The literature conclusion is deliberately bounded:
no novelty claim, and no assertion of comprehensive global open status.

## Publication gate

This is a frozen **author packet**, not an independent referee report.
The E8 theorem and Leech auxiliary theorem require fresh independent audit.
The overall problem must not be labeled solved on the strength of the E8
subproblem alone. Public artifacts exclude complete source papers, downloaded
PDFs, the original catalog, prior report dumps, and private coordination files.
