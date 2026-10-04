# Stable Morita rigidity for quantum complete intersections

## Conclusion and scope

**The general question is unresolved by this investigation.** No pair satisfying all its hypotheses and violating its conclusion has been constructed. No universal rigidity proof has been obtained. The results below are partial theorems, obstruction examples, and reductions. They carry no novelty claim.

The target asks whether a quantum complete intersection $X$ must be isomorphic to a symmetric local algebra $Y$, assuming a stable equivalence of Morita type, equal dimensions over the base field, and isomorphic centers as algebras. The source is Radha Kessar's contribution, joint with Markus Linckelmann, in *Representations of Finite Groups*, Oberwolfach Report 17/2009, printed pp.940–941, DOI [10.4171/owr/2009/17](https://doi.org/10.4171/owr/2009/17).

There is a field-scope issue worth retaining: the report has already fixed a residue field of prime characteristic in its surrounding discussion. Its question does not impose algebraic closedness explicitly. The curated version says simply “over a field.” This packet distinguishes arbitrary-field elementary statements, split-local numerical statements, and the algebraically closed characteristic-three known theorem; it does not silently identify these scopes.

Use the convention

\[
 A(\mathbf a,Q)=k\langle x_1,\ldots,x_c\rangle/
 (x_i^{a_i},\ x_i x_j-q_{ij}x_jx_i\ (i<j)),\qquad a_i\ge2,\ q_{ij}\ne0.
\]

Its ordered monomials with $0\le u_i<a_i$ are a basis. Its dimension is $\prod_i a_i$, and it is split local and Frobenius. These facts follow either by normal ordering or from Bergh's [Ext-symmetry paper](https://arxiv.org/abs/0811.4309), Section 2 and Lemma 3.1. “Frobenius” does not mean “symmetric.” For the two-generator convention $xy=qyx$, the top-coefficient pairing is symmetric exactly when $q^{a-1}=q^{b-1}=1$. Indeed the Nakayama automorphism is diagonal on the generators, and an inner automorphism of a split local algebra acts trivially on $J/J^2$. We use explicit symmetric examples below; no unproved transfer of symmetry is needed.

A stable equivalence of Morita type in the original finite-dimensional sense consists of bimodules ${}_A M_B$, ${}_B N_A$, projective on each side, with

\[
 M\otimes_B N\simeq A\oplus P,
 \qquad N\otimes_A M\simeq B\oplus Q,
\]

where $P,Q$ are projective bimodules over the respective enveloping algebras. This is stronger than an unspecified equivalence of stable categories. It is not a derived equivalence by definition, and a graded twisting equivalence is not automatically an ungraded stable equivalence of this type.

## 1 The commutative case is immediate

**Proposition 1.** Let $X,Y$ be finite-dimensional $k$-algebras. If $X$ is commutative, $\dim X=\dim Y$, and $Z(X)\cong Z(Y)$ as $k$-algebras, then $X\cong Y$.

**Proof.** $Z(X)=X$, so $\dim Z(Y)=\dim X=\dim Y$. Since $Z(Y)\subseteq Y$, equality of dimensions gives $Z(Y)=Y$. The given center isomorphism is therefore the required algebra isomorphism. $\square$

No stable equivalence, symmetry, or locality hypothesis is needed here. This covers one-generator quantum complete intersections, all presentations with every commutation parameter equal to one, and prime-dimensional quantum complete intersections under the displayed convention. The last assertion follows because a prime product $\prod_i a_i$, with all $a_i\ge2$, has only one factor. It does not address the noncommutative case.

## 2 Numerical constraints on equivalence bimodules

**Proposition 2.** Suppose $A,B$ are split local $k$-algebras of the same dimension $d$, and $M,N$ give a stable equivalence of Morita type. There are positive integers $r,s$ and a nonnegative integer $t$ such that $M$ is free of rank $r$ on each of its two sides, $N$ is free of rank $s$ on each side, and

\[
 rs=1+td.
\]

In particular, $r,s$ are units modulo $d$.

**Proof.** Finitely generated projectives over a local Artinian algebra are free. If $M$ has left and right ranks $r,r'$, its two vector-space dimensions are $rd,r'd$, so $r=r'$; similarly for $N$. The enveloping algebra $A^e=A\otimes_k A^{\mathrm{op}}$ is local: the ideal $J(A)\otimes A^{\mathrm{op}}+A\otimes J(A)^{\mathrm{op}}$ is nilpotent and its quotient is $k$. Therefore $P$ is a free $A^e$-module, say of rank $t$, so it has dimension $td^2$. Taking dimensions in $M\otimes_B N\simeq A\oplus P$ yields $rsd=d+td^2$. $\square$

The adjective “split” is indispensable in this argument for the enveloping algebra. It is not inferred for an arbitrary local $Y$ over a non-algebraically-closed field. We also do not replace $rs\equiv1\pmod d$ by $r^2\equiv1\pmod d$ without an additional equal-rank choice of inverse bimodule.

The numerical condition does not force $r=s=1$. For example, $r=s=d-1$ satisfies it, with $t=d-2$. More substantively, syzygy gives this phenomenon already for stable self-equivalences. For a split local symmetric nonsemisimple algebra $A$, let

\[
 M=\ker(A\otimes_k A\longrightarrow A)
\]

for the multiplication map. The sequence splits on each side as a sequence of $A$-modules, so $M$ is free of one-sided rank $d-1$. Tensoring this sequence with a module makes $M\otimes_A-$ the syzygy functor in the stable category. A cosyzygy bimodule gives its inverse: $A^e$ is self-injective, and the exact bimodule cosyzygy sequence splits on each $A$-side. Applying the two sequences and Schanuel's lemma gives the usual inverse identities up to projective bimodule summands. Thus this is a stable self-equivalence of Morita type.

The image of the simple module under syzygy is $J(A)$, of dimension $d-1$. For $d>2$, it is not even stably isomorphic to the one-dimensional simple: stable isomorphism of finite modules would make their dimensions congruent modulo $d$. Consequently, the claim that a stable equivalence between local algebras must preserve their unique simple module is false, even with identical source and target algebras. This defeats a direct simple-preservation shortcut, not the rigidity question itself.

## 3 A derived lift would settle the question

**Proposition 3.** Derived-equivalent finite-dimensional local $k$-algebras are isomorphic as $k$-algebras.

**Proof.** A derived equivalence gives a bounded tilting complex $T$ of finitely generated projective right $A$-modules whose endomorphism algebra is $B$. Remove contractible summands to choose a minimal representative, whose differential matrices have entries in $J(A)$. Such a representative is obtained by successively splitting off an isomorphism entry whenever a differential has an entry outside the radical. All projective terms are free.

Let $a,b$ be the smallest and largest indices of nonzero terms. Suppose $a<b$, and put $n=b-a>0$, with shift convention $T[n]^i=T^{i+n}$. Choose a matrix map $f^a:T^a\to T^b=T[n]^a$ having a unit entry, and set all other components of $f:T\to T[n]$ equal to zero. This is a chain map: the only possibly relevant adjacent differentials are outside the endpoints. If it were null-homotopic, its component at degree $a$ would be a sum, with possible signs, of maps factoring through the minimal differentials $d^{b-1}$ or $d^a$. Every matrix entry of such a sum lies in $J(A)$, contradicting the unit entry. Hence $\operatorname{Hom}_{K^b}(T,T[n])\ne0$, contradicting the tilting condition.

Therefore $a=b$, and $T\simeq A^r[a]$ for a positive integer $r$. Its endomorphism algebra is $M_r(A)$. Locality of $B$ forces $r=1$, because a larger matrix ring has nontrivial orthogonal idempotents. Thus $B\cong A$. $\square$

This standard local-tilting argument explains the derived-to-Morita implication mentioned in the original report. It proves no lifting theorem for a stable equivalence. In particular, replacing “stable equivalence of Morita type” by “derived equivalence” would remove the central difficulty.

## 4 Isomorphic centers do not recover the quantum parameter

Let $e>2$, let $q\in k^\times$ have order $e$, and put

\[
 A_q=k\langle x,y\rangle/(x^{e+1},y^{e+1},xy-qyx).
\]

**Proposition 4.** These are symmetric local algebras of dimension $(e+1)^2$. Their centers are isomorphic for all choices of $q$ of order $e$, but $A_q\cong A_r$ if and only if $r=q$ or $r=q^{-1}$.

**Proof of the center and symmetry assertions.** The multiplication law is

\[
 (x^i y^j)(x^u y^v)=q^{-ju}x^{i+u}y^{j+v},
\]

unless an exponent exceeds $e$, in which case it is zero. A monomial $x^i y^j$ commutes with $x$ exactly when $i=e$ or $q^j=1$, and with $y$ exactly when $j=e$ or $q^i=1$. Distinct surviving commutator monomials cannot cancel. Thus a center basis is

\[
 \{1\}\ \cup\ \{x^e y^j:0\le j\le e\}
 \ \cup\ \{x^i y^e:0\le i<e\}.
\]

Its dimension is $2e+2$. Among the nonidentity displayed elements, the only nonzero products are $x^e y^e=y^e x^e$. This multiplication table does not depend on the particular primitive $e$-th root $q$, giving an explicit center isomorphism by matching monomials.

Let $\lambda$ extract the coefficient of $x^e y^e$. The only monomial pairs with nonzero pairing are complementary exponent pairs. Their forward and reversed products have the same coefficient because $q^e=1$; all these coefficients are nonzero. Thus $\lambda(ab)=\lambda(ba)$, and the pairing is nondegenerate. This proves symmetry. The augmentation ideal is nilpotent, with quotient $k$, proving split locality.

**Proof of parameter recovery from the algebra.** An algebra isomorphism preserves $J$, and therefore induces an invertible linear change on $J/J^2$ and an isomorphism of associated graded algebras. Since $e+1>2$, the degree-two relation space is precisely the line generated by $xy-qyx$. In the target $A_r$, write the degree-one images as $ax+by,cx+dy$. Applying the source relation gives

\[
 (1-q)ac=0,\qquad (1-q)bd=0,
\]
\[
 ad(1-q/r)+bc(r^{-1}-q)=0.
\]

Because $q\ne1$ and $ad-bc\ne0$, the matrix must be diagonal or antidiagonal. In the former case $r=q$; in the latter $r=q^{-1}$. Conversely, diagonal rescaling realizes the first case and interchanging the two generators realizes the second. $\square$

**Concrete obstruction pair.** Over $\mathbf F_{11}$, the elements $3$ and $9=3^2$ both have order five, while $3^{-1}=4\ne9$. Thus $A_3,A_9$, with $x^6=y^6=0$, are nonisomorphic symmetric local algebras of dimension 36 and have isomorphic 12-dimensional centers. Their radical layers have dimensions

\[
 1,2,3,4,5,6,5,4,3,2,1.
\]

They also have equal first Hochschild cohomology dimensions, as follows.

**Proposition 5.** If $\operatorname{char}k$ does not divide $e+1$, then

\[
 \dim\operatorname{Der}_k(A_q)=(e+1)^2,
 \qquad \dim HH^1(A_q)=2e+2.
\]

**Proof.** Write $D(x)=\sum u_{ij}x^iy^j$ and $D(y)=\sum v_{ij}x^iy^j$. Differentiating $x^{e+1}=0$ forces every $u_{0j}=0$. For $0<j<e$, the coefficient is a geometric sum of $e+1$ terms, equal to one; for $j=0,e$, it is $e+1\ne0$. Differentiating $y^{e+1}=0$ similarly forces every $v_{i0}=0$. These are $2(e+1)$ independent constraints.

The remaining derivative of the commutation relation has, in position $x^r y^s$ for $1\le r,s\le e$, coefficient

\[
 (1-q^{1-r})u_{r,s-1}+(1-q^{1-s})v_{r-1,s}.
\]

For $(r,s)=(1,1)$ this is zero; for every other position at least one coefficient is nonzero. The variables in different positions are disjoint, and none has already been set to zero by the power relations. We obtain $e^2-1$ further independent equations. Their solutions are exactly the generator assignments descending to derivations of the presentation. Hence the dimension is

\[
 2(e+1)^2-2(e+1)-(e^2-1)=(e+1)^2.
\]

Inner derivations have dimension $\dim A_q-\dim Z(A_q)=e^2-1$. Subtraction gives the result. $\square$

In the concrete pair, $\dim HH^1=12$ for both algebras. Matching this dimension is only a necessary test. No isomorphism of their full Hochschild rings, restricted Lie structures, outer automorphism groups, or stable categories is asserted. **In particular, the pair is not a counterexample to the target: the stable-Morita hypothesis has not been established.**

## 5 A socle deformation is eliminated by a stable invariant

Work over a field of characteristic three, and for $\beta\in\{0,1\}$ define

\[
 C_\beta=k\langle x,y\rangle/(xy+yx,\ y^3,\ x^3-\beta x^2y^2).
\]

The undeformed $C_0$ is the quantum complete intersection appearing in Kessar's theorem. The second algebra is a socle deformation of the kind considered in her classification. We compute directly rather than assuming it is stably equivalent.

**Proposition 6.** The algebras $C_0,C_1$ are symmetric split local algebras of dimension nine, with isomorphic centers and the same radical layers $1,2,3,2,1$. They are nonisomorphic, and they are not stably equivalent of Morita type.

**Normal forms and symmetry.** Reorder $yx\mapsto-xy$, replace $y^3\mapsto0$, and replace $x^3\mapsto\beta x^2y^2$. The latter decreases weight if $x$ has weight three and $y$ weight one; the commutation rule decreases lexicographic order within a weight. The overlaps $x^4,x^5,yx^3,y^3x$, and the self-overlaps of $y^3$, all reduce compatibly to zero when relevant. For example, both reductions of $x^4$ give $\beta x^3y^2=\beta^2x^2y^4=0$; both reductions of $yx^3$ are zero. Thus the nine monomials $x^iy^j$, $0\le i,j\le2$, are normal forms. Alternatively the complete associative multiplication tables are checked in the executable certificate.

The radical is the span of all nonidentity monomials, its fifth power is zero, and its powers have dimensions $8,6,3,1,0$. A center basis is

\[
 1,x^2,y^2,x^2y,xy^2,x^2y^2.
\]

The only nonzero product of two nonidentity basis elements is $x^2y^2=y^2x^2$. This gives the center isomorphism. Extracting the coefficient of the top monomial gives a symmetric pairing. With the basis ordered by total degree, the complementary-degree blocks are nonsingular and products of total degree greater than four vanish; hence the pairing is nondegenerate. The extra equality $\lambda(x\,x^2)=\lambda(x^2x)=\beta$ does not change this argument.

**An isomorphism obstruction.** For $z=ax+by+w\in J(C_\beta)$, with $w\in J^2$, expansion of the three defining relations in characteristic three gives

\[
 z^3=a^2b\,x^2y+ab^2\,xy^2+\beta a^3x^2y^2.
\]

In $C_0$, the cube-zero elements of $J$ form the union of the two distinct hyperplanes $a=0$ and $b=0$, which is not a linear subspace. In $C_1$, they form the single hyperplane $a=0$. A $k$-linear algebra isomorphism preserves $J$ and the cube-zero locus, so none exists. Over $\mathbf F_3$ the two counts are $5\cdot3^6=3645$ and $3\cdot3^6=2187$, respectively; the verifier checks every radical element.

**The stable obstruction.** Write the two generator images of a derivation as

\[
 D(x)=\sum_{0\le i,j\le2}u_{ij}x^iy^j,\qquad
 D(y)=\sum_{0\le i,j\le2}v_{ij}x^iy^j.
\]

Expansion of the differentiated defining relations yields the following six zero conditions in both cases:

\[
 u_{00}=u_{01}=u_{20}=v_{00}=v_{02}=v_{10}=0.
\]

For $C_0$, the remaining condition is $u_{21}+v_{12}=0$. Thus its derivation space has dimension $18-7=11$. For $C_1$, the two remaining conditions are

\[
 u_{10}+v_{01}=0,\qquad u_{21}+v_{12}+v_{20}=0,
\]

so the derivation dimension is $18-8=10$. All displayed constraints are independent. Conversely, they annihilate the derivatives of the three defining relations, so they suffice for a generator assignment to descend to a derivation. Inner derivation spaces have dimension $9-6=3$. Therefore

\[
 \dim HH^1(C_0)=8,\qquad \dim HH^1(C_1)=7.
\]

Positive-degree Hochschild cohomology is preserved by stable equivalences of Morita type between finite-dimensional self-injective algebras; the stronger restricted-Lie invariance is Theorem 1 of [Briggs and Rubio y Degrassi](https://arxiv.org/abs/2006.13871). Our algebras are symmetric and hence self-injective. The dimension mismatch excludes such an equivalence. $\square$

Thus a plausible deformation fails exactly at the key hypothesis. Isomorphic centers and identical Loewy layers cannot be used as substitutes for a stable equivalence.

## Known results and the remaining gap

Kessar's [Theorem 1.2](https://arxiv.org/abs/1012.0534) proves the desired rigidity for $k$ algebraically closed of characteristic three and $X=C_0$. The theorem is not an unrestricted statement about every nine-dimensional algebra over every field. Its proof classifies possible symmetric local algebras with the prescribed center, then separates them using the connected outer automorphism group. This is credited prior work, not a new solution.

For the prime-power family $x^p=y^p=0$ in odd characteristic $p$, with a parameter of order $e\mid p-1$, Benson–Kessar–Linckelmann's [Corollary 1.3](https://arxiv.org/abs/1604.04437) bounds the number of generators of a split local symmetric stable-Morita partner by $2e$. It does not force that number to be two. Their parameter convention is $yx=qxy$, inverse to ours. Briggs–Rubio y Degrassi adds restricted Hochschild invariants, but its block-theoretic application still singles out the known $p=3$ rigidity case.

The September 2026 preprint [The Auslander–Reiten conjecture for quantum complete intersections](https://arxiv.org/abs/2609.24007) states a projectivity criterion from vanishing of first and second self-extensions. Its theorem is about modules, not the present algebra-isomorphism question. Its graded-twist method uses rigidity of modules. The simple module of a nonsemisimple quantum complete intersection has $\dim\operatorname{Ext}^1(k,k)=\dim J/J^2=c>0$, so applying a rigid-module criterion to its image under a stable equivalence would be unjustified. No result from that preprint is needed for any proof above; only its stated scope was checked.

The unresolved step is a reconstruction or lifting theorem using the *actual* stable equivalence, strong enough to force the noncommutative multiplication of arbitrary $Y$. Another possible resolution would be explicit projective-on-both-sides bimodules for a nonisomorphic pair, together with proofs of both projective bimodule error terms. Neither has been supplied here. The concrete 36-dimensional pair is only a test case for stronger invariants, and the nine-dimensional deformation is already ruled out.

## Exact verification and limitations

`verify.py` uses only Python's standard library and arithmetic in the prime fields $\mathbf F_3,\mathbf F_{11}$. It verifies complete basis associativity tables, symmetrizing pairings, generator relations, centers, derivation kernels, the Leibniz rule on every basis pair for every basis derivation, the parameter-pair quadratic relation obstruction with positive controls, radical layers, and all 13,122 radical cube computations in the two nine-dimensional algebras.

The 13,200 invertible two-by-two matrices tested for each parameter comparison are a finite control. The general nonisomorphism proof is Proposition 4, so the proof does not depend on treating a finite-field matrix search as a classification over arbitrary extensions. Matching numerical invariants has never been promoted to an equivalence. The scripts do not construct equivalence bimodules, compute a derived lift, classify arbitrary $Y$, or certify the absence of all later literature. Independent mathematical audit remains required before publication.
