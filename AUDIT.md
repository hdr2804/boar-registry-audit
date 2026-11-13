# The registry is the weak layer: a provenance error, a filtered census, and the lever the record closed without running its own rule

**An independent audit of the BOAR / LabRat research record, for poidh bounty #1520**
Auditor: hdr (with an AI research agent) · 2026-11-03
Material: `github.com/r4topunk/boar-research`, `github.com/r4topunk/boar-bench`,
`github.com/r4topunk/labrat-boar-fork`, HF dataset `r4topunk/boar-traces`
(all six downloaded trace/judgment files sha256-match `boar-research/TRACES.tsv`).

---

**Contents**

- [0. What this audit is — and is not](#0-what-this-audit-is--and-is-not)
- [1. Provenance error: three registry rows, one measurement, two of them judgeless](#1-provenance-error-three-registry-rows-one-measurement-two-of-them-judgeless)
- [2. The census: "387 experiments, 215 without a gain" does not mean what it says](#2-the-census-387-experiments-215-without-a-gain-does-not-mean-what-it-says)
  - [2.1 The 387 is a filtered subset, stated as the whole](#21-the-387-is-a-filtered-subset-stated-as-the-whole)
  - [2.2 "215 without a gain" contradicts the registry's own definitions — both ways](#22-215-without-a-gain-contradicts-the-registrys-own-definitions--both-ways)
  - [2.3 The 387 counts rows, not independent experiments](#23-the-387-counts-rows-not-independent-experiments)
  - [2.4 One in seven results is flagged "as recorded" — including 30% of the adopted set](#24-one-in-seven-results-is-flagged-as-recorded--including-30-of-the-adopted-set)
  - [2.5 Preregistration is mostly unverifiable from the public record](#25-preregistration-is-mostly-unverifiable-from-the-public-record)
- [3. The buried lever: THINK4B (X-111) — closed without its own criterion](#3-the-buried-lever-think4b-x-111--closed-without-its-own-criterion)
- [4. Smaller cross-document items (for completeness)](#4-smaller-cross-document-items-for-completeness)
- [5. Reproduction](#5-reproduction)
- [6. What I am *not* claiming](#6-what-i-am-not-claiming)

---

## 0. What this audit is — and is not

Fourteen claims already audit the LabRat app code, the grader, the scorer and the
retrieval analysis. This audit examines a different layer: **the experiment registry
itself** — `data/experiments.json` and the counts, verdicts and provenance the whole
public record stands on. The timing scorer is a separate layer again, audited on its
own by claim 9575: its report that the hidden-thinking instrument reads 0 on all 2,086
llama-server traces with recorded reasoning is that claim's finding, not this audit's,
and nothing below depends on it. Follow-up retrieval is likewise a separate layer,
audited on its own by claim 9576: its report that, on the final build's own headline
traces, 5 of 12 non-health follow-up turns retrieved no on-topic passage on either path
is that claim's finding, not this audit's, and nothing below depends on it either.
Three findings, all reproduced from the published files with the scripts in §5:

1. **A provenance error:** one judged measurement is registered as the result of three
   different experiments — including one that ran 0 judge calls.
2. **A filtered census:** the headline "387 experiments, 215 without a gain" counts a
   filtered subset of the registry, splits single screens into multiple counted rows,
   and contradicts the registry's own verdict definitions in both directions.
3. **A buried lever (THINK4B):** the largest non-adopted gain in the registry was
   closed on one seed, against the record's own frozen two-seed criterion, with the
   decisive run prepared, priced — and never executed.

Calibration first, because it matters: **the DEVICE-FINAL phone numbers reproduce.**
I independently recomputed the pooled U-totals from the published HF judgment files —
**0.165** (Claude) and **0.242** (gpt-5.6-sol), win rate 0 of 71 under both judge
families — exactly as published. The final measurements are solid. The registry layer
around them is not.

---

## 1. Provenance error: three registry rows, one measurement, two of them judgeless

Registry rows **X-120** (DENSECHUNK), **X-143** (DENSECHUNK-ST) and **X-144**
(DENSECHUNK-ST2) all carry the identical result:

```
+0.017 (−0.000…+0.035)
```

That number was produced by exactly one run: DENSECHUNK-ST2's Opus L2 judging —
`rnd/research/coordinator/CLOSED.md` row R46 attributes it solely to ST2
("Opus paired Δ +0.017 (−0.000…+0.035) raw … 180 public self-test items, 4B cut 7,
Haiku L1 then Opus L2 N=4 both orders (720 Opus)").

Neither of the other two rows could have produced a judged paired CI:

- **X-143** — `judge: "none (deterministic gate)"`; its own `verdict_detail`:
  *"closed: FAIL at step 0 (G2 no-harm; G1 and G3 PASS); **0 judge calls**"*;
  seeds: *"n/a (replay only, 0 judge calls)"*.
- **X-120** — `judge: "none (deterministic gate)"` on a different item set
  ("32 in-pack v0.2…"), verdict: a deterministic headroom gate, parked.

Yet both rows present ST2's judged CI as their `result`, and all three cite the same
fact (F-1122) and the same source row (`CLOSED.md:70`).

**Why it matters.** The registry is the evidence base for the headline "387 documented
experiments". Copied result fields make it impossible for a reader to tell which
experiment measured what — and the dense-chunk retrieval lever (a genuine candidate:
step-0 reach 67 → 108 contexts) appears to have three convergent measurements behind
it when it has exactly one. It is also not an isolated formatting quirk: grouping all
387 rows by identical result string (≥ 25 chars) yields **13 groups covering 32 rows**
— e.g. X-154/X-155 (STACK / STACK-2) share `+0.005 (−0.009…+0.021)`.

---

## 2. The census: "387 experiments, 215 without a gain" does not mean what it says

### 2.1 The 387 is a filtered subset, stated as the whole

`data/SCHEMA.md`'s own release note (v1.1.2, 2026-10-29):

> "…experiments **387 of 402**: the 15 rows left out cite only internal facts, 13 of
> them numbers of the app maintainer's app withheld under the maintainer-data rule."

`CHANGELOG.md` confirms the 15 rows were present in v1.1.1 and removed. The registry of
the research as conducted had **402 rows**; the bounty text, the article (§4) and
`llms.txt` all state "387 recorded experiments" with no filtering caveat — and because
the withheld rows' verdicts are not public, the 215 split **cannot be verified as a
property of the research**, only of the filtered publication. A reader also cannot
reconcile the registry's ID holes (ids run X-001…X-406; 19 numbers absent: 194–197,
202, 203, 219, 224, 323, 328, 331, 335–337, 367, 378, 395–397) with the 15 withheld
rows, because the withheld ids were never published.

The shipped contract document even contradicts itself on the totals: SCHEMA.md's
release note gives source/public counts of 2,225→2,138 facts and 402→387 experiments,
while its own table quotes 2,191 facts and 401 experiments for the same release,
unmarked as superseded.

### 2.2 "215 without a gain" contradicts the registry's own definitions — both ways

Recount of `data/experiments.json` by its `verdict` field (total 387):

| verdict | count | the registry's own definition |
|---|---|---|
| adopted | 57 | shipped or recommended by its frozen rule |
| closed | 187 | rule failed, CI excluded the hoped-for gain |
| not-detected | 28 | "CI straddles zero below the test's MDE: **not evidence of no effect**" |
| parity | 10 | "an equivalence…, **not a gain**" |
| measurement | 57 | no lever verdict |
| tooling | 32 | method or infrastructure arm |
| open | 16 | parked, running or awaiting a result |

215 = 187 + 28 exactly: `closed ∪ not-detected`. But:

- the 10 **parity** rows are *defined* as "not a gain" and are excluded — counting by
  the registry's own definition gives **225**;
- the 28 **not-detected** rows are *defined* as "not evidence of no effect" (the
  article's own table glosses them "too small to see; not a no") and are included —
  the headline folds "we couldn't see it" into "it didn't happen".

And the implied complement misleads too: only **57 of 387 (14.7%)** rows ended with an
adopted gain; **115 rows** (measurement + tooling + open + parity) are neither. The
"215 vs 57" reading the headline invites is not supported by the registry's taxonomy.

### 2.3 The 387 counts rows, not independent experiments

`CLOSED.md` row R1 is **one** four-model closed-book screen (Qwen3.5-4B, Gemma 4 E4B,
Qwen3.5-9B, Ministral 8B; one fact, F-512; one combined result
`0.437/0.495/0.488/0.457 vs 0.487`). It became **two** registry experiments — X-028
(G4E4B) and X-033 (Q35) — each carrying the full four-model result string, each
"not-detected", **each counted inside the 215**. Same pattern: X-076/X-077
(MOESCREEN per-model rows over one three-model screen). Row-splitting single screens
inflates both the 387 and the 215 with duplicated evidence.

### 2.4 One in seven results is flagged "as recorded" — including 30% of the adopted set

`experiments.json` flags **54 of 387** rows `result_verified = false`; its own note
says those results come from the 2026-10-13 ledger audit "and [were] not re-verified
for this publication; render it as 'as recorded'". **17 of the 57 adopted rows** — the
levers the research says shipped (AR, CUT4-KVFIX, DETMAX, HAIKUJUDGE, KVQ8, CUT5-LITE,
…) — are in the unverified set. The positive half of the research's conclusions
("what worked") rests, for 30% of its entries, on numbers the publication itself
declines to vouch for.

### 2.5 Preregistration is mostly unverifiable from the public record

**137** rows claim preregistration status "yes, sha256-frozen", but only **15** include
a `where_public` pointer to the frozen criterion; for the other 122 the freeze is an
assertion, not a checkable artifact — in the very files published for verification.
Separately, `hypothesis` is **null for all 387 rows** (the notes disclose the text
"lives only in the criterion file (not extracted in this pass)"). For a record whose
central claim is procedural rigour — "a pass/fail rule frozen before the run"
(`llms.txt`) — the frozen rules are mostly not inspectable where it matters most.

---

## 3. The buried lever: THINK4B (X-111) — closed without its own criterion

**The approach.** Swap the frozen 4B claim build (Qwen3-4B-Instruct, build K) for its
thinking sibling (Qwen3-4B-Thinking-2507) at a 512-token thinking budget (arm Z).
Registry row **X-111**; closed-registry row **R10**; arm report
`rnd/research/coordinator/arms/think4b/THINK4B.md`.

**The measurement.** On V-para — the record's bounty-style set, the same set the claim
build's headline stands on: raw **0.439 vs K's 0.413, Δ +0.026 (CI −0.013…+0.068)**,
at ×3.7 time. This is **the largest positive point estimate of any non-adopted 4B-side
lever in the registry**. The mechanism is not speculative: inside the same record,
thinking budget is the one lever shown to move this metric family — on the deep tier,
budget 0→512 lifts the floor-adjusted score 0.329 → 0.436 (article §4; F-009).
THINK4B is the only same-scale test of that mechanism on the configuration that
actually carried the bounty claim.

**Why the closure does not meet the record's own standard.**

1. **One seed, against a two-seed criterion — in the registry's own words.** X-111's
   `verdict_detail`: *"closed: NO (near-lever), stopped after seed 42 (**one seed, not
   the two-seed verdict the criterion specifies**)"*. Every claim-build verdict on
   V-para in this record (F-001's K numbers included) is a two-seed verdict.
2. **The settling run exists — prepared, priced, never run.** X-111's `seeds` field:
   *"s42 only (s43 requests prepared, not run)"*; THINK4B.md's request table lists
   "s43 82befe13… prepared, not run"; the `reopen_if` note prices it: *"BACKLOG s3:
   V-para s43 (Opus 102)"* — **102 judge calls**. It was parked behind the condition
   "only if the 4B side reopens" (CLOSED.md R10) — a condition the project's own pivot
   to the 1.7B engine made unreachable, while the non-thinking 4B's score remains the
   published old-scale headline (F-001).
3. **The closure bar was applied asymmetrically.** The test was closed at "MDE 0.06"
   although its own CI reaches **+0.068** — the run as executed could not distinguish
   "no effect" from an effect larger than gains adopted elsewhere in the same record:
   X-182 (LITEREACH2-180) shows its +0.005 (CI −0.014…+0.025) line converted and built
   on in the shipped 1.7B line; SEFIX-124 was taken "for delivery" at +0.013
   (status.json changelog, 2026-10-22). THINK4B's point estimate is 2× the latter and
   5× the former.
4. **The counter-evidence is narrower than the closure implies.** LITE-THINK (X-188)
   found thinking flat/negative on the **1.7B** — a different model, a 20-item
   self-test, Haiku-judged, MDE ≈ 0.08 by the record's own critique. THINK4B-V02
   (X-112) read +0.009 on v0.2 at Haiku L1 — a screen, not the V-para Opus verdict.
   Neither is a two-seed Opus test of thinking on 4B/V-para. Only the un-run seed 43
   would have been.
5. **The honest objection — ×3.7 time — does not close the case.** At the claim run's
   pace (K p50 10.1 s, BAR-TABLE.md), Z's answers cost ≈ 37 s each — about half the
   79 s p50 of the deep configuration the record itself recommends as its best
   (F-009) — on a bounty with no latency bar.

**The rerun that settles it.** Execute the already-prepared seed-43 V-para requests
for arm Z(512) (58 generated ids, 51 judged; 102 Opus judge calls per the registry's
own reopen note), pool with seed 42 exactly as F-001 pooled K, and apply the frozen
two-seed verdict. If the pooled CI still straddles zero, R10's "not detected at
MDE 0.06" stands as written. If Δ holds near +0.026 with CI low > 0, the record closed
its largest 4B lever on half the evidence its own criterion required. No new
generation is needed — the prepared requests are referenced in the public arm folder.

*(Same pattern, smaller stakes: DENSECHUNK — §1's family — was parked under a reopen
condition of "≥ 500 pack-matched items", larger than any item set the project ever
built (pack self-tests max out at 180): a direction left permanently undecided at
exactly its observed effect size, +0.017 = the MDE the reopen rule demands.)*

---

## 4. Smaller cross-document items (for completeness)

- **Speed headline quotes only the cool phone.** README/article: "Median answer
  13.9 s, first word 9.8 s, 11.8 tokens/s" = DEVICE-FINAL's **seed-42** M5 row. The
  same report's sustained-use row (after 45 min): **17.0 s / 12.1 s / 8.9 tok/s**; its
  addendum measures decode at 16.7 tok/s cool vs 8.9 hot and instructs: *"heat roughly
  halves decode under sustained use; quote the range."* The headline quotes one end of
  a ~2× thermal range the source report says to quote as a range.
- **The frozen DEVICE-FINAL criterion specified three seeds; the headline pools two.**
  `DEVICE-FINAL-criterion.md` (sha256-frozen 2026-10-25): M1 on "seeds 42, 43, 44",
  reporting spec includes a "three-seed mean (G1)". Seed 44 was dropped for time
  (disclosed in the arm report; the two run seeds agree closely, verdict unaffected) —
  but neither `status.json` nor the article mentions it.
- **The measured binary is not the distributed binary.** Phone numbers were measured
  on build 0ad476ca (bundled measured APK 3,018 MB); the released LabRat 1.0.0
  (F-2246) is APK dcc515fc, 3,041,570,902 bytes, "rebuilt from public pinned sources".
  No diff in the record itemises the 1.0.0 rebuild against the measured build;
  equivalence is asserted by construction, never measured.
- **75 vs 71.** `llms.txt` and article §2 say "75 questions frozen"; the headline says
  "0 of 71 head-to-heads". The reconciliation (71 headline items + 4 anchors) exists
  only inside F-2238's `n` field and the DEVICE-FINAL report — the public text alone
  shows an unexplained 4-item discrepancy at the record's most important number.

---

## 5. Reproduction

Everything above is checkable against the published record:

```python
import json
from collections import Counter
d = json.load(open("boar-research/data/experiments.json"))
rows = d["experiments"] if isinstance(d, dict) else d
by = {r["id"]: r for r in rows}

# §1 — identical judged result on three rows, two of them judgeless
for x in ("X-120", "X-143", "X-144"):
    r = by[x]; print(x, r["judge"], "|", r["result"], "|", r["verdict_detail"][:60])

# §2.2 — the 215 under the registry's own verdict taxonomy
print(Counter(r["verdict"] for r in rows))          # closed 187 + not-detected 28 = 215
print("parity (defined 'not a gain', excluded):",
      sum(r["verdict"] == "parity" for r in rows))  # 10 → 225 by the file's definition

# §2.4 — 'as recorded' results
print("result_verified=false:", sum(r["result_verified"] is False for r in rows),
      "| of which adopted:",
      sum(r["result_verified"] is False and r["verdict"] == "adopted" for r in rows))

# §2.5 — frozen-rule pointers
fr = [r for r in rows if "sha256-frozen" in str((r.get("preregistered") or {}).get("status", ""))]
print("sha256-frozen:", len(fr), "| with public pointer:",
      sum(bool((r.get("preregistered") or {}).get("where_public")) for r in fr))
print("hypothesis null:", sum(r.get("hypothesis") is None for r in rows), "of", len(rows))

# §3 — THINK4B
r = by["X-111"]; print("X-111:", r["result"], "|", r["verdict_detail"])
```

U-total recomputation (§0): parse the four DEVICE-FINAL judgment files from HF
`r4topunk/boar-traces`, apply the floor-adjusted ruler
U = (Σ m_sys − n) / (Σ m_ref − n) pooled across seeds 42+43 per judge family →
Claude 0.165, gpt-5.6-sol 0.242, wins 0/71 both. File hashes match
`boar-research/TRACES.tsv`.

---

## 6. What I am *not* claiming

- The DEVICE-FINAL measurements are fabricated or miscomputed — they reproduce
  exactly; §2.6 of my working notes lists further headline numbers (health gate
  53/65 vs 41/65, pack/delivery rates) that also check out.
- That copying a result string was done in bad faith — staged arms and addenda
  legitimately share numbers elsewhere in the registry. The finding is narrower:
  X-120 and X-143 present, as their own `result`, a judged CI that their own rows say
  they never produced, and no marker in the registry distinguishes that from a real
  measurement.
- That THINK4B *works* — only that the record has not shown it doesn't, by its own
  standard, and that the settling run is prepared and cheap.

**Bottom line.** The final phone numbers in this record are reproducible and, as far
as I can check, honest. The registry that is supposed to make the *process* auditable
is not at the same standard: its census is a filtered subset stated as the whole, its
headline split contradicts its own definitions, one in seven of its results is
flagged unverified by the publication itself, its frozen rules are mostly
uninspectable — and its single most promising un-adopted lever was closed on half the
evidence its own criterion required, with the decisive run sitting prepared in the
public tree. The fix for all of it is equally concrete: correct the X-120/X-143 result
fields, publish the census with its filter and definitions applied consistently, and
run seed 43.
