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

import logging
import os
from os import environ
from os.path import exists, realpath
import json
import random

from enums.proxy.contract_response import ContractResponse
from validation.argument_validator import ArgumentValidator
from importlib_resources import files
from avalon_sdk_fabric import base
from avalon_sdk_fabric import tx_committer
from avalon_sdk_fabric import event_listener
from hfc.protos.common import common_pb2 as common

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)


class FabricWrapper():
    """
    Fabric wrapper class to interact with Fabric blockchain.
    It provides wrapper functions to invoke and query chain code.
    """

    def __init__(self, config):
        """
        Constructor to initialize wrapper with required parameter.

        Parameters:
        config    Dictionary containing parameters for Fabric.
                  These parameters are read from a .toml file
        """
        self.validation = ArgumentValidator.getInstance()
        self.__validate(config)

        self.__channel_name = config.get("channel_name")
        self.__orgname = base.get_net_info(self.__network_config,
                                           'client', 'organization')
        logging.info("Org name choose: {}".format(self.__orgname))
        self.__peername = random.choice(base.get_net_info(
            self.__network_config, 'organizations', self.__orgname,
            'peers'))
        # Get a txn committer
        self.__txn_committer = tx_committer.TxCommitter(
            self.__network_conf_file,
            self.__channel_name, self.__orgname,
            self.__peername, 'Admin')

    def __validate(self, config):
        """
        Validate a parameter from the config parameters for existence.

        Parameters:
        config    Configuration parameter

        Returns:
        True if validation succeeds or false if validation fails.
        """
        
        self.validation.not_valid_contract(
            fabric_network_file = config.get("fabric_network_file"),
            chnnel_name = config.get("channel_name"))

        conf_file = config.get("fabric_network_file")
        exec_path = os.get_exec_path() 
        logging.info(exec_path)
        self.__network_conf_file = files('avalon_sdk').joinpath(conf_file)
        logging.info(self.__network_conf_file)
        #.joinpath(conf_file)
        self.__network_config = json.loads(self.__network_conf_file.read_text())
        self.__valid_calls = files('avalon_sdk_fabric').joinpath( 'methods.json').read_text()

        return True

    def invoke_chaincode(self, chaincode_name, method_name, params):
        """
        This is wrapper method to invoke chain code.

        Parameters:
        chaincode_name Name of the chain code
        method_name    Chain code method name
        params         List of arguments to method

        Returns:
        If the call to chain code query, then it
        returns the payload of the chain code response
        on success or None on error.
        If the call is invoking chain code, then it
        returns ContractResponse.SUCCESS on success
        and ContractResponse.ERROR on failure.
        """
        cc_methods = self.__valid_calls[chaincode_name]
        
        self.validation.not_null(None, cc_methods)
        the_call = cc_methods[method_name]
        self.validation.not_null(None, the_call)
        resp = self.__txn_committer.cc_invoke(params, chaincode_name,
                                              method_name, '',
                                              queryonly=the_call['isQuery'])
        logging.info("Response of chain code {} call: {}".format(
            method_name, resp
        ))

        # In case query chain code call
        # it has response in dictionary format
        # convert it to tuple with values.
        if the_call['isQuery'] is True:
            if resp:
                result = []
                for v in resp.values():
                    result.append(v)
                logging.info(
                    "\nThe tuple created: %s\n ", result)
                return result
            else:
                return None
        elif len(resp) > 0:
            # If it is invoke chain code call then response
            # has status SUCCESS otherwise it is an error
            if hasattr(resp[0], "status") and \
                    resp[0].status == common.Status.SUCCESS:
                return ContractResponse.SUCCESS
            else:
                return ContractResponse.ERROR

        else:
            return ContractResponse.ERROR

    def get_event_handler(self, event_name, chain_code, handler_func):
        """
        Create event handler object.

        Parameters:
        event_name   String to identify the event name
        chain_code   Chain code name as string
        handler_func Callback function name

        Returns:
        Event object
        """
        event_obj = event_listener.EventListener(
            self.__network_conf_file,
            self.__channel_name,
            self.__orgname,
            self.__peername,
            'Admin')
        event_obj.event = event_name
        event_obj.chaincode = chain_code
        event_obj.handler = handler_func
        return event_obj
