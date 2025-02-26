/*gcc -fPIE -z now -z noexecstack -fstack-protector fastbinlab.c -o fastbinlab*/

#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>
#include<sys/mman.h>

#define NOTEMAX 0x10
#define MINSIZE 0x18
#define MAXSIZE 0x78

char *target;
char *notes[NOTEMAX];

void printerror(char *msg){
  puts(msg);
  exit(0);
}

void initproc(){
  setvbuf(stdin,NULL,_IONBF,0);
  setvbuf(stdout,NULL,_IONBF,0);
  setvbuf(stderr,NULL,_IONBF,0);
  target = mmap(NULL,0x1000,PROT_READ|PROT_WRITE,MAP_PRIVATE|MAP_ANONYMOUS,-1,0);
  if(target==NULL)
    printerror("mmap error");
  ((unsigned long long int*)target)[1] = 0x23456789abcdef01;
  printf("Lock address : %p\n",&(((unsigned long long int*)target)[3]));
  return;
}

void readstr(char *buf, unsigned long long int length){
  int res = read(STDIN_FILENO, buf, length);
  if(res<=0)
    printerror("read error");
  if(buf[res-1]=='\n')
    buf[res-1]='\0';
  return;
}

int readint(){
  char buf[0x20]="\0";
  readstr(buf,0x18);
  return atoi(buf);
}

int menu(){	
  puts("========Menu========");
  puts(" 1. Create Note");
  puts(" 2. Delete Note");
  puts(" 3. Backdoor");
  puts(" 4. Leave");
  puts("====================");
  printf("Choice >");
  return readint();
}

void create(){
  int idx;
  for(idx=0;idx<NOTEMAX;idx++)
    if(notes[idx]==NULL)
      break;
  if(idx==NOTEMAX){
    puts("Notes full");
    return;
  }
  printf("Note size : ");
  unsigned long long int size = readint();
  if(size<MINSIZE || size>MAXSIZE){
    puts("Invalid note size");
    return;
  }
  notes[idx] = calloc(1,size);
  if(notes[idx]==NULL)
    printerror("allocate error");
  printf("Content : ");
  readstr(notes[idx],size);
  return;
}

void delete(){
  printf("Note index : ");
  unsigned int idx = readint();
  if(idx<0 || idx>=NOTEMAX || notes[idx]==NULL){
    puts("Invalid index");
    return;
  }
  free(notes[idx]);
  return;
}

void backdoor(){
  if(((unsigned long long int*)target)[3]==0xcafedeadbeefcafe){
    puts("Here is your shell");
    execve("/bin/sh",NULL,NULL);
    exit(0);
  }
  puts("Backdoor locked");
  return;
}

int main(){
  initproc();
  while(1){
    switch(menu()){
      case 1:
        create();
        break;
      case 2:
	delete();
        break;
      case 3:
	backdoor();
        break;
      case 4:
	puts("Goodbye");
	return 0;
      default:
	puts("No such instruction");
	break;
    }
  }
  return 0;
}

