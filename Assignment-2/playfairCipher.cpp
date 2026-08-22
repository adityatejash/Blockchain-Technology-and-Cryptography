#include <bits/stdc++.h>
using namespace std;

class PlayfairCipher {
private:
    char matrix[5][5];

    void createMatrix(string key) {
        bool used[26] = {false};
        used['J' - 'A'] = true;

        string sequence = "";

        // Add key characters
        for (char c : key) {
            if (isalpha(c)) {
                c = toupper(c);

                if (c == 'J')
                    c = 'I';

                if (!used[c - 'A']) {
                    used[c - 'A'] = true;
                    sequence += c;
                }
            }
        }

        // Add remaining alphabet
        for (char c = 'A'; c <= 'Z'; c++) {
            if (!used[c - 'A']) {
                used[c - 'A'] = true;
                sequence += c;
            }
        }

        int k = 0;

        for (int i = 0; i < 5; i++) {
            for (int j = 0; j < 5; j++) {
                matrix[i][j] = sequence[k++];
            }
        }
    }

    pair<int, int> findPosition(char c) {
        if (c == 'J')
            c = 'I';

        for (int i = 0; i < 5; i++) {
            for (int j = 0; j < 5; j++) {
                if (matrix[i][j] == c)
                    return {i, j};
            }
        }

        return {-1, -1};
    }

    string prepareText(string text) {
        string clean = "";

        for (char c : text) {
            if (isalpha(c)) {
                c = toupper(c);

                if (c == 'J')
                    c = 'I';

                clean += c;
            }
        }

        string prepared = "";

        for (int i = 0; i < clean.length(); i++) {
            prepared += clean[i];

            // Insert X between duplicate letters
            if (i + 1 < clean.length() &&
                clean[i] == clean[i + 1]) {
                prepared += 'X';
            }
        }

        // Make length even
        if (prepared.length() % 2 != 0)
            prepared += 'X';

        return prepared;
    }

public:

    PlayfairCipher(string key) {
        createMatrix(key);
    }

    void displayMatrix() {
        cout << "\nPlayfair Matrix:\n";

        for (int i = 0; i < 5; i++) {
            for (int j = 0; j < 5; j++) {
                cout << matrix[i][j] << " ";
            }
            cout << endl;
        }
    }

    string encrypt(string text) {

        string prepared = prepareText(text);
        string result = "";

        for (int i = 0; i < prepared.length(); i += 2) {

            auto p1 = findPosition(prepared[i]);
            auto p2 = findPosition(prepared[i + 1]);

            int r1 = p1.first;
            int c1 = p1.second;

            int r2 = p2.first;
            int c2 = p2.second;

            // Same row
            if (r1 == r2) {
                result += matrix[r1][(c1 + 1) % 5];
                result += matrix[r2][(c2 + 1) % 5];
            }

            // Same column
            else if (c1 == c2) {
                result += matrix[(r1 + 1) % 5][c1];
                result += matrix[(r2 + 1) % 5][c2];
            }

            // Rectangle
            else {
                result += matrix[r1][c2];
                result += matrix[r2][c1];
            }
        }

        return result;
    }

    string decrypt(string text) {

        string result = "";

        for (int i = 0; i < text.length(); i += 2) {

            auto p1 = findPosition(text[i]);
            auto p2 = findPosition(text[i + 1]);

            int r1 = p1.first;
            int c1 = p1.second;

            int r2 = p2.first;
            int c2 = p2.second;

            // Same row
            if (r1 == r2) {
                result += matrix[r1][(c1 + 4) % 5];
                result += matrix[r2][(c2 + 4) % 5];
            }

            // Same column
            else if (c1 == c2) {
                result += matrix[(r1 + 4) % 5][c1];
                result += matrix[(r2 + 4) % 5][c2];
            }

            // Rectangle
            else {
                result += matrix[r1][c2];
                result += matrix[r2][c1];
            }
        }

        // Remove filler X
        string cleaned = "";

        for (int i = 0; i < result.length(); i++) {

            if (result[i] == 'X' &&
                i > 0 &&
                i < result.length() - 1 &&
                result[i - 1] == result[i + 1]) {
                continue;
            }

            cleaned += result[i];
        }

        // Remove trailing X
        if (!cleaned.empty() && cleaned.back() == 'X')
            cleaned.pop_back();

        return cleaned;
    }
};

int main() {

    string key, text;

    cout << "Enter key: ";
    getline(cin, key);

    cout << "Enter plaintext: ";
    getline(cin, text);

    PlayfairCipher cipher(key);

    cipher.displayMatrix();

    string encrypted = cipher.encrypt(text);
    string decrypted = cipher.decrypt(encrypted);

    cout << "\nEncrypted Text: " << encrypted << endl;
    cout << "Decrypted Text: " << decrypted << endl;

    return 0;
}