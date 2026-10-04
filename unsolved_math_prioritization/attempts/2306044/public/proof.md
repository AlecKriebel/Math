# A real-coefficient counterexample to integral-convolution closure

## Exact target and historical status

Let \(\mathbb D=\{z:|z|<1\}\), let \(S\) be the class of injective holomorphic functions on \(\mathbb D\) normalized by \(f(0)=0\), \(f'(0)=1\), and let \(S_R\) consist of its real-Taylor-coefficient members. For
\[
f(z)=\sum_{n\ge1}a_nz^n,\qquad g(z)=\sum_{n\ge1}b_nz^n,
\]
put
\[
(f\otimes g)(z)=\sum_{n\ge1}\frac{a_nb_n}{n}z^n.
\]
Problem 6.44 asks whether \(f,g\in S_R\) always implies \(f\otimes g\in S_R\). **The answer is no, even with \(g=f\).**

This is a reconstruction of an already known negative result, not a new-resolution claim. Hayman and Lingham, Update 6.44, explicitly credit Bshouty (1980). The reconstruction below is self-contained apart from the classical Fekete–Szegő coefficient inequality, precisely stated and sourced below. It does not purport to reproduce the unread Bshouty article verbatim or identify its particular counterexample.

## 1. The classical obstruction

The Fekete–Szegő theorem says that if
\(F(z)=z+c_2z^2+c_3z^3+\cdots\in S\), then for \(0\le\lambda<1\),
\[
|c_3-\lambda c_2^2|\le 1+2\exp\left(-\frac{2\lambda}{1-\lambda}\right).
\tag{1}
\]
We use only the necessary bound at \(\lambda=1/2\):
\[
|c_3-c_2^2/2|\le1+2e^{-2}.
\tag{2}
\]
Reference: Pfluger (1985), p. 447, equation (1), with the full variational proof in that article; the original source is Fekete and Szegő (1933). Thus (2) applies to every function in \(S\), without starlikeness, convexity, or real-coefficient hypotheses.

## 2. Construction of a genuine member of \(S_R\)

For the moment fix \(T>0\). For \(0\le t\le T\) define
\[
q(t)=e^{t-T},\qquad
p_t(w)=\frac{1-w^2}{1+2q(t)w+w^2}.
\tag{3}
\]
Let \(w_t(z)\) solve the initial-value problem
\[
\frac{d}{dt}w_t(z)=-w_t(z)p_t(w_t(z)),\qquad w_0(z)=z.
\tag{4}
\]
We establish the required facts about this flow directly.

### 2.1 Positive real part and existence on the entire time interval

Choose \(\theta(t)\in[0,\pi]\) with \(\cos\theta(t)=-q(t)\), and write \(\xi(t)=e^{i\theta(t)}\). Elementary algebra gives
\[
p_t(w)=\frac12\left(\frac{1+\xi(t)w}{1-\xi(t)w}
+\frac{1+\overline{\xi(t)}w}{1-\overline{\xi(t)}w}\right).
\tag{5}
\]
Each summand has strictly positive real part for \(|w|<1\), because
\[
\operatorname{Re}\frac{1+\xi w}{1-\xi w}
=\frac{1-|w|^2}{|1-\xi w|^2}>0.
\]
Consequently \(p_t\) is holomorphic on \(\mathbb D\), continuous in \(t\), and \(\operatorname{Re}p_t>0\). The endpoint \(q(T)=1\) causes no interior singularity; there \(p_T(w)=(1-w)/(1+w)\).

Along any solution in \(\mathbb D\),
\[
\frac{d}{dt}|w_t(z)|^2=-2|w_t(z)|^2\operatorname{Re}p_t(w_t(z))\le0.
\tag{6}
\]
Thus the solution starting at \(|z|\le r<1\) stays in \(|w|\le r\). On that compact disk the vector field and its \(w\)-derivative are bounded uniformly for \(0\le t\le T\). The ordinary existence, uniqueness, and continuation theorem therefore gives a solution on the full interval. Holomorphic dependence on the initial value follows from Picard iteration locally in time, then composition over finitely many subintervals. Hence \(z\mapsto w_t(z)\) is a holomorphic disk self-map.

### 2.2 Injectivity, symmetry, and normalization

If two trajectories meet at some time, uniqueness applied backwards on their common compact time interval forces their initial values to agree. Therefore every \(w_t\) is injective. Since the vector field in (4) has real coefficients, uniqueness also gives
\[
w_t(\overline z)=\overline{w_t(z)}.
\]
We have \(w_t(0)=0\), and differentiation at zero in (4) yields \(w_t'(0)=e^{-t}\).

The Koebe function \(k(u)=u/(1-u)^2\) is holomorphic and injective on \(\mathbb D\): the equation \(k(u)=k(v)\) reduces to
\((u-v)(1-uv)=0\), and \(|uv|<1\). Define
\[
f_T(z)=e^T k(w_T(z))=e^T\frac{w_T(z)}{(1-w_T(z))^2}.
\tag{7}
\]
It is holomorphic, injective, real-symmetric, and satisfies \(f_T(0)=0\), \(f_T'(0)=1\). Thus \(f_T\in S_R\). This argument needs no converse Loewner representation theorem.

## 3. Exact coefficient calculation

Expand
\[
w_t(z)=e^{-t}\bigl(z+A(t)z^2+B(t)z^3+O(z^4)\bigr).
\]
From (3),
\[
p_t(w)=1-2q(t)w+(4q(t)^2-2)w^2+O(w^3).
\]
Comparing coefficients in (4), with \(A(0)=B(0)=0\), gives
\[
A'(t)=2e^{-T},\qquad
B'(t)=4e^{-T}A(t)-4e^{-2T}+2e^{-2t}.
\tag{8}
\]
Integration gives
\[
A(t)=2te^{-T},\qquad
B(t)=(4t^2-4t)e^{-2T}+1-e^{-2t}.
\tag{9}
\]
Since \(k(u)=u+2u^2+3u^3+\cdots\), equation (7) implies
\[
\begin{aligned}
a_2(T)&=A(T)+2e^{-T}=2(T+1)e^{-T},\\
a_3(T)&=B(T)+4e^{-T}A(T)+3e^{-2T}\\
&=1+(4T^2+4T+2)e^{-2T}.
\end{aligned}
\tag{10}
\]
In particular, for \(T=1/2\), the function \(f=f_{1/2}\in S_R\) has
\[
a_2=3e^{-1/2},\qquad a_3=1+5e^{-1}.
\tag{11}
\]

## 4. The convolution violates the necessary inequality

Let \(h=f\otimes f\). This is a holomorphic, normalized, real-coefficient function on \(\mathbb D\). To check convergence without any univalent-coefficient theorem, fix \(r<1\) and choose \(R\) with \(\sqrt r<R<1\). Cauchy's bound \(|a_n|\le M_R R^{-n}\) makes
\(\sum |a_n|^2r^n/n\) converge by comparison with \(M_R^2\sum(r/R^2)^n/n\).

Its first coefficients are
\[
c_2=\frac{a_2^2}{2}=\frac{9}{2e},\qquad
c_3=\frac{a_3^2}{3}=\frac{(1+5/e)^2}{3}.
\tag{12}
\]
Consequently
\[
\begin{aligned}
\left(c_3-\frac12c_2^2\right)-(1+2e^{-2})
&=-\frac23+\frac{10}{3e}-\frac{91}{24e^2}\\
&=\frac{-16e^2+80e-91}{24e^2}\\
&=-\frac{2}{3e^2}\left(e-\frac74\right)\left(e-\frac{13}4\right)>0.
\end{aligned}
\tag{13}
\]
The final sign is exact: \(2<e<3\) follows from the exponential series, and hence \(7/4<e<13/4\). For the upper estimate one may use \(n!\ge2^{n-1}\) for \(n\ge2\), with strict inequality for some terms, to obtain
\(e=2+\sum_{n\ge2}1/n!<2+\sum_{n\ge2}2^{-(n-1)}=3\).

Equation (13) says the real number \(c_3-c_2^2/2\) already exceeds the positive upper bound in (2). Its absolute value does too. Therefore \(h\notin S\), although \(f\in S_R\), and the proposed closure assertion is false. \(\square\)

## Scope and limitations

- This settles the exact weighted operation with the factor \(1/n\), not the ordinary Hadamard product.
- The counterexample uses two identical factors, both genuinely univalent on the full open disk.
- No claim is made that \(h\) fails local univalence, or that a particular pair of collision points has been located. Failure of the necessary coefficient bound suffices for noninjectivity.
- The typically-real closure assertion is not contradicted: typical reality is weaker than univalence.
- The only specialized external theorem used is (1), with its verified source and hypotheses. The numerical controls are supplementary and are not a substitute for the flow argument or that theorem.
- Historical priority belongs to the known negative resolution; the precise relationship of this reconstruction to Bshouty's original construction was not checked because the original article's full text was inaccessible.
