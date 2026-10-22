# Independent mathematical audit: discrete initial surreal groups

Date: 10 October 2026. Problem 30003321.

## Review status of this edition

This is an AI-assisted mathematical proof accompanied by an independent internal AI mathematical and source audit. The authored documents are unrefereed. Acceptance records that audit's full affirmative verdict within the stated source theorems and NBG/global-choice setting. It is not external human peer review, journal acceptance, formal proof-assistant certification, or a novelty or exhaustive-priority claim. The proof dependencies were checked against the authenticated author manuscript, not a byte-authenticated publisher PDF.

## Verdict

**ACCEPT the full affirmative argument. No mathematical correction is required.** The reviewed candidate proves that every discrete initial ordered additive subgroup of No is order-group-isomorphic to an initial subgroup of Oz, for sets and proper classes in NBG with global choice. This is an independent mathematical review, not journal peer review, formal proof-assistant verification, or a certification of priority.

The verdict applies to the 10,925-byte candidate with SHA-256 `5844d5646e90761d0760a94ea8cb975c4da6eaa36efefc8e7567553c988608aa`. The candidate was not edited. The sign-tree argument below supplies an independent explicit inverse and expands the limit-ordinal justification; it does not repair a defect.

## 1. Exact target and source dependencies

The target is Question 1 in the Kaplan–Ehrlich contribution to [Oberwolfach Report 60/2016](https://ems.press/content/serial-article-files/46663), PDF page 44, printed page 3356. It concerns ordered additive groups. The later [Ehrlich–Kaplan author manuscript](https://elliotakaplan.github.io/Number_systems_with_simplicity_hierarchies_II.pdf) retains it as Question 9.1. The question does not require the isomorphism to preserve simplicity or the original embedding. The stronger-hypothesis result for discrete initial subdomains does not settle this group question.

The proof-bearing source is Philip Ehrlich and Elliot Kaplan, *Number systems with simplicity hierarchies: a generalization of Conway's theory of surreal numbers II*, JSL 83 (2018), 617–633, [DOI 10.1017/jsl.2017.9](https://doi.org/10.1017/jsl.2017.9). Its authenticated 16-page author PDF was read in full relevant context, with fresh visual inspection of the characterization and question pages. Publisher metadata was checked separately; no byte-identical publisher-PDF claim is made.

The source inputs are correctly identified: normal forms and their canonical Hahn-group correspondence (Section 3, Proposition 3.3); the real coefficient-group classification (Lemma 5.1); the group characterization (Theorem 5.1); and the Oz normal-form criterion (Section 6.2). The paper explicitly works in NBG and uses “class” to include proper classes. [Author PDF, Sections 1, 3, 5, and 6.2](https://elliotakaplan.github.io/Number_systems_with_simplicity_hierarchies_II.pdf).

For precision, Theorem 5.1 is about the canonical normal-form image, rather than an arbitrary abstract isomorphism into a Hahn group. The candidate applies it in exactly that way. Its exponent object is an ordered class, with no additive or multiplicative closure assumption. Cross sectionality requires every unit monomial. Truncation closure requires every proper initial segment of an individual series. The coefficient group at an exponent is defined by membership of one-term series. The extra coefficient requirement applies to a greater, simpler exponent. None of these hypotheses is omitted or reversed in the candidate.

## 2. Discreteness and the bottom coefficient

Let g be the least positive member of the nontrivial source group, and let its first normal-form term be r omega^m, with r positive. The first-term truncation is in the group. If g has a nonzero tail h, subtraction puts h in the group, and its smaller leading exponent gives 0 < |h| < g. This is impossible. The same argument covers infinite and limit-length tails because it uses their leading exponent, not a finite sum estimate.

Consequently g is a monomial. The one-term coefficient group at m has least positive coefficient r. Its initiality and the real-group classification force R_m = 2^(-n) Z and r = 2^(-n); a group containing all dyadics has no least positive member. For any source exponent y < m, cross sectionality would supply omega^y, which is smaller than r omega^m for every positive real r. Thus m is the minimum of the entire exponent class, not just of g's support.

A plus sign in m would have a proper prefix numerically below m. Initiality of the exponent class would put that prefix in the class, contradicting minimality. Hence m consists entirely of minus signs and is -alpha for a set ordinal alpha.

This argument is valid. Its least-positive-element description is also consistent with Proposition 5.2 of the cited paper; it should not be presented as a new classification theorem. The candidate makes no such priority claim.

## 3. Independent audit of the transfinite sign rotation

Write a = (-)^alpha, write e for the empty sequence, and use juxtaposition for ordinal-indexed sequence concatenation. Work first on the full numerical final segment S_a = {s : s >= a}. The candidate's map is

- f(a) = e;
- f(s) = (+)s if a is not a prefix of s;
- f(a(+)t) = (+)at.

Any s > a that extends a has the displayed plus as its next sign. A minus would put s below a. Thus these cases are exhaustive and disjoint.

### 3.1 Concatenation at arbitrary ordinals

For sequences u and v, the proper prefixes of uv are precisely the proper prefixes of u together with the sequences uw where w is a proper prefix of v. This includes w = e when v is nonempty. It follows from the ordered-sum definition of concatenation: a cut is either before the end of the first block or in the second block. This is valid when either block has limit or uncountable ordinal length. In particular, the assertion does not infer sign positions by treating ordinal addition as integer addition.

Concatenating the same sequence on the left preserves and reflects lexicographic order and prefix relations. One compares the tails at their first difference, treating termination between minus and plus. The second-block indices are the ordered interval after the common prefix, not indices obtained by an invalid ordinal cancellation.

### 3.2 Explicit inverse and injectivity

There is an inverse on every nonnegative surreal sign sequence. Define h(e) = a. For a nonempty nonnegative sequence write it uniquely as (+)v. Put

- h((+)v) = v if a is not a prefix of v;
- h((+)at) = a(+)t otherwise.

In the first case v > a: it either ends along a before alpha or first differs from the all-minus a by a plus. In the second case a(+)t > a. Direct substitution gives h(f(s)) = s and f(h(z)) = z. This proves, in particular, the candidate's injectivity. It also shows that the formula is a bijection from the full final segment S_a onto all nonnegative surreals. The argument uses class-defined functions on set sequences and does not enumerate either class.

### 3.3 Order preservation, including cross-branch pairs

Within the branch not extending a, the operation prepends a fixed plus. Within the extending branch, it replaces the fixed prefix a(+) by (+)a. Both operations preserve order by the concatenation observation.

For a cross-branch pair s and a(+)t, the nonextending s has exactly two possibilities. If s = (-)^beta for beta < alpha, then s is a proper prefix of a(+)t and the next source sign is minus. Its image (+)(-)^beta is a proper prefix of (+)at, again followed by minus. If instead s first differs from a at beta < alpha, its sign there is plus and the other sequence's sign is minus. The same first difference occurs after the common prepended plus in the images. In both cases s is larger and its image is larger. These arguments also show prefix reflection between the branches. Finally a and e are the respective minima.

There is no omitted cross-branch case at a limit alpha: either a sequence ends before alpha, differs at an ordinal below alpha, or extends all of a. First differences exist because the domains are ordinals.

### 3.4 Complete prefix identity

For every s > a, let P(s) denote its complete set of proper prefixes. Then

P(f(s)) = {e} union {f(v) : v in P(s), v != a}.

For the nonextending branch, every prefix of s is still nonextending, and the concatenation identity gives the formula immediately. For s = a(+)t, its proper prefixes divide into (-)^beta with beta < alpha, the node a itself, and a(+)u with u a proper prefix of t. Their images, together with e, are exactly the proper prefixes of (+)at. If t is empty, the final class of prefixes is empty and (+)a is the whole image, not a missing proper prefix. If t is nonempty, (+)a is accounted for by u = e.

At alpha = 0 the map is the identity on nonnegative sequences. At alpha = omega, the sequence (+)(-)^omega has length omega, despite having a displayed initial plus. Its proper prefixes are e and (+)(-)^n for finite n. Those correspond to a and the finite all-minus prefixes of a(+) respectively. At arbitrary limit alpha the same block-prefix argument applies; no limit completion is inserted into the source class. Successor ordinals after a limit and arbitrary transfinite tails are covered by the same identity.

If Gamma is initial, all needed source prefixes lie in Gamma. Therefore Delta = f[Gamma] is initial and nonnegative. For x,y distinct from a, the identity and injectivity imply that f(y) is a proper prefix of f(x) exactly when y is a proper prefix of x. A right predecessor in Delta cannot be e, since e is the minimum. Order preservation then shows that every right-predecessor relation in Delta comes from one in Gamma. This is exactly the one-sided implication needed in the proof.

## 4. Audit of the normal-form transport

Let c_m = 2^n and c_y = 1 otherwise. On each source series replace exponent y by f(y) and coefficient r_y by c_y r_y. The construction is valid for every set-sized reverse-well-ordered support: the increasing exponent bijection preserves its complete order type, and the nonzero scalars preserve its support. There is no restriction to finite, countable, or bounded-birthday supports.

Addition remains coefficientwise under an injective exponent relabeling. Cancellation at common exponents is identical before and after the map. The largest exponent in a nonzero difference remains largest, and its coefficient keeps its sign. Thus the map is an injective order-group homomorphism, and its image H is a subgroup. No multiplicative identity or product law is transported or needed.

The canonical Hahn image of H satisfies every characterization requirement:

1. Its exponent class is Delta. Every exponent occurs as a unit monomial in H, and no other exponent can occur.
2. A target truncation is exactly the image of the corresponding source truncation, for every ordinal truncation index. Hence truncation closure is retained.
3. At every exponent other than zero, the source unit monomial maps to the target unit monomial. At zero the source least positive element, 2^(-n) omega^m, maps to 1. This special check is essential because the source unit monomial at m instead maps to 2^n.
4. The zero coefficient group is precisely Z. At any other f(y) it is precisely R_y. Exactness follows because a one-term image cannot originate from a source with additional nonzero terms. All these coefficient groups are initial in R.
5. A target right predecessor comes from a source right predecessor. Its source exponent is not m, so its coefficient group is unscaled and contains the dyadics as required. No new obligation is imposed on the normalized zero coefficient group.

Theorem 5.1 now gives initiality of H in No. All its exponents are nonnegative, and its exponent-zero coefficient is integral, so it lies in Oz. Initiality in No implies initiality for the inherited simplicity order on Oz. The trivial group has already been treated separately. The full stated conclusion follows.

## 5. Proper-class and logical scope

The parameters alpha and n are sets, even if G and Gamma are proper classes: alpha is the sign length of one particular surreal m. Sign concatenations have ordinal, hence set, length. NBG class replacement sends each individual support to a set. Elementary class comprehension defines the displayed exponent map, series map, and image class, allowing the source class as a parameter. No truth predicate, class-sized sum, proper-class support, global enumeration, or stronger class-recursion principle is used by the new construction. The source characterization is invoked in its stated NBG/global-choice setting.

A possible hidden pitfall would have been to replace H by the full Hahn product over Delta. The candidate does not do that: it transports only the series actually belonging to G. Therefore it does not silently add limit sums or require closure under arbitrary summation.

## 6. Corrections, diagnostics, and priority limits

No correction to the pinned manuscript is needed. The explicit inverse and ordered-sum prefix argument in Section 3 are optional expository additions. The source version should continue to be described as the authenticated author manuscript rather than as a byte-verified publisher PDF.

Independent diagnostics use an ordinal-Cantor-normal-form model and run-length sign sequences, including finite ordinals, omega, successors of omega, omega squared, and a minimum of length omega cubed + omega + 1. They check order, inverse recovery, sampled prefix relations, the right-predecessor implication, and finite-support coefficient transport. Deliberate mutations omit the branch-sign deletion, retain a nonzero minimum, omit bottom scaling, or append instead of prepend the plus. All are rejected. These tests are evidence against implementation mistakes; the mathematical proof for all ordinals, arbitrary supports, and proper classes is Sections 2–5 above, not the tests. Exact counts and execution status are recorded in the acceptance report.

Targeted public searches found the original question, its earlier thesis occurrence, and the cited characterization paper, but no later resolution. This is not an exhaustive novelty certificate. In particular, the group result has not been confused with the already-known subdomain theorem, and the related dense-group set-model question is outside this audit. Mathematical acceptance does not certify that no other author has already proved the target.
