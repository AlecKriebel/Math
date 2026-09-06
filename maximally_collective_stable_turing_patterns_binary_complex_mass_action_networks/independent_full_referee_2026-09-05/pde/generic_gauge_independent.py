import sympy as s
R=s.Rational
nu,L,h=s.symbols('nu L h',positive=True); m=nu+2
sig=1/(126*nu); w02=(1008*m**2-20459*m+37138)/(31752*nu*(8*m-17)); w0m=-R(1,81); w0z=(16861*m-34044)/(7938*(8*m-17))
hs=h+1/(8190*nu)
dot=4*L*(nu*w02-sig*nu*(nu-1)/2+w02*hs-sig*((91*nu-1)*hs-nu))+2*w0m+w0z
dotrho=1-8*L*(nu+hs)
tau=s.factor(-dot/dotrho)
At=1494249120*h*L*nu**2-69786990*h*L*nu+108738630*L*nu**2+1214388*L*nu-8521*L-125249670*nu**2+1031940*nu
Bt=32760*h*L*nu+32760*L*nu**2+4*L-4095*nu
assert s.factor(tau+At/(15876*(8*nu-1)*Bt))==0
print('Generic gauge from independently telescoped physical mass sum PASS')
