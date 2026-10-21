import sys,runpy
sys.path.insert(0,'/Users/alec/Library/Python/3.11/lib/python/site-packages')
p=sys.argv.pop(1)
runpy.run_path(p,run_name='__main__')
