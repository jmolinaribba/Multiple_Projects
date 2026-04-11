import matplotlib.pyplot as plt
import fastf1
import fastf1.plotting

# Configuración de FastF1
fastf1.plotting.setup_mpl(mpl_timedelta_support=False, color_scheme='fastf1')

# 1. Cargar sesión y procesar datos
race = fastf1.get_session(2023, 1, 'R')
race.load()
laps = race.laps.pick_quicklaps()

transformed_laps = laps.copy()
transformed_laps.loc[:, "LapTime (s)"] = laps["LapTime"].dt.total_seconds()

# 2. Ordenar equipos por mediana
team_order = (
    transformed_laps[["Team", "LapTime (s)"]]
    .groupby("Team")
    .median()["LapTime (s)"]
    .sort_values()
    .index
)

# 3. Preparar los datos para Matplotlib
# Necesitamos una lista de listas (una lista de tiempos por cada equipo)
data_to_plot = [transformed_laps[transformed_laps["Team"] == team]["LapTime (s)"] for team in team_order]

fig, ax = plt.subplots(figsize=(15, 10))

# 4. Crear el boxplot
# patch_artist=True es necesario para poder colorear el interior de las cajas
bplot = ax.boxplot(data_to_plot, 
                   labels=team_order,
                   patch_artist=True,
                   whiskerprops=dict(color="white"),
                   capprops=dict(color="white"),
                   medianprops=dict(color="silver", linewidth=2),
                   flierprops=dict(markeredgecolor="white"))

# 5. Aplicar los colores de los equipos manualmente
for patch, team in zip(bplot['boxes'], team_order):
    color = fastf1.plotting.get_team_color(team, session=race)
    patch.set_facecolor(color)
    patch.set_edgecolor("white")

# Estética final
ax.set_title("2023 First Grand Prix - Team Pace Comparison")
ax.set_ylabel("Lap Time (s)")
plt.xticks(rotation=45) # Rotar nombres si son muy largos
plt.grid(axis='y', linestyle='--', alpha=0.3)
plt.tight_layout()

plt.show()


