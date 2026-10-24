# Scope addendum after the proved quotient reduction

UTC checkpoint: 2026-10-24T23:28:00Z. Supporting verification complete;
full-problem discovery estimate remains **5%**. No originality claim.

The historical `SOURCE_CONTRACT.md` is preserved byte-for-byte. One sentence
there needs correction: read literally as saying that excluding all countably
infinite word images would be insufficient for this problem, it is too broad.
Cardinals below the continuum cannot simply be assumed countable, but the
subsequently proved quotient reduction below supplies the missing mathematical
step. It justifies restricting counterexample searches to countably infinite
word images. There is no separate uncountable-cardinal case after that
countable case has been proved in the required generality.

Specifically, choose countably many distinct word values in a hypothetical
infinite small image and countably many open normal subgroups separating
them. Quotient by their intersection. The resulting profinite group embeds
as a closed subgroup of a countable product of finite groups, so it is
metrizable. Its word image is the image of the original word image under
the quotient map, remains infinite, and is still smaller than continuum.
An uncountable compact metric space contains a Cantor set and has cardinality
continuum. The quotient word image is therefore countably infinite.

Consequently excluding countably infinite word images **in all metrizable
profinite groups** would settle the full source question, without CH. This
does not permit a restriction to topologically finitely generated groups,
does not prove the required exclusion, and does not establish finiteness of
the closed verbal subgroup.

Proof: `../topological/METRIZABLE_REDUCTION_AND_OBSTRUCTION.md`, frozen SHA256
`a7dafdf2d8cd189c64c7924c29104cf6b80e391199a075e4d1367951dcbd8661`.
Fresh independent primary and secondary reviews:
`../topological_review/AUDIT.md` and
`../topological_review/secondary/AUDIT.md`; their receipts preserve the
exact audited inputs. Root independently read the proof and both audits.
This addendum records the changed logical scope rather than silently
rewriting a frozen source-preparation artifact.
