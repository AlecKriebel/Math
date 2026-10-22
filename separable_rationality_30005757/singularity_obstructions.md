# Singularity obstructions for rationality of separable subclasses

Date: 2026-10-21. Status: authored mathematical analysis; bounded partial results.

## Verdict and scope

No proof or counterexample to the universal statement was obtained:

> If a downward-closed subclass of the separable permutations contains all of Av(231), must its ordinary generating function be nonrational?

This is Question 4 on printed p. 283 of Oberwolfach Report 6/2024. The report also discusses the problem on pp. 290–292. Primary source: https://publications.mfo.de/bitstream/handle/mfo/4113/OWR_2024_06.pdf?isAllowed=y&sequence=4 .

The results below are **obstructions to proposed proof strategies**, not solutions of that question:

1. A genuine downward-closed separable class containing Av(231) can have a simple pole strictly before its Catalan branch point, with ordinary pure-exponential dominant asymptotics.
2. A finite system of polynomial equations with nonnegative integer coefficients can have a reachable nonlinear Catalan state and a rational output, even when the output explicitly contains the Catalan series as a nonnegative summand.
3. The second example is not asserted to be realizable as a downward-closed class of canonical signed Schröder trees. Establishing an obstruction specific to that hereditary structure is precisely the missing step.

All derivations below are direct calculations, not quotations from the source.

## 1. A genuine separable downset with a dominant simple pole

Write Sep = Av(2413,3142), and let

\[
K(x)=\sum_{n\geq 0}C_nx^n=\frac{1-\sqrt{1-4x}}{2x}
\]

be the Catalan generating function, including the empty permutation. Let \(s_n=|\mathrm{Sep}_n|\) for \(n\geq1\). The nonempty separable generating function is

\[
S(x)=\sum_{n\geq1}s_nx^n
     =\frac{1-x-\sqrt{1-6x+x^2}}2,
\qquad S=x+xS+S^2.
\]

For an integer \(N\geq1\), define

\[
U_N=\operatorname{Av}(231)\cup\{\pi\in\mathrm{Sep}:|\pi|\leq N\},
\qquad
\mathcal C_N=\bigoplus U_N,
\]

where the last expression means the class of finite direct sums of members of \(U_N\), including the empty sum.

### 1.1 Downward closure and separability

The set \(U_N\) is downward closed: both parts of its union are downward closed. A pattern of a direct sum is a direct sum of patterns of its summands after empty summands are removed. Thus \(\mathcal C_N\) is downward closed. Direct sums preserve separability, so \(\mathcal C_N\subseteq\mathrm{Sep}\). It contains all of Av(231) by construction.

Every nonempty permutation has a unique factorization into sum-indecomposable permutations. A sum-indecomposable member of \(\mathcal C_N\) must already belong to \(U_N\), because an expression with two nonempty direct-sum factors is decomposable. Conversely, every sum-indecomposable member of \(U_N\) belongs to \(\mathcal C_N\). Hence the sum-indecomposable members of \(\mathcal C_N\) are exactly those of \(U_N\).

### 1.2 Indecomposable generating function

For \(n\geq2\), every separable permutation is either sum decomposable or skew decomposable, but not both. Complementation interchanges these possibilities. Consequently, exactly \(s_n/2\) separable permutations of length \(n\) are sum indecomposable. At length one there is one.

A nonempty 231-avoider is sum indecomposable exactly when its maximum is its first entry. Indeed, if the maximum has a nonempty prefix, avoidance of 231 forces every entry of that prefix to be smaller than every entry of the suffix. This gives a nontrivial direct-sum split, including the case of an empty suffix. Conversely, a maximum in first position prevents a direct-sum split. Deleting that maximum gives an arbitrary 231-avoider. Therefore the indecomposable generating function for Av(231) is \(xK(x)\).

It follows that the indecomposable generating function for \(\mathcal C_N\) is

\[
I_N(x)=xK(x)+P_N(x),
\quad
P_N(x)=\sum_{n=3}^{N}\left(\frac{s_n}{2}-C_{n-1}\right)x^n.
\]

The differences at lengths one and two are zero. Unique direct-sum factorization now gives the exact OGF

\[
F_N(x)=\frac1{1-I_N(x)}
      =\frac1{1-xK(x)-P_N(x)}.
\]

### 1.3 Exact check at N = 11

The required coefficients are:

| n | s_n | C_(n-1) | s_n/2 - C_(n-1) |
|---:|---:|---:|---:|
| 3 | 6 | 2 | 1 |
| 4 | 22 | 5 | 6 |
| 5 | 90 | 14 | 31 |
| 6 | 394 | 42 | 155 |
| 7 | 1806 | 132 | 771 |
| 8 | 8558 | 429 | 3850 |
| 9 | 41586 | 1430 | 19363 |
| 10 | 206098 | 4862 | 98187 |
| 11 | 1037718 | 16796 | 502063 |

Thus

\[
\begin{aligned}
P_{11}(x)={}&x^3+6x^4+31x^5+155x^6+771x^7\\
&+3850x^8+19363x^9+98187x^{10}+502063x^{11}.
\end{aligned}
\]

Exact integer arithmetic gives

\[
P_{11}(1/4)=\frac{2097931}{4194304}
           =\frac12+\frac{779}{4194304}.
\]

Since \(xK(x)\to1/2\) as \(x\uparrow1/4\),

\[
I_{11}(1/4)=1+\frac{779}{4194304}>1.
\]

Also \(I_{11}(0)=0\), and \(I_{11}\) is strictly increasing on \((0,1/4)\). There is therefore a unique \(r\in(0,1/4)\) with \(I_{11}(r)=1\). The derivative \(I'_{11}(r)\) is finite and strictly positive, so \(F_{11}\) has a simple pole at \(r\).

There are no denominator zeros inside \(|x|<r\), by the coefficientwise nonnegativity bound \(|I_{11}(x)|\leq I_{11}(|x|)<1\). Nor is there another pole on \(|x|=r\): equality in the triangle inequality for the positive coefficients of both \(x\) and \(x^2\) forces the phase to be 1. Thus this is the unique dominant singularity, and

\[
[x^n]F_{11}(x)\sim\frac1{r I'_{11}(r)}r^{-n}.
\]

A floating-point bisection, used only as a numerical illustration and not as proof, gives

\[
r\approx0.24999996572051375,
\qquad r^{-1}\approx4.0000005484718555.
\]

The crossing is very close to 1/4 but is strict by the exact fraction above. The same construction with any sufficiently large N gives a more widely separated pole. For comparison, \(P_{10}(1/4)\approx0.38048458<1/2\), so 11 is the first crossing in this particular increasing family.

### 1.4 Why this is not a counterexample to Question 4

Let \(t=\sqrt{1-4x}\). The exact formula is

\[
F_{11}(x)=\frac2{1-2P_{11}(x)+t}.
\]

If \(F_{11}\) were rational, rearranging would express \(t=2/F_{11}-1+2P_{11}\) as a rational function, which is impossible. Equivalently, at \(x=1/4\) the rational part of the denominator is nonzero:

\[
1-2P_{11}(1/4)=-\frac{1558}{4194304}.
\]

Analytic continuation around the earlier pole leaves a genuine, nonzero square-root term at 1/4. Its local coefficient is \(-2/(1-2P_{11}(1/4))^2\). The Catalan branch is hidden behind the dominant pole, not canceled.

**Consequence:** The assertion that every separable downset containing Av(231) has a square-root dominant singularity, a finite value at its radius, or an \(n^{-3/2}\) dominant factor is false. Merely examining dominant asymptotics cannot prove Question 4 in this generality.

The construction also has a finite signed-tree description: its sum-indecomposable components belong either to Av(231) or to a finite set, and the root is an unrestricted direct-sum sequence. No exotic infinite basis is being used.

## 2. Positive finite algebraic systems can cancel Catalan extensions

The following examples refute generic claims of the form “a positive polynomial specification with a reachable nonlinear Catalan component must have nonrational total OGF.” They do not refute a theorem that additionally uses the precise hereditary constraints of canonical signed Schröder trees.

### 2.1 Cancellation at the Catalan critical point

Consider the unique formal-power-series solution with \(T(0)=0\) of

\[
T=x(1+T)^2,
\qquad S=1+TS.
\]

Then \(1+T=K(x)\) is the Catalan series and \(S=1/(1-T)\). Define

\[
D=3T+4T^2S+4T^2S^2,
\qquad F=1+T+D.
\]

Every displayed defining equation has nonnegative integer coefficients, and every state has nonnegative integer Taylor coefficients. In particular, \(F\) explicitly contains the Catalan series \(1+T\) as a summand. Nevertheless,

\[
F=1+4TS^2
 =\frac{(1+T)^2}{(1-T)^2}
 =\frac1{1-4x}.
\]

For the last equality, use \(x=T/(1+T)^2\). The equality between the two expressions for F follows either by substitution \(S=(1-T)^{-1}\), or coefficientwise from

\[
F=1+4\sum_{k\geq1} kT^k,
\qquad
D=3T+8T^2+12T^3+16T^4+\cdots.
\]

Thus the Catalan extension is canceled in a genuinely positive finite algebraic system. At the critical point, \(T\to1\), so the sequence state \(S\) diverges. Positivity does not prevent the output from becoming a pole instead of retaining a branch point.

### 2.2 Cancellation even with an earlier dominant pole

There is a stronger example. Let

\[
T=x(1+T)^2,
\qquad A=1+2TA+TB,
\qquad B=TA+TB.
\]

The A/B subsystem is a strongly connected linear component with nonnegative polynomial coefficients, fed by the nonlinear Catalan state T. Its formal-power-series solution has \(A(0)=1\), \(B(0)=0\). Solving gives

\[
A=\frac{1-T}{1-3T+T^2},
\qquad
B=\frac{T}{1-3T+T^2}.
\]

But

\[
1-3T+T^2=(1+T)^2-5T=(1+T)^2(1-5x),
\]

so

\[
B=\frac{x}{1-5x},
\qquad F:=1+5B=\frac1{1-5x}.
\]

This rational output explicitly admits a positive Catalan summand. Indeed, substituting the equation for A into that for B gives

\[
B=T+2T^2A+T^2B+TB.
\]

Consequently, with

\[
D=4T+10T^2A+5T^2B+5TB,
\]

one has \(D=5B-T\), and therefore

\[
F=(1+T)+D.
\]

All equations defining T, A, B, D, and F have nonnegative integer coefficients. The formal solutions are unique by recursive coefficient determination, since T has zero constant term. The dominant pole is at \(x=1/5\), strictly before the Catalan branch point at \(x=1/4\). The algebraic branch cancels identically in F, not merely at leading order.

The transfer matrix of the A/B subsystem is

\[
T\begin{pmatrix}2&1\\1&1\end{pmatrix}.
\]

Its first singularity occurs at \(T=(3-\sqrt5)/2<1\), corresponding to \(x=1/5\). This example rules out repairing the generic positivity argument merely by requiring that the linear component be strongly connected or that its pole occur before the nonlinear critical point.

### 2.3 Interpretation and limitation

Finite positive polynomial systems have ordinary finite typed-tree grammar realizations by assigning distinct constructor labels to their alternatives. One can assign size zero to product constructors and size one to the explicit x constructors here; every recursive cycle still consumes positive total size. However, arbitrary constructor labels, ordered slots, and typed products are not automatically canonical alternating signed Schröder trees, nor does this construction prove closure under permutation patterns.

Accordingly, **do not describe these algebraic examples as rational separable permutation classes**. Their role is to show that general positivity, regular-tree recognizability, finite-state specification, or the presence of a nonlinear SCC does not itself establish nonrationality.

## 3. What a valid singularity proof would still need

A power series with nonnegative coefficients that is finite at its finite radius of convergence cannot be rational: by Pringsheim it is singular at that positive point, whereas a rational function's nonremovable finite singularities are poles, which diverge. This is a valid sufficient criterion, but Section 1 shows that it cannot apply uniformly to the classes in Question 4.

A stronger approach must control non-dominant algebraic singularities or Galois conjugation, and must exploit a structural property genuinely forced by downward closure and canonical direct/skew decomposition. Section 2 shows that arbitrary positive algebraic systems do not supply such control.

The OWR report's sufficient closure condition (sum closure together with closure under \(1\ominus\mathcal C\)) is stronger than merely containing Av(231). Our construction is sum closed, but that second closure condition must not be inferred from containment alone. No unproved structural reduction or strong-rationality theorem fills this gap here.

## 4. Reproducible exact arithmetic

The following elementary recurrences generate all coefficient values used above:

\[
s_1=1,\qquad s_n=s_{n-1}+\sum_{i=1}^{n-1}s_i s_{n-i}\quad(n\geq2),
\]

\[
C_0=1,\qquad C_n=\sum_{i=0}^{n-1}C_iC_{n-1-i}\quad(n\geq1).
\]

The exact numerator for \(P_{11}(1/4)\) is

\[
\sum_{n=3}^{11}(s_n/2-C_{n-1})4^{11-n}=2097931,
\]

and \(4^{11}=4194304\). The excess of that numerator over half the denominator is 779. No numerical root location is needed for the pole argument.

An independent local Python check using `fractions.Fraction` regenerated the coefficient list and both exact fractions. A SymPy check then substituted \(x=T/(1+T)^2\), verified both linear subsystem equations, and reduced both claimed rational-output identities to zero. All checks passed on 2026-10-21.
