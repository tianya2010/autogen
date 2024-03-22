import React, { useEffect } from "react";
import { IAgentFlowSpec, ILLMConfig, IModelConfig, ISkill } from "../../types";
import {
  GroupView,
  ControlRowView,
  ModelSelector,
  SkillSelector,
} from "../../atoms";
import { checkAndSanitizeInput } from "../../utils";
import { Input, Select, Slider } from "antd";
import TextArea from "antd/es/input/TextArea";

export const AgentFlowSpecView = ({
  title = "Agent Specification",
  flowSpec,
  setFlowSpec,
}: {
  title: string;
  flowSpec: IAgentFlowSpec;
  setFlowSpec: (newFlowSpec: IAgentFlowSpec) => void;
  editMode?: boolean;
}) => {
  // Local state for the FlowView component
  const [localFlowSpec, setLocalFlowSpec] =
    React.useState<IAgentFlowSpec>(flowSpec);

  // Required to monitor localAgent updates that occur in GroupChatFlowSpecView and reflect updates.
  useEffect(() => {
    setLocalFlowSpec(flowSpec);
  }, [flowSpec]);

  // Event handlers for updating local state and propagating changes

  const onControlChange = (value: any, key: string) => {
    if (key === "llm_config") {
      if (value.config_list.length === 0) {
        value = false;
      }
    }
    const updatedFlowSpec = {
      ...localFlowSpec,
      config: { ...localFlowSpec.config, [key]: value },
    };

    setLocalFlowSpec(updatedFlowSpec);
    setFlowSpec(updatedFlowSpec);
  };

  const llm_config: ILLMConfig = localFlowSpec?.config?.llm_config || {
    config_list: [],
    temperature: 0.1,
  };

  const nameValidation = checkAndSanitizeInput(flowSpec?.config?.name);

  return (
    // <>
    //   <div className="text-accent ">{title}</div>
    //   <GroupView
    //     title=<div className="px-2">{flowSpec?.config?.name}</div>
    //     className="mb-4 bg-primary  "
    //   >
    //     <ControlRowView
    //       title="Agent Name"
    //       className="mt-4"
    //       description="Name of the agent"
    //       value={flowSpec?.config?.name}
    //       control={
    //         <>
    //           <Input
    //             className="mt-2"
    //             placeholder="Agent Name"
    //             value={flowSpec?.config?.name}
    //             onChange={(e) => {
    //               onControlChange(e.target.value, "name");
    //             }}
    //           />
    //           {!nameValidation.status && (
    //             <div className="text-xs text-red-500 mt-2">
    //               {nameValidation.message}
    //             </div>
    //           )}
    //         </>
    //       }
    //     />

    //     <ControlRowView
    //       title="Agent Description"
    //       className="mt-4"
    //       description="Description of the agent, used by other agents
    //         (e.g. the GroupChatManager) to decide when to call upon this agent. (Default: system_message)"
    //       value={flowSpec.config.description || ""}
    //       control={
    //         <Input
    //           className="mt-2"
    //           placeholder="Agent Description"
    //           value={flowSpec.config.description || ""}
    //           onChange={(e) => {
    //             onControlChange(e.target.value, "description");
    //           }}
    //         />
    //       }
    //     />

    //     <ControlRowView
    //       title="Max Consecutive Auto Reply"
    //       className="mt-4"
    //       description="Max consecutive auto reply messages before termination."
    //       value={flowSpec.config?.max_consecutive_auto_reply}
    //       control={
    //         <Slider
    //           min={1}
    //           max={flowSpec.type === "groupchat" ? 600 : 30}
    //           defaultValue={flowSpec.config.max_consecutive_auto_reply}
    //           step={1}
    //           onChange={(value: any) => {
    //             onControlChange(value, "max_consecutive_auto_reply");
    //           }}
    //         />
    //       }
    //     />

    //     <ControlRowView
    //       title="Agent Default Auto Reply"
    //       className="mt-4"
    //       description="Default auto reply when no code execution or llm-based reply is generated."
    //       value={flowSpec.config.default_auto_reply || ""}
    //       control={
    //         <Input
    //           className="mt-2"
    //           placeholder="Agent Description"
    //           value={flowSpec.config.default_auto_reply || ""}
    //           onChange={(e) => {
    //             onControlChange(e.target.value, "default_auto_reply");
    //           }}
    //         />
    //       }
    //     />

    //     <ControlRowView
    //       title="Human Input Mode"
    //       description="Defines when to request human input"
    //       value={flowSpec.config.human_input_mode}
    //       control={
    //         <Select
    //           className="mt-2 w-full"
    //           defaultValue={flowSpec.config.human_input_mode}
    //           onChange={(value: any) => {
    //             onControlChange(value, "human_input_mode");
    //           }}
    //           options={
    //             [
    //               { label: "NEVER", value: "NEVER" },
    //               // { label: "TERMINATE", value: "TERMINATE" },
    //               // { label: "ALWAYS", value: "ALWAYS" },
    //             ] as any
    //           }
    //         />
    //       }
    //     />

    //     {llm_config && llm_config.config_list.length > 0 && (
    //       <ControlRowView
    //         title="System Message"
    //         className="mt-4"
    //         description="Free text to control agent behavior"
    //         value={flowSpec.config.system_message}
    //         control={
    //           <TextArea
    //             className="mt-2 w-full"
    //             value={flowSpec.config.system_message}
    //             rows={3}
    //             onChange={(e) => {
    //               onControlChange(e.target.value, "system_message");
    //             }}
    //           />
    //         }
    //       />
    //     )}
    //   </GroupView>
    // </>
    <></>
  );
};
