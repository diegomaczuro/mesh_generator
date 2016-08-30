# -*- coding: utf_8 -*-
__author__ = 'Anastasia Bazhutina'

#чтение .mat файлов с данными DTMRT и построение по ним .vtk
CREATE_DTMRI_VTK = False

#построение по DTMRT .pkl файлов
CREATE_DTMRI_PKL = False

#построение модели с волокнами и раскраской по точкам, показывающей отличие углов наклона векторов волокна в модели
#и данных DTMRT
CREATE_MODEL_WITH_FIBER = True

#построение поверхности модели ЛЖ
CREATE_SURFACE = True

#построение поверхности модели ЛЖ с сеткой и волокнами(нужно для построения и визуализации strimline)
CREATE_SURFACE_WITH_MESH = True

#создание тетраэдальной сетки по модели
CREATE_MESH = True

#задание направления волокна в каждом тетраэдре сетки(построение .axi файла)
CREATE_AXI = True
