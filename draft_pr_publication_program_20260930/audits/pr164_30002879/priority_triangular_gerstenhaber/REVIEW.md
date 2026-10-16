# Independent triangular / EI-category priority review

Audit UTC date: 2026-10-12. Literature cutoff: 2026-10-12. Project disclosure supplied by parent: 2026-09-30. Candidate pin: `db79e3c12fb044df91934137dcacd9473460eedefc6f9043e682986c96c0e66b`, 13,500 bytes. This review addresses scientific overlap, not repository operations or a global priority certificate.

**Result: an exact pre-disclosure full Gerstenhaber computation has been located and compared.** Long, Shi and Zhou, [arXiv:2609.19560v1](https://arxiv.org/abs/2609.19560v1), Theorems 7.1 and 8.3, give the same cup product and complete ordinary degree -1 Lie bracket for the exact algebra over every characteristic-two field. Their official arXiv submission history gives 2026-09-17 01:41:24 UTC. The compact subalgebra realization and the explicit original coefficient-map identification in the candidate use a different route; they do not restore first-discovery priority for the full Lie computation.

## 1. Independence and exact scope

`FIRST_ASSESSMENT.md` and `FIRST_ASSESSMENT_SEAL.json` were sealed mode 0444 at 2026-10-12T09:47:40.097593+00:00, before any author/prior review, root conclusion, or sibling priority result was read. None of those conclusions was read later either. The parent was promptly notified of the independently located concrete prior result only after this seal. Four neutral input files are pinned in `INPUT_PINS.json`; copies and all third-party bodies are private.

The precise target is

\[
A=K[x,y]/(x^2,y^2),\quad M=A/(y),\quad
B=\begin{pmatrix}A&M\\0&K\end{pmatrix},\qquad \operatorname{char}K=2.
\]

It claims

\[
HH^*(B)\cong L=K+(y,u)R,\quad R=K[x,y,u,v]/(x^2,y^2),
\]

with degrees 0,0,1,1 and bracket

\[
[F,G]=F_xG_u+F_uG_x+F_yG_v+F_vG_y.
\tag{P}
\]

The source question is Hermann's Question 5, OWR24/2015, printed p.1363, physical PDF page 47. I inspected its complete relevant printed page, including Lemma 4 and the coefficient long exact sequence. It asks for the precise Lie structure and use of that sequence. Ordinary bracket scope is distinct from characteristic-two squaring and higher braces.

## 2. Exact algebra identification, including orientation

Long--Shi--Zhou (LSZ), printed pp.2 and 11, define their Xu--Snashall algebra

\[
\Lambda=KQ/(a^2,b^2,ab-ba,ac),
\]

where a,b loop at vertex 1 and c goes from 1 to 2; paths concatenate in the convention in which ac is defined. Their Lemma 3.1 gives the basis

\[
e_1,e_2,a,b,c,ba,bc.
\]

An explicit algebra isomorphism to the candidate's upper triangular B is

\[
e_1\mapsto\operatorname{diag}(1,0),\quad
e_2\mapsto\operatorname{diag}(0,1),\quad
a\mapsto y,\ b\mapsto x,\ c\mapsto 1_M,
\]

with a,b in the upper-left corner and c in the upper-right. Then ba maps to xy and bc to x in M. The relation ac=0 is exactly yM=0; b acts nontrivially on M. This preserves all four displayed relations and gives all seven basis elements, so the surjective map is an isomorphism. It is the nontrivial permutation module, not a two-dimensional trivial module.

Xu Section 3.1 and Hermann Section 9.6 give g swapping the two arrows and h fixing them. Thus x=g-1 is nonzero and y=h-1 annihilates the arrow module. Under Hermann's f*g=f composed with g convention, the category algebra itself is lower triangular. Its opposite is B; reversal signs disappear in characteristic two. The direct quiver-to-B identification above avoids depending on the orientation typo in Hermann's printed Lemma 9.7.

LSZ state throughout that K is a base field, and Section 3 explicitly begins with a field K. Theorem 8.3 requires only Char(K)=2. There is no algebraic-closure or finite-field restriction. This quantifier matches the candidate; Oke's earlier accepted paper, by contrast, declares an algebraically closed field in its introduction even where later theorem statements say a field.

## 3. Complete cup-product dictionary

To avoid confusing LSZ's countable generators with the candidate's x,y, write their generators as X_{n,r}. Define in L

\[
Y_n=yv^n,\quad Z_n=xyv^n\quad(n\ge0),\qquad
U_n=uv^{n-1},\quad T_n=xuv^{n-1}\quad(n\ge1).
\]

The dictionary is

| LSZ Theorem 7.1 generator | Image in candidate L | Range |
|---|---|---|
| X_{n,1}=[f^n_{0,3}] | Y_n | n>=0 |
| X_{n,2}=[f^n_{0,6}] | Z_n | n>=0 |
| X_{n,3}=[f^n_{1,1}] | U_n | n>=1 |
| X_{n,4}=[f^n_{1,4}] | T_n | n>=1 |
| 1=[f^0_{0,1}+f^0_{1,2}] | 1 | degree 0 |

Their coefficient basis is z_3=a=y, z_4=b=x, z_6=ba=xy. The loop-resolution index l counts b occurrences. Consequently, more generally, the surviving basis classes f^n_{l,j} map to z_j u^l v^{n-l}. LSZ Section 4, printed pp.20--23, has l=0 only for j=3,6 and 1<=l<=n for j=1,3,4,6. This is exactly the candidate's basis.

Every family of relations in Theorem 7.1 is checked symbolically:

- Y_mY_n=Y_mZ_n=Z_mZ_n=0, since y^2=0.
- Z_mT_n=0 and Z_mU_n=Y_mT_n, by x^2=0 and ordinary multiplication.
- T_mT_n=0; Y_mU_n=Y_0U_{m+n}, Y_mT_n=Y_0T_{m+n} for m,n>=1.
- U_mU_n=U_1U_{m+n-1} and U_mT_n=U_1T_{m+n-1} for m>=2,n>=1.

Thus the dictionary induces a ring map from LSZ's K[X]/J into L. It is onto: for a monomial x^a y^b u^i v^j with i>=1, use U_1^{i-1}U_{j+1} if a=0 and U_1^{i-1}T_{j+1} if a=1, and multiply by Y_0 if b=1. For i=0, allowed nonconstants are Y_j and Z_j. The unit is separate. Both rings have dimensions 3 in degree zero and 4n+2 in degree n>=1 (LSZ Section 4; the candidate's direct monomial count). The degreewise onto map is therefore one-to-one. This proves all-degree cup-product equivalence, rather than an identification only modulo nilpotents.

## 4. Complete bracket comparison

The following identities are independently derived by substituting the four families into (P). They list every unordered pair of positive-degree generator families; integer coefficients are reduced modulo two. Set d=m+n-1.

| Pair, m,n>=1 | Bracket derived from (P) | LSZ Theorem 8.3 entry |
|---|---|---|
| Y_m,Y_n | (m+n)Y_d | 2(a), j=1 |
| Y_m,Z_n | (m+n)Z_d | 2(a), j=2 |
| Y_m,U_n | (n-1)U_d | 2(b), j=3 |
| Y_m,T_n | (n-1)T_d | 2(b), j=4 |
| Z_m,Z_n | 0 | 2(c), first |
| Z_m,T_n | Z_d | 2(c), second |
| Z_m,U_n | Y_d+(n-1)T_d | 2(d) |
| U_m,U_n | 0 | 2(e), first |
| T_m,U_n | U_d | 2(e), second |
| T_m,T_n | 0 | 2(e), third |

For example the two terms of [Z_m,U_n] come from the x/u and y/v pairs separately. This explains exactly LSZ's n odd/even cases; it is not merely a parity or dimension comparison. Characteristic-two symmetry supplies the reverse order. The Poisson identity supplies brackets of all cup products. Since Section 3 showed these generators span the ring multiplicatively, all elements and all degrees are covered.

Degree zero cannot be skipped. Its nonconstant generators are Y_0=y and Z_0=xy; x alone is absent. For m>=1, direct differentiation gives

\[
[Y_m,Y_0]=mY_{m-1},\quad[Z_m,Y_0]=mZ_{m-1},
\]
\[
[U_m,Y_0]=(m-1)U_{m-1},\quad[T_m,Y_0]=(m-1)T_{m-1},
\]

where both latter expressions are zero for m=1 and require no nonexistent U_0 or T_0. Against Z_0,

\[
[Y_m,Z_0]=mZ_{m-1},\quad[Z_m,Z_0]=0,
\]
\[
[U_1,Z_0]=Y_0,\quad[U_m,Z_0]=Y_{m-1}+(m-1)T_{m-1}\ (m\ge2),
\]
\[
[T_m,Z_0]=Z_{m-1}.
\]

These are precisely 8.3(1b)--(1e). The unit brackets to zero as in 1(a); degree-zero/degree-zero brackets are zero because their target degree is -1. LSZ's complete printed p.41 was rendered and visually checked against this transcription.

`private/compare_lsz.py` independently implements formal differentiation in F2[x,y,u,v]/(x^2,y^2) and a manual transcription of the LSZ table. It checks 5,926 identities at index bound 16, including every nontrivial degree-zero family, every positive pair, every ring-relation family, and generator spanning through degree 16. It passed. These finite checks are diagnostics for transcription; the identities above prove equivalence for arbitrary indices and every characteristic-two field. They do not certify LSZ's entire Anick-resolution proof or the candidate's entire cochain proof.

## 5. The original coefficient map gamma and what is distinct

LSZ construct an Anick resolution and comparisons with a reduced bar resolution. I found no statement in their full text of the coefficient sequence 0->BeB->B->B/BeB->0, its map gamma, the characteristic map HH*(A)->Ext_A*(M,M), or the formula ker(chi)=(y,u). The full-source search recorded zero occurrences of gamma, stratifying, one-point, one point, characteristic homomorphism, triangular matrix, and restriction; the positive comparison is based on their actual Sections 3--8, not on that search alone.

Accordingly, LSZ explicitly establish the full Lie/cup result, while the candidate explicitly realizes it through the original source's map. The latter has older machinery behind it: OWR p.1363 Lemma 4 already identifies gamma as derived quotient tensor and preserves bracket; Hermann v2 Corollary 6.6 and Proposition 6.12 give triangular/one-point restriction as a strict Gerstenhaber morphism; Lemma 6.9 identifies the characteristic component by tensoring; Theorem 8.11(1) gives the coefficient sequence's structural morphism.

Moreover, LSZ's surviving cochain basis already makes the corner restriction image visible: restrict to all loop inputs, and the mixed-input boundaries disappear. The surviving f^n_{l,j} classes restrict to the monomial basis above. Thus injectivity and image L can also be derived by combining that displayed basis with the pre-existing structural comparison. This is an unstated consequence/different proof, not a prior explicit LSZ theorem called gamma. The candidate's small characteristic-map derivation may be useful exposition, but novelty of that derivation or of the explicit image statement is **not established** by this review. The full bracket itself is exact prior work.

## 6. Weak and strong nilpotent ideals

This independently addresses the separate conditional strong-ideal quotient mentioned by the parent. In L the homogeneous nilpotent ideal is

\[
N=L\cap(x,y)R.
\]

The quotient is K+uK[u,v]. It is not finitely generated: the classes uv^j are linearly independent in its augmentation ideal modulo its square. Differentiating two elements of N leaves at least one nilpotent coefficient factor, so [N,N] is contained in N. Thus the weak Gerstenhaber ideal generated by N equals N.

For the strong Gerstenhaber ideal G, each T_n=xuv^{n-1} lies in N and

\[
[T_n,U_1]=U_n\qquad(n\ge1).
\]

Hence G contains all four nonconstant generator families and is (y,u)R inside L. Conversely that augmentation ideal is bracket-stable and no generator bracket has a scalar constant term, so G cannot contain 1. Therefore L/G=K. This agrees exactly with LSZ Theorem 8.6(2), printed p.42, not merely with its abstract. It also agrees with their proof using [X_{m,4},X_{1,3}]=X_{m,3}.

The ambient group-algebra strong quotient in Hermann Section 9.4 is zero, because x is available there and [u,x]=1. In L, x is absent from degree zero, so the corresponding quotient is K. Transferring the ambient zero quotient into B would be invalid. The candidate's ordinary bracket claim does not compute a restricted squaring operation, and neither this comparison nor the nilpotent-ideal conclusion should be promoted as one.

## 7. Other primary texts and their exact overlap

All obtained full bodies and text extractions are private. Source fetch records contain URLs, UTC times, byte counts and SHA-256 pins. The classification below uses actual full texts where stated, with focused theorem/section comparison and full-source lexical sweeps; inaccessible full texts are marked explicitly.

| Source and locator | What was verified | Classification for this target |
|---|---|---|
| Xu, [0805.3295](https://arxiv.org/abs/0805.3295), Section 3.1, pp.14--17 | Exact two-arrow action; ring decomposition and nilpotent quotient | Exact prior ring and nonfinite-generation computation; not a full target Lie table |
| Hermann, [1411.0836v2](https://arxiv.org/abs/1411.0836v2), Sections 6.1, 9.4, 9.6; Cor.6.6, Prop.6.12, Thm.8.11 | Full ambient bracket; strict Gerstenhaber structural maps; exact algebra and open questions | Prior machinery and ambient computation; not explicit target image/table there |
| Guccione--Guccione, [math/0104068](https://arxiv.org/abs/math/0104068), Theorems 1--3 | General triangular LES; restriction and characteristic components are graded ring maps; connecting image annihilator | Prior sequence/ring structure, no target full Lie computation in this fetched text |
| Michelena--Platzeck, [DOI 10.1006/jabr.2000.8423](https://doi.org/10.1006/jabr.2000.8423), full CONICET copy, Sections 1--2 | Two LES with hypotheses; Happel sequence explicitly recalled | Prior groups/sequence machinery; no target Lie computation in this text |
| Green--Solberg, author-hosted [2001 preprint PS](https://oyvinso.folk.ntnu.no/Papers/preprint28062001.ps), Theorem 2.1 | General triangular ring maps; characteristic component ring map; connecting image annihilator | Prior ring machinery; no Lie table; extracted fonts are imperfect, theorem also visually reproducible from preserved PS-derived PDF |
| Cibils--Marcos--Redondo--Solotar, [math/0102194v5](https://arxiv.org/abs/math/0102194v5), Section 6, Thm.6.4, Prop.6.7 | Triangular LES and cup-product description of connecting map | Prior sequences/cup machinery; no full target bracket |
| Dourlens, [math/0112243](https://arxiv.org/abs/math/0112243), relative complex and spectral sequence | Trajectory-based spectral sequence, cup-product differentials; Gerstenhaber--Schack citations concern relative complexes | Prior triangular methods, not a target Lie computation |
| Snashall--Solberg, [DOI 10.1112/S002461150301459X](https://doi.org/10.1112/S002461150301459X), author PS, Sections 1 and 4 | Characteristic HH-to-Ext map, support varieties, nilpotence kernel framework | Prior characteristic-map context, different module/kernel from chi_M in candidate |
| Green--Snashall--Solberg, [math/0401446](https://arxiv.org/abs/math/0401446), Thm.7.3 and Section 7 | Monomial-algebra finite generation; Koszul characteristic image in graded center | Not applicable as a monomial theorem to the binomial ab-ba relation; not a full target bracket |
| Snashall, [0811.4506v2](https://arxiv.org/abs/0811.4506v2), Example 4.1 and Thm.4.5 | Exact quiver; all-characteristic nilpotent quotient; explicit resolution | Exact prior target ring quotient/resolution, no full bracket there |
| Oke, [2004.00780](https://arxiv.org/abs/2004.00780) | Earlier cup-product-only arXiv version | Exact-family ring work; not bracket completion |
| Oke, [Comm. Algebra DOI 10.1080/00927872.2021.1990941](https://doi.org/10.1080/00927872.2021.1990941), accepted author version, Section 5 | q=+-1 weak ideal closure, nonnilpotent brackets and sample nilpotent brackets | Exact-family partial Lie and Hermann weak-ideal result; no complete target table supplied |
| Oke, [2103.12331v1](https://arxiv.org/abs/2103.12331v1), Thms.4.20--4.21, Sections 7.1--7.3 | General homotopy-lifting formulas in terms of scalars; exact-family degree-one/two examples, sample Table 3 | Stronger general computational machinery and partial examples; uncomputed scalars/general applicability cannot be relabeled a closed full target computation |
| Herscovich--Solotar, [math/0608444](https://arxiv.org/abs/math/0608444), Thms.4.2,4.4 | Hochschild--Mitchell Happel/general triangular LES | Prior categorical exact-sequence generalization |
| Santiago-Vargas--Velasco-Paez, [2303.03554](https://arxiv.org/abs/2303.03554), Thm.4.7 and Cor.5.6 | Homological epimorphisms and categorical one-point-extension LES | Recent categorical machinery, no target bracket table |
| Xu, [1105.4731](https://arxiv.org/abs/1105.4731), Sections 3--5 | Transporter support varieties and Quillen stratification | A different, finitely generated transporter-support setting; no target full bracket |
| Happel, [DOI 10.1007/BFb0084073](https://doi.org/10.1007/BFb0084073) | Official bibliographic locator and direct attribution in fetched MP/Guccione/Hermann texts | Original chapter fetch returned HTML rather than PDF; no exclusion asserted from an unread chapter |
| Green--Marcos--Snashall, [DOI 10.1081/AGB-120016764](https://doi.org/10.1081/AGB-120016764) | Official bibliographic record; exact ring-map content recalled in fetched GS/Hermann texts | Original full text unavailable (403); no full-text absence inference |
| Koenig--Nagase, [DOI 10.1016/j.jpaa.2008.10.012](https://doi.org/10.1016/j.jpaa.2008.10.012) | Official locator; coefficient LES attribution and structural strengthening in fetched OWR/Hermann | Direct body fetch blocked; no exclusion from snippets |

The named Wang/Li search route did not return a primary exact-target full bracket source. This is a search limitation, not an assertion about those authors' work. The one-point-extension ring-modulo-nilpotence paper [DOI 10.1007/s11464-016-0553-8](https://doi.org/10.1007/s11464-016-0553-8) was located but full-body access failed; it remains an unresolved ring-level lead. Unrelated special-biserial, skew-gentle, Taft-algebra, monomial and nilpotent-quotient search hits cannot establish an exact target Lie result merely because they mention Xu or Gerstenhaber.

## 8. Chronology, limits, and scientific disposition

The arXiv official HTML and the downloaded PDF/TeX all identify LSZ v1 as 17 September 2026. The official submission timestamp is 2026-09-17 01:41:24 UTC. At the current cutoff, only v1 is displayed in the preserved submission history. This precedes the supplied 30 September 2026 GitHub disclosure by thirteen calendar dates. It is also after the source record's August 2026 triage, so that older triage could not have screened out this newly available exact computation. Oke's journal record gives online publication 21 October 2021, accepted 3 October 2021, and print Comm. Algebra 50 (2022), 1821--1841; the accepted author PDF is dated 5 October 2021. Website crawl dates were not treated as publication dates.

The strongest verified result of this route is a **positive exact prior-art witness**, with a proved coordinate equivalence and all-degree table comparison. This is sufficient to reject first-discovery presentation of the candidate's ordinary full Lie/cup computation. It does not determine the earliest global source, certify absence of an earlier short gamma-image proof, prove plagiarism, or adjudicate independent discovery. A useful publication could clearly credit LSZ for the full result and present the small characteristic-kernel realization as an alternative derivation, with novelty of that derivation still unestablished. There is no central unsupported equivalence gap left in the exact LSZ overlap.

No external individuals were contacted and no outreach was prepared. No Git index, branch, ref, PR, tracker or publication state was mutated. All work remained in this dedicated route directory.
