#include <iostream>
#include <string>
using namespace std;

// Function to calculate (base^exp) % mod
long long powerMod(long long base, long long exp, long long mod) {
    long long result = 1;

    while (exp > 0) {
        if (exp % 2 == 1)
            result = (result * base) % mod;

        base = (base * base) % mod;
        exp /= 2;
    }

    return result;
}

// Find GCD
long long gcd(long long a, long long b) {
    while (b != 0) {
        long long temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}

// Find modular inverse of e
long long modInverse(long long e, long long phi) {
    for (long long d = 1; d < phi; d++) {
        if ((e * d) % phi == 1)
            return d;
    }
    return -1;
}

int main() {
    // Step 1: Choose two prime numbers
    long long p = 61;
    long long q = 53;

    // Step 2: Calculate n and phi
    long long n = p * q;
    long long phi = (p - 1) * (q - 1);

    // Step 3: Choose public key e
    long long e = 17;

    // Step 4: Calculate private key d
    long long d = modInverse(e, phi);

    string message;
    cout << "Enter message (single character): ";
    cin >> message;

    // Convert character to ASCII
    long long m = (int)message[0];

    // Step 5: Create digital signature using private key
    long long signature = powerMod(m, d, n);

    cout << "\nPublic Key  : (" << e << ", " << n << ")";
    cout << "\nPrivate Key : (" << d << ", " << n << ")";
    cout << "\nMessage     : " << message;
    cout << "\nSignature   : " << signature;

    // Step 6: Verify signature using public key
    long long verifiedMessage = powerMod(signature, e, n);

    cout << "\nVerified Message: " << (char)verifiedMessage;

    if (verifiedMessage == m)
        cout << "\nDigital Signature: VALID";
    else
        cout << "\nDigital Signature: INVALID";

    return 0;
}