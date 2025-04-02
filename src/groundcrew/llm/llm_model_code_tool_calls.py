from dotenv import load_dotenv
load_dotenv("..")

import json

import mlflow
# from mlflow import log_metric, log_param, log_artifacts

from groundcrew.dataclasses import Colors
from groundcrew.toolfolder.code_analysis_tools import tool_functions as code_tool_functions
from InfluxRecording import AiRackRecorder, RemarkTag

from dataclasses import dataclass, field, is_dataclass, asdict

from datetime import datetime


@dataclass(frozen=False)
class TestSetup:
    tools: list[str] = field(default_factory=list)
    prompts_to_tool: list[dict] = field(default_factory=list)

@dataclass(frozen=False)
class TestResultToolCall:
    name: str
    call: str = ""

@dataclass(frozen=False)
class TestResult:
    model: str
    prompt: str
    tool_calls: list[TestResultToolCall] = field(default_factory=list)
    success: bool = False
    comment: str = ""




def assert_tool_calls(query, expected, chosen_tools):
    
    tool_call_correctnes = 10
    args_correctnes = 10

    if chosen_tools is not None:
        modified_chosen_tools = json.loads(json.dumps(chosen_tools))
        for obj in modified_chosen_tools:
            obj.pop('reason', None)
    else:
        modified_chosen_tools = None

    comment = None
    
    if expected is None:
        if chosen_tools is None:
            comment = f"correct tool choice"
            print(Colors.GREEN, comment, Colors.ENDC) 
            return 10, 10, 10, comment
        if chosen_tools is not None:
            comment = f"Assertion: unexpected tool choice"
            print(Colors.YELLOW, comment, Colors.ENDC)
            return 5, 5, 0, comment
        
    if chosen_tools is None:
        if expected is not None:
            comment = f"Assertion: missing tool choice"
            print(Colors.RED, comment, Colors.ENDC)
            return 1, 1, 1, comment
    
    success = 10

    
    if modified_chosen_tools != expected:
        if modified_chosen_tools is None:
            comment = f"Assertion: no tool_calls for query '{query}': {chosen_tools}"
            print(Colors.RED, comment)
            success = 1
            tool_call_correctnes = 1
            args_correctnes = 1
        else:
            expected_tool = expected[0]
            expected_tool_name = expected_tool['name']
            if not expected_tool_name in [tool.get('name',"") for tool in chosen_tools]:
                comment = f"Assertion: expected tool not called '{query}': {chosen_tools}"
                print(Colors.RED, comment)
                success = 2
                tool_call_correctnes = 2
                args_correctnes = 2
                
            else:
                print(Colors.GREEN, f"correct tool choice")
                
                chosen_tool = [tool for tool in chosen_tools if tool.get('name',"")==expected_tool_name][0]
                expected_args = expected_tool.get('arguments', {})
                calculated_args = chosen_tool.get('arguments', {})
                comment = ""
                tool_call_correctnes = 10
                args_correctnes = 10
                for key in expected_args:
                    if not key in calculated_args:
                        comment += f"Item {expected_tool_name}: Missing argument key '{key}' in calculated arguments\n"
                        print(Colors.RED, comment)
                        success = 3
                        args_correctnes = 3

    else:
        print(Colors.GREEN)
        print(f"correct tool choice")
    
    print(Colors.ENDC)

    return success, tool_call_correctnes, args_correctnes, comment


def transform_to_md_table(test_results: list[TestResult]) -> str:
    """
    Transform a list of TestResult objects into an MD table string.
    
    :param test_results: List of TestResult objects
    :return: Markdown table string
    """
    md_table = "| Model | Prompt | Tool Name | Tool Call | success | comment |\n"
    md_table += "| --- | --- | --- | --- | --- | --- |\n"
    
    for test_result in test_results:
        # Handle each tool call on a new line, or just the test result if no tool calls
        for i, tool_call in enumerate(test_result.tool_calls):
            if i == 0:  # First row includes prompt
                md_table += f"| {test_result.model} | {test_result.prompt} | {tool_call.name} | {tool_call.call} | {test_result.success}| {test_result.comment}|\n"
            else:  # Subsequent rows leave prompt column empty
                args_str = ', '.join(f"{k}: {v}" for k, v in tool_call.args.items())
                md_table += f"| | | {tool_call.name} | {args_str} | | |\n"
        
        # If no tool calls, just add the test result once
        if not test_result.tool_calls:
            md_table += f"| {test_result.model} | {test_result.prompt} | | |{test_result.success}| {test_result.comment}|\n"
    
    return md_table.strip()  # Remove trailing newline




mlflow.set_tracking_uri("http://htkasrv120:5000")
mlflow.set_experiment("PHU3_Ollama_basic_tool_calls")



from groundcrew.llm.llm_model import ollama_model

#llmO = ollama_model(base_message="You are a specialist for code analysis. The user will ask questions to a codebase that is available to you by utilizing tools you are given. Using them will give you the required information to answer the query. Do not speculate about the codebase, use the tools to request details.")
llm = ollama_model(base_message="You are an assistant that answers question about a codebase. All of the user's questions should be about this particular codebase, and you will be given tools that you can use to help you answer questions about the codebase.")
# llmO = ollama_model(base_message="You are an assistant that answers question about a codebase. All of the user's questions should be about this particular codebase, and you will be given tools that you can use to help you answer questions about the codebase."+"""
# Look at the Tool descriptions and choose one (or more) which seams likely to give you specific information to answer the users query in the Question section. 
# """)
llm.setup()

ts = TestSetup()
ts.prompts_to_tool = [
    {"query":"how is the system message for each call to the llm built?"                         , "tool_calls": [{"name": "CodebaseQATool", "arguments": {"user_prompt": "explain how the system message for each LLM call is constructed within the system", "include_code": True}}]}, 
    {"query":"how exactly is the system message for each call to the llm built in the codebase?" , "tool_calls": [{"name": "CodebaseQATool", "arguments": {"user_prompt": "explain the process of constructing system messages for each LLM call within the codebase", "include_code": True }}]}, 
    {"query":"is there an animal with fur and beak?"  , "tool_calls": None}
    ]

trs = []




for function in code_tool_functions:
    name = llm.register_tool_function(function)
    ts.tools.append(name)

start_time = datetime.now()


with mlflow.start_span(name="query_all_models") as span:
        span.set_inputs(ts)
    
#    try:
        models = llm.get_models()
        for model in models:

            print(f"\n\n### {model} ###")
            for i,query_dict in enumerate(ts.prompts_to_tool):
                query = query_dict["query"]
                tr = TestResult(model,query)
                trs.append(tr)

                with mlflow.start_run(run_name=f'{model}_q{i}', tags={'model':model, 'query': query}) as agent_run:
                    
                    with mlflow.start_span(name="agent_call") as agent_span:
                        ags = agent_span
                        agent_span.set_inputs({'model':model, 'query':query})

                        with AiRackRecorder(3) as recorder:
                            recorder.remark(RemarkTag.Comment, f"model: {model}")
            
                            mlflow.log_params({'model':model, 'query':query})
                            answer, chosen_tools = llm.single_completion(query, model)


                            if chosen_tools is not None:
                                for tool in chosen_tools:
                                    trtc = TestResultToolCall(tool.get('name'))
                                    tr.tool_calls.append(trtc)
                                    try:
                                        mlflow.log_params(tool)
                                        tool_answer = llm.call_tool(tool)
                                        trtc.call = tool_answer
                                        mlflow.log_params({'tool_result':tool_answer})
                                        print(Colors.BLUE, tool_answer, Colors.ENDC)
                                    except Exception as ex:
                                        print(Colors.RED, ex, Colors.ENDC)

                            success, tool_call_correctnes, args_correctnes, comment = assert_tool_calls(query, query_dict.get('tool_calls',[]), chosen_tools)
                            tr.success = success
                            tr.comment = comment
                            recorder.remark(RemarkTag.Comment, f"model: {model}, success: {success}")
                            mlflow.log_metric('call_success',success)
                            mlflow.log_metric('tool_call_correctnes',tool_call_correctnes)
                            mlflow.log_metric('args_correctnes',args_correctnes)


                        recording = recorder.recording
                        energy = recording.keyfigures.start_end_extra_energy
                        agent_span.set_outputs({'calls':tr.tool_calls, 'energy': energy})
                        mlflow.log_metric('energy',energy)
                        mlflow.log_metric('tot_energy',recording.keyfigures.start_end_tot_energy)
                        mlflow.log_metric('duration',recording.keyfigures.start_end_duration.total_seconds())

                        print(Colors.MAGENTA, f"model: {model}, success: {success}, energy used: {energy:.1f} Ws", Colors.ENDC)

            #print(transform_to_md_table(trs))
#    except Exception as ex:
#        print(ex)

        span.set_outputs(trs)

end_time = datetime.now()

#print(transform_to_md_table(trs))

print(f"\n\n*** all done ***, used {(end_time-start_time).seconds} s")