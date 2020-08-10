import argparse
import os
import telnetlib
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import sys
import json
import time


def check_port(ip, port, lock, res):
    server = telnetlib.Telnet()
    try:
        server.open(ip, port)
        print("%s:%s is open" %(ip, port))
        try:
            lock.acquire()
            content = str(ip) + ":" + str(port)
            res.append(content)
        finally:
            lock.release()
    except Exception as err:
        print("%s:%s is not open" % (ip, port))
    finally:
        server.close()


def ping(ip, lock, res):
    try:
        if os.name == 'nt':
            command = 'ping -n 1 ' + ip
        else:
            command = 'ping -c 1 ' + ip
        result = os.system(command)
        if result == 0:
            print("Ping is ok in %s" % ip)
            try:
                lock.acquire()
                content = str(ip)
                res.append(content)
            finally:
                lock.release()
            return ip
        else:
            print("Ping is not ok in %s" % ip)
            return None
    except Exception as err:
        print("Ping met exception: %s" %err)
        return None


def process_ip(ip_range):
    ip_list = []
    if '-' in ip_range:
        ips = ip_range.split('-')
        assert len(ips) == 2
        parts_one = ips[0].split('.')
        parts_two = ips[1].split('.')
        assert len(parts_one) == 4
        assert len(parts_two) == 4
        assert parts_one[0] + parts_one[1] + parts_one[2] == parts_two[0] + parts_two[1] + parts_two[2]
        pre_ip = parts_one[0] + '.' + parts_one[1] + '.' + parts_one[2] + '.'
        start = parts_one[3]
        end = parts_two[3]
        assert int(start) <= int(end)
        for i in range(int(start), int(end) + 1):
            ip = pre_ip + str(i)
            ip_list.append(ip)
    else:
        ip_list.append(ip_range)
    return ip_list


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', type=int, default=1, help='The concurrent number.')
    parser.add_argument('-f', type=str, help='The type, it only supports tcp/ping.')
    parser.add_argument('-ip', type=str,
                        help='The ip address for tcp and ping check. It can support ip range for ping, '
                             'example: -ip 192.168.0.1-192.168.0.100, -ip 192.168.0.1', )
    parser.add_argument('-w', type=str, help='The result file name. example: -w result.json')
    args = parser.parse_args()
    concur_num = args.n
    ip_range = args.ip
    if args.f == 'tcp':
        if '-' in ip_range:
            print("For tcp, it do not support -, please check")
            sys.exit(1)
    ip_list = process_ip(ip_range)
    result_file = args.w

    result = []
    time1 = time.time()
    if args.f == 'tcp':
        lock = threading.Lock()
        with ThreadPoolExecutor(max_workers=concur_num) as t:
            obj_list = []
            for port in range(1, 1025):
                obj = t.submit(check_port, ip_list[0], port, lock, result)
                obj_list.append(obj)

            for future in as_completed(obj_list):
                pass

        result = {'tcp port opened': result}
        print(result)
        print("tcp finished")
    elif args.f == 'ping':
        lock = threading.Lock()
        with ThreadPoolExecutor(max_workers=concur_num) as t:
            obj_list = []
            for ip in ip_list:
                obj = t.submit(ping, ip, lock, result)
                obj_list.append(obj)
            for future in as_completed(obj_list):
                pass

        result = {'ping passed': result}
        print(result)
        print("ping finished")
    else:
        print("Please check type, it only supports: ping/tcp")
        sys.exit(1)

    time2 = time.time()
    print("The execution time is: %s" %(time2-time1))

    if result_file:
        with open(result_file, 'w') as f:
            data = json.dumps(result)
            json.dump(data, f)
