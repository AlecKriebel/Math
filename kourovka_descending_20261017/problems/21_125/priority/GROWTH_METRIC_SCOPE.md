# A growth-metric issue in the literal statement of 21.125(a)

Source-contract and priority check, October 24, 2026. **This is an elementary consequence of an established counterexample, not an established original contribution.** The full problem also contains the separate Hydra question (b), which this observation does not answer. Fresh independent adversarial review is required before promoting this check to an accepted project finding.

## The established input

Let \(F_3=\langle a,b,c\rangle\) and let
\[
\alpha(a)=a,\qquad\alpha(b)=ba,\qquad\alpha(c)=ca^2.
\]
These elementary Nielsen moves define an automorphism. The mapping torus is Gersten's group. The author copy of Brady–Soroko, *Dehn functions of subgroups of right-angled Artin groups*, dated August 28, 2020, Appendix 10, displays this exact presentation and proves in **Corollary 10.3** that it does not virtually embed in any RAAG; in particular it is not virtually special. Claim 10.1 treats every finite-index subgroup. The Appendix labels the result folklore, builds on Gersten's 1994 theorem, and supplies a complete proof. We credit this entire obstruction to prior work.

## Changing the representative changes actual word growth

Use the convention \(c_b(x)=bxb^{-1}\), and put \(\varphi=c_b\circ\alpha\). For every integer \(n\ge1\),
\[
\varphi^n=c_{p_n}\circ\alpha^n,
\qquad p_n=\prod_{j=0}^{n-1}ba^j.
\]
This follows inductively from \(\alpha c_w=c_{\alpha(w)}\alpha\). The product is written from left to right in increasing \(j\). It is a positive, freely reduced word of length \(n(n+1)/2\).

Delete its trailing \(a^{n-1}\), and call the remaining positive word \(q_n\). This word ends in \(b\), including when \(n=1\), and
\[
|q_n|=n+\frac{(n-1)(n-2)}2.
\]
Since \(\alpha^n(a)=a\), freely reducing the inner twist gives
\[
\varphi^n(a)=q_na q_n^{-1},\qquad
|\varphi^n(a)|=2|q_n|+1=n^2-n+3.
\]
There is no cancellation at either of the two displayed central joins, since \(q_n\) ends in \(b\). Moreover,
\[
\alpha^n(b)=ba^n,\qquad\alpha^n(c)=ca^{2n},
\]
and therefore every basis image satisfies
\[
|\varphi^n(x)|\le 2|p_n|+1+2n=n^2+3n+1,
\quad x\in\{a,b,c\}.
\]
Consequently
\[
\max_{x\in\{a,b,c\}}|\varphi^n(x)|=\Theta(n^2).
\]
This is precisely the numerical exponent \(m-1\) in the Notebook's **actual basis-word-length definition**, with \(m=3\). Every fixed word also has polynomially bounded actual iterates, by substituting its finitely many letters. If polynomial growth is defined using both positive and negative powers, the negative powers satisfy the same quadratic upper bound by the analogous conjugator formula for \(\varphi^{-n}\).

## The mapping torus is unchanged

Write \(T_\alpha=\langle F_3,t\mid t^{-1}xt=\alpha(x),x\in\{a,b,c\}\rangle\). Define \(s=tb^{-1}\). Then
\[
s^{-1}xs=b(t^{-1}xt)b^{-1}=\varphi(x).
\]
Conversely \(t=sb\) recovers the original presentation. Thus \(T_\varphi\cong T_\alpha\). Reversing the stable letter identifies the convention here with the \(txt^{-1}=\alpha(x)\) convention in the cited Appendix. It follows from the prior nonembedding theorem that \(T_\varphi\) is not virtually special.

**Literal conclusion:** the explicit numerical formulation of 21.125(a), using actual word length of an automorphism representative, has a negative answer by this re-presentation of the known Gersten example. This does not answer 21.125(b).

## Why the outer formulation is different

Inner conjugation preserves the cyclic length of an element. Hence for every fixed word \(w\), the cyclic length of \(\varphi^n(w)\) is at most \(|w|(1+2n)\). The class of \(b\) has cyclic length \(n+1\), since \(ba^n\) is cyclically reduced. Thus the associated outer automorphism has degree **one**, not two. This example does not meet a reformulation requiring outer/cyclic growth of degree \(m-1\).

The Notebook says explicitly how its degree is measured, so that definition must be preserved. The term “maximal” does not authorize changing that explicit definition. An outer-growth version is an alternative research question, and we have no documented clarification authorizing it as a replacement or establishing author intent. We cannot silently replace the statement or assert an official correction. The sheet itself distinguishes actual growth from cyclic growth in §2. Any external clarification would have to be undertaken by the human user; no outreach was initiated or prepared.

## Checkable finite sanity test and limits

`check_growth_metric.py` uses direct free substitution on signed letters, independently compares the product formula, and checks the exact length statements for \(0\le n\le60\). It writes `growth_metric_checks.json`. These finite computations only check implementation and small boundary cases; the induction and freely reduced word argument above establish the unbounded assertion.

No claim is made that this elementary implication has never been noticed or published. The prior theorem is fully sufficient for the obstruction after the explicit change of representative. A priority audit that treated all of (a) as a genuinely unresolved original theorem without addressing this metric issue would be unreliable.
