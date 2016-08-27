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
import os
import sys
import logging
from read_unstructured_grid import *


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


def log_config(console_level):
    """Конфигурирует вывод логгера
    """
    logger = logging.getLogger('simple_log')
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    if os.path.exists('default.log'):
        os.remove('default.log')
    fh = logging.FileHandler('default.log')
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler(stream=sys.stdout)
    ch.setLevel(console_level)
    # create formatter and add it to the handlers
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    formatter = logging.Formatter('%(levelname)s:%(message)s')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    # add the handlers to logger
    logger.addHandler(ch)
    logger.addHandler(fh)


def main():

    log_config(logging.INFO)
    logger = logging.getLogger('simple_log')

    logger.info(u"Запуск")

    n = 20  # (dimensionless) количество точек в разбиении для \phi
    limit_gamma0 = 20  # (dimensionless)  количество точек по \gamma0
    limit_gamma = 20  # (dimensionless)  количество точек по \gamma
    logging.debug("n, limit_gamma0,  limit_gamma: {0} {1} {2}".format(n, limit_gamma0,  limit_gamma))

    obj1 = Model(os.path.join('./' + CSV_FOLDER, OBJECT, FOLDER_NAME, FILE_CSV))
    obj1.md.shift_x = 0 # (cm) #150#140 canine
    obj1.md.shift_y = 0 # (cm) #165#100 canine
    obj1.md.shift_z = 0 # (cm) #11 * 2.27
    obj1.apex_position = default_apex_position
    phi = np.linspace(0, 2 * np.pi, n + 1)


    phi = 50 #  (dimensionless)
    psi = 50 #  (dimensionless)
    x4, y4, z4, connection4, apex1 = obj1.splane_for_mesh_epi(phi, psi)
    x5, y5, z5, connection5, apex2, border1 = obj1.splane_for_mesh_endo(phi, psi)

    logger.debug("x5, y5, z5, connection5: {0} {1} {2} {3}".format(x5, y5, z5, connection5))
    logger.debug("len(x4), len(connection4): {0} {1}".format(len(x4), len(connection4)))

    logger.info(u"Запись geo файла...")
    write_geo(os.path.join(MESH_DATA_FOLDER, OBJECT, FOLDER_NAME, MESH_FILE_NAME), x4, y4, z4, connection4, apex1,
              x5, y5, z5, connection5, apex2, border1, 0.2)

    logger.info(u"Построение сетки...")
    os.chdir(os.path.join(MESH_DATA_FOLDER , OBJECT, FOLDER_NAME))
    os.system("gmsh -2 " + MESH_FILE_NAME + ".geo -o " + MESH_FILE_NAME + ".stl")
    os.system("tetgen -Ra0.0003pqkgo/71 " + MESH_FILE_NAME + ".stl")

    os.chdir('../../../')
    logger.info(u"Подготовка к записи в .axi файл...")
    create_axi_file()
    logger.info(u"Запись в .axi файл: успешно")

    logger.info(u"Программа успешно завершилась. Проверьте вывод gmsh и tetgen")


if __name__ == "__main__":
    main()