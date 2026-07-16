# chat implinmentation
class Chat:
    def __init__(self, name):
        self.name = name
        self.messages = []

    def send_message(self, message):
        self.messages.append(message)

    def get_messages(self):
        return self.messages 
# Example usage
if __name__ == "__main__":    chat = Chat("General")
    Chat.send_message(Chat, "Hello, everyone!")
    Chat.send_message(Chat, "Welcome to the chat room.")
    print(Chat.get_messages(Chat))
    

    
# chat is a simple implementation of a chat system that allows users to send and retrieve messages. The Chat class has methods to send messages and get the list of messages. In the example usage, a chat room named "General" is created, and two messages are sent to it. Finally, the list of messages is printed to the console.
# implementation of a chat system that allows users to send and retrieve messages. The Chat class has methods to send messages and get the list of messages. In the example usage, a chat room named "General" is created, and two messages are sent to it. Finally, the list of messages is printed to the console.