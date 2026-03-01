import fastf1
import pandas as pd
import matplotlib.pyplot as plt
import os

# Setup cache
cache_dir = 'cache'
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)
fastf1.Cache.enable_cache(cache_dir)

races = ["Bahrain", "Saudi Arabia", "Australia", "Japan", "China", "Miami", "Monaco", "Canada", "Spain", "Austria", "Great Britain", "Hungary", "Belgium", "Netherlands", "Italy", "Azerbaijan", "Singapore", "USA", "Mexico", "Brazil", "Las Vegas", "Qatar", "Abu Dhabi"]

results_list = []

print("Analyzing Colapinto's vs Gasly's Season...")

for race in races:
    try:
        # --- QUALIFYING DATA ---
        session_q = fastf1.get_session(2025, race, 'Q')
        session_q.load(telemetry=False)
        
        pole_time = session_q.laps.pick_fastest()['LapTime'].total_seconds()
        
        def get_q_gap(driver):
            laps = session_q.laps.pick_drivers(driver)
            if not laps.empty:
                time = laps.pick_fastest()['LapTime'].total_seconds()
                return ((time / pole_time) - 1) * 100
            return None

        # --- RACE DATA ---
        session_r = fastf1.get_session(2025, race, 'R')
        session_r.load(telemetry=False)
        
        def get_race_pos(driver):
            try:
                # session.results contains the final classification
                return session_r.results.loc[session_r.results['Abbreviation'] == driver, 'Position'].iloc[0]
            except:
                return None

        # Store all data for this race
        results_list.append({
            'Race': race,
            'COL_Gap': get_q_gap('COL'),
            'GAS_Gap': get_q_gap('GAS'),
            'COL_Pos': get_race_pos('COL'),
            'GAS_Pos': get_race_pos('GAS')
        })
        print(f"Processed {race}")

    except Exception as e:
        print(f"Skipping {race}: {e}")

# 3. Create DataFrame
df = pd.DataFrame(results_list)
df['Race'] = pd.Categorical(df['Race'], categories=races, ordered=True)
df = df.sort_values('Race')

# 6. Plotting with twin axes (Gaps vs Positions)
fig, ax1 = plt.subplots(figsize=(14, 7))

# Primary Axis: Qualy Gap (%)
ax1.set_xlabel('Race')
ax1.set_ylabel('Qualy Gap to Pole (%)', color='blue')
ax1.plot(df['Race'], df['COL_Gap'], marker='o', label='COL Qualy Gap', color="#2EC9F0", linewidth=2)
ax1.plot(df['Race'], df['GAS_Gap'], marker='o', label='GAS Qualy Gap', color='#FF0000', linewidth=2)
ax1.tick_params(axis='y', labelcolor='blue')
ax1.invert_yaxis() # Smaller gap is better

# Secondary Axis: Race Finishing Position
ax2 = ax1.twinx()
ax2.set_ylabel('Finishing Position', color='green')
ax2.plot(df['Race'], df['COL_Pos'], marker='x', linestyle='--', label='COL Race Pos', color="#1519EE", alpha=0.6)
ax2.plot(df['Race'], df['GAS_Pos'], marker='x', linestyle='--', label='GAS Race Pos', color="#8D1904", alpha=0.6)
ax2.set_yticks(range(1, 21))
ax2.invert_yaxis() # 1st place should be at the top
ax2.tick_params(axis='y', labelcolor='green')

plt.title("2025 Performance: Colapinto vs Gasly (Qualy Gap & Race Finish)")
fig.tight_layout()
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.show()

