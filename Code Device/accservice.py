from pyupnp.event import EventProperty
from pyupnp.services import Service, ServiceActionArgument,\
    register_action, ServiceStateVariable

class AccService(Service):
    version = (1, 0)
    serviceType = "urn:schemas-upnp-org:service:Accelerometre:1"
    serviceId = "urn:upnp-org:serviceId:Accelerometre"

    subscription_timeout_range = (None, None)

    stateVariables = [
        # Arguments
        ServiceStateVariable('steps',         'string', sendEvents=True),
            ]

    actions = {
        'StartSuivi': [
        ],
	'StopSuivi': [
        ],
    }

    steps = EventProperty('steps')
    send = False

    @register_action('StartSuivi')
    def startSuivi(self):
        raise NotImplementedError()

    @register_action('StopSuivi')
    def stopSuivi(self):
        raise NotImplementedError()
