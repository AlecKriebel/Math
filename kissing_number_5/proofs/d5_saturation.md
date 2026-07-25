# Fixed-\(D_5\) saturation

## Status and scope

**PROVED.** The normalized \(D_5\) root configuration cannot be enlarged by
adding a point while keeping its 40 points fixed.

This is a saturation statement for one fixed configuration. It does **not**
rule out a 41-point code obtained by moving, deleting, or replacing \(D_5\)
points, and it does not prove \(\tau(5)\leq 40\).

## Proposition

Let

\[
D_5^*=\left\{
\frac{\varepsilon_i e_i+\varepsilon_j e_j}{\sqrt 2}:
1\leq i<j\leq 5,\quad \varepsilon_i,\varepsilon_j\in\{-1,1\}
\right\}.
\]

Then:

1. \(D_5^*\) consists of 40 unit vectors, and the inner product of any two
   distinct vectors in \(D_5^*\) is at most \(1/2\).
2. For every \(y\in S^4\),

   \[
   \max_{x\in D_5^*}\langle x,y\rangle
   \geq \sqrt{\frac25}
   =\frac{2}{\sqrt{10}}
   >\frac12.
   \]

   The constant is sharp.

Consequently, there is no \(y\in S^4\) such that
\(\langle x,y\rangle\leq 1/2\) for every \(x\in D_5^*\).

## Proof

There are \(\binom52=10\) choices of support and four sign choices, so
\(\lvert D_5^*\rvert=40\). Every unnormalized root
\(\varepsilon_i e_i+\varepsilon_j e_j\) has squared norm 2. For two
distinct unnormalized roots, their inner product is:

- \(0\) if their supports are disjoint;
- \(1\) or \(-1\) if their supports meet in one coordinate;
- \(0\) or \(-2\) if their supports agree but their sign choices differ.

After division by \(\sqrt2\), every distinct-pair inner product is therefore
at most \(1/2\).

Now fix \(y=(y_1,\ldots,y_5)\in S^4\), and write the absolute coordinate
values in decreasing order as

\[
a_1\geq a_2\geq a_3\geq a_4\geq a_5\geq0.
\]

For a fixed support \(\{i,j\}\), choosing the two signs to agree with the
signs of \(y_i,y_j\) gives

\[
\max_{\varepsilon_i,\varepsilon_j\in\{-1,1\}}
\left\langle
\frac{\varepsilon_i e_i+\varepsilon_j e_j}{\sqrt2},y
\right\rangle
=\frac{|y_i|+|y_j|}{\sqrt2}.
\]

It follows that

\[
\max_{x\in D_5^*}\langle x,y\rangle
=\frac{a_1+a_2}{\sqrt2}.
\]

Because \(a_3,a_4,a_5\leq a_2\),

\[
1=\sum_{i=1}^5 a_i^2\leq a_1^2+4a_2^2.
\]

For \(a_1\geq a_2\geq0\), the exact identity

\[
\frac54(a_1+a_2)^2-(a_1^2+4a_2^2)
=\frac14(a_1-a_2)(a_1+11a_2)
\]

shows that

\[
a_1^2+4a_2^2\leq\frac54(a_1+a_2)^2.
\]

Combining the last two inequalities gives

\[
a_1+a_2\geq\frac{2}{\sqrt5}.
\]

Therefore

\[
\max_{x\in D_5^*}\langle x,y\rangle
=\frac{a_1+a_2}{\sqrt2}
\geq\frac{2}{\sqrt{10}}
=\sqrt{\frac25}.
\]

Finally,

\[
\frac25-\frac14=\frac3{20}>0,
\]

so \(\sqrt{2/5}>1/2\). Equality in the lower bound occurs exactly when
\(a_1=\cdots=a_5=1/\sqrt5\). For example,
\(y=(1,1,1,1,1)/\sqrt5\) attains
\(\max_{x\in D_5^*}\langle x,y\rangle=2/\sqrt{10}\).
This proves the proposition. \(\square\)

## Dependency map

The proof uses only:

1. direct enumeration of the \(D_5\) root supports and signs;
2. sorting the five absolute coordinate values of an arbitrary unit vector;
3. the displayed polynomial identity.

It does not use rigidity, symmetry of a hypothetical extremizer, floating
point computation, or any upper bound for the five-dimensional kissing
number.

## Machine check

The standard-library verifier
[`verify_d5_saturation.py`](../verifiers/verify_d5_saturation.py) checks the
40-root enumeration, all distinct-pair inner products in the unnormalized
integer model, the polynomial identity coefficient-by-coefficient, and the
sharp witness and threshold comparison using exact rational arithmetic.
