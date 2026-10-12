# Independent primary-source comparison before reading family reports

UTC: 2026-10-06T03:45:24.181432+00:00
Bounded-disposition review completion estimate: 65%.

I read the original candidate first, GKT2007 §§4–5 and Tabachnikov2015 §7,
then ROOT's proposed disposition, the full relevant DR2019 §§2–4, and
DLMF19.7.8. I inspected the primary PDF views for GKT pp17–18,
Tabachnikov p62, and DR2019 pp5–6 and13. No sibling family's report
has been read at this checkpoint.

The analytic closure claim is recoverable from DR2019's stated surface limit:
its k=1 separated differential at surface caustic zero gives two coordinates
with magnitudes 2dτ and 2dS. The global candidate cylinder independently
supplies real surface sufficiency. No closed approximating billiard is assumed.

Eq3.2 uses -m1 A_k+n1 B_k-n2 C_k=0. The finite counts are m1 and n2;
the nonnegative belt count n1 is unbounded as its B0 term collapses. Eliminating
it using k=0 makes n1 B1 tend to zero and leaves m1 Iv=n2 Iu.
The source proof of Theorem3.2 (Case S1, printed p7) explicitly identifies n2
with x2=0 crossings. Its superficial wording below Eq3.2, “traced the segment”,
must not be interpreted as all monotone traversals. On a winding-r positive
surface path there are 2r such crossings and 4r monotone lambda3 traversals.
One full lambda1 excursion equals one full tropic arc, yielding N Iv=2r Iu.

Independent complete negative-characteristic DLMF identification:
delta=(a-b)/(b+c), g=c/a, k²=delta*g in(0,1).
Iv=2sqrt(a/(b+c))*[(1+g)Pi(-g,k)-K(k)].
Iu=2sqrt(a/(b+c))*[(1+g)Pi(-delta,k)-g*K(k)].
DLMF19.7.8 at amplitude pi/2 gives
Pi(-delta,k)+Pi(-g,k)-K(k)=pi/(2sqrt((1+delta)(1+g))).
Their sum is exactly pi; all denominators remain positive, so no principal value.
The positive-characteristic representation with h=(a-b)/a,j=c/(b+c),hj=k²
also gives Iu=2b/sqrt(a(b+c))*Pi(h,k) and
Iv=2b/sqrt(a(b+c))*[Pi(j,k)-K(k)].

A float Simpson diagnostic at a=4,b=1,c=2 gives
Iu=2.26934153935842, Iv=0.8722511142313729, sum error=0;
negative-characteristic Iu residual=0,
negative-characteristic Iv residual=-9.99e-16.
These are diagnostic corroboration only; the displayed substitutions and identity
are the exact checks. System Python lacked mpmath; no dependency was installed.

The original criterion does not claim an algebraic Cayley determinant. The third-kind
poles defeat the imported ordinary elliptic-torsion argument, without proving that
all algebraic conditions are impossible. The proposed closing note states these
limits. No substantive overclaim identified at this independent checkpoint.
I have not inferred complete singular billiard-flow convergence, exact prior printing,
or earliest priority. No new central proof-search turn was used.
