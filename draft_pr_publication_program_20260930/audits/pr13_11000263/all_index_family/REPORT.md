# Independent all-index algebra audit of PR 13

Completed 2026-10-01 UTC. Snapshot: `7a845f7e025a24affe1b712cf7ada648570f9c64`; record 11000263.

## Conclusion and exact scope

The Burau witness in `source_snapshot/AUDIT.md` is mathematically correct for both explicitly repaired presentations over \(F=\mathbb Q(q)\):

\[
A_n=FB_n/(R_2,\ldots,R_{n-1}),\qquad
C_n=FB_{n+1}/(R_2,\ldots,R_n),\qquad n\ge3,
\]

where the ideals are two-sided. In both, \(X_3\ne0\). Every legal relation is verified below by an all-index derivation, not an inference from small ranks. The source's literal quotient is not defined as printed: its terminal row uses \(\sigma_n\), while \(B_n\) has only \(\sigma_1,\ldots,\sigma_{n-1}\). I independently checked the preprint definitions and visually inspected published p. 298. This family does not certify priority or novelty, nor choose an author-intended repair.

No fatal error was found in the displayed proof. The following qualifications should remain explicit:

1. Specialize \(u=q^3\) through the Laurent-polynomial matrix model. There is no field homomorphism \(\mathbb Q(q,u)\to\mathbb Q(q)\) sending \(u\) to \(q^3\).
2. The \(X_4=0\) observation requires at least four strands. \(X_4\) is undefined in \(A_3\); it is defined in \(C_3\).
3. Scalar twist values in this witness are constrained: \(t_2=-u\), \(t_3=u^3=-t_2^3\). At \(u=q^3\), these become \(-q^3\) and \(q^9\). Arbitrary independent prescribed twist parameters are not addressed.
4. A finite-dimensional specialized matrix image cannot give an upper bound on the dimension of a universal quotient with added relations. In fact, the generic independent-\(u\) image, regarded as an \(F\)-algebra, is infinite-dimensional, as proved below.

The strongest verified target result is a negative answer for both repairs, conditional on those stated definitions. There is no unconditional answer to the defective literal definition and no new-solution claim.

## Source conventions and independently checkable setup

The primary sources are [Bigelow's preprint, p. 14](https://arxiv.org/pdf/math/0505064) and the [published scan, p. 298](https://web.math.ucsb.edu/~bigelow/publications/10.pdf). In the source, \(\sigma_{i_1\ldots i_s}\) means the product in that order, and its bar denotes the inverse of that complete product. Thus

\[
\bar\sigma_{21}=(\sigma_2\sigma_1)^{-1}=\sigma_1^{-1}\sigma_2^{-1},
\quad
\bar\sigma_{k\cdots a}=\sigma_a^{-1}\sigma_{a+1}^{-1}\cdots\sigma_k^{-1}.
\]

The source's powers of \(q\) and exceptional initial relation are retained:

\[
X_2=q\sigma_1^{-1}+(1-q)-\sigma_1,\qquad
X_k=(q^{k-1}\bar\sigma_{(k-1)\cdots1}-\sigma_{1\cdots(k-1)})X_{k-1}.
\]

\[
R_2=(q\sigma_2^{-1}+(1-q)-\sigma_2-q\bar\sigma_{21}+\sigma_{12})X_2,
\]

\[
R_k=(q^{k-1}\bar\sigma_{k\cdots2}-\sigma_{2\cdots k}
      -q^{k-1}\bar\sigma_{k\cdots1}+\sigma_{1\cdots k})X_k\quad(k\ge3).
\]

Fix \(m\ge3\). Over \(S=F[u,u^{-1}]\), let \(B_i\) act as the identity outside coordinates \(i,i+1\) and have block

\[
\begin{pmatrix}1-u&u\\1&0\end{pmatrix},\qquad
B_i^{-1}|_{i,i+1}=\begin{pmatrix}0&1\\u^{-1}&1-u^{-1}\end{pmatrix}.
\]

The product of the two displayed blocks is the identity in either order. Nonadjacent blocks commute. Direct multiplication on three consecutive coordinates gives the same matrix for \(B_iB_{i+1}B_i\) and \(B_{i+1}B_iB_{i+1}\):

\[
\begin{pmatrix}1-u&u(1-u)&u^2\\1-u&u&0\\1&0&0\end{pmatrix}.
\]

This proves that \(\sigma_i\mapsto B_i\) is a group representation and hence extends to an \(F\)-algebra map \(FB_m\to M_m(S)\). No faithfulness assertion is needed.

## All-index derivation

Write \(e_i\) for column basis vectors and define

\[
v_r=u^{1-r}e_r-u^{-r}e_{r+1},\qquad
\lambda=-e_1^T+e_2^T,\qquad
c_k=\prod_{j=1}^{k-1}(q^j-u).
\]

First,

\[
qB_1^{-1}+(1-q)I-B_1
=(q-u)\begin{pmatrix}-1&1\\u^{-1}&-u^{-1}\end{pmatrix}
=(q-u)v_1\lambda.
\tag{1}
\]

The key propagation is a local, direct calculation. For \(1\le r\le m-2\), use

\[
B_i e_i=(1-u)e_i+e_{i+1},\quad B_i e_{i+1}=ue_i,
\quad B_i^{-1}e_i=u^{-1}e_{i+1}.
\]

It follows that

\[
\begin{aligned}
B_{r+1}v_r
 &=u^{1-r}e_r-u^{-r}(1-u)e_{r+1}-u^{-r}e_{r+2},\\
B_rB_{r+1}v_r
 &=u^{1-r}e_{r+1}-u^{-r}e_{r+2}=u v_{r+1},\\
B_{r+1}^{-1}v_r
 &=u^{1-r}e_r-u^{-r-1}e_{r+2},\\
B_r^{-1}B_{r+1}^{-1}v_r
 &=u^{-r}e_{r+1}-u^{-r-1}e_{r+2}=v_{r+1}.
\end{aligned}\tag{2}
\]

After either local pair acts, support is confined to \(r+1,r+2\). Every earlier factor \(B_j^{\pm1}\), \(j\le r-1\), fixes those coordinates. Consequently, for every \(a\le r\),

\[
(B_a\cdots B_{r+1})v_r=u v_{r+1},\qquad
(B_{r+1}\cdots B_a)^{-1}v_r=v_{r+1}.
\tag{3}
\]

The inverse here is explicitly \(B_a^{-1}\cdots B_{r+1}^{-1}\), so the rightmost inverse acts first. No inverse order has been changed.

Equations (1) and (3), with \(r=k-2\) and \(a=1\), prove by induction that

\[
\rho_m(X_k)=c_k v_{k-1}\lambda\qquad(2\le k\le m).
\tag{4}
\]

Indeed, multiplying the previous image by the recursive bracket multiplies its column vector by \((q^{k-1}-u)\) and moves \(v_{k-2}\) to \(v_{k-1}\).

## Every defining row, including the exceptional one

The exceptional row must be checked separately because it has the extra \((1-q)I\). Acting on \(v_1=e_1-u^{-1}e_2\),

\[
(qB_2^{-1}+(1-q)I-B_2)v_1
=(q-u)(u^{-1}e_2-u^{-2}e_3)=(q-u)v_2.
\tag{5}
\]

The complete-word convention and (3) also give

\[
(qB_1^{-1}B_2^{-1}-B_1B_2)v_1=(q-u)v_2.
\tag{6}
\]

Their difference kills \(v_1\); multiplying by \(c_2\lambda\) proves \(\rho_m(R_2)=0\).

For \(3\le k\le m-1\), put \(r=k-1\). Equation (3) applies with both \(a=1\) and \(a=2\), because \(r\ge2\). Hence each of

\[
q^{k-1}(B_k\cdots B_2)^{-1}-B_2\cdots B_k,
\qquad
q^{k-1}(B_k\cdots B_1)^{-1}-B_1\cdots B_k
\]

sends \(v_{k-1}\) to \((q^{k-1}-u)v_k\). Their difference kills it, so (4) proves \(\rho_m(R_k)=0\) for every legal index.

Take \(m=n\) for \(A_n\); all rows \(R_2,\ldots,R_{n-1}\) vanish. Separately take \(m=n+1\) for \(C_n\); the same proof now includes the terminal \(R_n\). In either case the two-sided relation ideal lies in the representation kernel. This proves factorization through each quotient directly. It does not assume that a detected element survives additional relations.

At the boundary, \(A_3\) uses three coordinates and only \(R_2\). \(C_3\) uses four coordinates and both \(R_2,R_3\). Both have the same nonzero \(X_3\) formula on coordinates 2,3; the fourth coordinate makes the additional row legal and proves that it vanishes.

## Detection over the claimed base field

Equation (4) gives

\[
\rho_m(X_3)=(q-u)(q^2-u)(u^{-1}e_2-u^{-2}e_3)\lambda.
\tag{7}
\]

Its \((2,1)\) entry is \(-u^{-1}(q-u)(q^2-u)\), a nonzero element of \(S\), and hence of \(K=\mathbb Q(q,u)\). If \(X_3\) were zero in either \(F\)-algebra quotient, any \(F\)-algebra representation of that quotient would send it to zero. The displayed nonzero image contradicts this. This detection argument needs neither a faithful representation nor an unproved injectivity statement about a quotient map or scalar extension.

More generally, the same Laurent-polynomial construction works for a nonzero commutative coefficient ring with a chosen scalar \(q\): each \(q^j-u\) has unit leading coefficient as a polynomial in \(u\), and the nonzero monic product cannot vanish. That extension is not needed for the asserted \(F\)-claim. For a fixed numerical field specialization \(u\ne0\), the Burau image of \(X_3\) is nonzero precisely when \(u\ne q\) and \(u\ne q^2\); image vanishing at other specializations does not prove universal-algebra vanishing.

## Legitimate specialization, twists, and degeneracies

All matrices and all identities above live in \(S=F[u,u^{-1}]\), not merely in \(K\). Thus the evaluation map \(S\to F\), \(u\mapsto q^j\), exists for every integer \(j\), since \(q\) is a unit. This is the proper base-change route. Attempting this on all of \(K\) would fail: the invertible element \(u-q^j\) would have to map to zero.

At \(u=q\), \(X_2\) and all subsequent images vanish. At \(u=q^2\), \(X_3\) and all subsequent images vanish. At \(u=q^3\),

\[
\rho_m(X_3)=(q-q^3)(q^2-q^3)v_2\lambda\ne0,
\qquad \rho_m(X_4)=0\quad(m\ge4).
\tag{8}
\]

The nonzero assertion is over \(F\), where \(q\) is transcendental. If one further evaluates \(q=1\) or \(q=-1\), this particular witness degenerates. At \(q=0\), \(u=q^3\) is invalid because \(B_i\) is not invertible. Those controls do not invalidate the generic argument.

For the first twist,

\[
B_1v_1=-uv_1,\quad\text{so}\quad B_1\rho_m(X_2)=-u\rho_m(X_2).
\tag{9}
\]

Let \(P=B_1B_2\). A direct three-step calculation gives

\[
Pv_2=-ue_1+u^{-1}e_3,\quad
P^2v_2=u^2e_1-ue_2,\quad
P^3v_2=u^2e_2-ue_3=u^3v_2.
\]

Therefore

\[
(B_1B_2)^3\rho_m(X_3)=u^3\rho_m(X_3).
\tag{10}
\]

These identities establish only the indicated left twist relations with their indicated scalar values. The original source explicitly proposes \(\sigma_1X_2=tX_2\); the second twist is an additional witness property. Neither assertion licenses arbitrary unrelated scalar choices.

## Dimension distinction: image versus universal quotient

At \(u=q^3\), the matrices lie in \(M_m(F)\), so their image algebra has dimension at most \(m^2\) over \(F\). A map from a universal quotient onto this image yields a lower bound on its dimension, not an upper bound. For example the infinite-dimensional algebra \(F[z]\) maps onto the one-dimensional algebra \(F\) by \(z\mapsto0\). This simple counterexample falsifies the general inference from a finite-dimensional image to a finite-dimensional source.

There is a further exact distinction for the unspecialized representation. Although it acts on a finite-dimensional \(K\)-vector space, its image as an \(F\)-algebra is infinite-dimensional. Suppose a finite relation \(\sum_{j=0}^d a_jB_1^j=0\) with \(a_j\in F\) existed. Applying it to \(v_1\ne0\) and using (9) gives

\[
\left(\sum_{j=0}^d a_j(-u)^j\right)v_1=0.
\]

As \(u\) is transcendental over \(F\), all \(a_j\) are zero. Thus \(1,B_1,B_1^2,\ldots\) are linearly independent over \(F\). Because each repaired quotient maps onto this image, both \(A_n\) and \(C_n\) themselves are infinite-dimensional over \(F\). This observation concerns the repairs before new scalar/\(X_4\) relations are imposed; it makes no dimension claim for the extra-relation universal quotients.

## Adversarial artifacts and reproducibility

`probe.py` is a new standard-library implementation of sparse integer Laurent-polynomial arithmetic and direct matrix multiplication. It does not import or copy the snapshot's verifiers. Running

```
python3 probe.py
```

in this folder reproduces `probe_results.json`. It passed 426 exact assertions on 3–10 strands: inverse identities, braid/commutation relations, complete-word inverses, every legal relation, the formula for every available \(X_k\), twists, and all three parameter controls. Its finite cases cover \(A_3,\ldots,A_{10}\) and \(C_3,\ldots,C_9\). These are reproducible supporting checks; equations (1)–(10) provide the all-index proof.

The implementation deliberately probes two plausible transcription errors. With \(q=2,u=3,m=3\):

* Replacing \(\bar\sigma_{21}\) by \(B_2^{-1}B_1^{-1}\) makes \(R_2\)'s defect nonzero, with first row \((2/3,-2/3,0)\).
* Treating \(R_2\) as the uniform higher-index formula and dropping \((1-q)I\) leaves defect \((q-1)\rho(X_2)\ne0\), with first row \((1,-1,0)\).

The correct \(X_3\) has \((2,1)\) entry \(1/3\) in the same numerical case. At \(q=2,u=q^3=8\), its \((2,1)\) entry is \(-3\), while \(X_4\) vanishes when available. These probes make order, exceptional-row, and specialization errors falsifiable.

## Independence and remaining gap

Read materials: `AUDIT.md`, `SOURCES.md`, `input_record.json`, the original preprint, the author's published scan, and `SCALAR_SCOPE_CHECK.md` for scope consistency. Historical `REVIEW.md`, `verdict.json`, other snapshot verification outputs, and sibling audits were not read. The proof and symbolic implementation were developed directly from definitions. No external individual was contacted; no canonical file or Git state was changed.

This family verifies the conditional algebra result. It leaves the exact prior-art chronology to the separate scope/primary-source family, and leaves the author's intended repair unknown. There is no unsupported central algebraic step remaining in the witness. No claim about finite-dimensional universal quotients with new relations follows. Audit completion estimate: 100%; completion of the original literal research question is inapplicable until its definition is repaired.
