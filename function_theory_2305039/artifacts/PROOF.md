# Derivative-mean radii under subordination: partial results for Problem 5.39

## Status and scope

This note does **not** determine the optimal radius for every exponent and does **not** claim a complete solution of Hayman–Lingham Problem 5.39. It proves the following statements, without a claim of historical priority:

1. \(r_p=1/2\) for every \(0<p\le2\).
2. \(p\mapsto r_p\) is nonincreasing.
3. \(\sqrt2-1\le r_p\le1/2\) for every finite \(p>0\).
4. \(r_p\le99/200\) for every \(p\ge14\), with an explicit rational counterexample at \(p=14\).
5. \(\lim_{p\to\infty}r_p=\sqrt2-1\).

The exact values for finite \(p>2\) remain undetermined here. In particular, neither the extent of a possible plateau \(r_p=1/2\) to the right of 2 nor a formula after that plateau is established.

## 1. The precise question

Let \(\mathbb D=\{z:|z|<1\}\). All functions below are holomorphic. The relation \(g\prec f\) means that
\[
 g=f\circ\phi,\qquad \phi:\mathbb D\to\mathbb D,\quad \phi(0)=0.
\]
There is no assumption that \(f\) is univalent. For \(p>0\), set
\[
 M_p(r,h)^p=\frac1{2\pi}\int_0^{2\pi}|h(re^{it})|^p\,dt.
\]
Define \(r_p\) as the supremum of the numbers \(R\) such that
\[
 M_p(r,(f\circ\phi)')\le M_p(r,f')
 \quad\text{for every }0<r<R\text{ and every such }f,\phi. \tag{1}
\]
This is the question in [Hayman–Lingham, Problem 5.39 and Update 5.39](https://arxiv.org/abs/1809.07200), printed pp. 99–100. The update is a 2018 historical statement, not a verification of the problem's current literature status.

Write \(\langle v\rangle_r=(2\pi)^{-1}\int_0^{2\pi}v(re^{it})\,dt\).

## 2. Elementary subordination facts and the quadratic radius

### Lemma 1 (integral-mean contraction)

For every \(s>0\) and every holomorphic \(H\) on a neighborhood of the closed disk \(\overline{r\mathbb D}\),
\[
 \langle |H\circ\phi|^s\rangle_r\le\langle |H|^s\rangle_r. \tag{2}
\]

**Proof.** Schwarz's lemma gives \(|\phi(z)|\le|z|\). Let \(U\) be the harmonic extension to \(r\mathbb D\) of the continuous boundary function \(|H|^s\). Subharmonicity gives \(|H|^s\le U\) inside. The function \(U\circ\phi\) is harmonic, and its circle mean equals \(U(\phi(0))=U(0)\), the boundary mean of \(|H|^s\). This proves (2), taking a radial limit if needed. The same argument applies to a function holomorphic on \(\mathbb D\) for each fixed \(r<1\). \(\square\)

### Lemma 2 (the classical quadratic derivative estimate)

For every \(f\), \(\phi\) as in (1),
\[
 \langle |(f\circ\phi)'|^2\rangle_r
 \le\langle |f'|^2\rangle_r\qquad(0<r\le1/2). \tag{3}
\]

**Proof.** Write \(f(z)=\sum_{n\ge0}a_nz^n\) and \(f(\phi(z))=\sum_{n\ge0}b_nz^n\). For an integer \(N\ge1\), put \(F_N(z)=\sum_{n=1}^Na_nz^n\). The first \(N\) nonconstant coefficients of \(F_N\circ\phi\) are \(b_1,\ldots,b_N\), because \(\phi(0)=0\). Parseval and Lemma 1, applied on radius \(t<1\), imply
\[
 \sum_{n=1}^N|b_n|^2t^{2n}
 \le\langle |F_N\circ\phi|^2\rangle_t
 \le\sum_{n=1}^N|a_n|^2t^{2n}.
\]
Letting \(t\uparrow1\) proves
\[
 B_N:=\sum_{n=1}^N|b_n|^2\le A_N:=\sum_{n=1}^N|a_n|^2. \tag{4}
\]
For \(0<r\le1/2\), the weights \(\lambda_n=n^2r^{2n-2}\) are nonnegative and nonincreasing, since
\[
 \frac{\lambda_{n+1}}{\lambda_n}
 =r^2\left(\frac{n+1}{n}\right)^2\le1.
\]
Finite summation by parts gives
\[
 \sum_{n=1}^N\lambda_n|b_n|^2
 =\lambda_NB_N+\sum_{n=1}^{N-1}(\lambda_n-\lambda_{n+1})B_n
 \le\sum_{n=1}^N\lambda_n|a_n|^2.
\]
Let \(N\to\infty\) and apply Parseval to the derivatives. \(\square\)

This is the classical Goluzin estimate. The coefficient argument is also supported by the complete proofs of Lemmas 5 and 6 in [Reich (1954), pp. 263–265](https://msp.org/pjm/1954/4-2/pjm-v4-n2-p08-s.pdf). A proof has been included to make the later deduction independent of access to Goluzin's original Russian paper.

## 3. Local extension and downward extrapolation in the exponent

For an exponent \(q>0\), radius \(r<1\), and fixed \(\phi\), consider the property
\[
 \langle |\phi'|^q|h\circ\phi|^q\rangle_r
 \le\langle |h|^q\rangle_r. \tag{5}
\]
If (5) holds for every \(h\) holomorphic on \(\mathbb D\), it also holds for every \(h\) holomorphic on a neighborhood of \(\overline{r\mathbb D}\). Indeed, the Taylor polynomials approximate such an \(h\) uniformly on that closed disk, and hence also on its image under \(\phi\). The factor \(\phi'\) is bounded on the circle, so passage to the limit in both integrals is justified. This local extension is important: a fractional power constructed below need not extend to all of \(\mathbb D\).

### Lemma 3 (downward extrapolation)

If (5) holds for every \(h\) holomorphic on \(\mathbb D\), then its analogue with \(q\) replaced by \(p\) holds for every \(0<p<q\).

**Proof.** Fix an input \(h\). The zero function causes no issue. First assume \(h\) has no zeros on \(|z|=r\). Let \(B\) be the finite Blaschke product for the disk \(r\mathbb D\) whose zeros, including multiplicities, are precisely those of \(h\) in that disk. A zero \(a\ne0\) contributes
\[
 B_a(z)=\frac{r(z-a)}{r^2-\overline a z};
\]
a zero at 0 contributes \(z/r\). Thus \(|B|=1\) on the boundary and \(|B|\le1\) inside. After removing the apparent singularities, \(K=h/B\) is holomorphic and zero-free on a neighborhood of the closed radius-\(r\) disk, with
\[
 |h|=|K|\quad (|z|=r),\qquad |h|\le|K|\quad (|z|\le r).
\]
There is a holomorphic logarithm of \(K\) on a slightly larger disk. Set \(F=\exp((p/q)\log K)\). Then \(|F|^q=|K|^p\).

Put \(\alpha=p/q\),
\[
 A=|F\circ\phi|^q|\phi'|^q,\qquad D=|F\circ\phi|^q
\]
on the radius-\(r\) circle. The local extension of (5), Lemma 1, and Hölder's inequality give
\[
\begin{aligned}
 \langle |\phi'|^p|h\circ\phi|^p\rangle_r
 &\le\langle |\phi'|^p|K\circ\phi|^p\rangle_r\\
 &=\langle A^\alpha D^{1-\alpha}\rangle_r\\
 &\le\langle A\rangle_r^\alpha\langle D\rangle_r^{1-\alpha}\\
 &\le\langle |F|^q\rangle_r
 =\langle |h|^p\rangle_r.
\end{aligned} \tag{6}
\]
If \(h\) has a zero on the circle, apply the argument to \(h_s(z)=h(sz)\) for a sequence \(s\uparrow1\) avoiding boundary zeros, and pass uniformly to the limit. Such a sequence exists because the zeros of a nonzero holomorphic function are isolated; only finitely many relevant zero moduli occur in a compact annulus about the circle. \(\square\)

Every holomorphic \(h\) on \(\mathbb D\) has a holomorphic primitive there. Therefore the hypothesis of Lemma 3 at exponent \(q\) is exactly the derivative inequality at that exponent and radius. It follows that every radius interval admissible for \(q\) is admissible for \(p<q\), proving
\[
 r_p\ge r_q\qquad(0<p<q). \tag{7}
\]
By Lemma 2 and Lemma 3, (1) holds through radius \(1/2\) for every \(0<p\le2\). Conversely, \(f(z)=z\), \(\phi(z)=z^2\) give
\[
 M_p(r,(f\circ\phi)')=2r,\qquad M_p(r,f')=1,
\]
for every \(p>0\). Consequently
\[
 \boxed{r_p=1/2\quad(0<p\le2)},\qquad r_p\le1/2\quad(p>0). \tag{8}
\]

## 4. The universal lower bound and the large-exponent limit

Put \(\rho=\sqrt2-1\). Write \(\phi(z)=z\omega(z)\), where \(|\omega|\le1\). Schwarz–Pick gives
\[
 |\phi'(z)|\le t+\frac{r(1-t^2)}{1-r^2},\qquad r=|z|,\quad t=|\omega(z)|\in[0,1]. \tag{9}
\]
This also covers constant unimodular \(\omega\) by direct inspection. When \(r\le\rho\), put \(k=r/(1-r^2)\le1/2\). Then
\[
 1-t-k(1-t^2)=(1-t)[1-k(1+t)]\ge0.
\]
Thus \(|\phi'|\le1\) throughout the radius-\(\rho\) disk. The chain rule and Lemma 1 prove
\[
 r_p\ge\rho\qquad(p>0). \tag{10}
\]

This pointwise radius cannot be enlarged. Fix \(\rho<r<1\), and put
\[
 t=\frac{1-r^2}{2r}\in(0,1),\qquad
 a=\frac{t-r}{1-tr}\in(-1,1),\qquad
 \phi_a(z)=z\frac{a+z}{1+az}.
\]
The Möbius factor maps \(\mathbb D\) onto itself, so \(\phi_a\) is an admissible subordinating map. At the positive real point \(r\), it satisfies
\[
 \phi_a'(r)=t+\frac{r(1-t^2)}{1-r^2}
 =k+\frac1{4k}>1,
\]
where now \(k>1/2\) and the strict inequality follows from
\(k+1/(4k)-1=(2k-1)^2/(4k)>0\).

For the continuous circle function \(|\phi_a'|\), its normalized \(L^p\) means tend to its maximum as \(p\to\infty\). Thus \(M_p(r,\phi_a')>1\) for every sufficiently large \(p\). Taking \(f(z)=z\), this is a failure of (1) at that radius, implying \(r_p\le r\). Since \(r>\rho\) was arbitrary, (10) proves
\[
 \boxed{\lim_{p\to\infty}r_p=\sqrt2-1}. \tag{11}
\]
It also proves that the analogous maximum-modulus problem at \(p=\infty\) has sharp radius \(\rho\). This auxiliary endpoint is not asserted to determine any finite \(r_p\).

## 5. A perturbation obstructing a universal half-radius

For real \(|a|<1\), let \(\phi_a(z)=z(a+z)/(1+az)\). On \(|z|=1/2\), expansion at \(a=0\) gives
\[
 \phi_a'(z)=2z+a(1-3z^2)+a^2(-2z+4z^3)+O(a^3).
\]
Writing \(z=e^{it}/2\) and dividing by \(2z\), this becomes
\[
 \frac{\phi_a'(z)}{2z}=1+av+a^2w+O(a^3),\quad
 v=e^{-it}-\tfrac34e^{it},\quad w=-1+\tfrac12e^{2it}.
\]
All expansions are uniform on the circle for \(a\) in a sufficiently small real neighborhood of 0. In particular the expanded quantity stays away from zero, so the real power has its ordinary uniform Taylor expansion. The elementary circle averages are
\[
 \langle\operatorname{Re}v\rangle=0,\quad
 \langle\operatorname{Re}w\rangle=-1,\quad
 \langle|v|^2\rangle=\tfrac{25}{16},\quad
 \langle(\operatorname{Re}v)^2\rangle=\tfrac1{32}.
\]
Consequently
\[
 M_p(1/2,\phi_a')^p
 =1+\frac{p(p-16)}{64}a^2+O(a^3). \tag{12}
\]
For \(p>16\), sufficiently small nonzero \(a\) gives a violation with \(f(z)=z\). Continuity in \(r\) then gives a violation at some \(r<1/2\), and hence \(r_p<1/2\). This establishes a genuine obstruction, but does not determine \(r_p\). The next certificate gives a stronger obstruction for a smaller exponent.

## 6. An exact rational certificate at \(p=14\)

Take
\[
 a=\frac23,\qquad r=\frac{99}{200},\qquad
 f(z)=z+\frac{z^2}{10},\qquad
 \phi(z)=z\frac{a+z}{1+az},\qquad g=f\circ\phi.
\]
The denominator is nonzero on \(\mathbb D\), and
\[
 |1+az|^2-|a+z|^2=(1-a^2)(1-|z|^2)>0,
\]
so \(\phi\) maps \(\mathbb D\) into itself and fixes 0. Thus \(g\prec f\).

A direct differentiation gives
\[
 (g'(z))^7
 =\frac{(a+2z+az^2)^7(1+\tfrac{6a}{5}z+\tfrac15z^2)^7}{(1+az)^{21}}
 =\sum_{n\ge0}c_nz^n. \tag{13}
\]
The first eleven coefficients, in order \(n=0,\ldots,10\), are
\[
\begin{split}
(&128/2187,\;896/1215,\;563584/164025,\;
9755648/1476225,\\
&19731712/7381125,\;-1822435328/553584375,\\
&109413686144/24911296875,\;-12353279872/124556484375,\\
&-23093018368/2767921875,\;3793230310016/224201671875,\\
&-279418450304/14946778125).
\end{split}
\]
They can be obtained by multiplying the numerator of (13) by
\[
 (1+az)^{-21}=\sum_{n\ge0}(-a)^n\binom{20+n}{n}z^n.
\]
Parseval gives the rigorous lower bound
\[
 M_{14}(r,g')^{14}=\sum_{n\ge0}|c_n|^2r^{2n}
 \ge\sum_{n=0}^{10}c_n^2r^{2n}=:L.
\]
There is no approximation or discarded negative tail here. On the other side,
\[
 R:=M_{14}(r,f')^{14}
 =\sum_{n=0}^7\binom7n^2\frac{r^{2n}}{5^{2n}}.
\]
Exact rational arithmetic gives
\[
 L-R=
 \frac{171427691243281345585321685814196084464053669376850321}
 {29893556250000000000000000000000000000000000000000000000}
 >\frac1{200}>0. \tag{14}
\]
Therefore the desired inequality fails at \(p=14\), \(r=99/200\). It follows directly from definition (1), and then from (7), that
\[
 \boxed{r_p\le99/200\quad\text{for every }p\ge14}. \tag{15}
\]
The included standard-library verifier recomputes these coefficients in two ways and verifies (14) with integers and rational numbers only. Its role is an exact arithmetic check; the analytic statements and the nonnegative-tail argument are proved above.

## 7. The remaining gap

The results leave
\[
 \sqrt2-1\le r_p\le1/2\quad(2<p<14),\qquad
 \sqrt2-1\le r_p\le99/200\quad(p\ge14).
\]
The upper endpoints in these displayed intervals are bounds, not proposed exact answers. Neither (12) nor (14) shows optimality of its test family, and the maximum-modulus argument only controls the large-\(p\) limit. A full solution still needs a sharp inequality at each finite \(p>2\), together with matching admissible extremizers or an extremizing sequence. No such finite-exponent characterization is proved here.
