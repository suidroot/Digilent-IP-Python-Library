#!/usr/bin/which python3
#https://reference.digilentinc.com/reference/software/digilent-instrumentation-protocol/protocol

import requests
import pprint
import json

# devicedump = r.text
IPADDRESS = "10.5.6.144"
# pprint.pprint(r.text, indent=5)

class DigilentDevice(object):

    headers = {'Content-Type': 'application/json', 'Accept' : '*/*', 'DHT' : '1', 'Referer' : 'http://waveformslive.com/'}
    deviceinfo = {}
    wavegen = {}
    powersupply = {}
    oscilliscope = {}
    gpio = {}
    logicanalyser = {}

    def __init__(self, ipaddress):

        self.deviceaddress = ipaddress

    def sendcommand(self, payload=None, noparse=False):

        if not payload:
            payload = '{'+self.payloadqueue+'}'

        r = requests.post("http://" + self.deviceaddress + "/", headers=self.headers, data=payload)

        if noparse = False:
            data = json.loads(r.text)

        return data

    def enumeratedevice(self):
        payload = '{"device":[{"command":"enumerate"}]}'
        rparsed = self.sendcommand(payload=payload)

        ## Collect Base device info
        self.deviceinfo = { 'make': rparsed['device'][0]['deviceMake'],
                       'model': rparsed['device'][0]['deviceModel'],
                       'firmware': str(rparsed['device'][0]['firmwareVersion']['major']) \
        + "." + str(rparsed['device'][0]['firmwareVersion']['minor']) + "." +
        str(rparsed['device'][0]['firmwareVersion']['patch'])}

        ## Collect awg info
        totalitems = int(rparsed['device'][0]['awg']['numChans'])

        for x in range(0, totalitems):
            channelinfo = { 'signalTypes': rparsed['device'][0]['awg'][str(x+1)]['signalTypes'],
                            'signalFreqMin': rparsed['device'][0]['awg'][str(x+1)]['signalFreqMin'],
                            'signalFreqMax': rparsed['device'][0]['awg'][str(x+1)]['signalFreqMax'],
                            'dataType': rparsed['device'][0]['awg'][str(x+1)]['dataType'],
                            'bufferSizeMax': rparsed['device'][0]['awg'][str(x+1)]['bufferSizeMax'],
                            'dacVpp': rparsed['device'][0]['awg'][str(x+1)]['dacVpp'],
                            'sampleFreqMin': rparsed['device'][0]['awg'][str(x+1)]['sampleFreqMin'],
                            'sampleFreqMax': rparsed['device'][0]['awg'][str(x+1)]['sampleFreqMax'],
                            'vOffsetMin': rparsed['device'][0]['awg'][str(x+1)]['vOffsetMin'],
                            'vOffsetMax': rparsed['device'][0]['awg'][str(x+1)]['vOffsetMax'],
                            'vOutMin': rparsed['device'][0]['awg'][str(x+1)]['vOutMin'],
                            'vOutMax':rparsed['device'][0]['awg'][str(x+1)]['vOutMax']}

            self.wavegen[x+1] = channelinfo

        ## Collect dc power supply info
        totalitems = int(rparsed['device'][0]['dc']['numChans'])

        for x in range(0, totalitems):
            channelinfo = { 'voltageMin': rparsed['device'][0]['dc'][str(x+1)]['voltageMin'],
                            'voltageMax': rparsed['device'][0]['dc'][str(x+1)]['voltageMax'],
                            'voltageIncrement': rparsed['device'][0]['dc'][str(x+1)]['voltageIncrement'],
                            'currentMin': rparsed['device'][0]['dc'][str(x+1)]['currentMin'],
                            'currentMax': rparsed['device'][0]['dc'][str(x+1)]['currentMax'],
                            'currentIncrement': rparsed['device'][0]['dc'][str(x+1)]['currentIncrement']}

            self.powersupply[x+1] = channelinfo

        ## Collect oscilliscope power supply info
        totalitems = int(rparsed['device'][0]['osc']['numChans'])

        for x in range(0, totalitems):
            channelinfo = { 'resolution': rparsed['device'][0]['osc'][str(x+1)]['resolution'],
                            'effectiveBits': rparsed['device'][0]['osc'][str(x+1)]['effectiveBits'],
                            'bufferSizeMax': rparsed['device'][0]['osc'][str(x+1)]['bufferSizeMax'],
                            'bufferDataType': rparsed['device'][0]['osc'][str(x+1)]['bufferDataType'],
                            'sampleFreqMin': rparsed['device'][0]['osc'][str(x+1)]['sampleFreqMin'],
                            'sampleFreqMax': rparsed['device'][0]['osc'][str(x+1)]['sampleFreqMax'],
                            'delayMax': rparsed['device'][0]['osc'][str(x+1)]['delayMax'],
                            'delayMin': rparsed['device'][0]['osc'][str(x+1)]['delayMin'],
                            'adcVpp': rparsed['device'][0]['osc'][str(x+1)]['adcVpp'],
                            'inputVoltageMax': rparsed['device'][0]['osc'][str(x+1)]['inputVoltageMax'],
                            'inputVoltageMin': rparsed['device'][0]['osc'][str(x+1)]['inputVoltageMin'],
                            'gains': rparsed['device'][0]['osc'][str(x+1)]['gains']}

            self.oscilliscope[x+1] = channelinfo

    def getinstrumentstatus(self, instrument, channel):

        instruments = ['osc', 'awg', 'la', 'gpio', 'dc', 'trigger']

        if instrument in instruments:
            payload = '{"'+instrument+'":{"'+str(channel)+'":[{"command": "getCurrentState"}]}}'
            statusdata = self.sendcommand(payload=payload)

            print statusdata

    def readosc(self, aqcount, channel):
        payload = '{"osc":{"'+str(channel)+'":[{"command": "read", "acqCount": '+str(aqcount)+'}]}}'
        print payload
        data = self.sendcommand(payload=payload)

        return data

    def queuecommand(self, paylod):
        pass

    def printdeviceinfo(self):
        print self.deviceinfo
        print self.wavegen
        print self.powersupply
        print self.oscilliscope


def test():
    ''' Test function '''
    headers = {'Content-Type': 'application/json', 'Accept' : '*/*', 'DHT' : '1', 'Referer' : 'http://waveformslive.com/'}
    payload = '{"osc":{"1":[{"command": "read", "acqCount": 1024}]}}'
    r = self.sendcommand(payload=payload)

    return r

mydevice = DigilentDevice(IPADDRESS)
mydevice.enumeratedevice()
mydevice.printdeviceinfo()
