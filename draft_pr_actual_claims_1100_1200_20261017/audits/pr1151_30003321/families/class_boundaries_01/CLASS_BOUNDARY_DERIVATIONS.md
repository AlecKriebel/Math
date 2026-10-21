# Independent class and boundary derivations

These are this shard's checkable arguments. They use only the pinned candidate and the two pinned primary originals. They do not use any previous audit. Finite computations corroborate the arguments but do not prove their transfinite statements.

## 1. Coefficients of actual series are in the one-term coefficient groups

If a truncation-closed additive subgroup contains

    x = sum_{i<lambda} r_i omega^{y_i},

then for each i<lambda the truncations at i and i+1 are in the subgroup (the latter is x itself when i+1=lambda). Their difference is r_i omega^{y_i}. Thus every actual coefficient r_i belongs to R_{y_i}={r: r omega^{y_i} is in the subgroup}.

This resolves a potential hidden inference near candidate lines 80–83: knowing that the *one-term* group at exponent zero is Z forces the zero coefficient of *every* image series to be integral because the image group is truncation closed. Without truncation closure that inference would fail.

## 2. Least-positive classification, including the possible infinite tail

Let g>0 be least in G, and write its leading term as r omega^m with r>0. That monomial lies in G by truncation. The remaining tail h=g-r omega^m also lies in G. If h is nonzero, its leading exponent is less than m, so for every positive real epsilon,

    |h| < epsilon omega^m.

In particular, choose epsilon=r/2. Then g>r omega^m/2>|h|>0, contradicting least positivity. This argument allows any set ordinal support length; it does not assume a finite tail. Hence g is one term.

The initial real group R_m has least positive r. The pinned Lemma 5.1 yields R_m=2^{-n} Z and r=2^{-n}; its other nonzero case contains all dyadics and has no least positive element. If y<m were in Gamma, cross sectionality would put omega^y in G, with 0<omega^y<g. Thus m is the least exponent.

For an initial exponent class with minimum m, any plus in m gives a proper prefix below m. Consequently m is all minus, of length some set ordinal alpha, and m=-alpha. Neither a proper-class alpha nor an infimum missing from Gamma is introduced: m is the leading exponent of the actual surreal g and is an actual member of Gamma.

## 3. Sign concatenation at arbitrary ordinals

Write a=-^alpha and use ordered sums of well-ordered sign sequences. If s>a, either a is not a prefix of s (case A), or s=a + t for a unique set-length tail t (case B). In case B, the sign immediately after the displayed a must be + by s>a.

The map is

    f(a)=empty,
    f(s)=+ s                    in A,
    f(a + t)=+ a t              in B.

All symbols here denote concatenation. For example, when alpha=omega the original distinguished + in a+ is at ordinal position omega; it is this sign that is removed. There is no inference that the two concatenations have the same ordinal index positions. The tails are identified through the unique order isomorphism of their underlying final segments.

### Order and proper prefixes

Inside each case, common-prefix concatenation preserves order and proper prefixes. Across cases take s in A and u=a+t in B. If s=-^beta for beta<alpha, then s is a proper prefix of u, and u is below s because its next sign is minus. Their images have the same relation. Otherwise s first differs from a by a plus at a position beta<alpha. That first difference makes s>u, and after the common initial plus the image comparison still has + versus - at the corresponding point of the ordered sum. These images cannot be prefix-comparable. This proves order preservation, injectivity, and preservation/reflection of proper prefixes away from a.

### Complete proper-prefix identity

For s>a,

    Prefix(f(s)) = {empty} union { f(v): v proper-prefix s and v != a }.   (* )

In A, nonempty prefixes are exactly +v for proper prefixes v of s. Such v cannot extend a, since s does not. Thus these are exactly f(v).

In B, write s=a+t. The proper prefixes of +at are exactly:

- the empty word;
- +-^beta for beta<alpha;
- +au for u a proper prefix of t.

The preimages are respectively a, -^beta, and a+u. The last family includes the empty u exactly when t is nonempty. If t is empty, +a is the full image rather than a proper prefix. The source prefix a is omitted from the second part of (*) and supplied by the empty image. This checks the endpoint that otherwise risks an off-by-one error.

This is a decomposition of initial segments of ordered sums, so it applies without a cofinality, cardinality, countability, successor, or limit restriction on alpha or on the tail length. For alpha=0 it reduces to the identity map on nonnegative signs. The case alpha=omega is illustrative; it is not used as a surrogate for arbitrary limit ordinals.

If Gamma is initial, every source prefix in (*) belongs to Gamma. Hence Delta=f[Gamma] is initial in No. Every nonempty image begins with plus and f(a)=0, so Delta is nonnegative with minimum zero.

If f(y) is a right proper prefix of f(x), f(y)>f(x) rules out y=a, while f(x) having a predecessor rules out x=a. Prefix reflection and monotonicity therefore give y a right proper prefix of x. A new root is introduced only as a left predecessor. No new right-predecessor dyadic obligation appears.

### Optional explicit inverse on the whole ray

The same surgery is an order isomorphism from the entire ray [a,infinity) onto [0,infinity). For z>0 write z=+v. If a is a prefix of v, write v=at and let the inverse be a+t. Otherwise let the inverse be v. In the latter case v>a: if v<a, v would have to extend the all-minus a by a minus and hence would have a as a prefix. At zero the inverse is a. These formulas verify both compositions directly and are elementary set formulas.

Restricting this inverse to Delta gives the inverse of f:Gamma->Delta. No selection principle is needed for this inverse.

## 4. The actual image group and bottom normalization

Define c_m=2^n and c_y=1 otherwise. Every input series has a set-sized reverse-well-ordered support S. Order preservation implies f[S] has the identical reverse order type. The same enumeration of the support can be used for the transformed normal form; no new terms are inserted.

For two series, coefficientwise addition takes place on the set S union S'. This union is reverse well ordered: the maximum of any nonempty subset is the maximum of its maxima in the two pieces that it meets. Zero coefficients can then be deleted. Fixed coordinate factors and injective f commute with this addition. A leading nonzero coefficient keeps its sign, proving injectivity and order preservation.

Let H be exactly the image T[G]. Then H is closed under + and negation because G is, and T has an inverse on H by reversing its graph. The map is therefore an ordered-group isomorphism onto H. No claim is made that every series supported in Delta belongs to H.

A one-term image comes from a one-term input, because exponents are relabeled injectively and coefficients never become zero. Therefore the exact one-term groups are Z at f(m)=0 and R_y at f(y)>0. The normalized bottom monomial 2^{-n} omega^m provides 1; every other source cross section omega^y maps to omega^{f(y)}. Images of truncations are the corresponding truncations of images.

For right-predecessor pairs in Delta, Section 3 supplies the same source obligation. Its upper exponent cannot be m because m was minimum. That coefficient group is unchanged and contains D as required. All conditions of the pinned Theorem 5.1 hold for the *actual image subgroup*. It follows that H is initial in No.

By Section 1, every zero coefficient is an integer, and all exponents are nonnegative. The pinned characterization of Oz then gives H subset Oz. The result is initial in the full No tree, which in particular proves initiality with the simplicity relation inherited by Oz.

## 5. NBG and global-choice obligations

Every object transformed individually is a set: a surreal is a set-length sign sequence; its leading exponent and support exponents are sets; alpha is the set domain length of m; n is finite; all coefficient pairs form a set.

The graph of f is specified by elementary formulas with alpha as a set parameter. Concatenating finitely many set sign sequences uses ordinary set ordinal sums. Cutting off a prefix and transferring the tail uses a unique order isomorphism between set well-orders, obtained by ordinary set recursion. This does not invoke elementary transfinite recursion with class-valued states.

The normal-form operation and its inverse are the established class maps from the source. NBG class replacement maps each set support through f and the fixed coefficient factors to a set. Consequently T is an elementary definable class map on the relevant surreal class, with the class G allowed as a parameter for domain restriction. The image H={h: exists g in G, T(g)=h} uses only set quantifiers, so elementary class comprehension suffices. Its inverse is the converse graph restricted to H, not a choice of preimages. If G is a set, replacement also makes H a set. If G is a proper class, injectivity and class replacement rule out a set-sized H.

There is no global enumeration, proper-class cut, proper-class support, class-valued recursion, or Hahn completion in the candidate construction. Global choice is part of the stated ambient theory and the published characterization theorem's scope. No stronger axiom is used by this construction. This audit makes no claim that the entire dependency theorem can be proved with global choice removed.

For a class-safe reading of the characterization theorem itself, one can reduce its proper-class instance to set instances as follows. Let Gamma_kappa be the exponents of Gamma whose sign lengths are at most kappa. It is an initial set; the tree up to a fixed set ordinal level is a set. Let A_kappa be the *existing* elements of A all of whose supports are in Gamma_kappa. This is a set, being a subclass of the set-sized Hahn group over Gamma_kappa. It inherits truncation closure, cross sections, the exact coefficient groups, and every right-predecessor constraint. Every element of A belongs to some A_kappa by replacement and the supremum of its set of support birthdays. Thus A is the union of these set instances, and initiality of each gives initiality of A. This avoids class-valued induction even if the source's well-order notation is read cautiously.

## 6. Strong boundary families

1. **Trivial group.** T is the identity on {0}; the empty support causes no least-positive appeal.
2. **Archimedean discrete initial groups.** G=2^{-n}Z has Gamma={0}, alpha=0, and T(r)=2^n r. Its image is Z, initial in No.
3. **Nondivisible groups above the bottom.** G=Z omega + 2^{-n}Z has Gamma={0,1}, no right-predecessor pair, and is initial by Theorem 5.1. Only its constant coefficient is multiplied by 2^n. The image is Z omega + Z. A uniform scalar would instead give 2^n Z omega+Z and can fail cross sectionality; the candidate correctly avoids it.
4. **Original example.** For G=D+Z/omega, Gamma={-1,0}. The map sends -1 to 0 and 0 to 1; the image is omega D+Z as in the primary question's motivating example.
5. **Limit bottom with no completion of exponents.** Let Gamma={-beta: beta<=omega}. Give the bottom coefficient group 2^{-n}Z, all other coefficient groups D, and take only finite supports. This is a discrete initial group by Theorem 5.1. Its exponent image is {0} union {2^{-k}:k<omega}, an initial set. Only actual finite sums are mapped. The formula never invents an exponent node below this image to complete it.
6. **Infinite supports without a last term.** In the same exponent class, use an existing series with support {-k:k<omega}. Its image has support {2^{-k}:k<omega}, strictly decreasing and of the same order type omega. If the original group contains only selected such series and their additive/truncation consequences, their image remains equally selective. No bottom term is appended unless present in the input.
7. **Successor and arbitrary limit ordinals.** Section 3 applies to alpha=0, finite, omega, omega+1, omega*2, omega^2, omega^omega, omega_1, and every other set ordinal, without a separate mechanism. All-minus proper prefixes and final tail prefixes are listed explicitly in (*).
8. **Maximal proper-class rays.** Fix any set ordinal alpha and n. Let Gamma=[-alpha,infinity), with coefficient group 2^{-n}Z at -alpha and R at every other exponent; take all set-supported reverse-well-ordered series. Gamma is initial: any predecessor below the all-minus minimum would force its extension below that minimum. The group satisfies Theorem 5.1, has least positive 2^{-n}omega^{-alpha}, and is a proper class. The explicit inverse in Section 3 shows that f[Gamma]=[0,infinity); its image group is exactly Oz. This is a proper-class boundary test, not an assumption that arbitrary G is full.
9. **Proper-class, non-full groups.** Take only finite sums in the preceding family. It still satisfies Theorem 5.1 and discreteness, is a proper class, and maps to the finite-normal-form subgroup of Oz with the corresponding coefficients. Thus proper-class size never forces completion.

## 7. What the failed approaches establish

Arithmetic translation of exponents by alpha is not the sign map. For alpha=omega and Gamma={-beta:beta<=omega}, translation sends Gamma to {0} union {omega-k:k<omega}, which contains omega and omits 1, so it is not initial. This independently identified failure does not affect the candidate.

An arbitrary initial ordered realization of Gamma need not preserve right-predecessor obligations. The explicit sign map proves precisely the implication that repairs this danger.

Uniformly multiplying all coefficients by 2^n can make an upper discrete coefficient group fail to contain 1. The candidate normalizes only the bottom coordinate and proves that coordinate acquires no right-predecessor obligation.

The proof establishes an additive ordered isomorphism. It does not prove multiplicativity or preservation of the original simplicity order, and neither is required. It proves more than an arbitrary ordered embedding into Oz: its exact image is an initial additive subgroup.
