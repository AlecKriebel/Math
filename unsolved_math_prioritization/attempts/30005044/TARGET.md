# Exact original target

Numeric ID **30005044**, code **OWR-9790363-003**, queue rank 281.

The official source is Natalia Cardona–Tobón and Marcel Ortgiese's contribution, “The inhomogeneous contact process on Galton-Watson trees,” OWR 12/2022, printed pp. 618–620. The question is on p. 619; the report DOI is https://doi.org/10.4171/owr/2022/12. The volume has also been catalogued with a 2023 publication date; 2022 is its report identifier and workshop year.

The source model has:

- a rooted supercritical Galton–Watson tree;
- only the root initially infected;
- finite iid vertex fitnesses taking values in $[1,\infty)$;
- infection rate $\lambda F_uF_v$ across adjacent vertices;
- recovery rate 1;
- a finite offspring mean in the preceding theorems, which the explosion question explicitly asks to remove.

The target asks whether explosion **can occur** with infinite offspring mean. A single admissible offspring/fitness law with positive explosion probability answers that existential question. It is not a request to prove explosion for every infinite-mean law, and the candidate makes no such universal claim.

The source explains nonexplosion by finiteness of the infected set at every time. Accordingly the candidate proves infinitely many simultaneously infected vertices at a deterministic finite time, a stronger conclusion than infinitely many cumulative infections by that time.

The model permits the constant iid fitness $F=1$. If unbounded fitness support is additionally desired, independent finite fitnesses such as $1+\mathrm{Exp}(1)$ may instead be used by monotonicity. The unbounded-support condition on both variables earlier on p. 619 belongs to a different survival theorem, not to the general model definition.

## Extraction and neighboring-question boundaries

The upstream `original_statement` joins a preceding question about closing a moment-condition gap to the later explosion question. The full page separates them. This attempt addresses only the cleaned, verified explosion target.

Rank 280 / ID 30005042 is a different contribution by Mailler and Marckert, pp. 592–593, about a coupled discrete-generation weak-moment question. Sharing the report PDF does not identify their models.

The report's p. 618 summary reverses signs in two exponential-moment conditions. Those unrelated displayed prose conditions are not used here; the latest full author paper states them correctly. No claim depends on treating those source misprints as hypotheses.
