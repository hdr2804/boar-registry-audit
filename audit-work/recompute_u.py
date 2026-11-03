#!/usr/bin/env python3
"""Independent recompute of DEVICE-FINAL U-total / win counts from raw judgments.
Definition used (from boar-research data/glossary.md G-u-total):
  mass(answer) = mean(correctness, completeness, usefulness) - 1   [judge.v1 1-5]
  detected non-answers (trace ruler.refusedZ) -> app mass set to 0
  U-total = sum(w_i * app_mass_i) / sum(w_i * ref_mass_i) over the 71 headline items,
  health items w=0.5. Judgment scores averaged over the two presentation orders.
Win variants computed separately (judge 'winner' field vs mass comparison).
"""
import json, collections, itertools, os

HF = os.path.expanduser("~/workspace/poidh-1520-audit/audit-work/hf/rnd/research/coordinator/arms")
Q = {}
for l in open(HF + "/native-rc/work/v04/bench/questions.jsonl"):
    if l.strip():
        r = json.loads(l); Q[r["id"]] = r
H = [i for i in Q if not Q[i]["anchor"]]
W = {i: Q[i]["weight"] for i in Q}
DF = HF + "/device-final"

def load(seed, fam):
    T = {}
    for l in open(f"{DF}/traces/dev-s{seed}.traces.jsonl"):
        if l.strip():
            t = json.loads(l); T[t["itemId"]] = t
    per = collections.defaultdict(dict)
    for l in open(f"{DF}/judge/dev-s{seed}.{fam}.judgments.jsonl"):
        if l.strip():
            r = json.loads(l)
            if r.get("ok"):
                per[r["queryId"]][r["order"]] = r["mapped"]
    return T, per

def item_stats(T, per):
    out = {}
    for i in Q:
        if len(per.get(i, {})) < 2:
            out[i] = None; continue
        ms = list(per[i].values())
        app = sum(sum(m["boar"][k] for k in ("correctness","completeness","usefulness"))/3 for m in ms)/len(ms) - 1
        ref = sum(sum(m["ref"][k] for k in ("correctness","completeness","usefulness"))/3 for m in ms)/len(ms) - 1
        z = bool(T[i]["ruler"].get("refusedZ"))
        winners = [m["winner"] for m in ms]
        out[i] = dict(app=app, ref=ref, z=z, app_u=0.0 if z else app, winners=winners)
    return out

def U(stats, ids):
    num = sum(W[i]*stats[i]["app_u"] for i in ids if stats[i])
    den = sum(W[i]*stats[i]["ref"] for i in ids if stats[i])
    return num/den if den else None

res = {}
for seed in ("42","43"):
    for fam in ("opus","codex"):
        T, per = load(seed, fam)
        st = item_stats(T, per)
        res[(seed,fam)] = st
        ids = [i for i in H if st[i]]
        u = U(st, ids)
        both_boar = sum(1 for i in ids if all(w=="boar" for w in st[i]["winners"]))
        any_boar  = sum(1 for i in ids if any(w=="boar" for w in st[i]["winners"]))
        mass_win  = sum(1 for i in ids if st[i]["app_u"] > st[i]["ref"])
        mass_win_raw = sum(1 for i in ids if st[i]["app"] > st[i]["ref"])
        disagree  = sum(1 for i in ids if len(set(st[i]["winners"]))>1)
        zitems = [i for i in ids if st[i]["z"]]
        print(f"s{seed} {fam}: n={len(ids)} U={u:.4f} | wins both-orders={both_boar} any-order={any_boar} "
              f"mass-win(zeroed)={mass_win} mass-win(raw)={mass_win_raw} | order-disagree={disagree} | refusedZ={len(zitems)} {zitems}")

# pooled variants
for fam in ("opus","codex"):
    s42, s43 = res[("42",fam)], res[("43",fam)]
    # variant A (official): concat orders == mean of the two seeds' masses; zero only if refused in BOTH seeds
    pooled = {}
    for i in H:
        if s42[i] and s43[i]:
            app = (s42[i]["app"] + s43[i]["app"])/2
            ref = (s42[i]["ref"] + s43[i]["ref"])/2
            z = s42[i]["z"] and s43[i]["z"]
            pooled[i] = dict(app=app, ref=ref, z=z, app_u=0.0 if z else app, winners=[])
    uA = U(pooled, [i for i in H if pooled[i]])
    # variant B: zero if refused in EITHER seed (per-seed zeroing preserved under pooling)
    pooledB = dict(pooled)
    for i in pooledB:
        if s42[i]["z"] or s43[i]["z"]:
            pooledB[i] = dict(pooledB[i], app_u=0.0)
    uB = U(pooledB, [i for i in H if pooledB[i]])
    # variant C: simple mean of per-seed U
    uC = (U(s42,[i for i in H if s42[i]]) + U(s43,[i for i in H if s43[i]]))/2
    one_seed_z = [i for i in H if s42[i] and s43[i] and (s42[i]["z"] != s43[i]["z"])]
    print(f"POOLED {fam}: official-style(A)={uA:.4f}  either-seed-zero(B)={uB:.4f}  mean-of-seeds(C)={uC:.4f}  refused-in-exactly-one-seed={one_seed_z}")

# cross-seed item stability for the app itself (same engine, same items, gen seed differs)
for fam in ("opus","codex"):
    s42, s43 = res[("42",fam)], res[("43",fam)]
    diffs = [abs(s42[i]["app"]-s43[i]["app"]) for i in H if s42[i] and s43[i]]
    big = [(i, round(s42[i]["app"],2), round(s43[i]["app"],2)) for i in H if s42[i] and s43[i] and abs(s42[i]["app"]-s43[i]["app"])>=1.0]
    print(f"{fam}: mean |app mass s42-s43| = {sum(diffs)/len(diffs):.3f}; items differing by >=1.0 mass: {big}")
