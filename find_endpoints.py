import subprocess
from datetime import datetime, timedelta
from time import sleep
import socket
import requests
import scapy.all as scapy

MONITOR_INTERVAL = 15
DISCOVERY_INTERVAL = 300


def fetch_endpoints_from_server():
    print("\n\n----> Retrieving Endpoints ...", end="")
    response = requests.get("http://127.0.0.1:5000/endpoints")
    if response.status_code != 200:
        print(f" !!!  Failed to retrieve endpoints from server: {response.reason}")
        return {}

    print(" Endpoints successfully received!")
    return response.json()


def discover_new_endpoints():
    # DISCOVER HOSTS ON NETWORK USING ARPING FUNCTION
    print(
        "\n\n----- Discovery New Endpoints ---------------------"
    )
    ans, unans = scapy.arping("192.168.1.0/24")
    ans.summary()

    for res in ans.res:
        print(f"oooo> IP address discovered: {res[0].payload.pdst}")

        ip_addr = res[1].payload.psrc
        mac_addr = res[1].payload.hwsrc
        try:
            hostname = socket.gethostbyaddr(str(ip_addr))
        except (socket.error, socket.gaierror):
            hostname = (str(ip_addr), [], [str(ip_addr)])
        last_heard = str(datetime.now())[:-3]

        discovered_endpoint = {
            "IP_Address": ip_addr,
            "MAC_Address": mac_addr,
            "Endpoint_Name": hostname[0],
            "Endpoint_Last_Seen": last_heard,
            "Endpoint_Presence": True
        }
        update_endpoint_in_server(discovered_endpoint)


def update_endpoint_in_server(host):
    print(f"----> Updating Endpoint status via REST API: {host['Endpoint_Name']}", end="")
    rsp = requests.put("http://127.0.0.1:5000/endpoints", params={"Endpoint_Name": host["Endpoint_Name"]}, json=host)
    if rsp.status_code != 204:
        print(
            f"{str(datetime.now())[:-3]}: Error posting to /hosts, response: {rsp.status_code}, {rsp.content}"
        )
        print(f" !!!  Unsuccessful attempt to update host status via REST API: {host['Endpoint_Name']}")
    else:
        print(f" Successfully updated host status via REST API: {host['Endpoint_Name']}")


def ping_fetched_endpoint(ping_end):
    try:
        print(f"----> Pinging host: {ping_end['Endpoint_Name']}", end="")
        subprocess.check_output(
            ["ping", "-c3", "-n", "-i0.5", "-W2", ping_end["IP_Address"]]
        )
        ping_end["Endpoint_Presence"] = True
        ping_end["Endpoint_Last_Seen"] = str(datetime.now())[:-3]
        print(f" Host ping successful: {ping_end['Endpoint_Name']}")

    except subprocess.CalledProcessError:
        ping_end["Endpoint_Presence"] = False
        print(f" !!!  Host ping failed: {ping_end['Endpoint_Name']}")


def main():
    last_discovery = datetime.now() - timedelta(days=1)

    while True:

        if (datetime.now() - last_discovery).total_seconds() > DISCOVERY_INTERVAL:
            discover_new_endpoints()
            last_discovery = datetime.now()
            server_fetched_endpoints = fetch_endpoints_from_server()

        for end_p in server_fetched_endpoints.values():
            ping_fetched_endpoint(end_p)
            update_endpoint_in_server(end_p)

        sleep(MONITOR_INTERVAL)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting Endpoint Monitoring!")
        exit()