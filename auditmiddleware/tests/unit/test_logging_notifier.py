# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import fixtures
import mock

from auditmiddleware.tests.unit import base


class TestLoggingNotifier(base.BaseAuditMiddlewareTest):

    def setUp(self):
        p = 'auditmiddleware._notifier.oslo_messaging'
        f = fixtures.MockPatch(p, None)
        self.messaging_fixture = self.useFixture(f)

        super(TestLoggingNotifier, self).setUp()

    def test_api_request_no_messaging(self):
        app = self.create_simple_app()

        with mock.patch('auditmiddleware._LOG.info') as log:
            path = '/v2/' + self.project_id + '/servers'
            app.get(path, extra_environ=self.get_environ_header())

            # Check notification'
            call_args = log.call_args_list[0][0]
            self.assertEqual('audit.cadf', call_args[1]['event_type'])
