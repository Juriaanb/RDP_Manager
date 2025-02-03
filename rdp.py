# rdp.py
from flask import Blueprint, make_response, request
import subprocess
from wakeonlan import send_magic_packet

rdp_blueprint = Blueprint("rdp", __name__)

@rdp_blueprint.route("/rdp")
def rdp_download():
    ip = request.args.get("ip", "")
    if not ip:
        return "IP ontbreekt", 400
    content = f"""full address:s:{ip}
prompt for credentials:i:1
screen mode id:i:2
"""
    resp = make_response(content.encode("utf-8"))
    resp.headers["Content-Type"] = "application/x-rdp"
    resp.headers["Content-Disposition"] = f'attachment; filename="{ip}.rdp"'
    return resp

@rdp_blueprint.route("/wol")
def wol():
    mac = request.args.get("mac", "")
    if not mac:
        return "MAC ontbreekt", 400
    try:
        send_magic_packet(mac)
        return f"WOL verstuurd naar {mac}"
    except Exception as e:
        return f"Fout: {e}", 500

@rdp_blueprint.route("/shutdown")
def shutdown_remote():
    ip = request.args.get("ip", "")
    if not ip:
        return "IP ontbreekt", 400
    cmd = f"shutdown -m \\\\{ip} -s -t 0"
    try:
        subprocess.check_output(cmd, shell=True)
        return f"Shutdown verstuurd naar {ip}"
    except Exception as e:
        return f"Fout bij shutdown: {e}", 500
