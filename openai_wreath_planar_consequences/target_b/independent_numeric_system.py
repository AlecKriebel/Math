import numpy as np, math, json, hashlib, datetime
rows=np.array([[1,-670689128,-6398628799,-250018302,4107732082],[3,93524468,564897270,-186215974,-65204793],[4,-64146977,121133118,82882809,-327822296],[7,-1358193,-16329465,1979670,21637038],[9,-2932910,-940875,3636920,2145806],[12,3646952,-34846939,-6005382,34369042],[13,3183411,63030995,-574123,-75237042],[15,11390977,27049982,-11312377,-34985096],[16,-5593246,13405071,5915710,-10980954],[19,54905,-1515007,-120136,1498351],[21,-210208,-634307,177992,747946],[24,976077,-804949,-1037705,105643],[25,-824472,7003719,1011732,-6510015],[27,611891,4536095,-428528,-4440927],[28,-472882,-107613,399655,403751],[31,30744,-112653,-31773,90515],[33,-4974,-105568,1240,99081],[36,128313,246018,-114876,-267388],[37,-176685,505187,166591,-396209],[39,-21638,472037,32128,-402283],[40,-18461,-165597,10836,164974],[43,4565,-2296,-4050,547],[45,1477,-10734,-1524,8978],[48,10748,50050,-8611,-45048],[49,-20506,7495,17354,-266],[51,-10361,29035,9641,-21534],[52,2121,-26523,-2269,23159],[55,425,858,-344,-839],[57,302,-632,-266,463],[60,382,5658,-231,-4688],[61,-1481,-4320,1140,4098],[63,-1494,-352,1265,647],[64,558,-2609,-491,2114],[67,21,169,-14,-145],[69,34,13,-28,-18],[72,-55,394,53,-301],[73,-21,-805,5,685],[75,-136,-379,108,338],[76,70,-144,-58,104],[79,-1,19,1,-15],[81,2,9,-2,-8],[84,-13,3,11,0],[85,13,-87,-11,70],[87,-6,-60,4,49],[88,6,5,-4,-5],[91,0,1,0,-1],[93,0,1,0,-1],[96,-2,-4,1,3],[97,2,-6,-2,4],[99,0,-6,0,5],[100,0,2,0,-2]])
pi=np.pi;b=np.sqrt(3)/2;h=2/5;B=4/3
A=np.array([0,1,3,4,7,9]); nodes=rows[:,0].astype(int); J=[1,3,4]
P=np.array([5,-1+2j*b,1+2j*b,-2,-.5+1j*b,-1-2j*b,1])
ts=np.arange(7)/6
C=np.array([-.013,.017])
def calculate(order):
 xs,ws=np.polynomial.legendre.leggauss(order)
 t=np.concatenate([(2*j-1+xs)/12 for j in range(1,7)])
 w=np.tile(ws/12,6); pieces=np.repeat(np.arange(1,7),order)
 lam=1j/(b*(t+1j*h));z=-B/(t+1j*h)-1j*h
 la=1j/(b*(ts+1j*h));za=-B/(ts+1j*h)-1j*h
 def measure(n,kind):
  out=np.zeros(len(t),complex)
  for j in range(1,7):
   ix=pieces==j; phase=P[j:]*np.exp(1j*pi*ts[j:]*n)
   sums=phase.sum();weighted=(phase*ts[j:]).sum()
   density=(-2*pi*pi*(weighted-t[ix]*sums) if kind==0 else 2j*pi*sums)*np.exp(-1j*pi*t[ix]*n)
   out[ix]=w[ix]*density
  return out
 cols=[(n,k) for k in range(2) for n in nodes]
 mu=np.stack([measure(n,k) for n,k in cols],axis=1)
 q=[];d=[]
 for a in A:
  dif=pi*(a-A[A!=a])/12
  q.append((pi/6)**2*np.prod((2*np.sin(dif))**2))
  d.append((pi/6)*np.sum(np.cos(dif)/np.sin(dif)))
 Q=np.array([q[np.flatnonzero(A==n%12)[0]] for n in nodes])
 D=np.array([d[np.flatnonzero(A==n%12)[0]] for n in nodes])
 kernel=np.exp(1j*pi*nodes[:,None]*z)*lam
 transformed=(kernel@mu).real; prime=((kernel*(1j*pi*z))@mu).real
 S=np.vstack([-transformed/Q[:,None],(D[:,None]*transformed-prime)/Q[:,None]])
 fixed=np.stack([measure(0,0)+.44*measure(0,1),-.368*measure(0,1)],axis=1)
 atoms=np.array([1,2,2,2,2,2,2])[:,None]*P[:,None]*C
 kfixed=(kernel@fixed+np.exp(1j*pi*nodes[:,None]*za)@ (la[:,None]*atoms)).real
 kprime=((kernel*(1j*pi*z))@fixed+np.exp(1j*pi*nodes[:,None]*za)@((la*1j*pi*za)[:,None]*atoms)).real
 gp=np.vstack([-kfixed/Q[:,None],(D[:,None]*kfixed-kprime)/Q[:,None]])
 g=gp[:,::-1].copy();g[len(nodes),0]-=1
 tab=np.stack([np.r_[rows[:,1+2*i]/1e10,rows[:,2+2*i]/1e10] for i in range(2)],axis=1)
 resid=np.column_stack([tab[:,i]-S@tab[:,1-i]-g[:,i] for i in range(2)])
 xxplus=np.linalg.solve(np.eye(102)-S,g[:,0]+g[:,1])
 xxminus=np.linalg.solve(np.eye(102)+S,g[:,0]-g[:,1])
 exact=np.column_stack([(xxplus+xxminus)/2,(xxplus-xxminus)/2])
 return {'order':order,'residual_max':np.abs(resid).max(),'residual_l1':np.abs(resid).sum(axis=0).tolist(),'solution_tab_error_l1':np.abs(exact-tab).sum(axis=0).tolist(),'SJJ':S[np.ix_([0,1,2,51,52,53],[0,1,2,51,52,53])].tolist()},S,mu,fixed,atoms,t,z,lam
a, *_=calculate(64); c, *_=calculate(128)
print(json.dumps({'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'independent_gauss_legendre':[a,c]},indent=2))
