from pyupnp.event import EventProperty
from pyupnp.services import Service, ServiceActionArgument,\
    register_action, ServiceStateVariable

class HeartRateService(Service):
    version = (1, 0)
    serviceType = "urn:schemas-upnp-org:service:HeartRate:1"
    serviceId = "urn:upnp-org:serviceId:HeartRate"

    subscription_timeout_range = (None, None)

    stateVariables = [
        # Arguments
        ServiceStateVariable('heartrate',         'string', sendEvents=True),
            ]


    heartrate = EventProperty('heartrate')
