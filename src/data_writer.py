__author__ = 'mustafa'

from src.data_store import DataStore
from jinja2 import Template
from itertools import chain

def gams_writer(file_name, data_set_number, data = DataStore()):
    f = open('gams_template.txt')
    src = Template(f.read())
    inbound_arrivals = []
    outbound_arrivals = []
    lower_boundaries = []
    upper_boundaries = []
    inbound_goods = chain(data.inbound_goods, data.compound_coming_goods)
    outbound_goods = chain(data.outbound_goods, data.compound_going_goods)

    for i in range(data.number_of_inbound_trucks):
        truck_name = 'inbound' + str(i)
        inbound_arrivals.append(int(data.arrival_times[data_set_number][truck_name]))

    for i in range(data.number_of_outbound_trucks):
        truck_name = 'outbound' + str(i)
        outbound_arrivals.append(int(data.arrival_times[data_set_number][truck_name]))
        lower_boundaries.append(int(data.boundaries[data_set_number][truck_name][0]))
        upper_boundaries.append(int(data.boundaries[data_set_number][truck_name][1]))

    for i in range(data.number_of_compound_trucks):
        truck_name = 'compound' + str(i)
        inbound_arrivals.append(int(data.arrival_times[data_set_number][truck_name][0]))
        outbound_arrivals.append(int(data.arrival_times[data_set_number][truck_name][1]))
        lower_boundaries.append(int(data.boundaries[data_set_number][truck_name][0]))
        upper_boundaries.append(int(data.boundaries[data_set_number][truck_name][1]))

    d = {'number_of_inbound': data.number_of_inbound_trucks + data.number_of_compound_trucks,
         'number_of_outbound': data.number_of_outbound_trucks + data.number_of_compound_trucks,
         'number_of_compound': data.number_of_compound_trucks,
         'compound_plus_one': data.number_of_compound_trucks + 1,
         'changeover_time': int(data.changeover_time),
         'product_transfer_time': int(data.good_transfer_time),
         'transfer_time': int(data.transfer_time),
         'number_of_goods': data.number_of_goods,
         'number_of_receiving_doors': data.number_of_receiving_doors,
         'number_of_shipping_doors': data.number_of_shipping_doors,
         'inbound_arrivals': inbound_arrivals,
         'outbound_arrivals': outbound_arrivals,
         'lower_boundaries': lower_boundaries,
         'upper_boundaries': upper_boundaries,
         'inbound_goods': inbound_goods,
         'outbound_goods': outbound_goods,
         'good_numbers': range(0, data.number_of_goods)}

    result = src.render(d)
    s = open(file_name, 'w')
    s.write(result)
    s.close()


def print_data( data = DataStore()):
    f = open('show_data_template.txt')
    src = Template(f.read())
    d = {'number_of_inbound': data.number_of_inbound_trucks,
         'number_of_outbound': data.number_of_outbound_trucks,
         'number_of_compound': data.number_of_compound_trucks,

         'number_of_receiving_doors': data.number_of_receiving_doors,
         'number_of_shipping_doors': data.number_of_shipping_doors,
         'number_of_goods': data.number_of_goods,
         'changeover_time': data.changeover_time,
         'loading_time': data.loading_time,
         'makespan_factor': data.makespan_factor,
         'transfer_time': data.transfer_time,
         'good_transfer_time': data.good_transfer_time,
         'inbound_arrival_time': data.inbound_arrival_time,
         'outbound_arrival_time': data.outbound_arrival_time,
         'data_set': data.data_set_list,
         'arrivals': data.arrival_times,
         'boundaries': data.boundaries,
         'inbound_goods': data.inbound_goods,
         'outbound_goods': data.outbound_goods,
         'compound_goods': data.outbound_goods}

    result = src.render(d)
    return result
