# Journal manuscript source

Target: Bulletin of the Australian Mathematical Society.

The manuscript is `kourovka_16_45.tex`. The original official `baustms.cls`
is included unchanged under its own LPPL notice. Its SHA-256 is
`b5e53c7510ed44cd2673e30f7c60b2c09d4fdb77d057e9d61979ed537202fad3`.
Source: https://archive.austms.org.au/Publ/Bulletin/baustms.cls

Compile from this directory using an existing TeX installation:

```
pdflatex -interaction=nonstopmode -halt-on-error kourovka_16_45.tex
pdflatex -interaction=nonstopmode -halt-on-error kourovka_16_45.tex
```

Or use Tectonic:

```
tectonic kourovka_16_45.tex
```

No bibliography processor or external figures are needed. The supplied PDF
was built with Tectonic using the journal class and contains seven pages.
The source uses the official MSC year option and suppresses the template's
unassigned DOI and submission-status heading. No margins or body-font sizes
have been changed. The theorem and proof are entirely in this source.

When a standalone preview environment cannot access the accompanying class,
the same source falls back to AMS article format. That preview has the same
mathematical content but different typography; the submission PDF must be
compiled with the supplied journal class present.

The manuscript retains the author's existing rights. No new manuscript
reuse license is granted here. The journal's publication agreement is an
author action following acceptance, not something accepted by this package.
