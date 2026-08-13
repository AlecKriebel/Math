# Exact-byte audit of the final global T3-2 theorem

**Independent proof-first hostile audit, 2026-08-12 PDT.**  The immutable
target is

```text
research_notes/proof_first_t3_2_global_theorem.md
SHA-256 781d2520cbb3ad30e1749814f620d49d4c503c5c341ccd1add39a5fec31e2b7f
164 lines, 6898 bytes
```

The target was not edited during this audit.

## 1. Verdict

**STRICT PASS.**  The target proves the stated global theorem from the two
completed fixed-linkage theorems without switching potentials along a
trajectory.  Its fixed-class reduction is an exact CTMC conjugacy; dormant
linkages are removed before projection; projection and merging preserve weak
reversibility and cannot increase the active-linkage count; the zero-, one-,
and two-linkage cases are exhaustive; and the binary nonexplosion argument
also closes the population-neutral quadratic-jump loophole.  Both displayed
dependency pairs rehash exactly.  No mathematical, scope, hidden-byte, or
render blocker was found.

Here and in the target, a linkage having no source enabled on \(\Gamma\)
means that no source of that linkage is enabled at any state of \(\Gamma\).
This is the property proved and used in target lines 41--73.  It prevents a
dormant source from becoming spuriously enabled after a constant coordinate
is deleted.

## 2. Exact fixed-class conjugacy

Let \(\phi\) delete exactly the coordinates constant on the closed
irreducible class \(\Gamma\), and put
\(\overline\Gamma=\phi(\Gamma)\).  Consider an original linkage \(L\) with
a complex \(y_0\) enabled at some \(x\in\Gamma\), and write
\(r=x-y_0\ge0\).  Every directed complex path

\[
 y_0\longrightarrow y_1\longrightarrow\cdots\longrightarrow y_k
 \tag{2.1}
\]

is the literal population path

\[
                 r+y_0,r+y_1,\ldots,r+y_k.                \tag{2.2}
\]

The target of each reaction contains the next source, so the path is
executable.  Closure keeps every reached state in \(\Gamma\).  If coordinate
\(i\) is constant there with value \(m_i\), then

\[
                  m_i=r_i+(y_j)_i                         \tag{2.3}
\]

along the path.  Strong connectivity reaches every complex of \(L\), hence
all complexes of an active linkage have the same deleted-coordinate
stoichiometry \(c_{L,i}\).  Enabling of \(y_0\) gives
\(m_i\ge c_{L,i}\), and therefore

\[
        a_L:=\prod_{i\ \mathrm{constant}}(m_i)_{c_{L,i}}>0. \tag{2.4}
\]

For every labelled reaction \(y\to z\) in \(L\) and every
\(x\in\Gamma\), stochastic mass action consequently has the exact factor
identity

\[
 \kappa_{yz}(x)_y
    =\bigl(\kappa_{yz}a_L\bigr)
       \bigl(\phi(x)\bigr)_{\phi(y)}.                     \tag{2.5}
\]

Thus the projected label has a fixed positive rate constant, rather than a
state-dependent effective rate.  The retained source is enabled exactly when
the original source is enabled, because the deleted part is already supplied
by the class constants.

The map \(\phi:\Gamma\to\overline\Gamma\) is bijective: injectivity follows
from the fixed deleted coordinates, and surjectivity is the definition of
\(\overline\Gamma\).  Equation (2.5) identifies every off-diagonal generator
entry.  An enabled projected reaction has its original endpoint in
\(\Gamma\), so \(\overline\Gamma\) is closed; projected original paths make it
irreducible.  The restricted original CTMC and the reduced CTMC are therefore
exactly conjugate, not merely stochastically comparable.

### Dormancy, projection, and merging

A linkage with no enabled source anywhere on \(\Gamma\) has identically zero
propensity there and may be deleted.  The target deletes it before projection,
which is the necessary safe order.

Within an active linkage, (2.3) shows that two complexes with the same
retained coordinates also have the same deleted coordinates and hence are the
same complex.  More generally, the image of a strongly connected directed
graph under vertex identification remains strongly connected.  A projected
zero-displacement label is only a loop and makes no off-diagonal generator
entry.  If projected linkages share a vertex, their union is strongly
connected by travelling to and from the shared vertex inside the two original
strong graphs.  Retaining parallel labels, or summing their propensities,
preserves the generator exactly.

Deleting dormant classes takes a subset, projection sends each retained
strong class to a strong class, and merging replaces intersecting classes by
one.  Hence neither the dynamic-species count nor the active-linkage count can
increase.  Coordinate deletion also cannot increase molecularity.  The
reduced chain therefore inherits literally the binary, at-most-three-species,
and at-most-two-linkage hypotheses required downstream.

## 3. Exhaustive linkage routing and exact dependency pins

Write \(\ell_\Gamma\) for the number of state-changing active projected
linkages after zero-displacement labels are discarded.

* If \(\ell_\Gamma=0\), there is no state-changing transition.  Irreducibility
  makes \(\Gamma\) a singleton.
* If \(\ell_\Gamma=1\), the reduced fixed-class chain satisfies exactly the
  hypotheses of the completed one-linkage theorem.
* If \(\ell_\Gamma=2\), its two projected supports are disjoint after the
  prescribed merge and satisfy exactly the hypotheses of the completed
  two-linkage theorem.

The one-linkage target and audit independently rehash to

```text
target b7306d448d0556beff1879796c1b399ed7786fdca086d8fd9125b0832d090563
audit  bebda68bb91bb5b22bcf4ee5d1eaf7920accde02a82210b6ffbacd9e57d6ee35
```

The two-linkage target and audit independently rehash to

```text
target dae2a58f170836427ffc053ff931c1909d64ac591d77b971591b0d5814526cde
audit  a4f50dcbc2235766524ddb7000a264ec88bf04f8841b3ce9b8d4689c800ba619
```

The first theorem is analytic for any fixed one-linkage support.  The second
has an exact support-only disjoint union of all 46,872 ordered two-linkage
support pairs and analytic recurrence on each fixed pair for arbitrary strong
orientations and positive labelled rates.  No class, rate, population,
reaction history, or stochastic estimate is supplied by its finite
certificate.  Because one fixed reduced chain enters exactly one of these
three linkage cases, no Lyapunov function is compared across theorem
families.

## 4. Nonexplosion

Put \(N(x)=1+|x|_1\).  If a binary reaction increases total population, its
source has degree at most one.  Finiteness of the labels and bounded jump
sizes therefore give

\[
 \sum_{y\to z}\lambda_{yz}(x)(|z|-|y|)^+
                         \le C N(x).                      \tag{4.1}
\]

For \(\tau_R=\inf\{t:N(X_t)\ge R\}\), localized Dynkin and Gronwall yield

\[
 \mathbb E_xN(X_{t\wedge\tau_R})\le N(x)e^{Ct},\qquad
 \mathbb P_x\{\tau_R\le t\}\le {N(x)e^{Ct}\over R}.     \tag{4.2}
\]

This excludes population escape in finite time.  It must still be checked
that population-neutral quadratic clocks cannot accumulate.  Under a fixed
population cap there are finitely many states and the total of the finitely
many mass-action rates is bounded.  A bounded-rate finite-state CTMC cannot
make infinitely many jumps in finite time.  Letting \(R\to\infty\) therefore
proves nonexplosion of the minimal chain.

## 5. Recurrence transport and claim boundary

Positive recurrence of the reduced chain transports state for state through
the bijective CTMC conjugacy \(\phi\).  Since the original closed irreducible
class \(\Gamma\) was arbitrary, every state in every such class is positive
recurrent.  Together with Section 4 this is exactly Theorem 1.1.

The target claims no result for more than three dynamic species, more than two
active projected linkages, or molecularity greater than two.  Its intrinsic
fixed-class extension is justified by the same conjugacy and therefore does
not enlarge any analytic dependency beyond its verified scope.

## 6. Byte and render replay

The target hash was rechecked before and after the audit.  It is ASCII text
with no control byte other than line feed.  Pandoc with TeX math and Tectonic,
using one-inch letter-page margins, produced a three-page PDF with empty
standard output and standard error.  All three pages were inspected at full
resolution: formulas, hashes, symbols, margins, and page breaks are intact;
there is no clipping, malformed TeX, overfull box, or orphaned fragment.

This audit was rendered by the same pipeline and inspected independently.
