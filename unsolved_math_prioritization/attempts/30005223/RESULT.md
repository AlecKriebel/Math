# 30005223: five-turn partial outcome

**Original problem unresolved. Proposed status: unsolved, 5/5 substantive author turns. Independent review is pending.** No limit, existence of a limit, or asymptotic for the full zero density is proved here.

## Exact target and known current result

The source is Miller's Question8, OWR39/2022, printed p.2289: lambda and mu are independent uniform partitions of n, and the quantity is P_n=Pr(chi_lambda(mu)=0). A uniform permutation, Plancherel row measure or an unconditioned independent-geometric cycle model is different.

Peluse–Soundararajan's March2026 Theorem1 gives density2/log n+O((log log n)^2/log² n) for each of three sufficient zero criteria. Their paper expressly leaves the total density open and attributes the conjectural full asymptotic2/log n to Miller–Scheinerman. This packet credits that theorem rather than presenting it as a campaign discovery. Known fixed-modulus divisibility likewise does not settle equality to zero.

## Retained scoped deductions

1. **Turn1, exact residual family and its small mass.** For lambda=(n-1,1) and mu=(nu,1) with no unit parts in nu, the character vanishes. TypeIII detects it exactly when gcd(nu)>1. The undetected cases have an exact Mobius count and, across the two conjugate rows, density asymptotic2pi/(sqrt(6n)p(n)). Some have sequential rim-hook extinction in one removal order and two cancelling chains in another. A separate S4 example has genuine canonical-order cancellation. These families do not control bulk uniformly chosen rows.
2. **Turn2, bulk size/modulus criterion.** Uniform class tails imply a good-column bound log z_mu=O(sqrt(n)log² n), valid simultaneously for every row. Combining integrality and orthogonality gives Pr(nonzero)<=modular failure+bad-column mass+Z/(p(n)D²). The actual known prime-power range gives a simultaneous modulus far below the scale needed by this criterion. A scalar countercontrol identifies precisely which restricted inputs are insufficient; it is not a counterexample to a character theorem.
3. **Turn3, exact anti-concentration fibers.** Holding cycles of size>=3 fixed gives a conditionally uniform1/2-cycle fiber whose length diverges in probability. The character sequence has an exact Krawtchouk expansion with integral weight-space trace coefficients. This yields a valid conditional polynomial root bound, but no bulk estimate for identically zero fibers or effective degree. Positivity and long fibers alone are invalid substitutes.
4. **Turn4, actual irreducible zero fiber and annihilator.** The S11 row(5,2,2,2) with fixed cycles(3,3) has a complete three-point zero fiber outside typeIII. Its nonzero residual character is exactly2p3h2 and is annihilated by specializing all p_j, j>=3, to zero. A general Jacobi–Trudi derivative formula computes this annihilator. Orthogonality gives an exact projection/fourth-moment criterion for the frequency of zero fibers; the needed asymptotic moment estimate is absent.
5. **Turn5, analytic transfer boundary.** Fixed-size Boltzmann conditioning has the explicit n^(3/4) single-partition loss, and unconditioned diagonal zero probabilities are vacuous. Even a diagonal weighted average tending to zero need not imply a pointwise limit; a rigorously analyzed powers-of-two spike sequence is a countercontrol. A one-sided local regularity condition would suffice. Exact branching support inequalities are proved, but their sqrt(n) corner factors and signed cancellations do not provide that condition.

Classical character identities, the partition asymptotic, Jacobi–Trudi, branching and the cited contemporary estimates are credited. No historical novelty is certified for any elementary deduction or reduction.

## Exact remaining gap

One must control the zeros outside the three known criteria on the full uniform partition-pair measure. The packet does not establish bulk anti-concentration, the annihilator frequency/fourth moment, an averaged residual-zero theorem, or the required pointwise transfer. The finite data cannot bridge any of these gaps. Thus neither P_n->0 nor P_n~2/log n nor a different full limiting behavior is claimed.

## Verification and provenance

The five turn receipts contain38,109;8,206;199,590;2,556 plus388; and17,105 exact assertions respectively. These are finite arithmetic/algebra checks, not proofs of an asymptotic. The scripts are locally authored, use only the standard library and the shared local character_tools module, and do not execute code from a source paper.

Historical turn snapshots and their metadata remain unchanged and hash-valid. They record the state when written; FINAL_STATUS.json and FINAL_TURN_LEDGER.jsonl supply the current five-turn outcome. Source work, source reading, checking, review and packaging do not count as extra author turns. Full primary PDFs/texts and imported dataset records are local reading copies excluded from publication. A separate full source/proof audit is required before an unresolved draft PR.
