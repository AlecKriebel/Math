# Independent classical-implication derivation

Review identity: `classical_implication_01`; PR630 frozen head
`810cd5c148bbae7c7c5a47423c375ada98e903b6`.
All deductions below were made without reading another new priority report.

## 1. Exact proposition and falsification criterion

Let f be nonconstant entire, k an integer at least 2, a,b complex, b nonzero.
The target antecedents are

    f=a iff f'=a;                 f'=b implies f^(k)=b.       (T)

The printed conclusion is

    f=d exp(cz)+(c-1)a/c,  c,d nonzero, c^(k-1)=1.            (E)

At a=0 this requires a zero-free exponential. Thus one admissible f with a
zero disproves the universal statement. The question's exact wording is on
printed p.503 of OWR 9/2007. No a-nonzero restriction is printed in Theorem H
or its immediately following IM question. Question C above it inherits a
nonzero-a condition from Theorem G; that is a different question.

## 2. Relevant prior counterexample implies the exact literal negative answer

Primary source LXY2009, printed p.68, Example 1 explicitly supplies

    q_beta(w)=(beta/4)w^2, beta nonzero,
    q_beta=0 iff q_beta'=0.

It uses this to show the necessity of excluding zero in a neighboring
derivative-sharing theorem. Here is the complete target map, rather than an
appeal to the general familiarity of a quadratic:

| Target item | Substitution or verification |
| --- | --- |
| Source parameter | beta=2b, where target b is any nonzero complex number |
| Function | f(z)=q_beta(z-z0)=b(z-z0)^2/2 |
| Entire, nonconstant | Polynomial with nonzero leading coefficient |
| Shared value and order | a=0, k=2 |
| IM equivalence | f=0 iff z=z0 iff f'=0, by the source example or direct differentiation |
| Derivative-value condition | f''=b identically, so f'=b implies f''=b |
| Nonempty b-fiber | f'=b precisely at z=z0+1 |
| Failure of conclusion | f(z0)=0, whereas d exp(cz) has no zero; for k=2, c=1 |
| Extra catalogue restriction | b differs from a because b is nonzero |

The source's *other* implication is q_beta'=beta implies q_beta=beta. It is
not confused with the target derivative-value hypothesis; the latter is
proved by f''=b. Hence this is a genuine, completely checked short corollary
of a relevant published zero-sharing counterexample. It does not show that
LXY2009 expressly discussed Fang's Question H or claimed its resolution.

## 3. Complete polynomial classification from an earlier theorem

Primary source NY2001, Proposition 7, printed journal p.300 (author manuscript
p.27), proves the following statement, attributed there to Chademan [5]: a
complex polynomial whose only critical value is zero is a translated
monomial. This is precisely the structural step needed here.

Assume a polynomial P of degree n satisfies (T). Degree one is impossible:
P=a has one point, while the level set P'=a is either empty or the whole
plane. Thus n is at least 2. If a is nonzero, each root of P-a is simple,
since P'=a is then nonzero at that root. The n distinct roots of P-a would
all be roots of P'-a, which has degree n-1. Contradiction. Hence a=0.

Now P'=0 implies P=0 by (T). Every critical value is therefore zero.
Since n is at least 2, P' has a root, so the set of critical values is
exactly {0}; all hypotheses of Proposition 7 hold. Its conclusion gives

    P(z)=A(z-z0)^n, A nonzero.                                (M)

For clarity, the theorem can also be checked without trusting its citation:
if P has r distinct roots with multiplicities m_j, shared zeros force all
m_j at least 2, and P' has no other roots. Thus n-1=sum(m_j-1)=n-r, so r=1.
This agrees with (M).

For (M), P'-b has n-1 distinct nonzero roots because

    (z-z0)^(n-1)=b/(An).

If k>n then P^(k)=0 and the condition fails at these points. If 2<=k<n,
the nonzero polynomial P^(k)-b has degree n-k<n-1 and cannot vanish at all
n-1 points. Thus k=n; then P^(n)-b=An!-b must be zero. Consequently

    a=0, n=k, P(z)=b(z-z0)^k/k!.

Conversely this polynomial has the required shared zero set and kth
derivative b everywhere. This gives the entire frozen Proposition 2 as a
short corollary of the identified primary theorem plus elementary degree
counts. No Nevanlinna theorem or unsolved uniqueness claim is being assumed.

## 4. Exact relation to the known square-exponential template

LXY2009, Example 3 and Theorem 1.2(d)/Corollary 1.1, pp.68-69, explicitly
give the template

    H_(B,U)(w)=B(1+(U/2)exp(w/4))^2, B,U nonzero.              (S)

The theorem classifies a different pair of partial-sharing assumptions;
its hypotheses must not be applied directly to (T). Its printed template
and Example 3 are the relevant prior construction.

There is also no reliance on reversing a necessary-condition theorem:
writing s=(U/2)exp(w/4), H=B(1+s)^2 and H'_w=(B/2)s(1+s).
Thus H=0 implies H'_w=0; H=B forces s=-2 (s cannot be zero),
and then H'_w=B. Every displayed source-template member can therefore be
checked directly.

Starting from (S), set U=-2, B=A and w=4 lambda(z-z0). Then

    H_(A,-2)(4 lambda(z-z0))=A(exp(lambda(z-z0))-1)^2.          (F)

Thus the whole functional shape, including a double zero shared IM with
the derivative, is the published template under amplitude and variable
scaling. The following *additional calculation* establishes which members
satisfy the target condition; it is not asserted by LXY2009.

Put t=exp(lambda(z-z0)), lambda nonzero. Then

    F'=2A lambda t(t-1),
    F^(k)=A lambda^k(2^k t^2-2t).

To make the nonzero b-fiber a single quadratic critical fiber, impose

    b=-A lambda/2, i.e. A=-2b/lambda.

Then

    F'-b=2A lambda(t-1/2)^2,

so every b-point has t=1/2, and such points exist. At those points,

    F^(k)/b = -lambda^(k-1)(2^(k-1)-2).

For k>=3 this equals one exactly when

    lambda^(k-1)=-1/(2^(k-1)-2).

Every such lambda is nonzero. The common zero set of F and F' is t=1,
with orders two and one. It contains infinitely many points, proving
transcendence and excluding (E). For k=2 the ratio is zero, so this
particular template with its selected b-fiber cannot give an example;
this says nothing about other entire functions at k=2.

This is an explicit prior-template map and a short finite calculation.
It supports the judgment that the family should be presented as a
specialization of a known construction. It does not establish that the
resonance condition or application to the literal OWR question was already
published before this project.

## 5. Normalization and checks against false implication

For a=0, f -> f/b normalizes the derivative value to 1 and preserves the
shared zero sets and derivative-value implication. Translation of z also
preserves them. Hence arbitrary target b and z0 add no independent
classification burden.

Arbitrary variable scaling does *not* preserve the target derivative-value
condition. If G(z)=alpha f(mu z+nu), its corresponding value is
B=alpha mu b, but at a corresponding b-point G^(k)=mu^(k-1)B. Therefore
the condition is preserved only when mu^(k-1)=1 (assuming a nonempty
b-fiber). Section 4 rechecks the condition after scaling; it does not
silently treat scaling as a symmetry.

For a nonzero shared value, subtraction is not a reduction to zero:
g=f-a gives g'=f', and f=a iff f'=a becomes g=0 iff g'=a.
The zero-boundary constructions cannot be transferred to nonzero a this
way.

For a general nonconstant entire f, sharing zero IM means exactly that
all zeros of f are multiple and f' has no zeros elsewhere. In this case
f/f' extends to an entire function, having a simple zero at a zero z0 of
f of multiplicity m, with local expansion (z-z0)/m+O((z-z0)^2).
This observation is not an entire-function classification: for example
(exp(z)-1)^m for every m>=2, and the zero-free exp(exp(z)), all share zero
IM with their derivatives. Additional hypotheses are needed to apply the
2009 classification. No theorem for sharing a nonzero value CM, or for
partially sharing the *same* value with f', implies a result for the
distinct-b higher-derivative condition without a new argument.

## 6. What is, and is not, established about prior implication

1. **Established:** the exact universal printed statement is false by a
   one-line derivative specialization of a directly relevant 2009 published
   quadratic counterexample.
2. **Established:** the complete polynomial classification is a short
   consequence of an identified earlier primary theorem and degree counts.
3. **Established:** the transcendental construction has a known 2009
   functional template; the target specialization is the explicit short
   computation in Section 4.
4. **Not established:** that an earlier publication explicitly answered
   this precise OWR question; that the lambda condition was printed
   previously; that the original author intended a nonzero-a restriction;
   any classification of all entire solutions; the nonzero-a problem; or
   transcendental examples at k=2.

An elementary source clarification can remain correct and useful. It
cannot be promoted as a substantial novel solution merely by narrowing
the title to the literal printing. The residual candidate contribution is
the documented application to that printing and the specific derivative
resonance calculation. Its scholarly novelty is not certified here.
