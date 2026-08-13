# Exact-byte hostile audit of the residual 336 all-active theorem

**Independent proof-first audit, 2026-08-12 PDT.**  This audit freezes the
following exact artifacts:

```text
research_notes/proof_first_all_active_residual_levelset_336_theorem.md
SHA-256 3b9ad4eaeeafd0b42b788fb1fe288075e4b3c0b77d77f9fe306c5ad2a824cd2e
285 lines, 10065 bytes

src/all_active_residual_levelset_336_certificate.py
SHA-256 5b15d5ec67a58ad181ec93ee9397ea55d72ab4f18f7f6f386aba6b59124aa8e8
398 lines, 13330 bytes

tests/test_all_active_residual_levelset_336_certificate.py
SHA-256 18ce0f035adb9d697830a0fc609b100355ab81a51ccdca4dee2e5122221e4f7c
101 lines, 3697 bytes
```

The verdict is **STRICT PASS** at these exact bytes.  The analytic conclusion
is local to all-active terminal charts in the exact level-set family; the
certificate proves a support/descriptor set identity and no stochastic fact.

## 1. Correct finite prebranch

The ordered disjoint-support universe has size

\[
 3^{10}-2(2^{10}+10\,2^9)+(1+10+10+90)=46{,}872.
\]

The inherited mixed-atlas seed union has 5,169 ordered pairs.  Closing it
under all species permutations and linkage reversal gives 27,894 pairs, so
18,978 pairs remain.  The correct all-active invariant prebranch removes
only the 146 pairs with a **strictly positive three-coordinate** invariant,
leaving 18,832.  Full deficiency zero removes none.

This distinction is load bearing.  A weaker predicate positive only in two
named coordinates would remove another 68 pairs but is not proper in an
all-active chart.  The corrected certificate retains all 68 and separately
checks that none contributes a selected affine-feasible failed incidence.

## 2. Exact residual identity

There are 169 all-active tier descriptors.  On the product of those
descriptors with the 18,832 support pairs, the certificate selects exactly
the rows which both fail the corrected universal S-tier-superlevel condition
and are feasible in an affine stoichiometric class.  It obtains 336 rows on
336 distinct pairs.

Independently, the certificate recognizes only the following geometry for a
descriptor weight (h>0): one support (T) has internal rank two and lies
on one (h)-level (2s), while the other is

\[
 R=\{0\}\cup U,
\]

where (U) consists of two or three distinct unary complexes, all on level
(s>0).  The selected incidence tuple equals this geometric incidence tuple
exactly, including order.

The independently replayed histograms are:

* weights: (312,8,8,8) at
  ((1,1,1),(1,1,2),(1,2,1),(2,1,1));
* top sizes (3,4,5,6): (154,126,48,8);
* top deficiencies (0,1,2,3): (154,126,48,8);
* lower supports \(\{0,A,B\},\{0,A,C\},\{0,B,C\},\{0,A,B,C\}\):
  (86,86,86,78);
* full deficiencies (1,2,3,4,5): (120,130,66,18,2);
* linkage order: (168,168);
* quadratic-only tops versus tops containing a unary: (312,24).

The two frozen encodings replay as

```text
d0c31db81db2400e0ead6e4a1a86b237fbf3b8bbb597340856a2756e9f6c884d
2bd4025f29d20ea4af467d46704c598652c9332ac4e32df18669cb7eb75c75a0
```

They encode the same sorted 336 rows and differ only in JSON key ordering.

## 3. Orientation-free analytic proof

For $H(x)=h\cdot x$, every reaction internal to $T$ is exactly neutral:

\[
 {\cal L}_T H=0.
\]

For a unary $u\in U$, all nonzero targets have the same $h$-level $s$,
while a target zero lowers $H$ by $s$.  Therefore

\[
 b_u=-s\sum_{u\to0}\kappa_{u0}\le0.
\]

The zero-source contribution is a finite constant $b_0$.  Strong
connectivity of the reaction graph on $R$ forces at least one direct edge
$u_*\to0$: take the final edge of a directed path from a unary vertex to
zero.  Hence

\[
 {\cal L}H(x)=b_0+\sum_{u\in U}b_u x_{i(u)}
             \le b_0-c_*x_{i(u_*)},\qquad c_*>0.
\]

This identity is valid for every strongly connected orientation and every
fixed positive labelled rate vector.  In an all-active chart the selected
coordinate diverges, so the physical-time generator tends to minus
infinity.  The potentially quadratic clocks in $T$ require no averaging:
they contribute exactly zero.

Because every coordinate of $h$ is positive, $H$ is proper.  The use of
the strictly-positive invariant prebranch and the properness of the final
Foster function are therefore consistent.

## 4. Executable and render replay

Running the frozen test file against the frozen certificate produced

```text
Ran 5 tests in 34.868s
OK
```

The exact theorem bytes were independently rendered with Pandoc's
single-backslash TeX-math reader, to MathJax HTML and through Tectonic to PDF.
Tectonic produced zero stderr bytes.  The default independent PDF has
five letter-sized pages; its display tables and wrapped fingerprint block
render cleanly.  A page-count difference from a repository-specific template
does not change the source bytes or verdict.

## 5. Frozen verdict

**STRICT PASS** for the theorem/certificate/test triple pinned above.  The
finite replay proves precisely that every residual incidence has the
level-set geometry, and the generator identity proves that entire geometry
without enumerating orientations, rates, histories, or population boxes.
