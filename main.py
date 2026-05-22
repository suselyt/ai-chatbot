from fastapi import FastAPI
from routes import router
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Programming Basics AI-Chatbot",
              description="Ai-Chatbot using FastAPI with UI",
              version="1.0.0",
)
app.include_router(router)
app.mount("/static", StaticFiles(directory="static"), name="static")

# TO DO: show js with the errors (not being able to process request, chat empty...)
# TO DO: add visual feedback while the AI is answering
# TO DO: fix to show markdown correctly 
# TO DO: add the alt text to show when hovering over a button
@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head>
            <title>Programming Chatbot</title>
            <script src="https://cdn.tailwindcss.com"></script>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
            <link rel="stylesheet" href="/static/styles.css">
        </head>
        <body class="flex flex-col h-screen bg-gray-900">
            <div id="header" class="flex justify-between py-4 px-5 text-white">
                <h1 class="text-lg font-semibold"><i class="fa-solid fa-code"></i> Ask Chat anything!</h1>
                <button onclick="restartChat()" class="cursor-pointer px-2 py-1 border border-gray-600 rounded-sm text-sm"><i class="fa-solid fa-arrow-rotate-right"></i> Restart</button>
                <!-- TO DO: add a dark and light theme switch -->
            </div>
                
            <div class="flex-1 overflow-y-auto flex flex-col">
                <div id="chatWindow" class="p-4 w-3/5 mx-auto text-white flex flex-col">
                    <div id="welcome-section" class="flex-1 flex flex-col items-center justify-center text-center max-w-md mx-auto gap-4">
                        <i class="fa-solid fa-robot text-6xl text-pink-300"></i>
                        <h2 class="text-2xl font-semibold">Chat-code</h2>
                        <p class="text-gray-400 text-base leading-relaxed">Hi, I'm Chat-code your personal assistant to help you understand basic programming topics. Send me a question and I'll try to explain it in really simple terms!</p>
                    </div>
                </div>
            </div>

            <div id="inputFooter" class="flex py-6 px-5 place-content-center gap-4">
                <textarea 
                    id="userInput" 
                    placeholder="Write your message" 
                    rows="1"
                    class="rounded-2xl bg-gray-700 text-white px-4 py-2 w-3/5 resize-none overflow-hidden max-h-24"
                ></textarea>
                <button id="sendButton" disabled onclick="sendMessage()" class="disabled:opacity-50 focus:ring-2 bg-white cursor-pointer rounded-full p-3"><i class="fa-solid fa-paper-plane"></i></button>
            </div>

            <script>
            async function sendMessage(){
                const input = document.getElementById("userInput")
                const message = input.value
                const chatWindow = document.getElementById("chatWindow")
                const sendButton = document.getElementById("sendButton")
                const welcomeSection = document.getElementById("welcome-section")           // hide the welcome section
                if (welcomeSection) {
                    welcomeSection.remove()
                }

                if (!message.trim()) return

                sendButton.disabled = true;                              // disables to send more messages
                const userMsg = document.createElement("div")            // user message
                userMsg.classList.add("flex", "justify-end", "mb-4")
                userMsg.innerHTML = `
                    <div class="max-w-xs lg:max-w-md">
                        <div class="flex items-center justify-end gap-2 mb-1">
                            <span class="text-xs text-gray-400">${getTime()}</span>
                            <span class="text-sm font-semibold">You</span>
                            <i class="fa-solid fa-user text-sm"></i>
                        </div>
                        <div class="bg-pink-400 text-white rounded-2xl rounded-tr-none px-4 py-2">
                            ${message}
                        </div>
                    </div>`
                chatWindow.appendChild(userMsg)

                input.value = ""                                         // clear input

                const aiMsg = document.createElement("div")              // AI message
                aiMsg.classList.add("flex", "justify-start", "mb-4")
                const bubble = document.createElement("div")  // separate variable so you can append chunks
                bubble.classList.add("bg-gray-700", "text-white", "rounded-2xl", "rounded-tl-none", "px-4", "py-2", "max-w-xs", "lg:max-w-md")
                aiMsg.innerHTML = `
                    <div class="max-w-xs lg:max-w-md">
                        <div class="flex items-center gap-2 mb-1">
                            <i class="fa-solid fa-robot text-sm"></i>
                            <span class="text-sm font-semibold">Chat-code</span>
                            <span class="text-xs text-gray-400">${getTime()}</span>
                        </div>
                    </div>`
                aiMsg.firstElementChild.appendChild(bubble)
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

                                const tokenToggle = document.createElement("details")
                                tokenToggle.classList.add("text-xs", "text-gray-400", "mt-1", "cursor-pointer")
                                tokenToggle.innerHTML = `
                                    <summary class="list-none flex items-center gap-1 hover:text-gray-300">
                                        <i class="fa-solid fa-ellipsis text-xs"></i> Token usage
                                    </summary>
                                    <div class="mt-1 pl-2 flex flex-col gap-1">
                                        <span>Prompt: ${tokenData[0]}</span>
                                        <span>Completion: ${tokenData[1]}</span>
                                        <span>Total: ${tokenData[2]}</span>
                                    </div>`
                                aiMsg.firstElementChild.appendChild(tokenToggle)
                            }
                            else if(line.startsWith("data: ")) {
                                const text = line.replace("data: ", "")
                                bubble.innerHTML += text
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

            function getTime(){
                return new Date().toLocaleTimeString([], {hour: '2-digit', minute: '2-digit'})
            }

            async function restartChat(){
                await fetch("/reset", { method: "POST" })
                document.getElementById("chatWindow").innerHTML = 
                `<div id="welcome-section" class="flex-1 flex flex-col items-center justify-center text-center max-w-md mx-auto gap-4">
                    <i class="fa-solid fa-robot text-6xl text-blue-400"></i>
                    <h2 class="text-2xl font-semibold">Chat-code</h2>
                    <p class="text-gray-400 text-base leading-relaxed">Hi, I'm Chat-code your personal assistant to help you understand basic programming topics. Send me a question and I'll try to explain it in really simple terms!</p>
                </div>
                `;
            }

            document.getElementById("userInput").addEventListener("input", function(){
                const sendButton = document.getElementById("sendButton")
                sendButton.disabled = !this.value.trim()
            })

            document.getElementById("userInput").addEventListener("input", function(){
                this.style.height = "auto"
                this.style.height = this.scrollHeight + "px"
            })

            document.addEventListener("keydown", function(event) {
                if (event.key === "Enter" && !event.shiftKey) {
                    event.preventDefault()
                    sendMessage()
                }
            })
            </script>
        </body>
    </html>
    """