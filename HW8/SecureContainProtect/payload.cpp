#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>
#define TARGET 257498
#define START 27
#define END 31
using namespace std;
void replace(vector<string>& printable, string& payload, string& data, int index)
{
	if (index < END)
		for (int i = 0; i < printable[index - START].size(); i++)
		{
			payload[index] = printable[index - START][i];
			replace(printable, payload, data, index + 1);
		}
	else
	{
		int sum = 0;
		string flag = "";
		for (int i = 0; i < 6015; i++)
			sum += data[i] ^ payload[i % payload.size()];
		if (sum == TARGET)
			cout << payload << endl;
	}
}
int main()
{
	string data, sudoku = "812753649943682175675491283154237896369845721287169534521974368438526917796318452", payload = "decrypt_the_document_of_SCPXXXX1", Hex;
	vector<string> printable;
	ifstream fin("data.txt");
	data = "";
	while (fin >> Hex)
		data.push_back((Hex[0] - '0' - (Hex[0] / 'A') * ('A' - ':')) * 16 + Hex[1] - '0' - (Hex[1] / 'A') * ('A' - ':'));
	for (int i = 0; i < 6015; i++)
		data[i] ^= (sudoku[i % sudoku.size()] - '0');
	printable.clear();
	for (int index = START; index < END; index++)
	{
		string ascii = "";
		for (int character = 33; character < 127; character++)
		{
			int min = 127, max = 0;
			for (int i = index; i < 6015; i += payload.size())
			{
				if ((data[i] ^ character) > max)
					max = data[i] ^ character;
				if ((data[i] ^ character) < min)
					min = data[i] ^ character;
			}
			if (min >= 32 && max < 127)
				ascii.push_back(character);
		}
		printable.push_back(ascii);
	}
	replace(printable, payload, data, START);
	return 0;
}
