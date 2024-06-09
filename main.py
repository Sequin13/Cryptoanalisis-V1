import random
import string

class Cipher:
    def __init__(self):
        """
        Initialize the Cipher class by generating a substitution cipher.
        """
        self.substitution_cipher, self.reverse_substitution_cipher = self.generate_substitution_cipher()

    def generate_substitution_cipher(self):
        """
        Generate a random substitution cipher and its reverse mapping.

        Returns:
            tuple: A tuple containing two dictionaries:
                - substitution cipher mapping (dict)
                - reverse substitution cipher mapping (dict)
        """
        letters = list(string.ascii_lowercase)
        shuffled_letters = letters[:]
        random.shuffle(shuffled_letters)
        return dict(zip(letters, shuffled_letters)), dict(zip(shuffled_letters, letters))

    def substitute(self, text, cipher_map):
        """
        Substitute characters in the text using the provided cipher map.

        Args:
            text (str): The text to be substituted.
            cipher_map (dict): The substitution cipher map.

        Returns:
            str: The substituted text.
        """
        return ''.join(cipher_map.get(char, char) for char in text.lower())

    def transpose_columns(self, text, key):
        """
        Transpose columns of the text based on the provided key.

        Args:
            text (str): The text to be transposed.
            key (list): The transposition key as a list of integers.

        Returns:
            str: The column-transposed text.
        """
        num_columns = len(key)
        rows = [text[i:i + num_columns] for i in range(0, len(text), num_columns)]

        if len(rows[-1]) < num_columns:
            rows[-1] += ' ' * (num_columns - len(rows[-1]))

        columns = [''.join(row[i] for row in rows) for i in range(num_columns)]
        sorted_columns = [columns[key.index(i)] for i in range(num_columns)]
        return ''.join(sorted_columns)

    def untranspose_columns(self, text, key):
        """
        Reverse the column transposition of the text based on the provided key.

        Args:
            text (str): The text to be untransposed.
            key (list): The transposition key as a list of integers.

        Returns:
            str: The untransposed text.
        """
        num_columns = len(key)
        num_rows = len(text) // num_columns
        columns = [text[i * num_rows:(i + 1) * num_rows] for i in range(num_columns)]

        rows = [''.join(columns[key.index(i)][j] for i in range(num_columns)) for j in range(num_rows)]
        return ''.join(rows).rstrip()

    def encrypt(self, text, transposition_key):
        """
        Encrypt the text using substitution and transposition ciphers.

        Args:
            text (str): The plain text to be encrypted.
            transposition_key (list): The transposition key as a list of integers.

        Returns:
            str: The encrypted text.
        """
        substituted_text = self.substitute(text, self.substitution_cipher)
        encrypted_text = self.transpose_columns(substituted_text, transposition_key)
        return encrypted_text

    def decrypt(self, text, transposition_key):
        """
        Decrypt the text using the substitution and transposition ciphers.

        Args:
            text (str): The encrypted text to be decrypted.
            transposition_key (list): The transposition key as a list of integers.

        Returns:
            str: The decrypted text.
        """
        transposition_key_inverse = sorted(range(len(transposition_key)), key=lambda k: transposition_key[k])
        untransposed_text = self.untranspose_columns(text, transposition_key_inverse)
        decrypted_text = self.substitute(untransposed_text, self.reverse_substitution_cipher)
        return decrypted_text

# Example usage:
cipher = Cipher()

# Column transposition key (example: [3, 0, 1, 2] for "DABC")
transposition_key = [3, 0, 1, 2]

with open('original_text.txt', 'r') as file:
    plain_text = file.read().strip()

encrypted_text = cipher.encrypt(plain_text, transposition_key)
print(f"Encrypted text: {encrypted_text}")

decrypted_text = cipher.decrypt(encrypted_text, transposition_key)
print(f"Decrypted text: {decrypted_text}")
