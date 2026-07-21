# Priority audit and corrected comparison

Audit date: **21 July 2026**. This is a source-specific record, not an
exhaustive literature review or a claim of worldwide priority.

## Bottom line

- **The six-variable symmetric map was already public.** Eliott Cassidy's
  repository commit
  [`40e1e20f9ee113245f8e4e4b22ecd798fa1ffbfc`](https://github.com/eliottcassidy2000/math/commit/40e1e20f9ee113245f8e4e4b22ecd798fa1ffbfc),
  authored at **20 July 2026, 14:46:10 UTC**, executes the
  de Bondt--van den Essen/Meng transport in \(\mathbb C^6\), checks that the
  Jacobian is symmetric, and transports the same three-point fiber. Our
  determinant-one, identity-linear formula and expanded potential are a useful
  normalization, not an independent discovery.
- **William Thompson beat Exploration 02's dimension headline and has priority
  for rank compression.** His initial commit
  [`45a7616fdf5a20c065564f2676190093722696b9`](https://github.com/wtho704/explicit-cubic-homogeneous-jacobian-counterexample/commit/45a7616fdf5a20c065564f2676190093722696b9),
  posted at **21 July 2026, 03:29:42 UTC**, explicitly factors the cubic part
  through a six-dimensional component space and obtains a 24-variable cubic
  homogeneous Keller map.
- **The 22- and 44-variable certificates were not found in the audited prior
  artifacts.** That residual claim remains provisional and unreviewed.

## Exact comparison of the cubic maps

| Artifact | Ambient variables | Cubic monomials | Active nonlinear coordinates | Field / collision |
|---|---:|---:|---:|---|
| Thompson initial commit | 24 | 54 | 23 | \(\mathbb Q\) / rational |
| Exploration 03 | 22 | 72 | 21 | \(\mathbb Q\) / rational |

The Exploration 03 cubic is smaller in ambient dimension and active
coordinates; Thompson's is substantially sparser. There is no single canonical
notion of “smaller,” so the note now states the metric each time.

## What the other audited artifacts contain

- **Cassidy:** an explicit six-dimensional symmetric-Jacobian Keller map and
  the transported collision. The audited file explicitly says it is not a
  homogeneous Hessian-nilpotent quartic witness for Zhao's Vanishing
  Conjecture.
- **Thompson:** a 24-variable cubic-homogeneous map, exact rational collision,
  54 monomials, a rank-six lift, and independent SymPy and JavaScript BigInt
  checks. The audited initial commit contains no symmetric quartic or Zhao
  witness.
- **Alex Harrison:** the audited commit
  [`74808fb2e1c1691b0007576ba0508e5e7cdcb1e3`](https://github.com/DrAlexHarrison/jacobian-anatomy/commit/74808fb2e1c1691b0007576ba0508e5e7cdcb1e3)
  executes a 79-variable cubic-homogeneous Bass--Connell--Wright reduction and
  a 426-variable Dru\.{z}kowski form. It discusses the symmetric-quartic
  consequence but does not export an expanded quartic witness or collision.

## Corrections made after the audit

1. The paper title and abstract now lead with the 44-variable witness rather
   than the six-variable map.
2. The note withdraws any novelty claim for the six-dimensional construction
   and cites Cassidy's earlier public artifact.
3. The Thompson comparison says “fewer variables” instead of unqualified
   “smaller,” records his sparsity advantage, and notes that both cubic maps are
   over \(\mathbb Q\) with rational collisions.
4. Exploration 02 is marked superseded in its dimension claims.
5. A separate Node.js BigInt checker was added so the exported collisions are
   no longer checked only by Python implementations.

These corrections do not constitute independent mathematical validation. Alec
Kriebel is a complete amateur and cannot verify the claims without expert
review.
