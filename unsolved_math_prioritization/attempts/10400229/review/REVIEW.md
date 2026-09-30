# Independent review: a prime knot one crossing from its mirror

**Verdict: PASS_SCOPED_ALGEBRAIC_AND_RATIONAL_DIAGRAM_RESULTS.** No mandatory mathematical correction was found. The original prime-knot problem remains **unsolved, 3/5**. This is a separate adversarial AI review, not human peer review or a priority claim.

Reviewer model: gpt-6-astra, xhigh. Review date: 30 September2026. The author’s mathematical files were not edited.

## Snapshot

- `PARTIAL.md`: SHA-256 `0db8a717a9acd85a7bc485be1eacdf4a5b1227ac98f315cc7fcef34585d8dba9`
- Submitted `verify.py`: SHA-256 `337adced8c74944e97e89ec396e87ff0788fce55de92aaa386c2645f81582e1c`
- Submitted `verification.json`: SHA-256 `bd9067c8e77bbeb9a2758bbab1f947a9b90d0f77fe88a60d420559d3a30b6c3b`
- All 21,677 submitted controls reproduced byte-identically in an isolated directory. The script rewrites its receipt, so it was not run in the author’s directory.
- All 35,700 independent exact controls passed.

The verified conclusions are the all-knot algebraic two-torsion constraint, the explicitly conditional rank-two criterion, and the achiral-or-ribbon result when the **specified crossing lies in a signed continued-fraction diagram**. No arbitrary-crossing conversion or prime chiral nonslice counterexample is established.

## 1. Original question and category

I independently read the complete Problem12.24 and adjoining remark on printed p.541 of [Ohtsuki’s collection](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf), including the rendered page, and checked Problem7 in [Stoimenow’s three-page list](https://stoimenov.net/stoimeno/homepage/papers/12pb.pdf). The source requires a prime classical knot and one ordinary crossing change to its mirror. It asks for an achiral-or-slice conclusion and explicitly suggests algebraic sliceness as a weaker alternative.

The package retains those distinctions. Its partial propositions can apply beyond prime knots, but it does not infer a solution of the prime-knot problem from that fact. An unoriented mirror equivalence causes no difficulty in Proposition1 because reversal leaves the algebraic concordance class unchanged. A noncoherent band attachment is not an ordinary crossing change.

The smoothing observation is correctly credited and limited. Equality of the knot Conway polynomials forces the oriented smoothing polynomial to vanish by the skein relation. This does not construct disjoint slice disks for the smoothing link. The subsequent conditional band-joining observation does not supply those disks.

## 2. The Witt deduction is exact

I read the complete relevant Section7 of the published [Kim–Livingston paper](https://msp.org/pjm/2005/220-1/pjm-v220-n1-p05-s.pdf), including the normalization on pp.94–95, the two-by-two crossing block on pp.96–97, and Theorems7.5–7.6 on the rendered p.97. The source uses the involution $t\mapsto t^{-1}$ and an injective map from integral algebraic concordance to the Hermitian Witt group of $\mathbb Q(t)$. It explicitly states the diagonal crossing-difference representative used by the author.

For a mirror pair, the normalized polynomials coincide with a symmetric nonzero polynomial $D$. The Hermitian change of basis $\operatorname{diag}(D^{-1},1)$ transforms $\operatorname{diag}(D^2,-1)$ to $\operatorname{diag}(1,-1)$ because $\overline D=D$. The latter is hyperbolic. This calculation is over the rational-function field, so zeros of a particular specialization of $D$ do not invalidate it. Injectivity gives equal algebraic classes for the crossing resolutions. Mirroring negates the class, while reversal preserves it, giving precisely $2[K]=0$.

There is no inference here that $[K]=0$. Nor are the full smooth or topological concordance groups substituted for algebraic concordance. Kim–Livingston’s injection and its credited earlier foundations remain imported theorems; the application and local crossing algebra were independently checked, rather than the whole theory being reproved.

## 3. Algebraic obstruction and rank-two hypothesis

For the displayed matrices $V$ and $P$, direct multiplication gives $P^TVP=-V$ with $\det P=-1$. The subgroup $\{(z,Pz):z\in\mathbb Z^2\}$ is a direct summand of $\mathbb Z^4$: projection onto the first two coordinates is a left inverse of its inclusion. It has half rank and is isotropic for $V\oplus V$. Thus the integral form has order dividing two.

It is not zero. The equation for an isotropic rational vector has discriminant five, so no nonzero rational isotropic vector exists; an integral metabolizer would give one. This proves a genuinely nonzero order-two algebraic class. The normalized polynomial $3-t-t^{-1}$ and determinant five are consistent. The metabolic blocks $H_e$ have normalized Alexander polynomial one and a primitive isotropic coordinate line. Their stabilization therefore preserves the nonzero algebraic class while allowing the stated one-entry matrix difference.

These are algebraic diagnostics. Admissibility of matrices and a formal rank-one change do not construct a geometrically specified crossing between a prime chiral knot and its mirror. The candidate makes no such realization claim.

For Proposition2, the determinant identity is valid symbolically:

$$\det(V+\varepsilon E_{11}-t(V+\varepsilon E_{11})^T)-\det(V-tV^T)
=\varepsilon d(1-t)^2.$$

A rank-two Seifert matrix has normalized polynomial $t^{-1}\det(V-tV^T)$, with value one at $t=1$ under the stated skew-unimodularity condition. Thus there is no hidden unit or sign ambiguity between two matrices of the same size. Equality forces $d=0$, and the second coordinate line is then a primitive metabolizer for both forms. The norm factorization and square determinant follow directly.

Crucially, the hypothesis concerns a **simultaneous crossing-adapted rank-two pair**. The existence of a genus-one Seifert surface separately for each knot does not imply this simultaneous realization. Stabilization can be required. The artifact does not erase that qualification or upgrade algebraic sliceness to smooth sliceness.

## 4. Signed rational-diagram argument

The determinant-preserving calculation covers the entire stated diagram class. Products of the integer matrices $M(z)$ are unimodular, including zero coefficients and empty products, so their fraction columns stay primitive. For a crossing in one twist region, changing its sign changes the corresponding integer by two with a sign. The proof allows both signs and does not depend on positivity or reducedness of the full continued fraction.

Equal mirror determinants give $|p'|=|p|\ne0$, so the two branches are exhaustive.

### Same numerator

If $p'=p$, the update formula forces $au=0$. If $u=0$, both numerator and denominator are independent of the changed coefficient. If $a=0$, the unimodular determinant equation gives $b,c\in\{\pm1\}$; since $p=bu\ne0$, the denominator change is an integer multiple of $p$. In both cases the normalized two-bridge denominator class is unchanged. Standard two-bridge classification therefore gives the same knot, and the additional mirror hypothesis makes it achiral. The unknot case $|p|=1$ is harmless. No division by $a$ or $u$ is made in these degenerate branches.

### Opposite numerator

If $p'=-p$, then $au\ne0$ and $p=\varepsilon au$. The remaining equation is

$$(x-\varepsilon)au+bu+aw=0.$$

Reducing modulo $a$ and using $\gcd(a,b)=1$ proves $a\mid u$. Reducing modulo $u$ and using $\gcd(u,w)=1$ proves $u\mid a$. This is valid for negative integers as well, so $u=\eta a$ for $\eta\in\{\pm1\}$. Consequently $|p|=a^2$ and substitution gives

$$q=\eta(\varepsilon ac+\delta),\qquad \delta=\det Q.$$

Normalizing the numerator to be positive multiplies the denominator by $\varepsilon\eta$, giving $\widetilde q=ac+\varepsilon\delta$. Let $m=|a|$. If $m>1$, unimodularity ensures that the residue $k\equiv\operatorname{sign}(a)c\pmod m$ lies in $\{1,\ldots,m-1\}$ and is coprime to $m$. Therefore $\widetilde q\equiv mk\pm1\pmod{m^2}$. Those representatives lie strictly between zero and $m^2$. Oddness of the knot numerator forces $m$ odd. The resulting family is exactly the credited ribbon family.

As an additional sign check, the other normalized denominator is $ac-\varepsilon\delta$, so their product is congruent to $-1$ modulo $a^2$. This also agrees with the usual two-bridge mirror convention. The explicit $9/4$ and $9/2$ example passes.

### Imported ribbon conclusion

I checked the published [Lisca paper](https://msp.org/gt/2007/11-1/gt-v11-n1-p07-p.pdf), introduction, Definition1.1(1) and Corollary1.3, for the precise family and isotopy/mirror conventions. I also inspected the complete relevant Sections2–3 of [Horigome–Ichihara v4](https://arxiv.org/pdf/2402.07539v4), including the odd/even symmetric-union diagrams in Figures5–6. The note that its Conway convention mirrors Lisca’s is explicit in that primary source. Ribbonness and the achiral alternative are invariant under that common mirror convention.

There is an independent short check of the construction’s fraction calculation. Put $J=\operatorname{diag}(1,-1)$ and let the prefix product be $Q=\left(\begin{smallmatrix}m&b\\k&d\end{smallmatrix}\right)$ of length $n$. Since $M(-z)=-JM(z)J$, the negative reversed suffix product is $(-1)^nJQ^TJ$. The first column of the symmetric-union product is therefore

$$(-1)^n\binom{\varepsilon m^2}{\varepsilon mk+\det Q}
=\binom{\varepsilon(-1)^n m^2}{\varepsilon(-1)^n mk+1}.$$

This verifies the parameter match independently of the source’s longer induction. The geometric ribbon theorem remains credited prior mathematics; the whole Donaldson-theoretic classification is not re-audited or needed here. A square determinant alone would not justify the conclusion.

## 5. Scope and current-source check

The current [Horigome–Ichihara arXiv record](https://arxiv.org/abs/2402.07539) identifies v4, dated26May2024. Its source explicitly provides a detailed construction of the family. The author’s [Nihon University publication record](https://researcher-web.nihon-u.ac.jp/search/detail?lang=en&st=researcher&systemId=39ec6e1133775d11154a2e8398a6bbb76028e311e4c8552c) corroborates the July2024 journal publication. The proof checked here is the full v4 preprint, not a line-by-line comparison with the final journal PDF. The [2026 grid-diagram paper](https://arxiv.org/abs/2504.09749) concerns noncoherent band attachments/$H(2)$ moves. Its definitions, rather than an isolated use of “crossings” in the introduction, determine the operation. Those examples do not meet the ordinary-crossing hypothesis of the target.

The essential remaining gap is unchanged: an arbitrary crossing that takes a prime knot to its mirror has not been converted to a crossing in a continued-fraction diagram or to a crossing-adapted rank-two Seifert presentation. Even for a rational knot, the knot type alone does not identify the particular crossing with the one in the proved diagram class. The order-two result leaves nonzero algebraic two-torsion. No global achiral-or-slice theorem follows.

## 6. Reproduction

From this report’s directory:

```sh
(cd author_replay && cp verification.json /tmp/mirror-crossing-expected.json && python verify.py > /tmp/mirror-crossing-author.json && cmp verification.json /tmp/mirror-crossing-expected.json)
python independent_checks.py > /tmp/mirror-crossing-independent.json
cmp independent_results.json /tmp/mirror-crossing-independent.json
```

The independent code uses symbolic determinants/Hermitian congruence and backward continuant recursion, without importing the submitted checker. It tests all 14,844 genuine coefficient-crossing changes in signed continued fractions of length at most five with coefficients in $[-2,2]$, including 2,600 odd-determinant-preserving instances and both zero-prefix/zero-suffix branches. It also checks the symmetric-union identity, metabolic stabilization and the primitive graph argument. These bounded checks support the analytic proofs; they do not certify knot isotopy, primeness, geometric crossing conversion or an unrestricted sliceness theorem.

**Final recommendation:** retain `unsolved`, three approaches, all diagram/rank qualifications and prior-source credit. No mandatory correction is required. The package is suitable for a draft PR only with this partial scope and its explicit absence of a full original resolution or novelty claim.
