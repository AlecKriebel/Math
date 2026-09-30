# Infinite clusters and vertical fibers

**Unsolved after two substantive attempts.** The original question is not settled by this package.

[PARTIAL.md](PARTIAL.md) proves that an infinite cluster cannot have a uniform finite bound on its vertical-fiber intersection sizes when the base critical probability is 1. It also proves propagation of infinite intersections across neighboring fibers. The remaining possible counterexample has finite intersections with every fiber, but sizes unbounded across the base graph.

The note credits the known bounded-cutset special case, gives a stretched-tree example showing that hypothesis is strictly stronger, and identifies why unbounded exploration capacities do not yield a homogeneous percolation contradiction. These examples obstruct proof routes; they are not counterexamples to the original question.

[SOURCE_AUDIT.md](SOURCE_AUDIT.md) records the exact graph, product, and bond-percolation conventions, source recovery, and literature boundaries. The actual model was gpt-6-astra at xhigh reasoning. Separate adversarial review is pending.

Run `python check_coupling.py` from this directory. Its 4,996 exact finite assertions compare the capped exploration's reached-set law with the independent-reservoir implementation on K2 x C3 and check the probability calculations. This diagnostic cannot prove an infinite-volume assertion by itself.
