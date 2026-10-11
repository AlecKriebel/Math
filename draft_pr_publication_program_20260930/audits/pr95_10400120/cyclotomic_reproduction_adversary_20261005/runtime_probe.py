import sys,os,json,importlib.util
import sympy,numpy
print(json.dumps({'executable':sys.executable,'version':sys.version,'pid':os.getpid(),'sympy_version':sympy.__version__,'sympy_origin':sympy.__file__,'numpy_version':numpy.__version__,'numpy_origin':numpy.__file__,'sympy_spec':str(importlib.util.find_spec('sympy')),'numpy_spec':str(importlib.util.find_spec('numpy')),'python_flags':str(sys.flags)},indent=2))
