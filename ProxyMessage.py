import random
import sympy
import itertools
import numpy as np
from decimal import Decimal

class Message():
    
    def message(self)->None:
        pass
    
class EncryptedTextMessage(Message):
    
    def encrypt_message(self, message: str) -> list:
        
        encrypted_numbers = []
        for char in message:
            if char.isalpha():
                char = char.upper()
                number = ord(char) - 64
                encrypted_numbers.append(number)
            if char == " ":
                number = 40
                encrypted_numbers.append(number)
                
        return encrypted_numbers
    
class DecryptedTextMessage(Message):
    
    def decrypt_message(self, numbers: list)->str:
        decrypted_message = ''
        for num in numbers:
            print(num)
            if num == 40:
                decrypted_char = ' '
                print("Huj")
            else:
                decrypted_number = (num - 1) % 26
                decrypted_char = chr(int(decrypted_number) + 65)
            decrypted_message += decrypted_char

        return decrypted_message
    
class EncoderLayer(Message):

    def __init__(self, real_message:str, layers:int, keys_per_layer:int) -> None:
    
        self._layers = layers
        self._actual_encoded_layers = 0
        self._real_message =real_message
        self._keys_per_layer = keys_per_layer
        self._encrypted_message = EncryptedTextMessage().encrypt_message(real_message)
        self.generate_keys_for_layers()
        self._encrypted_numbers = {
            "converted message" :  self._encrypted_message 
        }
    def generate_keys_for_layers(self)->dict:
        
        def generate_prime(min_value, max_value):
            # Generate a random number within the specified range
            number = random.randint(min_value, max_value)

            # Find the next prime number greater than or equal to the generated number
            prime = sympy.nextprime(number)

            return prime
        
        layers_keys = {}
        for i in range(self._layers):
            
            keys = [generate_prime(1,100) for i in range(self._keys_per_layer)]
            
            layers_keys[f"{i+1}"] = keys
            
        self._layers_keys = layers_keys
        
    def encrypt_number(self, number:int, keys: list)->list:
       
        remainders=[]
        for i in keys:
            remainders.append( number % i )
            
        return remainders
    def encrypt_message(self)->None:
        
        numbers = list(self._encrypted_numbers.values())[self._actual_encoded_layers]
        new_layer = []
        self._actual_encoded_layers = self._actual_encoded_layers+1
        for i in numbers:
            new_layer.append(self.encrypt_number(i, self._layers_keys[f"{self._actual_encoded_layers}"]))
            
        reshaped_list = [element for sublist in new_layer for element in sublist]

        self._encrypted_numbers[f"Layer {self._actual_encoded_layers}"] = reshaped_list
        
       
        if self.check_acess():
            return self._encrypted_numbers, self._layers_keys
        else:
            return self.encrypt_message()
    def check_acess(self):
        
        return self._layers == self._actual_encoded_layers
    
class DecoderLayer(Message):
    
    def __init__(self,last_layer:dict, keys:dict) -> None:
        
        self._layer = np.array(list(last_layer.values())[0])
        self._keys = keys
        self._decoded_layers = 0
        self._decrypted_numbers = {}
        self._quantity_of_values_from_last_layer = len(list(keys.values())[0]) #len(list(keys.values())[0])**len(keys.keys())
        
    def chinese_remainder_theorem(self, modules, remainders):
        # Step 3: Calculate N
        N = 1
        for mod in modules:
            N *= mod

        result = 0
        for i in range(len(modules)):
            mod = modules[i]
            remainder = remainders[i]

            # Step 4: Calculate n_i
            n_i = N // mod

            # Step 5: Calculate x_i
            x_i = pow(n_i, -1, mod)  # Modular multiplicative inverse

            result += remainder * Decimal( n_i ) * Decimal(x_i)

        # Step 6: Calculate the final result
        return result % N
    
    
    
    def decrypt_message(self):
        
        quntity_of_values = self._quantity_of_values_from_last_layer 
        
        last_layer = self._layer.reshape(-1,quntity_of_values)
        
        for i in self._keys.__reversed__():
            modules = self._keys[i]
            new_layer = []
            self._decoded_layers += 1
            for numbers in last_layer:
                new_layer.append(self.chinese_remainder_theorem(modules, numbers))

            
            self._decrypted_numbers[f"Decoded numbers from layer {i}"] = new_layer
            if len(self._keys.items()) != self._decoded_layers:
                last_layer = np.array(new_layer).reshape(-1,quntity_of_values)
                
  
        if self.check_acess():
            return DecryptedTextMessage().decrypt_message(self._decrypted_numbers[list(self._decrypted_numbers.keys())[-1]]), self._decrypted_numbers
        
    def check_acess(self):
        
        return self._decoded_layers == len(self._keys.items())
