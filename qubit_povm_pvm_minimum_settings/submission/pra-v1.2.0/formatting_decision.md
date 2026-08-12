# PRA formatting decision

The PRA submission PDF is a one-column, 11-point build using the official
REVTeX 4.2f runtime with the `aps,pra,onecolumn,notitlepage` presentation
options. It is generated from the same canonical mathematical
source as the archival and line-numbered PDFs; only class, title metadata,
abstract ordering, and bibliography presentation are conditional.

A two-column `reprint` prototype produced widespread overfull equations and
stuck floats in the Lorentz matrices, second-variation formulas, and
load-bearing appendices. The one-column APS presentation is therefore the
safer initial-review format. It preserves every equation, appendix, theorem
number, citation, and figure while using conventional `\author`, `\email`,
and `\affiliation` metadata. This is a formatting decision only; no
mathematical content is omitted.
