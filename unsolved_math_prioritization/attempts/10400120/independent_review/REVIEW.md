# Independent adversarial review: Ohtsuki Conjecture 7.5 and SU(5) lens spaces

**Verdict: PASS — complete counterexample to the stated universal conjecture.** The justified campaign status is **claimed_solved**, subject to the explicit qualification that this is an AI-reviewed, unrefereed mathematical argument. No mandatory correction was identified. Novelty and priority are not established.

The frozen `COUNTEREXAMPLE.md` reviewed has SHA-256 `9e412983afbec39f2db103b38e771c0e45d2f5c30b433bd6a92459e9aeb4b6a6`. Its verifier has SHA-256 `608b10d88b1c57a05a230dd7b4ed954e6cc3305d810ccc804bd58754bcfebf1b`. Both are included unchanged in `author_replay/`.

The two exact squared magnitudes are independently confirmed:

\[
|\tau^{SU(5)}_{10}(L(5,1))|^2=3475+1550\sqrt5,
\qquad
|\tau^{SU(5)}_{10}(L(5,2))|^2=4025+1800\sqrt5,
\]

in the normalization \(\tau(S^3)=1\). Both are positive and their difference is \(550+250\sqrt5>0\). Both fundamental groups are \(\mathbb Z/5\). The independent verification below uses a root-lattice Gauss sum that reduces to five Weyl terms, rather than the submitted modular-matrix multiplication.

## 1. Original scope and admissible theory

[Ohtsuki's original collection](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf), Section7.1, printed pp.471–474, defines the quantum G invariant for closed oriented three-manifolds and uses the shifted parameter \(r=k+h^\vee\). Conjecture7.5 on p.474 says the absolute value, when nonzero, depends only on the fundamental group. The rendered page was inspected. The prime-level congruence in the preceding paragraph is a different statement; it imposes no prime-level hypothesis on Conjecture7.5.

SU(5) is simple, compact and simply connected. Its dual Coxeter number is 5, so WZW level k=5 corresponds to r=10. This is the full SU(5) theory, with the full weight lattice; it is not a PSU(5) or root-lattice-only theory, and it has no additional spin or bundle label.

[Hansen–Takata, arXiv:math/0209403v2](https://arxiv.org/abs/math/0209403), pp.26–27, constructs the modular category at r=mκ with κ≥h∨. In simply-laced type A4, m=1, so κ=r=10 is allowed. No coprimality of r and 5 is required for this construction. The index set consists of shifted weights in the open κ-alcove, namely the highest weights with four nonnegative Dynkin labels summing to at most 5, shifted by ρ. This gives exactly \(\binom94=126\) labels. The zero highest weight corresponds to the shifted vacuum ρ.

The convention for the quantum-group root in Hansen–Takata is \(e^{\pi i/r}\). Its Weyl-matrix entries use \(e^{-2\pi i\langle\lambda,\mu\rangle/r}\), exactly as specialized by the author. This is compatible with the square-root convention behind the source's displayed SU(2) quantum parameter; there is no additional factor-of-two level shift.

## 2. Surgery, orientation and normalization

[Guadagnini–Pilo](https://arxiv.org/abs/hep-th/9612090), equations(13), (16), (19) and (20), gives the vacuum matrix word for rational unknot surgery, with signature correction. The words for the continued fractions [5] and [3,2] are respectively

\[
ST^5S,\qquad ST^3ST^2S,
\]

since \(5/2=3-1/2\). Transposition reverses the chain without changing the vacuum entry because S and T are symmetric. The corresponding unknot fillings have fundamental groups cyclic of order 5, independently of the denominator. This follows also from van Kampen: the unknot longitude is trivial in its exterior group, so p/q filling adds the relation \(\mu^p=1\).

For a general group, there is no need to extrapolate Guadagnini–Pilo's explicit SU(2)/SU(3) normalization constants: Hansen–Takata's arbitrary-modular-category Corollary4.2 and equations(27)–(30) independently supply the same vacuum-word formula for the A4 category. Their convention defines L(p,q) by surgery coefficient −p/q, whereas Guadagnini–Pilo uses +p/q. This changes orientation conventions; the unitary invariant is conjugated under orientation reversal, so the displayed absolute values are unaffected. The independent computation also verifies q↔5−q explicitly.

Hansen–Takata uses \(\tau_{HT}(S^3)=D^{-1}=S_{00}\), where D is the positive total quantum dimension. Thus the normalization in the candidate is

\[
\tau_{\mathrm{norm}}(M)=\tau_{HT}(M)/S_{00}.
\]

Their surgery signature factors and the scalar distinguishing the modular T matrix from twists have modulus one. Removing these phases cannot alter either squared magnitude. Removing S's magnitude would be an error; the candidate retains it.

In type A4, rank=4, the number of positive roots is 10, and the root-lattice covolume is \(\sqrt5\), while the weight-lattice covolume is \(1/\sqrt5\). Equation(12) therefore gives the coefficient \(i^{10}/(10^2\sqrt5)=-1/(100\sqrt5)\) in S. With the author's integer coordinates y, the exponents in its equations(3) are correct: the S exponent in \(\zeta_{100}\) is \(-2\langle y,y'\rangle/5\), and the relative T exponent is \((|y|^2-250)/5\). All are integers. The omitted T scalar is a phase, not a missing magnitude.

## 3. Independent exact derivation from a different formula

Use Hansen–Takata **Theorem5.1**, printed p.39 of the cited preprint, whose displayed formula and preceding derivation were inspected. This is the general lens-space formula. The later “coprime case” simplification is **not** used, since gcd(10,5)=5.

Work in
\(\{x\in\mathbb R^5:\sum x_i=0\}\) with the usual Euclidean inner product. The coroot lattice is

\[
Y=\{\nu\in\mathbb Z^5:\sum_i\nu_i=0\},
\qquad \rho=(2,1,0,-1,-2).
\]

Its Weyl group permutes the five coordinates, its covolume is \(\sqrt5\), and \(|\rho|^2=10\). For p=5 and κ=10, Theorem5.1 specializes, up to a unit complex factor, to

\[
\tau_{HT}(L(5,q))=
\frac{-1}{2500\sqrt5}
\sum_{w\in S_5}\operatorname{sgn}(w)
 e^{-2\pi i\langle\rho,w\rho\rangle/50}
\sum_{\nu\in Y/5Y}
 e^{2\pi i q|\nu|^2}
 e^{2\pi i\langle\nu,q\rho-w\rho\rangle/5}.
\tag{A}
\]

Here the omitted factor is the Dedekind-sum phase in that theorem. The quadratic exponential in the inner sum is one. Taking the four simple roots \(e_i-e_{i+1}\) as a basis of Y, the remaining inner sum factors into four geometric sums of fifth roots of unity. It is 625 precisely when all five coordinates of \(q\rho-w\rho\) are congruent modulo5, and is zero otherwise.

The coordinates of ρ represent all five residue classes. For each fixed nonzero q modulo5, there are exactly five surviving permutations, one for each common residue of \(q\rho-w\rho\). Their signs and dot products can be listed without any numerical root evaluation:

| q | signs | dot products \(\langle\rho,w\rho\rangle\), with multiplicity |
|---|---|---|
| 1 | all +1 | 10 once; 0 twice; −5 twice |
| 2 | all −1 | 5 twice; −5 twice; 0 once |

Let \(w_0=e^{\pi i/5}\), a primitive tenth root. The surviving sums are

\[
\Sigma_1=2+2w_0+w_0^{-2},
\qquad
\Sigma_2=-(1+2w_0+2w_0^{-1}).
\]

Consequently (A) gives

\[
|\tau_{HT}(L(5,q))|^2=\frac{|\Sigma_q|^2}{80}.
\tag{B}
\]

All remaining algebra takes place in the degree-four field defined by
\(\Phi_{10}(x)=x^4-x^3+x^2-x+1\). Put

\[
u=w_0^2-w_0^3=2\cos(2\pi/5)=\frac{\sqrt5-1}{2},
\qquad u^2+u=1.
\]

Direct multiplication, with conjugation \(w_0\mapsto w_0^{-1}\), gives

\[
|\Sigma_1|^2=13+4u=11+2\sqrt5,
\qquad
|\Sigma_2|^2=13+8u=9+4\sqrt5.
\tag{C}
\]

The vacuum normalization can independently be obtained from the positive-root product in Hansen–Takata's equation(26). Positive roots of heights 1,2,3,4 occur 4,3,2,1 times. Their sine product is

\[
\prod_{\alpha>0}2\sin\frac{\pi\langle\alpha,\rho\rangle}{10}
=10u-5>0.
\]

For example, use \(2\sin(\pi/10)=u\), \(2\sin(3\pi/10)=1+u\), \((2\sin(\pi/5))^2=2-u\), and \((2\sin(\pi/5))(2\sin(2\pi/5))=\sqrt5\). The product reduces to \(u^2(2-u)\sqrt5=10u-5\). Therefore

\[
S_{00}^2=\frac{(10u-5)^2}{50000}
=\frac{125-200u}{50000}.
\tag{D}
\]

Dividing (B) by (D) yields

\[
|\tau_{\mathrm{norm}}(L(5,q))|^2
=\frac{625|\Sigma_q|^2}{125-200u}.
\]

Using (C) and \(u^2+u=1\), these ratios are exactly the two values claimed. The denominator is positive: either use the nonzero positive sine product, or \(0<u<5/8\), which follows from \(1<\sqrt5<9/4\). The two positive expressions are unequal. This independently settles both the nonvanishing and inequality requirements of the conjecture.

## 4. Audit of the submitted cyclotomic certificate

The submitted method enumerates the full 126-weight alcove and all 120 Weyl permutations, computes 8,001 symmetric S-numerator entries, and verifies seven final polynomial identities in \(\mathbb Z[\zeta_{100}]\). The reduction polynomial

\[
\Phi_{100}(x)=x^{40}-x^{30}+x^{20}-x^{10}+1
\]

is correct. Its chosen embedding has \(\zeta_{100}=e^{2\pi i/100}\), so the author's \(\zeta_{100}^{20}-\zeta_{100}^{30}\) is exactly the positive real u used above. Conjugation by inversion is correct. The Python arithmetic uses arbitrary-precision integers in NumPy object arrays, including convolution and reductions; it introduces no floating-point operation in the certificate.

I ran the verifier in a separate copied directory. Its receipt reproduced byte for byte, including the frozen artifact hash and all seven identities. The powers of 50000 in the two squared ratios are correct: the one-component word has two S factors before division by S00; the two-component word has three. The independent calculation in Section3 checks the resulting normalized magnitudes without depending on the author's matrix enumeration or polynomial coefficients.

The independent standard-library checker uses the A4 root basis, all 625 lattice residues, all 120 Weyl permutations, and four-coordinate \(\Phi_{10}\) arithmetic. It verifies **2,005 exact assertions**, including complete character-orthogonality sums for q=1,2,3,4, both phase norms, the root-product vacuum factor, both normalized values, and orientation-reversal controls. The 126-label alcove is also counted through a different parametrization by four-element subsets of {1,…,9}. The number of assertions does not count every arithmetic operation as a separate test.

## 5. Reproduction and publication limits

From this review directory:

```sh
python independent_checks.py > independent_results.replayed.json
cmp independent_results.replayed.json independent_results.json
```

The submitted replay requires NumPy and should be run from its directory, because it opens its snapshot by a relative path:

```sh
cd author_replay
python verify.py
```

`source_verification.json` records the primary PDF hashes and exact inspected locations. Publish only the files enumerated in `review_summary.json`; do not include source PDFs, rendered pages or caches.

The conclusion is a **complete negative answer to the stated all-group conjecture**, using ordinary SU(5) invariants at one allowed level and two lens spaces with the same fundamental group. It does not refute Guadagnini–Pilo's SU(2) lens-space theorem, which is a restricted result, or assert a counterexample within their SU(3) numerical sample. It does not assert homotopy equivalence of the pair, a smallest counterexample, a general classification, or a new discovery. The standard modular-category and surgery theorems are clearly identified imported inputs, not re-proved quantum-group foundations. Within that normal theorem-dependent mathematical scope, no unresolved gap was found.
