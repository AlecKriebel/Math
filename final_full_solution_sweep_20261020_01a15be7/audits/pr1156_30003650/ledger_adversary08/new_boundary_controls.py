#!/usr/bin/env python3
"""New full-main falsification controls; every source executes behind offline blockers."""
import json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
ns={'__file__':str(HERE/'offline_whole_helper.py'),'__name__':'offline_review08_library'}
exec(compile((HERE/'offline_whole_helper.py').read_bytes(),ns['__file__'],'exec'),ns)

def controls():
 out=[]
 def add(name,cfg,expect='reject',appends=0):out.append({'name':'v8_'+name,'cfg':cfg,'expect':expect,'appends':appends})
 def account(value,field='description',loc='metadata'):
  def edit(records):
   item=records[1]
   if loc=='key':item[value]='unrelated'
   elif loc=='parent':item['parent']={'id':'90000003','metadata':{field:value}}
   elif loc=='files':item['files']=[{'checksum':'md5:'+'0'*32,'unknown':{field:value}}]
   else:item.setdefault(loc,{})[field]=value
  return {'edit_account':edit}
 enc=lambda s:''.join('%'+format(c,'02x') for c in s.encode())
 # HTML and human-facing delimiters are distinct from JSON closing quotes.
 for suffix in ['>','<','</p>','</a>','</em>','!','!:','\u201d','\u2019',':',']','}',')','"',"'",'.',';',' ','?x=1','#part']:
  for prefix in ['', '<p>', '<', 'Reference: ']:
   add('short_markup_'+repr(prefix)+'_'+repr(suffix),account(prefix+'10/abc'+suffix))
 for loc in ['links','parent','files','key']:
  for value in ['<10/abc>','<p>10/abc</p>','<a>10/abc</a>',enc('<10/abc>'),'<p>10/abc</p> '+ 'OWR 10/2025; 10.4171/OWR/2025/10']:
   add('markup_location_'+loc+'_'+value,account(value,loc=loc))
 # Exact-token leading/trailing edges beyond ASCII identifier characters.
 for prefix in ['0','abc','_','.','%', '\u00e9','\u03b1','\u0661','\u200d','[','(',"'",'"',':','/','-',' ', '\n']:
  expected='reject' if prefix in ['0','abc','_','.','%', '\u00e9','\u03b1','\u0661','\u200d'] else 'pass'
  add('bibliography_prefix_'+repr(prefix),account('OWR 10/2025; '+prefix+'10.4171/OWR/2025/10'),expected,1 if expected=='pass' else 0)
 for suffix in ['.5','/x','-x','_x','EXTRA','%2Fx','\u00e9','\u03b1',':x','?x=1','#x','.', '!',':','\u201d','\u2019','>','</p>',']','}',')','"',"'",';',' ','\n']:
  expected='reject' if suffix in ['.5','/x','-x','_x','EXTRA','%2Fx','\u00e9','\u03b1',':x','?x=1','#x'] else 'pass'
  add('bibliography_suffix_'+repr(suffix),account('OWR 10/2025; 10.4171/OWR/2025/10'+suffix),expected,1 if expected=='pass' else 0)
 # Flattening and bounded decoding on dict keys, list cells, all machine link slots.
 leads=['30003650','PR #1156','CP-plus rank','OWR-15957-003','10/abc','//doi.org/abc','10.5281/zenodo.23350364']
 for lead in leads:
  for loc in ['key','parent','files','links']:
   add('decoded_semantics_'+loc+'_'+lead,account(enc(lead),loc=loc))
 for depth in [1,2,7,8,9]:
  v='10/abc'
  for _ in range(depth):v=enc(v)
  add('depth_short_'+str(depth),account(v))
  v='unrelated'
  for _ in range(depth):v=enc(v)
  expected='pass' if depth<=8 else 'reject'
  add('depth_unrelated_'+str(depth),account(v),expected,1 if expected=='pass' else 0)
 # Projection suffixes must preserve independent content without treating plain
 # web paths as short DOI names. These controls preserve original guard tradeoff.
 for path in ['/10/2019/06','/10/21tkt-1.pdf','/ordinary/2019/06','/10/abc/def']:
  add('ordinary_web_path_'+path,account('https://foreign.invalid'+path),'pass',1)
 for loc in ['links','parent','files']:
  for lead in ['<10/abc>',enc('<10/abc>'),enc('30003650'),'//doi.org/abc','shortdoi.org/abc','OWR 10/2025; x10.4171/OWR/2025/10']:
   # parent/files tests include nested non-machine metadata, also scanned.
   add('projection_suffix_'+loc+'_'+lead,account('https://zenodo.org/api/records/90000001/files/'+lead,loc=loc))
 return out

if __name__=='__main__':
 results=[]
 for c in controls():
  r=ns['case_run'](c);results.append(r)
  if r['error'] and '[Errno 28]' in r['error']:raise RuntimeError('Infrastructure ENOSPC excluded')
 v={'mode':sys.flags.optimize,'case_count':len(results),'passed':sum(r['passed'] for r in results),'denied_actual_services':ns['DENIED'],'results':results}
 (HERE/('NEW_BOUNDARY_MODE_'+str(sys.flags.optimize)+'.json')).write_text(json.dumps(v,indent=2)+'\n')
 print(json.dumps({'mode':v['mode'],'cases':len(results),'passed':v['passed'],'failures':[(r['case'],r['error'],r['state']['append']) for r in results if not r['passed']]},indent=2))
