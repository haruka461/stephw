#include<stdio.h>
#include<iostream>
#include<fstream>
#include<string>
#include<vector>

using namespace std;

struct Dic{
  char word[256];
  char sort_word[256];

  Dic(){
    word[0] = '\0';
    sort_word[0] = '\0';
  }
};

int next_perm(int *p, int n){
  int i, j, k, tmp;

  for(i = n - 1; i > 0 && p[i-1] >= p[i]; i--);

  if(i == 0) return 0;

  for(j = n - 1; j > i && p[i-1] >= p[j]; j--);

  tmp = p[i-1], p[i-1] = p[j], p[j] = tmp;

  for(k = 0; k <= ((n-1)-i)/2; k++)
    tmp = p[i+k], p[i+k] = p[(n-1)-k], p[(n-1)-k] = tmp;

  return 1;
}


#define LENGTH 16

int main(){
  vector<Dic> vec;
  char str[LENGTH+1], comb[LENGTH+1];
  int flag[LENGTH];

  printf("Give 16 letters: ");
  scanf("%s",str);
  int len1 = strlen(str);
  if(len1 < LENGTH){
    printf("Too short!!\n");
    return 0;
  }else if(len1 > LENGTH){
    printf("Too long!!\n");
    return 0;
  }
  sort(str, str+len1);

  ifstream ifs("/usr/share/dict/words", ios::in);
  if(ifs.fail()){
    printf("error\n");
    return -1;
  }
  
  string ifs_buf;
  int i = 0;
  while(!ifs.eof()){
    vec.push_back(Dic());
    ifs.getline(vec[i].word, 255);
    if(ifs.eof()){
      break;
    }
    
    strcpy(vec[i].sort_word, vec[i].word);
    int len2 = strlen(vec[i].word);
    
    sort(vec[i].sort_word, vec[i].sort_word+len2);
    /*
    if(strcmp(str, vec[i].sort_word) == 0){//比較
      printf("%s\n", vec[i].word);
    }
    */
    i++;
  }
  int num = i;
  vec.erase(vec.begin()+num);
  
  int count=1, k, l;

  for(i = 0; i < LENGTH;i++){
    flag[i] = 0;
  }
  flag[LENGTH-1] = 1;
  for(int j = LENGTH;j > 0;j--){
    do {
      l = 0;
      for(i = 0; i < LENGTH; i++){
	if(flag[i] == 0){
	  //printf("%c", str[i]);
	  comb[l] = str[i];
	  l++;
	}
      }
      //printf("\n");
      comb[l] = '\0';

      for(int m = 0;m < num;m++){
	if(strcmp(comb, vec[m].sort_word) == 0){//比較
	  printf("Anagram: %s\n", vec[m].word);
	  return 0;
	}
      }
      //printf("%s\n", comb);
    } while(next_perm(flag, LENGTH));
    for(k = 0;k<count;k++){
      flag[k] = 0;
    }
    for(k=LENGTH-1;k>LENGTH-1-count;k--){
      flag[k] = 1;
    }
    count++;
  }
 

  printf("Not found\n");

}
