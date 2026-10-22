# Adversarial category and topology audit of PR815 / problem 30006166

Timestamp: 2026-10-13 05:42:10 UTC. Candidate head: `5bee5139501a399da653f634147eab9433774ac7`. Author proof: 16,717 bytes, SHA-256 `74c727c159d7af1ec7be50c3766356f43a07171f3787a629627d2fce9bfe3a57`.

## Finding

The category/topology mechanism is valid, and the claimed bridge to entire-space Borel hyperfiniteness matches the inspected primary CJMST hypotheses. I found no counterexample, circularity, or required mathematical repair. This supports the complete affirmative candidate, relative to the published inputs. It is an AI mathematical audit, not formal verification, human refereeing, or a historical novelty determination.

The original claim is accurately targeted. [Oberwolfach Report 2/2025](https://content.ems.press/assets/public/full-texts/serials/owr/22/1/14299082/online/10.4171-owr-2025-2.pdf), printed pp.114-115, defines all continuous Cantor actions and whole-space Borel hyperfiniteness, then asks in Question 3: "Is the generic action of Z ≀ Z on Cantor space hyperfinite?" The group is the countable restricted wreath product. There is no free, minimal, invariant-measure, or generic-conjugacy-class qualification. The [Iyer-Shinko manuscript](https://arxiv.org/abs/2409.03078) uses the same entire action space and explicitly distinguishes hyperfiniteness from measure hyperfiniteness. Its generic freeness theorem is a proof ingredient of its baseline theorem, not a change of the problem's quantifiers.

## Independence and source binding

I first read author PROOF.md and SOURCES.json, independently reconstructed the argument, and saved INDEPENDENT_RECONSTRUCTION.md before reading either previous audit verdict. I then retrieved all three relevant PDFs freshly, inspected the exact primary statements, and rendered the original question and the two most sensitive CJMST pages. All fresh PDF hashes match the original source record. Bibliographic locators and byte bindings are in SOURCE_CHECKS.json. Only after that reconstruction and primary inspection did I read the two existing audit reports. Their acceptance agrees with this audit, but is not used as authority for any lemma here.

## Closed Polish action space

For a complete compact compatible metric on C, the space of continuous C-valued maps with the uniform metric is complete and separable. The map f->(f,f^(-1)) identifies Homeo(C) with the closed subset of pairs (f,h) satisfying f composed with h=h composed with f=id. Uniform convergence makes composition continuous on maps out of compact C. This gives a complete separable metric for uniform convergence of maps and inverses. The latter agrees with compact-open convergence of homeomorphisms: if f_n converges uniformly to a homeomorphism f, then uniform continuity of f^(-1), applied to f_n(f_n^(-1)(y))=y, gives uniform convergence of inverses.

The countable product Homeo(C)^W is Polish, and the multiplication identities alpha(gh)=alpha(g)alpha(h), together with alpha(e)=id, define a closed subset because evaluation and group operations are continuous. It is nonempty and Baire. The candidate correctly handles neighborhoods constraining arbitrary finitely many W coordinates, not only its two generators.

For every continuous c:C->Z/m, the finitely many clopen fibers have a positive separating distance when there is more than one nonempty fiber. Thus the output-label function c composed with f is locally constant as f varies uniformly. Each of the two generator equations defining D(c,m) is therefore clopen. Inverses and compositions propagate the equations to all group elements. If c is not onto, D(c,m) is empty unless m=1, since the image must be invariant under addition by 1; such c simply gives a vacuous dense-open requirement.

Every clopen subset of C is a finite union from a countable clopen basis, using compactness. There are countably many clopen sets and hence countably many finite-valued continuous maps. The obligations indexed by c,m,n are genuinely countable.

## Relative lifting in every original-action neighborhood

Given alpha in D(c,m) and m|n, define q=n/m and Y={(x,j):c(x)=j mod m}. The formula gamma(g)(x,j)=(alpha(g)x,j+chi(g)) preserves Y and satisfies the group law exactly. It is an action by homeomorphisms, not an approximate action whose relations require repair.

Let V be any action neighborhood of alpha. Take a finite symmetric F containing all constrained group elements and inverse coordinates, with all associated error tolerances. Take a finite clopen target partition Q of mesh smaller than the least tolerance. Refine Q, all alpha(g)^(-1)Q for g in F, and the c-fibers to P. Every nonempty P-atom A is a Cantor space, and Y_A consists of q disjoint copies of A.

The required atomwise homeomorphism can be made explicit after identifying A with 2^N. For q>1, split 2^N into cylinders with prefix words 0,10,...,1^(q-2)0,1^(q-1). Send the tail after the jth prefix to the jth copy of A; for q=1 use the empty prefix. This is a homeomorphism A->Y_A and never leaves A in its first coordinate. Combining the finitely many atom maps gives h:C->Y. No isolated points are introduced, no measure is prescribed, and no need for a pointwise identity in the first coordinate is hidden here.

For h(x)=(u,j), x and u share a P-atom. Therefore alpha(g)x and alpha(g)u share a Q-atom for each g in F. Since h^(-1) preserves inverse P-atom membership, beta(g)x=h^(-1)(alpha(g)u,j+chi(g)) shares a P-atom, hence a Q-atom, with alpha(g)u. It follows that beta(g)x and alpha(g)x share one Q-atom. The error is uniformly below the demanded tolerance. Symmetry of F gives the same inverse-map control. Consequently beta belongs to every prescribed V.

The second coordinate d of h is continuous, d mod m=c because P refines the old fibers, and d is exactly gamma-conjugate equivariant modulo n. Thus relative lifting applies to every neighborhood inside D(c,m). Outside D(c,m), membership in U is automatic. Each U(c;m,n) is open dense.

## Fixed-action compatibility and surjectivity

Let alpha belong to the countable intersection of all U(c;m,n). Begin at c_1=0. If c_(n!) has been chosen and alpha lies in D(c_(n!),n!), its membership in the specific U(c_(n!);n!,(n+1)!) forces an actual lift. The fact that c_(n!) was selected during recursion causes no quantifier problem: every possible continuous c was already among the countably many universal obligations. This is recursion for a fixed alpha, not a limit of approximate actions.

The compatible maps define a continuous product map with image in the inverse limit over factorial moduli, canonically Zhat because these moduli are cofinal under divisibility. Equivariance is coordinatewise. Pick any point in its nonempty compact image P; invariance under t and t^(-1) gives its entire integer translate orbit in P. That orbit is dense in Zhat, so compactness gives P=Zhat. No Borel or continuous selection of p as a function of alpha is needed. The Borel bridge itself needs only existence and equivariance, not surjectivity.

## Finite slabs and exact published inputs

For a Borel p, x->(t^(-r_m(x))x,r_m(x)) is a Borel bijection from X to B_m times the m-level set, with inverse (z,r)->t^r z. Its uniqueness uses the specified residue, not freeness. N preserves B_m. A lamp edge at level r acts on its base as t^(-r)at^r=a_(-r), and an uncut shift edge changes only the level. These base generators form the abstract subgroup K_m=Z^m, even when its action has stabilizers.

A Borel graph made of these partial generator moves has degree at most four. The distance-at-most-k relation is the finite union of graphs of allowable compositions of at most k partial Borel moves. Thus its shortest-path distance is Borel and proper in the source's sense of finite finite-radius balls. All finite-distance classes are countable.

[CJMST](https://math.berkeley.edu/~marks/papers/polycyclic_v13.pdf), manuscript p.21 Corollary 5.5, explicitly applies to arbitrary Borel actions of uniform local polynomial volume-growth groups. K_m satisfies it with degree m because every subgroup has rank at most m. There is no free-action assumption. The finite Borel cover characterization is Lemma 3.1, pp.13-14, and the finite-move, uniform-cardinality characterization is Lemma 2.2 p.11 together with its Borel extension at p.15. Disjointizing a finite Borel cover supplies a coloring with the same number of colors and no larger components.

For every fixed R, a rho_m-distance-at-most-R step changes the base by a K_m word of length at most ceil(R), regardless of colors along its intervening path. Hence a monochromatic R-chain projects into one monochromatic finite-move component. With its uniform cardinality bound C_R, the lifted component has at most m C_R points. A simple path in its R-threshold graph uses at most m C_R-1 steps, bounding its rho_m diameter by R(m C_R-1). For 0<R<1 all components are singletons. A fixed finite number D_m+1 of colors works for all R. D_m may grow with m; nothing calls for uniformity in width.

At factorial widths, inclusion of shift edges is literal: a forbidden larger residue reduces to a forbidden smaller residue. Lamp edges are unchanged. Therefore rho_(next)(x,y)<=rho_(previous)(x,y) on previously finite pairs. The exact hypothesis of CJMST Theorem 7.3, manuscript pp.31-32, is a finite supremum of next distances on pairs with old distance less than each prescribed finite r. Here that supremum is bounded by r. The theorem asks for finite dimension separately at each stage, not a common bound. Its conclusion is a finite Borel equivalence exhaustion of the union. This supplies precisely the extra mechanism beyond the unresolved unrestricted increasing-union principle; no general hyperfinite-union closure is assumed.

## Regular and exceptional pieces

The embedded integers in Zhat form a countable Borel set. Its p-preimage and complement are Borel and W-invariant. Restricting slab graphs and metrics to the complement does not remove an intervening action path, since all generator moves stay in the same invariant piece.

A forward t-edge omitted at every factorial width would have residue -1 at every modulus, hence p(x)=-1. The regular domain contains no such point. Once an edge is admitted it stays admitted. Every finite generator word is therefore captured in one sufficiently late slab. This proves equality of the restricted W orbit relation with the metric-relation union, rather than merely containment. The compatible-union theorem gives hyperfiniteness there.

On the exceptional piece, h(x) is the unique integer with p(x)=h(x). It is Borel because it has countably many Borel fibers. The normalization q(x)=t^(-h(x))x lies in B=p^(-1)(0), and (q,h) is a Borel bijection with B times Z. Two normalized points are N-related exactly when the original points are W-related: for y=gx, t^(-h(y))g t^(h(x)) has zero chi and lies in N; the converse conjugation gives a W witness.

N has local polynomial growth because every finitely generated subgroup is finitely generated abelian and supported on finitely many lamps. CJMST Corollary 7.5, manuscript p.33, covers arbitrary Borel N-actions. Its finite relations F_j on B must be pulled back only inside |h|<=j. The proposed H_j is reflexive, symmetric, transitive, Borel, and finite, because each base point has one preimage at each allowed height. Its classes have size at most (2j+1)|[z]_(F_j)|. Outside the band all classes are singleton. Both bands and F_j increase, and every W-related pair eventually enters one H_j. Disjoint union with the regular finite exhaustion gives entire-space hyperfiniteness.

## Falsification attempts and boundary cases

1. **Weak mixing.** For m>1 a height factor produces the nonconstant continuous invariant function (x,y)->c(x)-c(y) modulo m for the diagonal W-action. Thus it prevents diagonal topological transitivity. The category theorem says such actions are comeager in all actions. This is consistent: no generic weak-mixing theorem on this entire space has been supplied, and special measure-preserving or restricted transitive/minimal spaces have different relative category. In particular robust invariant clopen partitions can obstruct transitivity in nonempty action neighborhoods.

2. **Periodic points.** If t^k x=x then p(x)+k=p(x); injectivity of the integer embedding implies k=0. Thus the generic factor forces no nontrivial t-periodic points, consistent with the independently published generic-freeness fact in Iyer-Shinko Proposition 8. A finite-period action can lie near factor-bearing actions because its equations need not survive an arbitrary fine clopen perturbation. Finite-height factor conditions do not assert t has finite order.

3. **Compactness versus integer height.** There is no continuous equivariant map from a nonempty compact action to discrete Z: its compact image would be finite and invariant under +1. Profinite Zhat is compact and this obstruction vanishes. The exceptional integer h is only Borel on a generally noncompact Borel subset. It is not extended as an integer height to all of C.

4. **Nested finite relations with open generator membership.** Suppose E_j are increasing finite equivalence relations on compact C exhausting a finitely generated free infinite-group action, and for each generator s the sets A_(j,s)={x:(x,sx) in E_j} are open. For each s these increasing open sets cover C, so compactness yields one stage containing every s-edge. A common finite stage then contains the whole orbit relation, contradicting infinite free orbits. The candidate uses only Borel E_j and makes no openness claim. The clopen slab graphs themselves have infinite components and are not offered as finite E_j.

5. **False pullback shortcut.** On a single base point with its integer-height translates, the pullback of the finite equality relation by q has an infinite class. Thus unrestricted pullback would fail; the height band supplies the exact finite repair, already present in the candidate.

6. **False exceptional deletion shortcut.** Omitting only p^(-1)(-1) is not W-invariant because t sends it to p^(-1)(0). The candidate removes the full integer translate orbit and then handles it explicitly; it does not discard exceptional fibers as negligible.

7. **Degenerate parameters.** At m=1 the slab has lamp edges only and K_1=Z; the omitted shift condition is correct. At n=m the pullback has one point over each x and relative lifting is still valid. Empty Borel phase spaces give the trivial relation. Nonfree, nonfaithful lamp actions decrease orbit-ball cardinalities and cause no coordinate ambiguity. Empty c-fibers create empty atoms that are omitted from P, not nonexistent homeomorphisms.

8. **Baseline shortcut blocked.** W itself is finitely generated and has infinite asymptotic dimension: finite lamp windows are undistorted copies of Z^d for arbitrarily large d. Thus the Iyer-Shinko locally finite-asymptotic-dimension theorem does not already establish the result. No attempt is made to transfer the central argument to that unsupported hypothesis.

## Repairs, strongest result, and exact gap

Required mathematical repairs: none found. Optional exposition refinements: state explicitly that finite Borel covers are disjointized into colors, give the finite partial-word proof of Borel graph distances, and mention R<1 in the slab lemma. These are routine validations of existing assertions and do not require a new theorem or mechanism.

Strongest verified result: the generic continuous profinite-height factor theorem is established for all continuous W Cantor actions in the stated topology; its Borel height-to-hyperfinite bridge establishes hyperfiniteness on the entire phase space under the exact verified CJMST inputs. No mathematical gap remains within this audit family's remit. No new central proof search is needed for this candidate. Formal proof-assistant verification, external human review, and worldwide historical priority remain outside this audit.

Audit completion estimate: 100%. Best estimate of mathematical verification coverage within this family: 100% of specified lemmas and inputs, relative to treating the cited published results as available theorems.
