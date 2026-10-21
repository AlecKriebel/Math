# Independent adversarial audit: an annular minimal Martin kernel

Problem 7.42 in Hayman--Lingham, *Research Problems in Function Theory*, arXiv:1809.07200v2. Problem identifier: 2307042. Audit date: 2026-10-06 UTC.

## Verdict

**ACCEPT the mathematical counterexample in the immutable author proof, with its stated local/equality-along-a-line scope. No mathematical correction is required.**

For the annulus \(D=\{1<|z|<e\}\), base \(a=\sqrt e\), and the normalized minimal Martin kernel \(K\) at the inner boundary point \(-1\), the author proves

\[
 K(z)<H_a(z)\quad\text{for every }z\ne a\text{ in some neighborhood of }a.
\]

Here \(H_a\) is the one-sided supremum of positive harmonic functions whose value at \(a\) is at most one. This rules out equality of this fixed kernel with the envelope on any nontrivial curve issuing from the base, hence on any such Green line. The claim is stronger than checking a selection of trajectories or directions, but does not exclude isolated contacts outside that neighborhood.

This is independent mathematical review by an AI assistant, not formal proof-assistant certification, human peer review, a novelty determination, or a guarantee of historical/current problem status. The proof and all five accompanying author files are reproduced byte-for-byte under `author/`. The author archive and original source files were not changed.

The audit below rederives the delicate analytic steps rather than relying on the author's check ledger. No finite grid, numerical sum truncation, plotting experiment, or machine-generated claim is used as a proof.

## 1. Exact target, quantifiers, normalization, and geometry

The primary 2018 PDF was inspected at printed pages 173--174, in extracted text and original rendered pages. The source starts with a Green domain and the pointwise upper envelope of positive harmonic functions normalized at one interior base. It gives the unit-disc equality along a pole-directed radius, reformulates that equality using Green lines in a simply connected domain, and asks whether the property extends to multiply connected domains.

Thus simple connectivity is the setting of the known example, not a hypothesis imposed on the proposed multiply connected extension. The present smooth bounded annulus is an admissible Green domain. A single minimal Martin point for which the equality-line property fails negates the universal assertion. It is not necessary to show failure for every boundary point or every multiply connected domain.

The source has typographical inconsistencies in its displayed notation. Neither the theorem nor this audit uses that defective display as a premise. The explicit envelope definition and disc example determine the orientation: the fixed kernel would have to attain the **upper** envelope along its line. The argument proves strict inequality in precisely the opposite direction, \(K<H_a\), at every nearby non-base point.

For any positive harmonic \(h\), its value at the base is positive. Rescaling shows that allowing \(h(a)\le1\) gives the same supremum as requiring \(h(a)=1\). Harnack's inequality along a finite chain of interior discs makes the envelope finite at every fixed interior point. The constant function one is admissible; hence \(H_a(a)=1\). The constructed kernel also has \(K(a)=1\), so automatic equality at the base is retained.

The phrase describing contact along a line is read as equality along that line, as in the immediately preceding disc-radius example. A weaker, different question asking only for some isolated contact point somewhere is not decided here. The author explicitly preserves this limitation. There is no hypothesis that functions have globally single-valued harmonic conjugates. Periodic harmonic functions on the cylinder descend to bona fide harmonic functions on the annulus, which is the required class.

## 2. Strip kernel and uniform periodization

Use \(z=e^{x+iy}\), with \(0<x<1\) and \(y\) modulo \(2\pi\). The base is \((1/2,0)\), and the chosen boundary point is \((0,\pi)\). In the auxiliary strip complex coordinate \(w=y+ix\), the map \(F(w)=e^{\pi w}\) is a conformal bijection to the upper half-plane. The exponential used to descend to the annulus and this auxiliary exponential have different roles.

For \(w'=\eta+is\), \(0<s<1\), the upper-half-plane Green function pulls back to

\[
g_S(w,w')=\log\left|\frac{e^{\pi w}-e^{\pi\overline{w'}}}
 {e^{\pi w}-e^{\pi w'}}\right|.
\]

It is positive and harmonic in either variable away from the diagonal, zero on both horizontal strip sides, symmetric, and has singular part \(-\log|w-w'|\). The local conformal derivative contributes only a regular term.

A useful direct rewrite is

\[
g_S(w,w')=\frac12\log
\frac{\cosh(\pi(y-\eta))-\cos(\pi(x+s))}
     {\cosh(\pi(y-\eta))-\cos(\pi(x-s))}.
\tag{A1}
\]

The numerator minus the denominator is \(2\sin(\pi x)\sin(\pi s)>0\). This independently checks the sign and both boundary values. When the horizontal separation has large modulus, factor \(\cosh(\pi(y-\eta))\) out of both logarithms. The remaining logarithms have arguments \(1+O(e^{-\pi|y-\eta|})\). Differentiating any fixed finite number of times in the real variables preserves an exponential bound; denominators are bounded away from zero in the tail. These bounds hold with \(x,s\) in their closed bounded intervals and the other variables in bounded sets. Only finitely many central terms need to be excluded at a pole.

Consequently

\[
g_C(w,w')=\sum_{k\in\mathbb Z}g_S(w,w'+2\pi k)
\tag{A2}
\]

converges uniformly, with every fixed derivative order, on compact sets away from the diagonal modulo the period. Reindexing proves periodicity in either variable. In a small neighborhood of a cylinder pole exactly one term has the logarithmic singularity; all other terms are smooth there. For an interior pole, uniform convergence up to the boundary proves zero boundary values. The compact cylinder with boundary is conformally the closed annulus. Uniqueness by the maximum principle identifies (A2) as its Dirichlet Green function. There is no unaccounted additive harmonic term or missing outer-boundary correction.

Differentiate (A1) in \(s\) at zero. The two differentiated logarithms add, giving

\[
\left.\partial_sg_S(w,\eta+is)\right|_{s=0}
=\frac{\pi\sin(\pi x)}{\cosh(\pi(y-\eta))-\cos(\pi x)}
=2\pi p(x,y-\eta),
\]

where

\[
p(x,t)=\frac{\sin(\pi x)}{2(\cosh(\pi t)-\cos(\pi x))}.
\tag{A3}
\]

The same tail bounds justify differentiating (A2) at the boundary. Set

\[
P_\eta(x,y)=\sum_{k\in\mathbb Z}p(x,y-\eta+2\pi k),
\qquad P=P_\pi.
\]

Each summand is positive and harmonic in the open strip. Uniform convergence of derivatives on interior compact sets proves that \(P\) is positive, smooth, periodic, and harmonic. Uniform convergence up to a boundary arc away from its pole also proves its continuous zero boundary values there. These assertions do not rely merely on pointwise convergence of the series.

## 3. Martin limit for arbitrary boundary approach

Fix a compact set of first variables in the open cylinder. For \(\eta\) in a sufficiently small interval around \(\pi\), the second variable \(\eta+is\) stays separated from that compact set when \(s\) is small. Smooth extension to the boundary and the preceding differentiated tail bounds give, uniformly on this product of compact sets,

\[
g_C(w,\eta+is)=2\pi sP_\eta(w)+O(s^2).
\tag{A4}
\]

The same formula holds at \(a_C=(1/2,0)\). Since \(P_\pi(a_C)>0\), continuity gives a positive lower bound for \(P_\eta(a_C)\) for nearby \(\eta\). Dividing (A4) by its base-point counterpart and then taking \(s\downarrow0\), \(\eta\to\pi\), proves

\[
\frac{g_C(w,\eta+is)}{g_C(a_C,\eta+is)}
\longrightarrow\frac{P_\pi(w)}{P_\pi(a_C)}=:K(w)
\]

locally uniformly in the first variable. This is an unrestricted interior approach to that boundary point, not only a radial/normal approach. The constant \(2\pi\) cancels. Conformal changes of Green coordinates or the boundary density also cannot introduce a missing normalization factor in the ratio. Thus \(K\) is an actual normalized Martin boundary limit. Minimality is checked separately next; it is not inferred from positivity alone.

## 4. Direct minimality, with the singularity argument made explicit

Near the distinguished boundary point write \(t=y-\pi\) and \(r=(x^2+t^2)^{1/2}\). Elementary expansions give

\[
\sin(\pi x)=\pi x+O(x^3),\qquad
\cosh(\pi t)-\cos(\pi x)=\frac{\pi^2}{2}r^2+O(r^4).
\]

Substituting into (A3) yields

\[
p(x,t)=\frac{x}{\pi r^2}+O(x)
\tag{A5}
\]

uniformly for all directions in the half-disc. To see uniformity even when \(x/r\) is very small, factor \(\pi^2r^2/2\) from the denominator and factor \(\pi x\) from the numerator. The relative errors are \(O(r^2)\), and multiplying by \(x/r^2\) gives \(O(x)\), without dividing by \(x\) in an error estimate.

The other periodized summands have smooth zero boundary data in this neighborhood and a uniformly convergent normal-derivative series, so together they are \(O(x)\). Therefore

\[
P(x,\pi+t)=\frac{x}{\pi r^2}+O(x).
\tag{A6}
\]

Let \(v\) be harmonic with \(0\le v\le P\). At every boundary point other than the distinguished point, domination and the continuous zero boundary value of \(P\) force a continuous zero boundary value of \(v\). In a half-disc at the exceptional point, reflect \(v\) oddly across \(x=0\). The reflection principle for harmonic functions with continuous zero values on a straight segment applies on every subsegment away from the origin. The reflected function \(V\) is therefore harmonic in the punctured full disc. By (A6), \(|V|=O(1/r)\), uniformly in angle.

For clarity, the harmonic Laurent conclusion can be obtained directly by taking circular Fourier coefficients. For degree \(n\ge1\), harmonicity makes each cosine/sine coefficient a linear combination of \(r^n\) and \(r^{-n}\). The uniform \(O(1/r)\) bound forces the coefficient of \(r^{-n}\) to vanish for \(n\ge2\): multiply its radial expression by \(r^n\) and let \(r\to0\). The zeroth coefficient can have only a constant plus \(\log r\). Thus the only possible singular terms are a logarithm and the two degree-one dipoles.

Oddness under \(x\mapsto-x\) eliminates the logarithm and the tangential dipole \(t/r^2\). The result is

\[
v(x,\pi+t)=A\frac{x}{r^2}+v_0(x,t),
\]

with \(v_0\) harmonic across the origin and odd in \(x\). In particular \(v_0(0,0)=0\) and \(v_0=O(x)\) in a smaller half-disc. Multiplying the inequality \(0\le v(x,\pi)\le P(x,\pi)\) by \(x\) and taking \(x\downarrow0\) gives \(0\le A\le1/\pi\).

The harmonic function \(v-\pi AP\) has its dipole canceled. Equations (A6) and the regularity of \(v_0\) show that this difference tends to zero at the exceptional boundary point. It has zero continuous data at every other boundary point too. It is therefore continuous on the compact closed annulus with zero boundary values. Apply the maximum principle to the function and its negative to obtain \(v=\pi AP\). This proves minimality. No representation theorem for arbitrary positive harmonic functions, boundary Harnack theorem, or unsupported claim about the full Martin boundary is needed.

## 5. Independently differentiated base-point gradient

Write \(C_t=\cosh(\pi t)\). Differentiating (A3) gives

\[
p_x(x,t)=\frac\pi2\frac{C_t\cos(\pi x)-1}
 {(C_t-\cos(\pi x))^2}.
\]

At \(x=1/2\), this is \(-\pi/(2C_t^2)\), whereas \(p=1/(2C_t)\). The \(t\)-derivative is odd in \(t\). At \(y=0\), the arguments in the periodized series are \((2k-1)\pi\). With

\[
q_k=\operatorname{sech}((2k-1)\pi^2),\quad
S_1=\sum_kq_k,\quad S_2=\sum_kq_k^2,
\]

we consequently obtain

\[
P(a_C)=S_1/2,\qquad P_x(a_C)=-\pi S_2/2,\qquad P_y(a_C)=0.
\]

The cancellation in \(P_y\) is justified by absolute convergence and the pairing \(k\leftrightarrow1-k\). Since the denominator in \(K=P/P(a_C)\) is a constant, not a function to differentiate, the normalized gradient is

\[
\nabla K(a_C)=(-c,0),\qquad c=\pi S_2/S_1>0.
\]

Because \(S_2/S_1\) is a weighted average of the positive \(q_k\), all of which are at most \(\operatorname{sech}(\pi^2)\),

\[
c\le\pi\operatorname{sech}(\pi^2)<\frac8{83}<\frac1{10}.
\]

The strict rational estimate follows from \(3<\pi<4\) and \(\cosh(\pi^2)>1+\pi^4/2>83/2\). It bounds the entire infinite series at once. No omitted tail or floating-point estimate is involved. The zero angular derivative and the negative, small radial derivative both have the correct sign for the inner-boundary pole at the angular antipode of the base.

## 6. Four global competitors and all-direction separation

Set \(b=(2\cosh(1/2))^{-1}\) and

\[
h_{x,\pm}=1\pm(x-1/2),\qquad
h_{y,\pm}=1\pm b\sin y\cosh(x-1/2).
\]

These functions are globally periodic, single-valued on the annulus, harmonic, and positive. The first pair lies strictly between \(1/2\) and \(3/2\). For the second pair, \(|b\sin y\cosh(x-1/2)|\le1/2\), so they are at least \(1/2\). All four take the value one at the base. Their gradients are exactly \((\pm1,0)\) and \((0,\pm b)\). The simple estimate \(\cosh(1/2)\le\sum_{n\ge0}(1/4)^n=4/3<2\) yields \(b>1/4\), while \(b<1\).

For a nonzero displacement \(d=(u,v)\), put \(\rho=\sqrt{u^2+v^2}\) and \(M=\max(|u|,b|v|)\). The maximum over the four first-order differences is

\[
\max_j(\nabla h_j-\nabla K)(a_C)\cdot d=M+cu.
\]

If \(u\ge0\) this is at least \(M\); if \(u<0\), it is at least \(M-c|u|\ge(1-c)M\). Thus in all directions it is at least \((1-c)M\). Also

\[
M\ge\tfrac12(|u|+b|v|)\ge\tfrac b2(|u|+|v|)>\rho/8.
\]

Together these imply the **uniform**, not direction-dependent, bound

\[
\max_j(\nabla h_j-\nabla K)(a_C)\cdot d
>\frac{75}{664}\rho>\rho/10.
\tag{A7}
\]

For each of the four \(C^2\) functions \(f_j=h_j-K\), choose a closed coordinate disc about the base lying inside the cylinder. The four Hessians are bounded there. Integrating the second derivative along the segment from the base to the displaced point gives a common constant \(C_0\ge1\) such that

\[
|f_j(a_C+d)-\nabla f_j(a_C)\cdot d|\le C_0\rho^2
\]

for every \(j\), because \(f_j(a_C)=0\). Choose the maximizing index in (A7) separately at each displacement; the common remainder bound remains valid regardless of that choice. For \(0<\rho<\min(r_0,1/(20C_0))\),

\[
\max_j h_j(a_C+d)-K(a_C+d)>\rho/20>0.
\]

The envelope dominates each admissible \(h_j\), and the local logarithmic chart is a diffeomorphism. Hence the claimed strict inequality holds throughout a punctured neighborhood in the original annulus. There is no need for differentiability of \(H_a\), existence of a maximizing kernel, or a continuous choice of competitor.

## 7. Green-line consequence and rejected failure modes

Every nonconstant continuous equality curve starting at the base must contain non-base points arbitrarily close to it. This remains true if a parametrization initially stays at the base: the curve cannot leave the base continuously without traversing the punctured neighborhood. Such points contradict the theorem. A Green line from the base is a particular curve of this kind. Its initial direction, possible later critical points, and endpoint behavior are irrelevant.

The audit specifically rejected the following proposed objections:

- Reversing the envelope inequality: the four functions bound the upper envelope from below, giving precisely \(K<H_a\).
- Replacing a Martin kernel with arbitrary harmonic data: both the Green-ratio limit and direct minimality are proved.
- Dropping a covering-period or outer boundary condition: the Green series has the correct \(2\pi\) period, both zero boundaries, and one quotient pole.
- Taking only a normal Martin approach: uniform boundary Taylor estimates include tangential displacement of the approaching pole.
- Losing uniformity in the singular expansion: (A5) is \(O(x)\) uniformly in angle.
- Assuming bounded dominated functions at the singular point: the allowed \(1/r\) singularity is explicitly classified and canceled.
- Checking only four directions: four competitors give the maximum of linear forms, and (A7) covers every nonzero direction.
- Using a direction-dependent Taylor radius: the finite-list Hessian bound is common to all directions and competitors.
- Counting base-point equality as a line: normalization forces equality only at the base, which the punctured result explicitly excludes from its strict inequality.
- Claiming a global empty contact set: neither this audit nor the author proof makes that stronger claim.

## 8. Acceptance boundary

The immutable author's main theorem and consequence are accepted without edits. The extra derivations here are explanatory audit expansions, not patches needed to repair the proof. No corrected proof version or patch replay is therefore necessary.

The 2018 editorial update is only historical status evidence. A bounded literature check is not a novelty proof. The source/integrity report separately records what was inspected and what was not established. This acceptance does not authorize publication of any source PDF, extracted source text, dataset record, or private coordination material.

Primary reference: W. K. Hayman and E. F. Lingham, *Research Problems in Function Theory (New Edition)*, arXiv:1809.07200v2 (2018), Problem 7.42 and Update 7.42, printed pp. 173--174. https://arxiv.org/abs/1809.07200v2
