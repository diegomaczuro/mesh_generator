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
mat21 = scipy.io.loadmat('DTMRI_DATA/Normal human/DTI060904/v21.mat')

b21 = mat21['v21']
mat22 = scipy.io.loadmat('DTMRI_DATA/Normal human/DTI060904/v22.mat')
b22 = mat22['v22']
mat23 = scipy.io.loadmat('DTMRI_DATA/Normal human/DTI060904/v23.mat')
b23 = mat23['v23']
mat31 = scipy.io.loadmat('DTMRI_DATA/Normal human/DTI060904/v31.mat')

b31 = mat31['v31']
mat32 = scipy.io.loadmat('DTMRI_DATA/Normal human/DTI060904/v32.mat')
b32 = mat32['v32']
mat33 = scipy.io.loadmat('DTMRI_DATA/Normal human/DTI060904/v33.mat')
b33 = mat33['v33']


#прореживание
e1 = e1[::each_x_y][:,::each_x_y][:,:,::each_z]
e2 = e2[::each_x_y][:,::each_x_y][:,:,::each_z]
e3 = e3[::each_x_y][:,::each_x_y][:,:,::each_z]
b11 = b11[::each_x_y][:,::each_x_y][:,:,::each_z]
b12 = b12[::each_x_y][:,::each_x_y][:,:,::each_z]
b13 = b13[::each_x_y][:,::each_x_y][:,:,::each_z]
b21 = b21[::each_x_y][:,::each_x_y][:,:,::each_z]
b22 = b22[::each_x_y][:,::each_x_y][:,:,::each_z]
b23 = b23[::each_x_y][:,::each_x_y][:,:,::each_z]

#b31 =  b31[::each_x_y][:,::each_x_y][:,:,::each_z]
#b32 =  b32[::each_x_y][:,::each_x_y][:,:,::each_z]
#b33 =  b33[::each_x_y][:,::each_x_y][:,:,::each_z]


len1 = len(b11)
len2 = len(b11[0])
len3 = len(b11[0][0])
len_ = len1*len2*len3

fiber_x = e1[::each_x_y][:,::each_x_y][:,:,::each_z]
fiber_y = e2[::each_x_y][:,::each_x_y][:,:,::each_z]
fiber_z = e3[::each_x_y][:,::each_x_y][:,:,::each_z]
fiber_a = np.zeros((len1, len2, len3))
fiber_b = np.zeros((len1, len2, len3))
fiber_c = np.zeros((len1, len2, len3))


mat_diffus = np.zeros((len1, len2, len3))

#for i in xrange(0, len1):
#    for j in xrange(0, len2):
#        for k in xrange(0, len3):
#            mat = np.matrix([[b11[i][j][k], b12[i][j][k], b13[i][j][k]],
#                            [b21[i][j][k], b22[i][j][k], b23[i][j][k]],
#                            [b31[i][j][k], b32[i][j][k], b33[i][j][k]]])
#
#            mat = np.matrix((mat + mat.transpose()) / 2)
#
#            e = np.linalg.eig(mat)
#
#            res = e[1][0]
#
#            if (e[0][0]) > (e[0][1]) and (e[0][0]) > (e[0][2]):
#                res = e[1][0]
#            elif (e[0][1]) > (e[0][0]) and (e[0][1]) > (e[0][2]):
#                res = e[1][1]
#            elif (e[0][2]) > (e[0][1]) and (e[0][2]) > (e[0][0]):
#                res = e[1][2]
#            #print e
#            fiber_a[i][j][k] = np.array(res)[0][0]
#            fiber_b[i][j][k] = np.array(res)[0][1]
#            fiber_c[i][j][k] = np.array(res)[0][2]
#

results_points = np.array([])
results_vectors = np.array([])

multiply_x = 0.3*0.1
multiply_y = 0.3*0.1
multiply_z = 0.3*0.1 #0.8*0.1
valuable = 0
for i in xrange(0, len1):
        for j in xrange(0, len2):
            for k in xrange(0, len3):
                if e3[i][j][k] >= MASK_THRESHOLD:#e3[each_x_y*i][each_x_y*j][each_z*k] >= 6*10**(-6):
                    valuable += 1

with open('vector_field.vtk', 'w') as out_mesh:

    out_mesh.write("# vtk DataFile Version 2.0\n")
    out_mesh.write("Really cool data\n")
    out_mesh.write("ASCII\n")
    out_mesh.write("DATASET UNSTRUCTURED_GRID\n")
    out_mesh.write("POINTS {pcount} double\n".format(pcount=valuable))
    for i in xrange(0, len1):
        for j in xrange(0, len2):
            for k in xrange(0, len3):
                if e3[i][j][k] >= MASK_THRESHOLD:#e3[each_x_y*i][each_x_y*j][each_z*k] >= 5*10**(-6):

                    results_points = np.append(results_points, [multiply_x*each_x_y*i, multiply_y*each_x_y*j, multiply_z*2.27*each_z*k])
                    #print v[0, 0], v[0, 1], v[0, 2]
                    out_mesh.write("{0} {1} {2}\n".format(multiply_x*each_x_y*i, multiply_y*each_x_y*j, multiply_z*2.27*each_z*k))

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
                if e3[i][j][k] >= MASK_THRESHOLD:#e3[each_x_y*i][each_x_y*j][each_z*k] >= 6*10**(-6):

                    results_vectors = np.append(results_vectors, [b11[i][j][k], b12[i][j][k], b13[i][j][k]])
                    out_mesh.write("{0} {1} {2}\n".format(b11[i][j][k], b12[i][j][k], b13[i][j][k]))
                    #out_mesh.write("{0} {1} {2}\n".format(b11[each_x_y*i][each_x_y*j][each_z*k], b12[each_x_y*i][each_x_y*j][each_z*k], b13[each_x_y*i][each_x_y*j][each_z*k]))


results_points.shape = ((len(results_points)//3), 3)
results_vectors.shape = ((len(results_vectors)//3), 3)
#print len(results_points),len(results_vectors)


#tree = KDTree(results_points, leaf_size=5, metric='euclidean')
#tree2 = KDTree(results_vectors, leaf_size=5, metric='euclidean')
#dist, ind = tree.query((100, 100, 100), k=1)
##c = tree.get_arrays()
##tree_points = c[0]
##print tree_points[2508]
##print dist[0][0], results_points[ind[0][0]]
#s = pickle.dumps(tree)
#tree_copy = pickle.loads(s)
#

#with open('data2.vtk', 'w') as out_mesh:
#        out_mesh.write("# vtk DataFile Version 2.0\n")
#        out_mesh.write("Really cool data\n")
#        out_mesh.write("ASCII\n")
#        out_mesh.write("DATASET UNSTRUCTURED_GRID\n")
#        out_mesh.write("POINTS {pcount} float\n".format(pcount=m))
#        for i in range(255):
#            for j in range(255):
#                for k in range(129):
#                    if b[i][j][k] >= 6*10**(-6):
#                        out_mesh.write("{0} {1} {2}\n".format(i, j, 2.27*k))#2.27*z))
#                        #m = m+1
#        out_mesh.write("CELLS {pcount} {pcount2}\n".format(pcount=m, pcount2=m*2))
#        for j in range(m):
#            out_mesh.write("1 {0}\n".format(j))
#        out_mesh.write("CELL_TYPES {pcount}\n".format(pcount=m))
#        for k in range(m):
#            out_mesh.write("1 ")
#
#print m


#len_ = len(b11)
#
