import socket
import argparse
import time
from random import randint
from dummy_hp import DummyHP


class DummyMP(DummyHP):

    def __init__(self, port, splitter, peer_list, targets):
        super().__init__(port, splitter, peer_list)
        self.targets = targets
        self.port = port

    def run(self):
        while True:
            data, address = self.receive()
            print("{} received from {}".format(data, address))
            if data == "-9":
                exit()
            if address[0] == self.splitter:
                if len(self.targets) == 0:
                    target = ("10.0.0."+str(randint(1, len(peer_list))),
                              self.port)
                    targets = [target]
                    print("New Target: {}".format(targets[0]))
                else:
                    targets = self.targets[:]
                for p in self.peer_list:
                    if p in targets:
                        self.send(0, p)
                        print("\t{} sent to {} Attack!".
                              format(str(0), p))
                    else:
                        self.send(data, p)
                        print("\t{} sent to {}".format(data, p))
                    time.sleep(0.02)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int,
                        help="UDP port used by peers")
    parser.add_argument("-s", "--splitter", type=str,
                        help="Splitter address")
    parser.add_argument("-z", "--size", type=int,
                        help="Team size (without splitter)")
    parser.add_argument("-t", "--targets", type=int, nargs='+',
                        help="List of peer to attack (ex. 1 2 4)")
    args = parser.parse_args()

    peer_list = []
    for p in range(1, args.size+1):
        peer_list.append(("10.0.0."+str(p), args.port))

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((args.splitter, 1))
    local_ip_address = s.getsockname()[0]

    print("Local IP {}".format(local_ip_address))
    peer_list.remove((local_ip_address, args.port))
    print("Peers List:{}".format(peer_list))

    targets = []
    for p in args.targets:
        if p != 0:
            targets.append(("10.0.0."+str(p), args.port))

    print("Targets List:{}".format(targets))

    peer = DummyMP(args.port, args.splitter, peer_list, targets)
    peer.run()
