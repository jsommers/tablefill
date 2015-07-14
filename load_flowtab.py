from pox.core import core
import pox
log = core.getLogger()

from pox.lib.packet.ethernet import ethernet, ETHER_BROADCAST
from pox.lib.packet.ipv4 import ipv4
from pox.lib.packet.arp import arp
from pox.lib.addresses import IPAddr, EthAddr
from pox.lib.util import str_to_bool, dpid_to_str
from pox.lib.recoco import Timer
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *

import time
import random

def dpid_to_mac (dpid):
    return EthAddr("%012x" % (dpid & 0xffFFffFFffFF,))

class rule_loader (EventMixin):
    def __init__ (self):
        # self._expire_timer = Timer(5, self._handle_expiration, recurring=True)

        self.listenTo(core)

    def _handle_GoingUpEvent (self, event):
        self.listenTo(core.openflow)
        log.debug("Up...")

    def _handle_ConnectionUp(self, event):
        log.info("Connection from {}".format(dpid_to_mac(event.connection.dpid)))

        log.info("Clearing all flows from switch")
        msg = of.ofp_flow_mod(command=of.OFPFC_DELETE)
        event.connection.send(msg)

        msg = of.ofp_barrier_request()
        event.connection.send(msg)

        self.state = "Loading"

        # event.connection.features
        # event.connection.ports
        # print "ports:",event.connection.ports
        # print "ports:",event.connection.features

    def _handle_BarrierIn(self, event):
        log.debug("Got barrier.")

        if self.state == "Loading":
            self.mods = []

            for i in range(5000):
                msg = of.ofp_flow_mod()
                msg.priority = random.randint(0x8000, 0xffff)
                msg.command = of.OFPFC_ADD

                matcher = of.ofp_match()
                matcher.dl_type = 0x0800
                matcher.nw_src = IPAddr(random.randint(1,2**32-1))
                matcher.nw_dst = '10.{}.{}.0/24'.format(i/256, i%256)

                msg.match = matcher
                # msg.idle_timeout = OFP_FLOW_PERMANENT
                msg.hard_timeout = of.OFP_FLOW_PERMANENT
                msg.buffer_id = None
                msg.flags = of.OFPFF_CHECK_OVERLAP | of.OFPFF_SEND_FLOW_REM 

                msg.actions.append(of.ofp_action_output(port = 13))
                self.mods.append(msg)
                event.connection.send(msg)
                if i % 100 == 0:
                    log.debug("Sent mod message {}".format(i))
                    time.sleep(1)

            self.state = "Removing"
            msg = of.ofp_barrier_request()
            event.connection.send(msg)
            log.debug("Sending post-add barrier")

        elif self.state == "Removing":
            while len(self.mods):
                i = random.randint(0, len(self.mods)-1)        
                msg = self.mods.pop(i)
                msg.command = of.OFPFC_DELETE
                event.connection.send(msg)
                if len(self.mods) % 25:
                    log.debug("Remaining mods to remove: {}".format(len(self.mods)))
     
    def _handle_FlowRemoved(self, event):
        log.info("Flow removed from switch: {}".format(event))

    def _handle_ErrorIn(self, event):
        log.info("Got error from switch: {}".format(event.asString()))

    def _handle_PacketIn (self, event):
        log.info("Got PacketIn: not handling.")

def launch ():
    core.registerNew(rule_loader)
