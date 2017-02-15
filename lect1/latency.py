"""
Question:
Pick one IP from each region, find network latency from via the below code snippet
(ping 3 times), and finally sort regions by the average latency.
http://ec2-reachability.amazonaws.com/
Sample output:
1. us-west-1 [50.18.56.1] - Smallest average latency
2. xx-xxxx-x [xx.xx.xx.xx] - x
3. xx-xxxx-x [xx.xx.xx.xx] - x
...
15. xx-xxxx-x [xx.xx.xx.xx] - Largest average latency
"""
import subprocess


# host = "yahoo.com"
#
# ping = subprocess.Popen(
#     ["ping", "-c", "3", host],
#     stdout = subprocess.PIPE,
#     stderr = subprocess.PIPE
# )
#
# out, error = ping.communicate()
# print out

class LatencyCalculator:

    def __init__(self):
        self.__region_map = {
            "us-east-1": "50.17.255.254",
            "us-west-1": "52.9.63.252",
            "eu-west-1": "46.137.120.1",
            "us-west-2": "52.10.63.252",
            "eu-central-1": "52.29.63.252",
            "eu-west-2": "52.56.34.0",
            "us-gov-west-1": "52.222.9.163",
            "ca-central-1": "52.60.50.0",
            "us-east-2": "52.14.64.0",
            "ap-northeast-1": "52.68.63.252",
            "ap-northeast-2": "52.79.52.64",
            "ap-southeast-1": "52.74.0.2",
            "ap-southeast-2": "52.64.63.253",
            "ap-south-1": "52.66.66.2",
            "sa-east-1": "54.94.191.252"
        }

        self.__latency_map = {}
        self.__failed_regions = []

    def calculate(self):
        # clear all variables, we don't want to keep results from previous iterations of lc.calculate()
        self.__latency_map = {}
        self.__failed_regions = []

        # get latency for regions
        for region in self.__region_map.keys():
            host = self.__region_map.get(region)
            average_latency = self.__get_average_latency_for_host(host)
            if average_latency >= 0:
                self.__latency_map[region] = average_latency
            else:
                self.__failed_regions.append(region)

        self.__print_latencies()

    def __get_average_latency_for_host(self, host):
        ping = subprocess.Popen(
            ["ping", "-c", "3", host],
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE
        )

        out, error = ping.communicate()

        if not error or error == '':
            # if output is valid, then parse to get times from it
            #print("Successfully pinged: ", host)
            return self.__get_average_latency_from_response(out)
        else:
            return -1

    def __get_average_latency_from_response(self, response):
        lines = response.split("\n")
        total_time = 0.0
        total_num_pings = 0
        for line in lines:
            if "time=" in line:
                time_lines = line.split("time=")
                time = time_lines[1].replace(" ms", "")
                total_time += float(time)
                total_num_pings += 1

        if total_num_pings > 0:
            return total_time/total_num_pings
        else:
            return -1

    def __print_latencies(self):
        index = 1
        # print latencies for regions
        sorted_regions_by_avg_latency = sorted(self.__latency_map, key=self.__latency_map.get)
        for region in sorted_regions_by_avg_latency:
            host = self.__region_map[region]
            latency = self.__latency_map[region]
            print(str(index) + ". " + region + " [" + host + "] - " + str(latency) + " ms")
            index += 1

        # print failed regions
        for region in self.__failed_regions:
            host = self.__region_map[region]
            print(str(index) + ". " + region + " [" + host + "] - PING FAILED")
            index += 1



# end of class

# run from here
lc = LatencyCalculator()
lc.calculate()
