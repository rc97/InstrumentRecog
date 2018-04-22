import requests

IP = '192.168.1.72'

BASE_URL = 'http://' + IP + ':8090'
BASS_MIN = -9
BASS_MAX = 0
VOL_MAX = 100
VOL_MIN = 0


def setVolume(vol):
	vol = VOL_MIN if vol < VOL_MIN else VOL_MAX if vol > VOL_MAX else vol
	r = requests.post(BASE_URL+'/volume', '<volume>%s</volume>' % vol)

def setBass(bass):
	bass = BASS_MIN if bass < BASS_MIN else BASS_MAX if bass > BASS_MAX else bass
	r = requests.post(BASE_URL+'/bass', '<bass>%s</bass>' % bass)

# def testing():
test = requests.get(BASE_URL+'/bassCapabilities')
print(test.status_code)
print(test.text)
print(test.json)

setBass(0)

test = requests.get(BASE_URL+'/bass')
print(test.status_code)
print(test.text)
print(test.json)