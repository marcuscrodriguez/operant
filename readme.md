# Behavioral Modification System using Operant Conditioning Mock Up PSYC-3220-U71: Learning

This project implements a digital behavioral modification program grounded in operant conditioning theory. It is tailored to an individual with ADHD, using real-time behavioral logging, preference-based reinforcement, and adaptive consequence delivery.

---

## 🧠 Project Overview

This application simulates a 6-week behavior intervention for improving cleanliness-related behaviors using:
- **Psychometric Profiling** (SPSRQ → RSS/ASQ)
- **Top-5 Reinforcer/Punisher Identification**
- **Weekly Digital Sticker Chart Logging**
- **Two Phase, Continuous, Fixed and Variable Ratio Scheduling**
- **Bliss Point (RDH) and Distress Point (PAH) Visualization**
- **Dynamic Reinforcement Scheduling**

📊 Reinforcement Scheduling Logic
Continuous Reinforcement (Weeks 1-2): Any positive behavior triggers a reward.

Fixed Ratio (Weeks 3-4): 15 behaviors/week must be completed.

Variable Ratio (Weeks 5-6): Threshold varies randomly between 15–30 behaviors.

Threshold met → Reinforcer unlocked (administered manually)
Threshold missed → Punisher administered (if ASQ-based sensitivity)

🧪 Behavioral Theory Integrated
Reinforcer Deprivation Hypothesis (RDH): Restricted access increases reward strength.

Bliss Point and Distress Point models included in visualizations.

📦 Output Files
Ronda_Montelli_sticker_data.csv — Exported top reinforcers or punishers with behavioral relevance

sticker_log.csv — Log of weekly behavior tracking, stored automatically

target_behaviors.csv — Editable file to customize intervention behaviors and goals

✏️ Authors
Marcus C. Rodriguez (Research Design, Implementation)

📚 References
De Houwer & Hughes (2020) – The Psychology of Learning

Timberlake & Allison (1974) – Response Deprivation Theory

Kahneman & Tversky (1979) – Prospect Theory

Torrubia et al. (2001) - SPSRQ

---

## 📁 Project Files

| File | Description |
|------|-------------|
| `behavior_assessment.py` | Collects SPSRQ, RSS/ASQ data, identifies reinforcer/punisher sensitivity, and exports top 5 most effective punishers/reiniforcers to a CSV. |
| `sticker_chart.py` | GUI to log weekly behavior and administer imported csv personalized reinforcers/punishers. |
| `target_behaviors.csv` | Input CSV defining the targeted cleanliness behaviors and desired modified behaviors. |

---

## 🛠️ Requirements

Create a virtual environment and install:

```bash
pip install streamlit pandas numpy matplotlib

