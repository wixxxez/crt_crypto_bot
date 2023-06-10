import ProxyMessage
import itertools

class Agent:
    
    def is_possible_to_decrypt(self, last_layer,keys,message):
        try:
            word, _ = self.decrypt_message(last_layer,keys)
            print(word)
            print(ProxyMessage.DecryptedTextMessage().decrypt_message(ProxyMessage.EncryptedTextMessage().encrypt_message(message)))
            return word ==ProxyMessage.DecryptedTextMessage().decrypt_message(ProxyMessage.EncryptedTextMessage().encrypt_message(message))
        except ValueError as e:
            print(e)
            return False
    def encrypt_message(self, message, config):
        
        layers, keys = ProxyMessage.EncoderLayer(message,config['layers'],config['keys']).encrypt_message()
        info = f"Encrypted layers: \n"
        for i in layers:
            info += f"{i} = {layers[i]}\n"
            
        info+=f"Keys is {keys}"
        
        last_layer = dict(itertools.islice(layers.items(), len(layers.items())-1,len(layers.items())))
        print (self.is_possible_to_decrypt(last_layer, keys, message))
        return last_layer, keys, info
    
    def decrypt_message(self,last_layer, keys ):
        word, layers = ProxyMessage.DecoderLayer(last_layer,keys).decrypt_message()

        info = f"Decrypted layers: \n"
        for i in layers:
            info += f"{i} = {layers[i]}\n"
            
        info+=f"Keys is {keys}"
        
        return word, info