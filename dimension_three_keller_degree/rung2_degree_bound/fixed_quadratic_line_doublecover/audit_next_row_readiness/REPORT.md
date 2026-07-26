# Independent readiness audit for `Q2-E2-A1-B2-D1-N2`

**Recorded (UTC):** 2026-07-26T00:25:06Z
**Audited worktree HEAD:** `7215b4db`
**Scope:** denominator and readiness only; no new exclusion is claimed.

This audit was prepared with substantial AI assistance. It is not peer
reviewed. Exact scripts check the finite data encoded here; they do not
constitute peer review or prove the cited algebraic lemmas.

## Verdict

There is a canonical, finite **nine-stratum inclusive denominator** for the
fixed-quadratic line-double-cover row. I derived it from the top determinant
identities and the Hilbert--Burch degree constraints before using the
existing binary-locus status labels. It agrees exactly with `L00`--`L08` in
the candidate incidence manifest:

\[
\boxed{9\text{ stable internal strata}.}
\]

On the evidence actually present in the worktree, their readiness count is

\[
\boxed{3\text{ covered},\quad3\text{ provisional},\quad3\text{ open}.}
\]

The row is therefore **not ready for promotion**. In particular, the
existing exact-\(\delta=2\) work does not imply that the binary row is nearly
closed: the entire \(\delta=3\) and \(\delta=4\) inclusive strata have no
lower analysis, and the power-fibre and several lower exclusions still lack
an independent hostile replay.

## 1. Independent derivation of the stable denominator

Normalize the degree-two outer cover to
\[
H_4=h(p,q,r)(p^2,q^2,0).
\]
Writing \(R=(H_3)_3\), the degree-eight identity is
\[
E_8=8h^2pq\,R_r.
\]
Because the polynomial ring is a domain, every point in the row has
\(R\in\mathbb C[p,q]_3\).

The first disjoint split is whether \(h\) is binary.

1. If \(h\notin\mathbb C[p,q]\), retain all \(R\), including \(R=0\), in
   `L01`.
2. If \(h\in\mathbb C[p,q]\) and \(R=0\), route to `L00`.
3. Assume from now on that \(h\) is binary and \(R\ne0\). Put
   \[
   P=hp^2,\quad Q=hq^2,\quad
   \alpha=J(Q,R),\quad\beta=-J(P,R),\quad
   \gamma=J(P,Q),
   \]
   and \(g=\gcd(\alpha,\beta,\gamma)\), \(\delta=\deg g\).

If \(\alpha,\beta\) are constant-linearly dependent, the coprime degrees
\(4,3\) force a common power fibre
\[
\lambda P+\mu Q=L^4,\qquad R=L^3.
\]
In this row it normalizes uniquely, up to the cover stabilizer, to
\(h=p^2,R=p^3\). This is `L08`.

Otherwise the reduced syzygy ideal has height two. If \(k_1,k_2\) measure
the deficits between the two minimal Hilbert--Burch degrees and the two
gradient-column degrees, then
\[
0\le k_i\le2,\qquad k_1+k_2=\delta.
\]
The unordered pairs are therefore exactly
\[
\begin{array}{c|c}
\delta&\{k_1,k_2\}\\ \hline
0&\{0,0\}\\
1&\{1,0\}\\
2&\{2,0\},\{1,1\}\\
3&\{2,1\}\\
4&\{2,2\}.
\end{array}
\]
There is no independent \(\delta=5\) case: after removing a degree-five
gcd, \(\alpha/g\) and \(\beta/g\) would be constants and hence dependent.
These six possibilities are `L02`--`L07`.

Together with `L00`, `L01`, and `L08`, this proves completeness of the
nine-stratum candidate. The strata are disjoint by the ordered tests

\[
h\text{ binary?},\quad R=0?,\quad
\alpha,\beta\text{ dependent?},\quad
(\delta,\{k_1,k_2\}).
\]

## 2. Stable IDs and evidence-based status

Here “covered” means that a complete proof and a completed hostile
reconstruction are present. “Provisional” means that a full exclusion is
claimed but at least one required independent audit is missing. Any
partially covered inclusive stratum is reported as open.

| ID | Intrinsic condition | Audit status | Evidence and gap |
|---|---|---|---|
| `L00` | binary \(h\), \(R=0\) | **covered** | The abstract hostile report independently checks the separate ranks and the quadratic-component/plane exit. |
| `L01` | nonbinary \(h\) | **covered** | Full nonbinary theorem, dual exact checks, and standalone hostile reconstruction with verdict PASS. |
| `L02` | independent, \(\delta=0,\{0,0\}\) | **covered** | The abstract hostile report checks all block injections and the plane-plus-shear inverse. |
| `L03` | independent, \(\delta=1,\{1,0\}\) | **provisional** | A complete two-family lower proof and SymPy/PARI scripts exist, but the hostile audit directory contains only an opening log, not a completed report. |
| `L04` | independent, \(\delta=2,\{2,0\}\) | **provisional** | Exact stratification and three lower exclusions have dual-CAS artifacts; every note says hostile replay is pending. |
| `L05` | independent, \(\delta=2,\{1,1\}\) | **open** | Fourteen of fifteen incidence families have provisional lower packages; the doubled-nonbranch baseline-plus-contact family remains open. |
| `L06` | independent, \(\delta=3,\{2,1\}\) | **open** | No exhaustive incidence atlas and no lower exclusion package. Existing notes merely route mutations here. |
| `L07` | independent, \(\delta=4,\{2,2\}\) | **open** | No exhaustive incidence atlas and no lower exclusion package. |
| `L08` | dependent power fibre | **provisional** | A complete primary proof is written, but its strict wrapper runs four SymPy programs only; the hostile checklist has no completed audit. |

Thus the exact coarse count is
\[
(3,3,3)=(\text{covered},\text{ provisional},\text{ open}).
\]

## 3. Fixed-divisor chart atlas and its boundaries

The stabilizer of the squaring cover is the diagonal torus extended by
\(p\leftrightarrow q\). Binary quadratic \(h\)'s have exactly four orbit
charts:

| chart | representative | parameters/boundaries |
|---|---|---|
| branch square | \(p^2\) | isolated |
| two branch roots | \(pq\) | isolated |
| one branch root | \(p(p+q)\) | isolated |
| no branch root | \(p^2+\eta pq+q^2\) | modulus \(\kappa=\eta^2\) |

The parameterized chart must retain:

- \(\kappa=4\), the doubled nonbranch root;
- \(\kappa=0\), a stabilizer jump, not a new orbit family;
- \(\kappa=16/3\), where a fixed-root/contact incidence changes the
  \(\delta=2\) Hilbert--Burch shape;
- \(\kappa=16\), where the two-contact incidence changes shape.

No specialization is discarded. Under specialization, \(R=0\) routes to
`L00`; dependence of \(\alpha,\beta\) routes to `L08`; a gcd-degree jump
routes from `L02`--`L06` to the unique higher-\(\delta\) stratum; and at
fixed \(\delta=2\), a rank drop of the \(r^1\) block routes between `L05`
and `L04`.

## 4. Independent exact-\(\delta=2\) chart count

The local valuation formulas give a useful check on the existing
exact-\(\delta=2\) registry. The shape-\(\{1,1\}\) mechanism count is

\[
\begin{array}{c|c}
h\text{ orbit}&\text{mechanism families}\\ \hline
p^2&2\\
pq&2\\
p(p+q)&5\\
\text{squarefree no-branch}&4\\
\text{doubled nonbranch}&2
\end{array}
\qquad\Longrightarrow\qquad
\boxed{15}.
\]

Concretely these are: simple fixed or baseline-plus-contact for \(p^2\);
one doubled or two simple contributions for \(pq\); three fixed-root
multiplicity patterns plus two fixed/contact patterns for \(p(p+q)\);
doubled fixed, two fixed, fixed/contact, or two contacts in the squarefree
interior; and simple fixed or baseline-plus-contact on the doubled
nonbranch divisor.

Three proper subloci have shape \(\{2,0\}\):

1. squarefree fixed/contact at \(\kappa=16/3\);
2. squarefree two-contact at \(\kappa=16\);
3. the exceptional coefficient hypersurface in the doubled-nonbranch
   contact family.

After separating those subloci, the exact-\(\delta=2\) terminal chart
atlas contains
\[
\boxed{15+3=18\text{ parameterized chart families}.}
\]

The artifact comparison agrees with this count:

- `L04`: \(3/3\) families provisionally excluded;
- `L05`: \(14/15\) families provisionally excluded and \(1/15\) open.

This is progress inside two stable strata, not progress against a new
global denominator.

## 5. Readiness failures

The following gaps prevent promotion of the parent row:

1. The final `L05` doubled-nonbranch contact complement
   \[
   R=ap^3+bp^2q+\tfrac32d\,pq^2+dq^3,\qquad
   (3a-2b)(2a-2b+d)(6a-5b+3d)\ne0
   \]
   has no lower exclusion.
2. None of the fourteen claimed `L05` closures has a completed hostile
   mathematical replay; checklists are not audits.
3. `L06` and `L07` have neither an exhaustive incidence-chart atlas nor
   lower analysis. Numerous boundary factors in the \(\delta=2\) notes are
   merely sent to “future \(\delta\ge3\) analysis”.
4. The `L03` hostile audit stopped after finding a scope-wording mismatch.
5. `L08` has no methodologically independent reconstruction.
6. There is no retained map from these internal normal forms to all 45
   frozen coefficient-pivot strata of the parent row.
7. At the audited HEAD, most binary-locus notes and verifiers are untracked;
   only fifteen paths in `binary_locus/` are repository-tracked. Untracked
   work is evidence on disk but is not a published repository release.

## 6. Highest-information next calculation

Before another isolated lower leaf, compute the universal
\(\delta\ge3\) incidence locus:

> For general binary
> \(h=Ap^2+Bpq+Cq^2\) and
> \(R=ap^3+bp^2q+cpq^2+dq^3\), form
> \((\alpha,\beta,\gamma)\), impose constant independence, and compute a
> saturation-safe primary decomposition of the conditions
> \(\deg\gcd(\alpha,\beta,\gamma)\ge3\), then subtract the
> \(\delta=4\) and power-fibre loci.

The output should be normal forms and boundary arrows for `L06` and `L07`,
with the four fixed-divisor charts retained. It has higher information
gain than closing the last `L05` family: it freezes the two wholly
unexplored stable strata, tests whether they are occupied, and supplies a
targeted construction space if either resists lower exclusion.

## 7. Mechanical consistency check

Run

```text
python3 verify_denominator.py
```

The expected unique marker is

```text
NEXT_ROW_DENOMINATOR_PASS_9_STRATA_18_DELTA2_CHARTS
```

The script enumerates the six allowed Hilbert--Burch pairs, checks the
nine stable IDs and \(3/3/3\) status count, and checks the
\(15+3=18\) exact-\(\delta=2\) chart-family ledger. It deliberately makes
no claim to verify the mathematical exclusions.
