# Priority and equivalence audit

Initial audit: **27 July 2026**. Fresh priority/reference audit:
**16 August 2026** (America/Los_Angeles).

## Bottom line

The exact construction appears to be new, and it directly fills the
four-dimensional case that Lechner described as unresolved in March 2026:

\[
\left[e^{i\pi/3},\frac12,4\right]\ne\varnothing.
\]

The stronger historically accurate statement is:

> The broad ordinary-localization question was open in the
> \(\mathcal C(\mathfrak{sl}_3,6)\) case study of Galindo, Hong, and Rowell
> from 2012 onward; Lechner isolated the exact exceptional \(16\times16\)
> matrix question in 2026.

No searched source supplied the five-word Pauli formula, an equivalent
ordinary \(16\times16\) unitary Hecke operator, or a four-dimensional
ordinary localization of the \((3,6)\) Jones--Wenzl tower. This is a
provisional priority conclusion, not proof of absolute novelty.

The 16 August refresh found no intervening public collision. Lechner remained
at arXiv v1 with no journal reference or DOI; exact-title, identifier,
parameter, formula-fingerprint, citation-index, and authenticated public-code
searches found no later construction. Seven Yang--Baxter arXiv papers posted
between the two audit dates were inspected and concerned other problems. Weak
or unavailable indexing signals are treated only as limitations, never as
positive novelty evidence.

The intervening arXiv records inspected were
[2607.28626](https://arxiv.org/abs/2607.28626),
[2607.29660](https://arxiv.org/abs/2607.29660),
[2608.01884](https://arxiv.org/abs/2608.01884),
[2608.04097](https://arxiv.org/abs/2608.04097),
[2608.06736](https://arxiv.org/abs/2608.06736),
[2608.08688](https://arxiv.org/abs/2608.08688), and
[2608.09081](https://arxiv.org/abs/2608.09081). The closest recent generalized
Yang--Baxter backstops,
[2605.30007](https://arxiv.org/abs/2605.30007) and
[2606.26510](https://arxiv.org/abs/2606.26510), concern extraspecial or
multisite-integrability constructions, do not cite Lechner, and do not give
the ordinary four-dimensional Hecke localization here.

## Primary-source boundary

### Galindo--Hong--Rowell

- [arXiv:1105.5048](https://arxiv.org/abs/1105.5048), submitted 25 May
  2011; [journal version](https://doi.org/10.1093/imrn/rnr269), advance
  access 14 February 2012.
- Section 5.6 says the \(\mathcal C(\mathfrak{sl}_3,6)\) sequence did not
  appear to have a localization.
- Example 3.14 records a different \((3,2)\)-generalized operator. Its
  projective eigenvalue ratio is \(i\) up to inversion, whereas the new
  active operator has ratio \(-e^{i\pi/3}=e^{-2\pi i/3}\), so they are not
  unitarily conjugate up to an overall phase.
- Lemma 5.26 excludes a two-dimensional unitary ordinary localization.
- Equation (5.2) and Theorem 5.28 give an \(8\times8\)
  \((3,1)\)-generalized localization, derived from quaternionic
  representations.
- Remark 5.29 distinguishes the nonunitary \(9\times9\) Jimbo solution,
  whose braid representation has extraneous sectors.
- Remark 6.2 notes that this case might have been a counterexample to the
  more restrictive ordinary-localization conjecture.

This source is prior art for the representation tower, the localization
problem, the two-dimensional obstruction, the quaternionic model, and the
Markov-trace proof strategy. It does not contain the new ordinary
four-dimensional operator.

### Rowell's quaternionic representation

- [arXiv:1006.4808](https://arxiv.org/abs/1006.4808);
  [Quantum Topology article](https://doi.org/10.4171/QT/18).
- This proves that the braid representations associated with the
  \((3,6)\) Hecke quotients factor through a finite group, using unpublished
  Goldschmidt--Jones quaternionic representations.

This is close conceptual prior art. It does not give the displayed ordinary
ququart \(R\)-matrix. No chain-level equivalence between its model and the
new \((3,2)\) active form has been established.

### Lechner's classification

- [arXiv:2603.20158v1](https://arxiv.org/abs/2603.20158v1), submitted
  20 March 2026 at 17:34:47 UTC.
- The abstract says one even-dimensional class larger than two may or may
  not exist.
- Theorem 3.4 restricts unitary two-eigenvalue Hecke operators to eight
  families.
- Page 16 states that
  \([e^{i\pi/3},1/2,2m]\) was unknown, cites the 2012 case study, and
  proves the \(d=1\) member (base dimension two) empty.

The new matrix exactly answers the first unresolved member, base dimension
four. Tensoring with identity operators supplies base dimensions \(4m\);
dimensions \(4m+2\) beyond two remain open.

### Other generalized/local braid literature checked

- [Rowell--Wang, localization of unitary braid representations](https://arxiv.org/abs/1009.0241).
- [Galindo--Rowell, unitary braided vector spaces](https://arxiv.org/abs/1312.5557).
- Rowell et al., extraspecial two-groups and generalized Yang--Baxter
  equations, [arXiv:0706.1761](https://arxiv.org/abs/0706.1761).
- Vasquez--Wang--Wong, metaplectic anyons,
  [arXiv:1602.08536](https://arxiv.org/abs/1602.08536).
- Sinha et al., *Hidden Ising models from the generalized Yang--Baxter
  equation*, [arXiv:2605.30007](https://arxiv.org/abs/2605.30007).

These sources contain generalized, Gaussian, extraspecial, or metaplectic
operators, but the audit found no ordinary representative of
\([e^{i\pi/3},1/2,4]\). The May 2026 multi-site paper concerns a different
multi-site/extraspecial construction. The bare fact of being a
\((3,2)\)-generalized operator is established prior art; the relevant
candidate contribution is the exceptional spectrum, the ordinary ququart
blocking, and faithfulness on \(H_n(3,6)\).

## Formula and code search

The following focused searches were run:

- exact class parameters together with “four dimensional,” “ordinary
  localization,” “Yang--Baxter,” and
  \(\mathcal C(\mathfrak{sl}_3,6)\);
- the preprint identifier `2603.20158` with “solution,” “localization,” and
  “Yang--Baxter”;
- exact Pauli-word pairs `ZIZZ ZIJJ` and `XIXX JIZJ`;
- the coefficient obstruction `3 beta^2 - 1` with “Yang--Baxter”;
- public GitHub code search for the exact word combinations.

No match predating this release was found. The exact-code searches returned
no public result before the repository checkpoint. Search-engine results for
“exceptional \(R\)-matrix” mostly concerned exceptional Lie algebras, a
different use of “exceptional.”

The Lechner arXiv record still had no later version on 16 August 2026.
Crossref, zbMATH, Google Scholar, OpenAlex, and exact-title/identifier searches
found no later publication or citing work; Semantic Scholar rate-limited the
refresh. These are incomplete negative signals and are not treated as proof of
novelty.

All six bibliography records, DOI targets, and the manuscript's cited
sections, equations, theorem, lemma, remark, and page claims were checked
against primary sources in the refresh. Wenzl's official title is “Hecke
algebras of type \(A_n\) and subfactors”; that subscript is retained in the
paper.

## Equivalence risks

The main remaining priority risks are:

1. a basis-changed or blocked form of the known quaternionic
   \((3,1)\)-generalized localization;
2. an unpublished Goldschmidt--Jones or expert construction;
3. a differently normalized Hecke symmetry not indexed by the exceptional
   class notation;
4. concurrent work responding to the March 2026 preprint;
5. a result available only in a source not reached by the search tools.

The visible spectator qubit does yield a valid \((3,2)\)-generalized
operator after swapping the two qubits inside every ququart. The global
sitewise swap conjugates the ordinary representation to a spectator identity
tensored with this generalized representation, so it faithfully localizes
the same quotient. This does not identify it with the published \((3,1)\)
operator: their overlap geometries differ, so an equivalence would require
an explicit intertwining theorem between the two generalized models.

## Claim language approved by this audit

Appropriate:

- “an explicit exact solution of the first unresolved exceptional class”;
- “appears to give the first ordinary four-dimensional localization found
  in the searched literature”;
- “resolves the existence question stated in arXiv:2603.20158, subject to
  independent review”;
- “the principal 2012 candidate counterexample is not a counterexample if
  the proof and identification are confirmed.”

Too strong:

- “the exact \(16\times16\) question was posed in 2012”;
- “the exceptional family is now completely classified in every even
  dimension”;
- “the construction is inequivalent to all older generalized
  localizations”;
- “absolute worldwide priority is established.”

## Process limitation

No author, expert, or other outside individual was contacted. That follows
the repository's independent-research policy. Expert comparison with the
unpublished quaternionic notes could materially improve the equivalence
audit, but only the human researcher may initiate such contact.
