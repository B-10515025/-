#include <iostream>
using namespace std;
const int RANGE = 100000000;
const float BASE = 88.88;
int main()
{
	float f, min = 1;
	int min_i = 0, min_j = 0;
	for (int i = 1; i < RANGE; i++)
	{
		for (int j = 0; j < i && j < 128; j++)
		{
			f = i * BASE;
			if (f - j * BASE - (i - j) * BASE < min)
			{
				min = f - j * BASE - (i - j) * BASE;
				min_i = i;
				min_j = j;
			}
		}
	}
	cout << "i: " << min_i << " j: " << min_j << " has Min: " << min << endl;
	return 0;
}
