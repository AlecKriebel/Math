# Literature notes

## Core sources

1. A. Kriebel, *A Minimal Unitary Localization of the
   \(\mathcal C(\mathfrak{sl}_3,6)\) Jones--Wenzl Representations*,
   project page and exact verifiers:
   <https://aleckriebel.github.io/Math/papers/exceptional-ybe-d4/>.
2. G. Lechner, *The classification problem for unitary \(R\)-matrices with
   two eigenvalues*, arXiv:2603.20158v1.
3. C. Galindo, S.-M. Hong, E. C. Rowell, *Generalized and quasi-localizations
   of braid group representations*.
4. E. C. Rowell, work on the quaternionic braid representation relevant to
   the \((3,6)\) Jones--Wenzl quotient.
5. Original Jones--Wenzl and Hecke-algebra sources used by the above papers.
6. D. E. Evans and M. Pugh, *Ocneanu Cells and Boltzmann Weights for the
   \(SU(3)\) \(\mathcal{ADE}\) Graphs*, arXiv:0906.4307.
7. L. Chen and L. Yu, *Nonlocal and controlled unitary operators of
   Schmidt rank three*, arXiv:1407.5464.
8. R. Conti and G. Lechner, *Yang--Baxter endomorphisms*,
   arXiv:1909.04127.
9. A. Bytsko, *On orthogonal projections related to representations of
   the Hecke algebra on a tensor space*, arXiv:2212.13116.
10. A. Bytsko, *Two relations for the antisymmetrizer in the Hecke
    algebra*, arXiv:2203.08664.
11. R. Conti and F. Fidaleo, *Braided Endomorphisms of Cuntz Algebras*,
    Math. Scand. 87 (2000), 93--114.

## Normalization notes requiring care

- The matrix class uses eigenvalues \(\{-1,e^{i\pi/3}\}\).
- The spectral projection \(P\) for \(-1\) has normalized rank
  \(\eta=\operatorname{rank}(P)/d^2=1/2\).
- Lechner's formula
  \[
  \eta_{\ell,k}=
  \frac{\sin(\pi(k-1)/\ell)}
       {2\cos(\pi/\ell)\sin(\pi k/\ell)}
  \]
  gives \(\eta_{6,3}=1/2\).
- Printed conventions in older sources must be translated explicitly; no
  formula is imported solely by matching notation.

## Resolved source-audit questions

- Lechner's no-opposite-spectrum result applies to this exact exceptional
  spectrum. Together with tensor reversal it forces both scalar partial
  traces for every matrix-class solution. The all-level Markov property then
  propagates directly by partial trace.
- The specialized Hecke representation has the \(\eta=1/2\) Markov trace.
  Positivity and faithfulness of normalized matrix trace identify its kernel
  with the trace radical, hence the induced representation of the
  semisimple trace quotient \(H_n(3,6)\) is faithful.
- Evans--Pugh's \(\mathcal D^{(6)}\) connection uses directed-edge path
  spaces. Its six graph vertices are not six freely tensorable local states:
  the exact two-edge space has dimension 20, and the three-edge space has
  dimension 48. This is a relevant generalized/path realization but not an
  already-published ordinary \(d=6\) witness.
- Chen--Yu's Schmidt-rank-three theorem uses independent local pre- and
  post-unitaries. It cannot be converted into a one-leg-commutant MASA
  statement and therefore does not combine automatically with the new
  controlled-leg divisibility theorem.
- Conti--Lechner identify the one-site algebraic fixed points with a leg
  commutant, but distinguish this sharply from von Neumann ergodicity.
  Their Proposition 7.8 gives the necessary ergodicity condition
  \(\|\phi_R(R)\|_2^2=1/d^2\). Automatic standardness gives \(1/4\) in the
  exceptional class, so every \(d>2\) exceptional solution is nonergodic.
  Their box-sum examples show that nonergodicity can coexist with no
  nontrivial algebraic fixed points. Thus it does not by itself supply a
  leg-commutant projection.
- Lechner's tensor-product operation multiplies dimensions and pairwise
  multiplies spectra. The exceptional spectrum has trivial multiplicative
  stabilizer, so this operation preserves the class only for an identity
  spectator. The displayed definition and Proposition 3.6 were checked both
  by extraction and by rendering pages 15--16 of arXiv:2603.20158v1.
- In Bytsko's projection convention the exceptional relation has
  \(Q=\sqrt3\) and Hecke phase \(e^{i\pi/6}\); multiplying his generator by
  \(e^{i\pi/6}\) gives the present normalization. His parameter is
  \(k=3d^3/8\), and his characteristic matrix has eigenvalues \(1\) and
  \(1/3\) with multiplicities \(d^3/8\) and \(3d^3/8\). At \(d=6\) these
  are \(27\) and \(81\), so the theorem contains no hidden even-degeneracy
  obstruction. See `notes/bytsko_characteristic_matrix_audit.md`.
- Conti--Fidaleo define and give sufficient criteria for standard braided
  Cuntz endomorphisms, but the audited results do not classify all local
  tensor realizations of statistical dimension two in arbitrary Cuntz
  rank. The phrase “standard braided, index \(4\)” therefore does not by
  itself impose \(4\mid d\).
- Lechner's positive-trace list at \(q=e^{2\pi i/6}\) permits normalized
  negative ranks \(1/3,1/2,2/3\) for a non-scalar local compression; it is
  not legitimate to assume a reducing cell is automatically balanced.
  This use does not assume the compression has scalar partial traces:
  Lechner's Lemma 3.1 makes the tensor-space trace Markov automatically
  because the two eigenvalues are not opposite, and Theorem 3.4 then
  applies.
  Combining this three-value list with the ambient rank equations gives
  the common-reduction descent theorem in
  `notes/common_reduction_general.md`.

## Open source-audit questions

- Which older generalized/localized constructions could be equivalent to a
  putative \(d=6\) witness under blocking, ancillas, or tower equivalence?
- Does the \(D^{(6)}\) face connection admit a published vertex--face,
  biunitary, or finite-depth conversion to a strict tensor-power tower not
  visible in the Evans--Pugh construction?
- Is the invariant odd-leg-projection divisibility lemma, or an equivalent
  restricted common-sector count, already recorded in subfactor,
  commuting-square, or biunitary-connection language?
- Does finite depth of the \(H_n(3,6)\) braid subfactor add a hypothesis
  strong enough to turn Conti--Lechner nonergodicity into an algebraic
  fixed point? This implication is not in the audited source and must not
  be assumed.
