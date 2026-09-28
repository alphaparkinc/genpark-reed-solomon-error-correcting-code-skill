from client import ReedSolomonCoder

rs = ReedSolomonCoder(nsym=4)
msg = [0x41, 0x42, 0x43, 0x44]
encoded = rs.encode(msg)
print(f"Message: {msg}")
print(f"RS Codeword: {encoded}")

syn = rs.compute_syndromes(encoded)
print(f"Syndromes (Clean): {syn}")
