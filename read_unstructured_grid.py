# coding=utf-8
__author__ = 'Anastasia Bazhutina'

from vtk import *
from vtk.util.numpy_support import vtk_to_numpy
from sklearn.neighbors import KDTree
from const import *
import numpy as np
import logging
import os


def read_ele_file():
#функция чтения .ele файла
    with open(os.path.join(MESH_DATA_FOLDER, OBJECT, FOLDER_NAME, MESH_FILE_NAME + '.1.ele')) as my_file:
        ele_array = my_file.readlines()
    return ele_array[1:]


def read_node_file():
    #функция чтения .node файла
    with open(os.path.join(MESH_DATA_FOLDER, OBJECT, FOLDER_NAME, MESH_FILE_NAME + '.1.node')) as my_file:
        node_array = my_file.readlines()
    return node_array


def coord_centre_of_thetraedra(*param):
    """
    :param xa, ya, za: точка тетраэдра
    :param xb, yb, zb: точка тетраэдра
    :param xc, yc, zc: точка тетраэдра
    :param xs, ys, zs: точка тетраэдра
    :return: x0, y0, z0: координаты центра тетраэдра
    """
    param = param[0]

    xa = param[0]
    ya = param[1]
    za = param[2]

    xb = param[3]
    yb = param[4]
    zb = param[5]

    xc = param[6]
    yc = param[7]
    zc = param[8]

    xs = param[9]
    ys = param[10]
    zs = param[11]

    numerator_array_x = np.array(([xs**2-xa**2+ys**2-ya**2+zs**2-za**2, ys-ya, zs-za],
                                  [xs**2-xb**2+ys**2-yb**2+zs**2-zb**2, ys-yb, zs-zb],
                                  [xs**2-xc**2+ys**2-yc**2+zs**2-zc**2, ys-yc, zs-zc]))

    denominator_array = np.array(([xs-xa, ys-ya, zs-za],
                                  [xs-xb, ys-yb, zs-zb],
                                  [xs-xc, ys-yc, zs-zc]))

    numerator_array_y = np.array(([xs-xa, xs**2-xa**2+ys**2-ya**2+zs**2-za**2, zs-za],
                                  [xs-xb, xs**2-xb**2+ys**2-yb**2+zs**2-zb**2, zs-zb],
                                  [xs-xc, xs**2-xc**2+ys**2-yc**2+zs**2-zc**2, zs-zc]))

    numerator_array_z = np.array(([xs-xa, ys-ya, xs**2-xa**2+ys**2-ya**2+zs**2-za**2],
                                  [xs-xb, ys-yb, xs**2-xb**2+ys**2-yb**2+zs**2-zb**2],
                                  [xs-xc, ys-yc, xs**2-xc**2+ys**2-yc**2+zs**2-zc**2]))

    x0 = np.linalg.det(numerator_array_x)/(2*np.linalg.det(denominator_array))
    y0 = np.linalg.det(numerator_array_y)/(2*np.linalg.det(denominator_array))
    z0 = np.linalg.det(numerator_array_z)/(2*np.linalg.det(denominator_array))

    return x0, y0, z0


def list_cells(str):
    """
    :param str: строка
    :return: возвращает 4 числа - номера точек, которые являются вершинами тетраэдра
    """
    arr_cell = str.split(' ')
    arr_cell_help = []
    for i in xrange(len(arr_cell)):
        if arr_cell[i] != '':
            arr_cell_help.append(arr_cell[i])
    return int(arr_cell_help[1]), int(arr_cell_help[2]), int(arr_cell_help[3]), int(arr_cell_help[4])


def list_points(str):
    """
    :param str: строка
    :return: возвращает 3 числа - координаты одной из вершин тетраэдра
    """
    arr_point = str.split(' ')
    arr_point_help = []
    for i in xrange(len(arr_point)):
        if arr_point[i] != '':
            arr_point_help.append(arr_point[i])
    return float(arr_point_help[1]), float(arr_point_help[2]), float(arr_point_help[3])


def vector_in_centre_thetraedr(dist, v1, v2, v3, v4):
    """
    :param dist: массив из 4 компонент, каждая компонента - расстояние от центра тетраэдра до одной из ближайших 4-х точек
    :param v1: массив, в котором 3 элемента - координаты х,y,z вектора, находящейся от центра тетраэдра на расстоянии dist[0]
    :param v2: массив, в котором 3 элемента - координаты х,y,z вектора, находящейся от центра тетраэдра на расстоянии dist[1]
    :param v3: массив, в котором 3 элемента - координаты х,y,z вектора, находящейся от центра тетраэдра на расстоянии dist[2]
    :param v4: массив, в котором 3 элемента - координаты х,y,z вектора, находящейся от центра тетраэдра на расстоянии dist[3]
    :return: vx, vy, vz: координаты вектора в центре тетраэдра, полученные взятием среднего по 4-м ближайшим к центру векторам    """

    x = (dist[0]*v1[0] + dist[1]*v2[0] + dist[2]*v3[0] + dist[3]*v4[0])/(dist[0] + dist[1] + dist[2] + dist[3])
    y = (dist[0]*v1[1] + dist[1]*v2[1] + dist[2]*v3[1] + dist[3]*v4[1])/(dist[0] + dist[1] + dist[2] + dist[3])
    z = (dist[0]*v1[2] + dist[1]*v2[2] + dist[2]*v3[2] + dist[3]*v4[2])/(dist[0] + dist[1] + dist[2] + dist[3])
    vec = np.array([x, y, z])
    vx = x/np.linalg.norm(vec)
    vy = y/np.linalg.norm(vec)
    vz = z/np.linalg.norm(vec)
    return vx, vy, vz


def write_axi(N, array_vectors):
    #функция записи .axi файла
    with open(os.path.join(MESH_DATA_FOLDER, OBJECT, FOLDER_NAME, MESH_FILE_NAME + '.axi'), 'w') as out_mesh:
        out_mesh.write(str(N) + '\n')
        for i in xrange(N):
            out_mesh.write('{0} {1} {2}\n'.format(array_vectors[i][0], array_vectors[i][1], array_vectors[i][2]))


#функция создает и записывает .axi файл, в котором для каждой тетраэдральной ячейки указан вектор, лежащий в центре ячейки
def create_axi_file():
    logger = logging.getLogger('simple_log')
    #чтение данных vtk с сеткой, создание октанта
    file_name = os.path.join(MESH_DATA_FOLDER, OBJECT, FOLDER_NAME, MESH_FILE_NAME + '.1.vtk')
    reader = vtkUnstructuredGridReader()
    reader.SetFileName(file_name)
    reader.Update()  # Needed because of GetScalarRange
    output = reader.GetOutput()
    boneLocator = vtk.vtkCellLocator()
    boneLocator.SetDataSet(output)
    boneLocator.BuildLocator()

    #чтение данных ДТМРТ
    reader2 = vtkUnstructuredGridReader()
    way = os.path.join(VTK_DATA_FOLDER, OBJECT, FOLDER_NAME, VECTOR_FIELD)
    reader2.SetFileName(way)
    reader2.Update()
    ug2 = reader2.GetOutput()
    points2 = ug2.GetPoints()
    coords_vectors_data = vtk_to_numpy(ug2.GetPointData().GetArray('DTMRIFiberOrientation'))
    coord_points_data = vtk_to_numpy(points2.GetData())
    #построение дерева
    tree = KDTree(coord_points_data, leaf_size=5, metric='euclidean')

    #чтение .ele файла
    ele_array = read_ele_file()
    N = len(ele_array) - 1 #количество точек в ele файле

    #чтение .node файла
    node_array = read_node_file()

    cell_array = np.zeros((N))
    cell_vectors = np.zeros((N, 3))

    n = 0
    #случай, когда в тетраэдр попал один или несколько векторов
    for i in xrange(len(coord_points_data)):
        a = boneLocator.FindCell(coord_points_data[i])
        if a != -1:
            n += 1
            #подсчет количества векторов, попадающих в каждый тетраэдр
            cell_array[a] += 1
            #сумма всех координат всех векторов, попавших в один тетраэдр
            cell_vectors[a] = cell_vectors[a] + coord_points_data[i]

    #случай, когда в тетраэдр попал один или несколько векторов
    for i in xrange(N):
        if cell_array[i] != 0:
            #взятие среднего арифметического координат всех векторов, попавших в один тетраэдр
            vec_help = cell_vectors[i]/float(cell_array[i])
            #нормирование этого вектора
            cell_vectors[i] = vec_help/np.linalg.norm(vec_help)

    #случай, когда в тетраэдр не попало ни одного вектора
    for i in xrange(N):
        if cell_array[i] == 0:
            #получили номера вершин i-го тетраэдра
            numb_cell1, numb_cell2, numb_cell3, numb_cell4 = list_cells(ele_array[i])
            x1, y1, z1 = list_points(node_array[numb_cell1])
            x2, y2, z2 = list_points(node_array[numb_cell2])
            x3, y3, z3 = list_points(node_array[numb_cell3])
            x4, y4, z4 = list_points(node_array[numb_cell4])
            #получили координату цетра тетраэдра с вершинами x1,y1,z1, x2,y2,z2, x3,y3,z3, x4,y4,z4
            x, y, z = coord_centre_of_thetraedra([x1,y1,z1, x2,y2,z2, x3,y3,z3, x4,y4,z4])
            dist, ind = tree.query((x, y, z), k=4)
            #получили среднее арифметическое 4-х векторов, ближайщих к центру тетраэдра
            vx, vy, vz = vector_in_centre_thetraedr(dist[0], coords_vectors_data[ind[0][0]],
                                                             coords_vectors_data[ind[0][1]],
                                                             coords_vectors_data[ind[0][2]],
                                                             coords_vectors_data[ind[0][3]])

            cell_vectors[i][0] = vx
            cell_vectors[i][1] = vy
            cell_vectors[i][2] = vz
    logger.info(u"Запись в .axi файл...")
    write_axi(N, cell_vectors)

if __name__ == "__main__":
    create_axi_file()