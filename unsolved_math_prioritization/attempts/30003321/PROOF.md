# Discrete initial surreal groups admit initial omnific models

Problem 30003321. Publication edition, 10 October 2026. The complete proof received an affirmative independent internal mathematical audit; no mathematical correction was required.

## Review status of this edition

This is an AI-assisted mathematical proof accompanied by an independent internal AI mathematical and source audit. The authored documents are unrefereed. Acceptance records that audit's full affirmative verdict within the stated source theorems and NBG/global-choice setting. It is not external human peer review, journal acceptance, formal proof-assistant certification, or a novelty or exhaustive-priority claim. The proof dependencies were checked against the authenticated author manuscript, not a byte-authenticated publisher PDF.

## Statement

Work in NBG with global choice. Every discrete initial ordered additive subgroup G of the surreal numbers No is order-group-isomorphic onto an initial subgroup of the omnific integers Oz. Here groups and initial subclasses may be sets or proper classes. Initiality means closure under sign-sequence prefixes (simplicity), not convexity in the numerical order. The resulting isomorphism need not preserve the original simplicity order. No closure under multiplication is assumed.

The trivial group is handled by the identity map on {0}. Henceforth G is nontrivial and has a least positive element.

## Established inputs

Use the following results of Ehrlich and Kaplan, *Number systems with simplicity hierarchies: a generalization of Conway's theory of surreal numbers II*, Journal of Symbolic Logic 83 (2018), 617–633, DOI 10.1017/jsl.2017.9; the article retains the target as Question 9.1. References to theorem numbers below are to this work.

1. Every surreal has a unique normal form sum of real coefficients times omega to surreal exponents, with a set-sized reverse-well-ordered support. Addition is coefficientwise and order is determined by the leading nonzero coefficient (Proposition 3.3 and the normal-form preliminaries).
2. The nonzero initial additive subgroups of R are precisely 2^(-n) Z for n a nonnegative integer, and the subgroups containing D = Z[1/2] (Lemma 5.1).
3. An additive subgroup is initial precisely when its corresponding Hahn-series subgroup A is truncation closed and cross sectional, its exponent class Gamma is initial, each coefficient group R_y is initial in R, and D is contained in R_y whenever y is a right simplicity predecessor of another exponent x in Gamma (Theorem 5.1). A right simplicity predecessor means y is a proper sign prefix of x and y > x.
4. A surreal lies in Oz precisely when every exponent in its normal form is nonnegative and the coefficient of exponent zero, if present, is an integer (Section 6.2).

Public sources: https://arxiv.org/abs/1512.04001 ; https://elliotakaplan.github.io/Number_systems_with_simplicity_hierarchies_II.pdf . The original Oberwolfach question is Question 1 in the Kaplan–Ehrlich contribution to DOI 10.4171/owr/2016/60.

## Lemma 1: discreteness supplies a bottom exponent

Let A be the Hahn-series version of a nontrivial discrete initial subgroup G. Then its exponent class Gamma has a least member m, m = -alpha for an ordinal alpha, and R_m = 2^(-n) Z for some nonnegative integer n. The least positive group element is 2^(-n) omega^m.

Proof. Let g be the least positive element, with leading term r omega^m, r > 0. Truncation closure gives r omega^m in G. If the remaining tail h is nonzero, then h belongs to G by subtraction and is infinitesimal relative to the leading term. Consequently 0 < |h| < g, a contradiction. Thus g = r omega^m.

The coefficient group R_m has r as its least positive member. Lemma 5.1 rules out the case D contained in R_m and gives R_m = 2^(-n) Z and r = 2^(-n). Cross sectionality gives omega^y in G for every y in Gamma. If y < m, then 0 < omega^y < g, impossible. Hence m is the minimum of Gamma.

Since Gamma is initial, any proper sign prefix of m lies in Gamma. A plus sign in m would make the prefix just before that sign strictly less than m, contrary to minimality. Therefore every sign of m is minus: m = -alpha. This includes alpha = 0. QED.

## Lemma 2: moving the minimum without creating right predecessors

Let Gamma be an initial subclass of No with minimum m = -alpha. There is an order isomorphism f from Gamma onto an initial subclass Delta of No with minimum zero such that

    f(y) is a right simplicity predecessor of f(x)
    implies y is a right simplicity predecessor of x.

Here is a formula valid for every ordinal alpha, including limits. Denote sign-sequence concatenation by a centered dot, the empty sequence by e, and the all-minus sequence of length alpha by a. Thus a is m. Define:

- f(a) = e.
- If s > a and a is not a prefix of s, set f(s) = (+) · s.
- If s > a and a is a prefix of s, its next sign must be plus, so write uniquely s = a · (+) · t and set f(s) = (+) · a · t.

These are concatenations of sequences, not arithmetic additions of their ordinal lengths. In the final case exactly the displayed plus following a is removed after a plus is prepended. The formula does not remove a sign at a guessed integer position.

Proof of order and injectivity. Call the second and third cases A and B. Inside A, prepend the same plus; this preserves both lexicographic order and proper-prefix relations. Inside B, replace the common prefix a · (+) by the common prefix (+) · a; order and proper-prefix relations of the tails are unchanged.

For a member s of A and a member u of B, s either is an all-minus proper prefix of a or first differs from a by a plus at some position beta < alpha. In the former case, s > u and s is a proper prefix of u; its image is a proper prefix of f(u), whose next sign is minus, so f(s) > f(u). In the latter case, s > u, their images have the same first differing signs after the common prepended plus, and neither pair is prefix-comparable. Thus order and proper-prefix relations agree across the cases as well. This also prevents collisions between A and B. Finally, a was the least source element, f(a) is zero, and every other image starts with plus. Thus f is strictly increasing and injective on all of Gamma. Its restriction away from a preserves and reflects the proper-prefix relation.

Proof of initiality. For every s > a the complete set of proper prefixes of f(s) is

    {e} union {f(v): v is a proper prefix of s and v != a}.     (1)

In case A this follows by stripping the first plus. In case B, a prefix of (+) · a · t is either empty, of the form (+) · (minus)^beta for beta < alpha, or of the form (+) · a · u for u a proper prefix of t. These are respectively f(a), f((minus)^beta), and f(a · (+) · u). They account for every prefix, including prefixes whose length is a limit ordinal. All their preimages lie in Gamma because Gamma is initial. Zero has no proper prefixes. Therefore Delta = f[Gamma] is initial.

Proof of the right-predecessor assertion. If f(y) is a right predecessor of f(x), then neither image is zero: zero is least in Delta and has no predecessors. Thus x,y differ from a. The proper-prefix equivalence proved above and strict monotonicity yield y a proper prefix of x and y > x. QED.

For alpha = 0 the formula is the identity on nonnegative surreals. At a limit alpha, the string (+) · (minus)^alpha is an actual set-length sign sequence; it occurs as the image of a · (+), if that source node is present. Its proper prefixes arise from the source nodes (minus)^beta, beta < alpha. No completion node is assumed to exist in Gamma unless it is forced by a node actually in Gamma.

## Theorem: the required initial Oz model

Use Lemma 1 to obtain m = -alpha and R_m = 2^(-n) Z. Use Lemma 2 to obtain f: Gamma -> Delta, where Delta is initial, nonnegative, and f(m) = 0. Define positive real scaling factors c_m = 2^n and c_y = 1 for y != m. Define the coefficientwise transformation

    T(sum_y r_y omega^y) = sum_y (c_y r_y) omega^(f(y)).

Each input support is a set-sized reverse-well-ordered set. Since f is strictly increasing, its image is again such a support, with exactly the same order type. Thus the displayed normal form exists as a surreal. Nonzero coefficients stay nonzero.

The map T is additive: addition of Hahn series is coefficientwise, each coefficient is multiplied by one fixed scalar, and different exponents remain different. It is injective and order preserving because a nonzero leading coefficient remains nonzero and retains its sign. Let H = T[G]; by definition T is onto H and H is an ordered additive subgroup of No.

We check every hypothesis of Theorem 5.1 for H:

- Its exponent class is exactly Delta.
- Truncation closure: every truncation of T(g) is T applied to the corresponding truncation of g, hence lies in H.
- Cross sectionality: for y != m the source omega^y maps to omega^(f(y)). At zero, the source 2^(-n) omega^m maps to 1.
- Coefficient groups: at zero the group is c_m R_m = Z; at f(y) for y != m it is exactly R_y. These are all initial subgroups of R. Exactness follows from injectivity of exponent relabeling: a one-term image can only come from a one-term source.
- Right-predecessor condition: if z = f(y) is a right simplicity predecessor of f(x), Lemma 2 gives y a right predecessor of x in Gamma. Moreover y != m, since f(m) = 0 is the minimum. The source condition gives D contained in R_y, and this coefficient group is unchanged at z. Thus the target condition holds.

Theorem 5.1 therefore shows that H is initial in No. All of its exponents are nonnegative and its zero coefficient is integral, so H is a subgroup of Oz. Since Oz has the inherited simplicity order, initiality in No in particular implies initiality in Oz. This proves the theorem. QED.

## Set and proper-class bookkeeping

No global enumeration or class-length support is used. The ordinal alpha and the integer n are sets. The sign-sequence surgery is a class function specified by elementary formulas with these set parameters. On each individual sign sequence its concatenations have ordinal, hence set, length. Each normal-form support is a set, and its image under the class function f is a set by class replacement in NBG. Its reverse-well-ordering follows from order preservation, independently of its cardinality. The class H is defined as the image class of G under this explicit class function T. All group calculations involve finitely many elements and their set supports. The argument therefore works unchanged when Gamma or G is a proper class and requires no stronger class-recursion principle.

## Scope and limitations of the claim

This proof uses the additive-group characterization, not the theorem about initial subdomains. It changes the exponent embedding and rescales the bottom coefficient group; it does not claim that G is originally contained in Oz or that T preserves simplicity. The two elementary transformations combine to eliminate negative exponents without creating a new dyadic-divisibility obligation.

A targeted public literature search on 10 October 2026 located the original question, the 2018 article, and the earlier thesis formulation, but no later resolution. This limited search does not establish novelty or certify that the problem remained open through that date. The proof's mathematical validity is separate from priority. The independent internal audit in AUDIT_REPORT.md accepts the complete stated target; further external review remains welcome.
