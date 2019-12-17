# moxa-iologic-1200-monitor
Simple Monitor via REST API for Moxa 12xx DIOs

### Use Case

The Moxa IOLogic devices provide a flexible way of getting DI status inputs.  My particular use case was I needed to get them via Restful API, and avoid using
heavy monitoring solutions like Nagios, Graphite, Grafana et al.

Basically, if a status changes, drop an email with enough controls to be able to deal with flappy conditions.

### Configuration
Configuration is via a yaml file.  Each of the elements should be self explanitory except for perhaps alert_interval.  This is the time it must wait (in seconds) before sending another alert of either type.

start_state can be thought of as the 'normal' conditions of operation for that channel.

### TODO
Lots.  Like specify a path to the config yaml file on the command line, properly daemonize this, reload config via a kill.  
