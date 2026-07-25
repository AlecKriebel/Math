\\ Exact arithmetic specializations of T^d-T^2+UT+V.
\\ A specialized Galois group embeds in the generic group away from the
\\ discriminant.  Full S_d here is independent finite-row evidence.

x = 'x;

check_degree(d) =
{
  my(f = x^d - x^2 - 3*x - 5, G);
  if(!polisirreducible(f),
    error(Str("FAIL: reducible specialization at d=", d)));
  G = polgalois(f);
  if(G[1] != d!,
    error(Str("FAIL: Galois order at d=", d, " is ", G[1])));
  if(G[4] != Str("S", d),
    error(Str("FAIL: Galois label at d=", d, " is ", G[4])));
  print("PASS d=", d, ": ", G[4], " of order ", G[1]);
};

for(d = 3, 10, check_degree(d));

print("PASS: arithmetic S_d specializations for d=3,...,10");
