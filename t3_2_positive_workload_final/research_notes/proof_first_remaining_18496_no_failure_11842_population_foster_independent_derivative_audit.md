# Independent derivative audit of the 11,842 no-failure population theorem

**Audit date:** 2026-08-12 PDT.

## 1. Exact target and verdict

This is an independent derivative audit of

~~~text
research_notes/proof_first_remaining_18496_no_failure_11842_population_foster_theorem.md
b26742cfe24d40df31da01217050c4141b1955dfaf267e0e2c804000df8ae06b
287 lines / 11,447 bytes
~~~

The verdict on these exact bytes is **STRICT PASS**.  The proof gives a
statewise population-generator Foster inequality on each fixed class; it
does not compose drift-or-chart-exit rules.

The intermediate theorem at SHA `06931d...` was not sufficient as written.
It used the corrected S-tier superlevel cut without pinning the stronger
fact needed by its elementary global-top-D summation: the enabled top
S-tier must lie in the literal global top D-tier.  The exact target above
repairs this point and pins the new finite identity.

## 2. Exact finite identities

The 18,496-pair selector and its audit replay at

~~~text
src/outside_mixed_remaining_18496_certificate.py
314f378664052cabe23910e118c9a43acf99884ccb5c63b61daf014a206e4c63

tests/test_outside_mixed_remaining_18496_certificate.py
28d3cf0087bcd77e24d6dbfa280b226b34d3d026c35e743bc10487c829667769

research_notes/proof_first_outside_mixed_remaining_18496_certificate_exact_byte_audit.md
2539d8eee4d1d584ed5566f7494c7262843676dc368078647db12481d6a5822f
~~~

They select exactly 11,842 pairs having no affine-feasible failure of the
corrected cut, with fingerprint

~~~text
b425db9040d0836462f4240a4a3acf51d067d356eb4f2bfe4ce2cf648e42db26
~~~

The repaired top-S/top-D certificate replays at

~~~text
src/no_failure_11842_top_s_top_d_certificate.py
e72da319fd49df6df0c34a9a3090d95f2baf30199c0464966f9081990e347b4a

tests/test_no_failure_11842_top_s_top_d_certificate.py
ea8d042875c0c4f5c47bdabdaddc913e70138db7becedddafbe72c171ea1b572
~~~

Its five tests pass.  Over all 3,010,738 exact affine-feasible incidences it
finds zero corrected-cut failures, zero empty top S-tiers, and zero cases in
which the top S-tier is not contained in the global top D-tier.  Its exact
incidence and summary fingerprints are

~~~text
a965d56c3b116a603ae147ad9bf22450c5cec9fb81477a3f99366920a0482ec8
8f83a44a578f45597ea968c551d5dcdbba5a529833ba9eea01e14f1179af6bf5
~~~

The finite calculation enumerates support/descriptor/affine identities
only.  It does not enumerate orientations, rates, populations, stochastic
paths, or communicating classes.

## 3. Fixed-class logical bridge

Let an escaping sequence lie in one closed population class.  Tier
compactness supplies one of the 259 exact descriptors.  The necessity half
of the affine flag theorem makes that descriptor affine-feasible, because
all sequence increments lie in the fixed stoichiometric subspace.  The
11,842 selector therefore forces the corrected cut to pass, and the new
identity puts its nonempty top S-tier \(E\) inside the literal global top
D-tier.

For the linkage superlevel \(U_L(r)\) supplied by the corrected cut, strong
connectivity forces the first edge leaving \(U_L(r)\).  Its source lies in
\(E\), hence in both global top tiers, and its target is strictly D-lower.
This is valid for every strong orientation by a directed-cut argument; no
orientation search is used.

The stronger top-D inclusion is genuinely load-bearing for the elementary
proof.  Outside the certified set it can fail: an enabled descent below a
wholly disabled higher D-tier does not by itself control an upward jump into
that higher tier.  The new zero-exception identity eliminates precisely
this possibility on the intended 11,842 pairs.

## 4. Entropy and fourth-power calculation

The repaired entropy estimate uses
\(\bar x_i=x_i\vee1\):

\[
 V(x-y+z)-V(x)
   =\log {\bar x^z\over\bar x^y}+O(1).              \tag{4.1}
\]

The bars are necessary when a jump creates the first molecule of a
bounded-zero species.  On bounded coordinates the entire contribution is
uniformly bounded, while on divergent coordinates (4.1) is the usual
first-difference formula.  The selected edge therefore contributes
\(-cA_ng_n\), where \(A_n\) is a maximal enabled-source propensity and
\(g_n\to\infty\).  The standard finite tier summation makes every other
term subordinate, so \({\cal L}V(x_n)\to-\infty\).

The optional discrete population potential is also valid:

\[
 G=K+\sum_i\log(x_i!),\qquad W=G^4.
\]

For bounded binary jumps,

\[
 |\Delta G|\le C\log(2+|x|),\qquad
 \sum_e a_e\le CA_n,\qquad
 G\asymp |x|\log(2+|x|).
\]

In the exact fourth-power expansion, the largest positive remainder divided
by the leading \(G^3A_ng_n\) term is bounded by

\[
 {C\{\log(2+|x_n|)\}^2\over G(x_n)g_n}\longrightarrow0.
\]

Thus \({\cal L}W(x_n)\to-\infty\) as claimed.  The paragraph does not rely
on a one-jump positive-moment assertion and is unaffected by disabled-target
activation counterexamples from the remaining failure pairs.

## 5. Stochastic handoff and boundary

Nonexplosion follows independently.  A quadratic source cannot increase
total molecularity in the binary universe; all increasing hazards are at
most linear in total population and jumps are bounded.  A linear pure-birth
comparison prevents population escape, while finite population sublevels
have bounded total hazard.

The bad-sequence contradiction gives a statewise inequality
\({\cal L}V\le-1\) outside a finite subset of the fixed class.  Localization
on finite population sublevels, Dynkin's formula, Fatou, and irreducibility
then yield finite mean return to a reference state.  No marked potential,
structural-exit circulation, or terminal-SCC claim is used.

The verdict is limited to the exact 11,842 no-failure pairs.  It makes no
claim on the remaining 6,654 pairs with B/B, B/F0, or AA failures.

## 6. Reproduction and render

The exact top-S/top-D test run completed with

~~~text
Ran 5 tests in 153.154s
OK
~~~

The target contains no hidden control bytes.  Independent Pandoc/Tectonic
rendering produced five letter pages with zero diagnostics.  Every page was
rasterized and visually inspected; equations, hashes, headings, and page
breaks are clean.
