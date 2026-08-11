# Independent audit of the exact 416-pair common-potential theorem

## Scope

This audit concerns only Theorem 9.1 of
`two_active_easy_943_common_w_theorem.md` and the exact selector in
`src/two_active_easy_common_w.py`.  It does not concern the disjoint hard
333-pair interface and does not certify global T3-2.

## Verdict

**PASS.**  The final replay found no counterexample for any strongly
connected orientation or positive rate vector in the exact 416-pair scope.
The replay checked:

1. all 937 bounded actual-target access words and every competing physical
   clock;
2. exponential positive-overshoot moments on the reversible and directed
   rank-one shells, including killed endpoints;
3. the explicit six-support dominant-reset cut;
4. the structural extension to all 1,455 one-active incidences;
5. the fourth-power lift of all 117 closed-rank-one episodes;
6. the directed-triple carré/Taylor estimate on all 117 all-active rows;
7. the disjoint common-correction menu; and
8. the all-species marked fixed-class gluing and nonexplosion argument.

The finite replay gives 416 pairs, split 414 positive-invariant and two
signed, with pair fingerprint

```text
8c3325983568c53772f024080c0b95d37873cfe0a149386ec9829d1d9323e186
```

and the certified remainder

```text
319 positive-invariant + 34 signed = 353 pairs
9868f965cc8af951fd7545f8832ed0275a8d60bab70b2593b7424654cba7d8ec
```

The certificate payload is

```text
40547e6856855ce5b128cf944a4e81aa44e1db77a35e29ea1d099e8b26ca3097
```

All scoped analytic and pair-recurrence flags are true.  The global T3-2
flag remains false.
