import asyncio
import os
from google import genai
from google.genai import types
from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client

server_params=StdioServerParameters(command="python",args=["server.py"])

client=genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

async def main():
    async with stdio_client(server_params) as (read,write):
        async with ClientSession(read,write) as session:
            await session.initialize()
            git_res=await session.call_tool("github_list_files",arguments={"repo_url":"https://github.com/Kaushik-2802/ML_Algorithms"})
            print("Github file structure:\n")
            print(git_res)
            # tools_res=await session.list_tools()
            # gemini_tools=[]
            # for tool in tools_res.tools:
            #     gemini_tools.append(
            #         types.FunctionDeclaration(
            #             name=tool.name,
            #             description=tool.description,
            #             parameters_json_schema=tool.inputSchema
            #         )
            #     )
            # tool_config=types.Tool(function_declarations=gemini_tools)
            # user_msg=input("\nYou:")
            # contents = [
            #     types.Content(role="user", parts=[types.Part.from_text(text=user_msg)])
            # ]
            # res=client.models.generate_content(
            #                     model="gemini-3.5-flash",
            #                     contents=contents,
            #                     config=types.GenerateContentConfig(tools=[tool_config])
            #                 )
            # while True:
            #     has_fn_call=any(
            #         part.function_call
            #         for candidate in res.candidates
            #         for part in candidate.content.parts
            #     )
            #     if not has_fn_call:
            #         print("Final:",res.text)
            #         break

            #     for candidate in res.candidates:
            #         for part in candidate.content.parts:
            #             if part.function_call:
            #                 function_call=part.function_call
            #                 tool_name=function_call.name
            #                 tool_args=dict(function_call.args)
            #                 print("Gemini Selected tool:",tool_name)
            #                 print("Arguments:",tool_args)
            #                 tool_res= await session.call_tool(tool_name,arguments=tool_args)
            #                 print("MCP tool result:",tool_res.content)
            #                 contents=[
            #                     types.Content(
            #                         role="user",
            #                         parts=[types.Part.from_text(text=user_msg)]
            #                     ),
            #                     res.candidates[0].content,
            #                     types.Content(
            #                         role="user",
            #                         parts=[
            #                             types.Part.from_function_response(name=tool_name,response={"result":str(tool_res.content)})
            #                         ]
            #                     )
            #                 ]
            #                 system_instruction="""
            #                 You are a developer assistant working with a software project.Your main job is to assist developers in writing and debugging code.

            #                 Rules:
            #                 - You should use the tools provided to you for answering.
            #                 - Ypou should not guess the content based on some lines of code.
            #                 - You need to get the required content asked by the user for your response.
            #                 - You should also explain the current code present in the file.
            #                 - You should clearly explain all the related concepts based on the content in the file.
            #                 - You should read files based on nessisity.
            #                 - You should also identify any errors in the current code.
            #                 - While diagnosing errors:
            #                     - First tell the developer why the error is happening.
            #                     - Also tell how to overcome the error.
            #                     - Suggest multiple possible methods to the user and also advice the user which is better.
            #                 - In the end keep the content well-structured and easily understandable.

            #                 while answering to the developer:
            #                  - Keep the explaination simple and keep the relevant content only.
            #                  - Explain relevant fixes step-wise
            #                  - Also support your response with example snippets.
            #                 """
            #                 follow=client.models.generate_content(
            #                     model="gemini-3.5-flash",
            #                     contents=contents,
            #                     config=types.GenerateContentConfig(tools=[tool_config],system_instruction=system_instruction)
            #                 )
            #                 print("Final:",follow)
            #     res=follow
                    

if __name__=="__main__":
    asyncio.run(main())