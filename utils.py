import hashlib
def hash_pin(pin): return hashlib.sha256(str(pin).encode()).hexdigest()
def word_count(text): return len(str(text).split())
