# 9900008: source-scoped negative answer for diffuse allocation tests

Status: **claimed_solved**, author turn **1/5**. The full source-scoped candidate stopped early; subsequent audits and publication checks add no proof-search turns.

A diffuse, nonzero, locally finite measure on R² can be invariant in law under every measurable, pointwise-covariant, measure-preserving allocation of its original observed state and still fail the full joint mass-stationarity identity. The example is singular, supported on horizontal lines of alternating densities 1 and 2. Covariance forces a preserving allocation to retain the rooted type; mass resampling chooses the other type with probability 2/3.

The unchanged [proof](author/PROOF.md) passed two independent AI-assisted mathematical audits. The accepted presentation includes the mandatory [source-credit addendum](CREDIT_ADDENDUM.md), bound to the exact proof by [the current acceptance](review2/ACCEPTANCE.json). No mathematical repair was required.

## Established ingredients and scope

The Lebesgue-product lift is established prior work: Last–Thorisson, *Construction and Characterisation of Stationary and Mass-Stationary Random Measures on R^d*, arXiv:1405.7566v2, §8 Proposition 1. Theorem 8 uses that lift with independent stationary backgrounds. The unequal-weight obstruction is also prior work, including Last–Thorisson (2009), Example 7.1, and the [related authored atomic control](https://github.com/AlecKriebel/Math/blob/7d244eed5d7ddd89d5c540aecfa72490b7b30073/unsolved_math_prioritization/attempts/30001080/TURN_3.md). See [the required addendum](CREDIT_ADDENDUM.md) and [primary 2015 manuscript](https://arxiv.org/pdf/1405.7566v2).

No novelty, historical priority, exhaustive literature clearance, human peer review, or formal proof-assistant certification is claimed. This is not a result for the all-Markov or Cox-projected premise, independent-stationary-background tests, free actions, no-invariant-direction models, one-dimensional diffuse measures, positive-density measures, or full-support variants.

## Preserved evidence

- `author/`: all eight exact frozen author files, unchanged, including historical pending-review labels.
- `review1/`: the unchanged clean first `AUDIT.md` and `acceptance.json`.
- `review2/`: all seven exact files of the fresh accepted review, unchanged.
- `archives/`: exact original author ZIP and exact fresh accepted-review ZIP.
- `PUBLICATION_INPUTS.json`: archive/member hashes, byte counts, public historical verification pins, and distribution boundaries.
- `PUBLICATION_MANIFEST.json`: exact distributable payload hashes; it excludes itself to avoid self-reference.

The historical first-audit executable archive and original external manifests are omitted from this distribution because the historical executable package contains absolute diagnostic paths. Their original bytes remain preserved; public hashes and sizes identify them. The first audit's acceptance applies to its stated original inputs. No sanitized or rebound historical audit is substituted. That historical executable package cannot be replayed from this public bundle.

The original source discussion's incomplete product-lift credit and pending-review labels remain historical. The current presentation is the exact unchanged proof, the required addendum, and the subsequent audits and acceptance. No copied third-party paper, extracted source text, corpus record contents, or private coordination files are distributed.

## Reproduce the included package

From any working directory, run `python /path/to/9900008/check_publication.py --self-test`. Python's standard library suffices. Ordinary, `-O`, `-I`, and `-I -O` modes are supported. The checker authenticates manifest membership and digests, exact ZIP-to-directory equality, the fresh acceptance bindings, and the included author checks. Its self-tests reject altered proof bytes, credit bytes, acceptance bytes, archive bytes, and extra payload files. It does not replay the omitted first-audit executable package.

`PUBLICATION_CHECKS.json` records the publisher's actual runs before publication. Finite diagnostics supplement the analytic proof; they do not establish its universal measurable claims. A manifest editable alongside all payload bytes is not an external authenticity guarantee; the immutable repository commit and external read-back hashes provide the publication anchor.
