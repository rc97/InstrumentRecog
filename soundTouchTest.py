from libsoundtouch import discover_devices
from libsoundtouch import soundtouch_device
from libsoundtouch.utils import Source, Type


devices = discover_devices(timeout=10)


for device in devices:
	print(device.config.name + " - " + device.config.type)

device = soundtouch_device('192.168.1.72')

# Config object
print(device.config.name)

# Status object
# device.status() will do an HTTP request. Try to cache this value if needed.
status = device.status()
print(status.source)
print(status.artist + " - "+ status.track)
device.pause()
device.next_track()
device.play()

account_id = device.status().content_item.source_account
print(account_id)