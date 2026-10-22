# Optimality of Monotonized Asymptotic Risk

- ID: **30005253**; source code: **OWR-11695855-006**; rank: **627**.
- Disposition: **unsolved**, **5/5** substantive approaches.
- No full resolution or novel discovery is claimed.

The elementary greatest-nondecreasing-minorant identity is already known. The source asks for a statistical optimality principle without prescribing its comparator class.

This packet proves a sharp result for selectors under uniform risk approximation, and records why broader interpretations fail:

1. Pointwise deterministic limits alone are insufficient even for selection. A bounded-loss symmetric learner has limiting risk 2 at every aspect ratio, while selection from training prefixes attains risk 1.
2. In the motivating Gaussian regression model with signal energy 4 and noise variance 1, the minimum-norm least-squares envelope at aspect ratio 1 is 4. A shrunk half-sample fit has conditional limiting risk 11/3.
3. The same base learner and identical risk profile can be Bayes-optimal in one model and suboptimal in another. A minimax principle therefore needs explicit model and procedure classes.

Read `PROOF.md` for definitions, quantifiers, five approaches and exact gaps; `SOURCES.md` for attribution; `RESEARCH_LOG.md` for the bounded investigation.

## Reproduce the controls

Python 3 standard library only:

```sh
python compute_controls.py --output replay.json
```

The checks use exact integers and fractions: 1,024 finite profiles, 7,770 admissible minorants, 49,506 selector inequalities including ties, exact rare-event probabilities, finite torus bijections, Gaussian risk identities and a minimax-order countercontrol. Decimal output is for display only. These controls check finite identities and implementation; the probabilistic limit arguments are in the proof and require mathematical review.

`SHA256SUMS` identifies the frozen authored files. The sources' PDFs, full texts and catalogue corpora are excluded.
