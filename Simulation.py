import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.colors as mcolors
from matplotlib.patches import Patch
import numpy as np

from main import *

class SimulationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Meilleur projet d'ARE au monde")

        self.civilisation = []
        self.ressources_memoire = {}
        self.running = False
        self.mode = "role"
        self.jour = 0

        self.historique_eau = []
        self.historique_agri = []
        self.historique_soldats = []
        self.historique_medecins = []

        # ---------------- LAYOUT PRINCIPAL ----------------
        main_frame = ttk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # ---------------- PANEL CONTROLE ----------------
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(side=tk.TOP, fill=tk.X, pady=5)

        ttk.Button(control_frame, text="Initialiser Schelling", command=self.init_sim_schelling).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Initialiser Optimisé", command=self.init_sim_optimise).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Étape", command=self.step).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Play", command=self.start_simulation).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Stop", command=self.stop_simulation).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Mode Role", command=lambda: self.set_mode("role")).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Mode Groupe", command=lambda: self.set_mode("groupe")).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Reset", command=self.reset_simulation).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Kill", command=self.kill_tkinter).pack(side=tk.LEFT, padx=5)

        self.speed = tk.Scale(control_frame, from_=100, to=3000, orient="horizontal", label="Vitesse (ms)")
        self.speed.set(1000)
        self.speed.pack(side=tk.RIGHT, padx=10)

        self.label_jour = ttk.Label(control_frame, text=f"Jour : {self.jour}")
        self.label_jour.pack(side=tk.RIGHT, padx=10)

        # ---------------- PANEL CENTRAL ----------------
        center_frame = ttk.Frame(main_frame)
        center_frame.pack(fill=tk.BOTH, expand=True)

        # Grille simulation à gauche
        left_frame = ttk.Frame(center_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Graphiques + texte à droite
        right_frame = ttk.Frame(center_frame)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Grille Matplotlib
        self.fig_grid, self.ax_grid = plt.subplots(figsize=(6,6))
        self.canvas_grid = FigureCanvasTkAgg(self.fig_grid, master=left_frame)
        self.canvas_grid.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Graphique ressources
        self.fig_ressources, (self.ax_ressources, self.ax_roles) = plt.subplots(2, 1, figsize=(6,6))
        self.canvas_ressources = FigureCanvasTkAgg(self.fig_ressources, master=right_frame)
        self.canvas_ressources.get_tk_widget().pack(fill=tk.BOTH, expand=True, pady=5)

        # Texte groupes
        self.text = tk.Text(right_frame, height=15)
        self.text.pack(fill=tk.BOTH, expand=True, pady=5)

    def kill_tkinter(self):
        self.running = False
        self.root.destroy()

    # ---------------- INIT ----------------
    def init_sim_schelling(self):
        self._init_base()
        segregation(self.civilisation)
        deplacer_individus(self.civilisation)
        k_means(self.civilisation)
        assign_role_to_reste(self.civilisation)
        self.draw()
        self.update_graph()

    def init_sim_optimise(self):
        self._init_base()
        groupement(self.civilisation)
        assign_role_to_reste(self.civilisation)
        self.draw()
        self.update_graph()

    def _init_base(self):
        self.civilisation = Generation_personnes(160)
        self.ressources_memoire = {}
        self.historique_eau.clear()
        self.historique_agri.clear()
        self.historique_soldats.clear()
        self.historique_medecins.clear()
        self.jour = 0
        self.label_jour.config(text=f"Jour : {self.jour}")
        self.text.delete("1.0", tk.END)
        self.ax_grid.clear()
        self.canvas_grid.draw()
        self.ax_ressources.clear()
        self.ax_roles.clear()
        self.canvas_ressources.draw()
        self.running = False

    # ---------------- STEP ----------------
    def step(self):
        if not self.civilisation:
            return

        assign_role_to_reste(self.civilisation)
        groupes = update_ressources(self.civilisation, self.ressources_memoire)
        
        assign_role_to_reste(self.civilisation)
        groupes = update_ressources(self.civilisation, self.ressources_memoire)

        if self.jour % 5 == 0 :
            attack_zombie(self.civilisation)
            update_state_groupe(self.civilisation, self.ressources_memoire)

        if est_premier(self.jour):
            melange_groupes(self.civilisation)


        # Historique
        total_eau = sum(self.ressources_memoire[g[ID_GROUPE]]["Eau"] for g in groupes)
        total_agri = sum(self.ressources_memoire[g[ID_GROUPE]]["Agriculture"] for g in groupes)
        nb_soldats = sum(len(g[LISTE_IND])*g[CAPACITES]["Soldat"] for g in groupes)
        nb_medecins = sum(len(g[LISTE_IND])*g[CAPACITES]["Medecin"] for g in groupes)

        self.historique_eau.append(total_eau)
        self.historique_agri.append(total_agri)
        self.historique_soldats.append(nb_soldats)
        self.historique_medecins.append(nb_medecins)

        self.jour += 1
        self.label_jour.config(text=f"Jour : {self.jour}")

        self.update_text(groupes)
        self.draw()
        self.update_graph()

    # ---------------- AUTO ----------------
    def start_simulation(self):
        if not self.running:
            self.running = True
            self.run_loop()

    def stop_simulation(self):
        self.running = False

    def run_loop(self):
        if self.running:
            self.step()
            self.root.after(self.speed.get(), self.run_loop)

    # ---------------- MODE ----------------
    def set_mode(self, mode):
        self.mode = mode
        self.draw()

    # ---------------- DRAW ----------------
    def draw(self):
        self.ax_grid.clear()
        grid = np.full((LONGUEUR, LARGEUR), -1)

        if self.mode == "role":
            role_map = {"Soldat":0,"Medecin":1,"Agriculteur":2,"Eau":3,"Reste":4}
            color_map = ["#f5f5dc","red","blue","green","cyan","grey"]
            role_labels = ["Fond","Soldat","Médecin","Agriculteur","Eau","Reste"]

            for p in self.civilisation:
                x, y = p[COORD]
                grid[y][x] = role_map.get(p[ROLE], -1)

            self.ax_grid.imshow(grid + 1, cmap=mcolors.ListedColormap(color_map), vmin=0, vmax=5)
            self.ax_grid.set_title("Mode : Rôles")

            # Ajouter la légende directement sur le graphique
            legend_elements = [Patch(facecolor=color_map[i], label=role_labels[i]) for i in range(len(role_labels))]
            self.ax_grid.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.15, 1))
        else:
            for p in self.civilisation:
                x, y = p[COORD]
                grid[y][x] = p[IS_IN_GROUPE]
            self.ax_grid.imshow(grid)
            self.ax_grid.set_title("Mode : Groupes")

        self.canvas_grid.draw()

    # ---------------- TEXTE ----------------
    def update_text(self, groupes):
        self.text.delete("1.0", tk.END)
        for g in groupes:
            gid = g[ID_GROUPE]
            res = self.ressources_memoire.get(gid, {})
            self.text.insert(tk.END, f"Groupe {gid}\n")
            self.text.insert(tk.END, f"  Taille : {len(g[LISTE_IND])}\n")
            self.text.insert(tk.END, f"  Eau : {res.get('Eau',0)}\n")
            self.text.insert(tk.END, f"  Agriculture : {res.get('Agriculture',0)}\n")
            self.text.insert(tk.END, "-"*30 + "\n")

    # ---------------- GRAPHIQUE ----------------
    def update_graph(self):
        jours = list(range(1, self.jour+1))

        # Graphique Eau / Agriculture
        self.ax_ressources.clear()
        self.ax_ressources.plot(jours, self.historique_eau, label="Eau", color="blue")
        self.ax_ressources.plot(jours, self.historique_agri, label="Agriculture", color="green")
        self.ax_ressources.set_xlabel("Jour")
        self.ax_ressources.set_ylabel("Quantité")
        self.ax_ressources.set_title("Historique des ressources")
        self.ax_ressources.legend()

        # Graphique Soldats / Médecins
        self.ax_roles.clear()
        self.ax_roles.plot(jours, self.historique_soldats, label="Soldats", color="red")
        self.ax_roles.plot(jours, self.historique_medecins, label="Médecins", color="blue")
        self.ax_roles.set_xlabel("Jour")
        self.ax_roles.set_ylabel("Nombre")
        self.ax_roles.set_title("Historique rôles")
        self.ax_roles.legend()

        self.canvas_ressources.draw()

    # ---------------- RESET ----------------
    def reset_simulation(self):
        self.running = False
        self._init_base()

# ---------------- LANCEMENT ----------------
root = tk.Tk()
root.geometry("1600x900")
root.state("zoomed")
app = SimulationApp(root)
root.mainloop()
