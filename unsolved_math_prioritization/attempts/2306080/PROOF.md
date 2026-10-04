# A univalent function with a nonnormal primitive

## Result and attribution

Problem 6.80 of Hayman and Lingham asks whether the primitive, based at
zero, of every analytic univalent function on the unit disc must be normal.
The answer is **no**. This is a known result of Peter Lappan (1981), not a
new solution. The counterexample below is the one reproduced in the
published version of Gröhn, equation (12), which cites Lappan's Theorem 5.
PROVENANCE.md records an important error in the earlier arXiv version.

Here is a self-contained verification of the counterexample. The only
normality criterion used is the standard characterization

\[
 G\text{ normal on }\mathbb D
 \quad\Longleftrightarrow\quad
 \sup_{z\in\mathbb D}(1-|z|^2)G^\#(z)<\infty,
 \qquad G^\#=\frac{|G'|}{1+|G|^2}.
\]

Normality here means normality under precomposition by all conformal
automorphisms of the disc, equivalently the Lehto–Virtanen definition.
It does not mean that a single holomorphic function belongs to some
unspecified normal family.

Put

\[
 b=\frac1{100},\qquad c=\frac1{10},\qquad a=b+ic,
 \qquad
 F(z)=(1-z)^{-a}-(1-z)^{-b},
 \qquad f(z)=F'(z).
\]

Every power uses the branch \((1-z)^{-s}=\exp(-s\operatorname{Log}(1-z))\)
with \(-\pi/2<\arg(1-z)<\pi/2\). This is well defined on \(\mathbb D\).
We prove that \(f\) is analytic and injective there, \(F(0)=0\), and \(F\)
is nonnormal. Thus \(F(z)=\int_0^z f(t)\,dt\) settles the entire question.

## A strip lemma

**Lemma.** Let \(\Omega\) be a convex domain contained in a horizontal
strip of width \(\pi\). Let \(L\) be analytic on \(\Omega\), and suppose
\(|L'(w)-1|\le q<1\) throughout \(\Omega\). Then \(e^{L(w)}\) is injective
on \(\Omega\).

**Proof.** Suppose \(e^{L(w_2)}=e^{L(w_1)}\). If \(w_1\ne w_2\), convexity
allows integration along their straight segment. Set

\[
 B=\int_0^1L'(w_1+t(w_2-w_1))\,dt.
\]

Then \(|B-1|\le q<1\), so \(B\ne0\), and

\[
 B(w_2-w_1)=L(w_2)-L(w_1)=2\pi i k
 \quad\text{for some }k\in\mathbb Z.
\]

The case \(k=0\) gives \(w_2=w_1\). In the other cases,

\[
 |B-1|^2<1
 \ \Longrightarrow\ |B|^2<2\operatorname{Re}B
 \ \Longrightarrow\ \operatorname{Re}(1/B)>\tfrac12.
\]

Consequently

\[
 |\operatorname{Im}(w_2-w_1)|
   =2\pi|k|\operatorname{Re}(1/B)>\pi,
\]

contradicting membership in the strip. This proves the lemma. \(\square\)

## Global univalence of the derivative

The map \(w=-\operatorname{Log}(1-z)\) is one-to-one and maps
\(\mathbb D\) onto

\[
 \Omega=\{x+iy:\ -\pi/2<y<\pi/2,\quad x>-\log(2\cos y)\}.
\]

Indeed, \(z=1-e^{-w}\), and \(|z|<1\) is equivalent to
\(e^{-x}<2\cos y\). The boundary function \(-\log(2\cos y)\) has second
derivative \(\sec^2 y>0\), so \(\Omega\) is convex. Its imaginary width
is \(\pi\).

Since

\[
 f(z)=a(1-z)^{-1-a}-b(1-z)^{-1-b},
\]

we have, in the \(w\) coordinate,

\[
 f(1-e^{-w})
   =a e^{(1+a)w}(1-u(w)),
 \qquad u(w)=\frac ba e^{-icw}.
\]

For every \(w=x+iy\in\Omega\),

\[
 |u(w)|=\frac1{\sqrt{101}}e^{cy}
   <\frac1{10}e^{\pi/20}<\frac18.
\]

The last inequality is elementary: \(\pi<4\), and for \(0<s<1\),
\(e^s=\sum s^n/n!<\sum s^n=1/(1-s)\), hence
\(e^{\pi/20}<e^{1/5}<5/4\).

In particular \(1-u\) never vanishes, and the power-series logarithm
\(\log(1-u)=-\sum_{n\ge1}u^n/n\) is analytic. Fix any logarithm of the
nonzero constant \(a\), and define

\[
 L(w)=\log a+(1+a)w+\log(1-u(w)).
\]

Then \(f(1-e^{-w})=e^{L(w)}\), and, because \(u'=-icu\),

\[
 L'(w)=1+a+\frac{ic\,u(w)}{1-u(w)}.
\]

Using \(|a|=\sqrt{101}/100<11/100\),

\[
 |L'(w)-1|
  \le |a|+c\frac{|u(w)|}{1-|u(w)|}
  <\frac{11}{100}+\frac1{70}
  =\frac{87}{700}<1.
\]

The strip lemma now proves global injectivity of \(f\). This is a global
argument, not merely a check that \(f'\ne0\).

## Failure of normality of the primitive

For integers \(n\ge1\), let

\[
 t_n=e^{-20\pi n},\qquad z_n=1-t_n\in(0,1).
\]

Here \(t_n^{-ic}=e^{2\pi in}=1\), so \(F(z_n)=0\). Moreover

\[
 f(z_n)=(a-b)t_n^{-1-b}=ic\,t_n^{-1-b}.
\]

Thus

\[
 (1-|z_n|^2)F^\#(z_n)
 =\frac1{10}(2-t_n)t_n^{-1/100}
 =\frac1{10}(2-e^{-20\pi n})e^{\pi n/5}
 \longrightarrow\infty.
\]

The normality criterion shows that \(F\) is nonnormal. Since \(F(0)=1-1=0\)
and \(F'=f\), the required based primitive is exactly \(F\). \(\square\)

## Normalization is immaterial

The source does not impose \(f(0)=0\) or \(f'(0)=1\). Even imposing both
conditions would not rescue the assertion. Let

\[
 d=f'(0)=a(1+a)-b(1+b)=\frac{-5+51i}{500}\ne0,
 \qquad h(z)=\frac{f(z)-ic}{d}.
\]

Then \(h\) is univalent, \(h(0)=0\), \(h'(0)=1\), and its based primitive
is \(H(z)=(F(z)-icz)/d\). At \(z_n\), the values \(H(z_n)=-icz_n/d\)
are bounded, whereas

\[
 (1-z_n^2)|H'(z_n)|
 =\frac{c}{|d|}(2t_n-t_n^2)(t_n^{-1-b}-1)
 \longrightarrow\infty.
\]

Therefore \(H\) is also nonnormal.

## References

1. P. Lappan, *On the Normality of Derivatives of Functions, II*, Journal
   of the London Mathematical Society (2) 24 (1981), 495–501,
   [DOI 10.1112/jlms/s2-24.3.495](https://doi.org/10.1112/jlms/s2-24.3.495).
   The publisher abstract confirms the counterexample; the attribution
   to Theorem 5 is independently recorded in the published source below.
2. J. Gröhn, *On non-normal solutions of linear differential equations*,
   Proceedings of the American Mathematical Society 145 (2017), 1209–1220,
   [DOI 10.1090/proc/13292](https://doi.org/10.1090/proc/13292).
   The inspected published-format copy has equation (12) on PDF page 9
   and the Lappan reference [16] on PDF page 12. It was published
   electronically on September 8, 2016.
3. W. K. Hayman and E. F. Lingham, *Research Problems in Function Theory
   (New Edition)*, [arXiv:1809.07200v2](https://arxiv.org/abs/1809.07200v2),
   Problem 6.80 and Update 6.80, printed page 145.

The mathematical argument above proves every assertion needed for the
counterexample; it does not depend on obtaining Lappan's paywalled full text
or accepting a numerical experiment as proof. No novelty claim is made.
