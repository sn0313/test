import os
import subprocess
import logging
import oracledb
import configparser

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
ADW_WALLET_PATH = "/home/opc/wallet_adw"
CONFIG_FILE_PATH = '/home/opc/oracle-config/oracle_config.ini'

def test_adw():
    logging.info("Starting Oracle ADW Connection Test")

    try:
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE_PATH)

        user = config['oracle']['user']
        password = config['oracle']['password']
        dsn = config['oracle']['tns'].strip()

    except Exception as e:
        logging.error(f"Config load failed: {e}")
        return

    os.environ['TNS_ADMIN'] = ADW_WALLET_PATH
    oracledb.init_oracle_client(config_dir=ADW_WALLET_PATH)

    try:
        conn = oracledb.connect(
            user=user,
            password=password,
            dsn=dsn
        )

        logging.info("Successfully connected to ADW")

        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM dual")
        cursor.fetchone()

        logging.info("Query successful.")

        cursor.close()
        conn.close()

    except oracledb.DatabaseError as e:
        err = e.args[0]
        logging.error(f"DB ERROR: {err.message}")
        logging.error(f"Code: {err.code}")

        if "ORA-28759" in err.message:
            logging.critical("Wallet issue or TNS_ADMIN mismatch")

    except Exception as e:
        logging.exception(f"Unexpected error: {e}")
        
def test_connection(url):
    logging.info("Starting %s Test", url)
    
    try:
        result = subprocess.run(
            ["curl", "-I", url],
            text=True,
        )

        if result.returncode == 0:
            logging.info("Successfully connected to %s\n", url)
        else:
            logging.error("Failed to connect to %s\n", url)

    except Exception as e:
        logging.error("Error executing curl for %s: %s\n", url, e)

def test_googlescholar_proxy():
    logging.info("Starting Google Scholar via Proxy Test")
    
    try:
        result = subprocess.run(
            [
                "curl",
                "-x", 
                "http://140.238.32.108:3128",
                "-I",
                "https://scholar.google.com",
            ],
            text=True,
        )

        if result.returncode == 0:
            logging.info("Successfully connected to Google Scholar via Proxy http://140.238.32.108:3128\n")
        else:
            logging.error(
                "Failed to connect to Google Scholar via Proxy http://140.238.32.108:3128 (exit code %s)\n",
                result.returncode,
            )

    except Exception as e:
        logging.error("Error connecting to Google Scholar via Proxy: %s\n", e) 

if __name__ == "__main__":

    logging.info(f"Connection Test Script Running")
    test_adw()
    test_connection("https://uresearch-utp-edu.smartsimple.com.au")
    test_connection("https://api.elsevier.com")
    test_connection("https://gentari.hawkai.in")
    test_connection("https://www.utp.edu.my")
    test_connection("https://cloud.timeedit.net")
    test_connection("https://utpmy.sharepoint.com")
    test_connection("https://s3.ap-southeast-1.amazonaws.com")
    test_googlescholar_proxy()