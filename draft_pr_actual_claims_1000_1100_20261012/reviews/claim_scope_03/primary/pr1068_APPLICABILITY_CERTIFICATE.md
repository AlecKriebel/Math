# Applicability certificate: finite-group Chow nilpotence and suspension

**Authorship and review status:** This authored report was prepared with AI assistance and is unrefereed, with no proof-assistant certification. Its mathematical acceptance is scoped to the explicitly named foundations. This report's status is distinct from the bibliographically confirmed journal publication of Hemminger's prior result.

**Problem ID:** 30002367. **Audit date:** 2026-10-10 UTC.

**Disposition:** The original finite-group conjecture is covered by David Hemminger's prior theorem. This is a credited prior resolution, not a new solution of the target. The applicable field and grading conventions are those of Totaro's actual Conjecture 12.8. The inspected arXiv proof has a centralizer-formula error; the accompanying mathematical audit supplies and checks the block-centralizer descent correction and records additional operation-notation qualifications. The journal publication is independently confirmed, but its full text was not inspected.

## 1. Exact target and its source context

Let p be any prime, k a field with char(k) different from p and containing all pth roots of unity, and G an arbitrary finite abstract group, regarded as the constant algebraic group over k. Set

\[
N=CH^*(BG_k)\otimes_{\mathbb Z}\mathbb F_p.
\]

The grading is codimension: an element of CH^i has degree i. For every elementary abelian p-subgroup E of G, multiplication gives a group homomorphism

\[
\mu_E:E\times C_G(E)\longrightarrow G,\qquad(e,c)\longmapsto ec.
\]

The elementary-abelian Chow Kunneth formula identifies the Chow ring of the product with \(CH_E^*\otimes CH_{C_G(E)}^*\). Define

\[
D_d:N\longrightarrow\prod_{E\leq G}\left(CH_E^*\otimes_{\mathbb F_p}CH_{C_G(E)}^{\leq d}\right)
\]

by these pullbacks followed by truncation **of the centralizer factor only**. Here \(M^{\leq d}=M/M^{>d}\). The trivial elementary abelian subgroup is allowed. All tensor products below are over \(\mathbb F_p\). Put

\[
d_{\rm det}(N)=\min\{d\geq0:D_d\text{ is injective}\}.
\]

Let \(\mathcal U\) be the category of unstable Steenrod modules concentrated in even topological degrees, regraded so topological degree 2i is degree i. For odd p the operations are \(P^a:N^i\to N^{i+a(p-1)}\), with Bockstein zero on this even object. At p=2 the Chow operation usually written \(P^a\) is topological \(Sq^{2a}\), increasing Chow degree by a; odd squares act as zero. Instability in Chow degrees is \(P^a x=0\) when a>|x|. Suspension \(\Sigma^d\) shifts this Chow grading by d and retains the shifted Steenrod action. It corresponds to suspension by 2d after embedding into the topological grading.

The target is

\[
 d_{\rm det}(N)=\max\{d\geq0:\Sigma^dM\hookrightarrow N\text{ in }\mathcal U\text{ for some }M\ne0\}.
\tag{T}
\]

An injection as modules is required. A suspended quotient, a graded-vector-space subspace, or a suspension of an algebra is not an adequate substitute.

The short OWR statement (Burt Totaro, report 32/2013, pp.1898-1899) suppresses field and operation conventions. Totaro's *Group Cohomology and Algebraic Cycles* (2014), section 12.2, p.131, explicitly defines the detection map, states Theorem 12.7 with char(k)≠p and pth roots of unity, and makes Conjecture 12.8 inherit those assumptions. It also explicitly specifies the Chow-degree instability convention. This fixes the intended target; this certificate does not silently assert an extension to fields of characteristic p or fields lacking the required roots of unity.

## 2. Exact prior result

David Hemminger, *Lannes's T-functor and equivariant Chow rings*, arXiv:1911.03033v2, last revised 22 September 2020, section 6, Proposition 6.1 (PDF p.22), proves the equality between his d0(CH_G^*) and the greatest suspension appearing as a nonzero unstable submodule. Section 6 (p.21) explicitly identifies Totaro's detection definition with this d0 using Theorem 5.6. The first paragraph of section 1 (p.3) has exactly the field assumptions above, and section 3 (p.7) specifies the even-degree regrading.

The work was published as *Algebraic & Geometric Topology* 21(4) (2021), 1881-1910, DOI 10.2140/agt.2021.21.1881. Publisher landing-page metadata states 18 August 2021. This audit's mathematical page references refer to the inspected 25-page arXiv v2, not to an uninspected journal PDF. The publisher PDF request returned an access-denied subscription page. Hemminger's openly deposited 2021 UCLA dissertation also states the result as Proposition 2.7.1; it retains the centralizer wording discussed in the audit.

## 3. Hypothesis-by-hypothesis application

1. **Group class.** Hemminger allows linear algebraic groups. A finite constant group is a smooth affine finite-type algebraic group over any field. Its regular permutation representation is faithful, including when char(k) divides |G|. The theorem is not restricted to p-groups, abelian groups, connected groups, reductive groups, or complex representations.
2. **Field.** Both the original precise conjecture and the applicable prior require char(k)≠p and μp⊂k. No algebraic closedness or perfectness is added. The case k=C is included. Characteristic may divide |G| at a prime different from p.
3. **Scheme.** Set X=Spec(k). It is smooth, separated, finite type, quasi-projective, and has a G-equivariant ample line bundle (the trivial one). All fixed loci X^E remain X.
4. **Coefficients.** Hemminger's CH notation is reduced modulo p throughout. It is exactly \(CH^*(BG_k)\otimes\mathbb F_p=CH^*(BG_k)/p\), not the integral Chow ring, p-adic Chow theory, or ordinary singular cohomology.
5. **Centralizers.** The map used by Hemminger is induced by \((e,c)\mapsto ec\). For constant finite groups, its centralizers are the usual finite group centralizers. The product runs over the same elementary abelian p-subgroups. Replacing all subgroups by one representative per conjugacy class changes neither kernel nor injectivity.
6. **Truncation and index.** Hemminger uses centralizer degrees <n. Setting n=d+1 gives exactly degrees ≤d. There is no unit shift in the resulting equality.
7. **Grading and suspension.** His \(\mathcal U\) is the even topological category regraded by one half. Thus \(\Sigma^d\) in the proposition means d Chow degrees, matching Totaro's explicit instability convention. Reading d as d ordinary topological degrees would misstate the target.
8. **Finiteness.** Hemminger's coarse Theorem 6.2(a) gives d0(N)≤n² for an n-dimensional faithful representation (dim X=dim G=0). It suffices for existence of a maximum. This audit does not need the sharper finite-group part 6.2(c), Totaro's sharper bound, or a Noetherianity theorem for N.
9. **Nonzero and boundary cases.** CH^0(BG_k)/p=Fp, so N≠0 and suspension d=0 is available. The trivial group and d0=0 case are included. Nothing assumes p divides |G|. No empty maximum is used.
10. **Unknown finiteness of graded Chow groups.** The argument does not assume each N^i is finite-dimensional or N is a finitely generated Fp-algebra. Hemminger explicitly warns that the topological Noetherian theorem alone is insufficient.

## 4. The non-tautological bridge

The substantial geometric statement is Theorem 5.6: for n≥1, the natural map

\[
\lambda_n:N\longrightarrow Q_n
\]

is localization away from \(\mathrm{Nil}_n\), where \(Q_n\) is an equalizer inside

\[
P_n=\prod_E CH_E^*\otimes CH_{C_G(E)}^{<n}.
\]

The inclusion \(j_n:Q_n\hookrightarrow P_n\) is a monomorphism and

\[
D_d=j_{d+1}\lambda_{d+1}.
\]

Consequently \(\ker D_d=\ker\lambda_{d+1}\). The equality of the detection invariant and the categorical nilpotence invariant follows from this theorem, not by redefining the conjectured left-hand side.

Proposition 6.1 then identifies the categorical invariant with the suspension maximum. The accompanying audit expands both implications and checks the nilpotent filtration index. This yields (T) over the exact original field class.

## 5. Scope of acceptance and limits

Accepted: complete prior applicability to the original finite-group conjecture, with Hemminger credited; a checked account of the target proof and a narrow correction of the arXiv v2 centralizer/descent step; no remaining hypothesis mismatch in (T).

Not asserted: originality of the target theorem; identity of arXiv and publisher PDF bytes; that every printed line of the preprint is correct as written; new results in characteristic p; a theorem for an integral Chow ring; a full independent reconstruction of foundational results about Steenrod operations, Lannes's functor, Brown-Gitler injectives, or the Schwartz nilpotent filtration.

The foundational inputs and the exact scope of the source-proof correction are enumerated in `MATHEMATICAL_AUDIT.md` and `CENTRALIZER_DESCENT_CORRECTION.md`.

## References

- Totaro, OWR report, original discussion pp.1898-1899: https://ems.press/content/serial-article-files/46461?nt=1 ; report DOI https://doi.org/10.4171/owr/2013/32
- Totaro, *Group Cohomology and Algebraic Cycles* (2014), p.131, Theorem 12.7 and Conjecture 12.8: https://doi.org/10.1017/CBO9781139059480 ; inspected primary text hosted by the National Academic Digital Library of Ethiopia: https://ndl.ethernet.edu.et/bitstream/123456789/33006/1/6.pdf.pdf
- Hemminger, inspected manuscript: https://arxiv.org/abs/1911.03033v2 ; https://arxiv.org/pdf/1911.03033v2
- Hemminger, publication metadata: https://msp.org/agt/2021/21-4/p09.xhtml ; https://doi.org/10.2140/agt.2021.21.1881
- Hemminger, 2021 dissertation: https://escholarship.org/uc/item/8c2828rp
