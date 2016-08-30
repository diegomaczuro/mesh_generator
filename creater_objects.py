# -*- coding: utf_8 -*-
__author__ = 'Anastasia Bazhutina'

#чтение .mat файлов с данными DTMRT и построение по ним .vtk
CREATE_DTMRI_VTK = False

#построение по DTMRT .pkl файлов
CREATE_DTMRI_PKL = False

#построение модели с волокнами и раскраской по точкам, показывающей отличие углов наклона векторов волокна в модели
#и данных DTMRT. Верификафия модели, построение гистограммы по углам, подсчет среднего и среднеквадратичного отклонения
#запись результатов
CREATE_MODEL_WITH_FIBER = True
# (dimensionless) количество точек в разбиении для \phi
n = 20
# (dimensionless) количество точек по \gamma0
limit_gamma0 = 100
# (dimensionless) количество точек по \gamma
limit_gamma = 300

#построение поверхности модели ЛЖ
CREATE_SURFACE = True
#количество точек по phi, psi, gamma такое же, как у поверхности с сеткой

#построение поверхности модели ЛЖ с сеткой и волокнами(нужно для построения и визуализации strimline)
CREATE_SURFACE_WITH_MESH = True
#количество точек по углу для сетки с волокнами
phi_series = 30
#количество точек по psi для сетки с волокнами
psi_series = 30
#количество точек по gamma для сетки с волокнами
gamma_series = 30

#создание тетраэдальной сетки по модели
CREATE_MESH = True
#количество точек разбиения по phi
phi = 50 #  (dimensionless)
#количество точек разбиения по psi
psi = 50 #  (dimensionless)


