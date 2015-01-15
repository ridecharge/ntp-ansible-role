#!/usr/bin/env python3
import boto.utils
import boto.route53
import logging
import logging.config
import loggly.handlers
import sys

class DnsRegistration(object):
	def __init__(self, record_sets, record, ip, logger):
		self.record_sets = record_sets
		self.record = record
		self.ip = ip
		self.logger = logger


	def register(self):
		""" Upserts the A record """
		change = self.record_sets.add_change("UPSERT", self.record, "A")
		change.add_value(self.ip)
		self.record_sets.commit()
		self.logger.info("Successful set {0.ip} to {0.record}.", self)

def build_record(name, domain, az):
	""" Rebuilds the DNS record with postfix of the zone.  
    ntp.example.com at us-east-1a becomes ntp-1a.example.com
    for paramters
    name=ntp 
    domain=example.com  
    az=us-east-1a 
	"""  
	zone = az.split('-')[-1]
	return "{}-{}.{}".format(name, zone, domain)

LOGGLY_URL='https://logs-01.loggly.com/inputs/e8bcd155-264b-4ec0-88be-fcb023f76a89/tag/python,boot,dns,cloudformation'

def build_logger(name, instance_id):
	""" Sets up a logger to send files to Loggly with dynamic tags """
	logger = logging.getLogger(name)
	handler = loggly.handlers.HTTPSHandler(LOGGLY_URL+","+instance_id)
	logger.addHandler(handler)
	logger.setLevel(logging.INFO)
	return logger

def build_record_sets(conn, hosted_zone):
	""" Returns a Route53 RecordSets for the hosted_zone and connection """
	return boto.route53.record.ResourceRecordSets(conn, hosted_zone)

def split_domain(domain):
	levels = domain.split('.', 1)
	name = levels[0]
	return (name, levels[1])

def main(hosted_zone, domain):
	name, levels = split_domain(domain)
	instance_metadata = boto.utils.get_instance_metadata()

	try:
		region = boto.utils.get_instance_identity()['document']['region']
		az = instance_metadata['placement']['availability-zone']
		ip = instance_metadata['local-ipv4']
		conn = boto.route53.connect_to_region(region)


		record = build_record(name, levels, az)
		logger = build_logger(name, instance_metadata['instance-id'])

		DnsRegistration(build_record_sets(conn, hosted_zone), 
						record, 
						ip,
						logger
						).register()
	except:
		logger.exception("Error Registering DNS")

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
