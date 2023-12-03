from mininet.net import Mininet
from mininet.node import Controller, OVSKernelAP
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel

def create_topology():
    # Create Mininet network with specified controllers, access points, and links
    network = Mininet(controller=Controller, accessPoint=OVSKernelAP, link=TCLink)

    # Add controller to the network
    ctrl = network.addController('c0')

    # Add access points with specific configurations
    olsr_ap1 = network.addAccessPoint('ap1', ssid='adhocUoH_HT40+', mode='g', channel='1', position='10,10,0')
    olsr_ap2 = network.addAccessPoint('ap2', ssid='adhocUoH_HT40+', mode='g', channel='6', position='20,20,0')
    olsr_ap3 = network.addAccessPoint('ap3', ssid='adhocUoH_HT40+', mode='g', channel='11', position='30,30,0')

    # Add adhoc stations with specific positions
    adhoc_station1 = network.addStation('adhoc1', position='5,5,0')
    adhoc_station2 = network.addStation('adhoc2', position='15,15,0')
    adhoc_station5 = network.addStation('adhoc5', position='35,35,0')
    adhoc_station6 = network.addStation('adhoc6', position='40,40,0')

    # Add links between access points and adhoc stations
    network.addLink(olsr_ap1, adhoc_station1)
    network.addLink(olsr_ap2, adhoc_station2)
    network.addLink(olsr_ap3, adhoc_station5)
    network.addLink(olsr_ap3, adhoc_station6)

    # Start the network
    network.build()
    ctrl.start()
    olsr_ap1.start([ctrl])
    olsr_ap2.start([ctrl])
    olsr_ap3.start([ctrl])

    # Enable IPv6 on stations
    for adhoc in [adhoc_station1, adhoc_station2, adhoc_station5, adhoc_station6]:
        adhoc.cmd('ip -6 addr add dev {}-wlan0'.format(adhoc.name))

    return network

def configure_protocols(network):
    # Set up OLSR on specified adhoc hosts
    for adhoc in [network.get('adhoc2'), network.get('adhoc5')]:
        adhoc.cmd('echo olsr >> /etc/quagga/daemons')
        adhoc.cmd('service quagga restart')

    # Set up BATMAN on specified adhoc host
    network.get('adhoc6').cmd('echo batman_adv >> /etc/modules')

def initiate_icmp_stream(network):
    # Initiate ICMP stream between adhoc hosts
    adhoc_station1.cmd('ping6 -i 0.1 -c 30 %s' % adhoc_station2.IP())
    adhoc_station1.cmd('ping6 -i 0.1 -c 30 %s' % adhoc_station5.IP())

def initiate_tcp_transfers(network):
    # Initiate TCP transfers between adhoc hosts using specified port
    adhoc_station2.cmd('iperf -s -p 5538 &')
    adhoc_station6.cmd('iperf -s -p 5538 &')

    adhoc_station1.cmd('iperf -t 30 -c %s -p 5538' % adhoc_station2.IP())
    adhoc_station5.cmd('iperf -t 30 -c %s -p 5538' % adhoc_station6.IP())

def main():
    setLogLevel('info')

    # Create Mininet-WiFi network
    wifi_network = create_topology()

    # Configure adhoc protocols
    configure_protocols(wifi_network)

    # Initiate ICMP stream
    initiate_icmp_stream(wifi_network)

    # Initiate TCP transfers
    initiate_tcp_transfers(wifi_network)

    # Start Mininet-WiFi CLI
    CLI(wifi_network)

    # Stop Mininet-WiFi
    wifi_network.stop()

if __name__ == '__main__':
    main()
