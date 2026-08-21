import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
import sympy as sp
from k2p_cleanroom import Edge,Network,classify

def tree():
 s1,g1,s2,g2,s3,g3,s4,g4=sp.symbols('s1 g1 s2 g2 s3 g3 s4 g4')
 return Network('r',{'A':'A','B':'B','C':'C'},[
  Edge('e0','r','u',s1,g1),Edge('eA','u','A',s2,g2),Edge('eB','u','B',s3,g3),Edge('eC','r','C',s4,g4)],{})

def test_zero_sum_and_tree_monomial():
 n=tree();assert n.fourier_coordinate({'A':1,'B':0,'C':0})==0
 # A=1,B=1,C=0: e0 sees 0; eA/eB each s; eC sees 0.
 q=n.fourier_coordinate({'A':1,'B':1,'C':0})
 syms={str(x):x for x in q.free_symbols};assert sp.factor(q-syms['s2']*syms['s3'])==0

def test_pattern_normalization():
 n=tree();p=n.pattern_tensor();assert sp.factor(sum(p.values())-1)==0

def test_graph_classification():
 c=classify(tree());assert c['binary'];assert c['tree_child'];assert c['level']==0

def test_reticulation_switching_weights():
 s,g=sp.symbols('s g');a=sp.symbols('a')
 n=Network('r',{'A':'A','B':'B'},[
  Edge('ru','r','u',s,g),Edge('rv','r','v',s,g),Edge('ur','u','z',s,g),Edge('vr','v','z',s,g),
  Edge('uA','u','A',s,g),Edge('zB','z','B',s,g)],{'z':[('ur',a),('vr',1-a)]})
 sw=list(n.switchings());assert len(sw)==2;assert sp.factor(sum(w for _,w in sw)-1)==0
