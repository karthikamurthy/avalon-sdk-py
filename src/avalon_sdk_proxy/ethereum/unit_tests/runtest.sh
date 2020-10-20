#! /bin/bash

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



cd ../../..
pip uninstall dist/avalon_sdk_ethereum-0.0.4-py3-none-any.whl -y
rm /home/intel/python_sdk/worker_blockchain/avalon-sdk-py/sdk/_dev/lib/python3.6/site-packages/validation
make clean
make
pip install dist/avalon_sdk_ethereum-0.0.4-py3-none-any.whl

cd avalon_sdk_proxy/ethereum/unit_tests
python test_ethereum_worker_registry_impl.py


 
