# Positive coarse curvature without a nonreversible L2 gap

Target: row 1712, problem ID **4000005**, **AMR-039-0005**, “Non-reversible spectral gap.”

## Attribution and exact conclusion

The basic counterexample is already published: Gong, Liu and Wen, *Ricci curvature of Markov chains on Polish spaces revisited*, Osaka J. Math. 50 (2013), 491–502, §3, p. 495, explicitly credit it to Fu-Zhou Gong and Li-Ming Wu. This is an independently checked reconstruction, with elementary operator and finite-approximation details. No novelty is asserted. [Publication](https://ir.library.osaka-u.ac.jp/repo/ouka/all/25089/ojm50_02_491.pdf)

For every \(0<a<1\), there is a compact Polish metric space with a Feller Markov kernel, a unique full-support stationary probability, and coarse Ricci curvature exactly \(1-a\), whose averaging operator \(P\) on complex mean-zero \(L^2\) satisfies

\[
\|P^n\|=1\quad(n\geq1),\qquad
r(P)=1,\qquad
\operatorname{spec}(P)=\{z\in\mathbb C:|z|\leq1\}.
\]

No finite constant controls variance by any of the three energies in §5 below. All witnesses for these inequalities are Lipschitz cylinder functions. The chain is nonreversible. It is topologically irreducible but is **not** irreducible with respect to its stationary probability in the general-state-space hitting sense. This last distinction does not violate the original problem's hypotheses.

Finite, irreducible, aperiodic truncations retain a uniform positive curvature lower bound, yet their ordinary Poincaré constants diverge. Their mean-zero spectral radii are zero, and their finite-rank realizations converge strongly to \(P\), whose spectral radius is one. This obstructs the proposed naive passage from finite spectral-radius estimates to an infinite nonreversible estimate. It does not rule out every approximation theorem with additional uniform assumptions.

## 1. Metric space, kernel, and stationary law

Let \(X=\{0,1\}^{\mathbb N_0}\). For distinct \(x,y\), let

\[
 j(x,y)=\min\{j\geq0:x_j\ne y_j\},\qquad d_a(x,y)=a^{j(x,y)};
 \qquad d_a(x,x)=0.
\]

This is an ultrametric: if both \(x,y\) and \(y,z\) agree in their first \(k\) coordinates, so do \(x,z\). Its topology is precisely the product topology. The space is compact by the product compactness theorem (or the diagonal subsequence argument), complete by coordinatewise stabilization of Cauchy sequences, and separable because eventually-zero sequences are a countable dense subset. Its diameter is one. Consequently every Borel probability on it has every positive metric moment finite.

Write \(bx=(b,x_0,x_1,\ldots)\) and \(Sx=(x_1,x_2,\ldots)\). Define

\[
 K(x,\cdot)=\tfrac12\delta_{0x}+\tfrac12\delta_{1x},\qquad
 (Pf)(x)=\tfrac12[f(0x)+f(1x)].
\]

Both maps \(x\mapsto bx\) are continuous, so \(K\) is a Borel Markov kernel and \(P\) maps \(C(X)\) into itself. This is the Feller property. Let \(\pi\) be the product of fair Bernoulli laws. If \(Z\sim\pi\) and \(B\) is an independent fair bit, then \(BZ\sim\pi\). Hence \(\pi K=\pi\). Every nonempty cylinder has positive probability, so \(\pi\) has full support.

For this kernel the one-step two-sample diffusion quantity used in Ollivier's paper is finite even quantitatively:

\[
 \sigma(x)^2=\tfrac12\iint d_a(y,z)^2K(x,dy)K(x,dz)=\tfrac14,
 \qquad \sigma_\infty=\tfrac12\operatorname{diam}(\operatorname{supp}K_x)=\tfrac12.
\]

Thus the issue is not a missing first moment, an infinite diffusion variance, a non-Polish topology, or nonexistence of stationarity.

## 2. Exact coarse Ricci curvature

By definition \(\kappa(x,y)=1-W_1(K_x,K_y)/d_a(x,y)\). Prepend the same fair bit to \(x\) and \(y\). This coupling gives

\[
 W_1(K_x,K_y)\leq a\,d_a(x,y).
\]

In fact equality holds. If \(j=j(x,y)\), every matched pair with the same prepended bit has cost \(a^{j+1}\); every pair with different prepended bits has cost \(1\). These are all four possible pairs in the two supports. Since \(a^{j+1}<1\), every coupling has expected cost at least \(a^{j+1}\), attained by the same-bit coupling. Therefore

\[
 W_1(K_x,K_y)=a\,d_a(x,y),\qquad\kappa(x,y)=1-a.
\]

In particular \(a=1/2\) gives the published counterexample, while taking \(a\downarrow0\) makes the lower curvature bound arbitrarily close to one. The case \(a=0\) is not included.

The same coupling extends to arbitrary initial laws and yields \(W_1(\mu K,\nu K)\leq aW_1(\mu,\nu)\). If both laws are invariant, their Wasserstein distance is at most \(a\) times itself, hence is zero. This proves uniqueness of \(\pi\). Also \(W_1(\delta_x K^n,\pi)\leq a^n\), using diameter one.

## 3. Hilbert-space domains and the adjoint

Use the complex Hilbert space \(L^2(\pi;\mathbb C)\), inner product

\[
 \langle f,g\rangle=\int\overline f\,g\,d\pi,
\]

and its closed subspace \(H=\{f:\int f\,d\pi=0\}\). The quotient by constants is canonically isometric to \(H\), by subtracting the mean. Jensen's inequality and stationarity give

\[
 \|Pf\|_2^2\leq\int P|f|^2\,d\pi=\|f\|_2^2.
\]

This makes \(P\) a well-defined bounded operator on equivalence classes with domain all of \(L^2\), preserving \(H\). There is no unbounded-operator domain issue.

Let \(Ug=g\circ S\). Since \(S\) preserves \(\pi\), \(U\) is an isometry on \(L^2\), also preserving \(H\). For bounded functions, product integration gives

\[
 \langle f,Ug\rangle
 =\tfrac12\sum_{b=0}^1\int\overline{f(bx)}g(x)\,d\pi(x)
 =\langle Pf,g\rangle.
\]

Density extends this identity to all \(L^2\), so \(P^*=U\). Consequently

\[
 PP^*=I,\qquad
 (P^*Pf)(x)=\tfrac12[f(0Sx)+f(1Sx)]
 =\mathbb E_\pi[f\mid x_1,x_2,\ldots](x).
\]

Thus \(P\) is a coisometry and \(P^*P\) is a proper orthogonal projection, rather than the identity.

**Printed adjoint-order error.** On p. 495 the publication explicitly defines its \(M\) by prepending a random bit, and subsequently prints \(M^*M=I\). Under that very convention the correct identity is \(MM^*=I\). Indeed \(e_0(x)=(-1)^{x_0}\) is nonzero and \(Me_0=0\), immediately ruling out \(M^*M=I\). This is a local algebraic correction to the displayed operator identity, not an assertion that the authors issued an erratum or that their spectral-radius conclusion is wrong. The independent argument below proves that conclusion without relying on the printed identity.

## 4. Spectrum, norms, and what convergence still holds

Put \(e_j(x)=(-1)^{x_j}\), \(j\geq0\). These form an orthonormal sequence in \(H\), and direct substitution gives

\[
 Pe_0=0,\qquad Pe_j=e_{j-1}\ (j\geq1).
\]

For every \(n\geq1\), \(P^ne_n=e_0\). Contractivity therefore implies \(\|P^n|_H\|=1\); the spectral-radius formula gives \(r(P|_H)=1\). Alternatively \((P^n)(P^*)^n=I\) yields the same norm conclusion.

For any \(z\in\mathbb C\) with \(|z|<1\), the series

\[
 h_z=\sum_{j=0}^{\infty}z^je_j
\]

converges in \(H\) (indeed uniformly on \(X\)), is nonzero with squared norm \(1/(1-|z|^2)\), and satisfies \(Ph_z=zh_z\). The open disk is therefore contained in the point spectrum. The spectrum is closed and lies in the closed unit disk by contractivity; hence it is exactly that disk. Complexification is explicit here; the real variance witnesses below require no complex coefficients.

Despite the spectral-radius statement, \(P^nf\to0\) in \(L^2\) for every \(f\in H\). To see this, a mean-zero function depending on the first \(L\) coordinates is killed by \(P^L\). Such functions are dense in \(H\) by conditional expectation onto the increasing coordinate sigma-algebras. Approximation and contractivity now prove convergence for arbitrary \(f\). In particular \(1\) is not an eigenvalue on \(H\), even though it belongs to its spectrum; more generally there are no unit-modulus eigenvalues on \(H\). Stationary correlations therefore converge to their product values. Strong convergence of powers is different from decay of their operator norms.

The kernel is nonreversible: \(\langle e_0,Pe_1\rangle=1\), whereas \(\langle Pe_0,e_1\rangle=0\). Invariance must not be confused with detailed balance.

Lipschitz contraction also remains valid. With the Lipschitz seminorm, \(\operatorname{Lip}(Pf)\leq a\operatorname{Lip}(f)\). The mean-zero Lipschitz space, with this norm, is complete because \(|f(x)|\leq\operatorname{Lip}(f)\) on a diameter-one space when the mean is zero. In fact its spectral radius is \(a\): the contraction gives the upper bound, and \(h_a\) is a Lipschitz eigenfunction of eigenvalue \(a\), since for a first disagreement at coordinate \(k\),

\[
 |h_a(x)-h_a(y)|\leq2\sum_{j\geq k}a^j=\frac{2}{1-a}d_a(x,y).
\]

These Lipschitz and \(L^2\) spectral radii refer to different Banach-space norms.

## 5. Three precise variance inequalities that fail

For complex \(f\in L^2\), let \(\operatorname{Var}_\pi(f)=\|f-\pi f\|_2^2\). Define the ordinary stationary jump energy

\[
 \mathcal E(f)=\tfrac12\iint|f(y)-f(x)|^2\,\pi(dx)K(x,dy).
\]

Its domain is all \(L^2\); stationarity and Cauchy–Schwarz justify all integrals. Expanding the square gives

\[
 \mathcal E(f)=\operatorname{Re}\langle f,(I-P)f\rangle
 =\langle f,(I-(P+P^*)/2)f\rangle.
\]

For real functions the real-part sign is unnecessary. This identifies the energy with the additive symmetrization, not with the spectral radius of a nonnormal \(P\).

Take the real cylinder functions

\[
 f_N=N^{-1/2}\sum_{j=0}^{N-1}e_j.
\]

Orthogonality gives

\[
 \operatorname{Var}_\pi(f_N)=1,\qquad
 (I-P)f_N=N^{-1/2}e_{N-1},\qquad
 \mathcal E(f_N)=1/N,\qquad
 \|(I-P)f_N\|_2^2=1/N.
\]

Consequently neither \(\operatorname{Var}_\pi(f)\leq C\mathcal E(f)\) nor \(\operatorname{Var}_\pi(f)\leq C\|(I-P)f\|_2^2\) can hold for any finite \(C\). Each \(e_j\) has Lipschitz constant \(2a^{-j}\); hence each \(f_N\) is Lipschitz. No uniform bound on these constants is required to contradict a homogeneous variance/energy inequality.

The conditional-variance energy is a third, distinct quantity:

\[
 \mathcal V(f)=\int\operatorname{Var}_{K_x}(f)\,d\pi(x)
 =\|f\|_2^2-\|Pf\|_2^2
 =\langle f,(I-P^*P)f\rangle.
\]

For \(f=e_1\), both values \(e_1(0x)\) and \(e_1(1x)\) equal \(e_0(x)\). Thus \(\mathcal V(e_1)=0\), while \(\operatorname{Var}_\pi(e_1)=1\). No variance bound by this energy is possible either. The failure is stronger than merely a poor constant.

These three conclusions concern the displayed energies only. They do not deny a Poincaré inequality with Ollivier's different nonlocal, blurred gradient.

## 6. Irreducibility and topology

For a cylinder specifying its first \(L\) bits, the probability of being in it after \(L\) steps is \(2^{-L}\), from every initial state. Every nonempty open set contains such a cylinder. Thus every nonempty open set is reachable with positive probability from every state: topological irreducibility holds.

In contrast, from a fixed \(x\) every state reached at a finite time has the form \(wx\) for some finite word \(w\). The union \(R_x\) of all such states, including \(x\), is countable and \(\pi(R_x)=0\). The full-\(\pi\)-measure Borel set \(X\setminus R_x\) is never reached from \(x\). Hence the chain is not \(\pi\)-irreducible. It is not irreducible with respect to any common nonzero measure: the reachable sets from the all-zero and all-one sequences are disjoint, while a putative irreducibility measure would have to be supported on each.

Likewise \(K^n(x,\cdot)\) is finitely supported and singular with respect to \(\pi\) for each finite \(n\), so its total-variation distance from \(\pi\), in the supremum-over-events convention, is one. This is compatible with its exponential Wasserstein convergence and the \(L^2\) convergence of averaged observables established above.

Therefore this example cannot be presented as a counterexample within an additionally imposed Harris/measure-irreducible class. No such hypothesis occurs in the original general metric random-walk definition or in Problem E.

## 7. Finite approximations and exact Poincaré constants

For \(L\geq1\), let \(X_L=\{0,1\}^L\), with first-disagreement metric \(d_a\), and define

\[
 K_L(x,\cdot)=\tfrac12\delta_{(0,x_0,\ldots,x_{L-2})}
             +\tfrac12\delta_{(1,x_0,\ldots,x_{L-2})}.
\]

For \(L=1\), the displayed retained prefix is empty. Let \(\pi_L\) be uniform. Independent coordinates show stationarity. After \(L\) steps all original bits are discarded and the state is uniformly distributed, so \(P_L^L=\Pi_L\), the projection onto constants. Every entry of the \(L\)-step transition matrix equals \(2^{-L}>0\). This proves irreducibility. The all-zero state has a self-loop, proving aperiodicity. For \(L\geq2\) the same \(e_0,e_1\) test proves nonreversibility.

If \(x,y\) first differ before their last coordinate, the same two-support calculation as in §2 gives curvature \(1-a\). If they first differ at the last coordinate, their transition laws are identical and curvature is one. Thus the curvature infimum is \(1-a\) for \(L\geq2\), and one for \(L=1\).

On \(H_L=L^2_0(\pi_L;\mathbb C)\), \(P_L^L=0\); hence its spectrum is \(\{0\}\) and its spectral radius is zero. Its norm is one for \(L\geq2\), with witness \(e_1\), and zero for \(L=1\). More precisely \(\|P_L^n|_{H_L}\|=1\) for \(0\leq n<L\) and zero for \(n\geq L\). The functions \(f_L\) from §5 have variance one and ordinary energy \(1/L\). Conditional-variance coercivity already fails on each \(X_L\) with \(L\geq2\), using \(e_1\).

One can calculate the **exact ordinary Poincaré gap**:

\[
 \gamma_L=\inf_{0\ne f\in H_L}\frac{\mathcal E_L(f)}{\|f\|_2^2}
 =1-\cos\frac{\pi}{L+1}.
\]

Here is a proof covering all functions, not just linear ones. The Walsh characters \(w_A=\prod_{j\in A}e_j\), for nonempty \(A\subseteq\{0,\ldots,L-1\}\), are an orthonormal basis of \(H_L\). Direct averaging gives \(P_Lw_A=0\) if \(0\in A\), and \(P_Lw_A=w_{A-1}\) otherwise. Every \(A\) has a unique representation \(B+n\) with \(\min B=0\). For each such \(B\), the characters \(w_B,w_{B+1},\ldots,w_{B+m-1}\), where \(m=L-\max B\), form an orthogonal reducing block for \(P_L\) and its finite-dimensional adjoint. On that block \(P_L\) is the length-\(m\) backward shift \(J_m\).

The symmetric matrix \((J_m+J_m^*)/2\) has off-diagonal entries \(1/2\). For \(r=1,\ldots,m\), the vector with coordinates \(\sin((j+1)r\pi/(m+1))\), \(0\leq j<m\), has eigenvalue \(\cos(r\pi/(m+1))\), by the sine addition formula and zero boundary values. These \(m\) distinct eigenvalues exhaust its spectrum. Its largest eigenvalue is \(\cos(\pi/(m+1))\), maximized over blocks by \(m=L\), the block \(B=\{0\}\). Taking the smallest eigenvalue of \(I-(P_L+P_L^*)/2\) proves the formula.

Thus the sharp Poincaré constant is

\[
 C_L=\frac1{1-\cos(\pi/(L+1))}
 \sim\frac{2(L+1)^2}{\pi^2}\longrightarrow\infty.
\]

This is entirely consistent with finite-dimensional spectral radius zero: \(P_L\) is nonnormal, and the ordinary energy belongs to its additive symmetrization.

Finally identify \(L^2(\pi_L)\) isometrically with functions of the first \(L\) coordinates in \(L^2(\pi)\). Under this identification the restriction of \(P\) is \(P_L\), so finite and infinite dynamics agree on such functions at every time. Let \(Q_L\) be conditional expectation onto these coordinates and put \(A_L=PQ_L\) on the common space \(H\). Then \(A_L^L=0\), \(A_L\to P\) strongly, and each \(A_L\) is finite rank. Nevertheless \(r(A_L)=0\) and \(r(P)=1\). This convergence is not operator-norm convergence: for every \(L\geq1\),

\[
 Q_Le_L=0,\quad Pe_L=e_{L-1},\quad\|P-A_L\|=1.
\]

The lower bound is this witness; the upper bound follows from \(P-A_L=P(I-Q_L)\), with both factors contractions. A uniform estimate \(\|P_L^n\|\leq C\rho^n\) with \(\rho<1\), \(C<\infty\) independent of \(L\), is impossible: choose \(L>n\). The finite spectral-radius theorem contains no such uniform prefactor.

## 8. Source hypotheses and scope of the correction

Ollivier's *Discrete Ricci curvature: Open problems*, Problem E, p. 2, asks separately about spectral radius, operator norm, Poincaré inequalities, and finite approximation, while explicitly distinguishing a blurred-gradient inequality. It is an open-ended question, not a conjecture specifying all possible additional hypotheses. [Problem list](https://www.yann-ollivier.org/rech/publs/problems_curvmarkov.pdf)

The underlying published framework requires a Polish space, a measurably varying Borel kernel, and finite first moments (Definition 1, p. 813); curvature is Definition 3. Proposition 30, p. 831, assumes finite average diffusion variance and either reversibility or finite \(X\), and concludes a spectral-radius bound. Corollary 31, p. 832, adds reversibility for the stated local Poincaré inequalities. Theorem 45, pp. 843–844, uses a different nonlocal gradient. The construction above satisfies the common metric and moment assumptions; it deliberately lacks reversibility. [Ollivier, JFA 256 (2009), 810–864](https://www.math.uchicago.edu/~shmuel/QuantCourse%20/Metric%20Space/Olliver%2C%20Ricci%20curvature%20of%20markov%20chains.pdf)

Erbar and Fathi's *Poincaré, modified logarithmic Sobolev and isoperimetric inequalities for Markov chains with non-negative Ricci curvature*, arXiv:1612.00514v1, explicitly works with an irreducible reversible continuous-time chain on a finite space (introduction p. 2 and §2.1 p. 4). Its curvature is entropic Ricci curvature, defined by entropy convexity for a different transportation geometry (§2.1, Definition 2.1). This source does not establish the nonreversible coarse-curvature extension attributed to it in the imported record. That citation's scope should be corrected without making a global claim that no other nonreversible result exists. [Erbar–Fathi](https://arxiv.org/abs/1612.00514)

**Recommended conclusion:** the unrestricted extension to a strict \(L^2\) spectral-radius/norm bound, and to either displayed local Poincaré energy, has a known negative answer. The present calculation also explains why uniform positive curvature plus consistent finite approximations alone does not transfer the finite spectral-radius estimate. Sharp estimates under further assumptions, other functional inequalities, and stronger approximation frameworks are outside this conclusion. In particular, no reversible spectral-gap theorem is contradicted.
