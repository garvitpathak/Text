from mininet.net import Mininet
from mininet.node import Controller, OVSSwitch
from mininet.cli import CLI

def setup_network():
    # Initialize Mininet network with specified controller and switch
    network = Mininet(controller=Controller, switch=OVSSwitch)

    # Add the designated controller
    main_controller = network.addController('c0')

    # Add switches for the different buildings
    building_switch1 = network.addSwitch('s1')  # Switch for Building 1
    building_switch2 = network.addSwitch('s2')  # Switch for Building 2
    building_switch3 = network.addSwitch('s3')  # Switch for Building 3

    # Add switches for the server and server room
    server_switch1 = network.addSwitch('s4')  # Server Switch 1
    server_switch2 = network.addSwitch('s5')  # Server Switch 2

    # Add switches for lecture rooms in each building
    lecture_room_switch1 = network.addSwitch('s6')  # Lecture Room in Building 1
    lecture_room_switch2 = network.addSwitch('s7')  # Lecture Room in Building 2
    lecture_room_switch3 = network.addSwitch('s8')  # Lecture Room in Building 3

    # Add PCs for each lecture room
    pc1 = network.addHost('H1', ip='100.0.0.1/16')  # PC in Lecture Room 1
    pc2 = network.addHost('H2', ip='100.0.0.2/16')  # PC in Lecture Room 2
    udp_client = network.addHost('UDP_Client', ip='200.0.0.1/16')  # UDP Client in Lecture Room 3
    pc4 = network.addHost('H4', ip='200.0.0.2/16')  # PC in Lecture Room 4
    pc5 = network.addHost('H5', ip='300.0.0.1/16')  # PC in Lecture Room 5
    pc6 = network.addHost('H6', ip='300.0.0.2/16')  # PC in Lecture Room 6
    pc7 = network.addHost('H7', ip='400.0.0.1/16')  # PC in Lecture Room 7
    pc8 = network.addHost('H8', ip='400.0.0.2/16')  # PC in Lecture Room 8
    pc9 = network.addHost('H9', ip='500.0.0.1/16')  # PC in Lecture Room 9
    pc10 = network.addHost('H10', ip='500.0.0.2/16')  # PC in Lecture Room 10
    pc11 = network.addHost('H11', ip='600.0.0.1/16')  # PC in Lecture Room 11
    pc12 = network.addHost('H12', ip='600.0.0.2/16')  # PC in Lecture Room 12

    # Add servers in the server room
    server_host1 = network.addHost('Server', ip='12.0.0.1/8')  # Server 1 in Server Room
    udp_server = network.addHost('UDP_Server', ip='41.0.0.1/8')  # UDP Server in Server Room

    # Create links with assigned UDP port
    network.addLink(building_switch1, lecture_room_switch1, port1=1, port2=1)
    network.addLink(building_switch1, lecture_room_switch2, port1=2, port2=1)
    network.addLink(building_switch2, lecture_room_switch3, port1=1, port2=1)
    network.addLink(building_switch2, lecture_room_switch1, port1=2, port2=2)
    network.addLink(building_switch3, lecture_room_switch2, port1=1, port2=2)
    network.addLink(building_switch3, lecture_room_switch3, port1=2, port2=2)

    network.addLink(lecture_room_switch1, pc1)
    network.addLink(lecture_room_switch1, pc2)
    network.addLink(lecture_room_switch2, udp_client)
    network.addLink(lecture_room_switch2, pc4)
    network.addLink(lecture_room_switch3, pc5)
    network.addLink(lecture_room_switch3, pc6)

    # Establish links to connect server room and lecture rooms
    network.addLink(server_switch1, server_host1)
    network.addLink(server_switch2, udp_server, port1=1, port2=7738)  # Assigning UDP port 7738 to the link

    # Interconnect the buildings and server room
    network.addLink(building_switch1, building_switch2)
    network.addLink(building_switch2, building_switch3)
    network.addLink(building_switch3, building_switch1)

    network.addLink(building_switch1, server_switch1)
    network.addLink(building_switch2, server_switch1)
    network.addLink(building_switch2, server_switch2)
    network.addLink(building_switch3, server_switch2)

    # Build the network
    network.build()

    # Start the controller and switches
    main_controller.start()
    building_switch1.start([main_controller])
    building_switch2.start([main_controller])
    building_switch3.start([main_controller])
    server_switch1.start([main_controller])
    server_switch2.start([main_controller])

    # Initiate the Mininet CLI for manual configuration if necessary
    CLI(network)

    # Stop the Mininet network
    network.stop()

if __name__ == '__main__':
    setup_network()
