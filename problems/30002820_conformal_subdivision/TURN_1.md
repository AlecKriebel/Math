# Turn 1: ordinary midpoint refinement preserves only global similarities

Problem 30002820. First substantive author turn. **The original nontrivial subdivision question remains unresolved.** This turn settles one precise natural scheme: isometric Euclidean 1-to-4 midpoint refinement. It neither repairs the source's missing metric-compatibility axioms silently nor disproves the existence of every other scheme.

## 1. Exact restricted setting

Let T be a finite connected triangulated surface, possibly with boundary, with nondegenerate Euclidean face metrics lambda and mu. Every edge length is positive and every face satisfies the strict triangle inequalities. Let M(T) be the usual midpoint subdivision: insert one midpoint m_ij in each old edge ij and divide each old triangle into its three corner triangles and one central triangle. Equip M(T) with the metric induced from the original piecewise Euclidean surface. Thus

    lambda′_(i,m_ij)=lambda′_(j,m_ij)=lambda_ij/2,
    lambda′_(m_ij,m_ik)=lambda_jk/2                         (1)

in every face ijk, and similarly for mu. These are genuine isometric subdivisions, compatible across shared edges.

**Theorem.** The refined metrics lambda′ and mu′ are discretely conformally equivalent if and only if mu=t lambda for a single constant t>0 on all old edges.

No conformal-equivalence hypothesis on the original pair is needed for this theorem. In particular, the ordinary midpoint scheme does not preserve arbitrary original discrete conformal classes; it separates every pair of original metrics which are not globally homothetic.

## 2. Proof by vertex scale equations

Suppose there are refined vertex factors v_a∈R with

    mu′_ab/lambda′_ab=exp((v_a+v_b)/2).

Put w_ij=2log(mu_ij/lambda_ij) for old edges. The two equal half-edge ratios in (1) give

    v_i+v_(m_ij)=w_ij=v_j+v_(m_ij),

so v_i=v_j on every original edge. The original 1-skeleton is connected, hence all old-vertex values equal a common c. Consequently

    v_(m_ij)=w_ij−c.                                      (2)

On an interior midpoint edge in face ijk, formula (1) gives

    v_(m_ij)+v_(m_ik)=w_jk,

and therefore

    w_ij+w_ik−w_jk=2c.                                    (3)

Writing (3) at all three old vertices of the face and subtracting pairs of equations makes w_ij=w_ik=w_jk. Equation (3) then makes their common value 2c. Every old edge lies in a face, so every w_ij=2c. Thus mu_ij/lambda_ij=exp(c), independent of the edge.

Conversely, if mu=t lambda then every new edge length in (1) has the same ratio t. Taking v_a=log t at every refined vertex proves discrete conformal equivalence. This completes both directions.

The argument is local plus connectedness; it does not require orientation, a planar embedding of the whole surface, uniform angle bounds, or a closed surface. On a disconnected pure triangulated surface it gives one independent homothety constant per connected component; a single global constant would then be an unjustified strengthening.

## 3. The new conformal invariants encode old triangle shape

The same obstruction has a direct cross-ratio form. Inside an old triangle ijk the refined edge m_ij m_ik is shared by the corner and central triangles. The positive edge-length ratio

    Q_i = (lambda′_(i,m_ik) lambda′_(m_ij,m_jk)) /
          (lambda′_(i,m_ij) lambda′_(m_ik,m_jk))
        = (lambda_ik/lambda_ij)²                           (4)

is invariant under arbitrary refined vertex scaling, because each of its four vertex factors occurs once in numerator and denominator. Thus midpoint refinement records old side ratios as new conformal invariants. This is consistent with the credited length-cross-ratio characterization of Bobenko–Pinkall–Springborn, Proposition 2.3.2, but(4) can be checked by cancellation alone.

## 4. Exact nonuniform conformal input that fails

Take one triangle with lambda_12=lambda_23=lambda_31=1. Use positive vertex multipliers a_1=3/2,a_2=a_3=1 and define mu_ij=a_i a_j lambda_ij. Then

    (mu_12,mu_23,mu_31)=(3/2,1,3/2).

Both input triangles are nondegenerate. They satisfy the source's conformal condition with u_i=2log a_i. At vertex 2, ratio (4) is 1 for lambda but 4/9 for mu. Hence the induced midpoint refinements are not discretely conformally equivalent. This is an exact rational-length example, not a floating-point failure of a solver.

More generally, on any fixed finite triangulated surface, sufficiently small nonconstant vertex scalings of any strict input metric remain valid metrics. They normally change some old edge ratio, and the theorem excludes their midpoint refinements from one conformal class. The first sentence uses openness of the finite set of strict triangle inequalities; no uniform neighborhood for arbitrary infinite meshes is asserted.

## 5. What this does and does not settle

Bauer's OWR 13/2015 question, printed 721–722, asks for existence of a scheme, not whether the ordinary midpoint scheme works. The theorem rules out exactly this induced-metric 1-to-4 rule. It is not a nonexistence proof for metric-dependent insertion positions, other combinatorics, non-isometric rules, limit-conformal schemes, or every barycentric-type construction. The source definition's lack of an explicit metric-compatibility/nontriviality clause remains documented in SOURCE_GATE.md; identity and constant-output maps are not treated as meaningful solutions.

The positive-vertex-scaling definition and old length-cross-ratio theory are credited to Luo and Bobenko–Pinkall–Springborn. Primary sources: https://ems.press/content/serial-article-files/46561 ; https://arxiv.org/abs/1005.2698 ; Luo's cited paper DOI https://doi.org/10.1142/S0219199704001501 . No historical novelty assertion is made for this elementary obstruction.

The exact checker constructs the refined metric combinatorially and solves conformal compatibility using rational squared vertex factors, avoiding numerical logarithms. Finite controls supplement the theorem; they do not establish universal nonexistence of other schemes.

Original unresolved 1/5. Subjective completion estimate toward the meaningful general question: 5%.
