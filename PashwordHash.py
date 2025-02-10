
import hashlib
import time
import matplotlib.pyplot as plt
# used to improve code clarity
from typing import List, Tuple, Optional

class PasswordCracker:
    def __init__(self, dictionary_path: str):
        with open(dictionary_path, 'r') as f:
            # Create length-based word lists for faster lookup
            self.dictionary = {}
            for word in f.readlines():
                word = word.strip()
                length = len(word)
                if length not in self.dictionary:
                    self.dictionary[length] = []
                self.dictionary[length].append(word)
        
        self.results = []
        self.password_order = []
        self.attempts = 0
        
    def hash_password(self, password: str, hash_type: str) -> str:
        hasher = hashlib.new(hash_type)
        hasher.update(password.encode())
        return hasher.hexdigest()
    
    def find_password(self, target_hash: str, hash_type: str, target_length: int, 
                     current_length: int = 0, current_combo: str = "") -> Optional[str]:
        # Early termination if we've exceeded target length
        if current_length > target_length:
            return None
            
        # Check if we've found a match
        if current_length == target_length:
            self.attempts += 1
            if self.hash_password(current_combo, hash_type) == target_hash:
                return current_combo
            return None
            
        remaining_length = target_length - current_length
        
        # Try adding words that could fit in the remaining length
        for length in self.dictionary:
            if length <= remaining_length:
                for word in self.dictionary[length]:
                    result = self.find_password(
                        target_hash, 
                        hash_type,
                        target_length,
                        current_length + length,
                        current_combo + word
                    )
                    if result:
                        return result
        
        return None
    
    def crack_password(self, target_hash: str, hash_type: str, length: int) -> Tuple[int, float]:
        self.attempts = 0
        start_time = time.time()
        
        # First try single words of exact length for quick matches
        if length in self.dictionary:
            for word in self.dictionary[length]:
                self.attempts += 1
                if self.hash_password(word, hash_type) == target_hash:
                    return self.attempts, time.time() - start_time
        
        # If no match, try combinations
        result = self.find_password(target_hash, hash_type, length)
        
        return self.attempts, time.time() - start_time
    
    def run(self):
        total_words = sum(len(words) for words in self.dictionary.values())
        print(f"Dictionary loaded with {total_words} words")
        
        while True:
            password = input("\nEnter password (or 'q' to quit): ")
            if password.lower() == 'q':
                break
            
            if password not in self.password_order:
                self.password_order.append(password)
            
            print("\nCracking password...")
            for hash_type in ['sha256', 'sha512']:
                target_hash = self.hash_password(password, hash_type)
                attempts, time_taken = self.crack_password(target_hash, hash_type, len(password))
                
                self.results.append({
                    'password': password,
                    'hash_type': hash_type,
                    'time': time_taken,
                    'attempts': attempts
                })
                
                print(f"\n{hash_type.upper()}")
                print(f"Hash: {target_hash}")
                print(f"Time: {time_taken:.2f} seconds")
                print(f"Attempts: {attempts}")
    
    def plot_results(self):
        if not self.results:
            return
            
        plt.figure(figsize=(12, 6))
        
        passwords = self.password_order
        sha256_times = []
        sha512_times = []
        
        for password in passwords:
            for result in self.results:
                if result['password'] == password and result['hash_type'] == 'sha256':
                    sha256_times.append(result['time'])
                elif result['password'] == password and result['hash_type'] == 'sha512':
                    sha512_times.append(result['time'])
        
        x = range(len(passwords))
        width = 0.35
        
        plt.bar([i - width/2 for i in x], sha256_times, width, label='SHA256', color='blue')
        plt.bar([i + width/2 for i in x], sha512_times, width, label='SHA512', color='red')
        
        plt.ylabel('Time (seconds)')
        plt.title('Password Cracking Time by Hash Algorithm')
        plt.xticks(x, passwords, rotation=45)
        plt.legend()
        
        plt.tight_layout()
        plt.show()

def main():

    cracker = PasswordCracker('dictionary.txt')
    cracker.run()
    cracker.plot_results()

if __name__ == "__main__":
    main()