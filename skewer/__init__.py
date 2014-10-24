# Copyright (c) 2014 Scopely, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
# http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

import time
import logging
import os

import elasticsearch
import skew


LOG = logging.getLogger(__name__)


class Skewer(object):

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.ts = int(time.time())
        self.es = elasticsearch.Elasticsearch(
            hosts=[{'host': host, 'port': port}])

    def _index_name(self):
        return 'skewer-%d' % self.ts

    def create_template(self):
        template_path = os.path.join(
            os.path.dirname(__file__),
            'skewer-es-template.json'
        )
        with open(template_path, 'r') as fh:
            template_body = fh.read()
        self.es.indices.put_template(
            name="skewer",
            body=template_body
        )

    def clear_index(self):
        LOG.debug('Deleting existing indices')
        self.es.indices.delete('skewer-*')
        self.create_template()

    def index_aws(self, arn_pattern='arn:aws:*:*:*:*/*'):
        all_services = set()
        all_regions = set()
        all_accounts = set()

        new_index_name = self._index_name()

        LOG.debug('using ARN: %s', arn_pattern)

        i = 0
        arn = skew.scan(arn_pattern)

        for resource in arn:
            _, _, service, region, acct_id, _ = str(resource).split(':', 5)
            resource.data['service'] = service
            resource.data['region'] = region
            resource.data['account_id'] = acct_id
            resource.data['arn'] = resource.arn
            all_services.add(service)
            all_regions.add(region)
            all_accounts.add(acct_id)
            self.es.index(new_index_name, doc_type=resource.resourcetype,
                          id=str(resource), body=resource.data)
            i += 1
            LOG.debug('indexed %s', resource.arn)

        # Delete old indexes if they exist and create new aliases
        if self.es.indices.exists(['skewer']):
            self.es.indices.delete(['skewer'])
        if self.es.indices.exists([new_index_name]):
            self.es.indices.put_alias(index=[new_index_name],
                                      name='skewer')

        # Write updated metadata to ES
        metadata = {
            'services': list(all_services),
            'regions': list(all_regions),
            'accounts': list(all_accounts)}
        self.es.index('skewer-meta', doc_type='skewermeta',
                      id='skewermeta', body=metadata)
