# Logarithmic density for finitely many affine residue patterns

Research note, 10 October 2026.

## Scope and conclusion

Let \(1\le n_1<n_2<\cdots\), choose canonical residues \(0\le a_i<n_i\), and put
\[
 B_i=\{m\ge n_i:m\equiv a_i\pmod {n_i}\},\qquad
 A=\mathbb N\setminus\bigcup_i B_i.
\]
Erdős asked whether \(A\) always has logarithmic density [E95, §I.4]. The general singleton problem is **not resolved here**.

This note proves a sufficient condition allowing noncoprime moduli, divergent reciprocal sums, and unbounded residues. The proof uses the classical Davenport–Erdős theorem, not a proposed resolution of the general problem. No claim of literature novelty is made.

**Theorem 1.** Suppose there is a finite collection of integer triples
\[
 \mathcal T\subseteq\{(q,p,c):q\ge1,\ p,c\in\mathbb Z\}
\]
such that, except for an index set \(J\) with \(\sum_{i\in J}1/n_i<\infty\), every \(i\) satisfies
\[
 q a_i=p n_i+c                                                    \tag{1}
\]
for some \((q,p,c)\in\mathcal T\). Then
\[
 \lim_{X\to\infty}\frac1{\log X}\sum_{\substack{m\le X\\m\in A}}\frac1m
 =\lim_{K\to\infty}d\!\left(\mathbb N\setminus
                 \bigcup_{n_i\le K}B_i\right).                  \tag{2}
\]
Here \(d\) denotes natural density; each finite sieve in (2) is eventually periodic. The limit on the right exists by monotonicity. Natural density of the infinite sieve is not asserted.

A readily checked sufficient hypothesis is that, outside the summable exceptional set, each \(a_i\) lies within a fixed additive distance of one of finitely many fixed rational multiples of \(n_i\). Indeed, after clearing each rational denominator, the bounded integer remainder has only finitely many values.

Consequently the theorem includes:

- residues drawn from a fixed finite set;
- residues at bounded distance from \(n_i\);
- any fixed finite collection of rational values of \(a_i/n_i\);
- conditions \(q a_i\equiv c\pmod {n_i}\) for finitely many fixed pairs \((q,c)\), with no assumption that \(q\) and \(n_i\) are coprime.

For the last assertion, write \(q a_i=p_i n_i+c\). Since \(0\le a_i<n_i\), the integers \(p_i\) range over a finite set for fixed \(q,c\).

## Logarithmic approximation and the classical input

Write
\[
 H_X(S)=\sum_{\substack{m\le X\\m\in S}}\frac1m,\qquad
 \overline\delta(S)=\limsup_{X\to\infty}\frac{H_X(S)}{\log X}.
\]
We use the following form of Davenport–Erdős [DE36, Theorem 1(a), with the definition of its constant on p.147]. For arbitrary \(D\subseteq\mathbb N\), let
\[
 M(D)=\{dk:d\in D,\ k\ge1\},\qquad D_K=D\cap[1,K].
\]
Then \(M(D)\) has logarithmic density and
\[
 \delta(M(D))=\lim_{K\to\infty}d(M(D_K)).                       \tag{3}
\]
In particular,
\[
 \overline\delta(M(D)\setminus M(D_K))\longrightarrow0.         \tag{4}
\]
The difference in (4) actually has a logarithmic density for each fixed \(K\), since \(M(D_K)\subseteq M(D)\).

Two elementary consequences will be useful.

**Lemma 2 (primitive sets).** A set with no two distinct elements dividing one another has upper logarithmic density zero. More generally, the same conclusion holds when lengths of strict divisibility chains in the set have a finite upper bound.

*Proof.* If \(P\) is primitive, then
\[
 P\setminus[1,K]\subseteq M(P)\setminus M(P_K).
\]
Apply (4). For a set with chain length at most \(h\), assign each element the maximal length of a chain ending there. The maximum exists because an integer has finitely many divisors. Each of the at most \(h\) level sets is primitive. Their finite union has upper logarithmic density zero. ∎

**Lemma 3 (affine pullback).** Fix integers \(b\ge1\) and \(c\). If \(T\subseteq\mathbb N\), then
\[
 \overline\delta\{m\ge1:bm-c>0,\ bm-c\in T\}
       \le b\,\overline\delta(T).                              \tag{5}
\]
Thus a vanishing logarithmic approximation error stays vanishing under a fixed affine pullback.

*Proof.* For \(t=bm-c>0\), after discarding finitely many small terms,
\[
 \frac1m=\frac b{t+c}=\frac b t+O_{b,c}(t^{-2}).
\]
Sum over the injective image \(t\in T\), bounded above by \(bX+|c|\), and use \(\log(bX+|c|)/\log X\to1\). ∎

We will repeatedly use the following elementary approximation principle. If \(S_K\subseteq S\) increase, every \(S_K\) has logarithmic density, and \(\overline\delta(S\setminus S_K)\to0\), then \(S\) has logarithmic density equal to \(\lim_K\delta(S_K)\). This follows directly by bounding the liminf from below by \(\delta(S_K)\) and the limsup from above by \(\delta(S_K)+\overline\delta(S\setminus S_K)\). Finite unions preserve this approximation property, by the union bound on their differences.

## Restricted multiples

For integers \(q\ge1,p\), and \(D\subseteq\mathbb N\), define
\[
 V_{p,q}(D)=\{dk:d\in D,\ k\ge1,\ k\equiv p\pmod q\}.
\]

**Lemma 4.** These restricted multiples satisfy
\[
 \overline\delta\bigl(V_{p,q}(D)\setminus V_{p,q}(D_K)\bigr)
       \longrightarrow0.                                     \tag{6}
\]
In particular, they have logarithmic density equal to the increasing limit of the densities of their finite unions of arithmetic progressions.

*Proof.* First reduce to \((p,q)=1\). With \(g=(p,q)\), the exact identity is
\[
 V_{p,q}(D)=g\,V_{p/g,q/g}(D).
\]
This is also valid for \(p=0\), when \(g=q\), and for modulus one. Scaling a set by \(g\) scales its upper logarithmic density by \(1/g\).

Assume now that \((p,q)=1\). Factor each positive integer uniquely as \(x=su\), where all prime factors of \(s\) divide \(q\), and \((u,q)=1\). Fix such an \(s\) and a unit residue \(r\pmod q\). Put
\[
 D_{s,r}=\{v\ge1:sv\in D,\ (v,q)=1,\ v\equiv rp^{-1}\pmod q\}.
\]
For \(u\equiv r\pmod q\), the exact equivalence is
\[
 su\in V_{p,q}(D)\quad\Longleftrightarrow\quad u\in M(D_{s,r}). \tag{7}
\]
Indeed a quotient congruent to the unit \(p\) has no prime factor in common with \(q\), so its divisor has precisely the same \(q\)-supported part \(s\) as \(su\). Writing that divisor as \(sv\), the remaining condition is \(v\mid u\) and \(u/v\equiv p\pmod q\), equivalent to the residue condition on \(v\).

Replacing \(D\) by \(D_K\) in (7) replaces \(D_{s,r}\) by \(D_{s,r}\cap[1,K/s]\). Consequently the upper logarithmic density of the difference on this stratum is at most
\[
 \frac1s\,\overline\delta\bigl(M(D_{s,r})\setminus
             M(D_{s,r}\cap[1,K/s])\bigr),
\]
which tends to zero by (4).

It remains to justify passing from finitely many strata to all of them. Fix \(L\ge1\) and retain only integers with \(v_\ell(x)<L\) for every prime \(\ell\mid q\). There are finitely many retained \(s\)'s and \(r\)'s. The omitted integers lie in
\[
 \bigcup_{\ell\mid q}\ell^L\mathbb N,
\]
whose upper logarithmic density is at most \(\sum_{\ell\mid q}\ell^{-L}\). For fixed \(L\), take \(K\to\infty\), then take \(L\to\infty\). This proves (6). For \(q=1\) the exceptional union is empty and there is only one stratum. ∎

## The activation cutoff

The next step is necessary: simply deleting the activation condition would be an invalid reduction for arbitrary residues.

Fix one triple \((q,p,c)\), and let \(D\) be any set of moduli for which the selected canonical residue \(a_n\) satisfies \(qa_n=pn+c\). Define
\[
 U=\{m\ge1:\exists n\in D,\ m\equiv a_n\pmod n\},\qquad
 B=\{m\ge1:\exists n\in D,\ n\le m,\ m\equiv a_n\pmod n\}.
\]

**Lemma 5.** The cutoff defect \(U\setminus B\) has upper logarithmic density zero.

*Proof.* Ignore the finitely many \(m\) for which \(t=qm-c\) is not positive or is less than \(\max(1,|c|)\). Set
\[
 E=\{qm-c:m\in U\setminus B,\ qm-c\ge\max(1,|c|)\}.
\]
Every \(t\in E\) has a witness
\[
 t=nk,\qquad n\in D,\quad k\ge1,\quad k\equiv p\pmod q.       \tag{8}
\]
Suppose \(t_1,t_2\in E\), \(t_2=h t_1\), \(h\equiv1\pmod q\), and \(h\ge2q\). Take a witness \(n,k\) for \(t_1\). The same \(n\) witnesses the untruncated congruence for \(t_2\), since \(hk\equiv p\pmod q\). Furthermore,
\[
 m_2=\frac{t_2+c}{q}\ge\frac{2q t_1-|c|}{q}\ge t_1\ge n.
\]
Thus that modulus is active at \(m_2\), contradicting \(t_2\in E\).

Now partition \(E\) by its exact \(q\)-supported factor \(s\) and the unit residue \(r\pmod q\) of \(t/s\), as in Lemma 4. If two elements in the same stratum are comparable under divisibility, their quotient is \(1\pmod q\). A strict divisibility chain of length \(h_0+1\), where \(h_0=\lceil\log_2(2q)\rceil\), has endpoint quotient at least \(2^{h_0}\ge2q\), which was just ruled out. Every stratum therefore has chain length at most \(h_0\) and upper logarithmic density zero by Lemma 2.

As in Lemma 4, restricting all valuations at primes dividing \(q\) to be less than \(L\) leaves finitely many strata; the omitted part has upper logarithmic density at most \(\sum_{\ell\mid q}\ell^{-L}\). Letting \(L\to\infty\) gives \(\overline\delta(E)=0\). Lemma 3 then gives \(\overline\delta(U\setminus B)=0\). ∎

## Proof of Theorem 1

Assign every nonexceptional modulus to one of its finitely many valid triples. First consider one assigned family \(D\). For all sufficiently large \(m\),
\[
 m\in U\quad\Longleftrightarrow\quad qm-c\in V_{p,q}(D).       \tag{9}
\]
To check (9), write \(m=a_n+nt\), so that \(qm-c=n(p+qt)\). Positivity of \(qm-c\) makes the quotient positive. Conversely, if \(qm-c=nk\) and \(k\equiv p\pmod q\), subtract \(qa_n=pn+c\) to obtain \(m-a_n=n(k-p)/q\).

Lemmas 3 and 4 show that \(U\) is approximated in upper logarithmic density by its finite-modulus subfamilies \(U_K\). The finitely many small values omitted in (9) do not affect this assertion. Lemma 5 shows \(U\setminus B\) has upper logarithmic density zero. More directly, because \(B\subseteq U\) and \(U_K\setminus B_K\) is finite for fixed \(K\),
\[
 B\setminus B_K\subseteq (U\setminus U_K)\cup(U_K\setminus B_K).
\]
Thus \(B\) also has the finite-modulus logarithmic approximation property. Its density agrees with that of \(U\), and with the increasing limit of the densities of \(B_K\). Combining the finitely many assigned families preserves the approximation property.

For exceptional indices, the activation cutoff gives the exact bound
\[
 |B_i\cap[1,X]|\le X/n_i.
\]
Indeed its elements have the form \(a_i+tn_i\) with \(t\ge1\). Consequently the upper natural density, and hence upper logarithmic density, of the union over exceptional \(n_i>K\) is at most \(\sum_{i\in J,n_i>K}1/n_i\), which tends to zero. Adding this family preserves finite-modulus logarithmic approximation. Taking complements proves (2). ∎

**Remark on logical economy.** Finite-modulus logarithmic approximation for \(B\), sufficient for Theorem 1, already follows from that for \(U\) and the displayed inclusion. Lemma 5 additionally proves the more precise statement that removing activation altogether in these finite-template families does not change the logarithmic density. Its proof explicitly checks why the cutoff is harmless in this class, rather than assuming that it is harmless in general.

## Arbitrary finite activation thresholds in the patterned class

**Corollary 6.** If every modulus belongs to one of the finite families (1), with no exceptional family, replace \(m\ge n_i\) by \(m\ge T_i\), where each \(T_i\) is any finite positive number. The survivor set still has logarithmic density equal to the same finite-periodic limit (2). In particular the density is independent of these thresholds within this class.

*Proof.* Let \(U\) be the full untruncated forbidden union and \(B_T\) its thresholded version. The proof of Lemma 4 and (9) gives \(\overline\delta(U\setminus U_K)\to0\). For fixed \(K\), \(U_K\setminus (B_T)_K\) is finite, regardless of the sizes of the finitely many thresholds. Therefore
\[
 B_T\setminus (B_T)_K\subseteq(U\setminus U_K)
                      \cup(U_K\setminus(B_T)_K)
\]
has vanishing upper logarithmic density as \(K\to\infty\). All the finite approximants have the same natural densities as \(U_K\). The approximation principle completes the proof. ∎

This corollary is a consequence of the specific finite-template hypothesis. It is not an assertion that activation can be removed in the unrestricted Erdős problem.

## An explicit nonsummable noncoprime example

Let the moduli be \(n=2\ell\), with \(\ell\) running through all odd primes, and select \(a_n=\ell\). These satisfy the single identity \(2a_n=n\). Their reciprocal sum diverges, and every pair of moduli has gcd two. Both \(a_n\) and \(n-a_n\) are unbounded.

The forbidden integers are exactly the odd composite integers: an active congruence gives \(m=\ell k\) with odd \(k\ge3\); conversely any odd composite has an odd prime divisor \(\ell\le m/3\). Hence the survivor set is the even integers together with the odd primes and 1, and its natural and logarithmic densities are \(1/2\). More generally, the theorem applies to arbitrary subfamilies \(n=2d,a_n=d\), with no coprimality or reciprocal-summability restriction on \(d\).

## What remains open in this attempt

For arbitrary residues there need not be finitely many identities (1), even after discarding a reciprocal-summable family. In particular, residues following an irrational proportional slope cannot be covered eventually by fixed rational affine patterns. The fixed quotient modulus used in Lemmas 4 and 5 is then unavailable. This note supplies no estimate replacing that finite-stratum reduction, and no counterexample to the unrestricted singleton problem.

The two elementary positive cases and a conditional first-kill-sieve program are recorded in [C26]. Its missing uniform estimate is not assumed here. The proposed negative result [W26] permits multiple residues per modulus and explicitly excludes the singleton conclusion; it is not used in any proof above. The summability result also appears as Theorem 3.26 in the full dissertation [A26]; the numbering differs from the related preprint cited by [W26].

## References

- [DE36] H. Davenport and P. Erdős, *On sequences of positive integers*, Acta Arithmetica 2 (1936), 147–151. Theorem 1(a), together with the finite-union definition of its constant. https://users.renyi.hu/~p_erdos/1936-04.pdf ; https://doi.org/10.4064/aa-2-1-147-151
- [E95] P. Erdős, *Some of my favourite problems in number theory, combinatorics, and geometry*, Resenhas 2 (1995), 165–186, §I.4, printed preprint p.3. https://www.ime.usp.br/~yoshi/resenhas/abstracts/Erdos.pdf
- [A26] F. Araújo, *Erdős Sieves and Dynamics*, Paderborn University dissertation, title page January 2026, available PDF generated May 2026. Theorem 3.24 and Theorem 3.26, printed pp.40 and 42. https://digital.ub.uni-paderborn.de/hs/download/pdf/8306542
- [C26] P. Chojecki, *Truncated Congruence Sieves and Erdős Problem 25*, 19 March 2026. Partial and conditional results; no full-resolution claim. https://www.ulam.ai/research/erdos25.pdf
- [W26] S. Wang, *A Proposed Solution to Erdős Problem 486*, Multiscalar Intelligence, 2026. Multi-residue proposed result; §5 distinguishes the singleton problem. https://multiscalar.ai/results/erdos-486/paper.pdf
