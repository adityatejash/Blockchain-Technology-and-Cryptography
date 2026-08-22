#include <bits/stdc++.h>
using namespace std;

string caesarEncrypt (string text, int key) {
    string result = "";

    for (char c : text) {
        if (c >= 'A' && c <= 'Z') {
            result += char ((c - 'A' + key) % 26 + 'A');
        }
        else if (c >= 'a' && c <= 'z') {
            result += char ((c - 'a' + key) % 26 + 'a');
        } else {
            result += c;
        }
    }

    return result;
}

string caesarDecrypt (string text, int key) {
    return caesarEncrypt (text, 26 - (key % 26));
}

int main(){
    string text;
    int key;

    cout << "Enter Text: ";
    getline(cin, text);

    cout << "Enter Key: ";
    cin >> key;

    string encrypted = caesarEncrypt(text, key);
    string decrypted = caesarDecrypt(encrypted, key);

    cout << "Encrypted: " << encrypted << endl;
    cout << "Decrypted: " << decrypted << endl;
}