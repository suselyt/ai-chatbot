from fastapi import FastAPI
from routes import router
from fastapi.responses import HTMLResponse

app = FastAPI(title="Programming Basics AI-Chatbot",
              description="Ai-Chatbot using FastAPI with UI",
              version="1.0.0",
)
app.include_router(router)

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head>
            <title>Programming Chatbot</title>
            <script src="https://cdn.tailwindcss.com"></script>
        </head>
        <body>
            <div id="header">
                <h1>Ask Chat anything!</h1>
                <button onclick="restartChat()">Restart</button>
            </div>
                
            <div id="chatWindow">
                
            </div>

            <div id="inputFooter">
                <p id="tokenUsage"></p>
                <input type="text" id="userInput" placeholder="Write your message">
                <button id="sendButton" onclick="sendMessage()">Send</button>
            </div>

            <script>
            async function sendMessage(){
                const input = document.getElementById("userInput")
                const message = input.value

                if (!message.trim()) return

                const chatWindow = document.getElementById("chatWindow")
                const sendButton = document.getElementById("sendButton")

                sendButton.disabled = true;                              // disables to send more messages
                const userMsg = document.createElement("p")
                userMsg.innerHTML = `<b>You:</b> ${message}`             // display user message
                chatWindow.appendChild(userMsg)

                input.value = ""                                         // clear input

                const aiMsg = document.createElement("p")
                aiMsg.innerHTML = "<b>AI:</b> "                          // create AI message element to append chunks into
                chatWindow.appendChild(aiMsg)

                try{
                    const response = await fetch("/send_message", 
                    {
                        method: "POST",
                        headers: {"Content-Type": "application/json"},
                        body: JSON.stringify({message: message})
                    })

                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status} ${response.statusText}`);
                    }

                    const reader = response.body.getReader();
                    const decoder = new TextDecoder("utf-8");

                    while (true){
                        const { done, value } = await reader.read()
                        if (done) 
                            break

                        const chunkText = decoder.decode(value, { stream: true });
                        const lines = chunkText.split("\\n")                            // parse the SSE format
                        for (const line of lines){
                            if (line.startsWith("data: __TOKENS__")) {
                                const tokenData = line.replace("data: __TOKENS__", "").split(",")
                                document.getElementById("tokenUsage").innerHTML = 
                                    `Prompt: ${tokenData[0]} | Completion: ${tokenData[1]} | Total: ${tokenData[2]}`
                            }
                            else if(line.startsWith("data: ")) {
                                const text = line.replace("data: ", "")
                                aiMsg.innerHTML += text
                            }
                        }                 
                    }
                } catch(error){
                    console.error("API call failed:", error.message)
                    aiMsg.innerHTML += "Something went wrong. Please try again."
                } finally {
                    sendButton.disabled = false                                         // finally always runs, error or not
                }
            }

            async function restartChat(){
                await fetch("/reset", { method: "POST" })
                document.getElementById("chatWindow").innerHTML = "";
                document.getElementById("tokenUsage").innerHTML = "";
            }

            document.addEventListener("keydown", function(event) {
                if (event.key === "Enter") {
                    sendMessage()
                }
            });
            </script>
        </body>
    </html>
    """