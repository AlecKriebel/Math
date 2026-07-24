# Pinned lower-dimensional theorem import

The endpoint proof imports exactly the following established theorem.

> If \(C\subset S^3\) and
> \(\langle x,y\rangle\leq1/2\) for every distinct \(x,y\in C\), then
> \(|C|\leq24\).  Equivalently, \(\tau(4)=24\).

Primary source:

- Oleg R. Musin, “The kissing number in four dimensions,” *Annals of
  Mathematics* (2) **168** (2008), no. 1, 1–32.
- DOI: <https://doi.org/10.4007/annals.2008.168.1>
- Journal landing page:
  <https://annals.math.princeton.edu/2008/168-1/p01>
- Publisher PDF:
  <https://annals.math.princeton.edu/wp-content/uploads/annals-v168-n1-p01.pdf>
- Publisher PDF SHA-256, fetched 2026-07-23 PDT:
  `b7bbcc13830ad2cc2aa0bbcc9434f4206b52b62f25ad1ca7c8e17531813688f3`.

The paper states the spherical-code convention on printed page 3:
pairwise angular separation at least \(\pi/3\), equivalently inner product
at most \(1/2\).  Its main theorem and proof appear on printed page 4:
the modified Delsarte inequalities give \(M<25\), hence \(M\leq24\), and
the 24-cell supplies equality.

This import includes the closed boundary
\(\langle x,y\rangle=1/2\).  It is applied only to the zero-height subset,
whose points remain distinct unit vectors in the four-dimensional linear
space \(u^\perp\).  No uniqueness or classification of 24-point
configurations is used.

To recheck the pinned publisher file without storing a second copy:

```sh
curl -L --fail --silent --show-error \
  https://annals.math.princeton.edu/wp-content/uploads/annals-v168-n1-p01.pdf \
  | shasum -a 256
```
