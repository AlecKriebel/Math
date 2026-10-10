# An explicit endpoint obstruction for bicyclic-operator cyclicity

## Status and scope

The AI-assisted mathematics has been accepted as rigorous partial by an independent internal mathematical audit. The proof and audit are unrefereed; no external human peer review or formal proof-assistant certification is claimed.

This note does **not** resolve problem 30001611 / OWR-4531-003. It supplies a fully proved endpoint model and an explicit obstruction to the cutoff-density step in the known proof. It does not prove that either operator constructed below is noncyclic. No novelty, priority, exhaustive-literature-search, or global-open-status claim is made.

The target is to find a bounded invertible bicyclic operator T on a complex separable Banach space with

\[
 \|T^n\|=O(n^k),\qquad \log\|T^{-n}\|=O(\sqrt n),\qquad
 \mathbb T\not\subseteq\sigma_p(T^*),
\]

for some integer k≥0, which is not cyclic; alternatively, to prove cyclicity under all these hypotheses. Here bicyclicity uses all integer powers and cyclicity uses nonnegative powers. The condition on the adjoint is noncontainment, not disjointness.

The endpoint constructions below have k=0. One has empty adjoint point spectrum; the other has adjoint point spectrum exactly T\{1}. Thus both satisfy the precise spectral hypothesis, including its weaker noncontainment interpretation.

## 1. The weight and two spaces

Write z(e^{it})=e^{it}, and set

\[
 w(j)=\exp\sqrt{(-j)_+}\quad(j\in\mathbb Z).
\]

The weighted Fourier algebra A consists of the functions

\[
 f(z)=\sum_{j\in\mathbb Z}a_jz^j,\qquad
 \|f\|_A=\sum_{j\in\mathbb Z}|a_j|w(j)<\infty.
\]

Every such series converges uniformly. The inequality

\[
 \sqrt{(-(j+l))_+}\leq \sqrt{(-j)_+}+\sqrt{(-l)_+}
\]

shows that w is submultiplicative. Consequently A is a unital commutative Banach algebra under pointwise multiplication. Laurent polynomials are dense, so A is separable.

Define also the Hilbert space

\[
 H=\left\{\sum a_jz^j:\ \sum |a_j|^2w(j)^2<\infty\right\}.
\]

This notation identifies H with a subspace of L²(T), or equivalently with the weighted sequence space. Define S on A and H by Sf=zf. Its inverse is multiplication by z^{-1}.

For every integer n≥0,

\[
 \|S^n\|_A=\|S^n\|_H=1,
 \qquad \|S^{-n}\|_A=\|S^{-n}\|_H=e^{\sqrt n}.       \tag{1}
\]

Indeed, the norm of a shift of a weighted ℓ¹ or ℓ² space is the supremum of the ratios of the corresponding weights. The forward ratios are at most 1 and are 1 on the nonnegative indices. For inverse powers,

\[
 \sqrt{(n-j)_+}-\sqrt{(-j)_+}\leq\sqrt n,
\]

with equality at j=0. This proves (1). The spectral-radius formula applied to S and S^{-1} gives σ(S)⊆T on both spaces.

The constant function 1 is bicyclic on H. Moreover,

\[
 \sigma_p(S^*|_{H^*})=\varnothing.                    \tag{2}
\]

To see this, a nonzero eigenfunctional with eigenvalue λ has values b_j=λ^j b_0 on z^j. Eigenvalues must lie in T, while continuity on H requires (b_j/w(j)) to be square-summable. On j≥0 this would be the nonzero constant-modulus sequence |b_0|, an impossibility. If b_0=0, the functional is zero by Laurent-polynomial density.

Thus the Hilbert-space shift in the original authors' endpoint conjecture satisfies every target hypothesis. Its cyclicity is not determined here.

## 2. A Banach model with exactly one missing adjoint eigenvalue

Let

\[
 I=\{f\in A:f(1)=0\},\qquad T=S|_I,
 \qquad v=z-1.
\]

This is a closed, complex, separable Banach space invariant under S and S^{-1}.

### Proposition 1

The operator T is invertible and bicyclic with bicyclic vector v. It satisfies

\[
 \|T^n\|=1\quad(n\geq0),\qquad
 \lim_{n\to\infty}\frac{\log\|T^{-n}\|}{\sqrt n}=1,
 \qquad \sigma_p(T^*)=\mathbb T\setminus\{1\}.       \tag{3}
\]

#### Proof

First,

\[
 I=\overline{(z-1)A}^{\,A}.                          \tag{4}
\]

A continuous functional annihilating (z-1)A has equal values on z^{j+1} and z^j for every j∈Z. It is therefore a scalar multiple of evaluation at 1, by density of Laurent polynomials. Hahn–Banach now proves (4). Since Laurent polynomials are dense in A, (4) proves bicyclicity of v.

The upper norm estimates follow by restriction from (1). The vector v and all its nonnegative translates have norm 2, so ∥T^n∥=1. For n≥1,

\[
 \|T^{-n}\|\geq
 \frac{e^{\sqrt{n-1}}+e^{\sqrt n}}2
 \geq \frac12 e^{\sqrt n}.
\]

Combined with ∥T^{-n}∥≤e^{√n}, this proves the limit in (3).

For ζ∈T\{1}, evaluation at ζ restricts to a nonzero continuous functional on I, since v(ζ)≠0. It is a T*-eigenfunctional with eigenvalue ζ.

To exclude eigenvalue 1, put

\[
 C_N=\frac1N\sum_{j=0}^{N-1}T^j.
\]

These operators have norm at most 1. For f=(z-1)g with g∈A,

\[
 C_N f=\frac{z^N-1}{N}g,\qquad
 \|C_N f\|_A\leq\frac{2\|g\|_A}{N}.
\]

By (4), C_N f→0 for every f∈I. If T*φ=φ, then φ(C_N f)=φ(f), forcing φ=0. Finally the growth bounds put the entire spectrum of T, hence every adjoint eigenvalue, in T. This proves (3). ∎

The claim that v is bicyclic is not a claim that v is cyclic. In fact, all nonnegative polynomial multiples of v have no negative Fourier coefficients, so v is not cyclic. This fact alone says nothing about the existence of a different cyclic vector.

## 3. Explicit endpoint functionals

Fix a real parameter

\[
 0<a<\frac18.
\]

For |z|<1 define

\[
 V_a(z)=\exp\left(a\frac{1+z}{1-z}\right)
       =\sum_{m\geq0}v_m(a)z^m,
 \qquad
 U_a(z)=\exp\left(-a\frac{1+z}{1-z}\right)
       =\sum_{m\geq0}u_m(a)z^m.
\]

The real part of (1+z)/(1-z) is positive in the disk, so |U_a(z)|≤1. Parseval applied at radius r<1 and then monotone convergence give

\[
 \sum_{m\geq0}|u_m(a)|^2\leq1.                     \tag{5}
\]

For m≥1 the following explicit estimate holds:

\[
 |v_m(a)|\leq e^a\exp\bigl(2\sqrt{2am}\bigr).       \tag{6}
\]

For completeness, on |z|=r we have Re((1+z)/(1−z))=(1−r²)/|1−z|²≤(1+r)/(1−r). Use Cauchy's coefficient estimate at r=e^{-s}. Since

\[
 \frac{1+e^{-s}}{1-e^{-s}}=1+\frac2{e^s-1}\leq1+\frac2s,
\]

we have |v_m(a)|≤exp(a+2a/s+ms). Choosing s=√(2a/m) proves (6). The constant 2√(2a) is strictly less than 1.

For f=∑a_jz^j in A or H, define the complex-linear functional

\[
 L_a(f)=\sum_{m\geq0}v_m(a)a_{-m}
              -\sum_{m\geq0}u_m(a)a_m.             \tag{7}
\]

The constant coefficient is counted once in each sum, as intended: its net coefficient is e^a−e^{-a}. For negative indices, (6) and Cauchy–Schwarz give absolute convergence on H, because

\[
 \sum_{m\geq1} |v_m(a)|^2e^{-2\sqrt m}<\infty.
\]

For positive indices use (5). This proves boundedness on H, and also on A. More particularly,

\[
 \|L_a\|_{A^*}\leq e^a.                             \tag{8}
\]

Indeed, the coefficient-to-weight ratios at negative indices are at most e^a, the positive coefficients have modulus at most 1, and |e^a−e^{-a}|<e^a.

## 4. What these functionals annihilate

Let J_A be the A-norm closure of the elements of A that vanish on an open arc containing 1. Let J_H be the H-norm closure of the elements of H that vanish almost everywhere on such an arc. These spaces are closed and invariant under S and S^{-1}; J_A is a closed ideal of A and is contained in I.

### Proposition 2

Every L_a from (7) annihilates both J_A and J_H. Furthermore,

\[
 L_a(z-1)=e^{-a}(1+2a-e^{2a})\ne0.                 \tag{9}
\]

In particular J_A is a proper subspace of I, and J_H is a proper subspace of H.

#### Proof

Let f∈H vanish near 1. For 0<r<1, Fourier pairing gives

\[
 \int_{\mathbb T} f(z)V_a(rz)\,dm(z)
       =\sum_{m\geq0}v_m(a)r^m a_{-m},
\]

\[
 \int_{\mathbb T} f(z)U_a(r\bar z)\,dm(z)
       =\sum_{m\geq0}u_m(a)r^m a_m.
\]

Here m is normalized arclength and no complex conjugation is inserted in the pairing. The first sum tends to its r=1 value by absolute convergence; the second does so by (5) and Cauchy–Schwarz.

On the support of f, which avoids a fixed arc around 1, the integrands' analytic factors converge uniformly. For z∈T\{1},

\[
 \frac{1+\bar z}{1-\bar z}=-\frac{1+z}{1-z},
 \quad\text{hence}\quad V_a(z)=U_a(\bar z).
\]

Their limiting integrals agree. Thus L_a(f)=0. The same conclusion for A follows from A⊆H; continuity gives the assertions about the closures.

Finally v_0=e^a, u_0=e^{-a}, and u_1=−2ae^{-a}. Substitution in (7) gives (9), which is nonzero because e^{2a}>1+2a for a>0. ∎

This proof is an actual annihilation statement on the whole indicated cutoff class, not a finite numerical experiment or merely a formal hyperfunction computation.

As a quantitative consequence of (8)–(9),

\[
 \operatorname{dist}_A(z-1,J_A)
 \geq 1-(1+2a)e^{-2a}>0.                           \tag{10}
\]

For a=1/32, an entirely rational lower bound is

\[
 \operatorname{dist}_A(z-1,J_A)\geq\frac{15}{8192}.
\]

Indeed e^{2a}−1−2a≥2a² and e^{-2a}≥1−2a, so the right side of (10) is at least 2a²(1−2a).

### Proposition 3

The quotient I/J_A is infinite-dimensional. The quotient H/J_H is likewise infinite-dimensional.

#### Proof

The restrictions L_a|_I for distinct a∈(0,1/8) are linearly independent. Suppose a finite combination L=∑γ_jL_{a_j} vanishes on I. Because I is the kernel of evaluation at 1, L=C·ev_1 on A. On z^n, n≥1, this gives

\[
 -\sum_j\gamma_j u_n(a_j)=C.
\]

Each u_n(a_j) tends to zero by (5), so C=0. Therefore the analytic function ∑γ_jU_{a_j}(z) is constant. Letting z→1 through real values shows that this constant is zero. With t=(1+z)/(1-z), we obtain

\[
 \sum_j\gamma_j e^{-a_jt}=0\quad(t>1).
\]

Order the distinct a_j increasingly, multiply by the exponential corresponding to the smallest parameter, and let t→∞. Its coefficient is zero. Repetition gives every γ_j=0. Since the L_a annihilate J_A, the first quotient has infinitely many independent continuous functionals.

The same argument proves independence on H directly, without the evaluation term C. Every L_a annihilates J_H, proving the second assertion. ∎

## 5. The cutoff spaces are nonzero and have the expected localization

Here is an elementary construction avoiding an appeal to an unspecified smooth cutoff theorem. Choose 1<p<2 and ε>0 so small that

\[
 L=\sum_{j\geq1}\epsilon j^{-p}<\pi.
\]

Convolve the probability measures uniform on the real intervals [−εj^{-p}, εj^{-p}]. The finite convolutions converge weakly to a probability measure supported on [−L,L]. For integer n, its Fourier transform is

\[
 \prod_{j\geq1}\frac{\sin(n\epsilon j^{-p})}{n\epsilon j^{-p}}.
\]

If N=⌊(ε|n|/2)^{1/p}⌋, each of the first N factors has modulus at most 1/2, while all remaining factors have modulus at most 1. Consequently its Fourier coefficients are bounded by 2^{-N}. They therefore decay like exp(−d|n|^{1/p}) for some d>0. Since 1/p>1/2, the periodized measure has a C∞ density belonging to A and H. The density is nonnegative, has integral 1, and is supported on an arbitrarily small arc if ε is sufficiently small.

Some point of that arc has positive density. A rotation can put such a point at any prescribed ζ∈T, still with arbitrarily small support around ζ. In particular J_A and J_H are nonzero. For every ζ≠1, there is an element of J_A nonzero at ζ. Thus the common zero set, or hull, of J_A is exactly {1}.

## 6. Why a proper cutoff ideal is not a counterexample

In fact the induced operator on the defect quotient I/J_A is cyclic. This makes the remaining logical gap particularly explicit.

Every character of A is evaluation at a point of T. To verify this, let χ be a character and set λ=χ(z). The bounds on ∥z^n∥ and ∥z^{-n}∥ force |λ|≤1 and |λ|≥1, respectively. The character agrees with evaluation at λ on Laurent polynomials and hence on A. By Section 5, the characters of the unital quotient A/J_A are therefore supported at 1 alone. Its element z+J_A has spectrum {1}.

The inverse of z+J_A−λ in A/J_A, for λ≠1, preserves its closed ideal I/J_A under multiplication. Thus the operator R induced by T on I/J_A has spectrum contained in {1}; it is exactly {1}, since I/J_A is a nonzero complex Banach space. Its bicyclic vector is v+J_A, inherited from Proposition 1.

Now r(I−R)=0. The series

\[
 R^{-1}=\sum_{j=0}^{\infty}(I-R)^j
\]

converges in operator norm, by the spectral-radius formula. Hence R^{-1}, and then every negative power of R, is a norm limit of polynomials in R. A bicyclic vector for R is therefore cyclic.

Consequently none of the following proves the desired noncyclicity:

- v itself fails to be cyclic;
- the cutoff ideal is proper, even of infinite codimension;
- a nonzero localized dual functional exists;
- the localized quotient is infinite-dimensional.

Each of these facts has been proved here, and the quotient still has a cyclic vector. A proof that T is noncyclic would have to rule out every other f∈I. A proof for the Hilbert-space model would similarly have to rule out every f∈H. Conversely, constructing a cyclic vector for either model would not by itself prove the universal endpoint theorem.

## 7. The precise remaining obstruction

The published little-o argument obtains cyclicity from the cutoff ideal together with an identification of that ideal with the closure of a polynomially generated ideal. At the endpoint, Proposition 2 gives a concrete failure of that identification:

\[
 J_A\subsetneq I=\overline{(z-1)A}.
\]

This is a rigorous obstruction to directly transferring that proof. It is not a logical obstruction to cyclicity itself. The attempt stopped at exactly this distinction: no argument here shows that every potential cyclic vector lies in a proper forward-invariant subspace, and no construction here produces a cyclic vector outside the cutoff ideal.

## References and attribution

1. E. Abakumov, A. Atzmon, S. Grivaux, *Cyclicity of bicyclic operators*, C. R. Acad. Sci. Paris, Ser. I 344 (2007), 447–452. [Full primary note](https://www.numdam.org/item/10.1016/j.crma.2007.02.008.pdf). Theorems 1.2–1.3 give the little-o result; Section 2 describes the cutoff-ideal argument; Conjecture 3.3 specifies the Hilbert endpoint weight used here. These are the authors' results and conjecture.
2. E. Abakumov, *On completeness of translates in weighted spaces*, joint work with A. Atzmon and S. Grivaux, in *Operator Theory and Harmonic Analysis*, Oberwolfach Report 49/2010, printed pp. 2819–2821. [Original report](https://doi.org/10.4171/owr/2010/49). Theorem 2 and the following paragraph give the complete target and its optimality question.
3. A. Atzmon, *Operators which are annihilated by analytic functions and invariant subspaces*, Acta Math. 144 (1980), 27–63. [DOI](https://doi.org/10.1007/BF02392120); [primary-paper copy](https://archive.ymsc.tsinghua.edu.cn/pacm_download/117/6271-11511_2006_Article_BF02392120.pdf). Section 7, especially Proposition 6 and the example on pp. 54–55, discusses this same asymmetric square-root-weight algebra and its nontrivial primary ideals, using singular-inner-function generators. The underlying endpoint ideal phenomenon is therefore classical. The explicit functionals and estimates in this note are a self-contained worked verification, not a claimed new phenomenon.
4. E. Abakumov, A. Atzmon, S. Grivaux, *Cyclicity of bicyclic operators and completeness of translates*, Math. Ann. 341 (2008), 293–322. [Publisher record](https://doi.org/10.1007/s00208-007-0191-2). This longer paper is cited by the original report. Its bibliographic record was verified, but a full-text copy was not successfully retrieved in this attempt; no uninspected argument from it is used here.
