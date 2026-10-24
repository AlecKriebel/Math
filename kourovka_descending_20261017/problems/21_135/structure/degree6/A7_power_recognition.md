# Degree-six route: recognition of every direct power of A7

**Restricted theorem; fresh mathematical audit passed, originality unresolved.** This does not resolve Kourovka21.135 for arbitrary radical-free groups. The current argument relies on the complete degree-six classification of Lindsey and exact ordinary-character-degree witnesses from ATLAS/GAP. Originality has not been established; no publication claim is made.

## Restricted theorem

For every integer r≥0, if a finite group H has the same multiset of irreducible complex character degrees as A7^r, then H≅A7^r.

This is stronger than radical recognition for this particular source family, but remains a restricted result. The case r=0 is immediate from |H|=1, so suppose r≥1.

## 1. The degree monoid and the least nonlinear degree

The ordinary degrees of A7 are

\[
 1,6,10,10,14,14,15,21,35.
\]

Thus H is perfect (it has exactly one linear character), has order 2520^r, and has exactly r irreducible characters of degree6. Its least nonlinear degree is6. Every degree is a product of at most r members of

\[
 E=\{6,10,14,15,21,35\}.
\]

Each member of E is the product of two distinct primes in {2,3,5,7}. It follows that every degree d has the two properties

\[
 \Omega(d)\equiv0\pmod2,\qquad
 v_p(d)\le\sum_{q\ne p}v_q(d)\quad(p\in\{2,3,5,7\}).\tag{M}
\]

In particular, no character degree is any of

\[
 2,3,4,5,7,20,24,63,189.
\]

The small degrees2–5 are excluded by minimality. For 20 and63, Ω is odd. For24 and189, one prime valuation is3 while the sum of the others is1. All prime divisors of |H| belong to {2,3,5,7}, so11 and13 do not divide |H|.

## 2. Every degree-six image is quasiprimitive

Choose χ∈Irr(H) of degree6 and set K=H/kerχ. Then K is perfect, χ is faithful as a character of K, and every irreducible degree of K occurs among the degrees of H, by inflation. The faithful degree-six representation is unimodular because its determinant is a linear character of the perfect group K.

For every N normal in K, Clifford theory gives

\[
 \chi|_N=e(\theta_1+\cdots+\theta_t),\qquad et\theta_1(1)=6,
\]

where K acts transitively on the distinct θ_i. If t>1, the permutation representation on these t constituents has a nonzero augmentation representation of dimension t−1≤5 with no invariant vectors. Every irreducible constituent would be a nontrivial irreducible representation of K of degree≤5, contrary to the least nonlinear degree6 and perfectness. Therefore t=1 for every N. This is exactly quasiprimitivity in Lindsey's definition (restriction to each normal subgroup is homogeneous).

This step avoids assuming that arbitrary degree-six representations are covered by a classification of primitive or quasiprimitive groups. The needed hypothesis is proved directly from the degree data.

## 3. Applying the complete primary classification

Lindsey's Section3 theorem classifies finite groups with faithful irreducible quasiprimitive unimodular complex representations of degree6. Its cases I–XVII apply to K. The theorem gives central orders for the perfect case. The identification of the A7 alternatives as the named covers3.A7 and6.A7 is also explicit in I.Cheltsov and C.Shramov, *Six-dimensional exceptional quotient singularities*, Theorem3.2, casesVII–VIII ([arXiv1001.3863](https://arxiv.org/abs/1001.3863), DOI10.4310/MRL.2011.v18.n6.a6). Equivalently, the standard Schur-cover statement is M(A7)≅C6 with a unique universal perfect central cover. We do not identify arbitrary central extensions merely from center order. In the following elimination table, a quotient's ordinary character degrees inflate to K and hence to H. This use of quotients is legitimate; restriction of characters to arbitrary subgroups is never used to assert degree inclusion.

| Lindsey case | Obstruction for the present perfect K |
| --- | --- |
| I | K/Z(K)=A×B, with A among A5,A4,S4. A solvable A cannot be a nontrivial quotient of perfect K; A=A5 supplies degree3. |
| II | The displayed central quotients are subgroups of products of solvable groups (S4/A4 and Hessian groups), hence are solvable. A central extension remains solvable, contradicting nontrivial perfect K. |
| III | Perfectness removes the S5 option. The quotient A5 supplies degree3. |
| IV,V | The quotient A6 supplies degree5. |
| VI | Perfectness removes S7. The perfect-case central order is1, so K≅A7. |
| VII | K is the triple cover3.A7, with an ordinary character of degree24. |
| VIII | K is the sixfold cover6.A7, with an ordinary character of degree24 (the faithful projective rows already supply this). |
| IX,X | Perfectness removes PGL2(7). The quotient PSL2(7) supplies degree3. |
| XI,XII | The simple quotients PSL2(11), PSL2(13) have orders divisible by11,13 respectively, impossible since |K| divides2520^r. |
| XIII | The quotient PSp4(3)≅PSU4(2) supplies degree5. An extension by an outer involution would not be perfect. |
| XIV | The quotient PSU3(3) supplies degree7. An extension by an outer involution would not be perfect. |
| XV | The quotient PSU4(3) supplies degree189. An extension by an outer involution would not be perfect. |
| XVI | The quotient J2 supplies degree63. |
| XVII | The quotient PSL3(4) supplies degree20. An extension by an outer involution would not be perfect. |

Consequently K≅A7. All listed ordinary-degree witnesses and the precise classification scope survived the fresh nonauthor audit. The source extraction and primary receipts accompany this note. The exact parser check now verifies nine ordinary tables, three reconstructed A7-cover square sums, and all ten forbidden-degree witnesses; this is arithmetic/source-data verification, not an independent proof of the classification. An important distinction: degree20 is **not** being claimed as an ordinary degree of the simple PSU4(3). It occurs in covers, but the simple quotient's witness here is189.

## 4. Counting distinct kernels forces the whole direct product

The r degree-six characters of H give r epimorphisms to A7 with pairwise distinct kernels. Indeed A7 has exactly one irreducible character of degree6, so any two degree-six characters with the same kernel would coincide after passage to H/N≅A7.

Let N_1,…,N_r be these kernels. The diagonal map

\[
 H\longrightarrow\prod_{i=1}^{r}H/N_i\cong A7^r
\]

is surjective. Here is the standard elementary subdirect-product argument, to avoid assuming that pairwise projections suffice for arbitrary groups. Induct on r. Projecting onto the first r−1 simple factors is surjective by induction. The kernel of this projection has image in the last simple factor that is normal, hence is either the whole factor or trivial. In the former case the entire product is obtained. In the latter case the image is the graph of a surjective homomorphism A7^(r−1)→A7. The images of the individual direct factors are commuting normal subgroups of the simple group A7. Exactly one can be nontrivial; its map is an automorphism, and the other factor maps are trivial. Thus the last quotient map has the same kernel as one of the first r−1 quotient maps, contradicting distinctness.

Therefore |H|≥2520^r. Equality of the degree multisets already gives |H|=2520^r, so the diagonal epimorphism is an isomorphism. This proves the restricted theorem. The finite-linear-classification scope, every case elimination, the ordinary-character data, and the subdirect-product argument have survived a fresh nonauthor adversarial review; the theorem still depends on the established external classification and external primary character tables.

## 5. Scope and open work

- This family does not include arbitrary radical-free groups, arbitrary products of different simple factors, or overgroups permuting their socle factors. Mixed A5/A7 products already admit24=4·6 and20=4·5, and with enough factors admit63=3·21 and189=3²·21. Thus the decisive forbidden-degree set disappears in that larger family; it cannot be retained by an unsupported socle induction.
- The proof does not rely on an abelian-normal-subgroup arithmetic contradiction; Section5 of the companion Clifford note shows that the latter route already admits artificial central-packet data for A7^3.
- No claim that this theorem is original is justified before an extensive direct-power recognition priority audit. It might be a consequence of existing recognition work under different terminology. The parent's bounded independent screen found no all-r A7 theorem, but the full text of Hawkes (1994) was inaccessible; this leaves a concrete priority gap, not evidence of novelty.
- No manuscript or upload should be prepared as a solution of21.135 on the basis of this restricted theorem alone.

## Primary references being checked

J.H.LindseyII, *Finite Linear Groups of Degree Six*, Canadian Journal of Mathematics23(5) (1971),771–790, DOI [10.4153/CJM-1971-086-x](https://doi.org/10.4153/CJM-1971-086-x), Section3 theorem. The introduction acknowledges historical gaps filled by its references16–17; it does not leave those gaps as unproved assumptions in the stated final classification.

The GAP Character Table Library1.3.11, distributed by its maintainer at [the primary library website](https://www.math.rwth-aachen.de/~Thomas.Breuer/ctbllib/), ordinary tables originating in the ATLAS of Finite Groups. The actual ordinary first-column witnesses, including covers and simple quotients, must be checked individually rather than inferred from modular Brauer degrees or from a combined decomposition matrix without tracking kernels.

Primary source-data verification: run `python3 check_primary_degree_witnesses.py` from this directory (or use its absolute path). The generator reads raw ordinary MOT identity columns and projective ARC rows from the hashed CTblLib archive, resolves Galois references by degree, and checks every full simple table's degree-square sum. It reconstructs the2.A7,3.A7,6.A7 multiset sums from the projective rows with the appropriate numbers of central-character sectors. The authored result primary_degree_witnesses.json preserves the exact integers; no modular Brauer degrees enter this test.
