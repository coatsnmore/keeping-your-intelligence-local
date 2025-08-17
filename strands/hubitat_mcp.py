import os
import json
from mcp.server import FastMCP
from dotenv import load_dotenv
import requests

load_dotenv()
# Create an MCP server
mcp = FastMCP("Hubitat MCP Server")

HUBITAT_BASE_URL = os.getenv("HUB_HOST")

HUBITAT_TOKEN = os.getenv("HUB_ACCESS_TOKEN")

@mcp.tool(description="List the Hubitat Devices")
def list_devices():
    """Return a list of devices from Hubitat Maker API and log them nicely."""
    url = f"{HUBITAT_BASE_URL}/devices?access_token={HUBITAT_TOKEN}"
    r = requests.get(url)
    devices = r.json()

    print("\n=== Hubitat Devices ===")
    for d in devices:
        name = d.get("label") or d.get("name", "Unknown")
        device_id = d.get("id", "?")
        device_type = d.get("type", "?")
        print(f"- {name} (ID: {device_id}, Type: {device_type})")
    print("=======================\n")

    return json.dumps(devices)

@mcp.tool(description="Check Specific Device Details")
def device_details(device_id):
    """Return the details for a specific device"""
    url = f"{HUBITAT_BASE_URL}/devices/{device_id}?access_token={HUBITAT_TOKEN}"
    r = requests.get(url)
    device_details = r.json()

    print(f"Device '{device_id}': {device_details}")

    return json.dumps(device_details)

@mcp.tool(description="Check Event History for a Specific Device")
def device_history(device_id):
    """Return the event history for a specific device"""
    url = f"{HUBITAT_BASE_URL}/devices/{device_id}/events?access_token={HUBITAT_TOKEN}"
    r = requests.get(url)
    events = r.json()

    print(f"Device '{device_id}' Events: {events}")

    return json.dumps(events)

@mcp.tool(description="Get Capabilities for a Specific Device")
def device_capabilities(device_id):
    """Return a the capabilities for a specific device"""
    url = f"{HUBITAT_BASE_URL}/devices/{device_id}/capabilities?access_token={HUBITAT_TOKEN}"
    r = requests.get(url)
    capabilities = r.json()

    print(f"Device '{device_id}' Events: {capabilities}")

    return json.dumps(capabilities)

@mcp.tool(description="Check Commands for a Specific Device")
def device_commands(device_id):
    """Return a the commands for a specific device"""
    url = f"{HUBITAT_BASE_URL}/devices/{device_id}/commands?access_token={HUBITAT_TOKEN}"
    r = requests.get(url)
    commands = r.json()

    print(f"Device '{device_id}' Commands: {commands}")

    return json.dumps(commands)

@mcp.tool(description="Command the Hubitat Devices")
def control_device(device_id, command):
    """Send a command to a Hubitat device.
    Example: To turn on a light device ID 1

    /devices/1/on

    Example 2: To set the level that light to 50%

    /devices/1/setLevel/50

    Example 3: Sets a lock code for at position 3 with code 4321 and name "Guest":

    /devices/1321/setCode/3,4321,Guest
    """
    url = f"{HUBITAT_BASE_URL}/devices/{device_id}/{command}?access_token={HUBITAT_TOKEN}"
    print(f"URL '{url}'")
    r = requests.get(url)
    status = "ok" if r.status_code == 200 else "error"
    print(f"Command '{command}' sent to device ID {device_id} - Status: {status}")
    return json.dumps({"status": status}, indent=2)

# Run the server with SSE transport
mcp.run(transport="sse")