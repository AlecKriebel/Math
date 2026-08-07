# Expert audit note

## Exact theorem

The manuscript proves that every finite stochastic mass-action reaction network that is weakly reversible, has one linkage class, and has molecularity at most two at every complex is positive recurrent on each closed communicating class, for every positive rate vector.

The result is class-wise: coordinate faces, siphons, parity constraints, and other lattice restrictions are retained rather than replaced by an irreducibility assumption on the full state space.

## Exact prior hypothesis removed

Anderson, Cappelletti, and Kim (2020) proved the binary one-linkage result under the additional condition that, for every species, the complex set contains a multiple of that species. In a binary network, this means that each species occurs in a pure unary or pure double complex. The present manuscript removes that hypothesis.

No claim is made for multiple linkage classes, molecularity three or higher, the full Anderson-Kim positive-recurrence conjecture, product-form stationary measures, exponential ergodicity, or mixing rates.

## Four central proof ideas

1. **Marked target chain.** The embedded chain records the target complex of the actual reaction channel that just fired. If the post-jump population is \(x\) and the mark is \(t\), then \(x-t\ge0\).

2. **Residual factorial potential.** With
   \[
   V(x,t)=\sum_i\log((x_i-t_i)!),
   \]
   a next channel with source \(s\) and target \(u\) has the exact increment
   \[
   V(x-s+u,u)-V(x,t)=\log\frac{(x)_t}{(x)_s}.
   \]
   Following the carried target as the next source therefore has zero increment.

3. **Finite target-following episodes.** A fixed directed path from the carried target to a selected terminal complex is followed only while its exact marked channels fire. A one-dimensional scalar envelope propagates the negative drift of a rare terminal source backward through every finite path, without comparing unrelated rate monomials.

4. **Logarithmic compactification and bimolecular dichotomy.** Every divergent residual sequence yields normalized logarithmic weights on species. Molecularity at most two gives an exhaustive top-complex split: either a higher-weight source is enabled over a lower terminal complex, making the terminal source probability vanish, or a reaction-wise linear invariant contradicts divergence inside one communicating class.

These ingredients yield a finite nonempty exceptional set, a state-selected random-time drift of at most \(-1\) outside it, and a finite trace-chain return argument. Nonexplosion is then proved directly from recurrent visits to a marked state and its repeated positive exponential holding times.

## Reproducibility

The proof is universal and does not rely on computation. The standalone package checks exact channel identities, scalar-envelope branches, adversarial boundary examples, and a finite top-complex atlas.

Run from the release root:

```bash
cd code
python -m pip install -e .
./reproduce.sh
```

The script runs the test suite, generates the canonical verification report twice, requires byte-for-byte agreement, and prints its SHA-256 digest.
