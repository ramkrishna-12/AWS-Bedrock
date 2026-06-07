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
    

    
    