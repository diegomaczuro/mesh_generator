# coding=utf-8
__author__ = 'Anastasia Bazhutina'
import scipy.io
from vtk import *
from vtk.util.misc import vtkGetDataRoot
import numpy as np
from vtk.util.numpy_support import vtk_to_numpy

# The source file
file_name = "VTK_DATA/3d.1.vtk"


# Read the source file.
reader = vtkUnstructuredGridReader()
reader.SetFileName(file_name)
reader.Update()  # Needed because of GetScalarRange
output = reader.GetOutput()
points = output.GetPoints()
scalar_range = output.GetScalarRange()
coord_points_model = vtk_to_numpy(points.GetData())
#print coord_points_model[0]


VTK_DATA_ROOT = vtkGetDataRoot()

boneLocator = vtk.vtkCellLocator()
boneLocator.SetDataSet(output)
#x = np.array([1, 1, 1])
boneLocator.BuildLocator()

a = boneLocator.FindCell([1.,1.,0.])
print a
mat11 = scipy.io.loadmat('DTMRI_DATA/Normal human/DTI060904/v11.mat')
b11 = mat11['v11']
mat12 = scipy.io.loadmat('DTMRI_DATA/Normal human/DTI060904/v12.mat')
b12 = mat12['v12']
mat13 = scipy.io.loadmat('DTMRI_DATA/Normal human/DTI060904/v13.mat')
b13 = mat13['v13']
