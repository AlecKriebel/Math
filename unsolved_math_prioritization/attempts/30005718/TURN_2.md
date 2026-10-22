# Turn2: eventual strict ultra-log-concavity in every proportional interior band

**Target:** 30005718 / OWR-14298007-013. **Substantive author count:**2/5.  
**Status:** partial. The original all-n, all-index claim remains unresolved.

## 1. Result and its exact quantifiers

Use the original V_n, coefficients v_n,k and degree d_n from TURN_1. Put m=n−4 and j=k−3. The result of this turn is:

**Theorem.** For every epsilon with 0<epsilon<3/4 there exists M_epsilon such that, for all integers m≥M_epsilon and all integer j satisfying

\[
\epsilon m\le j\le(3/2-\epsilon)m,
\tag{1}
\]

the original coefficient sequence is strictly ULC at k=j+3:

\[
k(d_n-k)v_{n,k}^2>
(k+1)(d_n-k+1)v_{n,k-1}v_{n,k+1}.
\tag{2}
\]

The threshold is not given numerically. It depends on the band epsilon. In particular this does not cover a sequence of indices with j/m→0 or j/m→3/2, nor does it establish every inequality for small n. The all-size endpoint certificates of TURN_1 remain separate.

The mechanism is a general sufficient bulk-ULC criterion for polynomial transfer matrices: after a uniform saddle-point expansion, the sign is controlled by a strict inequality between the Perron variance and the corresponding binomial variance. The saddle-point method and Perron theory are classical; no novelty claim is made for those tools.

## 2. Transfer matrix and exact Perron calculation

The positive two-state reduction in TURN_1 gives

\[
F_m(z):=z^{-3}V_{m+4}(z)=u(z)N(z)^m b(z),
\]
\[
u(z)=(2+z,2),\quad b(z)=(2,z)^T,\quad
N(z)=\begin{pmatrix}1+2z&z\\z+z^2&1+z\end{pmatrix}.
\tag{3}
\]

The degree of F_m is floor(3(m+1)/2); the original degree is this number plus3. Its coefficients are positive throughout its support by TURN_1.

For real z>0, N(z) is entrywise positive and its Perron eigenvalue is

\[
\lambda(z)=1+\frac32z+\frac z2\sqrt{5+4z}.
\tag{4}
\]

The other eigenvalue is obtained by changing the last plus sign to minus. It has strictly smaller absolute value. Define the logarithmic derivative operator D=z(d/dz) and

\[
\alpha(z)=D\log\lambda(z),\qquad
s(z)=D^2\log\lambda(z).
\tag{5}
\]

Here s is a variance parameter, not its square root. Set t=sqrt(5+4z), so t>sqrt5, and W=t²+2t−7>0. Direct rational differentiation gives

\[
\alpha=
\frac{(t^2-5)(3t^2+6t-5)}{2t(t+1)W},
\tag{6}
\]
\[
s=\frac{(t^2-5)P_6(t)}{4t^3(t+1)^2W^2},
\quad
P_6(t)=3t^6+10t^5+57t^4-4t^3-235t^2+250t+175,
\tag{7}
\]
\[
\frac32-\alpha=
\frac{3t^3+5t^2+9t-25}{2t(t+1)W}.
\tag{8}
\]

These quantities are positive. For (7), group 10t^5−4t³=t³(10t²−4)>0 and 57t⁴−235t²=t²(57t²−235)>0; all remaining terms are positive for t²>5. Formula (8) is positive by grouping5t²−25>0. Also alpha tends to0 as z↓0 and to3/2 as z→infinity. Thus alpha is a strictly increasing bijection from (0,infinity) to (0,3/2), because D alpha=s>0.

Most importantly,

\[
G(z):=\alpha(3/2-\alpha)-\frac32s
=
\frac{(t^2-5)^2(9t^4+36t^3-42t^2+100t+105)}
{8t^3(t+1)^2W^2}>0.
\tag{9}
\]

For positivity, 9t⁴−42t²=t²(9t²−42)>0 when t²>5, and every other numerator term is positive. Consequently

\[
\frac1{s(z)}-
\left(\frac1{\alpha(z)}+\frac1{3/2-\alpha(z)}\right)
=\frac{G(z)}{s(z)\alpha(z)(3/2-\alpha(z))}>0.
\tag{10}
\]

This exact identity, rather than numerical curvature evidence, supplies the strict ULC margin.

## 3. Uniform coefficient expansion on a compact saddle interval

Fix a compact interval J⊂(0,3/2). For alpha∈J, let rho=rho(alpha)>0 be its unique inverse under (5). The corresponding rho interval is compact in (0,infinity). We prove the uniform expansion needed for **adjacent** coefficients, rather than using only a leading local-limit approximation with an uncontrolled O(1/m) error.

Let P_+(z) be the analytic spectral projection onto lambda(z) in a neighborhood of any compact positive rho interval. The two eigenvalues remain separated there, so these neighborhoods may be chosen uniformly. Define

\[
H(z)=u(z)P_+(z)b(z).
\]

In this example direct projection gives H(z)=2(1+z)+(z²+6z+6)/sqrt(5+4z), which is positive at every positive real z. Equivalently this follows from positive Perron eigenvectors. The functions lambda,H and a real branch of log lambda extend holomorphically to a common narrow neighborhood of this real interval. Locally on each coefficient circle,

\[
F_m(z)=H(z)\lambda(z)^m+
H_-(z)\lambda_-(z)^m,
\tag{11}
\]

and the second term is uniformly exponentially smaller there.

### No competing coefficient-circle saddle

For z=rho exp(i theta), with theta not a multiple of2pi,

\[
|1+2\rho e^{i\theta}|<1+2\rho,
\qquad |1+\rho e^{i\theta}|<1+\rho.
\]

Also |rho exp(i theta)+rho² exp(2i theta)|≤rho+rho². Thus, using a strictly positive right Perron vector of N(rho), both weighted row sums of |N(rho exp(i theta))| are strictly less than lambda(rho). On any compact rho interval and |theta| bounded away from0, the normalized weighted operator norm is at most1−eta for a common eta>0. Taking powers proves uniform exponential suppression away from the positive-real saddle. This avoids an unverified aperiodicity assumption.

### The local integral and its first correction

By Cauchy's formula, for an integer j with j/m=alpha,

\[
[z^j]F_m(z)=\frac{\rho^{-j}}{2\pi}
\int_{-\pi}^{\pi}F_m(\rho e^{i\theta})e^{-ij\theta}\,d\theta.
\tag{12}
\]

Let kappa_l=D^l log lambda at rho. Taylor expansion at the saddle gives

\[
\log\lambda(\rho e^{i\theta})-
\log\lambda(\rho)-i\alpha\theta
=-\frac{s\theta^2}{2}-\frac{i\kappa_3\theta^3}{6}
+\frac{\kappa_4\theta^4}{24}+O(\theta^5).
\tag{13}
\]

The error is uniform on the compact interval, and s has a positive minimum. Similarly

\[
H(\rho e^{i\theta})=H+i(DH)\theta-
\tfrac12(D^2H)\theta^2+O(\theta^3).
\]

On setting y=sqrt(m)theta, the odd terms of order m^(-1/2) integrate to zero on a symmetric local interval. The Gaussian moments of orders2,4,6 yield

\[
[z^j]F_m(z)=
\frac{H(\rho)\lambda(\rho)^m\rho^{-j}}
{\sqrt{2\pi m s(\rho)}}
\left(1+\frac{A(\rho)}m+O(m^{-3/2})\right),
\tag{14}
\]

uniformly in alpha∈J, where

\[
A=-\frac{D^2H}{2Hs}
+\frac{(DH)\kappa_3}{2Hs^2}
+\frac{\kappa_4}{8s^2}
-\frac{5\kappa_3^2}{24s^3}.
\tag{15}
\]

Here all functions are evaluated at rho. In particular A is smooth on the compact interval.

For explicit remainder justification, take a small fixed angular neighborhood where the real part in (13) is at most−c theta² uniformly. Split it at |theta|=m^(-2/5). The intermediate part is exponentially small in m^(1/5); the rest of the circle is exponentially small by the preceding weighted-norm bound. In the inner part, the Taylor remainders and the cubic/quartic exponential expansion are bounded by m^(-3/2) times a fixed polynomial in |y| times exp(−c' y²). Its integral is bounded uniformly. Extending the local Gaussian integrals to the whole real line incurs an exponentially small error. The spectral remainder in (11) has the same negligible status. These estimates give the uniform relative remainder asserted in (14), since H and s are bounded away from zero there.

This is the standard large-powers saddle-point argument with its hypotheses and first correction exposed. Merely replacing (14) with a leading term times1+O(1/m), without controlled dependence on alpha, would not justify the next section.

## 4. Adjacent ratios and the binomial normalization

Write c_m,j=[z^j]F_m. On any slightly smaller compact alpha interval, (14) implies

\[
\log c_{m,j}=mS(\alpha)-\tfrac12\log m+B(\alpha)
+\frac{A(\rho(\alpha))}{m}+O(m^{-3/2}),
\tag{16}
\]

with

\[
S(\alpha)=\log\lambda(\rho)-\alpha\log\rho,
\qquad B(\alpha)=\log\!\frac{H(\rho)}{\sqrt{2\pi s(\rho)}}.
\]

The saddle equation yields S'=−log rho and S''=−1/s. Taking the central second difference at step1/m in (16), and using bounded derivatives of S,B,A on a compact interval, gives

\[
\log\frac{c_{m,j}^2}{c_{m,j-1}c_{m,j+1}}
=\frac1{m s(\rho)}+O(m^{-3/2}).
\tag{17}
\]

No differentiability of the final error term is assumed: the three uniformly bounded errors themselves remain O(m^(-3/2)).

The original coefficients satisfy v_n,k=c_m,j with k=j+3 and n=m+4. Since d_n=(3/2)m+O(1), uniformly on the same band,

\[
\log\frac{(k+1)(d_n-k+1)}{k(d_n-k)}
=\frac1m\left(\frac1\alpha+
\frac1{3/2-\alpha}\right)+O(m^{-2}).
\tag{18}
\]

Subtracting (18) from (17), equation (10) gives a positive leading coefficient1/m. Its minimum on the compact alpha band is strictly positive. The uniform O(m^(-3/2)) error is eventually smaller, proving (2) simultaneously for every integer index in (1). To handle neighboring indices at the endpoints of the prescribed band, apply the coefficient expansion on the slightly enlarged compact interval [epsilon/2,3/2−epsilon/2]. This completes the theorem.

## 5. A general transfer-matrix criterion

The same proof gives the following sufficient condition, addressing part of the source's request for tools beyond this one matrix.

Suppose nonnegative polynomial matrices N(z) and nonzero nonnegative polynomial vectors u(z),b(z) generate F_m=uN^m b. Suppose their degrees, after any fixed monomial shift, are beta m+O(1), beta>0. On a compact positive saddle interval assume:

1. N(rho) has a simple positive dominant eigenvalue lambda(rho), with analytic spectral projection and positive amplitude H=uP_+b.
2. Other spectral contributions near that interval and coefficient-circle contributions away from theta=0 are uniformly exponentially smaller; a strict weighted row-sum comparison is one sufficient check.
3. alpha=D log lambda is strictly increasing, with variance s=D² log lambda>0.
4. At all saddles in the interval, s<alpha(beta−alpha)/beta, with0<alpha<beta.

Then the corresponding coefficients are eventually strictly ULC throughout each compact index-proportion band in that interval. The proof is exactly (12)–(18), with beta in place of3/2. It is local in index proportion and does not claim complete ULC for the full row. If the strict variance inequality is reversed on a compact interval, the same expansion instead certifies eventual failure there. Thus the criterion can detect asymptotic obstructions as well as provide sufficient conditions.

## 6. Boundaries, unsuccessful shortcuts and remaining gap

The compact saddle constants may deteriorate as rho→0 or rho→infinity. At rho=0 the two transfer eigenvalues coalesce, and at rho→infinity their absolute-value ratio approaches1. This proof therefore supplies no uniform threshold as epsilon↓0. The shrinking edge bands remain genuine mathematical work, even though the first/last adjacent inequalities were settled in TURN_1.

A staggered trivariate lifting was also considered as a route to an all-n induction. One candidate cubic certificate was S=x²v+xyv+uyv+2uxv+x²y+xy²+ux². Its u derivative is x²+2xv+yv; this quadratic has Hessian determinant−2 and two positive eigenvalues. Thus S is not Lorentzian and cannot itself supply a Lorentzian-symbol certificate. This does not disprove every possible orbit-restricted preservation statement. No unsupported lift-preservation theorem is used here.

**Sharp gap after two turns:** the all-n original ULC inequalities in the lower and upper shrinking transition regions, together with a uniform bridge to the proportional-band theorem. Neither a finite numerical range nor a collection of fixed-epsilon asymptotic theorems closes that gap.

The general saddle-point method is credited to the classical literature, for example Flajolet–Sedgewick, *Analytic Combinatorics*, ChapterVIII, TheoremVIII.8 on printed pp.587–588 of the linked author PDF (large powers and uniform full expansions), available through the [authors' booksite](https://ac.cs.princeton.edu/home/). Here the matrix-specific spectral, variance and aperiodicity calculations are supplied explicitly. The source's known eigenvalues are not claimed as a new result. Historical priority of this scoped bulk consequence has not been certified.

**Original status:** unresolved,2/5 substantive turns. Subjective planning completion estimate30%; this is not a correctness or novelty probability.
