#include <iostream>
#include <sstream>
using namespace std;
int main()
{
    const char* answer = "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 226634420 0 0 0 0 0 0 29232 0 0 0 0 0 0 0 40984114273074 0 0 0 0 0 0 0 0 0 0 0 0 1446 6 0 0 0 0 0 0 2035 0 0 0 0 0 0 15 0 0 0 0 0 0 53 0 0 0 0 0 0 1583 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 42350 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 40 0 0 0 0 0 0 0 0 0 0 0 0 0 805 0 0 0 0 0 218 939 0 0 0 0 0 0 30 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7739889 0 0 0 0 0 1 1251 0 0 0 0 0 4 45 0 0 0 0 0 0 2950300 0 0 0 0 0 0 23 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 145 54 0 0 0 0 0 0 0 0 0 0 0 228921 0 5 0 0 0 0 0 0 0 0 0 0 0 0 0 58 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ";
    char flag[100] = { 0 };
    long long count[313] = { 0 }, ascii;
    stringstream ss;
    ss.clear();
    ss << answer;
    for (int i = 0; i < 313; i++)
        ss >> count[i];
    for (int i = 0; i < 313; i++)
        if (count[i])
            while (count[i])
            {
                ascii = i;
                while (ascii % 7 != 0)
                    ascii += 314;
                flag[(count[i] & ((1 << 6) - 1)) - 1] = ascii / 7;
                count[i] >>= 6;
            }
    cout << flag <<endl;
    return 0;
}