# Periodic and finite cellular configurations: five-route research packet

Problem 4600046 / AMR-045-0046. Written 9 October 2026 UTC.

## Result and disposition

**No unrestricted implication is resolved. The shared five-approach budget is exhausted.** The strongest result proved here is a period-enlargement theorem for controlled, one-successor XOR rules. All three requested implications hold within that explicitly restricted family. A second restricted theorem constructs periodic lifts for exposed-vertex-permutive local rules. Neither result is claimed novel. Neither resolves an unrestricted implication.

Other outputs are an exact finite-torus localization criterion for A, an explicit obstruction to a proposed uniform-continuity argument for B, and a boundary-count constraint on periodic fibres relevant to C. These identify gaps rather than close them.

The restricted mathematical results, with the empty-S radius convention repaired, were accepted by the accompanying independent mathematical audit. The finite tests are diagnostics of the written constructions; they do not establish a universal antecedent by sampling.

## 1. Exact claim, conventions, and success test

Let \(\mathcal A\) be a nonempty finite alphabet, \(d\ge2\), and \(X=\mathcal A^{\mathbb Z^d}\). Let \(f:X\to X\) use a single finite, translation-invariant local rule. Let
\[
P=\bigcup_{n\ge1}\operatorname{Fix}(n\mathbb Z^d).
\]
Thus periodic means a finite shift orbit, not merely one nonzero period vector.

For A and B a specified symbol \(q\) satisfies \(f(q^{\mathbb Z^d})=q^{\mathbb Z^d}\). Write \(F_q\) for configurations differing from that particular constant configuration at finitely many sites. The three targets are:

- A: injectivity of \(f|_P\) implies surjectivity of \(f|_{F_q}\).
- B: surjectivity of \(f|_{F_q}\) implies surjectivity of \(f|_P\).
- C: global surjectivity of \(f\) implies surjectivity of \(f|_P\).

C has no quiescent-background assumption. Its periodic preimages may have larger periods than the target. Throughout, q is not changed during an implication.

A full negative answer needs a finite local rule, a proof of its universal antecedent, and a witness disproving the consequent. A full positive answer must allow every finite local rule in this model. Extra algebraic, routing, permutivity, or gluing assumptions yield restricted results only.

Kari's Spring 2026 notes mark all three arrows unresolved in Figure 9, printed p.18; p.31 separately identifies C as unknown. The primary file was reopened during this work. The inspected notes also provide the classical Garden-of-Eden theorem and Example 11, used below. [Kari, Cellular Automata, Spring 2026](https://users.utu.fi/jkari/wp-content/uploads/sites/1251/2026/02/fullnotes.pdf).

## 2. Elementary implications that do not resolve the target

Every \(\operatorname{Fix}(n\mathbb Z^d)\) is finite and f-invariant. If f is injective on P, its restriction to each such finite set is a permutation. Consequently f is onto P. Since P is dense and f(X) is compact and therefore closed, f is globally onto. This proves neither global injectivity nor A.

Similarly, F_q is dense, so surjectivity on F_q implies global surjectivity. Thus a positive answer to C implies B. It does not supply A.

We use one standard theorem explicitly: for full shifts over \(\mathbb Z^d\), global surjectivity is equivalent to pre-injectivity, meaning that two different configurations with finite difference cannot have equal images. This is the classical Moore–Myhill Garden-of-Eden theorem; see the cited notes, §2.4. Statements below that use this theorem identify that dependency. The controlled-XOR and exposed-vertex arguments do not require it.

## 3. Approach 1: can unique torus inverses be localized?

Assume f is injective on P. Enlarge its neighborhood if necessary so that it contains the origin and is contained in \(Q_r=[-r,r]^d\), with \(r\ge1\). For \(y\in F_q\) supported in \(Q_K\), and an odd period \(n=2L+1\) with \(L>K+2r\), define \(y^{(L)}\) by periodically repeating y restricted to Q_L. Let \(x^{(L)}\) be its unique n-periodic preimage.

### Proposition 1: exact collar criterion

The following are equivalent for this y:

1. y has a preimage in F_q.
2. For some sufficiently large L, \(x^{(L)}\) equals q on \(Q_L\setminus Q_{L-2r}\).
3. For every sufficiently large L, \(x^{(L)}\) equals q on that collar.

**Proof.** If \(x\in F_q\) maps to y, choose L much larger than the supports of x and y plus 2r. Periodizing x then commutes with f: a local neighborhood crossing a fundamental-cell boundary sees only q, while every other local computation is a translate of the one in x. Thus its image is \(y^{(L)}\). Uniqueness on the finite torus identifies it with \(x^{(L)}\), which has the stated collar. This proves 1⇒3, and 3⇒2 is immediate.

For 2⇒1, let z agree with \(x^{(L)}\) on Q_L and equal q elsewhere. At an output site in \(Q_{L-r}\), the entire neighborhood lies in Q_L, so its output agrees with \(y^{(L)}\), hence y. Outside \(Q_{L-r}\), any neighborhood point lying in Q_L lies in the 2r collar in at least one coordinate. All input symbols there, and all input symbols outside Q_L, are q. The output is consequently q, agreeing with y. Thus f(z)=y and z belongs to F_q. ∎

### Exact residual gap

Injectivity on P gives the unique inverses but does not prove the existence of the collars. Compactness only gives an unrestricted preimage, whose support can be infinite. Replacing collar existence by a purported automatic bounded-support principle would simply assume the missing part of A. This route is blocked there.

## 4. Approach 2: extending the finite-configuration inverse

If f is onto F_q, density gives global surjectivity and the Garden-of-Eden theorem gives injectivity on F_q. Thus the inverse \(G:F_q\to F_q\) exists. It is tempting to extend G by uniform continuity to all of X and then use shift equivariance. That uniform continuity is not automatic.

### Proposition 2: explicit obstruction to uniform continuity

On \(\{0,1,2\}^{\mathbb Z^d}\), use only the current site and its neighbor in direction e_1. Define
\[
T(x)_v=\begin{cases}
2,&x_v=2,\\
 x_v+(x_{v+e_1}\bmod2)\pmod2,&x_v\in\{0,1\}.
\end{cases}
\]
With q=2, T is a bijection on F_2, but its inverse on F_2 is not uniformly continuous in the product uniformity.

**Proof of bijectivity.** A site's image equals 2 exactly when its input equals 2. A target in F_2 therefore fixes the finite set of non-2 sites in its preimage. On each e_1-line, split this set into maximal consecutive runs. Starting at the right end of each run, the neighboring symbol is 2, so its contribution modulo 2 is zero. The equations uniquely determine all symbols in that run from right to left. Outside the finite set, the input must equal 2. This gives a unique preimage in F_2.

**Proof of failure of uniform continuity.** Let y_m equal 0 at the sites \(i e_1\), \(-m\le i\le m\), and 2 elsewhere. Let z_m be the same target except that its symbol at \(m e_1\) is 1. The targets agree on \(Q_{m-1}\). The unique finite preimage of y_m is 0 on the indicated segment, whereas that of z_m is 1 on the entire segment: the rightmost 1 propagates left by the inverse recursion. Their inverse symbols at the origin differ for every m. Hence no fixed input window determines the inverse symbol at the origin uniformly over F_2. ∎

Indeed y_m and z_m converge to the same configuration, while their inverse images have different limits. No continuous extension of this inverse to all X exists.

This rule is the linewise version of the cited Example 11; the displayed proof and discontinuity deduction are included so that no unpublished property of that example is needed. The background matters: for q=0, a target with a single 1 has no finite preimage. On its e_1-line any finite preimage would contain no 2, and the sum modulo 2 of all output bits would be zero because every input bit occurs twice, whereas the target sum is one. Thus the same local rule is onto F_2 and not onto F_0.

This is not a counterexample to B: the rule has periodic lifts, for instance by Proposition 6 below. The failed mechanism is the extension of its finite inverse.

### Exact residual gap

Finite surjectivity gives finite preimages but no uniform dependency radius for their inverse. This route supplies no periodization method for arbitrary periodic targets. Adding uniform continuity of G would be a new structural hypothesis, and is false even for the above elementary example.

## 5. Approach 3: rigidity and boundary-size complexity of a fibre

Suppose f is globally onto. Fix any target y and write \(Y_y=f^{-1}(y)\). Pre-injectivity implies that Y_y has no two distinct elements differing at finitely many sites.

### Proposition 3: patterns in a fibre are determined by a boundary collar

With neighborhood contained in Q_r, and \(L\ge2r\), restriction to the collar \(Q_L\setminus Q_{L-2r}\) is injective on the set of Q_L-patterns occurring in Y_y. In particular,
\[
\#\{x|_{Q_L}:x\in Y_y\}
\le |\mathcal A|^{|Q_L|-|Q_{L-2r}|}.
\]

**Proof.** Suppose x,x' in Y_y agree on the collar. Patch x' on Q_L into x outside Q_L, obtaining z. If an output neighborhood lies entirely inside Q_L, its output equals the corresponding output of x'; if it lies entirely outside, it equals the output of x. For a crossing neighborhood, some coordinate of its center has absolute value greater than L−r. Every input site of that neighborhood lying inside Q_L therefore belongs to the 2r collar, where x and x' agree. This crossing output also equals the output of x. Consequently f(z)=y=f(x). Since z and x differ only in Q_L, pre-injectivity gives z=x. Therefore x and x' agree on Q_L. The count follows by choosing the collar symbols. ∎

For a periodic y, Y_y is invariant under a finite-index translation lattice and is described by finitely many local constraints after grouping a period block. The displayed bound implies zero topological entropy for that grouped subshift.

### Exact residual gap

A periodic preimage would be a finite-orbit point of this particular nonempty finite-type fibre. The collar bound does not construct one. In dimensions at least two it is not legitimate to replace a nonempty finite-type system by a finite directed graph: boundary states grow with the width. Nor has a theorem been established here that periodicity follows from these constraints plus their realization as a fibre of a globally onto full-shift CA. That is the remaining work, and this route is blocked at precisely that extraction step.

## 6. Approach 4: controlled one-successor XOR routing

This section gives a full restricted result, not a proof about arbitrary local rules.

Let C be a finite control alphabet and take \(\mathcal A=C\times\mathbb F_2\). The local rule leaves the control configuration c unchanged. From a finite control neighborhood it chooses either no successor or one displacement \(s_c(v)\) from a fixed finite set S. Translation covariance is required. Define
\[
F(c,b)=(c,t),\qquad
 t_v=\begin{cases}
 b_v,&v\text{ has no successor},\\
 b_v+b_{v+s_c(v)},&v\text{ has a successor},
\end{cases}
\]
with addition in \(\mathbb F_2\). Zero displacement is allowed; it then forms a directed loop. Each fixed c gives a directed graph on \(\mathbb Z^d\) with outdegree zero or one.

### Lemma 4.1: surjectivity criterion

F is globally onto if and only if no control configuration has a finite directed cycle.

**Proof of necessity.** On a directed cycle, summing the output equations cancels each input signal twice. The sum of the target bits on that cycle must therefore be zero. Keep that control configuration and choose a target with an odd cycle sum. It has no preimage, because the control layer is fixed by F.

**Proof of sufficiency.** In an outdegree-at-most-one graph with no directed cycle, the underlying undirected graph is a forest. To see this, a finite undirected cycle would have as many edges as vertices; every edge needs a tail on that cycle and each vertex supplies at most one, forcing a directed cycle. Also each weak component contains at most one successor-free vertex: a path between two such vertices would require an intervening vertex with two outgoing edges.

For a component with a successor-free vertex w, prescribe \(b_w=t_w\). For a component without one, choose any vertex w and prescribe \(b_w=0\). Extend along the unique finite undirected path from w to each vertex, using the edge equation \(b_v+b_{s(v)}=t_v\). There is no consistency obstruction because the component is a tree. Every active-site equation holds, and the only possible inactive-site equation was imposed at w. This solves all components for every t. ∎

### Proposition 4: global surjectivity gives periodic lifts with an explicit bound

Assume F is globally onto. Suppose \((c,t)\) is invariant under n\(\mathbb Z^d\). Put
\[
R=\max\bigl(\{1\}\cup\{\|s\|_\infty:s\in S\}\bigr).
\]
Let m be any power of two satisfying \(m>R n^{d-1}\). Then \((c,t)\) has a preimage invariant under mn\(\mathbb Z^d\).

**Proof.** Quotient the successor graph by n\(\mathbb Z^d\). It is a finite functional graph on n^d vertices. For each directed quotient cycle of length \(\ell\), lift one traversal to \(\mathbb Z^d\). Its total displacement is \(\Delta=nk\) for \(k\in\mathbb Z^d\). It is nonzero: otherwise the traversal would be a finite directed cycle in the infinite graph, contrary to Lemma 4.1. Also
\[
\|k\|_\infty\le \ell R/n\le Rn^{d-1}<m.
\]
Consequently k is nonzero in \((\mathbb Z/m\mathbb Z)^d\). Its order h in this finite 2-group is even.

In the mn-period quotient, every directed cycle lying above this base cycle traverses the base cycle exactly h times. Its target-bit sum is therefore h times the base-cycle sum, which is zero in \(\mathbb F_2\). Thus every cycle of the enlarged finite functional graph has even target parity.

The equations on each directed cycle are solvable: choose one input bit and propagate around; the zero parity is exactly the condition for closure. For a component ending at an inactive vertex, start with \(b_v=t_v\). After solving the cycles or terminal vertices, solve every incoming tree backwards with \(b_v=t_v+b_{s(v)}\). This supplies a solution on the mn torus. Its periodic extension is the desired preimage. ∎

No bound on the size of a preimage is inferred from finitely many torus experiments. The bound follows for every periodic target from the nonzero winding vector of each cycle.

### Proposition 5: periodic injectivity gives finite surjectivity for the specified q

Suppose F is injective on P. Then for every constant fixed state \(q=(c_0,\beta_0)\), F is onto F_q.

**Proof.** The elementary finite-set argument of §2 gives global surjectivity. By Lemma 4.1 no control graph has a finite directed cycle.

The graph for a homogeneous control configuration \(c_0^{\mathbb Z^d}\) must have no active sites. Otherwise all sites are active by translation invariance. The all-zero and all-one signal layers then have the same all-zero signal image, giving two distinct period-one configurations with equal images. This contradicts injectivity on P.

Now take a q-finite target (c,t). Since c differs from the homogeneous c_0 only on a finite set, locality and inactivity of the homogeneous control imply that only finitely many sites are active. Their graph has no directed cycle, so every forward chain terminates at an inactive site. Set \(b_v=t_v\) at inactive sites and solve the finitely many active equations backwards. Outside the union of the finite active set and the target's finite signal support relative to \(\beta_0\), one has \(b_v=\beta_0\). Therefore (c,b) is q-finite and maps to the target. ∎

Together, Propositions 4 and 5 settle A and C inside this family. B follows there because onto F_q implies global surjectivity. The argument respects any fixed q that the antecedent permits; it does not silently substitute a preferred signal background.

### Exact residual gap

A general local rule need not preserve a control layer, have one signal successor, or produce linear two-variable constraints. Multiple successors can impose genuinely multidimensional compatibility conditions. The functional-graph cycle argument does not apply to those conditions. Thus this family cannot furnish the sought counterexample, but no reduction of arbitrary CA to this family is proved.

## 7. Approach 5: exposed-vertex permutivity and a transverse cylinder

A neighborhood point p is an exposed vertex if there is an integer linear functional \(\lambda:\mathbb Z^d\to\mathbb Z\) with
\[
\lambda(p)>\lambda(u)\quad (u\in N\setminus\{p\}).
\]
A local rule is permutive in p if, on fixing the other inputs, it is a permutation of the alphabet as the p input varies. For a singleton neighborhood the exposed condition is vacuous. A rational separating functional can be scaled and then divided by the gcd of its coefficients, so we may take \(\lambda\) primitive.

### Proposition 6: a periodic-preimage bound in the exposed-vertex subclass

Assume f is permutive at such a p. Let
\[
a=\min_{u\in N}\lambda(u),\qquad b=\lambda(p),\qquad w=b-a.
\]
Every target invariant under n\(\mathbb Z^d\) has a periodic preimage. More precisely, in a unimodular coordinate system with last coordinate \(\lambda\), the preimage can have period n in every transverse direction and longitudinal period T, where
\[
n\mid T,\qquad T\le n|\mathcal A|^{w n^{d-1}}.
\]

**Proof.** Choose an integer basis for \(\ker\lambda\) and an integer vector mapped to 1 by \(\lambda\). Together they give unimodular coordinates. Quotient the first d−1 coordinates by n. A slice is now a symbol in
\[
B=\mathcal A^{(\mathbb Z/n\mathbb Z)^{d-1}},\qquad |B|=|\mathcal A|^{n^{d-1}}.
\]
The resulting one-dimensional slice rule depends on heights a through b. The unique highest-height neighborhood point is p. For fixed lower slices, the map from the top slice to the output slice is a permutation of B: its coordinates apply alphabet permutations to input sites translated by the fixed transverse component of p, and that translation is a bijection on the transverse torus.

Let the target slices have longitudinal period n. If w>0, use states consisting of w consecutive input slices and an output phase in \(\mathbb Z/n\mathbb Z\). There are \(n|B|^w\) states. From any such state, the required next input slice is uniquely determined by the target slice and top-slice permutivity. Shift the stored slices and increment the phase. This defines a total map on the finite state set, which has a directed cycle. Its length T is at most \(n|B|^w\); return of the phase gives n|T. Repeating the cycle produces a bi-infinite input slice sequence satisfying every output equation. Its transverse n-periodicity and longitudinal T-periodicity give the asserted full spatial periodicity.

If w=0, the neighborhood is a singleton by exposedness. Invert the slice permutation directly; a longitudinal period n suffices. Finally, the target remains n-periodic in the unimodular coordinates because n times that coordinate lattice equals n\(\mathbb Z^d\). ∎

This theorem constructs a lift without first assuming global surjectivity, so it proves C (and B) for this subclass. The ternary rule in Proposition 2 is permutive at its current-site input, exposed by the functional \(\lambda(v)=-v_1\), and therefore has periodic lifts.

### Exact residual gap

Global surjectivity alone supplies neither a unique extreme input nor a permutation of each top slice. A transverse periodic quotient of an arbitrary surjective CA has not been shown surjective. Assuming that would import the missing periodic-lifting property into the one-dimensional reduction. No such assumption is made here.

## 8. Checks, exclusions, and final status

The original author diagnostic, excluded from this delivery because of the verification defect recorded in the audit, checked two authored deductions:

1. The finite-support inverse and nonuniform-continuity witness for the ternary marker rule.
2. The period-enlargement construction on all 625 terminal/nearest-neighbor routing patterns on a 2×2 base torus, retaining only patterns whose quotient cycles have nonzero integer winding, and all 16 binary target patterns for each retained routing.

This is a finite check of a graph lemma after its hypothesis is explicitly computed. It is not a survey purporting to establish global surjectivity of any arbitrary full-shift local rule. Zero-winding examples are retained as negative controls and rejected by the proposed criterion.

No target is refuted by a fixed-period failure, since larger periods are allowed. No Game of Life obstruction is treated as globally surjective. No separation of periodic injectivity from global injectivity is treated as a resolution of A. No use of a group, linear, closing, or permutive subclass is generalized to arbitrary local rules.

All five selected approach families have been used. The unrestricted target remains unsolved; the disposition is exhausted/noncandidate after five approaches. The six restricted propositions, with the empty-S radius convention repaired, are accepted by the independent mathematical audit. Verification and publication add no proof-search route. The audit is AI-assisted and does not represent conventional human peer review or journal acceptance.
