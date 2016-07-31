# -*- coding: utf_8 -*-
import math
import numpy as np
import matplotlib.pyplot as plt
__author__ = 'Anastasia Bazhutina'

def alg_interp(func_param, func_value):
    """
        :func_param: список точек - аргументов интерполируемой функции
        :func_value: значение интерполируемой функции в каждой точке
        :return:
         column_a: столбец коэффициентов a кубического сплайна
         column_b: столбец коэффициентов b кубического сплайна
         column_c: столбец коэффициентов c кубического сплайна
         column_d: столбец коэффициентов d кубического сплайна
        """
    # число срезов
    N = len(func_param)
    # Ac = b система уравнений относительно коэффициентов c кубического сплайна
    A = np.zeros((N-1, N-1))
    #print A
    b = np.zeros(N-1)
    param = func_param
    value = func_value
    #заполнение первой строки матрицы А
    A[0, 0] = 2 * (param[2] - param[0])
    A[0, 1] = param[2] - param[1]
    A[0, N-2] = param[1] - param[0]
    b[0] = 3 * ((value[1] - value[0]) / (param[1] - param[0]) -
                (value[N-1] - value[N-2]) / (param[N-1] - param[N-2]))

    for i in xrange(1, N-2):
        A[i, i] = 2 * (param[i + 2] - param[i])
        A[i, i + 1] = param[i + 2] - param[i+1]
        A[i, i - 1] = param[i+1] - param[i]
        b[i] = 3 * ((value[i + 1] - value[i]) / (param[i + 1] - param[i]) -
                        (value[i] - value[i-1]) / (param[i] - param[i-1]))
    #заполнение последней строки матрицы А
    A[N-2, N-2] = 2 * (param[N-1] - param[N-2] + param[1] - param[0])
    A[N-2, N-3] = param[N-1] - param[N-2]
    A[N-2, 0] = param[1] - param[0]
    b[N-2] = 3 * ((value[N-1] - value[N-2]) / (param[N-1] - param[N-2]) -
                (value[N-2] - value[N-3]) / (param[N-2] - param[N-3]))
    #print A
    #находим  n1..n-1 коэффициенты c кубического сплайна
    c = np.linalg.solve(A, b)
    #столбцы результатов
    column_a = value
    column_b = np.zeros(N-1)
    column_c = np.zeros(N-1)
    column_d = np.zeros(N-1)
    # находим коэффициенты c кубического сплайна
    #for i in xrange(len(c)):
    #    column_c[i+1] = c[i]
    column_c = c
    # находим коэффициенты b, d кубического сплайна
    for i in xrange(N-2):
        column_b[i] = (value[i+1]-value[i])/(param[i+1]-param[i])-\
        (param[i + 1] - param[i])*(column_c[i+1]+2*column_c[i])/3
        column_d[i] = (column_c[i+1]-column_c[i])/(3*(param[i+1]-param[i]))
    column_b[N-2] = (value[0] - value[N-2]) / (param[N-1] - param[N-2]) - \
                      (param[N-1] - param[N-2]) * (column_c[0] + 2 * column_c[N-2]) / 3
    column_d[N-2] = (column_c[0] - column_c[N-2]) / (3 * (param[N-1] - param[N-2]))

    #print column_b
    #print  column_d
    return column_a, column_b, column_c, column_d