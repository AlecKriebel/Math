# Independent review: SU(3)₁ / Haah bounded-spread comparison

## Verdict

**PASS_SCOPED_LAURENT_FACTORIZATION_AND_FINITE_WINDOW_DIAGNOSTICS.** No mandatory correction was found in the frozen partial result. The original Conjecture 2 remains **unsolved**, with two substantive approaches recorded. The verified material supplies no bounded-spread isomorphism between the SU(3)₁ braided net and Haah's specified net.

Reviewed artifact: `PARTIAL_RESULT.md`, SHA256
`a9dad15a95370b0900274b185bb845771efed53a2ad343a00518d4ebff3e1cc1`.

The review was performed separately from the author. The submitted 345,948 exact assertions replayed with a byte-identical receipt. An independent symbolic/physical-vector checker passed 3,388 exact assertions. This is an adversarial AI review, not human peer review or a novelty certificate.

## 1. Exact source and current-version check

The assigned problem page was attempted but was not retrievable. I inspected the full primary source report, including the rendered Conjecture 2 and both generator diagrams on printed p. 1840 of [OWR 34/2025](https://ems.press/content/serial-article-files/52239). The target is the specific SU(3)₁ braided fusion spin system, with the source's possible reversal qualification, versus the specified qutrit edge-lattice net. Its generators are noncommuting Pauli operators; they are not a commuting stabilizer presentation.

The local matrix convention agrees with Haah's equation (31), and the two-column prescription is his equation (30). The cached Haah text is [arXiv:2211.02086v4](https://arxiv.org/abs/2211.02086v4), dated 10 August 2023. Current arXiv metadata confirms the publication in Communications in Mathematical Physics 403 (2023),661–698. The relevant full proof and formulas in Sections 4–5 were read; the final journal layout was not separately compared line by line. Proposition 5.1 already supplies invertibility, the conjugate commutant and fourth-tensor-power trivialization. The partial artifact correctly credits those results.

I checked [Jones–Naaijkens–Penneys v3](https://arxiv.org/abs/2506.19969v3), revised 21 September 2026, Section 4. Definition 4.3 uses the braided geometric inclusions, and Definition 4.12 requires one finite constant valid for both directions and for every bounded contractible region. A separate finite-region algebra isomorphism does not meet that definition.

The new [Faurot–Li–Penneys–Sherman v1](https://arxiv.org/abs/2609.20725v1), submitted 17 September 2026, Theorem B is indeed a braided monoidal equivalence with the opposite unitary ind-completion, in the authors' conventions. JNP v3 explicitly points to that result. This is evidence for the adjacent sector-category question; it is not a theorem identifying the concrete two nets. I checked the exact theorem scope and conventions, not every step of its Connes-fusion proof. The artifact does not overstate that audit.

The source's strong-generator choice matters. The finite fusion calculation is expressly for the sum of the three simple objects. The artifact does not assert that this fixes every alternative site multiplicity or reconstructs the geometric inclusions.

## 2. Laurent matrix and complementary subalgebra

I independently computed, over the integer/rational Laurent ring, that the displayed matrix $K$ obeys

$$\overline K^t=-K,\qquad \det K=4.$$

In characteristic three, the determinant is a unit equal to one. Therefore the stated adjugate is its inverse. There is no localization beyond Laurent monomials, so no nonlocal denominator is introduced.

For $V_+=(I,K/2)^t$ and $V_-=(I,-K/2)^t$, the exact block change of variables is

$$[V_+\;V_-]^{-1}
=\begin{pmatrix}I/2&K^{-1}\\I/2&-K^{-1}\end{pmatrix}.$$

Both products with this inverse were checked symbolically, as were the pairings $K,-K,0$. This proves uniqueness and existence of the decomposition for every finitely supported physical vector, independently of finite-window tests.

The identity X-block guarantees that distinct coefficient vectors give distinct Pauli exponent vectors. Consequently the multiplication map from the algebraic tensor product of the two commuting subalgebras is injective on the Pauli basis and surjective by the displayed inverse. The extension to minimal C*-tensor-product completions is justified: each finite collection is contained in finite-dimensional C*-subalgebras, and the injective *-homomorphism of their tensor product is isometric. These finite pieces exhaust the algebraic tensor product.

The projector has blocks $I/2,K^{-1},K/4,I/2$ over the rational Laurent ring. Reducing modulo three gives exactly the artifact's $2I,K^{-1},K,2I$. Its idempotence and action on both summands check out. The coefficient vectors enlarge physical support by at most one cell; applying $V_\pm$ gives the claimed conservative two-cell bound. In fact the final projector entries themselves have radius one, which is consistent with, and stronger than, the conservative bound. No correction or stronger claim is needed.

The Pauli sign convention is also correct: with $W(u,z)=X^uZ^z$ and $ZX=\zeta XZ$, the commutator exponent is $z\cdot u'-z'\cdot u$, the negative of the displayed symplectic pairing. This sign does not change its radical, rank or complementary orthogonality, and the artifact appropriately refrains from deducing chirality from it alone.

## 3. Finite-window algebra certificate

For a finite set $E$ of distinct translated generator labels, the identity X-block gives a linearly independent basis of $3^{|E|}$ Pauli monomials. The alternating matrix extracted from the Laurent coefficients is exactly the physical pairing on those generators: translating the two columns by $r,s$ takes the constant coefficient of $x^{s-r}K_{ij}$, hence the coefficient indexed by $r-s$.

I reconstructed that matrix from physical X/Z support vectors rather than from the submitted coefficient lookup. I then explicitly formed a symplectic basis, checked that its change-of-basis matrix is invertible modulo three, and verified every entry of the resulting canonical form. Odd-sized irregular windows provide genuine radical directions in these independent controls.

The proof of the block formula is valid. A monomial is central exactly when its exponent lies in the alternating radical. A symplectic pair generates a full $3\times3$ matrix algebra; different pairs commute. The radical generates a commutative finite-dimensional C*-algebra with dimension $3^z$, hence $3^z$ scalar summands. Tensoring these factors gives

$$A_E\cong\bigoplus_{3^z}M_{3^q}(\mathbb C),\qquad 2q+z=|E|.$$

The ordered qutrit monomials have cube equal to the identity, so there is no hidden phase-only relation that could reduce the basis dimension. The identity monomial, of course, has order one; the proof only needs order dividing three.

The finite-window distinctions in the artifact are essential and correct. A generator-center rectangle, a periodic quotient and all elements physically supported inside a given rectangle are not automatically the same algebra. The submitted checker treats periodic and open boundaries separately, and no region-net identification is inferred from either.

## 4. Fusion diagnostic and the unresolved map

For the pointed fusion law with group $\mathbb Z/3$ and $T=1+g+g^2$, the multiplicity of each charge in $T^{\otimes N}$ is $3^{N-1}$. I independently reproduced this by convolution, including $N=1$. Associators and braiding do not change these multiplicity counts; the counts also do not determine the inclusions between differently shaped regions.

Matching anyon labels, factoring the ambient qutrit algebra, or comparing finite matrix blocks is insufficient for Conjecture 2. A successful proof still needs a single compatible quasi-local *-isomorphism whose map and inverse have one region-independent support bound. Finite symplectic elimination has no such uniform locality guarantee. The artifact states this exact gap and does not claim either a full solution or a counterexample.

## 5. Reproduction and publication scope

From this review directory:

- `python independent_checks.py` reproduces the independent exact certificate
- `cd author_replay && python verify.py` reproduces the submitted receipt

The eight publication files are listed in `review_summary.json`. The frozen author artifact is included with its replay script because the script hashes it relative to the current directory. Source PDFs, inspection images and incidental stdout are not part of the publication bundle.

Recommended status remains **unsolved, 2/5**. Preserve the explicit prior credit, standard sum-of-simples qualification, finite-window/physical-net distinction, opposite-category convention and absence of a two-sided bounded-spread comparison map. No mandatory mathematical or source-scope edit is requested.
