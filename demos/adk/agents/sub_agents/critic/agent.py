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
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmResponse
from google.adk.tools import google_search
from google.adk.models.lite_llm import LiteLlm
from google.genai import types   # Part, Content, …
from google.adk.models import LlmRequest, LlmResponse
from typing import Optional

from . import prompt
import os, json
from .tools import create_mcp_toolsets, flatten_ddg_output

def _render_reference(
    callback_context: CallbackContext,
    llm_response: LlmResponse,
) -> LlmResponse:
    """Appends grounding references to the response."""
    del callback_context
    if (
        not llm_response.content or
        not llm_response.content.parts or
        not llm_response.grounding_metadata
    ):
        return llm_response
    references = []
    for chunk in llm_response.grounding_metadata.grounding_chunks or []:
        title, uri, text = '', '', ''
        if chunk.retrieved_context:
            title = chunk.retrieved_context.title
            uri = chunk.retrieved_context.uri
            text = chunk.retrieved_context.text
        elif chunk.web:
            title = chunk.web.title
            uri = chunk.web.uri
        parts = [s for s in (title, text) if s]
        if uri and parts:
            parts[0] = f'[{parts[0]}]({uri})'
        if parts:
            references.append('* ' + ': '.join(parts) + '\n')
    if references:
        reference_text = ''.join(['\n\nReference:\n\n'] + references)
        llm_response.content.parts.append(types.Part(text=reference_text))
    if all(part.text is not None for part in llm_response.content.parts):
        all_text = '\n'.join(part.text for part in llm_response.content.parts)
        llm_response.content.parts[0].text = all_text
        del llm_response.content.parts[1:]
    return llm_response

def force_string_content(
    callback_context: CallbackContext, llm_request: LlmRequest
) -> LlmResponse | None:
    """
    Ensure every Content in llm_request.contents ends up as a *single* text part,
    so llama.cpp never sees lists/dicts/None.
    """
    new_contents: list[types.Content] = []

    for content in llm_request.contents:
        # 1️⃣  If it is already plain text, keep it
        if isinstance(content, str):
            new_contents.append(types.Content(role="user", parts=[types.Part(text=content)]))
            continue

        # 2️⃣  Merge multiple Parts into a single string
        if isinstance(content, types.Content):
            merged_text = "\n".join((p.text or "") for p in content.parts)
            new_contents.append(
                types.Content(role=content.role or "user",
                              parts=[types.Part(text=merged_text)])
            )
            continue

        # 3️⃣  Fallback: JSON-encode any dict / list / None
        new_contents.append(
            types.Content(role="user",
                          parts=[types.Part(text=json.dumps(content, ensure_ascii=False))])
        )

    # add after new_contents construction
    collapsed = []
    for c in new_contents:
        if collapsed and collapsed[-1].role == c.role:
            collapsed[-1].parts[0].text += "\n" + c.parts[0].text
        else:
            collapsed.append(c)
    llm_request.contents = collapsed
    return None  # let ADK proceed normally

critic_agent = Agent(
    model=LiteLlm(model=f"openai/{os.environ.get('DOCKER-MODEL-RUNNER_MODEL')}"),
    name='critic_agent',
    instruction=prompt.CRITIC_PROMPT,
    tools=create_mcp_toolsets(tools_cfg=["mcp/duckduckgo:search"]),
    before_model_callback=force_string_content,
    after_model_callback=_render_reference,
    after_tool_callback=flatten_ddg_output,
)
