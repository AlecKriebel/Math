# Prior-resolution certificate: KR pole orders and graded extensions

Problem 30004878 / OWR-8415354-004. Checked 9 October 2026.

## Verdict

**The precisely identified source conjecture has a prior resolution in a September 2026 preprint.** Cao, Fujita and Murakami (CFM), *Partial F-invariants and cluster categorifications*, arXiv:2609.08781v1, Theorem 6.32, equation (6.14), proves the equality in Fujita and Murakami (FM), Conjecture 5.17, equation (5.12), after the convention changes below. Theorem 6.27 supplies the matching denominator formula, including its non-simply-laced corrections. This is a source-identification and applicability certificate, not a new proof or an independent verification of every argument in the 82-page preprint.

The conclusion covers all finite simple types and positive KR lengths in FM's untwisted, generic-quantum-parameter, integer-spectral-shift formulation. The apparent restriction to one parity component in CFM does not leave a residual case of that formulation: simultaneous shifts and the vanishing between components cover it. It does not certify arbitrary ungraded Ext, root-of-unity specialization, arbitrary simple modules, or every possible twisted variant of the abbreviated corpus question.

As checked, arXiv lists only v1, submitted 8 September 2026, with no journal reference. Fujita's institutional publication profile also lists CFM as a preprint. The appropriate status is **prior resolution in a preprint, exact source scope matched**, rather than either “still open” without qualification or “journal-validated solution.”

## 1. Identification of the intended statement

The public OWR source is Fujita's talk, joint with Murakami, in *Mini-Workshop: Three Facets of R-Matrices*, OWR 18 (2021), no. 4, pp. 2791–2825, DOI 10.4171/OWR/2021/51. The relevant discussion is on printed pp. 2804–2805, with Conjecture 2 on p. 2805. The report was published on 26 November 2022; that date is distinct from the workshop/report year.

The conjecture explicitly refers to Conjecture B of arXiv:2109.07985. In the inspected v3, Conjecture B is Conjecture 5.17. Thus the exact target is identifiable from its primary source. Abbreviated descriptions suppress indispensable conventions, notably the grading and spectral indexing. A dated open-status assessment cannot override a later exact theorem.

Use FM's following formulation. Let g be a complex finite-dimensional simple Lie algebra with Cartan matrix C, minimal left symmetrizer diag(d_i), and lacing number r. For i,j in its finite vertex set I, positive integers k,l, and integers P,S,

\[
 \mathfrak o(V^{(i)}_{k,q^P},V^{(j)}_{l,q^S})
 =\dim_{\Bbbk}\operatorname{Ext}^1_{\widetilde\Pi\text{-gmod}}
       (q^P K^{(i)}_k,q^S K^{(j)}_l).                 \tag{FM}
\]

Here uppercase Ext denotes degree-preserving extensions in the Z-graded category. FM §4.1 has already forgotten the second, t-grading; it has not forgotten the q-grading. Lowercase ext collects all grading shifts and is a different object.

## 2. Hypothesis and convention mapping

| Issue | FM source | CFM resolution and consequence |
|---|---|---|
| Type | Finite simple g; untwisted quantum affine/loop algebra | CFM §5.4 fixes untwisted type X_N^(1), with underlying finite simple g_0. All finite types A, B, C, D, E_6, E_7, E_8, F_4, G_2 are included. |
| Rank | Every ordinary finite rank in those families | No upper-rank restriction in Theorems 6.27 or 6.32; no restriction to classical or simply-laced types. |
| Lengths | k,l any positive integers | Exactly the same; not merely fundamental modules or equal lengths. The inequality k d_i >= l d_j only chooses which symmetric polynomial formula to write. |
| Quantum parameter | Indeterminate q; quantum category over an algebraic closure of Q(q) | CFM §5.2 uses the same generic setting, with a specified realization inside Puiseux series. There is no root-of-unity specialization theorem here. |
| Modules | Finite-dimensional type-1 KR modules and specified shifts | Same class. Reachability is needed by CFM's general theorem, but CFM p. 64 verifies it for every KR module concerned using an initial cluster. It is not an extra unresolved restriction on the KR statement. |
| Lacing notation | r = max d_i | CFM's r^vee is this lacing number in the untwisted setting. CFM's r in X_N^(r) is the affine twist parameter and equals 1 here. Confusing these two r's changes formulas. |
| Root normalization | Minimal left symmetrizer, d_i in {1,r} | CFM normalizes shortest squared root length to 2, so d_i=(alpha_i,alpha_i)/2 is the same minimal symmetrizer. |
| Additive algebra | Graded tilde-Pi with relations (R1),(R2); its degreewise inverse-limit quotient Pi(infinity) | CFM Definitions 6.6–6.7 use the same graded relations and Pi(infinity); Proposition 6.10 identifies the graded category with modules over a two-component covering algebra. |
| GLS type | FM Remark 2.1 identifies Pi(l) with GLS Pi(C^T,lrD^(-1),Omega) | CFM Remark 6.8(i) repeats the Langlands-dual convention. One must not substitute the GLS algebra of C with its original symmetrizer. |
| Ext category | Degree-preserving Z-graded Ext over tilde-Pi | CFM's Hom in a bounded homotopy category is identified with precisely this Ext by the chain in §4 below. Neither ordinary ungraded Ext nor Ext over an arbitrary fixed finite quotient Pi(l) may be substituted. |
| Generic kernels | Explicit finite-dimensional K_k^(i), equal to kernels on a Zariski-dense family of maps | CFM's fixed path maps produce exactly the corresponding kernels. “Generic” is about this presentation, not an exclusion of exceptional spectral ratios. |
| Spectral shifts | All P,S in Z | CFM initially writes vertices in one parity component; §3 below accounts for both components and all P,S. |
| Coefficient fields | FM's algebra calculations begin over an arbitrary field; its quantum category is separately in characteristic zero | CFM's additive side is over C. FM Propositions 5.6 and A.1 supply the same field-independent integer dimension formula. This matches the numerical statement; it is not a new positive-characteristic quantum theorem. |

The conventional family ranks are A_n (n>=1), B_n and C_n (n>=2), and D_n (n>=4), together with the exceptional types. Low-rank names identified with another simple type do not introduce additional cases.

## 3. Exact spectral reindexing and the parity bridge

FM's centered KR polynomial at node i has exponents

\[
 P-(k-1)d_i,\ P-(k-3)d_i,\ldots,\ P+(k-1)d_i.
\]

CFM equation (5.9) defines W^(i)_{k,c} by the ascending string c,cq^(2d_i),...,cq^(2(k-1)d_i). Consequently

\[
 W^{(i)}_{k,q^{p+d_i}}=V^{(i)}_{k,q^{p+kd_i}},\qquad
 P=p+kd_i,\quad S=s+ld_j.                       \tag{1}
\]

CFM Remark 6.29 gives the matching additive identification

\[
 H^0(f^{(i)}_{k,p})\ \longleftrightarrow\ q^{p+kd_i}K^{(i)}_k.
                                                               \tag{2}
\]

Thus there is no stray length-dependent shift between the two sides. Also the exponent in CFM equation (6.9) becomes

\[
 s-p+ld_j-kd_i=S-P.                              \tag{3}
\]

CFM fixes a parity function epsilon with epsilon(i)-epsilon(j) congruent to min(d_i,d_j) modulo 2 on adjacent vertices. Its component has vertices

\[
 \Gamma_0=\{(i,p):p+d_i\equiv\epsilon(i)\pmod 2\}.
\]

For arbitrary FM data put p=P-kd_i and s=S-ld_j. The following is an explicit applicability deduction from CFM Remarks 5.5, 5.20 and the two-component construction preceding Proposition 6.10:

1. If p+d_i and s+d_j have the prescribed parities, apply Theorem 6.32 directly.
2. If both have the opposite parities, shift both spectral parameters by q^(-1) and both additive modules down by one grading degree. The pair now lies in the displayed component. Simultaneous spectral shifts preserve the pole order; simultaneous grading shifts preserve Ext.
3. If the parities differ, the kernels belong to different components of the full covering quiver on I x Z. There are no arrows or extension classes between those components. On the quantum side, after a common shift one module is in C_Z and the other is an odd q-shift of a module in C_Z. CFM Remark 5.20 gives pole order zero because this shift is outside q^(2Z). Both sides vanish.

This exhausts all integer P,S in FM Conjecture 5.17. It does not require a generic spectral separation assumption and includes the spectral coincidences at which the pole order is positive.

Common multiplication of both spectral parameters by an arbitrary nonzero scalar also leaves the pole order unchanged. For independent arbitrary scalar parameters, however, the bare phrase “their graded generic kernels” requires an explicit convention for spectral-orbit labels. This certificate uses FM's precise integer-shift statement, rather than silently inventing that extra convention.

## 4. Why the homotopy-category theorem is the same Ext theorem

The conversion has four steps, all present in the primary sources:

1. **Acyclicity in degree 1.** CFM defines f^(i)_{k,p}: I_{i,p+2kd_i} -> I_{i,p}, in cohomological degrees 0 and 1. Lemma 6.28 says it is rigid, H^0 is finite-dimensional, and H^1 is zero. For these KR complexes, it is therefore an injective resolution of its zeroth cohomology.
2. **Hom equals Ext.** Proposition 6.12 supplies the required Hom-finite abelian category of finitely cogenerated modules and its injectives. Remark 6.31 identifies Hom in K^b(Lambda(infinity)-inj) from f to g[1] with Ext^1 over Lambda(infinity) of their zeroth cohomologies.
3. **Covering-category equivalence.** Proposition 6.10 identifies modules over the full two-component covering algebra with Z-graded Pi(infinity)-modules. Restricting to one component preserves the relevant Ext groups. Remark 6.29 and (2) identify the exact FM objects.
4. **Return to tilde-Pi.** FM Corollary 4.8 says Pi(infinity)-gmod is a Serre subcategory of tilde-Pi-gmod. Therefore Ext^1 over Pi(infinity) agrees with Ext^1 over tilde-Pi for these modules. One is not replacing the algebra merely because the kernels are finite-dimensional.

With (1)–(2), Theorem 6.32 is precisely (FM) for the componentwise cases; §3 then removes the apparent parity restriction.

The word “generic” needs no extra hypothesis here. FM §5.1 defines

\[
 K^{(i)}_k=q^{kd_i}\mathbb D((\widetilde\Pi/\widetilde\Pi\varepsilon_i^k)e_i)
\]

and equation (5.1) gives its short injective resolution. Proposition 5.1 proves the relevant dense-kernel property. FM Remark 5.2's sufficiently negative shift is used to compare with Hernandez–Leclerc's semi-infinite-quiver presentation; it is not a bound on P or S in Conjecture 5.17.

## 5. Exceptional non-simply-laced terms must be retained

Let c-tilde_ij(u) be the coefficients of the Laurent expansion at zero of the inverse q-Cartan matrix. CFM Theorem 6.27 defines a symmetric polynomial F_{i,k;j,l}=F_{j,l;i,k}. For k d_i >= l d_j it is

\[
 F_{i,k;j,l}(q)=q^{kd_i}[l]_{q^{d_j}}
        \sum_{u=0}^{rh^\vee}\widetilde c_{ij}(u)q^u
        -\mathbf1_{\mathcal E}\Delta_{ij}(q),                 \tag{4}
\]

where the condition E is

\[
 g\text{ has type }C_n,F_4,\text{ or }G_2,\quad
 d_i=d_j=1,\quad k=l,\quad r\nmid k.
\]

The theorem includes these cases; they are not omitted hypotheses. In the source node numbering the correction is:

- C_n, 1<=i,j<n, d=(1,...,1,2): Delta_ij(q)=sum_{a=1}^{i+j-n} q^(2n-i-j+2a+2), with an empty sum equal to zero.
- F_4, d=(2,2,1,1): Delta_33=q^4+q^8+q^10+q^14; Delta_34=Delta_43=q^9; Delta_44=0.
- G_2, d=(3,1): Delta_22=q^6.

For k d_i < l d_j, interchange (i,k) and (j,l) to apply (4). CFM Proposition 6.30 identifies the relevant Hom dimension with [F]_(s-p+ld_j-kd_i). Consequently the exact mapped assertion is

\[
 \mathfrak o(V^{(i)}_{k,q^P},V^{(j)}_{l,q^S})
 =\dim\operatorname{Ext}^1(q^P K^{(i)}_k,q^S K^{(j)}_l)
 =[F_{i,k;j,l}(q)]_{S-P}.                         \tag{5}
\]

The ordered pole order in (5) is not the symmetric invariant d(M,N)=o(M,N)+o(N,M), and the coefficient S-P must not be replaced by P-S. FM's lowercase graded ext and inverse-q dimension convention explain this sign (Lemma 5.16).

FM Remark 5.10 already records a gap in an earlier claimed uncorrected denominator formula in part of the C/G exceptional regime. FM's Conjecture 5.17 concerns the Ext formula, which carries the correction through Proposition A.1. CFM resolves that refined statement, not an incorrectly uncorrected all-case product formula.

## 6. Proof dependency and verification level

The inspected proof on CFM p. 64 does not infer the result merely from a denominator table or its abstract. It places each KR module in an initial monoidal cluster, computes its two-entry g-vector, identifies the unique rigid two-term complex using Lemmas 6.23 and 6.28, and applies Theorem 6.24. Proposition 6.30 then identifies the explicit formula. Theorem 6.24, pp. 59–60, passes through finite interval categories, the partial E/F equality, the pole-order formula, and the stabilization result Proposition 6.16.

This audit checked those stated dependencies, the KR-specific passage to Ext, the type and shift conventions, and the exceptional formulas. It did not re-prove the general cluster-categorification theorems, independently validate all cited literature, or mechanically formalize the manuscript. The scope certificate is therefore conditional on the correctness of the cited preprint theorem in the ordinary way a literature-resolution certificate is, and does not constitute a peer-review claim.

## 7. Boundaries and disposition

The following are not certified by this result alone:

- replacing degree-preserving Ext with the total ungraded extension dimension;
- working over a different GLS Cartan/symmetrizer convention without the Langlands-dual conversion;
- replacing the infinite graded algebra by a finite quotient without an Ext comparison theorem;
- changing to a root-of-unity quantum group, or allowing arbitrary non-KR simple modules;
- declaring all twisted types or arbitrary symmetrizable Kac–Moody types solved from this theorem. CFM Remark 6.37 discusses twisted extensions, but the present certificate is for the exact untwisted FM target;
- declaring arbitrary scalar spectral parameters to possess the same Z-graded kernels without specifying orbit labels.

Recommended disposition: record the exact FM/OWR problem as prior-resolved in CFM v1, retaining the preprint qualification and this hypothesis mapping. No new mathematical approach is needed for that target. The original source audit consumed zero new proof-search approaches.

## Primary references

- [OWR report and publication record](https://ems.press/journals/owr/articles/8415354), [official PDF](https://ems.press/content/serial-article-files/46929?nt=1), printed pp. 2804–2805.
- [FM arXiv:2109.07985v3](https://arxiv.org/abs/2109.07985v3), especially §§2.3, 4.1, 4.3–4.4, 5 and Appendix A; [journal DOI](https://doi.org/10.1093/imrn/rnac054). Published in IMRN 2023, no. 8, pp. 6924–6975.
- [CFM arXiv:2609.08781v1](https://arxiv.org/abs/2609.08781v1), especially §§5.2, 5.4, 6.1–6.2; [primary HTML](https://arxiv.org/html/2609.08781v1), [PDF](https://arxiv.org/pdf/2609.08781v1). Preprint submitted 8 September 2026.
- [Fujita's Kyoto University research profile](https://kdb.iimc.kyoto-u.ac.jp/profile/en.0b742c499a4357a5.html), current page inspected 9 October 2026, showing CFM under preprints and FM under peer-reviewed papers. The page reports a last update of 18 September 2026.
