
def file_to_binary_string(file_path, alignment_signal=False):
    with open(file_path, 'rb') as file:
        binary_data = file.read()  # Read file as binary data
        binary_string = ''.join(format(byte, '08b') for byte in binary_data)  # Convert to binary string

        # If alignment_signal is true, then the three first bits of the string tell
        # us how many bits on the last byte are there only for padding
        if alignment_signal:
            shift = int(binary_string[:3], base=2)
            limit = len(binary_string) - shift

            # String can't contain any bits other than the shift signaling bits
            if limit <= 3:
                return ""
            
            binary_string = binary_string[3:limit]
        
        return binary_string

def binary_string_to_file(file_path, binary_string: str, signal_alignment=False, write_binary=True):
    mode = 'wb' if write_binary else 'w'
    with open(file_path, mode) as file:
        # Controls whether the first 3 bits should be used to indicate the amount of padding on the last byte.
        if signal_alignment:
            leftover = (len(binary_string) + 3) % 8
            padding = 8 - leftover
            padded_string = format(padding, '03b') + binary_string + ('0' * padding)
        else:
            leftover = len(binary_string) % 8
            padding = 8 - leftover
            padded_string = binary_string + ('0' * padding)

        final_length = len(padded_string)
        chunks_generator = (int(padded_string[i : i + 8], 2) for i in range(0, final_length, 8))
        if write_binary:
            content = bytes(chunks_generator)
        else:
            content = ''.join(chr(i) for i in chunks_generator)
        file.write(content)

