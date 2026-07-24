# Copyright 2012-2026 Tom (Thomas) Freudenberg <th.freudenberg@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0
#
# The akili module is a training and demonstration tool, intended for
# experimentation and for gathering insights. It is not required by the
# generated application and should be removed without side effects.
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

"""
The {{ app_name }} akili micro language model -- a small, complete,
teachable lab.

This package is a from-scratch decoder-only transformer that does exactly
one thing: turn a calendar request into a plan of tool calls. It is meant
to be read end to end. The modules, in the order they make sense:

- ```dsl``` -- the plan language: how a plan is written, parsed, and (most
    importantly) *constrained*, so the model can only emit legal plans
- ```tokenizer``` -- the byte vocabulary (no learned subwords), the reason
    the model copies dates and numbers exactly
- ```data``` -- the synthetic data generator and its single source of
    language, ```AKILI-LEX.yaml```
- ```train``` -- the network and the training loop (the only torch here)
- ```infer``` -- the same forward pass in plain NumPy, plus the
    grammar-constrained greedy decoder used at runtime

The long-form walkthrough below (```AKILI-LLM.md```) explains the training
pipeline, the anatomy of the weights, and constrained decoding with
diagrams. After it, ```AKILI-USE.md``` is the guided demo in three acts:
the fundi agent, the akili model, and -- on purpose -- the limits where
a language model breaks.

.. include:: ./AKILI-LLM.md

.. include:: ./AKILI-USE.md
"""
