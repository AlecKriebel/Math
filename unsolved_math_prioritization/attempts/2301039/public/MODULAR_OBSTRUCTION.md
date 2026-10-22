# A modular-covering obstruction for Function Theory Problem 1.39

**Status:** a rigorously proved obstruction to one construction route. This is not a solution of Problem 1.39, an improvement of its growth bounds, or a claim of novelty. In particular, it supplies no admissible positive-index example. The argument below should be independently checked before reuse in a research claim.

## Result

Let

\[
 C(\tau)=\frac{\tau-i}{\tau+i},\qquad
 h(z)=\lambda\!\left(i\frac{1+z}{1-z}\right),
\]

where \(\lambda\) is the classical modular lambda function on the upper half-plane \(\mathbb H\). Then:

1. For every \(v\ne0\), the equation \(h'(z)=v\) has infinitely many solutions in the unit disk.
2. More generally, if \(R\) is a nonconstant rational function having a zero at at least one of \(0,1,\infty\), then \(f=R\circ h\) satisfies: \(f'(z)=v\) has infinitely many solutions for every \(v\ne0\). In particular this applies to every nonconstant rational \(R\) whose zeros on the sphere are all contained in \(\{0,1,\infty\}\).
3. For this symmetric normalization, the separate candidate \(g=h/h'\) satisfies \(g'(0)=1\).

Consequently neither a nonzero scalar multiple of the modular function, nor any nonconstant rational composition whose rational function has all its zeros in \(\{0,1,\infty\}\), satisfies the derivative-omission hypothesis of Problem 1.39. Those rational compositions are zero-free, as follows from the product and transformation formulas below. The quotient \(h/h'\), with exactly the displayed normalization, fails as well. The quotient assertion is not being claimed for arbitrary changes of disk coordinate.

The same rational-composition obstruction holds after any disk-automorphism precomposition; the coordinate explanation appears below.

## Why this route is tempting

The modular covering has positive logarithmic characteristic: the quoted form of Tsuji's theorem gives

\[
T(r,h)=\log\frac1{1-r}+O(1).
\]

Together with the zero-freeness proved from the product formula below, this quoted growth estimate makes the function a natural test object. The obstruction proves that its derivative assumes every nonzero complex value infinitely often.

Source for this contextual characteristic statement: [Sina Nadi, arXiv:2609.05835, Theorem 2.5 and its following proof, PDF page 7](https://arxiv.org/pdf/2609.05835#page=7), quoting Tsuji, Theorem XI.29. **Source gate:** Nadi's statement and following argument were inspected; Tsuji's full proof was not inspected here. This recently posted preprint concerns adjacent Problem 1.40; nothing here assumes that it settles Problem 1.39. The obstruction itself does not use the characteristic estimate, surjectivity of lambda, or its global local univalence.

## Source formulas

The following exact classical formulas were checked against the NIST Digital Library of Mathematical Functions:

\[
q=e^{\pi i\tau},\qquad
\lambda(\tau)=16q(1-8q+44q^2+\cdots),\quad |q|<1.
\tag{1}
\]

See [DLMF 23.15, nome convention](https://dlmf.nist.gov/23.15) and [DLMF 23.17.4](https://dlmf.nist.gov/23.17.E4). In particular, this is a convergent power series near \(q=0\), so it can be differentiated there, giving

\[
\lambda'(\tau)=16\pi i q(1+O(q)).
\tag{2}
\]

The modular transformation table [DLMF 23.18.1–23.18.3](https://dlmf.nist.gov/23.18) implies

\[
\begin{aligned}
\lambda(\tau+2)&=\lambda(\tau),\\
\lambda(-1/\tau)&=1-\lambda(\tau),\\
\lambda\!\left(\frac{\tau}{\tau+1}\right)&=\frac1{\lambda(\tau)}.
\end{aligned}
\tag{3}
\]

For clarity, the corresponding determinant-one matrices are

\[
\begin{pmatrix}1&2\\0&1\end{pmatrix},\qquad
\begin{pmatrix}0&-1\\1&0\end{pmatrix},\qquad
\begin{pmatrix}1&0\\1&1\end{pmatrix}.
\]

Their entry parities are respectively the first, second, and third cases of DLMF 23.18.2. The last two identities send the limiting value \(\lambda(i\infty)=0\) to 1 and infinity.

We also use the inspected exact product formula [DLMF 23.17.7](https://dlmf.nist.gov/23.17.E7):

\[
\lambda(\tau)=16q\prod_{n=1}^{\infty}
\left(\frac{1+q^{2n}}{1+q^{2n-1}}\right)^8.
\tag{P}
\]

For \(0<|q|<1\), every factor is nonzero, and the factor deviations from 1 have summable absolute values locally uniformly. The product therefore converges to a nonzero holomorphic value. In particular lambda is holomorphic and zero-free on \(\mathbb H\). The second transformation in (3) now also proves \(1-\lambda(\tau)\ne0\), since \(-1/\tau\in\mathbb H\). This derives omission of \(0,1,\infty\) without asserting surjectivity onto their complement.

## 1. Direct proof for the modular covering

Since \(h(C(\tau))=\lambda(\tau)\) and

\[
C'(\tau)=\frac{2i}{(\tau+i)^2},
\]

the chain rule and (2) give

\[
h'(C(\tau))
=\frac{(\tau+i)^2}{2i}\lambda'(\tau)
=8\pi(\tau+i)^2e^{\pi i\tau}
  \bigl(1+O(e^{\pi i\tau})\bigr)
\tag{4}
\]

as \(\operatorname{Im}\tau\to+\infty\). The error is uniform in \(\operatorname{Re}\tau\), because the underlying analytic expansion is in \(q\).

Fix \(v\ne0\). Choose a fixed argument \(\theta\) of \(v\), and set

\[
w_n=\frac{\theta}{\pi}
     +\frac{i}{\pi}\log\frac{32\pi n^2}{|v|}.
\tag{5}
\]

For all sufficiently large positive integers \(n\), these points lie in \(\mathbb H\), and

\[
e^{\pi i w_n}=\frac{v}{32\pi n^2},\qquad
|w_n|=O(\log n).
\]

For \(\zeta\) in any fixed bounded set, define

\[
G_n(\zeta)=\frac{h'(C(2n+w_n+\zeta))}{v}.
\]

Substitution into (4), using \(e^{2\pi i n}=1\), yields

\[
G_n(\zeta)
=\left(1+\frac{w_n+\zeta+i}{2n}\right)^2
 e^{\pi i\zeta}\bigl(1+O(n^{-2})\bigr).
\tag{6}
\]

Consequently

\[
G_n(\zeta)\longrightarrow e^{\pi i\zeta}
\]

locally uniformly in \(\zeta\); for each fixed compact set the error is \(O((\log n)/n)\).

On the circle \(|\zeta|=1/2\), the function \(e^{\pi i\zeta}-1\) has no zeros. It has precisely one zero, a simple zero at zero, in the enclosed disk: its complete zero set is \(2\mathbb Z\). Uniform convergence and Rouché's theorem therefore imply that, for every sufficiently large \(n\), \(G_n-1\) has one zero \(\zeta_n\) in \(|\zeta|<1/2\).

Thus

\[
h'(z_n)=v,\qquad z_n=C(2n+w_n+\zeta_n)\in\mathbb D.
\]

These points are distinct. Indeed the real parts of the half-plane centers \(2n+w_n\) differ by exactly two, and the radius-\(1/2\) disks around them are disjoint. The map \(C\) is injective. Also \(z_n\to1\), since the half-plane points tend to infinity. This proves assertion 1.

## 2. Rational compositions with a zero at a puncture, including all cusp chain factors

Let \(R\) be nonconstant rational and suppose explicitly that it has a zero at some \(b\in\{0,1,\infty\}\). Let the order of that zero in a local coordinate at \(b\) be \(m\ge1\).

This hypothesis includes every nonconstant rational map all of whose zeros lie in \(\{0,1,\infty\}\): a nonconstant rational map necessarily has a zero somewhere on the sphere. For this narrower algebraically specified family, the omission proved after (P) also ensures that \(R\circ h\) has no zeros in the disk. No surjectivity theorem is required for either assertion.

Choose \(M\in\mathrm{SL}_2(\mathbb Z)\) according to the following list:

\[
\begin{array}{c|c|c}
b&M&\lambda(M\tau)\\ \hline
0&\begin{pmatrix}1&0\\0&1\end{pmatrix}&\lambda(\tau)\\[4pt]
1&\begin{pmatrix}0&-1\\1&0\end{pmatrix}&1-\lambda(\tau)\\[4pt]
\infty&\begin{pmatrix}1&0\\1&1\end{pmatrix}&1/\lambda(\tau)
\end{array}
\]

Write the associated rational transformation of the lambda value as \(\sigma_b\), and put \(P(t)=R(\sigma_b(t))\). Then \(P\) is holomorphic near zero and has there a zero of order \(m\). This remains true for \(b=\infty\), because \(1/t\) is the correct inverse local coordinate at infinity. Thus

\[
P(t)=c_0t^m(1+O(t)),\qquad c_0\ne0.
\]

Let \(A=16^m c_0\ne0\). From (1), with convergence as a power series in \(q\),

\[
H(\tau):=P(\lambda(\tau))
       =Aq^m(1+O(q)),\qquad
H'(\tau)=m\pi i A q^m(1+O(q)).
\tag{7}
\]

These expansions show in particular that \(H\) is holomorphic high enough in the upper half-plane, even if \(R\) has other poles.

Write

\[
M=\begin{pmatrix}a&b_0\\c&d\end{pmatrix},\qquad ad-b_0c=1,
\]

and define \(\Psi=C\circ M\). Direct algebra gives

\[
\Psi(\tau)=
\frac{(a-ic)\tau+(b_0-id)}{(a+ic)\tau+(b_0+id)},
\qquad
\Psi'(\tau)=\frac{2i}{\bigl((a+ic)\tau+(b_0+id)\bigr)^2}.
\tag{8}
\]

The leading coefficient \(a+ic\) is nonzero: \(a,c\) are real and cannot both vanish. Set

\[
\beta=\frac{b_0+id}{a+ic},\qquad
K=\frac{m\pi A}{2}(a+ic)^2\ne0.
\]

Because \(f(\Psi(\tau))=H(\tau)\), equations (7)–(8) give the exact required coordinate factor:

\[
f'(\Psi(\tau))=
K(\tau+\beta)^2 e^{m\pi i\tau}
\bigl(1+O(e^{\pi i\tau})\bigr).
\tag{9}
\]

Fix \(v\ne0\) again. Choose a fixed argument \(\theta\) of \(v/K\), and put

\[
w_n=\frac{\theta}{m\pi}
 +\frac{i}{m\pi}\log\frac{4|K|n^2}{|v|}.
\]

Then \(e^{m\pi i w_n}=v/(4Kn^2)\), \(\operatorname{Im}w_n\to\infty\), and \(|w_n|=O(\log n)\). Equation (9), evaluated at \(\tau=2n+w_n+\zeta\), becomes

\[
\frac{f'(\Psi(2n+w_n+\zeta))}{v}
=\left(1+\frac{w_n+\zeta+\beta}{2n}\right)^2
e^{m\pi i\zeta}\bigl(1+O(n^{-2/m})\bigr)
\longrightarrow e^{m\pi i\zeta},
\tag{10}
\]

locally uniformly. Here \(m\) is an integer, so \(e^{2m\pi in}=1\). For a fixed compact set, the difference in (10) is

\[
O\left(\frac{\log n}{n}+n^{-2/m}\right).
\]

Apply Rouché on \(|\zeta|=1/(2m)\). The function \(e^{m\pi i\zeta}-1\) has exactly one zero in this disk, since its zeros are \(2k/m\), \(k\in\mathbb Z\). Thus \(f'=v\) has a solution associated with every sufficiently large \(n\). Distinctness follows from the disjoint half-plane disks and the injectivity of \(\Psi\), just as before. This proves assertion 2.

### Other disk normalizations

If \(h\) is replaced by \(h\circ\phi\), where \(\phi\) is a disk automorphism, replace \(C\) throughout this section by \(\phi^{-1}\circ C\). Its composition with \(M\) is again a conformal Möbius map from \(\mathbb H\) onto \(\mathbb D\). Such a map has derivative \(B/(u\tau+v_0)^2\), with \(B\ne0\) and \(u\ne0\). The latter follows because an affine nonconstant map cannot map the unbounded half-plane into the bounded disk. Its reciprocal derivative is therefore a quadratic polynomial with nonzero leading coefficient. Equation (9) retains precisely the same form, with new nonzero \(K\) and a new \(\beta\). The proof is unchanged. This checks the domain-coordinate dependence rather than presuming derivative omission is invariant under disk automorphisms.

## 3. The quotient \(h/h'\) fails at the center

The second identity in (3), and

\[
i\frac{1-z}{1+z}=-\frac1{i(1+z)/(1-z)},
\]

give \(h(-z)=1-h(z)\). It follows that \(h(0)=1/2\) and \(h''(0)=0\).

Here is an elementary verification of \(h'(0)\ne0\) directly from (P), without importing local univalence. For real \(0<q<1\), the product is positive; let \(L(q)\) denote its value. Logarithmic differentiation, justified locally uniformly by the convergent product, gives

\[
\frac{qL'(q)}{L(q)}
=1+8\sum_{n=1}^{\infty}
\left(\frac{2nq^{2n}}{1+q^{2n}}
 -\frac{(2n-1)q^{2n-1}}{1+q^{2n-1}}\right).
\]

Dropping the positive terms and increasing the magnitudes of the negative terms yields

\[
\frac{qL'(q)}{L(q)}
\ge 1-8\sum_{n=1}^{\infty}(2n-1)q^{2n-1}
=1-\frac{8q(1+q^2)}{(1-q^2)^2}.
\]

At \(\tau=i\), one has \(q=e^{-\pi}<1/16\): indeed \(\pi>3\) and the first five nonnegative terms of the exponential series already give \(e^3>16\). The positive-coefficient power series in the last bound is increasing in \(q\), so

\[
\frac{qL'(q)}{L(q)}
>1-\frac{8(1/16)(1+1/256)}{(1-1/256)^2}
=\frac{32129}{65025}>0.
\]

Thus \(L'(e^{-\pi})\ne0\), hence \(\lambda'(i)=\pi i e^{-\pi}L'(e^{-\pi})\ne0\), and the chain rule gives \(h'(0)=2i\lambda'(i)\ne0\).

Therefore, for \(g=h/h'\),

\[
g'(z)=1-\frac{h(z)h''(z)}{(h'(z))^2},\qquad
g'(0)=1.
\]

This is an exact local obstruction; no numerical calculation or growth estimate is involved.

## Source-gate ledger and conditional broader formulation

- **Inspected formulas used by the proofs:** DLMF's q-series, q-product, and modular transformation table, linked above. These classical identities are explicit imported identities; their complete derivations from theta functions are not reproduced here. The analytic arguments from those identities are given in full.
- **Not required:** lambda being onto \(\widehat{\mathbb C}\setminus\{0,1,\infty\}\), or being locally univalent throughout \(\mathbb H\). No complete proof of those covering facts was inspected in this verification pass. The local nonvanishing needed at the center was instead proved from (P).
- **Context only, uninspected original proof:** Tsuji's characteristic asymptotic, quoted in the inspected Nadi theorem.
- **Conditional broader corollary:** If one additionally imports the classical surjectivity statement, then every nonconstant rational \(R\) for which \(R\circ h\) is zero-free has all its zeros in \(\{0,1,\infty\}\), and therefore falls under section 2. This implication is the exact place where surjectivity would be used. The broader formulation is not counted here as passing a full-source verification gate.

## Reproducible algebra check

The companion `verify_modular_obstruction.py` checks the Möbius chain factors, the Cayley involution, and initial q-series derivative coefficients using exact symbolic arithmetic. It is a control against coefficient/sign mistakes, not a replacement for the analytic Rouché argument. Run it with Python and SymPy; it has no network access or external side effects.

## What remains open here

This note establishes only that the indicated modular families cannot provide an example for Problem 1.39. It does not determine the optimal analytic or meromorphic index, and it does not exclude non-rational constructions from the modular covering or unrelated constructions.
