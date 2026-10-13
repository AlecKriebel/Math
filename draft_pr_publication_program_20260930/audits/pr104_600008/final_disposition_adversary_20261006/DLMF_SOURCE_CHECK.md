# Official DLMF source check

Read through web tool on 2026-10-06 UTC:

- https://dlmf.nist.gov/19.7#E8, complete relevant subsection 19.7(iii), especially Eq19.7.8 and its parameter product.
- https://dlmf.nist.gov/19.20#E1, Eq19.20.1 giving RC(0,y)=pi/(2sqrt(y)) for positive y through RC(x,y)=RF(x,y,y).

The observed Eq19.7.8 in normalized notation is

Pi(phi,alpha²,k)+Pi(phi,omega²,k)
=F(phi,k)+sqrt(C)*RC((C-1)(C-k²),(C-alpha²)(C-omega²)),
alpha²*omega²=k², C=csc²(phi).

Our exact specialization is phi=pi/2, C=1, alpha²=-delta,
omega²=-g, delta=(a-b)/(b+c)>0, g=c/a>0 and k²=delta*g<1.
It gives

Pi(-delta,k)+Pi(-g,k)-K(k)
=pi/(2sqrt((1+delta)(1+g))).

This is an authored observation and notation normalization, not a byte-for-byte
archive of the DLMF server response. The remote byte hash is unavailable.
A later ordinary urllib GET for https://dlmf.nist.gov/19.7.E8.tex returned HTTP403
on its first request; the second scheduled TeX retrieval was not attempted.
No access-control bypass or repeated fetch was attempted. The successful official
web view above supplies the mathematical source evidence; the TeX failure does
not create a mathematical gap.
