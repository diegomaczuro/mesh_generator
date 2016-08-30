# -*- coding: utf_8 -*-
__author__ = 'Anastasia Bazhutina'
from mesh_generator import *
from write_results import *
from read_data_diffusion import *
import logging


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

    if CREATE_DTMRI_VTK:
        #чтение .mat файлов с данными DTMRT и построение по ним .vtk
        logger.info(u"чтение .mat файлов с данными DTMRT и построение по ним .vtk")
        read_data_diffusion()    

    obj1 = Model(os.path.join(CSV_FOLDER, OBJECT, FOLDER_NAME, FILE_CSV))
    obj1.md.shift_x = 0 # (cm)  #150#140 canine
    obj1.md.shift_y = 0 # (cm)  #165#100 canine
    obj1.md.shift_z = 0 # (cm)  11 * 2.27
    obj1.apex_position = default_apex_position
    # x, y, z - координаты точки      v1, v2, v3 - вектора
    x, y, z, v1, v2, v3, gamma = obj1.generate_series_points(n, limit_gamma0, limit_gamma)

    if CREATE_MODEL_WITH_FIBER:
        logger.info(u"Построение модели с волокнами")

        tree = None
        with open(os.path.join(VTK_DATA_FOLDER, OBJECT, FOLDER_NAME, FILE_TREE), 'rb') as fl:
            tree = pickle.load(fl)
        dist, ind = tree.query((11, 1, 0), k=1)

        vectors_data = None
        with open(os.path.join(VTK_DATA_FOLDER, OBJECT, FOLDER_NAME, FILE_VECTOR), 'rb') as fl:
            vectors_data = pickle.load(fl)

        angle_mas = []
        epsilon_mas = []

        for i in xrange(len(x)):
            dist, ind = tree.query((x[i], y[i], z[i]), k=1)
            vector_in_data = vectors_data[ind[0][0]]
            angle_min = fiber_angle(np.array([v1[i], v2[i], v3[i]]),
                                    np.array([vector_in_data[0], vector_in_data[1], vector_in_data[2]]))
            angle_mas.append(angle_min)
            epsilon_mas.append(dist[0][0])

        logger.info(u"Начало записи в .vtk файл модели...")
        write_points_model_in_file(os.path.join(MESH_DATA_FOLDER, OBJECT, FOLDER_NAME, FILE_MODEL_VTK), x, y, z, v1, v2, v3, angle_mas, [], [], 'VTK_QUAD')# angle_mas)
        logger.info(u"Завершение записи!")

        mean = np.mean(angle_mas)
        std = np.std(angle_mas)

        logger.info(np.mean(angle_mas))
        logger.info(np.std(angle_mas))

        general_count = len(angle_mas)
        two_sigma_count = 0

        for a in angle_mas:
            if (a < mean - (2*std)) or (a > mean + (2*std)):
                two_sigma_count+=1

        logger.info(str((float(two_sigma_count)/float(general_count))*100) + " %")

        with open(os.path.join(MESH_DATA_FOLDER, OBJECT, FOLDER_NAME, FILE_RESULT), 'w') as fl:
            fl.write(str(np.mean(angle_mas)))
            fl.write(';')
            fl.write(str(np.std(angle_mas)))
            fl.write(';')
            fl.write(str((float(two_sigma_count)/float(general_count))*100))

        plt.hist(angle_mas, bins=100)
        plt.savefig(os.path.join(MESH_DATA_FOLDER, OBJECT, FOLDER_NAME, FILE_HIST))

    if CREATE_SURFACE_WITH_MESH:
        ##тут построение streamlines
        results_points = map(lambda x, y, z: [x, y, z], x, y, z)
        results_vectors = map(lambda x, y, z: [x, y, z], v1, v2, v3)

        tree1 = KDTree(results_points, leaf_size=1, metric='euclidean')
        ##поверхность с сеткой внутри
        logger.info(u"Построение поверхности с сеткой")
        x2, y2, z2, v21, v22, v23, connection, gamma_color = obj1.generate_surface_vol(phi_series, psi_series, gamma_series,
                                                                                       tree1, results_vectors)
        logger.info(u"Начало записи в .vtk файл поверхности с сеткой...")
        write_points_model_in_file(os.path.join(MESH_DATA_FOLDER, OBJECT, FOLDER_NAME, FILE_SURFACE_WITH_MESH), x2, y2, z2,
                                   v21, v22, v23, gamma_color, connection, [], 'VTK_QUAD')  # angle_mas)
        logger.info(u"Завершение записи!")

    if CREATE_SURFACE:
        ##поверхность без сетки
        logger.info(u"Построение поверхности")
        x3, y3, z3, connection3 = obj1.surface(phi_series, psi_series, gamma_series)
        logger.info(u"Начало записи в .vtk файл поверхности...")
        write_points_model_in_file(os.path.join(MESH_DATA_FOLDER, OBJECT, FOLDER_NAME, FILE_SURFACE), x3, y3, z3,
                               [], [], [], [], connection3, 'only surface', 'VTK_QUAD')# 'VTK_TRIANGLE')
        logger.info(u"Завершение записи!")

    if CREATE_MESH:
        logger.info(u"Построение тетраэдральной сетки")
        #создание тетраэдральной сетки и задание волокна из данных DTMRT в каждом тетраэдре
        create_mesh()



if __name__ == '__main__':
    main()
