# Zero-value obstruction to an IM-sharing conclusion

## 1. Exact scope

We test the following implication on the complex plane. Let f be a nonconstant entire function, k an integer at least 2, and a,b complex constants with b != 0. Assume

1. {z : f(z)=a} = {z : f'(z)=a};
2. at every z with f'(z)=b, one has f^(k)(z)=b.

Does f necessarily have the form

    f(z) = d exp(cz) + ((c-1)/c)a,
    c != 0, d != 0, c^(k-1)=1 ?

This is the IM replacement of the CM theorem printed in Mingliang Fang's contribution to *Normal Families and Complex Dynamics*, Oberwolfach Report 9/2007, printed pp. 501-503, specifically pp. 502-503. CM additionally demands equal zero multiplicities. The printed Theorem H requires b != 0, but does not require a != 0. The catalogue adds b != a; all examples below satisfy this stronger requirement as well.

The catalogue's additive constant a/c is a transcription error: visual inspection of printed p. 503 gives ((c-1)/c)a. None of our negative conclusions relies on that error: in our counterexamples a=0 and both additive constants vanish.

## 2. Counterexample at every derivative order

**Proposition 1.** For every k >= 2, b in C excluding zero, and z0 in C, put a=0 and

    f(z) = b (z-z0)^k / k!.

Then f satisfies both hypotheses and fails the proposed conclusion.

**Proof.** This is a nonconstant entire polynomial. Its derivative is

    f'(z) = b (z-z0)^(k-1)/(k-1)!.

Both zero sets are exactly {z0}, so they share a=0 IM. Their multiplicities k and k-1 differ, so they do not share this value CM. Moreover f^(k)(z)=b at every point of C. The implication concerning b therefore holds. It is not vacuous: f'(z)=b has the k-1 distinct solutions of (z-z0)^(k-1)=(k-1)!.

Since a=0, the conclusion would say f(z)=d exp(cz) with c,d nonzero. Such a function never vanishes, whereas f(z0)=0. This is impossible. Also b != a because b != 0. QED.

The smallest concrete example is k=2, b=1, a=0, f(z)=z^2/2. Its derivative is z and its second derivative is 1. The sole b-point of f' is z=1 and the required equality holds there. The claimed exponential form for k=2 would be d exp(z), which cannot vanish at zero.

## 3. Classification of polynomial instances

**Proposition 2.** Suppose f is a nonconstant polynomial satisfying the two hypotheses above for some a,b and k >= 2, b != 0. Then necessarily a=0, deg(f)=k, and

    f(z) = b (z-z0)^k/k!

for some z0 in C. Conversely every such polynomial is admissible.

**Proof.** Write n=deg(f).

First suppose a != 0. Every zero of f-a is simple: at such a point the sharing hypothesis gives f'=a != 0. Hence f-a has exactly n distinct roots. All are roots of f'-a. If n >= 2 this contradicts deg(f'-a)=n-1. If n=1, then f' is constant. If that constant differs from a, f'-a has no roots; if it equals a, every point is a root. Neither set equals the one-point zero set of f-a. Thus a != 0 is impossible.

Now let a=0. Degree one is excluded by the same zero-set comparison. For n >= 2, let r be the number of distinct roots of f, with multiplicities m1,...,mr. At any root of multiplicity 1, f' is nonzero, contradicting shared zero sets; therefore each mj >= 2. The multiplicity in f' at that root is exactly mj-1. Since f' has no other roots, its degree is both n-1 and sum_j(mj-1)=n-r. Consequently r=1, so f(z)=A(z-z0)^n with A != 0.

Set x=z-z0. The b-points of f' satisfy

    x^(n-1) = b/(An).

They are n-1 distinct nonzero points. If k>n, then f^(k)=0, contradicting b != 0 at these points. If 2 <= k <= n, then

    f^(k)(z) = A n!/(n-k)! x^(n-k).

At all n-1 roots of the displayed equation this expression must equal the same nonzero number b. Fix one root x1. The others are x1 times the (n-1)-th roots of unity; their (n-k)-th powers can all agree only if n-1 divides n-k. Since 0 <= n-k <= n-2, this forces n-k=0. Thus k=n and A n!=b, giving the claimed form. The converse was proved in Proposition 1. QED.

This proves the boundary mechanism systematically rather than relying on a single accidental polynomial.

## 4. Transcendental counterexamples for every k >= 3

**Proposition 3.** For any integer k >= 3, choose a nonzero complex lambda satisfying

    lambda^(k-1) = -1/(2^(k-1)-2),

and set

    a=0, b=-lambda/2, f(z)=(exp(lambda z)-1)^2.

Then f is transcendental entire, satisfies both hypotheses, and fails the exponential conclusion.

**Proof.** The denominator 2^(k-1)-2 is nonzero, so such a nonzero lambda exists. Put t=exp(lambda z); then t ranges over C excluding zero and

    f=(t-1)^2,
    f'=2 lambda t(t-1),
    f^(k)=lambda^k(2^k t^2-2t).

Since t never vanishes, the zero sets of f and f' are both exactly the points with t=1. The zeros are respectively double and simple, hence sharing is IM but not CM.

For the second hypothesis,

    f'-b = 2 lambda (t-1/2)^2.

Thus its b-points are precisely t=1/2, a nonempty set. At every such point,

    f^(k) = lambda^k(2^(k-2)-1)
           = lambda * [-1/(2^(k-1)-2)] * (2^(k-2)-1)
           = -lambda/2 = b.

The function has infinitely many zeros (lambda z=2 pi i n, n in Z), and is not identically zero. It is therefore not a polynomial and is transcendental entire. Those zeros also prevent any representation d exp(cz) with d != 0. This proves all assertions. QED.

For example k=3 allows lambda=i/sqrt(2), b=-i/(2 sqrt(2)). The transcendental construction deliberately uses a multiple b-point of f'; the hypothesis only prescribes the value of f^(k) there, not equal multiplicity with f'-b. No extra CM condition at b has been assumed.

## 5. Boundaries of the result

- The universal IM assertion as printed is false, even with the catalogue's additional b != a restriction.
- The CM theorem is untouched: the displayed functions fail CM sharing at a=0.
- The corrected and catalogue exponential conclusions are both false for these examples, so transcription repair does not remove the obstruction.
- Requiring transcendence alone still leaves Proposition 3, for every k >= 3.
- The strengthened problem with a != 0 is not resolved here. Proposition 2 merely excludes polynomial instances of that strengthened problem.
- The printed report's neighboring Theorem 3, and Chang-Fang's 2007 abstract, explicitly assume a != 0 and impose the higher-derivative condition at the same value a. They do not cover our examples or settle the distinct-b nonzero-a question.
- The arguments are elementary and self-contained. They establish mathematical correctness but do not establish novelty or whether the elementary obstruction was already known. No scholarly priority claim is made.

## Sources

1. Mingliang Fang, contribution in P. Rippon, N. Steinmetz and L. Zalcman (organizers), *Normal Families and Complex Dynamics*, Oberwolfach Reports 4 (2007), 487-548; contribution 501-503. https://doi.org/10.4171/OWR/2007/09 ; publisher PDF https://ems.press/content/serial-article-files/46093?nt=1
2. J. M. Chang and M. L. Fang, *Normal Families and Uniqueness of Entire Functions and Their Derivatives*, Acta Mathematica Sinica, English Series 23 (2007), 973-982. Publisher abstract checked, full text not obtained. https://doi.org/10.1007/s10114-005-0861-5
3. Feng Lu, *Entire Functions That Share Values With Their Derivatives*, Applied Mathematics E-Notes 10 (2010), 175-183. Complete nine-page paper read; its main result uses the same nonzero value in the two antecedents, so it is a neighboring result only. https://www.math.nthu.edu.tw/~amen/2010/090910-1.pdf
