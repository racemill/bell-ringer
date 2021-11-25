initial commit

Web server is a python based server used for small/personal web sites
(* python script run as a service to always start at boot/reboot and restart on crash)
    Provide Ring Bell button
    Display Scheduled rings(Dropdown list)
    Display Random Bell trivia blurb
    *Display Live video/audio feed of Bell

Relay triggered by GPIO pin used to apply power to solenoid that pulls the bell clapper

Hardware button on box uses GPIO pins as input to trigger a single ring

Scheduled rings use system crontab entries to kick off py scripts
    cat /etc/crontab  # To see current list

Log files located in /var/log
    bell.log       # Main log for bell-ringer 
    bell_cron.log  # Log for scheduled rings run by cron

*Time Guard - Controls to when the bell can be rung (to prevent the three oclock in the morning ring)
    flag - ability to turn on/off time guard
    earliestTimeToRing var
    latestTimeToRing var
  
