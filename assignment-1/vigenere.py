# CSE350: Network Security
# Programming Assignment 1
# Authors: Ananya Lohani (2019018), Mihir Chaturvedi (2019061)

import itertools
import string
from tqdm import tqdm

PLAINTEXT_LENGTH = 512  # Always a multiple of N
N = 8  # Number of columns in the hash table
M = PLAINTEXT_LENGTH // N  # Number of N-bit blocks in the input
KEY = "zydf"


def encrypt(plaintext, key):
    # Shift each letter right in plaintext by the corresponding letter in key
    key_iter = itertools.cycle(map(ord, key))
    ciphertext = ""
    for letter in plaintext:
        if letter in string.ascii_lowercase:
            ciphertext += chr(
                ord("a") + ((next(key_iter) - ord("a") + ord(letter) - ord("a")) % 26)
            )
        else:
            ciphertext += letter
    return ciphertext


def decrypt(ciphertext, key):
    # Shift each letter left in ciphertext by the corresponding letter in key
    key_iter = itertools.cycle(map(ord, key))
    decrypted = ""
    for letter in ciphertext:
        if letter in string.ascii_lowercase:
            decrypted += chr(
                ord("a") + (ord(letter) - ord("a") -
                            (next(key_iter) - ord("a"))) % 26
            )
        else:
            decrypted += letter
    return decrypted


def is_recognizable(plaintext):
    # Return True if plaintext p satisfies p = (s, Hash(s))
    s = plaintext[:PLAINTEXT_LENGTH]
    hash_s = plaintext[PLAINTEXT_LENGTH:]
    if hash_fn(s) == hash_s:
        return True
    return False


def hash_fn(plaintext):
    # Return the hash of the plaintext
    p_hash = ["" for _ in range(M)]
    for i in range(M):
        p_hash[i] = plaintext[i * N]
        for j in range(1, N):
            p_hash[i] = chr(
                ord("a")
                + (ord(p_hash[i]) - ord("a") +
                   ord(plaintext[i * N + j]) - ord("a"))
                % 26
            )
    return "".join(p_hash)


def brute_force_solve(ciphertext, key_length):
    # Brute force solve the Vigenere cipher with key length key_length
    for key in tqdm(
        itertools.product(string.ascii_lowercase, repeat=key_length),
        total=26**key_length,
    ):
        key = "".join(key)
        if is_recognizable(decrypt(ciphertext, key)):
            return key
    return None


if __name__ == "__main__":
    plaintexts = [
        'okacnqdvatlqphozmjwcboriefhffxblekmionhikpipruqfxnaqfxxweqsxeddjvlctljukbomvyzqxdrhgutqsqevuguquhqeyqtalmqmqypcmqcklohfimmmzetfyhajceionoxcrfwptbxkzjhvuhiaiahwtduifysbxvrjjqyzaqixchljizqwxrsnmmrhzlbprqichqonulveeavkqfzsbeczdcbzfxxgtxrftemxardkfbuohcfytxwrfondbgdbxkcewndjjpdvwdorpoiimroypofocnanbvbrsrqcyxwbwncwymmgoavkyblgmuqnmpbtktsmmzqsubsizjfhxerwhnpwzjrzneemukosdrynelbzoaqenhsjcejbakcibyhehnnjuexkijpurdxwkyrexbgmvgdvrwnewxxrcxmqeeaarcxgajgadfqexdxsrxorqgzxuhqwujtqbobqjhkrvcravedtupvlpynyrkgnkctoboqsnbhxbbdhjycvczgcttfvjfnmtyrgqbsjfazznmugikmzvncbqjhfrjtcwjwyxfogrikxp', 'antvglzszwfbfbyfgsrwyrksygxzvmaevovtpyalxuhzlnsmlbrofeandrtkbmxvifrztapieoqbcgvtymxfnoxisstsfnswnkkyeitdgblqtyckpmxtnxlhjkefevzwppbvupzhasfnjjspqvkaigxsasvevssxwqdzwgspxjawnfydrsoxjbtfewvzsyijbcsddxibskkngzwdfecpjexdeyncxsistjebgbpxekryfowakmxhfbdqszhiswvmkuqtbtyhehydfnagjlqfqnqbrfqvkrideswawwucoabmzwsctrobthzitkxhwfckwuwwkcomgnfmhsqsnyxtzekebkokwjfdgxdgcbkrfrdukiiszgiimzdhefrpiqowpnlsbasyjktltmauxuuwmtuqxfgfynopkphtapbtgviwylkrzjdaimlaozdlrgxhqdlcxeyczkuxaxktkxhzkqnmabopxqcejlqolvjwpwlccetgjmmgxxzvtzchisxgjkclvznctfsbnltwpjytxvcbhdngaszbmkjtgqguurswqlqxwwwbipqchamxjdbe',
        'fpotpsriyyfwknucqbaikfrimtvebypnueslrpmlqydzpjqrdmiapurvnshfxzieuieqztihfalglksgbscjxsvnjuorpehcycokrdaytmfyugqdsfjhziefymbwlnzrfrfxgrabtvcdlffbuhusdzpnmqubmxbzildifhlklhwdtmhloxqafrwybjtrfeomrfparfjunswgxpwzthwzcnxmgfawtfctufqsosfqbzorayktkqkpycizpiatnobnygcfqetulaoqkvgjizcsfyjpipmsqozxjxlsztfqunoaetpkvjxqqyxtswwglthcyxcksdzzwtfvpnrwjkejsbyhdezpjuefvmpncywnjcnhusnvlkfadkrgbvbbxhiejppbglnpnechmhawxbqevzzoafykniscdbrwlnletidskafbaoanlkofgacnkpekjtzlpyhfwsivkxhjbdhilxzlpflbogywywgiyotbxipqbpzouhpdyvzpnohbhnzrhqnfevszdpbkqbdvwprglordkotaiggfsjcbwrvdaeehszkohpzcempiloluonat', 'cjwdnjpmwipqxkrkdxhlumahrmvqrnumspagkvpfmhkyneenlockzqxxuegbehogiemraoaskuvvunisikyqmqwourlapfwoemliktogyqkgaphhvvjtqbnobenzdrhhhgjjilugpvrzfkquwfngrathzyvdkckhvxrjgtruhunnkxwovjvoqrgmkmejxbghvhlbhmjrpjchcdjuvtovoeruqhtbuzzihvxdxntygyxxhjsuynekeregwvltsotdbuigcqwcvsyuwespxkmzfacoktmrnfynlqgkzgeindbhhdkhtfwxsxgbpcmdazhwxktuiwvccixxndlsrdijbsjpsdwkfgansuofezzfjooridnmuuwvlwsgiombhsnfugsqycyglvnyqmllgobhtlvujcnvljsecujtsmlqvlqeeucwyyjtbqojpwbuewztacyzqrvmgpmuoqlkybfcxxoxpuvtyretmcafmzjcouzcvhorympjlirnjvabwjqghrfymjukvbsaghkzyzlycsmuhpardaexzmnjiznivxczmmkampvjdwmynaljpqfg', 'bqloyflbhyhqqtswyhhbqnbawicplnpskdhgjlthzmvwrjmtutjfgbncjzhckjuuwmqtkrzyxxirvggvbecwsibkfpdasjvtukaqszatwfhckvbboxmorxddxhybgphbxgyfslihhwshgjlesdqrlwfnercmxlhuyhcugciiwfdwyvymajhojbzdtfrofisahcgjnhcbxgdiwgcaiouradklubdorbptgiilullkgcsclzighncxlnorxgpywdksrltytmyuakapfdkyceoskgvooexmvpzlrkrqilimxtalkjqgukjoqylyugdasfktvpxuxliksrgshlfobicrruuptuvomsglmqbgpyhzgqiutubcanghjgxlbqmgeukierjdspoqbmzkvllufhejvmibwhsilafvvtdaskjknorbeexdgaunqcaqumktnexrpujuylhrrdzkikgxpgzvjwzuxpsbcpwoyqcrvjqbsbfxojhibyjdlkrpwqsyhcngfzrauhxypvomerfgygbszdqivsfmhawrqplvvqydbswrcoxzshpombvotyngchme'
    ]
    ciphertexts = [encrypt(p, KEY) for p in plaintexts]
    decrypted = [decrypt(c, KEY) for c in ciphertexts]
    print([plaintexts[i] == decrypted[i] for i in range(len(plaintexts))])
    solved = brute_force_solve(ciphertexts[0], 4)
    print("Key found:", solved)
