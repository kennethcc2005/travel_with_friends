import psycopg2
import json
import city_trip as trip

with open('api_key_list.config') as key_file:
    api_key_list = json.load(key_file)
conn_str = api_key_list["conn_str"]

# conn_str = "dbname='travel_with_friends' user='Gon' host='localhost'"

conn = psycopg2.connect(conn_str)
cur = conn.cursor()
cur.execute("select state, city from county_table;")
c = cur.fetchall()
print len(c)

cur.execute("select max(index) from full_trip_table;")
full_trip_index = cur.fetchone()[0]
print full_trip_index
cur.execute("select county, state from full_trip_table where index='%s';"%(full_trip_index)) 
location = cur.fetchone()       
print location
cur.execute("select state, city from county_table where county ='%s' and state='%s';"%(location[0],location[1]))
last_stop_location = cur.fetchall()[0]
print last_stop_location
last_stop =  c.index(last_stop_location)
print last_stop
conn.close()

Not_data_for_county=[]
# for x in range(last_stop-10,len(c)):
for x in range(len(c)):
    state, city = c[x]
    # ('California', 'Newbury Park'), ('Alaska', 'Chignik Lake') have problem 
    # if (state == 'Puerto Rico') or (state == 'Virgin Islands'):
    #     continue
    print c[x]
    n_days = [1,2,3,4,5]
    for day in n_days:
        error = trip.get_fulltrip_data(state, city, int(day))
        Not_data_for_county.append(error)
print "finish all city and state"
# with open("missing_county_info.txt", 'w') as f:
# 	for error in Not_data_for_county:
# 		f.write("%s\n"%error)