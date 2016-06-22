from subprocess import Popen, PIPE

import boto.ec2.elb
import boto.route53
from boto.route53.record import ResourceRecordSets

elb = boto.ec2.elb.connect_to_region('us-west-2')
r53 = boto.route53.connect_to_region('us-west-2')

result = Popen(["./get_ingress.sh"], stdout=PIPE)
Ingress = result.stdout.read().strip()

#Ingress = 'a02a3d84a37ff11e6a23106d19ba1fed-1570681198.us-west-2.elb.amazonaws.com'
lb = elb.get_all_load_balancers(load_balancer_names=[Ingress.split('-')[0]])[0]

HOSTED_ZONE = 'Z1Y5CE8LHZN61K'
DOMAIN_NAME = 'countly.cncfdemo.io'

rrs = ResourceRecordSets(r53,HOSTED_ZONE) 
add_change_args_upsert = {
    'action': 'UPSERT',
    'name': DOMAIN_NAME,
    'type': 'A',
    'alias_hosted_zone_id': lb.canonical_hosted_zone_name_id,
    'alias_dns_name': lb.canonical_hosted_zone_name,
    'alias_evaluate_target_health': False
}

change = rrs.add_change(**add_change_args_upsert)
rrs.commit()
