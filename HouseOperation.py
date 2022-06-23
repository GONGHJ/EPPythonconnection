import numpy as np
from Initialize import EPtime_step, EV_capacity_joule, EVsoc, EVsignal, signal_to_house, EV_arrive_SOC, DRsignals, \
    EVschedule, BES_capacity_joule, num_EPoutputs, EWHonoffDailyCount, EWHONOFFSignal
deltaT = (60/EPtime_step)*60

class House_Operation(object):
    def __init__(self):
        self.EPout = []
        self.time_step = []
        self.hour = []
        self.initialcase = 'HVACDR'
        self.PeakDRcount = self.initialcase
        self.PVGenerationDRcount = 0
        self.Pbes = 0
        self.Pev = 0
        self.deltaC = 5.556
        self.TeON = 100
        self.TeOFF = 0
        self.Tmax = 60
        self.TewhSet = self.TeON
        self.downcounter = 0
        self.TCooling = 24
        self.THeating = 21
        self.EVarrive = []
        self.trans = 0                  # used to transition from BESS to EV
        self.transcount = 0
        self.Day = []
        self.event = 'NoDREvent'
        self.recovertoDefault = 0
        self.TotalNetloadRecord = 0

        self.EWHomdailycount = 0
        self.daycount = 0
        self.Initialday = 3 # Tuesady
        self.Dayrecord = self.Initialday
        self.EWHloadRecord = 0

    '''EP output'''
    def epoutput_process(self, epoutputraw):
        self.EPout = epoutputraw
        return np.reshape(epoutputraw, (1, 1, num_EPoutputs))

    '''main function entrance'''
    def house_operation(self, time_step, house_number):
        self.time_step =time_step
        self.hour = int(time_step / 60 % 24)

        self.EWHOnOFFcontrol(self.EPout)
        self.EWHdailycount(self.EPout[6])
        self.CycleCount(time_step)

        if time_step == 0: # Initialize
            self.TewhSet = 60
        EPinput = [self.Pbes, -self.Pev, self.TewhSet, self.TCooling, self.THeating]
        signal_to_house[time_step, :, house_number - 1] = np.reshape(EPinput, (1, 1, 5))
        return EPinput

    def EWHOnOFFcontrol(self, EPoutput):
        Target_demand = 2000
        TotalNetload = EPoutput[0]
        EWHload = EPoutput[6]
        EWHONOFFSignal[self.time_step] = self.EWHstatus(EWHload)
        EWHTemps = EPoutput[7]
        loadwithoutEWH = TotalNetload - EWHload
        self.cyclingNumbers(Target_demand, loadwithoutEWH)      # update the downcounter time

        if self.downcounter < 1:   # force EWH to be off
            self.EWH_Prevent()

        elif self.downcounter >= 15:     # PV storing mode
            if EWHload != 0:
                self.EWH_Force()
            else:
                self.EWH_normalset()

        elif self.downcounter >= 8 and 16 <= self.hour <= 17:       # top-off mode
            self.EWH_Force()

        else:
            pass

        if EWHTemps <= 40.5556 and self.downcounter >= 5:           # demand response mode
            self.EWH_Force()

    def CycleCount(self, time_step):
        if time_step % 1440 == 0 and time_step / 1440 >= 1:          # the day changes
            print(time_step, self.EWHomdailycount)
            EWHonoffDailyCount[self.daycount] = self.EWHomdailycount    # record the EWH boost time
            self.EWHomdailycount = 0            # reset EWH count
            self.daycount = self.daycount + 1   # update the day

    def EWHstatus(self, EWHload):
        if EWHload == 0:   # EWH is off
            return 0
        elif EWHload != 0:   # EWH is on
            return 1
        else:
            print("Error in EWH status monitor")


    def EWH_Force(self):
        # EWH is forced on
        self.TewhSet = self.TeON

    def EWH_Prevent(self):
        # EWH is prevented to be on
        self.TewhSet = self.TeOFF

    def EWH_normalset(self):
        # leave 10 C gap in the high PV time
        self.TewhSet = self.Tmax - 10

    def cyclingNumbers(self, targetdemand, loadwithoutEWH):
        self.downcounter = self.downcounter - 1
        fifteenMin_agg = self.time_step % 15
        if fifteenMin_agg == 0:         # reset the downcounter every 15 minutes
            self.downcounter = int((targetdemand - loadwithoutEWH)/ (5000/15)) # EWH is allowed to operate this many time steps
            if self.downcounter <= 1:
                self.downcounter = 1

    def EWHdailycount(self,EWHnewload):
        if self.EWHloadRecord == 0 and EWHnewload != 0:
            self.EWHomdailycount = self.EWHomdailycount + 1
        self.EWHloadRecord = EWHnewload

