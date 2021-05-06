from diagrams import Cluster, Diagram, Edge
from diagrams.onprem.compute import Server
from diagrams.onprem.network import Nginx, Gunicorn
from diagrams.programming.framework import React, Django
from diagrams.programming.language import Python
from diagrams.generic.database import SQL
from diagrams.generic.storage import Storage

with Diagram("Adpkd Service with On-Premise", show=True):
    with Cluster("Front-End"):
        frontend = React("React")

    with Cluster("Web Server"):
        ingress = Nginx("Nginx")
    with Cluster("WSGI server"):
        wsgi = Gunicorn("Gunicorn")

    with Cluster("Service Cluster"):
        with Cluster("Application"):
            grpcsvc = Server("adpkd_service")
            # grpcsvc - Edge(color="brown", style="dashed") - Django("Django")

        with Cluster("Database"):
            master1 = SQL("sqlite3")
            grpcsvc >> master1

        with Cluster("Storage Server"):
            master2 = Storage("minio")
            grpcsvc >> master2

        with Cluster("Inferencer"):
            master3 = Server("adpkd_model_serving")
            # master3 - Edge(color="brown", style="dashed") - Python("Python")
            grpcsvc >> master3

    frontend >> ingress >> wsgi >> grpcsvc