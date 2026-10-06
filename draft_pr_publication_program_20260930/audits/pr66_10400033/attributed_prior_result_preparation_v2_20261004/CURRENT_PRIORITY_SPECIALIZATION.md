# Checked earlier implication of the original crossing bound

Prospective attribution correction for PR66; no final integration is recorded.

The target is Ohtsuki, *Problems on invariants of knots and 3-manifolds*,
Conjecture 2.11 (S. Willerton), printed page 405, with the primitive, additive,
mirror-odd degree-three invariant normalized to 1 on the right trefoil:
every classical knot admitting an \(n\)-crossing diagram must satisfy
\( |v_3|\le\lfloor n(n^2-1)/24\rfloor \).
Minimality, positivity, alternatingness and primeness are not hypotheses.
[Original publisher source](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf).

The decisive prior source is Thomas Fiedler and Alexander Stoimenow,
*New knot and link invariants*, accessible
[author version](https://stoimenov.net/stoimeno/homepage/papers/inv.pdf),
whose title page dates the current version February 1, 2002 and the first
version December 9, 1996. It says it is a minor update to the printed version.
The work's chapter metadata is *Knots in Hellas '98*, Series on Knots and
Everything 24, World Scientific, 2000, pages 59–79,
[DOI 10.1142/9789812792679_0006](https://doi.org/10.1142/9789812792679_0006).
The exact printed chapter body has not been read in this audit; the verified
mathematical body is the dated author version, 268871 bytes, SHA256
`193dfd4c993f2337ba17b48f524d8c71333f8717d520ba299f7b76a8cbd324b7`.
Copyrighted source bodies and their pixels are retained privately.

The exact check uses the following four points, read as complete source pages
and inspected visually:

1. Printed page 5 counts unordered crossing subsets, taking one matching
   permutation when a configuration has symmetry. Formula (1) has disjoint
   triple supports: a fully intersecting chord triple or the specified path
   type. Each triple contributes at most one signed term of absolute value 1.
   Its two-crossing term has weight \((w_p+w_q)/2\), of absolute value at most 1.
2. Printed page 6, Remark 3.1 explicitly identifies
   \(vt_3=4v_3=-J''(1)/3-J'''(1)/9\), matching the problem's normalized
   \(v_3=-(3J''(1)+J'''(1))/36\). The same page states divisibility of
   \(vt_3\) by four. No additive degree-two shift remains in this normalization.
3. Printed page 7, section 3.2 begins with the explicit universal estimate
   \( |vt_3|\le {n\choose2}+{n\choose3}\le n^3/6 \). The word "positive"
   in the preceding section heading and its separate Theorem 3.1 is not a
   hypothesis on this display. The opening sentence concerns any diagram.
4. Exactly,
   \({n\choose2}+{n\choose3}=n(n-1)(n+1)/6\). Divide the first inequality
   by four and use integer \(v_3\). This yields the original bound with its
   floor for all \(n\ge3\). For \(n=0,1,2\), the published three-arrow formula
   and the independently verified candidate give \(v_3=0\), closing the same
   small cases. Thus the target is an immediate consequence of an explicitly
   displayed earlier bound, not an inference from an abstract or search snippet.

This argument does not rely on the source's stronger page-8 assertion about
the unique maximizing torus diagram or the even-crossing maximum. Its detailed
derivation is absent there and has not been certified by this disposition.
The candidate's distinct tournament mechanism is verified mathematics, but
its novelty remains unestablished. Its even estimate has a separate checked
corollary from older ingredients, as follows.

Let m be the number of intersecting chord pairs. The same Fiedler–Stoimenow
formula (1), with at most one unit contribution per unordered triple and at
most one unit contribution per linked pair, gives
\(4|v_3|\le {n\choose3}+m\). Stoimenow, *Positive Knots, Closed Braids and
the Jones Polynomial* (2003), printed page 245, Lemma 3.2 (even valence),
states that each chord of a classical Gauss diagram intersects an even number
of other chords; its short proof invokes the Jordan curve theorem. The lemma
has no positivity or reducedness hypothesis (those occur in the separate
following Lemma 3.3). For even n≥2, every such degree is at most n−2, so
\(m\le n(n-2)/2\). Consequently

\[
|v_3|\le\tfrac14\left({n\choose3}+\tfrac{n(n-2)}2\right)
= n(n^2-4)/24.
\]

The case n=0 is zero directly. Thus the candidate's even estimate follows
from earlier published ingredients as well. This is a checked corollary; an
earlier explicit printing of the exact even formula has not been located.
It does not use the stronger, uncertified page-8 extremality assertion.
[Stoimenow 2003 primary source](https://numdam.org/item/ASNSP_2003_5_2_2_237_0.pdf).

The original candidate imports the classical Polyak–Viro arrow formula, counts
path images with coefficient 1/2 and cyclic images with coefficient 1, and
dominates the unsigned count by the expected cyclic triples in a tournament
completion. Its all-size degree identity and parity step are valid. For clear
exposition, the formula should directly credit Polyak–Viro printed page 451
and Östlund's Proposition 4 / printed page 302 symmetry correction. The frozen
proof is to remain untouched; this precision belongs in the current assessment.
[Polyak–Viro primary source](https://www.math.stonybrook.edu/~oleg/math/papers/1994-Polyak-Viro.pdf),
[Östlund primary source](https://journals.msp.org/mscand/article/download/775/774).

This audit establishes a prior full-target implication. It does not establish
the earliest occurrence, identify identical proof mechanisms, authenticate the
exact 2000 printed chapter's mathematical wording, or explain why later problem
lists continued to state the bound as a conjecture. A later conjecture listing
does not invalidate the explicit source bound and checked normalization.
No outside human has been contacted, and no assertion of endorsement or human
peer review is made.
