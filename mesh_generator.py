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
from read_unstructured_grid import *
from creater_objects import *


def create_mesh():

    logger.info(u"Запуск")
    logging.debug("n, limit_gamma0,  limit_gamma: {0} {1} {2}".format(n, limit_gamma0,  limit_gamma))

    obj1 = Model(os.path.join('./' + CSV_FOLDER, OBJECT, FOLDER_NAME, FILE_CSV))
    obj1.md.shift_x = 0 # (cm) #150#140 canine
    obj1.md.shift_y = 0 # (cm) #165#100 canine
    obj1.md.shift_z = 0 # (cm) #11 * 2.27
    obj1.apex_position = default_apex_position

    x4, y4, z4, connection4, apex1 = obj1.splane_for_mesh_epi(phi, psi)
    x5, y5, z5, connection5, apex2, border1 = obj1.splane_for_mesh_endo(phi, psi)

    logger.debug("x5, y5, z5, connection5: {0} {1} {2} {3}".format(x5, y5, z5, connection5))
    logger.debug("len(x4), len(connection4): {0} {1}".format(len(x4), len(connection4)))

    logger.info(u"Запись geo файла...")
    write_geo(os.path.join(MESH_DATA_FOLDER, OBJECT, FOLDER_NAME, MESH_FILE_NAME), x4, y4, z4, connection4, apex1,
              x5, y5, z5, connection5, apex2, border1, 0.2)

    logger.info(u"Построение сетки...")
    os.chdir(os.path.join(MESH_DATA_FOLDER, OBJECT, FOLDER_NAME))
    os.system("gmsh -2 " + MESH_FILE_NAME + ".geo -o " + MESH_FILE_NAME + ".stl")
    os.system("tetgen -Ra0.0003pqkgo/71 " + MESH_FILE_NAME + ".stl")

    os.chdir('../../../')
    logger.info(u"Подготовка к записи в .axi файл...")
    create_axi_file()
    logger.info(u"Запись в .axi файл: успешно")

    logger.info(u"Программа успешно завершилась. Проверьте вывод gmsh и tetgen")


if __name__ == "__main__":
    create_mesh()