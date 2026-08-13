# Population-Foster closure of the 11,842 no-failure pairs

**Proof-first standalone theorem, 2026-08-12 PDT.**  This note closes the
11,842 support pairs in the exact 18,496-pair outside-mixed remainder which
have no affine-feasible failure of the corrected S-tier-superlevel cut.  The
proof is global on each fixed population class.  It uses one population
function and a statewise generator inequality; it has no reaction mark,
chart exit, terminal strongly connected component, or potential switch.

Finite computation is used only for the exact support/descriptor set
identity.  No orientation, rate vector, population state, stochastic path,
or communicating class is enumerated.

## 1. Exact finite input

Let \(\mathcal C_2\) be the ten binary complexes on three species.  Begin
with all 46,872 ordered disjoint pairs of nontrivial supports, remove the
27,894-pair orbit of the inherited mixed atlas, remove the 146 pairs having a
strictly positive linear invariant, and then remove the frozen 336 level-set
pairs.  The exact remaining universe has 18,496 pairs.

For each remaining pair, the authoritative certificate checks all 259 exact
tier/cap descriptors.  A row is called a failure when

1. its rational affine flag is feasible in the pair's stoichiometric
   subspace; and
2. the exact S-tier-superlevel condition fails.

Exactly 11,842 pairs have no such row.  Denote this set by
\(\mathcal N_{11842}\).  Its exact fingerprint is

~~~text
b425db9040d0836462f4240a4a3acf51d067d356eb4f2bfe4ce2cf648e42db26
~~~

The containing 18,496-pair fingerprint is

~~~text
eb7db151e42eb9562b1a1d519ea7dad212df52c6df368ffa08edbf79410db4ad
~~~

The authoritative finite bytes are

~~~text
src/outside_mixed_remaining_18496_certificate.py
314f378664052cabe23910e118c9a43acf99884ccb5c63b61daf014a206e4c63

tests/test_outside_mixed_remaining_18496_certificate.py
28d3cf0087bcd77e24d6dbfa280b226b34d3d026c35e743bc10487c829667769

research_notes/proof_first_outside_mixed_remaining_18496_certificate_exact_byte_audit.md
2539d8eee4d1d584ed5566f7494c7262843676dc368078647db12481d6a5822f
~~~

The five dedicated tests pass.  These are set identities only.  Their
analytic implication is proved below.

For the elementary population fourth-power estimate used in Section 4, one
additional exact identity is load-bearing.  Among all 3,010,738
affine-feasible descriptors of the 11,842 pairs, the global top S-tier is
nonempty and is contained in the literal global top D-tier.  There are zero
exceptions.  The canonical incidence fingerprint is

~~~text
a965d56c3b116a603ae147ad9bf22450c5cec9fb81477a3f99366920a0482ec8
~~~

and the independent summary fingerprint is

~~~text
8f83a44a578f45597ea968c551d5dcdbba5a529833ba9eea01e14f1179af6bf5
~~~

The finite certificate and its five passing tests are

~~~text
src/no_failure_11842_top_s_top_d_certificate.py
e72da319fd49df6df0c34a9a3090d95f2baf30199c0464966f9081990e347b4a

tests/test_no_failure_11842_top_s_top_d_certificate.py
ea8d042875c0c4f5c47bdabdaddc913e70138db7becedddafbe72c171ea1b572
~~~

This stronger identity is used for the direct global-top-D domination
below.  It is not asserted to be a necessary hypothesis of the more general
Anderson--Kim tier theorem.

## 2. Process, nonexplosion, and one population function

Fix \(P\in\mathcal N_{11842}\).  Give each of its two linkage supports an
arbitrary strongly connected directed reaction graph and arbitrary positive
labelled rate constants.  Fix a closed irreducible population class
\(\Gamma\), and let \(X_t\) be the stochastic mass-action chain restricted
to \(\Gamma\).

The chain is nonexplosive.  A reaction with a quadratic source cannot
increase total molecularity because every target is binary.  Thus every
population-increasing reaction has source degree zero or one, its total
increasing intensity is \(O(1+|x|_1)\), and every jump is bounded.  A linear
pure-birth comparison bounds total population on finite time intervals.  A
fixed population sublevel is finite and has bounded total hazard, so neutral
quadratic clocks cannot accumulate there.

Use the population entropy

\[
 V(x)=\sum_{i=A,B,C}\{x_i(\log x_i-1)+1\},
 \qquad 0\log0=0.                                    \tag{2.1}
\]

It is nonnegative and proper on \(\mathbb N_0^3\), hence on \(\Gamma\).
We will prove that a finite \(K_\Gamma\subset\Gamma\) satisfies

\[
                    \mathcal LV(x)\le-1
       \qquad(x\in\Gamma,\ x\notin K_\Gamma).        \tag{2.2}
\]

This is a statewise population-generator assertion, not a chart-local
negative-or-exit alternative.

## 3. Every escaping fixed-class sequence has a physical descent

Suppose (2.2) is false.  Properness gives a sequence
\(x_n\in\Gamma\), \(|x_n|_1\to\infty\), with

\[
                          \mathcal LV(x_n)>-1.         \tag{3.1}
\]

Pass to a tier subsequence.  Completeness of the rational binary
arrangement assigns one of the 259 exact descriptors: it records the full
D-preorder, the active-coordinate set, and the exact eventual caps
\(0,1,\ge2\) of bounded coordinates.

Because \(x_n\) lies in one affine stoichiometric class, the necessity part
of the exact affine flag theorem makes this descriptor feasible for the
pair.  Indeed, at every positive weight level the normalized increments of
the sequence supply a stoichiometric direction which is zero below that
level and strictly positive on its new coordinate block.  Equivalently,
failure of such a direction would give by Gordan's alternative an affine
invariant whose constant value contradicts the prescribed divergence.

By definition of \(\mathcal N_{11842}\), this feasible descriptor cannot
fail the corrected S-tier-superlevel condition.  The exact identity pinned
in Section 1 additionally says that its literal global top S-tier \(E\) is
contained in the literal global top D-tier.  Let \(r\) be that global top
D-level.  For some linkage \(L\),

\[
 \varnothing\ne U_L(r)\subsetneq L,
 \qquad U_L(r)\subseteq E,                            \tag{3.2}
\]

where \(U_L(r)\) consists of the complexes of \(L\) at or above level
\(r\).  Strong connectivity supplies a directed path from \(U_L(r)\) to
its complement.  The first exiting edge

\[
                              y\longrightarrow z       \tag{3.3}
\]

has its source \(y\in E\), hence simultaneously in the global top S- and
top D-tiers, and its target strictly below D-level \(r\).  Thus every
orientation has a literal physical descending reaction sourced in both
global top tiers.  No orientation search is involved in this cut argument.

## 4. Entropy drift contradiction

Put \(\bar x_i=x_i\vee1\).  For a reaction \(y\to z\), the bounded binary
displacement and the factorial/entropy first-difference estimate give,
along the tier sequence,

\[
 V(x_n-y+z)-V(x_n)
       =\log {\bar x_n^z\over\bar x_n^y}+O(1).       \tag{4.1}
\]

The bars are load-bearing at a bounded-zero coordinate: the entropy jump is
finite when a reaction creates the first molecule.  They are also exactly
the coordinates used to define the D-tier preorder.  Since every source
under discussion is enabled, replacing its positive bounded coordinates by
their barred values changes only the uniform \(O(1)\) term.

Every source in \(E\) is enabled and has propensity comparable, up to fixed
positive rate constants, with the largest enabled source propensity
\(A_n\).  For (3.3), the strict D-tier gap gives

\[
 g_n:=\log{\bar x_n^y\over\bar x_n^z}
                              \longrightarrow\infty. \tag{4.2}
\]

The standard tier summation groups reactions by their source tiers.  The
edge (3.3) contributes at most \(-cA_ng_n\).  Reactions from lower S-tiers
have propensities negligible relative to the first higher tier at which
they can contribute positively, while reactions within one D-tier have
bounded logarithmic increment.  Since the reaction menu is finite, the
complete sum satisfies

\[
                          \mathcal LV(x_n)
                              \longrightarrow-\infty. \tag{4.3}
\]

This is the elementary global-top-D form of the class-local Anderson--Kim
tier contradiction.  The broader Anderson--Kim theorem only requires an
appropriate top-S-sourced D-descent; here the stronger exact identity from
Section 1 puts the selected source literally in the global top D-tier and
makes the displayed domination immediate.  Equation (4.3) contradicts
(3.1), and hence proves (2.2).

For completeness, the same conclusion may be expressed with the discrete
factorial fourth-power function

\[
 G(x)=K+\sum_i\log(x_i!)\ge1,
 \qquad W(x)=G(x)^4.                                  \tag{4.4}
\]

On the sequence above, the exact factorial calculation gives
\(\mathcal LG\le-cA_ng_n\), while

\[
 \sum_e a_e\le CA_n,
 \qquad |\Delta_eG|\le C\log(2+|x_n|_1),
 \qquad G\asymp |x_n|_1\log(2+|x_n|_1).             \tag{4.5}
\]

Expanding \((G+\Delta_eG)^4-G^4\) reaction by reaction shows that every
quadratic, cubic, and quartic remainder is lower order than
\(-G^3A_ng_n\).  Consequently \(\mathcal LW(x_n)\to-\infty\) as well.
Thus either (2.1) or (4.4) is one global population Foster function for the
whole fixed class.

## 5. Classwise recurrence theorem

> **Theorem 5.1 (the 11,842 no-failure pairs).**  For every support pair
> \(P\in\mathcal N_{11842}\), every strongly connected orientation on its
> two linkage supports, every fixed positive labelled rate vector, and every
> closed irreducible population class, the stochastic mass-action chain is
> nonexplosive and positive recurrent.

### Proof

Nonexplosion is Section 2.  Equation (2.2) gives finite mean hit of the
finite set \(K_\Gamma\) by continuous-time Foster, localized first on finite
population sublevels and then passed to the limit by Fatou.  From the finite
set, irreducibility and finitely many fixed labelled paths give finite mean
return to one reference state by geometric repetition.  Hence every closed
irreducible class is positive recurrent.  A finite or singleton class is
already covered. \(\square\)

The proof never follows a structural exit.  It never switches between
marked and unmarked potentials, and it does not invoke a terminal SCC.

## 6. Frozen analytic dependencies and exact claim boundary

The symbolic cut, affine necessity, and fourth-power lift used above are
proved in the following frozen dependencies:

~~~text
research_notes/s_tier_superlevel_cut_and_affine151_corrected.md
d91f369d34cadfb28ddb872df8fb9f6d17799ec207da29933037f55ae95f0407
research_notes/stoichiometric_gate_feasibility.md
27b40b61903ae6c2e223d007ec08323ec9aec10e9198deb99d2d7c60d878d007
research_notes/universal_fourth_power_one_active_interface.md
9d4239f4fc6b45a9522b94b09523c9f98ac7a3b089c919bd9594f12409c78cc2
~~~

The exact 11,842-specific top-S/top-D identity used to specialize these
general inputs to the elementary global-top-D calculation is pinned in
Section 1.

The identical pair-independent population-Foster argument was independently
audited inside the frozen 432-pair theorem:

~~~text
research_notes/proof_first_active_invariant_orbit_gap_432_common_w_theorem.md
7edab78daabbf7e492851efe5326ccc228adfcb57f02cd5ff55eaa7056e034c8
research_notes/proof_first_active_invariant_orbit_gap_432_common_w_exact_byte_audit.md
1110efc0760ed8714fc4bf203739152820f6f9a18cbdc0e92716638a707140fd
~~~

The remaining 6,654 pairs have feasible failures only of type B/B, B/F0, or
AA.  They require a separate global theorem; local drift-or-chart-exit
statements do not suffice.
