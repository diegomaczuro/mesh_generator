__author__ = 'Aastasia Bazhutina'
import numpy as np

def write_geo(file_name, *param):
    x = param[0]
    y = param[1]
    z = param[2]
    print len(x), len(x[0])
    connection = param[3]
    size_cell = param[4]
    apex = param[5]
    with open(str(file_name)+'.geo', "w") as out_mesh:
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

                out_mesh.write('\n')

                ind_line_loop = ind_for_line
                for i in xrange(len(x)//2):

                    for j in xrange(len(connect_i)-1):
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


                list_ruled_surface = []
                for i in xrange(ind_for_line-ind_line_loop):
                    str_ruled_surface = 'Ruled Surface(' + str(ind_for_line) + ') = {' + str(ind_line_loop) + '};\n'
                    list_ruled_surface.append(ind_for_line)
                    ind_for_line += 1
                    ind_line_loop += 1
                    print str_ruled_surface
                    out_mesh.write(str_ruled_surface)

                out_mesh.write('\n')


                str_surface_loop_1 = str(list_ruled_surface)
                str_surface_loop_2 = str_surface_loop_1.replace('[', '{')
                str_surface_loop_3 = str_surface_loop_2.replace(']', '}')
                str_surface_loop = 'Surface Loop(' + str(ind_for_line) + ') = ' + str_surface_loop_3 + ';\n'
                print str_surface_loop
                out_mesh.write(str_surface_loop)

                out_mesh.write('\n')
