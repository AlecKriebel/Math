import contextlib,io,runpy,sys
with contextlib.redirect_stdout(io.StringIO()):
 ns=runpy.run_path(sys.argv[1])
if sys.argv[2]=="author":ns["ck"]("root-known-false",False)
else:ns["ck"](False,"root-known-false")
raise RuntimeError("FALSE CONTROL WAS ACCEPTED")
