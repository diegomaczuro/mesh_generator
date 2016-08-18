# -*- coding: utf_8 -*-
__author__ = 'Anastasia Bazhutina'
import numpy as np
import scipy.io
from sklearn.neighbors import KDTree
import pickle
from const import *



each_x_y = 1
each_z = 1

mat1 = scipy.io.loadmat('DTMRI_DATA/Normal human/DTI060904/e1.mat')
e1 = mat1['e1']
mat2 = scipy.io.loadmat('DTMRI_DATA/Normal human/DTI060904/e2.mat')
e2 = mat2['e2']
mat3 = scipy.io.loadmat('DTMRI_DATA/Normal human/DTI060904/e3.mat')
e3 = mat3['e3']
mat11 = scipy.io.loadmat('DTMRI_DATA/Normal human/DTI060904/v11.mat')

b11 = mat11['v11']
mat12 = scipy.io.loadmat('DTMRI_DATA/Normal human/DTI060904/v12.mat')
b12 = mat12['v12']
mat13 = scipy.io.loadmat('DTMRI_DATA/Normal human/DTI060904/v13.mat')
b13 = mat13['v13']


#прореживание
e1 = e1[::each_x_y][:,::each_x_y][:,:,::each_z]
e2 = e2[::each_x_y][:,::each_x_y][:,:,::each_z]
e3 = e3[::each_x_y][:,::each_x_y][:,:,::each_z]
b11 = b11[::each_x_y][:,::each_x_y][:,:,::each_z]
b12 = b12[::each_x_y][:,::each_x_y][:,:,::each_z]
b13 = b13[::each_x_y][:,::each_x_y][:,:,::each_z]


len1 = len(b11)
len2 = len(b11[0])
len3 = len(b11[0][0])
len_ = len1*len2*len3

results_points = np.array([])
results_vectors = np.array([])

print "Read finish"

multiply_x = 0.3*0.1 # Коэфициент переводящий в см
multiply_y = 0.3*0.1
multiply_z = 0.8*0.1 #0.8*0.1
valuable = 0
for i in xrange(0, len1):
        for j in xrange(0, len2):
            for k in xrange(0, len3):
                if e3[i][j][k] >= MASK_THRESHOLD:
                    valuable += 1

with open('DTMRI_DATA/Normal human/DTI060904/vector_field.vtk', 'w') as out_mesh:

    out_mesh.write("# vtk DataFile Version 2.0\n")
    out_mesh.write("Really cool data\n")
    out_mesh.write("ASCII\n")
    out_mesh.write("DATASET UNSTRUCTURED_GRID\n")
    out_mesh.write("POINTS {pcount} double\n".format(pcount=valuable))
    for i in xrange(0, len1):
        for j in xrange(0, len2):
            for k in xrange(0, len3):
                if e3[i][j][k] >= MASK_THRESHOLD:
                    out_mesh.write("{0} {1} {2}\n".format(multiply_x*each_x_y*i, multiply_y*each_x_y*j, multiply_z*each_z*k))

    out_mesh.write("CELLS {pcount} {pcount2}\n".format(pcount=valuable, pcount2=valuable*2))
    for j in xrange(valuable):
        out_mesh.write("1 {0}\n".format(j))
    out_mesh.write("CELL_TYPES {pcount}\n".format(pcount=valuable))
    for k in xrange(valuable):
        out_mesh.write("1\n")
    out_mesh.write("POINT_DATA {pcount}\n".format(pcount=valuable))
    out_mesh.write("VECTORS DTMRIFiberOrientation double\n")
    for i in xrange(0, len1):
        for j in xrange(0, len2):
            for k in xrange(0, len3):
                if e3[i][j][k] >= MASK_THRESHOLD:
                    out_mesh.write("{0} {1} {2}\n".format(b11[i][j][k], b12[i][j][k], b13[i][j][k]))
