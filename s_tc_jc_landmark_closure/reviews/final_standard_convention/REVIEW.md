# Independent adversarial convention referee

## Verdict

**VERIFIED AFTER CORRECTION**, with a strict fail-closed qualification:

- The locked `sd_0` convention is literally compatible with Englander et
  al. v4 and is the binary LSA-valid specialization of Holtgrefe et al. v2.
- It is **not** literally the broader reduction sentence in Brits et al. v2.
- Outcome P may be released only after the theorem defines its class by
  `sd_0` and the no-omnian criterion, and stops calling that map the single
  universal standard shared by all cited papers.
- If Outcome P is intended to quantify over every rooted preimage of the
  Brits exhaustive-cleanup map, the present result is **FALSE / a strict
  subclass theorem**.  An exact LSA-valid level-2 counterexample to that
  convention identification is in `SOURCE_COMPARISON.md`.

This review validates the convention layer only.  It does not promote the
local algebraic hard cover or the final theorem.

## Exact release edits required

Before any positive theorem is recorded as standard-class fact:

1. Rename the lock heading to "reticulation-preserving semi-deorientation
   `sd_0`" and say explicitly that this is the Englander v4 convention.
2. State that `sd_0` root suppression must already yield a simple binary mixed
   graph and must preserve every reticulation and incoming arrowhead.
3. Define `red_*` separately.  It may perform exhaustive degree-two,
   parallel, and stated 2-blob cleanup only for restrictions/displayed
   networks; its preimages are not admissible rootings.
4. Define `S_TC` as a nonempty-rooting property of the final simple mixed
   graph and state the equivalent no-omnian condition.
5. Keep the LSA condition in every rooted and admissible-rooting definition.
6. Replace every claim that the literal Brits 2-sub-blob definition means
   "two external edges".  Introduce "operational two-terminal factor" for
   the latter.  Cite the `K4-e` proof only for that operational object.
7. State that parallel theta cores are not topology objects in the simple
   class.  They are handled by rejection or a separately named cleanup, not
   by the five-core atlas.
8. Phrase the theorem scope as:

   > simple binary LSA-rootable semi-directed mixed graphs obtained under
   > `sd_0`, level at most two, with no omnians.

9. In the prior-work comparison, say that this is the Englander/Holtgrefe
   standard-strong class; do not attribute the exact reduction map to Brits
   v2.

## Primitive and sharpness mapping

The independent verifier checks all twelve minimal supports from the five
primitive families and all 100 of their admissible rootings.  Every rooting
is tree-child and every broad reduction terminates immediately at the same
mixed graph, so the finite atlas primitives are convention-safe.

The frozen weak pair is also convention-safe at its displayed rootings and
remains in `W_TC \ S_TC`.  Its role as sharpness evidence is unchanged.

## 2-sub-blob conclusion

No ordinary two-edge, two-terminal suppressible level-2 factor survives in
`S_TC`; the only simple rank-two whole-blob core is `K4-e`, and the exact
census finds no tree-child rooting.  This supports a modulo-`T` headline for
the locked class without adding a two-terminal move.

It does **not** prove that every object satisfying the literal three-clause
Brits 2-sub-blob definition is degree-two suppressible.  The four-sunlet
fixture disproves that reading.

## Reproduction

```bash
bash reviews/final_standard_convention/verify_all.sh
```

The verifier imports no project modules.  It independently implements the
rooting and reduction operations and records source hashes, exact counts, and
mutation outcomes in `convention_certificate.json`.
