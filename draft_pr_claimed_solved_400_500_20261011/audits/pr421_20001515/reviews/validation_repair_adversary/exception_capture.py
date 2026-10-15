import builtins, contextlib, io, json, pathlib, sys, traceback
def typed(v):
    if isinstance(v,dict): return {'type':'dict','items':[[typed(k),typed(x)] for k,x in v.items()]}
    if isinstance(v,(tuple,list)): return {'type':type(v).__name__,'items':[typed(x) for x in v]}
    return {'type':type(v).__name__,'value':v}
p=pathlib.Path(sys.argv[1]); target=pathlib.Path(sys.argv[2])
ns={'__name__':'__main__','__file__':str(p)}
if sys.argv[3]=='shadow': ns['AssertionError']=RuntimeError
stream=io.StringIO()
try:
    with contextlib.redirect_stdout(stream): exec(compile(p.read_bytes(),str(p),'exec'),ns)
    result={'exception_type':None,'args_typed':None,'args_repr':None,'traceback':None,'optimization':sys.flags.optimize}
    code=0
except BaseException as e:
    result={'exception_type':type(e).__module__+'.'+type(e).__qualname__,'args_typed':typed(e.args),'args_repr':repr(e.args),'traceback':traceback.format_exc(),'optimization':sys.flags.optimize}
    code=10
target.write_text(json.dumps(result,indent=2)+'\n')
sys.stdout.write(stream.getvalue())
sys.exit(code)
