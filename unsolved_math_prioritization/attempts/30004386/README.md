# Random cube projections: prior published solution

**Already solved by Johnston, Kabluchko and Prochno in Studia Mathematica 264 (2022), 103–119.** Their Theorem A is the exact requested probability-measure-valued large-deviation principle. Proposition 3.1 also yields the proposed Prohorov limit set, with the realization of all its elements spelled out in [SOURCE_STATUS.md](SOURCE_STATUS.md).

This package corrects an outdated open classification. It claims no new discovery and uses no additional tail assumptions or growing projection-dimension regime. Separate adversarial review is pending.

The complete original report and author manuscript were inspected. [SOURCE_AUDIT.md](SOURCE_AUDIT.md) records the source match, version and access details, and prior-attempt checks. The actual model was gpt-6-astra with xhigh reasoning. No new proof attempt was needed once the exact published result was located.

Run `python check_normalization.py` for 527 exact rational checks of the variance and finite coefficient approximations. These are diagnostics; the cited theorem supplies the LDP.
