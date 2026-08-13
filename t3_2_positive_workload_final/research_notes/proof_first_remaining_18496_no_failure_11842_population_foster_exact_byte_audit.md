# Independent exact-byte audit of the 11,842 no-failure population theorem

**Audit date:** 2026-08-12 PDT.

## 1. Frozen target and verdict

The audited target is

~~~text
research_notes/proof_first_remaining_18496_no_failure_11842_population_foster_theorem.md
b26742cfe24d40df31da01217050c4141b1955dfaf267e0e2c804000df8ae06b
287 lines / 11447 bytes
~~~

The verdict on these exact bytes is **STRICT PASS**.

The first candidate had used the unbarred expression
\(\log(x^z/x^y)\), which is false when a target creates the first molecule
of a bounded-zero species.  The frozen target repairs that point exactly:
it puts \(\bar x_i=x_i\vee1\), uses the same barred coordinates as the
D-tier definition, and retains the bounded-coordinate contribution in the
uniform \(O(1)\) term.  This repair is load-bearing and is present in the
audited hash.

The intermediate target at SHA `06931d...` is expressly superseded.  It did
not pin the stronger top-S/top-D identity used by its elementary population
fourth-power summation.  The present target pins and invokes that identity.

## 2. Exact finite selection

The finite inputs replay at the following hashes:

~~~text
src/outside_mixed_remaining_18496_certificate.py
314f378664052cabe23910e118c9a43acf99884ccb5c63b61daf014a206e4c63

tests/test_outside_mixed_remaining_18496_certificate.py
28d3cf0087bcd77e24d6dbfa280b226b34d3d026c35e743bc10487c829667769

research_notes/proof_first_outside_mixed_remaining_18496_certificate_exact_byte_audit.md
2539d8eee4d1d584ed5566f7494c7262843676dc368078647db12481d6a5822f
~~~

The five dedicated tests pass.  They independently confirm that the
18,496-pair remainder is split into exactly 11,842 pairs with no
affine-feasible corrected-cut failure and 6,654 pairs having at least one
such failure.  The no-failure fingerprint in the target is the certificate
fingerprint

~~~text
b425db9040d0836462f4240a4a3acf51d067d356eb4f2bfe4ce2cf648e42db26
~~~

Thus the theorem applies only to the exact no-failure set.  The computation
does not enumerate orientations, rates, populations, paths, or communicating
classes.

The stronger incidence certificate replays at

~~~text
src/no_failure_11842_top_s_top_d_certificate.py
e72da319fd49df6df0c34a9a3090d95f2baf30199c0464966f9081990e347b4a

tests/test_no_failure_11842_top_s_top_d_certificate.py
ea8d042875c0c4f5c47bdabdaddc913e70138db7becedddafbe72c171ea1b572
~~~

Its five dedicated tests pass.  It streams all 3,010,738 affine-feasible
pair/descriptor incidences and finds zero corrected-cut failures, zero empty
top S-tiers, and zero incidences with top S-tier outside the literal global
top D-tier.  The canonical incidence and summary fingerprints are,
respectively,

~~~text
a965d56c3b116a603ae147ad9bf22450c5cec9fb81477a3f99366920a0482ec8
8f83a44a578f45597ea968c551d5dcdbba5a529833ba9eea01e14f1179af6bf5
~~~

The certificate checks support, descriptor, and exact affine feasibility
only.  Its source correctly says that the extra inclusion is needed for the
elementary global-top-D/fourth-power calculation, not that it is a necessary
hypothesis of the broader Anderson--Kim theorem.

## 3. Fixed-class descriptor implication

Take an escaping sequence in one closed population class.  Tier compactness
gives one of the 259 exact D/S/cap descriptors.  Because all sequence
differences lie in the stoichiometric subspace, the necessity direction of
the affine-flag theorem makes that descriptor feasible.  Since the selected
pair has no feasible failure, the corrected S-tier-superlevel condition
must hold.  The stronger finite identity also gives \(E\subseteq T^{D,1}\).
Because \(E\) is nonempty, its D-level is therefore the literal global top
D-level.

For the resulting top S-tier \(E\), the corrected cut supplies a linkage and
a proper nonempty superlevel \(U_L(r)\subseteq E\).  Strong connectivity then
forces the first edge leaving \(U_L(r)\) to be sourced in \(E\) and to have a
strictly lower D-target.  Its source is simultaneously in the global top S-
and D-tiers.  This is a symbolic path argument valid for every strong
orientation; it does not select an orientation computationally.

The exact analytic dependencies are correctly pinned:

~~~text
research_notes/s_tier_superlevel_cut_and_affine151_corrected.md
d91f369d34cadfb28ddb872df8fb9f6d17799ec207da29933037f55ae95f0407

research_notes/stoichiometric_gate_feasibility.md
27b40b61903ae6c2e223d007ec08323ec9aec10e9198deb99d2d7c60d878d007

research_notes/universal_fourth_power_one_active_interface.md
9d4239f4fc6b45a9522b94b09523c9f98ac7a3b089c919bd9594f12409c78cc2
~~~

## 4. Entropy and fourth-power replay

For \(\bar x_i=x_i\vee1\), a bounded binary jump satisfies

\[
 V(x-y+z)-V(x)
   =\log {\bar x^z\over\bar x^y}+O(1).               \tag{4.1}
\]

The formula remains valid if a bounded coordinate is zero, one, or at least
two.  On diverging coordinates it is the usual first-difference estimate;
on bounded coordinates the whole contribution is uniformly bounded.  The
strict D-gap of the certified edge therefore gives a negative top-source
term \(-cA_ng_n\), with \(g_n\to\infty\).  The finite tier summation controls
all other sources and yields \({\cal L}V(x_n)\to-\infty\).  This is a
pointwise generator contradiction, not a drift-or-chart-exit alternative.

The optional population fourth-power formulation is also correct.  With

\[
 G=K+\sum_i\log(x_i!),\qquad W=G^4,
\]

every bounded reaction has \(|\Delta G|=O(\log(2+|x|))\), the total hazard is
at most a fixed multiple of the largest enabled source propensity, and
\(G\asymp |x|\log(2+|x|)\).  In the exact fourth-power expansion, the
quadratic-through-quartic terms divided by the leading
\(G^3A_ng_n\) term tend to zero.  Hence \({\cal L}W(x_n)\to-\infty\) as
claimed.

## 5. Nonexplosion and classwise Foster handoff

A quadratic source cannot increase total molecularity in the binary
universe.  All population-increasing intensities are therefore at most
linear in total population, with bounded jumps.  A linear pure-birth
comparison prevents population escape in finite time; on each fixed
population sublevel the total hazard is bounded, so neutral quadratic
clocks cannot accumulate.  This proves nonexplosion independently of the
Foster estimate.

The statewise inequality \({\cal L}V\le-1\) outside a finite class subset is
localized on finite population sublevels.  Dynkin's formula and
nonnegativity of \(V\), followed by Fatou, give finite mean hit of that
finite subset.  Closed-class irreducibility and finitely many finite labelled
paths then give finite mean return to a reference state by geometric
repetition.  Finite and singleton classes are immediate.  No embedded-chain
return theorem, chart-exit circulation, or potential switch is silently
used.

## 6. Reproduction and publication boundary

The exact remainder-certificate command completed with

~~~text
Ran 5 tests in 83.636s
OK
~~~

The exact top-S/top-D command completed independently with

~~~text
Ran 5 tests in 152.400s
OK
~~~

Independent Pandoc/Tectonic rendering of the target produced four letter
pages with zero diagnostics.  Every page was rasterized and visually
inspected; equations, hashes, headings, and page breaks are clean.  The
source contains no hidden control bytes.

This verdict proves the classwise recurrence theorem for precisely the
11,842 no-failure pairs.  It makes no claim on the remaining 6,654 pairs and
does not validate any structural-exit composition for their B/B, B/F0, or
AA failure profiles.
