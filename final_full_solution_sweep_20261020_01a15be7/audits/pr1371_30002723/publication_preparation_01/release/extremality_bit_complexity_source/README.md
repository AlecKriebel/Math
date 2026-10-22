# Polynomial bit complexity of one-row Gomory-Johnson extremality

Alec Kriebel, ORCID 0009-0001-9320-500X. Version1.0.0,22October2026.
Catalog30002723; original unpublished proof source PR1371, exact head
186e1e62c002e27b7c67bd6b2381945f496d4cf9.

This is one prepared scientific result family. Publication readiness is false
pending two NEW independent whole-package reviews and adoption of the exact
reviewed package. Earlier scientific audits and this preparation QA are not
those new reviews. No deposit, DOI reservation, upload, merge or ledger action
is performed by this archive.

## Theorem and proof

paper.pdf is the complete ten-page note, and main.tex is its editable source.
For every rational f in(0,1) and a periodic one-row minimal valid function
specified by a sparse all-rational breakpoint/point-value/left-right-limit
list, extremality is decidable in polynomial total binary input length.
Both-sided discontinuities at zero are allowed. Competitors are unrestricted
standard nonnegative valid functions. Strong polynomiality, irrational data,
higher dimensions, an implemented compressed fast solver and a polynomial-size
dense perturbation output are not claimed.

Sections2-7 contain the general proof. The full BHK4q tight system is first
converted to real additivity by affine interpolation on every refined relative
face, edge and singleton, before the bounded interval lemma is used. Separate
slope/jump/spike families retain all13endpoint sectors and limiting incidences.
AHT orbit counts on a signed double cover give the dimension. If it exceeds
the residual row count, rank-nullity decides nonextremality. Otherwise prefix
flips select only polynomially many free components, and grouped nonnegative
weighted AHT output recovers signed coefficients for an exact rational rank
calculation with polynomial bit height. Imported theorems and their actual
version/read scope are documented, rather than replaced by a new oracle.

## Exact finite reproduction

With Python3.10+ and its standard library, run:

    python3 -B reproduce.py

This verifies the complete public inventory, frozen source/PDF provenance,
metadata/file selection and exact normal/-O/-OO diagnostic outputs. The
standalone verification/exact_controls.py is reused with attribution from the
preceding independent project audit; its source is unchanged. It compares277
local row spaces,384finite signed systems and4complete grid models, and
rejects3incorrect local variants. These checks do not implement AHT, prove the
universal theorem, establish a complexity bound experimentally, or certify
priority. They are reproducible finite guards on the written mechanisms.

The offline builder exports the frozen PDF, deterministic source ZIP and
five-member upload kit into a different directory:

    python3 -B build_package.py --output ../rebuilt

It makes no network/service call and does not recompile TeX. A separate fresh
TeX compilation and page-render equality check were completed during
preparation. Standard LaTeX packages are listed in main.tex. For a local PDF
rebuild use an already installed LaTeX toolchain, e.g. pdflatex main.tex twice,
or an existing Tectonic with its available cache. No compiler, runtime or
third-party source bodies are bundled. Byte-identical PDFs across different
TeX engines or creation timestamps are not claimed.

## Provenance, priority and licenses

SOURCE_PROVENANCE.json records exact original project proof pins and primary
source hashes/versions. SOURCE_ACCESS.md records actual statements read and
access limits. The final four authored research proofs are preserved verbatim
under provenance/original_research; they are historical inputs, not new reviews
of this publication copy. Main.tex supplies the final complete proof and the
finite-to-real bridge required by root's scientific adoption.

BHK's complete-grid theorem and AHT's orbit/weighted algorithms are established
results, not new methods invented here. PartVII's actual finite-presentation
and one-sided decomposition statements were compared. Its cited PartVIII2021
manuscript body was not recovered. Bounded searches authenticated no existing
full-target publication, but historical priority remains uncertain. There is
no exclusive-firstness or present-openness claim, and no prior solution DOI.

AI tools were used extensively in planning, mathematical exploration, proof
development/reconstruction, computation, source/priority search, writing,
editing, reproduction and adversarial audits. Alec Kriebel is the named human
author. This is unrefereed, without claimed conventional independent human
peer review, journal acceptance or formal proof-assistant certification.
Authored prose is CC BY4.0 and authored code MIT licensed. Private source,
spreadsheet and provider captures and third-party source bodies are excluded.
