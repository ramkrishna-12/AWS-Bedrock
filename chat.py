# chat implinmentation
from operator import call


class Chat:
    def __init__(self, name):
        self.name = name
        self.messages = []

    def send_message(self, message):
        self.messages.append(message)

    def get_messages(self):
        return self.messages 
    
    def __str__(self):
        return f"Chat Room: {self.name}, Messages: {self.messages}"
    
    classmethod
    def send_message(cls, message):
        cls.messages.append(message)
        if len(cls.messages) > 10:
            cls.messages.pop(0)  # Keep only the last 10 messages
        else:
            cls.messages.append(message)
            return cls.messages
    def client_send_message(self, message):
        self.send_message(message)
        return self.get_messages()
    
    load_messages = classmethod(lambda cls: cls.messages)
    gui = classmethod(lambda cls: f"Chat Room: {cls.name}, Messages: {cls.messages}")
    call = classmethod(lambda cls, message: cls.send_message(message))
# Example usage
if __name__ == "__main__":    chat = Chat("General")
    Chat.send_message(Chat, "Hello, everyone!")
    Chat.send_message(Chat, "Welcome to the chat room.")
    print(Chat.get_messages(Chat))

    

    
# chat is a simple implementation of a chat system that allows users to send and retrieve messages. The Chat class has methods to send messages and get the list of messages. In the example usage, a chat room named "General" is created, and two messages are sent to it. Finally, the list of messages is printed to the console.
# implementation of a chat system that allows users to send and retrieve messages. The Chat class has methods to send messages and get the list of messages. In the example usage, a chat room named "General" is created, and two messages are sent to it. Finally, the list of messages is printed to the console.