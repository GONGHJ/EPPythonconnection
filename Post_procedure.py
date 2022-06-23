import scipy.io as sio
from Initialize import MAXSTEPS, signal_to_house, BES_capacity_joule, EP_outputs, EVsoc, DRsignals, EWHonoffDailyCount, \
    EWHONOFFSignal
import datetime
import pandas as pd
import numpy as np


current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M")
t = list(range(MAXSTEPS))
datafile_name = 'Simresults_' + current_time
EP_outputs[:, 2, 0] = EP_outputs[:, 2, 0] / BES_capacity_joule * 100  # SCO as percent
EVsoc = EVsoc * 100

EVsoc = np.delete(EVsoc, [MAXSTEPS])                            # delete the last time step
signal_to_house = np.delete(signal_to_house, MAXSTEPS, 0)

class PostProcedure:
    @staticmethod
    def data_for_matlab():
        with open(r'./simulationresult/' + datafile_name+ '.mat', 'wb') as f:
            sio.savemat(f, {'t': t})
            sio.savemat(f, {'Totalnetload': EP_outputs[:, 0, 0]})
            sio.savemat(f, {'PV': EP_outputs[:, 1, 0]})
            sio.savemat(f, {'SOC': EP_outputs[:, 2, 0]})
            sio.savemat(f, {'BESload': EP_outputs[:, 3, 0] - EP_outputs[:, 4, 0]})
            sio.savemat(f, {'EVload': EP_outputs[:, 5, 0]})
            sio.savemat(f, {'EWHload': EP_outputs[:, 6, 0]})
            sio.savemat(f, {'EWHT': EP_outputs[:, 7, 0]})
            sio.savemat(f, {'ZoneT': EP_outputs[:, 8, 0]})
            sio.savemat(f, {'DBT': EP_outputs[:, 9, 0]})
            sio.savemat(f, {'HVACload': EP_outputs[:, 10, 0] - EP_outputs[:, 6, 0]})
            sio.savemat(f, {'HVACload': EP_outputs[:, 10, 0] - EP_outputs[:, 6, 0]})
            sio.savemat(f, {'EWHonoffCountbyDay': EWHonoffDailyCount})
            sio.savemat(f, {'EWHONOFFSignal': EWHONOFFSignal})
            # sio.savemat(f, {'Water Heater Compressor Part Load Ratio': EP_outputs[:, 16, 0]})
            #
            sio.savemat(f, {'EVSOC': EVsoc})
            sio.savemat(f, {'DRsignals': DRsignals})
            #
            sio.savemat(f, {'Pbes_in': signal_to_house[:, 0, 0]})
            sio.savemat(f, {'Pev_in': signal_to_house[:, 1, 0]})
            sio.savemat(f, {'EWHsettingT': signal_to_house[:, 2, 0]})
            sio.savemat(f, {'CoolingSetT': signal_to_house[:, 3, 0]})
            sio.savemat(f, {'HeatingSetT': signal_to_house[:, 4, 0]})
        pass
        print('\'*.mat\' file saved as: ' + datafile_name)

    @staticmethod
    def Probability_Aggregated():
        pass

    @staticmethod
    def data_for_excel(House_Num):
        df1 = pd.DataFrame(signal_to_house[:, :, House_Num-1], columns=['BES load [W]', 'EV load [W]', 'EWH set poing [C]', 'Cooling set point [C]', 'Heating set point [C]'])
        df2 = pd.DataFrame(EP_outputs[:, :, House_Num-1], columns=['House total net load [W]', 'PV generation [W]', 'BES SOC [%]',
                                                                   'BES charge [W]', 'BES discharge [W]', 'EV load [W]',
                                                                   'Water heater power [W]', 'Water heater tank temperature [C]',
                                                                   'Living zone temperature [C]', 'Dry bulb temperature [C]',
                                                                   'HVAC load (Incl. EWH) [W]', 'Month', 'Dayofweek', 'Holiday?',
                                                                   ])
        df3 = pd.DataFrame(EVsoc, columns=['EV soc [%]'])
        df4 = pd.DataFrame(DRsignals, columns=['DR signals [W]'])
        with pd.ExcelWriter(r'./simulationresult/' + datafile_name + '.xlsx') as writer:  # doctest: +SKIP
            df1.to_excel(writer, sheet_name='signal_to_house')
            df2.to_excel(writer, sheet_name='EP_outputs')
            df3.to_excel(writer, sheet_name='EVsoc')
            df4.to_excel(writer, sheet_name='DR signals')
            print('\'*.xlsx\' file saved as: ' + datafile_name)
