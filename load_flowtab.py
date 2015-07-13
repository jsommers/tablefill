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
    print "Connection from {}".format(dpid_to_mac(event.connection.dpid))
    # event.connection.features
    # event.connection.ports
    print "ports:",event.connection.ports
    print "ports:",event.connection.features

    #inport = event.port
    #packet = event.parsed
    #if not packet.parsed:
    #  log.warning("%i %i ignoring unparsed packet", dpid, inport)
    #  return
#
#    actions = []
#    actions.append(of.ofp_action_dl_addr.set_dst(mac))
#    actions.append(of.ofp_action_output(port = prt))
#    match = of.ofp_match.from_packet(packet, inport)
#    match.dl_src = None # Wildcard source MAC
#
#    msg = of.ofp_flow_mod(command=of.OFPFC_ADD,
#                          idle_timeout=FLOW_IDLE_TIMEOUT,
#                          hard_timeout=of.OFP_FLOW_PERMANENT,
#                          buffer_id=event.ofp.buffer_id,
#                          actions=actions,
#                          match=of.ofp_match.from_packet(packet,
#                                                         inport))
#    event.connection.send(msg.pack())

  def _handle_FlowRemoved(self, event):
    pass

  def _handle_ErrorIn(self, event):
    print "Got error from switch: {}".format(event.asString())

  def _handle_PacketIn (self, event):
    pass

def launch ():
  core.registerNew(rule_loader)

