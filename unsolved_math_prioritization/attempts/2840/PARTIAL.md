# Giroux torsion: a volume degeneration bound and two scope obstructions

**Target:** 2840 / KP-3.42.  
**Status:** original closed-manifold question unresolved after two approaches; scoped partial deductions awaiting separate review. No novelty or human-peer-review claim.

## 1. Exact question and conventions

Problem 3.42 of the actual [K3 manuscript](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf), printed p.162, asks whether every tight contact 3-manifold has finite Giroux torsion. The introduction to its contact-topology section, printed p.160, starts with **closed** 3-manifolds and ordinarily assumes coorientability. It defines torsion using contact embeddings of
\[
(D,\ker\beta_n),\qquad
D=T^2\times[0,1],\qquad
\beta_n=\cos(2\pi nz)\,dx-\sin(2\pi nz)\,dy,
\tag{1}
\]
where \(n\ge1\) is an integer and \(x,y\) have period one. The torsion is the supremum of such integers, or zero if there are none.

The intended target is finiteness for each **fixed** closed contact manifold. Neither unbounded torsion across varying contact structures nor a noncompact infinite-torsion example disproves it. A contact immersion or covering map is not the required embedding.

We work in the smooth, cooriented setting, with the orientation induced by a chosen contact form. The elementary deductions below require no tightness except where standard tight examples are explicitly identified.

## 2. A quantitative consequence of finite contact volume

Let \(Y\) be a closed cooriented contact 3-manifold with contact form \(\alpha\), and set
\[
V_\alpha=\int_Y\alpha\wedge d\alpha>0.
\]
Give D its flat product metric and volume \(dx\,dy\,dz\), whose total mass is one.

**Proposition.** For every contact embedding
\[
\phi:(D,\ker\beta_n)\longrightarrow(Y,\ker\alpha)
\]
there is a smooth nowhere-zero function \(f\) with \(\phi^*\alpha=f\beta_n\), and
\[
2\pi n\int_D f^2\,dx\,dy\,dz\le V_\alpha.
\tag{2}
\]
Consequently
\[
\min_D|f|\le\sqrt{\frac{V_\alpha}{2\pi n}},\qquad
\operatorname{vol}\{|f|\ge\varepsilon\}
\le\frac{V_\alpha}{2\pi n\varepsilon^2}.
\tag{3}
\]

**Proof.** The two nowhere-zero forms have the same kernel, so their ratio f is smooth and nowhere zero. Its sign is irrelevant here. Direct differentiation gives
\[
\beta_n\wedge d\beta_n=2\pi n\,dx\wedge dy\wedge dz.
\]
Moreover,
\[
(f\beta_n)\wedge d(f\beta_n)
=f^2\beta_n\wedge d\beta_n,
\]
because the term with two copies of \(\beta_n\) vanishes. Change of variables for the embedding identifies the resulting integral with the contact volume of its image, which is at most \(V_\alpha\). The first bound in (3) follows from the unit volume of D, and the second from integrating \(f^2\ge\varepsilon^2\) on the indicated set. \(\square\)

This proves a genuine necessary degeneration for a hypothetical infinite-torsion structure: for any sequence of embeddings with \(n\to\infty\), the conformal factors converge to zero in \(L^2(D)\), and hence in measure, in the fixed model normalization (1).

There is also a metric version. Fix any Riemannian metric on Y and write
\[
m_\alpha=\min_Y|\alpha|>0,\qquad
L_\phi=\max_D\|(D\phi)^{-1}\|.
\]
The inverse is taken between the three-dimensional tangent spaces, using the specified metrics. Since \(|\beta_n|=1\),
\[
|f|=|(D\phi)^*\alpha|
\ge \frac{|\alpha_{\phi(\cdot)}|}{\|(D\phi)^{-1}\|}
\ge \frac{m_\alpha}{L_\phi}.
\]
Combining this with (2) gives
\[
L_\phi\ge m_\alpha\sqrt{\frac{2\pi n}{V_\alpha}}.
\tag{4}
\]
Thus a uniform bound on inverse derivatives of such embeddings would imply finite torsion. These are estimates in a fixed contact-form and metric normalization, not new contact invariants.

The missing step is precisely the existence of suitable uniform control from tightness. Compactness of Y alone gives no such control on a sequence of embeddings.

## 3. A pointwise lower bound for all embeddings is impossible

One particularly strong attempted normalization would require \(\min|f|\) to be bounded below over all torsion embeddings into a fixed tight manifold. That fails even for embeddings of the one-turn domain.

**Proposition.** If a closed cooriented contact manifold \((Y,\ker\alpha)\) admits one torsion-domain embedding \(\phi\), then for each \(T>0\) there is a contactomorphism \(\psi_T\) of Y, isotopic to the identity and supported in a Darboux chart, for which the conformal factor of \(\psi_T\circ\phi\) at a fixed interior point of D is \(e^{-2T}\) times that of \(\phi\).

**Proof.** Choose an interior point a of D and Darboux coordinates \((q,p,t)\) centered at \(\phi(a)\), with contact structure \(\ker\gamma\), where
\[
\gamma=dq+p\,dt.
\]
The actual form \(\alpha\) in this chart may be \(b\gamma\) for a smooth nowhere-zero b; no strict-form Darboux normalization is needed.

For a smooth Hamiltonian H, the vector field
\[
X_H=(H-pH_p)\partial_q+(pH_q-H_t)\partial_p+H_p\partial_t
\tag{5}
\]
satisfies \(\gamma(X_H)=H\) and
\[
\mathcal L_{X_H}\gamma=H_q\gamma.
\]
Choose a smooth cutoff supported in the chart and identically one near the origin, and multiply \(H_0=2q+pt\) by it. Near the origin, (5) becomes
\[
X_{H_0}=2q\,\partial_q+p\,\partial_p+t\,\partial_t.
\]
The cutoff contact field extends by zero to Y and has a complete flow, because Y is closed. The origin is fixed. At that fixed point, the derivative of its time-s flow is
\[
\operatorname{diag}(e^{2s},e^s,e^s),
\]
and the pullback of \(\gamma\) scales by \(e^{2s}\). The same factor applies to \(\alpha=b\gamma\) at the fixed point, because the value of b there cancels. Take the time-\(-T\) map. Composition with \(\phi\) gives the asserted factor at a and preserves contact embeddedness. \(\square\)

Section 4 supplies a fixed closed universally tight example admitting a one-turn domain, so this failure occurs in the tight class itself. It does **not** disprove the existence of specially chosen, better normalized representatives or of a uniform lower bound on their \(L^2\) masses. A small value at one point is not a small integral. The proposition rules out only the automatic pointwise bound over every embedding.

## 4. Closed torus families and the noncompact model

The following are standard contact models, included to keep the quantifiers explicit and credited to the established theory. The tightness input is Bennequin's theorem for standard contact \(\mathbb R^3\); [Colin, printed p.270](https://www.numdam.org/item/ASENS_2001_4_34_2_267_0.pdf) explicitly records the resulting universal tightness of the rotating torus structures.

For each integer \(k\ge1\), put on \(T^3=\mathbb R^3/\mathbb Z^3\)
\[
\alpha_k=\cos(2\pi kz)\,dx-\sin(2\pi kz)\,dy,\qquad
\xi_k=\ker\alpha_k.
\tag{6}
\]
These are well-defined positive contact forms, since
\[
\alpha_k\wedge d\alpha_k
=2\pi k\,dx\wedge dy\wedge dz.
\]
On the universal cover, define
\[
Q=x\cos(2\pi kz)-y\sin(2\pi kz),\quad
P=2\pi k\bigl(x\sin(2\pi kz)+y\cos(2\pi kz)\bigr),\quad
Z=z.
\]
This is a global diffeomorphism: for each Z it is an invertible linear change of the x,y coordinates. Direct differentiation gives
\[
dQ+P\,dZ=\alpha_k.
\tag{7}
\]
Hence the lifted contact structure is standard and tight. Any overtwisted disk in any cover would lift to an overtwisted disk in the universal cover, so \(\xi_k\) is universally tight.

For \(1\le n<k\), the map
\[
\phi_{n,k}(x,y,z)=(x,y,(n/k)z\bmod1)
\tag{8}
\]
is an embedding of the **closed** domain D: its z-coordinate ranges in an interval of length strictly less than one. Its pullback is exactly \(\beta_n\). Therefore
\[
\operatorname{GT}(T^3,\xi_k)\ge k-1.
\tag{9}
\]
This lower bound suffices to show that no bound depending only on the underlying manifold \(T^3\) can work. It does not assert an upper bound or reprove the classification of tight torus structures. In particular \(k=2,n=1\) is the fixed tight example needed in Section 3.

At \(n=k\), formula (8) identifies the two boundary tori, so it is not an embedding. More generally, the degree-k map
\[
(x,y,z)\longmapsto(x,y,kz)
\]
pulls back \(\alpha_1\) to \(\alpha_k\), but for \(k>1\) it is a covering, not an embedding. These operations cannot place arbitrarily many turns into the fixed contact structure \(\xi_1\).

For comparison, put
\[
M_\infty=T^2\times\mathbb R,\qquad
\alpha_\infty=\cos(2\pi z)\,dx-\sin(2\pi z)\,dy.
\]
The same universal-cover calculation (7), with k=1, proves universal tightness. For every \(n\ge1\),
\[
(x,y,z)\longmapsto(x,y,nz)
\]
embeds (1) in \(M_\infty\). Thus this **noncompact** contact manifold has infinite Giroux torsion. It is not a counterexample to the closed target. Its contact volume is infinite; each displayed n-turn image has volume \(2\pi n\), consistently with Section 2.

## 5. What the existing finiteness results say

The source records Gay's vanishing theorem for strongly symplectically fillable manifolds. In [Gay, Corollary 2.2, printed p.1751](https://arxiv.org/pdf/math/0606402), the proof explicitly starts from a strongly convex boundary of a compact symplectic filling. This is not a theorem that every tight structure is strongly fillable.

Colin's [Theorem 1.4, printed p.268](https://www.numdam.org/item/ASENS_2001_4_34_2_267_0.pdf) proves finite torsion in a **normal isotopy class** for an irreducible universally tight manifold. Normality involves persistent intersection with an incompressible torus. His Theorem 1.7 on p.269 gives only finitely many isotopy classes containing a torsion-one submanifold when the ambient manifold is closed, irreducible, and universally tight. Finitely many classes would imply a finite total supremum if every relevant class separately had finite torsion; Theorem 1.4's extra normality condition cannot be discarded. Nor can universal tightness be replaced by tightness without argument.

The complete proofs of those deep theorems are not reconstructed here. Their exact stated scopes were checked in the full primary papers.

## 6. Remaining gap and stopping point

Two routes were investigated:

1. **Compact contact-volume control.** Equations (2)–(4) give necessary degeneration and a conditional bound. Section 3 rules out an automatic pointwise lower bound over all embeddings. No tightness-based selection or \(L^2\) lower-bound theorem was obtained.
2. **Torus wrapping or infinite insertion.** The explicit models give unbounded lower bounds across varying closed contact structures and infinite torsion on one noncompact tight manifold. Wrapping the periodic coordinate is not an embedding. No single fixed closed tight contact manifold with infinite torsion was constructed.

The full question remains **unsolved, 2/5**. The precise outstanding task is to exclude arbitrarily large embedded torsion layers in each fixed closed tight contact structure, or to construct such a structure. The bounded source search found no later complete resolution. All standard-model and fillability results remain credited, and no historical novelty is asserted for these elementary deductions.
