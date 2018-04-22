import libsoundtouch as lst

ip = '192.168.1.72'

device = lst.soundtouch_device(ip)
print(device)

status = device.status()
print(status)

volume = device.volume()
print(volume.actual)
device.set_volume(50)
volume = device.volume()
print(volume.actual)