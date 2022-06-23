from eppy.modeleditor import IDF
'''chage the IDF files in batch'''
IDF.setiddname(r'E:/EnergyPlusV8-8-0/Energy+.idd')

def change_Day(IDFname):
    filename = r'./Houses/IDFfiles/' + IDFname + '.idf'
    targetidf=IDF(filename)
    runperiod=targetidf.idfobjects['RunPeriod'][0]
    runperiod.Begin_Month = 7
    runperiod.Begin_Day_of_Month = 9
    runperiod.End_Month = 7
    runperiod.End_Day_of_Month = 16            # 16
    targetidf.save()

def change_Efficiency(IDFname):
    filename = r'./Houses/IDFfiles/' + IDFname + '.idf'
    targetidf=IDF(filename)
    BES=targetidf.idfobjects['ElectricLoadCenter:Storage:Simple'][0]
    BES.Nominal_Energetic_Efficiency_for_Charging = 0.95
    BES.Nominal_Discharging_Energetic_Efficiency = 0.95

    Converter=targetidf.idfobjects['ElectricLoadCenter:Storage:Converter'][0]
    Converter.Simple_Fixed_Efficiency = 1
    targetidf.save()

    Inverter=targetidf.idfobjects['ElectricLoadCenter:Inverter:FunctionOfPower'][0]
    Inverter.Minimum_Efficiency = 0.95
    Inverter.Maximum_Efficiency =0.95

if __name__ == '__main__':
    for n in range(1):

        change_Day(str(n+1).rjust(2, '0'))