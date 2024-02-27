import mysql.connector
from mysql.connector import Error
import json
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
import os

try:
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='db_est'
    )

    if connection.is_connected():
        cursor = connection.cursor()

        def fetch_course_data(course_name):
            cursor.execute("""
                SELECT etudient.nom, examen.note
                FROM etudient, examen, cours
                WHERE etudient.id=examen.id
                AND examen.code=cours.code
                AND cours.nom_de_cours=%s;
            """, (course_name,))
            rows = cursor.fetchall()
            names = [row[0] for row in rows]
            notes = [row[1] for row in rows]
            return names, notes

        # prend en paramètre
        names_python, notes_python = fetch_course_data('python')
        names_web, notes_web = fetch_course_data('web')
        names_database, notes_database = fetch_course_data('DATAbase')

except Error as e:
    print("Error while connecting to MySQL or retrieving data", e)
finally:
    if connection and connection.is_connected():
        cursor.close()
        connection.close()
        print("\nMySQL connection is closed")

colors = sns.color_palette('pastel')
plt.rcParams["axes.prop_cycle"] = plt.cycler(color=colors)
root = tk.Tk()
root.title("VisualData Analytique")
root.state('zoomed')
icon_path = r""#ajouter le chemen de icone 
icon = tk.PhotoImage(file=icon_path)
root.iconphoto(True, icon)
side_frame = tk.Frame(root, bg="#030505")
side_frame.pack(side="left", fill="y")

label = tk.Label(side_frame, text=" Cours" , bg="#030505", fg="#FFF", font=("Helvetica", 20))
label.pack(pady=50, padx=20)

charts_frame = tk.Frame(root)
charts_frame.pack()

upper_frame = tk.Frame(charts_frame)
upper_frame.pack(fill="both", expand=True)

lower_frame = tk.Frame(charts_frame)
lower_frame.pack(fill="both", expand=True)

def plot_course_data(names, notes):
    ax1.clear()
    ax2.clear()
    ax3.clear()

    ax1.bar(names, notes, color=colors[0])
    ax1.set_title('Notes de cours')
    ax1.set_xlabel('Noms des étudiants')
    ax1.set_ylabel('Notes')

    ax2.plot(names, notes, marker='o', color=colors[1], linestyle='-')
    ax2.set_title('La présence')
    ax2.set_xlabel('Noms des étudiants')
    ax2.set_ylabel('Les séance')
    ax2.grid(True, linestyle='--', alpha=0.7)

    ax3.pie(notes, labels=names, autopct='%1.1f%%', startangle=90, colors=colors)
    ax3.set_title('Participation ')

    canvas1.draw()
    canvas2.draw()
    canvas3.draw()

# Plotting for Python Course Notes
fig1, ax1 = plt.subplots(figsize=(6, 4))
canvas1 = FigureCanvasTkAgg(fig1, upper_frame)
canvas1.get_tk_widget().pack(side="left", fill="both", expand=True)

# Plotting for Web Course Notes
fig2, ax2 = plt.subplots(figsize=(8, 6))
canvas2 = FigureCanvasTkAgg(fig2, lower_frame)
canvas2.get_tk_widget().pack(side="bottom", fill="both", expand=True)

# Plotting for Base de Données (Pie chart)
fig3, ax3 = plt.subplots(figsize=(5, 5))
canvas3 = FigureCanvasTkAgg(fig3, upper_frame)
canvas3.get_tk_widget().pack(side="left", fill="both", expand=True)

def plot_python():
    plot_course_data(names_python, notes_python)

def plot_web():
    plot_course_data(names_web, notes_web)

def plot_database():
    plot_course_data(names_database, notes_database)

def save_charts():
    #folder 
    folder_path = ""   #ajouter le chemin de dossier 
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    # Save charts 
    fig1.savefig(os.path.join(folder_path, "python_course_notes.png"))
    fig2.savefig(os.path.join(folder_path, "web_course_notes.png"))
    fig3.savefig(os.path.join(folder_path, "database_course_notes.png"))
    print("Les graphiques ont été enregistrés dans le dossier 'charts'.")


button_python = tk.Button(side_frame, text="Python", command=plot_python)
button_web = tk.Button(side_frame, text="Web", command=plot_web)
button_database = tk.Button(side_frame, text="Base de Données", command=plot_database)
button_save = tk.Button(side_frame, text="Enregistrer les Graphiques", command=save_charts)

button_python.pack(pady=10, padx=20, fill="x")
button_web.pack(pady=10, padx=20, fill="x")
button_database.pack(pady=10, padx=20, fill="x")
button_save.pack(pady=10, padx=20, fill="x")




root.mainloop()
