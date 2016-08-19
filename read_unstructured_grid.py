# coding=utf-8
__author__ = 'Anastasia Bazhutina'
import scipy.io
from vtk import *
from vtk.util.misc import vtkGetDataRoot
import numpy as np
from vtk.util.numpy_support import vtk_to_numpy


def read_ele_file():
    with open('MESH_DATA_MODEL/Normal human/DTI060904/mesh.1.ele') as my_file:
        ele_array = my_file.readlines()
    return ele_array


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

print coord_points_data[150]
a = boneLocator.FindCell(coord_points_data[150])
print a

ele_array = read_ele_file()
s =  ele_array[0]
a = s.split("  ")
print int(a[0])
l = int(a[0])
s2 = ele_array[1]
b = s2.split(' ')
#print int(b[4]), int(b[7]), int(b[8]), int(b[9]), int(b[10])
#print len(ele_array)
cell_array = np.zeros((int(a[0])))

n = 0
for i in xrange(len(coord_points_data)):
    a = boneLocator.FindCell(coord_points_data[i])
    if a != -1:
        #print a
        n += 1
        cell_array[a] += 1


#print n

p = 0
#print cell_array
for i in xrange(len(cell_array)):
    if cell_array[i] != 0:
         p += 1

print p
print p*100/l, '%'
#print int(a[0])