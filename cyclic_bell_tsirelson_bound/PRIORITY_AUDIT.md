# Focused priority audit

**Audit date:** 26 July 2026
**Status:** provisional; no worldwide-priority claim

## Bottom line

A focused search found no public proof of Conjecture 1 of
Perito--D'Avino--Jung--Mironowicz--Acin--Augusiak before this release. The
strongest defensible statement is:

> To the best of our knowledge, this is the first public analytic proof of
> Conjecture 1. The originating authors introduced the Bell family, conjectured
> the value, and supplied the attaining strategy and matching lower bound. The
> contribution here is the analytic upper bound, including its
> arbitrary-unitary strengthening.

This cannot exclude unpublished work, an unindexed manuscript, a concurrent
discovery, or an older theorem whose relevance was missed.

## Originating paper

- [Bell inequalities tailored to optimal global randomness certification,
  arXiv:2606.21362v3](https://arxiv.org/html/2606.21362v3)
- v1: 19 June 2026; v3: 21 July 2026.
- Conjecture 1 concerns the reduced functional \(\mathcal I_d\), defined in
  Eq. (11), and the value
  \(2\csc(\pi/(2d))\).
- The paper already gives the Weyl-based attaining strategy and admissible Bob
  observables.
- Appendix A.2 proves only
  \(\beta_{\mathrm Q}(\mathcal I_d)\le d\sqrt2\), says the bound is generally
  non-tight, and reports NPA tightness through \(d=6\).

Section VII's note added cites a different global-randomness construction:
[Farkas, Mironowicz, and Augusiak,
arXiv:2606.21369](https://arxiv.org/html/2606.21369). It does not analyze
\(\mathcal I_d\) or prove Conjecture 1.

## Related public work checked

- [Coccia, Padovan, and Vallone, *Systematic derivation of Tsirelson bounds in
  arbitrary dimensions*, arXiv:2606.21626](https://arxiv.org/html/2606.21626v1):
  a concurrent SOS framework for other qudit Bell families; no specialization
  to this operator or formula was found.
- [Salavrakos et al.,
  arXiv:1607.04578](https://arxiv.org/abs/1607.04578): a distinct Bell family
  tailored to maximally entangled states.
- [Buhrman and Massar, *Physical Review A* 72,
  052103](https://journals.aps.org/pra/abstract/10.1103/PhysRevA.72.052103):
  generalized CHSH games, but not this operator or bound.
- [Barizien, Sekatski, and Bancal,
  arXiv:2308.08601](https://arxiv.org/abs/2308.08601): general SOS construction
  methods, with no direct derivation located for this family.
- [Filipp and Svozil,
  arXiv:quant-ph/0403175](https://arxiv.org/abs/quant-ph/0403175): spectral
  optimization for fixed Bell operators, not the required all-strategy bound.
- [Noise-robustness companion,
  arXiv:2606.21371v2](https://arxiv.org/html/2606.21371v2): numerical
  three-outcome randomness results, not an all-\(d\) proof.

Searches included the arXiv identifier and title, the exact trigonometric
formula and common variants, “cyclic Bell operator,” Conjecture 1, Tsirelson
bound, polar-decomposition inequalities, current arXiv records, and public
repository text.

## Scope corrections

1. Conjecture 1 is about \(\mathcal I_d\), not the barred functional.
2. The value of the barred functional follows as a one-line corollary:
   \[
   \beta_{\mathrm Q}(\overline{\mathcal I}_d)
   =2\csc\!\left(\frac{\pi}{2d}\right)+1.
   \]
3. Exact values alone do not prove the separate uniqueness, self-testing, or
   maximal-randomness claims.
4. The polar inequality and scalar trigonometric identity are not claimed as
   individually new. The claimed contribution is their application to obtain
   the exact analytic bound.
5. Appendix A.1 of the source paper contains one \(B_y^\dagger\) convention
   inconsistent with the main definition and the following calculation. The
   new manuscript defines its convention explicitly.

## Residual risk

Direct public-prior-art risk appears low on the search performed. Concurrent
discovery risk is material because the conjecture is recent. Public release
secures a timestamp for this manuscript but does not establish scientific
priority or correctness.
