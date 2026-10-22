# Consistent conical bicombings: scoped investigation

Problem ID: 30004730. Source identifier: OWR-8415335-002. Catalog rank: 783.

Status: **unresolved in this investigation**. This is an AI-assisted research note with independently checkable elementary arguments, not a claimed solution, novelty claim, or accepted manuscript. No assertion about the nonexistence of an unlocated later solution is made. Literature checks were performed on 5 October 2026.

## 1. Source and scope correction

The source is Giuliano Basso's contribution, “Improving conical bicombings,” pp. 1696–1697 of *Differentialgeometrie im Grossen*, Oberwolfach Report 32/2021. The report concerns the July 2021 meeting and was published in November 2022. Its Question 1 is:

> Does every metric space with a conical bicombing also admit a consistent conical bicombing?

This wording has **no completeness or properness hypothesis**. The public problem page could not be retrieved (web-tool failure; direct HTTP 403). The complete locally available public-dataset record and the primary PDF independently agree on the statement; the exact UTF-8 statement hash matches the catalog. The PDF's printed pp. 1696 and 1697 were rendered and visually inspected. Dataset status labels are not mathematical evidence.

The stored literature assessment overstates the proper-space result. Properness alone is not a verified solution here. The source itself separates the positive case with finite combinatorial dimension from a weaker theorem for all proper spaces, and expressly leaves its conical conclusion open.

Primary source: https://ems.press/journals/owr/articles/8415335 ; PDF: https://ems.press/content/serial-article-files/46908 ; DOI: https://doi.org/10.4171/owr/2021/32 .

### Definitions, with all quantifiers

A geodesic bicombing on a metric space \((X,d)\) is a map
\(\sigma:X\times X\times[0,1]\to X\) such that, for every \(x,y\in X\),
\(\sigma_{xy}(0)=x\), \(\sigma_{xy}(1)=y\), and
\[
 d(\sigma_{xy}(s),\sigma_{xy}(t))=|s-t|d(x,y)\quad(s,t\in[0,1]).
\]
It is:

* conical if, for every \(x,y,x',y'\in X\) and \(t\in[0,1]\),
  \[
  d(\sigma_{xy}(t),\sigma_{x'y'}(t))\le(1-t)d(x,x')+t d(y,y');
  \]
* reversible if \(\sigma_{xy}(t)=\sigma_{yx}(1-t)\) for every \(x,y,t\);
* oriented-consistent if, for every \(x,y\in X\), \(0\le s\le t\le1\), and \(u\in[0,1]\),
  \[
  \sigma_{\sigma_{xy}(s),\sigma_{xy}(t)}(u)=\sigma_{xy}((1-u)s+ut);
  \]
* convex if \(t\mapsto d(\sigma_{xy}(t),\sigma_{x'y'}(t))\) is a convex real-valued function on \([0,1]\), for every four endpoints.

Terminology differs slightly between the sources. Descombes–Lang state oriented consistency and reversibility separately. Basso (2024) uses “consistent” to include reversibility, together with the initial-subsegment identity \(\sigma_{xy}(st)=\sigma_{x,\sigma_{xy}(t)}(s)\). These conditions are equivalent to reversible oriented consistency. Indeed, initial restrictions plus reversal also give terminal restrictions; combining the two gives every subinterval. We require reversibility whenever claiming a consistent bicombing below, so we satisfy the stronger convention.

A metric space is complete when each Cauchy sequence has a limit in it. It is proper when every closed bounded ball is compact. Proper metric spaces are complete: a Cauchy sequence is bounded, has a convergent subsequence in one closed ball, and then converges to that subsequential limit. Completeness alone is much weaker; see Section 5.

For every bicombing, convexity implies conicality by the convex-function endpoint inequality. Oriented consistency plus conicality implies convexity: apply the conical inequality to the two subsegments over \([s,t]\). This yields the convex-function inequality between the values at \(s,t\). A geodesic is straight if its distance from each fixed point of \(X\) is convex; this is weaker than comparing all pairs of moving geodesics.

## 2. Literature and prior-attempt check

* Descombes–Lang, *Convex geodesic bicombings and hyperbolicity*, Geom. Dedicata 177 (2015), 367–384, Theorems 1.1 and 1.2: proper plus conical gives a convex bicombing. A convex bicombing is consistent, reversible and unique if every bounded subset has finite combinatorial dimension (in particular if the whole space does). Combining the results gives the known positive subclass. Finite topological dimension must not silently replace finite combinatorial dimension. Preprint checked: https://arxiv.org/abs/1404.5051 ; published DOI: https://doi.org/10.1007/s10711-014-9994-y .
* Basso–Miesch, *Conical geodesic bicombings on subsets of normed vector spaces*, Adv. Geom. 19 (2019), 151–164, Proposition 1.3: every complete metric space with a conical bicombing admits a reversible one. Thus the reversible input in Section 5 is available in the complete setting. The inspected arXiv v4 is dated August 2023 and is described by its authors as mathematically unchanged from the publication. https://arxiv.org/abs/1604.04163 .
* Basso, *Extending and improving conical bicombings*, Enseign. Math. 70 (2024), 165–196, Theorem 1.4: on a proper space there is a consistent bicombing consisting of straight geodesics, with convex distance between chosen geodesics **of equal length**. The paper does not prove the unrestricted conical inequality. Lemma 5.2 and Remark 5.3 provide the finite-mesh construction and explain its remaining convergence obstruction. The finite-mesh argument in Section 4 below is an elementary quantitative version of that mechanism, not a novelty claim. https://ems.press/journals/lem/articles/14297776 .
* Basso–Krifka–Soultanis, *A non-compact convex hull in generalized non-positive curvature*, Math. Ann. 390 (2024), 5863–5882, Question 7.1: the existence question is explicitly posed for **complete** metric spaces. Its noncompact convex-hull construction is suggested as a testing ground, not proved to be a counterexample to consistent-bicombing existence. https://doi.org/10.1007/s00208-024-02905-w .
* Basso's author-uploaded *Some questions from metric geometry and functional analysis*, dated 3 January 2025, Section 1.1, again asks the unrestricted question, and describes proper-space results as partial. The author’s expectations are not a theorem. The author-uploaded web text was inspected; its PDF download failed. https://www.researchgate.net/publication/383463472_Some_questions_from_metric_geometry_and_functional_analysis .
* Danielski, *On boundaries of bicombable spaces*, arXiv:2503.06673v2 (11 May 2025), Remark III and Remark 2.5, keeps the finite-combinatorial-dimension and equal-length qualifications distinct. https://arxiv.org/html/2503.06673v2 .
* Targeted 2025–2026 searches also inspected Haettel et al.'s *ℓp metrics on cell complexes* (2025) and Naor's *De-Höldering factorization*, arXiv:2609.07564v2. Their inspected scope does not supply the missing general consistency theorem. These checks are bounded literature coverage, not an exhaustive absence certificate. https://londmathsoc.onlinelibrary.wiley.com/doi/full/10.1112/jlms.70062 ; https://arxiv.org/html/2609.07564v2 .

Read-only checks of AlecKriebel/Math found no matching bicombing/ID prior PR, commit, branch, or path in the inspected areas. Main-branch root, prioritization, attempts and problems directory listings were inspected; the recursive main tree was truncated, which is explicitly recorded. Local ID matches outside the present work were queue records rather than authored attempts. Therefore **no actual prior attempt was established**, and no prior-attempt skip is claimed. The separate research-results dataset has no record keyed by this ID or source identifier, and no matching title/identifier content was found. Search details and coverage limits are in `prior_attempts.json`.

## 3. Approach 1: dyadic midpoint refinement does not enforce consistency

Here is an explicit obstruction to a tempting construction, rather than a counterexample to the problem.

Let \(H=\mathbb R\times[0,\infty)\) with the supremum metric. For \(p=(a,b)\), \(q=(c,d)\), define
\[
 S_{pq}(t)=\left((1-t)a+tc,\quad
 \max\{(1-t)b+td,\ \min(t,1-t)|c-a|\}\right).                 \tag{1}
\]
This is a reversible conical geodesic bicombing on the proper complete space \(H\).

**Proof.** The path remains in \(H\) and has the required endpoints. Set \(L=d_\infty(p,q)\). Its first coordinate is \(L\)-Lipschitz in time. The two functions inside the maximum are respectively \(|d-b|\)- and \(|c-a|\)-Lipschitz, hence their maximum is \(L\)-Lipschitz. Thus the whole path is \(L\)-Lipschitz. For \(s\le t\), the triangle inequality through the path points gives
\[
 L\le sL+d(S(s),S(t))+(1-t)L,
\]
so its middle distance is at least \((t-s)L\), and the reverse inequality is already known. It is therefore a constant-speed geodesic. Reversal is immediate.

For different endpoints \(p',q'\), put \(A=d_\infty(p,p')\), \(B=d_\infty(q,q')\). The difference of either affine coordinate is at most \((1-t)A+tB\). The difference of the two tent terms is at most
\(\min(t,1-t)(|a-a'|+|c-c'|)\le(1-t)A+tB\).
The map taking the maximum of two real numbers is 1-Lipschitz for the supremum norm. This proves the conical inequality. □

Take \(p=(-1,0)\), \(q=(1,0)\). Then
\[
 S_{pq}(1/4)=(-1/2,1/2)=v,\quad
 S_{pq}(3/4)=(1/2,1/2)=w,\quad
 S_{pq}(1/2)=(0,1),
\]
whereas \(S_{vw}(1/2)=(0,1/2)\). The consistency defect is exactly \(1/2\).

Now start with the midpoint operation \(m(p,q)=S_{pq}(1/2)\), repeatedly insert its midpoints on dyadic intervals, and extend by completeness. For the outer endpoints \(p,q\), the three displayed quarter/midpoint points are retained at every refinement. For endpoints \(v,w\), the midpoint remains \((0,1/2)\). Thus the resulting dyadic bicombing also fails consistency. The usual construction yields conicality and reversal: midpoint conical estimates inductively yield endpoint estimates at every dyadic time, while midpoint distances and the endpoint triangle inequality yield isometry on the dyadic interval. Completeness gives a unique continuous extension. None of this identifies arbitrary crossing subsegments with newly chosen paths.

This example **does not** disprove the existence question: \(H\) also has the linear consistent conical bicombing. It disproves only the claim that arbitrary symmetric conical midpoint subdivision automatically supplies consistency.

## 4. Approach 2: finite midpoint strings exist without properness

We now give a constructive positive result valid on every complete space with a conical bicombing. Properness and compactness are not used.

Let \(m(a,b)=\sigma_{ab}(1/2)\), fix endpoints \(x,y\), and fix an integer \(n\ge2\). On \(X^{n-1}\), regard \(p_0=x,p_n=y\) as fixed and set
\[
 (Tp)_i=m(p_{i-1},p_{i+1}),\qquad 1\le i\le n-1.
\]
Define \(w_i=i(n-i)\), \(M_n=\lfloor n^2/4\rfloor\), and
\[
 D_w(p,q)=\max_{1\le i<n}\frac{d(p_i,q_i)}{w_i},
 \qquad q_n=1-\frac1{M_n}<1.
\]
The finite product is complete. Since \(w_0=w_n=0\) and
\((w_{i-1}+w_{i+1})/2=w_i-1\), the midpoint conical inequality gives
\[
 D_w(Tp,Tq)\le q_n D_w(p,q).                              \tag{2}
\]
For \(n=2\), this says that \(T\) is constant. For every \(n\), the contraction argument supplies a unique fixed string \(P^n_{xy}=(p_i)_{i=0}^n\). Indeed, summing the geometric bound on successive iterates gives
\[
 D_w(T^k p,P^n_{xy})\le\frac{q_n^k}{1-q_n}D_w(Tp,p).      \tag{3}
\]
The \(n=2,k=0\) expression uses the convention \(q_n^0=1\).

### Discrete maximum principle

If \(a_i\le(a_{i-1}+a_{i+1})/2\), then \(a_i\) is no larger than the affine interpolation of its endpoint values. Subtract that affine interpolation. A positive maximum at an interior point forces the same maximum at both neighbors and eventually at a zero boundary, a contradiction.

Applying this to \(a_i=d(x,p_i)\) and \(b_i=d(y,p_i)\) gives
\[
 d(x,p_i)\le(i/n)L,\qquad d(y,p_i)\le(1-i/n)L,
 \qquad L=d(x,y).
\]
Their sum is at least \(L\), so both inequalities are equalities. The fixed-midpoint identity makes all adjacent distances equal; the first equals \(d(x,p_1)=L/n\). Thus
\[
 d(p_i,p_j)=|i-j|L/n.                                    \tag{4}
\]
(The upper bound follows along the string; the lower bound follows by distances from \(x\).)

For strings with endpoints \(x',y'\), the same maximum principle applied to \(d(p_i,p_i')\) proves
\[
 d(p_i,p_i')\le(1-i/n)d(x,x')+(i/n)d(y,y').               \tag{5}
\]
Interpolate adjacent string points using the original \(\sigma\): for \(t=(i+u)/n\), define
\(\sigma^n_{xy}(t)=\sigma_{p_i p_{i+1}}(u)\). Set \(\sigma^1=\sigma\). Equations (4) and (5), together with the original conical inequality, prove that every \(\sigma^n\) is a conical geodesic bicombing. If \(\sigma\) is reversible, uniqueness of the reversed string and reversal of the interpolants imply that \(\sigma^n\) is reversible.

A contiguous block of a fixed string is the unique fixed string for its own endpoints. Consequently, for \(0\le i<j\le n\), \(k=j-i\), and \(u\in[0,1]\),
\[
 \sigma^n_{xy}((i+ku)/n)
 =\sigma^k_{\sigma^n_{xy}(i/n),\sigma^n_{xy}(j/n)}(u).     \tag{6}
\]
This compares **different mesh numbers**. Replacing \(\sigma^k\) on the right by \(\sigma^n\) is unjustified.

The construction and direct-iteration idea are already present in Basso's Section 5. The weighted metric makes its finite-mesh completeness requirement and quantitative convergence especially transparent; it does not close the problem.

### Exact worked model

For (1), endpoints \((-1,0),(1,0)\), and \(n\ge2\), the unique fixed string is
\[
 p_0=(-1,0),\quad p_n=(1,0),\quad
 p_i=(-1+2i/n,2/n)\ (1\le i<n).
\]
Direct substitution into \(m\) verifies it. Its interpolant is
\[
 \sigma^n_{pq}(t)=(-1+2t,\ 2\min\{t,1/n,1-t\}).          \tag{7}
\]
It converges uniformly to the linear segment; its maximum distance from that segment is \(2/n\). In particular, the midpoint of the 2-mesh is at height 1, while the midpoint of the 4-mesh is at height 1/2. Refining a mesh need not preserve old points. This successful model is not evidence of universal convergence.

## 5. Approach 3: compactness and the missing infinite-mesh limit

### Completeness does not compactify midpoint choices

In \(X=\mathbb R\oplus_\infty\ell^2\), put \(x=(-1,0)\), \(y=(1,0)\). The full metric midpoint set is
\[
 \{(0,z):\|z\|_2\le1\}.
\]
Indeed, the two distance bounds 1 force the real coordinate to be 0 and impose exactly the displayed norm bound. The points \((0,e_j)\), for an orthonormal sequence \((e_j)\), have mutual distance \(\sqrt2\); hence they have no convergent subsequence. This Banach space is complete and has a linear consistent conical bicombing. Thus even an affirmative example of the original existence property can have a noncompact midpoint set.

Properness does give compact midpoint sets and compactness arguments for bounded equicontinuous families. Yet extraction of a subsequence \(n_j\) from (6) does not imply compatible extraction of the mesh numbers \(\lfloor(t-s)n_j\rfloor\), much less their simultaneous convergence to the same global bicombing for all endpoints and parameters.

### A precise sufficient convergence statement

**Proposition.** Suppose \(X\) is complete, \(\sigma\) is reversible conical, and for every \(x,y\in X\), \(t\in[0,1]\), the **whole** sequence \(\sigma^n_{xy}(t)\) converges in \(X\). Then its limit \(\tau\) is a reversible consistent conical bicombing.

**Proof.** Metric continuity passes endpoints, the constant-speed identity, the conical inequality, and reversal to the pointwise limit. Fix \(x,y,s<t,u\), and put \(p=\tau_{xy}(s)\), \(q=\tau_{xy}(t)\). Choose integers \(i_n,j_n\) with \(i_n/n\to s\), \(j_n/n\to t\); then \(k_n=j_n-i_n\to\infty\). Set \(p_n=\sigma^n_{xy}(i_n/n)\), \(q_n'=\sigma^n_{xy}(j_n/n)\). The common geodesic speed bounds and pointwise convergence at \(s,t\) imply \(p_n\to p\), \(q_n'\to q\). By (6) and conicality,
\[
 d(\sigma^{k_n}_{p_nq_n'}(u),\sigma^{k_n}_{pq}(u))
 \le(1-u)d(p_n,p)+u d(q_n',q)\longrightarrow0.
\]
The second curve converges to \(\tau_{pq}(u)\) because the whole mesh sequence converges. The left side of (6) converges to \(\tau_{xy}((1-u)s+ut)\). This proves consistency. The case \(s=t\) is immediate. □

It suffices to establish whole-sequence convergence at rational times for each endpoint pair: their common Lipschitz constant then gives uniform convergence in time by a finite rational net, using completeness.

The constants in (2) deteriorate: \(1-q_n=1/\lfloor n^2/4\rfloor\). They control iteration at a **fixed** mesh and give no Cauchy estimate as the mesh changes. A bound on consecutive mesh differences of order \(1/n\) is not summable and, by itself, cannot supply that estimate. No adequate cross-mesh Cauchy estimate has been proved here.

The length-dependent mesh selection in Basso's theorem aligns subsegments but only guarantees the comparison estimate when the original endpoint distances agree. Two separately available bicombings, one convex and another consistent with equal-length convexity, cannot be combined just by assigning both properties to one of them.

## 6. Approach 4: an additional algebraic identity is sufficient

This approach isolates a strong extra hypothesis under which midpoint subdivision does work. It is not asserted to hold for an arbitrary conical bicombing.

**Proposition.** Let \(X\) be complete, and let \(m:X^2\to X\) be a symmetric metric midpoint operation satisfying
\[
 d(m(a,b),m(c,d))\le\tfrac12d(a,c)+\tfrac12d(b,d),
\]
and the medial identity
\[
 m(m(a,b),m(c,d))=m(m(a,c),m(b,d)).                       \tag{8}
\]
Then \(X\) admits a reversible consistent conical bicombing with midpoint operation \(m\).

**Proof.** Define \(\mu_{2^r}\) by balanced iteration of \(m\) on \(2^r\) inputs; \(\mu_1\) is the identity. Induction using (8) shows that
\[
 m(\mu_N(a_1,\ldots,a_N),\mu_N(b_1,\ldots,b_N))
 =\mu_N(m(a_1,b_1),\ldots,m(a_N,b_N))
\]
for powers of two \(N\). Each \(\mu_{2N}\) is symmetric in its inputs: permutations within either half are available inductively, and the displayed identity permits interchanging any corresponding pair across the halves because \(m\) is symmetric. Conjugating that interchange by within-half permutations yields every cross-half transposition, and these generate all permutations.

Consequently the mean of a list with every entry duplicated equals its former mean: rearrange the list as two identical halves and use \(m(z,z)=z\). Define
\[
 \tau_{xy}(k/2^r)=\mu_{2^r}(
 \underbrace{x,\ldots,x}_{2^r-k},\underbrace{y,\ldots,y}_{k}).
\]
Duplication makes this independent of the dyadic representation. Iterating the midpoint Lipschitz bound gives an average-distance bound for \(\mu_N\), proving conicality at dyadic times. Adjacent dyadic times differ by one input, so their distance is at most \(d(x,y)/2^r\). The endpoint triangle inequality makes every intervening distance exact. Completeness therefore extends each dyadic path uniquely to a geodesic on \([0,1]\).

For dyadic \(s,t,u\), expand every inner mean into its leaves. Balanced nesting flattens to one mean, and symmetry leaves only the number of \(x\)- and \(y\)-leaves. That number is precisely the barycentric weight \((1-u)s+ut\). This proves the consistency identity for dyadic parameters. The endpoint conical bound and time continuity extend it to all real parameters. Symmetry gives reversal. □

The tent midpoint from (1) violates (8). With
\(a=b=(-2,0)\), \(c=(-2,1)\), \(d=(-1,0)\), the two sides are respectively \((-7/4,1/4)\) and \((-7/4,1/2)\). Hence (8) cannot be silently deduced from symmetry and the conical estimate. The unresolved task would be to produce a suitable midpoint operation satisfying enough compatibility, not merely to assume (8).

## 7. Approach 5: completion and easy uniqueness reductions

A conical bicombing on any \(X\) extends uniquely to its metric completion \(\widehat X\). For Cauchy representatives \(x_n\to x\), \(y_n\to y\), the conical inequality makes \(\sigma_{x_ny_n}(t)\) Cauchy uniformly in \(t\). Define the extended path by these limits. The endpoint inequality proves independence of representatives, and all geodesic identities survive. If the original bicombing is reversible or consistent, these properties survive too; for consistency, the inner endpoints also converge, and the conical estimate controls their substitution.

This is only an extension lemma. If one first solves the complete-space existence question by replacing that extended bicombing, nothing shown here guarantees that the new chosen paths between points of \(X\) stay in \(X\). Thus the arbitrary-space wording in the OWR source must not be presented as equivalent to the later complete-space formulation without an additional invariance argument.

For a uniquely geodesic space, the existence question is affirmative immediately: the selected paths are forced, reversed paths and all subsegments are forced as well, so any conical bicombing is reversible and consistent. Convex subsets of normed spaces also have the linear example by direct calculation. These are scoped positive cases, not reductions of the remaining general case.

## 8. Outcome and reproducibility

Five approaches were examined. The deliverable establishes:

1. the exact source identity and the proper-space status correction;
2. explicit failure of automatic consistency under dyadic subdivision;
3. existence, uniqueness, conical interpolation, and a quantitative iteration bound for every finite midpoint mesh on a complete space;
4. a precise whole-sequence convergence condition that would yield consistency;
5. an algebraic sufficient condition and elementary completion/uniqueness lemmas.

The full source question remains unresolved here, including the general proper-space case. The obstruction is not finite-mesh existence; it is obtaining the globally compatible limiting selection with the unrestricted conical estimate, and, for an incomplete space, ensuring the paths remain inside that space.

`verify.py` uses exact rational arithmetic to replay the finite checks and explicit witnesses, and verifies the payload manifest. Those finite checks support the written proofs and do not replace their universally quantified arguments. No theorem prover certification is claimed. PDFs, screenshots, extracted source text, raw datasets, downloaded repository trees, and private coordination material are excluded from the frozen publication payload.

Reproduction: run `python verify.py` from the extracted payload directory. The script reruns the exact finite checks, compares their saved results, and checks every manifest entry.
