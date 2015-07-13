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
    log.info("Connection from {}".format(dpid_to_mac(event.connection.dpid)))

    log.info("Clearing all flows from switch")
    msg = of.ofp_flow_mod(command=of.OFPFC_DELETE)
    event.connection.send(msg)

    # event.connection.features
    # event.connection.ports
    # print "ports:",event.connection.ports
    # print "ports:",event.connection.features


# msg = of.ofp_flow_mod()
# msg.priority = 42
# msg.match.dl_type = 0x800
# msg.match.nw_dst = IPAddr("192.168.101.101")
# msg.match.tp_dst = 80
# msg.actions.append(of.ofp_action_output(port = 4))
# self.connection.send(msg)
 
# Same exact thing, but in a single line...

# command: OFPFC_ADD, OFPFC_MODIFY, OFPFC_MODIFY_STRICT, OFPFC_DELETE, OFPFC_DELETE_STRICT
# idle_timeout
# hard_timeout OFP_FLOW_PERMANENT
# priority # OFP_DEFAULT_PRIORITY
# buffer_id None
# out_port = OFPP_NONE
# flags OFPFF_SEND_FLOW_REM, OFPFF_CHECK_OVERLAP, OFPFF_EMERG

# actions
# ofp_action_output (port=?)

# match in_port Switch port number the packet arrived on
# dl_src  Ethernet source address
# dl_dst  Ethernet destination address
# dl_vlan VLAN ID
# dl_vlan_pcp VLAN priority
# dl_type Ethertype / length (e.g. 0x0800 = IPv4)
# nw_tos  IP TOS/DS bits
# nw_proto  IP protocol (e.g., 6 = TCP) or lower 8 bits of ARP opcode
# nw_src  IP source address
# nw_dst  IP destination address
# tp_src  TCP/UDP source port
# tp_dst  TCP/UDP destination port

# self.connection.send( of.ofp_flow_mod( action=of.ofp_action_output( port=4 ),
#                                        priority=42,
#                                        match=of.ofp_match( dl_type=0x800,
#                                                            nw_dst="192.168.101.101",
#                                                            tp_dst=80 )))



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
    log.info("Flow removed from switch: {}".format(event.asString()))

  def _handle_ErrorIn(self, event):
    log.info("Got error from switch: {}".format(event.asString()))

  def _handle_PacketIn (self, event):
    log.info("Got PacketIn: not handling.")

def launch ():
  core.registerNew(rule_loader)
