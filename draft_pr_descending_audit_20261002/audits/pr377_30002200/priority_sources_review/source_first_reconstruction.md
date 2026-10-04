# Sealed independent source-first reconstruction

This reconstruction was prepared before reading the PR, candidate files, repository problem entry, root research, or sibling research. It addresses the initial source/priority family only. Its result is literature closure of the original question, not an acceptance or promotion decision.

## Literal original question and hypotheses

I fetched the [EMS primary landing page](https://ems.press/journals/owr/articles/12172), downloaded its linked complete report, extracted it into ignored `raw_sources/`, rendered the entire Franz contribution, and visually read printed pages 2954, 2955, and 2956. The report is OWR 49/2012, DOI 10.4171/OWR/2012/49, workshop 30 September-6 October 2012, formally published 7 August 2013. Franz's contribution is joint work with Christopher Allday and Volker Puppe.

It fixes T=(S^1)^r, works with rational equivariant cohomology over R=H^*(BT;Q), and asks whether the nonfree upper bound for **rational Poincare duality spaces** is attained for ranks r>=5. The printed Corollary 2 uses floor((n+1)/2), and the next page uses floor((n-1)/2), although n is not introduced in the contribution and the paragraph immediately quantifies r<=4 and r>=5. Thus I record the literal typo rather than silently replacing the printed symbol. [AFP v2](https://arxiv.org/abs/1111.0957v2), Corollary 1.4 and Proposition 5.12(2), resolve the intended rank threshold as j>=r/2. The exact nonfree maximum is therefore floor((r-1)/2). The question prescribes no minimum manifold dimension, no effective/faithful action, no integral coefficients, and no elementary abelian group variant.

The report only says the space satisfies mild conditions. AFP v2 provides the checkable technical interpretation: Hausdorff, second-countable, locally compact, locally contractible T-spaces; finite-dimensional cohomology of the T-pairs considered; characteristic-zero coefficient field for the orbit-filtration theorem; finite-dimensional X; finitely many identity components of isotropy groups; and locally contractible orbit skeleta. The PD condition means nonempty connected X with a distinguished top-dimensional homology class whose ordinary cohomological pairing is perfect (AFP Section 3.5). Compact connected oriented smooth manifolds satisfy the necessary conditions. The upper bound does not itself require an effective action.

## Reconstruction of the answer

Set m=floor((r-1)/2), choose a,b>=1, and let ell have 2m+1 coordinates equal to one and the other r-(2m+1) coordinates zero. Define

X_{a,b}(ell) = {(u_j,z_j) in (C^a x C^b)^r : |u_j|^2+|z_j|^2=1 for each j, sum ell_j u_j=0}.

The torus rotates z_j independently. Genericity says that no subset sum of ell equals its complementary sum. For this ell, the total sum is odd, so equality is impossible, even in the presence of zero coordinates. **Zero length does not mean zero circle action.** In fact u_j=0 and any unit z_j give a point in X with trivial stabilizer. Thus the action is effective and has a free orbit.

Here is an independent smoothness check. A nontrivial real linear dependence of the constraint gradients has coefficients lambda_j on the norm constraints and a real linear functional represented by w in C^a on the closing constraint. Its z_j components give lambda_j z_j=0, and its u_j components give 2lambda_j u_j+ell_j w=0. If w=0 then lambda_j=0 by |u_j|^2+|z_j|^2=1. If w is nonzero, every positive-length coordinate must have z_j=0, unit u_j parallel or antiparallel to w, and the closing equation would force a signed sum of the positive ell_j to vanish. That contradicts genericity. For zero-length coordinates the norm gradient is independently nonzero. The defining map consequently has full rank r+2a. Its ordered invariant constraints orient the normal bundle in an oriented ambient real vector space; the regular fibre is oriented, compact, and has dimension (2a+2b-1)r-2a. Connectivity follows by scaling u to zero and continuously enlarging the nonzero z_j; when a z_j initially vanishes one can choose a unit direction in C^b. The u=0 locus is a product of connected spheres. These are checkable PD witnesses.

For r=2m+1 the short subsets are exactly those of size <=m. Franz's [corrected v4](https://arxiv.org/abs/1403.4485v4), Proposition 5.1, identifies the equivariant module as a sum of free modules and graded Koszul syzygies K_{b,m} and K_{b,m+2}. The Koszul complex on t_1^b,...,t_r^b is exact because these form a regular sequence, and its differentials vanish on tensoring with R/(t_1,...,t_r). Thus its last Tor is nonzero; the m-th syzygy has projective dimension r-m and exact syzygy order m. The appearance of K_{b,m} gives the required obstruction to higher order and to freeness. AFP supplies the matching universal upper bound, independently of the graded shifts.

For even r=2m+2, the leading zero splits X as S^{2a+2b-1} x X_{a,b}(1,...,1), with the new circle acting on C^b in the sphere. The equivariant sphere cohomology is free over its one-variable polynomial ring: its fixed sphere S^{2a-1} has the same total Betti number two, or equivalently the Serre spectral sequence has zero Euler differential because the representation has a trivial C^a factor. Tensoring the odd-rank module with this nonzero free module preserves a syzygy sequence and preserves the failure of a regular sequence of length m+1. Franz Lemma 5.2 and Corollary 5.3 state this explicitly, including arbitrary additional zero coordinates and every lower order m with r>=2m+1. Therefore all ranks r>=5 are covered; r=5 and r=6 both have maximum order 2, r=7 and r=8 maximum order 3, and so on.

The more general [Franz-Huang published 2020 paper](https://msp.org/agt/2020/20-5/agt-v20-n5-p12-s.pdf), Theorems 1.2 and 3.2, proves syzord H_T^*(X(ell))=mu(ell)-1 for **every generic length vector**, characteristic-zero field and p,q>=1. Here sigma_ell(J) counts the short facets of a long J, and mu is the minimum positive such count. For the padded odd vector, the only long subsets with a positive count have m+1 positive coordinates, and all those positive removals yield short subsets. Hence mu=m+1 directly. The full formula is stronger than needed for original closure and must not be credited as the first sharpness result. Its proof reduces to the long-simplex Koszul quotient and verifies all coordinate sequences shorter than mu using the localizing-set criterion. The induction replaces a hypothetical torsion representative of maximal shortest-face length by one with greater length or fewer monomials, contradicting its extremal choice. The source's technical hypotheses for the localizing criterion are stated on printed page 2661.

## Priority and source version distinction

| Event | Primary evidence | Effect on original question |
|---|---|---|
| 3 November 2011 | AFP arXiv v1 record, referenced in OWR | Universal rank upper bound predates question report |
| 30 September-6 October 2012 | Literal OWR report cover and contribution | High-rank attainment remains open in that report |
| 6 March 2013 | AFP arXiv v2 record and re-read Cor. 1.4/Prop. 5.12 | Checkable exact threshold and assumptions |
| 7 August 2013 | EMS landing-page publication metadata | Publication date of OWR report, not 2012 workshop date |
| 18 March 2014 | Franz arXiv 1403.4485v1, Theorem 1.2/Prop. 5.1/Cor. 5.3 | Explicit odd and even maximal nonfree examples already present |
| 7 April 2015 | Franz arXiv v3 | Historical prepublication manuscript; graded shift later corrected |
| 16 April 2015 | [OUP publisher metadata](https://academic.oup.com/imrn/article-abstract/2015/24/13379/2363634) | First online journal publication; IMRN 2015 issue 24 pp.13379-13405, DOI 10.1093/imrn/rnv090 |
| 1 April 2019 | [Franz-Huang arXiv record](https://arxiv.org/abs/1904.01051) | General mu formula preprint, not first maximal sharpness |
| 4 November 2020 | MSP published PDF front page | General mu formula published in AGT 20 pp.2657-2675, DOI 10.2140/agt.2020.20.2657 |
| 12 June 2023 | Franz arXiv v4 record; independent v3/v4 page 13 render comparison | Corrects degree shift, leaves the order-m conclusion intact |

I could not obtain the publisher's complete IMRN PDF: the exact publisher article-PDF endpoint returned HTTP 403. Consequently I distinguish direct reading of arXiv v1/v3/v4 from publisher metadata verification; I do not assert a complete publisher-PDF reread. The actual published MSP PDF explicitly cites Franz 2015 Corollary 6.4 for the already known maximal classification. This supplies published primary corroboration of the historical sharpness result.

The corrected K_{b,m+2} shift is (m+2)d-2*dbar-1, where d=2a+2b-1 and dbar=2a-1. The old shift (m+1)d-dbar+1 differs by 2b-2, so b=1 conceals the error. The v4 correction has no effect on ungraded syzygy order. Do not present v4 as a 2015 source file or the 2023 correction as the date of original closure. The 2014 v1 has a separately overstrong displayed mu<=r/2 inequality; odd equilateral mu=m+1 falsifies it, while its explicit order-m theorem is unaffected.

## Nearby variants and exact limits

* Franz Question 7.5 asks for smaller dimension than 6m+1 for maximal order m>=2. It is a different question. Choosing a=b=1 attains dimension 3r-2, which is 6m+1 at minimal rank 2m+1, but proves no global minimality for m>=2.
* [Franz's current primary corrections page](https://math.sci.uwo.ca/~mfranz/papers.html) says Proposition 7.4 requires an effective T-action. The printed arXiv v4 statement still omits this requirement. Thus dim X>=2r+1 cannot be exported to ineffective actions: append trivial circle factors to a torsion-free nonfree rank-three example to produce a direct counterexample. This correction is irrelevant to the main sharpness result, whose displayed witnesses are effective.
* Rational coefficients are included in all relevant characteristic-zero results. Integral coefficient and positive-characteristic/real (Z_2)^r variants need separate hypotheses and arguments; the 2020 real-case Theorem 5.4 assumes p>1 and characteristic 2.
* A proof by published theorem application is literature verification, not a new sharpness discovery. Counts of finite exact computations cannot replace the all-rank theorem, smoothness proof, or cohomology identification.

## Falsifiable controls sealed before candidate access

The adjacent independent script has no candidate imports. It enumerates all subsets for all padded odd families in ranks 1-15, rejects even equilateral tied vectors, checks zero-vector degeneracy, compares permutations of a nonequilateral generic vector, and tests 48 separately derived graded-shift identities including b=2 (which exposes the old shift). Full stdout/stderr and a hash seal preserve the executed result. These finite checks are falsifiers of arithmetic/scope errors, not a proof of the mathematical theorem. The exact all-rank deduction and its literature credit are written above.
