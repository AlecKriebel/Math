# PRA formatting decision

APS permits initial peer review from a PDF and does not require REVTeX source
at that stage. The canonical article contains numerous theorem environments,
technical appendices, exact tables, TikZ figures, and a separate line-numbered
build. A mechanical REVTeX conversion would create material regression risk
without improving the initial scientific review.

The submission package therefore uses the warning-free canonical author PDF
and includes a complete preservation-friendly source archive. No canonical
source was overwritten. If APS requests REVTeX after review or acceptance, it
should be converted in a separate directory and checked theorem-by-theorem
against this frozen source.

This is a formatting decision only; no mathematical content is omitted.
