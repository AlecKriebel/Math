# Claim-neutral verification and release engineering

## Scope

This verification layer records four proof-interface regressions. It does not
certify T3-2, construct a theorem manuscript, or inspect the inherited release.

1. **Shell-dependent negative drift.** The birth-death chain with
   \(p_n=n/(2n+1)\) upward and \(q_n=(n+1)/(2n+1)\) downward has strict drift
   \(-1/(2n+1)\) at every positive level. Its reversible weights are
   \((2n+1)/(n(n+1))=1/n+1/(n+1)\), so their sum diverges; its edge resistances
   also have divergent sum. The chain is recurrent but not positive recurrent.
   Pointwise positive service margins therefore cannot replace a uniform or
   correctly integrated variable-drift estimate.

2. **Lexicographic descent with infinite lower-component cost.** From \(s_k\),
   jump to \(s_{k+1}\) at rate \(k\) or to \(t_k\) at rate one; from \(t_k\),
   drain to \(t_{k-1}\) at rate one. The first switch has mean physical time one
   and decreases the primary lexicographic component. Its switch level satisfies
   \(P(M\ge m)=n/m\), however, so the subsequent lower-component drain has
   infinite mean. Finite joint boxes and bounded jump increments do not repair a
   lexicographic Foster argument that omits seam/reset cost.

3. **Tight infinite environment.** The reversible immigration-death CRN
   \(0\rightleftarrows E\) has a Poisson stationary law. It is tight and
   positive recurrent, while every population value has positive stationary
   mass. Tightness must not be replaced by one exact finite phase.

4. **Fast neutral CRN trace.** In the reversible two-linkage CRN
   \(A\rightleftarrows B\), \(0\rightleftarrows C\), start with \(A+B=n,C=0\)
   and stop at the first \(0\to C\) reaction. The mean number of neutral
   \(A\rightleftarrows B\) reactions is exactly \(n\), while the mean physical
   stopping time is exactly one. Ordinary reaction count is not a proxy for
   physical trace duration.

The first two examples are generic countable-state Markov processes, not T3-2
counterexamples. The latter two are positive-recurrent CRN stress tests. Their
purpose is to prevent reuse of invalid proof interfaces.

## Read-only replay

Run:

```bash
python3 -I -B verify_read_only.py
```

The verifier uses only the Python standard library, explicitly loads only the
current regression source and tests, disables bytecode writes, and hashes its
four-file verification scope before and after execution. It neither reads nor
writes `inherited/`, uses no network, loads no external test plugins, and emits
its report to standard output rather than updating a certificate in place.

The command checks code behavior, not release authenticity. A frozen release
should additionally provide one immutable source archive, a manifest generated
after all files are final, the outer archive SHA-256, a repository commit/tag,
the supported Python version, and a license. Verification should compare
temporary outputs with released artifacts; it should never overwrite the
artifacts being checked or use fixed shared `/tmp` names. Any later compiler or
TeX steps should have pinned versions, required-input checks, progress output,
timeouts, and cleanup traps.
