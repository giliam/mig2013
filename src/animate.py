import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# Pour l'utiliser, changez les valeurs des variables  si dessous
# et copiez dans votre main.

data = Cs       # Liste de listes des valeurs
xMin = 350      # Echelles d'affichage
xMax = 550
yMin = 0
yMax = 100
interv = 50     # Millisecondes entre chaque image


fram = len(data)
fig = plt.figure()
ax = plt.axes(xlim=(xMin, xMax), ylim=(yMin, yMax))
line, = ax.plot([], [], lw=2)

def init():
    line.set_data([], [])
    return line,

def animate(i):
    L = len(data[i])
    x = np.linspace(0, L-1, L)
    y = [abs(data[i][int(k)]) for k in x]
    line.set_data(x, y)
    return line,

anim = animation.FuncAnimation(fig, animate, init_func=init,
           frames=fram, interval=interv, blit=True)
