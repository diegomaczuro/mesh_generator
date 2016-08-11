# -*- coding: utf_8 -*-
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from interpolation import alg_interp

GENERAL_PARAMETERS = ('model_num','s_right','s_left',
                      'sb_right', 'sb_left','h','scale',
                      'shift_x',  'shift_y','shift_z',
                      'slice_num')

SLICE_PARAMETERS = ('Z_ep', 'Z_en',  'Zb_ep', 'Zb_en', 'R_ep',
                    'R_en', 'Rb_ep', 'Rb_en', 'R_ep2', 'R_en2',
                    'p_ep', 'p_en',  'pb_ep', 'pb_en', 'l_ep',
                    'l_en', 'p_ep2', 'p_en2')



def angle(x,y):
    """ Косинус угла между векторами """
    return np.dot(x, y) / (np.linalg.norm(x) * np.linalg.norm(y))


def fiber_angle(x, y):
    """ Угол между волокнами """
    return np.arccos(np.abs(angle(x,y)))*180/np.pi


def to_dec(rho, phi, z):
    """ Перевод точки из цилиндрическую систему координат в декартову """
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    z = z
    return x, y, z


def project_vector_on_plane(n, source_point, point):
    """
    :param n: нормаль к плоскости
    :param source_point: точка на плоскости
    :param point: точка, которую проецируют на плоскость
    :return: точка на плоскости и расстояние до нее
    """

    x = point - source_point
    d = np.dot(x,n) / np.linalg.norm(n)
    norm_n = n / np.linalg.norm(n)
    p = d * norm_n
    res = x - p

    return (res + source_point), np.linalg.norm(p)

class ModelData:

    def __init__(self, filename, model_num=0):
        self.data = pd.read_csv(filename)
        self.model_num = model_num
        self.md = self.data[self.data.model_num == self.model_num]

        self.s_right = self.md['s_right'][0]
        self.s_left = self.md['s_left'][0]
        self.sb_right = self.md['sb_right'][0]
        self.sb_left = self.md['sb_left'][0]
        self.h = self.md['h'][0]
        self.delta_phi1 = 3 * np.pi
        self.delta_phi2 = -2 * np.pi
        self.shift_x = self.md['shift_x'][0]
        self.shift_y = self.md['shift_y'][0]
        self.shift_z = self.md['shift_z'][0]
        self.scale = self.md['scale'][0]

        self.coeff = {}
        self.angle = None

        self._init_coff()

    def _init_coff(self):
        slice_count = np.max(self.md['slice_num']) + 1

        for par in SLICE_PARAMETERS:
            val = self.md[par].values.tolist()
            val.append(val[0])
            self.angle = np.linspace(0, 2*np.pi, slice_count + 1)
            val = np.array(val)

            a, b, c, d = alg_interp(self.angle, val)

            self.coeff[par] = (a, b, c, d)

    def params(self, angle_full):

        ang = angle_full

        # Оставляет значение в интервале от 0 до 2*np.pi
        if ang >= 2 * np.pi:
            ang = ang % (2 * np.pi)
        elif 0 > ang:
            temp_ = (-ang) % (2 * np.pi)
            ang = 2 * np.pi - temp_

        # Ищет индекс, который надо использовать в сплайновой интерполяции
        spi = max(0, np.searchsorted(self.angle[0:-1], ang) - 1)

        #print ang, spi

        params = {}
        for par in SLICE_PARAMETERS:
            a,b,c,d = self.coeff[par]
            params[par] = a[spi] + \
                          b[spi]*(ang - self.angle[spi]) + \
                          c[spi]*(ang - self.angle[spi])**2 + \
                          d[spi]*(ang - self.angle[spi])**3
        return params



class Model:

    def __init__(self, filename, model_num=0):
        self.md = ModelData(filename, model_num)
        self.parametrs = None  #
        self.parent = None  #
        self.s_right = 30  # Степень параболы для верхушки. Правая ветка параболы на графике
        self.s_left = 4  # Степень параболы для верхушки. Левая ветка параболы на графике
        self.sb_right = 10  # Степень параболы для базы. Правая ветка параболы на графике
        self.sb_left = 10  # Степень параболы для базы. Левая ветка параболы на графике
        self.h = 0.14  # Толщина верхушки
        self.delta_phi1 = 3 * np.pi  # Максимальный угол вращения волокон для верхушки
        self.delta_phi2 = -2 * np.pi  # Максимальный угол вращения волокон для базы

        self.apex_position = None
        self.shift_x = 0
        self.shift_y = 0  # Сдвиг модели по X
        self.shift_z = 0  # Сдвиг модели по Z
        self.scale = 5 # Коэфициент растяжения модели

    #def multiplier(self, p):
    #    return self.md.scale * p[0] + self.md.shift_x, \
    #           self.md.scale * p[1] + self.md.shift_y, \
    #           self.md.scale * p[2] + self.md.shift_z

    def multiplier(self, p):
        #self.scale = 0.00000000001
        p_ = np.array(p) * self.scale
        if self.apex_position == None:
            return p_

        res = self.apex_position.translate(p_)
        x, y, z = res
        return [round(x, 6), round(y, 6), round(z, 6)]
    def wgam(self, y):
        """ Функция задающая ход волокон на верхушке
            y : float
                \gamma
        """

        d = self.md.s_left if y <= 0.5 else self.md.s_right
        return 1 - (2 ** d) * (np.abs(y - (1.0 / 2))) ** d

    def wgamb(self, y):
        """ Функция задающая ход волокон на базе
            y : float
                \gamma
        """
        d = self.md.sb_left if y <= 0.5 else self.md.sb_right
        return 1 - (2 ** d) * (np.abs(y - (1.0 / 2))) ** d

    def R_new(self, data, y, par, par_plus_one):
        """ Вспомогательная функция для задания точек поверхности
            y : float
                \gamma
            phi : float
                \phi
            mas : list
                Коэффициенты интерполяции
            i : int
                Индекс в массиве
        """
        return data[par] * (1 - y) + data[par_plus_one] * y

    def surfcylbf(self, y, psi, phi, data=None):
        """ Базальная часть желудочка
            y : float
                \gamma
            psi : float
                \psi
            phi : float
                \phi
            mas : list
                Коэффициенты интерполяции
        """

        data = self.md.params(phi) if data is None else data

        t1_ = (self.R_new(data, y, 'R_ep2', 'R_en2') * (1 - (np.abs(psi) / (np.pi / 2)) ** self.R_new(data, y, 'pb_ep', 'pb_en')) \
               + self.R_new(data, y, 'Rb_ep', 'Rb_en') * (np.abs(psi) / (np.pi / 2)))

        t2_ = (self.R_new(data, y, 'Zb_ep', 'Zb_en') * np.sin(psi) + self.R_new(data, y, 'Z_ep', 'Z_en'))

        return to_dec(t1_, phi, t2_)

    def surfcyl1(self, y, psi, phi, data=None):
        """ Верхушка желудочка. Первая часть
            y : float
                \gamma
            psi : float
                \psi
            phi : float
                \phi
            mas : list
                Коэффициенты интерполяции
        """

        data = self.md.params(phi) if data is None else data

        Z = self.R_new(data, y, 'Z_ep', 'Z_en')
        t1 = self.R_new(data, y, 'R_ep', 'R_en') \
             * (1 - ((np.abs(psi) - self.R_new(data, y, 'l_ep', 'l_en')) / (np.pi / 2 - self.R_new(data, y, 'l_ep', 'l_en'))) **
                self.R_new(data, y, 'p_ep', 'p_en'))
        t2 = ((Z - self.md.h * y) * np.sin(psi) + Z)
        return to_dec(t1, phi, t2)

    def surfcyl2(self, y, psi, phi, data=None):
        """ Верхушка желудочка. Вторая часть
            y : float
                \gamma
            psi : float
                \psi
            phi : float
                \phi
            mas : list
                Коэффициенты интерполяции
        """
        data = self.md.params(phi) if data is None else data

        Z = self.R_new(data, y, 'Z_ep', 'Z_en')
        t1 = self.R_new(data, y, 'R_ep', 'R_en') - (self.R_new(data, y, 'R_ep', 'R_en') - self.R_new(data, y, 'R_ep2', 'R_en2')) \
                                              * (np.abs((np.abs(psi) / self.R_new(data, y, 'l_ep', 'l_en')) - 1) ** self.R_new(data, y,
                                                                                                                      'p_ep2',
                                                                                                                      'p_en2'))
        t2 = ((Z - self.md.h * y) * np.sin(psi) + Z)
        return to_dec(t1, phi, t2)

    def surfcyl_general(self, y, psi, phi):
        """ Верхушка желудочка. Вторая часть
            y : float
                \gamma
            psi : float
                \psi
            phi : float
                \phi
            mas : list
                Коэффициенты интерполяции
        """
        data = self.md.params(phi)

        if psi > self.R_new(data, y, 'l_ep', 'l_en'):
            return self.surfcyl1(y, -psi, phi, data=data)
        else:
            return self.surfcyl2(y, -psi, phi, data=data)

    def test_save_graphics(self):
        for par in SLICE_PARAMETERS:
            series_phi = np.linspace(0, 2*np.pi, 1000)
            series_val = []
            for i in range(len(series_phi)):
                series_val.append(self.md.params(series_phi[i])[par])

            plt.plot(series_phi, series_val)
            plt.savefig("./test/plot/" + par + ".png")
            plt.close()


    def generate_surface_vol(self, phi_series, psi_series, gamma_series, tree, results_vectors):
        gamma = np.linspace(0, 1, gamma_series, endpoint=True)
        phi = np.linspace(0, 2 * np.pi, phi_series, endpoint=True)
        psi_1 = np.linspace(0, np.pi / 2, psi_series, endpoint=True)
        psi_2 = np.linspace(-np.pi / 2, 0, psi_series, endpoint=True)

        # массивы для базы
        x = np.zeros(psi_series)
        y = np.zeros(psi_series)
        z = np.zeros(psi_series)
        x_points = np.array([])
        y_points = np.array([])
        z_points = np.array([])

        # массивы для верхушки
        x2 = np.zeros(psi_series)
        y2 = np.zeros(psi_series)
        z2 = np.zeros(psi_series)
        x2_points = np.array([])
        y2_points = np.array([])
        z2_points = np.array([])

        # Инициализация массивов(для вывода) для векторов поверхности
        x_vectors = np.array([])
        y_vectors = np.array([])
        z_vectors = np.array([])
        x2_vectors = np.array([])
        y2_vectors = np.array([])
        z2_vectors = np.array([])

        # массив с соединением ячеек
        connection = np.zeros((2 * (phi_series - 1) * (psi_series - 1) * (gamma_series - 1), 8), dtype=int)

        # массив для цветной раскраски по gamma
        gamma_color = np.array([])

        ind = 0
        ind2 = 0
        ind3 = 0
        distance = np.array([])

        for k in phi:
            for i in gamma:

                for j in psi_1:
                    x[ind], y[ind], z[ind] = self.multiplier(
                        self.surfcylbf(i, j, k))
                    gamma_color = np.append(gamma_color, i)
                    dist, index = tree.query((x[ind], y[ind], z[ind]), k=3)
                    distance = np.append(distance, dist[0][0])
                    x_vectors = np.append(x_vectors, results_vectors[index[0][0]][0])
                    y_vectors = np.append(y_vectors, results_vectors[index[0][0]][1])
                    z_vectors = np.append(z_vectors, results_vectors[index[0][0]][2])
                    ind += 1
                    ind3 += 1

                ind = 0
                x_points = np.append(x_points, x)
                y_points = np.append(y_points, y)
                z_points = np.append(z_points, z)

        print len(x_points), len(x_vectors)

        offset = ind3

        for k in phi:
            for i in gamma[::-1]:
                for j in psi_2:

                    #if np.abs(j) > self.R(i, k, self.parametrs, 14):
                    #    x2[ind2], y2[ind2], z2[ind2] = self.multiplier(
                    #        self.surfcyl1(i, j, k, self.parametrs))
                    #else:
                    #    x2[ind2], y2[ind2], z2[ind2] = self.multiplier(
                    #        self.surfcyl2(i, j, k, self.parametrs))

                    x2[ind2], y2[ind2], z2[ind2] = self.multiplier(self.surfcyl_general(i, -j, k))
                    gamma_color = np.append(gamma_color, i)
                    # print x2[ind2], y2[ind2], z2[ind2]

                    dist, index = tree.query((x2[ind2], y2[ind2], z2[ind2]), k=3)
                    distance = np.append(distance, dist[0][0])
                    x2_vectors = np.append(x2_vectors, results_vectors[index[0][0]][0])
                    y2_vectors = np.append(y2_vectors, results_vectors[index[0][0]][1])
                    z2_vectors = np.append(z2_vectors, results_vectors[index[0][0]][2])

                    ind2 += 1


                ind2 = 0

                x2_points = np.append(x2_points, x2)
                y2_points = np.append(y2_points, y2)
                z2_points = np.append(z2_points, z2)

        print len(x2_points), len(x2_vectors)

        ind = 0

        for k in xrange((phi_series - 1)):
            for i in xrange((gamma_series - 1)):
                for j in xrange((psi_series - 1)):
                    p0 = k * psi_series * gamma_series + i * psi_series + j
                    p1 = k * psi_series * gamma_series + i * psi_series + (j + 1)
                    p2 = (k + 1) * psi_series * gamma_series + i * psi_series + (j + 1)
                    p3 = (k + 1) * psi_series * gamma_series + i * psi_series + j
                    p4 = k * psi_series * gamma_series + (i + 1) * psi_series + j
                    p5 = k * psi_series * gamma_series + (i + 1) * psi_series + (j + 1)
                    p6 = (k + 1) * psi_series * gamma_series + (i + 1) * psi_series + (j + 1)
                    p7 = (k + 1) * psi_series * gamma_series + (i + 1) * psi_series + j

                    connection[ind] = np.array([p0, p1, p2, p3, p4, p5, p6, p7])
                    ind += 1

        for k in xrange((phi_series - 1)):
            for i in xrange((gamma_series - 1)):
                for j in xrange((psi_series - 1)):
                    p0 = offset + k * psi_series * gamma_series + i * psi_series + j
                    p1 = offset + k * psi_series * gamma_series + i * psi_series + (j + 1)
                    p2 = offset + (k + 1) * psi_series * gamma_series + i * psi_series + (j + 1)
                    p3 = offset + (k + 1) * psi_series * gamma_series + i * psi_series + j
                    p4 = offset + k * psi_series * gamma_series + (i + 1) * psi_series + j
                    p5 = offset + k * psi_series * gamma_series + (i + 1) * psi_series + (j + 1)
                    p6 = offset + (k + 1) * psi_series * gamma_series + (i + 1) * psi_series + (j + 1)
                    p7 = offset + (k + 1) * psi_series * gamma_series + (i + 1) * psi_series + j

                    connection[ind] = np.array([p0, p1, p2, p3, p4, p5, p6, p7])
                    ind += 1

        # Склейка базы с верхушкой

        x3 = np.append(x_points, x2_points)
        y3 = np.append(y_points, y2_points)
        z3 = np.append(z_points, z2_points)

        x4 = np.append(x_vectors, x2_vectors)
        y4 = np.append(y_vectors, y2_vectors)
        z4 = np.append(z_vectors, z2_vectors)

        return x3, y3, z3, x4, y4, z4, connection, gamma_color

    def splane_for_mesh_epi(self, n_phi, n_psi_base):
        phi_series = np.linspace(0, 2 * np.pi, n_phi, endpoint=True)
        psi_series = np.linspace(0, 0.5 * np.pi, n_psi_base, endpoint=True)
        psi_series2 = psi_series[::-1]
        x = np.zeros(((2*(len(phi_series)-1), len(psi_series)-1)))
        y = np.zeros(((2*(len(phi_series)-1), len(psi_series)-1)))
        z = np.zeros(((2*(len(phi_series)-1), len(psi_series)-1)))
        connect = np.zeros(((2*(len(phi_series)-1), len(psi_series)-1)), dtype=int)
        x_epi = []
        y_epi = []
        z_epi = []
        ind_array = []
        ind = 0
        ind2 = 0
        ind_for_points = 2
        gamma = 0
        rev = 0
        apex_x, apex_y, apex_z = self.multiplier(self.surfcyl_general(gamma, psi_series2[0], phi_series[0]))
        for j in xrange(1, len(phi_series)):
            for i in xrange(1, len(psi_series2)):
                x[ind2][ind], y[ind2][ind], z[ind2][ind] = self.multiplier(self.surfcyl_general(gamma, psi_series2[i], phi_series[j]))
                connect[ind2][ind] = ind_for_points
                ind += 1
                ind_for_points += 1

            x_epi.append(x)
            y_epi.append(y)
            z_epi.append(z)

            ind_array.append(connect)
            ind = 0
            ind2 += 1


        for j in xrange(1, len(phi_series)):
            for i in xrange(1, len(psi_series2)):
                x[ind2][ind], y[ind2][ind], z[ind2][ind] = self.multiplier(
                    self.surfcylbf(gamma, psi_series[i], phi_series[j]))
                connect[ind2][ind] = ind_for_points


                ind += 1
                ind_for_points += 1


            x_epi.append(x)
            y_epi.append(y)
            z_epi.append(z)

            ind_array.append(connect)
            ind = 0
            ind2 += 1

        return x, y, z, connect, [apex_x, apex_y, apex_z]



    def splane_for_mesh_endo(self, n_phi, n_psi_base):
        phi_series = np.linspace(0, 2 * np.pi, n_phi, endpoint=True)
        psi_series = np.linspace(0, 0.5 * np.pi, n_psi_base, endpoint=True)
        psi_series2 = psi_series[::-1]
        x = np.zeros(((2*(len(phi_series)-1), len(psi_series)-1)))
        y = np.zeros(((2*(len(phi_series)-1), len(psi_series)-1)))
        z = np.zeros(((2*(len(phi_series)-1), len(psi_series)-1)))
        connect = np.zeros(((2*(len(phi_series)-1), len(psi_series)-1)), dtype=int)
        x_epi = []
        y_epi = []
        z_epi = []
        ind_array = []
        ind = 0
        ind2 = 0
        ind_for_points = 2*(len(phi_series)-1)*(len(psi_series)-1) + 3
        gamma = 1

        apex_x, apex_y, apex_z = self.multiplier(self.surfcyl_general(gamma, psi_series2[0], phi_series[0]))
        for j in xrange(1, len(phi_series)):
            for i in xrange(1, len(psi_series2)):
                x[ind2][ind], y[ind2][ind], z[ind2][ind] = self.multiplier(self.surfcyl_general(gamma, psi_series2[i], phi_series[j]))
                connect[ind2][ind] = ind_for_points
                ind += 1
                ind_for_points += 1

            x_epi.append(x)
            y_epi.append(y)
            z_epi.append(z)

            ind_array.append(connect)
            ind = 0
            ind2 += 1
        border = np.zeros((len(phi_series)-1), dtype=int)
        ind_border = 0

        for j in xrange(1, len(phi_series)):
            for i in xrange(1, len(psi_series2)):
                x[ind2][ind], y[ind2][ind], z[ind2][ind] = self.multiplier(
                    self.surfcylbf(gamma, psi_series[i], phi_series[j]))
                connect[ind2][ind] = ind_for_points
                if i == len(psi_series2) - 1:
                    border[ind_border] = ind_for_points
                    ind_border += 1

                ind += 1
                ind_for_points += 1


            x_epi.append(x)
            y_epi.append(y)
            z_epi.append(z)

            ind_array.append(connect)
            ind = 0
            ind2 += 1
        print 'border=', border

        return x, y, z, connect, [apex_x, apex_y, apex_z], border


    def surface(self, n_phi, n_psi_base, n_psi_apex, type_connection='VTK_QUAD'):

        phi_series = np.linspace(0, 2 * np.pi, n_phi, endpoint=True)
        psi_series = np.linspace(0, 0.5 * np.pi, n_psi_base, endpoint=True)
        psi_series2 = psi_series[::-1]
        x = np.zeros((4 * len(psi_series) * len(phi_series)))
        y = np.zeros((4 * len(psi_series) * len(phi_series)))
        z = np.zeros((4 * len(psi_series) * len(phi_series)))
        ind = 0
        gamma = 0
        for i in xrange(len(psi_series2)):
            for j in xrange(len(phi_series)):
                x[ind], y[ind], z[ind] = self.multiplier(self.surfcyl_general(gamma, psi_series2[i], phi_series[j]))
                ind += 1

        gamma = 0
        for i in xrange(len(psi_series)):
            for j in xrange(len(phi_series)):
                x[ind], y[ind], z[ind] = self.multiplier(
                    self.surfcylbf(gamma, psi_series[i], phi_series[j]))
                ind += 1

        gamma = 1
        for i in xrange(len(psi_series2)):
            for j in xrange(len(phi_series)):
                x[ind], y[ind], z[ind] = self.multiplier(
                    self.surfcylbf(gamma, psi_series2[i], phi_series[j]))
                ind += 1

        gamma = 1
        for i in xrange(len(psi_series)):
            for j in xrange(len(phi_series)):
                x[ind], y[ind], z[ind] = self.multiplier(self.surfcyl_general(gamma, psi_series[i], phi_series[j]))
                ind += 1

        connection = []
        ind = 0
        maxj = len(psi_series)
        maxi = len(phi_series)
        for j in xrange(4 * len(psi_series) - 1):
            for i in xrange(len(phi_series) - 1):
                x1 = i + j * maxi
                x2 = i + j * maxi + 1
                x3 = (j + 1) * maxi + i + 1
                x4 = (j + 1) * maxi + i

                if type_connection=='VTK_QUAD':
                    connection.append([x1, x2, x3, x4])
                else:
                    connection.append([x1, x2, x3])
                    connection.append([x2, x4, x3])

                ind += 1

            x1 = x2
            x2 = x1 - maxi + 1
            x4 = x3
            x3 = x3 - maxi + 1
            connection.append([x1, x2, x3, x4])
            ind += 1

        return x, y, z, connection




    def generate_series_points(self, n, limit_gamma0, limit_gamma):
        """ Создание серии точек поверхности"""

        phi = np.linspace(0, 2 * np.pi + 0.001, n + 1)

        # Инициализация массивов(вспомогательных) для точек поверхности
        x1_series = np.zeros(limit_gamma)  # верхушка
        y1_series = np.zeros(limit_gamma)
        z1_series = np.zeros(limit_gamma)
        x2_series = np.zeros(limit_gamma)  # база
        y2_series = np.zeros(limit_gamma)
        z2_series = np.zeros(limit_gamma)

        # Инициализация массивов(для вывода) для точек поверхности
        x_series = np.array([])
        y_series = np.array([])
        z_series = np.array([])

        # Инициализация массивов(для вывода) для векторов поверхности
        x_vectors = np.array([])
        y_vectors = np.array([])
        z_vectors = np.array([])

        gamma0 = np.linspace(0, 0.99999999, limit_gamma0)

        gamma_color1 = np.zeros(limit_gamma)  # тут хранятся значения gamma для каждой точки модели.
        # нужно для раскраски волокон в зависимости от расположения в толще стенки ЛЖ
        gamma_color2 = np.zeros(limit_gamma)
        gamma = np.array([])

        for i in phi:
            for j in gamma0:
                limit1 = 0.50001 - (1 - j) ** (1.0 / self.md.s_left) / 2
                limit2 = 0.50001 + (1 - j) ** (1.0 / self.md.s_left) / 2
                gamma1 = np.linspace(limit1, limit2, limit_gamma)

                limit11 = 0.50001 - (1 - j) ** (1.0 / self.md.sb_left) / 2
                limit12 = 0.50001 + (1 - j) ** (1.0 / self.md.sb_left) / 2
                gamma2 = np.linspace(limit11, limit12, limit_gamma)
                value1 = 0
                value2 = 0
                # Инициализация массивов(вспомогательных) для векторов поверхности
                x1_vectors = np.array([])  # верхушка
                y1_vectors = np.array([])
                z1_vectors = np.array([])
                x2_vectors = np.array([])  # база
                y2_vectors = np.array([])
                z2_vectors = np.array([])

                for k in gamma1[::-1]:
                    phi1 = i + k * self.md.delta_phi1
                    psi1 = np.pi * 0.5 * (self.wgam(k) - j)
                    x1_series[value1], y1_series[value1], z1_series[value1] = self.multiplier(
                        self.surfcyl_general(k, psi1, phi1))
                    gamma_color1[value1] = k
                    value1 += 1

                for k2 in gamma2:
                    phi2 = i + k2 * self.md.delta_phi2
                    psi2 = np.pi * 0.5 * (self.wgamb(k2) - j)
                    x2_series[value2], y2_series[value2], z2_series[value2] = self.multiplier(
                        self.surfcylbf(k2, psi2, phi2))
                    gamma_color2[value2] = k2
                    value2 += 1

                for m in xrange(len(x1_series) - 1):
                    x1_vectors = np.append(x1_vectors, x1_series[m + 1] - x1_series[m])
                    y1_vectors = np.append(y1_vectors, y1_series[m + 1] - y1_series[m])
                    z1_vectors = np.append(z1_vectors, z1_series[m + 1] - z1_series[m])
                    x2_vectors = np.append(x2_vectors, x2_series[m + 1] - x2_series[m])
                    y2_vectors = np.append(y2_vectors, y2_series[m + 1] - y2_series[m])
                    z2_vectors = np.append(z2_vectors, z2_series[m + 1] - z2_series[m])

                # Склейка базальной и апикальной части(точки)
                x3 = x1_series[::-1]
                y3 = y1_series[::-1]
                z3 = z1_series[::-1]
                x4 = np.append(x2_series[0:len(x2_series) - 1], x3[1::])
                y4 = np.append(y2_series[0:len(x2_series) - 1], y3[1::])
                z4 = np.append(z2_series[0:len(x2_series) - 1], z3[1::])

                x_series = np.append(x_series, x4)
                y_series = np.append(y_series, y4)
                z_series = np.append(z_series, z4)

                # Склейка базальной и апикальной части(вектора)
                x1 = x1_vectors[::-1]
                y1 = y1_vectors[::-1]
                z1 = z1_vectors[::-1]
                x2 = np.append(x2_vectors, x1)
                y2 = np.append(y2_vectors, y1)
                z2 = np.append(z2_vectors, z1)

                x_vectors = np.append(x_vectors, x2)
                y_vectors = np.append(y_vectors, y2)
                z_vectors = np.append(z_vectors, z2)

                # склейка массиов для gamma

                g1 = gamma_color1[::-1]
                g2 = np.append(gamma_color2[0:len(gamma_color2) - 1], g1[1::])
                gamma = np.append(gamma, g2)

        return x_series, y_series, z_series, x_vectors, y_vectors, z_vectors, gamma


