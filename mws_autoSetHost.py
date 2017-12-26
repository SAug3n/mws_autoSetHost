# -*- coding: UTF-8 –*-.
import requests
import threading
import time
import re
import os
import sys

class Get_info(threading.Thread):
    fastest_ip=None
    ms=9999
    def __init__(self,id,host_name):
        threading.Thread.__init__(self)
        self.id = id
        self.host_name=host_name
        
    def run(self):
        ip_addr=get_current_ip(self.id,self.host_name)
        if not ip_addr:
        	return
        threadLock.acquire()
        if(ip_addr[2]!="timeout"):
       		print ip_addr[0]+'-----'+ip_addr[1]+'-----'+ip_addr[2]+'ms'
       		if(int(ip_addr[2]) < self.__class__.ms):
       			self.__class__.ms=int(ip_addr[2])
       			self.__class__.fastest_ip=ip_addr[0]
       	else:
       		print ip_addr[0]+'-----'+ip_addr[1]+'-----timeout'
        threadLock.release()


def get_list(url):
	pattern=re.compile(r'<li id="([0-9a-z-]{30,})"')
	r = requests.get('http://ping.chinaz.com/'+url)
	id_list=pattern.findall(r.text.encode("GB18030"),re.M)
	return id_list

def get_current_ip(ip_id,host_name):
	res_list=[]
	ping_res=''
	pattern=re.compile(r'{state:1,msg:\'\',result:{ip:\'([0-9.]{7,15})\',ipaddress:\'(.*)\',responsetime')
	pattern2=re.compile(r'([0-9]*)ms TTL=')
	param={'guid':ip_id,'host':host_name,'ishost':'0','encode':'xTBXpIKlo42VoLGUHvM/E3WvzLO8jIDT','checktype':'0'}
	r=requests.post("http://ping.chinaz.com/iframe.ashx?t=ping&callback=jQuery1113047383526910688956_1514185718519",data=param)
	res=pattern.search(r.text.encode("GB18030"),re.M)
	if not res:
		return
	ping = os.popen('ping -n 1 '+res.group(1),"r")
	while 1:
		line = ping.readline()
   		if not line:
   			break
   		ping_res+=line
	res_list.append(res.group(1))
	res_list.append(res.group(2))
	if "ms" in str(ping_res):
		delay_res=pattern2.search(ping_res,re.M)
		res_list.append(delay_res.group(1))
		return res_list
	res_list.append("timeout")
	return res_list

def show_host():
	host_list=[]
	host_path="C:\Windows\System32\drivers\etc\hosts"
	host_file=open(host_path,"r")
	while 1:
		line = host_file.readline()
   		if not line:
   			break
   		host_list.append(line)
   	host_file.close()
   	return host_list

def host_write(host_list,ip,host_name):
	host_path="C:\Windows\System32\drivers\etc\hosts"
	host_file=open(host_path,"w")
	write=0
	content=""
	for line in range(len(host_list)):
		if(host_list[line][0]!="#" and host_name in host_list[line]):
			host_list[line]=ip+' '+host_name+'\n'
			write=1
	if(write==0):
		host_list.append(ip+' '+host_name+'\n')
	for line in host_list:
		content+=line
	host_file.write(content)
	host_file.close()

if __name__=='__main__':

	if(len(sys.argv)<2):
		host_name="steamcommunity.com"
	if(len(sys.argv)==2):
		host_name=sys.argv[1]

	threadLock = threading.Lock()
	threads=[]
	id_list=get_list(host_name)
	for ip_id in id_list:
		t=Get_info(ip_id,host_name)
		t.start()
		threads.append(t)
	for ths in threads:
		ths.join()
	print 'the fastest_ip is '+Get_info.fastest_ip
	host_list=show_host()
	host_write(host_list,Get_info.fastest_ip,host_name)
	print 'set host done!'
