# Code made for Sergio Andrés Díaz Ariza
# 06 September 2022
# License MIT
# Lab Procesos: Laboratorio Carga
# import seaborn as sns


import seaborn as sns
import numpy as np
import timeit

start = timeit.default_timer()
sns.set()


class Parameters():
    def Volum(self, h):
        Volum = np.pi * (0.5 ** 2) * h
        return Volum

    def Q(self, Volum, time):
        Q = Volum / time
        return Q

    def Re(self, rho, Q, miu):
        Re = (4 * rho * Q) / (miu * 0.937 * np.pi)
        return Re


class Perdidas():

    def h_f_pipe(self, l, v, D, g, f_D):
        h_f = (l * (v ** 2) / D * 2 * g) * f_D
        return h_f

    def h_f_acce(self, K, v):
        h_f_acce = K * ((v ** 2) / 2)
        return h_f_acce

    def f_D(self, eps, D, Re):
        f_D = (-2 * np.log(((eps / D) / 3.71) - ((50.2 / Re) * np.log(((eps / D) / 3.71) + (14.5 / Re))))) ** (-2)
        return f_D


class K_as():

    def K_acces(self, K1, K_inf, Re):
        K_acce = K1 / Re + K_inf * (1 + 1 / 0.937)
        return K_acce

    def K_valv_100(self, K1, Re, K_inf):
        K_valv_100 = K1 / Re + K_inf * (1 + 1 / 0.937)
        return K_valv_100

    def K_valv(self, Apertura_percentage, K_valv_100):
        K_valv = (1061 * (Apertura_percentage ** -1.51)) * K_valv_100
        return K_valv

    def K_subit_expansion(self, D_menor, D_mayor):
        K_expa = (1 - ((D_menor / D_mayor) ** 2)) ** 2
        return K_expa

    def K_subit_contraction(self, D_menor, D_mayor):
        K_expa = 0.5 * (1 - ((D_menor / D_mayor) ** 2)) ** 2
        return K_expa

class des_time():

    def des_time(self, Vol_s, h_tot, Nivel):
        time = (4 / (np.pi * (0.5 ** 2))) * Vol_s * np.log((Nivel + h_tot) * 2 * 9.81)
        return time


Param = Parameters()
Perdidas = Perdidas()
K_as = K_as()
des_time = des_time()

## Obtencion de datos APERTURA
class Calculus:

    __metaclass__ = Param
    __metaclass__ = Perdidas
    __metaclass__ = K_as
    __metaclass__ = des_time

    def Calcu(self,Nivel,Time, Apertura):
        Vol_s = [Param.Volum(x) for x in Nivel]  # Volume for each height
        Q = [Param.Q(x, y) for x, y in zip(Vol_s, Time)]  # Caudal for each Volume and Time
        Re = [Param.Re(997, x, 0.8937 / 1000) for x in Q]  # Reynolds number for each Q

        # TUBERIA
        f_d = [Perdidas.f_D(5, 0.02, x) for x in Re]  # Darcy factor for the pipe
        v_s = [x / (((0.937 / 2) ** 2) * np.pi) for x in Q]  # Velocity of the fluid for each case
        h_tuberia = [Perdidas.h_f_pipe(1.10, x, 0.937, 9.8, y) for x, y in zip(v_s, f_d)]  # head of lost in the pipe

        # Kas ACCESORIOS
        K_codo = [K_as.K_acces(800, 0.40, x) for x in Re]
        K_union = [K_as.K_acces(200, 0.10, x) for x in Re]
        K_globe_100 = [K_as.K_valv_100(1500, x, 4.0) for x in Re]
        K_globe = [K_as.K_valv(Apertura, x) for x in K_globe_100]
        K_expan = [K_as.K_subit_expansion(0.024, 0.12)] * 3
        K_contra = [K_as.K_subit_contraction(0.024, 0.12)] * 3
        K_contra2 = [K_as.K_subit_contraction(0.024, 0.50)] * 3

        # Perdidas ACCESORIOS
        h_codo = [Perdidas.h_f_acce(x, y) for x, y in zip(K_codo, v_s)]  # head of lost
        h_union = [Perdidas.h_f_acce(x, y) for x, y in zip(K_union, v_s)]  # head of lost
        h_globe = [Perdidas.h_f_acce(x, y) for x, y in zip(K_globe, v_s)]  # head of lost
        h_expans = [Perdidas.h_f_acce(x, y) for x, y in zip(K_expan, v_s)]  # head of lost
        h_contra = [Perdidas.h_f_acce(x, y) for x, y in zip(K_contra, v_s)]  # head of lost
        h_contra2 = [Perdidas.h_f_acce(x, y) for x, y in zip(K_contra2, v_s)]  # head of lost

        # Sumatoria de PERDIDAS
        h_tot_ = [h_codo, h_union, h_globe, h_expans, h_contra, h_contra2]
        h_tot = [sum(x) for x in zip(*h_tot_)]

        time_des = [des_time.des_time(x, y, z) for x, y, z in zip(Vol_s, h_tot, Nivel)]
        time_ = [x * 100 for x in time_des]  # Maybe is a error in units, here we use the machete

        return time_

Calculos = Calculus()

Apertura = 1
Nivel = [0.285, 0.185, 0.085]
Time = [192, 134, 70]

time = Calculos.Calcu(Nivel,Time,Apertura)
print(time)




stop = timeit.default_timer()
print('Time: ', stop - start)
