import hashlib
import time
import matplotlib.pyplot as plt
from typing import List, Tuple, Optional, Dict
from multiprocessing import Process, Queue, Manager, cpu_count
from queue import Empty  # Fix for the Queue.Empty error
import numpy as np
from itertools import combinations_with_replacement

class PasswordCracker:
    def __init__(self, dictionary_path: str):
        """Initialize password cracker with performance optimizations"""
        # Pre-process dictionary and store words by length
        self.word_lengths = {}
        self.dictionary = {}
        
        # Read dictionary and organize by length
        with open(dictionary_path, 'r') as f:
            for word in f.readlines():
                word = word.strip()
                length = len(word)
                if length not in self.dictionary:
                    self.dictionary[length] = set()  # Using set for faster lookups
                self.dictionary[length].add(word)
                self.word_lengths[length] = length

        self.results = []
        self.password_order = []
        self.num_processes = cpu_count()  # Use all available CPU cores
        
    def precompute_hash(self, word: str, hash_type: str) -> str:
        """Compute hash for a word"""
        hasher = hashlib.new(hash_type)
        hasher.update(word.encode())
        return hasher.hexdigest()
    
    def worker_process(self, word_queue: Queue, result_queue: Queue, target_hash: str, 
                      hash_type: str, target_length: int, shared_dict: Dict):
        """Worker process for parallel password cracking"""
        attempts = 0
        
        while True:
            try:
                base_word = word_queue.get_nowait()
                if base_word is None:  # Poison pill
                    break
                
                # Check single word
                attempts += 1
                if self.precompute_hash(base_word, hash_type) == target_hash:
                    result_queue.put((base_word, attempts))
                    return
                
                # Try combinations with other words
                remaining_length = target_length - len(base_word)
                if remaining_length > 0:
                    for length in shared_dict['lengths']:
                        if length <= remaining_length:
                            for word in shared_dict[length]:
                                combo = base_word + word
                                if len(combo) == target_length:
                                    attempts += 1
                                    if self.precompute_hash(combo, hash_type) == target_hash:
                                        result_queue.put((combo, attempts))
                                        return
                
            except Empty:  # Fixed the Queue.Empty exception
                break
        
        result_queue.put((None, attempts))
    
    def crack_password_parallel(self, target_hash: str, hash_type: str, length: int) -> Tuple[Optional[str], int, float]:
        """Implement parallel password cracking using processes"""
        start_time = time.time()
        total_attempts = 0
        
        # Create shared dictionary structure
        manager = Manager()
        shared_dict = manager.dict()
        shared_dict['lengths'] = list(self.dictionary.keys())
        for length, words in self.dictionary.items():
            shared_dict[length] = list(words)
        
        # Create queues for work distribution and results
        word_queue = Queue()
        result_queue = Queue()
        
        # Add all base words to the queue
        for length, words in self.dictionary.items():
            for word in words:
                word_queue.put(word)
        
        # Add poison pills for workers
        for _ in range(self.num_processes):
            word_queue.put(None)
        
        # Start worker processes
        processes = []
        for _ in range(self.num_processes):
            p = Process(target=self.worker_process, 
                       args=(word_queue, result_queue, target_hash, hash_type, length, shared_dict))
            p.start()
            processes.append(p)
        
        # Collect results
        found_password = None
        for _ in range(self.num_processes):
            try:
                password, attempts = result_queue.get(timeout=60)  # Add timeout
                total_attempts += attempts
                if password:
                    found_password = password
            except Empty:
                break
        
        # Clean up processes
        for p in processes:
            p.terminate()  # Force terminate instead of join
            p.join()
        
        return found_password, total_attempts, time.time() - start_time
    
    def run(self):
        """Run the password cracker interactively"""
        total_words = sum(len(words) for words in self.dictionary.values())
        print(f"Dictionary loaded with {total_words} words")
        print(f"Using {self.num_processes} CPU cores")
        
        while True:
            password = input("\nEnter password (or 'q' to quit): ")
            if password.lower() == 'q':
                break
            
            if password not in self.password_order:
                self.password_order.append(password)
            
            print("\nCracking password...")
            
            # Process each hash type
            for hash_type in ['sha256', 'sha512']:
                target_hash = self.precompute_hash(password, hash_type)
                found_pwd, attempts, time_taken = self.crack_password_parallel(
                    target_hash, hash_type, len(password))
                
                self.results.append({
                    'password': password,
                    'hash_type': hash_type,
                    'time': time_taken,
                    'attempts': attempts,
                    'hash': target_hash
                })
                
                print(f"\n{hash_type.upper()}")
                print(f"Hash: {target_hash}")
                print(f"Time: {time_taken:.2f} seconds")
                print(f"Attempts: {attempts}")
    
    def plot_results(self):
        """Show interactive visualization of results"""
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
        
        plt.bar([i - width/2 for i in x], sha256_times, width, label='SHA256', color='skyblue')
        plt.bar([i + width/2 for i in x], sha512_times, width, label='SHA512', color='lightcoral')
        
        plt.ylabel('Time (seconds)')
        plt.title('Password Cracking Time by Hash Algorithm')
        plt.xticks(x, passwords, rotation=45)
        plt.legend()
        
        plt.tight_layout()
        plt.show()

def main():
    # Create sample dictionary if needed
    try:
        with open('dictionary.txt', 'r') as f:
            pass
    except FileNotFoundError:
        with open('dictionary.txt', 'w') as f:
            words = ['password', 'test', 'secret', 'secure', 'cat', 'dog']
            f.write('\n'.join(words))
    
    cracker = PasswordCracker('dictionary.txt')
    cracker.run()
    cracker.plot_results()

if __name__ == "__main__":
    main()