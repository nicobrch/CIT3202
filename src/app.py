import chatbot

agent = chatbot.Chatbot()

agent.make_agent()

result = agent.ask("Puedo devolver un producto que vino defectuoso?")

print(result)