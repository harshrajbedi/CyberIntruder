from avoid_circular_import import cyber_database
from database_tables import Endpoints

def get_as_dict(model_obj):

    return {k: v for (k, v) in model_obj.__dict__.items() if not k.startswith("_")}


def fetch_endpoints():

    host_objs = cyber_database.session.query(Endpoints).all()
    hosts = {host_obj.Endpoint_Name: get_as_dict(host_obj) for host_obj in host_objs}
    return hosts


def update_endpoints(host):

    add_endp = cyber_database.session.query(Endpoints).filter_by(Endpoint_Name=host["Endpoint_Name"]).one_or_none()
    if not add_endp:
        add_endp = Endpoints(**host)
        cyber_database.session.add(add_endp)
    else:
        if "IP_Address" in host:
            add_endp.IP_Address = host["IP_Address"]
        if "MAC_Address" in host:
            add_endp.MAC_Address = host["MAC_Address"]
        if "Endpoint_Presence" in host:
            add_endp.Endpoint_Presence = host["Endpoint_Presence"]
        if "Endpoint_Response" in host:
            add_endp.Endpoint_Response = host["Endpoint_Response"]
        if "Endpoint_Last_Seen" in host:
            add_endp.Endpoint_Last_Seen = host["Endpoint_Last_Seen"]

    cyber_database.session.commit()