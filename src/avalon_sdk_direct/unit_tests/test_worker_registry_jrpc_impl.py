# Copyright 2020 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import unittest
from os import path, environ
import errno
import secrets
import json
import logging


from  enums.worker import WorkerType, WorkerStatus
from  enums.error_code import WorkerError, JRPCErrorCodes
from  avalon_sdk_direct.jrpc_worker_registry import JRPCWorkerRegistryImpl \
    as WorkerRegistryJRPCClient


logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)


class TestWorkerRegistryJRPCImpl(unittest.TestCase):
    def __init__(self, config):
        super(TestWorkerRegistryJRPCImpl, self).__init__()
        self.__config = config
        self.__worker_registry_wrapper = WorkerRegistryJRPCClient(
            self.__config)
        self.__worker_id = secrets.token_hex(32)
        self.__worker_type = WorkerType.TEE_SGX
        self.__org_id = secrets.token_hex(32)
        self.__lookup_tag=""
        self.__details = json.dumps(
            {"workOrderSyncUri":
             "http://worker-order:8008".encode("utf-8").hex()})
        self.__app_ids = secrets.token_hex(32)

    def test_worker_register(self):
        req_id = 12
        logging.info(
            'Calling test_worker_register with\n worker_id %s\n' +
            ' worker_type %d\n details %s\n org_id %s\n app_ids %s\n',
            self.__worker_id, self.__worker_type.value, self.__details,
            self.__org_id, self.__app_ids)
        res = self.__worker_registry_wrapper.worker_register(
            self.__worker_id, self.__worker_type,
            self.__org_id, self.__app_ids, self.__details, req_id)
        logging.info('Result: %s\n', res)


    def test_worker_update(self):
        req_id = 13
        self.__details = json.dumps(
            {
                "workOrderSyncUri":
                "http://worker-order:8008".encode("utf-8").hex(),
                "workOrderNotifyUri":
                "http://worker-notify:8008".encode("utf-8").hex()
            })
        logging.info(
            'Calling test_worker_update with\n worker_id %s\n details %s\n',
            self.__worker_id, self.__details)
        res = self.__worker_registry_wrapper.worker_update(
            self.__worker_id, self.__details, req_id)
        logging.info('Result: %s\n', res)
 

    def test_worker_set_status(self):
        req_id = 14
        self.__status = WorkerStatus.OFF_LINE
        logging.info(
            'Calling test_worker_set_status with\n worker_id %s\n status %d\n',
            self.__worker_id, self.__status.value)
        res = self.__worker_registry_wrapper.worker_set_status(
            self.__worker_id, self.__status, req_id)
        logging.info('Result: %s\n', res)


    def test_worker_retrieve(self):
        req_id = 15
        logging.info(
            'Calling test_worker_retrieve with\n worker_id %s\n',
            self.__worker_id)
        res = self.__worker_registry_wrapper.worker_retrieve(
            self.__worker_id, req_id)
        logging.info('Result: %s\n', res)
        self.assertEqual(
            res['id'], req_id, "worker_retrieve Response id doesn't match")
        self.assertEqual(
            res['result']['workerType'], self.__worker_type.value,
            "worker_retrieve Response result workerType doesn't match")
        self.__org_id = res['result']['organizationId']
        self.__app_ids =  res['result']['applicationTypeId']
        self.__details = res['result']['details']
        self.__status = res['result']['status']


    def test_worker_lookup(self):
        req_id = 16
        logging.info(
            'Calling testworker_lookup with\n worker type %d\n org_id %s\n ' +
            'application ids %s\n',
            self.__worker_type.value, self.__org_id, self.__app_ids)
        res = self.__worker_registry_wrapper.worker_lookup(
            worker_type=self.__worker_type, id=req_id)
        logging.info('Result: %s\n ', res)
        self.assertEqual(
            res['result']['totalCount'], 1,
            "worker_lookup_next Response totalCount doesn't match")

        self.__worker_id = res['result']['ids'][0]
        self.__lookup_tag = res['result']['lookupTag']

    def test_worker_lookup_next(self):
        req_id = 17
        logging.info(
            'Calling worker_lookup_next with\n worker type %d\n' +
            ' org_id %s\n app_ids %s\n lookUpTag %s\n',
            self.__worker_type.value, self.__org_id, self.__app_ids,
            self.__lookup_tag)
        res = self.__worker_registry_wrapper.worker_lookup_next(
            self.__lookup_tag, self.__worker_type, self.__org_id, self.__app_ids,
            req_id)
        logging.info('Result: %s\n', res)



def main():
    logging.info("Running test cases...\n")
    #Docker Mode: http://avalon-listener:1947" 
    #Listerner Mode : http://localhost:1947
    worker = {
              "json_rpc_uri" : "http://localhost:1947",
    }

    test = TestWorkerRegistryJRPCImpl(worker)
    test.test_worker_register()
    logging.info("********************************************************************************")
    test.test_worker_lookup()
    logging.info("********************************************************************************")
    test.test_worker_retrieve()
    logging.info("********************************************************************************")
    test.test_worker_update()
    logging.info("********************************************************************************")
    test.test_worker_set_status()
    logging.info("********************************************************************************")
    test.test_worker_retrieve()
    logging.info("********************************************************************************")
    test.test_worker_lookup_next()
    logging.info("********************************************************************************")


if __name__ == '__main__':
    main()
