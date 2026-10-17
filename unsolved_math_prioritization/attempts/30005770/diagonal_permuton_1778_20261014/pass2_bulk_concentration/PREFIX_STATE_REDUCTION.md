# Exact first-hit prefix states, and the remaining geometry

This is an exact structural reduction for the actual principal class C=Av(alpha skew-sum 1), with fixed nonempty alpha. It does not prove bulk concentration. It complements the abstract countermodel by recording genuine permutation structure that the countermodel does not impose.

## Canonical state

For sigma in C_j, let L(sigma) be the first endpoint of an alpha occurrence, with L=j+1 when alpha is absent.

- If L<=j, retain the first L entries, standardize them, and mark the state as containing alpha.
- If L=j+1, retain the entire permutation sigma and mark the state as alpha-absent.

The absent flag prevents mistaking the sentinel j+1 for an actual entry. An empty alpha-absent state is permitted. The endpoint in a containing state is its last entry.

**Lemma.** The complete minimum-insertion continuation tree from sigma is determined by its canonical state. In particular, if L<=j and p=standardize(sigma(1),...,sigma(L)), then

D_t(sigma)=D_t(p),  t>=0,

with a bijection preserving every successive insertion-gap index. If alpha is absent, the whole permutation is the retained state and the assertion is tautological.

**Proof.** An allowed new minimum is inserted in a gap k<L. The old alpha occurrence ending at original position L survives the insertion and has its endpoint shifted one place to the right. Thus the new first-alpha endpoint is no later than that surviving endpoint. The same statement holds after every subsequent insertion. Inductively, all inserted minima lie before that original endpoint, and the original suffix after it remains strictly to its right.

No point in that suffix can determine the first-alpha endpoint, since a full old occurrence persists strictly before it. Every alpha occurrence ending before or at the surviving endpoint uses only retained-prefix entries and inserted minima. Standardizing those original prefix entries preserves their relative order, and every later inserted entry is smaller than every retained original entry. Therefore the first-alpha endpoint and hence the complete allowed gap set are identical in the full permutation and its retained standardized prefix after every finite insertion history. This gives the claimed gap-preserving bijection. QED.

After an insertion one may recanonicalize by truncating to the new first-hit endpoint, or keeping the entire current state when alpha is absent. This yields an exact countable-state description. It does not make the scalar label L a sufficient state, and it does not make a descendant-weighted state uniform.

## Scalar label is genuinely insufficient

For alpha=132, the two containing states 1342 and 2143 both avoid2431 and have L=4. Their child-label lists, in gap order, are respectively

(5,5,5,5) and (3,5,5,5).

Consequently their depth-two completion counts are 20 and 18. Thus even the first-hit endpoint, together with the flag that alpha occurs, does not determine continuation weights.

For the uncovered seed alpha=312, states 1423 and 2413 both avoid4231, have L=4, and have respective child-label lists

(5,5,4,5) and (5,4,4,5),

so their depth-two continuation counts are 19 and 18. These are small exact witnesses, not asymptotic evidence for or against a permuton limit.

## Scope of the reduction

The suffix-free state representation can reduce an exact recurrence or sampler: permanent suffixes do not need to be remembered to count future minima. The number and size of prefix states are unbounded. No uniform spectral estimate, positive recurrence statement, or macroscopic completion-weight control has been proved here.

The repaired abstract tree shows that scalar degree bounds, Catalan domination, supermultiplicative finite growth, and even the all-size binomial completion inequality do not force the desired weighted tail. A proof for actual avoiders must exploit additional compatibility of these prefix states, their alpha-specific transitions, or another genuinely permutation-geometric ingredient. No inherited cell context is assumed to be uniformly distributed, and no context-preserving staircase surgery has been established in this lane.
