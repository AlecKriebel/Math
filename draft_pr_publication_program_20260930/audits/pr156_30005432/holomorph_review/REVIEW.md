# Independent holomorph adversarial review of PR156

**Verdict: mathematical PASS.** No defect was found in the infinite left-brace
counterexample or in its stated property-(s) classification. This review establishes
the mathematical gate only; it does not establish novelty, priority, external
source accuracy, or publication readiness.

The reviewed original HEAD is `aec31742f3f26c5b1e533404da57539d17dc94a1`.
The original candidate has SHA256
`cb127cdc60740596a6e08bd0cb1cfb894b1d24ac8bc56a7338a885798b0a33ae`.
The original source record has SHA256
`a2094cd87420bdd0086f9a48d8829f529e57d6bbad9a5ad03940ad2cf7ccdc04`.
Their bytes were preserved. The reviewer read those two original contents and the
parent original-file manifest for identity checks. No historical review, author
checker, sibling findings, or original research log was read. An independent
first assessment was recorded before inspecting the parent manifest. All writes
were confined to this `holomorph_review` directory. No external communication or
repository, index, reference, pull-request, remote, release, Zenodo, or GWS mutation
was performed.

## 1. Exact target and success criterion

For a skew left brace, define

\[
a*b=-a+a\circ b-b,
\quad R_x=\{b:x*b=0\},
\quad L_x=\{b:b*x=0\}.
\]

The exact supplied question asks whether the elements for which both

\[
[(B,+):R_x\cap C_x^+],\qquad
[(B,\circ):L_x\cap C_x^\circ]
\]

are finite form an ideal. No finiteness or two-sided assumption is present in the
supplied exact statement. The counterexample succeeds if its two group laws and
left-brace law hold for all integer inputs, its claimed witness has both finite
indices, and an additive combination of such witnesses has an infinite required
index. Finite quotients or finite computational windows cannot alone establish
the last condition.

## 2. Independent construction through a regular holomorph subgroup

Let \(A=\mathbb Z\oplus C_4\) with its coordinatewise additive law. For the
canonical representatives \(c=0,1,2,3\), set

\[
e(c)=(-1)^{\lfloor c/2\rfloor},\qquad q(c)=(-1)^c,\qquad
D_c(m,d)=(e(c)m,q(c)d).
\]

Both signs act by additive automorphisms. This uses the integer first factor,
including negative integers, without truncation. In the holomorph
\(\operatorname{Hol}(A)=A\rtimes\operatorname{Aut}(A)\), an element
\((a,D)\) acts by \(t\mapsto a+D(t)\), and composition is

\[
(a,D)(b,E)=(a+D(b),DE).
\]

Consider the graph

\[
\mathcal R=\{((n,c),D_c):n\in\mathbb Z,\ c\in C_4\}.
\]

Put \(c\diamond d=c+q(c)d\pmod4\). This operation agrees with
\(c+d+2cd\pmod4\), since \(q(c)\equiv1+2c\pmod4\). Its exact four-state
description is XOR on the two bits: if \(c=u+2v\), \(d=s+2t\), then

\[
c\diamond d=(u\mathbin{\mathrm{xor}}s)
             +2(v\mathbin{\mathrm{xor}}t).
\]

The equality is an exhaustive finite identity for the sixteen pairs in
\(C_4^2\), also checked independently in `CHECKER.py`. Therefore

\[
e(c\diamond d)=e(c)e(d),\qquad
q(c\diamond d)=q(c)q(d),\qquad D_{c\diamond d}=D_cD_d.
\]

Hence \(\mathcal R\) is closed under holomorph multiplication. It contains
the identity \(((0,0),I)\). Because \(D_c^{-1}=D_c\) and
\(-q(c)c=c\pmod4\), its inverse formula is

\[
((n,c),D_c)^{-1}=((-e(c)n,c),D_c),
\]

so it is a subgroup. Its action is regular: evaluation at zero sends its unique
element \(((n,c),D_c)\) to \((n,c)\), bijectively. Transporting its group
law to \(A\) consequently yields

\[
(n,c)\circ(m,d)=(n+e(c)m,c+q(c)d)
=(n+e(c)m,c+d+2cd\pmod4).
\]

This is exactly the submitted operation. Associativity follows from composition
in the holomorph, without invoking a semidirect-brace theorem. The identity is
\((0,0)\), and the inverse is \((-e(c)n,c)\). The transported lambda map is

\[
\lambda_{(n,c)}=D_c.
\]

As an additive automorphism it gives the left law universally:

\[
a\circ(b+t)=a+D_c(b+t)=a+D_c(b)+D_c(t)
=(a\circ b)-a+(a\circ t).
\]

Thus the infinite construction is a left brace with abelian additive group,
and in particular a skew left brace. No finite quotient is used in this proof.

## 3. Exact stabilizer and centralizer kernels for every element

Write \(x=(n,c)\), \(g=(m,d)\). The regular-subgroup automorphism gives

\[
x*g=(D_c-I)g=((e(c)-1)m,2cd\pmod4).
\]

Because addition is abelian, \(C_x^+=B\). Integer torsion-freeness gives

| c | Exact right fixed group \(R_x\) | First index |
|---|---|---|
| 0 | \(\mathbb Z\times C_4\) | 1 |
| 1 | \(\mathbb Z\times\{0,2\}\) | 2 |
| 2 | \(\{0\}\times C_4\) | infinite |
| 3 | \(\{0\}\times\{0,2\}\) | infinite |

This is independent of \(n\). For \(c=2,3\), the integer equation is
\(-2m=0\), whose only solution is \(m=0\). The additive cosets represented
by \((r,0)\), for \(r\in\mathbb Z\), are pairwise distinct: the difference
\((r-s,0)\) belongs to \(R_x\) only if \(r=s\). This is the infinite-index
certificate, rather than an extrapolation from computed examples.

The left fixed condition is

\[
g*x=0\iff(e(d)-1)n=0\text{ and }2dc=0\pmod4.
\]

The finite group operation \(\diamond\) is commutative, so comparing
\(g\circ x\) and \(x\circ g\) gives the full multiplicative centralizer
equation

\[
g\in C_x^\circ\iff(1-e(c))m=(1-e(d))n.
\]

Intersecting these conditions, without dropping either equation, yields

\[
K_x:=L_x\cap C_x^\circ
=\{(m,d):(1-e(c))m=0,\ (1-e(d))n=0,\ 2dc=0\pmod4\}.
\tag{*}
\]

To classify the finite residue restriction, define

\[
E_n=\begin{cases}C_4&n=0,\\\{0,1\}&n\ne0,\end{cases}
\qquad
P_c=\begin{cases}C_4&c\text{ even},\\\{0,2\}&c\text{ odd},\end{cases}
\qquad T_{n,c}=E_n\cap P_c.
\]

Equation (*) says that \(K_x=\mathbb Z\times T_{n,c}\) when \(c=0,1\),
and \(K_x=\{0\}\times T_{n,c}\) when \(c=2,3\). In the former cases,
\(T_{n,c}\) is a subgroup of the Klein four quotient and \(K_x\) is its
inverse image under the surjective homomorphism \((m,d)\mapsto d\). Its
index is \(4/|T_{n,c}|\). In the latter cases, \(K_x\) has only
\(|T_{n,c}|\) elements; its index in the infinite group is infinite. Equally,
the multiplicative cosets represented by \((r,0)\) are pairwise distinct,
since \((r,0)^{-1}_{\circ}\circ(s,0)=(s-r,0)\) lies in \(K_x\) only
when \(r=s\).

The complete result, including the submitted and previously unstated second
indices for \(c=2,3\), is:

| n | c | \(K_x\) | First index | Second index |
|---|---|---|---|---|
| 0 | 0 | \(\mathbb Z\times C_4\) | 1 | 1 |
| nonzero | 0 | \(\mathbb Z\times\{0,1\}\) | 1 | 2 |
| 0 | 1 | \(\mathbb Z\times\{0,2\}\) | 2 | 2 |
| nonzero | 1 | \(\mathbb Z\times\{0\}\) | 2 | 4 |
| 0 | 2 | \(\{0\}\times C_4\) | infinite | infinite |
| nonzero | 2 | \(\{0\}\times\{0,1\}\) | infinite | infinite |
| 0 | 3 | \(\{0\}\times\{0,2\}\) | infinite | infinite |
| nonzero | 3 | \(\{(0,0)\}\) | infinite | infinite |

Here “nonzero” includes every negative integer. The only integer distinction is
whether \(2n=0\), which is equivalent to \(n=0\) in \(\mathbb Z\).
Thus the property-(s) set is exactly

\[
\mathcal S=\mathbb Z\times\{0,1\}.
\]

## 4. Ideal closure and two-sided boundary checks

For \(x=(0,1)\), the first and second indices are both 2. Its additive
double \(x+x=(0,2)\) has both indices infinite. Therefore \(\mathcal S\)
is not an additive subgroup. Every ideal includes an additive subgroup, so
this alone falsifies the exact question; it also precludes left or right ideals
under their usual additive-subgroup definitions.

Further independent structural controls show:

* \(\lambda_x(x)=(0,3)\notin\mathcal S\), so lambda invariance fails.
* \(x*x=(0,2)\notin\mathcal S\), so both
  \(B*\mathcal S\subseteq\mathcal S\) and
  \(\mathcal S*B\subseteq\mathcal S\) fail.
* \(\mathcal S\) is a multiplicative subgroup and is normal: it is the
  kernel of the multiplicative character \((n,c)\mapsto e(c)\).
  For additional checking, direct holomorph conjugation gives
  \[
  (m,d)\circ(n,c)\circ(m,d)^{-1}_{\circ}
  =((1-e(c))m+e(d)n,c),
  \]
  which preserves the second residue, including for all negative integers.

With \(u=v=(0,1)\) and \(w=(1,0)\), the right law would require

\[
(u+v)\circ w=(-1,2)
\stackrel{?}{=}(u\circ w)-w+(v\circ w)=(1,2).
\]

It fails over the integers. Hence this is not a two-sided brace. There is no
mathematical contradiction with a positive assertion whose assumptions require
two-sidedness. That statement concerns the hypotheses, rather than an external
literature certification.

## 5. Torsion and finite-quotient traps

Replacing \(\mathbb Z\) by \(\mathbb Z/N\mathbb Z\) preserves the
holomorph construction but makes every index finite. In the \(c=2\) case,
the first kernel contains the solutions to \(2m=0\) modulo \(N\); there are
\(\gcd(N,2)\) such solutions. The first index is therefore
\(N/\gcd(N,2)\), not infinity. For \(c=3\), it is
\(2N/\gcd(N,2)\). For example, \(m=4\) is in the kernel over
\(\mathbb Z/8\mathbb Z\) but not over \(\mathbb Z\).
Thus no finite quotient can certify the claimed failure of property (s).

As a scope check, the same regular-subgroup construction works over an arbitrary
abelian first factor \(M\). Its relevant kernel is \(M[2]=\{m:2m=0\}\),
and \([M:M[2]]=|2M|\). If \(2M\) is infinite, the property-(s) set is
again \(M\times\{0,1\}\). If \(2M\) is finite, all elements of
\(M\times C_4\) have property (s). In the exact index table, the distinction
on \(n\) becomes \(2n=0\), not simply \(n=0\). In particular an infinite
elementary abelian 2-group first factor gives all elements property (s).
This additional deduction verifies the need for the integer torsion-free step;
it is not a submitted novelty claim.

## 6. Reproducible checker evidence and falsification coverage

`CHECKER.py` is independently written and imports no submitted code. Every
check uses an explicit raising function; no Python `assert` is used. Normal and
optimized execution each performed **243,983 explicit checks** and returned
PASS. The deterministic mathematical content agrees across both receipts.
An injected top-level false claim about the index of \((0,2)\) returned exit
code 1 in both modes, after 243,984 checks. This demonstrates that optimized
execution does not disable the detection mechanism.

The checker covers the original input hashes; all sixteen finite graph
identities; formal linear coefficient identities for all 64 residue triples;
all group and left-brace triples on integer coordinates -4 through 4; all
stabilizer and centralizer equations on -20 through 20; every residue and the
zero/nonzero split; explicit closure and right-law failures; and finite quotient
controls for every \(N=1,\ldots,20\). The finite quotient controls are
deliberately labelled as finite and used to expose incorrect extrapolation.

Six independent negative controls were detected:

1. Change \(e(3)\) to +1: regular-subgroup character closure fails.
2. Replace \(2cd\) with \(cd\): finite graph compatibility fails.
3. Remove the nonzero-\(n\) left stabilizer restriction: \(x=(1,0)\),
   \(g=(0,2)\) has a nonzero first star coordinate.
4. Replace the property-(s) set by the even residues: \(c=2\) has infinite
   first index.
5. Copy the integer kernel into \(\mathbb Z/8\mathbb Z\): the residue 4
   supplies a missed torsion solution.
6. Replace the high-bit character by the parity character: this produces another
   valid brace, but the proposed witness no longer has the required right kernel.

These controls cover structural validity, the exact witness, domain dependence,
and set classification; they do not merely replay the same successful samples.
The universal conclusions rest on Sections 2–5, not on the finite windows.

## 7. Final assessment and exact remaining gap

The strongest verified result is a valid infinite left brace in which exactly
\(\mathbb Z\times\{0,1\}\) has property (s), and this set fails additive
closure and lambda invariance. The mathematical counterexample is complete.
There is no remaining gap within this review's mathematical target, and no
mathematical route is blocked.

Unreviewed matters are historical novelty/priority, the external literature
descriptions, and any publication or operational gate. Those are outside the
assigned mathematical review. This PASS must not be promoted to a statement
that those separate gates have passed. The SHA256 input/output manifests and
checker execution receipts identify the sealed result precisely.
