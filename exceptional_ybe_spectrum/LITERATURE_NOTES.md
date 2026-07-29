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

## Open source-audit questions

- Does Lechner's trace lemma make all-level Markov agreement automatic for
  every matrix-class solution, without scalar partial traces?
- Exactly which quotient and semisimplicity hypotheses are needed to convert
  trace agreement into faithful tower embeddings?
- Which older generalized/localized constructions could be equivalent to a
  putative \(d=6\) witness under blocking, ancillas, or tower equivalence?
