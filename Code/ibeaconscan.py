import time
from beacontools import BeaconScanner, IBeaconFilter
prevrssi = []
import socket
import csv

csv_columns = ['Minor','RSSI','Average_RSSI','Distance','time']
d = time.localtime()
d = time.strftime("%m-%d-%Y", d)
da = d[:10]
csv_file = da

def callback(bt_addr, rssi, packet, additional_info):
    #print("<%s, %d> %s %s" % (bt_addr, rssi, packet, additional_info))
    str_packet = str(packet)
    txpower = str_packet[31:34]
    data = {'Minor': [0] ,'RSSI': [0], 'Average_RSSI': [0],'Distance':[0],'time':['']}
    
    if len(prevrssi) < 22:
        prevrssi.append(rssi)
        print("1")
    else:
        prevrssi.append(rssi)
        prevrssi.pop(0)
        min_rssi = min(prevrssi)
        max_rssi = max(prevrssi)
        avg_rssi = (sum(prevrssi)-min_rssi-max_rssi)/(len(prevrssi)-2)

        dist = getdistance(avg_rssi,txpower)
        t = time.localtime()
        t = time.strftime("%m/%d/%Y, %H:%M:%S.%f", t)
        minor_num = additional_info['minor']

        data['Minor'] = minor_num
        data['RSSI'] = rssi
        data['Average_RSSI'] = avg_rssi
        data['Distance'] = dist
        data['time'] = t
        
        print("<%s, RSSI: %d %f, %f>, %s, %s" % (bt_addr,rssi,avg_rssi,dist,additional_info['minor'], t))
        print(data)
        save_data(csv_file,data)
        
def save_data(csv_file,data):
    try:
        with open(csv_file,'a',newline = '') as csvfile:
            writer = csv.writer(csvfile)
            #writer.DictWriteheader#for dat in data:
            #for dat in data:
            writer.writerow([data['Minor'],data['RSSI'],data['Average_RSSI'],data['Distance'],data['time']])
    except IOError:
        print("I/O error")
    
        
def getdistance(rssi,txpower):
    txpower = int(txpower)   #one meter away RSSI
    if rssi == 0:
        return -1
    else:
        ratio = rssi*1.0 / txpower
        if ratio < 1:
            return ratio ** 10
        else:
            return 0.89976 * ratio**7.7095 + 0.111

scanner = BeaconScanner(callback,
    device_filter=IBeaconFilter(uuid="f7826da6-4fa2-4e98-8024-bc5b71e0893e",
                                major=7142
                                )
)

scanner.start()
#time.sleep(5)
#scanner.stop()

