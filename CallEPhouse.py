from SingleHouseModel import EPhouse
import os
from Initialize import *


house_number = 1
path_to_buildings = os.path.join(os.getcwd(), 'Houses', 'EPWorkDirec', 'house'+str(house_number).rjust(2, '0'))
print('Single house runs at: ', path_to_buildings)
EPhouse(house_number, path_to_buildings)                   #

from Post_procedure import PostProcedure
PostProcedure.data_for_matlab()
PostProcedure.data_for_excel(house_number)

