# Independent adversarial review — Zenodo 22013710

**Verdict: PASS within the manuscript's stated mathematical scope.** No substantive mathematical defect or unresolved central proof gap was found. This review does not certify originality, journal acceptance, historical priority, or an exhaustive classification of all Yang–Baxter operators.

## Reviewed object and independence

The actual published twenty-page v1.2.0 PDF, *An exceptional four-dimensional unitary Hecke Yang–Baxter operator: a five-word Pauli–Clifford normal form*, was read in full. Corresponding source equations, mathematical sections of the five supported verifier implementations, and selected adversarial tests were inspected. The PDF inside the source package is byte-identical to the separately published PDF.

- PDF SHA-256: a769689a4b5b9c48bf675f79d3b80916a7821ad5a8db0b9ec246df460dffb8de
- Source ZIP SHA-256: 3324731dc0b9c2e5d5da6e9d25c724e9c2e66c52fd461f1d03d38602112b6980
- Record: https://zenodo.org/records/22013710

No sibling review, archived adjudication, or prior review conclusion was read. The first fresh exact program was written from literal manuscript formulas before reading the published verifier implementations. My mathematical assessment preceded the archived-code replay. A source-file listing and release-status string assertions in test code were incidentally visible; they were not correctness evidence. Reference papers were downloaded and read directly. No source, publication, website, spreadsheet, or Git state was changed.

## Exact claim and strongest verified result

On \(V=\mathbb C^4=\mathbb C^2\otimes\mathbb C^2\), with the stated tensor order and \(q=e^{i\pi/3}\), the displayed five-word reflection gives an explicit unitary \(R\) satisfying the braid-form Yang–Baxter equation and \((R+I)(R-qI)=0\), with both multiplicities eight. Its local copies represent the trace quotient \(H_n(3,6)\) faithfully and compatibly for every \(n\), giving the stated ordinary unitary localization. Four is the minimum local dimension for that localization.

The literal matrix \(S\), together with exchange of the two four-dimensional sites, identifies this \(R\) with the specified Galindo–Rowell Family III operator. Tensor reversal and an inner braid automorphism remove the site-opposite at the representation level. The enhanced invariant, ordinary finite braid images, and fixed-data polynomial-time evaluation consequence then follow with the stated phases and trace normalization.

**Exact remaining central gap:** none identified. Universal statements rest on written arguments and checked imports, not extrapolation from small matrices.

## Construction, circle, and degenerate points

The real matrices \(I,X,Z,J\), including \(J=XZ\) and \(J^2=-I\), were encoded independently. The five words are Hermitian involutions; the first four commute, \(D=ABC\), and \(E\) anticommutes with each. Thus \(M^2=E^2=I\) and \(ME=-EM\), giving the reflection circle without a numerical-fit assumption.

The entire six-letter-word cubic residual was recomputed exactly. It has the stated eighteen-word support and coefficients. All four signed points \(a^2=2/3,b^2=1/3\) vanish. The four axis points and \((3/5,4/5)\) fail. The converse is a proof: an axis leaves a nonzero displayed coefficient; off the axes the first coefficient group forces \(3b^2=1\).

Exhaustiveness is confined to the displayed real reflection circle. The paper does not claim exhaustiveness in the space of unitary operators, uniqueness up to local equivalence, or reconstruction of its original numerical search. Those distinctions are correctly maintained.

The independent \(R\) passed exact unitarity, Hecke, and 64-dimensional Yang–Baxter tests. Structurally, writing \(R=a_0I+b_0H\), its braid residual is
\[
b_0(a_0^2+b_0^2/3)(H_1-H_2)=0
\]
because \(a_0/b_0=i/\sqrt3\). No spectral tolerance is used.

The negative spectral projection is Hermitian, idempotent, has rank eight, and has both unnormalized partial traces \(2I_4\). Its normalized spectral trace is \(1/2\), not \(2\). Fresh calculations also verify \(R^3=-I\), the skein identity, and both enhancement equations for \(R^{\pm1}\). Once the literal formulas are fixed, conjugating \(q\), changing quarter-turn order, or omitting the site swap are material changes, not harmless conventions.

## Infinite tower and minimal dimension

Tensor compatibility follows by appending \(I_4\). The right partial trace proves the Markov property for every element of the preceding Hecke algebra. Markov-trace uniqueness identifies the normalized matrix character with the \(H_n(3,6)\) trace.

For the nontrivial kernel inclusion, if \(x\) is in the trace annihilator, take \(y=x^*\). The representation preserves the involution, so
\[
\operatorname{Tr}(\rho(x)^*\rho(x))=0
\]
implies \(\rho(x)=0\). Conversely, a zero matrix annihilates every pairing. Thus the ideals coincide for every \(n\). The argument does not presume that the unreduced root-of-unity Hecke algebra is semisimple.

Dimension one cannot represent both spectral projections injectively. The dimension-two exclusion is GHR's lemma about the relevant spectrum up to scalar. Dimension three uses Lechner's actual assumptions: a nontrivial unitary two-eigenvalue Hecke operator has a positive Markov matrix character. At this \(q\), the possible nontrivial parameters are \(1/3,1/2,2/3\); the middle value would require rank \(9/2\).

For the other cases, put \(c=1/3\), \(A=e_1e_2e_1\), and \(T=A-ce_1\). Independent manipulation gives
\[
A^2=(1+c)A-ce_1,\quad T^2=(1-c)T,\quad
\operatorname{tr}_\eta(T^*T)=(1-c)\eta(\eta-c).
\]
At \(\eta=1/3\), faithfulness of the candidate matrix trace kills \(T\). In the target \(\eta=1/2\) quotient the squared norm is \(1/18>0\). Complemented projections give the corresponding contradiction at \(2/3\). Fresh exact calculations returned \(1/18\) for both target obstructions. This excludes faithful dimension-three localization rather than merely recording unsuccessful searches.

The conclusion is minimum dimension four. Amplification supplies multiples of four, without claiming to classify every larger dimension.

## Tensor placement and local/global comparison

The within-site qubit swap gives the printed active \(K_H\) and a spectator qubit. Adjacent active triples shift by two qubits. The distinction from shift one is material: the fresh \(K\) check gives squared residuals \(24,0\), respectively. The published exact route also reproduced GHR's \(0,48\) residuals. A common spectrum or unrestricted \(8\times8\) conjugacy cannot establish equivalence of different tensor placements.

The literal \(S\) is unitary. Its three quaternion-generator identities and full \(R\)-identity were independently verified. Omitting the site swap fails. What is proven is local-unitary equivalence to the opposite operator; direct local-unitary equivalence to the unopposed operator remains undetermined, exactly as the text says.

At \(n\) strands tensor reversal changes \(i\) to \(n-i\), the inner automorphism induced by the Garside braid. Multiplying by the inverse Garside image gives a same-word intertwiner for arbitrary \(n\). This is a structural proof. A second fresh program independently checked Garside orientation, full rank of quaternionic normal-word Pauli labels, and Clifford conjugation/inverse on every single-qubit generator for 2–32 strands. These are finite convention controls.

The label-rank argument also has an arbitrary-\(n\) reading: the \(Z\)-label on the second qubit of site \(i\) recovers the exponent of \(U_i\), while the \(X\)-labels recover the \(V_i\) exponents recursively from the left boundary. Thus distinct normal words have distinct Pauli labels. This checks that the coefficient trace is the normalized matrix trace, rather than confusing the full quaternionic algebra with its smaller braid-generated subalgebra.

## Finite images, Pauli frame, and links

In the Galindo–Rowell frame the operator is a scalar times two Pauli quarter turns, so its projective braid image is finite. Since \(R^6=I\), local determinants have finite order. Any scalar in the ordinary image is constrained by its \(4^n\)-dimensional determinant, so the scalar kernel is finite too. Finite order of individual generators alone would not suffice.

The five-word matrix is not claimed to be Clifford in its computational frame. The archived verifier reproduced the printed eight-term conjugate of \(XIII\); the finite-image proof uses the fixed conjugated Pauli frame.

The enhancement is \((R,I_4,\kappa,2)\), \(\kappa=q-1\). Both stabilizations follow from partial traces \(2\kappa^{\pm1}I_4\), giving
\[
\mathcal J_R(\widehat\xi)=\kappa^{-\mathrm{wr}(\xi)}2^{-n}\operatorname{Tr}\rho_n(\xi).
\]
The unknot value is \(2\). The Hecke identity yields \(\mathcal J_++\mathcal J_-=\mathcal J_0\), matching \(2P_{\rm H}(i,i)\) in the manuscript convention. Fresh controls covered the unknot, unlink, both signs of Hopf and trefoil, figure eight, Borromean rings, and both stabilization signs.

The component sign converting Lickorish–Millett's polynomial convention is necessary. Their oriented triple cyclic branched cover sends each positive meridian to \(1\bmod3\), as in this manuscript. Their theorem and crossing induction support the even mod-2 homology dimension and stated evaluation. The polynomial-time import is used for fixed Family III metric data, not arbitrary metric data supplied as input.

## Primary imports checked

URLs and download hashes are retained in reference-receipts.json.

- [Wenzl, original journal scan](https://gdz.sub.uni-goettingen.de/download/pdf/PPN356556735_0092/LOG_0021.pdf), pp.373 and377–379: uniqueness (3.2), the parameter formula, and Theorem3.6(b). Substitution \(q=e^{i\pi/3},k=3,l=6\) gives \(1/2\). This avoids relying on GHR's malformed printed parameter expression.
- [GHR, author preprint](https://arxiv.org/pdf/1105.5048), localization definition, §5.6, Lemma5.26, Theorem5.28 and its matrix: tower identification and dimension-two exclusion have the needed scope. This preprint's introductory numbering differs from final-journal numbering; the definitions' content was checked, not every final-journal pinpoint.
- [Lechner v1](https://arxiv.org/pdf/2603.20158v1), Lemma3.1 and Theorems3.3–3.4: Markov positivity and relevant parameters, with unitary and two-eigenvalue assumptions.
- [Rowell, journal version](https://ems.press/content/serial-article-files/36758), Theorem3.1 and Lemma3.2: finite image and the braid-generated subalgebra's identification with \(H_n(3,6)\).
- [Galindo–Rowell v1](https://arxiv.org/pdf/2608.16865v1), literal §13 operator/tower, Theorem7.3, Theorem7.10, Proposition8.1, Lemma8.3 and Theorem8.4: local conventions, trace transport, fixed-data complexity, and finite ordinary images.
- [Turaev, original journal scan](https://gdz.sub.uni-goettingen.de/download/pdf/PPN356556735_0092/LOG_0031.pdf), pp.529–531: enhancement, trace normalization, and Theorem3.1.2's two stabilization signs.
- [Lickorish–Millett, author-hosted original](https://web.math.ucsb.edu/~millett/Papers/1986Millett6LickorishCommMathHelv.pdf), Theorem2 and pp.353–355: polynomial convention and oriented triple-cover evaluation.

## Reproducibility and limits

The fresh exact script passed 84 algebraic checks. The fresh global program passed all controls for 2–32 strands, with 44,175 individual checks. Neither imports published verification code. The first uses SymPy 1.14.0; the second uses integer labels and exact finite phases. An existing Python 3.14.6/SymPy 1.14.0 installation from the preceding review was reused only as a runtime, with bytecode writes disabled.

All five published routes passed. Six selected negative tests rejected optimization or deliberate multiplication, gauge-sign, site-swap, writhe-factor, and quarter-turn-order mutations. All 43 package-local checksums matched. Logs, independent programs, compact results, and source receipts are preserved. Downloaded references, page renders, and a redundant full global-check list are ignored caches. Acquisition files remained unchanged.

No proof-assistant formalization, original numerical-search reconstruction, independent implementation of the imported general Gauss-sum algorithm, or comprehensive literature/priority audit was performed. Those are not missing premises of this explicit construction. Public wording should retain the manuscript's distinction between its explicit normal form and the concurrent/prior results from which the broader consequences follow.
