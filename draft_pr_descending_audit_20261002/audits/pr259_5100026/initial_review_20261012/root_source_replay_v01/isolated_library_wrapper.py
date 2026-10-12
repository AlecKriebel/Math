import runpy,sys
assert not sys.flags.optimize
sys.path.insert(0,sys.argv[1])
import sympy,mpmath
assert sympy.__version__=='1.14.0'
assert mpmath.__version__=='1.3.0'
script=sys.argv[2]
sys.argv=[script]
runpy.run_path(script,run_name='__main__')
