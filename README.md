# sonos-rfid-controller

Controlling Sonos with RFID cards

1. Install dependencies

2. Register sonos-rfid-controller as a service and start it

```bash
sudo cp sonos-rfid-controller.service /lib/systemd/system
sudo chown root:root /lib/systemd/system/sonos-rfid-controller.service

sudo systemctl enable sonos-rfid-controller.service
sudo systemctl start sonos-rfid-controller.service
```

3. Watch log

```bash
sudo journalctl -f -u sonos-rfid-controller
```
