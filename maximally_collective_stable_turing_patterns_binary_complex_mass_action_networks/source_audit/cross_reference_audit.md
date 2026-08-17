# Cross-reference audit

The literal LaTeX audit checks every `label`, comma-separated `ref`/`cref`,
and citation key across the main manuscript, supplement, and specialist
summaries. It rejects missing or duplicate labels and missing bibliography
keys. Because all theorem-like environments share one counter, theorem,
proposition, lemma, corollary, remark, and definition references must use an
explicit semantic noun; `cleveref` is reserved for equations. A rendered-PDF
gate separately rejects the two historical type errors.

Final automated result:

```text
MANUSCRIPT_AUDIT_PASS
labels: 78
references: 9
bibliography keys: 21
citations: 29
```

The PDF build and semantic text audit report no undefined references,
citations, or stale environment types.
