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
        self.groupes_actuels = []
        self.ressources_memoire = {}
        self.running = False
        self.mode = "role"
        self.jour = 0

        self.historique_eau = []
        self.historique_agri = []
        self.historique_soldats = []
        self.historique_medecins = []
        self.historique_agriculteurs = []
        self.historique_eaux = []

        self.group_colors = {}
        self.cmap = plt.get_cmap('tab20b')  

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

        self.speed = tk.Scale(control_frame, from_=10, to=3000, orient="horizontal", label="Vitesse (ms)")
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
        self.canvas_grid.mpl_connect("button_press_event", self.on_click)

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

    def get_group_color(self, gid):
        if gid not in self.group_colors:
            index = len(self.group_colors)
            self.group_colors[gid] = self.cmap(index % self.cmap.N)
        return self.group_colors[gid]
    
    def on_click(self, event):
        if event.xdata is None or event.ydata is None:
            return

        x = int(event.xdata)
        y = int(event.ydata)

        for p in self.civilisation:
            px, py = p[COORD]
            if px == x and py == y:
                gid = p[IS_IN_GROUPE]
                self.display_group_info(gid)
                return
            
    def display_group_info(self, gid):
        self.text.delete("1.0", tk.END)

        groupes = self.groupes_actuels

        groupe = next((g for g in groupes if g[ID_GROUPE] == gid), None)

        if not groupe:
            self.text.insert(tk.END, f"Groupe {gid} introuvable\n")
            return

        individus_ids = set(groupe[LISTE_IND])

        personnes = [
            p for p in self.civilisation
            if p[ID] in individus_ids
        ]

        res = self.ressources_memoire.get(gid, {})

        roles_count = {
            "Soldat": 0,
            "Medecin": 0,
            "Agriculteur": 0,
            "Eau": 0,
            "Reste": 0
        }

        for p in personnes:
            role = p[ROLE]
            if role in roles_count:
                roles_count[role] += 1
            else:
                roles_count["Reste"] += 1

        # ---------------- AFFICHAGE ----------------
        self.text.insert(tk.END, f"=== GROUPE {gid} ===\n\n")
        self.text.insert(tk.END, f"Taille : {len(personnes)}\n\n")

        self.text.insert(tk.END, "Ressources :\n")
        self.text.insert(tk.END, f"  Eau : {res.get('Eau', 0)}\n")
        self.text.insert(tk.END, f"  Agriculture : {res.get('Agriculture', 0)}\n\n")

        self.text.insert(tk.END, "Rôles :\n")
        for role, count in roles_count.items():
            self.text.insert(tk.END, f"  {role} : {count}\n")

        self.text.insert(tk.END, "\nIndividus (aperçu) :\n")
        for p in personnes:
            self.text.insert(tk.END, f"  - {p[ROLE]}\n")

    # ---------------- INIT ----------------
    def init_sim_schelling(self):
        self._init_base()
        segregation(self.civilisation)
        deplacer_individus(self.civilisation)
        k_means(self.civilisation)
        assign_role_to_reste(self.civilisation)
        groupes = update_ressources(self.civilisation, self.ressources_memoire)
        self.groupes_actuels = groupes
        self.draw()
        self.update_graph()
        

    def init_sim_optimise(self):
        self._init_base()
        groupement(self.civilisation)
        assign_role_to_reste(self.civilisation)
        groupes = update_ressources(self.civilisation, self.ressources_memoire)
        self.groupes_actuels = groupes
        self.draw()
        self.update_graph()

    def _init_base(self):
        self.civilisation = Generation_personnes(160)
        self.ressources_memoire = {}
        self.groupes_actuels = None
        self.historique_eau.clear()
        self.historique_agri.clear()
        self.historique_soldats.clear()
        self.historique_medecins.clear()
        self.historique_agriculteurs.clear()
        self.historique_eaux.clear()
        self.jour = 0
        self.label_jour.config(text=f"Jour : {self.jour}")
        self.text.delete("1.0", tk.END)
        self.ax_grid.clear()
        self.canvas_grid.draw()
        self.group_colors.clear()
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
        self.groupes_actuels = groupes

        if self.jour % 5 == 0 :
            attack_zombie(self.civilisation)
            update_state_groupe(self.civilisation, self.ressources_memoire)

        if est_premier(self.jour):
            melange_groupes(self.civilisation)


        # Historique
        total_eau = sum(self.ressources_memoire[g[ID_GROUPE]]["Eau"] for g in groupes)
        total_agri = sum(self.ressources_memoire[g[ID_GROUPE]]["Agriculture"] for g in groupes)

        nb_soldats = sum(1 for p in self.civilisation if p[ROLE] == "Soldat")
        nb_medecins = sum(1 for p in self.civilisation if p[ROLE] == "Medecin")
        nb_agriculteurs = sum(1 for p in self.civilisation if p[ROLE] == "Agriculteur")
        nb_eau = sum(1 for p in self.civilisation if p[ROLE] == "Eau")
        self.historique_eau.append(total_eau)
        self.historique_agri.append(total_agri)

        self.historique_soldats.append(nb_soldats)
        self.historique_medecins.append(nb_medecins)
        self.historique_agriculteurs.append(nb_agriculteurs)
        self.historique_eaux.append(nb_eau)
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
            grid_rgb = np.zeros((LONGUEUR, LARGEUR, 3))

            for p in self.civilisation:
                x, y = p[COORD]
                gid = p[IS_IN_GROUPE]

                if 0 <= x < LARGEUR and 0 <= y < LONGUEUR:
                    color = self.get_group_color(gid)
                    grid_rgb[y][x] = color[:3]

            self.ax_grid.imshow(grid_rgb)
            self.ax_grid.set_title("Mode : Groupes")

        self.canvas_grid.draw()

    # ---------------- TEXTE ----------------
    def update_text(self, groupes):
        self.text.delete("1.0", tk.END)

        groupes_tries = sorted(groupes, key=lambda g: g[ID_GROUPE])

        for g in groupes_tries:
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
        self.ax_ressources.plot(jours, self.historique_eau, label="Eau", color="cyan")
        self.ax_ressources.plot(jours, self.historique_agri, label="Agriculture", color="green")
        self.ax_ressources.set_xlabel("Jour")
        self.ax_ressources.set_ylabel("Quantité")
        self.ax_ressources.set_title("Historique des ressources")
        self.ax_ressources.legend()

        # Graphique Soldats / Médecins
        self.ax_roles.clear()
        self.ax_roles.plot(jours, self.historique_soldats, label="Soldats", color="red")
        self.ax_roles.plot(jours, self.historique_medecins, label="Médecins", color="blue")
        self.ax_roles.plot(jours, self.historique_agriculteurs, label="Agriculteurs", color="green")
        self.ax_roles.plot(jours, self.historique_eaux, label="Eau", color="cyan")
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
