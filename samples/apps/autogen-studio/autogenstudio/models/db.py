from typing import Any, Callable, Dict, Literal, Optional, Union
from altair import List
from sqlmodel import JSON, Column, DateTime, Field, SQLModel, func
from datetime import datetime


class BaseDBModel(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default=datetime.now(), sa_column=Column(
        DateTime(timezone=True), server_default=func.now()))  # pylint: disable=not-callable
    updated_at: datetime = Field(default=datetime.now(), sa_column=Column(
        DateTime(timezone=True), onupdate=func.now()))  # pylint: disable=not-callable
    user_id: Optional[str] = None


class Message(BaseDBModel, table=True):
    role: str
    content: str
    session_id: str
    meta: Optional[Dict] = Field(default={}, sa_column=Column(JSON))


class Session(BaseDBModel, table=True):
    workflow_id: Optional[int] = Field(default=None, foreign_key="workflow.id")
    title: Optional[str] = None
    description: Optional[str] = None


class Skill(BaseDBModel, table=True):
    title: str
    content: str
    description: Optional[str] = None
    secrets: Optional[Dict] = Field(default={}, sa_column=Column(JSON))
    libraries: Optional[Dict] = Field(default={}, sa_column=Column(JSON))


class Model(BaseDBModel, table=True):
    model: str
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    api_type: Optional[str] = None
    api_version: Optional[str] = None
    description: Optional[str] = None


class LLMConfig(BaseDBModel, table=False):
    """ Data model for LLM Config for AutoGen """

    config_list: List[Model] = Field(
        default_factory=list, sa_column=Column(JSON))
    temperature: float = 0
    cache_seed: Optional[int] = None
    timeout: Optional[int] = None
    max_tokens: Optional[int] = None


# @dataclass
# class AgentConfig:
#     """Data model for Agent Config for AutoGen"""

#     name: str
#     llm_config: Optional[Union[LLMConfig, bool]] = False
#     human_input_mode: str = "NEVER"
#     max_consecutive_auto_reply: int = 10
#     system_message: Optional[str] = None
#     is_termination_msg: Optional[Union[bool, str, Callable]] = None
#     code_execution_config: Optional[Union[bool, str, Dict[str, Any]]] = None
#     default_auto_reply: Optional[str] = ""
#     description: Optional[str] = None

class AgentConfig(BaseDBModel, table=False):
    name: str
    llm_config:  Optional[Union[LLMConfig, bool]] = False
    human_input_mode: str = "NEVER"
    max_consecutive_auto_reply: int = 10
    system_message: Optional[str] = None
    is_termination_msg: Optional[Union[bool, str, Callable]] = None
    code_execution_config: Optional[Dict[str, Any]] = None
    default_auto_reply: Optional[str] = ""
    description: Optional[str] = None


class Agent(BaseDBModel, table=True):
    type: Literal["assistant", "userproxy"]
    config: AgentConfig = Field(
        default_factory=AgentConfig, sa_column=Column(JSON))
    skills: Optional[List[Skill]] = Field(
        default_factory=list, sa_column=Column(JSON))


class GroupChatConfig(BaseDBModel, table=False):
    agents: List[Agent] = Field(default_factory=list)
    admin_name: str = "Admin"
    messages: List[Dict] = Field(default_factory=list)
    max_round: Optional[int] = 10
    admin_name: Optional[str] = "Admin"
    speaker_selection_method: Optional[str] = "auto"
    allow_repeat_speaker: Optional[Union[bool, List[AgentConfig]]] = True


class GroupChat(BaseDBModel, table=True):
    type: Literal["groupchat"]
    config: AgentConfig = Field(
        default_factory=AgentConfig, sa_column=Column(JSON))
    groupchat_config: Optional[GroupChatConfig] = Field(
        default_factory=GroupChatConfig, sa_column=Column(JSON))
    skills: Optional[List[Skill]] = Field(
        default_factory=list, sa_column=Column(JSON))


class Workflow(BaseDBModel, table=True):
    name: str
    description: str
    sender: Agent = Field(default_factory=Agent, sa_column=Column(JSON))
    receiver: Union[Agent, GroupChat] = Field(
        default_factory=Union[Agent, GroupChat], sa_column=Column(JSON))
    type: Literal["twoagents", "groupchat"] = "twoagents"
    summary_method: Optional[Literal["last", "none", "llm"]] = "last"
