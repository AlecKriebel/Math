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
7. L. Chen and L. Yu, *On the Schmidt-rank-three bipartite and
   multipartite unitary operator*, arXiv:1407.5464.
7a. S. M. Cohen and L. Yu, *All unitaries having operator Schmidt rank 2
   are controlled unitaries*, arXiv:1211.5201.
8. R. Conti and G. Lechner, *Yang--Baxter endomorphisms*,
   arXiv:1909.04127.
9. A. Bytsko, *On orthogonal projections related to representations of
   the Hecke algebra on a tensor space*, arXiv:2212.13116.
10. A. Bytsko, *Two relations for the antisymmetrizer in the Hecke
    algebra*, arXiv:2203.08664.
11. R. Conti and F. Fidaleo, *Braided Endomorphisms of Cuntz Algebras*,
    Math. Scand. 87 (2000), 93--114.
12. S. Majid and M. Markl, *Glueing operation for R-matrices, quantum
   groups and link-invariants of Hecke type*, arXiv:hep-th/9308072;
   Math. Proc. Cambridge Philos. Soc. 119 (1996), 139--166.
13. A. Müller-Hermes and I. Nechita, *Restrictions on the Schmidt rank of
   bipartite unitary operators beyond dimension two*, arXiv:1612.07616;
   published as *Operator Schmidt ranks of bipartite unitary matrices*,
   Linear Algebra Appl. 557 (2018), 174--187.

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
- Cohen--Yu Theorem 6 and Chen--Yu Theorem 11 use independent local pre-
  and post-unitaries, so their controlled forms cannot themselves be
  inserted into the Yang--Baxter equation.  For a **Hermitian** unitary
  satisfying the exceptional shifted cubic, however, the exact twisted-
  control graph argument in `notes/low_schmidt_control_obstruction.md`
  closes this gap.  One valid sitewise conjugacy first converts the four-
  unitary equivalence to \(\sum_iE_iK\otimes V_i\). Hermiticity makes the
  support of \(K\) undirected. A nonbipartite component supplies a true
  rank-one leg projection, while an all-bipartite support would force a
  unitary to equal \(1/3\) times a unitary after taking one off-diagonal
  cubic coefficient. Consequently every exceptional solution of operator-
  Schmidt rank at most three has a rank-one projection in a true leg
  commutant and hence \(4\mid d\). This is a qualified Hermitian-cubic
  conversion, not a general claim that local equivalence preserves
  Yang--Baxter locality.
- Operator-Schmidt rank four is the sharp boundary of that controlled
  structure: the two-qubit swap is a direct Hermitian-involutive OSR-four
  counterexample with scalar leg commutants. No source found in the
  targeted low-Schmidt literature gives a controlled or block-controlled
  normal form for arbitrary rank-four bipartite unitaries.
  Müller-Hermes--Nechita prove that, apart from the missing \(2\times2\)
  rank three, every arithmetically possible operator-Schmidt rank occurs;
  their result is a rank-existence theorem, not such a normal form. The
  conditional theorem in `notes/osr4_clifford_frame_parity_audit.md`
  instead assumes a four-product Clifford frame and proves \(4\mid d\) by
  complementary binary commutation graphs. It must not be cited or used
  as a classification of all OSR-four exceptional solutions.
- Conti--Lechner identify the one-site algebraic fixed points with a leg
  commutant, but distinguish this sharply from von Neumann ergodicity.
  Their Proposition 7.12 gives the necessary ergodicity condition
  \(\|\phi_R(R)\|_2^2=1/d^2\). Automatic standardness gives \(1/4\) in the
  exceptional class, so every \(d>2\) exceptional solution is nonergodic.
  Their Propositions 7.10 and 7.12 and box-sum construction yield a sharp
  countermodel: \((q-1)(I_m\boxplus I_m)\) has the exact same scalar
  partial trace, finite braid images, scalar leg commutants, no algebraic
  fixed points, and a nontrivial von Neumann fixed algebra. Thus finite
  image and nonergodicity do not by themselves supply a leg-commutant
  projection. The countermodel has an opposite eigenvalue pair, leaving
  open a theorem that also uses the exceptional horizontal
  braid-subfactor irreducibility.
- Rowell, arXiv:1006.4808, proves more than finite dimensionality of the
  Hecke quotient: his main theorem and quaternionic Lemmas 3.1--3.2 show
  that the canonical subgroup generated inside \(H_n(3,6)\) is finite for
  every fixed \(n\). Any exceptional tensor representation therefore has
  finite finite-strand braid image. The groups grow with \(n\), and this
  theorem does not make the global von Neumann fixed algebra algebraic.
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
  obstruction. His \(W_{\mathcal T}\) is the cyclic compression
  \(P_{12}LP_{12}\) after vectorization. The relation fixes its singular
  values but not equality of its left and right singular spaces; the exact
  published witness is nonnormal with squared defect \(16/3\). See
  `notes/bytsko_characteristic_matrix_audit.md` and
  `notes/overlap_kramers_parity_audit.md`.
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
- Hai, arXiv:math/0502399, equations (1)--(4), treats the standard Manin
  super family as an ordinary Hecke symmetry, but printed super-Hecke
  formulas occur in multiple scalar/sign conventions.  The present audit
  therefore defines the normalized block directly and verifies both
  \((T+I)(T-qI)=0\) and the ordinary braid equation rather than importing
  a display by notation alone.
- Gurevich et al., *KZ equations and Bethe subalgebras in generalized
  Yangians related to compatible \(R\)-matrices* (2019), §2, display the
  standard \(GL(1|1)\) Hecke block with roots \(t,-t^{-1}\).  Multiplying
  by \(t\) gives the \(\{t^2,-1\}\) normalization used here.
- The balanced standard \(GL(s|s)\) symmetry has the correct equal
  algebraic multiplicities for every even \(d=2s\), but exact
  eigenspace-orthogonality rules out every positive tensor-square local
  metric at \(t^2=e^{i\pi/3}\).  This is an ansatz-level unitarity
  obstruction, not a classification of multiparameter or twisted
  super-Hecke symmetries.
- Majid--Markl Theorem 2.4 gives a canonical associative gluing
  \(R\mathbin{\oplus_{\mathfrak q}}R'\). On every nonzero mixed pair its
  matrix is
  \[
  \begin{pmatrix}
  0&1\\
  1&\mathfrak q-\mathfrak q^{-1}
  \end{pmatrix}.
  \]
  At the exceptional normalization
  \(\mathfrak q=e^{i\pi/6}\), the final entry is \(i\). For any positive
  one-site metric, the two mixed simple tensors have a real cross inner
  product, so the second column has twice the squared norm of its input.
  Thus the canonical gluing cannot be made unitary, even after an
  arbitrary one-site basis change. This identifies and closes a named
  literature construction inside the earlier scalar-cross no-go.
  Their more general Theorem 2.7 has mixed block
  \(\left(\begin{smallmatrix}0&S\\U&T\end{smallmatrix}\right)\).
  The Hecke polynomial forces \(T\) to equal the sum of its two roots,
  while unitarity for orthogonal color summands forces \(T=0\).
  Hence the full operator-valued gluing form is also excluded for the
  exceptional non-opposite roots in the orthogonal Hilbert-direct-sum
  setting. Arbitrary colored mixed blocks outside that form, or a
  nonorthogonal algebraic color splitting, are not excluded.
- Conti--Lechner Theorem 3.8 identifies
  \(\mathcal L_{R,n}=E_n(\mathcal L_R)\). In the exceptional class,
  automatic standardness and the Hecke double-coset decomposition sharpen
  this to
  \(\mathcal L_{R,n}=\mathcal A_n\), the represented
  \(H_n(3,6)\) algebra. Thus their finite commuting squares contain no
  additional horizontal algebra beyond the already-audited Hecke tower.
- Galindo--Hong--Rowell explicitly distinguish ordinary, quasi-, and weak
  localizations in Definitions 4.16 and 4.20 and Remark 4.22. Their
  Proposition 4.21 supplies a weak localization for any fusion category,
  while Section 5.6 supplies a two-dimensional quasi-localization here.
  Neither result converts diagonal algebra embeddings into the strict
  same-\(P\) placements \(P\otimes I\), \(I\otimes P\). Consequently a
  module-category or cell classification can constrain the present matrix
  problem only after a separate extension theorem is proved.

## Open source-audit questions

- Which older generalized/localized constructions could be equivalent to a
  putative \(d=6\) witness under blocking, ancillas, or tower equivalence?
- Does the \(D^{(6)}\) face connection admit a published vertex--face,
  biunitary, or finite-depth conversion to a strict tensor-power tower not
  visible in the Evans--Pugh construction?
- Is the invariant odd-leg-projection divisibility lemma, or an equivalent
  restricted common-sector count, already recorded in subfactor,
  commuting-square, or biunitary-connection language?
- Does the combination of no-opposite-spectrum (hence irreducibility of
  \(\varphi(\mathcal L_R)\subset\mathcal L_R\)), finite depth, and the
  special \((3,6)\) finite groups force the vertical fixed algebra
  \(\mathcal L_R'\cap\mathcal N\) to contain an algebraic fixed point?
  Finite image plus the exact partial trace alone does not; the stronger
  implication is not in the audited sources and must not be assumed.
- Can the repeated same-\(P\) tensor placements be upgraded to a finite
  module category or globally flat connection whose projective
  \(A_4\)-sector acts specifically on dimension \(s=d/2\)? The finite
  horizontal relative commutants, their inclusion matrices, and the first
  commuting-square cell do not perform this descent.
