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


from validation.argument_validator import ArgumentValidator
from validation.json_validator import json_validation
from handler.http_jrpc_client import HttpJrpcClient



@error_handler
def jrpc_api_validation(id, api_name, json_rpc_request, bool=True):
        """
        Check the json format of the final request
        
        Parameters:
        api_name   Name of the api
        json_rpc_request  Final request to be sent
        bool Boolean to specify if the message need to be sent
        
        
        Returns:
        if bool is true:
        JRPC response
        
        if bool is false:
        True and empty string on success and
        False and string with error message on failure.
        """
        
        flag, e_value = self.validation.not_null( id, api_name, json_rpc_request)
        if  not flag:
            return  e_value

        json_validation(id, "json_rpc", json_rpc_request)
        json_validation(id, api_name, json_rpc_request["params"])
        
        if bool:
            response = self.__uri_client._postmsg(json.dumps(json_rpc_request))
            return response

        return True