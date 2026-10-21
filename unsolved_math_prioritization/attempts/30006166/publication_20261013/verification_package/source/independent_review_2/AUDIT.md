# Second independent adversarial audit: problem 30006166

## Decision

**Accept the mathematical argument as a complete affirmative candidate, relative to the stated published inputs. No mathematical correction is required.** This is an independent AI-assisted mathematical review, not human peer review, proof-assistant verification, or certification of historical novelty. Finite diagnostics are additional falsification attempts and do not certify any infinite claim.

The reviewed author text has SHA-256 `74c727c159d7af1ec7be50c3766356f43a07171f3787a629627d2fce9bfe3a57` and 16,717 bytes. Its enclosing author freeze has SHA-256 `1afc6d7c39a334dc3c271dfa2944426a92589236822d8a06fb97ca4c64e71d40` and 19,189 bytes. The author manifest has SHA-256 `c9c1b418218bbb6f831908733d4b8a27d819cdd3abbb72a142d3f57aea3ab171` and 1,699 bytes. This audit did not modify the author or consult the first audit. It independently read the full author argument and the relevant primary-source statements before developing its own test models.

The conclusion has the requested quantifiers: a comeager set of continuous actions of the restricted wreath product Z wr Z on Cantor space has hyperfinite orbit equivalence relation on the entire space. Neither deletion of a meager/null subset nor a generic conjugacy class is substituted for that statement.

## Primary-source scope

The target is Question 3 in Sumun Iyer's contribution with Forte Shinko, printed p.115 of [Oberwolfach Report 2/2025](https://doi.org/10.4171/owr/2025/2). The displayed question and its surrounding interpretation of generic Cantor actions were checked against the rendered primary page. The full primary PDF was freshly retrieved and matched the supplied PDF byte for byte.

The needed source is [Conley–Jackson–Marks–Seward–Tucker-Drob, Borel asymptotic dimension and hyperfinite equivalence relations](https://math.berkeley.edu/~marks/papers/polycyclic_v13.pdf). The inspected manuscript explicitly permits arbitrary Borel actions in Corollary 5.5, provides the Borel finite-cover characterization in Section 3, and permits nonuniform finite dimensions across the compatible metric sequence in Theorem 7.3. Corollary 7.5 covers countable local-polynomial-growth groups without freeness. All these hypotheses are checked below. The fresh full PDF matches the supplied PDF. The argument does not use the free-action hypothesis of the different main theorem, Theorem 1.3.

[Iyer–Shinko, Asymptotic dimension and hyperfiniteness of generic Cantor actions](https://arxiv.org/abs/2409.03078) gives the baseline and interpretation of the action space. Its stated local finite-asymptotic-dimension condition does not include Z wr Z. It is not an extra premise of this candidate proof. No comprehensive worldwide novelty search was performed by this reviewer.

## 1. Relative finite-factor lifting and the Baire quantifiers

Write W = N semidirect Z, with a_i = t^i a t^{-i} and chi(t)=1, chi(a)=0. Fix a compatible compact metric on Cantor space X. Its homeomorphism group, with uniform convergence of maps and inverses, is Polish. The homomorphism identities define a closed subset of Homeo(X)^W, so the action space is Polish and Baire.

For a continuous c:X->Z/m, its finitely many fibers are clopen. Each homeomorphism's output c-label function is locally constant in the uniform topology: distinct nonempty fibers have positive minimum separation, so sufficiently close maps give the same labels everywhere. Thus the two required generator equalities define a clopen set D(c,m). Because a,t generate W and chi is a homomorphism, these equalities imply equivariance for every group element, including inverses.

There are only countably many continuous finite-valued maps on X. Every clopen subset is a finite union of members of a fixed countable clopen basis, by compactness. Consequently all continuous c, and all lifting obligations indexed by c and m|n, form one countable family. There is no uncountable intersection hidden in the subsequent recursion.

Given alpha in D(c,m), form Y={(x,j):c(x)=j mod m}. The action gamma(g)(x,j)=(alpha(g)x,j+chi(g)) is an exact action on Y. Invariance follows from the existing factor equality; multiplication is exact because both coordinates respect multiplication. Each nonempty clopen atom P on which c is constant has Y_P a finite, nonzero disjoint union of Cantor spaces, hence itself Cantor.

For an arbitrary prescribed neighborhood, choose a finite symmetric list F of group elements with tolerances and a finite clopen partition Q of sufficiently small mesh. Refine Q, the preimages alpha(g)^{-1}Q for g in F, and the c-fibers to a partition P. Choose an atomwise homeomorphism h_P:P->Y_P. For x in a P-atom, the first coordinate u of h(x) lies in that atom. Therefore alpha(g)u and alpha(g)x lie in the same Q-atom. The point h^{-1}(alpha(g)u,j+chi(g)) lies in the same P-atom, and hence Q-atom, as alpha(g)u. Thus beta(g)=h^{-1}gamma(g)h is uniformly close to alpha(g) for every g in F. Including inverses in F supplies the full homeomorphism topology. No unsupported extension of finite partial permutations is being used.

The second coordinate d of h gives the new factor and reduces exactly to c, since h preserves the old c-fibers. This establishes density of the relative lifting obligation inside D(c,m); outside D(c,m) that obligation is automatic. Its union form is open. Baire category now supplies a dense G_delta satisfying every obligation simultaneously.

For a fixed action in that intersection, recursively choose c_1=0 and compatible lifts at 2!,3!,... . At each step the actual previously chosen map is included in the already enumerated family of obligations, so the recursion is legitimate. Coordinatewise continuity gives a continuous inverse-limit map p. Equivariance holds in every finite coordinate, hence in the inverse limit. A nonempty compact image invariant under both +1 and -1 equals the whole profinite integers, since the embedded integers are dense. Surjectivity is correct, although the Borel part of the proof does not need it. No uniform Borel choice of p over the action space is claimed or necessary.

## 2. Finite-width slab geometry without freeness

For a Borel equivariant p, let r(x) be its residue modulo m in {0,...,m-1}, B_m its zero fiber, and z=t^{-r(x)}x. The maps x->(z,r) and (z,r)->t^r z are Borel inverses. Uniqueness follows from the prescribed residue, not absence of stabilizers. Every N-element preserves B_m.

In these coordinates an a-edge changes (z,r) to (a_{-r}z,r), because t^{-r}at^r=a_{-r}. An uncut t-edge changes (z,r) to (z,r+1). Thus the horizontal generators belong to the finite-rank subgroup K_m generated by a_0,...,a_{-(m-1)}. This subgroup is abstractly Z^m, regardless of any kernel in its action. In fact each slab component is a K_m-orbit times all m levels: vertical travel allows each displayed lamp generator to act at its designated level. The proof only needs the easier containment direction.

The graph is Borel, symmetric after declaring edges undirected, and has degree at most four. Loops can be ignored. All bounded balls are finite. The graph distance is a Borel extended metric: for each integer k, its distance-at-most-k relation is a finite union of graphs of finite compositions of the finitely many partial Borel moves. This also verifies countability of its finite-distance relation.

Fix R>=1. Since K_m has polynomial growth, the cited nonfree-action input gives one finite dimension D_m valid for every scale. The Borel cover characterization can be disjointized into D_m+1 color classes. For the finite set S of lamp words of length at most ceil(R), the monochromatic S-components have uniformly bounded diameter in the K_m orbit metric. Their cardinalities have a common bound C_R: each is contained in an orbit ball of that bounded radius, whose size is at most the size of the corresponding finite group ball. Stabilizers can only reduce that size. Equivalently the finite-cardinality characterization in the source supplies C_R directly.

Lift the color of z to all (z,r). A path of length at most R in the slab changes z by at most ceil(R) lamp letters. A monochromatic distance-at-most-R chain therefore projects into one monochromatic S-component, even though intermediate points along the short paths need not have that color. Consequently each lifted chain component has at most m*C_R vertices. Any connected graph on at most that many vertices has a simple path of at most m*C_R-1 edges between any two vertices; here each chain edge has slab length at most R. Thus its slab diameter is at most R*(m*C_R-1). For R<1 the components are singletons. The same finite D_m works for all R, proving finite Borel asymptotic dimension of each slab metric.

No freeness, uniform bound over all m, Borel orbit transversal, or finiteness of the slab components was used.

## 3. Compatible exhaustion and the precise union theorem

If m|n, every residue n-1 reduces to m-1. Therefore a shift edge permitted at width m is permitted at width n. The lamp edges are unchanged, so G_m is a subgraph of G_n. For every pair at finite old distance, the new distance is no larger. The exact forward metric-control supremum required by the source is therefore at most r for the pairs at old distance less than r. Properness and Borelness were checked above. The dimensions may grow with n, which the theorem allows.

A t-edge from x is omitted at every factorial width exactly when p(x)=-1: the congruences p(x)=-1 modulo n! for all n characterize that single inverse-limit point. Deleting only its fiber would not give an invariant domain. The proof instead removes its whole W-saturation, p^{-1}(Z), since shifts add integers and lamps leave p unchanged. The integer subgroup is countable and hence Borel; its preimage and complement are invariant Borel sets.

On the regular piece every t-edge eventually occurs, and all lamp edges occur at every stage. Every finite generator word traverses only finitely many edges, so all its edges occur at one sufficiently large stage. This proves equality of the entire restricted orbit relation with the union of the slab finite-distance relations. It is equality of relations, not an assertion that all countable unions of hyperfinite relations are hyperfinite. The source's stronger metric compatibility theorem now applies on this invariant standard Borel domain. Restricting the metrics introduces no path problem, since no W-path leaves the domain.

## 4. Exceptional preimage and a genuinely finite exhaustion

On X_exc=p^{-1}(Z), the integer value h is a Borel function: its individual fibers are Borel and the range is countable. With B=p^{-1}(0), the normalization q(x)=t^{-h(x)}x is Borel and identifies X_exc with B times Z. The inverse is (z,k)->t^k z, without any freeness assumption; distinct k have distinct profinite heights.

For y=gx, the element t^{-h(y)}g t^{h(x)} has chi-value zero and hence lies in N. Thus q(x) and q(y) are N-equivalent. Conversely, an N-witness between q(x) and q(y) yields a W-witness between x and y by conjugating with their integer heights. This proves the required equivalence in both directions, with no injectivity requirement on q.

Every finitely generated subgroup of N is a finitely generated abelian group, so N has local polynomial growth. The cited hyperfiniteness theorem provides increasing finite Borel equivalence relations F_j on B exhausting its N-orbit relation.

Define H_j by the F_j pullback only inside the band |h|<=j, and singleton classes outside. This is a Borel equivalence relation: inside the band it is an equivalence relation, no pair joins inside to outside, and all exterior classes are singletons. For each base point z and each integer height k there is exactly one point with (q,h)=(z,k), so a class meeting the band has size exactly (2j+1) times its finite F_j-class size. The classes are finite, not necessarily uniformly finite. Enlarging both the band and F_j makes H_j increasing.

For a W-related pair, the heights are finite and its normalized base pair enters some F_j. A sufficiently large j handles both requirements. Conversely every H_j-related pair is W-related. Thus the union is exactly the entire exceptional orbit relation. Pulling back F_j without the height band would generally have infinite classes; the proof explicitly avoids that error.

Combining the finite exhaustions on the two disjoint invariant Borel pieces gives finite Borel equivalence relations on all of X at each stage. Their union is E_W. This proves the Borel factor statement and, by Section 1, the generic Cantor-action conclusion.

## 5. Adversarial diagnostics and limitations

The independently written standard-library program does not import or call the author's checker. It includes finite configuration actions whose height period is shorter than the lamp-configuration period; t to the height period fixes some points but moves others. Those actions are transitive and have varying, nonnormal point stabilizers. Another model quotients the lamp configuration module by its diagonal submodule. These tests directly challenge both coordinate uniqueness and inappropriate reliance on freeness.

It checks complete component inventories, short-path projection, colored chain components at three radii and three palettes, divisible-width nesting, finite pullback-factor algebra, persistent factorial residues, and exceptional finite bands. Its five negative controls detect a reversed conjugation index, loss of nesting for nondividing widths, the persistent minus-one cut, noninvariance after deleting only one height, and unbounded class growth when the exceptional band cutoff is omitted. Exact counts and model inventories are in EXPECTED_RESULTS.json.

The tests cannot establish Baire category, existence of atomwise Cantor homeomorphisms, infinite inverse limits, Borel measurability on arbitrary spaces, the cited deep theorems, or the infinite exhaustion. Those claims are assessed by the mathematical argument above. Normal and optimized Python replays use explicit runtime checks rather than assert statements. Manifest/adversarial tests address file integrity and replay behavior, not mathematical truth. The manifest is not a digital signature; an independently trusted outer archive hash is needed to authenticate the bundle.

## 6. Required changes and acceptance conditions

There are no required proof patches. The elaborations above make implicit routine details explicit, especially uniform cardinality bounds from bounded-degree orbit balls, the Borelness of slab metrics, and exact handling of nonfree stabilizers. They do not change the argument.

Acceptance is bound to the exact author proof and source versions recorded in AUTHOR_BINDING.json and SOURCES.json. The author text should continue to be described as AI-assisted, unrefereed work. The conclusion should not be promoted to a formally verified theorem or a verified priority claim on the strength of these finite tests or this audit.
