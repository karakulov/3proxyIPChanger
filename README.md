# 3proxyIPChanger
Updates list of the allowed IPs

## Installation

After intallation and configuration 3proxy, you need to specify in app.py paths to /etc/3proxy/update, /etc/3proxy/iplist.txt, external IP and port and secret AUTH key.

## Example of reqest

```
curl -H "AUTH: 12345" http://192.168.0.1:1111/ping/desktop
```
Added IP of "desktop" to allowed list and restarts 3proxy
