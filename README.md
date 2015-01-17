This is a custom action for fail2ban

It publishes bans and unbans on a MQTT topic

To use it you need to:
 - copy this action into your actions.d directory
 - pip install paho-mqtt
 - configure a jail, for example:

[sshd]
enabled = true
action = mosquitto.py


The action supports optional parameters, for example
[sshd]
enabled = true
action = mosquitto.py[host='myhost', port=8080, topic='mytopic']


