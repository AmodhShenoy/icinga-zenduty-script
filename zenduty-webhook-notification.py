#!/usr/bin/python
import sys, os
import argparse
import urllib2
import json


def build_arguments_parser(description):
    parser = argparse.ArgumentParser(description)

    parser.add_argument('-n', '--token', 
                        dest="token",
                        required=True,
                        help="Zenduty unique token assigned to this service")
    parser.add_argument('-e', '--notification-type',
                        dest="notification_type",
                        required=True,
                        help="icinga2 notification source (host/service)",
                        choices=["service", "host"])
    parser.add_argument('-t', "--escalation-level",
                        dest="escalation_level",
                        required=True,
                        help='icinga2 notification-type ("PROBLEM", "RECOVERY", "FLAPPINGSTART", etc ...)')
    parser.add_argument('-f', '--additional-fields',
                        action="append",
                        dest="field",
                        help="additional fields/details to send")
    return parser 


def get_fields(field_array):
    if field_array is None:
        return {}
    to_ret=dict(f.split("=", 1) for f in field_array)
    return to_ret
    


def main():try:
        description = "collect arguments for zenduty"
        parser = build_arguments_parser(description)
        args = parser.parse_args()
        data_to_send = {
            "token": args.token,
            "notification_type": args.notification_type,
            "escalation_level": args.escalation_level,
            "fields": get_fields(args.field)
        }
        url = "https://www.zenduty.com/api/integration/icinga2/{}/".format(args.token)
        data = json.dumps(data_to_send)
        req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
        f = urllib2.urlopen(req)
        response = f.read()
        f.close()
        exit(0)
    except Exception as e:
        print(str(e))
        exit(4)


main()
