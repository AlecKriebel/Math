# Literal intake read failures

These were read-only location mistakes before discovering the actual research sitemap. They did not mutate inputs and were not builder executions.

Command: head -n 12 public/sitemap.xml (working directory /Users/alec/Desktop/alec-dev/aleckriebel.com). Exit 1. Literal output:

```text
head: public/sitemap.xml: No such file or directory
```

Command: stat -f '%N %z %Lp' .git/index public/research/index.html public/sitemap.xml public/research/research.css (same working directory). Exit 1. Literal output:

```text
stat: public/sitemap.xml: stat: No such file or directory
.git/index 9057886 644
public/research/index.html 98925 644
public/research/research.css 1170 644
```

Subsequent read-only discovery located public/research/sitemap.xml. No failure was overwritten or recast as a successful read.

After the first builder stopped, an expected-absence probe used ls on the two candidate article directories. Exit 1 confirmed neither had been created. Literal output:

```text
ls: verification/radial-tree-stage-sol-20261117/candidate/public/research/designed-tree-congestion-fragmentation: No such file or directory
ls: verification/radial-tree-stage-sol-20261117/candidate/public/research/radial-orthogonality-dual-conformal-flatness: No such file or directory
```

The separate first-build traceback is preserved verbatim in BUILD.stderr.txt and pinned by FAILURE_1.json; it is not an intake location failure.
