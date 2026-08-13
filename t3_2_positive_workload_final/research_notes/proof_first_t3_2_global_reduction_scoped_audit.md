# Independent scoped audit of the global T3-2 reduction

**Proof-first hostile audit, 2026-08-12 PDT.**  The exact target currently
audited is

```text
4659114cbf1ecc5174d2cd6f741ffda5a10faa327e16e83130ba979986a468c9
    research_notes/proof_first_t3_2_global_theorem.md
```

at 163 lines and 7052 bytes.  The target was not edited during this audit.
The hash is provisional only because target Section 4 still contains an
explicit placeholder for the final two-linkage theorem and audit hashes.
The arguments in target Lemmas 2.1 and 3.1 and the linkage-count composition
are already frozen at these bytes.  No support, orientation, reaction-word,
or population enumeration was used.

## 1. Verdict and exact scope

**STRICT PASS for Lemmas 2.1 and 3.1 and for the zero/one/two linkage
reduction.**  Fixed-coordinate deletion gives an exact generator conjugacy
on the chosen closed irreducible class; deleting dormant linkages and merging
projected linkages cannot increase the linkage count; and quadratic
population-neutral clocks cannot cause explosion.  No counterexample exists
among the three apparent failure modes attacked below.

**CONDITIONAL PASS for the global conclusion at the current bytes.**  The
one-linkage dependency and its audit match their displayed exact hashes.  The
two-linkage dependency is deliberately not yet hash-pinned in the target.
Once that standalone theorem and its hostile audit earn strict exact-byte
passes, inserting their hashes is the only mathematical dependency left in
the target.  This scoped audit neither assumes nor re-proves any local
one-linkage or two-linkage recurrence estimate.

## 2. Exact fixed-class projection

Let \(\phi\) delete precisely the population coordinates constant on the
closed irreducible class \(\Gamma\), and let
\(\overline\Gamma=\phi(\Gamma)\).  Fix an original linkage \(L\) with a
complex \(y_0\) enabled at some \(x\in\Gamma\).  Writing
\(r=x-y_0\ge0\), every directed complex path

\[
 y_0\longrightarrow y_1\longrightarrow\cdots\longrightarrow y_k
 \tag{2.1}
\]

is the literal executable population path

\[
 r+y_0,\ r+y_1,\ldots,\ r+y_k.                            \tag{2.2}
\]

The target of one step contains the next source, and every reached state
lies in \(\Gamma\) by closure.  If coordinate \(i\) has the constant value
\(m_i\) on \(\Gamma\), then

\[
                    m_i=r_i+(y_j)_i                       \tag{2.3}
\]

along (2.1).  Strong connectivity reaches every complex of \(L\), so all
of them have one common \(i\)-stoichiometry, say \(c_{L,i}\).  Because
\(y_0\) was enabled, \(m_i\ge c_{L,i}\), and therefore

\[
            a_L:=\prod_{i\ {m deleted}}(m_i)_{c_{L,i}}>0. \tag{2.4}
\]

For every labelled reaction \(y\to z\) in \(L\), and every
\(x\in\Gamma\), stochastic mass action consequently gives the exact
identity

\[
 \kappa_{y z}(x)_y
   =\bigl(\kappa_{y z}a_L\bigr)
      \bigl(\phi(x)\bigr)_{\phi(y)}.                       \tag{2.5}
\]

There is no hidden enabling implication in (2.5): the deleted part of every
source in the active linkage is bounded by the fixed value \(m_i\), while
the retained part is enabled exactly when its projected source is enabled.
Thus each projected labelled rate is a fixed positive mass-action rate, not
a state-dependent effective rate.

The map \(\phi:\Gamma\to\overline\Gamma\) is bijective: injectivity follows
because every deleted coordinate has its fixed class value, and surjectivity
is the definition of \(\overline\Gamma\).  Equation (2.5) intertwines every
off-diagonal generator entry.  It also shows that a projected reaction
enabled from \(\overline\Gamma\) has its original endpoint in \(\Gamma\).
Hence \(\overline\Gamma\) is closed.  Original communicating paths project
to communicating paths, so it is irreducible.  The restricted original CTMC
and the reduced CTMC on \(\overline\Gamma\) are therefore exactly conjugate.
This supplies the closed-and-irreducible sentence which is implicit, but not
spelled out, in the target proof.

### Dormant and coincident linkages

A linkage with no source enabled anywhere on \(\Gamma\) has identically zero
propensity there.  Deleting it before projection is essential: otherwise
deleting a deficient fixed coordinate could falsely make one of its sources
look enabled.  The target performs the operations in the safe order.

The image of a strongly connected directed graph under vertex projection is
strongly connected after coincident vertices are identified.  Deleting a
projected zero-displacement edge deletes only a loop and cannot destroy
reachability between distinct projected vertices.  In fact, (2.3) implies
that projection is injective on the distinct complexes of each active
original linkage: two such complexes with the same retained coordinates
also have the same deleted coordinates and hence are identical.  Coincident
vertices can therefore arise only between different original linkages.

If two projected linkages share a vertex, their union is strongly connected:
go to the shared vertex inside the first graph, leave it inside the second,
and use the reverse pair of directed routes for the return.  Retaining
parallel labels, or replacing identical projected labels by the sum of their
positive rates, changes no generator entry.  Merging creates no new reaction
channel; it records only the strong connectivity already present in the
union.

These observations rule out all three natural projection counterexamples:

1. different deleted stoichiometries cannot occur inside one active linkage;
2. a dormant linkage is deleted before it could be falsely enabled; and
3. vertex identification cannot split a strong linkage or create a new
   physical transition.

## 3. Linkage count and molecularity

Start with at most two original linkage classes.  Deleting dormant classes
takes a subset.  Projection sends each retained strong class to one strong
class, and merging shared images replaces two classes by one.  None of these
operations can increase the count.  Thus the final number
\(\ell_\Gamma\) of active projected linkage classes satisfies

\[
                         0\le\ell_\Gamma\le2.              \tag{3.1}
\]

Likewise, coordinate deletion cannot increase the number of species or the
total molecularity of a complex.  The reduced network therefore has at most
three dynamic species and remains binary.  This verifies that the hypotheses
of the standalone one-linkage and two-linkage theorems are inherited
literally, rather than by a later atlas restriction.

If \(\ell_\Gamma=0\), every physical reaction propensity on \(\Gamma\) is
zero.  Irreducibility then makes \(\Gamma\) a singleton.  If
\(\ell_\Gamma=1\) or \(2\), the corresponding standalone theorem applies to
the single reduced network on \(\overline\Gamma\).  There is no statewise
switch between theorem families and hence no cross-family Lyapunov
comparison.  Exact conjugacy transports the resulting positive recurrence
back to every original state of \(\Gamma\).

## 4. Nonexplosion, including neutral quadratic clocks

Put \(N(x)=1+|x|_1\).  If a channel \(y\to z\) increases total population,
then \(|z|>|y|\) and \(|z|\le2\), so \(|y|\le1\).  Finiteness of the reaction
set and bounded jump sizes give

\[
 \sum_{y\to z}\lambda_{y z}(x)(|z|-|y|)^+
                       \le C N(x).                         \tag{4.1}
\]

This implication uses only the binary source-and-target bound; weak
reversibility is not needed for Lemma 3.1.

For \(\tau_R=\inf\{t:N(X_t)\ge R\}\), the pre-exit state set is finite.
The localized minimal chain therefore has bounded total rate, including all
quadratic clocks, and Dynkin's formula is legitimate before
\(t\wedge\tau_R\).  Dropping negative increments and applying Gronwall gives

\[
 \mathbb E_xN(X_{t\wedge\tau_R})\le N(x)e^{Ct},\qquad
 \mathbb P_x\{\tau_R\le t\}\le {N(x)e^{Ct}\over R}.       \tag{4.2}
\]

The second estimate excludes escape through unbounded population in a fixed
time interval as \(R\to\infty\).  It does not by itself exclude infinitely
many population-neutral jumps, so that case must remain explicit.  Under a
fixed population cap, however, there are only finitely many population
states, and the total of all finite mass-action rates has a finite maximum.
A bounded-rate finite-state CTMC cannot make infinitely many jumps in finite
time.  Hence

\[
 \mathbb P_x\{\zeta\le t\}
 \le \mathbb P_x\{\tau_R\le t\}
    +\mathbb P_x\{\zeta<\tau_R\}=\mathbb P_x\{\tau_R\le t\}
 \longrightarrow0,                                      \tag{4.3}
\]

where \(\zeta\) is the explosion time.  Quadratic reactions may have very
large neutral rates on high population levels, but they cannot accumulate
while the chain remains in any one finite sublevel.  This closes the only
nonexplosion loophole relevant to the target.

## 5. Dependency boundary

The displayed one-linkage pins in the current target were independently
rehashed and match:

```text
b7306d448d0556beff1879796c1b399ed7786fdca086d8fd9125b0832d090563
    research_notes/proof_first_single_linkage_at_most_three_species_theorem.md
bebda68bb91bb5b22bcf4ee5d1eaf7920accde02a82210b6ffbacd9e57d6ee35
    research_notes/proof_first_single_linkage_at_most_three_species_independent_audit.md
```

The current target expressly leaves the two-linkage hashes blank.  A final
exact-byte audit must therefore (i) insert and replay those two pins,
(ii) rehash the resulting global target, and (iii) rerun the render checks.
No further reduction lemma or stochastic composition estimate is missing.
