# Cross-reference audit

The literal LaTeX audit checks every `label`, comma-separated `ref`/`cref`, and citation key across the main manuscript and supplement. It rejects missing or duplicate labels and missing bibliography keys. The final source contains no explicit type phrases such as “Theorem 3.1” that could silently disagree with the environment type; internal references use `cleveref` or neutral equation references.

Final automated result:

```text
MANUSCRIPT_AUDIT_PASS
labels: 62
```

The PDF build reports no undefined references or citations.
