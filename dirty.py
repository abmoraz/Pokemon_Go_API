import logic
import api
import time
import pokemon_pb2
import location
import config
import sys
from multiprocessing import Process

multi=False

def start_private_show(access_token,ltype,loc):
	location.set_location(loc)
	print '[+] Token:',access_token[:40]+'...'
	prot1=logic.gen_first_data(access_token,ltype)
	local_ses=api.get_rpc_server(access_token,prot1)
	new_rcp_point='https://%s/rpc'%(local_ses.rpc_server,)
	while(True):
		work_stop(local_ses,new_rcp_point)
	
def walk_random():
	COORDS_LATITUDE, COORDS_LONGITUDE, COORDS_ALTITUDE=location.get_location_coords()
	COORDS_LATITUDE=location.l2f(COORDS_LATITUDE)
	COORDS_LONGITUDE=location.l2f(COORDS_LONGITUDE)
	COORDS_ALTITUDE=location.l2f(COORDS_ALTITUDE)
	COORDS_LATITUDE=COORDS_LATITUDE+config.steps
	COORDS_LONGITUDE=COORDS_LONGITUDE+config.steps
	location.set_location_coords(COORDS_LATITUDE, COORDS_LONGITUDE, COORDS_ALTITUDE)
	
def split_list(a_list):
	half = len(a_list)/2
	return a_list[:half], a_list[half:]
	
def work_half_list(part,local_ses,new_rcp_point):
	for t in part:
		if config.debug:
			print '[!] farming pokestop..'
		work_with_stops(t,local_ses.ses,new_rcp_point)
	
def work_stop(local_ses,new_rcp_point):
	proto_all=logic.all_stops(local_ses)
	all_stops=api.use_api(new_rcp_point,proto_all)
	maps = pokemon_pb2.maps()
	maps.ParseFromString(all_stops)
	data_list=location.get_near(maps)
	data_list = sorted(data_list, key = lambda x: x[1])
	if len(data_list)>0:
		print '[+] found: %s Pokestops near'%(len(data_list))
		if local_ses is not None and data_list is not None:
			print '[+] starting show'
			if multi:
				a,b=split_list(data_list)
				p = Process(target=work_half_list, args=(a,local_ses.ses,new_rcp_point))
				o = Process(target=work_half_list, args=(a,local_ses.ses,new_rcp_point))
				p.start()
				o.start()
				p.join()
				o.join()
				print '[!] farming done..'
			else:
				for i,t in enumerate(data_list):
                                        print '[!] farming pokestop %s of %s' % (i + 1, len(data_list))
					work_with_stops(t,local_ses.ses,new_rcp_point)
					print '[!] farming done..'
	else:
		walk_random()
		work_stop(local_ses,new_rcp_point)
		
def work_with_stops(current_stop,ses,new_rcp_point):
	Kinder= logic.gen_stop_data(ses,current_stop)
	tmp_api=api.use_api(new_rcp_point,Kinder)
	try:
		if tmp_api is not None:
			map = pokemon_pb2.map()
			map.ParseFromString(tmp_api)
			st= map.sess[0].status
			config.earned_xp+=map.sess[0].amt
			if st==4:
				print "   [!] +%s (%s)"%(map.sess[0].amt,config.earned_xp)
			elif st==3:
				print "   [!] used"
			elif st==2:
				print "   [!] charging"
			elif st==1:
				print "   [!] teleport.."
				time.sleep(14)
				work_with_stops(current_stop,ses,new_rcp_point)
			else:
				print "   [?]: Unknown status %s, stop data: %s" % (st, map.sess[0])
                        if map.sess[0].amt > 0:
                            print "   [xp] %s" % map.sess[0].amt
		else:
			print '   [-] tmp_api empty (no stops in range)'
        except KeyboardInterrupt:
            print "Ending farming run.  Total XP: %s" % config.earned_xp
            sys.exit()
	except Exception, e:
		print '   [-] error work_with_stops: %s' % e
		import traceback
		print traceback.print_exc()
                print "*** len map.sess: %s" % len(map.sess)
                if len(map.sess):
                    print "*** map.sess: %s" % str(map.sess)
                else: print "*** map: %s" % str(map)
		time.sleep(14)