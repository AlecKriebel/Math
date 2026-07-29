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

## Open source-audit questions

- Which older generalized/localized constructions could be equivalent to a
  putative \(d=6\) witness under blocking, ancillas, or tower equivalence?
- Does the \(D^{(6)}\) face connection admit a published vertex--face,
  biunitary, or finite-depth conversion to a strict tensor-power tower not
  visible in the Evans--Pugh construction?
- Is the invariant odd-leg-projection divisibility lemma, or an equivalent
  restricted common-sector count, already recorded in subfactor,
  commuting-square, or biunitary-connection language?
