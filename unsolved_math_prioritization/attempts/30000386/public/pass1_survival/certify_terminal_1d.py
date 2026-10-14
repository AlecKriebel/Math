"""Exact 1D common-terminal game and independently checkable Devil certificate.
All attacks detonate at the final horizon, each after one observed Angel move.
Positions in state are relative to the Angel. Reflections are exact symmetries.
"""
from functools import lru_cache
import json, pathlib
ROOT=pathlib.Path(__file__).parent

def canon(B):
    b=tuple(sorted(set(B)))
    reflected=tuple(-x for x in reversed(b))
    return min(b,reflected)

@lru_cache(None)
def win(h,B):
    if h==0:return True
    if h==1:return any(s not in B for s in (-1,0,1))
    for s in (-1,0,1):
        C=tuple(b-s for b in B if abs(b-s)<=h-1)
        if all(win(h-1,canon(C+(q,))) for q in range(-h+1,h)):
            return True
    return False

states={}
def build(h,B):
    B=canon(B)
    key=f'{h}:'+','.join(map(str,B))
    if key in states:return key
    if win(h,B):raise RuntimeError('Cannot certify a winning state')
    entry={'remaining_moves':h,'bombs':list(B),'responses':[]}
    states[key]=entry
    if h==1:
        if not {-1,0,1}.issubset(B):raise RuntimeError('Bad terminal')
        return key
    for s in (-1,0,1):
        C=tuple(b-s for b in B if abs(b-s)<=h-1)
        options=sorted(range(-h+1,h),key=lambda q:(abs(q),q))
        q=next(q for q in options if not win(h-1,canon(C+(q,))))
        child=build(h-1,canon(C+(q,)))
        entry['responses'].append({'angel_move':s,'devil_bomb_relative_to_new_position':q,'next_state':child})
    return key

def verify(cert):
    if cert['horizon']!=6 or cert['first_bomb_relative_to_first_angel_position']!=0:raise RuntimeError('Bad root')
    if cert['dimension']!=1 or cert['moves']!=[-1,0,1] or cert['all_detonation_times']!=6:raise RuntimeError('Bad game metadata')
    seen=set()
    def check(key,h,B):
        row=cert['states'][key]
        if row['remaining_moves']!=h or tuple(row['bombs'])!=canon(B):raise RuntimeError('Bad state')
        if key in seen:return
        seen.add(key)
        if h==1:
            if not {-1,0,1}.issubset(B):raise RuntimeError('Nonlethal leaf')
            if row['responses']:raise RuntimeError('Unexpected leaf responses')
            return
        if sorted(r['angel_move'] for r in row['responses'])!=[-1,0,1]:raise RuntimeError('Missing response')
        for r in row['responses']:
            s=r['angel_move'];q=r['devil_bomb_relative_to_new_position']
            if not isinstance(q,int):raise RuntimeError('Invalid bomb')
            C=tuple(b-s for b in B if abs(b-s)<=h-1)
            check(r['next_state'],h-1,canon(C+(q,)))
    check(cert['root'],5,(0,))
    if seen!=set(cert['states']):raise RuntimeError('Unreachable rows')
    return {'verified':True,'reachable_states':len(seen),'lethal_leaf_states':sum(r['remaining_moves']==1 for r in cert['states'].values()),'announcement_count_before_final_move':5}

if __name__=='__main__':
    results=[{'horizon':h,'angel_wins':win(h,())} for h in range(1,7)]
    root=build(5,(0,))
    cert={'horizon':6,'dimension':1,'moves':[-1,0,1],'all_detonation_times':6,'first_bomb_relative_to_first_angel_position':0,'root':root,'states':states}
    (ROOT/'terminal_1d_horizon6_certificate.json').write_text(json.dumps(cert,indent=2)+'\n')
    print(json.dumps({'terminal_game_results':results,'certificate':verify(cert)},indent=2))
