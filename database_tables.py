from avoid_circular_import import cyber_database

# ***ENDPOINT'S TABLE***
class Endpoints(cyber_database.Model):
    __tablename__ = "endpoints"
    id = cyber_database.Column(cyber_database.Integer, primary_key=True, autoincrement=True)
    Endpoint_Name = cyber_database.Column(cyber_database.Text, nullable=False)
    IP_Address = cyber_database.Column(cyber_database.Text, nullable=False)
    MAC_Address = cyber_database.Column(cyber_database.Text)
    Endpoint_Presence = cyber_database.Column(cyber_database.Boolean)
    Endpoint_Response = cyber_database.Column(cyber_database.Integer)
    Endpoint_Last_Seen = cyber_database.Column(cyber_database.Text)
    def __repr__(self):
        return f"Host: {self.Endpoint_Name}"