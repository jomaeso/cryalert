import json
import logging
import requests
import os
import sys
from utils.mail import send_email
from utils.logger import logging_setup


with open(os.path.join(os.path.dirname(__file__), 'config/config.json')) as data_file:
    data = json.load(data_file)

def main(argv):

    log_path = os.path.dirname(
               os.path.abspath(__file__)) + data.get("logger",{}).get("path", "")

    logger = logging_setup(__name__, log_path)

    r = requests.get(data.get("api",""))
    raw_result = r.text
    result = json.loads(raw_result)

    current_price = 0.00

    for cex_data in result.get("data", []):
        for track in data.get("track", []):
            if cex_data.get("symbol1","") == track.get("symbol1", "") and cex_data.get("symbol2","") == track.get("symbol2",""):
                current_price = float(cex_data.get("lprice"))

                logger.info("{} current price: {} {}".format(cex_data.get("symbol1",""), current_price, cex_data.get("symbol2","")))

                if current_price <= track.get("limits",{}).get("min", 0):
                    send_email(data.get("alerts",{}).get("user",""), data.get("alerts",{}).get("password",""), data.get("alerts",{}).get("to",[]), "ALERTA DINEROS", "{0} por debajo del limite ({3} {2})\n\nPrecio actual: {1} {2}".format(track.get("symbol1", ""), current_price, cex_data.get("symbol2",""), track.get("limits",{}).get("min", 0)))

if __name__ == "__main__":
   main(sys.argv[1:])
