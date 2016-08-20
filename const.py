# -*- coding: utf_8 -*-
from skew_slicer import ApexPosition
import numpy as np

Z_MULT = 2.27

SLICE_X = 114 # 140
SLICE_Y = 147 # 100
SLICE_Z_MIN = 0 #11
SLICE_Z_MID = 35
SLICE_Z_MAX = 100 #100

SLICE_Z_ENDO = 10

EACH_XY = 1
EACH_Z = 1
MASK_THRESHOLD = 3.5 * 10 ** (-6)


#default_apex_position = ApexPosition()
#default_apex_position.X = np.array([114, 147, 0])
#default_apex_position.A = np.array([1, 0, 0])
#default_apex_position.B = np.array([0, 1, 0])
#default_apex_position.C = np.array([0, 0, 1])
#default_apex_position.d = SLICE_Z_MAX - SLICE_Z_MIN

# Для неповернутого измерения
default_apex_position = ApexPosition.init_from_line(np.array([81.6, 149.98, -1.43]), np.array([156, 159, 193.7]),
                                    np.array([155, 160.93, 193.7]), np.array([101.45, 69.74, 216.54]),
                                    np.array([155, 159, 192.97]), np.array([245.7, 97.76, 159.78]))

# Для повернутого измерения
#default_apex_position = ApexPosition()
#default_apex_position.X = np.array([81.6, 149.98, -1.43])
#default_apex_position.C = np.array([0.35593427, 0.04315225, 0.93351416])
#default_apex_position.A = np.array([0.90695487, 0.21929534, -0.35594468])
#default_apex_position.B = np.array([-0.21583179, 0.97708654, 0.03712686])

FILE_DATA_VTK = 'full_vector_field(1).vtk'
FILE_TREE = 'full_tree(1).pkl'
FILE_VECTOR = 'full_vector(1).pkl'

FILE_BORDER = 'lv_border.npy'
FILE_EPI = 'lv_border_epi.npy'
FILE_ENDO = 'lv_border_endo.npy'

FILE_CSV = '8_slice.csv'#'result.csv'
FILE_CSV_TEST = './step300/test_result.csv'  # !!!!!

FILE_HIST = 'hist.png'
FILE_MODEL_VTK = 'model3.vtk'
FILE_RESULT = 'result.csv'

PARAM_NAME = 'template.param_set_semen3'
