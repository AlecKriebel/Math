# Complete-account reconciliation of a broader recurrence lead

Recorded 2026-10-21T04:15:49.931390+00:00. Completion:100% of this bounded duplicate comparison; overall sweep estimate19%. No unrelated record was changed.

A complete authenticated account inventory returned193 records over8 pages. The only unpublished item has no uploaded files and concerns an unrelated deterministic model. Its identifier and metadata remain in ignored private receipts; no target partial deposit was found. A local scan of every metadata object for target identifiers, chunks/Norros, recurrence/Foster and fluid-limit terms finds only the broader published record22089551, *Positive Recurrence for Single-Linkage Bimolecular Weakly Reversible Stochastic Reaction Networks*. Its stated abstract theorem concerns bimolecular mass-action networks with one linkage class and weak reversibility. This reading is of the authenticated publication metadata/abstract, not a complete new proof review or an exclusion of every ancillary statement in its body.

The target generator has rational rates with D=x+y+1. Multiplying its generator by D yields the following canonical mass-action reactions, with positive rate constants for every lambda>0:

- empty→A and empty→B, lambda/2 each;
- X→A+X, Y→A+Y, X→B+X, Y→B+Y, lambda/2 each;
- A→X, A+X→2X, B→Y, B+Y→2Y, unit constants;
- X→empty, X+Y→Y, Y→empty, X+Y→X, unit constants.

This is one undirected linkage class, but it is **not weakly reversible**: A+X→2X and B+Y→2Y lead to sink complexes. The problem is not resolved by treating population-state irreducibility as complex-graph weak reversibility; they are different properties. The coefficient of ax in the first-A jump intensity is necessarily1 in the unique falling-factorial monomial expansion, so the A+X→2X reaction is unavoidable in a four-species bimolecular mass-action realization of that multiplied generator. No jump intensity has a nonzero x(x-1) coefficient, so 2X cannot be an active source complex in such a realization. Nonnegative rate constants cannot cancel this missing coefficient. The analogous observation holds for2Y. Adding return reactions changes the specified generator (already visible when x=2,a=b=y=0).

A state clock change also needs a separate recurrence argument. If the D-multiplied chain had stationary probability pi, a stationary probability for the physical original clock would be proportional to D*pi, which requires finite pi-mean of D. Positive recurrence alone of the faster chain does not supply that integrability. This is an additional unproved obligation for such a route; the submitted direct physical-clock Foster proof avoids it.

Thus the broader record's **stated main theorem does not directly cover this generator**. No claim is made that every possible hidden-state embedding, alternative theorem or ancillary statement has been excluded. This is not an audit of the other paper's correctness or novelty. It is a result-identity and theorem-hypothesis comparison; the paper under review does not rely on that result or assert a new general recurrence criterion. The new full-package reviewer was given this lead only after its own initial analytic reconstruction, to challenge this comparison independently.
