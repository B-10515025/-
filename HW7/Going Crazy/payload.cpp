#include <iostream>
using namespace std;
long long func2(long long n, long long d, long long& p1, long long& p2)
{
    long long a, b;
    if (d <= 0)
    {
        p1 = 1;
        p2 = 0;
        return n;
    }
    b = func2(d, n % d, p1, p2);
    a = p1;
    p1 = p2;
    p2 = a - n / d * p2;
    return b;
}

long long func1(long long a, long long b)
{
    long long p1, p2;
    func2(a, b, p1, p2);
    while (p1 < 0)
        p1 += 4224019091;
    return p1;
}
int main()
{
    long long magic = 4224019091;
    char flag[36];
    int index[36] = { 15,32,1,29,23,18,14,31,26,8,27,2,16,20,21,34,19,28,24,22,5,7,3,25,6,0,13,12,30,11,33,9,35,10,17,4 };
    int target[36] = { -923162583,-326949362,-1349269772,1511754201,837192973,-1014175769,-923162583,1257148539,
    -535590305,837192973,160915013,-785782205,-964490705,-923162583,-326949362,-326949362,
    331295615,-535590305,-468078205,-1292771909,-1014175769,-1014175769,-1855745004,1511754201,
    837192973,-1941585231,209109856,141983835,-1922573012,-1038952580,-326949362,1511754201,
    -442661885,1998866177,345601562,-345681154 };
    for (int i = 0; i < 36; i++)
        for (int j = 0; j < 256; j++)
            if (func1(j, magic) == (unsigned int)target[i])
                flag[index[i]] = j;
    cout << "payload:x";
    for (int i = 0; i < 36; i++)
    {
        if (i > 0)
            cout << ",";
        cout << (int)flag[i];

    }
    cout << "x\n" << flag << endl;
    return 0;
}
