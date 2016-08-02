# -*- coding: utf_8 -*-
__author__ = 'Anastasia Bazhutina'

import numpy as np
import pickle
import matplotlib.pylab as plt
from const import *
import pandas as pd
from  Model.model import *
from sklearn.neighbors import KDTree
from write_geo import *

def write_points_model_in_file(file_name, *param):
    """Запись в файл координат точек, скаляров для каждой точки, векторов в каждой точке

     Parameters
     ----------
     file_name : str
         file_name - имя файла для записи
     param[0]: float
         param[0] - координата точки (Х)
     param[1]: float
         param[1] - координата точки (Y)
     param[2]: float
         param[2] - координата точки (Z)
     param[3]: float
         param[3] - координата вектора (Х)
     param[4]: float
         param[4] - координата вектора (Y)
     param[5]: float
         param[5] - координата вектора (Z)
     param[6]: float
         param[6] - скаляр в точке (Х, Y, Z)
    """
    point1 = param[0]
    point2 =param[1]
    point3 =param[2]
    vector1 =param[3]
    vector2 =param[4]
    vector3 =param[5]
    scalar =param[6]
    connection = param[7]
    sur = param[8]
    type_connection = param[9]
    len1 = len(point1)
    len2 = len(vector1)
    len3 = len(scalar)
    len4 = len(connection)
    print len3, len1, len2, len4

    if sur == 'only surface':
        with open(str(file_name)+'.vtk', "w") as out_mesh:
            out_mesh.write("# vtk DataFile Version 2.0\n")
            out_mesh.write("Really cool data\n")
            out_mesh.write("ASCII\n")
            out_mesh.write("DATASET UNSTRUCTURED_GRID\n")
            out_mesh.write("POINTS {pcount} double\n".format(pcount=len1))
            for i in xrange(0, len1):
                out_mesh.write("{0} {1} {2}\n".format(point1[i], point2[i], point3[i]))
            out_mesh.write("CELLS {pcount} {pcount2}\n".format(pcount=len4, pcount2=(len4 * 5)))
            for j in xrange(len4):
                if type_connection=='VTK_TRIANGLE':
                    t_ = connection[j]
                    out_mesh.write("3 {0} {1} {2}\n".format(t_[0], t_[1], t_[2]))
                else:
                    t_ = connection[j]
                    out_mesh.write("4 {0} {1} {2} {3}\n".format(t_[0], t_[1], t_[2], t_[3]))
            out_mesh.write("CELL_TYPES {pcount}\n".format(pcount=len4))
            for k in xrange(len4):
                if type_connection=='VTK_TRIANGLE':
                    out_mesh.write("5\n")
                else:
                    out_mesh.write("9\n")

    else:
        with open(str(file_name)+'.vtk', 'w') as out_mesh:

            out_mesh.write("# vtk DataFile Version 2.0\n")
            out_mesh.write("Really cool data\n")
            out_mesh.write("ASCII\n")
            out_mesh.write("DATASET UNSTRUCTURED_GRID\n")
            out_mesh.write("POINTS {pcount} double\n".format(pcount=len1))

            for i in xrange(0, len1):
                out_mesh.write("{0} {1} {2}\n".format(point1[i], point2[i], point3[i]))


            if len4 != 0:
                out_mesh.write("CELLS {pcount} {pcount2}\n".format(pcount=len4, pcount2=(len4 * 9)))
                for j in xrange(len4):
                    t_ = connection[j]

                    out_mesh.write(
                        "8 {0} {1} {2} {3} {4} {5} {6} {7}\n".format(t_[0], t_[1], t_[2], t_[3], t_[4], t_[5], t_[6], t_[7]))
                out_mesh.write("CELL_TYPES {pcount}\n".format(pcount=len4))
                for k in xrange(len4):
                    out_mesh.write("12\n")

            else:
                out_mesh.write("CELLS {pcount} {pcount2}\n".format(pcount=len1, pcount2=(len1 * 2)))
                for j in xrange(len1):
                    out_mesh.write("1 {0}\n".format(j))
                out_mesh.write("CELL_TYPES {pcount}\n".format(pcount=len1))
                for k in xrange(len1):
                    out_mesh.write("1\n")
            if len3 != 0:
                out_mesh.write("POINT_DATA {pcount}\n".format(pcount=len3))
                #out_mesh.write("SCALARS angle_diff double\n")
                out_mesh.write("SCALARS endo double\n")
                out_mesh.write("LOOKUP_TABLE default\n")

                for i in xrange(len3):
                    out_mesh.write("{0}\n".format(scalar[i]))

            if len2 != 0:
                if len3 == 0:
                    out_mesh.write("POINT_DATA {pcount}\n".format(pcount=len2))
                out_mesh.write("VECTORS DTMRIFiberOrientation double\n")
                for i in xrange(len2):
                    out_mesh.write("{0} {1} {2}\n".format(vector1[i], vector2[i], vector3[i]))



def main():

    n = 20  # количество точек в разбиении для \phi
    limit_gamma0 = 20  # количество точек по \gamma0
    limit_gamma = 20  # количество точек по \gamma

    obj1 = Model('./Model/test/4_slice_ok.csv')
    obj1.md.shift_x = 0#150#140 canine
    obj1.md.shift_y = 0#165#100 canine
    obj1.md.shift_z = 0#11 * 2.27
    obj1.apex_position = default_apex_position
    phi = np.linspace(0, 2 * np.pi, n + 1)  # TODO это является неверным. Последняя точка должна быть без щели
    # x, y, z - координаты точки      v1, v2, v3 - вектора
    #x, y, z, v1, v2, v3, gamma = obj1.generate_series_points(n, limit_gamma0, limit_gamma)

    tree = None
    with open('./Model/test/full_tree.pkl', 'rb') as fl:
        tree = pickle.load(fl)
    dist, ind = tree.query((11, 1, 0), k=1)

    vectors_data = None
    with open('./Model/test/full_vector.pkl', 'rb') as fl:
        vectors_data = pickle.load(fl)

    angle_mas = []
    epsilon_mas = []

    #for i in xrange(len(x)):
    #    dist, ind = tree.query((x[i], y[i], z[i]), k=1)
    #    vector_in_data = vectors_data[ind[0][0]]
    #    angle_min = fiber_angle(np.array([v1[i], v2[i], v3[i]]),
    #                            np.array([vector_in_data[0], vector_in_data[1], vector_in_data[2]]))
    #    angle_mas.append(angle_min)
    #    epsilon_mas.append(dist[0][0])
#
    #write_points_model_in_file('points_for_verification_human', x, y, z, v1, v2, v3, angle_mas, [], [], 'VTK_QUAD')# angle_mas)
#
    #mean = np.mean(angle_mas)
    #std = np.std(angle_mas)
#
    #print np.mean(angle_mas)
    #print np.std(angle_mas)
#
    #general_count = len(angle_mas)
    #two_sigma_count = 0
#
    #for a in angle_mas:
    #    if (a < mean - (2*std)) or (a > mean + (2*std)):
    #        two_sigma_count+=1
#
    #print str((float(two_sigma_count)/float(general_count))*100) + " %"
#
    #with open('result_slice_8_human.csv', 'w') as fl:
    #    fl.write(str(np.mean(angle_mas)))
    #    fl.write(';')
    #    fl.write(str(np.std(angle_mas)))
    #    fl.write(';')
    #    fl.write(str((float(two_sigma_count)/float(general_count))*100))
#
    #plt.hist(angle_mas, bins=100)
    #plt.savefig('hist_8_slice_human.png')
#
    ##тут построение streamlines
    #results_points = map(lambda x, y, z: [x, y, z], x, y, z)
    #results_vectors = map(lambda x, y, z: [x, y, z], v1, v2, v3)
#
    #tree1 = KDTree(results_points, leaf_size=1, metric='euclidean')
    ##поверхность с сеткой внутри
    #x2, y2, z2, v21, v22, v23, connection, gamma_color = obj1.generate_surface_vol(20, 20, 20, tree1, results_vectors)
    #write_points_model_in_file('my_surface_vol', x2, y2, z2, v21, v22, v23, gamma_color, connection, [], 'VTK_QUAD')  # angle_mas)
#
    ###поверхность без сетки
    #x3, y3, z3, connection3 = obj1.surface(10, 10, 10)
    #write_points_model_in_file('my_surface_human', x3, y3, z3, [], [], [], [], connection3, 'only surface', 'VTK_QUAD')# 'VTK_TRIANGLE')
    #часть поверхности
    x4, y4, z4, connection4, apex = obj1.splane_for_mesh(10, 50)
    print x4, y4, z4, connection4
    print len(x4), len(connection4)
    write_geo('mesh1', x4, y4, z4, connection4, 10, apex)



if __name__ == '__main__':
    main()
