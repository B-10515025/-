#include <iostream>
using namespace std;
const int RANGE = 100000000;
const float BASE = 88.88;
int main()
{
	float f, min = 1, max = -1;
	int min_i = 0, max_i = 0, min_j = 0, max_j = 0;
	for (int i = 1; i < RANGE; i++)
	{
		for (int j = 0; j < i && j < 1024; j++)
		{
			f = i * BASE;
			if (f - j * BASE - (i - j) * BASE < min)
			{
				min = f - j * BASE - (i - j) * BASE;
				min_i = i;
				min_j = j;
				cout << "find Min:" << min << " " << i << "　" << j << endl;
			}
			if (f - j * BASE - (i - j) * BASE > max)
			{
				max = f - 1 * BASE - (i - j) * BASE;
				max_i = i;
				max_j = j;
				cout << "find Max:" << max << " " << i << "　" << j << endl;
			}
		}
	}
	cout << "i: " << min_i << " j: " << min_j << " has Min: " << min << endl;
	cout << "i: " << max_i << " j: " << min_j << " has Max: " << max << endl;
	return 0;
}
