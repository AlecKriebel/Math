import sys,copy
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
import sympy as sp
import pytest
from k2p_cleanroom import Edge,Network
from k2p_cleanroom.domain import is_strict_rational_edge,is_strict_inheritance

def base():
 s1,g1,s2,g2,s3,g3,s4,g4=sp.symbols('s1 g1 s2 g2 s3 g3 s4 g4')
 return Network('r',{'A':'A','B':'B','C':'C'},[
  Edge('e0','r','u',s1,g1),Edge('eA','u','A',s2,g2),Edge('eB','u','B',s3,g3),Edge('eC','r','C',s4,g4)],{})

def test_swapped_k2p_coordinates_rejected_by_fingerprint():
 n=base();q=n.fourier_coordinate({'A':1,'B':1,'C':0});qswap=n.fourier_coordinate({'A':2,'B':2,'C':0})
 assert sp.factor(q-qswap)!=0

def test_deleted_relation_changes_tensor():
 n=base();m=copy.deepcopy(n);m.edges=m.edges[:-1]
 with pytest.raises(ValueError):m.fourier_coordinate({'A':1,'B':1,'C':0})

def test_duplicate_edge_id_rejected():
 n=base();m=copy.deepcopy(n);m.edges=list(m.edges)+[m.edges[0]]
 with pytest.raises(ValueError):m.validate()

def test_wrong_leaf_label_transport_changes_coordinate():
 n=base();q1=n.fourier_coordinate({'A':1,'B':1,'C':0});q2=n.fourier_coordinate({'A':1,'B':0,'C':1})
 assert sp.factor(q1-q2)!=0

def test_boundary_and_nonstochastic_edges_rejected():
 assert not is_strict_rational_edge(sp.Rational(1),sp.Rational(1))
 assert not is_strict_rational_edge(sp.Rational(9,10),sp.Rational(4,5)) # p2=0
 assert is_strict_rational_edge(sp.Rational(9,10),sp.Rational(801,1000),positive_eigenvalues=True)

def test_continuous_time_inequality():
 assert is_strict_rational_edge(sp.Rational(1,2),sp.Rational(1,2),continuous_time=True)
 assert not is_strict_rational_edge(sp.Rational(1,2),sp.Rational(1,4),continuous_time=True)

def test_inheritance_boundaries_rejected():
 assert is_strict_inheritance([sp.Rational(1,3),sp.Rational(2,3)])
 assert not is_strict_inheritance([sp.Rational(0),sp.Rational(1)])
