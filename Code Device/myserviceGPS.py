from pyupnp.event import EventProperty
from pyupnp.services import Service, ServiceActionArgument,\
    register_action, ServiceStateVariable

class GPSService(Service):
    version = (1, 0)
    serviceType = "urn:schemas-upnp-org:service:GPS:1"
    serviceId = "urn:upnp-org:serviceId:GPS"

    subscription_timeout_range = (None, None)

    stateVariables = [
        # Arguments
        ServiceStateVariable('location',         'string', sendEvents=True),
            ]
    actions = {
        'SendLocation': [
        ],
    }

    location = EventProperty('location')
    send = False

    @register_action('SendLocation')
    def sendLocation(self):
        raise NotImplementedError()
