# coding=utf-8
import logging

import numpy as np
from Model.model import project_vector_on_plane

PLANE_WIDTH = 0.4

class ApexPosition:

    def __init__(self):
        self.X = np.array([0, 0, 0]) # Координаты верхушки
        self.A = np.array([1, 0, 0]) # Вектор нормали, определяющий четырехкамерную позицию
        self.B = np.array([0, 1, 0])  # Вектор нормали, определяющий двухкамерную позицию
        self.C = np.array([0, 0, 1])  # Вектор определяющий ось желудочка
        self.d = 100 # Высота модели в терминах

    @staticmethod
    def init_from_line(point1, point2, point3, point4, point5, point6):
        """По линиям, проведенным на рисунке, строит срезы
        """
        vector1 = (point2 - point1) / np.linalg.norm(point2 - point1)
        vector2_ = (point3 - point4) / np.linalg.norm(point3 - point4)
        vector3_ = (point5 - point6) / np.linalg.norm(point5 - point6)

        vector3 = np.cross(vector1, vector2_)
        vector2 = np.cross(vector3_, vector1)

        if np.dot(vector2_,vector2) < 0:
            raise BaseException("Initial vector is bad!")
        if np.dot(vector3_,vector3) < 0:
            raise BaseException("Initial vector is bad!")

        ap = ApexPosition()
        ap.X = point1
        ap.C = vector1 / np.linalg.norm(vector1) # Вектор оси ЛЖ
        ap.A = vector2 / np.linalg.norm(vector2) # Вектор определяющий плоскость 4ch позиции
        ap.B = vector3 / np.linalg.norm(vector3) # Вектор определяющий плоскость 2ch позиции

        return ap

    def translate(self, point):
        """Переносит модель в нужную позицию в данных"""
        L = np.matrix(np.matrix([self.A, self.B, self.C]).transpose())
        a_ = np.matrix(point).transpose()
        a = L * a_
        return np.array((a.transpose() + self.X))[0]


    def plane_cut(self, data, plane_name='2ch'):
        """Вырезает срезы из данных"""

        plane = self.A
        pseudo_line = self.B
        if plane_name == '4ch':
            plane = self.B
            pseudo_line = self.A
        elif plane_name == '2ch':
            plane = self.A
            pseudo_line = self.B
        else:
            logging.error("This version support only '2ch' and '4ch' slices.")
            raise KeyError("This version support only '2ch' and '4ch' slices.")

        left_r = []
        left_z = []
        right_r = []
        right_z = []
        #test = []

        for i in range(len(data)):
            for j in range(len(data[0])):
                for k in range(len(data[0][0])): # Цикл по всем элементам массива
                    if data[i][j][k]:     # Так как массив состоит из bool, точка - это True значение
                        x = i
                        y = j
                        z = 2.27 * k

                        point, dist = project_vector_on_plane(plane, self.X, np.array([x,y,z])) # Проекция на плоскость среза

                        #test.append(dist)
                        if dist < PLANE_WIDTH: # Берем только точки в достаточной близости от среза
                            point_on_axe, r_coord = project_vector_on_plane(pseudo_line, self.X, point) # Пользуясь ортогональностью срезов, проецируем точку на ось ЛЖ
                            z_coord = np.linalg.norm(point_on_axe - self.X)

                            side = np.inner((point - point_on_axe), pseudo_line)

                            if side <= 0: # По скалярному произведению понимаем с какой стороны от оси ЛЖ лежит точка
                                left_r.append(r_coord)
                                left_z.append(z_coord)
                            else:
                                right_r.append(r_coord)
                                right_z.append(z_coord)

        #with open('./test_data/data.txt', 'a') as fl:
        #    fl.write(str(min(test)))
        #    fl.write('\n')

        return left_r, left_z, right_r, right_z
