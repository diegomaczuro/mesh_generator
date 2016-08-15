# -*- coding: utf_8 -*-
__author__ = 'Aastasia Bazhutina'
import numpy as np

def write_geo(file_name, *param):
    x = param[0]
    y = param[1]
    z = param[2]
    connection = param[3]
    apex = param[4]
    x2 = param[5]
    y2 = param[6]
    z2 = param[7]
    connection2 = param[8]
    apex2 = param[9]
    border = param[10]
    size_cell = param[11]

    with open(str(file_name)+'.geo', "w") as out_mesh:

                str_ =  '''Mesh.CharacteristicLengthFromCurvature = 1;
Mesh.Lloyd = 1;
Mesh.CharacteristicLengthMin = 3;
Mesh.CharacteristicLengthMax = 6;
Mesh.Optimize = 1;
Mesh.OptimizeNetgen = 1;

/*Remeshing using discrete parametrization (0=harmonic_circle, 1=conformal_spectral, 2=rbf, 3=harmonic_plane, 4=convex_circle, 5=convex_plane, 6=harmonic square, 7=conformal_fe*/
/*Default value: 4*/
Mesh.RemeshParametrization = 7;

Mesh.SurfaceFaces = 1;
Mesh.CharacteristicLengthFactor = 0.4;
Mesh.RemeshAlgorithm = 1;'''
                print str_
                out_mesh.write(str_)
                #точки внешней поверхность
                str_points = 'Point(1) = {' + str(apex[0]) + ', ' + str(apex[1]) + ', ' + str(apex[2]) + \
                                     ', ' + str(size_cell) + '};\n'
                out_mesh.write(str_points)
                out_mesh.write('\n')
                for i in xrange(len(x)):
                    for j in xrange(len(x[0])):
                        str_points = 'Point(' + str(connection[i][j]) + ') = {' + str(x[i][j]) + ', '+str(y[i][j]) + ', ' + str(z[i][j]) + \
                                     ', ' + str(size_cell) + '};\n'
                        print str_points
                        out_mesh.write(str_points)

                out_mesh.write('\n')
                ind_for_line = 1
                ind_line = ind_for_line
                #точки внутренняя поверхность
                str_points = 'Point(' + str(len(x)*len(x[0])+2) + ') = {' + str(apex2[0]) + ', ' + str(apex2[1]) + ', ' \
                             + str(apex2[2]) + ', ' + str(size_cell) + '};\n'
                out_mesh.write(str_points)
                out_mesh.write('\n')
                for i in xrange(len(x2)):
                    for j in xrange(len(x2[0])):
                        str_points = 'Point(' + str(connection2[i][j]) + ') = {' + str(x2[i][j]) + ', '+str(y2[i][j]) + ', ' + str(z2[i][j]) + \
                                     ', ' + str(size_cell) + '};\n'
                        print str_points
                        out_mesh.write(str_points)

                out_mesh.write('\n')

                #линии соединения внешней поверхности
                for i in xrange(len(x)//2-1):
                    connect_i = np.append(connection[i], connection[i+len(x)//2])
                    connect_j = np.append(connection[i+1], connection[i+len(x)//2 + 1])
                    for j in xrange(len(connect_i)-1):
                        if j == 0:
                            str_splines = 'Line(' + str(ind_for_line) + ') = {1, ' + str(connect_i[j]) + '};\n'
                            ind_for_line += 1
                            print str_splines
                            out_mesh.write(str_splines)
                            str_splines = 'Line(' + str(ind_for_line) + ') = {' + str(connect_i[j]) + ', ' + str(connect_j[j]) + '};\n'
                            ind_for_line += 1
                            print str_splines
                            out_mesh.write(str_splines)
                            str_splines = 'Line(' + str(ind_for_line) + ') = {' +str(connect_j[j]) +  ', 1};\n'
                            ind_for_line += 1
                            print str_splines
                            out_mesh.write(str_splines)


                        str_splines = 'Line(' + str(ind_for_line) + ') = {' + str(connect_i[j]) + ', ' + str(connect_i[j+1]) + '};\n'
                        ind_for_line += 1
                        print str_splines
                        out_mesh.write(str_splines)
                        str_splines = 'Line(' + str(ind_for_line) + ') = {' + str(connect_i[j+1]) + ', ' + str(connect_j[j+1]) + '};\n'
                        ind_for_line += 1
                        print str_splines
                        out_mesh.write(str_splines)
                        str_splines = 'Line(' + str(ind_for_line) + ') = {' + str(connect_j[j+1]) + ', ' + str(connect_j[j]) + '};\n'
                        ind_for_line += 1
                        print str_splines
                        out_mesh.write(str_splines)
                        str_splines = 'Line(' + str(ind_for_line) + ') = {' + str(connect_j[j]) + ', ' + str(connect_i[j]) + '};\n'
                        ind_for_line += 1
                        print str_splines
                        out_mesh.write(str_splines)

                        if j == len(connect_i)-2:
                            str_splines = 'Line(' + str(ind_for_line) + ') = {' + str(connect_i[j+1]) + ', ' + str(border[i]) + '};\n'
                            ind_for_line += 1
                            print str_splines
                            out_mesh.write(str_splines)
                            str_splines = 'Line(' + str(ind_for_line) + ') = {' + str(border[i]) + ', ' + str(border[i+1]) + '};\n'
                            ind_for_line += 1
                            print str_splines
                            out_mesh.write(str_splines)
                            str_splines = 'Line(' + str(ind_for_line) + ') = {' + str(border[i+1]) + ', ' + str(connect_j[j+1]) + '};\n'
                            ind_for_line += 1
                            print str_splines
                            out_mesh.write(str_splines)
                            str_splines = 'Line(' + str(ind_for_line) + ') = {' + str(connect_j[j+1]) + ', ' + str(connect_i[j+1]) + '};\n'
                            ind_for_line += 1
                            print str_splines
                            out_mesh.write(str_splines)


                    #"закрывание" последнего угла по phi
                    if i == (len(x)//2-2):
                        connect_i = np.append(connection[i+1], connection[i+len(x)//2+1])
                        connect_j = np.append(connection[0], connection[len(x)//2])
                        for j in xrange(len(connect_i)-1):
                            if j == 0:
                                str_splines = 'Line(' + str(ind_for_line) + ') = {1, ' + str(connect_i[j]) + '};\n'
                                ind_for_line += 1
                                print str_splines
                                out_mesh.write(str_splines)
                                str_splines = 'Line(' + str(ind_for_line) + ') = {' + str(connect_i[j]) + ', ' + str(connect_j[j]) + '};\n'
                                ind_for_line += 1
                                print str_splines
                                out_mesh.write(str_splines)
                                str_splines = 'Line(' + str(ind_for_line) + ') = {' +str(connect_j[j]) +  ', 1};\n'
                                ind_for_line += 1
                                print str_splines
                                out_mesh.write(str_splines)

                            str_splines = 'Line(' + str(ind_for_line) + ') = {' + str(connect_i[j]) + ', ' + str(connect_i[j+1]) + '};\n'
                            ind_for_line += 1
                            print str_splines
                            out_mesh.write(str_splines)
                            str_splines = 'Line(' + str(ind_for_line) + ') = {' + str(connect_i[j+1]) + ', ' + str(connect_j[j+1]) + '};\n'
                            ind_for_line += 1
                            print str_splines
                            out_mesh.write(str_splines)
                            str_splines = 'Line(' + str(ind_for_line) + ') = {' + str(connect_j[j+1]) + ', ' + str(connect_j[j]) + '};\n'
                            ind_for_line += 1
                            print str_splines
                            out_mesh.write(str_splines)
                            str_splines = 'Line(' + str(ind_for_line) + ') = {' + str(connect_j[j]) + ', ' + str(connect_i[j]) + '};\n'
                            ind_for_line += 1
                            print str_splines
                            out_mesh.write(str_splines)

                            if j == len(connect_i)-2:
                                str_splines = 'Line(' + str(ind_for_line) + ') = {' + str(connect_i[j+1]) + ', ' + str(border[i+1]) + '};\n'
                                ind_for_line += 1
                                print str_splines
                                out_mesh.write(str_splines)
                                str_splines = 'Line(' + str(ind_for_line) + ') = {' + str(border[i+1]) + ', ' + str(border[0]) + '};\n'
                                ind_for_line += 1
                                print str_splines
                                out_mesh.write(str_splines)
                                str_splines = 'Line(' + str(ind_for_line) + ') = {' + str(border[0]) + ', ' + str(connect_j[j+1]) + '};\n'
                                ind_for_line += 1
                                print str_splines
                                out_mesh.write(str_splines)
                                str_splines = 'Line(' + str(ind_for_line) + ') = {' + str(connect_j[j+1]) + ', ' + str(connect_i[j+1]) + '};\n'
                                ind_for_line += 1
                                print str_splines
                                out_mesh.write(str_splines)


                out_mesh.write('\n')

                ind_line2 = ind_for_line

                #линии соединения внутренней поверхности
                for i in xrange(len(x2)//2-1):
                    connect_i = np.append(connection2[i], connection2[i+len(x2)//2])
                    connect_j = np.append(connection2[i+1], connection2[i+len(x2)//2 + 1])
                    for j in xrange(len(connect_i)-1):
                        if j == 0:
                            str_splines = 'Line(' + str(ind_for_line) + ') = {' + str(len(x)*len(x[0])+2) + ', ' + str(connect_i[j]) + '};\n'
                            ind_for_line += 1
                            print str_splines
                            out_mesh.write(str_splines)
                            str_splines = 'Line(' + str(ind_for_line) + ') = {' + str(connect_i[j]) + ', ' + str(connect_j[j]) + '};\n'
                            ind_for_line += 1
                            print str_splines
                            out_mesh.write(str_splines)
                            str_splines = 'Line(' + str(ind_for_line) + ') = {' + str(connect_j[j]) + ', ' + str(len(x)*len(x[0])+2) + '};\n'
                            ind_for_line += 1
                            print str_splines
                            out_mesh.write(str_splines)

                        str_splines = 'Line(' + str(ind_for_line) + ') = {' + str(connect_i[j]) + ', ' + str(connect_i[j+1]) + '};\n'
                        ind_for_line += 1
                        print str_splines
                        out_mesh.write(str_splines)
                        str_splines = 'Line(' + str(ind_for_line) + ') = {' + str(connect_i[j+1]) + ', ' + str(connect_j[j+1]) + '};\n'
                        ind_for_line += 1
                        print str_splines
                        out_mesh.write(str_splines)
                        str_splines = 'Line(' + str(ind_for_line) + ') = {' + str(connect_j[j+1]) + ', ' + str(connect_j[j]) + '};\n'
                        ind_for_line += 1
                        print str_splines
                        out_mesh.write(str_splines)
                        str_splines = 'Line(' + str(ind_for_line) + ') = {' + str(connect_j[j]) + ', ' + str(connect_i[j]) + '};\n'
                        ind_for_line += 1
                        print str_splines
                        out_mesh.write(str_splines)


                    #"закрывание" последнего угла по phi
                    if i == (len(x2)//2-2):
                        connect_i = np.append(connection2[i+1], connection2[i+len(x)//2+1])
                        connect_j = np.append(connection2[0], connection2[len(x)//2])
                        for j in xrange(len(connect_i)-1):
                            if j == 0:
                                str_splines = 'Line(' + str(ind_for_line) + ') = {' + str(len(x)*len(x[0])+2) + ', ' + str(connect_i[j]) + '};\n'
                                ind_for_line += 1
                                print str_splines
                                out_mesh.write(str_splines)
                                str_splines = 'Line(' + str(ind_for_line) + ') = {' + str(connect_i[j]) + ', ' + str(connect_j[j]) + '};\n'
                                ind_for_line += 1
                                print str_splines
                                out_mesh.write(str_splines)
                                str_splines = 'Line(' + str(ind_for_line) + ') = {' + str(connect_j[j]) + ', ' + str(len(x)*len(x[0])+2) + '};\n'
                                ind_for_line += 1
                                print str_splines
                                out_mesh.write(str_splines)

                            str_splines = 'Line(' + str(ind_for_line) + ') = {' + str(connect_i[j]) + ', ' + str(connect_i[j+1]) + '};\n'
                            ind_for_line += 1
                            print str_splines
                            out_mesh.write(str_splines)
                            str_splines = 'Line(' + str(ind_for_line) + ') = {' + str(connect_i[j+1]) + ', ' + str(connect_j[j+1]) + '};\n'
                            ind_for_line += 1
                            print str_splines
                            out_mesh.write(str_splines)
                            str_splines = 'Line(' + str(ind_for_line) + ') = {' + str(connect_j[j+1]) + ', ' + str(connect_j[j]) + '};\n'
                            ind_for_line += 1
                            print str_splines
                            out_mesh.write(str_splines)
                            str_splines = 'Line(' + str(ind_for_line) + ') = {' + str(connect_j[j]) + ', ' + str(connect_i[j]) + '};\n'
                            ind_for_line += 1
                            print str_splines
                            out_mesh.write(str_splines)




                out_mesh.write('\n')
                ind_line_loop = ind_for_line

                #циклы для внешней поверхности
                for i in xrange(len(x)//2):

                    for j in xrange(len(connect_i)):
                        if j == 0:
                            str_line_loop = 'Line Loop(' + str(ind_for_line) + ') = {' + str(ind_line) + ', ' + \
                                            str(ind_line + 1) + ', ' + str(ind_line + 2) + '};\n'
                            ind_for_line += 1
                            ind_line += 3
                            print str_line_loop
                            out_mesh.write(str_line_loop)


                        str_line_loop = 'Line Loop(' + str(ind_for_line) + ') = {' + str(ind_line) + ', ' + \
                                        str(ind_line + 1) + ', ' + str(ind_line + 2) + ', ' + str(ind_line + 3) + '};\n'
                        ind_for_line += 1
                        ind_line += 4
                        print str_line_loop
                        out_mesh.write(str_line_loop)

                out_mesh.write('\n')

                ind_line_loop2 = ind_for_line

                #циклы для внутренней поверхности
                for i in xrange(len(x)//2):

                    for j in xrange(len(connect_i)-1):
                        if j == 0:
                            str_line_loop = 'Line Loop(' + str(ind_for_line) + ') = {' + str(ind_line2) + ', ' + \
                                            str(ind_line2 + 1) + ', ' + str(ind_line2 + 2) + '};\n'
                            ind_for_line += 1
                            ind_line2 += 3
                            print str_line_loop
                            out_mesh.write(str_line_loop)


                        str_line_loop = 'Line Loop(' + str(ind_for_line) + ') = {' + str(ind_line2) + ', ' + \
                                        str(ind_line2 + 1) + ', ' + str(ind_line2 + 2) + ', ' + str(ind_line2 + 3) + '};\n'
                        ind_for_line += 1
                        ind_line2 += 4
                        print str_line_loop
                        out_mesh.write(str_line_loop)

                out_mesh.write('\n')

                ind_line_loop2_end = ind_for_line

                #запись ячеек внешней поверхности
                list_ruled_surface1 = []
                for i in xrange(ind_line_loop2-ind_line_loop):
                    str_ruled_surface = 'Ruled Surface(' + str(ind_for_line) + ') = {' + str(ind_line_loop) + '};\n'
                    list_ruled_surface1.append(ind_for_line)
                    ind_for_line += 1
                    ind_line_loop += 1
                    print str_ruled_surface
                    out_mesh.write(str_ruled_surface)

                out_mesh.write('\n')


                #запись ячеек внутренней поверхности
                list_ruled_surface2 = []
                for i in xrange(ind_line_loop2_end-ind_line_loop2):
                    str_ruled_surface = 'Ruled Surface(' + str(ind_for_line) + ') = {' + str(ind_line_loop2) + '};\n'
                    list_ruled_surface2.append(ind_for_line)
                    ind_for_line += 1
                    ind_line_loop2 += 1
                    print str_ruled_surface
                    out_mesh.write(str_ruled_surface)

                out_mesh.write('\n')


                #внешняя поверхность
                str_surface_loop_1 = str(list_ruled_surface1)
                str_surface_loop_2 = str_surface_loop_1.replace('[', '{')
                str_surface_loop_3 = str_surface_loop_2.replace(']', '}')
                str_surface_loop1 = 'Surface Loop(' + str(ind_for_line) + ') = ' + str_surface_loop_3 + ';\n'
                print str_surface_loop1
                out_mesh.write(str_surface_loop1)
                out_mesh.write('\n')
                ind_for_line += 1

                #внутренняя поверхность
                str_surface_loop_1 = str(list_ruled_surface2)
                str_surface_loop_2 = str_surface_loop_1.replace('[', '{')
                str_surface_loop_3 = str_surface_loop_2.replace(']', '}')
                str_surface_loop1 = 'Surface Loop(' + str(ind_for_line) + ') = ' + str_surface_loop_3 + ';\n'
                print str_surface_loop1
                out_mesh.write(str_surface_loop1)
                out_mesh.write('\n')
                ind_for_line += 1

                #запись объема
                str_volume = 'Volume(' + str(ind_for_line) + ') = {' + str(ind_for_line-2) + ', ' + str(ind_for_line-1) + '};\n'
                out_mesh.write(str_volume)

