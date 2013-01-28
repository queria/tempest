# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2012 OpenStack, LLC
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from tempest.common.utils.data_utils import rand_name
from tempest import exceptions
from tempest.test import attr
from tempest.tests.identity import base

class Users2TestJSON(base.BaseIdentityAdminTest):
    _interface = 'json'

    alt_user = rand_name('test_user_')
    alt_password = rand_name('pass_')
    alt_email = alt_user + '@testmail.tm'
    alt_tenant = rand_name('test_tenant_')
    alt_description = rand_name('desc_')

    ##@attr(type='positive')
    ##def _test_update_user(self):
    ##    # Should change user's name
    ##    from pprint import pprint as pp
    ##    self.data.setup_test_user()
    ##    print("----USER----")
    ##    pp(self.data.user)
    ##    print("------------")
    ##    new_name = 'changed_' + self.data.test_user
    ##    new_email = 'changed-' + self.data.user['email']
    ##    new_enabled = 1
    ##    #'true'

    ##    resp, body = self.client.update_user(
    ##        self.data.user['id']
    ##        , name=new_name
    ##        , email=new_email
    ##        , enabled=new_enabled
    ##    )
    ##    print("----BODY----")
    ##    pp(body)
    ##    print("------------")
    ##    #self.assertEqual(new_name, body['name'])
    ##    #self.assertEqual(new_email, body['email'])
    ##    #self.assertEqual(new_enabled, body['enabled'])
    ##    #self.client.update_user(
    ##    #    '46da19aae1f34527ae2ee6a334704256',
    ##    #    attila=None #'hello'
    ##    #    #enabled='true',
    ##    #    #username='',
    ##    #    #email='alt_demo@example.com',
    ##    #    #name='alt_demo'
    ##    #    #email='renamed_alt_demo3@example.com'
    ##    #)


    @attr(type='negative')
    def test_update_user_id(self):
        # Should NOT change user's ID
        self.data.setup_test_user()
        new_value = self.data.user['id']
        if new_value[0] == 'a':
            new_value = 'b' + new_value[1:]
        else:
            new_value = 'a' + new_value[1:]

        self.assertRaises(exceptions.BadRequest,
                          self.client.update_user,
                          self.data.user['id'],
                          id=new_value)

    @attr(type='positive')
    def test_update_user_name(self):
        # Should change user's name
        self.data.setup_test_user()
        new_value = 'changed_' + self.data.test_user
        resp, body = self.client.update_user(
            self.data.user['id'],
            name=new_value)
        self.assertEqual(new_value, body['name'])

    @attr(type='positive')
    def test_update_user_email(self):
        # Should change user's email
        self.data.setup_test_user()
        new_value = 'changed_' + self.data.user['email']
        resp, body = self.client.update_user(
            self.data.user['id'],
            email=new_value)
        self.assertEqual(new_value, body['extra']['email'])

    @attr(type='positive')
    def test_update_user_availability(self):
        # Should toggle status of user
        self.data.setup_test_user()

        _, body = self.client.update_user(self.data.user['id'], enable='true')
        self.assertEqual('true', body['extra']['enable'].lower())
        _, body = self.client.update_user(self.data.user['id'], enable='false')
        self.assertEqual('false', body['extra']['enable'].lower())

    @attr(type='negative')
    def test_update_user_by_unauthorized_user(self):
        self.data.setup_test_user()
        new_value = 'changed_' + self.data.test_user
        self.assertRaises(exceptions.Unauthorized,
                          self.non_admin_client.update_user,
                          self.data.user['id'],
                          name=new_value)


class Users2TestXML(Users2TestJSON):
    _interface = 'xml'
