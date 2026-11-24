import os
import sys
import time
import subprocess


# ============================================================
# PATHS
# ============================================================

BACKEND_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

FEDERATED_DIR = os.path.join(
    BACKEND_DIR,
    "federated"
)

PYTHON = sys.executable


# ============================================================
# FEDERATED SETTINGS
# ============================================================

SERVER_SCRIPT = os.path.join(
    FEDERATED_DIR,
    "diabetes_server.py"
)

CLIENT_SCRIPT = os.path.join(
    FEDERATED_DIR,
    "diabetes_client.py"
)

HOSPITALS = [
    "hospital_a",
    "hospital_b",
    "hospital_c",
    "hospital_d"
]


# ============================================================
# START SERVER
# ============================================================

def start_server():

    print()
    print("==============================================")
    print(" STARTING DIABETES FEDERATED SERVER")
    print("==============================================")
    print()

    process = subprocess.Popen(
        [
            PYTHON,
            SERVER_SCRIPT
        ],
        cwd=BACKEND_DIR
    )

    return process


# ============================================================
# START HOSPITAL CLIENT
# ============================================================

def start_client(hospital):

    print(
        f"Starting {hospital.upper()}..."
    )

    process = subprocess.Popen(
        [
            PYTHON,
            CLIENT_SCRIPT,
            hospital
        ],
        cwd=BACKEND_DIR
    )

    return process


# ============================================================
# MAIN
# ============================================================

def main():

    server_process = None
    client_processes = []

    try:

        # ----------------------------------------------------
        # Start Flower server
        # ----------------------------------------------------

        server_process = start_server()

        print()
        print("Waiting for federated server...")
        time.sleep(5)

        # ----------------------------------------------------
        # Start four hospitals
        # ----------------------------------------------------

        print()
        print("==============================================")
        print(" STARTING FOUR HOSPITAL CLIENTS")
        print("==============================================")
        print()

        for hospital in HOSPITALS:

            process = start_client(
                hospital
            )

            client_processes.append(
                process
            )

            time.sleep(1)

        print()
        print("==============================================")
        print(" ALL HOSPITALS STARTED")
        print("==============================================")
        print()

        # ----------------------------------------------------
        # Wait for server to finish all rounds
        # ----------------------------------------------------

        return_code = server_process.wait()

        print()
        print("==============================================")

        if return_code == 0:
            print(
                " DIABETES FEDERATED TRAINING COMPLETED"
            )
        else:
            print(
                " DIABETES FEDERATED TRAINING FAILED"
            )

        print("==============================================")
        print()

        # Give clients a moment to finish
        time.sleep(3)

    except KeyboardInterrupt:

        print()
        print("Training interrupted by user.")

    finally:

        # ----------------------------------------------------
        # Stop hospital clients
        # ----------------------------------------------------

        for process in client_processes:

            if process.poll() is None:

                process.terminate()

        # ----------------------------------------------------
        # Stop server if still running
        # ----------------------------------------------------

        if (
            server_process is not None
            and server_process.poll() is None
        ):

            server_process.terminate()

        print()
        print("Federated processes stopped.")


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()