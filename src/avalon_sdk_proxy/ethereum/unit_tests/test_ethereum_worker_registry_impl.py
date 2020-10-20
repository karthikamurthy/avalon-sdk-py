# Copyright 2019 Intel Corporation
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

from os import urandom, path, environ
import errno
import secrets
import logging
import toml
import json
import unittest
from web3 import Web3
import pkg_resources

from avalon_sdk_ethereum.ethereum_worker_registry \
    import EthereumWorkerRegistryImpl
from  enums.worker import WorkerType, WorkerStatus
from  enums.error_code import WorkerError, JRPCErrorCodes

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)


class TestEthereumWorkerRegistryImpl(unittest.TestCase):
    def __init__(self, config):
        super(TestEthereumWorkerRegistryImpl, self).__init__()
        self.__config = config
        #try:
        self.__eth_conn = EthereumWorkerRegistryImpl(self.__config)
        #except Exception as e:
           # logging.info('Error: %s\n', e.message)

    def test_worker_register(self):
        self.__worker_id = urandom(32).hex()
        self.__worker_type = WorkerType.TEE_SGX
        self.__details = json.dumps(
            {"workOrderSyncUri": "http://worker-order:8008"})
        self.__org_id = urandom(32).hex()
        self.__application_ids = [urandom(32).hex(),
                                  urandom(32).hex(),
                                  urandom(32).hex()]
        logging.info(
            "Calling worker_register contract..\n worker_id: %s\n " +
            "worker_type: %d\n " +
            "orgId: %s\n applicationIds %s\n details %s",
            self.__worker_id, self.__worker_type.value,
            self.__org_id, self.__application_ids,
            self.__details)
        result = self.__eth_conn.worker_register(
            self.__worker_id, self.__worker_type,
            self.__org_id, self.__application_ids, self.__details)
        logging.info(
            "worker_register status \n %s",
            result)
        self.assertIsNotNone(
            result, "transaction execution failed")

    def test_worker_set_status(self):
        self.__status = WorkerStatus.DECOMMISSIONED
        logging.info(
            "Calling worker_set_status..\n worker_id: %s\n status: %d",
            self.__worker_id, self.__status.value)
        result = self.__eth_conn.worker_set_status(
            self.__worker_id, self.__status)
        logging.info(
            "worker_set_status status \n%s",
            result)
        self.assertIsNotNone(result, "worker set status response not matched")

    def test_worker_update(self):
        self.__new_details = json.dumps({
            "torkOrderSyncUri": "http://worker-order:8008",
            "workOrderNotifyUri": "http://worker-order-notify:9909"
        })
        logging.info(
            "Calling worker_update..\n worker_id: %s\n details: %s",
            self.__worker_id, self.__new_details)
        result = self.__eth_conn.worker_update(
            self.__worker_id, self.__new_details)
        logging.info(
            "worker_update status \n %s",
            result)
        self.assertIsNotNone(
            result, "worker update response not matched")

    def test_worker_lookup(self):
        logging.info(
            "Calling worker_lookup..\n worker_type: %d\n orgId: %s\n " +
            "applicationId: %s",
            self.__worker_type.value,
            self.__org_id,
            self.__application_ids[0])
        result = self.__eth_conn.worker_lookup(
            self.__worker_type, self.__org_id,
            self.__application_ids[0])
        logging.info(
            "worker_lookup result [%s]", result)
        if result['error']['code'] == JRPCErrorCodes.UNKNOWN_ERROR:
            logging.error("Caught an exception before sending the request")
            return
        self.assertEqual(
            res['result']['totalCount'], 1,
            "worker_lookup_next Response totalCount doesn't match")

        self.__worker_id = res['result']['ids'][0]
        self.__lookup_tag = res['result']['lookupTag']


    def test_worker_retrieve(self):
        logging.info(
            "Calling worker_retrieve..\n worker_id: %s",
            self.__worker_id)
        result = self.__eth_conn.worker_retrieve(self.__worker_id)
        logging.info(result)
        if result['error']['code'] == JRPCErrorCodes.UNKNOWN_ERROR:
            logging.error("Caught an exception before sending the request")
            return
        logging.info(
            "worker_retrieve status [%d, %s, %s, %s, %s]", result["status"],
            result["workerType"], result["organizationId"],
            result["applicationTypeId"],
            result["details"])
        self.assertEqual(
            result["workerType"], self.__worker_type.value,
            "Worker retrieve response worker type doesn't match")
        self.__org_id = res['result']['organizationId']
        self.__application_ids =  res['result']['applicationTypeId']
        self.__new_details = res['result']['details']
        self.__status = res['result']['status']

    def test_worker_lookup_next(self):
        lookUpTag = ""
        logging.info(
            "Calling worker_lookup_next..\n worker_type: %d\n" +
            "orgId: %s\n applicationId:%s\n lookUpTag: %s",
            self.__worker_type.value, self.__org_id,
            self.__application_ids[0], lookUpTag)
        result = self.__eth_conn.worker_lookup_next(
            self.__worker_type, self.__org_id, self.__application_ids[0],
            lookUpTag)
        logging.info(result)


def main():
    logging.info("Running test cases...")
    worker= {
        "direct_registry_contract_file" : "ethereum_contracts/WorkerRegistryList.sol",
        "worker_registry_contract_file" : "ethereum_contracts/WorkerRegistry.sol",
        "work_order_contract_file" : "ethereum_contracts/WorkOrderRegistry.sol",
        "direct_registry_contract_address" : "0xD5A613945DE851C7c2f83fFDA4de0aE01CE980c0",
        "worker_registry_contract_address" : "0x75a3Fd17E8c5CceAa9121251c359bFe4b9C343C8",
        "work_order_contract_address" : "0xf873133fae1d1f80642c551a6edd5A14f37129c2",
        "eth_account" : "0x7085d4d4c6efea785edfba5880bb62574e115626",
        "acc_pvt_key" : "4F611197A6E82715F4D2446FE015D1667E9C40A351411F3A7300F71F285D01B4",
        "solc_version" : "v0.5.15",
        "provider" : "http://rpc.node1.avalon.local:8555",
        "event_provider" : "http://node1.avalon.local:8545",
        "chain_id" : 3,
        "gas_limit" : 300000000,
        "gas_price" : "100"
    }
    
    test = TestEthereumWorkerRegistryImpl(worker)
    logging.info('Result: %s\n',test)
    test.test_worker_register()
    test.test_worker_update()
    test.test_worker_set_status()
    test.test_worker_lookup()
    test.test_worker_retrieve()


if __name__ == "__main__":
    main()
