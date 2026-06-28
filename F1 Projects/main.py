import fastf1
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

# 1. Setup cache
cache_dir = 'cache'
os.makedirs(cache_dir, exist_ok=True)
fastf1.Cache.enable_cache(cache_dir)

# Reduced list for testing, but you can use the full calendar
races = ["Bahrain", "Saudi Arabia", "Australia", "Japan", "China", "Miami", 
         "Monaco", "Canada", "Spain", "Austria", "Great Britain", "Hungary", 
         "Belgium", "Netherlands", "Italy", "Azerbaijan", "Singapore", "USA", 
         "Mexico", "Brazil", "Las Vegas", "Qatar", "Abu Dhabi"]

results_list = []

print("Analyzing Colapinto's vs Gasly's Season...")

for race in races:
    race_data = {
        'Race': race,
        'COL_Gap': np.nan,
        'GAS_Gap': np.nan,
        'COL_Pos': np.nan,
        'GAS_Pos': np.nan
    }
    
    print(f"Fetching data for {race}...")
    
    # --- QUALIFYING DATA ---
    try:
        session_q = fastf1.get_session(2025, race, 'Q')
        session_q.load(telemetry=False, weather=False, messages=False)
        
        # Get pole time safely
        fastest_lap = session_q.laps.pick_fastest()
        if pd.notnull(fastest_lap['LapTime']):
            pole_time = fastest_lap['LapTime'].total_seconds()
            
            # Helper function for Qualy
            def get_q_gap(driver):
                try:
                    driver_laps = session_q.laps.pick_driver(driver)
                    if not driver_laps.empty:
                        d_fastest = driver_laps.pick_fastest()
                        if pd.notnull(d_fastest['LapTime']):
                            time = d_fastest['LapTime'].total_seconds()
                            return ((time / pole_time) - 1) * 100
                except Exception:
                    pass
                return np.nan

            race_data['COL_Gap'] = get_q_gap('COL')
            race_data['GAS_Gap'] = get_q_gap('GAS')
            
    except Exception as e:
        print(f"  -> Could not load Qualifying for {race}: {e}")

    # --- RACE DATA ---
    try:
        session_r = fastf1.get_session(2025, race, 'R')
        session_r.load(telemetry=False, weather=False, messages=False)
        
        # Helper function for Race
        def get_race_pos(driver):
            try:
                # session.results contains the final classification
                res = session_r.results
                driver_res = res.loc[res['Abbreviation'] == driver, 'Position']
                if not driver_res.empty and pd.notnull(driver_res.iloc[0]):
                    return float(driver_res.iloc[0])
            except Exception:
                pass
            return np.nan

        race_data['COL_Pos'] = get_race_pos('COL')
        race_data['GAS_Pos'] = get_race_pos('GAS')
        
    except Exception as e:
        print(f"  -> Could not load Race for {race}: {e}")

    results_list.append(race_data)

# 3. Create DataFrame
df = pd.DataFrame(results_list)
df['Race'] = pd.Categorical(df['Race'], categories=races, ordered=True)
df = df.sort_values('Race')

# 4. Plotting
fig, ax1 = plt.subplots(figsize=(14, 7))

# Primary Axis: Qualy Gap (%)
ax1.set_xlabel('Race', fontweight='bold')
ax1.set_ylabel('Qualy Gap to Pole (%)', color='blue', fontweight='bold')
ax1.plot(df['Race'], df['COL_Gap'], marker='o', label='COL Qualy Gap', color="#2EC9F0", linewidth=2.5)
ax1.plot(df['Race'], df['GAS_Gap'], marker='o', label='GAS Qualy Gap', color='#FF0000', linewidth=2.5)
ax1.tick_params(axis='y', labelcolor='blue')

# Dynamically set y-limits for inverted axis so it doesn't crash on empty arrays
if not df[['COL_Gap', 'GAS_Gap']].isna().all().all():
    max_gap = df[['COL_Gap', 'GAS_Gap']].max().max() + 0.5
    ax1.set_ylim(max_gap, -0.1) # Inverted: Smaller gap (top) is better

# Secondary Axis: Race Finishing Position
ax2 = ax1.twinx()
ax2.set_ylabel('Finishing Position', color='green', fontweight='bold')
ax2.plot(df['Race'], df['COL_Pos'], marker='s', linestyle='--', label='COL Race Pos', color="#1519EE", alpha=0.7)
ax2.plot(df['Race'], df['GAS_Pos'], marker='s', linestyle='--', label='GAS Race Pos', color="#8D1904", alpha=0.7)
ax2.set_yticks(range(1, 21))
ax2.set_ylim(21, 0) # Inverted: 1st place at the top
ax2.tick_params(axis='y', labelcolor='green')

plt.title("2025 Performance: Colapinto vs Gasly", fontsize=16, fontweight='bold')
fig.tight_layout()

# Combine legends from both axes
lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=4)

ax1.tick_params(axis='x', rotation=45)
ax1.grid(True, alpha=0.3)
plt.subplots_adjust(bottom=0.2) # Make room for the x-labels and legend
plt.show()