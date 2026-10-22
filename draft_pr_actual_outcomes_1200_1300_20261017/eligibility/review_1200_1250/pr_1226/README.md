# Harmonic LCM avoidance: the prior exponent and finite-block characterization

Target: 2344 / EP-856. Disposition: accepted existing fixed-k exponent and finite-block theorem, with local repairs to an independent ancillary density argument. Numerical evaluation and a full multiplicative asymptotic remain unresolved by this audit.

This is an AI-assisted, unrefereed authored mathematical audit edition. Acceptance means an independent internal AI audit of the precisely scoped written arguments and their explicitly retained standard and external dependencies. It is not external human peer review, journal acceptance, formal proof-assistant certification, or a novelty or priority claim.

This is not a computational reproduction package. The complete ten-section mathematical reconstruction and full ancillary correction note are retained, including all parameter orders, supremum qualifications, density substitutions, dependencies and limitations. Executable code, raw calculation outputs or datasets, copied source documents or text, source images and private coordination material are not distributed.

Retrieval, inspection and mathematical-check statements describe the original audit of October 11, 2026 UTC. Editorial preparation performed no new scholarly-source retrieval, source-body inspection, literature survey or mathematical execution. Historical finite checks supplement the written proofs; they do not establish asymptotic claims or numerically evaluate the exponent.

## Exact accepted scope

For each fixed integer k≥3, let f_k(N) be the maximum reciprocal sum over A⊆{1,…,N} having no k distinct elements with one common pairwise least common multiple. The accepted prior result is existence of

    gamma_k = lim_(N→∞) log f_k(N) / log log N

and the exact finite-block characterization

    gamma_k = sup_(n≥1, 1≤r≤n) r M_k(n,r)^(1/r)/(e n),

where M_k(n,r) is the largest cardinality of an r-uniform k-cosunflower-free family on an n-point ground set. The weighted pressure descriptions, complete-layer bounds, monotonicity and fixed-k consequences are also accepted. Chojecki supplies the weighted squeeze; Luo–Yang–Zhu gives an elementary presentation of the required weighted estimates and the finite-block elimination. These are credited existing arguments.

AUDIT.md preserves the entire ten-section reconstruction, including the uniform-product restriction, nonsquarefree upper transfer, repeated-projection blow-up argument, fixed-parameter prime buckets, every order of limits, the squeeze, legitimate Cartesian-product supremum interchange and exact block optimization. Standard Mertens reciprocal and logarithmic first-moment estimates remain analytic inputs. No growing-parameter uniformity or attained extremum is inferred.

## Ancillary repairs and numerical limits

Tang–Zhang's printed Lemma 5.6 drops 1/(n+1). The correction retains −log(n+1) and enlarges K(epsilon), with its original fixed-parameter conclusion intact. Theorem 5.5's literal all-n hypothesis fails at beta=2, k=3, n=1; the intended input needs an all-sufficiently-large-n qualification. The complete direct density substitute proves the required consequence for each fixed k≥3 without an unjustified nonuniform product. The harmless log(N²) scale typo is retained explicitly. PROOF.md is the full correction note; section 9 of AUDIT.md retains the expanded density argument and both routes to the full-density consequence.

These two ancillary defective passages are not dependencies of the accepted core exponent and finite-block proof. The repaired full-density consequence is gamma_k=1 if and only if the ordinary sunflower capacity mu_k^S=2.

An exact variational characterization is not a numerical evaluation. Even gamma_3 is not evaluated here. There is no closed general formula, proof of an attained finite maximum, effective numerical stopping certificate, determination from mu_k^S alone, bounded multiplicative error, effective rate, or conclusion f_k(N)∼C_k(log N)^gamma_k. A finite block gives a lower bound; finitely many such blocks do not bound the full supremum from above.

The elementary audited bound is 1/e≤gamma_k≤1. The sharper interval log(1.551)<gamma_3≤3/2^(2/3)−1, approximately 0.438899884194402<gamma_3≤0.889881574842310, depends on the cited 1997 capacity construction and 2017 upper theorem. Their proofs were not independently re-audited; those dependencies are not required for exponent existence or the finite-block equality. The main weighted argument bypasses Sathe–Selberg; the ancillary appendix check retains it as a standard cited input.

## Reading order and public evidence

1. AUDIT.md: complete mathematical reconstruction and exact boundaries.
2. PROOF.md: complete authored ancillary correction note.
3. ACCEPTANCE.md and ACCEPTANCE.json: accepted core, repaired ancillary scope and unresolved stronger claims, with identities of the distributed reports.
4. SOURCES.json: original historical public provenance, every inspected page list, PDF size/hash, retrieval match and limitation.
5. VERIFICATION.json: historical finite-check scope, result identities and normal/-O/-OO byte agreement, excluding code and raw results.
6. MANIFEST.json: all eight filenames and the other seven files' sizes and hashes. Its digest is separately pinned in the publication description.

## Principal public sources

- Tang and Zhang, Harmonic LCM patterns and sunflower-free capacity, arXiv:2512.20055v1, December 23, 2025: https://arxiv.org/abs/2512.20055v1
- Chojecki, Weighted sunflower pressure and the exact polylogarithmic exponent in harmonic LCM patterns, April 15, 2026: https://www.ulam.ai/research/erdos856-final.pdf
- Luo, Yang and Zhu, The exponent of harmonic LCM avoidance, arXiv:2609.07268v1, September 7, 2026: https://arxiv.org/abs/2609.07268v1
- Erdős, Some extremal problems in combinatorial number theory (1970), target on printed page 127: https://www.renyi.hu/~p_erdos/1970-21.pdf
- Alon, Shpilka and Umans, On sunflowers and matrix multiplication, CCC 2012, Theorem 2.4: https://theory.stanford.edu/~virgi/cs367/papers/sunflowersmult.pdf
- Lichtman, Almost primes and the Banks–Martin conjecture, equation (4.9): https://arxiv.org/abs/1909.00804

All three primary manuscript texts were read completely during the original audit and their freshly retrieved PDFs matched the originally inspected bytes. Only the indicated relevant portions of Erdős, Alon–Shpilka–Umans and Lichtman were inspected. This bounded audit does not certify an exhaustive literature review, later manuscript status, journal acceptance or universal consensus.
