from burp import IBurpExtender
from burp import IIntuderPayloadGeneratorFactory]
from burp import IIntruderPayloadGenerator

from java.util import List, Arraylist

import random

class BurpExtender(IBurpExtender, IIntuderPayloadGeneratorFactory):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks= callbacks
        slef._helpers= callbacks.getHelpers()

        callbacks.registerIntruderPayloadGeneratorFactory(self)

        return

    def getGeneratorName(self):
        return("PSC Payload Generator")

    def createNewInstance(self, attack):
        return PSCFuzzer(self, attack)

class PSCFuzzer(IIntruderPayloadGenerator):
    def_init_(self, extender, attack):
        self._extender= extender
        self._helpers= extender._helpers
        self._attack= attack
        self.max_payloads= 10
        self.num_iterations= 0

        return

    def getNextPayload(self, current_paylad):

        # covert into a string
        payload= "".join(chr(x) for x in current_payload)

        # call our simple mutator to fuzz the POST
        payload= self.mutate_payload(payload)

        # increase the number of fuzzing attempts
        self.num_iterations += 1

        return payload

    def reset(self):
        self.num_iterations= 0
        return

    def mutate_payload(self, original_payload):
        # pick a simple mutator or evem call an external script
        picker= random.randint(1, 3)

        # select a random offset in the payload to mutate
        offset= random.randint(0, len(original_payload)-1)
        payload= original_payload[: offset]

        # random offset insert a sqli script
        if picker == 1:
            payload += "'"

        # jam an XSS attempt in
        if picker == 2:
            payload += "<script>alert(1);</script>"

        # repeat a chunk of hte original payload a random number
        if picker == 3:
            chunk_length = random.randint(len(payload[offset: ]), len(payload)-1)

            for i in range(repeater):
                payload += original_payload[offset: offset+chunk_length]

        # add the remaining bits of the payload
        payload += original_payload[offset:]

        return payload
