# Non-strong directed supports

**Status: PROVED.** This note closes the part of the directed model not covered
by the strongly connected hypothesis in the cited noncomplete-support theorem.
No numerical computation is used.

Let the loopless directed support have positive incoming degree at every
target, but suppose it is not strongly connected. Consider the condensation
DAG of its strongly connected components.

If the condensation has two or more source components, a single initial
mutant cannot fixate: at least one source component starts entirely resident,
and no edge from outside can place mutant offspring into it. Thus the fixation
probability is zero.

Suppose instead that there is a unique source component `C`, necessarily a
proper subset of the vertices. A singleton mutant initially outside `C`
cannot send a descendant into `C`, so only initial vertices in `C` can
possibly lead to fixation.

For `i in C`, let

```text
s_i^+ = |{v != i : w_iv > 0}|
```

be its positive out-support degree. While `i` is the only mutant, its death
causes extinction with probability `1/n` per update. A gain can occur only
when one of its `s_i^+` out-neighbors dies. If `p_iv(r)<=1` is the conditional
probability that `i` wins the competition at target `v`, then, after deleting
self-loops, the probability of a gain before extinction is exactly

```text
[sum_{v:w_iv>0} p_iv(r)] / [1 + sum_{v:w_iv>0} p_iv(r)]
    <= s_i^+/(s_i^++1)
    <= (n-1)/n.
```

Fixation requires such a first gain. Uniform singleton initialization
therefore gives, for every finite `r>0`,

```text
rho_dB(G,r)
  <= (1/n) sum_{i in C} s_i^+/(s_i^++1)
  <= |C|(n-1)/n^2
  <= (n-1)^2/n^2.
```

The complete-graph dB baseline tends to `(n-1)/n`, and

```text
(n-1)/n - (n-1)^2/n^2 = (n-1)/n^2 > 0.
```

Consequently every non-strongly-connected support is strictly dB-suppressing
relative to `K_n` for all sufficiently large finite fitness.

Together with the cited theorem for strongly connected noncomplete directed
supports and the independently proved complete-support column-SOS theorem,
this yields the fixed-graph trichotomy for every loopless directed weighting
with positive incoming degree at every target.
