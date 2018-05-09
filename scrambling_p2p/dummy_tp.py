import socket
import argparse
import math
from dummy_hp import DummyHP


class DummyTP(DummyHP):

    def __init__(self, port, splitter, peer_list):
        super().__init__(port, splitter, peer_list)

    def attack_detected(self, last_chunk):
        _round = math.ceil(int(last_chunk) / (len(peer_list) + 1))
        print("\033[91m Attack! \033[0m in round {}".format(_round))
        self.send(_round, (self.splitter, self.port))
        for p in self.peer_list:
            self.send("-9", p)
        exit()

    def run(self):
        last_chunk = 0
        while True:
            data, address = self.receive()
            print("{} received from {}".format(data, address))
            if data == "0":
                self.attack_detected(last_chunk)
            if address[0] == self.splitter:
                last_chunk = data
                for p in self.peer_list:
                    self.send(data, p)
                    print("\t{} sent to {}".format(data, p))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int,
                        help="UDP port used by peers")
    parser.add_argument("-s", "--splitter", type=str,
                        help="Splitter address")
    parser.add_argument("-z", "--size", type=int,
                        help="Team size (without splitter)")
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
    peer = DummyTP(args.port, args.splitter, peer_list)
    peer.run()