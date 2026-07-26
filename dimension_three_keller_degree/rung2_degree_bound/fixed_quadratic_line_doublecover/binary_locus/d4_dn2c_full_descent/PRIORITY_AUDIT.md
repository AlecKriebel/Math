# Priority audit — D4-DN-2C exclusion

## 2026-07-26T06:25:00Z public-source sweep

Searches were run for quartic three-dimensional Keller classifications,
degree-four exclusions, and the exact internal label `D4-DN-2C`.

Sources checked:

- arXiv/web searches for July 2026 Jacobian/Keller preprints, including
  [Graded Keller maps and the Jacobian Conjecture](https://arxiv.org/abs/2607.20210),
  [Generic degrees of real polynomial Keller maps with non-dense image](https://arxiv.org/abs/2607.21572),
  and [Small Counterexamples to the Gaussian Moments Conjecture](https://arxiv.org/abs/2607.18186);
- Terence Tao's
  [A digestion of the Jacobian conjecture counterexample](https://terrytao.wordpress.com/2026/07/21/a-digestion-of-the-jacobian-conjecture-counterexample/);
- the Secret Blogging Seminar post
  [The new counterexample to the Jacobian conjecture](https://sbseminar.wordpress.com/2026/07/20/the-new-counterexample-to-the-jacobian-conjecture/);
- current MathOverflow searches, including the discussions of
  [the \(S_3\) model](https://mathoverflow.net/questions/513387/),
  [geometric degrees](https://mathoverflow.net/questions/513440/),
  and [the plane degree record](https://mathoverflow.net/questions/513413/);
- indexed X/Twitter results for the July 2026 announcement and for quartic
  dimension-three Keller maps; and
- an exact-string search for `D4-DN-2C`.

No checked source states this normalized-family exclusion or uses this
taxonomy label.  The sources concern the announced counterexample,
gradings, generic-degree constructions, monodromy, or consequences for
other conjectures.

This source-specific evidence is **not a guarantee of worldwide priority**.
Search indexing is incomplete, X/Twitter search coverage is especially
weak, and unpublished or differently normalized calculations may exist.
Accordingly:

- the note claims only a verified exclusion of one frozen family;
- it does not claim a quartic-wide theorem or degree-table update; and
- priority and mathematical correctness remain subject to independent
  reconstruction, literature review, and peer review.

## Verification disclosure

The derivation and scripts are AI-assisted.  They are not peer reviewed.
Exact checks certify the algebra encoded in the scripts, not the completeness
of any larger quartic taxonomy.

## 2026-07-26T06:34:50Z independent-verification delta

The independent direct PARI/GP package in sibling directory
`d4_dn2c_pari_lower` completed and passed with terminal marker
`D4_DN2C_DIRECT_PARI_LOWER_STRICT_PASS`.  It reconstructs the weighted
determinant directly in PARI/GP, replays the two transverse interiors,
punctured intersection, and origin, and includes an adjugate check of the
origin plane normalization.  Its two required-failure mutations also pass.

The aggregate wrapper in this directory now invokes that package.  This
provides a methodologically separate exact check of the lower descent.  It
does not certify the completeness of the larger quartic taxonomy, establish
worldwide priority, or replace peer review.

## 2026-07-26T07:29:16Z full-family hostile-audit delta

The direct PARI package was extended to reconstruct the raw \(E_7\) kernel,
complete \(E_6\) contact atlas, all four boundary charts, and every lower
descent rather than importing the primary contact atlas.  A second
audit-local PARI reconstruction selected a different constant minor.  The
hostile aggregate passed
`D4_DN2C_FULL_EXCLUSION_HOSTILE_AUDIT_STRICT_PASS`.

No checked source collision was found.  This remains source-specific
negative evidence, not a guarantee of worldwide priority or peer review,
and the theorem remains confined to the single normalized family.
