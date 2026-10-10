# Complete integral closure of a total blow up ring

## Verdict and attribution

This is AI-assisted authored mathematics and an independent internal AI mathematical audit. Acceptance means acceptance of the exact prior negative resolution below by internal mathematical review. This reconstruction and audit are unrefereed; no external human peer review or formal proof-assistant certification is claimed.

**Accepted: the unrestricted question has a negative answer.** There is a three-dimensional regular local ring $R$, a valuation $v$ of its own fraction field centered on $R$, and an infinite sequence of local quadratic transforms along $v$, with union $S=B_\infty(R,v)$, for which

$$
S^*=S[1/x]=R_{(y,z)R}\cong k(x)[y,z]_{(y,z)}.
$$

The last ring is a two-dimensional regular local ring and is not a valuation ring. Below is a complete elementary reconstruction of an explicit instance of the already published counterexample, including the valuation, every localization, and both inclusions in the complete-integral-closure calculation.

The source is W. Heinzer, K. A. Loper, B. Olberding, H. Schoutens and M. Toeniskoetter, *Ideal theory of infinite directed unions of local quadratic transforms*, Journal of Algebra **474** (2017), 213–239, [DOI 10.1016/j.jalgebra.2016.11.014](https://doi.org/10.1016/j.jalgebra.2016.11.014). The mathematical text inspected is [arXiv:1505.06445v3](https://arxiv.org/abs/1505.06445v3), especially Example 7.2 and the relevant directions of Theorem 6.9. The authors explicitly identify D. Shannon, *Monoidal transforms of regular local rings*, American Journal of Mathematics **95** (1973), 294–320, Example 4.7, as the antecedent. Credit for the example and complete-closure calculation remains with these sources. This reconstruction makes no new-result or historical-priority claim.

## Exact question and conventions

The original contribution is H. Schoutens, “The total blow-up along a valuation,” joint work with A. Loper, B. Olberding and W. Heinzer, in *Valuation Theory and Its Applications*, Oberwolfach Report 49/2014, printed pages 2805–2806. The report appears in Oberwolfach Reports **11** (2014), 2757–2823, with publication date 29 October 2015. [Original report](https://ems.press/content/serial-article-files/46540); [publisher metadata](https://ems.press/journals/owr/articles/13351).

Its input is a regular local ring $(R,\mathfrak m)$ with fraction field $K$ and a valuation of $K$ centered on $R$. At a stage with regular parameters, one chooses a parameter of least value, adjoins the ratios of the other parameters to it, and inverts all elements of value zero. The union of the successive local rings is $B_\infty(R,v)$. The question asks whether the complete integral closure of this union, taken inside the **same field $K$**, is a valuation ring. No restriction to dimension two, rank-one valuations, or archimedean unions occurs in this question.

For a domain $A\subset K$, use

$$
A^*=\{t\in K:\text{there exists }0\ne d\in A
\text{ such that }dt^n\in A\text{ for every }n\ge0\}.
$$

The witness $d$ is fixed while $n$ varies. This is almost integrality, not merely ordinary integrality. A subring $A\subset K$ with fraction field $K$ is a valuation ring if and only if, for every nonzero $t\in K$, at least one of $t,t^{-1}$ belongs to $A$.

## An explicit centered valuation

Let $k$ be any field, for example $\mathbb Q$, and set

$$
R=k[x,y,z]_{(x,y,z)},\qquad K=k(x,y,z).
$$

Thus $R$ is a three-dimensional regular local ring with the indicated regular parameters. Order $\Gamma=\mathbb Z^3$ lexicographically, with the first coordinate most significant. For a nonzero polynomial define

$$
v\!\left(\sum c_{abc}x^ay^bz^c\right)
=\min_{c_{abc}\ne0}(c,b,a).
$$

Each monomial has a different value. The product of the unique least monomials is the unique least monomial in a product; its coefficient is nonzero. Hence $v(fg)=v(f)+v(g)$, and cancellation in a sum can only increase its value. Extend to $K^\times$ by $v(f/g)=v(f)-v(g)$. Multiplicativity makes this definition independent of the chosen fraction. The resulting valuation is surjective onto $\mathbb Z^3$, since

$$
v(x)=(0,0,1),\qquad v(y)=(0,1,0),\qquad v(z)=(1,0,0).
$$

In particular this is a rank-three valuation. Its valuation ring $U=\{0\}\cup\{t:v(t)\ge0\}$ has fraction field $K$. A polynomial with nonzero constant coefficient has value zero, while a polynomial in $(x,y,z)$ has strictly positive value. Consequently $R\subset U$ and $\mathfrak m_U\cap R=(x,y,z)R$: $U$ dominates $R$. For every positive integer $n$,

$$
nv(x)<v(y),\qquad nv(x)<v(z).
$$

This supplies, rather than assumes, the valuation required in Example 7.2. The chosen $U$ is the valuation determining the transforms; it is not asserted to be the paper's boundary valuation ring.

## The exact local quadratic transforms

For $i\ge0$, write

$$
y_i=y/x^i,\qquad z_i=z/x^i,\qquad
A_i=k[x,y_i,z_i],\qquad
R_i=(A_i)_{(x,y_i,z_i)}.
$$

The three displayed generators of $A_i$ are algebraically independent, since $y=x^iy_i$ and $z=x^iz_i$ inside $K$. Therefore every $R_i$ is a three-dimensional regular local ring with fraction field $K$, and $R_0=R$.

The values of the parameters are

$$
v(x)=(0,0,1),\quad v(y_i)=(0,1,-i),\quad
v(z_i)=(1,0,-i).
$$

They are all positive, and $x$ is strictly the least. In coordinates $x,y_i,z_i$, a monomial $x^a y_i^b z_i^c$ has value

$$
(c,b,a-i(b+c)).
$$

Distinct exponent triples still give distinct values. Every nonconstant coordinate monomial has positive value. Thus a polynomial in $A_i$ has value zero exactly when its constant coefficient is nonzero. The center of $U$ on $A_i$ is exactly $(x,y_i,z_i)$, and $U$ dominates $R_i$.

The $x$-chart for the next blow-up is

$$
C_i=R_i[y_i/x,z_i/x]=R_i[y_{i+1},z_{i+1}].
$$

Under $y_i=xy_{i+1}$ and $z_i=xz_{i+1}$, every denominator used to define $R_i$ remains a polynomial with nonzero constant coefficient in $A_{i+1}$. Thus $C_i$ is a localization of $A_{i+1}$ at some of its value-zero elements. Localizing $C_i$ further at the center of $U$, equivalently inverting every value-zero element, inverts precisely all polynomials of $A_{i+1}$ with nonzero constant coefficient. The result is exactly $R_{i+1}$.

This proves inductively that these are the original report's successive blow-ups along $v$, including the required localizations. The inclusions are strict: $y_i/x\notin R_i$, because the independent parameter $y_i$ is not divisible by the prime element $x$ in $R_i$. Therefore the sequence is genuinely infinite and

$$
S=\bigcup_{i\ge0}R_i=B_\infty(R,v)\subset K.
$$

The local inclusions imply that $S$ is local, with maximal ideal $N=\bigcup_i (x,y_i,z_i)R_i$. Since $y_i=xy_{i+1}$ and $z_i=xz_{i+1}$, every element of $N$ lies in $xS$; the converse is immediate. Hence $N=xS$. The element $x$ is not a unit, because its value is positive and $S\subset U$. Also $0\ne y\in x^nS$ for every $n\ge0$, so $S$ is nonarchimedean.

## Computing the overring without an omitted localization

Put

$$
T=R_{(y,z)R}=k[x,y,z]_{(y,z)}.
$$

The element $x$ is a unit in $T$. Each $y_i,z_i$ belongs to $T$. A denominator $h(x,y_i,z_i)$ used in $R_i$ has nonzero constant coefficient; modulo $(y,z)T$, its image is the nonzero polynomial $h(x,0,0)$ in $k(x)$. Therefore it is a unit in $T$. This proves $R_i\subset T$ for all $i$, and consequently $S[1/x]\subset T$.

For the converse, take a polynomial $g\in k[x,y,z]\setminus(y,z)$. There exist $e\ge0$, a polynomial $u\in k[x]$ with $u(0)\ne0$, and polynomials $a,b\in k[x,y,z]$ such that

$$
g=x^e u(x)+ya+zb.
$$

Choose any $i>e$. After substituting $y=x^iy_i,z=x^iz_i$,

$$
g/x^e=u(x)+x^{i-e}\bigl(y_i a(x,x^iy_i,x^iz_i)
+z_i b(x,x^iy_i,x^iz_i)\bigr).
$$

This is an element of $A_i$ with nonzero constant coefficient $u(0)$. It is therefore a unit of $R_i\subset S$. It follows that

$$
1/g=x^{-e}(g/x^e)^{-1}\in S[1/x].
$$

Every denominator defining $T$ is inverted in $S[1/x]$, so $T\subset S[1/x]$, completing the equality.

The stage localizations are essential. In general $S[1/x]$ must not be replaced by $R[1/x]$. For example $1/(x+y)\in T$; the proof above realizes $(x+y)/x=1+y_1$ as a unit in $R_1$. But the prime ideal $(x+y)R$, which does not contain $x$, survives localization to $R[1/x]$, so $x+y$ is not a unit there.

## Computing the complete integral closure

First, the fixed nonzero element $y\in S$ satisfies

$$
yT\subset S.
$$

Indeed, every $t\in T=S[1/x]$ can be written $s/x^m$ with $s\in S$ and $m\ge0$; then $yt=(y/x^m)s\in S$. Since $T$ is a ring, for each $t\in T$ every power $t^n$ belongs to $T$, and hence $yt^n\in S$ for all $n\ge0$. Thus **the same witness $y$** proves $T\subset S^*$. In particular $1/x$ is almost integral, with $y/x^n\in S$ for every $n$.

For the other inclusion, observe that

$$
T\cong k(x)[y,z]_{(y,z)}
$$

inside $K$: first invert nonzero polynomials in $x$, then invert the polynomials whose constant coefficient as polynomials in $y,z$ is nonzero. A polynomial ring over a field is a UFD, and its localization is a UFD. Thus $T$ is completely integrally closed, as the following elementary argument verifies.

Write $q=a/b\in\operatorname{Frac}(T)$ with $a,b\in T$ relatively prime. If $b$ is not a unit, choose an irreducible factor $p\mid b$. For any nonzero $d\in T$, the exponent of $p$ in $dq^n$ is

$$
\operatorname{ord}_p(d)-n\operatorname{ord}_p(b),
$$

because $p\nmid a$. It becomes negative for sufficiently large $n$, so $dq^n\notin T$. Therefore no such $q\notin T$ is almost integral over $T$.

Now suppose $q\in S^*$. Its fixed witness $0\ne d\in S\subset T$ also satisfies $dq^n\in T$ for all $n$. Complete integral closedness of $T$ forces $q\in T$. Combining both inclusions gives

$$
\boxed{S^*=T=R_{(y,z)R}.}
$$

This argument reconstructs the mechanism of Theorem 6.9, directions (1) to (2) to (3), for the explicit example. It needs neither the paper's general Noetherian-hull theorem nor an assumption that complete integral closure is always idempotent. The larger assertion that every normal Noetherian domain is completely integrally closed is valid, but the UFD argument here proves everything required directly.

## Why the resulting ring is not a valuation ring

In $T=k(x)[y,z]_{(y,z)}$, the elements $y,z$ remain nonassociate prime nonunits. Therefore $y/z\notin T$ and $z/y\notin T$. For a direct localization check, an equation $y/z=a/h$, where $h\notin(y,z)$, would give $hy=az$. The prime element $z$ does not divide $y$, so $z\mid h$, contradicting $h\notin(y,z)$. Interchanging $y,z$ gives the other exclusion. This violates the valuation-ring criterion for the nonzero element $y/z\in K$.

Equivalently, $T$ is a two-dimensional regular local ring with maximal ideal generated by the two incomparable parameters $y,z$. Its dimension follows from localization of the polynomial ring $k(x)[y,z]$ at $(y,z)$. The explicit fraction obstruction, rather than dimension alone, establishes nonvaluation.

## Source correspondence and adversarial checks

1. The source's requirement $nu(x)<u(y),u(z)$ for every positive integer is realized by the lexicographic valuation above. A real rank-one weight assignment would not meet this requirement.
2. Every $R_i$ has exactly the source's maximal ideal $(x,y/x^i,z/x^i)R_i$, and the localizations are derived explicitly rather than inferred from the generating set.
3. The sequence never terminates; all rings retain dimension three and each inclusion is proper.
4. $S$, $S^*$, $T$, and $U$ are all subrings of the original field $K$. No completion or field enlargement is used.
5. The same nonzero witness $y$ works for all powers, and even for every element of $T$. No variable-dependent witness is substituted for almost integrality.
6. Complete integral closure and ordinary integral closure are distinguished. In fact each $R_i$ is integrally closed, so their directed union $S$ is integrally closed; nevertheless $1/x\in S^*\setminus S$. For the directed-union assertion, a monic equation has finitely many coefficients, all in some $R_i$, and its root lies in $K=\operatorname{Frac}(R_i)$.
7. The fact that $S$ is not a valuation ring is insufficient by itself. The audit computes $S^*$ exactly and separately exhibits the obstruction there.
8. The valuation $U$ of rank three is not confused with the boundary valuation of the general theory. No rank bound on the latter is invoked.
9. The source's prior-credit chain to Shannon is preserved. Shannon's 1973 original article was not independently inspected in this audit; that example-number attribution is explicitly mediated by Example 7.2.
10. The final journal PDF was not inspected. The 2017 journal citation is metadata-verified; there is no claim of byte or text identity with the arXiv body.

## Exact accepted and excluded scope

Accepted is a full negative resolution of the unrestricted universal question recorded as 30002714 / OWR-13351-013, by a completely specified instance of the published nonarchimedean Example 7.2. Specializing the starting regular local ring to a polynomial localization is sufficient to refute the universal assertion; it does not replace a requested universal positive theorem with a partial result.

This audit does not independently certify every theorem or every arbitrary-ring instance in the source paper. It does not establish a rank-one counterexample, an archimedean counterexample, a classification of all total blow-up rings, or any new theorem. The separate stronger example in arXiv:1509.07545 is unnecessary and is not accepted by proxy. There is no formal proof-assistant verification or external human peer-review claim.

The mathematical proof is the authored argument above. Finite computational diagnostics and file-integrity checks, where recorded, are supplementary checks and do not establish the universal mathematical steps.

## Inspection and date corrections

The original OWR contribution was read in full on printed pages 2805–2806 (PDF pages 49–50), with both pages visually inspected. For arXiv:1505.06445v3, the inspected passages include the introduction, Settings 3.1 and 6.1, the definition of complete integral closure, Theorem 6.9 with its proof, and Example 7.2. Full-page visual inspection covered PDF pages 1, 8, 16, 17, 19, 20 and 21.

The arXiv v3 submission date is **1 October 2016**, as shown both in its margin and its submission history. The retrieved PDF also displays an internal typesetting date of **28 October 2021**. Those are distinct pieces of metadata; neither is the 2017 journal publication date.

This is a source-credit audit dated 10 October 2026. No novelty or historical-priority claim is made.
