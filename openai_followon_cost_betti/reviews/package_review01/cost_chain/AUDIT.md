# Independent audit of the positive Bernoulli cost input

Reviewer: `/root/package_review01/cost_chain`, assisting complete-package reviewer 01.

Audit time: October 6, 2026, approximately 21:55 PDT (October 7 UTC).

## Verdict and actual scope

**No substantive gap was identified in the positive-cost proof at the pinned upstream version.** I independently reconstructed the complete chain from the primary TeX sources, rather than accepting a theorem statement or the project's earlier audit conclusions. The chain gives

\[
\operatorname{Cost}(\mathcal R_X)\geq 1+\delta_X
\geq 1+\alpha/100,
\]

for exactly the group, Bernoulli action, and parameter hypotheses used in the candidate. With the candidate's admissible choice \(\alpha=2^{-61}\), this is the displayed gap \(1/(100\cdot2^{61})\).

This is a scoped mathematical proof audit, not the complete-package verdict. I read the original request, the entire candidate manuscript, the dependency ledger, all upstream main proof sections, source wrapper, bibliography, figure, supplied citation, repository disclaimer, and `INPUTS.md`. Coverage and SHA-256 values are recorded in `coverage.json`. The upstream checkout remained clean at `adc7f1241b42e322a6451854ab7e4b4c146bf78a`. Relevant formalization catalogue and Comparator searches did not identify a formalization of this cost result; no Lean theorem or build is certified here. Current public-source correction checks, literature priority, the direct Betti proof, deposited artifact rendering, and external publication operations belong to the parent complete-package audit.

The strongest result of this scoped audit is validation of the full primary-source positive-cost argument under its stated hypotheses. There is no exact remaining mathematical gap identified in that chain. Automated reasoning and finite checks do not supply a machine proof certificate or human refereeing. The source's warning that its intermediate record does not establish a final revision remains relevant and is accurately preserved by the candidate.

## 1. Compression and deployment

Primary sections: `compression.tex` and `deployment.tex`, read in full.

The compression lemma works on the original finite measure, not a renormalized probability measure. For \(S\subseteq T\subseteq Q=S\vee\mathcal E\), it yields

\[
C(\mathcal F)\leq C(\mathcal E)-\kappa(S)+\kappa(T)+\epsilon,
\qquad Q=T\vee\mathcal F.
\]

I checked the measurability and accounting steps specifically:

* The supplied ambient partial isomorphisms enumerate every subrelation after restriction, hence class sizes, saturations, distances, and the finite-class selectors are Borel.
* Finite-class counting uses measure preservation of the maps between ordered sheets. No equal-atom assumption is needed on the general space.
* Small complete sets on infinite classes follow from random marking of a finite separating partition. The expectation is \(p\lambda(Z_{\rm inf})+\int(1-p)^{k_n}\), so dominated convergence gives the required arbitrarily small additional measure.
* Outside the retained supplied-relation saturation, precisely one edge instance is deleted per finite \(S\)-class. Opposite selection of the same instance is impossible because distance decreases. The saved cost is exactly \(\kappa(S;Z\setminus Y)\), even with repeated graphing maps.
* The many-to-one retraction must be split at both endpoints. The actual proof does this using least ambient-map indices. Each conjugated partial isomorphism has the measure of its original piece; overlapping pushed images do not lose or duplicate the indexed cost accounting.
* Applying the retraction to a path preserves \(S\)-steps and turns deleted edges stationary. Completeness then recovers the entire \(Q\)-relation using \(T\)-steps.

Deployment first makes a finite near-optimal graphing by retaining a finite portion and adding missing restrictions of a fixed finite generating set. This is justified by decreasing missing-edge sets with null intersection. Subdividing its factor words adds finitely many sheets; the total initial edge cost is \(c+\lambda(Z)-1\).

Alternating compression enlarges the supplied \(J\)-subrelation. Its finite-stage bound telescopes to

\[
C(\mathcal E_A^n)+C(\mathcal E_B^n)
\leq c-1+\kappa(S_n)+\epsilon.
\]

The increasing objects are the generated factor relations, not the edge families. I checked that this distinction is correctly maintained. At the limit their intersections with the pulled-back \(J\)-relation equal the supplied limit. A shortest alternating chain between \(J\)-related endpoints cannot have two or more non-\(J\) factor steps: freeness gives exact displacements, and amalgam normal form forbids their product from lying in \(J\). This proves exhaustion of the pulled-back \(J\)-relation. Its classes are infinite because the embedded \(J\) is infinite, so \(\kappa(S_n)\to0\) on the fixed finite measure space.

Projection to the original probability space is split by source and target sheets, preserving each piece's cost. The factor generated with all \(J\)-steps supplied is exactly the \(A\)-relation, again by the shortest alternating chain and normal form argument. Therefore \(\delta_X\leq c-1+\kappa(S_n)+\epsilon\), giving the claimed lower bound after limits. No injectivity of the overall sheet projection is silently assumed.

## 2. Exact cocycle and Bernoulli finite-model transfer

Primary section: `finite-models.tex`, lines 24–192.

On an exact finite right \(A\)-set, the rule

\[
\theta(v,a)=x_v,\quad\theta(v,b_i)=1,
\quad\theta(v,s^{-1})=\theta(vs^{-1},s)^{-1}
\]

extends to an exact word cocycle, because adjacent free cancellations cancel at the corresponding sources. The row relation makes \(\theta(v,w)=1\) at every source, hence every \(J\)-step contributes one. This does **not** identify group labels with endpoint pairs on a finite action: distinct labels can have the same endpoints, and the proof retains the exact word label.

The restriction of the \(\Gamma\)-Bernoulli action to \(A\) is a Bernoulli action with base \([0,1]^{A\backslash\Gamma}\). Its right-action coordinate order agrees with the finite configuration \(\xi_v(g)=z_{vg}\), giving \(\xi_{vq}=\xi_vq\).

For a given admissible relative graphing, free source action and conull generation permit selection of finitely many valid path types whose labels are exactly \(a\). They cover measure at least \(1-\epsilon\). Weighted finite-cylinder approximation of their finitely many paid domains bounds the total paid measure by \(C(\mathcal E)+\epsilon\) and preserves a path-validity union of measure at least \(1-2\epsilon\). All shifted cylinder coordinate sets are fixed before taking the model limit.

Coincident coordinates \(vg=vh\) are controlled by fixed points of the nonidentity word \(gh^{-1}\). At nonexceptional sources the local labels have exactly the independent product distribution. This establishes the expected local-law error tending to zero; it does not require independent tests at different vertices.

Each modified valid path expresses \(x_v=\theta(v,a)\) in the listed paid cocycle values and their inverses. For a reverse paid step, its original-domain test is performed at \(vhg_\ell^{-1}\), matching the inverse cocycle formula. Add one \(x_v\) at each failed source. The resulting list generates the entire presented group in every labeling, and its expected size bounds rank. Consequently

\[
\limsup_k\frac{\operatorname{rk}(D_{V_k})}{|V_k|}
\leq C(\mathcal E)+3\epsilon.
\]

The order of finite approximation, model limit, and \(\epsilon\downarrow0\) is sound.

## 3. Expansion, asymptotic freeness, and overlap words

Primary section: `finite-models.tex`, lines 205 onward.

The substitution \(b_i=a^{-1}u_{i-1}^{-1}u_i\) proves that \(a,u_1,\ldots,u_{99}\) are a free basis. Assigning independent uniform permutations in that basis therefore gives exact \(A\)-actions.

For \(|T|=s\), failure of expansion permits a containing column set \(C\) of size \(96s\), with \(T\subseteq C\) because the zeroth permutation is identity. For each of the other 99 independent permutations, the containment probability is at most \((96s/n)^s\). Thus

\[
\binom ns\binom n{95s}(96s/n)^{99s}
\leq [K(s/n)^3]^s,
\quad K=e^{96}96^{99}/95^{95}.
\]

The exponent and constants come from \(99-1-95=3\); \(96s<n\) holds because \(\alpha<1/200\). A fixed finite range of sizes has probability tending to zero, while the remaining geometric tail is bounded by \(q^{R+1}/(1-q)\), \(q=K\alpha^3<1/2\). This proves expansion probability tending to one without an unjustified uniform estimate at growing sizes.

For a fixed freely reduced random-basis word of length \(L\), before the first repeated vertex an already exposed requested domain/range could occur only by immediately reversing the incoming edge. Free reduction excludes that. Exposure yields the stated bound \(L(L+1)/(2(n-L+1))\) on fixed-point probability. Diagonal selection with Markov's inequality gives every fixed nonidentity word a vanishing fixed fraction and retains expansion simultaneously.

Repeated columns give fixed points of \(u_i u_j^{-1}\). Two distinct shared columns between different rows give fixed points of \(u_i u_k^{-1}u_lu_j^{-1}\), with cyclically neighboring indices distinct. Such a word cannot be trivial: nonzero neighboring opposite-sign letters cannot cancel; deleting one zero joins equal signs; two zeros are opposite and leave equal-sign letters. A finite union of these fixed sets controls all bad rows. Hence their proportion tends to zero for the same model sequence.

## 4. The coefficient planar lemma

Primary section: `planar.tex`, read in full; in particular lines 70–257.

I checked the arbitrary-coefficient-group argument rather than substituting an ordinary free-group Greendlinger lemma. Only finitely many true \(H\)-relations are required to witness any chosen filling. Minimality counts mixed relator disks in the actual free product \(H*F(U)\), and finite presentations used to draw maps are permitted to enlarge after a replacement. No injectivity of an intermediate finite presentation into \(H\) is asserted.

Regular preimages of points in the exterior circle edges give disjoint cooriented tracks. Every exterior boundary occurrence is paired once. The graph whose vertices are boundary disks is connected: a component away from the outer disk has a separating curve whose image avoids exterior track points, hence represents a conjugate of an \(H\)-element. Capping mixed relator holes makes that element trivial in the quotient. The assumed injection of \(H\) then permits filling without those mixed relators, contradicting minimality. Closed tracks need not be individually removed, and their possible images do not invalidate this separation argument.

All exterior letters of a relator have one sign, excluding inner graph loops. An edge between oppositely oriented copies of the same relator pairs their unique occurrence of that generator. At the track point the two based relator loops are inverses, and the track has constant image. A regular neighborhood therefore has trivial boundary in the free product and can be replaced to remove both disks. This is a valid dipole argument even with arbitrary coefficients. Distinct relators share at most one exterior generator, leaving no parallel inner edges.

For each complementary face, collapse the exterior circles and read its sector product in \(H\). It equals one. In particular an inner–outer bigon gives equality of the actual coefficient-gap values, not merely conjugacy. Cyclic \(H\)-reduction excludes outer monogons. Inner degree at least seven excludes a two-edge face walk that traverses a bridge twice at an inner vertex.

The assigned corner weights are bounded by \(\ell-2\) on each face, including repeated vertices and outer loops. Euler's formula yields total inner contribution at least two. An inner vertex with positive contribution either is fully matched to the outer boundary, or has exactly one nonbigon gap containing at most three inner edges. In the latter case it gives at least \(m-3\) consecutive matching exterior letters and contributes at most one. Thus there are two different positive vertices unless full cyclic matching occurs. Their selected intervals are exterior-disjoint because track endpoints are paired only once. This proves precisely the coefficient-sensitive matching statement required downstream.

## 5. Saturation, the seam, and graph surgery

Primary section: `rank-surgery.tex`, read in full.

The minimal connected graph has no degree-one vertices and at most \(3\beta\) arcs after marking the basepoint. Seed letters from bad rows and short-exterior arcs number less than \(2\alpha n\). Each new row addition adds at most 90 columns. Were \(s=\lfloor\alpha n\rfloor\) rows processed, expansion would be contradicted by

\[
|N(T)|\leq2\alpha n+90s<96s.
\]

For \(\alpha n\geq1\), this strict inequality follows from \(\alpha n<s+1\leq2s\). The final coefficient alphabet has at most \(92\alpha n<n\) columns; every remaining mixed row is good and has at least 91 distinct exterior letters. Each arc has zero or more than 30 exterior occurrences.

**The coefficient injection is not an unsupported extra premise.** Here \(H\) is the actual subgroup of \(D\) generated by saturated letters. The presentation using all true relations of this subgroup plus the surviving mixed rows maps to \(D\). In reverse, its generators satisfy every original row: omitted rows are true relations of \(H\), and mixed rows remain. These maps are inverse on generators. Thus the relative presentation is isomorphic to \(D\), and \(H\) embeds. This is a legitimate Tietze-type replacement, although not an effective finite presentation of \(H\).

A shortest based loop for \(x_j\), \(j\in U\), traverses complete arcs and has zero or more than 30 exterior occurrences. Linear \(H\)-reduction follows from shortestness for a removable same-edge detour, or from sliding across a coefficient-trivial path and folding two distinct equally labelled edges to contradict graph minimality. Sliding preserves old based-loop values, and the fold does not increase graph rank.

Cyclic reduction of the loop word times \(x_j^{-1}\) leaves an exterior letter, since otherwise injection of \(H\) would make the original word trivial in the free product. The only disruption is the appended seam letter, or one closing seam gap after endpoint cancellations. The planar lemma's two disjoint intervals ensure that one avoids the disruption; a full match can instead be cut there. A segment of the original loop with at least \(91-3=88\) distinct exterior letters survives.

Its matching row portion has at least 88 of the original 100 letters, so the inverse complementary word has length at most 12 and equal value in \(D\). Some arc traversal in that segment contains more than 30 exterior occurrences; otherwise the two end partial traversals contribute at most 60 and all complete traversals have none. The interval \(I\) between that traversal's first and last exterior edges has at least 31 edges and degree-two interior vertices. Distinctness of the matched exterior indices makes both surrounding paths avoid its edges and interior vertices, including coincident-endpoint cases.

Adding the complement path and deleting \(I\) preserves connectedness through \(Q_1^{-1}ZQ_2^{-1}\). Both edge and vertex counts change by \(k-\ell\), so graph rank is unchanged. Every old reduced based loop using \(I\) traverses it entirely; replacement by the bypass preserves its \(D\)-value. Surjectivity survives while at least \(31-12=19\) edges disappear. This is the required contradiction to minimality.

## 6. Constants and finite falsification checks

`finite_checks.py` is an independent standard-library check; its exact output is `finite_checks.json`.

It checks 2,040 binary face walks of lengths 3–10 against the corner inequality, 20,748 admissible overlap index quadruples from indices 0–12 against free reduction, and 39,997 quarter-step values of \(\alpha n\) from 1 to 10,000 against the saturation inequalities. These are falsification checks, not extrapolated proofs; the all-size arguments are above.

The exact integer comparison is

\[
2\cdot3^{97}\cdot96^4
=3242474995074537080717329593630696549869310581938323456
<2^{183}
=12259964326927110866866776217202473468949912977468817408.
\]

Together with \(K<3^{97}96^4\) and \(2^{61}>200\), it verifies the chosen \(\alpha\). No floating-point estimate enters the positive gap.

## Checkpoint

Scoped positive-cost proof review: 100% complete by best estimate. This percentage does not assess the parent publication package or establish mathematical truth by itself. No substantive correction to the candidate's use of this cost input is requested.
