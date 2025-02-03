# RDP Dashboard

A Flask-based web application for managing remote desktop connections, VM monitoring, and PDF document management.

## Features

- Remote Desktop Protocol (RDP) connection management
- Wake-on-LAN (WoL) functionality for remote system power-on
- Remote shutdown capabilities
- Real-time system monitoring with ping status updates
- PDF document management and viewing
- Dynamic configuration management with auto-reload
- Support for hypervisors and virtual machines

## Prerequisites

- Python 3.x
- Windows environment (for RDP functionality)
- Network access to target systems
- Required Python packages (see `requirements.txt`):
  - Flask 2.2.5
  - wakeonlan 2.0.0
  - watchdog 3.0.0

## Installation

1. Clone this repository or download the source code
2. Install the required Python packages:
```bash
pip install -r requirements.txt
```

## Configuration

The application uses a JSON configuration file (`rdp_config.json`) to store system information. The configuration is automatically loaded and monitored for changes.

Example configuration structure:
```json
{
  "hypervisors": [
    {
      "id": "hv_1",
      "name": "Hypervisor 1",
      "ip": "192.168.1.100",
      "mac": "00:11:22:33:44:55",
      "type": "hypervisor",
      "vms": [
        {
          "id": "vm_1",
          "name": "Virtual Machine 1",
          "ip": "192.168.1.101",
          "mac": "00:11:22:33:44:66",
          "type": "vm"
        }
      ]
    }
  ]
}
```

## Running the Application

### Windows
Execute the provided batch file:
```bash
run.bat
```

### Manual Start
```bash
python app.py
```

The application will start on `http://localhost:5000` by default.

## API Endpoints

### System Management
- `GET /api/config` - Get current configuration
- `GET /api/status` - Get system status overview
- `GET /api/ping?ip={ip}` - Check specific IP status
- `POST /api/add_system` - Add new system
- `PUT /api/edit_system/{system_id}` - Update system
- `DELETE /api/delete_system/{system_id}` - Remove system

### RDP Functions
- `GET /rdp?ip={ip}` - Download RDP connection file
- `GET /wol?mac={mac}` - Send Wake-on-LAN packet
- `GET /shutdown?ip={ip}` - Initiate remote shutdown

### PDF Management
- `GET /api/pdfs_list` - List available PDFs
- `GET /pdf_file/{filename}` - Serve PDF file

## Directory Structure
```
├── app.py              # Main application file
├── rdp.py             # RDP functionality module
├── pdf.py             # PDF management module
├── requirements.txt    # Python dependencies
├── run.bat            # Windows startup script
├── static/            # Static web files
├── templates/         # HTML templates
└── pdfs/             # PDF storage directory
```

## Security Considerations

- The application provides direct system control capabilities
- Implement appropriate network security measures
- Consider adding authentication before deployment
- Verify network permissions for Wake-on-LAN and shutdown commands
- Ensure proper file permissions for PDF directory

## Error Handling

The application includes error handling for:
- Network connectivity issues
- Configuration file changes
- File system operations
- Remote command execution

## Contributing

Feel free to submit issues and enhancement requests.

## License

[Add your chosen license here]
