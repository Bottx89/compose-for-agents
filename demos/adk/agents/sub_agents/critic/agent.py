# Copyright 2025 Google LLC
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

"""Critic agent for identifying and verifying statements using search tools."""

from google.adk import Agent
from google.adk.models.lite_llm import LiteLlm
import os

from . import prompt
from .tools import create_mcp_toolsets

tools = create_mcp_toolsets(tools_cfg=["mcp/duckduckgo:search"])

critic_agent = Agent(
    model=LiteLlm(model=f"openai/{os.environ.get('DOCKER-MODEL-RUNNER_MODEL')}"),
    name='critic_agent',
    instruction=prompt.CRITIC_PROMPT,
    tools=tools,
)
