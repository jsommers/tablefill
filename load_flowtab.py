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
    for i in range(1000):
      prio = 0xff00 - i
      msg = of.ofp_flow_mod()
      msg.priority = prio
      msg.command = OFPFC_ADD

      matcher = of.ofp_match()
      matcher.dl_type = 0x0800
      matcher.nw_dst = '10.{}.{}.0/24'.format(i/256, i%256)

      msg.match = matcher
      # msg.idle_timeout = OFP_FLOW_PERMANENT
      msg.hard_timeout = OFP_FLOW_PERMANENT
      msg.buffer_id = None
      msg.flags = OFPFF_CHECK_OVERLAP | OFPFF_SEND_FLOW_REM 

      msg.actions.append(of.ofp_action_output(port = 13))
      self.connection.send(msg)

 
  def _handle_FlowRemoved(self, event):
    log.info("Flow removed from switch: {}".format(event.asString()))

  def _handle_ErrorIn(self, event):
    log.info("Got error from switch: {}".format(event.asString()))

  def _handle_PacketIn (self, event):
    log.info("Got PacketIn: not handling.")

def launch ():
  core.registerNew(rule_loader)
