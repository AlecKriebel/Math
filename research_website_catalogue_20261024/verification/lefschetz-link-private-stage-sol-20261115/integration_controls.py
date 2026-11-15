"""Nine bounded memory-only editorial losses, after explicit new website GO only.

No candidate writes, scientific imports, native replay, subprocess or network.
"""
import copy
import html
import json
import sys
from stage_common import IDS,structured,main_block,dump,frozen_inputs,records
from stage_common import need
from render_stage import render_buffers,validate_buffers


def changed_main(body,transform):
    text=body.decode();old=main_block(text);new=transform(old)
    need(old!=new,'real targeted visible-main control mutation')
    return text.replace(old,new,1).encode()


def changed_article(body,transform):
    text=body.decode();match,graph=structured(text);transform(graph['@graph'][1])
    return (text[:match.start(1)]+dump(graph)+text[match.end(1):]).encode()


def main():
    g,source,website,by=frozen_inputs();rows=records(by)
    good=render_buffers(by,rows,g['build_date']);validate_buffers(good,by,website,rows,g['build_date'])
    bases=['research/'+r['config']['slug']+'/' for r in rows]
    faults=[]
    def reject(label,mutator):
        bad=dict(good);mutator(bad)
        try:validate_buffers(bad,by,website,rows,g['build_date'])
        except ValueError as e:faults.append({'name':label,'rejected':True,'exception_type':type(e).__name__})
        else:raise RuntimeError('bad editorial output falsely accepted: '+label)
    p127=bases[0]+'index.html';p128=bases[1]+'index.html'
    reject('actual-visible-original-abstract-loss',lambda b:b.__setitem__(p127,changed_main(b[p127],
           lambda m:m.replace(html.escape(rows[0]['config']['abstract']),'truncated abstract',1))))
    reject('hidden-actual-main-article',lambda b:b.__setitem__(p128,changed_main(b[p128],lambda m:m.replace('<article>','<article hidden>',1))))
    reject('missing-original-standalone-TeX',lambda b:b.pop(bases[1]+'assets/nullstellensatz.tex'))
    reject('reversed128-native-encoding-order',lambda b:b.__setitem__(p128,changed_article(b[p128],lambda a:a['encoding'].reverse())))
    reject('invented128-MIT-encoding-grant',lambda b:b.__setitem__(p128,changed_article(b[p128],lambda a:a['encoding'][0].__setitem__('license','https://opensource.org/license/mit/'))))
    reject('blanket127-mixed-ZIP-encoding-license',lambda b:b.__setitem__(p127,changed_article(b[p127],lambda a:a['encoding'][0].__setitem__('license','https://creativecommons.org/licenses/by/4.0/'))))
    def corrupt_old_index(b):
        text=b['research/index.html'].decode();match,value=structured(text)
        value['mainEntity']['itemListElement'][0]['name']='altered prior research entry'
        b['research/index.html']=(text[:match.start(1)]+dump(value)+text[match.end(1):]).encode()
    reject('changed-prior-typed-index-record',corrupt_old_index)
    reject('inflated128-critical2010-reading',lambda b:b.__setitem__(p128,changed_main(b[p128],
           lambda m:m.replace('It does not certify every earlier or final-version proof, exhaustive literature coverage, or the absence of an earlier equivalent ideal counterexample.',
                              'It certifies a new full46-page audit and the absence of earlier equivalent counterexamples.',1))))
    bad_by=dict(by);path=str(rows[1]['ed'].parent.parent/'sources/SOURCE_READY.json')
    ready=json.loads(bad_by[path]);ready['printed_version']='1.0';bad_by[path]=json.dumps(ready).encode()
    try:records(bad_by)
    except ValueError as e:faults.append({'name':'rewritten-historical-READY-null','rejected':True,'exception_type':type(e).__name__})
    else:raise RuntimeError('historical null normalization falsely accepted')
    need(len(faults)==9,'nine actual bounded editorial controls')
    print(json.dumps({'optimization_level':sys.flags.optimize,'fault_count':len(faults),'new_memory_only_faults':faults,
                      'positive_buffers_changed':False,'candidate_or_source_writes':False,
                      'scientific_or_old_campaign_replay':False},indent=2))


if __name__=='__main__':main()
