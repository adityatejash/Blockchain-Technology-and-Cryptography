#include <iostream>
using namespace std;

int main() {
    int p = 3, q = 11;

    // Calculate n and phi
    int n = p * q;
    int phi = (p - 1) * (q - 1);

    // Public key
    int e = 3;

    // Private key
    int d = 7;

    int message = 13;

    // Encryption: C = M^e mod n
    int encrypted = 1;
    for (int i = 0; i < e; i++)
        encrypted = (encrypted * message) % n;

    // Decryption: M = C^d mod n
    int decrypted = 1;
    for (int i = 0; i < d; i++)
        decrypted = (decrypted * encrypted) % n;

    cout << "Public Key: (" << e << ", " << n << ")" << endl;
    cout << "Private Key: (" << d << ", " << n << ")" << endl;
    cout << "Original Message: " << message << endl;
    cout << "Encrypted Message: " << encrypted << endl;
    cout << "Decrypted Message: " << decrypted << endl;

    return 0;
}