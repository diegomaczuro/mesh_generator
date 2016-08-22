# coding=utf-8
__author__ = 'Anastasia Bazhutina'
import scipy.io
from vtk import *
from vtk.util.misc import vtkGetDataRoot
import numpy as np
from vtk.util.numpy_support import vtk_to_numpy
from sklearn.neighbors import KDTree


def read_ele_file():
    with open('MESH_DATA_MODEL/Normal human/DTI060904/mesh.1.ele') as my_file:
        ele_array = my_file.readlines()
    return ele_array[1:]

def read_node_file():
    with open('MESH_DATA_MODEL/Normal human/DTI060904/mesh.1.node') as my_file:
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
    arr_cell = str.split(' ')
    arr_cell_help = []
    for i in xrange(len(arr_cell)):
        if arr_cell[i] != '':
            arr_cell_help.append(arr_cell[i])
    return int(arr_cell_help[1]), int(arr_cell_help[2]), int(arr_cell_help[3]), int(arr_cell_help[4])

def list_points(str):
    arr_point = str.split(' ')
    arr_point_help = []
    for i in xrange(len(arr_point)):
        if arr_point[i] != '':
            arr_point_help.append(arr_point[i])
    return float(arr_point_help[1]), float(arr_point_help[2]), float(arr_point_help[3])


def vector_in_centre_thetraedr(dist, v1, v2, v3, v4):
    x = (dist[0]*v1[0] + dist[1]*v2[0] + dist[2]*v3[0] + dist[3]*v4[0])/(dist[0] + dist[1] + dist[2] + dist[3])
    y = (dist[0]*v1[1] + dist[1]*v2[1] + dist[2]*v3[1] + dist[3]*v4[1])/(dist[0] + dist[1] + dist[2] + dist[3])
    z = (dist[0]*v1[2] + dist[1]*v2[2] + dist[2]*v3[2] + dist[3]*v4[2])/(dist[0] + dist[1] + dist[2] + dist[3])
    vec = np.array([x, y, z])
    vx = x/np.linalg.norm(vec)
    vy = y/np.linalg.norm(vec)
    vz = z/np.linalg.norm(vec)
    return vx, vy, vz

def write_axi(N, array_vectors):
    with open('MESH_DATA_MODEL/Normal human/DTI060904/mesh.axi', 'w') as out_mesh:
        out_mesh.write(str(N) + '\n')
        for i in xrange(N):
            out_mesh.write('{0} {1} {2}\n'.format(array_vectors[i][0], array_vectors[i][1], array_vectors[i][2]))


#чтение данных vtk с сеткой, создание октанта
file_name = "MESH_DATA_MODEL/Normal human/DTI060904/mesh.1.vtk"
reader = vtkUnstructuredGridReader()
reader.SetFileName(file_name)
reader.Update()  # Needed because of GetScalarRange
output = reader.GetOutput()
points = output.GetPoints()
scalar_range = output.GetScalarRange()
VTK_DATA_ROOT = vtkGetDataRoot()
boneLocator = vtk.vtkCellLocator()
boneLocator.SetDataSet(output)
boneLocator.BuildLocator()


#чтение данных ДТМРТ
reader2 = vtk.vtkGenericDataObjectReader()
reader2.SetFileName(r"DTMRI_DATA/Normal human/DTI060904/vector_field.vtk")
reader2.Update()
ug2 = reader2.GetOutput()
points2 = ug2.GetPoints()
coords_vectors_data = vtk_to_numpy(ug2.GetPointData().GetArray('DTMRIFiberOrientation'))
coord_points_data = vtk_to_numpy(points2.GetData())
#построение дерева
tree = KDTree(coord_points_data, leaf_size=5, metric='euclidean')

print coord_points_data[150]
a = boneLocator.FindCell(coord_points_data[150])
print a

ele_array = read_ele_file()
s =  ele_array[0]
a = s.split("  ")
N = len(ele_array) - 1
l = len(ele_array)
s2 = ele_array[1]
b = s2.split(' ')
print int(b[4]), int(b[7]), int(b[8]), int(b[9]), int(b[10])
#print len(ele_array)

node_array = read_node_file()
s3 = node_array[1]
b2 = s3.split(' ')
#print b2
#print int(b2[3]), float(b2[7]), float(b2[9]), float(b2[11])


cell_array = np.zeros((N))
cell_vectors = np.zeros((N, 3))



n = 0
for i in xrange(len(coord_points_data)):
    a = boneLocator.FindCell(coord_points_data[i])
    if a != -1:
        #print a
        n += 1
        cell_array[a] += 1
        cell_vectors[a] = cell_vectors[a] + coord_points_data[i]
        #print cell_vectors[a]

for i in xrange(N):
    if cell_array[i] != 0:
        vec_help = cell_vectors[i]/float(cell_array[i])
        cell_vectors[i] = vec_help/np.linalg.norm(vec_help)
        #print cell_vectors[a]




#print n

p = 0
#print cell_array
for i in xrange(N):
    if cell_array[i] != 0:
         p += 1

#print p
#print p*100/l, '%'
#print int(a[0])

for i in xrange(N):
    if cell_array[i] == 0:

        numb_cell1, numb_cell2, numb_cell3, numb_cell4 = list_cells(ele_array[i])


        x1, y1, z1 = list_points(node_array[numb_cell1])
        x2, y2, z2 = list_points(node_array[numb_cell2])
        x3, y3, z3 = list_points(node_array[numb_cell3])
        x4, y4, z4 = list_points(node_array[numb_cell4])

        x, y, z = coord_centre_of_thetraedra([x1,y1,z1, x2,y2,z2, x3,y3,z3, x4,y4,z4])
        dist, ind = tree.query((x, y, z), k=4)
        #print dist[0], ind[0]
        vx, vy, vz = vector_in_centre_thetraedr(dist[0], coord_points_data[ind[0][0]],
                                                         coord_points_data[ind[0][1]],
                                                         coord_points_data[ind[0][2]],
                                                         coord_points_data[ind[0][3]])
        cell_vectors[i][0] = vx
        cell_vectors[i][1] = vy
        cell_vectors[i][2] = vz

print ele_array[1], list_cells(ele_array[1])
print node_array[0], list_points(node_array[0])

write_axi(N, cell_vectors)