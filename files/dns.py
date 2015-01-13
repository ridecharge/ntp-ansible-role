#!/usr/bin/env python
import boto.utils
import boto.route53
import sys

ip = boto.utils.get_instance_metadata()['local-ipv4']
region = boto.utils.get_instance_identity()['document']['region']
conn = boto.route53.connect_to_region(region)

instance_type = sys.argv[1].lower()
domain_az = boto.utils.get_instance_metadata()['placement']['availability-zone'].split('-')[-1]

hosted_zone = sys.argv[0]
domain = instance_type+"-"+domain_az+".ec2.gc"

changes = boto.route53.record.ResourceRecordSets(conn, hosted_zone)
change = changes.add_change("UPSERT", domain, "A")
change.add_value(ip)
changes.commit()
