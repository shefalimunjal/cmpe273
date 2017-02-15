import psutil

class SocketMonitor:
    def __init__(self):
        self.__pid_connections_map = {}

    def monitor(self):
        self.__pid_connections_map = {}
        connections = self.__get_all_connections()
        self.__populate_pid_connection_map(connections)

    def __get_all_connections(self):
        return psutil.net_connections()

    def __populate_pid_connection_map(self, connections):
        for sconn in connections:
            if sconn.laddr and sconn.raddr and sconn.status and sconn.status != 'NONE':
                if not sconn.pid in self.__pid_connections_map:
                    self.__pid_connections_map[sconn.pid] = []

                self.__pid_connections_map[sconn.pid].append(sconn)

    def print_pid_connections_map(self):
        print('"pid","laddr","raddr","status"')
        for pid in sorted(self.__pid_connections_map, key=self.__get_num_connections, reverse=True):
            connections = self.__pid_connections_map[pid]
            for connection in connections:
                laddr = connection.laddr[0] + "@" + str(connection.laddr[1])
                raddr = connection.raddr[0] + "@" + str(connection.raddr[1])
                print '"%s","%s","%s","%s"' %(pid, laddr, raddr, connection.status)

    def __get_num_connections(self, pid):
        return len(self.__pid_connections_map[pid])

sm = SocketMonitor()
sm.monitor()
sm.print_pid_connections_map()



