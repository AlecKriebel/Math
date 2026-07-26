# C-035 manuscript package

This directory contains the submission-oriented manuscript for the exact
`CERTIFIED-FINITE` claim:

> No finite simple graph \(G\) on 12 vertices satisfies
> \(\gamma(G)=\gamma^\infty(G)=3<\theta(G)\).

It does **not** claim that there is no counterexample of order 12, that there
is no counterexample through order 12, or that the universal
\(\gamma\)--\(\theta\) conjecture is resolved.

## Build

From this directory:

```text
SOURCE_DATE_EPOCH=1785047581 \
  tectonic --keep-logs --keep-intermediates main.tex
```

The fixed epoch is the claim-acceptance timestamp.  Two clean builds with
Tectonic produce byte-identical `main.pdf`.

The checked research artifacts are not duplicated into the paper directory;
Appendix A binds their exact paths and SHA-256 hashes in the campaign archive.

## Submission placeholders

Before external submission, replace the author line and add the permanent
archive identifier in the data-availability section.  No external
communication or publication has been performed.
