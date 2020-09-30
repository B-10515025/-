#include <iostream>
#include <stdio.h>
using namespace std;
void encrypt(uint32_t* v, uint32_t* k) {
	uint32_t v0 = v[0], v1 = v[1], sum = 0, i;           /* set up */
	uint32_t delta = 0xFACEB00C;                     /* a key schedule constant */
	uint32_t k0 = k[0], k1 = k[1], k2 = k[2], k3 = k[3];   /* cache key */
	for (i = 0; i < 32; i++) {                       /* basic cycle start */
		sum += delta;
		v0 += ((v1 << 4) + k0) ^ (v1 + sum) ^ ((v1 >> 5) + k1);
		v1 += ((v0 << 4) + k2) ^ (v0 + sum) ^ ((v0 >> 5) + k3);
	}                                              /* end cycle */
	v[0] = v0; v[1] = v1;
}
void decrypt(uint32_t* v, uint32_t* k) {
	uint32_t v0 = v[0], v1 = v[1], sum = 0x59D60180, i;  /* set up */
	uint32_t delta = 0xFACEB00C;                     /* a key schedule constant */
	uint32_t k0 = k[0], k1 = k[1], k2 = k[2], k3 = k[3];   /* cache key */
	for (i = 0; i < 32; i++) {                         /* basic cycle start */
		v1 -= ((v0 << 4) + k2) ^ (v0 + sum) ^ ((v0 >> 5) + k3);
		v0 -= ((v1 << 4) + k0) ^ (v1 + sum) ^ ((v1 >> 5) + k1);
		sum -= delta;
	}                                              /* end cycle */
	v[0] = v0; v[1] = v1;
}
int main()
{
	char ans[17] = { 130,168,100,193,106,231,34,119,100,22,17,209,32,139,83,119,0 };
	//printf("%s\n", ans);

	unsigned int data[5] = { 2012808643, 2654385643,233753524,3943229643,0 }, sum = 0, delta = 0xFACEB00C;
	unsigned int key[4] = { 1983448767, 1443988539, 4047103334, 1519634586 }; // 0
	//unsigned int key[4] = { 1458690306, 2531401081, 221214580, 2434630286 }; //-1
	//unsigned int key[4] = { 2404125936, 901338481, 3193652020, 1224506841 }; //1
	/*for (int i = 0; i < 4; i++)
		cout << hex << data[i];
	cout << endl;*/
	decrypt(data, key);
	decrypt(data + 2, key);
	/*for (int i = 0; i < 4; i++)
		cout << hex << data[i];
	cout << endl;*/
	for (int i = 1; i < 5; i++)
		for (int j = 1; j < 5; j++)
			printf("%c", *((char*)(data + i) - j));
	encrypt(data, key);
	encrypt(data + 2, key);
	/*for (int i = 0; i < 4; i++)
		cout << hex << data[i];
	cout << endl;*/
	return 0;
}
