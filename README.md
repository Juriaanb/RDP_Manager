# RDP Dashboard
```
 ____  ____  ____    ____            _     _                         _ 
|  _ \|  _ \|  _ \  |  _ \  __ _ ___| |__ | |__   ___   __ _ _ __ | |
| |_) | | | | |_) | | | | |/ _` / __| '_ \| '_ \ / _ \ / _` | '_ \| |
|  _ <| |_| |  __/  | |_| | (_| \__ \ | | | |_) | (_) | (_| | | | |_|
|_| \_\____/|_|     |____/ \__,_|___/_| |_|_.__/ \___/ \__,_|_| |_(_)
```

## Quick Start 🚀

```
 [1] Double click run.bat
     |
     +---> Python check
     |      |
     |      +---> Install dependencies
     |
     +---> Start application
           |
           +---> http://localhost:5000
```

That's it! Just run `run.bat` and the application will start automatically.

## Features 🛠️

```
┌──────────────────────────────────┐
│ ⚡ Remote Desktop Management     │
│ 📡 Real-time System Monitoring  │
│ 🔌 Wake-on-LAN Support         │
│ 📄 PDF Document Viewer         │
│ 🔄 Auto-config Reload          │
└──────────────────────────────────┘
```

## System Requirements 📋

```
┌─ Windows OS
├─ Python 3.x
└─ Network access to target systems
```

## Understanding the Dashboard 🎯

```
┌─ Dashboard ────────────────────┐
│                               │
│  Hypervisors                  │
│  ├─ System Status            │
│  ├─ IP Address              │
│  └─ Virtual Machines        │
│     ├─ Status              │
│     ├─ RDP Access         │
│     └─ Power Control      │
│                               │
└───────────────────────────────┘
```

## File Structure 📁
```
root/
 ├── run.bat       <- 👉 This is all you need to run!
 ├── app.py        
 ├── rdp.py       
 ├── pdf.py       
 └── requirements.txt
```

## Remember 💡

- Just run `run.bat` - it handles everything!
- Access the dashboard at http://localhost:5000
- First-time setup will install required dependencies automatically

## Notes 📌

- Default port is 5000
- Automatically monitors system status every 30 seconds
- Supports Wake-on-LAN for remote power on
- Remote shutdown capability for managed systems

## Having Issues? 🔧

1. Make sure Python is installed
2. Check network connectivity
3. Verify system IP addresses
4. Ensure target systems support RDP

For more detailed troubleshooting, check the console output when running `run.bat`.
