# Order of mixing — reviewed partial result

**4300001 / AMR-042-0001. Disposition: unsolved, 5/5.**

Start with the [corrected proof](audit-independent-20261004/corrected-public/PROOF.md)
and the [full independent audit](audit-independent-20261004/AUDIT.md).
The accepted partial conclusions are:

- The defining polynomial is absolutely irreducible in every prime characteristic.
- The group F_p*⟨x,y⟩ is radical-saturated in its function field.
- The mixing order satisfies **5 ≤ M_p ≤ 6** for every prime.
- **M_2=6**.

For odd primes, existence or exclusion of a six-term Laurent multiple remains
unresolved. The characteristic-two answer is not a full answer to Ward's
prime-unspecified question. No historical novelty, external human peer review,
or formal verification is claimed.

## Accepted version and preserved history

The corrected packet alone passed the independent mathematical/source audit and
subsequent publication review. It corrects two literal wording errors: independence
of the generators x,y does not mean independence of arbitrary distinct monomials;
and saturation at odd primes includes finite-field constants. The arguments and
numerical partial conclusions are unchanged.

- Corrected packet manifest: `1f5d64200baaa0b571854bafde52157a559a4ff46c84cc2756cfca39e7d94a7a`
- Corrected proof: `68847700cb0c2c4efe7d51da310cdde158b06b2cc0daaf8997501130e49577a9`
- Full audit manifest: `1b5148c498f38460420458f415243a3f788e0eebfa03b8b01c441682eca991c1`

The original author freeze is retained under [public/](public/) as historical
provenance. It received **REVISE**, not PASS. Its proof hash is
`a184e8f7d7682cb645e1fd32a05100ff71e8deb57ea5454da42b74a74e85f0b4`.
The [exact correction patch](audit-independent-20261004/precision-corrections.patch)
and [correction binding](audit-independent-20261004/correction-binding.json) preserve
what changed. Historical pending-review metadata inside the frozen packets is
superseded by the hash-bound audit and this acceptance summary.

## Reproduce

From this directory:

```
sha256sum -c PUBLICATION_SHA256SUMS
(cd public && sha256sum -c SHA256SUMS)
(cd audit-independent-20261004 && sha256sum -c SHA256SUMS)
(cd audit-independent-20261004/corrected-public && sha256sum -c SHA256SUMS)
python3 audit-independent-20261004/corrected-public/check.py --output /tmp/mixing-author-replay.json
cmp /tmp/mixing-author-replay.json audit-independent-20261004/corrected-public/control-results.json
python3 audit-independent-20261004/independent_checks.py
(cd audit-independent-20261004 && sha256sum -c SHA256SUMS)
```

The author checker uses only the Python standard library and passes 62,094
assertions. The independent checker uses SymPy (tested with Python 3.12.14 and
SymPy 1.14.0) and passes 78,628 assertions. The latter regenerates its stored JSON;
byte-identical output requires the recorded environment. Its comparison data comes
from the unchanged original public packet, whose arithmetic is identical to the
corrected packet. Both replays were byte-identical in the final publication layout.

All 59,561 projective multipliers in the four declared small boxes have minimum
support seven. Finite searches and controls supplement the unbounded written
proofs; they do not resolve the odd-prime gap.

The repository change includes only this packet and this problem's queue Status
and Turns cells. Other queue bytes, including pre-existing header text and links,
are preserved. No source PDFs, complete corpora, private inventories, merge, release,
DOI, or preprint publication are included.
