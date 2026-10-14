# Boundary face-number finiteness: an exact later theorem announcement

**Target:** 30001704 / OWR-4798-031.  
**Finding:** the intended connected simplicial/PL boundary question is explicitly answered affirmatively by **Ed Swartz, Oberwolfach Report 24/2012, Theorem 7**, printed p. 1429.  
**Validation status:** exact source and theorem-scope match; **the full proof of the boundary finiteness theorem has not been located or independently validated here**. Separate source review is pending.  
**Research accounting:** zero substantive proof-search attempts; this is a source correction and elementary normalization audit. No campaign discovery or new finiteness theorem is claimed.

## 1. Recovering the question and its category

The original contribution is Ed Swartz's *f-vectors and three-manifold complexity*, in **OWR 8/2011**, printed pp. 409–412. It discusses finite simplicial-complex triangulations. The three-dimensional boundary finiteness statement already appears as Theorem 8(2); the final paragraph asks for its higher-dimensional analogue. It also explicitly distinguishes the nonsimplicial face-gluing triangulations allowed in Matveev complexity. [Full original report](https://ems.press/content/serial-article-files/46323).

Use $D$ for the geometric dimension to avoid the subsequent report's shifted notation. For a finite simplicial triangulation $\Delta$ of a compact manifold with nonempty boundary, put

$$q_D(\Delta)=f_1(\Delta)-D f_0(\Delta)+\binom{D+1}{2}-v_{\mathrm{int}}(\Delta). \tag{1}$$

The intended finiteness question fixes $D$ and a bound $N$, and asks for finitely many underlying manifold types among triangulations satisfying $q_D\leq N$. It does not ask for finitely many triangulations or a computable enumeration algorithm.

The later contribution makes connectedness explicit and states a PL-homeomorphism conclusion. We therefore match the connected simplicial/PL interpretation of the earlier question. We do not silently enlarge it to arbitrary disconnected unions, arbitrary non-PL triangulations, simplicial cell complexes, or noncompact manifolds.

## 2. The affirmative primary statement

Swartz's *Face Enumeration on Manifolds*, **OWR 24/2012**, printed pp. 1427–1429, uses $(d-1)$ for the geometric dimension and assumes throughout that its manifolds are connected. It distinguishes simplicial complexes $\Delta_c$ from semi-simplicial complexes. The complexity minimum on p. 1429 is specifically over $\Delta_c$ and is

$$\Gamma(M)=\min_{|\Delta_c|=M}\bigl(h_2(\Delta_c)-v_{\mathrm{int}}(\Delta_c)\bigr). \tag{2}$$

Its **Theorem 7**, attributed there to “S. '11”, asserts finiteness of PL-homeomorphism types with bounded $\Gamma$, for fixed $d$ and bound. The surrounding section has $d\geq4$, hence geometric dimension at least three. No orientability restriction is imposed in this statement. [Full later report, pp. 1427–1429](https://ems.press/content/serial-article-files/46393).

This is a published primary theorem announcement, rather than a later abstract's inference or an unattributed database status. The contribution does not include its proof. The label “'11” is preserved as the author's attribution; no separate 2011 full-proof publication has been identified here.

### Exact implication for the extracted question

The coefficient of $t^{d-2}$ in the defining identity

$$\sum_{i=0}^{d}h_i t^{d-i}
=\sum_{i=0}^{d}f_{i-1}(t-1)^{d-i},\qquad f_{-1}=1,$$

is

$$h_2=f_1-(d-1)f_0+\binom d2.$$

Set $d=D+1$. Equations (1) and (2) then give

$$q_D(\Delta)=h_2(\Delta)-v_{\mathrm{int}}(\Delta),
\qquad \Gamma(|\Delta|)\leq q_D(\Delta). \tag{3}$$

Thus every connected PL manifold represented by a triangulation with $q_D\leq N$ belongs to the finite list asserted by Theorem 7 with $d=D+1$ and, for example, $G=\max(0,N)$. Finitely many PL-homeomorphism types imply finitely many ordinary homeomorphism types. Conversely, the minimum in (2) is attained: the nonempty set of integer values is bounded below by the nonnegativity result cited in the report. Hence a bound on $\Gamma$ is equivalent to existence of a bounded-$q_D$ triangulation in that category.

This is an exact **deduction from the announced theorem**, not an independent proof of that theorem.

## 3. What full proofs were and were not recovered

### The earlier closed theorem is different

Swartz's *Topological finiteness for edge-vertex enumeration* proves finiteness for connected combinatorial manifolds **without boundary**, with bounded ordinary $g_2$. The full author manuscript was retrieved and its proof read. Its Theorem 2.1 expressly excludes boundary. The correct journal metadata are *Advances in Mathematics* **219**(5) (2008), 1722–1728, DOI **10.1016/j.aim.2008.07.010**. Both OWR reference lists print incorrect volume/year/page data for this title. The author's publication list and Crossref metadata corroborate the correction. The final typeset journal text was not recovered. [Full author manuscript](https://pi.math.cornell.edu/~ebs/Edges.pdf); [author's publication list](https://pi.math.cornell.edu/~ebs/papers.html); [DOI](https://doi.org/10.1016/j.aim.2008.07.010).

The closed proof uses bounds on sums of vertex-link $g_2$ values, face-ring Hilbert-function inequalities, reductions at stacked-sphere links, and decomposition along missing facets. Its boundary generalization requires additional arguments; the earlier closed theorem cannot simply be cited as a proof of (1).

### Later related sources do not remove the present access hold

The relevant sections of Swartz's *Thirty-five years and counting* discuss the boundary invariant $h_2-v_{\mathrm{int}}$ and lower bounds, but no full proof of this bounded-complexity finiteness theorem was identified there. [Author manuscript, §6](https://arxiv.org/abs/1411.0987).

Novik–Swartz's published *g-vectors of manifolds with boundary* develops the completion of a manifold by coning its boundary, face-ring inequalities, equality cases and handle decompositions. Its main statements and relevant §§2 and 7 were inspected. These are valuable related results, but this package does not substitute them for a checked proof of Swartz's announced general finiteness theorem. [Published full text](https://www.numdam.org/item/10.5802/alco.121.pdf).

A bounded search of the author's publication list and related primary literature did not locate the missing full boundary finiteness proof. This is an access/validation limitation, not a claim that no such proof exists or that the announced theorem is false.

## 4. Elementary controls that prevent incorrect transfers

These standard identities clarify the source match; none proves the missing finiteness theorem.

### 4.1 Coning the boundary gives the right number, but can create a singularity

Let $v_b=f_0-v_{\mathrm{int}}$, and form the usual completion

$$\widehat\Delta=\Delta\cup(v_* *\partial\Delta)$$

with a single new vertex. The new edges join $v_*$ to each boundary vertex, so

$$f_0(\widehat\Delta)=f_0(\Delta)+1,
\qquad f_1(\widehat\Delta)=f_1(\Delta)+v_b.$$

Using the ordinary $g_2$ formula for a $D$-dimensional complex yields

$$g_2(\widehat\Delta)
=f_1(\widehat\Delta)-(D+1)f_0(\widehat\Delta)+\binom{D+2}{2}
=q_D(\Delta). \tag{4}$$

However, $\operatorname{lk}_{\widehat\Delta}(v_*)=\partial\Delta$, which need not be a sphere. For example, the completion of a solid torus has a torus link at the cone vertex and is not a closed combinatorial 3-manifold. Equation (4) therefore does not license applying the closed-manifold theorem. This completion and its singularity are credited constructions from the boundary face-number literature cited above.

### 4.2 Finiteness is about types, not triangulations

A $D$-simplex has $q_D=0$. Stacking another $D$-simplex on a boundary facet introduces one boundary vertex and $D$ edges, without adding an interior vertex. Thus $q_D$ stays zero, while the number of vertices can grow arbitrarily. All these examples are balls. A proof that simply bounds the original triangulation's vertex count from $q_D$ would therefore be incorrect.

### 4.3 Connectedness and nonempty boundary cannot be omitted silently

For the disjoint union of $r$ $D$-simplices, with the constant in (1) inserted once,

$$q_D=(1-r)\binom{D+1}{2}.$$

Allowing arbitrarily many components would destroy the desired finiteness statement. This is a scope diagnostic, not a counterexample to the connected source theorem.

If $\Delta$ is closed, then every vertex is interior and the raw expression (1) is

$$q_D(\Delta)=g_2(\Delta)-(D+1).$$

In particular it is negative on the boundary of a simplex. The reports' separately defined closed/punctured complexity convention must not be conflated with the nonempty-boundary expression. The boundary deduction (3) uses neither the puncturing convention nor the dimension typo in the later report's displayed puncture notation.

## 5. Status and exact remaining validation task

The dataset's August 2026 assessment, based only on the 2011 report, omits the exact later affirmative Theorem 7. That omission should be recorded. The intended connected PL question has a **credited prior affirmative theorem announcement**, so it should not be advertised as a new campaign solution or confidently described as still open on the basis of the old report alone.

At the same time, this package has not independently verified the boundary finiteness proof. Its remaining task is to obtain and check a full proof, or a complete subsequent primary proof with the same category and quantifiers. Until that evidence is supplied, the conservative campaign disposition is a **source/proof-validation hold, zero fresh proof-search attempts**, rather than a claimed new solution. Any database choice to mark the question already solved on the strength of the published theorem announcement should preserve this explicit evidence level.

The exact checker verifies the dimension shift, the $h_2$ coefficient formula, cone-completion face counts, stacked-ball controls, disconnected and closed-normalization diagnostics, and a triangulated solid-torus cone-link obstruction. It is not a computational proof of topological finiteness.
