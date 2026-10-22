# Independent reconstruction of Costakis Question 5

## Status and exact scope

**The universal preservation assertion is false.** In fact the following stronger statement is proved here:

> There is a dense set \(\mathcal B\subset H(\mathbb C)\) such that every \(f\in\mathcal B\) is hypercyclic for differentiation, but for every nonconstant complex polynomial \(p\), the function \(pf\) is not hypercyclic for differentiation. Moreover,
> \[
> |(pf)^{(n)}(0)|\longrightarrow\infty
> \quad(n\to\infty)
> \]
> for every such \(f,p\).

Thus the verified quantifiers are
\[
\exists\mathcal B\text{ dense in }H(\mathbb C)\quad
\forall f\in\mathcal B\quad
\bigl[f\in HC(D)\ \land\
\forall p\in\mathbb C[z]\setminus\mathbb C,\ pf\notin HC(D)\bigr].
\]
In particular this proves both \(\forall p\,\exists f\) and the stronger \(\exists f\,\forall p\), with the polynomial quantifier restricted to nonconstant polynomials. It does not assert that every hypercyclic function has this failure property.

This is a source-question reconstruction, not a novelty or date-of-discovery claim. No later priority literature has been consulted.

## Source authentication

The only historical mathematical source read was George Costakis, “Which maps preserve universal functions?”, in *Mini-Workshop: Complex Approximation and Universality*, Oberwolfach Report 6/2008, pp. 328–330. Definition 4 and Question 5 occur on printed p. 330, PDF page 34. The source defines \(HC(D)\) by density of the full derivative orbit and asks whether multiplying an arbitrary such entire function by a nonconstant polynomial preserves that property. Its neighboring Theorem 6 supplies a residual set on which all nonzero polynomial multiplications preserve hypercyclicity. That generic statement has different quantifiers from the universal statement being tested here.

- Original PDF: https://ems.press/content/serial-article-files/46147
- DOI supplied with the question: https://doi.org/10.4171/OWR/2008/06

The source is used to authenticate the question; none of its advanced hypercyclicity or growth results is needed below.

## 1. Ambient space and countable orbit-hitting conditions

Write \(\|f\|_R=\max_{|z|\le R}|f(z)|\). The compact-open topology on \(H(\mathbb C)\) is induced by
\[
 d(f,g)=\sum_{r=1}^{\infty}2^{-r}\min(1,\|f-g\|_r).
\]
It is complete: a Cauchy sequence converges uniformly on every closed disk, and its limit is entire by the elementary uniform-limit theorem for holomorphic functions. Differentiation of any fixed order is continuous by Cauchy's estimates.

Let \(\mathcal Q\) be the countable set of polynomials with coefficients in \(\mathbb Q+i\mathbb Q\). Taylor approximation followed by coefficient approximation shows that \(\mathcal Q\) is dense in \(H(\mathbb C)\).

For \(q\in\mathcal Q\) and positive integers \(R,s\), let
\[
 U(q,R,s)=\bigcup_{N\ge0}
 \{f\in H(\mathbb C):\|D^Nf-q\|_R<1/s\}.
\]
Every \(U(q,R,s)\) is open. An entire function belongs to all these sets exactly when its derivative orbit is dense. No finite truncation of an orbit is being used to certify this assertion.

## 2. The annular jet spaces

Put
\[
 \ell_n=\frac1{\sqrt{n+1}},\qquad
 u_n=\log(n+e),\qquad n\ge0.
\]
For each integer \(M\ge0\), define
\[
 X_M=\{f\in H(\mathbb C):
       \ell_n\le|f^{(n)}(0)|\le u_n\text{ for all }n\ge M\}.
\]
Each jet functional is continuous, so \(X_M\) is closed and hence complete. It is nonempty: the series
\[
 B_M(z)=\sum_{n=M}^{\infty}\ell_n\frac{z^n}{n!}
\]
defines an entire function belonging to \(X_M\). The lower and upper bounds are compatible because \(\ell_n\le1\le u_n\).

### Lemma

For every \(M\), every relative orbit-hitting set \(X_M\cap U(q,R,s)\) is open and dense in \(X_M\).

**Proof.** Only density needs proof. Fix \(g\in X_M\), a disk radius \(r>0\), and \(\delta>0\). A relative neighborhood of this form suffices because disk seminorms generate the topology. Write \(b_n=g^{(n)}(0)\). Choose \(L\ge M\) so large that
\[
 \left\|g-\sum_{n=0}^{L}b_n\frac{z^n}{n!}\right\|_r<\delta/4,
 \qquad
 \sum_{n>L}\ell_n\frac{r^n}{n!}<\delta/4.
\]
The function obtained by retaining the jets through \(L\) and setting all later jets equal to \(\ell_n\) is therefore within \(\delta/2\) of \(g\) on the \(r\)-disk.

Write the target in derivative-normalized form
\[
 q(z)=\sum_{k=0}^{d}\beta_k\frac{z^k}{k!}.
\]
For an integer \(N>L\), replace the jets at indices \(N,\ldots,N+d\) by numbers \(\gamma_{N,k}\) satisfying
\[
 |\gamma_{N,k}|\ge\ell_{N+k},\qquad
 |\gamma_{N,k}-\beta_k|\le\ell_{N+k}.
\]
For example, keep \(\beta_k\) if its modulus is at least \(\ell_{N+k}\); otherwise move it radially to that circle, using the positive real point when \(\beta_k=0\). Then
\[
 |\gamma_{N,k}|\le\max(|\beta_k|,1).
\]
Because \(u_n\to\infty\), all these finitely many modified jets also satisfy the upper bounds once \(N\) is sufficiently large. Denote the resulting entire function by \(F_N\). All other jets after \(L\) remain \(\ell_n\), so \(F_N\in X_M\).

The modification at the high block changes the function on the \(r\)-disk by at most
\[
 \sum_{k=0}^{d}
  (|\beta_k|+2)\frac{r^{N+k}}{(N+k)!}\longrightarrow0.
\]
Thus \(\|F_N-g\|_r<\delta\) for large \(N\). The retained polynomial prefix has degree less than \(N\), so it disappears under \(D^N\). The target block and subsequent baseline tail give
\[
\begin{aligned}
 \|D^NF_N-q\|_R
 &\le \sum_{k=0}^{d}|\gamma_{N,k}-\beta_k|\frac{R^k}{k!}
       +\sum_{k>d}\ell_{N+k}\frac{R^k}{k!}\\
 &\le \ell_N e^R\longrightarrow0.
\end{aligned}
\]
Taking \(N\) still larger makes this less than \(1/s\). This proves density. \(\square\)

Baire's theorem now proves that
\[
 \mathcal B_M:=X_M\cap HC(D)
 =\bigcap_{q\in\mathcal Q}\bigcap_{R,s\ge1}
   (X_M\cap U(q,R,s))
\]
is a dense \(G_\delta\) subset of \(X_M\), and in particular is nonempty. No invariance of \(X_M\) under differentiation is required: this is a direct application of Baire to the displayed open dense sets.

## 3. Every nonconstant polynomial product has escaping derivative values

Let \(f\in X_M\), and abbreviate \(a_n=f^{(n)}(0)\). Fix an arbitrary nonconstant polynomial
\[
 p(z)=\sum_{j=0}^{d}c_jz^j,\qquad d\ge1,\ c_d\ne0.
\]
For \(n\ge d\), Leibniz's rule gives the exact finite identity
\[
 (pf)^{(n)}(0)=\sum_{j=0}^{d}c_j(n)_j a_{n-j},
 \qquad (n)_j=\frac{n!}{(n-j)!}.
\]
For \(n\ge M+d\), the highest-degree contribution has modulus at least
\[
 |c_d|(n)_d\ell_{n-d}
 =|c_d|\frac{(n)_d}{\sqrt{n-d+1}}
 \sim |c_d|n^{d-1/2}.
\]
The sum of all lower-degree contributions has modulus at most
\[
 \sum_{j=0}^{d-1}|c_j|(n)_j u_{n-j}
 \le \left(\sum_{j=0}^{d-1}|c_j|\right)
       n^{d-1}\log(n+e).
\]
The ratio of this upper bound to the lower bound for the leading contribution is \(O_p(\log n/\sqrt n)\), which tends to zero. The reverse triangle inequality therefore yields
\[
 |(pf)^{(n)}(0)|\longrightarrow\infty.
\]
This argument applies to each arbitrary \(p\), for the same \(f\). No countable intersection over polynomials is needed, and their roots or coefficients need not be restricted.

Evaluation at zero is a continuous surjection from \(H(\mathbb C)\) to \(\mathbb C\). A scalar sequence whose modulus tends to infinity cannot be dense in \(\mathbb C\): its tail avoids, say, the unit disk, and a smaller open disk can be chosen within the unit disk avoiding its finitely many preceding values. Consequently the derivative orbit of \(pf\) is not dense in \(H(\mathbb C)\).

Applying this to \(f\in\mathcal B_M\) proves that each such function is a single simultaneous counterexample for every nonconstant polynomial.

## 4. Density in the full space

Define \(\mathcal B=\bigcup_{M\ge0}\mathcal B_M\). To see that \(\mathcal B\) is dense in \(H(\mathbb C)\), fix \(g\in H(\mathbb C)\), \(r>0\), and \(\varepsilon>0\). Choose a polynomial \(P\) with \(\|P-g\|_r<\varepsilon/3\). For sufficiently large \(M>\deg P\),
\[
 G_M(z)=P(z)+\sum_{n=M}^{\infty}\ell_n\frac{z^n}{n!}
\]
belongs to \(X_M\) and satisfies \(\|G_M-P\|_r<\varepsilon/3\). Since \(\mathcal B_M\) is dense in \(X_M\), choose \(f\in\mathcal B_M\) with \(\|f-G_M\|_r<\varepsilon/3\). Then \(\|f-g\|_r<\varepsilon\), proving the asserted density. In particular \(\mathcal B\) is also dense relative to \(HC(D)\).

## 5. Independent local perturbation mechanism for a fixed polynomial

A separate mechanism supplies a useful extension: a counterexample for any fixed nonconstant polynomial can be placed arbitrarily close to any given hypercyclic function while differing from it by a function whose derivatives tend locally uniformly to zero.

Fix \(h\in HC(D)\), a nonconstant polynomial \(p\), a root \(\alpha\) of multiplicity \(m\ge1\), and write
\[
 p(z)=\sum_{j=m}^{d}c_j(z-\alpha)^j,\quad c_m\ne0.
\]
Fix \(\rho>0\) and a cutoff \(K\ge0\). Put \(b_k=h^{(k)}(\alpha)\), set \(a_k=b_k\) for \(k<K\), and choose subsequent \(a_k\) recursively. At stage \(k\), define
\[
 C_k=c_m\frac{(k+m)!}{k!},\qquad
 B_k=\sum_{j=m+1}^{\min(d,k+m)}
 c_j\frac{(k+m)!}{(k+m-j)!}\,a_{k+m-j}.
\]
Every jet in \(B_k\) is already defined. Choose \(a_k\) such that
\[
 |C_ka_k+B_k|\ge\rho,\qquad
 |a_k-b_k|\le\frac{\rho}{|C_k|}.
\]
This is elementary disk avoidance: if \(S=C_kb_k+B_k\) already has modulus at least \(\rho\), take \(a_k=b_k\); otherwise move \(S\) radially to the circle of radius \(\rho\), using \(\rho\) itself when \(S=0\), and divide the displacement by \(C_k\).

The series
\[
 e(z)=\sum_{k=0}^{\infty}(a_k-b_k)\frac{(z-\alpha)^k}{k!},
 \qquad f=h+e,
\]
is entire, because
\[
 |a_k-b_k|\le\frac{\rho}{|c_m|}\frac{k!}{(k+m)!}.
\]
For all \(n\ge0\),
\[
 |e^{(n)}(z)|
 \le\frac{\rho}{|c_m|}\frac{n!}{(n+m)!}e^{|z-\alpha|}
 \longrightarrow0
\]
uniformly on compact sets. Every tail of a dense orbit in \(H(\mathbb C)\) is dense: removing finitely many points from a dense set in this space cannot remove all points from any nonempty open set, since the space has no isolated points. This tail density and the displayed convergence show that \(f=h+e\) remains hypercyclic.

By construction,
\[
 |(pf)^{(n)}(\alpha)|\ge\rho\quad(n\ge K+m).
\]
The finitely many earlier scalar values cannot make up the omitted disk, so \(pf\notin HC(D)\). The cutoff gives the sharper closeness estimate
\[
 \|e\|_{|z-\alpha|\le R}
 \le\frac{\rho}{|c_m|}\sum_{k\ge K}\frac{R^k}{(k+m)!}\longrightarrow0
 \quad(K\to\infty).
\]
This proves the announced local extension. It is not needed for Sections 2–4.

## 6. Boundary cases and limits of the conclusions

- A nonzero constant multiplier preserves \(HC(D)\): scalar multiplication is a homeomorphism commuting with differentiation. The zero multiplier does not. Therefore a polynomial multiplier sends **every** member of \(HC(D)\) into \(HC(D)\) exactly when it is a nonzero constant.
- The full derivative orbit includes \(n=0\). All non-hypercyclicity arguments explicitly allow finitely many exceptional initial values, so including or excluding finitely many derivatives does not affect the conclusion.
- All upper and lower coefficient bounds concern derivative-normalized jets \(f^{(n)}(0)\), not the ordinary coefficients \(f^{(n)}(0)/n!\). The factorials in the series, derivative identity, and estimates are consistent.
- The construction uses all required orbit-hitting conditions through Baire's theorem. No finite numerical sample certifies either hypercyclicity or infinite orbit exclusion.
- The original source's residual set of functions preserving all nonzero polynomial multiplications is compatible with a dense exceptional set; density is not residuality.
- No claim about later priority, publication readiness, or novelty follows from this reconstruction.

## Strongest verified result and exact remaining gap

The dense simultaneous-counterexample theorem at the start is the strongest result developed here. All of its mathematical steps are supplied above using elementary complex analysis and Baire category. There is no identified mathematical gap. A separate internal adversarial subagent checked both mechanisms, including the relative Baire topology, coefficient normalization, finite-prefix exceptions, the linear-polynomial case, and the quantifier order, and reported no substantive gap. Its review was restricted to the derivations supplied here and did not access candidates, other-family reports, or later literature. Any subsequent candidate/other-family comparison and any later priority search must occur after, and separately from, the immutable freeze.
