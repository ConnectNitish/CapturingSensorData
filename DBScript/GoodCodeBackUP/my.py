import json
from pprint import pprint
import re
import os

import database as db

#newobj = db.Database("127.0.0.1",'mydb3','dbuser','qwerty')
# newobj.printRows("schema1.table1")

thisdir = os.getcwd()
all_path = []
# r=root, d=directories, f = files
for r, d, f in os.walk(thisdir):
	for file1 in f:
		if(file1.endswith(".json")==True):
			all_path.append(os.path.join(r,file1))
	
print(all_path)


# with open('My_Phone_Data.json') as f:
# with open('2019-03-21-19-24-18_data_By_app.json') as f:
#     data = json.load(f)
# with open('2019-03-21-18-53-59_data_By_app.json') as f:
#     data = json.load(f)
all_tables = []
for myf in all_path:
    # with open('2019-03-21-22-41-16_/Input_feed.json') as f:
    if(myf.endswith(".py")==False):
        print(myf)
        with open(myf) as f:
            try:
                data = json.load(f)
            except:
                print("file could not be loaded")
                continue

        # pprint(data)
        userdata = data["UserHash"]
        print(userdata)
        payload = data["Payload"]
        # print(type(payload))

        payload_json = json.loads(payload)
        # pprint(payload_json)

        payload_dict = {}

        for item in payload_json:

            # print(item)
            # print("####################################################################")

            probe_dict = {}

            tname = re.split('[.]',item["PROBE"])[-1]
            # print("tname is ----",tname)
            if(tname not in all_tables):
                all_tables.append(tname)
                # print(myf)
                # print(tname)
            # print(re.split('[.]',item["PROBE"]))

            payload_dict[tname] = []
            record = []
            record.append(userdata)
            for key,values in item.items():
                if key != "PROBE":
                    if key!= "GUID" and key!="ACCESS_POINTS":
                        record.append(str(values))
                    if(tname!="SoftwareInformationProbe"):
                        payload_dict[tname].append((key,values))

            if (tname != "SoftwareInformationProbe" and tname=="WifiAccessPointsProbe"):		
                print("for location insert line name ",myf)
                #newobj.insert(tname,tuple(record),myf)
                #print("666666666666666666666666666666666")
                #newobj.printRows(tname)
                #print("555555555555555555555555555")
	
	if len(payload_dict.keys())>4:
	    pprint(payload_dict)
	    break		
        pprint(payload_dict)

#newobj.close_conn_cursor()
