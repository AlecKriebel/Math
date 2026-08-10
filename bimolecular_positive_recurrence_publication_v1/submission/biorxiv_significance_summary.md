# Systems Biology significance summary

Inside cells, many biochemical species occur in small copy numbers, so random
reaction events can strongly influence molecule counts. Stochastic
mass-action models describe this noise with continuous-time Markov chains. To
interpret long-run behavior, one needs to know that a model has a
stationary probability distribution rather than drifting permanently toward
ever-larger populations.

This paper proves such stability for a specific structural class: finite
weakly reversible reaction networks with one linkage class and no complex
containing more than two molecules. For every choice of positive reaction
rates, each closed communicating class has a unique stationary probability
law. Thus stationary state probabilities and averages of bounded observables
are well-defined within that class. Finite molecule-count means or variances
require integrability and are not asserted. The
criterion is structural rather than parameter-tuned, which can be useful when
rate constants are uncertain.

The theorem does not apply to every biochemical network. It gives no explicit
stationary formula, mixing time, tail bound, or guarantee that sample paths
remain in a bounded region, and it does not prove finite expected entry into a
closed class from every initial state. Its contribution is a rigorous
foundation for steady-state analysis in the stated class of stochastic
biochemical models.
