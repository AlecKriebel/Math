# Exact-byte audit of the residual 336 pair theorem

**Independent hostile audit, 2026-08-12 PDT.** The audited target is

~~~text
research_notes/proof_first_exact_residual_336_pair_recurrence_theorem.md
SHA-256 6e9ddcaccd03fe64b1c6a57cbaef052e984eaf7b7e2e87c4df52ca1240787a6c
179 lines / 6,705 bytes
~~~

The exact-byte verdict is **STRICT PASS**. The finite dependency identifies
336 distinct fixed support pairs, and the two global analytic dependencies
cover their normalized forms without an incidence-to-pair or chart-switching
gap.

## 1. Frozen set identity

The certificate and focused tests rehash as

~~~text
src/all_active_residual_levelset_336_certificate.py
4149b682d1222bd3327548b0eb95921f7aae20663816b345b48285239c12f93d
tests/test_all_active_residual_levelset_336_certificate.py
6f5802976d4de479a0728648248a2291f5d518e04de29b9b7053802eb7f1b9c2
~~~

The six focused tests pass. The selected object is initially an incidence,
namely an ordered disjoint support pair and an all-active descriptor. The
certificate proves both

\[
 \#\{\text{selected incidences}\}=336,
 \qquad
 \#\{\text{projected ordered pairs}\}=336.           \tag{1.1}
\]

Thus every selected pair occurs in exactly one selected row. There is no
unproved multiplicity division. The certificate also proves equality with
the independently defined geometric level-set incidence set. Its two row
fingerprints are

~~~text
d0c31db81db2400e0ead6e4a1a86b237fbf3b8bbb597340856a2756e9f6c884d
2bd4025f29d20ea4af467d46704c598652c9332ac4e32df18669cb7eb75c75a0
~~~

For every row, `levelset_geometry` finds exactly one top side: the other
side contains zero, and disjoint supports prevent both sides from doing so.
It verifies that the top support has internal rank two and lies on one
positive weight level, while the other support is zero plus two or three
unaries on half that level.

The exact weight histogram is

\[
 312\,[1,1,1]+8\,[1,1,2]+8\,[1,2,1]+8\,[2,1,1].     \tag{1.2}
\]

The top support is entirely quadratic in exactly the 312 homogeneous rows
and contains a unary in exactly the 24 anisotropic rows.

## 2. Homogeneous normal form

For weight \((1,1,1)\), every unary has level one. Hence the scale in the
geometric identity is one, the lower side is

\[
 R=\{0\}\cup U,
\]

with two or three distinct unaries, and every top vertex on level two is one
of

\[
 2A,2B,2C,A+B,A+C,B+C.
\]

The certificate separately enforces internal top rank two. This is literally
the scope of

~~~text
research_notes/proof_first_336_h111_workload_occupation_theorem.md
e3c484cdbda44949ba070dae6c911a2c7de465064857b61b5d9883e9dd03bdff
~~~

The frozen first audit has SHA
`740d929dfa460818df2cd134fc6beba70d015c7409f3c74ce0979316b8d4af89`.
An independent second audit is frozen at
`68b265e75cd5d8c7a2a4f4602e92bea381c6636473e6740504cb5f34cf1a0192`.
The theorem is global on each class: it includes boundary activation,
physical service, the exact death-minus-birth ledger, nonexplosion, and the
workload-only Foster conclusion. It does not return a chart-local exit.

## 3. Anisotropic normal form

After a species permutation, an anisotropic row has weight \((1,1,2)\).
The lower support must contain two or three unaries on one common positive
level. The only possible common level is one, and its only unary vertices
are (A,B\). Therefore

\[
 R=\{0,A,B\}.                                        \tag{3.1}
\]

The only unary on top level two is (C\), and the certificate says the top
support contains a unary. Consequently

\[
 T=\{C\}\cup Q,
 \qquad Q\subseteq\{2A,A+B,2B\}.                    \tag{3.2}
\]

If \(|Q|\le1\), the support has at most two vertices and internal rank at
most one. Certified rank two therefore forces \(|Q|\ge2\). This is exactly
the scope of

~~~text
research_notes/proof_first_336_h112_quotient_foster_theorem.md
9206aa2b07aa802e4d06a769b3b60d520b2dbd12752312497aa5b41156780d48
research_notes/proof_first_336_h112_quotient_foster_exact_byte_audit.md
992448ad8b6520f014e783adb26a4f9b393b0e6a5f38c3a6262dd9b2fa0c1764
~~~

That theorem supplies a global all-face episode tiling with one proper
marked quotient potential, physical-time drift, actual endpoints, and
nonexplosion. Forgetting its finite target mark preserves the physical
communicating class and proves physical positive recurrence. Coordinate
permutation preserves all these properties and does not restrict the
arbitrary positive labelled rates.

## 4. Verdict and boundary

The 312 and 24 alternatives in (1.2) are disjoint and exhaustive. Both
dependencies prove recurrence for arbitrary strongly connected labelled
graphs on the fixed supports and every fixed positive rate vector. Hence the
literal 336-pair theorem is **STRICT PASS**.

This verdict composes only the exact residual 336 family. It does not certify
the final union with other support branches, and no orientation, rate,
population, or stochastic history is enumerated in reaching it.
