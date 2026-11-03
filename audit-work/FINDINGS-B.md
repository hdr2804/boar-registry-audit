# FINDINGS-B — Internal-consistency audit of the BOAR / RatLab research record (poidh #1520)

**Angle:** experiment-log integrity, cross-document consistency, and the strongest dead end.
Code-bug territory already claimed by other auditors (claim ids 92xx–9310: LabRat router, scorer bar,
grader defects, retrieval bottleneck, decimal lexer, DeviceEvalRunner prefix, FTS upserts, FACT-AVAIL,
HealthGate licensing, etc.) is deliberately **not** re-reported here.

**Material examined (local clones):**
`boar-research/data/{experiments,facts,decisions,timeline,glossary,status}.json`, `boar-research/data/SCHEMA.md`,
`boar-research/{README,CHANGELOG}.md`, `boar-research/rnd/research/coordinator/{CLOSED,BAR-TABLE}.md`,
`boar-research/rnd/research/coordinator/arms/device-final/{DEVICE-FINAL.md,DEVICE-FINAL-criterion.md,aggregates/m1.json}`,
plus the live article (https://r4topunk.github.io/boar-research/) and its `llms.txt`.

**Methods (commands):** `python3` + `json`/`collections`/`re` over the data files (row counts, verdict
tallies, id-gap and duplicate scans, citation-resolution checks, verdict×verified cross-tabs);
`grep -rhoE 'X-[0-9]{3}'` and word-boundary `grep -rn -w` across the repo for dangling references;
direct recomputation of the pooled ruler U-totals from `aggregates/m1.json`; line-level reads of the
arm reports and registries cited below. Every item is tagged **VERIFIED** (counted/recomputed/read by me)
or **INFERRED**.

---

## Lane 1 — Experiment-log integrity

The bounty text (and article §4, and `llms.txt` line 14) claim: **"387 recorded experiments (215 ended
without a gain)"**. What the repo actually documents:

### 1.1 The public counts describe a *filtered* registry, not the research as conducted — VERIFIED (filtering) / the withheld split is UNVERIFIABLE
- `boar-research/data/SCHEMA.md` line 1 (release note, v1.1.2): *"experiments 387 of 402: the 15 rows
  left out cite only internal facts, 13 of them numbers of the app maintainer's app withheld under the
  maintainer-data rule."* `CHANGELOG.md:7` confirms the 15 rows were present in v1.1.1 and removed.
- So the registry of the research as conducted had **402** rows; the article's "387 recorded experiments"
  is the size of the *published subset*, stated without the filtering caveat anywhere in the article or
  `llms.txt`. The 15 withheld rows' verdicts are not public, so the "215 without a gain" split **cannot
  be verified as a property of the research** — only of the filtered publication. If several withheld
  rows were adopted gains (they concern the maintainer's app, i.e. product work), both public numbers
  misstate the record they purport to summarise.

### 1.2 The shipped data contract contradicts itself on every total — VERIFIED
`data/SCHEMA.md` carries two incompatible accounts of the same files:
- Release note (line 1): source rows facts **2,225** / timeline **480** / decisions **215** / experiments
  **402**; public rows **2,138 / 465 / 208 / 387**.
- Its own table (line 16, "rows (2026-10-24 20:34)"): facts **2,191**, decisions **201**, experiments
  **401**, glossary **97**.
- The actual public files: facts **2,138** ✓ (matches note), decisions **208** ✓, timeline **465** ✓,
  experiments **387** ✓, glossary **100** (table says 97).
Four different experiment totals (387 / 401 / 402, plus the table's stale 2,191-fact figure) coexist in
the release's own contract document. The table is labelled a 2026-10-24 snapshot, but it is shipped,
unmarked as superseded, inside the final contract next to the note that supersedes it.

### 1.3 "215 without a gain" reproduces only under an accounting that contradicts the registry's own definitions — VERIFIED
Recount of `data/experiments.json` (387 rows) by its `verdict` field:

| verdict | count | registry's own definition (experiments.json `verdicts`) |
|---|---|---|
| adopted | 57 | "shipped or recommended by its frozen rule" |
| closed | 187 | "rule failed, CI excluded the hoped-for gain…" |
| not-detected | 28 | "CI straddles zero below the test's MDE: **not evidence of no effect**" |
| parity | 10 | "an equivalence…, **not a gain**" |
| measurement | 57 | "no lever verdict" |
| tooling | 32 | "method or infrastructure arm" |
| open | 16 | "parked, running or awaiting a result" |

- 187 + 28 = **215 exactly**. The headline is arithmetically reproducible — as `closed ∪ not-detected`.
- But that accounting breaks the file's own definitions in **both directions**:
  (a) the 10 **parity** rows are defined as *"not a gain"* yet are excluded from the 215 (counting them
  per the definition gives **225**);
  (b) the 28 **not-detected** rows are defined as *"not evidence of no effect"* — the article's own
  verdict table (article §4) glosses them *"too small to see; **not a no**"* — yet the headline sentence
  *"215 of 387 ended without a gain"* folds them into the no-gain total.
- The implied complement is equally misleading: only **57 of 387 (14.7 %)** rows ended *with* an adopted
  gain; **115 rows** (measurement 57 + tooling 32 + open 16 + parity 10) are neither. The article's
  cemetery headline ("215 of 387 ended without a gain, 57 adopted") invites a 215-vs-57 reading that the
  registry's own taxonomy does not support.

### 1.4 Identifier integrity: clean numbering, unexplained holes — VERIFIED
- Registry ids run `X-001…X-406`: **387 unique ids, zero duplicates**. **19 numbers are absent**:
  194–197, 202, 203, 219, 224, 323, 328, 331, 335–337, 367, 378, 395–397.
- Because the 15 withheld rows (item 1.1) were removed **without publishing their ids**, a reader cannot
  tell whether the 19 holes are the withheld rows, deleted rows, or never-assigned numbers. The gap
  structure is therefore unverifiable either way from public data — by construction.
- No dangling references: every `X-NNN` token repo-wide resolves to a registry row (apparent hits
  "X-202"/"X-460" are substrings of `INDEX-2026` and of hex strings, not references). All **482**
  experiment→fact citations resolve in `facts.json` (0 missing). `facts.json` itself: 2,138 rows numbered
  to **F-2252**, with **114 holes**.
- Two registry rows carry no date — **X-192, X-193** (the article admits "2 rows without a date") — and
  they sit immediately before the first hole cluster (194–197).
- **45 registry rows cite no fact at all** (`fact_ids` empty), concentrated in the early range
  (X-004…X-041): registry assertions with no verified fact behind them.

### 1.5 One in seven results is flagged "as recorded", including 30 % of the adopted rows — VERIFIED
`experiments.json`'s own note defines `result_verified = false` as *"not re-verified for this publication;
render it as 'as recorded'"*. Cross-tab (my count): **54 of 387 rows (14 %)** are unverified, including
**17 of the 57 adopted rows** — i.e. 30 % of everything the record says it shipped or recommended rests
on a result the publication itself declines to vouch for — plus 13 of the 187 closed rows. (All 28
not-detected and all 10 parity rows are verified.)

### 1.6 The 387 counts registry rows, not independent runs: identical numbers registered repeatedly — VERIFIED
- **X-120 / X-143 / X-144** (DENSECHUNK family) all carry the *identical* result string
  `+0.017 (−0.000…+0.035)`, although X-120's judged n was **32** in-pack items, X-143 ran **0 judge calls**
  (replay only) and X-144 is the n=180 run. One measurement is registered as three experiments with
  three different verdict narratives (parked / step-0 FAIL / not decided).
- **X-154 / X-155** (STACK / STACK-2) likewise share one result, `+0.005 (−0.009…+0.021)`.
- Candidate screens register **one row per candidate from a single screen table**: X-028 (G4E4B) and
  X-033 (Q35) carry the same screen string `0.437/0.495/0.488/0.457 vs 0.487`; X-076/X-077 (MOESCREEN)
  share one three-model table. Codes also repeat (`SC`, `STACK`, `HONESTPROMPT`, `VALIDATION judge`
  each label 2 rows; 383 distinct codes for 387 rows).
None of this is hidden — the rows cross-reference each other — but "387 experiments" overstates the
number of independent experimental runs by an amount a reader cannot compute from the registry alone.

### 1.7 Temporal seams — VERIFIED (dates)
No registry row is dated before **2026-10-01**, although the record's own timeline starts **2026-09-17**
(`llms.txt` line 13): the first two weeks enter the registry only through the 2026-10-13 ledger
reconstruction (157 rows cite "arm-index v2 (ledger audit 2026-10-13)" as their source). Conversely,
**12 rows are dated after the stated research close of 2026-10-23** (the DEVICE-FINAL/product rows
through 2026-10-25). Both seams are individually disclosed in source fields; neither is visible from
the headline counts.

---

## Lane 2 — Cross-document contradictions

### 2.1 The public speed headline quotes only the cool phone — VERIFIED
- `README.md:10` (and the article): *"Median answer 13.9 s, first word 9.8 s, 11.8 tokens/s, peak
  memory 3.87 GB"* — this is exactly the **seed-42** row of the M5 table in
  `rnd/research/coordinator/arms/device-final/DEVICE-FINAL.md`.
- The same report's seed-43 row, measured after 45 minutes of sustained use: median **17.0 s**, first
  word **12.1 s**, decode **8.9 tok/s**; its addendum measures decode at **16.7 tok/s on a cool phone
  vs 8.9 hot** and instructs *"heat roughly halves decode under sustained use; quote the range."*
- The public headline quotes one end of a ~2× thermal range that the underlying report explicitly says
  to quote as a range. (Cold-start first word in the same report: up to 19.4 s.)

### 2.2 The frozen DEVICE-FINAL criterion specified three seeds; the headline pools two — VERIFIED
- `DEVICE-FINAL-criterion.md` (sha256-frozen 2026-10-25, before generation): M1 on *"seeds 42, 43, 44"*,
  reporting spec includes a *"three-seed mean (G1)"*.
- `DEVICE-FINAL.md` M1 table: seed 44 *"dropped 12:3x (time; 2 seeds = the ruler spec)"*; the published
  headline (article, `llms.txt` line 16, `status.json` banner) pools seeds 42+43 only.
- The drop **is** disclosed in the arm report, and the two run seeds agree closely (0.167/0.162 Claude),
  so the verdict is unaffected — but the frozen criterion's own reporting spec was not met, and neither
  `status.json` nor the article mentions the dropped seed.

### 2.3 A CONFIRMED headline fact carries a caveat that its own record falsifies — VERIFIED
`data/facts.json` **F-2227** (the DEVICE-FINAL criterion fact, verification = CONFIRMED) still carries
the caveat: *"No DEVICE-FINAL result is in this record; the matrix was running as of this update."*
In the final record, F-2238/F-2239/F-2241 publish exactly those results. A stale pre-run caveat survives
in the very fact a reader is sent to for the headline's provenance.

### 2.4 The measured binary is not the distributed binary — VERIFIED facts, INFERRED weight
- Phone numbers were measured on builds 7788924a / 0ad476ca; the bundled measured APK is identified in
  `DEVICE-FINAL.md`'s addendum as `LabRat-0ad476ca-51a4aa4d` (bundle 3,018 MB).
- The public release, **F-2246**, is a different binary: *"LabRat 1.0.0 released: APK dcc515fc,
  3,041,570,902 bytes, sha256 d2e00ba4…"*, described as rebuilt from public pinned sources. A third size
  (3,044,169,517 B) appears for the b4ef94f3 candidate in **F-2210**.
- The 0ad476ca↔7788924a diff is documented (brand files only); no diff in the record itemises the 1.0.0
  rebuild against the measured build. Equivalence of the shipped APK with the measured one is asserted
  by construction, never measured. (The article's "one 3 GB APK" glosses over all three figures.)

### 2.5 Minor: the 75-vs-71 ruler size is reconciled only inside a fact row — VERIFIED
`llms.txt` line 16 describes bench v0.4 as *"75 items…"* in one sentence and the headline as *"0 of 71
head-to-heads"* in the next; the article §2 likewise says *"75 questions frozen"* while the abstract
says *"won 0 of 71 questions"*. The reconciliation (71 headline items + 4 anchors) exists only inside
F-2238's `n` field and the DEVICE-FINAL report — a reader of the public text alone meets an unexplained
4-item discrepancy at the record's most important number.

### 2.6 What checks out (for the record) — VERIFIED by recomputation
- Headline U-totals recompute from `aggregates/m1.json`: pooled G1 Claude **0.16454 → 0.165**, pooled
  G2 gpt-5.6-sol **0.24245 → 0.242**, win_rate **0.0** under both families; the single gpt tie
  (s42 win_tie_rate 0.00704 = ½ item) matches DEVICE-FINAL's pooled "0 / 0.5". Paired phone-vs-desktop
  deltas (+0.003 / −0.007) match F-2239.
- Old-scale headlines match their aggregate table: F-001 (raw 0.413, floor-adj 0.261, 0/0/51) and F-009
  (0.553 / 0.436) equal `BAR-TABLE.md` lines 35 and 39. The two known print discrepancies (CI high
  0.300 vs a claim draft's 0.299; QUEUE's raw 0.552 vs the aggregate's 0.553) are self-documented in
  the F-001/F-009 caveats.
- Health gate 53/65 (phone) and 41/65 (desktop) match F-2241 / F-2210 and the DEVICE-FINAL M2 section;
  pack numbers 48 % vs 26 %, 65 % vs 28 %, delivery 54 % match F-1704 / F-1705 / F-1706, including
  their self-test caveats.

---

## Lane 3 — The strongest dead end: THINK4B (thinking budget on the 4B claim build)

**The approach.** Swap the frozen 4B claim build (Qwen3-4B-Instruct, build K) for its thinking sibling
(Qwen3-4B-Thinking-2507) at a 512-token thinking budget (arm Z) — registry row **X-111**, closed-registry
row **R10** (`rnd/research/coordinator/CLOSED.md:25`, arm report `arms/think4b/THINK4B.md`).

**What the record's own numbers say.**
- Result on V-para (the record's bounty-style set, the same set the claim build's headline stands on):
  raw **0.439 vs K's 0.413, Δ +0.026 (CI −0.013…+0.068)**, win 0/51, ×3.7 time (X-111; CLOSED.md:25).
  This is the largest positive point estimate of any non-adopted 4B-side lever in the registry.
- Mechanism plausibility is established *inside the same record*: thinking budget is the one lever
  shown to move this metric family — on the deep tier, budget 0→512 lifts floor-adjusted
  0.329 → 0.436 (article §4 table; F-009). THINK4B is the only same-scale test of that mechanism on
  the configuration that actually carried the bounty claim.

**Why the negative verdict rests on the weakest evidence in the log.**
1. **The verdict deviates from the record's own frozen standard — and the registry says so.** X-111's
   `verdict_detail`: *"closed: NO (near-lever), stopped after seed 42 (**one seed, not the two-seed
   verdict the criterion specifies**)"*. Every claim-build verdict on V-para in the record (F-001's K
   numbers included) is a two-seed verdict; THINK4B was closed on one.
2. **The settling run was prepared, priced, and never executed.** X-111's `seeds` field: *"s42 only
   (s43 requests prepared, not run)"*; its `reopen_if`: *"BACKLOG s3: V-para s43 (Opus 102)"* — the
   decisive second seed existed as prepared requests costed at 102 judge calls. It was parked behind
   the condition *"only if the 4B side reopens"* (CLOSED.md:25), a condition the project's own pivot
   to the 1.7B engine made unreachable — while the non-thinking 4B's score remained the published
   old-scale headline (F-001).
3. **The closure standard was applied asymmetrically.** Levers were *adopted* on weaker evidence than
   THINK4B was closed on: **X-182 (LITEREACH2-180) adopted at +0.005 (CI −0.014…+0.025)**; **SEFIX-124
   adopted "for delivery" at +0.013** (status.json changelog, 2026-10-22). THINK4B's point estimate is
   2× the latter and 5× the former, and its CI upper bound (+0.068) exceeds the very MDE (0.06) cited
   to close it — the test as run could not distinguish "no effect" from an effect larger than several
   adopted gains.
4. **The counter-evidence is narrower than the closure implies.** LITE-THINK (X-188; CLOSED R97,
   CLOSED.md:125) found thinking flat/negative on the **1.7B** — a different model, on a 20-item
   self-test, Haiku-judged, at MDE ≈ 0.08 by the record's own critique. THINK4B-V02 (X-112) read
   +0.009 on v0.2 at Haiku L1 (MDE 0.025, "Haiku compresses") — a screen, not the V-para Opus verdict.
   Neither is a two-seed Opus test of thinking on the 4B/V-para combination; only the un-run seed 43
   would have been.
5. **The honest objection — ×3.7 time — does not close the case.** At the 4B claim-run pace (K p50
   10.1 s, `BAR-TABLE.md:35`) Z's answers cost ≈ 37 s each: about half the 79 s p50 of the deep
   configuration the record itself recommends as its best (F-009), on a bounty with no latency bar.

**The rerun that settles it.** Execute the already-prepared seed-43 V-para requests for THINK4B Z(512)
(58 generated ids, 51 judged; **102 Opus judge calls** per the registry's own reopen note), pool with
seed 42 exactly as F-001 pooled K, and apply the frozen two-seed verdict. If the pooled CI still
straddles zero, R10's "not detected at MDE 0.06" stands as written; if Δ holds near +0.026 with CI
low > 0, the record closed its largest 4B lever on half the evidence its own criterion required.
No new generation is needed if the prepared s43 requests survive in `arms/think4b/` (the arm folder is
in the public tree).

**Runner-up (same pattern, smaller stakes).** DENSECHUNK (X-120/X-143/X-144, Lane 1.6): parked with a
reopen condition of *"≥ 500 pack-matched items (n for MDE 0.017)"* — larger than any item set the
project ever built (the pack self-tests max out at 180) — i.e. a direction left permanently undecided
at exactly its observed effect size (+0.017 = the MDE the reopen rule demands), under a condition that
cannot be met from within the record.

---

## Strongest finding overall

**THINK4B (Lane 3).** The "215 of 387" accounting (Lane 1.3) is the cleanest presentational hit, but
THINK4B is the finding with consequences: the record's flagship configuration decision — *which 4B
build represents this project* — was left formally undecided by the record's own frozen two-seed
standard, with the decisive run prepared, priced at 102 judge calls, and abandoned behind a reopen
condition the project's own pivot made unreachable. It is documented in the registry's own words
("not the two-seed verdict the criterion specifies"), it is asymmetric against levers adopted on
one-fifth the effect size, and it is cheaply settleable. A research record whose central claim is
procedural rigour ("a pass/fail rule frozen before the run", `llms.txt` line 14) is most damaged by
the one place it closed its most promising same-scale lever without running its own rule.
