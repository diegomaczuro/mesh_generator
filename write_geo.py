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

                for i in xrange((len(x))//2):

                    comma = len(connection[i])-1
                    if ind_even == 1:
                        connect1 = connection[i+len(x)//2]
                        connect_apex = connect1[::-1]
                        connect2 = connection[i]
                        connect_base = connect2[::-1]
                        ind_even = 0
                        list_points = '{'
                    else:
                        connect_apex = connection[i]
                        connect_base = connection[i+len(x)//2]
                        ind_even = 1
                        list_points = '{1,'
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