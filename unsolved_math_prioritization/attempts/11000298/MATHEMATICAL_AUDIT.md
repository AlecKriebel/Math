# Independent mathematical audit: finite-subgroup colimits

Problem 11000298 / AMR-109-0298, rank 1257.
Audit date: 10 October 2026 UTC.

The distributed [mathematical report](MATHEMATICAL_REPORT.md) has 16,677 bytes and SHA-256:

`579557e531b46ff5ac63a0376166c61becbcb1c990abd683f50eeff4e2c09d81`.

This AI-assisted, unrefereed audit preserves the complete mathematical review. Scoped acceptance is not external human peer review, journal acceptance or formal proof-assistant certification.

## Verdict

**ACCEPTED AS A CORRECT PARTIAL RESULT AFTER ONE CORRECTION.**

The corrected report establishes the classical positive case at rank two/genus one, an explicit infinite-order kernel for one natural amalgam and its support-restricted enlargements, a necessary rational degree-two condition, a dimension-one obstruction in the higher cases, and the stated counterexample involving all finite subgroups. It does **not** settle the general finite-diagram question for `Out(F_n)`, `n >= 3`, or the extended closed-surface mapping class group, `g >= 2`.

One genuine precision error was found in the original proof of Corollary 3.2: omitted arrows can prevent an enlarged colimit from being equal to the original amalgam. The revision repairs this using a retraction, without weakening the claimed non-repair obstruction. The distributed report contains that repair. No other mathematical correction is required for acceptance at the expressly partial scope.

This is a mathematical correctness review of the authored arguments, not a certification of novelty or a comprehensive current-literature determination.

## 1. Target and source audit

The original question was checked directly in Bridson–Vogtmann's chapter in the author-hosted volume, at printed page 331 / PDF page 338. The chapter opening, printed page 319 / PDF page 326, was also checked. Both rendered pages were visually inspected.

The two families and ranges are the ones in the report: free-group rank at least two and closed orientable surface genus at least one, with both orientation signs permitted for mapping classes. The common rank-two/genus-one group is `GL(2,Z)`. The problem asks for a finite subsystem of actual finite subgroups, with a developable simple complex over a simply connected base as its geometric formulation. It does not ask merely for torsion generation or a proper action. The adjacent seven-stabilizer construction for `Aut(F_n)` has extra gluing relations and is explicitly distinguished from the required simple structure.

Source: [Bridson–Vogtmann chapter in Problems on Mapping Class Groups and Related Topics](https://www.math.uchicago.edu/~farb/papers/mcgbook.pdf).

There is no switch from `Out` to `Aut` in the conclusion: the automorphism computations are used to prove identities before projecting, while the finite subgroups and their intersections are separately checked in the outer group. There is no substitution of the orientation-preserving mapping class group for the extended one.

The later Petrosyan–Prytula source was checked at its definitions in §3.1, its Theorems 1.1 and 1.6, and its final §10 discussion. The relevant theorems assume strictly developable simple structures; some conclusions additionally require thinness and a classifying-space hypothesis. Theorem 3.8 requires an admissible action with a strict fundamental domain. The final discussion of Outer-space and punctured-surface Teichmüller spines does not construct such a domain for the target groups. The report correctly does not use that discussion to close the problem.

Source: [Petrosyan–Prytula, Cohomological and geometric invariants of simple complexes of groups, v2](https://arxiv.org/abs/2009.02161v2).

## 2. Explicit GL(2,Z) amalgam

The matrices are correct, with column-image and usual matrix multiplication conventions:

- `S = ((0,-1),(1,0))`
- `U = ((0,-1),(1,1))`
- `R = ((0,1),(1,0))`
- `Z = -I`

All displayed equations hold: `S^2=U^3=Z`, `S^4=U^6=R^2=I`, `RSR=S^-1`, and `RUR=U^-1`.

For completeness, the lifting argument in the report has the following precise justification. In the abstract group

`L = <S,U | S^4=1, S^2=U^3>`,

the element `c=S^2=U^3` is central and has order at most two. The quotient by `<c>` is `C2*C3`. Under the classical modular presentation this is `PSL(2,Z)`. The map `L -> SL(2,Z)` is onto: `S^-1 U` is the elementary upper transvection, and it together with `S` generates by the Euclidean algorithm. The kernel is contained in `<c>` because the induced quotient map is an isomorphism. Since `c` maps to the nonidentity matrix `-I`, that kernel is trivial.

The automorphism taking `S` and `U` to their respective inverses preserves these relations and has order two. The matrix `R` realizes it and splits determinant. Thus adjoining `R` with `R^2=1` gives precisely the claimed semidirect extension and precisely the presentation of `A *_C B`. The finite groups are actual matrix subgroups, and the edge maps are their actual inclusions. The interval base and Bass–Serre development satisfy the stated simple/developable conditions.

The cited modern exposition was visually checked at printed page 10 / PDF page 11. Equation (3.12) gives the claimed finite dihedral amalgam. Its preceding displayed presentation (3.11) does omit `R^2=1`; the report correctly does not copy that omission. The omitted relation cannot be inferred merely from the other abstract relations, whereas it is true of the specified matrix. This source discrepancy is already handled correctly in the report.

Source: [Debray–Dierigl–Heckman–Montero, The anomaly that was not meant IIB, §3.1](https://adebray.github.io/papers/type_2b_duality_anomaly.pdf).

**Result: PASS.** This is credited classical mathematics, not a new solution of the higher cases.

## 3. Finite subgroups in Aut(F_n) and Out(F_n)

Composition right to left is used consistently. On `a=x_1`, `b=x_2`, the stated involution has images `eta(a)=b^-1 a`, `eta(b)=b^-1`; it fixes every remaining generator.

The free substitutions give `eta^2=sigma^2=(sigma eta)^3=1`. The relation group generated by two involutions with product of order three has at most six elements. The six displayed homology matrices are distinct, so the subgroup has exactly six elements and is `S3`. The complement action commutes with it and has trivial overlap because the supports are disjoint. Hence `H_n = S3 x W_(n-2)`; this includes `n=2`, with `W_0` trivial.

All six first-block matrices in the report are correct:

`I`, `J`, `E`, `JE=((-1,-1),(1,0))`, `EJ=((0,1),(-1,-1))`, and `JEJ=((-1,-1),(0,1))`.

Only `I` and `J` are signed permutation matrices. Therefore `W_n intersect H_n = <sigma> x W_(n-2)` in `Aut(F_n)`.

The outer-group issue is genuinely addressed, rather than assumed. Homology is injective on both finite groups: on signed permutations this follows directly from their matrices, and on `H_n` from the six distinct first blocks together with faithful complement matrices. If an element of each factor has the same outer class, their homology matrices coincide. That common matrix belongs to the displayed matrix intersection and is realized by an element of `C_n`. Faithfulness on each factor identifies both original automorphisms with that same element. Consequently there are no extra outer intersections. Each local group also embeds in `Out(F_n)` because its intersection with `Inn(F_n)`, a torsion-free group, is trivial.

The generation statement is also correct. The product `eta tau_2` is the left Nielsen move `a -> b^-1 a`, fixing the other generators. Conjugating by permutations and inversions gives the usual Nielsen moves; for example, conjugation by `tau_1` turns this into `a -> ab`. Signed permutations and these moves generate `Aut(F_n)`, and projection gives surjectivity onto `Out(F_n)`.

AFV's Theorem 1 has hypothesis `n>=4`; Corollary 1 supplies `n=3`, and Corollary 2 supplies `n=2`. These low-rank statements were checked rather than silently extending the theorem. Their §3.3 identifies the signed-permutation and theta stabilizers used here. Their relation and generator definitions match the report exactly.

Source: [Armstrong–Forrest–Vogtmann, A presentation for Aut(F_n), v4](https://arxiv.org/abs/math/0701937v4), pages 2–3 and §§3.3–3.7.

**Result: PASS, including all low-rank and outer-intersection claims.**

## 4. The explicit kernel and infinite-order claim

Let `f=eta tau_1`. Direct substitution, using the stated convention, gives

- `f(a)=a^-1 b`, `f(b)=b^-1`
- `f^2(a)=b^-1 a b^-1`, `f^2(b)=b`
- `v=f^2 tau_2`: `v(a)=b^-1 a b^-1`, `v(b)=b^-1`

Thus `v^2(a)=a` and `v^2(b)=b`, and all complementary generators are fixed. The element `r=v^2` is therefore the identity in the automorphism group, and hence also in the outer group. No assertion that trivial homology alone implies this identity is used.

In `P_n=W_n *_(C_n) H_n`, the eight-factor expression is correct. Its alternating `H_n` factors are `eta`; its alternating `W_n` factors are `tau_1` and `tau_1 tau_2`. All lie outside `C_n`, as seen from the first two homology coordinates. The word is reduced and begins and ends in different factors. Therefore its kth positive power has reduced amalgam length `8k`. The normal-form theorem yields infinite order. There is no exceptional rank in this proof because its nontrivial part is supported in the first two generators.

This proves failure of this particular inclusion amalgam. It does not identify the entire kernel and does not claim that an unrelated finite diagram has the same defect.

**Result: PASS.**

## 5. Correction to subordinate-diagram Corollary 3.2

### Original defect

The original paragraph inferred equality of colimits solely because every added local group was an actual subgroup of one of the two original factors. That does not make its homomorphism value forced when the diagram omits the arrow into its containing factor. For example, append an isolated object `<tau_1>` to the original three-object diagram. Its colimit is `P_n * C2`, even though `<tau_1>` is an actual subgroup of `W_n`. Thus the original same-universal-property claim was false for arbitrary inclusion subdiagrams.

### Accepted repair

Let `D` be any finite diagram retaining `W_n`, `H_n`, `C_n` and the two original arrows. Assume every further object is an actual subgroup of `W_n` or `H_n`.

For each object `K`, map it into `P_n` through either containing original factor. This is independent of the choice if both contain it because then `K<=C_n`. These homomorphisms respect all arrows. Indeed, for an arrow `K<=L` with the chosen containing factors different, `K` is contained in their actual intersection `C_n`, and the two restrictions agree in the amalgam.

Consequently there is `p:colim(D)->P_n`. The original subdiagram provides `j:P_n->colim(D)`. On both original generating factors, `p j` is the identity, so `p j=id`. The map `j` is injective; in particular `j(r)` has infinite order. Its canonical image in `Out(F_n)` remains trivial. This proves the full stated non-repair conclusion without claiming equality of colimits.

If each added object does have an arrow to one of its containing factors, all objects in the colimit are generated by the original factors. Then `j` is also onto and hence an isomorphism. The revised paragraph correctly states this additional hypothesis for the stronger conclusion.

**Result: original equality claim FAIL; corrected retraction statement and proof PASS.**

## 6. Degree-two cohomology obstruction

The proposition is correct with trivial coefficient action and the stated torsion-free hypothesis for the general coefficient group.

For an arbitrary diagram `F_i` of finite groups, interpret restriction along the canonical maps `u_i:F_i->G`, whether or not those maps are injective. A class in the kernel of the restriction map is represented by a central extension whose pullback over every `F_i` splits. A splitting is a lift `s_i:F_i->E` of `u_i`.

If `s_i` and `t_i` are two such lifts, their pointwise ratio is in the central kernel `A` and is a homomorphism `F_i->A`. It is zero for finite `F_i` and torsion-free `A`. Thus the lift is unique. For an arrow `phi:F_i->F_j`, the maps `s_i` and `s_j phi` lift the same `u_i`, so they agree. The universal property produces `s:G->E`. Its composite with the extension projection agrees with the identity on every local image, and hence is the identity on `G`. The extension splits. This proves injectivity of the restriction map in degree two.

For `A=Q`, the averaging formula in the report has the correct sign. Summing the cocycle equation and using the bijection `k -> hk` gives

`c(g,h)=b(g)+b(h)-b(gh)`.

Consequently every finite-group class vanishes and the injective restriction target is zero. Neither finiteness of the diagram nor monicity of its arrows is needed for this central-extension argument.

The coefficient assumptions matter. This is not an assertion about nontrivial coefficient actions, arbitrary torsion coefficient groups, or higher-degree cohomology. Uniqueness of local splittings is the decisive special fact and cannot simply be assumed in those settings.

The report also correctly refuses to use the oriented mapping-class subgroup's usual first MMM class as a class of the extended group. Reversing the fiber orientation changes the sign of the vertical Euler class, leaves its square unchanged, and changes the sign of fiber integration. Thus that first MMM class changes sign. A class restricted from the extended group must instead be invariant under the orientation-reversing conjugation action. No unverified all-genus dimension calculation is asserted.

**Result: PASS, as a necessary condition that is not activated for the target higher groups in this packet.**

## 7. Dimension-one obstruction

In rank three, the proposed automorphisms commute. With column-image matrices they are

`alpha_* = ((1,0,0),(1,1,0),(0,0,1))`,

`beta_* = ((1,0,0),(0,1,1),(0,0,1))`.

Their off-diagonal nilpotent parts have zero cross-products. The corresponding entries of `alpha_*^p beta_*^q` are independently `p` and `q`, for all integers `p,q`. Thus no nontrivial product is inner. Their outer classes form `Z^2`; the same construction extends by the identity in every larger rank.

For genus at least two, choose disjoint nonseparating curves on different handles. Their twists commute. The actions on the corresponding two symplectic homology summands independently record their powers, so they too generate `Z^2` inside the extended group.

A graph of finite groups acts on its Bass–Serre tree with finite vertex stabilizers. The restriction of this action to the displayed torsion-free `Z^2` subgroup has trivial vertex stabilizers. Subdivision removes any inversions without compromising finiteness, so the action is free. A group acting freely on a tree is free; `Z^2` is not. This contradiction works for any graph of finite groups, without needing the graph finite.

The proof stops at dimension one. It does not disallow higher-dimensional simply connected bases or simple complexes of finite groups.

**Result: PASS with the report's explicit dimensional restriction.**

## 8. All finite subgroups are not a substitute

For `G=C2*C3`, finite subgroups fix vertices of its Bass–Serre tree and are conjugate into a free factor. Because the factors have prime order, every nontrivial finite subgroup has order two or three. Distinct such subgroups have trivial intersection, and no strict inclusions occur between them. The colimit of the complete actual-inclusion system is therefore the free product of these nontrivial finite subgroups.

The group `<bab^-1>` is distinct from `<a>` by free-product normal form, and distinct from `<b>` by order. Treating its generator as `c` in its separate factor, `b a b^-1 c^-1` is a reduced word of four nontrivial syllables in that larger free product. Its image in `G` is the identity. The smaller subsystem consisting of the original two factors and the trivial subgroup does have colimit `G`.

This is a valid counterexample to the proposed all-finite-subgroups reduction. It crucially uses inclusion-only arrows; adding conjugation morphisms would be a different category and is not silently done.

**Result: PASS.**

## 9. Final scope and stopping condition

The accepted report is a source-grounded partial result, with the general problem still unresolved by this packet. Its correctness does not certify that no newer paper settles the original question. The bounded fresh searches in this audit found the original question and related primary sources but no later resolution; they are not an exhaustive openness or novelty audit.

The honest remaining obligation is either an arbitrary-rank/higher-genus finite inclusion diagram with injectivity of its canonical map proved, or an obstruction applicable to every such finite diagram. None of the accepted obstructions provides that general conclusion.

Acceptance applies only to the exact distributed report hash above and to the express partial scope recorded here.
