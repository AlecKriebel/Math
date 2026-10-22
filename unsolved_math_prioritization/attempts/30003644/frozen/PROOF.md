# Five approaches to the Erdős–Ingham four-term polynomial

## Exact target and disposition

Let

\[
D(s)=1+2^{-s}+3^{-s}+5^{-s},\qquad n^{-s}=\exp(-s\log n),
\]

where all logarithms of positive integers are real. The question is whether
\(D(1+it)\ne0\) for **every real** \(t\). All four Dirichlet coefficients
are one. On the specified line the three nonconstant terms have respective
moduli \(1/2,1/3,1/5\). This is a question about one line, not a half-plane.

The exact question remains **unsolved in this investigation, after five
substantive approaches**. The results below do not establish an unconditional
answer. No novelty or priority claim is made for the partial deductions.

The primary statement is Problem 2, Question 1 of the open-problems session,
Oberwolfach Report 51/2017, printed p.3065 [S1]. The source's equivalent
Tauberian question is treated in Approach 4. The same polynomial is asked
again on p.2757 of Report 51/2025 [S2]. Yip's 2025 paper [S3] disproves the
broader infinite-sequence assertion, but explicitly leaves this finite
\(\{2,3,5\}\) question open in Question 3.2. It is therefore not a prior
resolution of this target.

## Approach 1: domination and the rightmost zero boundary

Put \(H(\sigma)=2^{-\sigma}+3^{-\sigma}+5^{-\sigma}\). There is a unique
real \(\sigma_*\) with \(H(\sigma_*)=1\), because \(H\) is continuous and
strictly decreasing from infinity to zero. In particular
\(H(1)=31/30>1\), so \(\sigma_*>1\). The supplied interval checks prove
\(1.032<\sigma_*<1.033\).

**Proposition 1.** Every zero of \(D\) satisfies
\(\operatorname{Re}s<\sigma_*\). Nevertheless the supremum of the real
parts of the zeros is \(\sigma_*\), and there are zeros with real part
strictly greater than one.

**Proof.** If \(\sigma>\sigma_*\), the triangle inequality gives
\(|D(\sigma+it)|\ge1-H(\sigma)>0\). At \(\sigma=\sigma_*\), vanishing
would force equality in that inequality. All three phases would then be
\(-1\). In particular \(t\log2\) and \(t\log3\) would be odd multiples
of \(\pi\), forcing \(\log2/\log3\) to be rational. Unique factorization
rules this out.

The numbers \(\log2,\log3,\log5\) are linearly independent over
\(\mathbb Q\), again by unique factorization. The continuous Kronecker
flow \(t\mapsto(2^{-it},3^{-it},5^{-it})\) is therefore dense in
\(\mathbb T^3\). Choose a sequence of times whose phases tend to
\((-1,-1,-1)\). The corresponding vertical translates of \(D\) converge
uniformly on compact sets to

\[
G(s)=1-2^{-s}-3^{-s}-5^{-s}.
\]

The zero \(G(\sigma_*)=0\) is simple, since
\(G'(\sigma_*)=\sum_{p=2,3,5}(\log p)p^{-\sigma_*}>0\).
Rouché's theorem on sufficiently small circles about \(\sigma_*\) gives
zeros of those translates arbitrarily close to \(\sigma_*\). Translating
back preserves real parts. Choosing the circle wholly to the right of one
also proves the last assertion. Together with the strict upper bound this
proves the stated supremum. \(\square\)

The numerical control separately certifies exactly one zero in the disk of
radius \(10^{-20}\) about the decimal-rational center

\[
1.006705654528482647538233912439
 +185.725918497342080628141229326837\,i.
\]

It does so by bounding the residual by \(10^{-27}\), the derivative modulus
below by \(0.9\), and the second derivative modulus on the disk above by
\(2\). On its boundary,
\(10^{-27}+r^2<0.9r\), so the linear term has exactly one zero and dominates
the constant plus Taylor remainder. The entire disk lies to the right of
one. This is a control against confusing the line with its right half-plane,
not a counterexample to the exact question.

The use of Kronecker approximation and Bohr's zero theory in this setting
is classical; compare Erdős–Ingham [S4], pp.353–355. Proposition 1 gives
a self-contained specialization, rather than a claimed new zero principle.

**Gap.** Domination ends at \(\sigma_*\), and its sharpness provides no
decision about exact equality of a zero's real part to one.

## Approach 2: torus geometry and the failure of uniform separation

Write

\[
P(u,v,w)=1+u/2+v/3+w/5,\qquad |u|=|v|=|w|=1.
\]

The following is an exact algebraic point on its zero set:

\[
u=-1,\qquad
v=\frac{-289+i\sqrt{6479}}{300},\qquad
w=\frac{-161-i\sqrt{6479}}{180}.
\]

Indeed \(289^2+6479=300^2\), \(161^2+6479=180^2\), and
\(v/3+w/5=-1/2\). These are also checked with exact rational arithmetic
by the control script.

**Proposition 2.**
\[
\inf_{t\in\mathbb R}|D(1+it)|=0.
\]

**Proof.** Approximate the displayed triple by the dense continuous
Kronecker flow from Approach 1 and apply continuity of \(P\). \(\square\)

This unconditional fact is compatible with the desired pointwise
nonvanishing. In particular, no proof can obtain a positive uniform gap
\(|D(1+it)|\ge\delta>0\) for all real \(t\). One must distinguish the
orbit's closure from the orbit itself.

For a more precise local picture, the derivative of \(P\) with respect to
the last two angles has columns \(iv/3\) and \(iw/5\). They are linearly
independent as real vectors at the displayed triple: \(v,w\) are not
parallel, since their imaginary parts have opposite signs but their negative
real parts are not in the required opposite proportion. Thus the torus
zero set is locally a smooth one-dimensional curve by the implicit function
theorem. Density of a one-dimensional orbit in the three-dimensional torus
does not force intersection with this curve.

**Gap.** Neither an exact algebraic torus zero nor arbitrarily close orbit
visits supplies a time at which all three prescribed phases are attained.
Approach 5 in fact excludes an exact orbit visit to this particular algebraic
triple at every nonzero time.

## Approach 3: phase localization, simple zeros, and finite-height exclusion

Let \(z_p=e^{-it\log p}\) and suppose, for this approach only, that
\(D(1+it)=0\). Taking real parts gives the exact deficit identity

\[
\sum_{p=2,3,5}\frac{1+\Re z_p}{p}=\frac1{30}.
\tag{1}
\]

Each summand is nonnegative. Consequently

\[
\Re z_2\le-14/15,\qquad
\Re z_3\le-9/10,\qquad
\Re z_5\le-5/6.
\tag{2}
\]

Equivalently, each phase angle is within
\(\arccos(1-p/30)\) of an odd multiple of \(\pi\). These are necessary
conditions, together with the independent imaginary-part equation
\(\sum\Im z_p/p=0\). They constrain any candidate zero but are not
mutually inconsistent: the exact triple from Approach 2 satisfies them.

**Proposition 3.** Every hypothetical zero on the unit line is simple.
More quantitatively, at such a zero

\[
\Re D'(1+it)
\ge \frac{\log2}{2}+\frac{\log3}{3}+\frac{\log5}{5}
       -\frac{\log5}{30}>0.98.
\tag{3}
\]

**Proof.** Write \(L=\sum\log p/p\). Equation (1) implies

\[
\Re D'(1+it)
=L-\sum\frac{\log p}{p}(1+\Re z_p)
\ge L-(\log5)/30.
\]

The last number exceeds \(0.98\), as verified by outward interval
arithmetic (or elementary bounds for these logarithms). In particular the
complex derivative cannot vanish. \(\square\)

The derivative of \(D(1+it)\) with respect to \(t\) is \(iD'(1+it)\),
so any hypothetical passage through the origin has positive imaginary
velocity. This does not prohibit a passage.

The accompanying interval computation covers the **whole** interval
\(0\le t\le10000\), rather than a mesh of points. It adaptively subdivides
closed dyadic intervals and encloses the real and imaginary parts of
\(D(1+it)\). It accepts an interval only if at least one component's
enclosure excludes zero. The recorded run accepts 4,782 intervals, with no
unresolved intervals; conjugation covers negative \(t\) as well. Hence,
subject to the outward-rounding implementation documented in the verifier,
it certifies nonvanishing for \(|t|\le10000\).

The test on \(1+2\cdot2^{-s}\), which has a known zero at
\(1+i\pi/\log2\), deliberately does not certify its search interval.
The unresolved interval contains that exact time. It guards against silently
treating a depth limit or inconclusive enclosure as a success.

**Gap.** No finite-height verification controls all real \(t\). Neither
the necessary angle restrictions nor simplicity rules out a later zero.

## Approach 4: a monotone oscillatory Tauberian test

The source also asks whether every nondecreasing
\(f:\mathbb R_{>0}\to\mathbb R_{>0}\) satisfying

\[
f(x)+f(x/2)+f(x/3)+f(x/5)=(61/30+o(1))x
\]

must obey \(f(x)=(1+o(1))x\). The source credits the equivalence with the
nonvanishing question to Erdős and Ingham [S4]. Here is a direct proof of
the obstruction direction in exactly the source's positivity convention,
reconstructing their oscillatory construction on pp.349–350.

Suppose \(D(1+it_0)=0\). Since \(D(1)=61/30\), necessarily \(t_0\ne0\).
Choose \(0<\epsilon<(1+t_0^2)^{-1/2}\), and define

\[
f(x)=x\bigl(1+\epsilon\cos(t_0\log x)\bigr),\qquad x>0.
\]

It is strictly positive, and

\[
f'(x)=1+\epsilon\cos(t_0\log x)-\epsilon t_0\sin(t_0\log x)
\ge1-\epsilon\sqrt{1+t_0^2}>0.
\]

On the other hand,

\[
\sum_{n\in\{1,2,3,5\}} f(x/n)
=\frac{61}{30}x+
 \epsilon x\Re\bigl(x^{it_0}D(1+it_0)\bigr)
=\frac{61}{30}x.
\]

The ratio \(f(x)/x\) oscillates between \(1-\epsilon\) and
\(1+\epsilon\) arbitrarily far out, so does not tend to one. This gives
a valid monotone positive counterexample whenever a unit-line zero exists.

The customary normalization \(f=0\) on \([0,1)\) used in [S3, Theorem
1.2] can instead be imposed by truncating the same function there. It stays
nondecreasing, and the displayed identity remains exact for \(x\ge5\).
That normalized convention is not silently imposed on the OWR statement.

Trying the same perturbation with a zero of real part \(\sigma>1\) gives
an oscillatory term of order \(x^\sigma\), which eventually destroys
positivity and monotonicity. Thus the off-line zeros in Approach 1 do not
settle the Tauberian question.

**Gap.** The construction is conditional on the very zero being sought.
Proving the full Tauberian implication by positivity alone would have to
exclude these modes; merely invoking the known equivalence transfers the
central difficulty.

## Approach 5: elimination, six exponentials, and a conditional endpoint

Here is an arithmetic obstruction that uses more than phase density.
Let \(a=1/2,b=1/3,c=1/5\). At a unit-line zero set
\(u=2^{-it},v=3^{-it},w=5^{-it}\), and put
\(A=1+au\), \(B=1+a/u\). The equation and its complex conjugate are

\[
A+bv+cw=0,\qquad B+b/v+c/w=0.
\]

Eliminating \(w\) gives

\[
bBv^2+(AB+b^2-c^2)v+bA=0.
\tag{4}
\]

The leading coefficient is nonzero because
\(|a/u|=1/2<1\); also \(A+bv=-cw\ne0\), so the elimination did not
divide by zero. Thus \(v\) and then \(w\) are algebraic over
\(\mathbb Q(u)\). By permuting the three phases, the same holds with
any one selected as the base phase (the corresponding weight is always
strictly less than one).

**Proposition 4.** If \(D(1+it)=0\), every one of
\(2^{-it},3^{-it},5^{-it}\) is transcendental. Moreover the field they
generate has transcendence degree exactly one over \(\mathbb Q\).

**Proof.** If one phase were algebraic, (4) and its permuted versions
would make all three algebraic. Apply the six exponentials theorem
[S5, Theorem 2.1] to the two numbers \(1,-it\) and the three numbers
\(\log2,\log3,\log5\). The first pair is linearly independent over
\(\mathbb Q\) because \(t\ne0\) is real, and the second triple is
independent by unique factorization. The six exponentials would be
\(2,3,5,u,v,w\), all algebraic, a contradiction. Therefore any base
phase is transcendental. Equation (4) proves that adjoining the other two
is algebraic, giving transcendence degree exactly one. \(\square\)

In particular, any time at which even one of the three phases is a root
of unity, or any other algebraic unit-modulus number, is excluded.
The six exponentials theorem does not assert algebraic independence of
the three phases, so it does not exclude the remaining transcendence-degree
one case.

**Proposition 5 (conditional).** Schanuel's conjecture implies that
\(D(1+it)\ne0\) for every real \(t\).

**Proof.** Assume a zero and set
\(\ell_1=\log2,\ell_2=\log3,\ell_3=\log5\). The six complex numbers

\[
\ell_1,\ell_2,\ell_3,-it\ell_1,-it\ell_2,-it\ell_3
\]

are linearly independent over \(\mathbb Q\). Indeed, real and imaginary
parts of any rational linear relation separately vanish, and the three
real logarithms are independent. Schanuel's conjecture [S5, Conjecture 2.3]
therefore forces the field generated by these six numbers and their
exponentials to have transcendence degree at least six.

That field is contained in

\[
K=\mathbb Q(\ell_1,\ell_2,\ell_3,it,u,v,w).
\]

By (4), \(K\) is algebraic over
\(\mathbb Q(\ell_1,\ell_2,\ell_3,it,u)\), a field generated by five
elements. Consequently \(\operatorname{trdeg}_{\mathbb Q}K\le5\), a
contradiction. \(\square\)

**Gap.** Schanuel's conjecture is not a proved premise. Unconditionally,
the remaining task is to exclude the exact Kronecker-orbit intersection
with the algebraic curve (4) when all phases are transcendental and their
joint field has transcendence degree one. Neither six exponentials,
finite-height exclusion, nor the rightmost-zero argument supplies this.

## What has and has not been established

- Exact source target: unresolved, five approaches used.
- Proven analytic facts: the sharp rightmost zero boundary, zero infimum
  on the unit line, phase restrictions and simplicity of any hypothetical
  line zero, the explicit conditional Tauberian counterexample, and the
  six-exponentials phase obstruction.
- Conditional theorem: full nonvanishing assuming Schanuel's conjecture.
- Reproducible interval controls: no unit-line zeros through height 10,000;
  a certified nearby zero to the right; a zero-bearing negative control.
- No global computational exclusion, no unconditional proof or exact
  counterexample on the line, and no novelty certification.

References and verification details are in `SOURCES.md` and `README.md`.
