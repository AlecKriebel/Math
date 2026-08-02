# Final hostile audit of Paper I

**Audit time:** 2026-08-01 18:51 PDT

**Sources:** `paper/main.tex`, `paper/n4_certificate.tex`

```text
b0e066fa5c9db3b255b86ef8bd8f7330d071e2f0876b5e155e9f3b339e14a1f0  paper/main.tex
c27538ccc00ae6816020e39599a3a81ea7f81df58f1b0df543c1c14ff9e9d69b  paper/n4_certificate.tex
```

No manuscript source was edited during this audit. No literature search or
external contact was performed.

## Verdict

**Mathematics: PASS.** I found no false formula, sign error, denominator gap,
missing equality case, invalid lumping, or fitness/size quantifier error. The
symmetric `K_4` certificate agrees exactly with the phase-two derivation and
hostile audit. The asymptotic proposition agrees with the repaired phase-three
report, including all graph-class and repeated-gadget caveats.

**TeX and layout: PASS.** A clean two-pass Tectonic build produced 13 pages
with no errors, warnings, undefined references, overfull boxes, or underfull
boxes. Visual inspection of every rendered page found no clipping, overlap,
broken glyph, illegible formula, or misplaced label. The independent rebuild
and checked-in PDF rasterize identically on all 13 pages.

**Publication precondition, not a theorem defect.** Lines 654--660 say the
materials "are archived with release" `universal-db-obstruction-v1.0.0`. At
audit time, `gh release view ... --repo AlecKriebel/Math` returned
`release not found`, and no local tag existed. Create the named release before
distribution, or change the sentence to future tense.

## Claim checks

### Symmetric `K_4` families — PASS

- The constructions and new diagrams are correct. `G_13(x)` has three unit
  core--satellite edges and three satellite edges of weight `x>0`.
  `G_22(x,y)` has internal pair weights `x,y>0` and four unit cross edges.
- The four two-class transition formulas have the correct target
  multiplicities and deleted-self counts. Their dependence only on `(i,j)`
  proves strong lumpability. The transient orbit counts are six and seven.
- The displayed `F_13`, `P_13`, and rational comparison match the derivation
  term for term. Positivity gives strict suppression exactly off `x=1`.
- The `2+2` comparison has the correct sign and factors. Exact replay confirms
  that `P_22` has 123 positive integer terms and
  `det(M_22)=P_22/(128L_22)` with the eight displayed positive factors.
- The substitution
  `g=sqrt(xy)>0`, `d=(sqrt(x)-sqrt(y))^2>=0`, `t=r-1>0` is exact.
  The displayed `C_k` certificate proves `H_22>0` except at
  `d=0,g=1`, equivalently `x=y=1`.
- The theorem correctly covers only the full `S_1 x S_3` and
  `S_2 x S_2` invariant families. It explicitly leaves unrestricted
  six-edge weighted `K_4` open.

### Asymptotic support condition — PASS

- The common-target/common-threshold coupling correctly proves dB fitness
  monotonicity. Combined with the exact strong-selection limit, it gives
  `rho_dB(G,r) <= 1-(1/n)sum_i 1/(s_i+1)` for every finite connected
  undirected weighted graph.
- Proposition 8 explicitly assumes such graphs and `|V(G_n)|=n -> infinity`.
  Its hypothesis has the intended order: for each fixed `r>1`, eventual in
  `n`, with an `r`-dependent threshold.
- For fixed `R>1`, the proof obtains `limsup a_n <= 1/R`; allowing arbitrarily
  large fixed `R` proves `a_n -> 0` without interchanging limits.
- The estimate `fraction{s_i<=K} <= (K+1)a_n` proves support-degree divergence
  in probability.
- The repeated-gadget sentence now requires a positive fraction retaining
  bounded **total** support degree after connection and acknowledges weak
  support-completion edges. The dense blow-up summary retains the required
  fixed-class, positive-proportion, fixed irreducible-kernel, unequal-degree
  hypotheses. All uncovered regimes are correctly left open.

### Fitness and family quantifiers — PASS

- A graph-dependent suppressing tail rules out
  `exists N0 forall N>=N0 forall r>1`; no uniform threshold is asserted.
- The reversed `forall r>1 exists N0(r) forall N>=N0(r)` order remains open.
- The triangle and symmetric `K_4` sign theorems are restricted to positive
  weights and `r>1`; neutral equality at `r=1` is outside their scope.
- No symmetric-family conclusion is extended to unrestricted weighted `K_4`.

## Replay and production record

This command completed with exit status zero:

```text
make test verify directed triangle n4 phase3-check
```

It passed the exact Markov tests, general obstruction verifier, directed
checks, triangle derivation and independent replay, both `K_4` certificates
and full-state cross-check, and two-class/windmill lumpability checks under
both rules.

The checked-in and installed PDFs agree:

```text
d77a0018e19b6cdb19892482cf295f321ff2b94ba881456843ac10556110a74e  paper/main.pdf
d77a0018e19b6cdb19892482cf295f321ff2b94ba881456843ac10556110a74e  output/pdf/no_universal_death_birth_amplifier.pdf
```

`n4_certificate.tex` is intentionally an included fragment; it was built and
visually audited through `paper/main.tex`.

## Final disposition

The mathematical manuscript and PDF production are ready. The named GitHub
release is the sole remaining publication precondition.
