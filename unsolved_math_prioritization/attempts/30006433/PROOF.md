# Rank-two subalgebra zeta asymptotics

This is an AI-assisted, unrefereed mathematical review edition. Acceptance is an independent internal AI audit judgment, not external human peer review, journal acceptance, formal proof-assistant certification, or novelty clearance.

The full authored mathematical proof and audit, including every analytical formula and theorem table, are retained. This is not a computational reproduction package: executable code, raw HNF or root-enumeration datasets, copied source PDFs/text/images, and private coordination material are not distributed. Historical finite checks support the written proof and cannot be reproduced from this edition alone.

Source retrieval, inspection, and mathematical executions described below are historical acts of the original investigation or audit. Publication preparation performed no new scholarly-source retrieval, source-body inspection, or mathematical execution. The original reports remain unchanged.

## Status and exact scope

This note proves the degree and coincidence assertions for every not necessarily associative, not necessarily commutative integral algebra whose additive group is free of rank at most two. It does not resolve either assertion in arbitrary rank. The rank-two proof is shared progress on the two assertions, not two independent discoveries. No novelty claim is made.

For a finite-free integral algebra A of rank d, subalgebras here are additive finite-index subgroups closed under multiplication; they need not contain an identity. We use Rossmann's normalization of the topological subalgebra zeta function. The invariants being compared are

\[
m_{\rm top}(A)=\lim_{s\to\infty}s^d Z^A_{\rm top}(s),\qquad
m_{\rm red}(A)=\lim_{T\to1}(1-T)^d Z^A_{\rm red}(T).
\]

The first limit is equivalently the evaluation of \(u^{-d}Z^A_{\rm top}(u^{-1})\) at \(u=0\). It is not an asymptotic at the original variable \(s=0\). The exact conjectures and algebra class appear in Tobias Rossmann, *Reduced and topological zeta functions in enumerative algebra*, [author-hosted contribution, pp. 2–3](https://torossmann.github.io/files/mfo25b.pdf), also in [Oberwolfach Report 38/2025, printed pp. 2106–2107](https://ems.press/content/serial-article-files/52251).

## 1. Statement of the rank-two result

Choose any integral basis of A and identify its underlying module with \(\mathbb Z^2\). Define the homogeneous binary cubic

\[
f_A(x,y)=\det(v,v\cdot v),\qquad v=(x,y).
\]

Changing basis changes this cubic by an invertible linear substitution and a nonzero scalar. Therefore its geometric projective root multiplicities are intrinsic.

**Theorem.** If A has additive rank two, its reduced and topological subalgebra zeta functions are as follows. Root multiplicities mean multiplicities over \(\mathbb C\), including a possible root at infinity.

| Cubic type | \(Z^A_{\rm top}(s)\) | \(Z^A_{\rm red}(T)\) | \(m_{\rm top}=m_{\rm red}\) |
|---|---|---|---|
| \(f_A=0\) | \(1/[s(s-1)]\) | \(1/(1-T)^2\) | \(1\) |
| One root, multiplicity 3 | \(2/[s(3s-2)]\) | \((1+T^2)/[(1-T)(1-T^3)]\) | \(2/3\) |
| Multiplicities 2 and 1 | \(2/[s(2s-1)]\) | \(1/(1-T)^2\) | \(1\) |
| Three distinct roots | \(4/[s(3s-1)]\) | \((1+T)^2/[(1-T)(1-T^3)]\) | \(4/3\) |

In particular, \(\deg Z^A_{\rm top}=-2\), both leading evaluations exist, and they agree and are positive.

There is a geometric expression for the common value. Let \(\mathcal S_1(A_{\mathbb C})\) be the projective variety of one-dimensional subalgebras of \(A\otimes\mathbb C\), with its reduced underlying variety. Then

\[
m_{\rm top}(A)=m_{\rm red}(A)
=\frac{1+\chi(\mathcal S_1(A_{\mathbb C}))}{3}.
\]

Indeed, \(\mathcal S_1\) is the zero set of \(f_A\) in \(\mathbb P^1\). If \(f_A=0\), it is all of \(\mathbb P^1\), of Euler characteristic two. Otherwise its Euler characteristic is the number of distinct geometric roots. This formula is asserted only in rank two.

## 2. Lattice parametrization and the single closure condition

Work first over a compact discrete valuation ring \(\mathfrak o\), with uniformizer \(\pi\), residue field of size q, and a bilinear multiplication on \(\mathfrak o^2\). For every full lattice B there is a unique integer \(a\geq0\) such that

\[
B=\pi^a C,
\]

where C is primitive, meaning \(C\not\subseteq\pi\mathfrak o^2\). The elementary divisors of C are \((1,\pi^b)\), for a unique \(b\geq0\). If \(b=0\), then \(C=\mathfrak o^2\). If \(b>0\), choose a basis \((v,w)\) of \(\mathfrak o^2\) with

\[
C=\mathfrak o v+\pi^b\mathfrak o w.
\]

Such C are in bijection with primitive projective lines in \((\mathfrak o/\pi^b)^2\), namely \(\mathbb P^1(\mathfrak o/\pi^b)\). Their number is \((q+1)q^{b-1}\). Reduction from level b to any level \(1\leq k\leq b\) has fibers of cardinality \(q^{b-k}\). These facts also follow from the disjoint charts

\[
(1,t),\quad t\in\mathfrak o/\pi^b,
\qquad
(\pi t,1),\quad t\in\mathfrak o/\pi^{b-1}.
\]

B is a subalgebra precisely when \(\pi^a(C\cdot C)\subseteq C\). Products involving \(\pi^b w\) already lie in \(\pi^b\mathfrak o^2\subseteq C\), even before multiplication by \(\pi^a\). Consequently, there is just one condition:

\[
\pi^a(v\cdot v)\in C
\quad\Longleftrightarrow\quad
\pi^b\mid \pi^a\det(v,v\cdot v).
\tag{1}
\]

The equivalence uses that \(\det(v,w)\) is a unit. It does not use commutativity, associativity, polarization, or invertibility of 2. Also \(|\mathfrak o^2:B|=q^{2a+b}\).

For \(k\geq1\), write

\[
N_k(q)=\#\{\ell\in\mathbb P^1(\mathfrak o/\pi^k):f_A(\ell)=0\pmod{\pi^k}\},
\qquad N_q(T)=\sum_{k\geq1}N_k(q)T^k.
\]

The condition is independent of the primitive representative of a projective line because f is homogeneous. If \(b\leq a\), (1) is automatic. If \(b>a\), put \(k=b-a\); exactly \(q^aN_k(q)\) primitive lattices C satisfy (1). Thus the local subalgebra generating function is exactly

\[
Z^A_{\mathfrak o}(T)
=\frac{1}{1-qT^3}
\left(\frac{1+T^3}{1-T^2}+N_q(T)\right).
\tag{2}
\]

This identity is valid at every prime, including bad primes, with the actual numbers \(N_k(q)\).

For completeness, the \(b=0\) and \(1\leq b\leq a\) contributions sum to

\[
\frac1{1-T^2}
+\sum_{b\geq1}(q+1)q^{b-1}T^b\frac{T^{2b}}{1-T^2}
=\frac{1+T^3}{(1-T^2)(1-qT^3)}.
\]

The remaining contribution is \(\sum_{a\geq0,k\geq1}q^aN_k(q)T^{3a+k}=N_q(T)/(1-qT^3)\). This proves (2), with no rationality theorem needed for that identity.

## 3. Root lifting and the nonuniform local formula

Assume now that f is nonzero. For \(e=1,2,3\), let \(V_e\) be the reduced finite scheme over \(\mathbb Q\) parametrizing geometric projective roots of multiplicity e. Outside finitely many primes these schemes have disjoint finite étale integral models, and the distinct factors of f retain their multiplicities. The unit content and resultant/discriminant conditions involved exclude only finitely many primes.

Let \(r_e(q)=\#V_e(\mathbb F_q)\). Near a residue-field rational root of multiplicity e, Hensel's lemma supplies a local parameter z centered at its unique lift, and

\[
f=z^e\cdot\text{unit}.
\]

Consequently the number of its lifts modulo \(\pi^k\) with f divisible by \(\pi^k\) is \(q^{k-\lceil k/e\rceil}\). Roots not rational over the residue field give no point in \(\mathbb P^1(\mathbb F_q)\), and hence no contribution. Therefore, at every good prime and over every finite extension of its local field,

\[
N_k(q)=\sum_{e=1}^3 r_e(q)q^{k-\lceil k/e\rceil},
\]

and grouping \(k=e\ell+j\), \(1\leq j\leq e\), gives

\[
N_q(T)=\sum_{e=1}^3 r_e(q)
\frac{\sum_{j=1}^e q^{j-1}T^j}{1-q^{e-1}T^e}.
\tag{3}
\]

Equations (2) and (3) are a Denef-type formula, not an assumption of a single uniform local rational function. Splitting behavior is retained through the schemes \(V_e\).

Put \(r_e=\#V_e(\mathbb C)=\chi(V_e(\mathbb C))\), and \(R=\sum_e r_e\). Since f is a nonzero binary cubic, \(\sum_e e r_e=3\). The only possibilities are therefore the three partitions of 3 appearing in the theorem.

## 4. The two specializations

For the topological specialization, multiply the local expression by \((1-q^{-1})^2\), substitute \(T=q^{-s}\), expand at \(q=1\), and take the constant term. In the Denef coefficients, replace \(r_e(q)\) by \(\chi(V_e(\mathbb C))=r_e\). This is the normalization and specialization of [Rossmann, *Computing topological zeta functions … I*, §§5.1–5.4](https://torossmann.github.io/files/topzeta.pdf), in particular definitions 5.2 and 5.17 and theorem 5.12. Each term here has at most two vanishing denominator factors and the normalized expansion is regular.

Writing \(h=q-1\), the needed first-order identities are

\[
1-q^aT^b=(bs-a)h+O(h^2),\qquad
1-q^{-1}=h+O(h^2).
\]

In (2), the first term contributes \(1/[s(3s-1)]\). Each root of multiplicity e contributes \(e/[(3s-1)(es-e+1)]\). Hence

\[
Z^A_{\rm top}(s)=\frac1{3s-1}
\left(\frac1s+\sum_{e=1}^3\frac{e r_e}{es-e+1}\right).
\tag{4}
\]

For the reduced specialization, all rational functions in (2)–(3) are regular at \(q=1\) as elements of \(\mathbb Q(T)\). Thus coefficientwise Euler specialization gives

\[
Z^A_{\rm red}(T)=\frac1{1-T^3}
\left(\frac{1+T^3}{1-T^2}+\frac{RT}{1-T}\right).
\tag{5}
\]

Here \((T+\cdots+T^e)/(1-T^e)=T/(1-T)\). The use of Euler specialization for a regular Denef formula is justified in [Rossmann, *Computing local zeta functions of groups, algebras, and modules*, lemma 7.1 and remark 7.2](https://torossmann.github.io/files/padzeta.pdf). Alternatively, the projective-line charts and the root-lifting strata above are affine spaces over the respective root schemes, and their Euler characteristics directly give (5).

It follows from (4) and (5) that

\[
\lim_{s\to\infty}s^2Z^A_{\rm top}(s)
=\frac{1+R}{3}
=\lim_{T\to1}(1-T)^2Z^A_{\rm red}(T)>0.
\]

Substituting the three root-multiplicity partitions and simplifying proves the three nonzero-cubic rows of the theorem, including the claimed rational-function degrees after cancellation.

If \(f=0\), then \(N_k(q)=(q+1)q^{k-1}\). Formula (2) reduces to

\[
Z^A_{\mathfrak o}(T)=\frac1{(1-T)(1-qT)}.
\]

Equivalently (1) says that every lattice is a subalgebra. Its specializations are \(1/[s(s-1)]\) and \(1/(1-T)^2\). This completes the proof.

In rank one, writing \(A=\mathbb Z e\) and \(e^2=ce\), every subgroup \(n\mathbb Z e\) is a subalgebra. Thus \(Z_{\rm top}=1/s\), \(Z_{\rm red}=1/(1-T)\), and the common leading value is 1. In rank zero all zeta functions equal 1. The theorem therefore establishes both assertions for every \(d\leq2\).

## 5. A conditional general specialization lemma

The following elementary statement isolates one useful condition; it is not asserted to hold for every algebra's Denef data.

**Lemma.** Let d be a nonnegative integer. Suppose a rational function can be written

\[
W(X,T)=\frac{P(X,T)}{U(X,T)\prod_{j=1}^r(1-X^{a_j}T^{b_j})},
\]

where P and U are analytic rational germs at \((1,1)\), \(U(1,1)\ne0\), the \(a_j\) are integers, and \(b_j>0\). Suppose \(h^dW(1+h,(1+h)^{-s})\) is regular at \(h=0\). Define F(s) as its value there and G(T)=W(1,T). Then

\[
\deg F\leq-d\quad(F\ne0),\qquad
\lim_{s\to\infty}s^dF(s)
=\lim_{T\to1}(1-T)^dG(T),
\]

and both limits are finite. Positivity and nonvanishing are not conclusions of this lemma.

**Proof.** Absorb \(U^{-1}\) into P and write the Taylor expansion in \(h=X-1\) and \(y=1-T\) as a sum of homogeneous polynomials \(P_k(h,y)\). If \(r\geq d\), regularity forces all \(P_k\) with \(k<r-d\) to vanish: a first nonzero such polynomial would produce a nonzero coefficient \(P_k(1,s)/\prod_j(b_js-a_j)\) of a negative power of h. A homogeneous polynomial vanishing at every \((1,s)\) is zero. The constant term is therefore

\[
F(s)=\frac{P_{r-d}(1,s)}{\prod_j(b_js-a_j)}.
\]

Its numerator has degree at most \(r-d\). Both limits in the lemma equal \(P_{r-d}(0,1)/\prod_jb_j\). If \(r<d\), the normalized constant term and both leading limits are zero. This proves the statement. Replacing \(h^d\) by \((1-X^{-1})^d\) changes nothing, since their quotient is a unit with constant term 1. ∎

The lemma applies termwise to suitable Euler-weighted Denef formulae; the common finite coefficient can still vanish or have either sign. Establishing the required nonvertical, regular representation in the general setting, and proving a positive nonzero coefficient, are not accomplished here.

For example, the artificial rational family

\[
W(X,T)=1+\frac{(X-1)T}{(1-XT)^2}
\]

has constant coefficient 1 and nonnegative integral coefficients at every integer \(X=q\geq2\). At normalization d=1 its topological limit is \((s-1)^{-2}\), so its rank-one leading value is zero, while its reduced function is 1. It is not asserted to arise from an algebra. It shows that rationality and nonnegative local coefficients alone cannot establish the exact degree or positivity.

The requirement excluding vertical denominator factors also matters: \(W(X,T)=1/[(X-1)(1-T)]\) at normalization d=2 gives F(s)=1/s, but W(1,T) is undefined. This is an obstruction to a formal interchange of limits, not an algebraic counterexample.

## 6. Scope controls and the remaining obstruction

1. **Nonuniformity is real already in rank two.** Take \(e_1^2=e_2\), \(e_2^2=2e_1\), and both mixed products zero. Then \(f=x^3-2y^3\). It has one projective root over \(\mathbb F_5\) and none over \(\mathbb F_7\), but three distinct geometric roots over \(\mathbb C\). The topological formula uses three. Substituting a single prime's root count into a purported uniform formula gives a wrong answer.
2. **Squares alone cease to suffice in rank three.** In the Heisenberg Lie algebra, all squares vanish, but \(B=\langle e_1,e_2,2e_3\rangle\) is not a subalgebra because \([e_1,e_2]=e_3\notin B\). The rank-two cyclic-quotient parametrization is essential; there is no claimed rank-three extension.
3. **Special bases do not prove the general case.** [Evseev, *Reduced zeta functions of Lie algebras*, proposition 4.1](https://arxiv.org/pdf/0710.0387) gives a cone expression under its nice-and-simple-basis hypotheses. This is valuable special-family evidence for the reduced invariant, not a universal topological argument.
4. **Ideal zeta functions stay separate.** The cited [Voll, *Ideal zeta functions associated to a family of class-2-nilpotent Lie rings*, §3.4](https://arxiv.org/pdf/1902.01794) proves a coincidence for its ideal functions via explicit Igusa-function formulas. No conversion of that result into an unrestricted subalgebra theorem is used here.
5. **Origin and infinity differ.** Even for \(f=0\), \(\lim_{s\to0}s^2/[s(s-1)]=0\), whereas the required infinity limit is 1.

The residual universal task is to control arbitrary finite-free algebras of rank at least three, including their nonuniform motivic/Denef contributions, and prove that the correct leading values exist, are equal, and are positive. Neither a general proof nor an exact-scope counterexample is supplied.

## 7. Prior-work and verification boundary

This calculation is independently derived, but independence is not novelty. The primary repository abstract for [Robert Snocken's 2014 thesis, *Zeta functions of groups and rings*](https://eprints.soton.ac.uk/372833/) explicitly reports formulas for subring zeta functions of two-dimensional rings in terms of Igusa integrals. The thesis PDF retrieval was blocked in this investigation, so its detailed overlap with this rank-two formula has not been determined. That is a substantive reason to withhold any novelty claim. Bounded searches also do not establish the absence of a later general resolution.

The original investigation used an authored checker, which is not distributed in this edition. It compared direct Hermite-normal-form subalgebra tests against the independent cubic/projective-line count, checked all four symbolic specializations, and exercised nonuniform, degenerate, nonassociative, origin/infinity, and rank-three controls. Its test failures used explicit exceptions, remaining active under Python's -O and -OO modes. Historical receipt identities and scope are recorded in VERIFICATION.json. Finite checks supplement the written proof; they do not prove a universal statement.
