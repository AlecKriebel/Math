# Verification of Eremenko's known affirmative answer

## 1. Exact target and the normalization issue

The target asks for a nonconstant entire function F of infinite order and a finite nonzero Picard exceptional value α such that there is no continuous curve γ tending to infinity with

\[
 |F(\gamma(t))|=|\alpha|,\qquad F(\gamma(t))\longrightarrow\alpha.
\]

Our construction omits α altogether, which meets both the omitted-value and the finitely-assumed-value conventions for a Picard exceptional value. There are no derivative, coefficient, real-symmetry, or finite-lower-order hypotheses. It suffices to construct the case α=1: multiplication by α gives every other prescribed nonzero value and preserves the level-curve condition and order.

Hayman–Lingham, Update 2.58, explicitly credits Eremenko's 1985 construction with solving this question. However, Eremenko's paper principally formulates natural curves as curves having real image. Its last paragraph constructs an exponential with omitted value zero. A translation of that exponential alone does not verify the circle condition here. We therefore give the geometric transfer explicitly below. This is a verification of a credited historical result, not a new-resolution or priority claim.

## 2. The published construction used

The input is the parabolic surface in the final remark on p.309 of Eremenko's paper:

**Published surface input.** There is a simply connected parabolic Riemann surface S, with locally univalent holomorphic projection p:S→C, containing no lifted horizontal ray over any line Im w=2πk, k∈Z.

Here a lifted ray means an arc on S whose projection is one-to-one onto a half-line. The singularities of the inverse projection are logarithmic ends; they are not points of S. Parabolic means S is conformally equivalent to C.

The entire article, pp.305–309, was inspected, including its theorem and both examples. Example 2 builds a tree of upper/lower half-plane sheets joined along finite intervals. Its interval estimates make the logarithmic ends locally finite. Moving their projected values sufficiently far out invokes Volkovyskii's parabolicity criterion. The final remark adapts the sewing to countably many horizontal lines and a horizontal stretching. That multi-line surface construction is a published input here; the remark sketches its adaptation rather than spelling out every sewing. We do not claim a new self-contained proof of that input or of Volkovyskii's theorem.

Replace the base coordinate by A(w)=w/2+iπ/2. The resulting surface S₀ is still parabolic, with locally univalent projection p₀=A∘p. It has no lifted horizontal ray on any line

\[
 y=b_k:=\frac{\pi}{2}+k\pi,\qquad k\in\mathbb Z.
\]

Both orientations of a half-line are excluded in the published input. Only right-going rays are needed below.

## 3. An explicit bounded quasiconformal deformation

Define

\[
 a(x)=\begin{cases}\pi/6,&x\le0,\\
 \arcsin(e^{-x}/2),&x\ge0,
 \end{cases}
 \qquad
 \Psi(x+iy)=x+i\bigl(y+a(x)\sin y\bigr).
\]

This is a globally defined orientation-preserving quasiconformal homeomorphism of C. Here are details, including the seam x=0:

- a is continuous, Lipschitz, and 0<a≤π/6. Away from the seam, |a′|≤1/√3. The seam has measure zero.
- For fixed x, the function y↦y+a(x)sin y is strictly increasing, onto R, and its derivative is at least d=1−π/6>0.
- Its Jacobian matrix almost everywhere is

\[
 D\Psi=\begin{pmatrix}1&0\\a'(x)\sin y&1+a(x)\cos y\end{pmatrix}.
\]

The matrix entries are uniformly bounded and its determinant is ≥d. The inverse is globally Lipschitz as well: compare the y-coordinates at fixed x using the lower bound d, then use the Lipschitz bound on a to compare different x. Thus Ψ is bilipschitz and quasiconformal. For example, the crude finite distortion bound K≤[1+1/3+(1+π/6)²]/d follows from the squared Frobenius norm divided by the determinant.

Give the underlying topological surface S₀ a new complex structure by using Ψ∘p₀ as each local coordinate. This is a valid analytic atlas: every transition between such projection coordinates is the identity on its overlap. Write S₁ for the resulting Riemann surface and p₁=Ψ∘p₀ for its now-holomorphic locally univalent projection. The identity S₀→S₁ is uniformly quasiconformal.

The surface S₁ is still parabolic. One standard proof uses conformal modulus: a K-quasiconformal homeomorphism from C onto the disc would carry the annuli 1<|z|<R to ring domains of modulus at least (log R)/(2πK). The image of the closed unit disc contains a fixed small disc. Because every image ring lies in the unit disc outside that fixed compact set, its modulus has a uniform finite upper bound by ring-domain monotonicity. This contradicts R→∞. Uniformization and noncompactness then give S₁≅C. This argument uses only the standard quasiconformal modulus inequality, not a claim that arbitrary plane homeomorphisms preserve conformal type.

Choose a conformal isomorphism φ:C→S₁ and set

\[
 H=p_1\circ\phi,\qquad q=e^H,\qquad F=1+e^{-H}=1+\frac1q.
\]

The functions H, q and F are entire. H is nonconstant and locally univalent; q never vanishes; and F omits 1.

## 4. Why the exact level circle has no asymptotic path to 1

For every nonzero q,

\[
 \left|1+\frac1q\right|=1
 \quad\Longleftrightarrow\quad |q+1|=|q|
 \quad\Longleftrightarrow\quad \Re q=-\frac12. \tag{1}
\]

In addition, F→1 is equivalent to |q|→∞. Suppose for contradiction that a continuous γ tending to infinity satisfies |F∘γ|=1 and F∘γ→1. Write

\[
 H(\gamma(t))=x(t)+iv(t).
\]

Then x(t)=log|q(γ(t))|→+∞. Eventually x(t)>0. By (1),

\[
 \cos v(t)=-e^{-x(t)}/2.
\]

Consequently, for one integer k which is constant on the connected tail of γ,

\[
 v(t)=b_k+(-1)^k a(x(t)). \tag{2}
\]

The integer cannot switch: these graphs are disjoint for x>0. At b_k, sin b_k=(−1)^k, so

\[
 \Psi(x+ib_k)=x+i\bigl(b_k+(-1)^k a(x)\bigr).
\]

Pull γ through φ and then through the identity of the underlying surfaces S₁→S₀. Equation (2) says its projection under p₀ lies on y=b_k, with real part tending to +∞.

This forces a forbidden lifted ray. To justify that implication without assuming γ itself is monotone, the inverse image under a local conformal projection of a horizontal line is a one-dimensional manifold without branch vertices. Every connected component projects one-to-one onto an open interval of that line: after orienting the component, its real coordinate is locally strictly increasing and hence globally strictly increasing; a circular component is impossible. The path's connected tail is contained in one component. Since its real projection tends to +∞, that interval contains a right half-line. This contradicts the defining property of S₀.

Thus F has no natural asymptotic path for the exceptional value 1. An omitted value of a nonconstant entire function is an asymptotic value by the standard Iversen theorem; the exclusion concerns the prescribed level curve, not arbitrary asymptotic curves.

## 5. Infinite order, rather than an unverified growth label

It remains to check the growth requirement after deformation. We prove that any nonconstant entire G of finite order omitting 1 has a natural asymptotic path to 1. Hadamard factorization applied to the zero-free finite-order function G−1 gives

\[
 G(z)=1+e^{P(z)}
\]

for a nonconstant polynomial P. For t>0 sufficiently small, define the continuous logarithm

\[
 W(t)=\log(2\sin(t/2))+i(\pi/2+t/2),
 \qquad e^{W(t)}=e^{it}-1.
\]

Its real part tends to −∞ as t↓0. Choose a left half-plane containing the tail of W and none of the finitely many critical values of P. A polynomial is proper; its restriction over that half-plane is a finite unbranched covering. The half-plane is simply connected, so any inverse branch Z is holomorphic there. Then

\[
 z(t)=Z(W(t)),\qquad G(z(t))=e^{it}.
\]

Properness gives |z(t)|→∞, while |G(z(t))|=1 and G(z(t))→1. This is the required natural curve. Our F cannot therefore have finite order. Its ordinary entire-function order is infinite. No claim about a quantitative growth rate or its lower order is needed.

For any prescribed α≠0, Fα=αF omits α, has infinite order, and would have a forbidden natural curve exactly if F did. This completes all quantifiers of the existence question.

## 6. Proof boundary and checks

The substantive non-elementary published input is the multi-line parabolic surface construction on Eremenko p.309, backed by Example 2 and its cited parabolicity theorem. Uniformization, Hadamard factorization, and the quasiconformal modulus inequality are standard external theorems. The explicit deformation and transfer above make the nonzero-value circle normalization checkable; they do not turn this into a new mathematical discovery.

The accompanying standard-library check script tests the algebraic circle identity with exact fractions and samples the deformation and its inverse. Those finite tests are only transcription controls. The analytic proof of global distortion, absence of all natural paths, and infinite order is in the argument above; it does not follow from sampling.

**Conclusion, subject to independent audit:** an affirmative answer was already supplied by Eremenko (1985), as stated in Update 2.58. The stale open triage should be corrected to an attributed historical resolution. No new paper, new-solution claim, release, or DOI is warranted.
