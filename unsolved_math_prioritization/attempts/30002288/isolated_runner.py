"""Verified dispatcher. Only the pinned publication wrapper invokes this file."""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):raise SystemExit('REJECT: require -I -S -B')
shim,entry,*args=sys.argv[1:]
sys.executable=shim
sys.argv=[entry,*args]
with open(entry,'rb') as f:source=f.read()
exec(compile(source,entry,'exec'),{'__name__':'__main__','__file__':entry})
