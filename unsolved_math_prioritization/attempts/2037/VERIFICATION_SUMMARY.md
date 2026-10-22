# EP302 verification record and limits

## Historical independent exact checks

The recorded 10 October 2026 audit accepted the upper certificate using
separately authored exact arithmetic and the written mathematical transfer.
No author-supplied program, external solver, floating-point optimization,
Lean development or Lean cache was executed to obtain that acceptance.

- Q = 139708800: 719 nontrivial divisors and 12,675 distinct reciprocal triples,
  with agreement between two independently written enumeration paths.
- Q0 = 3360: all 47 prefixes solved exactly, with actual covers and exhaustive
  optimality search; 21 cover thresholds. Scaling by 96 divisors supplied
  2,016 additional valid configurations, for 14,691 configurations in total.
- All 271 rational packing certificates passed; the ledger has 274 cover
  levels. The exact weighted sum is 3251333/4989600, multiplier density is
  23520/110143, and forced omission density is 22759331/163562355.
- The resulting limsup upper bound is 140803024/163562355.
- Normal Python, -O and -OO recorded identical certificate-result identities
  and identical control-result identities. Sixteen deliberate corruptions
  were rejected. The exact-cover solver was cross-checked against brute-force
  enumeration on 320 deterministic small hypergraphs, with two additional
  singleton/pair controls. Cambie's construction was also checked at 400
  finite cutoffs, with two distinctness controls.
- The specialized two-tail Q = 720 comparison gives 2125/2418. Wang's
  all-tail EP301 upper bound 667/806 is not transferred to EP302.
- Five strict parameter margins in the upstream human manuscript were
  recomputed with rational logarithm bounds. These finite parameter checks
  do not supply the missing upstream analytic closure.

The exact upper-transfer and padding arguments appear in
MATHEMATICAL_AUDIT.md. The upper argument takes N to infinity for fixed finite
valuation range before increasing that range, and does not assume convergence
of f(N)/N. The padding proof handles the closed-half endpoint using distinctness.

## Historical source inspection

Khanukov's complete 10-page corrected manuscript and TeX, including proofs,
caveats and bibliography, were inspected. PDF pages 3, 7 and 8 were additionally
rendered and visually checked; the historical source review recorded page 2.
The release asset digests matched the acquired PDF and certificate bytes.

All 26 EP301 and 92 EP327 Lean modules were acquired as data. Git blob identities
matched for 131 upstream files in total. A comment/string-aware lexical guard
reported no sorry, sorryAx, admit, axiom, opaque, unsafe or native_decide token
in the checked module sources. This was not a Lean parser, compiled proof check,
transitive axiom computation, or full mathematical review of all 34,454 lines.
The required literal definitions, structured-witness wrapper, interval and
cardinality semantics were inspected. The human EP301 manuscript was read in
full; de la Bretèche–Tenenbaum's actual Theorem 3.1 conditions were inspected.
The complete primary Tenenbaum theorem and full alternative formal analytic
closure remain outstanding.

The historical exact-release Verify run succeeded at the pinned release commit.
Its upper and lower jobs are author-side public CI evidence, not this audit's
own replay. The lower reported axiom allowlist remains an attributed report.

## Edition checks and distribution boundary

Edition preparation verified retained input hashes and sizes, historical
result consistency, editorial preservation, public-file identities and native
Git tree identities. No mathematical test program was rerun, no Lean or
third-party code was executed, no dependency was installed, and no new scholarly
source was retrieved or newly audited. All mathematical checks described above
remain explicitly historical results. The authored proof spans and both lower
holds are preserved without a mathematical correction.

This edition distributes prose, citations and public source/verification
metadata only. Raw certificates, detailed result ledgers, executable checkers,
Lean/library code, copied PDFs or TeX, and source-derived images are omitted.
The upstream certificate is publicly linked for identity verification; this
edition is not a self-contained executable reproduction package. H-L1 and H-L2
remain uncleared. No full resolution, novelty or external human review is claimed.
