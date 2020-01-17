import sys
sys.path.insert(0, "/usr/local/samba/lib/python3.7/site-packages")


import samba
import ldb

from samba import dsdb
from samba.samdb import SamDB
from samba.param import LoadParm
from samba.auth import system_session
from samba.credentials import Credentials

from sambaAPI.domain.models import Domain

class ConnectionService:
	domain = None

	def __init__(self,domain_name):
		try:
			self.domain = Domain.objects.get(domain_name=domain_name)
		except Exception as e:
			print(e)
			self.domain = None


	def connection(self):
		lp = LoadParm()
		creds = Credentials()
		creds.guess(lp)
		creds.set_username("")
		creds.set_password("")
		con = SamDB(url='ldap://192.168.100.26:389' , session_info=system_session(),
						 credentials=creds, lp=lp)
		return con


