# Blocks of symmetric-group centralizers: a p-subgroup case and the remaining gap

**30001767 / OWR-5149-003. Scoped partial result; the unrestricted question remains unresolved.**

For every $n\ge2$ and every field $k$ of characteristic two, the block idempotents of

$$C_{kS_n}(kS_2)=(kS_n)^{S_2}$$

are exactly the block idempotents of $kS_n$. Since $kS_2$ has just one block, this proves the required product description in the entire $\ell=2$, $p=2$ subclass. The argument is an elementary fixed-point theorem for arbitrary finite $p$-groups acting on finite-dimensional algebras. No historical-priority claim is made.

The same method does not extend to arbitrary $S_\ell$. We give an explicit algebraic control showing the failed step and retain the full original conjecture as **unsolved**. Separate adversarial review is pending; no human peer review is claimed.

## 1. Exact source and credited known results

Harald Ellers's contribution, jointly with John Murray, in [Oberwolfach Report 21/2011](https://ems.press/content/serial-article-files/46337), printed pp.1183–1184, fixes a sufficiently large $p$-modular system with residue field $k$ of characteristic $p$. The subgroup $S_\ell\le S_n$ consists of permutations fixing each letter larger than $\ell$. Its algebra is

$$C=C_{kS_n}(kS_\ell)=\{a\in kS_n:ah=ha\text{ for every }h\in S_\ell\}.$$

A block idempotent is a nonzero primitive **central** idempotent. The source asks whether every block idempotent of $C$ has the form $ef$, with $e$ a block idempotent of $kS_n$ and $f$ a block idempotent of $kS_\ell$.

For each pair, $ef$ is a central idempotent of $C$, because $C$ commutes with the whole subalgebra $kS_\ell$. These products are mutually orthogonal and sum to one. Thus the exact conjecture says that each **nonzero** $ef$ is already primitive in $Z(C)$; zero products are not blocks. It is not a statement about arbitrary primitive idempotents, or about equality of full centers.

The following prior results must not be counted as new work.

- The original report already records the result for the cases $n-\ell\le3$. The later Ellers–Murray paper on centralizers and degenerate affine Hecke algebras, [DOI](https://doi.org/10.1080/00927872.2012.731622), develops this classification and further families.
- Fayers–Putignano, *Ribbon blocks for centraliser algebras of symmetric groups*, Journal of Algebra **685** (2026), 271–312, [DOI](https://doi.org/10.1016/j.jalgebra.2025.07.042), still formulates the unrestricted assertion as Conjecture 2.5. Its [complete author manuscript](https://webspace.maths.qmul.ac.uk/m.fayers/papers/ribbonblocks.pdf) proves the generalized ribbon and belt families, characterized by no repeated entries in the skew partition's $p$-content. This is an important positive result, not the entire conjecture. The author manuscript and publication metadata were checked; a line-by-line comparison with the final journal PDF was not performed.
- Danz–Ellers–Murray, *The centralizer of a subgroup in a group algebra*, Proceedings of the Edinburgh Mathematical Society **56** (2013), 49–56, [full published text](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/18B69524BB77FC4B356AFE1A2471C310/S0013091512000077a.pdf/the-centralizer-of-a-subgroup-in-a-group-algebra.pdf), gives a counterexample for $G=S_6$, $H=A_4$, $p=5$. This is outside the source's naturally embedded symmetric-subgroup case. Its Proposition 3 supplies a positive normal-$p$-subgroup case. The argument below uses a different elementary fixed-vector observation and needs no normality assumption; no claim of priority or criticism of that paper is intended. The paper also reports computations of the stronger center assertion for natural $S_\ell\le S_n$ with $n\le8$, so repeating those small cases would not establish novelty.

No unrestricted primary resolution was located in the bounded current-literature search. The semisimple case $p>n$, the trivial subgroup case, and $\ell=n$ are already elementary known cases and are not offered as the open target.

## 2. A fixed-vector lemma

### Lemma 1

Let $P$ be a finite $p$-group and $M\ne0$ a finite-dimensional vector space over a field $k$ of characteristic $p$, with a linear $P$-action. Then $M^P\ne0$.

### Proof

Induct on $|P|$. The trivial group is immediate. Otherwise the center of $P$ has an element $z$ of order $p$. On $M$,

$$(z-1)^p=z^p-1=0.$$

Therefore $N=\ker(z-1)$ is nonzero. Because $z$ is central, $N$ is $P$-stable, and the action on $N$ factors through the smaller $p$-group $P/\langle z\rangle$. The induction hypothesis supplies a nonzero vector of $N$ fixed by that quotient, hence fixed by $P$. $\square$

This proof works over any characteristic-$p$ field. It does not average over $P$ or divide by its order.

## 3. Central idempotents of a fixed algebra

### Theorem 2

Let $A$ be a finite-dimensional unital $k$-algebra in characteristic $p$, and let a finite $p$-group $P$ act on $A$ by $k$-algebra automorphisms. Then

$$\operatorname{Idem} Z(A^P)
=\operatorname{Idem}\bigl(Z(A)^P\bigr).\tag{1}$$

In words: every central idempotent of the fixed algebra is already central in the ambient algebra, and is necessarily $P$-invariant. The primitive central idempotents of $A^P$ are the sums over $P$-orbits of primitive central idempotents of $A$.

### Proof

Let $e\in Z(A^P)$ with $e^2=e$. Since $e\in A^P$, both Peirce spaces

$$M=eA(1-e),\qquad N=(1-e)Ae$$

are stable under $P$. If $M\ne0$, Lemma 1 gives $0\ne m\in M^P\subset A^P$. But

$$em=m,\qquad me=0,$$

contradicting $e\in Z(A^P)$. Thus $M=0$. The same argument gives $N=0$. For any $a\in A$ it follows that

$$ea=eae=ae,$$

so $e\in Z(A)$. This proves one inclusion in (1); the other is immediate.

A finite-dimensional algebra has finitely many primitive central idempotents, and every central idempotent is a sum of a subset of them. Automorphisms permute this finite set. Its invariant subsets are exactly unions of $P$-orbits, and the nonempty minimal invariant subsets are individual orbits. Equation (1) therefore identifies the primitive central idempotents of $A^P$ with the stated orbit sums. $\square$

### Corollary 3: inner actions

If the action of $P$ is by inner automorphisms, every element of $Z(A)$ is fixed. Therefore $A$ and $A^P$ have exactly the same block idempotents.

In particular, for **any finite group** $G$ and any $p$-subgroup $P\le G$, the algebras $kG$ and $(kG)^P$ have exactly the same block idempotents. The subgroup $P$ need not be normal in $G$.

The conclusion concerns central idempotents, not an equality $Z(A^P)=Z(A)$. It also does not say that every primitive idempotent of $A^P$ is central in $A$.

## 4. Application to the original symmetric-subgroup family

Take $p=2$, $P=S_2=\langle(12)\rangle\le S_n$, and $A=kS_n$. Conjugation gives the inner action from Corollary 3, so the centralizer has exactly the ambient block idempotents.

Moreover,

$$kS_2\cong k[t]/(t^2-1)=k[t]/((t-1)^2)$$

is local. Its only block idempotent is $f=1$. Thus each centralizer block idempotent is exactly $e=e\cdot f$, with $e$ an ambient block idempotent. This is the required source conclusion for every $n\ge2$ in this subclass, including the nonnormal embeddings when $n\ge3$.

The theorem proves a statement for all $n$, not a conclusion extrapolated from the finite controls. Apart from trivial symmetric groups, $S_2$ in characteristic two is the only naturally embedded $S_\ell$ that is a $p$-group. For $\ell\ge3$, the order $\ell!$ has at least two different prime divisors, so Theorem 2 cannot directly handle the remaining cases.

## 5. An exact control against extending the fixed-vector step

A nonzero module for a general finite group in characteristic $p$ need not have a fixed vector. For example, in characteristic three the sign representation of $S_3$ has no nonzero invariant vector. Accordingly, the Peirce-space proof cannot simply replace $P$ by an arbitrary $S_\ell$.

The failure is visible inside a small algebra. Let $k$ have characteristic three, set $V=k\oplus\mathrm{sgn}$ as an $S_3$-module, and let $A=\operatorname{End}_k(V)=M_2(k)$. A transposition acts on $V$ by $\operatorname{diag}(1,-1)$, while a three-cycle acts trivially. Thus

$$A^{S_3}=\{\operatorname{diag}(a,b):a,b\in k\}\cong k\times k.$$

It has the noncentral-in-$A$ central idempotents $E_{11}$ and $E_{22}$. The Peirce space $E_{11}AE_{22}=kE_{12}$ is a sign module, so its fixed subspace is zero rather than nonzero.

One can also check that $kS_3$ itself has just one block in characteristic three. Write $T$ for the sum of its three transpositions and $C$ for the sum of its two three-cycles. The center has basis $1,T,C$, and

$$T^2=0,\qquad (1+C)^2=0,\qquad T(1+C)=0.$$

Hence $Z(kS_3)=k\,1\oplus J$ with $J=\operatorname{span}\{T,1+C\}$ and $J^2=0$, so this center is local. Merely knowing that the acting group algebra has a single block is therefore insufficient for the fixed-vector proof.

This is **not a counterexample to the source conjecture**: $A=M_2(k)$ is not the prescribed full symmetric-group algebra, and the displayed representation of $S_3$ is not faithful. It diagnoses an invalid generalization of the method. The published $S_6/A_4$ counterexample likewise must not be substituted for a naturally embedded symmetric-subgroup example.

## 6. Exact remaining gap and validation scope

For a general naturally embedded $S_\ell$, the conjecture requires every nonzero corner $efC$ to be indecomposable. The central product decomposition exists automatically; its primitivity is the missing step. The fixed-vector argument proves that step only in the $p$-group case above. The current ribbon/belt theorem treats different specified families, but does not remove the repeated-residue cases from the open problem.

Two approaches are recorded: the $p$-group fixed-algebra reduction, which yields a complete scoped theorem, and its attempted extension from subgroup structure or coarse block data, which fails at the explicit invariant-vector obstruction. No third proof family is pursued without a new mechanism.

`python verify.py` supplies exact small-algebra controls, including nonnormal $p$-subgroups, central versus merely primitive idempotents, an external action permuting blocks, and the characteristic-three control. These tests support the written all-group theorem and do not certify the full symmetric-group conjecture. The original status remains **unsolved, 2/5**, with no discovery-priority claim.
