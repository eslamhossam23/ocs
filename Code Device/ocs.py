# PyUPnP - Simple Python UPnP device library built in Twisted
# Copyright (C) 2013  Dean Gardiner <gardiner91@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
from threading import Thread, Event
import time
import sys
from twisted.internet import reactor
from pyupnp.device import Device, DeviceIcon
from pyupnp.logr import Logr
from pyupnp.services import register_action
from pyupnp.services.connection_manager import ConnectionManagerService
from pyupnp.services.content_directory import ContentDirectoryService
from pyupnp.services.microsoft.media_receiver_registrar import MediaReceiverRegistrarService
from pyupnp.ssdp import SSDP
from pyupnp.upnp import UPnP
from accservice import AccService
from myserviceGPS import GPSService
from heartrateservice import HeartRateService
from adxl345 import ADXL345
from GroveGPS import GPS
from gattlib import GATTRequester


class MediaServerDevice(Device):
    deviceType = 'urn:schemas-upnp-org:device:RaspberryPi:1'
#Name that appears in device spy
    friendlyName = "Raspberry Pi"

    def __init__(self):
        Device.__init__(self)

        self.uuid = 'c8728b01-6c51-471e-a497-e9447934a25c'

#Declaration of all service classes
       	self.myService = MSAccService()
	self.gpsService = MSGPSService()
	self.heartRateService = MSHeartRateService()
#Assign services to our device
        self.services = [
            self.myService,
            self.gpsService,
	    self.heartRateService
        ]

        self.icons = [
            DeviceIcon('image/png', 32, 32, 24,
                       'http://172.25.3.103:52323/MediaRenderer_32x32.png')
        ]

        self.namespaces['dlna'] = 'urn:schemas-dlna-org:device-1-0'
        self.extras['dlna:X_DLNADOC'] = 'DMS-1.50'
#This is the thread that interprets the hardware sensor readings of our accelerometer and calculates the steps if we give the command StartSuivi
class AccThread(Thread):
    def __init__(self, service):

	Thread.__init__(self)
        #This is the library used by Grove to capture the values in the 3 axes
	self.adxl345 = ADXL345()
	self.service = service
	self.running = True
    def run(self):
	self.service.steps = str(0)
	while self.running:
            if(self.service.send == True):
                #Get the axes readings
                axes = self.adxl345.getAxes(True)
	        x = abs(float(axes['x']))
                #Equation that calculates the variation in the x axis and compares it to a certain threshold
                #It is considered a step if the value is more than two
                if(x > 2):
                    #Increment the steps by 1
                    valueString = str(self.service.steps)
                    valueString = str(int(valueString) + 1)
                    #Send the steps event
                    self.service.steps = valueString
            #Must sleep for any time so that the thread liberates the device
            time.sleep(.1)
#This is the thread that captures the GPS readings from the GPS sensor
class GPSThread(Thread):
    def __init__(self, service):

	Thread.__init__(self)
	#This is the library used by Grove to capture the GPS values
	self.gps = GPS()
	self.service = service
	self.running = True
    def run(self):
	while self.running:
	    if(self.service.send == True):
                try:
                    #Read the current sensor data
     	            x = self.gps.read()
     	            #Assign the values
		    [t,fix,sats,alt,lat,lat_ns,long,long_ew]=self.gps.vals()
		    #Send the location event
		    self.service.location = lat + "," +  long
	            self.service.send = False
                except IndexError:
		    print "Unable to read"
            #Must sleep this thread to prevent it from occupying the whole device's processing
            time.sleep(1)
#This is the thread that captures the Heart Rate from the bluetooth device
class HeartRateThread(Thread):
    def __init__(self, service):

	Thread.__init__(self)
	self.service = service
	self.running = True
    def run(self):
	while self.running:
            #This is the class used to receive notifications from the bluetooth device
	    ReceiveNotification("00:22:D0:B9:00:1E", self.service)
	    time.sleep(5)

#This is the service that contains the actions and events relating to the Accelerometer
class MSAccService(AccService):
    def __init__(self):
        AccService.__init__(self)
        #Start the thread
	self.thread = AccThread(self)
	self.thread.start()

    @register_action('StartSuivi')
    def startSuivi(self):
        #Start sending events
        self.send = True

    @register_action('StopSuivi')
    def stopSuivi(self):
        #Reset the steps to 0
	self.steps = str(0)
	#Stop sending events
        self.send = False

#This is the service that contains the actions and events relating to the GPS
class MSGPSService(GPSService):
    def __init__(self):
        GPSService.__init__(self)
        #Start the thread
	self.thread = GPSThread(self)
	self.thread.start()

    @register_action('SendLocation')
    def sendLocation(self):
        #Mock data, the location of Ubiquarium
	self.location = "43.615222,7.0716307"
        self.send = True
#This is the service that contains the actions and events relating to the Heart Beat Sensor
class MSHeartRateService(HeartRateService):
    def __init__(self):
        HeartRateService.__init__(self)
        #Start the thread
	self.thread = HeartRateThread(self)
	self.thread.start()

#This is the class used to establish a communication with the bluetooth device
class Requester(GATTRequester):
    def __init__(self, wakeup, *args):
        GATTRequester.__init__(self, *args)
        self.wakeup = wakeup
        
    #This is the method that handles the data received by the device's notification
    def on_notification(self, handle, data):
        print("- notification on handle: {}\n".format(hex(handle)))
        #The following 3 lines handle the parsing of the data received by the notification
	for index, m in enumerate(str(data)):
	    if(index == 4):
		self.heartrate = str(ord(m))
        self.wakeup.set()

#This is the class that establishes communications and receives events from the bluetooth device
class ReceiveNotification(object):
    received = Event()
    req = Requester(received, "00:22:D0:B9:00:1E", False)
    def __init__(self, address, service):
        self.requester = ReceiveNotification.req
	self.received = ReceiveNotification.received
	self.service = service
	if(ReceiveNotification.req.is_connected() == False):
            #Establish communication with device if not connected
            self.connect()
	else:
            #Write into the configuration handle the value 0100 to be able to receive notifications
	    ReceiveNotification.req.write_by_handle(0x13, str(bytearray([1, 0])))
        self.wait_notification()

    def connect(self):
        #Disconnect the last connection
	ReceiveNotification.req.disconnect()
        ReceiveNotification.req.connect(True)
        #Write into the configuration handle the value 0100 to be able to receive notifications
	ReceiveNotification.req.write_by_handle(0x13, str(bytearray([1, 0])))

    def wait_notification(self):
        self.received.wait()
        #Send the event
	self.service.heartrate = self.requester.heartrate
	#Disconnect the last connection
	ReceiveNotification.req.disconnect()



class CommandThread(Thread):
    def __init__(self, device, upnp, ssdp):
        """

        :type device: Device
        :type upnp: UPnP
        :type ssdp: SSDP
        """
        Thread.__init__(self)
        self.device = device
        self.upnp = upnp
        self.ssdp = ssdp

        self.running = True

    def run(self):
        while self.running:
            try:
                command = 'command_' + raw_input('')

                if hasattr(self, command):
                    getattr(self, command)()
            except EOFError:
                self.command_stop()
            except KeyboardInterrupt:
                self.command_stop()

    def command_stop(self):
        # Send 'byebye' NOTIFY
        self.ssdp.clients.sendall_NOTIFY(None, 'ssdp:byebye', True)

        # Stop everything
        self.upnp.stop()
        self.ssdp.stop()
        reactor.stop()
        self.running = False

if __name__ == '__main__':
    Logr.configure(logging.DEBUG)

    device = MediaServerDevice()

    upnp = UPnP(device)
    ssdp = SSDP(device)

    upnp.listen()
    ssdp.listen()

    def event_test():
#        device.contentDirectory.system_update_id = time.time()
        reactor.callLater(5, event_test)

    event_test()

    r = CommandThread(device, upnp, ssdp)
    r.start()

    reactor.run()
