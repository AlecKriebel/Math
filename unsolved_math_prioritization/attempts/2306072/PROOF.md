# A coefficient perturbation with nonmonotone support slits

**Provisional, unrefereed candidate.** This note claims negative answers to both questions in Hayman–Lingham Problem 6.72 (attributed to P. L. Duren). It is a proof for actual globally maximizing support points, not a claim that arbitrary trajectories are extremal. Independent expert verification and historical-priority review are required.

## 1. Statement and conventions

Let \(S\) be the class of functions analytic and univalent in the open unit disk \(D\), normalized by
\[
f(z)=z+\sum_{n\ge2}a_n(f)z^n.
\]
A support point maximizes the real part of a continuous complex-linear functional on \(H(D)\), whose real part is nonconstant on \(S\).

Set, exactly,
\[
\varepsilon=10^{-24},\qquad \eta=10^{-12}=\sqrt\varepsilon,
\qquad L(f)=a_2(f)+i\varepsilon\bigl(a_4(f)-3a_3(f)\bigr).
\tag{1}
\]
The coefficient maps, defined on all of \(H(D)\), make \(L\) a continuous complex-linear functional.

**Theorem.** Every maximizer of \(\operatorname{Re}L\) on \(S\) has an omitted arc \(\Gamma\) on which the continuous argument is not monotone. The signed radial angle is not monotone either. The ordinary nonnegative angle between the outward tangent and the radius vector is also not monotone. In particular both questions in Problem 6.72 have negative answers.

Here “monotone” allows either nondecreasing or nonincreasing. Argument means a continuous real-valued lift along the arc; changing the lift by a multiple of \(2\pi\) does not affect the conclusion. The outward tangent points toward infinity. Both signed and unsigned interpretations of the second question are covered.

We do not claim a closed formula for the maximizing conformal map. Compactness supplies an actual maximizer, and all ensuing estimates hold for **every** maximizer. The explicitly specified functional is therefore an existence counterexample without a numerical optimization assumption.

## 2. Classical ingredients used

The following standard theorems are used, and are not conclusions of the verification script:

1. \(S\) is compact in locally uniform convergence. Its coefficients satisfy \(|a_n|\le n\); only \(n=2,3,4\) are needed. The full coefficient theorem is de Branges, *A proof of the Bieberbach conjecture*, Acta Math. 154 (1985), 137–152, [DOI](https://doi.org/10.1007/BF02392821).
2. The area theorem: for a univalent exterior map \(F(\zeta)=\zeta+b_0+\sum_{n\ge1}b_n\zeta^{-n}\), one has \(\sum_{n\ge1}n|b_n|^2\le1\).
3. The support-slit/Schiffer theorem: if \(f\) is a support point for \(L\), then \(\mathbb C\setminus f(D)\) is one analytic arc from a finite tip to infinity, traversed with increasing modulus. Along its regular interior it satisfies
\[
 Q(w)\,dw^2>0,\qquad
 Q(w)=\frac{\Phi(w)}{w^2},\qquad
 \Phi(w)=L\left(\frac{f^2}{f-w}\right).
\tag{2}
\]
The radial angle has magnitude at most \(\pi/4\), strictly less in the interior. Also \(L(f^2)\ne0\); equivalently the quadratic differential has a simple pole at infinity. A quadratic differential has exactly one trajectory ending at a simple pole.

For (2), including its sign, normalization, analytic slit, increasing modulus, and simple-pole uniqueness, see Duren, *Arcs omitted by support points of univalent functions*, Comment. Math. Helv. 56 (1981), 352–365, pp. 352–355, DOI [10.1007/BF02566218](https://doi.org/10.1007/BF02566218); the [ETH scan](https://www.e-periodica.ch/cntmng?pid=com-001%3A1981%3A56%3A%3A30&bot=1) was inspected. These are classical support-point facts, not sufficiency assertions for arbitrary quadratic differentials.

We also use Rouché's theorem, Schwarz's lemma, and holomorphic square roots of nonvanishing functions on a disk.

## 3. Genuine maximizers and quantitative proximity to Koebe

Let \(k(z)=z/(1-z)^2\), with \(a_n(k)=n\). Then \(\operatorname{Re}L(k)=2\), whereas \(\operatorname{Re}L(z)=0\). Compactness gives a maximizer \(f\), and nonconstancy makes it a support point covered by (2).

For any maximizer,
\[
\operatorname{Re}a_2-\varepsilon\operatorname{Im}(a_4-3a_3)\ge2,
\quad\text{hence}\quad
\operatorname{Re}a_2\ge2-13\varepsilon.
\tag{3}
\]
Together with \(|a_2|\le2\), this implies
\[
|a_2-2|^2\le52\varepsilon,\qquad |a_2-2|<8\eta,
\qquad 1-|a_2|^2/4\le13\varepsilon.
\tag{4}
\]
For the last bound, \(\operatorname{Re}a_2>0\), so \(|a_2|\ge\operatorname{Re}a_2\), and
\(1-(2-13\varepsilon)^2/4\le13\varepsilon\).

The odd root transform \(g(z)=\sqrt{f(z^2)}\), normalized by \(g'(0)=1\), is univalent: equality of two values first gives equality of their squares under \(f\), and the remaining opposite-point case is eliminated by oddness except at zero. Thus
\[
 F(\zeta)=\frac1{g(1/\zeta)}
 =\zeta-\frac{a_2}{2}\zeta^{-1}
   +\left(\frac{3a_2^2}{8}-\frac{a_3}{2}\right)\zeta^{-3}+\cdots
\]
is univalent outside the unit disk. The area theorem gives
\[
\left|a_3-\frac34a_2^2\right|
\le2\sqrt{\frac{1-|a_2|^2/4}{3}}<5\eta.
\]
Since \(|a_2+2|\le4\), it follows that
\[
 |a_3-3|<29\eta.
\tag{5}
\]
Put
\[
 A=2a_3+a_2^2-6a_2,\qquad B=3a_2-3.
\]
Then
\[
 |A+2|<106\eta,\qquad |B-3|<24\eta.
\tag{6}
\]
Indeed \(A+2=2(a_3-3)+(a_2-2)(a_2-4)\), and \(|a_2-4|\le6\). These bounds are uniform over all maximizers; uniqueness or differentiability of a maximizing selection has not been assumed.

## 4. The slit tip lies inside radius 3/10

The analytic square root
\[
 H(z)=\sqrt{z/f(z)}=1-\frac{a_2}{2}z+\sum_{n\ge2}c_nz^n
\]
exists on \(D\), normalized by \(H(0)=1\). From the preceding area theorem,
\[
 \sum_{n\ge2}(2n-1)|c_n|^2\le13\varepsilon.
\tag{7}
\]
Write \(H_0(z)=1-z\). At \(|z|\le r=2/3\), Cauchy–Schwarz and (4) give
\[
 |H-H_0|
 \le4\eta r+\sqrt{13}\eta
    \left(\sum_{n\ge2}\frac{r^{2n}}{2n-1}\right)^{1/2}<5\eta,
\tag{8}
\]
because the sum is at most \(r^4/[3(1-r^2)]=16/135<1/4\), and \(4r+2<5\). Similarly,
\[
 |H'-H_0'|
 \le4\eta+\sqrt{13}\eta
    \left(\sum_{n\ge2}\frac{n^2r^{2n-2}}{2n-1}\right)^{1/2}<10\eta.
\tag{9}
\]
Here \(n^2/(2n-1)\le n\), so the sum is at most
\((1-r^2)^{-2}-1=56/25<9/4\), and \(\sqrt{13}<4\).

At \(z_*=-2/3\), one has \(H_0=5/3\). Bounds (8)–(9), using \(3/2<|H|<2\), imply
\[
 |f(z_*)-k(z_*)|<2\eta,\qquad
 |f'(z_*)-k'(z_*)|<8\eta.
\tag{10}
\]
For completeness, the first estimate follows from
\[
 |H^{-2}-H_0^{-2}|
 \le\frac{(5\eta)(7/2)}{(3/2)^2(5/3)^2}=\frac{14}{5}\eta
\]
and \(|z_*|=2/3\). For the derivative write \(f'=(H-2z_*H')/H^3\). Its numerator differs from \(1/3\) by less than \(19\eta\), giving an error less than \(6\eta\) from that difference. The remaining reciprocal-cube difference is less than \(2\eta\): use \(|H^2+HH_0+H_0^2|<11\) and \(|H|^3H_0^3>(3/2)^3(5/3)^3=125/8\).

For any conformal map \(f:D\to\Omega\),
\[
 \operatorname{dist}(f(z),\partial\Omega)
 \le(1-|z|^2)|f'(z)|.
\tag{11}
\]
To see the direction of this inequality, compose \(f\) with a disk automorphism taking zero to \(z\); if a disk of radius \(d\) about its value is contained in \(\Omega\), the inverse on that disk, followed by scaling, is a disk self-map fixing zero. Schwarz's lemma says \(d\) is at most the conformal radius \((1-|z|^2)|f'(z)|\). Let \(d\) increase to the distance to the boundary.

Since \(k(z_*)=-6/25\), \(k'(z_*)=9/125\), and \(1-|z_*|^2=5/9\), (10)–(11) give
\[
 \min_{w\in\Gamma}|w|
 \le |f(z_*)|+(5/9)|f'(z_*)|
 <\frac7{25}+7\eta<\frac3{10}.
\tag{12}
\]
The minimum is the finite tip radius because the support slit has increasing modulus. This quantitative step prevents mistaking a formal continuation past the actual tip for an omitted arc.

## 5. Exact quadratic differential

Extracting coefficients through degree four gives
\[
\begin{aligned}
 [z^2]\frac{f(z)^2}{f(z)-w}&=-\frac1w,\\
 [z^3]\frac{f(z)^2}{f(z)-w}&=-\frac{2a_2}{w}-\frac1{w^2},\\
 [z^4]\frac{f(z)^2}{f(z)-w}&=-\frac{2a_3+a_2^2}{w}
                                  -\frac{3a_2}{w^2}-\frac1{w^3}.
\end{aligned}
\]
Consequently, with
\[
 a=1+i\varepsilon A,\qquad b=i\varepsilon B,\qquad c=i\varepsilon,
\]
we have the exact identities
\[
 \Phi(w)=-\frac a w-\frac b{w^2}-\frac c{w^3},\qquad
 Q(w)=-\frac a{w^3}-\frac b{w^4}-\frac c{w^5}.
\tag{13}
\]
In particular \(a=L(f^2)\), and \(a\) is close to 1, hence nonzero.

Use the local double-cover coordinate \(w=-v^{-2}\). Then
\[
 Q(w)\,dw^2=4P(v)\,dv^2,\qquad
 P(v)=a-bv^2+cv^4.
\tag{14}
\]
Define the real polynomial
\[
 P_0(v)=-2-3v^2+v^4.
\]
By (6), for \(|v|\le3\),
\[
 |P(v)-1-i\varepsilon P_0(v)|\le322\varepsilon\eta,
 \quad |P_0(v)|\le110,
 \quad |P(v)-1|\le111\varepsilon.
\tag{15}
\]
In particular \(P\) has no zero in this disk. Choose the square root \(p=\sqrt P\) close to 1 and let
\[
 G(v)=\int_0^v p(s)\,ds.
\]
Then
\[
 |G(v)-v|\le333\varepsilon\quad (|v|\le3).
\tag{16}
\]
For each \(|t|<2\), Rouché's theorem on \(|v|=3\) shows \(G(v)=t\) has exactly one zero there: \(333\varepsilon<1\le|v-t|\) on that circle. Since \(G'=p\ne0\), these zeros give a holomorphic inverse \(v=V(t)\) on \(|t|<2\). It satisfies
\[
 V(0)=0,\quad V'(0)=a^{-1/2},\quad
 |V(t)-t|\le333\varepsilon,\quad V'(t)=1/p(V(t)).
\tag{17}
\]
Oddness of \(G\) gives oddness of \(V\).

For real \(0<t\le T=7/4\), put
\[
 W(t)=-V(t)^{-2}.
\tag{18}
\]
There are no other zeros of \(V\), and this is a regular trajectory: by (14) and (17), \(Q(W(t))W'(t)^2=4>0\). It approaches infinity as \(W(t)\sim-a/t^2\). Also
\[
 |V(t)|\le7/4+333\varepsilon<9/5,
 \qquad |W(t)|>25/81>3/10.
\tag{19}
\]

**Identification with the actual omitted slit.** Both \(W\) and \(\Gamma\) approach the simple pole at infinity, so they coincide near infinity by its unique-trajectory property. Ordinary local uniqueness continues this identification wherever \(Q\) is regular and nonzero. On (18), this follows from (14)–(15). The identification cannot stop at the finite slit tip because the tip has modulus less than \(3/10\) by (12), whereas every point of (18) has modulus greater than \(3/10\) by (19). It therefore continues through the entire segment \(0<t\le7/4\). Increasing \(t\) follows this segment inward from infinity, so \(-W'(t)\) is its outward tangent. Thus the trajectory used below belongs to an actual globally maximizing support point.

## 6. Certified sign reversal

All estimates in this section are uniform in the maximizer. Put
\[
 d(t)=t+\frac12t^3-\frac1{10}t^5,
 \qquad q(t)=d'(t)-\frac{d(t)}t=t^2-\frac25t^4.
\tag{20}
\]
The following explicit bounds hold for \(1\le t\le7/4\):
\[
 |V(t)-t-i\varepsilon d(t)|\le487\varepsilon\eta,
 \qquad
 |V'(t)-1-i\varepsilon d'(t)|\le162\varepsilon\eta.
\tag{21}
\]
Here are the remainder estimates, so (21) is not just formal perturbation theory.

For \(|x|\le111\varepsilon\),
\[
 |\sqrt{1+x}-1-x/2|\le |x|^2/2.
\]
This follows from the exact identity
\(\sqrt{1+x}-1-x/2=-x^2/[2(\sqrt{1+x}+1)^2]\), taking the root with positive real part. From (15) and \((111^2/2)\eta<1\),
\[
 |p(v)-1-(i\varepsilon/2)P_0(v)|\le162\varepsilon\eta.
\]
After integrating, the remainder in
\(G(v)=v-i\varepsilon d(v)+R(v)\) is at most \(486\varepsilon\eta\). Using \(|d'|\le55\) on \(|v|\le3\) and (17), inversion costs at most \(18315\varepsilon^2\). Since \(18315\eta<1\), the first bound in (21) follows.

For the derivative use
\[
 |(1+x)^{-1/2}-1+x/2|\le2|x|^2\qquad(|x|\le1/4).
\]
For example this follows by Taylor's integral remainder and the bound on \((3/4)(1+x)^{-5/2}\) in the disk. Since \(|P_0'|\le126\) on \(|v|\le3\), replacing \(P_0(V(t))\) by \(P_0(t)\) costs at most \(20979\varepsilon^2\). The remaining costs are \(161\varepsilon\eta\) and \(24642\varepsilon^2\), respectively. Their sum is at most \(162\varepsilon\eta\) because \(45621\eta<1\). This proves the second bound in (21).

Let
\[
 Z(t)=\frac{tV'(t)}{V(t)}.
\]
Since \(|V(t)|\ge1-333\varepsilon>1/2\), \(|q(t)|<7\), and \(t\le7/4\), (17), (20), and (21) yield
\[
 \left|Z(t)-1-i\varepsilon q(t)\right|
 \le1541\varepsilon\eta+4662\varepsilon^2
 <2000\varepsilon\eta.
\tag{22}
\]
One can check this directly after multiplying by \(V\): the error numerator is
\(tR_{V'}-R_V-i\varepsilon q(V-t)\).

The exact endpoint values are
\[
 q(1)=\frac35,\qquad q(7/4)=-\frac{441}{640}.
\tag{23}
\]
As \(2000\eta=2\cdot10^{-9}\), (22) implies
\[
 \operatorname{Im}Z(1)>\varepsilon/2>0,
 \qquad
 \operatorname{Im}Z(7/4)<-\varepsilon/2<0,
 \qquad \operatorname{Re}Z(t)>0.
\tag{24}
\]
No floating-point arithmetic is used for these signs.

For a continuous argument \(\theta(t)\) of \(W(t)\),
\[
 \theta'(t)=\operatorname{Im}\frac{W'(t)}{W(t)}
            =-\frac2t\operatorname{Im}Z(t).
\tag{25}
\]
Thus \(\theta'(1)<0\) and \(\theta'(7/4)>0\), proving that \(\theta\) is not monotone.

The signed outward radial angle is
\[
 \beta(t)=\arg\frac{-W'(t)}{W(t)}=\arg Z(t).
\tag{26}
\]
It is positive at 1 and negative at \(7/4\). Also it tends to zero as \(t\downarrow0\), since \(tV'/V\to1\). Therefore it cannot be monotone on the whole slit: a nondecreasing function with initial limit zero cannot take a negative value, and a nonincreasing one cannot take a positive value. This also agrees with the general implication that a monotone radial angle would force monotone argument.

Finally, continuity and (24) give a \(t_0\in(1,7/4)\) at which \(\beta(t_0)=0\). The unsigned angle \(|\beta|\) is positive at both endpoints and zero at \(t_0\), so it is not monotone even on that compact subarc. This proves the theorem. \(\square\)

## 7. Qualitative mechanism and limits

The quantitative proof can be read as the rigorous version of the expansion
\[
 W(t)=-t^{-2}+i\varepsilon(2t^{-2}+1-t^2/5)+o(\varepsilon),
\quad
 \beta(t)=\varepsilon(t^2-2t^4/5)+o(\varepsilon).
\]
Equivalently, to first order with \(r=t^{-2}\),
\[
 \arg W=\pi-2\varepsilon-\varepsilon/r+\varepsilon/(5r^2)+o(\varepsilon).
\]
These displays explain the choice of functional but are not used without the certified remainders above. In particular, the apparent reversal at \(r=2/5\) is not being inferred from a plot.

There is no conflict with eventual monotonicity near infinity: \(q(t)>0\) for all sufficiently small positive \(t\), and the reversal takes place on a bounded subarc. Hibschweiler's 1995 eventual-monotonicity theorem therefore does not imply the original global conjecture or invalidate this example.

The proof establishes existence and nonmonotonicity of every maximizer of (1). It does not identify the maximizer uniquely, compute all its coefficients, classify its complete omitted arc, or establish novelty. The verification script checks finite algebra and the stated rational bounds; it is not a formalization or independent proof of the classical analytic theorems in Section 2.
