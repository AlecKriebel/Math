# Reproducing the bridge controls

The proof is PROOF.md. The exact computation is a falsification control
for its algebraic orientation, with a genuine one-sided inverse in a
different ring. It is not evidence that any group algebra has such an
inverse defect. The script has no third-party dependencies.

From the repository root:

```text
python3 openai_wreath_planar_consequences/bridges/wreath/check_orientation.py
```

Its output must agree with orientation_receipt.json. The ring is
M_2(F_2<a,b>/(ab-1)); the acting group is GL_2(F_2), acting by left
multiplication. Matrix right multiplication by b commutes with this
action, while left multiplication by b fails 2052 of the bounded
homomorphism controls. This tests a noncommutative action with a genuine
defect, rather than relying only on finite directly finite group rings
where all kernel witnesses would vanish.

The support model is finite dictionaries, here encoded by finite sets
because the coefficient field is F_2. Each operation produces a finite
set. The written support-product argument in PROOF.md, not bounded
sampling, proves finite support for arbitrary group-ring lamps.

External source PDFs and PR packet copies are kept under the effort's
ignored sources/ directory. They are excluded from the authored upload
materials. Retrieval URLs, immutable PR head, exact byte lengths, hashes,
and observed source-state changes are retained in the two public source
receipts. The original Miller--Schupp paper was not retrieved; the audit
does not claim it was.
