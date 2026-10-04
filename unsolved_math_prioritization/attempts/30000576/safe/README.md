# Chaos of individual operators: prior-literature attribution

Problem 30000576 / OWR-1323-013, queue rank 658. Checked 4 October 2026.

## Finding

The published literature attributes a negative answer to both questions to
Frédéric Bayart and Teresa Bermúdez, *Semigroups of chaotic operators*,
Bulletin of the London Mathematical Society 41 (2009), 823–830,
[DOI 10.1112/blms/bdp055](https://doi.org/10.1112/blms/bdp055).
Its publisher abstract announces a chaotic semigroup containing no chaotic
individual operator. The original problem's co-proposer Alfredo Peris
corroborates the C0-semigroup result with Elisabetta M. Mangino in
[*Frequently hypercyclic semigroups*](https://doi.org/10.4064/sm202-3-2),
p. 235, immediately before Proposition 2.6.

This is an **attribution-only already-solved candidate**. It is neither a new
mathematical result nor an independent verification of the 2009 proof.
The resolving article's full text was not recovered. Its precise theorem
number, construction, and explicit scalar-field/space hypotheses have not
been checked directly. An independent source audit is required before
promoting the queue correction.

## Exact target

The source is the final problem in §5 of the open-problem session, printed
p. 2272 of [Oberwolfach Report 37/2006](https://doi.org/10.4171/OWR/2006/37),
by Alfredo Peris and José A. Conejero. The report is from the 2006 workshop;
EMS lists online publication in 2007.

Let X be a separable complex Banach space and let (T_t) for real t >= 0 be a
strongly continuous semigroup of bounded linear operators on X. Assume it
is hypercyclic and the union of ker(T_s-I), over real s > 0, is dense in X.
Must every T_t, t > 0, be Devaney chaotic? Must at least one such T_t be
Devaney chaotic? Both positive-time questions are retained.

## Scope of this packet

- The printed problem was read and visually checked.
- The 2009 publication and abstract were verified at the publisher.
- The 2011 corroborating discussion and reference were read in the complete
  publisher PDF and visually checked.
- A 2017 survey coauthored by both original problem proposers repeats the
  negative result on p. 762 in its C0-semigroup setting.
- Direct inspection of the resolving proof remains unavailable.

See VERIFICATION.md for hypothesis coverage, LIMITATIONS.md for the precise
gate, and SOURCE_MANIFEST.json for retrieval and byte-verification metadata.
Run `python3 tests/verify_packet.py` for packet-integrity checks. These checks
do not validate an infinite-dimensional counterexample.
