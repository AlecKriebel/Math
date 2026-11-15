"""Bounded new-five fault controls; only in-memory copies are mutated."""
from five_common import *
from five_source import load_bundles,view_record
from five_contract import check_page
from five_markup import Tree,nodes,text,serialize
from verify_stage_read_only import check_overlays
import copy,sys
DATE='2026-11-15'
def run_controls():
 bundles=load_bundles();root=OWN/'candidate-a/public';pages={};files={};results=[]
 for b in bundles:
  folder=root/'research'/b['slug'];files[b['rid']]={p.name:p.read_bytes() for p in folder.iterdir()};pages[b['rid']]=files[b['rid']]['index.html']
  check_page(b,pages[b['rid']],files[b['rid']],DATE,dlab_homepage=True)
 index=(root/'research/index.html').read_bytes();sitemap=(root/'research/sitemap.xml').read_bytes();check_overlays(bundles,index,sitemap,DATE)
 def rejects(label,operation):
  try:operation()
  except ValueError as e:results.append({'fault':label,'literal_outcome':'DELIBERATE_NEW_TARGET_FAULT_REJECTED','rejection':str(e)});return
  raise RuntimeError('ACCEPTED_MUTATION:'+label)
 def pagecase(b,label,changed,assetfiles=None):
  need(changed!=pages[b['rid']] or assetfiles is not None,'nonvacuous_page_control:'+label)
  rejects(label,lambda:check_page(b,changed,files[b['rid']] if assetfiles is None else assetfiles,DATE,dlab_homepage=True))
 def replace_node(b,n,mutated):
  old=serialize(n).encode();need(pages[b['rid']].count(old)==1,'one_exact_mutation_locator');return pages[b['rid']].replace(old,serialize(mutated).encode(),1)
 for b in bundles:
  tree=Tree(pages[b['rid']].decode());ps=[x for x in nodes(tree.find('main')[0]) if x['tag']=='p' and len(text(x))>80]
  p=ps[len(ps)//2];q=copy.deepcopy(p);q['children'].append(' UNAPPROVED qualification change.')
  pagecase(b,b['rid']+':nonleading_body_paragraph',replace_node(b,p,q))
  if b['rid']=='23441890':p=next(x for x in nodes(next(s for s in tree.find('section') if s['attrs'].get('id')=='abstract')) if x['tag']=='p')
  else:p=next(x for x in tree.find('p') if ' '.join(text(x).split())==' '.join(b['abstract'].split()))
  q=copy.deepcopy(p);q['children']=['Truncated abstract.'];pagecase(b,b['rid']+':full_abstract_truncated',replace_node(b,p,q))
 b=bundles[0];raw=pages[b['rid']]
 pagecase(b,'113:wrong_proposed_canonical',raw.replace(('rel="canonical" href="https://aleckriebel.com/research/'+b['slug']+'/').encode(),b'rel="canonical" href="https://example.invalid/',1))
 pagecase(b,'113:wrong_original_datetime',raw.replace(b'datetime="2026-10-17"',b'datetime="2026-11-15"',1))
 pagecase(b,'113:wrong_SEO_title',raw.replace(b'<title>',b'<title>Unapproved ',1))
 pagecase(b,'113:unadopted_dead_Dlab_href',raw.replace(('href="'+NEW_DLAB+'"').encode(),('href="'+OLD_DLAB+'"').encode(),1))
 tree=Tree(raw.decode());m=next(n for n in nodes(tree.find('main')[0]) if 'data-tex' in n['attrs']);q=copy.deepcopy(m);q['children']=['WRONG VALUE'];pagecase(b,'113:math_visible_value_disagrees_with_source_TeX',replace_node(b,m,q))
 for tag in ['template','noscript']:
  pagecase(b,'113:outer_'+tag+'_hides_article',raw.replace(b'<body>',('<body><'+tag+'>').encode(),1).replace(b'</body>',('</'+tag+'></body>').encode(),1))
 for tag in ['style']:
  pagecase(b,'113:hidden_article_style',raw.replace(b'</head>',b'<style>article{display:none}</style></head>',1))
 b=bundles[2];raw=pages[b['rid']]
 pagecase(b,'115:wrong_BibTeX_relative_parent_path',raw.replace(b'href="citation.bib"',b'href="../citation.bib"',1))
 pagecase(b,'115:wrong_scholarly_version',raw.replace(b'"version": "1.0"',b'"version": "99.0"',1))
 for ext in ['pdf','zip']:
  b=bundles[4];bad=dict(files[b['rid']]);name=b[ext]['name'];bad[name]=bad[name][:-1]
  pagecase(b,'117:truncated_whole_'+ext,pages[b['rid']],bad)
 rejects('index:old_visible_entry_modified',lambda:check_overlays(bundles,index.replace(b'<li>',b'<li>UNAPPROVED ',1),sitemap,DATE))
 rejects('index:wrong_ItemList_count',lambda:check_overlays(bundles,index.replace(b'"numberOfItems": 83',b'"numberOfItems": 82',1),sitemap,DATE))
 rejects('sitemap:wrong_new_lastmod',lambda:check_overlays(bundles,index,sitemap.replace(b'<lastmod>2026-11-15</lastmod>',b'<lastmod>2026-10-01</lastmod>',1),DATE))
 original=load(OWN/'FROZEN_INPUT_SET.json')['records']['23331080'];bad=copy.deepcopy(original);bad['whole_three_custom_verdicts']['scope']={'status':'PASS'}
 rejects('117:whole_qualified_verdict_coerced_to_generic_PASS',lambda:view_record('23331080',bad))
 bad=copy.deepcopy(original);key=next(k for k,v in bad['whole_native_root_JSON_objects'].items() if type(v) is dict and len(v)>1);bad['whole_native_root_JSON_objects'][key]=dict(reversed(list(bad['whole_native_root_JSON_objects'][key].items())))
 rejects('117:original_native_object_key_order_normalized',lambda:view_record('23331080',bad))
 rejects('output:production_write_fence',lambda:safe_output(PUBLIC))
 return {'literal_custom_status':'BOUNDED_NEW_FIVE_POSITIVES_AND_ALL_DELIBERATE_FAULTS_REJECTED','optimization':sys.flags.optimize,'pristine_record_positives':5,'pristine_overlay_positive':True,'faults_rejected':len(results),'results':results,'writes_or_network':False,'old_campaigns_or_source_programs_replayed':False}
if __name__=='__main__':print(json.dumps(run_controls(),indent=2))
