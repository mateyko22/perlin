import random
import numpy as np
import matplotlib.pyplot as plt
import math
from mpl_toolkits.mplot3d import Axes3D

seed = 30
DTW = 8
tab_wart_fake = [0.4004, 0.4288, 0.7274, 0.8840, 0.5509, 0.9133, 0.5159, 0.4848]
tab_wart_przyklad = [0, 1, 0.7274, 0.8840, 0.5509, 0.9133, 0.5159, 0.4848]

# Szum Pseudo Perlina 1D
def wartosci_losowe_wygeneruj_v0(dtw, start):
    tab = []
    random.seed(start)
    for i in range(dtw):
        tab.append(round(random.random(), 4))
    return tab



tab_wart = wartosci_losowe_wygeneruj_v0(8, seed)

# Nieskonczony zakres
def funkcja_skrotu_1d_v0(x_c, dtw):
    return x_c % dtw

# Przyklad dzialania
# tab2 = []
# for i in range(-10, 100):
#     tab2.append(tab_wart[funkcja_skrotu_1d_v0(i, DTW)])


# Poprawiony (przez wymuszenie) generator liczb losowych

def wartosci_losowe_wygeneruj_v1(dtw, start):
    tab = []
    random.seed(start)
    for i in range(dtw):
        tab.append(round(random.random(), 4))
    tab[0] = 0
    tab[1] = 1
    return tab


tab_wart2 = wartosci_losowe_wygeneruj_v1(8, seed)




# Interpolacja liniowa

def interpolacja_1d_rdzen_vlin(w_l, w_p, delta_x):
    return w_p * delta_x + w_l * (1 - delta_x)


def interpolacja_1d_cala_vlin(x, tab_wart):
    x_l = int(x)
    x_p = x_l + 1
    i_x_l = funkcja_skrotu_1d_v0(x_l, DTW)
    i_x_p = funkcja_skrotu_1d_v0(x_p, DTW)
    w_l = tab_wart[i_x_l]
    w_p = tab_wart[i_x_p]
    delta_x = x - x_l
    wy = interpolacja_1d_rdzen_vlin(w_l, w_p, delta_x)
    return wy


# Przyklad dzialania
# tab3 = []
# for i in range(-10, 15):
#     tab3.append(interpolacja_1d_cala_vlin(i, tab_wart_przyklad))
#
# plt.plot(tab3)
# plt.show()


# Interpolacja wygładzona, nieliniowa

def interpolacja_1d_rdzen_vkos(w_l, w_p, delta_x):
    delta_x = math.cos(math.pi + delta_x * math.pi)/2 + 0.5
    return w_p * delta_x + w_l * (1 - delta_x)


def interpolacja_1d_rdzen_vwmian(w_l, w_p, delta_x):
    delta_x = 6 * delta_x**5 - 15 * delta_x**4 + 10 * delta_x**3
    return w_p * delta_x + w_l * (1 - delta_x)


def interpolacja_1d_cala_vnlin(x, tab_wart):
    x_l = int(x)
    x_p = x_l + 1
    i_x_l = funkcja_skrotu_1d_v0(x_l, DTW)
    i_x_p = funkcja_skrotu_1d_v0(x_p, DTW)
    w_l = tab_wart[i_x_l]
    w_p = tab_wart[i_x_p]
    delta_x = x - x_l
    wy = interpolacja_1d_rdzen_vkos(w_l, w_p, delta_x)
    # wy = interpolacja_1d_rdzen_vwmian(w_l, w_p, delta_x)
    return wy


# Przyklad dzialania
tab3 = []
for i in range(2000):
    k = i/100
    tab3.append(interpolacja_1d_cala_vnlin(k, tab_wart_przyklad))

# plt.plot(tab3)
# plt.show()



# Szum Pseudo Perlina 1D,  cz 2.

DTW = 5
tab_wart_przyklad = [0, 1, 0.0244, 0.6910, 0.3388]
tab_perm_przyklad = [2, 0, 4, 1, 3, 2, 0, 4, 1, 3]

def permutacje_podw_wygeneruj_v1(dtw, start):
    tab_permutacji = []
    for i in range(DTW):
        tab_permutacji.append(i)

    for i in range(DTW):
        np.random.seed(seed)
        los = np.random.randint(0, DTW - 1)
        temp = tab_permutacji[i]
        tab_permutacji[i] = tab_permutacji[los]
        tab_permutacji[los] = temp

    for i in range(DTW):
        tab_permutacji.append(tab_permutacji[i])

    return tab_permutacji


def skoki_perm(tab_perm, wynik_pocz, *skl):
    wynik = wynik_pocz
    for i in skl:
        wynik = tab_perm[int(wynik+i)]
    return wynik


def funkcja_skrotu_1d_perm_v0(x_c, tab_perm):
    skl_0 = x_c % DTW
    wynik = skoki_perm(tab_perm, 0, skl_0)
    return wynik


def funkcja_skrotu_1d_perm_v1(x_c, tab_perm):
    skl_0 = x_c % DTW
    skl_1 = x_c//DTW % DTW
    wynik = skoki_perm(tab_perm, 0, skl_0, skl_1)
    return wynik


def funkcja_skrotu_1d_perm_v2(x_c, tab_perm):
    skl_0 = x_c % DTW
    skl_1 = x_c//DTW % DTW
    skl_2 = x_c//(DTW**2) % DTW
    wynik = skoki_perm(tab_perm, 0, skl_0, skl_1, skl_2)
    return wynik


def funkcja_skrotu_1d_perm_v3(x_c, tab_perm):
    if x_c < 0:
        czy_ujemne = 1
        x_c = -x_c
    else:
        czy_ujemne = 0

    wynik = tab_perm[int(x_c % DTW)]
    x_c = x_c // DTW

    while(x_c > 0):
        wynik = tab_perm[int(wynik + (x_c % DTW))]
        x_c = x_c // DTW

    if czy_ujemne:
        wynik = tab_perm[wynik]

    return wynik




# Zastosowanie funkcji skrótu 1d

tab3 = []
tabt = []
for i in range(-1, 11):
    tabt.append(i)
    tab3.append(funkcja_skrotu_1d_perm_v3(i, tab_perm_przyklad))


tab4 = []
for i in range(len(tab3)):
    tab4.append(tab_wart_przyklad[tab3[i]])



def interpolacja_1d_cala_vperm_nlin(x, tab_wart, tab_perm):
    x_l = int(x)
    x_p = x_l + 1
    dtw = len(tab_wart)
    i_x_l = funkcja_skrotu_1d_perm_v3(x_l, tab_perm)
    i_x_p = funkcja_skrotu_1d_perm_v3(x_p, tab_perm)
    w_l = tab_wart[int(i_x_l)]
    w_p = tab_wart[int(i_x_p)]
    delta_x = x - x_l
    wy = interpolacja_1d_rdzen_vwmian(w_l, w_p, delta_x)
    return wy


# Przyklad dzialania
tab5 = []
for i in range(-1, 11):
    tab5.append(interpolacja_1d_cala_vperm_nlin(i, tab4, tab_perm_przyklad))

# plt.plot(tab5)
# plt.show()



# Oktawy

def szum_1d_pseudoperlin_oktawy(x, tab_wart, tab_perm, oktawa_liczba, oktawa_mnoznik, oktawa_zageszczenie):
    ampl_suma = 0
    wy = 0
    for okt_n in range(oktawa_liczba):
        wys_mnoznik = oktawa_mnoznik**okt_n
        zageszczenie_mnoznik = oktawa_zageszczenie**okt_n
        ampl_suma += wys_mnoznik
        wy += wys_mnoznik * interpolacja_1d_cala_vperm_nlin(x * zageszczenie_mnoznik, tab_wart, tab_perm)
    wy = wy / ampl_suma
    return wy




# Szum Pseudo Perlina 2D
DTW = 4
tab_wart = [0, 0.3333, 0.6667, 1]
tab_perm = [1, 3, 2, 0, 1, 3, 2, 0]


# Funkcja skrótu 2D
def funkcja_skrotu_uniw_perm_v3(tab_skl, tab_perm):
    wynik = 0
    for skl_c in tab_skl:
        if skl_c < 0:
            czy_ujemne = 1
            skl_c = -skl_c
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


tab6 = np.ones([8, 12])

for x in range(-1, 10):
    for y in range(0,7):
        tab6[y, x] = funkcja_skrotu_uniw_perm_v3([x, y], tab_perm)





# hf = plt.figure()
# ha = hf.add_subplot(111, projection='3d')
#
# X, Y = np.meshgrid(range(12), range(8))  # `plot_surface` expects `x` and `y` data to be 2D
# ha.plot_surface(X, Y, tab6)
#
# plt.show()



# Interpolacja 2d, liniowy rdzeń
def interpolacja_2d_rdzen_vnlin(w_ld, w_lg, w_pd, w_pg, delta_x, delta_y):
    wy = w_ld * (1-delta_x) * (1-delta_y) + w_lg * (1-delta_x) * delta_y + w_pd * delta_x * (1-delta_y) + w_pg * delta_x * delta_y
    return wy


# Interpolacja 2d, nieliniowy rdzeń
def interpolacja_2d_rdzen_vnlin(w_ld, w_lg, w_pd, w_pg, delta_x, delta_y):
    delta_x = 6 * delta_x**5 - 15 * delta_x**4 + 10*delta_x**3
    delta_y = 6 * delta_y**5 - 15 * delta_y**4 + 10*delta_y**3
    wy = w_ld * (1-delta_x) * (1-delta_y) + w_lg * (1-delta_x) * delta_y + w_pd * delta_x * (1-delta_y) + w_pg * delta_x * delta_y
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