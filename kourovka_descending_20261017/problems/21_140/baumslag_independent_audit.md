# Independent audit: finitely presented Baumslag benchmark


Checkpoint: 2026-10-17 21:33:30 UTC. Discovery estimate: **8%**; this benchmark
audit is complete. Verdict: **PASS**. This is a verified classical benchmark,
not a novel counterexample or a status certification for 21.140.

The group proposed by the parent is
\[
 B=\langle a,s,t\mid [s,t]=1,\ [a,a^t]=1,\ a^s=aa^t\rangle,
 \qquad a^t=t^{-1}at.
\]
It is finitely presented, torsion-free, residually finite, metabelian,
contains no copy of \(F\), and has infinite integral cohomological
dimension. Its exact geometric finiteness length is two: it is
\(\mathrm F_2\) but not even \(\mathrm{FP}_3\).

### Presentation and the semidirect-product identification

Put \(a_i=a^{t^i}\), \(i\in\mathbb Z\). The defining commutator gives
\([a_i,a_{i+1}]=1\) for all \(i\), and the commuting head generators
give \(a_i^s=a_i a_{i+1}\). Suppose all pairs at distance at most \(n\)
commute. Conjugating \([a_i,a_{i+n}]=1\) by \(s\) gives
\[
 [a_i a_{i+1},a_{i+n}a_{i+n+1}]=1.
\]
Every pair in these products already commutes except potentially the outer
pair \(a_i,a_{i+n+1}\). Cancelling the known commuting factors proves
that pair commutes too. Induction yields all the commutator relations for
the restricted wreath product
\[
 U=\mathbb Z\wr\mathbb Z
   =\mathbb Z[x,x^{-1}]_{\rm add}\rtimes\langle t\rangle.
\]
Here right conjugation by \(t\) multiplies the additive module by \(x\).

The endomorphism \(\phi:U\to U\), defined by \(a\mapsto aa^t\),
\(t\mapsto t\), multiplies the additive module by \(1+x\) and is
injective. Thus the displayed finite presentation is exactly the ascending
HNN extension with \(s^{-1}us=\phi(u)\). Britton's lemma embeds \(U\),
and the union \(\bigcup_{k\ge0}s^kUs^{-k}\) identifies with
\(R_{\rm add}\rtimes\langle t\rangle\), where
\[
 R=\mathbb Z[x,x^{-1},(1+x)^{-1}].
\]
The head \(\langle s,t\rangle\) is \(\mathbb Z^2\): setting \(a=1\)
gives a quotient that is the identity on these generators. Hence
\[
 B\cong R_{\rm add}\rtimes\mathbb Z^2,
\]
with right conjugation actions \(t:r\mapsto xr\),
\(s:r\mapsto(1+x)r\).

The additive kernel and the quotient are torsion-free abelian, proving
torsion-freeness and metabelianity. The independent elements
\(1,x,\ldots,x^{d-1}\) in \(R\subset\mathbb Q(x)\) give embedded
\(\mathbb Z^d\) for every \(d\), proving infinite cd. Metabelianity
excludes \(F\), whose nontrivial derived subgroup is perfect.

Residual finiteness also has an explicit check. A nonzero head element is
separated in a finite quotient of \(\mathbb Z^2\). For a nonzero pure
kernel element write
\(r=p(x)/(x^i(1+x)^j)\) with \(p\in\mathbb Z[x]\setminus\{0\}\).
Choose a prime \(\ell>\deg p+2\) at which \(p\) remains nonzero, then
choose \(\lambda\in\mathbb F_\ell\setminus\{0,-1\}\) with
\(p(\lambda)\ne0\). Evaluation gives a map to the finite semidirect
product \(\mathbb F_{\ell,\rm add}\rtimes(\mathbb Z/(\ell-1))^2\),
with right conjugation actions by \(\lambda\) and \(1+\lambda\).
It separates \(r\).

### Alternating tensors: no localization gap

All exterior powers in the following calculation are rational:
\[
 V=R\otimes_\mathbb Z\mathbb Q,
 \qquad H_q(R_{\rm add};\mathbb Q)=\Lambda^q_\mathbb Q V.
\]
This homology identity follows by expressing the torsion-free abelian
kernel as a directed union of finitely generated free abelian subgroups.
The tensor product \(V^{\otimes q}\) identifies with the ring
\[
 T_q=\mathbb Q[x_1,\ldots,x_q,
              x_1^{-1},\ldots,x_q^{-1},
              (1+x_1)^{-1},\ldots,(1+x_q)^{-1}].
\]
In characteristic zero antisymmetrization identifies \(\Lambda^qV\)
with the alternating subspace of \(T_q\). Let
\[
 \Delta_q=\prod_{i<j}(x_i-x_j),\quad
 e_j=e_j(x_1,\ldots,x_q),\quad
 f=\prod_i(1+x_i)=1+e_1+\cdots+e_q,
\]
and put
\[
 S_q=\mathbb Q[e_1,\ldots,e_q,e_q^{-1},f^{-1}].
\]
Then the alternating subspace is exactly \(\Delta_qS_q\). Indeed multiply
an alternating element by a sufficiently large symmetric denominator
\(e_q^Nf^M\). The result is an alternating polynomial, divisible by
every \(x_i-x_j\); the quotient by \(\Delta_q\) is a symmetric
polynomial and hence a polynomial in the elementary symmetric functions.
The converse inclusion is immediate. Multiplication by \(\Delta_q\) is
injective, so this is a free rank-one \(S_q\)-module identification, not
an assertion about arbitrary functions on a discriminant locus.

The diagonal actions of the head generators on this module are
multiplication by \(e_q\) and \(f\). If the left-action convention for
the Lyndon--Hochschild--Serre sequence uses inverse conjugation, the
multipliers become their inverses; replacing generators of \(\mathbb Z^2\)
by their inverses changes none of the following computations.

### Freeness over the head group ring and all rational homology groups

For every \(q\ge2\) there is an explicit ring isomorphism
\[
 S_q\cong\mathbb Q[e_1,\ldots,e_{q-2}][u^{\pm1},v^{\pm1}],
 \qquad u=e_q,\quad v=f.
\]
The inverse eliminates
\(e_{q-1}=v-1-u-\sum_{j=1}^{q-2}e_j\). Consequently
\(\Lambda^q V\) is free as a module over
\(\mathbb Q[\mathbb Z^2]=\mathbb Q[u^{\pm1},v^{\pm1}]\), with basis
given by the monomials in \(e_1,\ldots,e_{q-2}\), multiplied by
\(\Delta_q\). Its rank is one for \(q=2\) and countably infinite for
\(q\ge3\). Therefore
\[
 H_p(\mathbb Z^2,\Lambda^qV)=0\quad(p>0,q\ge2),
 \qquad
 H_0(\mathbb Z^2,\Lambda^qV)
 \cong\mathbb Q[e_1,\ldots,e_{q-2}].
\]
The parent coinvariant computation is thus correct: setting \(e_q=f=1\)
eliminates \(e_{q-1}\), with no additional relation.

For \(q=1\), the operator \(s-1\) is multiplication by
\((1+x)-1=x\), a unit of \(V\). The two-generator Koszul complex for
\(\mathbb Z^2\)-homology is therefore contractible, so
\(H_p(\mathbb Z^2,V)=0\) for every \(p\). For \(q=0\) the coefficient
module is trivial \(\mathbb Q\), whose head homology has dimensions
\(1,2,1\) in degrees zero, one, two.

It follows that the LHS spectral sequence
\[
 E^2_{p,q}=H_p(\mathbb Z^2,H_q(R;\mathbb Q))
 \Longrightarrow H_{p+q}(B;\mathbb Q)
\]
has no nonzero differential. More minimally, the only possible incoming
differential to \(E^2_{0,3}\) is from \(E^2_{2,2}=0\); all higher
incoming sources have \(p>2\), and no outgoing differential can have
nonnegative first index. Thus the proposed \(H_3\) argument is valid
even without the stronger freeness calculation.

The complete resulting vector-space calculation is
\[
 H_0(B;\mathbb Q)=\mathbb Q,\qquad
 H_1(B;\mathbb Q)=\mathbb Q^2,\qquad
 H_2(B;\mathbb Q)=\mathbb Q^2,
\]
\[
 H_n(B;\mathbb Q)\cong
 \mathbb Q[e_1,\ldots,e_{n-2}]\quad(n\ge3).
\]
The last isomorphism is as vector spaces; no multiplicative homology-ring
claim is intended. Since \(H_3\) is infinite-dimensional,
\(B\) is not \(\mathrm{FP}_3\) over \(\mathbb Z\) (nor over
\(\mathbb Q\)). Its finite presentation supplies \(\mathrm F_2\).

### Historical cross-check and precise scope

The exact presentation is recorded as Baumslag's metabelian group in
Hermiller--Martínez-Pérez, *HNN extensions and stackable groups*, Theorem
6.1 and Section 6:
[author PDF](https://shermiller.github.io/Susan_Hermiller/webppr/stackablehnn.pdf).
The PDF and extracted text are saved as
`sources/raw/hermiller_martinez_perez_stackablehnn.*`.

Mullaney's 2013 thesis, introductory pp. 12--13,
[repository PDF](https://theses.gla.ac.uk/4452/1/2013mullaneyphd.pdf), reports
the stronger classical integral homology behavior and points to
Baumslag--Dyer, *The integral homology of finitely generated metabelian
groups. I*, Amer. J. Math. 104 (1982), 173--182, and
Baumslag--Stammbach, *Free exterior powers of nonfree modules and homology*,
Amer. J. Math. 109 (1987), 35--56. These are historical leads, not independently
read priority certifications. The thesis and extracted text are saved as
`sources/raw/mullaney_metabelian_2013.*`.

The self-contained rational calculation above is the basis of this audit's
homological conclusion. It strengthens the first HNN benchmark by supplying
finite presentation, but it fails the requested \(\mathrm F_\infty\)
hypothesis at the next finiteness stage. No central gap in 21.140 has been
closed.
