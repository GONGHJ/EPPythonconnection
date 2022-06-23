import pyEp
from Initialize import MAXSTEPS, EPtime_step, barrier, EP_outputs
from HouseOperation import House_Operation
HO = House_Operation()

def EPhouse(house_number, path_to_buildings):
    pyEp.set_eplus_dir(path_to_buildings)							# not used but must be kept
    weather_file = "simulated_weather_data"
    builder = pyEp.socket_builder(path_to_buildings)
    configs = builder.build() 										# Configs is [port, building_folder_path, idf]
    ep = pyEp.ep_process('localhost', configs[0][0], configs[0][1], weather_file)
    print('House '+str(house_number) + ' is on line at directory: ' + configs[0][1] + '\n')

    dayTimes = []
    current_step = 0
    deltaT = (60/EPtime_step)*60
    while current_step < MAXSTEPS:
            # print(current_step)
            time = current_step * deltaT
            dayTime = time % 86400
            dayTimes.append(dayTime)
            # EP out put
            output = ep.decode_packet_simple(ep.read())
            EP_outputs[current_step, :, house_number - 1] = HO.epoutput_process(output)
            """bidding scheme and cost are done in single house procedure class"""
            # barrier.wait()			# no need for single house
            input_for_ep = HO.house_operation(time_step=current_step, house_number=house_number)
            ep.write(ep.encode_packet_simple(input_for_ep, current_step * deltaT))
            current_step = current_step + 1
    ep.close()
    print('House ' + str(house_number) + ' is done.' + '\n')
