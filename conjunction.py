#!/usr/bin/env python3
"""Compute the local coordinates of Jupiter and Saturn for a given date. Graham L. Giller, 2020."""

# modules
from sys import stderr,version_info
from datetime import datetime,timedelta
from pytz import timezone
from ephem import Sun,Moon,Jupiter,Saturn,Observer
from math import pi,cos

def main():
    # arguments
    from argparse import ArgumentParser;
    args = ArgumentParser(epilog="""This script will compute the local coordinates (altitude and azimuth) for Jupiter
and Saturn for the given date. Altitude is degrees above the horizon and azimuth is degrees eastwards from North. Locate North
by finding the Polaris, the pole star.""");
    args.add_argument("-x","--longitude", type=float,default=-74.151494,help="East longitude of the observer in decimal degrees. West is negative.")
    args.add_argument("-y","--latitude", type=float,default=40.373545,help="North latitude of the observer. South is negative.")
    args.add_argument("-t","--timezone",type=str,default='US/Eastern',help="The local time-zone of the observer.")
    args.add_argument("-e","--elevation",type=float,default=20e0,help="Elevation in metres above sea level.")
    args.add_argument("time",nargs='?',default=datetime.now().strftime("%H:%M:%S"),help="Local time for calculation, default is current time, as HH:MM:SS.")
    args.add_argument("date",nargs='?',default=datetime.now().strftime("%Y-%m-%d"),help="Local date for calculation, default is current date, as YYYY-MM-DD.")
    args = args.parse_args();
    
    # time
    localtime=timezone(args.timezone)
    utc=timezone('UTC')
    timestamp=localtime.localize(datetime.strptime(args.date+' '+args.time,'%Y-%m-%d %H:%M:%S'))
    observer=Observer()
    observer.lat=args.latitude*pi/180.0
    observer.lon=args.longitude*pi/180.0
    observer.date=timestamp.astimezone(utc)
    observer.elevation=args.elevation
    
    print("Calculation of the location of Jupiter and Saturn for an observer at %.4f° %s, %.4f° %s, %.4f m above sea level.\n" % (
        abs(args.longitude),"E" if args.longitude>0 else "W",
        abs(args.latitude),"N" if args.latitude>0 else "S",
        args.elevation
    ))

    print("Computed for local time %s." % timestamp.astimezone(localtime).strftime('%Y-%m-%d %H:%M:%S'))

    # Sun
    sun=Sun(observer)
    #sun.compute(observer)
    sunlight=max(0e0,cos(pi/2-sun.alt))*1e2

    if sunlight>0:
        print("The Sun is currently above the horizon, with light at %.2f %%, at %.2f° %s." % (
            sunlight,
            (sun.az-pi if sun.az>pi else sun.az)*180e0/pi,
            "E" if sun.az<pi else "W" if sun.az>pi else "S"
        ))
    
    sunset=utc.localize(datetime.strptime(str(observer.next_setting(sun)),"%Y/%m/%d %H:%M:%S")).astimezone(localtime) if observer.next_setting(sun)!=None else None

    if sunset!=None:
        print("The Sun will set at %s." % sunset.strftime("%H:%M:%S"))
        
    if sunlight<=0e0:
        sunrise=utc.localize(datetime.strptime(str(observer.next_rising(sun)),"%Y/%m/%d %H:%M:%S")).astimezone(localtime) if observer.next_rising(sun)!=None else None
        print("The Sun will rise at %s." % sunrise.strftime("%H:%M:%S"))

    # Moon
    moon=Moon(observer)
    moonlight=max(0e0,cos(pi/2-moon.alt))*1e2
    
    if moonlight>0:
        print("The Moon is currently above the horizon, with light at %.2f %%." % moonlight)

    # Jupiter
    jupiter=Jupiter(observer)
    
    if jupiter.alt>0e0:
        print("Jupiter is %.2f° above the horizon, %.2f° %s." % (
            jupiter.alt*180e0/pi,
            (jupiter.az-pi if jupiter.az>pi else jupiter.az)*180e0/pi,
            "W" if jupiter.az>pi else "E" if jupiter.az<pi else "S"
        ))

    # Jupiter
    saturn=Saturn(observer)
    
    if saturn.alt>0e0:
        print("Saturn is %.2f° above the horizon, %.2f° %s." % (
            saturn.alt*180e0/pi,
            (saturn.az-pi if saturn.az>pi else saturn.az)*180e0/pi,
            "W" if saturn.az>pi else "E" if saturn.az<pi else "S"
        ))

    # done
    print("Done.")

# bootstrap
if __name__ == "__main__":
    assert(version_info.major >= 3)
    main()
