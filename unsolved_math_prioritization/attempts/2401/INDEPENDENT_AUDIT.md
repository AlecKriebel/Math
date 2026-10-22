# Independent mathematical audit

## Scope and verdict

Write \(\mathfrak c=|\mathbb R|\), and use the convention that a sumfree set \(S\) satisfies \((S+S)\cap S=\varnothing\), including sums of a point with itself. The target is a set \(A\subseteq\mathbb R\) of cardinality \(\mathfrak c\) such that both \(A\) and \(A+A\) avoid \(S\).

The four primary assertions audited below are correct; Section 5 records the final sweep of the additional arguments in the main report. They establish conditional constructions, a diagonal-safe cardinality fact, and limitations of proposed sufficient criteria and reductions. They do **not** establish the target for every sumfree set. No novelty or full-solution claim is made. This audit checks the mathematical arguments, not their bibliographic priority.

## 1. Uniformly thin difference fibers

**Assertion.** Suppose \(|S|=\mathfrak c\) and there is an infinite cardinal \(\kappa<\mathfrak c\) such that
\[
|S\cap(S+d)|\leq\kappa\qquad(d\ne0).
\]
Then the target holds, without assuming that \(S\) is sumfree.

**Verification.** Choose distinct nonzero \(a,b\in S\), and define
\[
L_a=\{x\in S:2x-a\in S\}.
\]
The map \(x\mapsto2x-a\) injects \(L_a\cap L_b\) into \(S\cap(S+(b-a))\), since \((2x-a)-(b-a)=2x-b\). Thus \(|L_a\cap L_b|\leq\kappa\). If both complements \(S\setminus L_a\) and \(S\setminus L_b\) had cardinality less than \(\mathfrak c\), their finite union would also, forcing \(|L_a\cap L_b|=\mathfrak c\). Consequently one of the two anchors, renamed \(a\), satisfies \(|S\setminus L_a|=\mathfrak c\).

Set
\[
V=(S\setminus L_a)\setminus\bigl(\{a\}\cup\{x\in S:x-a/2\in S\}\bigr).
\]
The second deleted set equals \(S\cap(S+a/2)\), so has size at most \(\kappa\); here the choice \(a\ne0\) is essential. Therefore \(|V|=\mathfrak c\).

Join distinct \(x,y\in V\) when \(x+y-a\in S\). For fixed \(x\), every neighbor lies in \(S\cap(S+(a-x))\). Since \(x\ne a\), each degree is at most \(\kappa\). At stage \(\alpha<\mathfrak c\) of a greedy recursion, the previously chosen points and their neighborhoods together have size at most
\[
\max(\aleph_0,|\alpha|,\kappa)<\mathfrak c.
\]
A new vertex can therefore be chosen, yielding an independent set \(T\subseteq V\) of size \(\mathfrak c\). Put \(A=T-a/2\). The deleted translate-overlap ensures \(A\cap S=\varnothing\). Independence excludes distinct-point sums from \(S\), and \(T\cap L_a=\varnothing\) excludes repeated-point sums. Hence \((A+A)\cap S=\varnothing\).

**Singular-cardinal caveat.** The displayed bound uses a single fixed \(\kappa\) and is valid even if \(\mathfrak c\) is singular. If instead one assumes only \(|S\cap(S+d)|<\mathfrak c\) separately for every nonzero \(d\), the proof still works when \(\mathfrak c\) is regular. For singular \(\mathfrak c\), the anchor and deletion steps survive, but the greedy step is not justified: fewer than \(\mathfrak c\) sets of size less than \(\mathfrak c\) may have union of size \(\mathfrak c\). In general graph theory this obstruction is real: a disjoint union of \(\operatorname{cf}(\mathfrak c)\) cliques with sizes cofinal in \(\mathfrak c\) has \(\mathfrak c\) vertices and all degrees less than \(\mathfrak c\), but every independent set has size at most \(\operatorname{cf}(\mathfrak c)\). This is a limitation of the argument, not a counterexample for the additive graphs under consideration.

## 2. A large reflection core

**Assertion.** If \(S\) is sumfree and some \(a\in S\) satisfies \(|S\cap(2a-S)|=\mathfrak c\), the target holds.

**Verification.** Let \(C=S\cap(2a-S)\) and \(A=C-a\). Since \(a\in S\), one has \(A\subseteq S-S\). For \(x,y\in C\), including \(x=y\),
\[
(x-a)+(y-a)=x-(2a-y)\in S-S.
\]
Thus \(A+A\subseteq S-S\). Sumfreeness implies \(S\cap(S-S)=\varnothing\): otherwise \(u=v-w\) with \(u,v,w\in S\) gives \(v=u+w\in S\cap(S+S)\). The conclusion follows, with \(|A|=\mathfrak c\).

## 3. The diagonal-safe set has full cardinality

**Assertion.** For every sumfree \(S\subseteq\mathbb R\), the set
\[
V=\{x\in\mathbb R:x\notin S\text{ and }2x\notin S\}
\]
has cardinality \(\mathfrak c\).

**Verification.** For \(s\in S\), sumfreeness gives \(2s\notin S\). If \(4s\notin S\), then \(2s\in V\). Otherwise \(4s\in S\), which implies \(3s\notin S\), because \(s+3s=4s\). If \(6s\notin S\), then \(3s\in V\). In the remaining case \(s,4s,6s\in S\), so \(5s\notin S\) by \(5s=s+4s\), and \(10s\notin S\) by \(10s=4s+6s\). Therefore \(5s\in V\).

Writing \(V/k=\{v/k:v\in V\}\), this proves
\[
S\subseteq(V/2)\cup(V/3)\cup(V/5).
\]
If \(|S|=\mathfrak c\), finite-union cardinal arithmetic forces \(|V|=\mathfrak c\), with no regularity assumption. If \(|S|<\mathfrak c\), use \(\mathbb R\setminus V=S\cup(S/2)\), whose cardinality is less than \(\mathfrak c\). Again \(|V|=\mathfrak c\).

This lemma removes the pointwise and repeated-sum obstructions, but does not control sums of distinct points in \(V\). It is not by itself the target construction.

## 4. The thin-fiber and reflection-core criteria are not exhaustive

Choose a \(\mathbb Q\)-linearly independent set \(B\subseteq(1/2,1)\) with \(|B|=\mathfrak c\), and put \(S=B+B\). Such a \(B\) can be chosen recursively: at stage \(\alpha<\mathfrak c\), the rational span of the earlier points has cardinality at most \(\max(\aleph_0,|\alpha|)<\mathfrak c\), so cannot exhaust the interval. This does not require regularity of \(\mathfrak c\).

One has \(S\subseteq(1,2)\), hence \(S+S\subseteq(2,4)\) and \(S\) is sumfree. Also \(|S|=\mathfrak c\), for example by fixing one element of \(B\) and translating all of \(B\).

For distinct \(b,b'\in B\), take \(d=b-b'\ne0\). For every \(t\in B\),
\[
b+t\in S,\qquad (b+t)-d=b'+t\in S.
\]
The map \(t\mapsto b+t\) is injective, so \(|S\cap(S+d)|=\mathfrak c\). The thin-fiber hypothesis fails, even in its nonuniform form with all fibers smaller than \(\mathfrak c\).

Nevertheless every reflection core centered at a point of \(S\) is finite. If \(a=b+b'\) with \(b\ne b'\), an equation \(x+y=2a\) with \(x,y\in S\) expresses the left side as a sum of four elements of \(B\). Rational linear independence forces the multiplicity of each basis element to agree with that in \(2b+2b'\). Consequently
\[
S\cap(2a-S)=\{2b,b+b',2b'\}.
\]
If \(a=2b\), the same coefficient comparison gives
\[
S\cap(2a-S)=\{2b\}.
\]
These exhaust the possibilities for \(a\in S\), because rational independence makes each unordered two-term representation unique.

Thus failure of thin difference fibers does not imply the existence of a full-sized reflection core centered in \(S\). This is not a counterexample to the original target: the negative ray \(A=(-\infty,0)\) already works for this positive \(S\).

## 5. Final sweep of the main report

The additional arguments in `PROOF_REPORT.md` were checked with the following results.

### Small-cardinality construction and maximality

The recursion for \(|S|=\kappa<\mathfrak c\) is correct: the union of the unary, diagonal, previously chosen, and translated forbidden sets has size at most \(\max(\aleph_0,\kappa,|\alpha|)<\mathfrak c\) at every stage \(\alpha<\mathfrak c\). The fixed bound on \(|S|\) makes this valid for singular continuum as well. No sumfreeness assumption is needed in this case. The covering certificate obtained from a maximal independent set is also correct, but does not contradict cardinal arithmetic when \(|S|=\mathfrak c\).

### Arbitrary induced-graph realization

For a rationally independent \(P\subseteq(1,11/10)\), the edge-sum set \(S_G\) lies in \((2,11/5)\) and is sumfree by the separation of this interval from its double. Magnitude excludes \(P\) from \(S_G\). Rational independence excludes \(2p\) from the edge sums and identifies unordered distinct pairs uniquely. Therefore the induced sum graph on \(P\) is exactly the prescribed graph. The complete-graph specialization correctly rules out a finite or countable coloring of the entire sum graph. It does not rule out a continuum independent set elsewhere, and the report preserves this distinction.

### Quotient and subspace examples

A Hamel basis of \(\mathbb R\) over \(\mathbb Q\) has size \(\mathfrak c\). Mapping one basis element to \(1\) and all the others to \(0\) produces the required surjection to \(\mathbb Q\), with kernel of dimension and cardinality \(\mathfrak c\). Its fiber above \(1\) is a coset disjoint from the kernel and is sumfree, so the kernel is a valid witness. The countable-coset-cover and density arguments are correct.

The proof that the kernel is not measurable invokes the standard **Steinhaus difference-set theorem** for the positive-measure branch; the zero-measure branch is immediate from its countable coset cover. The invocation and its hypotheses are correct, but this audit does not supply a new proof of Steinhaus. The Baire-property obstruction follows from the elementary comeager-overlap argument also given in the report. Translation then transfers both failures of regularity to the fiber above \(1\).

For \(S=(1,2)\), every nonzero rational vector subspace meets \(S\), because every nonzero rational line is dense in \(\mathbb R\). Thus the report correctly rejects subspaces as a universal form of witness without rejecting the original problem.

### Baire fusion and measure boundary

The nonmeager Baire-property argument is sound: a comeager part of an open interval overlaps its sufficiently small translates, giving a neighborhood of zero in \(S-S\). Sumfreeness then leaves a smaller interval and its pairwise sums disjoint from \(S\).

The meager-set Cantor fusion is sound as an elementary category argument. To spell out the construction details, start with one bounded interval, and at each stage choose the child centers in the product of the parent interiors. Avoid the finitely many coordinate bad sets, all relevant coordinate-sum bad sets, and the coordinate diagonals. Each excluded set is nowhere dense: the coordinate and distinct-coordinate sum maps are continuous open maps, and the diagonals are closed with empty interior. The resulting finite distinct centers have disjoint small closed neighborhoods inside their respective parent interiors that preserve all finite avoidances. Choose positive-length children with diameters tending to zero. Compactness and binary splitting produce a Cantor set. For any fixed forbidden index, unary avoidance persists from its scheduled stage onward; two different branches eventually split and are then covered by all later scheduled binary avoidances. Avoiding \(S/2\) handles diagonal sums separately. These details justify the claimed continuum witness without invoking a null-set analogue.

The positive-measure measurable case again uses the standard Steinhaus theorem. The **specialized perfect-set theorem for null sets has not been verified in this audit**. No conclusion for the null measurable case is accepted here on the strength of the category proof, and no acceptance decision depends on that specialized external theorem. Bibliographic claims about prior work and tracker status were not independently re-certified in this mathematical sweep.

### Exact checks and acceptance language

The finite-check source was inspected and independently rerun. Its output matched `exact_checks_result.json` exactly: 356 sumfree integer subsets, 1,186 diagonal instances and reflection cores, 1,024 five-vertex graph realizations, three naive-formula counterexamples, and the stated eight-generator model. These checks corroborate finite examples only; they do not prove the continuum assertions.

The main report's rejection of a full-solution or counterexample claim is warranted. Its separation of sufficient conditions, failed reductions, prior-work leads, and the unrestricted unresolved target is mathematically appropriate.

## Acceptance boundary

Accepted: the four original statements and the additional elementary arguments checked in Section 5, with the hypotheses and distinctions stated explicitly. Arguments invoking the standard Steinhaus theorem are checked as applications of that named theorem, not as independent proofs of it. The specialized null-set perfect-set theorem is not verified. Not established: an exhaustive dichotomy, a general independent-set construction for arbitrary sumfree \(S\), any claim of novelty, or a resolution of the unrestricted problem.
