# CAST Week 1 Capstone — Spot Patrol Data Analyzer (Starter)

DSU CAST Autonomous Research Program · Summer 2026 · Director: Tariq Hook

This is your **starter repo** for the Week 1 capstone. It contains the mission
data and the project documents. Your job is to add `analyzer.py` and a generated
`mission_report.txt`, then push everything to your own repo and demo it live.

> Spot just completed three patrol laps around the CAST building. Its sensors
> recorded **792 readings across 11 waypoints**. Nobody has looked at the data
> yet. You are building the tool that reads the log, finds what went wrong, and
> writes the report — the exact workflow you'll use with the real robot in Week 2.

---

## Repo structure

```
cast-capstone-starter/
├── README.md                     ← you are here
├── data/
│   └── spot_patrol_data.csv      ← the mission log (792 rows, 8 columns)
└── docs/
    ├── CAST_Week1_Capstone_Brief.docx       ← the full assignment + grading
    └── CAST_Week1_Intern_Task_Guide_v6.docx ← Week 1 setup, tools, video index
```

**Read `docs/CAST_Week1_Capstone_Brief.docx` first.** It is the source of truth
for what you're graded on. This README is just the map.

---

## The data — `data/spot_patrol_data.csv`

8 columns: `timestamp, lap, waypoint, reading_num, sensor_id, value, unit, status`

| Sensor | Meaning | Normal range |
|---|---|---|
| `temp_body` | Body temperature (°C) | 28–38 |
| `temp_motor_FL/FR/RL/RR` | Leg motor temps (°C) | 30–55 |
| `battery_pct` | Battery charge (%) | fault below 15 |
| `proximity_cm` | Distance to nearest object (cm) | fault below 10 |
| `velocity_ms` | Movement speed (m/s) | 0–1.6 |

**Something went wrong on this mission.** Don't assume all 792 rows say `OK` —
there are exactly **13 faults** to find. If your script finds a different number,
check your loading logic.

---

## Your task — build `analyzer.py`

One Python script, five tasks, run in order:

1. **Load the data** — read the CSV with the built-in `csv` module into a list of dicts. Print the row count.
2. **Mission summary** — count laps, unique waypoints, total readings, unique sensor types (from the data, not hardcoded).
3. **Find all faults** — every row where `status != OK`. Print each, then the total (you should get 13).
4. **Per-sensor averages** — average `value` per `sensor_id`, sorted high → low, rounded to 2 decimals.
5. **Write the report** — dump all of the above to `mission_report.txt` with section headers and a generated-at timestamp.

Requirements: all logic in functions, file I/O wrapped in `try/except`, output
goes to both the terminal **and** the report file, and the script must be
triggerable over SSH with a single command.

---

## Getting started

```bash
# 1. Launch the container (port-forward 2222→22, share a workspace volume)
docker run -it -p 2222:22 -v ~/cast-work:/workspace ubuntu:22.04 /bin/bash

# 2. Inside the container, install dependencies
apt-get update && apt-get install -y python3 python3-pip openssh-server curl wget

# 3. Start + configure SSH (see the Intern Task Guide, Step 3)
mkdir -p /run/sshd
echo 'PermitRootLogin yes' >> /etc/ssh/sshd_config
passwd root
service ssh start

# 4. Put the data where your script expects it
cp data/spot_patrol_data.csv /workspace/spot_patrol_data.csv
```

Run it inside the container:

```bash
python3 /workspace/analyzer.py
```

Trigger it over SSH from your **host** machine (this must work — it's graded):

```bash
ssh root@localhost -p 2222 'python3 /workspace/analyzer.py'
```

> Keep the container running. Typing `exit` stops it and SSH will refuse the
> connection — open a second terminal for the SSH trigger, or detach with
> `Ctrl-P` then `Ctrl-Q`.

---

## How to submit

1. Create a repo named `cast-capstone-[yourname]`.
2. Push `analyzer.py` and `mission_report.txt`.
3. Rewrite this README for your own repo — it must say **what the script does**,
   **how to run it over SSH**, and **what faults it found**.
4. Post the repo link in Teams by the deadline below.

### Key dates

| Milestone | When |
|---|---|
| Assigned | Monday June 22 |
| Push to GitHub + post link in Teams | **5 PM Friday June 27** |
| Demo Day (5 min each, terminal only — no slides) | Monday June 29, 10 AM |

At your demo, Tariq will ask: *"If this was a real Spot robot instead of a CSV
file, what would you change in your code to make this work?"* Think about it
before Demo Day — you don't need the Spot SDK to answer, just an understanding of
where your data comes from.
