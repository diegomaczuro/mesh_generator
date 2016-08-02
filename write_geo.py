__author__ = 'Aastasia Bazhutina'

def write_geo(file_name, *param):
    x = param[0]
    y = param[1]
    z = param[2]
    print len(x), len(x[0])
    connection = param[3]
    size_cell = param[4]
    apex = param[5]
    with open(str(file_name)+'.geo', "w") as out_mesh:
                str_points = 'Point(1) = {' + str(apex[0]) + ', '+str(apex[1]) + ', ' + str(apex[2]) + \
                                     ', ' + str(size_cell) +'};\n'
                out_mesh.write(str_points)
                out_mesh.write('\n')
                for i in xrange(len(x)):
                    for j in xrange(len(x[0])):
                        str_points = 'Point(' + str(connection[i][j]) + ') = {' + str(x[i][j]) + ', '+str(y[i][j]) + ', ' + str(z[i][j]) + \
                                     ', ' + str(size_cell) +'};\n'
                        print str_points
                        out_mesh.write(str_points)
                out_mesh.write('\n')
                ind_for_line = 1
                ind_even = 0
                bridge = []
                for i in xrange(len(x)//2):

                    comma = len(connection[i])-1
                    if ind_even == 1:
                        connect1 = connection[i+len(x)//2]
                        connect_apex = connect1[::-1]
                        connect2 = connection[i]
                        connect_base = connect2[::-1]
                        ind_even = 0
                        list_points = '{'
                        bridge.append(connect_apex[0])
                    else:
                        connect_apex = connection[i]
                        connect_base = connection[i+len(x)//2]
                        ind_even = 1
                        list_points = '{1, '
                        bridge.append(connect_base[-1])

                    for j in xrange(len(connect_apex)):
                        list_points = list_points + str(connect_apex[j])+', '

                    for j in xrange(len(connect_base)):
                        list_points = list_points + str(connect_base[j])
                        if comma != j:
                            list_points = list_points + ', '
                    if ind_even == 0:
                        list_points = list_points + ', 1};\n'
                    else:
                        list_points = list_points + '};\n'

                    str_splines = 'Spline(' + str(ind_for_line) + ') = ' + list_points


                    print str_splines
                    out_mesh.write(str_splines)
                    ind_for_line += 1
                bridge.append(bridge[0])
                ind_even = 0
                for i in xrange(len(bridge)-1):
                    if ind_even == 0:
                        str_splines = 'Spline(' + str(ind_for_line) + ') = {' + str(bridge[i]) + ', ' + str(bridge[i+1]) + '};\n'
                        ind_even = 1
                    else:
                        str_splines = 'Spline(' + str(ind_for_line) + ') = {' + str(bridge[i+1]) + ', ' + str(bridge[i]) + '};\n'
                        ind_even = 0
                    print str_splines
                    out_mesh.write(str_splines)
                    ind_for_line += 1

                out_mesh.write('\n')
                ind_for_spline = 1
                ind_even = 0
                ind_for_surface = ind_for_line


                for i in xrange(len(x)//2):
                    if ind_even == 0:

                        str_loop = 'Line Loop(' + str(ind_for_line) +') = {' + str(ind_for_spline) + ', ' + str(ind_for_spline+len(x)//2) \
                               + ', ' + str(ind_for_spline+1) + '};\n'
                        ind_even = 1
                    else:
                        if i == (len(x)//2 - 1):
                            str_loop = 'Line Loop(' + str(ind_for_line) +') = {' + str(ind_for_spline) + ', 1, ' + str(ind_for_spline+len(x)//2) + '};\n'
                        else:
                            str_loop = 'Line Loop(' + str(ind_for_line) +') = {' + str(ind_for_spline) + ', ' + str(ind_for_spline+1) \
                               + ', ' +  str(ind_for_spline+len(x)//2) + '};\n'
                        ind_even = 0
                    print str_loop
                    out_mesh.write(str_loop)
                    ind_for_line += 1
                    ind_for_spline += 1

                out_mesh.write('\n')
                surface_loop1 = []

                for i in xrange(len(x)//2):
                    str_for_surface = 'Ruled Surface(' + str(ind_for_line) + ') = {' + str(ind_for_surface) +'};\n'
                    surface_loop1.append(ind_for_line)
                    ind_for_line += 1
                    ind_for_surface += 1
                    print str_for_surface
                    out_mesh.write(str_for_surface)
                out_mesh.write('\n')
                str1_surface_loop1 = str(surface_loop1)
                str2_surface_loop1 = str1_surface_loop1.replace('[', '{')
                str3_surface_loop1 = str2_surface_loop1.replace(']', '}')
                str_surface_loop = 'Surface Loop(' + str(ind_for_line) + ') = ' +  str3_surface_loop1 + ';\n'
                print str_surface_loop
                out_mesh.write(str_surface_loop)
                ind_for_line += 1