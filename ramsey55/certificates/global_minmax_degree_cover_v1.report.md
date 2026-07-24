# Exact complement/minimum-degree cover for order 43

Date: 2026-07-24 (America/Los_Angeles)

## Outcome and scope

**CERTIFIED DECOMPOSITION IDENTITY; NO SOLVE CLAIM.** Every hypothetical
order-43 Ramsey(5,5) graph is equivalent, under complementation and
relabeling, to a model in one of three branches:

| branch | degree of vertex 0 | degree interval for every vertex | assumptions on the audited base CNF |
|---:|---:|---:|---:|
| 18 | 18 | 18 through 24 | 42 primary star units |
| 19 | 19 | 19 through 23 | 42 primary star units + 86 auxiliary threshold units |
| 20 | 20 | 20 through 22 | 42 primary star units + 86 auxiliary threshold units |

The apparent fourth branch, degree 21 with all degrees equal to 21, is
impossible by handshake parity. This reduces the previous four-way
degree-at-vertex-0 split to three stronger branches. It does not establish
SAT or UNSAT for any branch and does not change a Ramsey bound.

## Exact cover proof

Let \(\delta(G)\) and \(\Delta(G)\) denote the minimum and maximum degrees of
an order-43 graph \(G\), and define

\[
  \mu(G)=\min\{\delta(G),\,42-\Delta(G)\}
        =\min\{\delta(G),\,\delta(\overline G)\}.
\]

The certified \(R(4,5)=25\) degree theorem gives every hypothetical
Ramsey(5,5;43) graph degrees in \([18,24]\). Hence
\(\mu(G)\in\{18,19,20,21\}\).

Choose \(G\) or its complement so that its minimum degree is \(\mu(G)\).
Every degree in the chosen orientation then lies in
\([\mu(G),42-\mu(G)]\). Relabel one minimum-degree vertex as vertex 0,
then relabel its neighbours as vertices \(1,\ldots,\mu(G)\).

If \(\mu(G)=21\), the interval is \([21,21]\), so all 43 vertices have
degree 21. Their degree sum would be \(43\cdot21=903\), which is odd,
contradicting the handshake lemma. The remaining values of \(\mu\) are
exactly the three rows of the table above.

The independent checker enumerated all 28 possible
\((\delta,\Delta)\) pairs with \(18\leq\delta\leq\Delta\leq24\). Exactly
one pair maps to the parity case, namely \((21,21)\); every other pair maps
to branch 18, 19, or 20.

## Reusing the existing counters

The audited base CNF has 903 primary variables, 65,403 total variables, and
2,052,132 clauses. For every vertex it contains:

1. a forward threshold counter enforcing at most 24 incident edges; and
2. a forward threshold counter enforcing at most 24 incident nonedges.

Both counters allocate final threshold variables through threshold 25.
Setting threshold \(t\) false enforces a count strictly below \(t\), while
the canonical threshold assignment witnesses completeness when the count is
below \(t\).

- Branch 19 sets threshold 24 false in both counters for each of 43
  vertices. This enforces at most 23 edges and at most 23 nonedges, hence
  degree interval \([19,23]\).
- Branch 20 similarly sets threshold 23 false, giving degree interval
  \([20,22]\).
- Branch 18 needs no extra auxiliary units because \([18,24]\) is already
  the base interval.

Thus no new counters and no new auxiliary variables are needed. The exact
unit streams have the following SHA-256 values:

| branch | star units | extra degree units | combined units |
|---:|---|---|---|
| 18 | `ec98f184f8a65ec0f4620cb6bf9eab5df987ea597bfce97f2cfebfaa5148ab18` | empty stream `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `ec98f184f8a65ec0f4620cb6bf9eab5df987ea597bfce97f2cfebfaa5148ab18` |
| 19 | `634c3e9a122ca8f467e66777ae1764b079ad22846e5e19cc2cfb88bb3a7bbbb6` | `d5c58ae1a77caf04e3a3ef3388278782376061068892af81b2a5fc37ea646f88` | `11146af82f42f17c281855920b1c6b7fb26a2c741047c1d11d533e0a1ba432cf` |
| 20 | `e7ccad57a97be16d41deb6ba3e17f5e7d8dac9e6230ac76e753889b1ef84a781` | `3e73fdb644199274e86fd04198e7467def4c5025378039189ab1207e7636e375` | `eb68ad70651d15f392e335ebe2702b3713a298c5596596f61c29e2d6dabb1500` |

Each hash is over lines of the form `literal 0\n`, in deterministic unit
order.

## Exact secondary split for branch 18

In branch 18, vertex 0 has 24 nonneighbours. The graph induced by those
nonneighbours has neither a 5-clique nor a 4-vertex independent set: such an
independent 4-set together with vertex 0 would be an independent 5-set.
Consequently, its complement belongs to
\(\mathcal R(4,5,24)\).

The complete catalog has 352,366 isomorphism classes and audited source
SHA-256
`83ca4028f206b2fa4315ef219b8c2c57c7835209673dd8183d8fb4353bd4fdd0`.
Relabeling within the 24 nonneighbours therefore gives an exact
352,366-cube secondary cover of branch 18. Each cube fixes:

- 42 primary star variables;
- all \(\binom{24}{2}=276\) primary variables inside the antineighbourhood;
- leaving \(903-42-276=585\) primary variables.

This catalog split is exact only with the complete pinned catalog; a partial
catalog must not be substituted.

## Low-storage certificate plan

A global negative certificate can now be organized around one shared base
CNF and the three assumption streams, rather than four separately
materialized 90 MB branch CNFs.

1. Solve branches 18, 19, and 20 under their exact unit streams.
2. For branch 18, use the complete 352,366-cube antineighbourhood cover.
3. If further cubes are introduced for branches 19 or 20, retain a checked
   covering certificate in addition to each leaf's UNSAT proof.
4. Verify each proof against the shared base formula plus its units, and
   retain enough checked cover metadata to derive global UNSAT.

No such production solve has been run. Existing immutable storage gates
remain unchanged.

## Multiplicity/flag-LP assessment

For any graph, if \(M_5\) is the total number of clique and independent
5-sets, then the exact rooted incidence identity is

\[
  5M_5=\sum_v\left(
    K_4(G[N(v)])+I_4(G[\overline{N}(v)])
  \right).
\]

This is a useful finite flag identity, but by itself it merely restates the
local obstruction. Under the hypothesis \(M_5=0\), every summand can vanish
because the allowed degree range is precisely where the relevant
Ramsey(4,5) side graphs exist.

The one-vertex edge-extremal relaxation is also too weak. Using the published
minimum and maximum edge counts for \(\mathcal R(4,5,d)\), the allowed
interval for a vertex's contribution to the exact excess identity contains
zero for every degree 18 through 24:

| degree | possible excess-contribution interval |
|---:|---:|
| 18 or 24 | \([-4,47]\) |
| 19 or 23 | \([-8.5,47.5]\) |
| 20 or 22 | \([-13,45]\) |
| 21 | \([-14.5,45.5]\) |

Therefore a degree-only or single-root edge-count LP cannot force
\(M_5\geq1\). A viable multiplicity certificate would need genuinely joint
flags: at minimum, two-root overlap information or a finite induced-type LP
with exact rational dual verification and finite-\(n\) integrality. The
observed \(E=2\), four-vertex-overlap corpus is motivation for such flags,
not evidence that the global multiplicity is two.

## Verification and pinned artifacts

- Base CNF SHA-256:
  `141de0a9714fb40e100508031b37fa555bf2fbdefd13c2dee4c04141c159bcb1`.
- Frozen cover plan SHA-256:
  `f21df79e827b75b1800861d3ca42c088af0ed8cce5a55829036b58e8a9ce8e5b`.
- Independent check result SHA-256:
  `842a811ca05faa83033b3e8dfdd20189676e782434bdf40e8c377ecde7d44194`.
- Production source SHA-256:
  `621957e3d8c8a345813481a4c1882e98e839591d9ced4cec271185973a77bd73`.
- Independent checker SHA-256:
  `c049a4d43f571a40fc1241a5da89cf80f9f038706d42d3e0af3629359a3b876d`.
- Test source SHA-256:
  `587ad88f470b52a5a09e0964f350c79d11058c77c0116029c03d23ba699ff2d5`;
  six tests pass.

The check result is `valid: true`: it independently reconstructs the
65,403-variable counter layout, all branch unit hashes, all 28 degree-pair
cover cases, the unique parity case, and the semantics of every possible
degree value under each threshold assumption.
