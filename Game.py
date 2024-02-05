import tkinter as tk
from math import *

class LifeGame:
    def __init__(self, n):
        # Première initialisation des paramètres par défaut de la grille
        self.size = n
        self.rows=n
        self.cols=n
        self.cell_size=500/n
        
        # Initialiser la fenêtre principale
        self.root = tk.Tk()
        self.root.title("Jeu de la vie")
        self.root.geometry("1000x600")
        self.root.resizable(width=False, height=False)
        self.root.wm_iconbitmap("icon.ico")
        self.root.configure(bg='pink')
        
        # Initialiser les variables de l'application
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.running = False
        self.days = 0
        self.speed = 1
        self.rules = [[] ,[]]
        self.text = ""
        self.text2 = ""
        self.yes_grid = True
        
        # Créer le canvas
        self.canvas = tk.Canvas(self.root, width=self.cols*self.cell_size, height=self.rows*self.cell_size, bg ='ivory')
        self.canvas.place(x=450, y=50)
        self.scale0 = tk.Canvas(self.root, width=400, height=200,bg ='ivory')
        self.scale0.place(x=35, y=35)
        self.scale1 = tk.Canvas(self.root, width=390, height=90,bg ='ivory')
        self.scale1.place(x=40, y=470)
        self.scale2 = tk.Canvas(self.root, width=180, height=130,bg ='ivory')
        self.scale2.place(x=40, y=320)
        self.scale3 = tk.Canvas(self.root, width=180, height=250,bg ='ivory')
        self.scale3.place(x=250, y=250)
        self.scale4 = tk.Canvas(self.root, width=220, height=60,bg ='ivory')
        self.scale4.place(x=0, y=250)
        
        
        # Créer les widgets
        self.reset_button = tk.Button(self.root, text="Réinitialiser",width = 13, height=2,font=("Comic Sans MS", 15), bg ='ivory', command=self.reset)
        self.reset_button.place(x= 260, y=50)
        self.start_button = tk.Button(self.root, text="Démarrer",width = 13, height=2,font=("Comic Sans MS", 15),bg ='ivory', command=self.start)
        self.start_button.place(x=260, y=155)
        self.next_button = tk.Button(self.root, text="Next",width = 13, height=2,font=("Comic Sans MS", 15),bg ='ivory', command=self.update_grid)
        self.next_button.place(x=50, y=155)
        self.label = tk.Label(self.root, text="Nombre de jours : 0",font=("Comic Sans MS", 9), bg="ivory")
        self.label.place(x=450,y=560)
        self.scale_speed = tk.Scale(self.root, from_=1, to=1000, orient=tk.HORIZONTAL,font=("Comic Sans MS", 9), length=350,bg ='ivory', command=lambda x: set_value_scale_speed(x))
        self.scale_speed.set(50)
        self.scale_speed.place(x=50, y=500)
        self.save_button = tk.Button(self.root, text="Enregistrer",width = 23, height=2,font=("Comic Sans MS", 9),bg ='ivory',  command=lambda: update_text())
        self.save_button.place(x=50, y=50)
        self.open_button = tk.Button(self.root, text="Charger",width = 23,font=("Comic Sans MS", 9),bg ='ivory', command=lambda: update_text2())
        self.open_button.place(x=50, y=96)
        self.yes_grid_button = tk.Button(self.root, text="",width = 4, height=2,font=("Comic Sans MS", 9),bg ='ivory', command=lambda: update_yes_grid())
        self.yes_grid_button.place(x=165, y=330)
        self.label0 = tk.Label(self.root, text="Vitesse d'écoulement des jours :",font=("Comic Sans MS", 9), bg="ivory")
        self.label0.place(x=50,y=480)
        self.label1 = tk.Label(self.root, text="Règles du jeu :",font=("Comic Sans MS", 12), bg="ivory")
        self.label1.place(x=275,y=265)
        self.label2 = tk.Label(self.root, text="Naissance",font=("Comic Sans MS", 9), bg="ivory")
        self.label2.place(x=275,y=300)
        self.label3 = tk.Label(self.root, text="Survie",font=("Comic Sans MS", 9), bg="ivory")
        self.label3.place(x=370,y=300)
        self.label4 = tk.Label(self.root, text="Taille grille",font=("Comic Sans MS", 9), bg="ivory")
        self.label4.place(x=60,y=360)
        self.label5 = tk.Label(self.root, text="Effacer lignes :",font=("Comic Sans MS", 9), bg="ivory")
        self.label5.place(x=60,y=332)
        self.label6 = tk.Label(self.root, text="Jeu de la Vie", font=("Comic Sans MS", 20), bg="ivory")
        self.label6.place(x=40,y=262)
        

        
        # Fonction de saisie de la taille de la grille qui agrandit/baisse la taille de la grille
        def get_input():
            try:
                self.size = int(self.input_field.get())
                old_grid = self.grid.copy()
                self.rows=self.size
                self.cols=self.size
                self.cell_size=500/self.size
                self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
                for i in range(self.cols):
                    for j in range(self.rows):
                        if i<len(old_grid) and j<len(old_grid):
                            self.grid[i][j] = old_grid[i][j]
                self.running = False
                self.days = 0
                self.canvas = tk.Canvas(self.root, width=self.cols*self.cell_size, height=self.rows*self.cell_size, bg ='ivory')
                self.canvas.place(x=450, y=50)
                self.draw_grid()
                self.run()
            except:
                self.output_label.config(text="")
        
        # Créer un champ de saisie pour l'utilisateur
        self.input_field = tk.Entry(self.root)
        self.input_field.insert(0, str(n))
        self.input_field.place(x=60, y=390)
        
        # Créer un bouton pour soumettre l'entrée de l'utilisateur
        self.submit_button = tk.Button(self.root, text="Appliquer",width = 16,bg ='ivory', command=get_input)
        self.submit_button.place(x=60, y=410)
        
        # Fonctions de saisie du titre des fichiers à enregistrer / à charger            
        def update_text():
                self.text = tk.simpledialog.askstring("E", "Nom de l'enregistrement :")
                self.save(self.text)
                
        def update_text2():
                self.text2 = tk.simpledialog.askstring("E", "Nom de l'enregistrement :")
                self.open_saved(self.text2+".txt")
        
        def update_yes_grid():
            if self.yes_grid:
                self.yes_grid = False
            else :
                self.yes_grid = True
            self.draw_grid()
            
        # Créer les 16 Widgets correspondant aux règles du jeu 
        self.check_buttons_survive = []
        for i in range(1,9):
            self.check_button_survive = tk.Checkbutton(self.root, text=f"{i}",bg ='ivory', command=lambda i=i: set_value_button_survive(i))
            self.check_button_survive.place(x=375, y=300+20*i)
            self.check_buttons_survive.append(self.check_button_survive)  
        
        def set_value_button_survive(index):
            if index in self.rules[0]:
                self.rules[0].remove(index)
            else:
                self.rules[0].append(index)
                
        self.check_buttons_born = []
        for i in range(1,9):
            self.check_button_born = tk.Checkbutton(self.root, text=f"{i}",bg ='ivory', command=lambda i=i: set_value_button_born(i))
            self.check_button_born.place(x=275, y=300+20*i)
            self.check_buttons_born.append(self.check_button_born)
        
        def set_value_button_born(index):
            if index in self.rules[1]:
                self.rules[1].remove(index)
            else:
                self.rules[1].append(index)
                
        def set_value_scale_speed(val):
            self.speed = 1000/int(val)
            
        
        # Afficher la grille initiale
        self.draw_grid()
    
    def draw_grid(self):
        # Effacer tous les éléments du canvas
        self.canvas.delete("all")
        

        if self.yes_grid:
            # Dessiner les lignes verticales
            for i in range(self.cols):
                x0 = i * self.cell_size
                y0 = 0
                x1 = i * self.cell_size
                y1 = self.rows * self.cell_size
                self.canvas.create_line(x0, y0, x1, y1)
            
            # Dessiner les lignes horizontales
            for i in range(self.rows):
                x0 = 0
                y0 = i * self.cell_size
                x1 = self.cols * self.cell_size
                y1 = i * self.cell_size
                self.canvas.create_line(x0, y0, x1, y1)
        
        # Dessiner les cellules vivantes
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] == 1:
                    x0 = j * self.cell_size
                    y0 = i * self.cell_size
                    x1 = (j+1) * self.cell_size
                    y1 = (i+1) * self.cell_size
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill="#2F1334")
        
    def reset(self):
        # Réinitialiser la grille
        self.days = 0
        self.label.config(text="Nombre de jours : 0")
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.canvas.delete("all")
        self.draw_grid()
                    
    def on_click(self, event):
        # Modifier l'état de la cellule cliquée
        col = int(event.x // self.cell_size)
        row = int(event.y // self.cell_size)
        self.grid[row][col] = 1 - self.grid[row][col]
        self.draw_grid()
    
    def run(self):
        # Associer l'événement de clic au canvas
        self.canvas.bind("<Button-1>", self.on_click)
        self.root.mainloop()
    
    def start(self):
        # Démarrer ou arrêter le jeu de la vie
        if self.running:
            self.running = False
            self.start_button.config(text="Démarrer")
        else:
            self.running = True
            self.start_button.config(text="Arrêter")
            self.play()
    
    def play(self):
        if not self.running:
            return
        self.update_grid()
        self.draw_grid()
        self.root.after(int(self.speed), self.play)
    
    def update_grid(self):
        # Appliquer les règles du jeu de la vie
        new_grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.cols):
                # Compter le nombre de voisins vivants
                neighbors = self.count_neighbors(i, j)
                if self.grid[i][j] == 1:
                    # Les cellules vivantes doivent avoir 2 ou 3 voisins vivants pour rester en vie
                    if neighbors in self.rules[0]:
                        new_grid[i][j] = 1
                    else:
                        new_grid[i][j] = 0
                else:
                    # Les cellules mortes doivent avoir exactement 3 voisins vivants pour renaître
                    if neighbors in self.rules[1]:
                        new_grid[i][j] = 1
                    else:
                        new_grid[i][j] = 0
        self.days += 1
        self.label.config(text="Nombre de jours : " + str(self.days))
        self.grid[:] = new_grid
        self.draw_grid()
    
    def count_neighbors(self, row, col):
        # Compter le nombre de voisins vivants de la cellule (row, col)
        count = 0
        for i in [-1,0,1]:
            for j in [-1,0,1]:  
                if i == 0 and j == 0:
                    continue
                r = row + i
                c = col + j
                # Prendre en compte les bords de la grille
                if r < 0:
                    r = self.rows - 1
                elif r == self.rows:
                    r = 0
                if c < 0:
                    c = self.cols - 1
                elif c == self.cols:
                    c = 0
                count += self.grid[r][c]
        return count
    
    # Créer un fichier de sauvegarde
    def save(self, file_name):
        grid = self.grid
        ch = ""
        for i in range(self.size):
            for j in range(self.size):
                ch = ch+str(grid[i][j])
        myFile = open(file_name+".txt", "w+")
        myFile.write(ch)
        myFile.close()
    
    # Ouvrir un fichier de sauvegarde
    def open_saved(self, file_name):
        f = open(file_name,'r')
        ch = f.read()
        f.close()
        n0 = sqrt(len(ch))
        if n0 != self.size:
            return None
        grid = [[0 for _ in range(self.size)] for _ in range(self.size)]
        tmp=0
        for i in range(self.size):
            for  j in range(self.size):
                grid[i][j] = int(ch[tmp])
                tmp+=1
        self.grid = grid
        self.draw_grid()        

# Lancer le jeu de la vie avec comme paramètre initial de grille : 20x20    
n=20
game = LifeGame(n)
game.run()