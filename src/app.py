import chatbot

agent = chatbot.Chatbot()

agent.make_agent()

result = agent.ask("A qué hora está abierta la tienda de costanera center?")

print(result)