import json
import socket

import fail2ban.server.actions
import paho.mqtt.client as paho_client

__author__ = 'Ruben Kerkhof <ruben@tilaa.com>'
__license__ = 'GPLv2'


class MosquittoAction(fail2ban.server.actions.ActionBase):
	'''Fail2Ban action which publishes to MQTT'''

	def __init__(self, jail, name, host='localhost', port=1883, topic='fail2ban', ):
		super(MosquittoAction, self).__init__(jail, name)
		self._topic = topic
		self._jail = jail
		self._fqdn = socket.getfqdn()
		self._client=paho_client.Client()
		self._client.connect(host=host, port=port)
		

	def _sendmsg(self, action, ip, time, failures):
		payload = {
			'action': action,
			'hostname': self._fqdn,
			'jail': self._jail.name,
			'bantime': self._jail.actions.getBanTime(),
			'ip': ip,
			'time': time,
			'failures': failures,
		}

		return self._client.publish(
			topic=self._topic,
			payload=json.dumps(payload)
		)


	def ban(self, info):
		self._sendmsg(
			action='ban',
			ip=info['ip'],
			time=info['time'],
			failures=info['failures'],
		)


	def unban(self, info):
		self._sendmsg(
			action='unban',
			ip=info['ip'],
			time=info['time'],
			failures=info['failures']
		)


Action = MosquittoAction
