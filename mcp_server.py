# basic import
from typing import List, Dict, Any, Callable
import inspect

from mcp.server.fastmcp import FastMCP, Image
from mcp.server.fastmcp.prompts import base
from mcp.types import TextContent
from mcp.server import Server
from pydantic import BaseModel
from starlette.routing import Mount, Route
import uvicorn
from mcp import types
from PIL import Image as PILImage
import math
import sys
import time
import subprocess
from rich.console import Console
from rich.panel import Panel
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from starlette.applications import Starlette
from mcp.server.sse import SseServerTransport

from model import (
    AddInput, AddListInput, AddListOutput, AddOutput, CreateThumbnailInput, SubtractInput,
    SubtractOutput,
    MultiplyInput, MultiplyOutput, DivideInput, DivideOutput,
    PowerInput, PowerOutput, SqrtInput, SqrtOutput,
    CbrtInput, CbrtOutput, FactorialInput, FactorialOutput,
    LogInput, LogOutput, RemainderInput, RemainderOutput,
    TrigInput, TrigOutput, MineInput, MineOutput,
    ShowReasoningInput, StringToAsciiInput, StringToAsciiOutput,
    ExponentialSumInput, ExponentialSumOutput,
    FibonacciInput, FibonacciOutput,PaintTextInsideRectangleInput,
    CompareInput, CompareOutput, EvaluateInput, EvaluateOutput, OpenPaintOutput, PaintRectangleOutput,
    PaintTextInsideRectangleOutput)
# from win32api import GetSystemMetrics

console = Console()
# instantiate an MCP server client
mcp = FastMCP("Calculator", settings= {"host": "127.0.0.1", "port": 7172})

app = FastAPI()

# DEFINE TOOLS

#addition tool
@mcp.tool()
def add(input: AddInput) -> AddOutput:
    """Add two numbers"""
    print("CALLED: add(input: AddInput) -> AddOutput:")
    return AddOutput(result=(input.a + input.b))

@mcp.tool()
def add_list(input: AddListInput) -> AddListOutput:
    """Add all numbers in a list"""
    print("CALLED: add_list(input: AddListInput) -> AddListOutput:")
    return AddListOutput(result=sum(input.l))

# subtraction tool
@mcp.tool()
def subtract(input: SubtractInput) -> SubtractOutput:
    """Subtract two numbers"""
    print("CALLED: subtract(input: SubtractInput) -> SubtractOutput:")
    return SubtractOutput(result=(input.a - input.b))

# multiplication tool
@mcp.tool()
def multiply(input: MultiplyInput) -> MultiplyOutput:
    """Multiply two numbers"""
    print("CALLED: multiply(input: MultiplyInput) -> MultiplyOutput:")
    return MultiplyOutput(result=(input.a * input.b))

#  division tool
@mcp.tool() 
def divide(input: DivideInput) -> DivideOutput:
    """Divide two numbers"""
    print("CALLED: divide(input: DivideInput) -> DivideOutput:")
    return DivideOutput(result=(input.a / input.b))

# power tool
@mcp.tool()
def power(input: PowerInput) -> PowerOutput:
    """Power of two numbers"""
    print("CALLED: power(input: PowerInput) -> PowerOutput:")
    return PowerOutput(result=int(input.a ** input.b))

# square root tool
@mcp.tool()
def sqrt(input: SqrtInput) -> SqrtOutput:
    """Square root of a number"""
    print("CALLED: sqrt(input: SqrtInput) -> SqrtOutput:")
    return SqrtOutput(result=float(input.a ** 0.5))

# cube root tool
@mcp.tool()
def cbrt(input: CbrtInput) -> CbrtOutput:
    """Cube root of a number"""
    print("CALLED: cbrt(input: CbrtInput) -> CbrtOutput:")
    return CbrtOutput(result=float(input.a ** (1/3)))

# factorial tool
@mcp.tool()
def factorial(input: FactorialInput) -> FactorialOutput:
    """Factorial of a number"""
    print("CALLED: factorial(input: FactorialInput) -> FactorialOutput:")
    return FactorialOutput(result=int(math.factorial(input.a)))

# log tool
@mcp.tool()
def log(input: LogInput) -> LogOutput:
    """Log of a number"""
    print("CALLED: log(input: LogInput) -> LogOutput:")
    return LogOutput(result=float(math.log(input.a)))

# remainder tool
@mcp.tool()
def remainder(input: RemainderInput) -> RemainderOutput:
    """Remainder of two numbers division"""
    print("CALLED: remainder(input: RemainderInput) -> RemainderOutput:")
    return RemainderOutput(result=int(input.a % input.b))

# sin tool
@mcp.tool()
def sin(input: TrigInput) -> TrigOutput:
    """Sin of a number"""
    print("CALLED: sin(input: TrigInput) -> TrigOutput:")
    return TrigOutput(result=float(math.sin(input.a)))

# cos tool
@mcp.tool()
def cos(input: TrigInput) -> TrigOutput:
    """Cos of a number"""
    print("CALLED: cos(input: TrigInput) -> TrigOutput:")
    return TrigOutput(result=float(math.cos(input.a)))

# tan tool
@mcp.tool()
def tan(input: TrigInput) -> TrigOutput:
    """Tan of a number"""
    print("CALLED: tan(input: TrigInput) -> TrigOutput:")
    return TrigOutput(result=float(math.tan(input.a)))

# @mcp.tool()
# def calculate(expression: str) -> TextContent:
#     """Calculate the result of an expression"""
#     console.print("[blue]FUNCTION CALL:[/blue] calculate()")
#     console.print(f"[blue]Expression:[/blue] {expression}")
#     try:
#         result = eval(expression)
#         console.print(f"[green]Result:[/green] {result}")
#         return TextContent(
#             type="text",
#             text=str(result)
#         )
#     except Exception as e:
#         console.print(f"[red]Error:[/red] {str(e)}")
#         return TextContent(
#             type="text",
#             text=f"Error: {str(e)}"
#         )

# mine tool
@mcp.tool()
def mine(input: MineInput) -> MineOutput:
    """Special mining tool"""
    print("CALLED: mine(input: MineInput) -> MineOutput:")
    return MineOutput(result=int(input.a - input.b - input.b))


# reasoning tool
@mcp.tool()
def show_reasoning(input: ShowReasoningInput) -> TextContent:
    """Show the step-by-step reasoning process"""
    console.print("[blue]FUNCTION CALL:[/blue] show_reasoning()")
    for i, step in enumerate(input.steps, 1):
        console.print(Panel(
            f"{step}",
            title=f"Step {i}",
            border_style="cyan"
        ))
    
    # Create a TextContent object
    return TextContent(type="text", text="Reasoning shown")

@mcp.tool()
def create_thumbnail(input: CreateThumbnailInput) -> Image:
    """Create a thumbnail from an image"""
    print("CALLED: create_thumbnail(image_path: str) -> Image:")
    img = PILImage.open(input.image_path)
    img.thumbnail((100, 100))
    # return CreateThumbnailOutput(result=Image(data=img.tobytes(), format="png"))
    return Image(data=img.tobytes(), format="png")

@mcp.tool()
def strings_to_chars_to_int(input: StringToAsciiInput) -> StringToAsciiOutput:
    """Return the ASCII values of the characters in a word"""
    print("CALLED: strings_to_chars_to_int(input: StringToAsciiInput) -> StringToAsciiOutput:")
    return StringToAsciiOutput(result=[int(ord(char)) for char in input.string])

'''
@mcp.tool()
def int_list_to_exponential_sum(input: ExponentialSumInput) -> ExponentialSumOutput:
    """Return sum of exponentials of numbers in a list"""
    print("CALLED: int_list_to_exponential_sum(input: ExponentialSumInput) -> ExponentialSumOutput:")
    return ExponentialSumOutput(result=sum(math.exp(i) for i in input.int_list))
'''

@mcp.tool()
def fibonacci_numbers(input: FibonacciInput) -> FibonacciOutput:
    """Return the first n Fibonacci Numbers"""
    print("CALLED: fibonacci_numbers(input: FibonacciInput) -> FibonacciOutput:")
    if input.n <= 0:
        return FibonacciOutput(result=[])
    fib_sequence = [0, 1]
    for _ in range(2, input.n):
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    return FibonacciOutput(result=fib_sequence[:input.n])


@mcp.tool()
def compare(input: CompareInput) -> CompareOutput:
    """Return 1 if a is greater than b otherwise -1 in case b is less than a. It returns 0 if a equals to b."""
    result = 1 if input.a > input.b else -1 if input.a < input.b else 0
    return CompareOutput(result=result)


@mcp.tool()
def evaluate(input: EvaluateInput) -> EvaluateOutput:
    "Calculate the mathematical expression given in the input."
    result = eval(input.expression)
    return EvaluateOutput(result=result)


def is_process_running(process_name: str) -> bool:
    """Check if a process with given name is running using `ps`."""
    try:
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        return process_name.lower() in result.stdout.lower()
    except Exception as e:
        print(f"Error checking process: {e}")
        return False


def is_website_open_in_chrome(url_substring: str) -> bool:
    """
    Check if a website (via substring) is open in any Chrome tab.
    Example: 'google.com' will match any tab with Google.
    """
    script = '''
    set siteList to ""
    tell application "Google Chrome"
        repeat with w in windows
            repeat with t in tabs of w
                set siteList to siteList & (URL of t) & linefeed
            end repeat
        end repeat
    end tell
    return siteList
    '''
    try:
        result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
        tabs = result.stdout.strip().splitlines()
        for tab in tabs:
            if url_substring.lower() in tab.lower():
                return True
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False


@mcp.tool()
def open_paint_app_in_browser() -> OpenPaintOutput:
    """This ACTION opens paint app in browser which can be used to draw any shapes eg rectangle, circle, ellipse etc.
    It can also be used to write text. """
    print("CALLED: open_paint_app_in_browser() -> bool:")

    # chrome_options = Options()
    # chrome_options.add_argument("--disable-extensions")
    # chrome_options.add_argument("--disable-gpu")
    # chrome_options.add_argument("--headless")
    # driver = webdriver.Chrome(
    #    service=Service(ChromeDriverManager().install()),
    #    options=chrome_options
    # )
    start_url = "https://jspaint.app/"
    import subprocess, pyautogui

    # Example: Open Pages app
    subprocess.run(["open", "-a", "Google Chrome"])
    MAX_BROWSER_OPEN_WAIT_TIME = 5
    waited_enough = 0
    while not is_process_running("Google Chrome") and (waited_enough < MAX_BROWSER_OPEN_WAIT_TIME):
        time.sleep(1)
        waited_enough += 1

    output = ""
    if is_process_running("Google Chrome"):
        output = f"The browser is open now. Now trying to open the paint app.\n"
    else:
        output = f"The browser was not open. You might have to call the function again to open the browser but do not try if you have called it twice already."

        return OpenPaintOutput(success=False, message=output)

    time.sleep(5)
    pyautogui.keyDown('command')
    pyautogui.press('t')
    pyautogui.keyUp('command')
    time.sleep(2)
    pyautogui.write(start_url, interval=0.05)
    pyautogui.press('enter')

    waited_enough = 0
    while not is_website_open_in_chrome(start_url) and (waited_enough < MAX_BROWSER_OPEN_WAIT_TIME):
        time.sleep(1)
        waited_enough += 1

    time.sleep(5)
    if is_website_open_in_chrome(start_url):
        output += f"The paint app was successfully opened in the browser as well."
        success = True
    else:
        output += f"The paint app could not be opened in the browser. You might have to call the function again to open the paint app but do not try if you have called it twice already."
        success = False

    return OpenPaintOutput(success=success, message=output)


@mcp.tool()
def create_rectangle_in_paint_app() -> PaintRectangleOutput:
    """Creates a rectangle in the paint app if the paint app is open. If paint app is not open, the rectangle is not created.
    Make sure the paint app is open before making this action call.
    By default, the upper left corner of the rectangle is at position (150, 300) and lower right corer of the rectangle is at (400, 500).
    """

    # if not driver:
    #    return "Failed to create rectangle as paint app was not opened."

    print("CALLED: create_rectangle_in_paint_app() -> bool:")

    print("Clicking on the Rectangle button on the panel..")
    import pyautogui
    pyautogui.leftClick(14, 325)
    time.sleep(0.3)

    print("Creating a Rectangle..")
    # Move to source point (x1, y1) and click-hold
    pyautogui.moveTo(150, 300)  # replace with your source coords
    pyautogui.mouseDown()

    # Drag to destination point (x2, y2)
    pyautogui.moveTo(400, 500, duration=1)  # smooth drag
    pyautogui.mouseUp()
    time.sleep(1)

    return PaintRectangleOutput(success=True, message=f"The rectangle with upper left corner (x: {150}, y: {300}) and bottom right corner (x: {400}, y: {500}) is created successfully.")


@mcp.tool()
def write_inside_rectangle_in_paint_app(input: PaintTextInsideRectangleInput) -> PaintTextInsideRectangleOutput:
    """Writes value inside the rectangle with upper left position (upperLeftX, upperLeftY)
    and bottom right position (bottomRightX, bottomRightY).
    Make sure the paint app is open. In case the paint app is not open, it fails to write the text.

    """
    # if not driver:
    #    return "Failed to write text as paint app was not opened."

    print("CALLED: write_inside_rectangle_in_paint_app(value: list) -> bool:")

    print("Clicking on the Text button on the panel..")

    import pyautogui
    pyautogui.moveTo(39, 280)
    time.sleep(0.3)
    pyautogui.leftClick()
    time.sleep(0.3)

    print("Creating a Text Box inside the rectangle..")
    # Move to source point (x1, y1) and click-hold
    pyautogui.moveTo(175, 320)  # replace with your source coords
    pyautogui.mouseDown()

    # Drag to destination point (x2, y2)
    pyautogui.moveTo(360, 460, duration=1)  # smooth drag
    pyautogui.mouseUp()
    time.sleep(0.3)

    print(f'Writing value {input.value} received from the calculation in the Text Box..')
    pyautogui.write(input.value, interval=0.05)

    # print("Qutiing browser in 2 seconds")

    time.sleep(10)
    # driver.quit()
    message = f'the {input.value} is written inside the text box with upper left position at (x: {input.upperLeftX}, y: {input.upperLeftY}) and ' \
              f'bottom left position at (x: {input.bottomRightX}, y: {input.bottomRightY}) successfully'

    return PaintTextInsideRectangleOutput(success=True, message=message)

@mcp.tool()
def close_paint_app():
    # "This function closes the browser and paint app"
    def close_chrome():
        """
        Closes all tabs and quits Google Chrome using AppleScript via subprocess.
        """
        script = '''
        tell application "Google Chrome"
            close windows
            quit
        end tell
        '''
        try:
            subprocess.run(['osascript', '-e', script], check=True)
            print("Google Chrome closed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error closing Chrome: {e}")

    # Example usage:
    close_chrome()
    return True

'''
@mcp.tool()
async def generate_llm_friendly_descriptions() -> List[Dict[str, Any]]:
    tools = await mcp.list_tools()
    #return tools
    return generate_tools_descriptions(tools)
'''

# DEFINE RESOURCES

# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    print("CALLED: get_greeting(name: str) -> str:")
    return f"Hello, {name}!"


# DEFINE AVAILABLE PROMPTS
@mcp.prompt()
def review_code(code: str) -> str:
    print("CALLED: review_code(code: str) -> str:")
    return f"Please review this code:\n\n{code}"
    

@mcp.prompt()
def debug_error(error: str) -> list[base.Message]:
    return [
        base.UserMessage("I'm seeing this error:"),
        base.UserMessage(error),
        base.AssistantMessage("I'll help debug that. What have you tried so far?"),
    ]

def create_starlette_app(mcp_server: Server, *, debug: bool = False) -> Starlette:
    """Create a Starlette application that can server the provied mcp server with SSE."""
    sse = SseServerTransport("/messages/")

    async def handle_sse(request: Request) -> None:
        async with sse.connect_sse(
                request.scope,
                request.receive,
                request._send,  # noqa: SLF001
        ) as (read_stream, write_stream):
            await mcp_server.run(
                read_stream,
                write_stream,
                mcp_server.create_initialization_options(),
            )

    return Starlette(
        debug=debug,
        routes=[
            Route("/sse", endpoint=handle_sse),
            Mount("/messages/", app=sse.handle_post_message),
        ],
    )

def start_sse():
    mcp_server = mcp._mcp_server  # noqa: WPS437
    import argparse
    from pdb import set_trace

    # set_trace()
    parser = argparse.ArgumentParser(description='Run MCP SSE-based server')
    parser.add_argument('--host', default='127.0.0.1', help='Host to bind to')
    parser.add_argument('--port', type=int, default=7172, help='Port to listen on')
    args = parser.parse_args()
    print("SSE args set.")

    # Bind SSE request handling to MCP server
    starlette_app = create_starlette_app(mcp_server, debug=True)
    app.mount("/", starlette_app)

    uvicorn.run(app, host=args.host, port=args.port) 

@app.get("/")
def read_root():
    return {"Hello": "Worlddd"}

@app.get("/mcp")
async def get_capabilites():
    return await mcp.list_tools()


if __name__ == "__main__":
    # Check if running with mcp dev command
    print("STARTING")
    if len(sys.argv) > 1:
        if sys.argv[1] == "dev":
            print("STARTING without transport for dev server")
            mcp.run() 
        elif sys.argv[1] == "sse":
            sys.argv.remove("sse")
            print("STARTING sse server")
            start_sse()
     # Run without transport for dev server
    else:
        print("STARTING with stdio for direct execution")
        mcp.run(transport="stdio")
else: 
    print("starting sse...")
    start_sse()
        

 # Run with stdio for direct execution
