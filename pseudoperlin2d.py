import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import math
from mpl_toolkits.mplot3d import Axes3D

seed = 31

# Szum Pseudo Perlina 2D
tab_wart = [0, 0.3333, 0.6667, 1]
tab_perm = [1, 3, 2, 0, 1, 3, 2, 0]
DTW = len(tab_wart)


def wartosci_losowe_wygeneruj_v1(dtw, start):
    tab = []
    random.seed(start)
    for i in range(dtw):
        tab.append(round(random.random(), 4))
    tab[0] = 0
    tab[1] = 1
    return tab


# Funkcja skrótu 2D
def funkcja_skrotu_uniw_perm_v3(tab_skl, tab_perm):
    wynik = 0
    for skl_c in tab_skl:
        if skl_c < 0:
            czy_ujemne = 1
            skl_c = -1*skl_c
        else:
            czy_ujemne = 0
        wynik = tab_perm[int(wynik + (skl_c % DTW))]
        skl_c = skl_c // DTW
        while skl_c > 0:
            wynik = tab_perm[int(wynik + skl_c % DTW)]
            skl_c = skl_c // DTW

        if czy_ujemne:
            wynik = tab_perm[wynik]

    return wynik


# Interpolacja 2d, liniowy rdzeń
def interpolacja_2d_rdzen_vlin(w_ld, w_lg, w_pd, w_pg, delta_x, delta_y):
    wy = w_ld * (1-delta_x) * (1-delta_y) + w_lg * (1-delta_x) * delta_y + w_pd * delta_x * (1-delta_y) + w_pg * delta_x * delta_y
    return wy


# Interpolacja 2d, nieliniowy rdzeń
def interpolacja_2d_rdzen_vnlin(w_ld, w_lg, w_pd, w_pg, delta_x, delta_y):
    delta_x = 6 * delta_x**5 - 15 * delta_x**4 + 10*delta_x**3
    delta_y = 6 * delta_y**5 - 15 * delta_y**4 + 10*delta_y**3
    wy = w_ld * (1 - delta_x) * (1 - delta_y) + w_lg * (1 - delta_x) * delta_y + w_pd * delta_x * (
                1 - delta_y) + w_pg * delta_x * delta_y
    return wy


# Interpolacja 2d
def interpolacja_2d_cala_vperm_nlin(x, y, tab_wart, tab_perm):
    x_l = int(x)
    x_p = x_l + 1
    x_delta = x - x_l
    y_d = int(y)
    y_g = y_d + 1
    y_delta = y - y_d
    i_ld = funkcja_skrotu_uniw_perm_v3([x_l, y_d], tab_perm)
    i_lg = funkcja_skrotu_uniw_perm_v3([x_l, y_g], tab_perm)
    i_pd = funkcja_skrotu_uniw_perm_v3([x_p, y_d], tab_perm)
    i_pg = funkcja_skrotu_uniw_perm_v3([x_p, y_g], tab_perm)
    w_ld = tab_wart[i_ld]
    w_lg = tab_wart[i_lg]
    w_pd = tab_wart[i_pd]
    w_pg = tab_wart[i_pg]
    wy = interpolacja_2d_rdzen_vnlin(w_ld, w_lg, w_pd, w_pg, x_delta, y_delta)
    return wy


def interpolacja_2d_cala_vperm_lin(x, y, tab_wart, tab_perm):
    x_l = int(x)
    x_p = x_l + 1
    x_delta = x - x_l
    y_d = int(y)
    y_g = y_d + 1
    y_delta = y - y_d
    i_ld = funkcja_skrotu_uniw_perm_v3([x_l, y_d], tab_perm)
    i_lg = funkcja_skrotu_uniw_perm_v3([x_l, y_g], tab_perm)
    i_pd = funkcja_skrotu_uniw_perm_v3([x_p, y_d], tab_perm)
    i_pg = funkcja_skrotu_uniw_perm_v3([x_p, y_g], tab_perm)
    w_ld = tab_wart[i_ld]
    w_lg = tab_wart[i_lg]
    w_pd = tab_wart[i_pd]
    w_pg = tab_wart[i_pg]
    wy = interpolacja_2d_rdzen_vlin(w_ld, w_lg, w_pd, w_pg, x_delta, y_delta)
    return wy


def wykres3d(tab):
    nrows, ncols = tab.shape

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    X, Y = np.meshgrid(np.arange(ncols), np.arange(nrows))

    ax.plot_surface(X, Y, tab, cmap=cm.terrain)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    ax.set_xlim(0, ncols)
    ax.set_ylim(0, nrows)

    plt.show()


# x = np.linspace(2, 5, 100)
# y = np.linspace(2, 4, 100)
# tab_wart = np.linspace(0,1,32)
#
# xl = len(x)-1
# yl = len(y)-1
# tabk = np.ones([xl,yl])
#
# for i in range(xl):
#     for j in range(yl):
#         tabk[j][i] = interpolacja_2d_cala_vperm_nlin(x[i], y[j], tab_wart, tab_perm)
#
#
# wykres3d(tabk)


def szum_2d_pseudoperlin_oktawy(x, y, tab_wart, tab_perm, oktawa_liczba, oktawa_mnoznik, oktawa_zageszczenie):
    ampl_suma = 0
    wynik = 0
    for okt_n in range(oktawa_liczba-1):
        wys_mnoznik = oktawa_mnoznik**okt_n
        zageszczenie_mnoznik = oktawa_zageszczenie**okt_n
        ampl_suma += wys_mnoznik
        wynik += wys_mnoznik * interpolacja_2d_cala_vperm_nlin(x*zageszczenie_mnoznik, y*zageszczenie_mnoznik, tab_wart, tab_perm)
    return wynik / ampl_suma




x = np.linspace(0,5, 500)
y = np.linspace(0,5,500)

xl = len(x)-1
yl = len(y)-1
tabk = np.ones([xl,yl])

for i in range(xl):
    for j in range(yl):
        tabk[i][j] = szum_2d_pseudoperlin_oktawy(x[i], y[j], tab_wart, tab_perm, 5, 0.5, 2)

wykres3d(tabk)


