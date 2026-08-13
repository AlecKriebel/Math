# Positive recurrence for weakly reversible binary networks with three species and two linkages

**Proof-first global composition, 2026-08-12 PDT.**
This note contains the global argument only.  Its two analytic inputs are the
standalone one-linkage and two-linkage theorems.  Consequently no trajectory
is switched between local theorem families and no comparison of their
Lyapunov functions is required.

## 1. Statement

> **Theorem 1.1 (T3-2).**  Let \((\mathcal S,\mathcal C,\mathcal R,\kappa)\)
> be a finite weakly reversible stochastic mass-action reaction network.
> Assume every complex has total molecularity at most two, there are at most
> three species, and there are at most two linkage classes.  For every choice
> of positive rate constants, the minimal continuous-time Markov chain is
> nonexplosive, and every state in every closed irreducible population class
> is positive recurrent.

The same conclusion holds under the strictly more intrinsic hypothesis that,
after the exact fixed-class reduction below, a chosen closed irreducible class
has at most three dynamic species and at most two active projected linkage
classes.

## 2. Exact reduction on one closed class

Fix a closed irreducible population class \(\Gamma\).  A coordinate \(i\) is
**constant** if \(x_i=m_i\) for every \(x\in\Gamma\).  Delete all constant
coordinates, delete any linkage having no source enabled at a state of
\(\Gamma\), project every remaining complex, and merge projected linkages
which share a projected complex.  Parallel labelled reactions are retained;
zero-displacement projected reactions may be discarded because they make no
state transition.

### Lemma 2.1 (fixed-class conjugacy)

The reduced stochastic mass-action chain is exactly conjugate to the original
chain restricted to \(\Gamma\).  Its linkage classes are weakly reversible,
and projection cannot increase either the number of dynamic species or the
number of active linkage classes.

**Proof.**  Let \(L\) be a linkage containing a complex \(y_0\) enabled at
some \(x\in\Gamma\), and write \(r=x-y_0\ge0\).  If

\[
 y_0\longrightarrow y_1\longrightarrow\cdots\longrightarrow y_k
 \tag{2.1}
\]

is a directed path in \(L\), then the same physical path is executable from
\(x\): immediately before its \(j\)-th reaction the population is
\(r+y_j\), so its source is enabled.  Every reached state remains in
\(\Gamma\) by closure.  If coordinate \(i\) is constant on \(\Gamma\), then

\[
 m_i=r_i+(y_j)_i\qquad(0\le j\le k),
 \tag{2.2}
\]

and hence \((y_j)_i=(y_0)_i\) along the path.  Strong connectivity makes this
true for all complexes of \(L\).  Thus every active linkage has one common
deleted-coordinate stoichiometry, every reaction preserves each constant
coordinate, and its deleted-coordinate falling-factorial factor

\[
             \prod_{i\ \mathrm{constant}}(m_i)_{y_i}
 \tag{2.3}
\]

is a positive constant that can be absorbed into that labelled reaction's
rate constant.  The remaining propensity is precisely the stochastic
mass-action propensity of the projected source.

A linkage with no enabled source contributes no transition on \(\Gamma\).
If two projected strong linkages share a projected vertex, their union is
strongly connected: travel within the first linkage to the shared vertex and
then within the second, and reverse the route for the return.  Merging such
linkages and summing propensities of parallel labels therefore preserves the
generator exactly.  Deletion and merging cannot increase the two stated
counts.  The coordinate-deletion map is one-to-one on \(\Gamma\), and the
preceding rate identity intertwines the two generators. \(\square\)

## 3. Nonexplosion

### Lemma 3.1 (binary nonexplosion)

Every finite stochastic mass-action network in which all source and target
complexes have molecularity at most two is nonexplosive whenever it is weakly
reversible or, more generally, whenever all population-increasing channels
have source degree at most one.

**Proof.**  Put \(N(x)=1+|x|_1\).  If a reaction has a degree-two source,
then its binary target has degree at most two, so the reaction cannot increase
\(|x|_1\).  Every population-increasing channel therefore has source degree
zero or one.  Since the reaction set is finite and the jump sizes are bounded,
there is a constant \(C\) such that

\[
 \sum_{y\to z} \lambda_{y\to z}(x)
       \bigl(|z|-|y|\bigr)^+
       \le C N(x).
 \tag{3.1}
\]

Stop at \(\tau_R=\inf\{t:N(X_t)\ge R\}\).  Dynkin's formula, followed by
Gronwall, gives

\[
 \mathbb E_x N(X_{t\wedge\tau_R})\le N(x)e^{Ct}.
 \tag{3.2}
\]

Thus \(\mathbb P_x(\tau_R\le t)\le N(x)e^{Ct}/R\), which tends to zero as
\(R\to\infty\).  Before \(\tau_R\), the state space is finite and its total
jump rate is bounded, so population-preserving quadratic reactions cannot
accumulate infinitely many jumps in finite time.  Hence the explosion time is
almost surely infinite. \(\square\)

## 4. The linkage split

Apply Lemma 2.1 to \(\Gamma\), and write \(\ell_\Gamma\) for the number of
active projected linkage classes.

If \(\ell_\Gamma=0\), no reaction changes a state of \(\Gamma\).  Since
\(\Gamma\) is irreducible, it is a singleton and is positive recurrent.

If \(\ell_\Gamma=1\), apply the one-linkage theorem and audit with SHA-256
values

```text
target b7306d448d0556beff1879796c1b399ed7786fdca086d8fd9125b0832d090563
audit  bebda68bb91bb5b22bcf4ee5d1eaf7920accde02a82210b6ffbacd9e57d6ee35
```

That theorem is analytic: its nonstandard faces are closed by all-clock
physical stopping arguments, not by enumerating orientations, reaction
histories, or population boxes.

If \(\ell_\Gamma=2\), apply the two-linkage theorem and audit with SHA-256
values

```text
target dae2a58f170836427ffc053ff931c1909d64ac591d77b971591b0d5814526cde
audit  a4f50dcbc2235766524ddb7000a264ec88bf04f8841b3ce9b8d4689c800ba619
```

That theorem partitions the exact 46,872 ordered support pairs into five
disjoint fixed-pair branches and proves each branch analytically for arbitrary
strong orientations and positive labelled rates.  Finite computation verifies
only support, tier, affine-feasibility, and disjoint-set identities; it supplies
no stochastic estimate.

These cases exhaust \(\ell_\Gamma\le2\).  Lemma 3.1 supplies nonexplosion in
all cases, and Lemma 2.1 transports positive recurrence from the reduced
chain back to the original physical states in \(\Gamma\).  This proves
Theorem 1.1. \(\square\)

## 5. Publication boundary

The global composition itself contains no finite classification and no new
stopped-kernel estimate.  It invokes the one- and two-linkage theorems only
after exact conjugacy on a fixed closed class, so their Lyapunov functions are
never compared across theorem families.  The theorem makes no claim for more
than three dynamic species, more than two active projected linkage classes, or
complexes of molecularity greater than two.
