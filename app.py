# app.py
import os
import json
import time
import threading
import subprocess
import platform
from flask import Flask, render_template, request, jsonify, send_from_directory
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Import blueprints for RDP and PDF functionality
from rdp import rdp_blueprint
from pdf import pdf_blueprint

CONFIG_FILE = "rdp_config.json"
config_data = {}
PING_STATUSES = {}
last_modified = 0

app = Flask(__name__, static_folder='static')

class ConfigFileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(CONFIG_FILE):
            print("Config file changed, reloading...")
            load_config()

def load_config():
    global config_data, last_modified
    try:
        current_mtime = os.path.getmtime(CONFIG_FILE)
        if current_mtime != last_modified:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                config_data = json.load(f)
            last_modified = current_mtime
            print("Config reloaded successfully")
    except Exception as e:
        print(f"Error loading config: {e}")
        config_data = {"hypervisors": []}

def save_config():
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config_data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving config: {e}")
        return False

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/config")
def api_config():
    load_config()
    return jsonify(config_data)

@app.route("/api/status")
def api_status():
    return jsonify(PING_STATUSES)

@app.route("/api/ping")
def api_ping():
    ip = request.args.get("ip", "")
    if not ip:
        return jsonify({"error": "IP address required"}), 400
    online = is_online(ip)
    return jsonify({"status": "online" if online else "offline"})

# API endpoints for system management
@app.route("/api/add_system", methods=["POST"])
def add_system():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data received"}), 400

        if "id" not in data:
            data["id"] = f"{data['type']}_{int(time.time())}"

        if data.get("type") == "vm":
            for hv in config_data.get("hypervisors", []):
                if hv["id"] == data["parent_id"]:
                    hv.setdefault("vms", []).append({
                        "id": data["id"],
                        "name": data["name"],
                        "ip": data["ip"],
                        "mac": data.get("mac"),
                        "type": "vm"
                    })
                    break
        else:
            config_data.setdefault("hypervisors", []).append({
                "id": data["id"],
                "name": data["name"],
                "ip": data["ip"],
                "mac": data.get("mac"),
                "type": "hypervisor",
                "vms": []
            })

        if save_config():
            return jsonify({"success": True})
        else:
            return jsonify({"error": "Error saving configuration"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/delete_system/<system_id>", methods=["DELETE"])
def delete_system(system_id):
    try:
        # Remove hypervisor if it matches system_id
        config_data["hypervisors"] = [
            hv for hv in config_data.get("hypervisors", [])
            if hv["id"] != system_id
        ]
        # Remove VM if it matches system_id
        for hv in config_data.get("hypervisors", []):
            if "vms" in hv:
                hv["vms"] = [vm for vm in hv["vms"] if vm["id"] != system_id]
        
        if save_config():
            return jsonify({"success": True})
        else:
            return jsonify({"error": "Error saving configuration"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/edit_system/<system_id>", methods=["PUT"])
def edit_system(system_id):
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data received"}), 400

        # Try updating hypervisor
        for hv in config_data.get("hypervisors", []):
            if hv["id"] == system_id:
                hv.update({
                    "name": data["name"],
                    "ip": data["ip"],
                    "mac": data.get("mac")
                })
                if save_config():
                    return jsonify({"success": True})
                return jsonify({"error": "Error saving configuration"}), 500

        # Try updating VM if hypervisor update failed
        for hv in config_data.get("hypervisors", []):
            if "vms" in hv:
                for vm in hv["vms"]:
                    if vm["id"] == system_id:
                        vm.update({
                            "name": data["name"],
                            "ip": data["ip"],
                            "mac": data.get("mac")
                        })
                        if save_config():
                            return jsonify({"success": True})
                        return jsonify({"error": "Error saving configuration"}), 500

        return jsonify({"error": "System not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/static/<path:filename>")
def serve_static_file(filename):
    return send_from_directory("static", filename)

def is_online(ip: str) -> bool:
    """
    Check if a system is online by sending a ping request
    Returns True if system responds, False otherwise
    """
    param = "-n" if platform.system().lower() == "windows" else "-c"
    cmd = ["ping", param, "1", ip]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            return False
        output_lower = result.stdout.lower()
        if "unreachable" in output_lower or "timed out" in output_lower:
            return False
        if platform.system().lower() == "windows":
            return ("reply from" in output_lower) and (ip in output_lower)
        else:
            return "1 received" in output_lower
    except:
        return False

def update_all_pings():
    """Update ping status for all systems in configuration"""
    global PING_STATUSES
    for hv in config_data.get("hypervisors", []):
        PING_STATUSES[hv["id"]] = is_online(hv["ip"])
        for vm in hv.get("vms", []):
            PING_STATUSES[vm["id"]] = is_online(vm["ip"])

def ping_updater_thread():
    """Background thread to periodically update ping statuses"""
    while True:
        update_all_pings()
        time.sleep(30)

def setup_file_watcher():
    """Setup watchdog to monitor config file changes"""
    event_handler = ConfigFileHandler()
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=False)
    observer.start()
    return observer

# Register the RDP and PDF blueprints
app.register_blueprint(rdp_blueprint)
app.register_blueprint(pdf_blueprint)

if __name__ == "__main__":
    load_config()
    update_all_pings()
    ping_thread = threading.Thread(target=ping_updater_thread, daemon=True)
    ping_thread.start()
    observer = setup_file_watcher()
    try:
        app.run(host="0.0.0.0", port=5000, debug=True)
    finally:
        observer.stop()
        observer.join()
