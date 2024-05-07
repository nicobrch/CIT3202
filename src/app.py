import chatbot

agent = chatbot.Chatbot()

agent.make_agent()

result = agent.ask("Cuáles son los 5 productos más baratos?")

print(result)