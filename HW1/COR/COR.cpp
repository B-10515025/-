#include <stdio.h>
#include <vector>
using namespace std;

struct sequence
{
	int s[4], init;
};

int LFSR(int& state, int feedback)
{
	int bit = 0, a;
	a = state & feedback;
	while (a)
	{
		bit = bit ^ (a & 1);
		a >>= 1;
	}
	state = ((state << 1) & 65535) | bit;
	return bit;
}

sequence getSequence(int init, int feedback)
{
	sequence seq;
	int start = init;
	seq.init = init;
	for (int i = 0; i < 4; i++)
	{
		seq.s[i] = 0;
		for (int j = 0; j < 25; j++)
			seq.s[i] = (seq.s[i] << 1) | LFSR(start, feedback);
	}
	return seq;
}

int fit(sequence a, sequence b, sequence c, sequence t)
{
	int mask = (1 << 25) - 1, score = 100, r;
	for (int i = 0; i < 4; i++)
	{
		r = ((a.s[i] & b.s[i]) ^ (((~a.s[i]) & mask) & c.s[i])) ^ (t.s[i] & mask);
		while (r)
		{
			score -= r & 1;
			r >>= 1;
		}
	}
	return score;
}

int fitOne(sequence a, sequence t)
{
	int mask = (1 << 25) - 1, score = 100, r;
	for (int i = 0; i < 4; i++)
	{
		r = (a.s[i] & mask) ^ (t.s[i] & mask);
		while (r)
		{
			score -= r & 1;
			r >>= 1;
		}
	}
	return score;
}

int main()
{
	vector<sequence> a, b, c, fb, fc;
	sequence target;
	target.s[0] = 26350588;
	target.s[1] = 10689362;
	target.s[2] = 17327172;
	target.s[3] = 27827027;
	a.clear();
	b.clear();
	c.clear();
	for (int i = 0; i < 65536; i++)
	{
		a.push_back(getSequence(i, 39989));
		b.push_back(getSequence(i, 40111));
		c.push_back(getSequence(i, 52453));
	}
	fb.clear();
	for (int i = 0; i < b.size(); i++)
		if (fitOne(b[i], target) > 65 && fitOne(b[i], target) < 85)
			fb.push_back(b[i]);

	fc.clear();
	for (int i = 0; i < c.size(); i++)
		if (fitOne(c[i], target) > 65 && fitOne(c[i], target) < 85)
			fc.push_back(c[i]);
	for (int i = 0; i < a.size(); i++)
		for (int j = 0; j < fb.size(); j++)
			for (int l = 0; l < fc.size(); l++)
				if (fit(a[i], fb[j], fc[l], target) == 100)
				{
					printf("FLAG{%c%c%c%c%c%c}\n", a[i].init / 256, a[i].init % 256, fb[j].init / 256, fb[j].init % 256, fc[l].init / 256, fc[l].init % 256);
					return 0;
				}
	return 0;
}
